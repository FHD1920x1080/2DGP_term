from pico2d import *

import random
import math

# 1. 게임 초기화
window_size = [900, 900]
open_canvas(window_size[0], window_size[1])


# 2. 게임창 옵션 설정

# 3. 게임 내 필요한 설정
class Obj:
    def __init__(self):
        self.x, self.y = 0, 0  # 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈
        self.img_now = [0, 0]  # 스프라이트 좌표
    def put_img(self, file):
        self.img = load_image(file)

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)


class Bullet_anim:
    def __init__(self):
        self.frame = random.randint(0, 4)
        self.x, self.y = 0, 0  # 좌표
        self.x1, self.y1 = 0, 0  # 좌표
        self.x2, self.y2 = 0, 0  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.speed = 5
        self.t = 0

    def put_img(self, file):
        self.img = load_image(file)
        self.img_now = [0, 0]  # 스프라이트 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈

    def move(self):
        i = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** (1 / 2)
        self.t += 1 * (self.speed / i)
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)

    def add_hit_size(self, x, y):
        self.hit_sx, self.hit_sy = x, y

    def anim(self):
        self.img_now[0] = self.frame * self.sx
        self.frame = (self.frame + 1) % 5


class Bullet_32:
    def __init__(self,x1,y1,x2,y2):
        self.x1, self.y1 = x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.x2  # 현재 좌표
        self.speed = 5
        self.t = 0
        self.r = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** (1 / 2)
    def put_img(self, file):
        self.img = load_image(file)
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈

    def move(self):
        self.t += 1 * (self.speed / self.r)
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2

    def show(self):
        self.img.clip_draw(0, 0, self.sx, self.sy, self.x, self.y)


class Cursor:
    def __init__(self):
        self.img = load_image('arrowx200.png')
        self.img_now = [2, 2]  # 스프라이트 좌표
        self.x = round(window_size[0] / 2)
        self.y = round(window_size[1] / 2)
        self.draw_x = self.x + 20
        self.draw_y = self.y - 21
        self.frame = 0

    def show(self):
        self.img.clip_draw(self.img_now[0] + self.frame * 44, self.img_now[1], 40, 42, self.draw_x, self.draw_y)


class RealObj(Obj):
    def __init__(self):
        super().__init__()
        self.stand_x, self.stand_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.
        self.stand_sx, self.stand_sy = 0, 0  # 유닛이 지나갈 수 있는 발판 크기
        self.look_now = 0  # 바라보고 있는방향 0 이 북쪽 0~15 16가지

    def x_move(self, x):
        self.x += x
        self.stand_x += x
        self.hit_x += x

    def y_move(self, y):
        self.y += y
        self.stand_y += y
        self.hit_y += y


class Marine(RealObj):
    bullet_list = []

    def __init__(self):
        super().__init__()
        self.put_img('marine250x2_blue.png')
        self.sx, self.sy = 100, 85
        self.img_now = [30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)]
        self.hit_sx, self.hit_sy = 48, 72
        # marine.img = load_image('marine.png')
        # marine.re_size(48,72)
        self.stand_x = round(window_size[0] / 2)
        self.stand_y = round(window_size[0] / 2)
        self.x = self.stand_x
        self.y = self.stand_y + 20
        self.stand_sx = 36
        self.stand_sy = 36
        self.hit_x = self.x
        self.hit_y = self.y
        self.speed = 3
        self.left_move = False
        self.right_move = False
        self.up_move = False
        self.down_move = False
        self.shoot = False
        self.move_able = True
        self.Wmove_able = True
        self.Hmove_able = True
        self.idle = True
        self.shoot_idle = True
        self.shoot_frame = 0
        self.move_frame = 0
        self.idle_frame = 0
        self.shoot_idle_frame = 0
        self.bullet_speed = 20
        self.moving_attack = False  # 1이면 움직이면서 공격 가능 g키
        self.nfs = 6  # 몇프레임당 공격이 나갈건지
        self.accuracy = 10 # 0이 가장 높은 스텟
        self.interrupted_fire = 5 # 점사, 쏘는 시간만큼 쉼
        self.magazine_gun = False
        self.LEFT_DOWN = False
        self.LEFT_UP = True

