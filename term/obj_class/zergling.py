from obj_class.obj import *

AUTO, LOCK_ON, ATTACK = range(3)

class Zergling(GroundObj):
    img = None
    print_sx = 80
    print_sy = 78
    stand_sx = 18
    stand_sy = 16
    hit_sx = 22
    hit_sy = 20
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 5
    hit_y_gap = 5

    hp = 6
    speed = 3
    speed_sup = speed / 3 # 저글링은 프레임마다 속도가 달라서 만들어준 변수 기본속도가 3이라고 가정하고 만듦
    zm = 0.02

    def __init__(self, x, y):
        self.exist = True  # 존재 변수 삭제 할지 판정
        self.collision = True  # 충돌체크 함.s
        self.img_now = [692, 1138]  ##86, 84 씩 옮겨야 함
        self.stand_x = x
        self.stand_y = y
        self.hp = Zergling.hp
        self.speed = Zergling.speed
        self.move_frame = 0
        self.attack_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)
        self.exist = True  # 충돌 gn False로 바꿔줄 존재 변수
        self.face_dir = 0
        self.state = AUTO
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.Y2 = None
        self.t = 0
        self.r = None

    def stop(self):
        self.img_now = self.img_now[0], 1138

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
            self.exist = False # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = Zergling.get_speed(self)
        self.y_move(- cur_speed)
        self.img_now = 692, 1138 - 84 * self.move_frame

    def move_left_down(self):
        if self.get_hit_top() < 0:
            self.exist = False # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = Zergling.get_speed(self) * 0.707
        self.y_move(-cur_speed)
        self.x_move(-cur_speed)
        self.img_now = 692 + 86 * 2, 1138 - 84 * self.move_frame
        if self.get_stand_left() < 0:
            self.x_move_point(self.stand_sx)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        if self.get_hit_top() < 0:
            self.exist = False # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = Zergling.get_speed(self) * 0.707
        self.y_move(-cur_speed)
        self.x_move(cur_speed)
        self.img_now = 520, 1138 - 84 * self.move_frame
        if self.get_stand_right() > play_state.window_size[0]:
            self.x_move_point(play_state.window_size[0]-self.stand_sx)
            self.direction = random.randrange(1, 3)

    def anim(self):
        if self.time % 6 == 0:
            self.move_frame = (self.move_frame + 1) % 7

    def auto_move(self):
        if (self.direction == 0):
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
        #if self.state == AUTO:
        self.auto_move()
        cheak_collision_min_move(self, play_state.player)
        self.anim()
        self.time += 1

    def die(self):
        if self.hp <= 0:
            Die_Zergling(self.stand_x, self.stand_y)
        #print(len(Zergling.list))
        pass

    @staticmethod
    def make_zergling():
        if random.random() <= Zergling.zm:
            zergling = Zergling(random.randrange(Zergling.stand_sx , play_state.window_size[0] - Zergling.stand_sx), play_state.window_size[1] + Zergling.stand_sy)
            game_world.ground_obj.append(zergling)

    @staticmethod
    def load_resource():
        Zergling.img = load_image("resource\\zergling\\zerglingx200x2.png")
        Die_Zergling.load_resource()


class Die_Zergling(Effect):
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
        self.exist = True # 존재함
        self.stand_x = x
        self.stand_y = y
        self.print_x, self.print_y = self.stand_x + self.print_x_gap, self.stand_y + self.print_y_gap
        self.img_now = [2, 0]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        game_world.ground_obj.append(self)
        play_state.sound.Zergling_die = True

    @staticmethod
    def play_sound():
        Die_Zergling.sound.play()


    @staticmethod
    def load_resource():
        Die_Zergling.img = load_image("resource\\zergling\\die_zergling.png")
        Die_Zergling.sound = load_wav('resource\\zergling\\zzedth01.wav')
        Sound.list.append(Die_Zergling.sound)
        Sound.volume_list.append(8)