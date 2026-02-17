import taichi as ti
from core.processor import Processor, get_luma

@ti.data_oriented
class BoxBloom(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        distance = 7
        loss = 0.99

        colour = pixels_in[x, y]

        curr_luma = get_luma(colour)

        for i in range(-distance, distance):
            for j in range(-distance, distance):
                nx = x + i
                ny = y + j                

                nc = self.get_pixel(pixels_in, nx, ny)

                colour += (nc * (1.0 - loss))

        return colour
