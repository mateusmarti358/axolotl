import taichi as ti

INT32_MAX = 0x7FFFFFFF

@ti.data_oriented
class Random:
    def __init__(self, seed):
        self.seed = seed

    def set_seed(self, seed):
        self.seed = seed

    @ti.func
    def splitmix64(self, x):
        x += 0x9E3779B
        x = (x ^ (x >> 30)) * 0xBF58476
        x = (x ^ (x >> 27)) * 0x94D049B
        x = x ^ (x >> 31)
        return x

    @ti.func
    def randint(self, index):
        return self.splitmix64(ti.i32(self.seed) ^ ti.i32(index))
    
    @ti.func
    def random(self, index):
        return self.randint(index) / INT32_MAX