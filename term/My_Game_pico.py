from pico2d import *

import random
import math

# 1. 게임 초기화
window_size = [900, 900]
open_canvas(window_size[0], window_size[1])
background_img = load_image('tile.png')


# 2. 게임창 옵션 설정

# 3. 게임 내 필요한 설정

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
    def __init__(self, marine, x2, y2):
        self.x1, self.y1 = self.get_bullet_start(marine)#x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.x2  # 현재 좌표
        self.speed = marine.bullet_speed  # 생성되는 곳에서 마린의 탄속으로 초기화해주고 있음.
        self.t = 0 # 브리즌헴 변수
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리

        self.num = self.get_bullet_num(get_rad(self.x1, self.y1, self.x2, self.y2))
        self.img = load_image("bullet_blue32\\" + str( self.num ) + ".png")
        self.sx, self.sy = self.get_bullet_size(self.num)

    def put_img(self, file):
        self.img = load_image(file)  # 지금은 총알 하나씩 읽어들이고 있어서 크게 나쁘지 않은데, 전체 스프라이트 하나 읽고 좌표값만 바꾸는게 나은지 아직 모름.
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈

    def move(self):
        self.t += 1 * (self.speed / self.r)
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2

    def show(self):
        self.img.clip_draw(0, 0, self.sx, self.sy, self.x, self.y)

    def get_bullet_start(self, marine):
        x, y = 0, 0
        if marine.look_now < 17:
            if marine.look_now == 0:
                x = marine.x + 8
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

    def get_bullet_num(self, rad):
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

    def get_bullet_size(self, num):
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

