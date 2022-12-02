import game_world
import play_state
from obj_class.obj import *

AUTO, LOCK_ON, ATTACK, WAIT = range(4)


class Mutal(FlyObj):
    img = None
    shadow = None
    print_sx = 144
    print_sy = 130
    stand_sx = 0
    stand_sy = 0
    hit_sx = 35
    hit_sy = 35
    stand_x_gap = 0
    hit_x_gap = 0
    stand_y_gap = 90
    hit_y_gap = -12

    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌 함
    hp = 9
    max_speed = 5
    accel = 0.05
    zm = 0.002

    hit_sound = None

    start_pos = None
    def __init__(self, x, y):
        self.img_now = [60, 1100]  ##86, 84 씩 옮겨야 함
        self.print_x = x
        self.print_y = y
        self.hp = Mutal.hp
        self.max_speed = Mutal.max_speed
        self.cur_speed = 0
        self.accel = Mutal.accel
        self.move_frame = 0
        self.attack_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)
        self.exist = True  # 충돌 gn False로 바꿔줄 존재 변수
        self.collision = True
        self.face_dir = 0
        self.state = LOCK_ON
        self.rad = None
        self.cos = None
        self.sin = None


    @staticmethod
    def play_hit_sound():
        pass

    def stop(self):
        self.img_now = 60 + 256 * self.face_dir, 1100 - 256 * self.move_frame

    def anim(self):
        if self.state > LOCK_ON:
            if self.time % 6 == 0:
                self.move_frame = (self.move_frame + 1) % 5
            if self.time % 4 == 0:
                self.attack_frame += 1
        else:
            if self.time % 3 == 0:
                self.move_frame = (self.move_frame + 1) % 5

    # def auto_move(self):
    #     if self.move_frame == 0:
    #         r = math.dist([self.stand_x, self.stand_y],
    #                       [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
    #     if r > 0:
    #         if r < 200:
    #             self.time = 0
    #             self.state = LOCK_ON
    #             self.dir_adjust()
    #             return
    #     if self.direction == 0:
    #         self.stop()
    #     elif self.direction == 1:
    #         if self.move_down() == False:
    #             return
    #     if self.direction == 2:
    #         if self.move_left_down() == False:
    #             return
    #     elif self.direction == 3:
    #         if self.move_right_down() == False:
    #             return
    #     if self.time % self.direction_rand_time == 0:
    #         j = self.direction
    #         self.direction = random.randrange(0, 4)
    #         if j == 0 and self.direction != 0:  # 멈춰있었다가 움직이면 무브프레임 초기화
    #             self.move_frame = 0
    #         if self.direction == 0:
    #             self.direction_rand_time = self.time + random.randrange(10, 30)
    #         else:
    #             self.direction_rand_time = self.time + random.randrange(50, 200)

    def update(self):
        if self.state == LOCK_ON:  # player를 발견한 상태
            if self.move_frame == 0:
                self.dir_adjust()
            self.lock_on_move()
        else:
            self.inertia_move()
        if self.state == ATTACK:
            self.attack()
        elif self.state == WAIT:
            self.wait()

        self.anim()
        self.time += 1

    def dir_adjust(self):
        self.rad = get_rad(self.print_x, self.print_y - 40, play_state.player.stand_x, play_state.player.stand_y)
        self.cos = math.cos(self.rad)
        self.sin = math.sin(self.rad)
        self.face_dir = self.get_face_dir(self.rad)

    def lock_on_move(self):
        self.cur_speed = min(self.cur_speed + self.accel, self.max_speed)
        if self.move_frame == 0:
            r = math.dist([self.print_x, self.print_y - 40],
                          [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
            if r > 0:
                if r < 300:
                    self.state = ATTACK
                    return
        if self.rad == None:
            self.dir_adjust()
        self.x_move(self.cos * self.cur_speed)
        self.y_move(self.sin * self.cur_speed)
        self.img_now = 60 + 256 * self.face_dir, 1100 - 256 * self.move_frame

    def inertia_move(self):
        self.cur_speed = max(self.cur_speed - self.accel * 2, 0)
        if self.rad == None:
            self.dir_adjust()
        self.x_move(self.cos * self.cur_speed)
        self.y_move(self.sin * self.cur_speed)
        self.img_now = 60 + 256 * self.face_dir, 1100 - 256 * self.move_frame
    def attack(self):
        self.img_now = 60 + 256 * self.face_dir, 1100 - 256 * self.move_frame
        if self.attack_frame == 1:
            #play_state.sound.Mutal_hit = True
            #play_state.player.hp -= 1
            pass
        elif self.attack_frame > 3:  # 여기서는 0, 1, 2, 3 ,4 동안 머물고 5가 되면 나감
            self.state = WAIT

    def wait(self):
        self.img_now = 60 + 256 * self.face_dir, 1100  - 256 * self.move_frame
        if self.attack_frame > 10:
            self.state = LOCK_ON
            self.attack_frame = 0
            self.move_frame = 0
            self.dir = None

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
                else: # rad < 1.8:
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
                else:# rad > -1.9371:
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
            dm = DieMutal(self.print_x, self.print_y)
            game_world.fly_obj.insert(i + 1, dm)

    @staticmethod
    def make_mutal():
        if random.random() <= Mutal.zm:
            pos = random.randint(0, 4)
            if pos == 0:
                mutal = Mutal(-200, random.randint(Mutal.start_pos, play_state.window_size[1] + 100))
                game_world.fly_obj.append(mutal)
            elif pos == 1:
                mutal = Mutal(play_state.window_size[0] + 200, random.randint(Mutal.start_pos, play_state.window_size[1] + 100))
                game_world.fly_obj.append(mutal)
            else:
                mutal = Mutal(random.randint(-200, play_state.window_size[0] + 200), play_state.window_size[1] + 200)
                game_world.fly_obj.append(mutal)
    @staticmethod
    def load_resource():
        Mutal.start_pos = play_state.window_size[1] // 3 * 2
        Mutal.img = load_image("resource\\mutal\\mutal200x2_red.png")
        Mutal.shadow = load_image("resource\\mutal\\mutal_shad200x2_30.png")
        #Mutal.hit_sound = load_wav('resource\\mutal\\zulhit00.wav')
        #Sound.list.append(mutal.hit_sound)
        #Sound.volume_list.append(6)
        DieMutal.load_resource()


class DieMutal(Effect):
    img = None
    sound = None
    print_sx = 154
    print_sy = 120
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 0  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 160
    max_frame = 9  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6
    exist = True  # 존재함
    collision = False

    def __init__(self, x, y):
        self.print_x, self.print_y = x - 4, y - 16
        self.img_now = [3, 20]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        self.start_frame = play_state.frame % self.any_frame_rate
        play_state.sound.Mutal_die = True

    def die(self, i=0):
        pass

    @staticmethod
    def play_sound():
        DieMutal.sound.play()

    @staticmethod
    def load_resource():
        DieMutal.img = load_image("resource\\mutal\\die_mutal200_80.png")
        DieMutal.sound = load_wav('resource\\mutal\\zmudth00.wav')
        Sound.list.append(DieMutal.sound)
        Sound.volume_list.append(8)
