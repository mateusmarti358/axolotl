import taichi as ti
import numpy as np

from core.processor import Processor, get_luma

@ti.data_oriented
class Filter(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)
        self.threshold = params['threshold']

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        pixel = self.get_pixel(pixels_in, x, y)
        if get_luma(pixel) < self.threshold:
            pixel = ti.Vector([0.0, 0.0, 0.0])
        return pixel
