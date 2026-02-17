import taichi as ti
from core.processor import Processor

@ti.data_oriented
class Neonedges(Processor):
    @ti.func
    def get_luma(self, pixels_in, x, y):
        nx = ti.max(0, ti.min(x, self.width - 1))
        ny = ti.max(0, ti.min(y, self.height - 1))
        
        color = pixels_in[nx, ny]
        
        return color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        t *= 0.06

        tl = self.get_luma(pixels_in, x - 1, y - 1)
        tc = self.get_luma(pixels_in, x,     y - 1)
        tr = self.get_luma(pixels_in, x + 1, y - 1)
        l  = self.get_luma(pixels_in, x - 1, y)
        r  = self.get_luma(pixels_in, x + 1, y)
        bl = self.get_luma(pixels_in, x - 1, y + 1)
        bc = self.get_luma(pixels_in, x,     y + 1)
        br = self.get_luma(pixels_in, x + 1, y + 1)

        gx = -tl - 2.0 * l - bl + tr + 2.0 * r + br
        gy = -tl - 2.0 * tc - tr + bl + 2.0 * bc + br

        magnitude = ti.sqrt(gx * gx + gy * gy)

        angle = ti.atan2(gy, gx)

        neon_r = ti.sin(angle + t + 0.0) * 0.5 + 0.5
        neon_g = ti.sin(angle + t + 2.0) * 0.5 + 0.5
        neon_b = ti.sin(angle + t + 4.0) * 0.5 + 0.5

        glow = ti.max(0.0, ti.min(magnitude * 2.5, 1.0))

        return ti.Vector([neon_r * glow, neon_g * glow, neon_b * glow])