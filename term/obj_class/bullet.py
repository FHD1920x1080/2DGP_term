from pico2d import*
from func import*
import game_world
import play_state
import random
import math
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
    img = []
    def __init__(self, player, x2, y2):
        self.x1, self.y1 = self.get_bullet_start(player)  # x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.x2  # 현재 좌표
        self.speed = player.bullet_speed  # 생성되는 곳에서 마린의 탄속으로 초기화해주고 있음.
        self.t = 0  # 브리즌헴 직선 변수
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        if self.r == 0:
            return False#조준한 위치가 출발점과 같을 때 이동불가
        self.num = self.get_bullet_num(get_rad(self.x1, self.y1, self.x2, self.y2))
        self.img = Bullet_32.img[self.num]
        #self.sx, self.sy = self.get_bullet_size(self.num)
        self.exist = True #충돌 수 False로 바꿔줄 변수

    def x_move(self, x):
        self.x += x
        self.x1 += x
        self.x2 += x

    def y_move(self, y):
        self.y += y
        self.y1 += y
        self.y2 += y

    def move(self):
        self.t += 1 * (self.speed / self.r)
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2
        pass

    def show(self):
        self.img.draw(self.x, self.y)

    def get_bullet_start(self, player):
        if player.unit_type == 0:# 마린일 때 1 은 골리앗
            x, y = player.stand_x, player.stand_y + 14
            if player.look_now < 10:
                x += 8
                y += 4
            elif player.look_now > 26:
                x -= 8
                y += 4

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


    @staticmethod
    def load_resource():
        for i in range(0, 32):
            Bullet_32.img.append(load_image("resource\\bullet\\" + str(i) + ".png"))
        Effect.load_resource()

class Effect():
    crash_img = None
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
        Effect.crash_img.clip_draw(0, self.img_now_y, 80, 80, self.x, self.y)

    @staticmethod
    def load_resource():
        Effect.crash_img = load_image('resource\\marine\\attack_effect_blue.png')