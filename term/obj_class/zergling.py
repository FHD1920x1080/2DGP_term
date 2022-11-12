from obj_class.obj import *

AUTO, LOCK_ON, ATTACK = range(3)

class Zergling(RealObj):
    sum = 0
    sx = 80
    sy = 78
    stand_sx = 18
    stand_sy = 16
    hit_sx = 22
    hit_sy = 20
    hp = 6
    speed = 3
    img = None
    zm = 0.02

    x_gap = 0
    hit_x_gap = 0
    y_gap = 5
    hit_y_gap = 5
    def __init__(self, x, y):
        self.img_now = [692, 1138]  ##86, 84 씩 옮겨야 함
        self.stand_x = x
        self.stand_y = y
        self.x = self.stand_x
        self.y = self.stand_y + 5
        self.hit_x = self.x
        self.hit_y = self.y
        self.hp = Zergling.hp
        self.stand_sx = Zergling.stand_sx
        self.stand_sy = Zergling.stand_sy
        self.hit_sx = Zergling.hit_sx
        self.hit_sy = Zergling.hit_sy
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
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.Y2 = None
        self.t = 0
        self.r = None

    def show(self):
        Zergling.img.clip_draw(self.img_now[0], self.img_now[1], Zergling.sx, Zergling.sy, self.x, self.y)
        #draw_rectangle(*self.get_stand_box())

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
        if self.get_left() - cur_speed < 0:
            self.x_move(round(self.stand_sx / 2) - self.stand_x)
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
        if self.get_right() + cur_speed > play_state.window_size[0]:
            self.x_move(play_state.window_size[0] - (self.stand_x + round(self.stand_sx / 2)))
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
        die_zergling = Die_Zergling(self.stand_x, self.stand_y - 5)
        play_state.sound.Zergling_die = True
        game_world.die_list.append(die_zergling)  # 죽은 저글링 리스트에 추가함
        game_world.ground_enemy.remove(self)
        del self  # 실제 저글링은 삭제
        #print(len(Zergling.list))
        pass

    @staticmethod
    def make_zergling():
        if random.random() <= Zergling.zm:
            Zergling.sum += 1
            zergling = Zergling(random.randrange(round(Zergling.sx / 2), play_state.window_size[0] - round(Zergling.sx / 2)),
                                play_state.window_size[1] + Zergling.sy)
            game_world.ground_enemy.append(zergling)
    @staticmethod
    def load_resource():
        Zergling.img = load_image("resource\\zergling\\zerglingx200x2.png")
        Die_Zergling.load_resource()


class Die_Zergling(Obj):
    img = None
    sound = None
    list = []

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
        Die_Zergling.img.clip_draw(self.img_now_x, 0, 130, 106, self.x, self.y)


    @staticmethod
    def play_sound():
        Die_Zergling.sound.play()

    def anim(self):
        self.die_anim()
        if self.die_frame > play_state.FPS:  # 일정 시간이 지난 시체 3초
            game_world.die_list.remove(self)
            del self

    @staticmethod
    def load_resource():
        Die_Zergling.img = load_image("resource\\zergling\\die_zergling.png")
        Die_Zergling.sound = load_wav('resource\\zergling\\zzedth01.wav')
        Sound.list.append(Die_Zergling.sound)
        Sound.volume_list.append(8)