class Zergling(RealObj):
    sum = 0
    list = []
    die_list = []
    sx = 80
    sy = 78
    hit_sx = 44
    hit_sy = 40
    hp = 1

    def __init__(self, x, y):
        super().__init__()
        self.hp = Zergling.hp
        self.put_img("zerglingx200x2.png")
        self.img_now = [692, 1138]  ##86, 84 씩 옮겨야 함
        self.sx = Zergling.sx
        self.sy = Zergling.sy
        self.stand_x = x
        self.stand_y = y
        self.x = self.stand_x
        self.y = self.stand_y
        self.hit_x = self.x
        self.hit_y = self.y
        self.hit_sx = Zergling.hit_sx
        self.hit_sy = Zergling.hit_sx
        self.stand_sx = self.hit_sx
        self.stand_sy = self.hit_sy
        self.speed = 0
        self.move_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)

    def show_All(self):
        for zg in Zergling.die_list:
            zg.show()
        for zg in Zergling.list:
            zg.show()

    def stop(self):
        self.img_now = self.img_now[0], 1138

    def get_speed(self):
        if zgl.move_frame == 0:
            return 1
        elif zgl.move_frame == 1:
            return 2
        elif zgl.move_frame == 2:
            return 5
        elif zgl.move_frame == 3:
            return 4
        elif zgl.move_frame == 4:
            return 4
        elif zgl.move_frame == 5:
            return 3
        elif zgl.move_frame == 6:
            return 2

    def move_down(self):
        i = Zergling.get_speed(self)
        self.y_move(- i)
        self.img_now = 692, 1138 - 84 * self.move_frame
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라

    def move_left_down(self):
        i = Zergling.get_speed(self)
        self.y_move(- i * 0.707)
        self.x_move(- i * 0.707)
        self.img_now = 692 + 86 * 2, 1138 - 84 * self.move_frame
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        if self.stand_x - self.speed * 0.707 <= round(self.stand_sx / 2):
            self.x_move(round(self.stand_sx / 2) - self.stand_x)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        i = Zergling.get_speed(self)
        # i = zgl.move_frame - 6 #0 1 2 3 4 5 6 -3 -2 -1 0 1 2 3
        self.y_move(- i * 0.707)
        self.x_move(+ i * 0.707)
        self.img_now = 520, 1138 - 84 * self.move_frame
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        if self.stand_x + self.speed * 0.707 >= window_size[0] - round(self.stand_sx / 2):
            self.x_move(window_size[0] - (self.stand_x + round(self.stand_sx / 2)))
            self.direction = random.randrange(1, 3)
class Die_Zergling(Obj):
    def __init__(self, x, y):
        self.put_img("zerglingx200x2.png")
        self.x = x
        self.y = y
        self.img_now_x = 5  # 스프라이트 좌표
        self.die_frame = 0
    def die_anim(self):
        if self.die_frame == 5:
            self.x -= 2
        if self.die_frame < 7:
            self.y -= 4
            self.img_now_x = 5 + self.die_frame * 136
        self.die_frame += 1
    def show(self):
        self.img.clip_draw(self.img_now_x, 18, 128, 106, self.x, self.y)

def crash(a, b):
    if a.hit_sx <= 0 or b.hit_sx <= 0:
        return False
    if a.hit_x + (a.hit_sx / 2) >= b.hit_x - (b.hit_sx / 2) and a.hit_x - (a.hit_sx / 2) <= b.hit_x + (
            b.hit_sx / 2) and a.hit_y + (a.hit_sy / 2) >= b.hit_y - (b.hit_sy / 2) and a.hit_y - (
            a.hit_sy / 2) <= b.hit_y + (b.hit_sy / 2):
        return True
    else:
        return False


def bullet_crash(a, b):
    if a.sx <= 0:
        return False
    if (a.x >= b.hit_x - b.hit_sx / 2) and (a.x <= b.hit_x + b.hit_sx / 2) and (a.y >= b.hit_y - b.hit_sy / 2) and (
            a.y <= b.hit_y + b.hit_sy / 2):
        return True
    else:
        return False


