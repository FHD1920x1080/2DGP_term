from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024


def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        # elif event.type == SDL_MOUSEMOTION:
        #     x, y = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


open_canvas(TUK_WIDTH, TUK_HEIGHT)

# fill here
TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
arrow = load_image('hand_arrow.png')


running = True
sx, sy = TUK_WIDTH // 2, TUK_HEIGHT // 2 #소년의 시작 위치
x, y = sx, sy #소년의 현재 위치
ax, ay = x, y #커서의 위치
a_draw_x = ax + 20
a_draw_y = ay - 23
t = 0
frame = 0
character_pose = 3 #3 오른쪽 멈춤, 1오른쪽 달림 2왼쪽 멈춤 0왼쪽 달림
character_speed = 100
hide_cursor()


def reset_world():
    global character_pose
    global ax, ay
    global t
    global sx, sy
    global a_draw_x
    global a_draw_y
    ax, ay = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)    
    a_draw_x = ax + 20
    a_draw_y = ay - 23
    t = 0
    sx, sy = x, y
    if sx < ax:
        character_pose = 1
    elif sx > ax:
        character_pose = 0
    else:
        pass

def update_world():
    global x, y
    global t
    i = ((ax-sx)**2+(ay-sy)**2)**(1/2)
    t += 0.01*(character_speed/i)
    x = (1 - t) * sx + t * ax
    y = (1 - t) * sy + t * ay

    if t >= 1.0:
        reset_world()

reset_world()

while running:
    update_world()
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    arrow.draw(a_draw_x, a_draw_y)
    character.clip_draw(frame * 100, 100 * character_pose, 100, 100, x, y)

    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()
