import taichi as ti
import numpy as np

from core.processor import Processor, lerp

@ti.func
def calc_id(x, y, width):
    return x + (y * width)

@ti.func
def calc_xy(id, width):
    return int(id % width), int(ti.floor(id / width))

DMA_EFFECT = 0.3

@ti.data_oriented
class Datamisalignment(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        id = calc_id(x, y, self.width)

        c = id % 3

        src_id = id + int(id / 3)

        color = ti.Vector([0.0, 0.0, 0.0])

        if c == 0:
            src_x, src_y = calc_xy(src_id, self.width)
            color = pixels_in[src_x, src_y]
        elif c == 1:
            src1_x, src1_y = calc_xy(src_id + 1, self.width)
            src2_x, src2_y = calc_xy(src_id + 2, self.width)
            color[0] = pixels_in[src1_x, src1_y][1]
            color[1] = pixels_in[src1_x, src1_y][2]
            color[2] = pixels_in[src2_x, src2_y][0]
        else:
            src1_x, src1_y = calc_xy(src_id + 1, self.width)
            src2_x, src2_y = calc_xy(src_id + 2, self.width)
            color[0] = pixels_in[src1_x, src1_y][2]
            color[1] = pixels_in[src2_x, src2_y][0]
            color[2] = pixels_in[src2_x, src2_y][1]

        prev_colour = pixels_in[x, y]

        color[0] = lerp(prev_colour[0], color[0], DMA_EFFECT)
        color[1] = lerp(prev_colour[1], color[1], DMA_EFFECT)
        color[2] = lerp(prev_colour[2], color[2], DMA_EFFECT)

        return color
        