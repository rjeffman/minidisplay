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

"""SSD1306 OLED Display."""

import board  # pylint: disable=import-error
import busio  # pylint: disable=import-error
import adafruit_ssd1306  # pylint: disable=import-error

from minidisplay.display import BaseDisplay


class I2CDisplay(BaseDisplay):
    """SSD1306 implementation."""

    # write_text and draw_image don't need to be overriden.

    def __init__(self, width=128, height=64, address=0x3C, reset=None):
        """Initialize I2C display."""
        super().__init__(width, height)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.display = adafruit_ssd1306.SSD1306_I2C(
            width, height, i2c, addr=address, reset=reset
        )

    def update(self):
        """Update hardware display."""
        self.display.image(self.buffer.convert(mode="1"))
        self.display.show()
