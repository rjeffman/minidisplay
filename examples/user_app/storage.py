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

"""Disk information."""

from collections import namedtuple
import os


def get_mount_point(path):
    """Get the mount point for a file."""
    path = os.path.abspath(path)
    while not os.path.ismount(path):
        path = os.path.dirname(path)
    return path


def get_local_fs():
    """Retrieve all possibly usable local filesystems."""
    valid_fs = ["tmpfs", "/dev"]
    return [
        namedtuple("FSType", "device mount type")(dev[1], dev[4], dev[7])
        # pylint: disable=unspecified-encoding
        for mount in open("/proc/self/mountstats", "rt")
        if any(
            (dev := mount.split())[1].startswith(valid) for valid in valid_fs
        )
    ]


def get_fs_info(path):
    """Retrieve info for file system conaining file defined by path."""
    mnt = get_mount_point(path)
    if not any(x.mount == mnt for x in get_local_fs()):
        raise Exception(f"Not in a local filesystem: {path}")
    stat = os.statvfs(path)
    size = stat.f_frsize * stat.f_blocks
    free = stat.f_bsize * stat.f_bavail
    used = size - free
    return namedtuple("FSInfo", "mount size free used")(mnt, size, free, used)
