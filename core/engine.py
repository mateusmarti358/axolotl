import taichi as ti
import numpy as np
from PIL import Image

from core.processor import Processor, lerp

from typing import Type

@ti.data_oriented
class Engine:
    def __init__(self, processor, params, intensity, width, height, rnd):
        self.width = width
        self.height = height
        self.pixels_in = ti.Vector.field(3, dtype=ti.f32, shape=(self.height, self.width))
        self.pixels_out = ti.Vector.field(3, dtype=ti.f32, shape=(self.height, self.width))

        if params is None:
            self.processor = processor(width, height)
        else:
            self.processor = processor(width, height, params)

        self.rnd = rnd
        self.intensity_field = ti.field(dtype=ti.f32, shape=())
        self.intensity_field[None] = intensity 

    def set_intensity(self, intensity):
        self.intensity_field[None] = intensity

    def set_rnd(self, rnd):
        self.rnd = rnd

    def set_pixels_in(self, pixels_in):
        self.pixels_in = pixels_in

    @ti.kernel
    def process(self, t: float):
        for x, y in self.pixels_in:
            processed = self.processor.process(self.pixels_in, x, y, t, self.rnd)
            self.pixels_out[x, y] = lerp(self.pixels_in[x, y], processed, self.intensity_field[None])
