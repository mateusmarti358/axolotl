import taichi as ti
from core.processor import Processor, clamp

@ti.data_oriented
class Dither(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        levels = 0.5
        bayer = ti.Vector([
             0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
            12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
             3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
            15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0
        ])

        bayer_idx = ((y//3) % 4) * 4 + ((x//3) % 4)
        threshold = bayer[bayer_idx]

        colour = pixels_in[x, y]

        colour[0] = ti.floor(colour[0] * levels + threshold) / levels
        colour[1] = ti.floor(colour[1] * levels + threshold) / levels
        colour[2] = ti.floor(colour[2] * levels + threshold) / levels

        return colour
