import game_world
from obj_class.obj import *

class Zealot(RealObj):
    sum = 0
    list = []
    sx = 110
    sy = 78
    stand_sx = 20
    stand_sy = 20
    hit_sx = 20
    hit_sy = 31
    hp = 10
    speed = 2.5
    img = None
    zm = 0.01
    def __init__(self, x, y):
        super().__init__()
        self.img_now = [4169, 1881]  ##256, 256 씩 옮겨야 함 73,3328-167 맨위에 첫 이미지
        self.stand_x = x
        self.stand_y = y
        self.x = self.stand_x
        self.y = self.stand_y + 21
        self.hit_x = self.x
        self.hit_y = self.y
        self.hp = Zealot.hp
        self.stand_sx = Zealot.stand_sx
        self.stand_sy = Zealot.stand_sy
        self.hit_sx = Zealot.hit_sx
        self.hit_sy = Zealot.hit_sy
        self.speed = Zealot.speed
        self.move_frame = 0
        self.time = 0  # direction_rand_time
        self.direction = random.randrange(0, 4)  # 0==멈춤,1==아래,2==왼쪽 3==오른쪽
        self.direction_rand_time = random.randrange(50, 200)

    def show(self):
        Zealot.img.clip_draw(self.img_now[0], self.img_now[1], Zealot.sx, Zealot.sy, self.x, self.y)

    @staticmethod
    def show_All():
        for zl in Zealot.list:
            zl.show()
        for zl in Die_Zealot.list:
            zl.show()

    def stop(self):
        self.img_now = self.img_now[0], 1881


    def move_down(self):
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        i = self.speed
        self.y_move(- i)
        self.img_now = 4169, 1881 - 256 * self.move_frame

    def move_left_down(self):
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        i = self.speed
        self.y_move(- i * 0.707)
        self.x_move(- i * 0.707)
        self.img_now = 73 + 256 * 20, 1881 - 256 * self.move_frame
        if self.stand_x - self.speed * 0.707 <= round(self.stand_sx / 2):
            self.x_move(round(self.stand_sx / 2) - self.stand_x)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        if self.stand_y < -self.sy:  # 아래쪽 화면 범위 밖으로 나갔을때
            return 1  # 저글링이 화면 밖으로 나갔으니 없애버려라
        i = self.speed
        # i = zgl.move_frame - 6 #0 1 2 3 4 5 6 -3 -2 -1 0 1 2 3
        self.y_move(- i * 0.707)
        self.x_move(+ i * 0.707)
        self.img_now = 73 + 256 * 12, 1881 - 256 * self.move_frame
        if self.stand_x + self.speed * 0.707 >= play_state.window_size[0] - round(self.stand_sx / 2):
            self.x_move(play_state.window_size[0] - (self.stand_x + round(self.stand_sx / 2)))
            self.direction = random.randrange(1, 3)

    def move(self):
        self.time += 1
        if self.direction == 0:
            self.stop()
        elif self.direction == 1:
            if self.move_down() == 1:
                return 1
        if self.direction == 2:
            if self.move_left_down() == 1:
                return 1
        elif self.direction == 3:
            if self.move_right_down() == 1:
                return 1

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
        die_zealot = Die_Zealot(self.stand_x, self.stand_y + 46)
        play_state.sound.Zealot_die = True
        game_world.die_list.append(die_zealot)  # 죽은 리스트에 추가함
        game_world.Zealot_list.remove(self)
        del self  # 실제 저글링은 삭제
        #print(len(Zealot.list))
        pass
    @staticmethod
    def list_move():
        zd_list = []
        for i in range(len(Zealot.list)):  # 저글링 다운
            zgl = Zealot.list[i]
            if zgl.move() == 1:
                zd_list.append(i)

        zd_list.sort(reverse=True)
        for d in zd_list:
            #Zealot.list[d].die()
            del Zealot.list[d]
    @staticmethod
    def make_zealot():
        if random.random() <= Zealot.zm:
            zealot = Zealot(random.randrange(round(Zealot.sx / 2), play_state.window_size[0] - round(Zealot.sx / 2)),
                                play_state.window_size[1] + Zealot.sy)
            game_world.Zealot_list.append(zealot)
    @staticmethod
    def load_resource():
        Zealot.img = load_image("resource\\zealot\\zealot200x2.png")
        Die_Zealot.load_resource()


class Die_Zealot(Obj):
    img = None
    sound = None
    list = []

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.img_now_x = 78  # 스프라이트 좌표
        self.die_frame = 0  # 100이 되면 저글링 시체 사라짐

    def die_anim(self):
        if self.die_frame < 7:
            self.img_now_x = 78 + self.die_frame * 256
        self.die_frame += 1

    def show(self):
        Die_Zealot.img.clip_draw(self.img_now_x, 80, 110, 142, self.x, self.y)
        pass


    @staticmethod
    def play_sound():
        Die_Zealot.sound.play()

    def anim(self):
        self.die_anim()
        if self.die_frame > 7:  # 일정 시간이 지난 시체 3초
            game_world.die_list.remove(self)
            del self

    @staticmethod
    def load_resource():
        Die_Zealot.img = load_image("resource\\zealot\\die_zealot200.png")
        Die_Zealot.sound = load_wav('resource\\zealot\\pzedth00.wav')
        Die_Zealot.sound.set_volume(8)