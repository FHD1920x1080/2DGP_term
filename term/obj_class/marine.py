import play_state
from obj_class.obj import *

from obj_class.bullet import Bullet32

IDLE, MOVE, DASH, SHOOT, WAIT = range(5)

class Marine(GroundObj):
    unit_type = 0  # 마린인걸 인식하는데 씀, 골리앗은 1, 드라군은 2

    img = None
    portrait = None
    print_sx = 110
    print_sy = 85
    stand_sx = 18
    stand_sy = 18
    hit_sx = 24 # 히트박스 크기, 반쪽
    hit_sy = 30
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 20
    hit_y_gap = 20

    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.

    hit_sound = None
    shoot_sound00 = None
    shoot_sound01 = None
    shoot_sound02 = None
    shoot_sound03 = None

    def __init__(self):
        self.stand_x = play_state.window_size[0] / 2  # 마린이 서있는 좌표
        self.stand_y = 100
        self.face_dir = 0 #얼굴 방향
        self.hp = 200  # 체력
        self.max_hp = 200
        self.AD = 3  # 공격력
        self.img = Marine.img
        self.img_now = [30, 2180 - 80 - 320]  # 스프라이트 좌표
        self.speed = 2.8  # 이동속도w
        self.shoot_able = False  # 마우스 좌클릭이 눌렸는지
        self.move_able = True  # 움직일 수 있는 상태인지
        self.Wmove_able = True  # 움직일 수 있다면 가로로 움직이는지
        self.Hmove_able = True  # 움직일 수 있다면 세로로 움직이는지, 가로와 세로가 같이 움직일때 즉 대각선으로 이동할때 이동속도에 0.707을 곱해주기 위함
        self.idle = True  # 아무것도 안하고 있는지
        self.shoot_idle = True  # 총을 안쏘고 있는지(걸어다니는걸로는 안풀림)
        self.shoot_frame = 0  # 연사력과, 점사구현을 위한 프레임
        self.move_frame = 0  # 마린의 걸어다니는 애니메이션을 위한 프레임
        self.idle_frame = 0  # 아무것도 안한 시간만큼의 프레임
        self.shoot_idle_frame = 0  # 총을 안쏜 시간만큼의 프레임
        self.bullet_speed = 20  # 탄속
        self.moving_attack = False  # 1이면 움직이면서 공격 가능 g키
        self.nfs = 8  # 몇프레임당 공격이 나갈건지
        self.n_shot = 1  # 산탄량
        self.accuracy = 10  # 총의 정확도, 정확이는 오차율 0이 가장 높은 스텟
        self.interrupted_fire = 5  # 몇점사, 쏘는 시간만큼 쉼
        self.magazine_gun = False  # 연사모드
        self.rad = None
        self.x1, self.y1 = self.stand_x, self.stand_y  # 대쉬할때 필요함
        self.x2, self.y2 = 0, 0
        self.t = 0
        self.r = None
        self.dash_state = False
        self.dash_cool_time = 100  #
        self.cur_dash_cool_time = 0
        self.dash_frame = 0
        self.dash_dir = 0  # 16방향
        self.dash_speed = 17
        self.cur_dash_speed = 0 # self.dash_speed
        self.dash_accel = -0.73 # 같이 -0.9 / self.r로 초기화 해줌
        self.portrait_state = 0
        self.portrait_frame = 0

    def portrait_anim(self):
        if play_state.frame % 10 == 0:
            self.portrait_frame += 1
            if self.portrait_state == 0:
                if self.portrait_frame > 18:
                    self.portrait_frame = 0
                    self.rand_portrait()
            elif self.portrait_state == 1:
                if self.portrait_frame > 9:
                    self.portrait_frame = 0
                    self.rand_portrait()
            elif self.portrait_state == 2:
                if self.portrait_frame > 15:
                    self.portrait_frame = 0
                    self.rand_portrait()
            elif self.portrait_state == 3:
                if self.portrait_frame > 29:
                    self.portrait_frame = 0
                    self.rand_portrait()


    def rand_portrait(self):
        self.portrait_state = random.randint(0, 3)
        pass

    @staticmethod
    def play_shoot_sound():
        i = random.randint(0, 3)
        if i == 0:
            Marine.shoot_sound00.play()
        elif i == 1:
            Marine.shoot_sound01.play()
        elif i == 2:
            Marine.shoot_sound02.play()
        elif i == 3:
            Marine.shoot_sound03.play()
    # def x_move(self, x):
    #     self.stand_x += x
    #
    # def y_move(self, y):
    def update(self):
        self.check_magazine()
        if self.dash_state == True:
            self.dash()
        else:
            self.move()
            self.shoot()
        self.shoot_frame += 1
        if self.magazine_gun == False:
            if self.shoot_idle == True:
                self.shoot_idle_frame += 1
                if self.shoot_idle_frame > self.nfs * self.interrupted_fire - 1:
                    self.shoot_frame = 0
            else:
                self.shoot_idle_frame = 0
        if self.idle:
            self.idle_frame += 1
        else:
            self.idle_frame = 0
        if self.dash_state == True:
            if play_state.frame % 2 == 0:
                self.move_frame = (self.move_frame + 1) % 8
        else:
            if play_state.frame % 4 == 0:
                self.move_frame = (self.move_frame + 1) % 8
        self.cur_dash_cool_time -= 1
        if self.cur_dash_cool_time < 0:
            self.cur_dash_cool_time = 0

    def handle_events(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
                else:
                    User_input.left_button = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.face_dir, 1780
                else:
                    User_input.left_button = False

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                self.try_dash()
            elif event.key == SDLK_a:
                User_input.left_key = True
            elif event.key == SDLK_d:
                User_input.right_key = True
            elif event.key == SDLK_w:
                User_input.up_key = True
            elif event.key == SDLK_s:
                User_input.down_key = True
            elif event.key == SDLK_e:
                self.bullet_speed += 1
            elif event.key == SDLK_q:
                self.bullet_speed -= 1
            elif event.key == SDLK_r:
                self.nfs -= 1
                if self.nfs <= 0:
                    self.nfs = 1
            elif event.key == SDLK_f:
                self.nfs += 1
            elif event.key == SDLK_g:
                if self.moving_attack:
                    self.moving_attack = False
                else:
                    self.moving_attack = True
            elif event.key == SDLK_t:
                if self.magazine_gun == True:
                    self.magazine_gun = False
                    self.nfs //= 2
                    User_input.left_button = False
                    self.shoot_idle = True
                    self.shoot_idle_frame = 0
                    if self.nfs <= 0:
                        self.nfs = 1
                else:
                    self.magazine_gun = True
                    self.nfs *= 2
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                User_input.left_key = False
            elif event.key == SDLK_d:
                User_input.right_key = False
            elif event.key == SDLK_w:
                User_input.up_key = False
            elif event.key == SDLK_s:
                User_input.down_key = False

    def dash_move(self):
        self.x_move(math.cos(self.rad) * self.cur_dash_speed)
        self.y_move(math.sin(self.rad) * self.cur_dash_speed)
        self.cur_dash_speed += self.dash_accel

    def dash(self):
        self.dash_move()
        if self.get_stand_right() > play_state.window_size[0]:
            self.x_move(play_state.window_size[0] - self.get_stand_right())
        if self.get_stand_top() > play_state.window_size[1]:
            self.y_move(play_state.window_size[1] - self.get_stand_top())
        if self.get_stand_left() < 0:
            self.x_move(-self.get_stand_left())
        if self.get_stand_bottom() < 0:
            self.y_move(-self.get_stand_bottom())
        self.idle = False
        self.img_now = 30 + 160 * self.dash_dir, 1460 - (160 * self.move_frame)
        self.dash_frame += 1
        if self.dash_frame > 25: # 0 ~ 24
            self.dash_state = False
            self.dash_frame = 0
            self.shoot_frame = 0
        pass

    def try_dash(self):
        if self.cur_dash_cool_time > 0:
            print('cooltime')
            return
        self.cur_dash_cool_time = 1
        if self.idle:  # 가만히 있을 때 대쉬
            self.rad = get_rad(self.stand_x, self.stand_y, play_state.cursor.x, play_state.cursor.y)
            self.dash_dir = self.get_face_dir(self.rad)
            self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
            if self.r != 0:
                self.dash_set()
                return
        else:  # 움직이는 중, 또는 총 쏘는중
            if (User_input.left_key == True and User_input.right_key == False) or (
                    User_input.left_key == False and User_input.right_key == True):
                self.Wmove_able = True
            else:
                self.Wmove_able = False
            if (User_input.up_key == True and User_input.down_key == False) or (
                    User_input.up_key == False and User_input.down_key == True):
                self.Hmove_able = True
            else:
                self.Hmove_able = False

            if self.Wmove_able == False and self.Hmove_able == False: # 가만히서 총만 쏘고 있는 상황
                self.dash_dir = self.face_dir
                self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리
                if self.r != 0:
                    self.dash_set()
                return
            right, left, up, down = False, False, False, False  # 실질적인 입력값
            if self.Wmove_able:
                if User_input.right_key:
                    right = True
                else:
                    left = True
            if self.Hmove_able:
                if User_input.up_key:
                    up = True
                else:
                    down = True

            if right:
                if up:  # 오른쪽 위 대각선
                    self.dash_dir = 4
                    self.rad = 0.785398
                elif down:  # 오른쪽 아래 대각선
                    self.dash_dir = 12
                    self.rad = -0.785398
                else:  # 그냥 오른쪽
                    self.dash_dir = 8
                    self.rad = 0.0
                self.dash_set()
                return
            if left:
                if up:  # 왼쪽 위 대각선
                    self.dash_dir = 28
                    self.rad = 2.35619
                elif down:  # 왼쪽 아래 대각선
                    self.dash_dir = 20
                    self.rad = - 2.35619
                else:  # 그냥 왼쪽
                    self.dash_dir = 24
                    self.rad = 3.14159
                self.dash_set()
                return
            if up:  # 그냥 위
                self.dash_dir = 0
                self.rad = 1.5708
                self.dash_set()
                return
            if down:  # 그냥 아래
                self.dash_dir = 16
                self.rad = -1.5708
                self.dash_set()
                self.dash_set()
                return

    def dash_set(self):
        self.dash_state = True
        self.cur_dash_cool_time = self.dash_cool_time
        self.cur_dash_speed = self.dash_speed

    def move(self):
        if self.move_able == True:  # 움직이는 상태 말고, 움직여도 되는 상태인지(총쏘고있으면 해당 안됨.)
            if (User_input.left_key == True and User_input.right_key == False) or (
                    User_input.left_key == False and User_input.right_key == True):
                self.Wmove_able = True
            else:
                self.Wmove_able = False
            if (User_input.up_key == True and User_input.down_key == False) or (
                    User_input.up_key == False and User_input.down_key == True):
                self.Hmove_able = True
            else:
                self.Hmove_able = False
            if self.Wmove_able == False and self.Hmove_able == False:
                self.idle = True
                self.img_now = self.img_now[0], 2100
                return
            if self.Wmove_able == True and self.Hmove_able == True:
                speed = self.speed * 0.707
            else:
                speed = self.speed * 1

            right, left, up, down = False, False, False, False  # 실제 움직일 수 있는지를 담는 변수
            # 이 밑에선 실제로 움직일 수 있는지 검사
            if self.Wmove_able == True:
                if User_input.right_key == True:
                    if self.get_stand_right() + speed > play_state.window_size[0]:
                        self.x_move(play_state.window_size[0] - self.get_stand_right())
                    else:
                        right = True
                else:
                    if self.get_stand_left() - speed < 0:
                        self.x_move(-self.get_stand_left())
                    else:
                        left = True
            if self.Hmove_able == True:
                if User_input.up_key == True:
                    if self.get_stand_top() + speed > play_state.window_size[1]:
                        self.y_move(play_state.window_size[1] - self.get_stand_top())
                    else:
                        up = True
                else:
                    if self.get_stand_bottom() - speed < 0:
                        self.y_move(-self.get_stand_bottom())
                    else:
                        down = True

            if right:
                if up:  # 오른쪽 위 대각선
                    self.x_move(speed)
                    self.y_move(speed)
                    self.img_now = 30 + 320 * 2, 1460 - (160 * self.move_frame)
                elif down:  # 오른쪽 아래 대각선
                    self.x_move(speed)
                    self.y_move(-speed)
                    self.img_now = 30 + 320 * 6, 1460 - (160 * self.move_frame)
                else:  # 그냥 오른쪽
                    self.x_move(speed)
                    self.img_now = 30 + 320 * 4, 1460 - (160 * self.move_frame)
                    self.dash_dir = 8
                self.idle = False
                return
            if left:
                if up:  # 왼쪽 위 대각선
                    self.x_move(-speed)
                    self.y_move(speed)
                    self.img_now = 30 + 320 * 14, 1460 - (160 * self.move_frame)
                elif down:  # 왼쪽 아래 대각선
                    self.x_move(-speed)
                    self.y_move(-speed)
                    self.img_now = 30 + 320 * 10, 1460 - (160 * self.move_frame)
                else:  # 그냥 왼쪽
                    self.x_move(-speed)
                    self.img_now = 30 + 320 * 12, 1460 - (160 * self.move_frame)
                self.idle = False
                return
            if up:  # 그냥 위
                self.y_move(speed)
                self.img_now = 30, 1460 - (160 * self.move_frame)
                self.idle = False
                return
            if down:  # 그냥 아래
                self.y_move(-speed)
                self.img_now = 30 + 320 * 8, 1460 - (160 * self.move_frame)
                self.idle = False
                return
            print('can not move')
            self.img_now = self.img_now[0], 1460

    def check_magazine(self):
        if self.magazine_gun == False:  # 점사모드일때
            if User_input.left_button == True:
                if self.shoot_frame == 0:
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
            else:
                if self.shoot_frame // (self.nfs * self.interrupted_fire) % 2 != 0:
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.face_dir, 1780

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

    def shoot(self):
        if self.shoot_able == True:
            if self.magazine_gun == False:
                if (self.shoot_frame) // (self.nfs * self.interrupted_fire) % 2 != 0:  # 점사 구현
                    return
            if self.shoot_frame % self.nfs == 0:  # self.nfs은 마린이 몇프레임마다 쏠건지 1이 가장 빠름
                # 여기에 사운드
                # self.play_shoot_sound()
                play_state.sound.Marine_shoot = True
                for i in range(self.n_shot):
                    a = get_rad(self.stand_x, self.stand_y, play_state.cursor.x, play_state.cursor.y)
                    self.face_dir = self.get_face_dir(a)  # 각도를 가지고 마린이 바라볼 방향 정함.
                    x2, y2 = play_state.cursor.x + random.randint(-self.accuracy,
                                                                  self.accuracy), play_state.cursor.y + random.randint(
                        -self.accuracy, self.accuracy)
                    Bullet32(self, x2, y2)  # x1==x2 and y1==y2 일 때 False 반환
                    self.shoot_idle = False
                    self.idle = False
                    self.img_now = 30 + (160 * self.face_dir), 1620  # 격발 이미지
            elif self.shoot_frame % self.nfs == self.nfs // 2:
                self.img_now = 30 + (160 * self.face_dir), 1780  # 견착 이미지
        else:
            self.shoot_idle = True


    @staticmethod
    def load_resource():
        Marine.img = load_image('resource\\marine\\marine250x2_blue.png')
        Marine.portrait = load_image('resource\\marine\\marine_portrait.png')
        Marine.shoot_sound00 = load_wav('resource\\marine\\shoot_sound\\00.wav')
        Marine.shoot_sound01 = load_wav('resource\\marine\\shoot_sound\\01.wav')
        Marine.shoot_sound02 = load_wav('resource\\marine\\shoot_sound\\02.wav')
        Marine.shoot_sound03 = load_wav('resource\\marine\\shoot_sound\\03.wav')
        Sound.list.append(Marine.shoot_sound00)
        Sound.volume_list.append(16)
        Sound.list.append(Marine.shoot_sound01)
        Sound.volume_list.append(16)
        Sound.list.append(Marine.shoot_sound02)
        Sound.volume_list.append(16)
        Sound.list.append(Marine.shoot_sound03)
        Sound.volume_list.append(16)
