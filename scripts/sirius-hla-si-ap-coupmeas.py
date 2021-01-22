#!/usr/bin/env python-sirius

"""SI Injection Trajectory Fitting Application."""

import sys
import argparse as _argparse

from siriushla.sirius_application import SiriusApplication

from siriushlafac.si_ap_coupling_meas import SICoupMeasWindow


parser = _argparse.ArgumentParser(
    description="Run Coupling Measurement Interface.")
args = parser.parse_args()

app = SiriusApplication()
app.open_window(SICoupMeasWindow, parent=None)
sys.exit(app.exec_())
