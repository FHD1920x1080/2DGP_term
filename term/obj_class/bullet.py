import game_world
import play_state
from obj_class.obj import *


class Bullet32:
    img = []  # 얘는 좀 특이하게 스프라이트 시트가 아니고 하나씩 잘라놈

    hit_sound = None

    def __init__(self, player, x2, y2):
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
        self.img = Bullet32.img[self.num]
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
                    if bullet_crash(self, obj) == True:
                        play_state.sound.Bullet32_hit = True
                        Bullet32_Effect(self.x, self.y)
                        self.exist = False
                        obj.state = 1
                        obj.hp -= self.AD
                        if obj.hp <= 0:
                            obj.exist = False  # 마지막에 한번에 삭제해줄 것이고 지금은 아님
                            obj.collision = False  # 충돌체크 안함
                        break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음
            for obj in game_world.fly_obj:
                if bullet_crash(self, obj) == True:
                    play_state.sound.Bullet32_hit = True
                    Bullet32_Effect(self.x, self.y)
                    self.exist = False
                    obj.state = 1
                    obj.hp -= self.AD
                    if obj.hp <= 0:
                        obj.exist = False  # 마지막에 한번에 삭제해줄 것이고 지금은 아님
                        obj.collision = False  # 충돌체크 안함
                    break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음

    def die(self):
        pass

    @staticmethod
    def load_resource():
        for i in range(0, 32):
            Bullet32.img.append(load_image("resource\\bullet\\" + str(i) + ".png"))
        Bullet32_Effect.load_resource()
        Bullet32.hit_sound = load_wav('resource\\bullet\\hit_sound\\06.wav')
        Sound.list.append(Bullet32.hit_sound)
        Sound.volume_list.append(6)
        DragBull.load_resource()
        Missile.load_resource()


class Bullet32Gol(Bullet32):
    def __init__(self, player):
        self.x, self.y = player.shoot_point
        self.speed = player.bullet_speed
        self.AD = player.AD
        rad = player.rad + player.error_rate()
        self.cos = math.cos(rad)
        self.sin = math.sin(rad)
        num = self.get_bullet_num(rad)
        self.img = Bullet32.img[num]
        self.exist = True
        game_world.ground_bullet.append(self)

    @staticmethod
    def play_hit_sound():
        Bullet32.hit_sound.play()

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def move(self):
        self.x_move(self.cos * self.speed)
        self.y_move(self.sin * self.speed)


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
        self.start_frame = play_state.frame % self.any_frame_rate
        self.exist = True
        game_world.objects[layer].append(self)

    def x_move(self, x):
        self.print_x += x

    def y_move(self, y):
        self.print_y += y

    @staticmethod
    def load_resource():
        pass
        Bullet32_Effect.img_red = load_image('resource\\bullet\\bullet_hit_effect_orange.png')
        Bullet32_Effect.img_blue = load_image('resource\\bullet\\bullet_hit_effect_blue.png')


class DragBull:
    img = None

    def __init__(self, player):
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
        elif self.t > 0.99:
            self.exist = False

    def anim(self):
        self.img_now_x = self.frame * 20
        self.frame = (self.frame + 1) % 5

    @staticmethod
    def load_resource():
        DragBull.img = load_image('resource\\bullet\\dragbull.png')
        DragBullEffect.load_resource()


class DragBullEffect(Effect):
    img = None
    bomb_sound = None

    print_sx = 188
    print_sy = 150
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 0  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 191
    max_frame = 10  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6

    rect_sx = [0, 0, 0]
    rect_sy = [0, 0, 0]
    rect_sx[0] = 34
    rect_sy[0] = 54
    rect_sx[1] = 76
    rect_sy[1] = 24
    rect_sx[2] = (rect_sx[0] + rect_sx[1]) // 2
    rect_sy[2] = (rect_sy[1] + rect_sy[1]) // 2

    def __init__(self, bullet):
        self.collision = False
        self.exist = True  # 존재함
        self.print_x = bullet.x
        self.print_y = bullet.y
        self.img_now = [0, 0]
        self.cur_frame = 0
        self.cur_size = bullet.cur_size * 1.2  # 배율
        self.cur_size_x = self.cur_size * 188
        self.cur_size_y = self.cur_size * 150
        self.AD = bullet.AD
        self.start_frame = play_state.frame % self.any_frame_rate
        play_state.sound.Dragoon_bull_bomb = True
        game_world.objects[BOMB_EFFECT].append(self)

    def show(self):
        DragBullEffect.img.clip_composite_draw(self.img_now[0], self.img_now[1], 188, 150, 0, '', self.print_x,
                                               self.print_y,
                                               self.cur_size_x, self.cur_size_y)

    def x_move(self, x):
        self.print_x += x

    def y_move(self, y):
        self.print_y += y

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
                            obj.hp -= self.AD
                            obj.state = 1
                            Bullet32_Effect(obj.stand_x, obj.stand_y, 1)
                            if obj.hp <= 0:
                                obj.exist = False
                                obj.collision = False
                for obj in game_world.fly_obj:
                    if tir_rect_crash(self, obj):
                        obj.hp -= self.AD
                        obj.state = 1
                        Bullet32_Effect(obj.print_x, obj.print_y, 1, AIR_CRASH_EFFECT)
                        if obj.hp <= 0:
                            obj.exist = False
                            obj.collision = False
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


