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

"""Display implementation."""

from PIL import Image, ImageDraw

from minidisplay.colors import Color


class BaseDisplay:
    """Base class for actual displays."""

    def __init__(self, width, height):
        """Initialize offscreen buffer and display base data."""
        self.size = (width, height)
        self.buffer = Image.new("RGB", self.size)
        self.draw = ImageDraw.Draw(self.buffer)
        self.clear()

    def clear(self):
        """Clear offscreen buffer."""
        self.buffer.paste(Color.Black, [0, 0, *self.size])

    def write_text(self, text, x, y, font):
        """Write text to the offscreen buffer."""
        self.draw.text((x, y), text, font=font, fill=Color.White, align="left")

    def draw_image(self, image, x, y, image_filter=None):
        """Draw image to offscreen buffer."""
        if isinstance(image, str):
            image = Image.open(image)
        if (
            image.mode in ("RGBA", "LA")
            or image.mode == "P"
            and "transparency" in image.info
        ):
            bg_colour = (255,) * 3
            bgimage = Image.new("RGBA", image.size, bg_colour)
            image = Image.alpha_composite(
                bgimage, image.convert("RGBA")
            ).convert("RGB")
        image.thumbnail(self.size, Image.ANTIALIAS)
        if image_filter:
            image = image_filter(image)
        self.buffer.paste(image, (x, y))

    def set_pixel(self, x, y, color=(1,)):
        """Set a pixel in the offscreen buffer with the given color."""
        self.buffer.putpixel((x, y), color)

    def update(self):
        """Update display with offscreen buffer."""
        raise NotImplementedError("BaseDisplay.update() not overriden.")
