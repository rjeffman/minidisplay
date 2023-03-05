# This file is part of minidisplay
#
# Copyright (C) 2023 Rafael Guterres Jeffman
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <https://www.gnu.org/licenses/>.

"""Start mini display."""

import importlib
import argparse

import yaml

from minidisplay.application import Application


__VERSION__ = "0.1"


def parse_cli():
    """Parse command line options."""
    parser = argparse.ArgumentParser(
        prog="minidisplay",
        description="Control an SDD1306 I2C display.",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__VERSION__}"
    )

    parser.add_argument(
        "configpath",
        help="Configuration path.",
        metavar="CONFIG",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=int,
        nargs=1,
        help="The I2C device to use. If not providev I2C bus will be scanned.",
    )
    parser.add_argument(
        "-s",
        "--simulator",
        action="store_true",
        help="Run in simulation mode.",
    )
    return parser.parse_args()


def main():
    """Program entry point."""
    options = parse_cli()
    with open(options.configpath, "r") as conffile:  # pylint: disable=W1514
        configuration = yaml.safe_load(conffile)
    configuration.update(vars(options))
    print(configuration)
    module = f"minidisplay.{'simulator' if options.simulator else 'device'}"
    try:
        device_impl = importlib.import_module(f"{module}")
    except ModuleNotFoundError as mnfe:
        if (
            module == "minidisplay.device"
            and mnfe.name == "board"
            and not options.simulator
        ):
            print(
                f"{str(mnfe)}\nDid you want to run in simulator mode?",
                file=sys.stderr
            )
        else:
            print(str(mnfe))
        return 1
    context = device_impl.init(configuration)
    Application(context, configuration).run()
    device_impl.shutdown(context)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
