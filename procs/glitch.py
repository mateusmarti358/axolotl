import taichi as ti

from core.processor import Processor, clamp

@ti.data_oriented
class Glitch(Processor):
    @ti.func
    def get_pixel_wrap_around(self, pixels_in, x, y):
        x = x % self.width
        y = y % self.height
        return pixels_in[x, y]

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        s = min(100, rnd.random((t*0.03) + (y//60)) * 400)
        r = rnd.random((t*0.1) + ((y//s) * s)) - 0.5

        color = pixels_in[x, y]

        if r < -0.48 or r > 0.48:
            color = self.get_pixel_wrap_around(pixels_in, x + int(r * 300), y)
        
        return color
