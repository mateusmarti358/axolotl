import taichi as ti
import numpy as np
from PIL import Image

import sys

from core.pixels import Pixels
from core.engine import Engine
from core.procloader import load_processor_class

def main(img_path, procs):
    ti.init(arch=ti.gpu)

    img = Image.open(img_path).convert("RGB")
    img = Pixels(img)

    engines: list[Engine] = []
    for proc in procs:
        engines.append(Engine(proc, img.width, img.height))

    engines[0].set_pixels_in(img.pixels)

    gui = ti.GUI("", res=(img.width, img.height))

    while gui.running:
        for i in range(len(engines)):
            engines[i].process(gui.frame)
            if i < len(engines) - 1:
                engines[i + 1].set_pixels_in(engines[i].pixels_out)

        gui.set_image(engines[-1].pixels_out)

        gui.show()

if __name__ == "__main__":
    procs = []
    for i in range(2, len(sys.argv)):
        procs.append(load_processor_class(sys.argv[i]))
    main(sys.argv[1], procs)
    
