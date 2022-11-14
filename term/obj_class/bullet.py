from obj_class.obj import *

class DragBull:
    img = None
    sx = 0
    sy = 0

    def __init__(self, player):
        self.x1, self.y1 = player.print_x(), player.print_y() + 5  # x1, y1  # 시작 좌표
        self.x2, self.y2 = player.bull_x2, player.bull_y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.max_speed = player.bullet_speed
        self.speed = self.max_speed - 20
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        self.cur_speed = self.speed / self.r
        self.accel = 0.5 / self.r # t에 더하는 self.cur_speed 에 더할 속도
        self.img_now_x = 0
        self.frame = 0
        self.cur_size = player.bull_size  # 100% 기준
        self.exist = True

    def show(self):
        self.img.clip_composite_draw(self.img_now_x, 0, 20, 18, 0, '', self.x, self.y, 20 * self.cur_size,
                                          20 * self.cur_size)

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
            DragBullEffect(self)

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
        self.stand_x = bullet.x
        self.stand_y = bullet.y
        self.img_now = [0, 0]
        self.cur_frame = 0
        self.cur_size = bullet.cur_size
        self.AD = bullet.AD
        DragBullEffect.play_bomb_sound()
        game_world.ground_crash_effect.append(self)

    def show(self):
        DragBullEffect.img.clip_composite_draw(self.img_now[0], self.img_now[1], 188, 150, 0, '', self.stand_x, self.stand_y,
                                                 188 * self.cur_size, 150 * self.cur_size)

    def get_left(self, i):
        return self.stand_x - self.rect_sx[i] * self.cur_size

    def get_right(self, i):
        return self.stand_x + self.rect_sx[i] * self.cur_size

    def get_bottom(self, i):
        return self.stand_y - self.rect_sy[i] * self.cur_size

    def get_top(self, i):
        return self.stand_y + self.rect_sy[i] * self.cur_size

    def anim(self):
        if self.cur_frame < self.max_frame:
            self.img_now[0] += self.next_gap
            self.cur_frame += 1
            if self.cur_frame == 2:
                for obj in game_world.ground_obj:
                    if obj != play_state.player:
                        if tir_rect_crash(self, obj):
                            obj.hp -= self.AD
                            attack_effect = Bullet32_Effect(obj.print_x(), obj.print_y(), 1)
                            game_world.ground_crash_effect.append(attack_effect)
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


class Bullet32:
    img = [] # 얘는 좀 특이하게 스프라이트 시트가 아니고 하나씩 잘라놈

    def __init__(self, player, x2, y2):
        self.x1, self.y1 = self.get_start_point(player)  # x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.y1  # 현재 좌표
        self.speed = player.bullet_speed
        self.AD = player.AD
        self.t = 0
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
        self.cur_speed = self.speed / self.r
        self.num = self.get_bullet_num(get_rad(self.x1, self.y1, self.x2, self.y2))
        self.img = Bullet32.img[self.num]
        # self.sx, self.sy = self.get_bullet_size(self.num)
        self.exist = True  # 충돌 gn False로 바꿔줄 존재 변수

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
        if player.unit_type == 0:  # 마린일 때 1 은 골리앗
            if player.face_dir < 10:
                return player.stand_x + 8, player.stand_y + 18
            elif player.face_dir > 26:
                return player.stand_x - 8, player.stand_y + 18
            else:
                return player.stand_x, player.stand_y + 14

    def get_bullet_num(self, rad): # 그냥 쓸까 deg로 고쳐서 할까 정수연산으로 하는게 이득일라나
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

    def update(self):
        self.move()
        self.crash_check()

    def crash_check(self):
        if self.y > play_state.window_size[1] + 60 or self.y < - 60 or self.x > play_state.window_size[
            0] + 60 or self.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
            self.exist = False
        else:
            for em in game_world.ground_obj:
                if em != play_state.player: #주인공은 지 몸땡이에 서 총알 쏴서 충돌체크 하면 안됨.
                    if bullet_crash(self, em) == True:
                        self.exist = False
                        attack_effect = Bullet32_Effect(self.x, self.y)
                        game_world.ground_crash_effect.append(attack_effect)
                        em.hp -= self.AD
                        if em.hp <= 0:
                            em.exist = False  # 마지막에 한번에 삭제해줄 것이고 지금은 아님
                            em.collision = False  # 충돌체크 안함
                        break # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음



    @staticmethod
    def load_resource():
        for i in range(0, 32):
            Bullet32.img.append(load_image("resource\\bullet\\" + str(i) + ".png"))
        Bullet32_Effect.load_resource()
        DragBull.load_resource()


class Bullet32_Effect(Effect):
    img_red = None
    img_blue = None
    hit_sound = None

    print_sx = 80  # 그려줄 스프라이트 시트에서 얼마나 잘라다가 쓸꺼냐
    print_sy = 80
    anim_direction = 'h'  # 스프라이트 이미지 재생 방향
    next_gap = 80  # 스프라이트에서 어느 만큼씩 옮길건지
    max_frame = 4  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6 #몇프레임마다 재생할것인가
    def __init__(self, x, y, color = 0):
        if color == 1:
            self.img = Bullet32_Effect.img_blue
        else:
            self.img = Bullet32_Effect.img_red
            play_state.sound.Bullet32_hit = True
        self.print_x = x
        self.print_y = y
        self.img_now = [0, random.randint(3, 14) * 80]  # 1120  # 스프라이트 좌표
        self.cur_frame = 0
        self.exist = True


    @staticmethod
    def play_hit_sound():
        Bullet32_Effect.hit_sound.play()

    @staticmethod
    def load_resource():
        pass
        Bullet32_Effect.img_red = load_image('resource\\bullet\\attack_effect_red.png')
        Bullet32_Effect.img_blue = load_image('resource\\bullet\\attack_effect_blue.png')
        Bullet32_Effect.hit_sound = load_wav('resource\\bullet\\hit_sound\\06.wav')
        Sound.list.append(Bullet32_Effect.hit_sound)
        Sound.volume_list.append(6)
