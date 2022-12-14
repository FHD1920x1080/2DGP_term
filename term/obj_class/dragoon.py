from obj_class.obj import *

from obj_class.bullet import DragBull

IDLE, MOVE, OPEN, READY, SHOOT, WAIT = range(6)


class Dragoon(GroundObj):
    unit_type = 2

    img = None
    portrait = None
    print_sx = 192
    print_sy = 192
    stand_sx = 34
    stand_sy = 34
    hit_sx = 31
    hit_sy = 40
    print_x_gap = 0
    hit_x_gap = 0
    print_y_gap = 23
    hit_y_gap = 18
    exist = True  # 존재 변수 삭제 할지 판정
    collision = True  # 충돌체크 함.
    shoot_sound = None

    def __init__(self):
        self.kill = 0
        self.stand_x = play_state.window_size[0] / 2
        self.stand_y = 100
        self.hp = 300  # 체력
        self.max_hp = 300
        self.AD = 12
        self.img = Dragoon.img
        self.state = IDLE
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
                          1: 10,
                          2: 14,
                          3: 9,
                          4: 19}

    def rand_portrait(self):
        self.portrait_state = random.randint(0, 4)
        self.cur_portrait_max_frame = self.portrait_max_frame[self.portrait_state]
        pass


    def show_passive(self):
        UI.font16.draw(550, 115, '폭발형 저글링과 뮤탈에게', (255, 255, 255))
        UI.font16.draw(550, 90, '절반의 피해만 입는다.', (255, 255, 255))
        UI.font16.draw(550, 65, '드라군의 공격은 공중 유닛에게 절반의 피해만 준다.', (255, 255, 255))
    def show_right(self):
        UI.font16.draw(play_state.window_size[0] - 280, 150, '미구현', (255, 255, 255))
    def show_left(self):
        UI.font16.draw(play_state.window_size[0] - 200, 200, '가속을 받아 날아가며,', (255, 255, 255))
        UI.font16.draw(play_state.window_size[0] - 200, 175, '지정한 위치에서 폭발', (255, 255, 255))
        UI.font16.draw(play_state.window_size[0] - 160, 150, f'피해량:{self.AD}', (255, 255, 255))
    def show_main_ui(self):
        UI.skill_icon.clip_draw_to_origin(88 * 4, 88 * 11 + 13, 84, 84, 450, 50)
        UI.font22.draw(450, 30, 'PASSIVE', (255, 255, 255))

        UI.skill_icon.clip_draw_to_origin(1, 88 * 14 + 17, 84, 84, play_state.window_size[0] - 300, 50)
        UI.font22.draw(play_state.window_size[0] - 288, 30, 'RIGHT', (255, 255, 255))


        UI.skill_icon.clip_draw_to_origin(88 * 7 - 2, 88 * 12 + 13, 84, 84, play_state.window_size[0] - 160, 48)
        #UI.font22.draw(play_state.window_size[0] - 300, 30, 'LEFT', (255, 255, 255))
        UI.infinite.draw_to_origin(play_state.window_size[0] - 70, 75, 50, 30)

    def show_sub_ui(self):
        pass

    def suffer(self, damage, attack_type=0, owner=None):  # 피격당하면 해줄것
        if attack_type == 1: # 폭발형은 절반
            self.hp -= damage / 2
        else:
            self.hp -= damage
        if self.hp <= 0:
            pass

    def add_kill(self):
        self.kill += 1

    @staticmethod
    def play_shoot_sound():
        Dragoon.shoot_sound.play()

    def update(self):
        if self.state == MOVE:
            self.move()
            if play_state.frame % 4 == 0:
                self.move_frame = (self.move_frame + 1) % 8
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
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                User_input.left_button = False
                pass
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = False
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
            elif event.key == SDLK_p:
                self.AD += 1
            elif event.key == SDLK_o:
                self.AD = max(self.AD - 1, 0)
            elif event.key == SDLK_l:
                self.bull_size += 0.1
            elif event.key == SDLK_k:
                self.bull_size -= 0.1
                if self.bull_size < 0.1:
                    self.bull_size = 0.1
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
            self.img_now = [0, 1344]
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
            self.img_now = [960, 384 - (192 * (self.shoot_frame // 6))]
        self.shoot_frame += 1
        if self.shoot_frame > 17:
            DragBull(self)
            self.wait_frame = 0
            self.state = WAIT

    def die(self):
        self.img_now = [192 * 6, (1536 - 192) - (192 * self.die_frame)]
        self.die_frame = (self.die_frame + 1) % 7

    @staticmethod
    def load_resource():
        Dragoon.img = load_image('resource\\dragoon\\dragoon200_green.png')
        Dragoon.portrait = load_image('resource\\dragoon\\dragoon_portrait.png')
        Dragoon.shoot_sound = load_wav('resource\\dragoon\\sound\\dragbull.wav')
        Sound.list.append(Dragoon.shoot_sound)
        Sound.volume_list.append(10)
