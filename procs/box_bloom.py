import taichi as ti
from core.processor import Processor, get_luma

@ti.data_oriented
class BoxBloom(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)

        self.distance = params["distance"]
        self.loss = params["loss"]

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        distance = ti.static(self.distance)
        loss = ti.static(self.loss)

        colour = pixels_in[x, y]

        curr_luma = get_luma(colour)

        for i in range(-distance, distance):
            for j in range(-distance, distance):
                nx = x + i
                ny = y + j                

                nc = self.get_pixel(pixels_in, nx, ny)

                colour += (nc * (1.0 - loss))

        return colour
