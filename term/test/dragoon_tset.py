from pico2d import *
import random

w = 1200
h = 900
open_canvas(w, h, sync=True)
running = True
x = w // 2
y = h // 2


class Dragoon:
    img = None
    def __init__(self):
        self.img = Dragoon.img
        self.state = "IDLE"
        self.attack_ready_framet_frame = None
        self.x = w // 2
        self.y = h // 2
        self.sx = 192
        self.sy = 192
        self.img_now = [0, 0]
        self.idle_frame = 0
        self.move_frame = 0
        self.open_frame = 0
        self.attack_frame = 0
        self.die_frame = 0
        self.dir = range(4)  # 0 1 2 3

    def idle(self):
        self.img_now = [0, 1536 - 192 - 192 * self.idle_frame]
        self.idle_frame = (self.idle_frame + 1) % 8

    def l_move(self):
        self.x -= 10
        self.img_now = [192 * 1, 1536 - 192 - 192 * self.move_frame]

    def r_move(self):
        self.x += 10
        self.img_now = [192 * 2, 1536 - 192 - 192 * self.move_frame]

    def u_move(self):
        self.y += 10
        self.img_now = [192 * 3, 1536 - 192 - 192 * self.move_frame]

    def d_move(self):
        self.y -= 10
        self.img_now = [192 * 4, 1536 - 192 - 192 * self.move_frame]

    def move(self):
        if self.dir == 0:
            self.l_move()
        elif self.dir == 1:
            self.r_move()
        elif self.dir == 2:
            self.u_move()
        elif self.dir == 3:
            self.d_move()
        self.move_frame = (self.move_frame + 1) % 8

    def open(self):
        self.img_now = [192 * 5, (1536 - 192) - (192 * self.open_frame)]
        self.open_frame = (self.open_frame + 1) % 6

    def attack_ready(self):
        self.img_now = [192 * 5, (1536 - 192) - (192 * 5)]

    def attack(self):
        self.img_now = [192 * 5, (1536 - 192) - (192 * (5 + self.attack_frame))]
        self.attack_frame = (self.attack_frame + 1) % 3

    def die(self):
        self.img_now = [192 * 6, (1536 - 192) - (192 * self.die_frame)]
        self.die_frame = (self.die_frame + 1) % 7

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)
    @staticmethod
    def load_resource():
        Dragoon.img = load_image('../resource\\dragoon\\dragoon200.png')


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                exit()
            elif event.key == SDLK_a:
                dragoon.state = "MOVE"
                dragoon.dir = 0
            elif event.key == SDLK_d:
                dragoon.state = "MOVE"
                dragoon.dir = 1
            elif event.key == SDLK_w:
                dragoon.state = "MOVE"
                dragoon.dir = 2
            elif event.key == SDLK_s:
                dragoon.state = "MOVE"
                dragoon.dir = 3
            elif event.key == SDLK_1:
                dragoon.state = "IDLE"
            elif event.key == SDLK_2:
                dragoon.state = "OPEN"
            elif event.key == SDLK_3:
                dragoon.state = "ATT"
            elif event.key == SDLK_4:
                dragoon.state = "DIE"
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                dragoon.state = "IDLE"
                dragoon.move_frame = 0
            elif event.key == SDLK_d:
                dragoon.state = "IDLE"
                dragoon.move_frame = 0
            elif event.key == SDLK_w:
                dragoon.state = "IDLE"
                dragoon.move_frame = 0
            elif event.key == SDLK_s:
                dragoon.state = "IDLE"
                dragoon.move_frame = 0


frame = 0

FPS = 100
Dragoon.load_resource()
dragoon = Dragoon()

while running:
    handle_events()
    if dragoon.state == "IDLE":
        if frame % 5 == 0:
            dragoon.idle()
    elif dragoon.state == "MOVE":
        if frame % 4 == 0:
            dragoon.move()
    elif dragoon.state == "OPEN":
        if frame % 4 == 0:
            dragoon.open()
            if dragoon.open_frame == 0:
                dragoon.state = "ATT_R"
    elif dragoon.state == "ATT_R":
        dragoon.attack_ready()
    elif dragoon.state == "ATT":
        if frame % 5 == 0:
            dragoon.attack()
            if dragoon.attack_frame == 0:
                dragoon.state = "ATT_R"
    elif dragoon.state == "DIE":
        if frame % 5 == 0:
            dragoon.die()

    clear_canvas()
    dragoon.show()
    update_canvas()
    frame = (frame + 1) % FPS  # 0~99



def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                exit()


close_canvas()
