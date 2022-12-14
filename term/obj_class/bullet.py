import math

import game_world
import play_state
from obj_class.obj import *

pi2 = math.pi * 2


class Bomb(Effect):
    img = None
    print_sx = 0  # 출력할 이미지 x 크기
    print_sy = 0  # 출력할 이미지 y 크기
    print_x_gap = 0  # 입력받은 위치와의 x값 차이
    print_y_gap = 0  # 입력받은 위치와의 y값 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 0  # 다음 이미지와의 갭
    max_frame = 0  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 0  # 몇 프레임마다 재생하는가
    size = 1.0  # 크기 배율

    # 폭발 범위 1사이즈 일때,
    rect_sx = [0, 0, 0]
    rect_sy = [0, 0, 0]
    rect_sx[0] = None  # 세로로 큰 사각형
    rect_sy[0] = None  # 세로로 큰 사각형
    rect_sx[1] = None  # 가로로 큰 사각형
    rect_sy[1] = None  # 가로로 큰 사각형
    rect_sx[2] = None  # 0,1번 사각형의 중간 값
    rect_sy[2] = None  # 0,1번 사각형의 중간 값

    def __init__(self, bullet):
        self.owner = bullet.owner
        self.collision = False
        self.exist = True  # 존재함
        self.print_x = bullet.x + self.print_x_gap
        self.print_y = bullet.y + self.print_y_gap
        self.img_now = [0, 0]
        self.cur_frame = 0
        self.AD = bullet.AD
        self.time = 0
        self.cur_size = bullet.cur_size * self.size  # 배율
        self.cur_size_x = self.cur_size * self.print_sx
        self.cur_size_y = self.cur_size * self.print_sy

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x, self.print_y,
                           self.cur_size_x, self.cur_size_y)

    def get_left(self, i):
        return self.print_x - self.rect_sx[i] * self.cur_size

    def get_right(self, i):
        return self.print_x + self.rect_sx[i] * self.cur_size

    def get_bottom(self, i):
        return self.print_y - self.rect_sy[i] * self.cur_size

    def get_top(self, i):
        return self.print_y + self.rect_sy[i] * self.cur_size

    def anim(self):
        self.cur_frame += 1
        if self.cur_frame < self.max_frame:
            self.img_now[0] += self.next_gap
            if self.cur_frame == 2:
                for obj in game_world.ground_obj:
                    if obj != play_state.player:
                        if tir_rect_crash(self, obj):
                            Bullet32_Effect(obj.stand_x, obj.stand_y, 1)
                            obj.suffer(self.AD, 1, self.owner)
                for obj in game_world.fly_obj:
                    if tir_rect_crash(self, obj):
                        Bullet32_Effect(obj.print_x, obj.print_y, 1, AIR_CRASH_EFFECT)
                        obj.suffer(self.AD, 1, self.owner)
        else:
            self.exist = False

    # def die(self):
    #     pass

