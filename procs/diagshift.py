import taichi as ti
import numpy as np

from core.random import Random
from core.processor import Processor, get_luma

@ti.data_oriented
class Diagshift(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        ts = [
            (0.0, 0.09, 0.8),
            (0.1, 0.19, 1.2),
            (0.2, 0.39, 1.4),
            (0.4, 0.59, 1.6),
            (0.6, 0.79, 1.9),
            (0.8, 1.0, 2.3)
        ]

        distance1 = 4.0
        distance2 = 4.0
        threshold = 0.05

        for i in range(2):
            for r in ti.static(ts):
                n = rnd.random(int(t/5) + (x + y))
                if r[0] < n < r[1]:
                    distance1 *= 1 + r[2]
                    threshold *= 1 + r[2]
            for r in ti.static(ts):
                n = rnd.random(int(t/5) + (x - y))
                if r[0] < n < r[1]:
                    distance2 *= 1 + r[2]

        distance1 = int(distance1)
        distance2 = int(distance2)

        curr_luma = get_luma(self.get_pixel(pixels_in, x, y))

        best_xr = x
        best_yr = y
        best_luma_r = curr_luma

        r_dir = -1 if y % 2 == 0 else 1

        for i in range(1, distance1 + 1):
            neighbour_x = x + (i * r_dir)
            neighbour_y = y - (i * r_dir)
            neighbour_luma = get_luma(self.get_pixel(pixels_in, neighbour_x, neighbour_y))

            if neighbour_luma > best_luma_r + threshold:
                best_luma_r = neighbour_luma
                best_xr = neighbour_x
                best_yr = neighbour_y

        final_r = self.get_pixel(pixels_in, best_xr, best_yr)[0]

        best_xb = x
        best_yb = y
        melhor_luma_b = curr_luma

        b_dir = 1 if x % 2 == 0 else -1

        for i in range(1, distance2 + 1):
            neighbour_x = x - (i * b_dir)
            neighbour_y = y - (i * b_dir)
            neighbour_luma = get_luma(self.get_pixel(pixels_in, neighbour_x, neighbour_y))

            if neighbour_luma > melhor_luma_b + threshold:
                melhor_luma_b = neighbour_luma
                best_xb = neighbour_x
                best_yb = neighbour_y

        final_b = self.get_pixel(pixels_in, best_xb, best_yb)[2]

        # noise
        # float noise = sin(dot((float2)(x,y), (float2)(12.9898f,78.233f))) * 43758.5453f;
        # noise = noise - floor(noise); // Fica entre 0.0 e 1.0
        # int azul_ruidoso = (int)pixel_atual.z + (int)((noise - 0.5f) * 40.0f);
        # uchar final_b = (uchar)clamp(azul_ruidoso, 0, 255);

        og = self.get_pixel(pixels_in, x, y)
        color = ti.Vector([final_r, og[1], final_b])

        return color
