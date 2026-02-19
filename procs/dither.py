import taichi as ti
from core.processor import Processor, clamp

@ti.data_oriented
class Dither(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)
        self.levels = params['levels']
        self.group_size = params['group_size']

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        levels = self.levels
        group_size = self.group_size

        gx = (x // group_size) * group_size
        gy = (y // group_size) * group_size

        bayer = ti.Vector([
             0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
            12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
             3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
            15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0
        ])

        bayer_idx = ((gy // group_size % 4) * 4 + (gx // group_size % 4))
        threshold = bayer[bayer_idx]

        colour = pixels_in[gx, gy]

        res_r = ti.floor(colour[0] * levels + threshold) / levels
        res_g = ti.floor(colour[1] * levels + threshold) / levels
        res_b = ti.floor(colour[2] * levels + threshold) / levels

        return ti.Vector([res_r, res_g, res_b])