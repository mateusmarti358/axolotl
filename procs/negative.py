import taichi as ti
import numpy as np

from core.processor import Processor

@ti.data_oriented
class Negative(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        return ti.Vector([1.0 - pixels_in[x, y][0], 1.0 - pixels_in[x, y][1], 1.0 - pixels_in[x, y][2]])