class Obj:
    def __init__(self):
        self.x, self.y = 0, 0  # 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈

    def put_img(self, file):
        self.img = load_image(file)

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)

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
    list = []
    effect_img = load_image('attack_effect_blue.png')
    img = load_image('marine250x2_blue.png')
    hit_sound = load_wav('hit_sound\\06.wav')
    hit_sound.set_volume(6)

    shoot_sound00 = load_wav('bullet_sound\\00.wav')
    shoot_sound00.set_volume(16)
    shoot_sound01 = load_wav('bullet_sound\\01.wav')
    shoot_sound01.set_volume(16)
    shoot_sound02 = load_wav('bullet_sound\\02.wav')
    shoot_sound02.set_volume(16)
    shoot_sound03 = load_wav('bullet_sound\\03.wav')
    shoot_sound03.set_volume(16)

    def __init__(self):
        super().__init__()
        self.bullet_list = []  # 발사된 총알 리스트
        self.effect_list = []  # 총알과 오브젝트의 충돌 시 생성된 이펙트 리스트
        self.hp = 100  # 체력
        self.AD = 1  # 공격력
        self.img = Marine.img
        self.sx, self.sy = 110, 85  # 그려줄 스프라이트 크기
        self.img_now = [30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)]  # 스프라이트 좌표
        self.hit_sx, self.hit_sy = 48, 72  # 마린의 히트박스 크기
        self.stand_x = round(window_size[0] / 2)  # 마린이 서있는 좌표
        self.stand_y = round(window_size[0] / 2)
        self.x = self.stand_x  # 마린을 그려줄 좌표
        self.y = self.stand_y + 20
        self.stand_sx = 36  # 마린이 밟을 수 있는 땅의 넓이
        self.stand_sy = 36
        self.hit_x = self.x  # 마린의 히트박스 중앙 좌표
        self.hit_y = self.y
        self.speed = 3  # 이동속도
        self.left_move = False  # 왼쪽으로 가는키가 눌렸는지
        self.right_move = False
        self.up_move = False
        self.down_move = False
        self.shoot_able = False  # 마우스 좌클릭이 눌렸는지
        self.move_able = True  # 움직일 수 있는 상태인지
        self.Wmove_able = True  # 움직일 수 있다면 가로로 움직이는지
        self.Hmove_able = True  # 움직일 수 있다면 세로로 움직이는지, 가로와 세로가 같이 움직일때 즉 대각선으로 이동할때 이동속도에 0.707을 곱해주기 위함
        self.idle = True  # 아무것도 안하고 있는지
        self.shoot_idle = True  # 총을 안쏘고 있는지(걸어다니는걸로는 안풀림)
        self.shoot_frame = 0  # 연사력과, 점사구현을 위한 프레임
        self.move_frame = 0  # 마린의 걸어다니는 애니메이션을 위한 프레임
        self.idle_frame = 0  # 아무것도 안한 시간만큼의 프레임
        self.shoot_idle_frame = 0  # 총을 안쏜 시간만큼의 프레임
        self.bullet_speed = 20  # 탄속
        self.moving_attack = False  # 1이면 움직이면서 공격 가능 g키
        self.nfs = 6  # 몇프레임당 공격이 나갈건지
        self.n_shot = 1  # 산탄량
        self.accuracy = 10  # 총의 정확도, 정확이는 오차율 0이 가장 높은 스텟
        self.interrupted_fire = 5  # 몇점사, 쏘는 시간만큼 쉼
        self.magazine_gun = False  # 연사모드
        self.LEFT_DOWN = False  # 마우스 왼쪽버튼이 눌렸었는지 선입력 체크하기위한 변수
        self.LEFT_UP = True  # 마우스버튼이 눌렸다가 때졌는지 선입력 체크하기위한 변수 # 스무스한 점사 무빙을 위해 필요함

    def play_shoot_sound(self):
        i = random.randint(0, 3)
        if i == 0:
            Marine.shoot_sound00.play()
        elif i == 1:
            Marine.shoot_sound01.play()
        elif i == 2:
            Marine.shoot_sound02.play()
        elif i == 3:
            Marine.shoot_sound03.play()

    def play_hit_sound(self):
        Marine.hit_sound.play()

    def handle_events(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
                else:
                    self.LEFT_DOWN = True
                    self.LEFT_UP = False
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
                else:
                    self.LEFT_UP = True
                    self.LEFT_DOWN = False

        if event.type == SDL_KEYDOWN:

            if event.key == SDLK_a:
                self.left_move = True
            elif event.key == SDLK_d:
                self.right_move = True
            if event.key == SDLK_w:
                self.up_move = True
            elif event.key == SDLK_s:
                self.down_move = True
            if event.key == SDLK_e:
                self.bullet_speed += 1
            if event.key == SDLK_q:
                self.bullet_speed -= 1
            if event.key == SDLK_r:
                self.nfs -= 1
                if self.nfs <= 0:
                    self.nfs = 1
            if event.key == SDLK_f:
                self.nfs += 1
            if event.key == SDLK_g:
                if self.moving_attack == False:
                    self.moving_attack = True
                elif self.moving_attack == True:
                    self.moving_attack = False
            if event.key == SDLK_1:
                if self.magazine_gun == True:
                    self.magazine_gun = False
                    self.nfs //= 2
                    self.LEFT_DOWN = False
                    self.LEFT_UP = False
                    self.shoot_idle = True
                    self.shoot_idle_frame = 0
                    if self.nfs <= 0:
                        self.nfs = 1
            if event.key == SDLK_2:
                if self.magazine_gun == False:
                    self.magazine_gun = True
                    self.nfs *= 2
            if event.key == SDLK_SPACE:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
                else:
                    self.LEFT_DOWN = True
                    self.LEFT_UP = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.left_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            elif event.key == SDLK_d:
                self.right_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            if event.key == SDLK_w:
                self.up_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            elif event.key == SDLK_s:
                self.down_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            if event.key == SDLK_SPACE:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
                else:
                    self.LEFT_UP = True
                    self.LEFT_DOWN = False

    def check_magazine(self):
        if self.magazine_gun == False:  # 점사모드일때
            if self.LEFT_UP == True:
                if self.shoot_frame // (self.nfs * self.interrupted_fire) % 2 != 0:
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
            if self.LEFT_DOWN == True:
                if self.shoot_frame == 0:
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False

    def get_look_now(self, rad):
        if rad >= 0:  # 1, 2 사분면
            if rad < 0.1963:  # 우측
                return 8
            elif rad < 0.589:
                return 6
            elif rad < 1.0517:
                return 4
            elif rad < 1.3844:
                return 2
            # elif rad < 1.5708:
            #     return 0
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

    def move(self):
        if self.move_able == True:
            if (self.left_move == True and self.right_move == False) or (
                    self.left_move == False and self.right_move == True):
                self.Wmove_able = True
            else:
                self.Wmove_able = False
            if (self.up_move == True and self.down_move == False) or (
                    self.up_move == False and self.down_move == True):
                self.Hmove_able = True
            else:
                self.Hmove_able = False
            if self.Wmove_able == True and self.Hmove_able == True:
                speed = 0.707
            else:
                speed = 1
            if self.Wmove_able == True:
                if self.left_move == True:
                    if self.stand_x - self.speed * speed <= round(self.stand_sx / 2):
                        self.x_move(round(self.stand_sx / 2) - self.stand_x)
                    else:
                        self.x_move(- self.speed * speed)
                        if not self.shoot_able:
                            self.img_now = 30 + 320 * 12, 1460 - (160 * self.move_frame)
                            self.idle = False
                else:  # self.right_move == True:
                    if self.stand_x + self.speed * speed >= window_size[0] - round(self.stand_sx / 2):
                        self.x_move(window_size[0] - (self.stand_x + round(self.stand_sx / 2)))
                    else:
                        self.x_move(self.speed * speed)
                        if not self.shoot_able:
                            self.img_now = 30 + 320 * 4, 1460 - (160 * self.move_frame)
                            self.idle = False
            if self.Hmove_able == True:
                if self.up_move == True:
                    if self.stand_y >= window_size[1] - round(self.stand_sy / 2):
                        self.y_move(window_size[1] - (self.stand_y + round(self.stand_sy / 2)))
                    else:
                        self.y_move(self.speed * speed)
                        if not self.shoot_able:
                            if self.Wmove_able == True:
                                if self.left_move == True:
                                    self.img_now = 30 + 320 * 14, 1460 - (160 * self.move_frame)
                                    self.idle = False
                                elif self.right_move == True:
                                    self.img_now = 30 + 320 * 2, 1460 - (160 * self.move_frame)
                                    self.idle = False
                            else:
                                self.img_now = 30, 1460 - (160 * self.move_frame)
                                self.idle = False
                else:
                    if self.stand_y <= round(self.stand_sy / 2):
                        self.y_move(round(self.stand_sy / 2) - self.stand_y)
                    else:
                        self.y_move(- self.speed * speed)
                        if not self.shoot_able:
                            if self.Wmove_able == True:
                                if self.left_move == True:
                                    self.img_now = 30 + 320 * 10, 1460 - (160 * self.move_frame)
                                    self.idle = False
                                elif self.right_move == True:
                                    self.img_now = 30 + 320 * 6, 1460 - (160 * self.move_frame)
                                    self.idle = False
                            else:
                                self.img_now = 30 + 320 * 8, 1460 - (160 * self.move_frame)
                                self.idle = False

    def shoot(self):
        if self.shoot_able == True:
            if self.magazine_gun == False:
                if (self.shoot_frame) // (self.nfs * self.interrupted_fire) % 2 != 0:  # 점사 구현
                    return
            if self.shoot_frame % self.nfs == 0:  # self.nfs은 마린이 몇프레임마다 쏠건지 1이 가장 빠름
                # 여기에 사운드
                self.play_shoot_sound()
                for i in range(self.n_shot):
                    a = get_rad(self.x, self.y, cursor.x, cursor.y)
                    self.look_now = marine.get_look_now(a)  # 각도를 가지고 마린이 바라볼 방향 정함.
                    x2, y2 = cursor.x + random.randint(-self.accuracy, self.accuracy), cursor.y + random.randint(
                        -self.accuracy, self.accuracy)
                    bullet = Bullet_32(marine, x2, y2)
                    self.bullet_list.append(bullet)
                    self.shoot_idle = False
                    self.idle = False
                    self.img_now = 30 + (160 * self.look_now), 1620  # 격발 이미지
            elif self.shoot_frame % self.nfs == self.nfs // 2:
                self.img_now = 30 + (160 * self.look_now), 1780  # 견착 이미지
        else:
            self.shoot_idle = True

    def state_update(self):
        self.move()
        self.shoot()
        self.shoot_frame += 1  # 0~59
        if self.magazine_gun == False:
            if self.shoot_idle == True:
                self.shoot_idle_frame += 1
                if self.shoot_idle_frame > self.nfs * self.interrupted_fire - 1:
                    self.shoot_frame = 0
            else:
                self.shoot_idle_frame = 0

        if self.idle:
            self.idle_frame += 1
        else:
            self.idle_frame = 0

class Effect(Obj):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_now_y = random.randint(3, 14) * 80  # 1120  # 스프라이트 좌표
        self.frame = 0  # 100이 되면 저글링 시체 사라짐

    def anim(self):
        if self.frame < 4:
            self.img_now_y -= 80
        self.frame += 1

    def show(self):
        Marine.effect_img.clip_draw(0, self.img_now_y, 80, 80, self.x, self.y)

class Zergling(RealObj):
    sum = 0
    list = []
    die_list = []
    sx = 80
    sy = 78
    hit_sx = 44
    hit_sy = 40
    hp = 3
    speed = 3
    img = load_image("zerglingx200x2.png")
    die_img = load_image("die_zergling.png")

    def __init__(self, x, y):
        super().__init__()
        self.hp = Zergling.hp
        # self.put_img("zerglingx200x2.png")
        self.img_now = [692, 1138]  ##86, 84 씩 옮겨야 함
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
        self.speed = Zergling.speed
        self.move_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)

    def show(self):
        Zergling.img.clip_draw(self.img_now[0], self.img_now[1], Zergling.sx, Zergling.sy, self.x, self.y)

    def show_All(self):
        for zg in Zergling.die_list:
            zg.show()
        for zg in Zergling.list:
            zg.show()

    def stop(self):
        self.img_now = self.img_now[0], 1138

    def get_speed(self):
        if self.move_frame == 0:
            return 1
        elif self.move_frame == 1:
            return 2
        elif self.move_frame == 2:
            return 5
        elif self.move_frame == 3:
            return 4
        elif self.move_frame == 4:
            return 4
        elif self.move_frame == 5:
            return 3
        elif self.move_frame == 6:
            return 2

    def move_down(self):
        i = Zergling.get_speed(self) * self.speed / 3
        self.y_move(- i)
        self.img_now = 692, 1138 - 84 * self.move_frame
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라

    def move_left_down(self):
        i = Zergling.get_speed(self) * self.speed / 3
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
        i = Zergling.get_speed(self) * self.speed / 3
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
    die_sound = load_wav('zzedth01.wav')
    die_sound.set_volume(8)

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.img_now_x = 2  # 스프라이트 좌표
        self.die_frame = 0  # 100이 되면 저글링 시체 사라짐

    def die_anim(self):
        if self.die_frame < 7:
            self.img_now_x = 2 + self.die_frame * 136
        self.die_frame += 1

    def show(self):
        Zergling.die_img.clip_draw(self.img_now_x, 0, 130, 106, self.x, self.y)

    def play_sound(self):
        Die_Zergling.die_sound.play()

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
    if b.hp <= 0:
        return False
    if (a.x >= b.hit_x - b.hit_sx / 2) and (a.x <= b.hit_x + b.hit_sx / 2) and (a.y >= b.hit_y - b.hit_sy / 2) and (
            a.y <= b.hit_y + b.hit_sy / 2):
        return True
    else:
        return False

