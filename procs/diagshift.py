import taichi as ti
import numpy as np

from core.random import Random
from core.processor import Processor, get_luma

@ti.data_oriented
class Diagshift(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        ts = [
            (0.01, 0.19, 0.3),
            (0.2, 0.39, 0.6),
            (0.4, 0.59, 0.9),
            (0.6, 0.69, 1.2),
            (0.7, 0.79, 1.5),
            (0.8, 1.0, 1.8)
        ]

        distance = 10
        threshold = 0.05
        for r in ti.static(ts):
            n = rnd.random(int(t/5) + x)
            if r[0] < n < r[1]:
                distance *= int(1 + r[2])
                threshold *= 1 + r[2]

        curr_luma = get_luma(self.get_pixel(pixels_in, x, y))

        best_xr = x
        best_yr = y
        best_luma_r = curr_luma

        r_dir = -1 if y % 2 == 0 else 1

        for i in range(1, distance + 1):
            neighbour_x = x + (i * r_dir)
            neighbour_y = y - (i * r_dir)
            neighbour_luma = get_luma(self.get_pixel(pixels_in, neighbour_x, neighbour_y))

            if neighbour_luma > best_luma_r + threshold:
                best_luma_r = neighbour_luma
                best_xr = neighbour_x
                best_yr = neighbour_y

        final_r = self.get_pixel(pixels_in, best_xr, best_yr)[0]

        best_xg = x
        best_yg = y
        melhor_luma_b = curr_luma

        b_dir = 1 if x % 2 == 0 else -1

        for i in range(1, distance + 1):
            neighbour_x = x - (i * b_dir)
            neighbour_y = y - (i * b_dir)
            neighbour_luma = get_luma(self.get_pixel(pixels_in, neighbour_x, neighbour_y))

            if neighbour_luma > melhor_luma_b + threshold:
                melhor_luma_b = neighbour_luma
                best_yg = neighbour_y
                best_xg = neighbour_x

        final_b = self.get_pixel(pixels_in, best_xg, best_yg)[2]

        # noise
        # float noise = sin(dot((float2)(x,y), (float2)(12.9898f,78.233f))) * 43758.5453f;
        # noise = noise - floor(noise); // Fica entre 0.0 e 1.0
        # int azul_ruidoso = (int)pixel_atual.z + (int)((noise - 0.5f) * 40.0f);
        # uchar final_b = (uchar)clamp(azul_ruidoso, 0, 255);

        og = self.get_pixel(pixels_in, x, y)
        color = ti.Vector([final_r, og[1], final_b])

        return color
