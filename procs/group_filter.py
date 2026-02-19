import taichi as ti
import numpy as np

from core.processor import Processor, get_luma

@ti.data_oriented
class GroupFilter(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)
        self.radius = params['radius']
        self.threshold = params['threshold'] * (self.radius + 0.01)

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        luma_acc = 0.0
        for i in range(-self.radius, self.radius + 1):
            for j in range(-self.radius, self.radius + 1):
                pixel = self.get_pixel(pixels_in, x + i, y + j)
                luma_acc += get_luma(pixel)

        pixel = self.get_pixel(pixels_in, x, y)

        if luma_acc < self.threshold:
            pixel = ti.Vector([0.0, 0.0, 0.0])

        return pixel
