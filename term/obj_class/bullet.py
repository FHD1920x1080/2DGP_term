from pico2d import *
from func import *
import game_world
import play_state
import random
import math


class Drag_Bull:
    img = None
    sx = 0
    sy = 0

    def __init__(self, player):
        self.x1, self.y1 = player.x, player.y + 5  # x1, y1  # 시작 좌표
        self.x2, self.y2 = player.bull_x2, player.bull_y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.max_speed = player.bullet_speed
        self.speed = self.max_speed - 20
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        if self.r == 0:
            del self
            return False
        self.img_now_x = 0
        self.frame = 0
        self.current_size = player.bull_size  # 100% 기준

    def show(self):
        Drag_Bull.img.clip_composite_draw(self.img_now_x, 0, 20, 18, 0, '', self.x, self.y, 20 * self.current_size,
                                          20 * self.current_size)

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
        if self.speed < self.max_speed:
            self.speed += 0.5
        else:
            self.speed = self.max_speed

    @staticmethod
    def list_move():
        db_list = []
        for i in range(len(game_world.explosive_bullet_list)):  # 불릿을 이동 시킨 후 범위탈출 및 충돌 체크
            blt = game_world.explosive_bullet_list[i]
            blt.move()
            blt.anim()
            if blt.y > play_state.window_size[1] + 60 or blt.y < - 60 or blt.x > play_state.window_size[
                0] + 60 or blt.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
                db_list.append(i)  # 총알이 범위 밖으로 나갔으니 삭제 리스트에 추가
            elif blt.t > 0.99:  # 여기서 폭발
                attack_effect = Drag_Bull_Effect(blt.x, blt.y, blt.current_size)
                game_world.effect_list.append(attack_effect)
                Drag_Bull_Effect.play_bomb_sound()
                db_list.append(i)
                for j in range(len(game_world.ground_enemy)):
                    em = game_world.ground_enemy[j]
                    if tir_rect_crash(attack_effect, em):
                        em.hp -= blt.AD
                        if em.hp <= 0:
                            play_state.die_ground_list.append(j)
        db_list.sort(reverse=True)
        for db in db_list:
            del game_world.explosive_bullet_list[db]  # 충돌하거나 나갔던 불릿들 삭제

    def anim(self):
        if play_state.frame % 10 == 0:
            self.img_now_x = self.frame * 20
            self.frame = (self.frame + 1) % 5

    @staticmethod
    def load_resource():
        Drag_Bull.img = load_image('resource\\bullet\\dragbull.png')
        Drag_Bull_Effect.load_resource()


class Drag_Bull_Effect:
    img = None
    bomb_sound = None
    rect_sx = [0, 0, 0]
    rect_sy = [0, 0, 0]
    rect_sx[0] = 34
    rect_sy[0] = 54
    rect_sx[1] = 76
    rect_sy[1] = 24
    rect_sx[2] = (rect_sx[0] + rect_sx[1]) // 2
    rect_sy[2] = (rect_sy[1] + rect_sy[1]) // 2

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.img_now_x = 0
        self.frame = 0
        self.current_size = size

    def get_left(self, i):
        return self.x - Drag_Bull_Effect.rect_sx[i] * self.current_size

    def get_right(self, i):
        return self.x + Drag_Bull_Effect.rect_sx[i] * self.current_size

    def get_bottom(self, i):
        return self.y - Drag_Bull_Effect.rect_sy[i] * self.current_size

    def get_top(self, i):
        return self.y + Drag_Bull_Effect.rect_sy[i] * self.current_size

    def anim(self):
        self.img_now_x += 191
        self.frame += 1
        if self.frame > 10:  # 마린 공격 이펙트 프레임
            game_world.effect_list.remove(self)
            del self

    def show(self):
        Drag_Bull_Effect.img.clip_composite_draw(self.img_now_x, 0, 188, 150, 0, '', self.x, self.y,
                                                 188 * self.current_size, 150 * self.current_size)

    @staticmethod
    def play_bomb_sound():
        Drag_Bull_Effect.bomb_sound.play()

    @staticmethod
    def load_resource():
        Drag_Bull_Effect.img = load_image('resource\\bullet\\protoss_bomb12.png')
        Drag_Bull_Effect.bomb_sound = load_wav('resource\\bullet\\hit_sound\\tbadth1.wav')
        Sound.list.append(Drag_Bull_Effect.bomb_sound)
        Sound.volume_list.append(26)


