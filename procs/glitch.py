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
        r = rnd.random(t + (y/3))
        
        color = pixels_in[x, y]

        if r > 0.5:
            color = self.get_pixel_wrap_around(pixels_in, x + int(r * 20), y)
        
        return color
        