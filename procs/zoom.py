import taichi as ti
import numpy as np
from core.processor import Processor

@ti.data_oriented
class Zoom(Processor):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.zoom_amount = ti.field(dtype=ti.f32, shape=())
        self.center = ti.Vector.field(2, dtype=ti.f32, shape=())
        
        self.zoom_amount[None] = 1.0
        self.center[None] = [0.5, 0.5]

    @ti.func
    def process(self, pixels_in, x, y, t):
        z = self.zoom_amount[None]
        
        cx = self.center[None][0] * self.width
        cy = self.center[None][1] * self.height

        src_x = int((x - cx) / z + cx)
        src_y = int((y - cy) / z + cy)

        color = ti.Vector([0.0, 0.0, 0.0])

        if 0 <= src_x < self.width and 0 <= src_y < self.height:
            color = pixels_in[src_x, src_y]
        
        return color