import taichi as ti
from core.processor import Processor, get_luma

@ti.data_oriented
class Neonedges(Processor):
    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        t *= 0.06

        tl = get_luma(self.get_pixel(pixels_in, x - 1, y - 1))
        tc = get_luma(self.get_pixel(pixels_in, x,     y - 1))
        tr = get_luma(self.get_pixel(pixels_in, x + 1, y - 1))
        l  = get_luma(self.get_pixel(pixels_in, x - 1, y))
        r  = get_luma(self.get_pixel(pixels_in, x + 1, y))
        bl = get_luma(self.get_pixel(pixels_in, x - 1, y + 1))
        bc = get_luma(self.get_pixel(pixels_in, x,     y + 1))
        br = get_luma(self.get_pixel(pixels_in, x + 1, y + 1))

        gx = -tl - 2.0 * l - bl + tr + 2.0 * r + br
        gy = -tl - 2.0 * tc - tr + bl + 2.0 * bc + br

        magnitude = ti.sqrt(gx * gx + gy * gy)

        angle = ti.atan2(gy, gx)

        neon_r = ti.sin(angle + t + 0.0) * 0.5 + 0.5
        neon_g = ti.sin(angle + t + 2.0) * 0.5 + 0.5
        neon_b = ti.sin(angle + t + 4.0) * 0.5 + 0.5

        glow = ti.max(0.0, ti.min(magnitude * 2.5, 1.0))

        return ti.Vector([neon_r * glow, neon_g * glow, neon_b * glow])