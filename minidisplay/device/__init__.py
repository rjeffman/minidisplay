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

"""Initialize SSD1306 display module."""


from minidisplay import RenderContext
from minidisplay.fontmanager import FontManager
from minidisplay.device.display import I2CDisplay


def init(_configuration):
    """Initialize display device."""
    return RenderContext(I2CDisplay(), FontManager())


def shutdown(rendercontext):
    """Shutdown display device."""
    rendercontext.display.fill(0)
    rendercontext.display.show()
