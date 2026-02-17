import taichi as ti
from core.processor import Processor, clamp

@ti.data_oriented
class Crt(Processor):
    def __init__(self, width, height):
        super().__init__(width, height)

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        nx = (float(x) / self.width) * 2.0 - 1.0
        ny = (float(y) / self.height) * 2.0 - 1.0

        warp = 0.09
        r_sq = nx * nx + ny * ny
        
        uv_x = nx * (1.0 + r_sq * warp)
        uv_y = ny * (1.0 + r_sq * warp)

        offset_dist = 5.0 * r_sq 
        
        px = (uv_x + 1.0) * 0.5 * self.width
        py = (uv_y + 1.0) * 0.5 * self.height

        # r = self.get_pixel(pixels_in, px - offset_dist, py)[0]
        # g = self.get_pixel(pixels_in, px, py)[1]
        # b = self.get_pixel(pixels_in, px + offset_dist, py)[2]
        
        color = self.get_pixel(pixels_in, px, py) # ti.Vector([r, g, b])

        scanline = ti.sin(((uv_y * self.height) * 0.03) + (t * 0.1)) * 0.10 + 0.75
        color *= scanline

        vignette = 1.0 - self.smoothstep(0.8, 1.5, r_sq)
        color *= vignette

        if uv_x < -1.0 or uv_x > 1.0 or uv_y < -1.0 or uv_y > 1.0:
            color = ti.Vector([0.0, 0.0, 0.0])

        return color

    @ti.func
    def smoothstep(self, edge0, edge1, x):
        t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)