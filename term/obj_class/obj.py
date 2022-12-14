from pico2d import *
from func import *
from sound import *
from ui import *
import random
import math
import game_world
import play_state

# 레이어
MAP_FLOOR, FLOOR_EFFECT, GROUND_BULLET, GROUND_OBJ, BOMB_EFFECT, GROUND_CRASH_EFFECT, AIR_BULLET, FLY_OBJ, AIR_CRASH_EFFECT = range(
    9)


# GROUND_OBJ 는 정렬 후 출력, 커서는 하나밖에 없으니 그냥 마지막에 그리면 됨.


class Obj:
    layer = AIR_CRASH_EFFECT

    def __init__(self):
        self.print_x, self.print_y = 0, 0  # 그릴 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈
        self.img = None

    def put_img(self, file):
        self.img = load_image(file)

    def x_move(self, x):
        self.print_x += x

    def y_move(self, y):
        self.y += y

    def show(self):
        pass
        # .img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.print_x, self.print_y)


class GroundObj:
    layer = GROUND_OBJ

    img = None
    print_sx = 0  # 그려줄 스프라이트 크기
    print_sy = 0
    stand_sx = 0  # 발판 크기 반쪽
    stand_sy = 0
    hit_sx = 0  # 히트박스 크기 반쪽
    hit_sy = 0
    print_x_gap = 0  # x - stand_x
    hit_x_gap = 0  # hit_x - stand_x
    print_y_gap = 0  # y - stand_y
    hit_y_gap = 0  # hit_y - stand_y

    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.
    collision_type = 1  # 기본 충돌 남을 못밀어냄

    def __init__(self):
        # self.print_x, self.print_y = 0, 0  # 그릴 좌표
        self.time = None
        self.hp = None
        self.state = None
        self.speed = None
        self.anger_speed = None
        self.img_now = [0, 0]
        self.stand_x, self.stand_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x(),
                           self.print_y())
        # draw_rectangle(*self.get_stand_box())
        # draw_rectangle(*self.get_hit_box())

    def update(self):
        pass

    def suffer(self, damage, owner=None, attack_type=0): #attack_type 0 : 일반, 1 : 폭발
        self.hp -= damage
        pass

    def die(self):
        pass

    def hit_x(self):
        return self.stand_x + self.hit_x_gap

    def hit_y(self):
        return self.stand_y + self.hit_y_gap

    def print_x(self):
        return self.stand_x + self.print_x_gap

    def print_y(self):
        return self.stand_y + self.print_y_gap

    def get_stand_box(self):
        return self.stand_x - self.stand_sx, self.stand_y - self.stand_sy, self.stand_x + self.stand_sx, self.stand_y + self.stand_sy

    def get_hit_box(self):
        return self.hit_x() - self.hit_sx, self.hit_y() - self.hit_sy, self.hit_x() + self.hit_sx, self.hit_y() + self.hit_sy

    def x_move(self, x):
        self.stand_x += x

    def y_move(self, y):
        self.stand_y += y

    def x_move_point(self, x):
        self.stand_x = x

    def y_move_point(self, y):
        self.stand_y = y

    def move_point(self, x, y):
        self.stand_x = x
        self.stand_y = y

    def get_stand_left(self):
        return self.stand_x - self.stand_sx

    def get_stand_right(self):
        return self.stand_x + self.stand_sx

    def get_stand_top(self):
        return self.stand_y + self.stand_sy

    def get_stand_bottom(self):
        return self.stand_y - self.stand_sy

    def get_hit_left(self):
        return self.hit_x() - self.hit_sx

    def get_hit_right(self):
        return self.hit_x() + self.hit_sx

    def get_hit_top(self):
        return self.hit_y() + self.hit_sy

    def get_hit_bottom(self):
        return self.hit_y() - self.hit_sy

    def dir_adjust(self):
        pass


