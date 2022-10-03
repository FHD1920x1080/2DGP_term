from pico2d import *
import random

open_canvas()
character = load_image('marine250x2.png')
effect = load_image('image2.png')
running = True
x = 800 // 2
y = 600 // 2


def idle_1():
    a = random.randrange(0, 16) # 0~15
    b = random.randrange(0, 2) # 0~1
    if b == 0:
        b = -1
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * a), 2180 - 80, 100, 75, x, y)
    update_canvas()
    delay(1)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (5 * 160 * 1), 100, 75, x, y)
    update_canvas()
    delay(0.08)
    a = a + b
    a = a % 16
    clear_canvas()
    character.clip_draw(30 + 2 * 160 * a, 2180 - 80 - (6 * 160 * 1), 100, 75, x, y)
    update_canvas()
    delay(0.08)
    a = a + b
    a = a % 16
    clear_canvas()
    character.clip_draw(30 + 2 * 160 * a, 2180 - 80, 100, 75, x, y)
    update_canvas()
    delay(1)
    pass


def idle_2():
    a = 3  # random.randrange(0, 6)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 0), 100, 75, x, y)
    update_canvas()
    delay(1)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 1), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 1), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 2), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 3), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 4), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.5)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 3), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 2), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 1), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 1), 100, 75, x, y)
    update_canvas()
    delay(0.2)
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 0), 100, 75, x, y)
    update_canvas()
    delay(0.5)
    pass


def right_move():
    frame = 0
    for asd123 in range(27):
        clear_canvas()
        character.clip_draw(1310, 2180 - 720 - (160 * frame), 100, 75, x, y)
        update_canvas()
        frame = (frame + 1) % 9
        delay(0.05)
    pass


def die():
    clear_canvas()
    character.clip_draw(30 + (2 * 160 * 8), 2180 - 80 - (1 * 160 * 0), 100, 75, x, y)
    update_canvas()
    delay(1)
    frame = 0
    for asd123 in range(8):
        print(asd123)
        clear_canvas()
        character.clip_draw(0 + (1 * 160 * frame), 2180 - 80 - (1 * 160 * 13)-13, 160, 100, x, y)
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.1)
    delay(1)
    pass

def test():
    frame = 0
    for asd123 in range(16):
        clear_canvas()
        character.clip_draw(30 + ( 2* 160 * frame), 2180 - 80 - (1 * 160 * 3), 100, 85, x, y)
        update_canvas()
        frame = (frame + 1) % 16
        delay(0.5)
    pass
def attack():
    for a in range(0,16):
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 0), 100, 85, x, y)
        update_canvas()
        delay(0.2)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 1), 100, 85, x, y)
        update_canvas()
        delay(0.2)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 2), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 3), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 2), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 3), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 2), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 3), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 2), 100, 85, x, y)
        update_canvas()
        delay(0.08)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 3), 100, 85, x, y)
        update_canvas()
        delay(0.15)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 1), 100, 85, x, y)
        update_canvas()
        delay(0.2)
        clear_canvas()
        character.clip_draw(30 + (2 * 160 * a), 2180 - 80 - (1 * 160 * 0), 100, 85, x, y)
        update_canvas()
        delay(0.2)
    pass
def effect123():
    frame=0
    for asd in range(0,15):
        clear_canvas()
        effect.clip_draw(0, 1200-80*frame, 80, 80, x, y)
        frame = (frame + 1) % 15
        update_canvas()
        delay(0.08)
    pass

while running:
    idle_1()
    idle_2()
    die()
    right_move()
    test()
    attack()
    effect123()
    update_canvas()

close_canvas()
