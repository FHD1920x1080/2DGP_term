import game_world
import play_state
from obj_class.obj import *

AUTO, LOCK_ON, ATTACK, WAIT = range(4)


class Mutal(GroundObj):
    img = None
    print_sx = 140
    print_sy = 130
    stand_sx = 0
    stand_sy = 0
    hit_sx = 22
    hit_sy = 20
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 20
    hit_y_gap = 5

    exist = True  # 존재 변수 삭제 할지 판정
    collision = False  # 충돌 안함
    crash = True # 총알은 맞음
    hp = 6
    speed = 3
    zm = 0.02

    hit_sound = None

    def __init__(self, x, y):

        self.img_now = [74, 2910]  ##86, 84 씩 옮겨야 함
        self.stand_x = x
        self.stand_y = y
        self.hp = Mutal.hp
        self.speed = Mutal.speed
        self.move_frame = 0
        self.attack_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)
        self.exist = True  # 충돌 gn False로 바꿔줄 존재 변수
        self.face_dir = 0
        self.state = AUTO
        self.rad = None

    @staticmethod
    def play_hit_sound():
        Mutal.hit_sound.play()

    def stop(self):
        self.img_now = 74 + 256 * self.face_dir, 1630

    def get_speed(self):
        if self.move_frame == 0:
            return 1 * self.speed_sup
        elif self.move_frame == 1:
            return 2 * self.speed_sup
        elif self.move_frame == 2:
            return 5 * self.speed_sup
        elif self.move_frame == 3:
            return 4 * self.speed_sup
        elif self.move_frame == 4:
            return 4 * self.speed_sup
        elif self.move_frame == 5:
            return 3 * self.speed_sup
        elif self.move_frame == 6:
            return 2 * self.speed_sup

    def move_down(self):
        if self.get_hit_top() < 0:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = Mutal.get_speed(self)
        self.y_move(- cur_speed)
        self.face_dir = 8
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame

    def move_left_down(self):
        if self.get_hit_top() < 0:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = Mutal.get_speed(self) * 0.707
        self.y_move(-cur_speed)
        self.x_move(-cur_speed)
        self.face_dir = 10
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame
        if self.get_stand_left() < 0:
            self.x_move_point(self.stand_sx)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        if self.get_hit_top() < 0:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = Mutal.get_speed(self) * 0.707
        self.y_move(-cur_speed)
        self.x_move(cur_speed)
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
            if self.time % 6 == 0:
                self.move_frame = (self.move_frame + 1) % 7

    def auto_move(self):
        r = math.dist([self.stand_x, self.stand_y],
                      [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
        if r > 0:
            if r < 200:
                self.time = 0
                self.state = LOCK_ON
                self.dir_adjust()
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

        self.anim()
        self.time += 1

    def dir_adjust(self):
        self.rad = get_rad(self.stand_x, self.stand_y, play_state.player.stand_x, play_state.player.stand_y)
        self.face_dir = self.get_face_dir(self.rad)
        # 여기서 사인 코사인 써서 이동하면 거리를 더 안재도 되겠네? 바보였잖아 나

    def lock_on_move(self):
        r = math.dist([self.stand_x, self.stand_y],
                      [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
        if r > 0:
            if play_state.player.unit_type == 0:
                if r < 60:
                    self.state = ATTACK
                    return
            else:
                if r < 80:
                    self.state = ATTACK
                    return
        cur_speed = Mutal.get_speed(self)
        if self.rad == None:
            self.dir_adjust()
        self.x_move(math.cos(self.rad) * cur_speed)
        self.y_move(math.sin(self.rad) * cur_speed)
        self.img_now = 74 + 256 * self.face_dir, 1630 - 256 * self.move_frame

    def attack(self):
        self.img_now = 74 + 256 * self.face_dir, 2910 - 256 * self.attack_frame
        if self.attack_frame == 1:
            play_state.sound.Mutal_hit = True
            play_state.player.hp -=1
        elif self.attack_frame > 3:  # 여기서는 0, 1, 2, 3 ,4 동안 머물고 5가 되면 나감
            self.state = WAIT

    def wait(self):
        self.img_now = 74 + 256 * self.face_dir, 1630
        if self.attack_frame > 10:
            self.state = LOCK_ON
            self.attack_frame = 0
            self.move_frame = 0
            self.dir = None

    def get_face_dir(self, rad):
        if rad >= 0:  # 1, 2 사분면
            if rad < 0.1963:  # 우측
                return 4
            elif rad < 0.589:
                return 3
            elif rad < 1.0517:
                return 2
            elif rad < 1.3844:
                return 1
            # elif rad < 1.5708:
            #     return 0
            elif rad < 1.8:
                return 0
            elif rad < 2.0898:
                return 15
            elif rad < 2.5525:
                return 14
            elif rad < 2.9452:
                return 13
            else:  # rad <= 3.1415:
                return 12
        else:  # 3,4분면
            if rad > -0.0663:  # 우측
                return 4
            elif rad > -0.31:
                return 5
            elif rad > -0.7017:
                return 6
            elif rad > -1.2044:
                return 7
            # elif rad > -1.5708:
            #     return 8
            elif rad > -1.9371:
                return 8
            elif rad > -2.4398:
                return 9
            elif rad > -2.8315:
                return 10
            elif rad > -3.0752:
                return 11
            else:  # rad >= -3.1415:
                return 12

    def die(self):
        if self.hp <= 0:
            DieMutal(self.stand_x, self.stand_y)
        # print(len(mutal.list))
        pass

    @staticmethod
    def make_mutal():
        if random.random() <= Mutal.zm:
            mutal = Mutal(random.randrange(Mutal.stand_sx, play_state.window_size[0] - Mutal.stand_sx),
                                play_state.window_size[1] + Mutal.stand_sy)
            # game_world.ground_obj.append(mutal)
            game_world.ground_obj.insert(0, mutal)

    @staticmethod
    def load_resource():
        Mutal.img = load_image("resource\\mutal\\mutal200x2.png")
        #Mutal.hit_sound = load_wav('resource\\mutal\\zulhit00.wav')
        #Sound.list.append(mutal.hit_sound)
        #Sound.volume_list.append(6)
        DieMutal.load_resource()


class DieMutal(Effect):
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
        self.start_frame = play_state.frame % self.any_frame_rate
        game_world.ground_obj.append(self)
        play_state.sound.Mutal_die = True

    def die(self):
        pass

    @staticmethod
    def play_sound():
        pass
        #DieMutal.sound.play()

    @staticmethod
    def load_resource():
        DieMutal.img = load_image("resource\\mutal\\die_mutal200.png")
        #DieMutal.sound = load_wav('resource\\mutal\\zzedth01.wav')
        #Sound.list.append(Diemutal.sound)
        #Sound.volume_list.append(8)
