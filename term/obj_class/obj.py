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
    x_gap = None
    hit_x_gap = None
    y_gap = None
    hit_y_gap = None
    def __init__(self):
        super().__init__()
        self.hit_y = None
        self.hit_x = None
        self.stand_x, self.stand_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.
        self.stand_sx, self.stand_sy = 0, 0  # 유닛이 지나갈 수 있는 발판 크기
        self.look_now = 0  # 바라보고 있는방향 0 이 북쪽 0~15 16가지

    def x_update(self):
        self.x = self.stand_x + self.x_gap
        self.hit_x = self.stand_x + self.hit_x_gap

    def y_update(self):
        self.y = self.stand_y + self.y_gap
        self.hit_y = self.stand_y + self.hit_y_gap

    def x_move(self, x):
        self.x += x
        self.stand_x += x
        self.hit_x += x

    def y_move(self, y):
        self.y += y
        self.stand_y += y
        self.hit_y += y

    def x_move_point(self, x):
        self.stand_x = x
        self.x_update()

    def y_move_point(self, y):
        self.stand_y = y
        self.y_update()

    def move_point(self, x, y):
        a = self.stand_x - self.x
        b = self.stand_x - self.hit_x
        self.stand_x = x
        self.x = x - a
        self.hit_x = x - b

        c = self.stand_y - self.y
        d = self.stand_y - self.hit_y
        self.stand_y = y
        self.y = y - c
        self.hit_y = y - d

    def get_left(self):
        return self.stand_x - self.stand_sx // 2

    def get_right(self):
        return self.stand_x + self.stand_sx // 2

    def get_top(self):
        return self.stand_y + self.stand_sy // 2

    def get_bottom(self):
        return self.stand_y - self.stand_sy // 2
