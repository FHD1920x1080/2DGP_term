from pico2d import *
import random

open_canvas()
head = load_image('../resource\\goliath\\goliath_head200x2.png')
leg = load_image('../resource\\goliath\\goliath_leg200x2.png')
running = True
x = 800 // 2
y = 600 // 2
shoot_state = False
frame = 0
frame2 = 0
look = 4
leg_look = 4
def leg_draw():
    leg.clip_draw(32 + 152 * leg_look, 1519 - 152 - 152 * frame, 84, 152, x, y)
    pass

def head_draw():
    if shoot_state:
        head.clip_draw(14 + 152 * look, 1671 - 152 - 152 * 10, 120, 152, x, y)
        update_canvas()
        delay(0.025)
        clear_canvas()
        leg_draw()
        head.clip_draw(14 + 152 * look, 1671 - 152 - 152 * frame, 120, 152, x, y)
    else:
        head.clip_draw(14 + 152 * look, 1671 - 152 - 152 * frame, 120, 152, x, y)
    pass

def test():
    global frame, look, leg_look
    while running:

        clear_canvas()
        leg_draw()
        head_draw()
        update_canvas()
        if shoot_state:
            delay(0.025)
        else:
            delay(0.05)
        frame = (frame + 1) % 10
        #if frame == 9:
        # if frame == 9:
        #     look = (look + 1) % 18
        # if frame % 5 == 0:
        #     leg_look = (leg_look - 1) % 18
        if look % 2 == 0:
            shoot_able()
        else:
            shoot_disable()
    pass

def shoot_able():
    global shoot_state
    shoot_state = True
    pass
def shoot_disable():
    global shoot_state
    shoot_state = False
    pass
def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

test()