def get_rad(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

def marien_rotate():  # 현재 이미지와 움직임을 입력할때 바뀔 이미지의 갭을 메꾸기 위한 함수 자연스럽게 회전하둣이,근데 절대 오래걸리면 안됨, 항상 0.1초가 걸리게 조절해도 됨.
    pass  # 양쪽 회전 해야할 정도를 비교해서 짧은쪽 우선, 180도 회전해야하면 항상 우회전

def handle_events():
    global SB
    for event in get_events():
        if event.type == SDL_QUIT:
            SB = 1
        if event.type == SDL_MOUSEMOTION:
            cursor.x, cursor.y = event.x, window_size[1] - 1 - event.y
            cursor.draw_x = cursor.x + 20
            cursor.draw_y = cursor.y - 21
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                SB = 1
        for marine in Marine.list:
            marine.handle_events(event)
    for marine in Marine.list:
        marine.check_magazine()


def make_zergling():
    if random.random() > 0.95:
        Zergling.sum += 1
        zergling = Zergling(random.randrange(round(Zergling.sx / 2), window_size[0] - round(Zergling.sx / 2)),
                            window_size[1] + Zergling.sy)
        Zergling.list.append(zergling)

def zergling_list_move():
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
            j = zgl.direction
            zgl.direction = random.randrange(0, 4)
            if j == 0 and zgl.direction != 0:  # 멈춰있었다가 움직이면 무브프레임 초기화
                zgl.move_frame = 0
            if zgl.direction == 0:
                zgl.direction_rand_time = zgl.time + random.randrange(10, 30)
            else:
                zgl.direction_rand_time = zgl.time + random.randrange(50, 200)
    if len(zd_list) > 1:
        print(len(zd_list))
    zd_list.sort(reverse=True)
    for d in zd_list:
        del Zergling.list[d]

def bullet_move_crash_chack():
    for marine in Marine.list:
        db_list = []
        dz_list = []
        for i in range(len(marine.bullet_list)):  # 불릿을 이동 시킨 후 범위탈출 및 충돌 체크
            blt = marine.bullet_list[i]
            blt.move()
            if blt.y > window_size[1] + 60 or blt.y < - 60 or blt.x > window_size[
                0] + 60 or blt.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
                db_list.append(i)  # 총알이 범위 밖으로 나갔으니 삭제 리스트에 추가
            else:  # 나간 총알이랑은 충돌 체크 할 필요 없으니 안나간 것만 충돌체크
                for j in range(len(Zergling.list)):
                    zgl = Zergling.list[j]
                    if bullet_crash(blt, zgl) == True:
                        attack_effect = Effect(blt.x, blt.y)
                        marine.effect_list.append(attack_effect)
                        marine.play_hit_sound()
                        db_list.append(i)
                        blt.sx = 0  # 불릿 크기를 0으로 만듦, 겹쳐있는 저글링 동시에 패는걸 막기 위해,
                        zgl.hp -= marine.AD
                        if zgl.hp <= 0:
                            Zergling.sum -= 1
                            dz_list.append(j)
                            # zgl.hit_sx = 0  # 저글링의 크기도 0으로 만듦, 동시에 여러발 흡수하느걸 막기 위해, 충돌체크 조건문에서 걸러짐 # hp 검사로 조건 바꿈
                        break  # 이제 사라진 불sa릿이기 때문에 다른 저글링이랑 체크 할 필요 없음
                    # elif 다른 유닛 충돌 체크 할 구문
        dz_list.sort(reverse=True)
        db_list.sort(reverse=True)
        for dz in dz_list:
            die_zergling = Die_Zergling(Zergling.list[dz].stand_x, Zergling.list[dz].stand_y - 5)
            die_zergling.play_sound()
            Zergling.die_list.append(die_zergling)  # 죽은 저글링 리스트에 추가함
            del Zergling.list[dz]  # 실제 저글링은 삭제
        for db in db_list:
            del marine.bullet_list[db]  # 충돌하거나 나갔던 불릿들 삭제

def show_All():
    Zergling.show_All(Zergling)
    for marine in Marine.list:
        for blt in marine.bullet_list:
            blt.show()

    for marine in Marine.list:
        marine.show()
    for marine in Marine.list:
        for eft in marine.effect_list:
            eft.show()
    cursor.show()

def animation(frame):
    if frame % 4 == 0:
        for marine in Marine.list:
            marine.move_frame = (marine.move_frame + 1) % 8

    if (frame + every_3frame) % 3 == 0:  # 3프레임마다 저글링 사망 애니메이션 프레임 증가하는 구간
        dz2_list = []
        for i in range(len(Zergling.die_list)):
            Zergling.die_list[i].die_anim()
            if Zergling.die_list[i].die_frame > FPS:  # 일정 시간이 지난 시체 3초
                dz2_list.append(i)
        dz2_list.sort(reverse=True)
        for dz2 in dz2_list:
            del Zergling.die_list[dz2]

    if (frame + every_6frame) % 6 == 0:
        for zgl in Zergling.list:
            zgl.move_frame = (zgl.move_frame + 1) % 7  # 저글링 무브 프레임
        for marine in Marine.list:
            de_list = []
            for i in range(len(marine.effect_list)):
                marine.effect_list[i].anim()
                if marine.effect_list[i].frame > 4:  # 마린 공격 이펙트 프레임
                    de_list.append(i)
            de_list.sort(reverse=True)
            for de in de_list:
                del marine.effect_list[de]

    if frame % 10 == 0:
        cursor.frame = (cursor.frame + 1) % 5  # 커서 프레임

SB = 0
FPS = 100
frame = 0
for asdasd in range(3):
    marine1 = Marine()
    marine1.x_move(50*asdasd)
    Marine.list.append(marine1)
for asdasd in range(3):
    marine1 = Marine()
    marine1.x_move(50*asdasd)
    marine1.y_move(-50)
    Marine.list.append(marine1)
for asdasd in range(3):
    marine1 = Marine()
    marine1.x_move(50*asdasd)
    marine1.y_move(-50*2)
    Marine.list.append(marine1)
cursor = Cursor()
hide_cursor()
every_6frame = 0
every_3frame = 0

while SB == 0:  # 종료 조건 1초에 한번만 검사
    for frame in range(0, FPS):
        # FPS 설정, 배경 초기화
        SDL_Delay(7)
        clear_canvas()
        background_img.clip_draw(0, 0, 1500, 1000, window_size[0] // 2, window_size[1] // 2)

        # 각종 입력 감지
        handle_events()
        # 입력에 따른 중인공 변화
        for marine in Marine.list:
            marine.state_update()
        # 확률에 따른 적 생성 및 이동
        make_zergling()
        zergling_list_move()
        # 주인공의 공격과 적 충돌체크
        bullet_move_crash_chack()

        # 4-4. 그리기
        show_All()
        animation(frame)  # 애니메이션 재생 출력은 아님 상태값만 변경
        update_canvas()

    # 일정 프레임마다 수행해줘야 하는 조건문에 필요함 # FPS에 대해 나누어 떨어지면 필요 없음. ex) FPS가 100일때 2,4,5,10,25 등은 설정 안해줘도 됨.
    # 애니메이션 재생에 필요
    every_6frame = (FPS + every_6frame) % 6
    every_3frame = (FPS + every_3frame) % 3

# 5. 게임 종료
close_canvas()
