#!/usr/bin/env python-sirius

"""SI Injection Trajectory Fitting Application."""

import sys
import argparse as _argparse

from siriushla.sirius_application import SiriusApplication

from siriushlafac.as_ap_trajfit import ASFitTrajWindow


parser = _argparse.ArgumentParser(
    description="Run Injection Trajectory Fitting Interface.")
args = parser.parse_args()

app = SiriusApplication()
app.open_window(ASFitTrajWindow, acc='SI', parent=None)
sys.exit(app.exec_())
