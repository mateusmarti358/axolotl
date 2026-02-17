import taichi as ti
import numpy as np

from core.processor import Processor

@ti.data_oriented
class Chromaberration(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t):
        t *= 0.3
        m = 10
        color = pixels_in[x, y]

        if x <= m or x >= self.width - m or y <= m or y >= self.height - m:
            pass
        else:
            color = pixels_in[x, y]

            gxm = (ti.sin(-t))
            gym = (ti.cos(-t))

            oxm = (ti.sin(t))
            oym = (ti.cos(t))

            offset = m # int(ti.floor(((ti.sin(t * 10)/2) + 0.5) * m))

            ox = int(offset * oxm)
            oy = int(offset * oym)

            gx = int(offset * gxm)
            gy = int(offset * gym)

            color[0] = pixels_in[x + ox, y - oy][0]
            color[1] = pixels_in[x - gx, y + gy][1]
            color[2] = pixels_in[x - ox, y + oy][2]

        return color
