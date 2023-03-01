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

"""Example app: stage"""

import psutil
from user_app import network, storage  # pylint: disable=import-error


def render_header(rendercontext):
    """Render common screen header."""
    hostname = network.get_hostname().split(".")[0]
    ifaces = network.get_interfaces_addresses()
    ipaddress = [
        ip for ifname, ip in ifaces.items() if ifname.lower()[0] == "w"
    ][0]
    font = rendercontext.font_manager.get_font("DejaVuSansMono", 10)
    rendercontext.display.write_text(f"{hostname:<11s}", 0, 0, font)
    font = rendercontext.font_manager.get_font("DejaVuSansMono", 9)
    rendercontext.display.write_text(f"{ipaddress:>16s}", 40, 7, font)


def render_info(rendercontext):
    """Render information data."""
    font = rendercontext.font_manager.get_font("DejaVuSansMono", 12)
    cpu_usage = int(psutil.cpu_percent(percpu=False))
    memory = psutil.virtual_memory()
    total = memory.total / 2**30  # GB
    free = memory.available / 2**30  # GB
    used = 100 * ((total - free) / total)
    disk = storage.get_fs_info("/")
    diskfree = disk.free / 2**30
    disksize = disk.size / 2**30
    diskused = 100 * ((disksize - diskfree) / disksize)
    rendercontext.display.write_text(f"CPU:  {cpu_usage: 3d}%", 0, 16, font)
    rendercontext.display.write_text(
        f"MEM:  {int(used): 2d}% {free:>0.2f}GB", 0, 28, font
    )
    rendercontext.display.write_text(
        f"DISK: {int(diskused): 2d}% {diskfree:>0.2f}GB",
        0,
        40,
        font,
    )


def render(rendercontext):
    """Render applet."""
    render_header(rendercontext)
    render_info(rendercontext)