def get_rad(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


def get_bullet_num(rad):
    # a5625 = 0.09817477
    if rad >= 0:  # 1, 2 사분면
        if rad <= 1.7089711:  # 1사분면
            if rad > 1.40262156:  # -0.07
                return 0
            elif rad > 1.15627201:  # -0.12
                return 1
            elif rad > 0.89992247:  # -0.18
                return 2
            elif rad > 0.70357293:  # -0.18
                return 3
            elif rad > 0.50722339:  # -0.18
                return 4
            elif rad > 0.41087385:  # -0.08
                return 5
            elif rad > 0.29452431:
                return 6
            elif rad > 0.09817477:
                return 7
            else:  # >0 오른쪽
                return 8
        else:  # 2사분면
            if rad < 1.93532064:
                return 31
            elif rad < 2.20167018:
                return 30
            elif rad < 2.41801972:
                return 29
            elif rad < 2.65436926:
                return 28
            elif rad < 2.7807188:
                return 27
            elif rad < 2.88706834:
                return 26
            elif rad < 3.04341788:
                return 25
            else:  # >0 왼쪽
                return 24
    else:  # rad < 0 3,4분면
        if rad >= -1.6689711:  # 4사분면
            if rad < -1.47262156:
                return 16
            elif rad < -1.15627201:
                return 15
            elif rad < -0.92992247:
                return 14
            elif rad < -0.70357293:
                return 13
            elif rad < -0.52722339:
                return 12
            elif rad < -0.36087385:
                return 11
            elif rad < -0.22452431:
                return 10
            elif rad < -0.09817477:
                return 9
            else:  # 오른쪽
                return 8
        else:  # 3사분면
            if rad > -1.98532064:  # -0.12
                return 17
            elif rad > -2.24167018:  # 18
                return 18
            elif rad > -2.43801972:  # 18
                return 19
            elif rad > -2.63436926:  # 18
                return 20
            elif rad > -2.7307188:  # 08
                return 21
            elif rad > -2.90706834:  # 06
                return 22
            elif rad > -3.04341788:
                return 23
            else:  # 왼쪽
                return 24


def get_bullet_size(num):
    if num < 16:
        if num < 8:
            if num == 0:
                return 5, 50
            elif num == 1:
                return 16, 52
            elif num == 2:
                return 32, 49
            elif num == 3:
                return 42, 41
            elif num == 4:
                return 50, 38
            elif num == 5:
                return 57, 31
            elif num == 6:
                return 49, 19
            else:  # num == 7:
                return 50, 10
        elif num == 15:
            return 17, 51
        elif num == 14:
            return 26, 44
        elif num == 13:
            return 39, 40
        elif num == 12:
            return 52, 35
        elif num == 11:
            return 49, 21
        elif num == 10:
            return 54, 17
        elif num == 9:
            return 53, 10
        else:  # num == 8
            return 52, 5
    else:  # num >= 16
        if num < 24:
            if num == 23:
                return 50, 10
            elif num == 22:
                return 49, 19
            elif num == 21:
                return 57, 31
            elif num == 20:
                return 50, 38
            elif num == 19:
                return 43, 41
            elif num == 18:
                return 32, 49
            elif num == 17:
                return 16, 51
            else:  # num == 16:
                return 5, 51
        elif num == 31:
            return 17, 50
        elif num == 30:
            return 26, 44
        elif num == 29:
            return 40, 40
        elif num == 28:
            return 52, 35
        elif num == 27:
            return 49, 21
        elif num == 26:
            return 54, 17
        elif num == 25:
            return 53, 10
        else:  # num == 24
            return 52, 5


def get_bullet_start():
    x, y = 0, 0
    if marine.look_now < 17:
        if marine.look_now == 0:
            x = marine.x + 4
            y = marine.y + 30
        elif marine.look_now == 2:
            x = marine.x + 20
            y = marine.y + 28
        elif marine.look_now == 4:
            x = marine.x + 34
            y = marine.y + 22
        elif marine.look_now == 6:
            x = marine.x + 40
            y = marine.y + 10
        elif marine.look_now == 8:
            x = marine.x + 40
            y = marine.y - 2
        elif marine.look_now == 10:
            x = marine.x + 40
            y = marine.y - 12
        elif marine.look_now == 12:
            x = marine.x + 34
            y = marine.y - 26
        elif marine.look_now == 14:
            x = marine.x + 15
            y = marine.y - 30
        else:  # 16
            x = marine.x - 5
            y = marine.y - 30
    else:  # marine.look_now >= 17
        if marine.look_now == 30:
            x = marine.x - 20
            y = marine.y + 28
        elif marine.look_now == 28:
            x = marine.x - 34
            y = marine.y + 22
        elif marine.look_now == 26:
            x = marine.x - 40
            y = marine.y + 10
        elif marine.look_now == 24:
            x = marine.x - 40
            y = marine.y - 2
        elif marine.look_now == 22:
            x = marine.x - 40
            y = marine.y - 12
        elif marine.look_now == 20:
            x = marine.x - 34
            y = marine.y - 26
        elif marine.look_now == 18:
            x = marine.x - 15
            y = marine.y - 30
        else:  # 17
            x = marine.x + 5
            y = marine.y - 30

    return x, y


def get_look_now(rad):
    if rad >= 0:  # 1, 2 사분면
        if rad < 0.1963:  # 우측
            return 8
        elif rad < 0.589:
            return 6
        elif rad < 1.0517:
            return 4
        elif rad < 1.4444:
            return 2
        elif rad < 1.5708:
            return 0
        elif rad < 1.8:
            return 0
        elif rad < 2.0898:
            return 30
        elif rad < 2.5525:
            return 28
        elif rad < 2.9452:
            return 26
        else:  # rad <= 3.1415:
            return 24
    else:  # 3,4분면
        if rad > -0.0663:  # 우측
            return 8
        elif rad > -0.31:
            return 10
        elif rad > -0.7017:
            return 12
        elif rad > -1.2044:
            return 14
        elif rad > -1.5708:
            return 16
        elif rad > -1.9371:
            return 17
        elif rad > -2.4398:
            return 18
        elif rad > -2.8315:
            return 20
        elif rad > -3.0752:
            return 22
        else:  # rad >= -3.1415:
            return 24


def marien_rotate():  # 현재 이미지와 움직임을 입력할때 바뀔 이미지의 갭을 메꾸기 위한 함수 자연스럽게 회전하둣이,근데 절대 오래걸리면 안됨, 항상 0.1초가 걸리게 조절해도 됨.
    pass  # 양쪽 회전 해야할 정도를 비교해서 짧은쪽 우선, 180도 회전해야하면 항상 우회전


def handle_events():
    global shoot_frame
    global SB
    for event in get_events():
        if event.type == SDL_QUIT:
            SB = 1
        if event.type == SDL_MOUSEMOTION:
            cursor.x, cursor.y = event.x, window_size[1] - 1 - event.y
            cursor.draw_x = cursor.x + 20
            cursor.draw_y = cursor.y - 21
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if marine.magazine_gun == True:
                    marine.shoot_frame = 0
                    marine.shoot = True
                    if marine.moving_attack == False:
                        marine.move_able = False
                else:
                    marine.LEFT_DOWN = True
                    marine.LEFT_UP = False
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                if marine.magazine_gun == True:
                    marine.shoot_frame = 0
                    marine.shoot = False
                    marine.idle = True
                    marine.move_able = True
                    marine.img_now = 30 + 160 * marine.look_now, 1780
                else:
                    marine.LEFT_UP = True
                    marine.LEFT_DOWN = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                SB = 1
            if event.key == SDLK_a:
                marine.left_move = True
            elif event.key == SDLK_d:
                marine.right_move = True
            if event.key == SDLK_w:
                marine.up_move = True
            elif event.key == SDLK_s:
                marine.down_move = True
            if event.key == SDLK_SPACE:
                marine.shoot = True
                #marine.shoot_frame = 0
                # marine.move_able = False
            if event.key == SDLK_e:
                marine.bullet_speed += 1
            if event.key == SDLK_q:
                marine.bullet_speed -= 1
            if event.key == SDLK_r:
                marine.nfs -= 1
                if marine.nfs <= 0:
                    marine.nfs = 1
            if event.key == SDLK_f:
                marine.nfs += 1
            if event.key == SDLK_g:
                if marine.moving_attack == False:
                    marine.moving_attack = True
                elif marine.moving_attack == True:
                    marine.moving_attack = False
            if event.key == SDLK_1:
                if marine.magazine_gun == True:
                    marine.magazine_gun = False
                    marine.nfs //= 2
                    marine.LEFT_DOWN = False
                    marine.LEFT_UP = False
                    marine.shoot_idle = True
                    marine.shoot_idle_frame = 0
                    if marine.nfs <= 0:
                        marine.nfs = 1
            if event.key == SDLK_2:
                if marine.magazine_gun == False:
                    marine.magazine_gun = True
                    marine.nfs *= 2
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                marine.left_move = False
                marine.idle = True
                marine.img_now = marine.img_now[0], 2100
            elif event.key == SDLK_d:
                marine.right_move = False
                marine.idle = True
                marine.img_now = marine.img_now[0], 2100
            if event.key == SDLK_w:
                marine.up_move = False
                marine.idle = True
                marine.img_now = marine.img_now[0], 2100
            elif event.key == SDLK_s:
                marine.down_move = False
                marine.idle = True
                marine.img_now = marine.img_now[0], 2100
            if event.key == SDLK_SPACE:
                marine.shoot = False
                marine.move_able = True
                marine.img_now = 30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)


