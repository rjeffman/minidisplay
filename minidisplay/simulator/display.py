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

"""Simulator display."""

import pygame

from minidisplay.colors import Color
from minidisplay.display import BaseDisplay


class SimulatorDisplay(BaseDisplay):
    """Implement a simulator display."""

    def __init__(  # pylint: disable=W0613
        self, width, height, dpi=122, host_scale=2
    ):
        """Initialize simulator display."""
        pygame.display.set_caption("Simulator")
        self.ratio = host_scale
        division = (height // 4) * self.ratio
        width, height = (int(width * self.ratio), int(height * self.ratio))
        super().__init__(width, height)
        self.screen = pygame.display.set_mode((width, height))
        self.color = pygame.Surface((width, height))
        pygame.draw.rect(self.color, Color.Yellow, (0, 0, width, division))
        pygame.draw.rect(self.color, Color.Blue, (0, division, width, height))

    def update(self):
        """Update display view."""
        buffer = pygame.image.fromstring(
            self.buffer.tobytes(), self.buffer.size, self.buffer.mode
        ).convert()
        self.screen.blit(buffer, (0, 0))
        self.screen.blit(self.color, (0, 0), None, pygame.BLEND_MIN)
        pygame.display.update()

    def write_text(self, text, x, y, font):
        """Write text to display, repecting display scale."""
        super().write_text(
            text, int(x * self.ratio), int(y * self.ratio), font
        )

    def draw_image(self, image, x, y, image_filter=None):
        """Draw image to display."""
        super().draw_image(
            image, int(x * self.ratio), int(y * self.ratio), image_filter
        )
