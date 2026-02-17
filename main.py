import taichi as ti
import numpy as np
from PIL import Image

import sys

from core.pixels import Pixels
from core.engine import Engine
from core.procloader import load_processor_class

class Main:
    def __init__(self, img_path, procs):
        raw_img = Image.open(img_path).convert("RGB")
        raw_img = raw_img.resize((1000, 1000), Image.Resampling.LANCZOS)
        self.img = Pixels(raw_img)

        self.engines: list[Engine] = []
        for proc in procs:
            self.engines.append(Engine(proc, self.img.width, self.img.height))
        self.engines.append(Engine(load_processor_class('zoom'), self.img.width, self.img.height))
        self.engines[0].set_pixels_in(self.img.pixels)

        self.last_mouse = None
        self.zoom_proc = self.engines[-1].processor

    def handle_events(self, gui):
        curr_mouse = gui.get_cursor_pos()

        if gui.is_pressed(ti.GUI.LMB) and self.zoom_proc is not None and self.last_mouse is not None:
            dx = self.last_mouse[0] - curr_mouse[0]
            dy = self.last_mouse[1] - curr_mouse[1]

            if self.zoom_proc.zoom_amount[None] < 1.0:
                dx = -dx
                dy = -dy

            self.zoom_proc.center[None][0] += dx / self.zoom_proc.zoom_amount[None]
            self.zoom_proc.center[None][1] += dy / self.zoom_proc.zoom_amount[None]

        for e in gui.get_events():
            zoom_proc = None
            for engine in self.engines:
                if engine.processor.__class__.__name__ == 'Zoom':
                    zoom_proc = engine.processor

            if e.delta[1] > 0:
                zoom_proc.zoom_amount[None] *= 1.1
            elif e.delta[1] < 0:
                zoom_proc.zoom_amount[None] *= 0.9

            zoom_proc.zoom_amount[None] = max(0.1, zoom_proc.zoom_amount[None])

        self.last_mouse = curr_mouse

    def run(self):
        gui = ti.GUI("", res=(self.img.width, self.img.height))
        while gui.running:
            self.handle_events(gui)

            if gui.is_pressed(ti.GUI.ESCAPE):
                break

            for i in range(len(self.engines)):
                self.engines[i].process(gui.frame)
                if i < len(self.engines) - 1:
                    self.engines[i + 1].set_pixels_in(self.engines[i].pixels_out)

            gui.set_image(self.engines[-1].pixels_out)

            gui.show()

if __name__ == "__main__":
    procs = []
    for i in range(2, len(sys.argv)):
        procs.append(load_processor_class(sys.argv[i]))

    ti.init(arch=ti.gpu)
    main = Main(sys.argv[1], procs)
    main.run()
    
