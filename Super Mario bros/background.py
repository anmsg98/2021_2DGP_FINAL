from pico2d import *

class Background:
    def __init__(self, imageName):
        self.imageName = imageName
        self.image = load_image(imageName)
        self.target = None
        self.cw, self.ch = get_canvas_width(), get_canvas_height()
        self.win_rect = 0, 0, self.cw, self.ch
        self.center = self.image.w // 2, self.image.h // 2
        hw, hh = self.cw // 2, self.    ch // 2
        self.boundary = hw, hh, self.image.w - hw, self.image.h - hh
    def set_target(self, target):
        self.target = target
        self.update()
    def draw(self):
        self.image.clip_draw_to_origin(*self.win_rect, 0, 0)
    def update(self):
        if self.target is None:
            return
        tx, ty = self.target.pos
        sl = round(tx - self.cw / 2)
        sb = round(ty - self.ch / 2)
        self.win_rect = sl, sb, self.cw, self.ch
    def get_boundary(self):
        return self.boundary
    def translate(self, point):
        x, y = point
        l, b, r, t = self.win_rect
        return l + x, b + y
    def to_screen(self, point):
        # return self.cw // 2, self.ch // 2
        x, y = point
        l, b, r, t = self.win_rect
        return x - l, y - b

    # def to_screen(self, point):
    #     hw, hh = self.cw // 2, self.ch // 2
    #     x, y = point

    #     if x > self.image.w - hw:
    #         x = self.cw - (self.image.w - x)
    #     elif x > hw:
    #         x = self.cw // 2

    #     if y > self.image.h - hh:
    #         y = self.ch - (self.image.h - y)
    #     elif y > hh:
    #         y = self.ch // 2

    #     return x, y

class FixedBackground:
    def __init__(self, level):
        self.image = load_image("resource/BG%d.png" % level)
        self.cw, self.ch = get_canvas_width(), get_canvas_height()
        self.window_left, self. window_bottom = 0, 0
        self.center_object = None

    def set_center_object(self, boy):
        self.center_object = boy

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.cw, self.ch,
            0, 0)

    def update(self):
        self.window_left = clamp(0,
             int(self.center_object.x) - self.cw // 2,
             self.image.w - self.cw)

        self.window_bottom = clamp(0,
            int(self.center_object.y) - self.ch // 2,
            self.image.h - self.ch)
