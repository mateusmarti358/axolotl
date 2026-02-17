import taichi as ti
import numpy as np
from PIL import Image

from core.random import Random
from core.pixels import Pixels
from core.engine import Engine
from core.procloader import ProcLoader

class App:
    def __init__(self, img_path, procs, procs_params):
        # SETTING UP
        ti.init(arch=ti.gpu)
        self.rnd = Random(12)

        # LOAD IMAGE
        raw_img = Image.open(img_path).convert("RGB")

        max_size = 1000
        ratio = min(max_size / raw_img.width, max_size / raw_img.height)
        new_size = (int(raw_img.width * ratio), int(raw_img.height * ratio))

        raw_img = raw_img.resize(new_size, Image.Resampling.LANCZOS)
        self.img = Pixels(raw_img)

        self.pixels_in = ti.Vector.field(3, dtype=ti.f32, shape=(self.img.width, self.img.height))
        self.pixels_out = ti.Vector.field(3, dtype=ti.f32, shape=(self.img.width, self.img.height))

        # ENGINES
        self.engines: list[Engine] = []
        for proc, params in zip(procs, procs_params):
            self.engines.append(Engine(proc, params, params['intensity'], self.img.width, self.img.height, self.rnd))
        
        self.engines.append(Engine(ProcLoader().load('procs/zoom.py')[0], None, 1, self.img.width, self.img.height, self.rnd))

        # INPUTS
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
        gui = ti.GUI("Axolotl", res=(self.img.width, self.img.height))

        buffers = [self.pixels_in, self.pixels_out]
        while gui.running:
            self.handle_events(gui)

            if gui.is_pressed(ti.GUI.ESCAPE):
                break

            self.engines[0].process(self.img.pixels, self.pixels_in, gui.frame)
            for i in range(1, len(self.engines)):
                self.engines[i].process(buffers[(i + 1) % 2], buffers[i % 2], gui.frame)
                # if i < len(self.engines) - 1:
                #     self.engines[i + 1].set_pixels_in(self.engines[i].pixels_out)

            gui.set_image(buffers[(len(self.engines)-1) % 2])

            gui.show()
