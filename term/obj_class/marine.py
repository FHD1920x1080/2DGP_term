import play_state
from obj_class.obj import *

from obj_class.bullet import Bullet32, DragBullMarine

IDLE, MOVE, DASH, SHOOT, WAIT = range(5)
#첫째 아들이지만 전혀 객체 지향적이지 않은 막코드, 특히 상태 관련

class Marine(GroundObj):
    unit_type = 0  # 마린인걸 인식하는데 씀, 골리앗은 1, 드라군은 2

    img = None
    portrait = None
    print_sx = 110
    print_sy = 85
    stand_sx = 18
    stand_sy = 18
    hit_sx = 24  # 히트박스 크기, 반쪽
    hit_sy = 30
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 20
    hit_y_gap = 20

    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.

    shoot_sound = None
    shoot_sound2 = None


    def __init__(self):
        self.kill = 0
        self.stand_x = play_state.window_size[0] / 2  # 마린이 서있는 좌표
        self.stand_y = 100
        self.face_dir = 0  # 얼굴 방향
        self.hp = 200  # 체력
        self.max_hp = 200
        self.AD = 6  # 공격력
        self.img = Marine.img
        self.img_now = [30, 2180 - 80 - 320]  # 스프라이트 좌표
        self.speed = 2.5  # 이동속도w
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
        self.bullet_speed = 30  # 탄속
        self.moving_attack = False  # 1이면 움직이면서 공격 가능 g키
        self.nfs = 8  # 몇프레임당 공격이 나갈건지
        self.n_shot = 1  # 산탄량
        self.accuracy = 10  # 총의 정확도, 정확이는 오차율 0이 가장 높은 스텟
        self.interrupted_fire = 5  # 몇점사, 쏘는 시간만큼 쉼
        self.magazine_gun = False  # 연사모드
        self.rad = None
        self.cos = None
        self.sin = None
        self.drag_bull_size = 1.0
        self.drag_bull_cool_time = 300
        self.cur_drag_bull_cool_time = 0
        self.dash_state = False
        self.dash_cool_time = 100  #
        self.cur_dash_cool_time = 0
        self.dash_frame = 0
        self.dash_dir = 0  # 16방향
        self.dash_speed = 17
        self.cur_dash_speed = 0  # self.dash_speed
        self.dash_accel = -0.73  # 같이 -0.9 / self.r로 초기화 해줌
        self.portrait_state = 0
        self.portrait_frame = 0
        self.cur_portrait_max_frame = 18


    def portrait_anim(self):
        if play_state.frame % 10 == 0:
            self.portrait_frame += 1
            if self.portrait_frame > self.cur_portrait_max_frame:
                self.portrait_frame = 0
                self.rand_portrait()

    portrait_max_frame = {0: 18,
                          1: 9,
                          2: 15,
                          3: 29}

    def rand_portrait(self):
        self.portrait_state = random.randint(0, 3)
        self.cur_portrait_max_frame = self.portrait_max_frame[self.portrait_state]

    def show_passive(self):
        UI.font16.draw(550, 115, 'TAB키를 이용해 발사모드를 변경할 수 있다.', (255, 255, 255))
        UI.font16.draw(550, 90, '점사모드는의 연사력이 두배 빠르다.', (255, 255, 255))
        UI.font16.draw(550, 65, '마린의 공격은 지상과 공중 구분이 없다.', (255, 255, 255))
        UI.font16.draw(550, 40, 'SPACE: 쿨타임이 1초인 대쉬', (255, 255, 255))
    def show_right(self):
        UI.font16.draw(play_state.window_size[0] - 340, 175, '충돌 시 폭발 하는 로켓', (255, 255, 255))
        UI.font16.draw(play_state.window_size[0] - 300, 150, f'피해량:{self.AD*2}', (255, 255, 255))
    def show_left(self):
        UI.font16.draw(play_state.window_size[0] - 195, 200, '가까이 조준 할수록', (255, 255, 255))
        UI.font16.draw(play_state.window_size[0] - 185, 175, '집탄률이 떨어짐', (255, 255, 255))
        UI.font16.draw(play_state.window_size[0] - 155, 150, f'피해량:{self.AD}', (255, 255, 255))

    def show_main_ui(self):
        UI.skill_icon.clip_draw_to_origin(1, 88 * 13 + 15, 84, 84, 450, 48)
        UI.font22.draw(462, 30, 'SPACE', (255, 255, 255))
        if self.cur_dash_cool_time > 0:
            UI.black_50.draw_to_origin(450, 48, 84, 84)
            UI.black_50.draw_to_origin(450, 48, 84, self.cur_dash_cool_time / self.dash_cool_time * 84)
            UI.font22.draw(475, 90, f'0.{self.cur_dash_cool_time // 10}', (255, 255, 255))


        UI.skill_icon.clip_draw_to_origin(1, 2, 84, 84, play_state.window_size[0] - 300, 50)
        UI.font22.draw(play_state.window_size[0] - 288, 30, 'RIGHT', (255, 255, 255))
        if self.cur_drag_bull_cool_time > 0:
            UI.black_50.draw_to_origin(play_state.window_size[0] - 300, 48, 84, 84)
            UI.black_50.draw_to_origin(play_state.window_size[0] - 300, 48, 84, self.cur_drag_bull_cool_time / self.drag_bull_cool_time * 84)
            UI.font22.draw(play_state.window_size[0] - 275, 90, f'{(self.cur_drag_bull_cool_time*0.01):1.1f}', (255, 255, 255))


        UI.skill_icon.clip_draw_to_origin(88 * 7 - 2, 88 * 8 + 11, 84, 84, play_state.window_size[0] - 160, 50)
        #UI.font22.draw(play_state.window_size[0] - 300, 30, 'LEFT', (255, 255, 255))
        UI.infinite.draw_to_origin(play_state.window_size[0] - 70, 75, 50, 30)

    def show_sub_ui(self):
        pass

    def suffer(self, damage, attack_type=0, owner=None):  # 피격당하면 해줄것
        self.hp -= damage
        if self.hp <= 0:
            pass

    def add_kill(self):
        self.kill += 1

    @staticmethod
    def play_shoot_sound():
        Marine.shoot_sound.play()
        # i = random.randint(0, 3)
        # if i == 0:
        #     Marine.shoot_sound00.play()
        # elif i == 1:
        #     Marine.shoot_sound01.play()
        # elif i == 2:
        #     Marine.shoot_sound02.play()
        # elif i == 3:
        #     Marine.shoot_sound03.play()
    @staticmethod
    def play_shoot2_sound():
        Marine.shoot_sound2.play()

    def update(self):
        self.check_magazine()
        if self.dash_state:
            self.dash()
        else:
            self.move()
            self.shoot()
            self.shoot_drag_bull()
            self.shoot_frame += 1
        if not self.magazine_gun:
            if self.shoot_idle:
                self.shoot_idle_frame += 1
                if self.shoot_idle_frame > self.nfs * self.interrupted_fire - 1:
                    self.shoot_frame = 0
            else:
                self.shoot_idle_frame = 0
        if self.idle:
            self.idle_frame += 1
        else:
            self.idle_frame = 0
        if self.dash_state:
            if play_state.frame % 2 == 0:
                self.move_frame = (self.move_frame + 1) % 8
        else:
            if play_state.frame % 4 == 0:
                self.move_frame = (self.move_frame + 1) % 8

    def handle_events(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun:
                    self.shoot_able = True
                    self.shoot_frame = 0
                    if not self.moving_attack:
                        self.move_able = False
                else:
                    User_input.left_button = True
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                if self.magazine_gun:
                    self.shoot_frame = 0
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.face_dir, 1780
                else:
                    User_input.left_button = False
            if event.button == SDL_BUTTON_RIGHT:
                self.img_now = 30 + (160 * self.face_dir), 1780  # 견착 이미지
                User_input.right_button = False
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
            elif event.key == SDLK_p:
                self.AD += 1
            elif event.key == SDLK_o:
                self.AD = max(self.AD - 1, 0)
            elif event.key == SDLK_l:
                if self.magazine_gun:
                    self.nfs -= 2
                    self.nfs = max(self.nfs - 2, 2)
                else:
                    self.nfs -= 1
                    self.nfs = max(self.nfs - 1, 1)
            elif event.key == SDLK_k:
                if self.magazine_gun:
                    self.nfs += 2
                    self.nfs = min(self.nfs + 2, 40)
                else:
                    self.nfs += 1
                    self.nfs = min(self.nfs + 1, 20)
            elif event.key == SDLK_m:
                self.n_shot = min(self.n_shot + 1, 5)
            elif event.key == SDLK_n:
                self.n_shot = max(self.n_shot - 1, 1)
            elif event.key == SDLK_g:
                if self.moving_attack:
                    self.moving_attack = False
                else:
                    self.moving_attack = True
            elif event.key == SDLK_TAB:
                if self.magazine_gun:
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
        self.x_move(self.cos * self.cur_dash_speed)
        self.y_move(self.sin * self.cur_dash_speed)
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
        if self.dash_frame > 25:  # 0 ~ 24
            self.dash_state = False
            self.dash_frame = 0
            self.shoot_frame = 0
            if not self.magazine_gun:
                self.shoot_able = False
                self.move_able = True
        pass

    def try_dash(self):
        if self.cur_dash_cool_time > 0:
            print('cooltime')
            return
        self.cur_dash_cool_time = 1
        if self.idle:  # 가만히 있을 때 대쉬
            self.rad = get_rad(self.stand_x, self.stand_y, play_state.cursor.x, play_state.cursor.y)
            self.dash_dir = self.get_face_dir(self.rad)
            self.dash_set()
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

            if self.Wmove_able == False and self.Hmove_able == False:  # 가만히서 총만 쏘고 있는 상황
                self.dash_dir = self.face_dir
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
                return

    def dash_set(self):
        self.cos = math.cos(self.rad)
        self.sin = math.sin(self.rad)
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
            if self.Wmove_able:
                if User_input.right_key:
                    if self.get_stand_right() + speed > play_state.window_size[0]:
                        self.x_move(play_state.window_size[0] - self.get_stand_right())
                    else:
                        right = True
                else:
                    if self.get_stand_left() - speed < 0:
                        self.x_move(-self.get_stand_left())
                    else:
                        left = True
            if self.Hmove_able:
                if User_input.up_key:
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
        if not self.magazine_gun:  # 점사모드일때
            if User_input.left_button:
                if self.shoot_frame == 0:
                    self.shoot_able = True
                    if not self.moving_attack:
                        self.move_able = False
            else:
                if self.shoot_frame // (self.nfs * self.interrupted_fire) % 2 != 0:
                    self.shoot_able = False
                    self.idle = True
                    self.move_able = True
                    self.img_now = 30 + 160 * self.face_dir, 1780

    @staticmethod
    def get_face_dir(rad):
        if rad >= 0:  # 1, 2 사분면
            if rad < 1.8:
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
                else: # rad < 1.8:
                    return 0
            else:
                if rad < 2.0898:
                    return 30
                elif rad < 2.5525:
                    return 28
                elif rad < 2.9452:
                    return 26
                else:  # rad <= 3.1415:
                    return 24
        else:  # 3,4분면
            if rad > -1.5708:
                if rad > -0.0663:  # 우측
                    return 8
                elif rad > -0.31:
                    return 10
                elif rad > -0.7017:
                    return 12
                elif rad > -1.2044:
                    return 14
                else: # rad > -1.5708:
                    return 16
            else:
                if rad > -1.9371:
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
        if self.shoot_able:
            if not self.magazine_gun:
                if (self.shoot_frame) // (self.nfs * self.interrupted_fire) % 2 != 0:  # 점사 구현
                    return
            if self.shoot_frame % self.nfs == 0:  # self.nfs은 마린이 몇프레임마다 쏠건지 1이 가장 빠름
                # 여기에 사운드
                # self.play_shoot_sound()
                play_state.sound.Marine_shoot = True
                a = get_rad(self.stand_x, self.stand_y, play_state.cursor.x, play_state.cursor.y)
                self.face_dir = self.get_face_dir(a)  # 각도를 가지고 마린이 바라볼 방향 정함.
                for i in range(self.n_shot):
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

    def shoot_drag_bull(self):
        if User_input.right_button:
            if self.cur_drag_bull_cool_time == 0:
                a = get_rad(self.stand_x, self.stand_y, play_state.cursor.x, play_state.cursor.y)
                self.face_dir = self.get_face_dir(a)  # 각도를 가지고 마린이 바라볼 방향 정함.
                self.shoot_idle = False
                self.idle = False
                DragBullMarine(self)
                play_state.sound.Marine_shoot2 = True
                self.cur_drag_bull_cool_time = self.drag_bull_cool_time
        if self.cur_drag_bull_cool_time > self.drag_bull_cool_time - 5:
            self.img_now = 30 + (160 * self.face_dir), 1620  # 격발 이미지

    @staticmethod
    def load_resource():
        Marine.img = load_image('resource\\marine\\marine250x2_blue_blue.png')
        Marine.portrait = load_image('resource\\marine\\marine_portrait.png')
        Marine.shoot_sound = load_wav('resource\\marine\\shoot_sound\\laserhit.wav')
        Marine.shoot_sound2 = load_wav('resource\\marine\\shoot_sound\\lasrhit3v2.wav')
        Sound.list.append(Marine.shoot_sound)
        Sound.volume_list.append(16)
        Sound.list.append(Marine.shoot_sound2)
        Sound.volume_list.append(16)