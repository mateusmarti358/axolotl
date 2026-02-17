import taichi as ti
import numpy as np

from sys import exit

from core.random import Random
from core.processor import Processor, get_luma

@ti.data_oriented
class Shift(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)

        channels = {
            'r': 0,
            'g': 1,
            'b': 2
        }

        c = str(params["channels"][0]).lower()
        if not c:
            print('Not enough components in Shift.')
            exit(1)
        
        c1 = channels[c]
        c2 = channels[str(params["channels"][1]).lower()]

        self.c1 = c1
        self.c2 = c2

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

        dx = 10
        dy = 10
        threshold = 0.05
        for r in ti.static(ts):
            n = rnd.random(int(t/5) + x)
            if r[0] < n < r[1]:
                dx *= int(1 + r[2])
                # threshold *= 1 + r[2]
            n = rnd.random(int(t/5) + y)
            if r[0] < n < r[1]:
                dy *= int(1 + r[2])

        curr_luma = get_luma(self.get_pixel(pixels_in, x, y))

        best_xr = x
        best_luma_r = curr_luma

        r_dir = -1 if y % 2 == 0 else 1

        for i in range(1, dy + 1):
            neighbour_x = x + (i * r_dir)
            neighbour_luma = get_luma(self.get_pixel(pixels_in, neighbour_x, y))

            if neighbour_luma > best_luma_r + threshold:
                best_luma_r = neighbour_luma
                best_xr = neighbour_x

        final_r = self.get_pixel(pixels_in, best_xr, y)[self.c1]

        best_yg = y
        melhor_luma_g = curr_luma

        g_dir = 1 if y % 2 == 0 else -1

        for i in range(1, dx + 1):
            neighbour_y = y + (i * g_dir)
            neighbour_luma = get_luma(self.get_pixel(pixels_in, x, neighbour_y))

            if neighbour_luma > melhor_luma_g + threshold:
                melhor_luma_g = neighbour_luma
                best_yg = neighbour_y

        final_g = self.get_pixel(pixels_in, x, best_yg)[self.c2]

        # noise
        # float noise = sin(dot((float2)(x,y), (float2)(12.9898f,78.233f))) * 43758.5453f;
        # noise = noise - floor(noise); // Fica entre 0.0 e 1.0
        # int azul_ruidoso = (int)pixel_atual.z + (int)((noise - 0.5f) * 40.0f);
        # uchar final_b = (uchar)clamp(azul_ruidoso, 0, 255);

        color = self.get_pixel(pixels_in, x, y)

        color[self.c1] = final_r
        color[self.c2] = final_g

        return color
