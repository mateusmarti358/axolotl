import taichi as ti
import numpy as np

from core.processor import Processor, get_luma


@ti.data_oriented
class Filter(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        return pixels_in