class Bullet32:
    orange_img = []  # 얘는 좀 특이하게 스프라이트 시트가 아니고 하나씩 잘라놈
    blue_img = []
    hit_sound = None

    def __init__(self, player, x2, y2):
        self.owner = player
        self.x1, self.y1 = self.get_start_point(player)  # x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.speed = player.bullet_speed
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        if self.r == 0:
            del self
            return
        self.cur_speed = self.speed / self.r
        self.num = self.get_bullet_num(get_rad(self.x1, self.y1, self.x2, self.y2))
        self.img = Bullet32.blue_img[self.num]
        # self.sx, self.sy = self.get_bullet_size(self.num)
        self.exist = True  # 충돌 gn False로 바꿔줄 존재 변수
        game_world.ground_bullet.append(self)

    @staticmethod
    def play_hit_sound():
        Bullet32.hit_sound.play()

    def x_move(self, x):
        self.x += x
        self.x1 += x
        self.x2 += x

    def y_move(self, y):
        self.y += y
        self.y1 += y
        self.y2 += y

    def move(self):
        self.t += self.cur_speed
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2
        pass

    def show(self):
        self.img.draw(self.x, self.y)

    def get_start_point(self, player):
        if player.face_dir < 10:
            return player.stand_x + 8, player.stand_y + 18
        elif player.face_dir > 26:
            return player.stand_x - 8, player.stand_y + 18
        else:
            return player.stand_x, player.stand_y + 14

    @staticmethod
    def get_bullet_num(rad):  # 그냥 쓸까 deg로 고쳐서 할까 정수연산으로 하는게 이득일라나
        # a5625 = 0.09817477
        if rad >= 0:  # 1, 2 사분면
            if rad <= 1.7089711:  # 1사분면
                if rad > 0.50722339:  # -0.18
                    if rad > 0.89992247:  # -0.18
                        if rad > 1.40262156:  # -0.07
                            return 0
                        elif rad > 1.15627201:  # -0.12
                            return 1
                        else:  # rad > 0.89992247:  # -0.18
                            return 2
                    elif rad > 0.70357293:  # -0.18
                        return 3
                    else:  # rad > 0.50722339:  # -0.18
                        return 4
                else:
                    if rad > 0.41087385:  # -0.08
                        return 5
                    elif rad > 0.29452431:
                        return 6
                    elif rad > 0.09817477:
                        return 7
                    else:  # >0 오른쪽
                        return 8
            else:  # 2사분면
                if rad < 2.65436926:
                    if rad < 1.93532064:
                        return 31
                    elif rad < 2.20167018:
                        return 30
                    elif rad < 2.41801972:
                        return 29
                    else:  # rad < 2.65436926:
                        return 28
                else:
                    if rad < 2.7807188:
                        return 27
                    elif rad < 2.88706834:
                        return 26
                    elif rad < 3.04341788:
                        return 25
                    else:  # >0 왼쪽
                        return 24
        else:  # rad < 0 3,4분면
            if rad >= -1.6689711:  # 4사분면
                if rad < -0.52722339:
                    if rad < -0.92992247:
                        if rad < -1.47262156:
                            return 16
                        elif rad < -1.15627201:
                            return 15
                        else:  # rad < -0.92992247:
                            return 14
                    elif rad < -0.70357293:
                        return 13
                    else:  # rad < -0.52722339:
                        return 12
                else:
                    if rad < -0.36087385:
                        return 11
                    elif rad < -0.22452431:
                        return 10
                    elif rad < -0.09817477:
                        return 9
                    else:  # 오른쪽
                        return 8
            else:  # 3사분면
                if rad > -2.63436926:  # 18
                    if rad > -1.98532064:  # -0.12
                        return 17
                    elif rad > -2.24167018:  # 18
                        return 18
                    elif rad > -2.43801972:  # 18
                        return 19
                    else:  # rad > -2.63436926:  # 18
                        return 20
                else:
                    if rad > -2.7307188:  # 08
                        return 21
                    elif rad > -2.90706834:  # 06
                        return 22
                    elif rad > -3.04341788:
                        return 23
                    else:  # 왼쪽
                        return 24

    def update(self):
        self.move()
        self.crash_check()

    def crash_check(self):
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
            self.exist = False
        else:
            for obj in game_world.ground_obj:
                if obj != play_state.player:  # 주인공은 지 몸땡이에서 총알 쏴서 충돌체크 하면 안됨.
                    if bullet_crash(self, obj):
                        play_state.sound.Bullet32_hit = True
                        Bullet32_Effect(self.x, self.y, 1)
                        self.exist = False
                        obj.suffer(self.AD, 0, self.owner)
                        break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음
            for obj in game_world.fly_obj:
                if bullet_crash(self, obj):
                    play_state.sound.Bullet32_hit = True
                    Bullet32_Effect(self.x, self.y, 1)
                    self.exist = False
                    obj.suffer(self.AD, 0, self.owner)
                    break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음

    def die(self):
        pass

    @staticmethod
    def load_resource():
        for i in range(0, 32):
            Bullet32.orange_img.append(load_image("resource\\bullet\\bullet32_orange\\" + str(i) + ".png"))
            Bullet32.blue_img.append(load_image("resource\\bullet\\bullet32_blue\\" + str(i) + ".png"))
        Bullet32_Effect.load_resource()
        Bullet32.hit_sound = load_wav('resource\\bullet\\hit_sound\\06.wav')
        Sound.list.append(Bullet32.hit_sound)
        Sound.volume_list.append(6)
        DragBull.load_resource()
        MutalBullet.load_resource()
        Missile.load_resource()
        ZergBomb.load_resource()

