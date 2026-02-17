import taichi as ti
import numpy as np
from PIL import Image

class Pixels:
    def __init__(self, img_raw: Image):
        img_array = np.array(img_raw).astype(np.float32) / 255.0

        self.width, self.height, _ = img_array.shape

        self.pixels = ti.Vector.field(3, dtype=ti.f32, shape=(self.height, self.width))
        self.pixels.from_numpy(np.transpose(img_array[::-1, :, :], (1, 0, 2)))
