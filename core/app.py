import taichi as ti
import numpy as np
from PIL import Image

import time

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

        max_size = 900
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

        self.keys = set()

    def just_pressed(self, window, key):
        if window.is_pressed(key):
            if key in self.keys:
                return False
            self.keys.add(key)
            return True
        else:
            self.keys.discard(key)
            return False

    def handle_zoom(self, window: ti.ui.Window):
        zoom_proc = None
        for engine in self.engines:
            if engine.processor.__class__.__name__ == 'Zoom':
                zoom_proc = engine.processor

        curr_mouse = window.get_cursor_pos()

        if window.is_pressed(ti.GUI.LMB) and self.zoom_proc is not None and self.last_mouse is not None:
            factor = self.zoom_proc.zoom_amount[None]

            dx = self.last_mouse[0] - curr_mouse[0]
            dy = self.last_mouse[1] - curr_mouse[1]

            if factor < 1.0:
                dx = -dx
                dy = -dy

            self.zoom_proc.center[None][0] += dx / (factor * 0.9)
            self.zoom_proc.center[None][1] += dy / (factor * 0.9)
        
        if self.just_pressed(window, 'c'):
            zoom_proc.zoom_amount[None] *= 1.1
        if self.just_pressed(window, 'v'):
            zoom_proc.zoom_amount[None] *= 0.9

        zoom_proc.zoom_amount[None] = max(0.1, zoom_proc.zoom_amount[None])

    def handle_events(self, window: ti.ui.Window):
        curr_mouse = window.get_cursor_pos()

        self.handle_zoom(window)

        for e in window.get_events():
            pass

        self.last_mouse = curr_mouse

    def run(self):
        window = ti.ui.Window("Axolotl", res=(self.img.width, self.img.height), fps_limit=144)
        canvas = window.get_canvas()
        # gui = ti.GUI("Axolotl", res=(self.img.width, self.img.height))

        total_time = 0
        
        curr_in = self.img.pixels
        curr_out = self.pixels_in

        while window.running:
            start = time.perf_counter()
            self.handle_events(window)

            if window.is_pressed(ti.GUI.ESCAPE):
                break

            for engine in self.engines:
                engine.process(curr_in, curr_out, total_time * 60)

                curr_in = curr_out

                curr_out = self.pixels_out if curr_in is self.pixels_in else self.pixels_in

            canvas.set_image(curr_in)

            window.show()
            
            ti.sync()
            
            end = time.perf_counter()
            total_time += end - start

            curr_in = self.img.pixels