class Bullet32Gol(Bullet32):
    def __init__(self, player):
        self.owner = player
        self.x, self.y = player.shoot_point
        self.speed = player.bullet_speed
        self.AD = player.AD
        rad = player.rad + player.error_rate()
        self.cos = math.cos(rad)
        self.sin = math.sin(rad)
        num = self.get_bullet_num(rad)
        self.img = Bullet32.orange_img[num]
        self.exist = True
        game_world.ground_bullet.append(self)

    @staticmethod
    def play_hit_sound():
        Bullet32.hit_sound.play()

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def update(self):
        self.move()
        self.crash_check()

    def move(self):
        self.x_move(self.cos * self.speed)
        self.y_move(self.sin * self.speed)

    def crash_check(self):
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
            self.exist = False
        else:
            for obj in game_world.ground_obj:
                if obj != play_state.player:  # 주인공은 지 몸땡이에서 총알 쏴서 충돌체크 하면 안됨.
                    if bullet_crash(self, obj):
                        play_state.sound.Bullet32_hit = True
                        Bullet32_Effect(self.x, self.y)
                        self.exist = False
                        obj.suffer(self.AD, 0, self.owner)
                        return

class Bullet32_Effect(Effect):
    img_red = None
    img_blue = None

    print_sx = 80  # 그려줄 스프라이트 시트에서 얼마나 잘라다가 쓸꺼냐
    print_sy = 80
    anim_direction = 'h'  # 스프라이트 이미지 재생 방향
    next_gap = 80  # 스프라이트에서 어느 만큼씩 옮길건지
    max_frame = 4  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6  # 몇프레임마다 재생할것인가

    def __init__(self, x, y, color=0, layer=GROUND_CRASH_EFFECT):
        if color == 1:
            self.img = Bullet32_Effect.img_blue
        else:
            self.img = Bullet32_Effect.img_red
        self.print_x = x
        self.print_y = y
        self.img_now = [0, random.randint(3, 14) * 80]  # 1120  # 스프라이트 좌표
        self.cur_frame = 0
        self.time = 0
        self.exist = True
        game_world.objects[layer].append(self)

    @staticmethod
    def load_resource():
        pass
        Bullet32_Effect.img_red = load_image('resource\\bullet\\bullet_hit_effect_orange.png')
        Bullet32_Effect.img_blue = load_image('resource\\bullet\\bullet_hit_effect_blue.png')
        ZergSpark.load_resource()

class DragBull:
    img = None
    def __init__(self, player):
        self.owner = player
        self.x1, self.y1 = player.print_x(), player.print_y() + 5  # x1, y1  # 시작 좌표
        self.x2, self.y2 = player.bull_x2, player.bull_y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.max_speed = player.bullet_speed
        self.speed = self.max_speed - 20
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        if self.r == 0:
            del self
            return
        play_state.sound.Dragoon_shoot = True
        self.cur_speed = self.speed / self.r
        self.accel = 0.5 / self.r  # t에 더하는 self.cur_speed 에 더할 속도
        self.img_now_x = 0
        self.frame = 0
        self.cur_size = player.bull_size  # 100% 기준
        self.cur_print_size = self.cur_size * 20
        self.exist = True
        game_world.objects[AIR_BULLET].append(self)

    def show(self):
        self.img.clip_draw(self.img_now_x, 0, 20, 18, self.x, self.y, self.cur_print_size,
                           self.cur_print_size)

    def x_move(self, x):
        self.x += x
        self.x1 += x
        self.x2 += x

    def y_move(self, y):
        self.y += y
        self.y1 += y
        self.y2 += y

    def update(self):
        self.move()
        if play_state.frame % 10 == 0:
            self.anim()

    def die(self):
        DragBullEffect(self)
        pass

    def move(self):
        self.t += self.cur_speed
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2
        self.cur_speed += self.accel
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
            self.exist = False
        elif self.t > 0.999:
            self.exist = False

    def anim(self):
        self.img_now_x = self.frame * 20
        self.frame = (self.frame + 1) % 5

    @staticmethod
    def load_resource():
        DragBull.img = load_image('resource\\bullet\\dragbull.png')
        DragBullEffect.load_resource()

