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

"""FontManager implementation."""

import os

from PIL import ImageFont


class FontManager:  # pylint: disable=too-few-public-methods
    """Font manager class."""

    def __init__(self, dpi=122):
        """Initialize FontManager for a given DPI."""

        def scandir(path):
            _res = []
            for entry in os.scandir(os.path.abspath(path)):
                if entry.path.endswith("."):
                    continue
                abspath = os.path.abspath(entry.path)
                if entry.is_dir():
                    _res.extend(scandir(abspath))
                elif entry.is_file():
                    if abspath.lower().endswith(".ttf"):
                        _res.append(abspath)
            return _res

        self.font_list = scandir("/usr/share/fonts")
        self.ratio = dpi / (128 * 0.96)
        self.cache = {}

    def get_font(self, name, size):
        """Retrieve a font object with a given name and size."""
        _res = self.cache.get((name, size))
        if not _res:
            font = [
                font_file
                for font_file in self.font_list
                if font_file.lower().endswith(f"/{name}.ttf".lower())
            ]
            if font:
                _res = ImageFont.truetype(font[0], int(size * self.ratio))
                self.cache[(name, size)] = _res
        return _res
