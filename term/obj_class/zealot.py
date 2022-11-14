from obj_class.obj import *

AUTO, LOCK_ON, ATTACK, WAIT = range(4)


class Zealot(GroundObj):
    img = None

    print_sx = 110
    print_sy = 78
    stand_sx = 20
    stand_sy = 20
    hit_sx = 20
    hit_sy = 28
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 21
    hit_y_gap = 21

    hp = 10
    speed = 2.5
    zm = 0.1

    attack_sound = None
    def __init__(self, x, y):
        self.exist = True  # 존재 변수 삭제 할지 판정
        self.collision = True  # 충돌체크 함.
        self.img_now = [4169, 1881]  ##256, 256 씩 옮겨야 함 73,3328-167 맨위에 첫 이미지
        self.stand_x = x
        self.stand_y = y
        self.hp = Zealot.hp
        self.speed = Zealot.speed
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
    def play_attack_sound():
        Zealot.attack_sound.play()

    def stop(self):
        self.img_now = self.img_now[0], 1881

    def move_down(self):
        if self.get_hit_top() < 0:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        self.y_move(- self.speed)
        self.img_now = 4169, 1881 - 256 * self.move_frame

    def move_left_down(self):
        if self.get_hit_top() < 0:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = self.speed * 0.707
        self.y_move(-cur_speed)
        self.x_move(-cur_speed)
        self.img_now = 73 + 256 * 20, 1881 - 256 * self.move_frame
        if self.get_stand_left() < 0:
            self.x_move_point(self.stand_sx)
            self.direction = random.randrange(1, 3)
            if self.direction == 2:
                self.direction = 3

    def move_right_down(self):
        if self.get_hit_top() < 0:
            self.exist = False  # 화면 밖으로 나갔으니 없애버려라
            return False
        cur_speed = self.speed * 0.707
        self.y_move(-cur_speed)
        self.x_move(cur_speed)
        self.img_now = 73 + 256 * 12, 1881 - 256 * self.move_frame
        if self.get_stand_right() > play_state.window_size[0]:
            self.x_move_point(play_state.window_size[0] - self.stand_sx)
            self.direction = random.randrange(1, 3)

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

    def anim(self):
        if self.state > LOCK_ON:  # ATTACK, WAIT
            if self.time % 4 == 0:
                self.attack_frame += 1
        else:
            if self.time % 4 == 0:
                self.move_frame = (self.move_frame + 1) % 8

    def update(self):
        if self.state == AUTO:
            self.auto_move()  # atuo move에서 바로 LOCK_ON으로 갈 수 있음.
        elif self.state == LOCK_ON:  # player를 발견한 상태
            if self.time % 50 == 0:  # 0.5초마다 방향 조정
                self.dir_adjust()
            self.lock_on_move()
        elif self.state == ATTACK:
            self.attack()
        elif self.state == WAIT:
            self.wait()
        cheak_collision_min_move(self, play_state.player)

        self.anim()
        self.time += 1

    def dir_adjust(self):
        self.rad = get_rad(self.stand_x, self.stand_y, play_state.player.stand_x, play_state.player.stand_y)
        self.face_dir = self.get_face_dir(self.rad)
        # 여기서 사인 코사인 써서 이동하면 거리를 더 안재도 되겠네? 바보였잖아 나

    def lock_on_move(self):
        self.x_move(math.cos(self.rad) * self.speed)
        self.y_move(math.sin(self.rad) * self.speed)
        self.img_now = 73 + 256 * self.face_dir, 1881 - 256 * self.move_frame
        r = math.dist([self.stand_x, self.stand_y],
                      [play_state.player.stand_x, play_state.player.stand_y])  # 두 점 사이의 거리
        if r > 0:
            if play_state.player.unit_type == 0:
                if r < 60:
                    self.time = 0
                    self.state = ATTACK
            else:
                if r < 80:
                    self.time = 0
                    self.state = ATTACK

    def attack(self):
        self.img_now = 73 + 256 * self.face_dir, 3161 - 256 * self.attack_frame
        if self.attack_frame == 1:
            play_state.sound.Zealot_attack = True
        elif self.attack_frame > 4:  # 여기서는 0, 1, 2, 3 ,4 동안 머물고 5가 되면 나감
            self.state = WAIT

    def wait(self):
        self.img_now = 73 + 256 * self.face_dir, 3161
        if self.attack_frame > 15:
            self.state = LOCK_ON
            self.attack_frame = 0
            self.time = 0
            self.dir_adjust()

    def die(self):
        if self.hp <= 0:
            Die_Zealot(self.stand_x, self.stand_y)

    def get_face_dir(self, rad):
        if rad >= 0:  # 1, 2 사분면
            if rad < 0.1963:  # 우측
                return 8
            elif rad < 0.589:
                return 6
            elif rad < 1.0517:
                return 4
            elif rad < 1.3844:
                return 2
            # elif rad < 1.5708:
            #     return 0
            elif rad < 1.8:
                return 0
            elif rad < 2.0898:
                return 30
            elif rad < 2.5525:
                return 28
            elif rad < 2.9452:
                return 26
            else:  # rad <= 3.1415:
                return 24
        else:  # 3,4분면
            if rad > -0.0663:  # 우측
                return 8
            elif rad > -0.31:
                return 10
            elif rad > -0.7017:
                return 12
            elif rad > -1.2044:
                return 14
            elif rad > -1.5708:
                return 16
            elif rad > -1.9371:
                return 17
            elif rad > -2.4398:
                return 18
            elif rad > -2.8315:
                return 20
            elif rad > -3.0752:
                return 22
            else:  # rad >= -3.1415:
                return 24

    @staticmethod
    def make_zealot():
        if random.random() <= Zealot.zm:
            zealot = Zealot(random.randrange(Zealot.stand_sx, play_state.window_size[0] - Zealot.stand_sx),
                            play_state.window_size[1] + Zealot.stand_sy)
            #game_world.ground_obj.append(zealot)
            game_world.ground_obj.insert(0, zealot)

    @staticmethod
    def load_resource():
        Zealot.img = load_image("resource\\zealot\\zealot200x2.png")
        Zealot.attack_sound = load_wav('resource\\zealot\\pzehit00.wav')
        Sound.list.append(Zealot.attack_sound)
        Sound.volume_list.append(6)

        Die_Zealot.load_resource()


