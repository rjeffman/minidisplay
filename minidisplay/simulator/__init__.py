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

"""Display simulator module."""

import pygame

from minidisplay import RenderContext
from minidisplay.fontmanager import FontManager
from minidisplay.simulator.display import SimulatorDisplay


def init(configuration):
    """Initialize simulator."""
    resolution = configuration.get("resolution", (128, 64, 122, 2))
    default_display_config = {
        "width": 128,
        "height": 64,
        "dpi": 122,
        "simulator_scale": 2,
    }
    if isinstance(resolution, dict):
        resolution = tuple(
            resolution.get(arg, default)
            for arg, default in default_display_config.items()
        )

    pygame.init()

    display = SimulatorDisplay(
        resolution[0],  # width
        resolution[1],  # height
        dpi=resolution[2],  # dpi
        host_scale=resolution[3],  # host scale
    )
    font_manager = FontManager(dpi=resolution[3] * resolution[2])
    return RenderContext(display, font_manager)


def shutdown(_context):
    """Shutdown simulator."""
    pygame.quit()
