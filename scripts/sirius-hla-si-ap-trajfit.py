#!/usr/bin/env python-sirius

"""SI Injection Trajectory Fitting Application."""

import sys
import argparse as _argparse

from siriushla.sirius_application import SiriusApplication
from siriuspy.envars import VACA_PREFIX

from siriushlafac.si_ap_trajfit import MainWindow


parser = _argparse.ArgumentParser(
    description="Run Injection Trajectory Fitting Interface.")
parser.add_argument(
    '-p', "--prefix", type=str, default=VACA_PREFIX,
    help="Define the prefix for the PVs in the window.")

args = parser.parse_args()

app = SiriusApplication()
app.open_window(MainWindow, parent=None, prefix=args.prefix)
sys.exit(app.exec_())