def marine_move():
    if marine.move_able == True:
        if (marine.left_move == True and marine.right_move == False) or (
                marine.left_move == False and marine.right_move == True):
            marine.Wmove_able = True
        else:
            marine.Wmove_able = False
        if (marine.up_move == True and marine.down_move == False) or (
                marine.up_move == False and marine.down_move == True):
            marine.Hmove_able = True
        else:
            marine.Hmove_able = False
        if marine.Wmove_able == True and marine.Hmove_able == True:
            speed = 0.707
        else:
            speed = 1
        if marine.Wmove_able == True:
            if marine.left_move == True:
                if marine.stand_x - marine.speed * speed <= round(marine.stand_sx / 2):
                    marine.x_move(round(marine.stand_sx / 2) - marine.stand_x)
                else:
                    marine.x_move(- marine.speed * speed)
                    if not marine.shoot:
                        marine.img_now = 30 + 320 * 12, 1460 - (160 * marine.move_frame)
                        marine.idle = False
            else:  # marine.right_move == True:
                if marine.stand_x + marine.speed * speed >= window_size[0] - round(marine.stand_sx / 2):
                    marine.x_move(window_size[0] - (marine.stand_x + round(marine.stand_sx / 2)))
                else:
                    marine.x_move(marine.speed * speed)
                    if not marine.shoot:
                        marine.img_now = 30 + 320 * 4, 1460 - (160 * marine.move_frame)
                        marine.idle = False
        if marine.Hmove_able == True:
            if marine.up_move == True:
                if marine.stand_y >= window_size[1] - round(marine.stand_sy / 2):
                    marine.y_move(window_size[1] - (marine.stand_y + round(marine.stand_sy / 2)))
                else:
                    marine.y_move(marine.speed * speed)
                    if not marine.shoot:
                        if marine.Wmove_able == True:
                            if marine.left_move == True:
                                marine.img_now = 30 + 320 * 14, 1460 - (160 * marine.move_frame)
                                marine.idle = False
                            elif marine.right_move == True:
                                marine.img_now = 30 + 320 * 2, 1460 - (160 * marine.move_frame)
                                marine.idle = False
                        else:
                            marine.img_now = 30, 1460 - (160 * marine.move_frame)
                            marine.idle = False
            else:
                if marine.stand_y <= round(marine.stand_sy / 2):
                    marine.y_move(round(marine.stand_sy / 2) - marine.stand_y)
                else:
                    marine.y_move(- marine.speed * speed)
                    if not marine.shoot:
                        if marine.Wmove_able == True:
                            if marine.left_move == True:
                                marine.img_now = 30 + 320 * 10, 1460 - (160 * marine.move_frame)
                                marine.idle = False
                            elif marine.right_move == True:
                                marine.img_now = 30 + 320 * 6, 1460 - (160 * marine.move_frame)
                                marine.idle = False
                        else:
                            marine.img_now = 30 + 320 * 8, 1460 - (160 * marine.move_frame)
                            marine.idle = False


