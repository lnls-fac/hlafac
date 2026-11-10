#!/usr/bin/env python-sirius
"""SI Bumps application connected to an originating SOFB register."""

import argparse
import sys

from siriushla.sirius_application import SiriusApplication
from siriushlafac.si_ap_bumps import SIBumpsWindow


def main():
    parser = argparse.ArgumentParser(description='Run SI Bumps Interface.')
    parser.add_argument('--register-channel', required=True,
                        help='Local socket created by the SOFB orbit register.')
    args = parser.parse_args()
    # Do not let the Qt application parse our custom command-line argument.
    sys.argv = sys.argv[:1]
    app = SiriusApplication()
    app.open_window(SIBumpsWindow, parent=None,
                    register_channel=args.register_channel)
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())

# #!/usr/bin/env python-sirius

# """SI Bumps Application."""

# import sys
# import argparse as _argparse

# from siriushla.sirius_application import SiriusApplication

# from siriushlafac.si_ap_bumps import SIBumpsWindow


# parser = _argparse.ArgumentParser(
#     description="Run SI Bumps Interface.")
# args = parser.parse_args()

# app = SiriusApplication()
# app.open_window(SIBumpsWindow, parent=None)
# sys.exit(app.exec_())