class DragBullMarine(DragBull):
    def __init__(self, player):
        self.owner = player
        self.x, self.y = player.print_x(), player.print_y()  # x1, y1  # 시작 좌표
        self.cur_size = player.drag_bull_size * 1.5
        self.speed = 20
        self.AD = player.AD * 2
        self.t = 0
        rad = get_rad(self.x, self.y, play_state.cursor.x, play_state.cursor.y)  # 두 점 사이의 거리
        self.cos = math.cos(rad)
        self.sin = math.sin(rad)
        self.img_now_x = 0
        self.frame = 0
        self.exist = True
        game_world.objects[GROUND_BULLET].append(self)

    def show(self):
        self.img.clip_draw(self.img_now_x, 0, 20, 18, self.x, self.y, 40, 36)

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def update(self):
        self.move()
        self.crash_check()
        if play_state.frame % 10 == 0:
            self.anim()

    def die(self):
        pass

    def move(self):
        self.x_move(self.cos * self.speed)
        self.y_move(self.sin * self.speed)

    def anim(self):
        self.img_now_x = self.frame * 20
        self.frame = (self.frame + 1) % 5

    def crash_check(self):
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
            self.exist = False
        else:
            for obj in game_world.ground_obj:
                if obj != play_state.player:
                    if bullet_crash(self, obj):
                        DragBullEffect(self)
                        play_state.sound.Bullet32_hit = True
                        self.exist = False
                        return
            for obj in game_world.fly_obj:
                if obj != play_state.player:
                    if bullet_crash(self, obj):
                        DragBullEffect(self)
                        play_state.sound.Bullet32_hit = True
                        self.exist = False
                        return

class DragBullEffect(Bomb):
    img = None
    bomb_sound = None

    print_sx = 188  # 출력할 이미지 x 크기
    print_sy = 150  # 출력할 이미지 y 크기
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = -20  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 191  # 다음 이미지와의 갭
    max_frame = 10  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6  # 몇 프레임마다 재생하는가
    size = 1.2  # 크기 배율

    rect_sx = [0, 0, 0]
    rect_sy = [0, 0, 0]
    rect_sx[0] = 34  # 세로로 큰 사각형
    rect_sy[0] = 54  # 세로로 큰 사각형
    rect_sx[1] = 76  # 가로로 큰 사각형
    rect_sy[1] = 24  # 가로로 큰 사각형
    rect_sx[2] = (rect_sx[0] + rect_sx[1]) // 2  # 0,1번 사각형의 중간 값
    rect_sy[2] = (rect_sy[1] + rect_sy[1]) // 2  # 0,1번 사각형의 중간 값

    def __init__(self, bullet):
        super().__init__(bullet)
        play_state.sound.Dragoon_bull_bomb = True
        game_world.objects[BOMB_EFFECT].append(self)

    def anim(self):
        self.cur_frame += 1
        if self.cur_frame < self.max_frame:
            self.img_now[0] += self.next_gap
            if self.cur_frame == 2:
                for obj in game_world.ground_obj:
                    if obj != play_state.player:
                        if tir_rect_crash(self, obj):
                            Bullet32_Effect(obj.stand_x, obj.stand_y, 1)
                            obj.suffer(self.AD, 1, self.owner)
                for obj in game_world.fly_obj:
                    if tir_rect_crash(self, obj):
                        Bullet32_Effect(obj.print_x, obj.print_y, 1, AIR_CRASH_EFFECT)
                        obj.suffer(self.AD, 1, self.owner)
        else:
            self.exist = False

    # def die(self):
    #     pass

    @staticmethod
    def play_bomb_sound():
        DragBullEffect.bomb_sound.play()

    @staticmethod
    def load_resource():
        DragBullEffect.img = load_image('resource\\bullet\\protoss_bomb12.png')
        DragBullEffect.bomb_sound = load_wav('resource\\bullet\\hit_sound\\tbadth1.wav')
        Sound.list.append(DragBullEffect.bomb_sound)
        Sound.volume_list.append(26)

