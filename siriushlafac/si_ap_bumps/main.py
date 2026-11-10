"""SI bumps dialog; communicate with the originating SOFB register via IPC."""

import json

import numpy as np
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QDoubleValidator
from qtpy.QtNetwork import QLocalSocket
from qtpy.QtWidgets import (
    QComboBox, QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton,
)
from siriuspy.clientconfigdb import ConfigDBClient
from siriuspy.sofb.utils import si_calculate_bump
from siriushla.as_ap_configdb import LoadConfigDialog


class SIBumpsWindow(QDialog):
    """Calculate one bump and return it to the register that launched us.

    Protocol: UTF-8 JSON objects, one per line, version 1. Only one request
    is in flight. The parent owns the register and all of its Qt signals.
    No import from the SOFB register module is needed here.
    """

    MAX_BUMP_CURR = 10  # mA
    MAX_MESSAGE = 1024 * 1024
    TIMEOUT_MS = 10000

    def __init__(self, parent=None, register_channel=None):
        super().__init__(parent)
        self.setObjectName('SIApp')
        self.setWindowTitle('SI Bumps')
        self._channel = register_channel
        self._config_type = 'si_orbit'
        self._client = ConfigDBClient(config_type=self._config_type)
        self._pending = None
        self._request_id = 0
        self._buffer = bytearray()
        self._closing = False
        self._nr_bpms = None
        self._parameters = None
        self._build_ui()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._timeout)
        self._socket = QLocalSocket(self)
        self._socket.connected.connect(self._connected)
        self._socket.readyRead.connect(self._receive)
        self._socket.disconnected.connect(self._disconnected)
        error_signal = getattr(self._socket, 'errorOccurred', None)
        if error_signal is None:  # Older Qt 5 bindings.
            error_signal = self._socket.error
        error_signal.connect(self._socket_error)
        QTimer.singleShot(0, self._start)

    def _build_ui(self):
        layout = QGridLayout(self)
        self._base = QComboBox(self)
        self._base.addItems(['Register', 'ref_orb', 'bba_orb', 'other...'])
        self._base.setCurrentIndex(1)
        self._base.activated[int].connect(self._add_entry)
        layout.addWidget(QLabel('Base Orbit', self), 0, 0)
        layout.addWidget(self._base, 0, 1)
        self._section = QComboBox(self)
        self._section.addItems([f'{i:02d}' for i in range(1, 21)])
        self._section.setMaxVisibleItems(7)
        self._section.setStyleSheet('QComboBox{combobox-popup: 0;}')
        layout.addWidget(QLabel('Section', self), 1, 0)
        layout.addWidget(self._section, 1, 1)
        self._subsection = QComboBox(self)
        self._subsection.addItems(['SS', 'C1', 'C2', 'BC'])
        self._subsection.setMaxVisibleItems(5)
        self._subsection.setStyleSheet('QComboBox{combobox-popup: 0;}')
        layout.addWidget(QLabel('Subsection', self), 2, 0)
        layout.addWidget(self._subsection, 2, 1)
        self._entries = []
        for row, label in enumerate(
                ['θ<sub>x</sub> [urad]', 'X [um]',
                 'θ<sub>y</sub> [urad]', 'Y [um]'], start=3):
            entry = QLineEdit('0.0', self)
            entry.setValidator(QDoubleValidator(entry))
            entry.setAlignment(Qt.AlignCenter)
            entry.setStyleSheet('max-width:5em;')
            layout.addWidget(QLabel(label, self), row, 0)
            layout.addWidget(entry, row, 1)
            self._entries.append(entry)
        self._status = QLabel('Connecting to the orbit register...', self)
        self._status.setWordWrap(True)
        layout.addWidget(self._status, 7, 0, 1, 2)
        buttons = QHBoxLayout()
        self._cancel = QPushButton('Cancel', self)
        self._ok = QPushButton('Ok', self)
        self._ok.setDefault(True)
        self._ok.setEnabled(False)
        self._cancel.clicked.connect(self.reject)
        self._ok.clicked.connect(self._submit)
        buttons.addStretch()
        buttons.addWidget(self._cancel)
        buttons.addStretch()
        buttons.addWidget(self._ok)
        buttons.addStretch()
        layout.addLayout(buttons, 8, 0, 1, 2)

    def _start(self):
        if not self._channel:
            self._fatal('Open this application from an SOFB orbit register. '
                        'The --register-channel argument is required.')
            return
        self._timer.start(self.TIMEOUT_MS)
        self._socket.connectToServer(self._channel)

    def _connected(self):
        self._timer.stop()
        self._request('context', {}, self._context_received)

    def _request(self, operation, payload, callback):
        if self._closing:
            return
        if self._pending is not None:
            self._fatal('Another register request is still pending.')
            return
        self._request_id += 1
        self._pending = (self._request_id, operation, callback)
        message = dict(v=1, id=self._request_id, op=operation, **payload)
        data = (json.dumps(message, allow_nan=False) + '\n').encode('utf-8')
        if self._socket.write(data) < 0:
            self._fatal('Could not send the request to the orbit register.')
            return
        self._timer.start(self.TIMEOUT_MS)

    def _receive(self):
        self._buffer.extend(bytes(self._socket.readAll()))
        if len(self._buffer) > self.MAX_MESSAGE:
            self._fatal('Register response exceeds the protocol limit.')
            return
        while b'\n' in self._buffer and not self._closing:
            line, _, rest = self._buffer.partition(b'\n')
            self._buffer = bytearray(rest)
            try:
                reply = json.loads(line.decode('utf-8'))
                if (not isinstance(reply, dict) or reply.get('v') != 1
                        or self._pending is None
                        or reply.get('id') != self._pending[0]):
                    raise ValueError('Unexpected register response.')
                callback = self._pending[2]
                operation = self._pending[1]
                self._pending = None
                self._timer.stop()
                if reply.get('ok') is not True:
                    raise ValueError(reply.get('error', 'Register request failed.'))
                callback(reply)
            except Exception as error:
                self._fatal(str(error))
                return

    def _context_received(self, reply):
        self._nr_bpms = int(reply['nr_bpms'])
        curr = reply['current']
        if curr is None:
            # Original behavior: warn, then allow the calculation to proceed.
            QMessageBox.warning(self, 'Warning', 'Could not read current value.',
                                QMessageBox.Ok)
        elif curr > self.MAX_BUMP_CURR:
            answer = QMessageBox.question(
                self, 'Are you Sure?',
                f'Stored current is above {self.MAX_BUMP_CURR}mA '
                f'({curr:.2f}mA),\nare you sure you want to continue?',
                QMessageBox.Yes, QMessageBox.Cancel)
            if answer != QMessageBox.Yes:
                self.reject()
                return
        if not self._closing:
            self._status.setText('Destination: ' + reply['name'])
            self._ok.setEnabled(True)

    def _add_entry(self, index):
        if not self._base.itemText(index).startswith('other'):
            return
        name, accepted = LoadConfigDialog(self._config_type, self).exec_()
        if not accepted:
            self._base.setCurrentIndex(0)
            return
        self._base.insertItem(index, name)
        self._base.setCurrentIndex(index)

    def _submit(self):
        if self._pending is not None or self._closing:
            return
        try:
            values = []
            for entry in self._entries:
                value, valid = entry.validator().locale().toDouble(entry.text())
                if not entry.hasAcceptableInput() or not valid or not np.isfinite(value):
                    raise ValueError('Enter finite numbers in all four fields.')
                values.append(value)
            agx, psx, agy, psy = values
            section = self._section.currentText()
            sub = self._subsection.currentText()
            if sub == 'SS':
                sub = 'SA'
                if not int(section) % 2:
                    sub = 'SB'
                elif not (int(section) + 1) % 4:
                    sub = 'SP'
            index = self._base.currentIndex()
            if index == self._base.count() - 1:
                return
            name = self._base.currentText()
            self._parameters = (section + sub, name, agx, agy, psx, psy)
            self._ok.setEnabled(False)
            if index == 0:
                self._request('get_orbit', {}, self._calculate)
            else:
                self._calculate(self._client.get_config_value(name))
        except Exception as error:
            self._ok.setEnabled(True)
            QMessageBox.warning(self, 'Bump calculation', str(error))

    def _orbit_arrays(self, data):
        x, y = np.asarray(data['x'], dtype=float), np.asarray(data['y'], dtype=float)
        if (x.shape != (self._nr_bpms,) or y.shape != (self._nr_bpms,)
                or not np.isfinite(x).all() or not np.isfinite(y).all()):
            raise ValueError('Invalid orbit dimensions or non-finite values.')
        return x.copy(), y.copy()

    def _calculate(self, data):
        try:
            x, y = self._orbit_arrays(data)
            location, name, agx, agy, psx, psy = self._parameters
            x, y = si_calculate_bump(x, y, location, agx, agy, psx, psy)
            x, y = self._orbit_arrays({'x': x, 'y': y})
            text = f'Bump@{location}; ref={name}; '
            text += f'ax={agx:.1f} ay={agy:.1f} dx={psx:.1f} dy={psy:.1f}'
            # After sending, cancellation cannot retract an update in flight.
            self._cancel.setEnabled(False)
            self._status.setText('Waiting for the register to confirm the update...')
            self._request('set_orbit', dict(text=text, x=x.tolist(), y=y.tolist()),
                          self._updated)
        except Exception as error:
            self._ok.setEnabled(True)
            self._cancel.setEnabled(True)
            QMessageBox.warning(self, 'Bump calculation', str(error))

    def _updated(self, reply):
        self._closing = True
        self._socket.disconnectFromServer()
        self.accept()

    def _timeout(self):
        self._fatal('Timed out waiting for the orbit register.')

    def _disconnected(self):
        self._fatal('The connection to the orbit register was closed.')

    def _socket_error(self, _error):
        self._fatal(self._socket.errorString())

    def _fatal(self, message):
        if self._closing:
            return
        if self._pending is not None and self._pending[1] == 'set_orbit':
            message += ('\nThe update may already have reached the register. '
                        'Check it in SOFB before trying again.')
        self._closing = True
        self._timer.stop()
        self._socket.abort()
        QMessageBox.warning(self, 'SI Bumps', message)
        super().reject()

    def reject(self):
        if self._pending is not None and self._pending[1] == 'set_orbit':
            return
        self._closing = True
        self._timer.stop()
        self._socket.abort()
        super().reject()

    def closeEvent(self, event):
        if self._pending is not None and self._pending[1] == 'set_orbit':
            event.ignore()
            return
        self.reject()
        event.accept()
