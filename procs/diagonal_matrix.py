import taichi as ti
from core.processor import Processor, clamp

@ti.data_oriented
class DiagonalMatrix(Processor):
    def __init__(self, width, height, params):
        super().__init__(width, height, params)

        self.square_size = params["square_size"]
        self.thickness = params["thickness"]
        self.diagonals = params['diagonals']

    @ti.func
    def process(self, pixels_in, x, y, t, rnd):
        pitch = self.square_size + self.thickness

        color = pixels_in[x, y]

        mod_x = x % pitch
        mod_y = y % pitch
        
        vertical = mod_x < self.thickness
        horizontal = mod_y < self.thickness

        diag1 = mod_x == mod_y
        diag2 = mod_x == pitch - mod_y
        diagonal = (diag1 or diag2) if self.diagonals else diag1;

        if not vertical:
            color[0] = 0.0
        if not horizontal:
            color[1] = 0.0
        if not diagonal:
            color[2] = 0.0

        return color