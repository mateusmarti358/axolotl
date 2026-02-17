import taichi as ti
import numpy as np
from abc import ABC, abstractmethod

class Processor(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_shape(self, width, height):
        self.width = width
        self.height = height

    @abstractmethod
    @ti.func
    def process(self, pixels_in, x, y, t):
        pass