def marine_shoot():
    if marine.shoot == True:
        if marine.magazine_gun == False:
            if (marine.shoot_frame) // (marine.nfs * marine.interrupted_fire) % 2 != 0:# 점사 구현
                return
        if marine.shoot_frame % marine.nfs == 0:  # marine.nfs은 마린이 몇프레임마다 쏠건지 1이 가장 빠름
            # 여기에 사운드
            a = get_rad(marine.x, marine.y, cursor.x, cursor.y)
            marine.look_now = get_look_now(a)  # 각도를 가지고 마린이 바라볼 방향 정함.
            x1, y1 = get_bullet_start()  # 마린이 바라보고 있는방향의 총구에서 총알은 발사됨, 이것때문에 자연스럽게 쏘지만, 마린 가까이에 커서를 두고 쏘면 이상하게 됨.
            x2, y2 = cursor.x + random.randint(-marine.accuracy, marine.accuracy), cursor.y + random.randint(-marine.accuracy, marine.accuracy)
            b = get_rad(x1, y1, x2, y2)
            bullet_num = (get_bullet_num(b))  # 마린과 커서의 각도로 어떤 불릿 이미지를 쓸건지 정함. 그냥 동그란 총알이나 쓸까 ㅋㅋ
            bullet = Bullet_32(x1, y1, x2, y2)
            bullet.put_img("bullet_blue32\\" + str(bullet_num) + ".png")
            bullet.sx, bullet.sy = get_bullet_size(bullet_num)
            bullet.speed = marine.bullet_speed  # 마린의 스탯에서 가져옴
            marine.bullet_list.append(bullet)
            marine.shoot_idle = False
            marine.idle = False
            marine.img_now = 30 + (160 * marine.look_now), 1620  # 격발 이미지
        elif marine.shoot_frame % marine.nfs == marine.nfs // 2:
            marine.img_now = 30 + (160 * marine.look_now), 1780  # 견착 이미지
    else:
        marine.shoot_idle = True
