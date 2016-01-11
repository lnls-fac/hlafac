
from PyQt5 import QtWidgets, QtCore
import sys
import epics
import datetime
import time
import collections
import numpy
import lnls
import os
import hlaplot.datetime_plot

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.ip_widget = IPWindow()
        self.ip_widget.button.clicked.connect(self.set_ip)
        self.central_widget.addWidget(self.ip_widget)
        self.setWindowTitle('Top-up Injection')

    def set_ip(self):
        os.environ["EPICS_CA_ADDR_LIST"] = self.ip_widget.ip.text()
        os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "no"
        mywindow_widget = MyWindow()
        self.central_widget.addWidget(mywindow_widget)
        self.central_widget.setCurrentWidget(mywindow_widget)
        self.resize(600,600)


class IPWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        label = QtWidgets.QLabel("Virtual Accelerator IP Address:")
        self.ip = QtWidgets.QLineEdit(" ")
        self.button = QtWidgets.QPushButton('Start')
        self.button.setFixedSize(80,80)
        self.button.setAutoDefault(True)

        hlayout = QtWidgets.QHBoxLayout()
        vlayout1 = QtWidgets.QVBoxLayout()
        vlayout2 = QtWidgets.QVBoxLayout()
        vlayout1.addWidget(label)
        vlayout1.addWidget(self.ip)
        vlayout2.addWidget(self.button)
        hlayout.addLayout(vlayout1)
        hlayout.addSpacing(20)
        hlayout.addLayout(vlayout2)
        self.setLayout(hlayout)
        self.setTabOrder(self.ip, self.button)

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)

        self.set_default_values()

        # Widgets
        title = QtWidgets.QLabel("Top-up Injection")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: bold 15pt")
        parameters_label = QtWidgets.QLabel("Top-up Parameters")
        parameters_label.setStyleSheet("font: bold")
        current_label = QtWidgets.QLabel("Storage Ring Current:")
        current_label.setStyleSheet("font: bold 12pt")
        self.current_value = QtWidgets.QLabel("PV Disconnect")
        self.button = QtWidgets.QPushButton("Start Top-up Injection")
        self.button.setCheckable(True)
        self.button.setFixedWidth(200)
        self.button.toggled.connect(self.button_toggled)
        self.button.setMaximumSize(200, 200)

        # Layout
        mlayout  = QtWidgets.QVBoxLayout()
        vlayout1 = QtWidgets.QVBoxLayout()
        vlayout2 = QtWidgets.QVBoxLayout()
        hlayout1 = QtWidgets.QHBoxLayout()
        hlayout2 = QtWidgets.QHBoxLayout()
        mlayout.addWidget(title)
        mlayout.addSpacing(30)
        vlayout1.addWidget(parameters_label)
        self.max_current = self.add_parameter("Maximum Current:", "%s"%self.max_c, vlayout1,  "mA")
        self.max_decay   = self.add_parameter("Maximum Current Decay:", "%s"%self.max_d, vlayout1, " %")
        self.freq        = self.add_parameter("Frequency:", "%s"%self.f, vlayout1, "Hz")

        self.add_operation_mode_buttons(vlayout1)

        vlayout2.addWidget(self.button)
        hlayout1.addLayout(vlayout1)
        hlayout1.addSpacing(50)
        hlayout1.addLayout(vlayout2)
        mlayout.addLayout(hlayout1)
        mlayout.addSpacing(50)
        hlayout2.addWidget(current_label)
        hlayout2.addWidget(self.current_value)
        hlayout2.addStretch(100)
        mlayout.addLayout(hlayout2)
        self.setLayout(mlayout)

        # PVs
        self.cycle_pv    = epics.PV('VA-LITI-CYCLE')
        self.current_pv  = epics.PV('SIDI-CURRENT')
        self.mode_pv     = epics.PV('VA-LIFK-MODE')
        self.mode_pv.connect(0.1)
        self.update_label()


        # Timer threads
        self.topup_timer = lnls.Timer(self.time_interval, self.check_inject)
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.update_plot_datetime)
        self.current_timer = QtCore.QTimer()
        self.current_timer.timeout.connect(self.update_label)
        self.current_timer.setInterval(1000.0)
        self.current_timer.start()

        # DateTimePlot
        self.plot_datetime = hlaplot.datetime_plot.DateTimePlot()
        mlayout.addWidget(self.plot_datetime)

        self.plot_datetime.x_label = 'Time'
        self.plot_datetime.y_label = 'Current (mA)'
        self.plot_datetime.y_autoscale = False
        self.plot_datetime.y_axis = (0.0, 360.0)
        self.plot_datetime.x_ticks_label_format = '%H:%M:%S'
        self.plot_datetime.x_tick_label_rotation = 0
        self.plot_datetime.datetime_coord_format = '%H:%M:%S'

        delta0 = datetime.timedelta(seconds=0)
        delta1 = datetime.timedelta(seconds=0)
        self.plot_datetime.x_axis_extra_spacing = (delta0, delta1)
        self.plot_datetime.y_axis_extra_spacing = 0.1
        self.plot_datetime.set_ticker('linear', 5)
        self.plot_datetime.interval = datetime.timedelta(seconds=60)
        self.plot_datetime.add_line('line', 1000)

        t0 = datetime.datetime.now() - datetime.timedelta(seconds=360)
        t = [t0 + datetime.timedelta(seconds=i) for i in range(360)]
        y1 = numpy.zeros(len(t))

        self.plot_datetime.line('line').x = t
        self.plot_datetime.line('line').y = y1

        self.update_times = collections.deque(maxlen=100)
        self.last_update = datetime.datetime.now()
        self.plot_timer.start(100)

    def set_default_values(self):
        # Top-up default parameters
        self.max_c = 350 # [mA]
        self.max_d = 0.5 # [%]
        self.f     = 2.0 # [Hz]
        self.time_interval = 2.0 # [s]
        self.is_injecting  = False
        self.stop          = False

    def add_operation_mode_buttons(self, layout):
        mode_label = QtWidgets.QLabel("Operation Mode:")
        self.mode_group = QtWidgets.QButtonGroup()
        self.single_bunch_mode = QtWidgets.QRadioButton("Single-bunch")
        self.multi_bunch_mode = QtWidgets.QRadioButton("Multi-bunch")
        self.single_bunch_mode.clicked.connect(self.single_bunch_button_clicked)
        self.multi_bunch_mode.clicked.connect(self.multi_bunch_button_clicked)
        self.mode_group.addButton(self.single_bunch_mode)
        self.mode_group.addButton(self.multi_bunch_mode)
        hlayout = QtWidgets.QHBoxLayout()
        vlayout = QtWidgets.QVBoxLayout()
        hlayout.addWidget(mode_label)
        vlayout.addWidget(self.single_bunch_mode)
        vlayout.addWidget(self.multi_bunch_mode)
        hlayout.addLayout(vlayout)
        hlayout.addSpacing(50)
        layout.addLayout(hlayout)

    def single_bunch_button_clicked(self):
        if self.mode_pv.connected:
            self.mode_pv.put(1)

    def multi_bunch_button_clicked(self):
        if self.mode_pv.connected:
            self.mode_pv.put(0)

    def update_plot_datetime(self):
        t = datetime.datetime.now()
        if self.current_pv.connected:
            y1 = self.current_pv.get()
        else:
            y1 = 0.0
        self.plot_datetime.line('line').add_xy(t, y1)
        self.plot_datetime.update_plot()

        delta = datetime.datetime.now() - self.last_update
        self.update_times.append(delta)
        sum_seconds = 0
        for t in self.update_times:
            sum_seconds += t.seconds + t.microseconds / 1e6
        fps = len(self.update_times) / sum_seconds
        self.last_update = datetime.datetime.now()


    def add_parameter(self, label, text, layout, units=None):
        label = QtWidgets.QLabel(label)
        wid = QtWidgets.QLineEdit(text)
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(wid)
        if units is not None:
            units_label = QtWidgets.QLabel(units)
            hlayout.addWidget(units_label)
        layout.addLayout(hlayout)
        return wid

    def button_toggled(self):
        if self.button.isChecked():
            if len(self.max_current.text())!= 0: self.max_c = float(self.max_current.text())
            if len(self.max_decay.text())!= 0: self.max_d = float(self.max_decay.text())
            if len(self.freq.text())!= 0: self.f = float(self.freq.text())
            self.min_c = self.max_c * (1.0 - self.max_d/100.0)
            self.cycle_interval = 1.0/self.f
            self.stop = False
            self.max_current.setReadOnly(True)
            self.max_decay.setReadOnly(True)
            self.freq.setReadOnly(True)
            if self.cycle_pv.connected and self.current_pv.connected:
                self.topup_timer.start()
                self.button.setText("Stop Top-up Injection")
            else:
                self.button.setText("  PV Disconnected    ")
        else:
            self.stop = True
            self.max_current.setReadOnly(False)
            self.max_decay.setReadOnly(False)
            self.freq.setReadOnly(False)

            if self.topup_timer.is_running:
                self.topup_timer.stop()
            self.button.setText("Start Top-up Injection")

    def update_label(self):
        if self.mode_pv.connected:
            self.single_bunch_mode.setEnabled(1)
            self.multi_bunch_mode.setEnabled(1)
            value = self.mode_pv.get()
            if value == 1:
                self.single_bunch_mode.setChecked(1)
            else:
                self.multi_bunch_mode.setChecked(1)
        else:
            self.single_bunch_mode.setDisabled(1)
            self.multi_bunch_mode.setDisabled(1)
        if self.current_pv.connected:
            value = self.current_pv.get()
            self.current_value.setText("%3.5f mA"%value)
        else:
            self.current_value.setText("PV Disconnected")

    def check_inject(self):
        if self.is_injecting: return
        if not self.current_pv.connected:return
        while self.current_pv.get() < self.min_c and not self.stop:
            self.is_injecting = True
            while self.current_pv.get() < self.max_c and not self.stop:
                self.cycle()
        self.is_injecting = False

    def cycle(self):
        """Cycle injection"""
        if self.cycle_pv.connected:
            t0 = time.time()
            self.cycle_pv.put(1)
            t1 = time.time()
            while t1 < t0 + self.cycle_interval:
                time.sleep(self.cycle_interval-(t1-t0))
                t1 = time.time()

def exec_(app):
    result = app.exec_()
    epics.ca.finalize_libca()
    return result

if __name__ == '__main__':
    epics.ca.initialize_libca()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(exec_(app))
