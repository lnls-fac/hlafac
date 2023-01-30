"""Main module of the Application Interface."""
import os as _os
import logging as _log
from threading import Thread
import pathlib as _pathlib

import matplotlib.pyplot as mplt
import matplotlib.gridspec as mgs
from matplotlib import rcParams

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QPushButton, QGridLayout, QSpinBox, \
    QLabel, QGroupBox, QDoubleSpinBox, QComboBox, QHBoxLayout, QFileDialog, \
    QVBoxLayout

import qtawesome as qta

# from pydm.widgets.logdisplay import PyDMLogDisplay

from siriuspy.envars import VACA_PREFIX
from siriuspy.namesys import SiriusPVName
from siriushla import util
from siriushla.widgets import MatplotlibWidget, SiriusMainWindow, \
    SiriusLogDisplay, SiriusSpinbox, SiriusLabel

from apsuite.commisslib.meas_coupling_tune import MeasCoupling

rcParams.update({
    'font.size': 12, 'axes.grid': True, 'grid.linestyle': '--',
    'grid.alpha': 0.5})


class SICoupMeasWindow(SiriusMainWindow):
    """."""

    EXT = 'pickle'
    EXT_FLT = f'Pickle Files (*.{EXT:s})'
    DEFAULT_DIR = _pathlib.Path.home().as_posix()
    DEFAULT_DIR += _os.path.sep + _os.path.join(
        'shared', 'screens-iocs', 'data_by_day')
    print(DEFAULT_DIR)

    def __init__(self, parent=None):
        """."""
        super().__init__(parent=parent)
        self.meas_coup = MeasCoupling()
        self._last_dir = self.DEFAULT_DIR

        self.setupui()
        self.setObjectName('SIApp')
        color = util.get_appropriate_color('SI')
        icon = qta.icon('mdi.notebook', 'mdi.pulse', options=[
            dict(scale_factor=0.5, color=color, offset=(0.2, -0.3)),
            dict(scale_factor=1, color=color, offset=(0, 0.0))])
        self.setWindowIcon(icon)
        self.resize(1100, 700)

    def setupui(self):
        """."""
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("SI - Coupling Measurement")
        self.setDocumentMode(False)
        self.setDockNestingEnabled(True)

        mwid = self._create_central_widget()
        self.setCentralWidget(mwid)

    def _create_central_widget(self):
        wid = QWidget(self)
        wid.setLayout(QGridLayout())

        wid.layout().addWidget(
            QLabel(f'<h1>SI - Coupling Measurement </h1>', wid),
            0, 0, 1, 2, alignment=Qt.AlignCenter)

        fig_wid = self.make_figure(wid)
        ctrls = self.get_param_control_widget(wid)
        status = self.get_measurement_status_widget(wid)
        anly = self.get_analysis_control_widget(wid)
        apply = self.get_adjust_coupling_widget(wid)
        saveload = self.get_saveload_widget(wid)

        wid.layout().addWidget(ctrls, 1, 0)
        wid.layout().addWidget(status, 2, 0)
        wid.layout().addWidget(anly, 3, 0)
        wid.layout().addWidget(apply, 4, 0)
        lay = QVBoxLayout()
        lay.addWidget(saveload)
        lay.addWidget(fig_wid)
        wid.layout().addLayout(lay, 1, 1, 4, 1)
        wid.layout().setRowStretch(2, 10)
        return wid

    def make_figure(self, parent):
        """."""
        self.fig = mplt.figure(figsize=(7, 14))
        fig_widget = MatplotlibWidget(self.fig, parent=parent)

        gs = mgs.GridSpec(1, 1)
        gs.update(
            left=0.145, right=0.95, bottom=0.13, top=0.9,
            hspace=0.5, wspace=0.35)
        self.axes = self.fig.add_subplot(gs[0, 0])

        self.axes.set_xlabel('Current [A]')
        self.axes.set_ylabel('Transverse Tunes')
        self.axes.set_title(
            'Transverse Linear Coupling: ({:.2f} ± {:.2f}) %'.format(0, 0),
            fontsize='x-large')

        # plot meas data
        self.line_tune1 = self.axes.plot([], [], 'o', color='C0')[0]
        self.line_tune2 = self.axes.plot([], [], 'o', color='C1')[0]

        # plot fitting
        self.line_fit1 = self.axes.plot([], [], color='tab:gray')[0]
        self.line_fit2 = self.axes.plot([], [], color='tab:gray')[0]

        self.line_exptune1 = self.axes.plot(
            [], [], 'o--', color='C0', alpha=0.75)[0]
        self.line_exptune2 = self.axes.plot(
            [], [], 'o--', color='C1', alpha=0.75)[0]
        self.line_exptune1.set_label(r'expected $\nu_1$')
        self.line_exptune2.set_label(r'expected $\nu_2$')
        self.axes.legend(loc='best')
        return fig_widget

    def get_param_control_widget(self, parent):
        """."""
        wid = QGroupBox('Measurement Control', parent)
        wid.setLayout(QGridLayout())

        self.wid_quadfam = QComboBox(wid)
        self.wid_quadfam.addItems(self.meas_coup.params.QUADS)
        self.wid_quadfam.setCurrentText(self.meas_coup.params.quadfam_name)
        self.wid_quadfam.currentTextChanged.connect(self._update_quadcurr_wid)

        self._currpvname = SiriusPVName(
            'SI-Fam:PS-'+self.meas_coup.params.quadfam_name+':Current-SP')
        self._currpvname = self._currpvname.substitute(prefix=VACA_PREFIX)
        self.wid_quadcurr_sp = SiriusSpinbox(self, self._currpvname)
        self.wid_quadcurr_sp.showStepExponent = False
        self.wid_quadcurr_mn = SiriusLabel(
            self, self._currpvname.substitute(propty_suffix='Mon'))
        self.wid_quadcurr_mn.showUnits = True

        self.wid_nr_points = QSpinBox(wid)
        self.wid_nr_points.setValue(self.meas_coup.params.nr_points)

        self.wid_time_wait = QDoubleSpinBox(wid)
        self.wid_time_wait.setValue(self.meas_coup.params.time_wait)
        self.wid_time_wait.setMinimum(0)
        self.wid_time_wait.setMaximum(20)
        self.wid_time_wait.setDecimals(1)
        self.wid_time_wait.setSingleStep(0.1)

        self.wid_lower_percent = QDoubleSpinBox(wid)
        self.wid_lower_percent.valueChanged.connect(
            self._calc_expected_dtunes)
        self.wid_lower_percent.setValue(
            self.meas_coup.params.lower_percent*100)
        self.wid_lower_percent.setMinimum(-3.0)
        self.wid_lower_percent.setMaximum(+3.0)
        self.wid_lower_percent.setDecimals(2)
        self.wid_lower_percent.setSingleStep(0.01)

        self.wid_upper_percent = QDoubleSpinBox(wid)
        self.wid_upper_percent.valueChanged.connect(
            self._calc_expected_dtunes)
        self.wid_upper_percent.setValue(
            self.meas_coup.params.upper_percent*100)
        self.wid_upper_percent.setMinimum(-3.0)
        self.wid_upper_percent.setMaximum(+3.0)
        self.wid_upper_percent.setDecimals(2)
        self.wid_upper_percent.setSingleStep(0.01)

        pusb_start = QPushButton(qta.icon('mdi.play'), 'Start', wid)
        pusb_start.clicked.connect(self.start_meas)
        pusb_stop = QPushButton(qta.icon('mdi.stop'), 'Stop', wid)
        pusb_stop.clicked.connect(self.meas_coup.stop)

        lab_name = QLabel('Fam. Name', wid)
        lab_curr = QLabel('', wid)
        lab_curr.setPixmap(qta.icon('ei.arrow-right').pixmap(16, 16))
        lab_nrpt = QLabel('Nr. of Points', wid)
        lab_wait = QLabel('Wait time [s]', wid)
        lab_lowe = QLabel('Lower Lim. [%]', wid)
        lab_uppe = QLabel('Upper Lim. [%]', wid)

        wid.layout().addWidget(lab_name, 1, 1, alignment=Qt.AlignRight)
        wid.layout().addWidget(self.wid_quadfam, 1, 2)
        lay = QHBoxLayout()
        lay.addWidget(lab_curr)
        lay.addWidget(self.wid_quadcurr_sp)
        wid.layout().addLayout(lay, 1, 3)
        wid.layout().addWidget(self.wid_quadcurr_mn, 1, 4)
        wid.layout().addWidget(lab_lowe, 2, 1, alignment=Qt.AlignRight)
        wid.layout().addWidget(self.wid_lower_percent, 2, 2)
        wid.layout().addWidget(lab_uppe, 2, 3, alignment=Qt.AlignRight)
        wid.layout().addWidget(self.wid_upper_percent, 2, 4)
        wid.layout().addWidget(lab_nrpt, 3, 1, alignment=Qt.AlignRight)
        wid.layout().addWidget(self.wid_nr_points, 3, 2)
        wid.layout().addWidget(lab_wait, 3, 3, alignment=Qt.AlignRight)
        wid.layout().addWidget(self.wid_time_wait, 3, 4)
        lay = QHBoxLayout()
        lay.addStretch()
        lay.addWidget(pusb_start)
        lay.addStretch()
        lay.addWidget(pusb_stop)
        lay.addStretch()
        wid.layout().addLayout(lay, 4, 1, 1, 4)
        wid.layout().setColumnStretch(0, 2)
        wid.layout().setColumnStretch(6, 2)
        return wid

    def get_measurement_status_widget(self, parent):
        """."""
        wid = QGroupBox('Measurement Status', parent)
        wid.setLayout(QGridLayout())

        self.log_label = SiriusLogDisplay(wid, level=_log.INFO)
        self.log_label.logFormat = '%(message)s'
        wid.layout().addWidget(self.log_label, 0, 0)
        return wid

    def get_analysis_control_widget(self, parent):
        """."""
        wid = QGroupBox('Analysis Control', parent)
        wid.setLayout(QGridLayout())
        self.wid_coupling_resolution = QDoubleSpinBox(wid)
        self.wid_coupling_resolution.setValue(
            self.meas_coup.params.coupling_resolution*100)
        self.wid_coupling_resolution.setMinimum(0.0)
        self.wid_coupling_resolution.setDecimals(2)
        self.wid_coupling_resolution.setSingleStep(0.01)
        self.wid_coupling_resolution.setStyleSheet('max-width:5em;')

        pusb_proc = QPushButton(qta.icon('mdi.chart-line'), 'Process', wid)
        pusb_proc.clicked.connect(self._plot_results)

        wid.layout().addWidget(QLabel('Coupling Resolution [%]', wid), 0, 0)
        wid.layout().addWidget(self.wid_coupling_resolution, 0, 1)
        wid.layout().addWidget(pusb_proc, 0, 3)
        wid.layout().setColumnStretch(2, 5)
        return wid

    def get_adjust_coupling_widget(self, parent):
        """."""
        wid = QGroupBox('Apply Achromatic ΔKsL', parent)
        wid.setLayout(QGridLayout())
        self.wid_apply_factor = QDoubleSpinBox(wid)
        self.wid_apply_factor.setValue(self.meas_coup.apply_factor)
        self.wid_apply_factor.setMinimum(-2.0)
        self.wid_apply_factor.setMaximum(2.0)
        self.wid_apply_factor.setDecimals(1)
        self.wid_apply_factor.setSingleStep(0.1)
        self.wid_apply_factor.setStyleSheet('max-width:5em;')

        pusb_updt = QPushButton(qta.icon('fa.refresh'), 'Update Ref.', wid)
        pusb_updt.clicked.connect(self._update_reference)

        pusb_proc = QPushButton(qta.icon('ei.arrow-down'), 'Apply', wid)
        pusb_proc.clicked.connect(self._apply_skews)

        wid_factor_label = QLabel('(1:1 to coupling [%])', wid)
        tooltip = 'The relation between multiplicative factor on the left '
        tooltip += 'and ΔCoupling [%] is roughly 1:1'
        wid_factor_label.setToolTip(tooltip)
        wid.layout().addWidget(self.wid_apply_factor, 0, 0)
        wid.layout().addWidget(wid_factor_label, 0, 1)
        wid.layout().addWidget(pusb_updt, 0, 3)
        wid.layout().addWidget(pusb_proc, 0, 4)
        wid.layout().setColumnStretch(2, 5)
        return wid

    def get_saveload_widget(self, parent):
        """."""
        svld_wid = QGroupBox('Save and Load', parent)
        svld_lay = QGridLayout(svld_wid)

        pbld = QPushButton('Load', svld_wid)
        pbld.setIcon(qta.icon('mdi.file-upload-outline'))
        pbld.setToolTip('Load data from file')
        pbld.clicked.connect(self._load_data_from_file)

        pbsv = QPushButton('Save', svld_wid)
        pbsv.setIcon(qta.icon('mdi.file-download-outline'))
        pbsv.setToolTip('Save data to file')
        pbsv.clicked.connect(self._save_data_to_file)
        self.loaded_label = QLabel('', svld_wid)
        self.loaded_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        svld_lay.addWidget(pbsv, 0, 0)
        svld_lay.addWidget(pbld, 1, 0)
        svld_lay.addWidget(self.loaded_label, 0, 1, 2, 1)
        svld_lay.setColumnStretch(1, 2)
        return svld_wid

    def _save_data_to_file(self, _):
        filename = QFileDialog.getSaveFileName(
            caption='Define a File Name to Save Data',
            directory=self._last_dir,
            filter=self.EXT_FLT)
        fname = filename[0]
        if not fname:
            return
        self._last_dir, _ = _os.path.split(fname)
        self.loaded_label.setText('')
        fname += '' if fname.endswith(self.EXT) else ('.' + self.EXT)
        self.meas_coup.save_data(fname, overwrite=True)

    def _load_data_from_file(self):
        filename = QFileDialog.getOpenFileName(
            caption='Select a Coupling Data File.',
            directory=self._last_dir,
            filter=self.EXT_FLT)
        fname = filename[0]
        if not fname:
            return
        self._last_dir, _ = _os.path.split(fname)

        self.meas_coup.load_and_apply_old_data(fname)
        splitted = fname.split('/')
        stn = splitted[0]
        leng = len(stn)
        for s in splitted[1:]:
            if leng + len(s) > 90:
                stn += '/\n' + s
                leng = len(s)
            else:
                stn += '/' + s
                leng += len(s)
        self.loaded_label.setText('File Loaded: \n' + stn)

        self.wid_quadfam.setCurrentIndex(
            self.meas_coup.params.QUADS.index(
                self.meas_coup.params.quadfam_name))
        self.wid_nr_points.setValue(self.meas_coup.params.nr_points)
        self.wid_time_wait.setValue(self.meas_coup.params.time_wait)
        self.wid_lower_percent.setValue(
            self.meas_coup.params.lower_percent*100)
        self.wid_upper_percent.setValue(
            self.meas_coup.params.upper_percent*100)
        self.wid_coupling_resolution.setValue(
            self.meas_coup.params.coupling_resolution*100)
        self._plot_results()

    def start_meas(self):
        """."""
        if self.meas_coup.ismeasuring:
            _log.error('There is another measurement happening.')
            return
        Thread(target=self._do_meas, daemon=True).start()

    def _do_meas(self):
        self.meas_coup.params.quadfam_name = self.wid_quadfam.currentText()
        self.meas_coup.params.nr_points = int(self.wid_nr_points.value())
        self.meas_coup.params.time_wait = float(self.wid_time_wait.value())
        self.meas_coup.params.lower_percent = float(
            self.wid_lower_percent.value()) / 100
        self.meas_coup.params.upper_percent = float(
            self.wid_upper_percent.value()) / 100

        self.loaded_label.setText('')

        self.meas_coup.wait_for_connection()
        self.meas_coup.start()
        self.meas_coup.wait_measurement()
        self._plot_results()

    def _process_data(self):
        try:
            self.meas_coup.process_data()
        except Exception as err:
            _log.error('Problem processing data.')
            _log.error(str(err))

    def _plot_results(self):
        self.line_exptune1.set_visible(False)
        self.line_exptune2.set_visible(False)
        self.line_exptune1.set_label('_nolegend_')
        self.line_exptune2.set_label('_nolegend_')

        self.meas_coup.params.coupling_resolution = float(
            self.wid_coupling_resolution.value()) / 100
        self._process_data()
        anl = self.meas_coup.analysis
        if 'qcurr' not in anl:
            _log.error('There is no data to plot.')
            return
        qcurr, tune1, tune2 = anl['qcurr'], anl['tune1'], anl['tune2']
        self.line_tune1.set_xdata(qcurr)
        self.line_tune2.set_xdata(qcurr)
        self.line_tune1.set_ydata(tune1)
        self.line_tune2.set_ydata(tune2)
        self.axes.set_xlabel(f'{self.meas_coup.data["qname"]} Current [A]')

        if 'fitted_param' in anl:
            fit_vec = anl['fitted_param']['x']
            fittune1, fittune2, qcurr_interp = self.meas_coup.get_normal_modes(
                params=fit_vec, curr=qcurr, oversampling=10)

            self.line_fit1.set_xdata(qcurr_interp)
            self.line_fit2.set_xdata(qcurr_interp)
            self.line_fit1.set_ydata(fittune1)
            self.line_fit2.set_ydata(fittune2)
            self.axes.set_title(
                'Transverse Linear Coupling: ({:.2f} ± {:.2f}) %'.format(
                    fit_vec[-1]*100, anl['fitting_error'][-1] * 100))
        else:
            self.line_fit1.set_xdata([])
            self.line_fit2.set_xdata([])
            self.line_tune1.set_ydata([])
            self.line_tune2.set_ydata([])
            self.axes.set_title('Transverse Linear Coupling: (Nan ± Nan) %')

        self.line_tune1.set_label(r'$\nu_1$')
        self.line_tune2.set_label(r'$\nu_2$')
        self.line_fit1.set_label('fitting')
        self.axes.legend(loc='best')
        self.axes.relim(visible_only=True)
        self.axes.autoscale_view()
        self.fig.canvas.draw()

    def _apply_skews(self):
        self.meas_coup.apply_factor = float(
            self.wid_apply_factor.value())
        self.meas_coup.apply_achromatic_delta_ksl()

    def _update_reference(self):
        self.meas_coup.initial_strengths = None

    def _update_quadcurr_wid(self, text):
        self._currpvname = self._currpvname.substitute(dev=text)
        self.wid_quadcurr_sp.channel = self._currpvname
        self.wid_quadcurr_mn.channel = self._currpvname.substitute(
            propty_suffix='Mon')

    def _calc_expected_dtunes(self):
        try:
            dcurr_low = float(self.wid_lower_percent.value())/100
            dcurr_upp = float(self.wid_upper_percent.value())/100
            quad_fam = str(self.wid_quadfam.currentText())
            rel_dnux, rel_dnuy = self.meas_coup.REL_DELTATUNE_QUADFAM[quad_fam]
            self.dnux_low = rel_dnux * dcurr_low
            self.dnuy_low = rel_dnuy * dcurr_low
            self.dnux_upp = rel_dnux * dcurr_upp
            self.dnuy_upp = rel_dnuy * dcurr_upp
        except AttributeError:
            self.dnux_low = 0
            self.dnuy_low = 0
            self.dnux_upp = 0
            self.dnuy_upp = 0
        self._plot_expected()

    def _plot_expected(self):

        if len(self.line_fit1.get_xdata()) > 0:
            self.line_tune1.set_label(r'$\nu_1$')
            self.line_tune2.set_label(r'$\nu_2$')
            self.line_fit1.set_label('fitting')

        curr0 = float(self.wid_quadcurr_sp.value())
        dcurr_low = float(self.wid_lower_percent.value())/100
        dcurr_upp = float(self.wid_upper_percent.value())/100
        xaxis = [curr0*(1+dcurr_low), curr0*(1+dcurr_upp)]
        tune_dev = self.meas_coup.devices['tune']
        nux0, nuy0 = tune_dev.tunex, tune_dev.tuney
        self.line_exptune1.set_xdata(xaxis)
        self.line_exptune1.set_ydata(
            [nuy0 + self.dnuy_low, nuy0 + self.dnuy_upp])
        self.line_exptune2.set_xdata(xaxis)
        self.line_exptune2.set_ydata(
            [nux0 + self.dnux_low, nux0 + self.dnux_upp])

        self.line_exptune1.set_visible(True)
        self.line_exptune2.set_visible(True)
        self.line_exptune1.set_label(r'expected $\nu_1$')
        self.line_exptune2.set_label(r'expected $\nu_2$')

        self.axes.legend(loc='best')
        self.axes.relim(visible_only=True)
        self.axes.autoscale_view()
        self.fig.canvas.draw()
