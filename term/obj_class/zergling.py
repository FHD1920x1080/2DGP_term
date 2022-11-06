from obj_class.obj import *

class Zergling(RealObj):
    sum = 0
    list = []
    sx = 80
    sy = 78
    stand_sx = 36
    stand_sy = 32
    hit_sx = 44
    hit_sy = 40
    hp = 3
    speed = 3
    img = None
    zm = 0.03
    def __init__(self, x, y):
        super().__init__()
        self.hp = Zergling.hp
        # self.put_img("zerglingx200x2.png")
        self.img_now = [692, 1138]  ##86, 84 씩 옮겨야 함
        self.stand_x = x
        self.stand_y = y
        self.stand_sx = Zergling.stand_sx
        self.stand_sy = Zergling.stand_sy
        self.x = self.stand_x
        self.y = self.stand_y + 5
        self.hit_x = self.x
        self.hit_y = self.y
        self.hit_sx = Zergling.hit_sx
        self.hit_sy = Zergling.hit_sx
        self.speed = Zergling.speed
        self.move_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)

    def show(self):
        Zergling.img.clip_draw(self.img_now[0], self.img_now[1], Zergling.sx, Zergling.sy, self.x, self.y)

    @staticmethod
    def show_All():
        for zg in Die_Zergling.list:
            zg.show()

        for zg in Zergling.list:
            zg.show()

    def stop(self):
        self.img_now = self.img_now[0], 1138

    def get_speed(self):
        if self.move_frame == 0:
            return 1
        elif self.move_frame == 1:
            return 2
        elif self.move_frame == 2:
            return 5
        elif self.move_frame == 3:
            return 4
        elif self.move_frame == 4:
            return 4
        elif self.move_frame == 5:
            return 3
        elif self.move_frame == 6:
            return 2

    def move_down(self):
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        i = Zergling.get_speed(self) * self.speed / 3
        self.y_move(- i)
        self.img_now = 692, 1138 - 84 * self.move_frame

    def move_left_down(self):
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        i = Zergling.get_speed(self) * self.speed / 3
        self.y_move(- i * 0.707)
        self.x_move(- i * 0.707)
        self.img_now = 692 + 86 * 2, 1138 - 84 * self.move_frame
        if self.stand_x - self.speed * 0.707 <= round(self.stand_sx / 2):
            self.x_move(round(self.stand_sx / 2) - self.stand_x)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        i = Zergling.get_speed(self) * self.speed / 3
        # i = zgl.move_frame - 6 #0 1 2 3 4 5 6 -3 -2 -1 0 1 2 3
        self.y_move(- i * 0.707)
        self.x_move(+ i * 0.707)
        self.img_now = 520, 1138 - 84 * self.move_frame
        if self.stand_x + self.speed * 0.707 >= play_state.window_size[0] - round(self.stand_sx / 2):
            self.x_move(play_state.window_size[0] - (self.stand_x + round(self.stand_sx / 2)))
            self.direction = random.randrange(1, 3)

    def move(self):
        self.time += 1
        if (self.direction == 0):
            self.stop()
        elif (self.direction == 1):
            if self.move_down() == 1:
                Zergling.sum -= 1
                return 1
        if (self.direction == 2):
            if self.move_left_down() == 1:
                Zergling.sum -= 1
                return 1
        elif (self.direction == 3):
            if self.move_right_down() == 1:
                Zergling.sum -= 1
                return 1
        for zz in Zergling.list:
            cheak_collision(self, zz)
        for mm in play_state.Marine.list:
            cheak_collision(self, mm)

        if self.time % self.direction_rand_time == 0:
            j = self.direction
            self.direction = random.randrange(0, 4)
            if j == 0 and self.direction != 0:  # 멈춰있었다가 움직이면 무브프레임 초기화
                self.move_frame = 0
            if self.direction == 0:
                self.direction_rand_time = self.time + random.randrange(10, 30)
            else:
                self.direction_rand_time = self.time + random.randrange(50, 200)

    def die(self):
        die_zergling = Die_Zergling(self.stand_x, self.stand_y - 5)
        play_state.sound.Zergling_die = True
        Die_Zergling.list.append(die_zergling)  # 죽은 저글링 리스트에 추가함
        Zergling.list.remove(self)
        del self  # 실제 저글링은 삭제
        print(len(Zergling.list))
        pass
    @staticmethod
    def list_move():
        zd_list = []
        for i in range(len(Zergling.list)):  # 저글링 다운
            zgl = Zergling.list[i]
            if zgl.move() == 1:
                zd_list.append(i)

        zd_list.sort(reverse=True)
        for d in zd_list:
            #Zergling.list[d].die()
            del Zergling.list[d]

    @staticmethod
    def make_zergling():
        if random.random() <= Zergling.zm:
            Zergling.sum += 1
            zergling = Zergling(random.randrange(round(Zergling.sx / 2), play_state.window_size[0] - round(Zergling.sx / 2)),
                                play_state.window_size[1] + Zergling.sy)
            Zergling.list.append(zergling)
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

    def play_sound(self):
        Die_Zergling.sound.play()

    @staticmethod
    def anim():
        dz2_list = []
        for i in range(len(Die_Zergling.list)):
            Die_Zergling.list[i].die_anim()
            if Die_Zergling.list[i].die_frame > play_state.FPS:  # 일정 시간이 지난 시체 3초
                dz2_list.append(i)
        dz2_list.sort(reverse=True)
        for dz2 in dz2_list:
            del Die_Zergling.list[dz2]

    @staticmethod
    def load_resource():
        Die_Zergling.img = load_image("resource\\zergling\\die_zergling.png")
        Die_Zergling.sound = load_wav('resource\\zergling\\zzedth01.wav')
        Die_Zergling.sound.set_volume(8)