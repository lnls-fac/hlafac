"""Main module of the Application Interface."""

import numpy as np
import matplotlib.pyplot as mplt
import matplotlib.gridspec as mgs
from matplotlib import rcParams

from qtpy.QtCore import Qt
from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QWidget, QPushButton, QGridLayout, QSpinBox, \
    QDoubleSpinBox, QLabel, QGroupBox, QLineEdit

import qtawesome as qta

from siriuspy.sofb.csdev import SOFBFactory
from siriushla import util
from siriushla.widgets import MatplotlibWidget, SiriusMainWindow

from apsuite.commissioning_scripts.inj_traj_fitting import SIFitInjTraj, \
    BOFitInjTraj
from apsuite.optics_analysis import TuneCorr

rcParams.update({
    'font.size': 12, 'axes.grid': True, 'grid.linestyle': '--',
    'grid.alpha': 0.5})


class ASFitTrajWindow(SiriusMainWindow):
    """."""

    def __init__(self, acc='SI', parent=None):
        """."""
        super().__init__(parent=parent)
        acc = acc.upper()
        self._csorb = SOFBFactory.create(acc)
        if acc == 'SI':
            self.fit_traj = SIFitInjTraj()
        else:
            self.fit_traj = BOFitInjTraj()
        self.tunecorr = TuneCorr(
            self.fit_traj.model, acc, method='Proportional',
            grouping='TwoKnobs')

        self.setupui()
        self.setObjectName(acc+'App')
        color = util.get_appropriate_color(acc)
        icon = qta.icon('mdi.calculator-variant', 'mdi.chart-line', options=[
            dict(scale_factor=0.4, color=color, offset=(0.1, -0.3)),
            dict(scale_factor=1, color=color, offset=(0, 0.0))])
        self.setWindowIcon(icon)

    def setupui(self):
        """."""
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(self._csorb.acc+" - Trajectory Fitting")
        self.setDocumentMode(False)
        self.setDockNestingEnabled(True)

        mwid = self._create_central_widget()
        self.setCentralWidget(mwid)

    def _create_central_widget(self):
        wid = QWidget(self)
        wid.setLayout(QGridLayout())

        wid.layout().addWidget(
            QLabel(f'<h1> {self._csorb.acc} - Fit Trajectory </h1>', wid),
            0, 0, 1, 2, alignment=Qt.AlignCenter)

        fig_wid = self.make_figure(wid)
        wid.layout().addWidget(fig_wid, 1, 0, 5, 1)

        tune = self.get_tune_fit_widget(wid)
        wid.layout().addWidget(tune, 1, 1)

        ctrls = self.get_param_control_widget(wid)
        wid.layout().addWidget(ctrls, 3, 1)

        results = self.get_results_widget(wid)
        wid.layout().addWidget(results, 5, 1)

        wid.layout().setRowStretch(2, 2)
        wid.layout().setRowStretch(4, 2)
        return wid

    def make_figure(self, parent):
        """."""
        self.fig = mplt.figure(figsize=(7, 14))
        fig_widget = MatplotlibWidget(self.fig, parent=parent)

        gs = mgs.GridSpec(3, 1)
        gs.update(left=0.15, right=0.98, top=0.94, bottom=0.1, hspace=0.35)
        self.axes_x = self.fig.add_subplot(gs[0, 0])
        self.axes_y = self.fig.add_subplot(gs[1, 0], sharex=self.axes_x)
        self.axes_s = self.fig.add_subplot(gs[2, 0], sharex=self.axes_y)

        bpmpos = self.fit_traj.twiss.spos[self.fit_traj.bpm_idx]
        zer = np.zeros(bpmpos.size)
        self.line_measx = self.axes_x.plot(
            bpmpos, zer, '-d', label='Trajectory')[0]
        self.line_measy = self.axes_y.plot(
            bpmpos, zer, '-d', label='Trajectory')[0]
        self.line_meass = self.axes_s.plot(bpmpos, zer, '-k')[0]
        self.line_fitx = self.axes_x.plot(
            bpmpos, zer, '-o', label='Fitting', linewidth=1)[0]
        self.line_fity = self.axes_y.plot(
            bpmpos, zer, '-o', label='Fitting', linewidth=1)[0]
        self.axes_x.set_title(
            r"$x_0$ = {:.3f}mm   $x_0'$ = {:.3f}mrad".format(0.0, 0.0) +
            r"   $\delta$ = {:.2f}%".format(0.0))
        self.axes_y.set_title(
            r"$y_0$ = {:.3f}mm   $y_0'$ = {:.3f}mrad".format(0.0, 0.0))
        self.axes_y.legend(
            loc='upper center', bbox_to_anchor=(0.5, -0.05), fontsize='small',
            ncol=2)
        self.axes_s.set_xlabel('Position [m]')
        self.axes_x.set_ylabel('X [mm]')
        self.axes_y.set_ylabel('Y [mm]')
        self.axes_s.set_ylabel('Sum [counts]')
        [label.set_visible(False) for label in self.axes_x.get_xticklabels()]
        [label.set_visible(False) for label in self.axes_y.get_xticklabels()]
        return fig_widget

    def get_tune_fit_widget(self, parent):
        """."""
        wid = QGroupBox('Model Tune Adjustment', parent)
        wid.setLayout(QGridLayout())

        self.wid_nux = QDoubleSpinBox(wid)
        self.wid_nuy = QDoubleSpinBox(wid)
        self.lab_tune = QLabel(wid)
        pusb = QPushButton('Adjust Model Tune', wid)
        pusb.clicked.connect(self._adjust_tune)

        if self._csorb.acc == 'SI':
            self.wid_nux.setValue(49.09)
            self.wid_nuy.setValue(14.15)
        else:
            self.wid_nux.setValue(19.204)
            self.wid_nuy.setValue(7.314)
        self.wid_nux.setSingleStep(0.001)
        self.wid_nuy.setSingleStep(0.001)
        self.wid_nux.setDecimals(4)
        self.wid_nuy.setDecimals(4)

        wid.layout().addWidget(QLabel('\u03bd<sub>x</sub>', wid), 1, 0)
        wid.layout().addWidget(QLabel('\u03bd<sub>y</sub>', wid), 2, 0)
        wid.layout().addWidget(self.wid_nux, 1, 1)
        wid.layout().addWidget(self.wid_nuy, 2, 1)
        wid.layout().addWidget(pusb, 3, 0, 1, 2)
        wid.layout().addWidget(self.lab_tune, 4, 0, 1, 2)
        return wid

    def get_param_control_widget(self, parent):
        """."""
        wid = QGroupBox('Fitting Control', parent)
        wid.setLayout(QGridLayout())

        self.wid_nr_iter = QSpinBox(wid)
        self.wid_tol = QLineEdit('100', wid)
        self.wid_thres = QLineEdit('10.0', wid)
        self.lab_fitting = QLabel(wid)
        pusb = QPushButton('Fit Trajectory', wid)
        pusb.clicked.connect(self._do_fitting)

        self.wid_nr_iter.setValue(10)
        self.wid_tol.setValidator(QDoubleValidator())
        self.wid_thres.setValidator(QDoubleValidator())

        wid.layout().addWidget(QLabel('# Iterations', wid), 1, 0)
        wid.layout().addWidget(QLabel('Tolerance [um]', wid), 2, 0)
        wid.layout().addWidget(QLabel('Min BPM Sum [%]', wid), 3, 0)
        wid.layout().addWidget(self.wid_nr_iter, 1, 1)
        wid.layout().addWidget(self.wid_tol, 2, 1)
        wid.layout().addWidget(self.wid_thres, 3, 1)
        wid.layout().addWidget(pusb, 4, 0, 1, 2)
        wid.layout().addWidget(self.lab_fitting, 5, 0, 1, 2)
        return wid

    def get_results_widget(self, parent):
        """."""
        wid = QGroupBox('Fitting Results', parent)
        wid.setLayout(QGridLayout())

        self.wid_x0 = QLabel('0.000', wid)
        self.wid_xl0 = QLabel('0.000', wid)
        self.wid_y0 = QLabel('0.000', wid)
        self.wid_yl0 = QLabel('0.000', wid)
        self.wid_en0 = QLabel('0.000', wid)
        self.wid_res = QLabel('0.000', wid)
        self.wid_unreliable = QLabel('Warning: Unreliable Fitting!', wid)
        self.wid_unreliable.setStyleSheet('color:red; font-weight:bold;')
        self.wid_unreliable.setVisible(False)
        self.wid_unre_reason = QLabel('', wid)
        self.wid_unre_reason.setStyleSheet('color:red;')
        self.wid_unre_reason.setVisible(False)
        wid.layout().addWidget(QLabel('x<sub>0</sub> [mm]', wid), 1, 0)
        wid.layout().addWidget(QLabel("x'<sub>0</sub> [mm]", wid), 2, 0)
        wid.layout().addWidget(QLabel('y<sub>0</sub> [mm]', wid), 3, 0)
        wid.layout().addWidget(QLabel("y'<sub>0</sub> [mm]", wid), 4, 0)
        wid.layout().addWidget(QLabel('\u03b4<sub>0</sub> [%]', wid), 5, 0)
        wid.layout().addWidget(QLabel('\u03c7 [\u03bcm]', wid), 6, 0)
        wid.layout().addWidget(self.wid_x0, 1, 1)
        wid.layout().addWidget(self.wid_xl0, 2, 1)
        wid.layout().addWidget(self.wid_y0, 3, 1)
        wid.layout().addWidget(self.wid_yl0, 4, 1)
        wid.layout().addWidget(self.wid_en0, 5, 1)
        wid.layout().addWidget(self.wid_res, 6, 1)
        wid.layout().addWidget(self.wid_unreliable, 7, 0, 1, 2)
        wid.layout().addWidget(self.wid_unre_reason, 8, 0, 1, 2)
        return wid

    def _adjust_tune(self):
        tunex_goal = float(self.wid_nux.value())
        tuney_goal = float(self.wid_nuy.value())

        self.tunecorr.get_tunes(self.fit_traj.model)
        tunemat = self.tunecorr.calc_jacobian_matrix()
        self.tunecorr.correct_parameters(
            model=self.fit_traj.model,
            goal_parameters=np.array([tunex_goal, tuney_goal]),
            jacobian_matrix=tunemat)

        self.lab_tune.setText('Done!')

    def _do_fitting(self):
        trjx, trjy, trjs = self.fit_traj.get_traj_from_sofb()
        # trjx, trjy, trjs = self.fit_traj.simulate_sofb(
        #     -8.2e-3, 0.1e-3, y0=0.4e-3, yl0=0, delta=0.002,
        #     errx=0.5e-3, erry=0.3e-3)

        tol = float(self.wid_tol.text()) * 1e-6
        max_iter = self.wid_nr_iter.value()
        self.fit_traj.params.count_rel_thres = float(self.wid_thres.text())/100
        vecs, _, chis = self.fit_traj.do_fitting(
            trjx, trjy, tol=tol, max_iter=max_iter, full=True)
        x, xl, y, yl, de = vecs[-1]
        chi = chis[-1]

        self.wid_x0.setText(f'{x*1e3:.3f}')
        self.wid_xl0.setText(f'{xl*1e3:.3f}')
        self.wid_y0.setText(f'{y*1e3:.3f}')
        self.wid_yl0.setText(f'{yl*1e3:.3f}')
        self.wid_en0.setText(f'{de*1e2:.3f}')
        self.wid_res.setText(f'{chi*1e6:.1f}')
        self.axes_x.set_title(
            r"$x_0$ = {:.3f}mm   $x_0'$ = {:.3f}mrad".format(x*1e3, xl*1e3) +
            r"   $\delta$ = {:.2f}%".format(de*100))
        self.axes_y.set_title(
            r"$y_0$ = {:.3f}mm   $y_0'$ = {:.3f}mrad".format(y*1e3, yl*1e3))

        self.lab_fitting.setText('Calculating Trajectory...')

        trjx_fit, trjy_fit = self.fit_traj.calc_traj(*vecs[-1], size=trjx.size)
        bpmpos = self.fit_traj.twiss.spos[self.fit_traj.bpm_idx]
        bpmpos = bpmpos[:trjx.size]

        self.line_measx.set_xdata(bpmpos)
        self.line_measy.set_xdata(bpmpos)
        self.line_meass.set_xdata(bpmpos)
        self.line_fitx.set_xdata(bpmpos)
        self.line_fity.set_xdata(bpmpos)
        self.line_measx.set_ydata(trjx*1e3)
        self.line_measy.set_ydata(trjy*1e3)
        self.line_meass.set_ydata(trjs)
        self.line_fitx.set_ydata(trjx_fit*1e3)
        self.line_fity.set_ydata(trjy_fit*1e3)
        self.axes_x.relim()
        self.axes_y.relim()
        self.axes_s.relim()
        self.axes_x.autoscale_view()
        self.axes_y.autoscale_view()
        self.axes_s.autoscale_view()
        self.fig.canvas.draw()

        self.lab_fitting.setText('Done!')

        unre_fit = self.fit_traj.unreliable_fitting()
        self.wid_unreliable.setVisible(bool(unre_fit))
        self.wid_unre_reason.setVisible(bool(unre_fit))
        self.wid_unre_reason.setText(unre_fit)
