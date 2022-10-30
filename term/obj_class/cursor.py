import play_state

class Cursor:
    arrow_img = None
    cross_hair_img = None

    def __init__(self):
        self.img = Cursor.arrow_img
        self.img_now = [2, 2]  # 스프라이트 좌표
        self.x = round(play_state.window_size[0] / 2)
        self.y = round(play_state.window_size[1] / 2)
        self.draw_x = self.x + 20
        self.draw_y = self.y - 21
        self.frame = 0

    def show(self):
        self.img.clip_draw(self.img_now[0] + self.frame * 44, self.img_now[1], 40, 42, self.draw_x, self.draw_y)