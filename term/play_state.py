from obj_class.marine import Marine
from obj_class.dragoon import Dragoon
from obj_class.bullet import *
from obj_class.zergling import *
from obj_class.zealot import *
from obj_class.cursor import Cursor
from ui import *
from sound import Sound

import game_world
import game_framework
import camera

# 1. 게임 초기화
window_size = [1600, 900]
background_img = None
FPS = None # 초당 프레임 90~100 생각 하고 있음.
frame = None # 현재 프레임 0 ~ (FPS-1) 사이값
sound = None
cursor = None
player = None
sub_unit = None
any_6frame = 0 # 6프레임마다 해줄 일들 FPS로 나누어 떨어지는 애들은 필요 없음
any_3frame = 0 # 3프레임마다 해줄 일들
die_ground_list = []

def enter():
    global FPS, frame, sound, cursor, every_6frame, every_3frame, player, sub_unit
    load_resource()
    hide_cursor()
    cursor = Cursor()
    sound = Sound()
    Sound.volume_set_up()
    FPS = 100
    frame = 0
    game_world.Marine = Marine()
    game_world.Dragoon = Dragoon()
    player = game_world.Marine
    sub_unit = game_world.Dragoon
    game_world.ground_obj.append(player)
    every_6frame = 0
    every_3frame = 0
    camera.enter()
    #UnitState.red = load_image('red.png')

def handle_events():
    global player
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_MOUSEMOTION:
            cursor.x, cursor.y = event.x, window_size[1] - 1 - event.y
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_1:
                if player.unit_type != 0:
                    change_character(1)
            if event.key == SDLK_3:
                if player.unit_type != 2:
                    change_character(3)
            if event.key == SDLK_o:
                Zergling.zm = 0.03
            if event.key == SDLK_p:
                Zergling.zm = 0.15
        player.handle_events(event)

def update():
    #print(len(game_world.ground_obj))
    Zergling.make_zergling()
    Zealot.make_zealot()
    game_world.set_clean_list()
    game_world.update_game_world()
    game_world.clean_objects()

    global frame
    if frame % 10 == 0:
        player.hp += 1
        player.hp = clamp(0, player.hp, player.max_hp)
        sub_unit.hp += 2
        sub_unit.hp = clamp(0, sub_unit.hp, sub_unit.max_hp)
        # game_world.Marine.hp += 1
        # game_world.Marine.hp = clamp(0, game_world.Marine.hp, game_world.Marine.max_hp)
        # game_world.Dragoon.hp += 2
        # game_world.Dragoon.hp = clamp(0, game_world.Dragoon.hp, game_world.Dragoon.max_hp)


def draw_world():
    background_img.draw(window_size[0] // 2, window_size[1] // 2)

    for obj in game_world.all_objects():
        obj.show()

    UI.draw_hp_bar(50, window_size[1] - 50, player)
    UI.draw_hp_bar(50, window_size[1] - 100, sub_unit)

    cursor.show()

def draw():
    global frame
    global any_6frame, any_3frame, sound, FPS
    clear_canvas()
    draw_world()
    update_canvas()

    animation(frame)  # 애니메이션 재생 출력은 아님 상태값만 변경
    sound.play()
    frame += 1
    if frame == 1000000:
        frame = 0
        # any_6frame = (any_6frame + FPS) % 6
        # any_3frame = (any_6frame + FPS) % 3


def animation(frame):
    if frame % 10 == 0:
        cursor.frame = (cursor.frame + 1) % 5  # 커서 프레임




def load_resource():
    global background_img

    background_img = load_image('resource\\image\\map.png')
    Marine.load_resource()
    Dragoon.load_resource()
    Bullet32.load_resource()
    Zergling.load_resource()
    Zealot.load_resource()
    UI.load_resource()


def exit():
    global cursor, sound
    del game_world.Player
    del game_world.ground_obj
    del game_world.ground_crash_effect
    del cursor
    del sound


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