def make_zergling():
    if random.random() > 0.95:
        Zergling.sum += 1
        zergling = Zergling(random.randrange(round(Zergling.sx / 2), window_size[0] - round(Zergling.sx / 2)),
                            window_size[1] + Zergling.sy)
        # zergling.put_img("zerglingx200.png")
        # bullet.show()
        Zergling.list.append(zergling)
        # print(zergling.direction)
        # print(zergling.hit_x, zergling.hit_y, zergling.hit_sx, zergling.hit_sy)
        # print(Zergling.sum)


SB = 0
FPS = 100
frame = 0
marine = Marine()
cursor = Cursor()
hide_cursor()
evrey_6frame = 0
evrey_3frame = 0
while SB == 0:
    for frame in range(0, FPS):
        print(marine.idle_frame, marine.shoot_idle_frame, marine.shoot_frame)

        # 4-1. FPS 설정
        clear_canvas()
        # delay(0.01)
        SDL_Delay(6)
        # 4-2. 각종 입력 감지
        # events = get_events()
        handle_events()
        if marine.magazine_gun == False:
            if marine.LEFT_UP == True :
                if marine.shoot_frame // (marine.nfs * marine.interrupted_fire) % 2 != 0:
                    marine.shoot = False
                    marine.idle = True
                    marine.move_able = True
                    marine.img_now = 30 + 160 * marine.look_now, 1780
            if marine.LEFT_DOWN == True:
                if marine.shoot_frame == 0:
                    marine.shoot = True
                    if marine.moving_attack == False:
                        marine.move_able = False

        marine_move()
        marine_shoot()
        # print(event)
        marine.shoot_frame += 1  # 0~59
        if marine.magazine_gun == False:
            if marine.shoot_idle == True:
                marine.shoot_idle_frame += 1
                if marine.shoot_idle_frame > marine.nfs * marine.interrupted_fire-1:
                    marine.shoot_frame = 0
            else:
                marine.shoot_idle_frame = 0

        if marine.idle:
            marine.idle_frame += 1
        else:
            marine.idle_frame = 0
        if (frame + evrey_6frame) % 4 == 0:
            marine.move_frame = (marine.move_frame + 1) % 8
        make_zergling()

        zd_list = []
        for i in range(len(Zergling.list)):  # 저글링 다운
            zgl = Zergling.list[i]
            zgl.time += 1
            if (zgl.direction == 0):
                zgl.stop()
            elif (zgl.direction == 1):
                if zgl.move_down() == 1:
                    zd_list.append(i)
                    Zergling.sum -= 1
            if (zgl.direction == 2):
                if zgl.move_left_down() == 1:
                    zd_list.append(i)
                    Zergling.sum -= 1
            elif (zgl.direction == 3):
                if zgl.move_right_down() == 1:
                    zd_list.append(i)
                    Zergling.sum -= 1
            if zgl.time % zgl.direction_rand_time == 0:
                i = zgl.direction
                zgl.direction = random.randrange(0, 4)
                if i == 0 and zgl.direction != 0:  # 멈춰있었다가 움직이면 무브프레임 초기화
                    zgl.move_frame = 0
                if zgl.direction == 0:
                    zgl.direction_rand_time = zgl.time + random.randrange(10, 30)
                else:
                    zgl.direction_rand_time = zgl.time + random.randrange(50, 200)
        for d in zd_list:
            del Zergling.list[d]
        if (frame + evrey_6frame) % 6 == 0:
            # for blt in marine.bullet_list: #dragbull.png
            #     blt.anim()
            for zgl in Zergling.list:
                zgl.move_frame = (zgl.move_frame + 1) % 7
        # print(len(Zergling.list))

        db_list = []
        dz_list = []
        for i in range(len(marine.bullet_list)):  # 불릿을 이동 시킨 후 범위탈출 및 충돌 체크
            blt = marine.bullet_list[i]
            blt.move()
            if blt.y > window_size[1] + 60 or blt.y < - 60 or blt.x > window_size[0] + 60 or blt.x < - 60:# 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
                db_list.append(i)  # 총알이 범위 밖으로 나갔으니 삭제 리스트에 추가
            else:  # 나간 총알이랑은 충돌 체크 할 필요 없으니 안나간 것만 충돌체크
                for j in range(len(Zergling.list)):
                    zgl = Zergling.list[j]
                    if bullet_crash(blt, zgl) == True:
                        db_list.append(i)
                        blt.sx = 0  # 불릿 크기를 0으로 만듦, 충돌체크 조건문에서 걸러내기 위해
                        zgl.hp -= 1
                        if (zgl.hp <= 0):
                            Zergling.sum -= 1
                            dz_list.append(j)
                        break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음

        dz_list = list(set(dz_list))  # 혹시 모를 중복 제거
        db_list = list(set(db_list))
        try:
            dz_list.reverse()
            db_list.reverse()
            for dz in dz_list:
                die_zergling = Die_Zergling(Zergling.list[dz].stand_x, Zergling.list[dz].stand_y)#die_zergling 이라는 저글링 객체를 만듦, 메모리가 크므로 작은 클래스로 수정할 예정 위치만 받으면 되기 때문, 사망 애니메이션도 저글링 스프라이트에서 따로 잘라서 써야겠다.
                Zergling.die_list.append(die_zergling)#죽은 저글링 리스트에 추가함
                del Zergling.list[dz]#실제 저글링은 삭제
            for db in db_list:
                del marine.bullet_list[db]#충돌하거나 나갔던 불릿들 삭제
        except:
            pass

        if (frame + evrey_3frame) % 3 == 0:# 3프레임마다 저글링 사망 애니메이션 프레임 증가하는 구간
            dz2_list = []
            for i in range(len(Zergling.die_list)):
                Zergling.die_list[i].die_anim()
                if Zergling.die_list[i].die_frame > FPS :  # 일정 시간이 지난 시체 3초
                    dz2_list.append(i)
            try:
                dz2_list.reverse()
                for dz2 in dz2_list:
                    del Zergling.die_list[dz2]
            except:
                pass
        # 4-4. 그리기
        # screen.fill(color)
        Zergling.show_All(Zergling)
        # for zg in Zergling.die_list:
        #     zg.show()
        # for zg in Zergling.list:
        #     zg.show()
        for blt in marine.bullet_list:
            blt.show()
        marine.show()
        cursor.show()
        if frame % 10 == 0:
            cursor.frame = (cursor.frame + 1) % 5
        update_canvas()
        # print(frame+evrey_6frame)

    evrey_6frame = (FPS + evrey_6frame) % 6
    evrey_3frame = (FPS + evrey_3frame) % 3

# 5. 게임 종료
close_canvas()