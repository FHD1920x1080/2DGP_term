import game_world
import play_state
from obj_class.obj import *

AUTO, LOCK_ON, ATTACK, WAIT = range(4)


class Zergling(GroundObj):
    img = None
    print_sx = 110
    print_sy = 78
    stand_sx = 18
    stand_sy = 16
    hit_sx = 22
    hit_sy = 20
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 20
    hit_y_gap = 5

    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.s
    hp = 6
    speed = 3
    anger_speed = 4
    AD = 1
    speed_sup = speed / 3  # 저글링은 프레임마다 속도가 달라서 만들어준 변수 기본속도가 3이라고 가정하고 만듦
    zm = 0.01
    rd = 500
    hit_sound = None

    def __init__(self, x, y):
        self.img_now = [74, 2910]
        self.stand_x = x
        self.stand_y = y
        self.hp = Zergling.hp
        self.speed = Zergling.speed
        self.speed_sup = self.speed / 3
        self.move_frame = 0
        self.attack_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)
        self.exist = True  # 충돌 gn False로 바꿔줄 존재 변수
        self.face_dir = 0
        self.state = AUTO
        self.rad = None
        self.cos = None
        self.sin = None
        self.frame_speed = [1 * self.speed_sup, 3 * self.speed_sup, 6 * self.speed_sup, 4 * self.speed_sup,
                            4 * self.speed_sup, 2 * self.speed_sup, 1 * self.speed_sup]
        self.cur_speed = Zergling.get_speed(self)

    @staticmethod
    def play_hit_sound():
        Zergling.hit_sound.play()

    def stop(self):
        self.img_now = 74 + 256 * self.face_dir, 1630

    def get_speed(self):
        return self.frame_speed[self.move_frame]

    def move_down(self):
        self.y_move(- self.cur_speed)
        self.face_dir = 8
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame

    def move_left_down(self):
        s = self.cur_speed * 0.707
        self.y_move(-s)
        self.x_move(-s)
        self.face_dir = 10
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame
        if self.get_stand_left() < 0:
            self.x_move_point(self.stand_sx)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        s = self.cur_speed * 0.707
        self.y_move(-s)
        self.x_move(s)
        self.face_dir = 6
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame
        if self.get_stand_right() > play_state.window_size[0]:
            self.x_move_point(play_state.window_size[0] - self.stand_sx)
            self.direction = random.randrange(1, 3)

    def anim(self):
        if self.state > LOCK_ON:  # ATTACK, WAIT
            if self.time % 4 == 0:
                self.attack_frame += 1
        else:
            if self.time % 5 == 0:
                self.move_frame = (self.move_frame + 1) % 7
                self.cur_speed = Zergling.get_speed(self)

    def suffer(self, damage):  # 피격당하면 해줄것
        self.hp -= damage
        if self.hp <= 0:
            self.exist = False  # 마지막에 한번에 삭제해줄 것이고 지금은 아님
            self.collision = False  # 충돌체크 안함
            return
        if self.state != 1:
            self.state = 1
            self.time = 0
            self.speed = self.anger_speed
            self.dir_adjust()
            self.speed_sup = self.speed / 3
            self.frame_speed = [1 * self.speed_sup, 3 * self.speed_sup, 6 * self.speed_sup, 4 * self.speed_sup,
                                4 * self.speed_sup, 2 * self.speed_sup, 1 * self.speed_sup]

    def auto_move(self):
        if self.move_frame == 0:
            r = math.dist([self.stand_x, self.stand_y],
                          [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리

            if r < Zergling.rd:
                self.state = LOCK_ON
                self.time = 0
                self.dir_adjust()
                self.speed = self.anger_speed
                self.speed_sup = self.speed / 3
                self.frame_speed = [1 * self.speed_sup, 3 * self.speed_sup, 6 * self.speed_sup, 4 * self.speed_sup,
                                    4 * self.speed_sup, 2 * self.speed_sup, 1 * self.speed_sup]
                return
        if self.direction == 0:
            self.stop()
        elif self.direction == 1:
            if self.move_down() == False:
                return
        if self.direction == 2:
            if self.move_left_down() == False:
                return
        elif self.direction == 3:
            if self.move_right_down() == False:
                return
        if self.time % self.direction_rand_time == 0:
            j = self.direction
            self.direction = random.randrange(0, 4)
            if j == 0 and self.direction != 0:  # 멈춰있었다가 움직이면 무브프레임 초기화
                self.move_frame = 0
            if self.direction == 0:
                self.direction_rand_time = self.time + random.randrange(10, 30)
            else:
                self.direction_rand_time = self.time + random.randrange(50, 200)

    def update(self):
        if self.state == AUTO:
            self.auto_move()  # atuo move에서 바로 LOCK_ON으로 갈 수 있음.
        elif self.state == LOCK_ON:  # player를 발견한 상태
            if self.move_frame == 0:
                self.dir_adjust()
            self.lock_on_move()
        elif self.state == ATTACK:
            self.attack()
        elif self.state == WAIT:
            self.wait()
        if self.stand_y < -100:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        self.anim()
        self.time += 1

    def dir_adjust(self):
        self.rad = get_rad(self.stand_x, self.stand_y, play_state.player.stand_x, play_state.player.stand_y)
        self.cos = math.cos(self.rad)
        self.sin = math.sin(self.rad)
        self.face_dir = self.get_face_dir(self.rad)

    def lock_on_move(self):
        r = math.dist([self.stand_x, self.stand_y],
                      [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
        if r > 0:
            if play_state.player.unit_type == 0:
                if r < 60:
                    self.state = ATTACK
                    return
            elif play_state.player.unit_type == 1:
                if r < 68:
                    self.state = ATTACK
                    return
            else:
                if r < 75:
                    self.state = ATTACK
                    return
        # if self.rad == None:
        #     self.dir_adjust()
        self.x_move(self.cos * self.cur_speed)
        self.y_move(self.sin * self.cur_speed)
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame

    def attack(self):
        if self.time % 4 == 0:
            self.img_now = 74 + 256 * self.face_dir, 2910 - 256 * self.attack_frame
            if self.attack_frame == 1:
                play_state.player.suffer(self.AD)
                play_state.sound.Zergling_hit = True
            elif self.attack_frame > 3:  # 여기서는 0, 1, 2, 3동안 머물고 4가 되면 나감
                self.state = WAIT

    def wait(self):
        self.img_now = 74 + 256 * self.face_dir, 1630
        if self.attack_frame > 10:
            self.state = LOCK_ON
            self.attack_frame = 0
            self.move_frame = 0

    @staticmethod
    def get_face_dir(rad):
        if rad >= 0:  # 1, 2 사분면
            if rad < 1.8:
                if rad < 0.1963:  # 우측
                    return 4
                elif rad < 0.589:
                    return 3
                elif rad < 1.0517:
                    return 2
                elif rad < 1.3844:
                    return 1
                else:  # rad < 1.8:
                    return 0
            else:
                if rad < 2.0898:
                    return 15
                elif rad < 2.5525:
                    return 14
                elif rad < 2.9452:
                    return 13
                else:  # rad <= 3.1415:
                    return 12
        else:  # 3,4분면
            if rad > -1.9371:
                if rad > -0.0663:  # 우측
                    return 4
                elif rad > -0.31:
                    return 5
                elif rad > -0.7017:
                    return 6
                elif rad > -1.2044:
                    return 7
                else:  # rad > -1.9371:
                    return 8
            else:
                if rad > -2.4398:
                    return 9
                elif rad > -2.8315:
                    return 10
                elif rad > -3.0752:
                    return 11
                else:  # rad >= -3.1415:
                    return 12

    def die(self, i=0):
        if self.hp <= 0:
            dz = DieZergling(self.stand_x, self.stand_y)
            game_world.ground_obj.insert(i + 1, dz)
        # print(len(Zergling.list))
        pass

    @staticmethod
    def make_zergling():
        if random.random() <= Zergling.zm:
            zergling = Zergling(random.randrange(Zergling.stand_sx, play_state.window_size[0] - Zergling.stand_sx),
                                play_state.window_size[1] + Zergling.stand_sy)
            # game_world.ground_obj.append(zergling)
            game_world.ground_obj.insert(0, zergling)

    @staticmethod
    def load_resource():
        Zergling.img = load_image("resource\\zergling\\zergling200x2_brown.png")
        Zergling.hit_sound = load_wav('resource\\zergling\\zulhit00.wav')
        Sound.list.append(Zergling.hit_sound)
        Sound.volume_list.append(6)
        DieZergling.load_resource()
        BombZergling.load_resource()


class DieZergling(Effect):
    img = None
    sound = None
    print_sx = 130
    print_sy = 106
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = -3  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 136
    max_frame = 7  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6

    def __init__(self, x, y):
        self.exist = True  # 존재함
        self.stand_x = x
        self.stand_y = y
        self.print_x, self.print_y = self.stand_x + self.print_x_gap, self.stand_y + self.print_y_gap
        self.img_now = [2, 0]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        self.time = 0
        play_state.sound.Zergling_die = True

    def die(self, i=0):
        DeathZergling(self.print_x - 2, self.print_y - 7)

    @staticmethod
    def play_sound():
        DieZergling.sound.play()

    @staticmethod
    def load_resource():
        DieZergling.img = load_image("resource\\zergling\\die_zergling200_80.png")
        DieZergling.sound = load_wav('resource\\zergling\\zzedth01.wav')
        Sound.list.append(DieZergling.sound)
        Sound.volume_list.append(8)

        DeathZergling.load_resource()


class DeathZergling(Effect):
    img = None
    print_sx = 130
    print_sy = 64
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 256
    max_frame = 5  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 200

    def __init__(self, x, y):
        self.exist = True  # 존재함
        self.print_x, self.print_y = x, y
        self.img_now = [42, 88]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        self.time = 0
        game_world.objects[FLOOR_EFFECT].append(self)

    def x_move(self, x):
        self.print_x += x

    def y_move(self, y):
        self.print_y += y

    @staticmethod
    def load_resource():
        DeathZergling.img = load_image("resource\\zergling\\death_zergling200_80.png")


from obj_class.bullet import ZergBomb


class BombZergling(Zergling):
    img = None
    speed = 3.5
    anger_speed = 4.5

    collision_type = 2 # 남을 밀어냄
    def __init__(self, x, y):
        super().__init__(x, y)
        # self.img = BombZergling.img
        self.AD = 10

    def lock_on_move(self):
        # if self.move_frame % 4 == 0:
        r = math.dist([self.stand_x, self.stand_y],
                      [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
        if r > 0:
            if play_state.player.unit_type == 0:
                if r < 50:
                    self.hp = 0
                    self.exist = False
                    self.collision = False
                    return
            elif play_state.player.unit_type == 1:
                if r < 58:
                    self.hp = 0
                    self.exist = False
                    self.collision = False
                    return
            else:
                if r < 60:
                    self.hp = 0
                    self.exist = False
                    self.collision = False
                    return
        # if self.rad == None:
        #     self.dir_adjust()
        self.x_move(self.cos * self.cur_speed)
        self.y_move(self.sin * self.cur_speed)
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame

    @staticmethod
    def make_zergling():
        if random.random() <= BombZergling.zm:
            zergling = BombZergling(random.randrange(Zergling.stand_sx, play_state.window_size[0] - Zergling.stand_sx),
                                    play_state.window_size[1] + Zergling.stand_sy)
            # game_world.ground_obj.append(zergling)
            game_world.ground_obj.insert(0, zergling)

    def die(self, i=0):
        # if self.hp > 0:
        # if self.state == LOCK_ON:
        if self.hp <= 0:
            self.x = self.stand_x
            self.y = self.stand_y
            self.cur_size = 1.0
            self.index = i
            ZergBomb(self)
            # dz = DieZergling(self.stand_x, self.stand_y)
            # game_world.ground_obj.insert(i + 1, dz)
        # else:
        #     dz = DieZergling(self.stand_x, self.stand_y)
        #     game_world.ground_obj.insert(i + 1, dz)

    @staticmethod
    def load_resource():
        BombZergling.img = load_image("resource\\zergling\\zergling200x2_green.png")
