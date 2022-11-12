from obj_class.bullet import *


class Obj:
    def __init__(self):
        self.x, self.y = 0, 0  # 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈
        self.img = None

    def put_img(self, file):
        self.img = load_image(file)

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)


class RealObj(Obj):
    x_gap = None  # x - stand_x
    hit_x_gap = None  # hit_x - stand_x
    y_gap = None  # y - stand_y
    hit_y_gap = None  # hit_y - stand_y

    def __init__(self):
        super().__init__()
        self.hit_y = None
        self.hit_x = None
        self.hit_sy = None
        self.hit_sx = None
        self.stand_x, self.stand_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.
        self.stand_sx, self.stand_sy = 0, 0  # 유닛이 지나갈 수 있는 발판 크기
        self.dir = 0  # 바라보고 있는방향 0 이 북쪽 0~15 16가지

    def get_stand_box(self):
        return self.stand_x - self.stand_sx, self.stand_y - self.stand_sy, self.stand_x + self.stand_sx, self.stand_y + self.stand_sy

    def x_update(self):
        self.x = self.stand_x + self.x_gap
        self.hit_x = self.stand_x + self.hit_x_gap

    def y_update(self):
        self.y = self.stand_y + self.y_gap
        self.hit_y = self.stand_y + self.hit_y_gap

    def x_move(self, x):
        self.stand_x += x
        self.x += x
        self.hit_x += x

    def y_move(self, y):
        self.stand_y += y
        self.y += y
        self.hit_y += y

    def x_move_point(self, x):
        self.stand_x = x
        self.x_update()

    def y_move_point(self, y):
        self.stand_y = y
        self.y_update()

    def move_point(self, x, y):
        self.stand_x = x
        self.x_update()
        self.stand_y = y
        self.y_update()

    def get_left(self):
        return self.stand_x - self.stand_sx

    def get_right(self):
        return self.stand_x + self.stand_sx

    def get_top(self):
        return self.stand_y + self.stand_sy

    def get_bottom(self):
        return self.stand_y - self.stand_sy

    def get_hit_left(self):
        return self.hit_x - self.hit_sx

    def get_hit_right(self):
        return self.hit_x + self.hit_sx

    def get_hit_top(self):
        return self.hit_y + self.hit_sy

    def get_hit_bottom(self):
        return self.hit_y - self.hit_sy
