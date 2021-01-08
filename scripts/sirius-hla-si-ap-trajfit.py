#!/usr/bin/env python-sirius

"""SI Injection Trajectory Fitting Application."""

import sys
import argparse as _argparse

from siriushla.sirius_application import SiriusApplication

from siriushlafac.si_ap_trajfit import SIFitTrajWindow


parser = _argparse.ArgumentParser(
    description="Run Injection Trajectory Fitting Interface.")
args = parser.parse_args()

app = SiriusApplication()
app.open_window(SIFitTrajWindow, parent=None)
sys.exit(app.exec_())