class MutalBullet:
    img = None

    def __init__(self, player, x2, y2):
        self.owner = player
        self.x1, self.y1 = player.print_x, player.print_y  # x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.speed = player.bullet_speed
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        if self.r == 0:
            del self
            return
        #play_state.sound.Dragoon_shoot = True
        self.cur_speed = self.speed / self.r
        self.img_now_x = 15
        self.frame = 0
        self.exist = True
        game_world.objects[AIR_BULLET].append(self)

    def show(self):
        self.img.clip_draw(self.img_now_x, 0, 44, 44, self.x, self.y)

    def x_move(self, x):
        self.x += x
        self.x1 += x
        self.x2 += x

    def y_move(self, y):
        self.y += y
        self.y1 += y
        self.y2 += y

    def update(self):
        self.move()
        self.anim()
    def die(self):
        #DragBullEffect(self)
        pass

    def move(self):
        self.t += self.cur_speed
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
            self.exist = False
        elif self.t > 0.999:
            #여기서 충돌
            if bullet_crash(self, play_state.player):
                play_state.player.suffer(self.AD, 0, self.owner)
                ZergSpark(play_state.player.hit_x(), play_state.player.hit_y())
            MutalHitEffect(self.x, self.y)
            #이펙트 추가
            self.exist = False

    def anim(self):
        self.img_now_x = 15 + self.frame * 72
        self.frame = (self.frame + 1) % 10

    @staticmethod
    def load_resource():
        MutalBullet.img = load_image('resource\\bullet\\mutalbull200.png')
        MutalHitEffect.load_resource()

class ZergBomb(Bomb):
    img = None
    bomb_sound = None

    print_sx = 80  # 출력할 이미지 x 크기
    print_sy = 80  # 출력할 이미지 y 크기
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 15  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 80  # 다음 이미지와의 갭
    max_frame = 10  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 4  # 몇 프레임마다 재생하는가
    size = 2.0  # 크기 배율

    rect_sx = [0, 0, 0]
    rect_sy = [0, 0, 0]
    rect_sx[0] = 22  # 세로로 큰 사각형
    rect_sy[0] = 28  # 세로로 큰 사각형
    rect_sx[1] = 36  # 가로로 큰 사각형
    rect_sy[1] = 16  # 가로로 큰 사각형
    rect_sx[2] = (rect_sx[0] + rect_sx[1]) // 2  # 0,1번 사각형의 중간 값
    rect_sy[2] = (rect_sy[1] + rect_sy[1]) // 2  # 0,1번 사각형의 중간 값

    def __init__(self, bullet):
        super().__init__(bullet)
        self.index = bullet.index
        game_world.objects[BOMB_EFFECT].append(self)
        # play_state.sound.Dragoon_bull_bomb = True

    def anim(self):
        self.cur_frame += 1
        if self.cur_frame < self.max_frame:
            self.img_now[0] += self.next_gap
            if self.cur_frame == 1:
                play_state.sound.Zerg_Bomb = True
            elif self.cur_frame == 3:
                for obj in game_world.ground_obj:
                    if tir_rect_crash(self, obj):
                        ZergSpark(obj.stand_x, obj.stand_y)
                        obj.suffer(self.AD, 0, play_state.player)
                        #ZergBomb.bomb_sound.play()
        else:
            self.exist = False

    def die(self):
        pass

    @staticmethod
    def play_bomb_sound():
        ZergBomb.bomb_sound.play()
        pass

    @staticmethod
    def load_resource():
        ZergBomb.img = load_image('resource\\bullet\\zerg_bomb_80.png')
        ZergBomb.bomb_sound = load_wav('resource\\bullet\\hit_sound\\explo1_short.wav')
        Sound.list.append(ZergBomb.bomb_sound)
        Sound.volume_list.append(12)

class MutalHitEffect(Effect):
    img = None

    print_sx = 88  # 그려줄 스프라이트 시트에서 얼마나 잘라다가 쓸꺼냐
    print_sy = 88
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 88     # 스프라이트에서 어느 만큼씩 옮길건지
    max_frame = 12  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 4  # 몇프레임마다 재생할것인가

    def __init__(self, x, y, layer=GROUND_CRASH_EFFECT):
        self.print_x = x
        self.print_y = y
        self.img_now = [0, 0]  # 1120  # 스프라이트 좌표
        self.cur_frame = 0
        self.time = 0
        self.exist = True
        game_world.objects[layer].append(self)

    @staticmethod
    def load_resource():
        pass
        MutalHitEffect.img = load_image('resource\\bullet\\mutal_hit_effect200_70.png')

class ZergSpark(Effect):
    img = None

    print_sx = 80  # 그려줄 스프라이트 시트에서 얼마나 잘라다가 쓸꺼냐
    print_sy = 80
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 80  # 스프라이트에서 어느 만큼씩 옮길건지
    max_frame = 8  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 4  # 몇프레임마다 재생할것인가

    def __init__(self, x, y, layer=GROUND_CRASH_EFFECT):
        self.print_x = x
        self.print_y = y
        self.img_now = [0, 0]  # 1120  # 스프라이트 좌표
        self.cur_frame = 0
        self.time = 0
        self.exist = True
        game_world.objects[layer].append(self)

    @staticmethod
    def load_resource():
        pass
        ZergSpark.img = load_image('resource\\bullet\\zerg_spark200.png')