class Effect:
    layer = GROUND_OBJ
    collision = False
    collision_type = 0  # 충돌 안함.

    img = None
    sound = None
    print_sx = 0  # 그려줄 스프라이트 시트에서 얼마나 잘라다가 쓸꺼냐
    print_sy = 0
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 0  # 스프라이트에서 어느 만큼씩 옮길건지
    max_frame = 0  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 10  # 몇프레임마다 재생할것인가

    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 0

    def __init__(self):
        self.exist = True  # 존재함
        self.img_now = [0, 0]
        self.stand_x, self.stand_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.
        self.print_x, self.print_y = self.stand_x + self.print_x_gap, self.stand_y + self.print_y_gap
        self.cur_frame = 0
        self.time = 0
        game_world.ground_obj.append(self)

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x, self.print_y)

    def update(self):
        self.time += 1  # O으로 시작하므로 바로 애니메이션을 재생시켜버림. 첫번째 이미지가 스킵되는걸 막기 위해 먼저 올려줌
        if self.time % self.any_frame_rate == 0:
            self.anim()

    def anim(self):
        self.cur_frame += 1  # 맥스랑 맞춰주기 위해서 먼저 프레임 올림.
        if self.cur_frame < self.max_frame:
            if self.anim_direction == 'w':
                self.img_now[0] += self.next_gap
            else:
                self.img_now[1] -= self.next_gap
        else:  # 애니메이션이 끝
            self.exist = False

    def x_move(self, x):
        self.print_x += x

    def y_move(self, y):
        self.print_y += y

    def play_sound(self):
        self.sound.play()

    def die(self):  # 사라지면서 해줄 게 있으면 재정의 해서 써야함.
        pass


class FlyObj:  #
    layer = FLY_OBJ

    img = None
    shadow = None
    print_sx = 0  # 그려줄 스프라이트 크기
    print_sy = 0
    stand_sx = 0  # 발판 크기 반쪽
    stand_sy = 0
    hit_sx = 0  # 히트박스 크기 반쪽
    hit_sy = 0
    stand_x_gap = 0  # x - stand_x
    hit_x_gap = 0  # hit_x - stand_x
    stand_y_gap = 0  # y - stand_y
    hit_y_gap = 0  # hit_y - stand_y

    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.

    def __init__(self):
        # self.print_x, self.print_y = 0, 0  # 그릴 좌표
        self.state = None
        self.speed = None
        self.anger_speed = None
        self.hp = None
        self.img_now = [0, 0]
        self.print_x, self.print_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.s

    def show(self):
        self.shadow.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.stand_x(),
                              self.stand_y())
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x,
                           self.print_y)
        # draw_rectangle(*self.get_hit_box())

    def update(self):
        pass

    def suffer(self, damage):  # 피격당하면 해줄것
        self.hp -= damage

    def die(self):  # 죽으면서 해줄것
        pass

    def hit_x(self):
        return self.print_x + self.hit_x_gap

    def hit_y(self):
        return self.print_y + self.hit_y_gap

    def stand_x(self):
        return self.print_x - self.stand_x_gap

    def stand_y(self):
        return self.print_y - self.stand_y_gap

    def get_hit_box(self):
        return self.hit_x() - self.hit_sx, self.hit_y() - self.hit_sy, self.hit_x() + self.hit_sx, self.hit_y() + self.hit_sy

    def x_move(self, x):
        self.print_x += x

    def y_move(self, y):
        self.print_y += y

    def x_move_point(self, x):
        self.print_x = x

    def y_move_point(self, y):
        self.print_y = y

    def move_point(self, x, y):
        self.print_x = x
        self.print_y = y

    def get_hit_left(self):
        return self.hit_x() - self.hit_sx

    def get_hit_right(self):
        return self.hit_x() + self.hit_sx

    def get_hit_top(self):
        return self.hit_y() + self.hit_sy

    def get_hit_bottom(self):
        return self.hit_y() - self.hit_sy
