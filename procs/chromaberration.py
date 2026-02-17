import taichi as ti
import numpy as np

from core.processor import Processor

@ti.data_oriented
class Chromaberration(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        # TODO OFFSET PARAM
        color = pixels_in[x, y]

        moffs = ti.Vector([10, 10, 10])

        color = pixels_in[x, y]

        color[0] = self.get_pixel(pixels_in, x + moffs[0], y - moffs[0])[0]
        # color[1] = self.get_pixel(pixels_in, x + moffs[1], y - moffs[1])[1]
        color[2] = self.get_pixel(pixels_in, x - moffs[2], y + moffs[2])[2]

        return color
