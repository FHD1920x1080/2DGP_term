import game_world
from obj_class.obj import *
import random

IDLE, MOVE, OPEN, READY, SHOOT, WAIT = range(6)


class Dragoon(RealObj):
    img = None
    shoot_sound1 = None
    shoot_sound2 = None
    unit_type = 2

    x_gap = 0
    hit_x_gap = 0
    y_gap = 23
    hit_y_gap = 23

    def __init__(self):
        self.hp = 100  # 체력
        self.AD = 8
        self.img = Dragoon.img
        self.state = IDLE
        self.attack_ready_framet_frame = None
        self.stand_x = play_state.window_size[0] / 2  # 마린이 서있는 좌표
        self.stand_y = play_state.window_size[1] / 2
        self.x = self.stand_x
        self.y = self.stand_y + 23
        self.sx = 192
        self.sy = 192
        self.hit_x = self.x
        self.hit_y = self.y
        self.hit_sx = 31
        self.hit_sy = 44
        self.stand_sx = 34
        self.stand_sy = 34
        self.img_now = [0, 1344]
        self.bullet_speed = 25
        self.idle_frame = 0
        self.move_frame = 0
        self.open_frame = 0
        self.wait_frame = 0
        self.shoot_frame = 0
        self.die_frame = 0
        self.speed = 3.5
        self.state = IDLE
        self.Wmove_able = False
        self.Hmove_able = False
        self.bull_x2, self.bull_y2 = None, None
        self.bull_size = 2
    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)
    def play_shoot_sound(self):
        i = random.randint(0, 1)
        if i==0:
            Dragoon.shoot_sound1.play()
        else:
            Dragoon.shoot_sound2.play()
    def update(self):
        if self.state == MOVE:
            self.move()
        elif self.state == IDLE:
            self.idle()
        elif self.state == OPEN:
            self.open()
        elif self.state == READY:
            self.ready()
        elif self.state == WAIT:
            self.wait()

        elif self.state == SHOOT:
            self.shoot()
        # else:
        #     if len(game_world.explosive_bullet_list) > 0:
        #         if self.shoot_success == False:
        #             del game_world.explosive_bullet_list[0]
    def handle_events(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if self.state == IDLE or self.state == MOVE:
                    self.bull_x2, self.bull_y2 = play_state.cursor.x, play_state.cursor.y
                    self.open_frame = 0
                    self.state = OPEN
                User_input.left_button = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                User_input.left_button = False
                pass
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
        if play_state.frame % 4 == 0:
            self.move_frame = (self.move_frame + 1) % 8
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
            self.img_now = [0, 1344]
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
            elif down:  # 오른쪽 아래 대각선
                self.x_move(speed)
                self.y_move(-speed)
            else:  # 그냥 오른쪽
                self.x_move(speed)
            self.img_now = [384, 1344 - 192 * self.move_frame]
            return
        if left:
            if up:  # 왼쪽 위 대각선
                self.x_move(-speed)
                self.y_move(speed)
            elif down:  # 왼쪽 아래 대각선
                self.x_move(-speed)
                self.y_move(-speed)
            else:  # 그냥 왼쪽
                self.x_move(-speed)
            self.img_now = [192, 1344 - 192 * self.move_frame]
            return
        if up:  # 그냥 위
            self.y_move(speed)
            self.img_now = [576, 1344 - 192 * self.move_frame]
            return
        if down:  # 그냥 아래
            self.y_move(-speed)
            self.img_now = [768, 1344 - 192 * self.move_frame]
            return
        print('can not move')
        self.state = IDLE

    def idle(self):
        self.img_now = [0, 1344 - 192 * self.idle_frame]
        if play_state.frame % 6 == 0:
            self.idle_frame = (self.idle_frame + 1) % 8

    def open(self):
        self.img_now = [960, 1344 - (192 * self.open_frame)]
        if play_state.frame % 3 == 0:
            self.open_frame += 1
            if self.open_frame > 5:
                self.shoot_frame = 0
                self.state = SHOOT

    def ready(self):
        self.img_now = [960, 384]
        if User_input.left_button:
            self.bull_x2, self.bull_y2 = play_state.cursor.x, play_state.cursor.y
            self.shoot_frame = 0
            self.state = SHOOT

    def wait(self):
        self.img_now = [960, 384]
        self.wait_frame += 1
        if self.wait_frame >= 55:
            self.state = READY

    def shoot(self):
        if self.shoot_frame % 6 == 0:
            self.img_now = [960, 384 - (192 * (self.shoot_frame//6))]
        self.shoot_frame += 1
        if self.shoot_frame > 17:
            bull = Drag_Bull(self)
            game_world.explosive_bullet_list.append(bull)
            self.play_shoot_sound()
            self.wait_frame = 0
            self.state = WAIT

    def die(self):
        self.img_now = [192 * 6, (1536 - 192) - (192 * self.die_frame)]
        self.die_frame = (self.die_frame + 1) % 7

    @staticmethod
    def load_resource():
        Dragoon.img = load_image('resource\\dragoon\\dragoon200.png')
        Dragoon.shoot_sound1 = load_wav('resource\\dragoon\\sound\\dragbull.wav')
        Dragoon.shoot_sound2 = load_wav('resource\\dragoon\\sound\\tphfi201.wav')
        Dragoon.shoot_sound1.set_volume(10)
        Dragoon.shoot_sound2.set_volume(10)
