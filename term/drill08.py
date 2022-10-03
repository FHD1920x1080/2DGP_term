from pico2d import *
#TUK_WIDTH, TUK_HEIGHT = 1280, 1024
TUK_WIDTH, TUK_HEIGHT = 800, 600
def handle_events():
    global running
    global x, y
    global x_dir
    global y_dir
    global character_pose
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                x_dir += 1
                character_pose = 1
            elif event.key == SDLK_LEFT:
                x_dir -= 1
                character_pose = 0
            elif event.key == SDLK_UP:
                y_dir += 1
                if character_pose == 3:
                    character_pose = 1
                elif character_pose == 2:
                    character_pose = 0
            elif event.key == SDLK_DOWN:
                y_dir -= 1
                if character_pose == 3:
                    character_pose = 1
                elif character_pose == 2:
                    character_pose = 0
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                x_dir -= 1
                character_pose = 3
            elif event.key == SDLK_LEFT:
                x_dir += 1
                character_pose = 2
            elif event.key == SDLK_UP:
                y_dir -= 1
                if character_pose == 1:
                    character_pose = 3
                elif character_pose == 0:
                    character_pose = 2
            elif event.key == SDLK_DOWN:
                y_dir += 1
                if character_pose == 1:
                    character_pose = 3
                elif character_pose == 0:
                    character_pose = 2

    pass


open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x = 800 // 2
y = 90
frame = 0
x_dir = 0
y_dir = 0
character_pose = 3#3 오른쪽 멈춤, 1오른쪽 달림 2왼쪽 멈춤 0왼쪽 달림
while running:
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * character_pose, 100, 100, x, y)
    update_canvas()

    handle_events()
    frame = (frame + 1) % 8
    if x + x_dir * 5 > TUK_WIDTH - 30:
        if y_dir == 0:
            character_pose = 3
    elif x + x_dir * 5 < 30:
        if y_dir == 0:
            character_pose = 2
    else:
        x += x_dir * 5

    if y + y_dir * 5 > TUK_HEIGHT - 50:
        if x_dir == 0:
            if character_pose == 1:
                character_pose = 3
            elif character_pose == 0:
                character_pose = 2
    elif y + y_dir * 5 < 50:
        if x_dir == 0:
            if character_pose == 1:
                character_pose = 3
            elif character_pose == 0:
                character_pose = 2
    else:
        y += y_dir * 5
    delay(0.01)

close_canvas()

