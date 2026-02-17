import taichi as ti
import numpy as np

from core.processor import Processor

@ti.data_oriented
class Chromaberration(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        color = pixels_in[x, y]

        ts = [
            (0.01, 0.19, -0.3),
            (0.2, 0.39, -0.6),
            (0.4, 0.59, 0.9),
            (0.6, 0.69, -1.2),
            (0.7, 0.79, 1.5),
            (0.8, 1.0, -1.8)
        ]

        moffs = [1.2, -1.1, 1.1]
        for r in ti.static(ts):
            n = rnd.random(int(t/5) + x * y)
            if r[0] < n < r[1]:
                moffs[0] *= 1 + r[2]

            n = rnd.random(int(t/5) + x * y)
            if r[0] < n < r[1]:
                moffs[1] *= 1 + r[2]

            n = rnd.random(int(t/5) + x * y)
            if r[0] < n < r[1]:
                moffs[2] *= 1 + r[2]

        color = pixels_in[x, y]

        color[0] = self.get_pixel(pixels_in, x + moffs[0], y - moffs[0])[0]
        color[1] = self.get_pixel(pixels_in, x + moffs[1], y - moffs[1])[1]
        color[2] = self.get_pixel(pixels_in, x - moffs[2], y + moffs[2])[2]

        return color