class Die_Zealot(Effect):
    img = None
    sound = None
    print_sx = 100
    print_sy = 142
    print_x_gap = 0  # 그려줄 위치와 stand_x와의 차이
    print_y_gap = 46  # stand_y와의 차이
    anim_direction = 'w'  # 스프라이트 이미지 재생 방향
    next_gap = 256
    max_frame = 7  # 몇개의 이미지로 되어있는 이펙트인가
    any_frame_rate = 6
    def __init__(self, x, y): #질럿이 죽은 위치
        self.exist = True # 존재함
        self.stand_x = x
        self.stand_y = y
        self.print_x, self.print_y = self.stand_x + self.print_x_gap, self.stand_y + self.print_y_gap
        self.img_now = [85, 80]  # 스프라이트 좌표
        self.cur_frame = 0  # 100이 되면 저글링 시체 사라짐
        game_world.ground_obj.append(self)
        play_state.sound.Zealot_die = True

    @staticmethod
    def play_sound():
        Die_Zealot.sound.play()

    @staticmethod
    def load_resource():
        Die_Zealot.img = load_image("resource\\zealot\\die_zealot200.png")
        Die_Zealot.sound = load_wav('resource\\zealot\\pzedth00.wav')
        Sound.list.append(Die_Zealot.sound)
        Sound.volume_list.append(8)


class Die_Zealot_copy:
    img = None
    sound = None
    list = []

    print_sx = 100
    print_sy = 142

    def __init__(self, x, y):
        super().__init__()
        play_state.sound.Zealot_die = True
        self.print_x = x
        self.print_y = y
        self.img_now = [78, 80]  # 스프라이트 좌표
        self.die_frame = 0  # 100이 되면 저글링 시체 사라짐

    def die_anim(self):
        if self.die_frame < 7:
            self.img_now[0] = 78 + self.die_frame * 256
        self.die_frame += 1

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.print_sx, self.print_sy, self.print_x, self.print_y)
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
        Sound.list.append(Die_Zealot.sound)
        Sound.volume_list.append(8)