class Bullet32:
    img = []

    def __init__(self, player, x2, y2):
        self.x1, self.y1 = self.get_bullet_start(player)  # x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.speed = player.bullet_speed
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        if self.r == 0:
            return False  # 조준한 위치가 출발점과 같을 때 이동불가
        self.num = self.get_bullet_num(get_rad(self.x1, self.y1, self.x2, self.y2))
        self.img = Bullet32.img[self.num]
        # self.sx, self.sy = self.get_bullet_size(self.num)
        self.exist = True  # 충돌 수 False로 바꿔줄 변수

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
        if player.unit_type == 0:  # 마린일 때 1 은 골리앗
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
    def list_move_crash_chack():
        db_list = []
        for i in range(len(game_world.bullet_list)):  # 불릿을 이동 시킨 후 범위탈출 및 충돌 체크
            blt = game_world.bullet_list[i]
            blt.move()
            if blt.y > play_state.window_size[1] + 60 or blt.y < - 60 or blt.x > play_state.window_size[
                0] + 60 or blt.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
                db_list.append(i)  # 총알이 범위 밖으로 나갔으니 삭제 리스트에 추가
            else:  # 나간 총알이랑은 충돌 체크 할 필요 없으니 안나간 것만 충돌체크
                for j in range(len(game_world.ground_enemy)):
                    em = game_world.ground_enemy[j]
                    if bullet_crash(blt, em) == True:
                        attack_effect = Bullet32_Effect(blt.x, blt.y)
                        game_world.effect_list.append(attack_effect)
                        # player.play_hit_sound()
                        play_state.sound.Bullet32_hit = True
                        db_list.append(i)
                        blt.exist = False  # 아직 삭제 시킬 수 없으므로 존재변수를 0으로 함, 겹쳐있는 저글링 동시에 패는걸 막기 위해,
                        em.hp -= blt.AD
                        if em.hp <= 0:
                            play_state.die_ground_list.append(j)
                            # zgl.hit_sx = 0  # 저글링의 크기도 0으로 만듦, 동시에 여러발 흡수하느걸 막기 위해, 충돌체크 조건문에서 걸러짐 # hp 검사로 조건 바꿈
                        break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음
        db_list.sort(reverse=True)
        for db in db_list:
            del game_world.bullet_list[db]  # 충돌하거나 나갔던 불릿들 삭제

    @staticmethod
    def load_resource():
        for i in range(0, 32):
            Bullet32.img.append(load_image("resource\\bullet\\" + str(i) + ".png"))
        Bullet32_Effect.load_resource()
        Drag_Bull.load_resource()


class Bullet32_Effect():
    crash_img = None
    hit_sound = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_now_y = random.randint(3, 14) * 80  # 1120  # 스프라이트 좌표
        self.frame = 0  # 100이 되면 저글링 시체 사라짐

    def anim(self):
        self.img_now_y -= 80
        self.frame += 1
        if self.frame > 4:  # 마린 공격 이펙트 프레임
            game_world.effect_list.remove(self)
            del self

    def show(self):
        Bullet32_Effect.crash_img.clip_draw(0, self.img_now_y, 80, 80, self.x, self.y)

    @staticmethod
    def play_hit_sound():
        Bullet32_Effect.hit_sound.play()

    @staticmethod
    def load_resource():
        Bullet32_Effect.crash_img = load_image('resource\\bullet\\attack_effect_red.png')
        Bullet32_Effect.hit_sound = load_wav('resource\\bullet\\hit_sound\\06.wav')
        Sound.list.append(Bullet32_Effect.hit_sound)
        Sound.volume_list.append(6)