class Missile:
    img = None
    propel_img = None
    hit_sound = None
    max_speed = 27

    def __init__(self, player):
        self.owner = player
        self.x, self.y = player.head_x(), player.head_y()
        self.x2 = play_state.cursor.x
        self.y2 = play_state.cursor.y
        self.AD = player.AD2
        self.time = 0
        self.line = False
        self.lock_on_obj = None
        self.lock_on_rad = None
        self.cur_speed = random.randint(6, 9)
        self.accel = 0.3
        if player.shoulder == 0:
            self.cur_rad = player.rad + math.pi + random.random()
        else:
            self.cur_rad = player.rad - math.pi - random.random()
        if self.cur_rad > math.pi:
            self.cur_rad -= pi2
        self.cos = math.cos(self.cur_rad)
        self.sin = math.sin(self.cur_rad)
        self.dir = Bullet32.get_bullet_num(self.cur_rad)
        self.img_now_x = 12 + 64 * self.dir
        self.first_lock_on()
        self.exist = True
        game_world.objects[AIR_BULLET].append(self)

    def show(self):
        self.img.clip_draw(self.img_now_x, 0, 40, 40, self.x, self.y)
        if self.lock_on_obj is not None:
            draw_rectangle(*self.lock_on_obj.get_hit_box())

    def first_lock_on(self):
        length = len(game_world.fly_obj)
        if length == 0:
            self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
            return False
        else:
            min_r = None
            start = 0
            for i in range(0, length):
                if game_world.fly_obj[i].collision:
                    self.lock_on_obj = game_world.fly_obj[i]
                    min_r = math.dist([self.x2, self.y2],
                                      [self.lock_on_obj.print_x, self.lock_on_obj.print_y])  # 두 점 사이의 거리
                    break
                else:
                    start += 1
            for i in range(start + 1, length):
                if game_world.fly_obj[i].collision:
                    r = math.dist([self.x2, self.y2],
                                  [game_world.fly_obj[i].print_x, game_world.fly_obj[i].print_y])  # 두 점 사이의 거리
                    if r < min_r:
                        min_r = r
                        self.lock_on_obj = game_world.fly_obj[i]
            if min_r is not None:
                self.lock_on_update()
                return True
            else:
                self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
                return False

    def try_lock_on(self):
        length = len(game_world.fly_obj)
        if length == 0:
            if not self.line:
                self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
            return False
        else:
            min_r = None
            start = 0
            for i in range(0, length):
                if game_world.fly_obj[i].collision:
                    r = math.dist([self.x, self.y],
                                  [game_world.fly_obj[i].print_x, game_world.fly_obj[i].print_y])  # 두 점 사이의 거리
                    if r < 300:
                        min_r = r
                        self.lock_on_obj = game_world.fly_obj[i]
                        break
                    else:
                        start += 1
                else:
                    start += 1
            for i in range(start + 1, length):
                if game_world.fly_obj[i].collision:
                    r = math.dist([self.x, self.y],
                                  [game_world.fly_obj[i].print_x, game_world.fly_obj[i].print_y])  # 두 점 사이의 거리
                    if r < min_r:
                        min_r = r
                        self.lock_on_obj = game_world.fly_obj[i]
            if min_r is not None:
                self.lock_on_update()
                return True
            else:
                if not self.line:
                    self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
                return False

    def lock_on_update(self):
        self.x2 = self.lock_on_obj.print_x
        self.y2 = self.lock_on_obj.print_y
        self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
        pass

    def rotate(self):
        # self.cur_rad = self.lock_on_rad#천천히 돌기 위해 수정해야하는 부분
        if self.time % 4 == 0:
            if self.time % 12 == 0:
                MissilePropelEffect(self.x, self.y)
            dr = None
            if self.cur_rad >= 0:
                if self.lock_on_rad >= 0:
                    dr = self.lock_on_rad - self.cur_rad
                else:  #
                    dr = self.lock_on_rad - self.cur_rad
                    if dr < -math.pi:
                        dr += pi2
                    pass
            else:
                if self.lock_on_rad < 0:
                    dr = self.lock_on_rad - self.cur_rad
                else:
                    dr = self.lock_on_rad - self.cur_rad
                    if dr > math.pi:
                        dr -= pi2
                    pass
            abs_dr = abs(dr)
            if abs_dr < 0.0001:  # 거의 일자이니까 이후 연산 안함.
                self.line = True
            else:
                # if abs_dr > 0.523599:#15도
                #     abs_dr = 0.523599
                #     dr = clamp(-0.523599, dr, 0.523599)
                # self.cur_speed *= (5 - (abs_dr / 0.523599)) / 5
                # 아래의 수식으로 단순화
                if abs_dr > 0.5:  # 약 28.6479 deg
                    abs_dr = 0.5
                    dr = clamp(-0.5, dr, 0.5)
                self.cur_speed *= 1 - abs_dr * 0.4
                self.cur_rad += dr
                if self.cur_rad > math.pi:  # dr > 0
                    self.cur_rad -= pi2
                elif self.cur_rad <= -math.pi:  # dr < 0
                    self.cur_rad += pi2
                self.cos = math.cos(self.cur_rad)
                self.sin = math.sin(self.cur_rad)
                self.img_now_x = 12 + 64 * Bullet32.get_bullet_num(self.cur_rad)

    def x_move(self, x):
        self.x += x
        self.x2 += x

    def y_move(self, y):
        self.y += y
        self.y2 += y

    def xx_move(self, x):
        self.x += x

    def yy_move(self, y):
        self.y += y

    def move(self):
        self.xx_move(self.cos * self.cur_speed)
        self.yy_move(self.sin * self.cur_speed)
        if self.time < 20:
            self.cur_speed = max(self.cur_speed - self.accel, 0)  # 20프레임까지는 감속
        else:
            self.cur_speed = min(self.cur_speed + self.accel, self.max_speed)

    def update(self):
        if self.time > 300:
            self.exist = False
            MissileHitEffect(self.x, self.y)
            return
        self.move()
        if self.y > play_state.window_size[1] + 300 or self.y < - 300 or self.x > play_state.window_size[  # 아웃체크
            0] + 300 or self.x < - 300:
            self.exist = False
            return
        if self.lock_on_obj is None:
            self.try_lock_on()
            self.rotate()
        else:  # lock_on is True
            if not self.lock_on_obj.collision:
                self.lock_on_obj = None
                self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
                return
            self.lock_on_update()
            self.rotate()
            if bullet_crash(self, self.lock_on_obj):
                self.exist = False
                Missile.hit_sound.play()
                MissileHitEffect(self.x, self.y)
                self.lock_on_obj.suffer(self.AD, 0, self.owner)
        self.time += 1

    def die(self):
        pass

    @staticmethod
    def load_resource():
        Missile.img = load_image('resource\\bullet\\missile200x2.png')
        Missile.hit_sound = load_wav('resource\\bullet\\hit_sound\\weapon-sound19.wav')
        Sound.list.append(Missile.hit_sound)
        Sound.volume_list.append(4)
        MissileHitEffect.load_resource()
        MissilePropelEffect.load_resource()

class MissilePropelEffect(Effect):
    img = None
    print_sx = 42
    print_sy = 40
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 0  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 168
    max_frame = 5  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 5

    def __init__(self, x, y):
        self.exist = True  # 존재함
        self.print_x, self.print_y = x, y
        self.img_now = [60, 8]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        self.time = 0
        game_world.objects[AIR_BULLET].append(self)

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x, self.print_y)

    def die(self):
        pass

    @staticmethod
    def load_resource():
        MissilePropelEffect.img = load_image('resource\\bullet\\missile_propel200_70_10.png')

class MissileHitEffect(Effect):
    img = None
    print_sx = 36
    print_sy = 36
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 0  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 44
    max_frame = 10  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 4

    def __init__(self, x, y):
        self.exist = True  # 존재함
        self.print_x, self.print_y = x, y
        self.img_now = [0, 0]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        self.time = 0
        game_world.objects[AIR_CRASH_EFFECT].append(self)

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x, self.print_y, 60, 60)

    def die(self):
        pass

    @staticmethod
    def load_resource():
        MissileHitEffect.img = load_image("resource\\bullet\\missile_hit_effect_60.png")

