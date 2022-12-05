from obj_class.obj import *

from obj_class.bullet import Bullet32Gol, Missile

IDLE, MOVE = range(2)


class Goliath(GroundObj):
    unit_type = 1

    head_img = None
    leg_img = None
    portrait = None

    stand_sx = 28
    stand_sy = 28
    hit_sx = 30
    hit_sy = 38
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 15
    hit_y_gap = 15
    head_gap = 40
    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.
    shoot_sound1 = None
    shoot_sound2 = None

    def __init__(self):
        self.stand_x = play_state.window_size[0] / 2
        self.stand_y = 100
        self.hand = 0
        self.shoulder = 0
        self.shoot_point = [self.head_x(), self.head_y()]
        self.hp = 300  # 체력
        self.face_dir = 0  # 얼굴 방향
        self.leg_dir = 0  # 다리 방향
        self.rad = None  # 머리 각도
        self.max_hp = 250
        self.AD = 1
        self.AD2 = 5
        self.nfs = 12  # 몇프레임당 공격이 나갈건지
        self.n_shot = 3 # 산탄량
        self.nfs_m = 24  # 몇프레임당 공격이 나갈건지
        self.n_shot_m = 1  # 미사일 산탄량
        self.head_img = Goliath.head_img
        self.leg_img = Goliath.leg_img
        self.bullet_speed = 20
        self.head_img_now = [14, 1823]
        self.leg_img_now = [32, 1367]
        self.idle_frame = 0
        self.move_frame = 0
        self.shoot_frame = 0
        self.shoot_missile_frame = 0
        self.die_frame = 0
        self.speed = 3
        self.state = IDLE
        self.shoot_state = False
        self.shoot_missile_state = False
        self.max_save_missile = 5
        self.cur_save_missile = self.max_save_missile
        self.max_missile_charge_time = 50
        self.missile_charge_time = self.max_missile_charge_time
        self.accuracy = 0.125 #탄퍼짐 라디안값
        self.accuracy2 = self.accuracy * 2.0
        self.Wmove_able = False
        self.Hmove_able = False
        self.portrait_state = 0
        self.portrait_frame = 0
        self.cur_portrait_max_frame = 9

    def update(self):
        self.head_trace()
        if self.state == MOVE:
            self.move()
            if play_state.frame % 5 == 0:
                self.move_frame = (self.move_frame + 1) % 8
        else:
            self.leg_img_now[1] = 1367
        if self.shoot_state:
            self.shoot()
        else:
            self.head_img_now[1] = 1823 - 152 * self.move_frame
        if self.shoot_missile_state:
            self.shoot_missile()

    def head_x(self):
        return self.stand_x

    def head_y(self):
        return self.stand_y + self.head_gap

    def show(self):
        self.leg_img.clip_draw(self.leg_img_now[0], self.leg_img_now[1], 84, 152, self.print_x(), self.print_y())
        self.head_img.clip_draw(self.head_img_now[0], self.head_img_now[1], 120, 152, self.print_x(), self.print_y())
        # draw_rectangle(*self.get_stand_box())
        # draw_rectangle(*self.get_hit_box())

    def error_rate(self):
        return random.random() * self.accuracy2 - self.accuracy

    def portrait_anim(self):
        if play_state.frame % 10 == 0:
            self.portrait_frame += 1
            if self.portrait_frame > self.cur_portrait_max_frame:
                self.portrait_frame = 0
                self.rand_portrait()

    portrait_max_frame = {0: 9,
                          1: 9,
                          2: 9,
                          3: 19}

    def rand_portrait(self):
        self.portrait_state = random.randint(0, 3)
        self.cur_portrait_max_frame = self.portrait_max_frame[self.portrait_state]
        pass

    def show_passive(self):
        UI.font22.draw(550, 90, '움직이면서 공격 가능', (255, 255, 255))

    def show_main_ui(self):
        UI.skill_icon.clip_draw_to_origin(88 * 7 - 1, 88 * 1 + 1, 82, 82, 450, 50)
        UI.font22.draw(450, 30, 'PASSIVE', (255, 255, 255))

        UI.skill_icon.clip_draw_to_origin(88 * 4, 88 * 3 + 5, 84, 84, play_state.window_size[0] - 300, 50)
        UI.font22.draw(play_state.window_size[0] - 300, 30, 'RIGHT', (255, 255, 255))
        UI.font22.draw(play_state.window_size[0] - 210, 90, f'{self.cur_save_missile}/{self.max_save_missile}', (255, 255, 255))

        UI.skill_icon.clip_draw_to_origin(88 * 1 + 1, 88 * 6 + 9, 84, 84, play_state.window_size[0] - 160, 50)
        #UI.font22.draw(play_state.window_size[0] - 300, 30, 'LEFT', (255, 255, 255))
        UI.infinite.draw_to_origin(play_state.window_size[0] - 70, 75, 50, 30)


    @staticmethod
    def play_shoot_sound():
        pass


    def handle_events(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                User_input.left_button = True
                self.shoot_state = True
                self.shoot_frame = 0
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = True
                self.shoot_missile_state = True
                self.shoot_missile_frame = 0
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                User_input.left_button = False
                self.shoot_state = False
                self.shoot_frame = 0
                if self.state == MOVE:
                    self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * self.move_frame]
                else:
                    self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * 3]
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = False
                self.shoot_missile_state = False
                self.shoot_missile_frame = 0
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                User_input.left_key = True
                self.state = MOVE
            elif event.key == SDLK_d:
                User_input.right_key = True
                self.state = MOVE
            elif event.key == SDLK_w:
                User_input.up_key = True
                self.state = MOVE
            elif event.key == SDLK_s:
                User_input.down_key = True
                self.state = MOVE
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                User_input.left_key = False
                if self.state == IDLE:
                    self.state = MOVE
            elif event.key == SDLK_d:
                User_input.right_key = False
                if self.state == IDLE:
                    self.state = MOVE
            elif event.key == SDLK_w:
                User_input.up_key = False
                if self.state == IDLE:
                    self.state = MOVE
            elif event.key == SDLK_s:
                User_input.down_key = False
                if self.state == IDLE:
                    self.state = MOVE

    def move(self):
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
            self.state = IDLE
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
                self.leg_dir = 2
            elif down:  # 오른쪽 아래 대각선
                self.x_move(speed)
                self.y_move(-speed)
                self.leg_dir = 6
            else:  # 그냥 오른쪽
                self.x_move(speed)
                self.leg_dir = 4
            self.leg_img_now = [32 + 152 * self.leg_dir, 1367 - 152 * self.move_frame]
            return
        if left:
            if up:  # 왼쪽 위 대각선
                self.x_move(-speed)
                self.y_move(speed)
                self.leg_dir = 14
            elif down:  # 왼쪽 아래 대각선
                self.x_move(-speed)
                self.y_move(-speed)
                self.leg_dir = 10
            else:  # 그냥 왼쪽
                self.x_move(-speed)
                self.leg_dir = 12
            self.leg_img_now = [32 + 152 * self.leg_dir, 1367 - 152 * self.move_frame]
            return
        if up:  # 그냥 위
            self.y_move(speed)
            self.leg_dir = 0
            self.leg_img_now = [32 + 152 * self.leg_dir, 1367 - 152 * self.move_frame]
            return
        if down:  # 그냥 아래
            self.y_move(-speed)
            self.leg_dir = 8
            self.leg_img_now = [32 + 152 * self.leg_dir, 1367 - 152 * self.move_frame]
            return
        print('can not move')

    def head_trace(self):
        self.rad = get_rad(self.head_x(), self.head_y(), play_state.cursor.x, play_state.cursor.y)
        self.face_dir = self.get_face_dir(self.rad)
        self.head_img_now[0] = 14 + 152 * self.face_dir

    left_hand = {0: [-20, 10],
                 2: [-16, 12],
                 4: [-8, 12],
                 6: [12, 20],
                 8: [15, 18],
                 10: [23, 15],
                 12: [37, 6],
                 14: [34, 0],
                 16: [27, -10],
                 17: [28, -20],
                 18: [12, -32],
                 20: [0, -30],
                 22: [-16, -24],
                 24: [-18, -20],
                 26: [-18, -16],
                 28: [-24, -10],
                 30: [-30, 0],
                 32: [-24, 10]}

    right_hand = {0: [28, 10],
                  2: [30, 0],
                  4: [24, -20],
                  6: [28, -14],
                  8: [18, -20],
                  10: [16, -24],
                  12: [4, -30],
                  14: [-12, -28],
                  16: [-25, -20],
                  17: [-23, -10],
                  18: [-30, 0],
                  20: [-33, 6],
                  22: [-23, 15],
                  24: [-15, 18],
                  26: [-13, 22],
                  28: [6, 22],
                  30: [16, 12],
                  32: [25, 10]}

    def shoot(self):
        if self.shoot_frame % self.nfs == 0:  # 몇프레임마다 쏠건지 1이 가장 빠름
            play_state.sound.Marine_shoot = True
            if self.hand == 0:
                self.shoot_point = self.right_hand[self.face_dir].copy()
                self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * 11]
                self.hand = 1
            else:
                self.shoot_point = self.left_hand[self.face_dir].copy()
                self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * 12]
                self.hand = 0
            self.shoot_point[0] += self.head_x()
            self.shoot_point[1] += self.head_y()
            for i in range(self.n_shot):
                Bullet32Gol(self)  # x1==x2 and y1==y2 일 때 False 반환
            #self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * 10]
        elif self.shoot_frame % self.nfs == self.nfs // 2:
            if self.state == MOVE:
                self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * self.move_frame]
            else:
                self.head_img_now = [14 + 152 * self.face_dir, 1823 - 152 * 3]
        self.shoot_frame += 1

    def shoot_missile(self):
        if self.shoot_missile_frame % self.nfs_m == 0:  # 몇프레임마다 쏠건지 1이 가장 빠름
            if self.cur_save_missile > 0:
                self.cur_save_missile -= 1
                Goliath.shoot_sound2.play()
                for i in range(self.n_shot_m):
                    Missile(self)  # x1==x2 and y1==y2 일 때 False 반환
                    self.shoulder = (self.shoulder + 1) % 2  # 오른손 왼손 변경
        self.shoot_missile_frame += 1

    @staticmethod
    def get_face_dir(rad):
        if rad >= 0:  # 1, 2 사분면
            if rad < 1.5708:
                if rad < 0.1963:  # 우측
                    return 8
                elif rad < 0.589:
                    return 6
                elif rad < 0.8517:
                    return 4
                elif rad < 1.2645:
                    return 2
                else:  # 1.2645 <  rad < 1.5708:
                    return 0
            else:
                if rad < 1.8771:
                    return 32
                elif rad < 2.0898:
                    return 30
                elif rad < 2.7525:
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
                else:  # rad > -1.5708:
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

    def die(self):
        pass

    @staticmethod
    def load_resource():
        Goliath.head_img = load_image('resource\\goliath\\goliath_head200x2v2_eva.png')
        Goliath.leg_img = load_image('resource\\goliath\\goliath_leg200x2_eva.png')
        Goliath.portrait = load_image('resource\\goliath\\goliath_portrait.png')
        # Goliath.portrait = load_image('resource\\goliath\\goliath_portrait.png')
        #Goliath.shoot_sound1 = load_wav('resource\\goliath\\sound\\dragbull.wav')
        # Sound.list.append(Goliath.shoot_sound1)
        # Sound.volume_list.append(10)
        Goliath.shoot_sound2 = load_wav('resource\\goliath\\pinlau001.wav')
        Sound.list.append(Goliath.shoot_sound2)
        Sound.volume_list.append(10)
