from obj_class.bullet import *
import play_state


class Marine(RealObj):
    list = []
    img = None
    hit_sound = None

    shoot_sound00 = None
    shoot_sound01 = None
    shoot_sound02 = None
    shoot_sound03 = None
    def __init__(self):
        super().__init__()
        self.bullet_list = []  # 발사된 총알 리스트
        self.effect_list = []  # 총알과 오브젝트의 충돌 시 생성된 이펙트 리스트
        self.hp = 100  # 체력
        self.AD = 1  # 공격력
        self.img = Marine.img
        self.sx, self.sy = 110, 85  # 그려줄 스프라이트 크기
        self.img_now = [30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)]  # 스프라이트 좌표
        self.hit_sx, self.hit_sy = 48, 72  # 마린의 히트박스 크기
        self.stand_x = play_state.window_size[0] / 2  # 마린이 서있는 좌표
        self.stand_y = play_state.window_size[1] / 2
        self.x = self.stand_x  # 마린을 그려줄 좌표
        self.y = self.stand_y + 20
        self.stand_sx = 36  # 마린이 밟을 수 있는 땅의 넓이
        self.stand_sy = 36
        self.hit_x = self.x  # 마린의 히트박스 중앙 좌표
        self.hit_y = self.y
        self.speed = 3  # 이동속도
        self.left_move = False  # 왼쪽으로 가는키가 눌렸는지
        self.right_move = False
        self.up_move = False
        self.down_move = False
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
        self.nfs = 12  # 몇프레임당 공격이 나갈건지
        self.n_shot = 1  # 산탄량
        self.accuracy = 10  # 총의 정확도, 정확이는 오차율 0이 가장 높은 스텟
        self.interrupted_fire = 5  # 몇점사, 쏘는 시간만큼 쉼
        self.magazine_gun = True  # 연사모드
        self.LEFT_DOWN = False  # 마우스 왼쪽버튼이 눌렸었는지 선입력 체크하기위한 변수
        self.LEFT_UP = True  # 마우스버튼이 눌렸다가 때졌는지 선입력 체크하기위한 변수 # 스무스한 점사 무빙을 위해 필요함

    def play_shoot_sound(self):
        i = random.randint(0, 3)
        if i == 0:
            Marine.shoot_sound00.play()
        elif i == 1:
            Marine.shoot_sound01.play()
        elif i == 2:
            Marine.shoot_sound02.play()
        elif i == 3:
            Marine.shoot_sound03.play()

    def play_hit_sound(self):
        Marine.hit_sound.play()

    def handle_events(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
                else:
                    self.LEFT_DOWN = True
                    self.LEFT_UP = False
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
                else:
                    self.LEFT_UP = True
                    self.LEFT_DOWN = False

        if event.type == SDL_KEYDOWN:

            if event.key == SDLK_a:
                self.left_move = True
            elif event.key == SDLK_d:
                self.right_move = True
            if event.key == SDLK_w:
                self.up_move = True
            elif event.key == SDLK_s:
                self.down_move = True
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
                if self.moving_attack == False:
                    self.moving_attack = True
                elif self.moving_attack == True:
                    self.moving_attack = False
            if event.key == SDLK_1:
                if self.magazine_gun == True:
                    self.magazine_gun = False
                    self.nfs //= 2
                    self.LEFT_DOWN = False
                    self.LEFT_UP = False
                    self.shoot_idle = True
                    self.shoot_idle_frame = 0
                    if self.nfs <= 0:
                        self.nfs = 1
            if event.key == SDLK_2:
                if self.magazine_gun == False:
                    self.magazine_gun = True
                    self.nfs *= 2
            if event.key == SDLK_SPACE:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False
                else:
                    self.LEFT_DOWN = True
                    self.LEFT_UP = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.left_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            elif event.key == SDLK_d:
                self.right_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            if event.key == SDLK_w:
                self.up_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            elif event.key == SDLK_s:
                self.down_move = False
                self.idle = True
                self.img_now = self.img_now[0], 2100
            if event.key == SDLK_SPACE:
                if self.magazine_gun == True:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
                else:
                    self.LEFT_UP = True
                    self.LEFT_DOWN = False

    def check_magazine(self):
        if self.magazine_gun == False:  # 점사모드일때
            if self.LEFT_UP == True:
                if self.shoot_frame // (self.nfs * self.interrupted_fire) % 2 != 0:
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.look_now, 1780
            if self.LEFT_DOWN == True:
                if self.shoot_frame == 0:
                    self.shoot_able = True
                    if self.moving_attack == False:
                        self.move_able = False

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

    def move(self):
        if self.move_able == True:
            if (self.left_move == True and self.right_move == False) or (
                    self.left_move == False and self.right_move == True):
                self.Wmove_able = True
            else:
                self.Wmove_able = False
            if (self.up_move == True and self.down_move == False) or (
                    self.up_move == False and self.down_move == True):
                self.Hmove_able = True
            else:
                self.Hmove_able = False
            if self.Wmove_able == True and self.Hmove_able == True:
                speed = 0.707
            else:
                speed = 1
            if self.Wmove_able == True:
                if self.left_move == True:
                    if self.stand_x - self.speed * speed <= round(self.stand_sx / 2):
                        self.x_move(round(self.stand_sx / 2) - self.stand_x)
                    else:
                        self.x_move(- self.speed * speed)
                        if not self.shoot_able:
                            self.img_now = 30 + 320 * 12, 1460 - (160 * self.move_frame)
                            self.idle = False
                else:  # self.right_move == True:
                    if self.stand_x + self.speed * speed >= play_state.window_size[0] - round(self.stand_sx / 2):
                        self.x_move(play_state.window_size[0] - (self.stand_x + round(self.stand_sx / 2)))
                    else:
                        self.x_move(self.speed * speed)
                        if not self.shoot_able:
                            self.img_now = 30 + 320 * 4, 1460 - (160 * self.move_frame)
                            self.idle = False
            if self.Hmove_able == True:
                if self.up_move == True:
                    if self.stand_y >= play_state.window_size[1] - round(self.stand_sy / 2):
                        self.y_move(play_state.window_size[1] - (self.stand_y + round(self.stand_sy / 2)))
                    else:
                        self.y_move(self.speed * speed)
                        if not self.shoot_able:
                            if self.Wmove_able == True:
                                if self.left_move == True:
                                    self.img_now = 30 + 320 * 14, 1460 - (160 * self.move_frame)
                                    self.idle = False
                                elif self.right_move == True:
                                    self.img_now = 30 + 320 * 2, 1460 - (160 * self.move_frame)
                                    self.idle = False
                            else:
                                self.img_now = 30, 1460 - (160 * self.move_frame)
                                self.idle = False
                else:
                    if self.stand_y <= round(self.stand_sy / 2):
                        self.y_move(round(self.stand_sy / 2) - self.stand_y)
                    else:
                        self.y_move(- self.speed * speed)
                        if not self.shoot_able:
                            if self.Wmove_able == True:
                                if self.left_move == True:
                                    self.img_now = 30 + 320 * 10, 1460 - (160 * self.move_frame)
                                    self.idle = False
                                elif self.right_move == True:
                                    self.img_now = 30 + 320 * 6, 1460 - (160 * self.move_frame)
                                    self.idle = False
                            else:
                                self.img_now = 30 + 320 * 8, 1460 - (160 * self.move_frame)
                                self.idle = False

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
                    x2, y2 = play_state.cursor.x + random.randint(-self.accuracy, self.accuracy), play_state.cursor.y + random.randint(
                        -self.accuracy, self.accuracy)
                    bullet = Bullet_32(self, x2, y2)
                    # if bullet.r == 0:
                    #     print(bullet.x1, bullet.x2)
                    #     del bullet
                    #     return
                    self.bullet_list.append(bullet)
                    self.shoot_idle = False
                    self.idle = False
                    self.img_now = 30 + (160 * self.look_now), 1620  # 격발 이미지
            elif self.shoot_frame % self.nfs == self.nfs // 2:
                self.img_now = 30 + (160 * self.look_now), 1780  # 견착 이미지
        else:
            self.shoot_idle = True

    def state_update(self):
        self.move()
        for mm in Marine.list:
            cheak_collision(self, mm)
        self.shoot()
        self.shoot_frame += 1  # 0~59
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