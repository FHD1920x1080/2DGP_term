from pico2d import *
import random

open_canvas()
dragoon = load_image('resource\\dragoon\\dragoon200.png')
running = True
x = 800 // 2
y = 600 // 2


def idle():
    frame = 0
    frame2 = 0
    for i in range(8):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 0, 1536 - 192 - 192 * frame, 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)
    pass
def l_move():
    frame = 0
    frame2 = 0
    for i in range(8):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 1, 1536 - 192 - 192 * frame, 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)
    pass
def r_move():
    frame = 0
    frame2 = 0
    for i in range(8):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 2, 1536 - 192 - 192 * frame, 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)
    pass
def u_move():
    frame = 0
    frame2 = 0
    for i in range(8):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 3, 1536 - 192 - 192 * frame, 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)
    pass
def d_move():
    frame = 0
    frame2 = 0
    for i in range(8):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 4, 1536 - 192 - 192 * frame, 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)
    pass
def attack_ready():
    frame = 0
    frame2 = 0
    for i in range(6):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 5, (1536 - 192) - (192 * frame), 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 6
        delay(0.05)
    pass
def attack():
    frame = 1
    frame2 = 0
    for i in range(3):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 5, (1536 - 192) - (192 * (5+frame)), 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 3
        delay(0.05)
    pass
def die():
    frame = 0
    frame2 = 0
    for i in range(8):
        handle_events()
        clear_canvas()
        dragoon.clip_draw(192 * 6, (1536 - 192) - (192 * frame), 192, 192, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.1)
    pass
def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                exit()

#idle()
# for i in range(8):
#     idle()
# for i in range(8):
#     l_move()
# for i in range(8):
#     r_move()
# for i in range(8):
#     u_move()
for j in range(4):
    for i in range(4):
         d_move()
    attack_ready()
    for i in range(4):
        attack()
        delay(0.6)
    for i in range(4):
         l_move()
    attack_ready()
    for i in range(4):
        attack()
        delay(0.6)
    for i in range(4):
         u_move()
    attack_ready()
    for i in range(4):
        attack()
        delay(0.6)
    for i in range(4):
         r_move()
    attack_ready()
    for i in range(4):
        attack()
        delay(0.6)
# for i in range(8):
#     die()
close_canvas()