class Missile:
    img = None

    def __init__(self, player):
        self.lock_on_rad = None
        self.x, self.y = player.head_x(), player.head_y()
        self.x2 = play_state.cursor.x
        self.y2 = play_state.cursor.y
        self.lock_on_obj = None
        self.speed = player.missile_speed
        self.AD = player.AD2
        self.dir = (Bullet32.get_bullet_num(player.rad) + 16) % 32
        self.img_now_x = 12 + 64 * self.dir
        self.cur_rad = player.rad + math.pi
        if self.cur_rad > math.pi:
            self.cur_rad -= 2 * math.pi
        self.cos = math.cos(self.cur_rad)
        self.sin = math.sin(self.cur_rad)
        self.first_lock_on()
        self.exist = True
        game_world.objects[AIR_BULLET].append(self)

    def show(self):
        self.img.clip_draw(self.img_now_x, 0, 40, 40, self.x, self.y)

    def first_lock_on(self):
        length = len(game_world.fly_obj)
        if length == 0:
            self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
        else:
            self.lock_on_obj = game_world.fly_obj[0]
            min_r = math.dist([self.x2, self.y2],
                              [self.lock_on_obj.print_x, self.lock_on_obj.print_y])  # 두 점 사이의 거리
            for i in range(1, length):
                r = math.dist([self.x2, self.y2],
                              [game_world.fly_obj[i].print_x, game_world.fly_obj[i].print_y])  # 두 점 사이의 거리
                if r < min_r:
                    min_r = r
                    self.lock_on_obj = game_world.fly_obj[i]

    def try_lock_on(self):
        length = len(game_world.fly_obj)
        if length == 0:
            return False
        else:
            self.lock_on_obj = game_world.fly_obj[0]
            min_r = math.dist([self.x, self.y],
                              [self.lock_on_obj.print_x, self.lock_on_obj.print_y])  # 두 점 사이의 거리

            for i in range(1, length):
                r = math.dist([self.x, self.y],
                              [game_world.fly_obj[i].print_x, game_world.fly_obj[i].print_y])  # 두 점 사이의 거리
                if r < min_r:
                    min_r = r
                    self.lock_on_obj = game_world.fly_obj[i]
            self.lock_on_update()

    def lock_on_update(self):
        self.x2 = self.lock_on_obj.print_x
        self.y2 = self.lock_on_obj.print_y
        self.lock_on_rad = get_rad(self.x, self.y, self.x2, self.y2)
        pass

    def rotate(self):
        self.cur_rad = self.lock_on_rad
        self.cos = math.cos(self.cur_rad)
        self.sin = math.sin(self.cur_rad)
        self.img_now_x = 12 + 64 * Bullet32.get_bullet_num(self.cur_rad)
        pass

    def x_move(self, x):
        self.x += x

    def y_move(self, y):
        self.y += y

    def move(self):
        self.x_move(self.cos * self.speed)
        self.y_move(self.sin * self.speed)

    def update(self):
        self.move()
        self.out_check()
        if self.lock_on_obj is None:
            self.try_lock_on()
            self.rotate()
        else:  # lock_on == True
            print(self.lock_on_obj)
            self.lock_on_update()
            self.rotate()
            self.crash_check()

    def out_check(self):
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:
            self.exist = False

    def crash_check(self):
        if self.y > self.y2 + 3:
            return
        if self.y2 - 3 > self.y:
            return
        if self.x > self.x2 + 3:
            return
        if self.x2 - 3 > self.x:
            return
        self.exist = False

    def die(self):
        pass

    @staticmethod
    def load_resource():
        Missile.img = load_image('resource\\bullet\\missile200x2.png')
