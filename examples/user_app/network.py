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

"""Network information retrieval."""

import fcntl
import socket
import struct


def get_interface_address(if_name):
    """Get IPv4 address of an interface."""
    try:
        sket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(
            fcntl.ioctl(
                sket.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack("256s", if_name[:15].encode()),
            )[20:24]
        )
    except OSError:
        return None


def get_interfaces_addresses():
    """Retrieve a list of interfaces and their INET adddresses."""
    return {
        if_name: get_interface_address(if_name)
        for index, if_name in socket.if_nameindex()
    }


def get_hostname():
    """Retrieve hostname."""
    return socket.gethostname()
