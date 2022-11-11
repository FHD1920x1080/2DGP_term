from obj_class.obj import *

IDLE, MOVE, DASH, SHOOT, WAIT = range(5)

class Marine(RealObj):
    list = []
    img = None
    hit_sound = None
    shoot_sound00 = None
    shoot_sound01 = None
    shoot_sound02 = None
    shoot_sound03 = None
    unit_type = 0 # 총알에서 마린인걸 인식하는데 씀, 골리앗은 1



    x_gap = 0
    hit_x_gap = 0
    y_gap = 20
    hit_y_gap = 20
    def __init__(self):
        super().__init__()
        self.hp = 100  # 체력
        self.AD = 2  # 공격력
        self.img = Marine.img
        self.dash_state = False
        self.sx, self.sy = 110, 85  # 그려줄 스프라이트 크기
        self.img_now = [30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)]  # 스프라이트 좌표
        self.stand_x = play_state.window_size[0] / 2  # 마린이 서있는 좌표
        self.stand_y = play_state.window_size[1] / 2
        self.x = self.stand_x  # 마린을 그려줄 좌표
        self.y = self.stand_y + 20
        self.stand_sx = 18  # 마린이 밟을 수 있는 땅의 넓이
        self.stand_sy = 18
        self.hit_sx = 24 # 마린의 히트박스 크기
        self.hit_sy = 36
        self.hit_x = self.x  # 마린의 히트박스 중앙 좌표
        self.hit_y = self.y
        self.speed = 3  # 이동속도
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
        self.nfs = 15  # 몇프레임당 공격이 나갈건지
        self.n_shot = 1  # 산탄량
        self.accuracy = 10  # 총의 정확도, 정확이는 오차율 0이 가장 높은 스텟
        self.interrupted_fire = 5  # 몇점사, 쏘는 시간만큼 쉼
        self.magazine_gun = True  # 연사모드
    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)

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

    def update(self):
        self.check_magazine()
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
                    self.img_now = 30 + 160 * self.look_now, 1780
                else:
                    User_input.left_button = False

        if event.type == SDL_KEYDOWN:

            if event.key == SDLK_a:
                User_input.left_key = True
            elif event.key == SDLK_d:
                User_input.right_key = True
            if event.key == SDLK_w:
                User_input.up_key = True
            elif event.key == SDLK_s:
                User_input.down_key = True
            if event.key == SDLK_e:
                self.bullet_speed += 1
            if event.key == SDLK_q:
                self.bullet_speed -= 1
            if event.key == SDLK_r:
                self.nfs -= 1
                if self.nfs <= 0:
                    self.nfs = 1
            if event.key == SDLK_f:
                self.nfs += 1
            if event.key == SDLK_g:
                if self.moving_attack:
                    self.moving_attack = False
                else:
                    self.moving_attack = True
            if event.key == SDLK_t:
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
            if event.key == SDLK_SPACE:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
                else:
                    User_input.left_button = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                User_input.left_key = False
            elif event.key == SDLK_d:
                User_input.right_key = False
            if event.key == SDLK_w:
                User_input.up_key = False
            elif event.key == SDLK_s:
                User_input.down_key = False
            if event.key == SDLK_SPACE:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
                else:
                    User_input.left_button = False

    def dash(self):
        #쿨타임이 안찼을 때:
            #return
        if User_input.up_key == False and User_input.down_key == False and User_input.right_key == False and User_input.left_key == False:
            a = get_rad(self.stand_x, self.stand_y, play_state.cursor.x, play_state.cursor.y)
            self.look_now = self.get_look_now(a)
            self.img_now = 30 + 160 * self.look_now, 1780
        pass

    def move(self):
        if self.move_able == True: # 움직이는 상태 말고, 움직여도 되는 상태인지(총쏘고있으면 해당 안됨.)
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
                    if self.get_right() + speed > play_state.window_size[0]:
                        self.x_move(play_state.window_size[0] - self.get_right())
                    else:
                        right = True
                else:
                    if self.get_left() - speed < 0:
                        self.x_move(-self.get_left())
                    else:
                        left = True
            if self.Hmove_able == True:
                if User_input.up_key == True:
                    if self.get_top() + speed > play_state.window_size[1]:
                        self.y_move(play_state.window_size[1] - self.get_top())
                    else:
                        up = True
                else:
                    if self.get_bottom() - speed < 0:
                        self.y_move(-self.get_bottom())
                    else:
                        down = True

            if right:
                if up:  # 오른쪽 위 대각선
                    self.x_move(speed)
                    self.y_move(speed)
                    self.img_now = 30 + 320 * 2, 1460 - (160 * self.move_frame)
                elif down: # 오른쪽 아래 대각선
                    self.x_move(speed)
                    self.y_move(-speed)
                    self.img_now = 30 + 320 * 6, 1460 - (160 * self.move_frame)
                else: # 그냥 오른쪽
                    self.x_move(speed)
                    self.img_now = 30 + 320 * 4, 1460 - (160 * self.move_frame)
                self.idle = False
                return
            if left:
                if up:  # 왼쪽 위 대각선
                    self.x_move(-speed)
                    self.y_move(speed)
                    self.img_now = 30 + 320 * 14, 1460 - (160 * self.move_frame)
                elif down: # 왼쪽 아래 대각선
                    self.x_move(-speed)
                    self.y_move(-speed)
                    self.img_now = 30 + 320 * 10, 1460 - (160 * self.move_frame)
                else: # 그냥 왼쪽
                    self.x_move(-speed)
                    self.img_now = 30 + 320 * 12, 1460 - (160 * self.move_frame)
                self.idle = False
                return
            if up: # 그냥 위
                self.y_move(speed)
                self.img_now = 30, 1460 - (160 * self.move_frame)
                self.idle = False
                return
            if down: # 그냥 아래
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
                    self.img_now = 30 + 160 * self.look_now, 1780

    def get_look_now(self, rad):
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
                    self.look_now = self.get_look_now(a)  # 각도를 가지고 마린이 바라볼 방향 정함.
                    x2, y2 = play_state.cursor.x + random.randint(-self.accuracy,
                                                                  self.accuracy), play_state.cursor.y + random.randint(
                        -self.accuracy, self.accuracy)
                    bullet = Bullet32(self, x2, y2)  # x1==x2 and y1==y2 일 때 False 반환
                    if bullet == False:
                        print('총알 발사 안됨')
                        return
                    # if bullet.r == 0:
                    #     print(bullet.x1, bullet.x2)
                    #     del bullet
                    #     return
                    game_world.bullet_list.append(bullet)
                    self.shoot_idle = False
                    self.idle = False
                    self.img_now = 30 + (160 * self.look_now), 1620  # 격발 이미지
            elif self.shoot_frame % self.nfs == self.nfs // 2:
                self.img_now = 30 + (160 * self.look_now), 1780  # 견착 이미지
        else:
            self.shoot_idle = True

    @staticmethod
    def load_resource():
        Marine.img = load_image('resource\\marine\\marine250x2.png')
        Marine.shoot_sound00 = load_wav('resource\\marine\\shoot_sound\\00.wav')
        Marine.shoot_sound00.set_volume(16)
        Marine.shoot_sound01 = load_wav('resource\\marine\\shoot_sound\\01.wav')
        Marine.shoot_sound01.set_volume(16)
        Marine.shoot_sound02 = load_wav('resource\\marine\\shoot_sound\\02.wav')
        Marine.shoot_sound02.set_volume(16)
        Marine.shoot_sound03 = load_wav('resource\\marine\\shoot_sound\\03.wav')
        Marine.shoot_sound03.set_volume(16)