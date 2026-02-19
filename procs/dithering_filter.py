import taichi as ti
import numpy as np

from core.processor import Processor, get_luma

from procs.dither import Dither

@ti.data_oriented
class DitheringFilter(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)
        self.threshold = params['threshold']
        self.dither = Dither(width, height, params)

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        pixel = self.get_pixel(pixels_in, x, y)
        
        if get_luma(pixel) >= self.threshold:
            pixel = self.dither.process(pixels_in, x, y, t, rnd)

        return pixel