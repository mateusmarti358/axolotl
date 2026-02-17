import taichi as ti
import numpy as np
from abc import ABC, abstractmethod

@ti.func
def clamp(x, min, max):
    return ti.min(ti.max(x, min), max)

@ti.func
def lerp(a, b, t):
    return a + (b - a) * t

@ti.func
def get_luma(pixel):
    return pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114

class Processor(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_shape(self, width, height):
        self.width = width
        self.height = height

    @staticmethod
    def get_default_params():
        return None

    @ti.func
    def get_pixel(self, pixels_in, x, y):
        return pixels_in[int(clamp(x, 0, self.width - 1)), int(clamp(y, 0, self.height - 1))]

    @abstractmethod
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        pass
