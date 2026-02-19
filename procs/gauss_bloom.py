import taichi as ti
import numpy as np

from core.processor import Processor, get_luma

RADIUS = 9
SIGMA = 3.0
THRESHOLD = 0.1
INTENSITY = 0.9

@ti.data_oriented
class GaussBloom(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height)

        self.radius = params["radius"]
        self.sigma = params["sigma"]
        self.threshold = params["threshold"]
        self.intensity = params["intensity"]

        self.weights_field = ti.field(dtype=ti.f32, shape=(self.radius * 2 + 1,))
        
        self.compute_weights()

        self.bright_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(self.width, self.height))
        self.hb_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(self.width, self.height))
        self.vb_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(self.width, self.height))

    def set_shape(self, width, height):
        self.bright_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))
        self.hb_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))
        self.vb_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))
        return super().set_shape(width, height)

    def compute_weights(self):
        weights = []
        sum_w = 0.0
        for i in range(-self.radius, self.radius + 1):
            w = np.exp(-(i*i) / (2 * self.sigma**2))
            weights.append(w)
            sum_w += w
        
        normalized_weights = [w / sum_w for w in weights]
        
        for i in range(len(normalized_weights)):
            self.weights_field[i] = normalized_weights[i]

    # GPU

    @ti.func
    def bright_pass(self, pixels_in, x, y):
        c = self.get_pixel(pixels_in, x, y)
        if get_luma(c) < self.threshold:
            c = ti.Vector([0.0, 0.0, 0.0])
        return c

    @ti.func
    def horizontal_pass(self, pixels_in, x, y):
        acc = ti.Vector([0.0, 0.0, 0.0])
        for i in range(-self.radius, self.radius + 1):
            pixel = self.get_pixel(pixels_in, x + i, y)
            w = self.weights_field[i+self.radius]
            acc += pixel * w
        return acc
    
    @ti.func
    def vertical_pass(self, pixels_in, x, y):
        acc = ti.Vector([0.0, 0.0, 0.0])
        for i in range(-self.radius, self.radius + 1):
            pixel = self.get_pixel(pixels_in, x, y + i)
            w = self.weights_field[i+self.radius]
            acc += pixel * w
        return acc

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        colour = pixels_in[x, y]

        self.bright_buffer[x, y] = self.bright_pass(pixels_in, x, y)
        self.hb_buffer[x, y] = self.horizontal_pass(self.bright_buffer, x, y)
        self.vb_buffer[x, y] = self.vertical_pass(self.hb_buffer, x, y)

        return colour + self.intensity * self.vb_buffer[x, y]
