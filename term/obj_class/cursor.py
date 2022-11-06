import pico2d
import play_state

class Cursor:
    img = None
    cross_hair_img = None

    def __init__(self):
        if Cursor.img == None:
            Cursor.img = pico2d.load_image('resource\\image\\arrowx200.png')
        self.img_now = [2, 2]  # 스프라이트 좌표
        self.x = round(play_state.window_size[0] / 2)
        self.y = round(play_state.window_size[1] / 2)
        self.frame = 0

    def show(self):
        self.img.clip_draw(self.img_now[0] + self.frame * 44, self.img_now[1], 40, 42, self.x + 20, self.y - 21)