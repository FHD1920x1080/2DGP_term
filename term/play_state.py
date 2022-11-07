import game_world
from obj_class.marine import *
from obj_class.zergling import *
from obj_class.zealot import *
from obj_class.cursor import *
import game_framework
import camera

# 1. 게임 초기화
window_size = [1200, 900]
background_img = None
FPS = None # 초당 프레임 90~100 생각 하고 있음.
frame = None # 현재 프레임 0 ~ (FPS-1) 사이값
sound = None
cursor = None
every_6frame = None # 6프레임마다 해줄 일들 FPS로 나누어 떨어지는 애들은 필요 없음
every_3frame = None # 3프레임마다 해줄 일들

class Sound:
    def __init__(self):
        self.Marine_shoot = False
        self.Marine_hit = False
        self.Zergling_die = False
        self.Zealot_die = False

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_MOUSEMOTION:
            cursor.x, cursor.y = event.x, window_size[1] - 1 - event.y
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_EQUALS:
                marine1 = Marine()
                last_marine = Marine.list[len(Marine.list) - 1]
                marine1.move_point(last_marine.stand_x + 40, last_marine.stand_y)
                Marine.list.append(marine1)
            if event.key == SDLK_MINUS:
                if len(Marine.list) > 1:
                    del Marine.list[len(Marine.list) - 1]
            if event.key == SDLK_o:
                Zergling.zm = 0.03
            if event.key == SDLK_p:
                Zergling.zm = 0.3
        for marine in Marine.list:
            marine.handle_events(event)

def animation(frame):
    if frame % 4 == 0:
        for marine in Marine.list:
            marine.move_frame = (marine.move_frame + 1) % 8
        for de in game_world.die_list:
            de.anim()
        for zl in game_world.Zealot_list:
            zl.move_frame = (zl.move_frame + 1) % 8  # 질럿 무브 프레임
    # if (frame + every_3frame) % 3 == 0:
    #     for zl in Zealot.list:
    #         zl.move_frame = (zl.move_frame + 1) % 8  # 질럿 무브 프레임

    if (frame + every_6frame) % 6 == 0:
        for zgl in game_world.Zergling_list:
            zgl.move_frame = (zgl.move_frame + 1) % 7  # 저글링 무브 프레임

        Marine.effect_anim()

    if frame % 10 == 0:
        cursor.frame = (cursor.frame + 1) % 5  # 커서 프레임


def play_sound(frame):
    if (frame + every_3frame) % 6 == 0:
        if sound.Marine_shoot:
            Marine.play_shoot_sound(Marine)
            sound.Marine_shoot = False
        if sound.Marine_hit:
            Marine.play_hit_sound(Marine)
            sound.Marine_hit = False
        if sound.Zergling_die:
            Die_Zergling.play_sound(Die_Zergling)
            sound.Zergling_die = False
        if sound.Zealot_die:
            Die_Zealot.play_sound(Die_Zealot)
            sound.Zealot_die = False


def load_resource():
    global background_img
    background_img = load_image('resource\\image\\tile.png')

    Marine.load_resource()
    Bullet_32.load_resource()
    Zergling.load_resource()
    Zealot.load_resource()


def enter():
    global FPS, frame, sound, cursor, every_6frame, every_3frame, zm
    load_resource()
    hide_cursor()
    cursor = Cursor()
    sound = Sound()
    FPS = 100
    frame = 0
    for asdasd in range(1):
        marine1 = Marine()
        marine1.x_move(40 * asdasd)
        Marine.list.append(marine1)
    every_6frame = 0
    every_3frame = 0
    camera.enter()


def exit():
    global cursor, sound
    del Marine.list
    del game_world.enemy_list
    del Zergling.list
    del Die_Zergling.list
    del Zealot.list
    del Die_Zealot.list
    del cursor
    del sound


def update():
    #SDL_Delay(6)
    for marine in Marine.list:
        marine.state_update()
    # 확률에 따른 적 생성 및 이동

    Zergling.make_zergling()
    Zealot.make_zealot()

    move_enemy_list()
    #Zergling.list_move()
    #Zealot.list_move()

    # 주인공의 공격과 적 충돌체크
    # camera.camera()


def show_All():
    pass


def draw_woral():
    background_img.draw(window_size[0] // 2, window_size[1] // 2)
    # Zergling.show_All()
    # Zealot.show_All()
    show_enemy_list()
    for marine in Marine.list:
        marine.show()
    cursor.show()


def draw():
    global frame
    global every_6frame, every_3frame
    # 게임 월드 렌더링
    clear_canvas()
    # print_fps()
    draw_woral()
    update_canvas()

    animation(frame)  # 애니메이션 재생 출력은 아님 상태값만 변경
    play_sound(frame)
    frame += 1
    if frame == FPS:
        frame = 0
        every_6frame = (FPS + every_6frame) % 6
        every_3frame = (FPS + every_3frame) % 3
    # print(frame)


def pause():
    pass


def resume():
    pass


def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas(window_size[0], window_size[1], sync=True)
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__':
    test_self()
