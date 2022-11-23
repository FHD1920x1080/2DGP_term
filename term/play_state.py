from obj_class.marine import Marine
from obj_class.dragoon import Dragoon
from obj_class.bullet import *
from obj_class.zergling import *
from obj_class.zealot import *
from obj_class.mutal import *
from obj_class.cursor import Cursor
from ui import UI
from map import Map
from sound import Sound

import game_world
import game_framework
import camera

# 1. 게임 초기화
window_size = [1920, 1080]
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
                Zergling.zm = 0.01
                Zealot.zm = 0.004
                Mutal.zm = 0.002
            if event.key == SDLK_p:
                Zergling.zm = 0.2
                Zealot.zm = 0.08
                Mutal.zm = 0.04
                game_world.Marine.magazine_gun = True
                game_world.Marine.nfs = 1
                game_world.Marine.n_shot = 1
                game_world.Marine.moving_attack = True
                game_world.Marine.speed = 4
                game_world.Dragoon.speed = 6
                game_world.Dragoon.bull_size = 14
                game_world.Dragoon.AD = 100
        player.handle_events(event)

def update():
    #print(len(game_world.ground_obj))
    Zergling.make_zergling()
    Zealot.make_zealot()
    Mutal.make_mutal()
    game_world.set_clean_list()
    game_world.update_game_world()
    game_world.clean_objects()

    global frame
    if frame % 20 == 0:
        player.hp += 1
        player.hp = clamp(0, player.hp, player.max_hp)
        print(len(game_world.ground_obj))
    if frame % 10 == 0:
        sub_unit.hp += 1
        sub_unit.hp = clamp(0, sub_unit.hp, sub_unit.max_hp)
    camera.moving()


def draw_world():
    for obj in game_world.all_objects():
        obj.show()


    UI.show_sub_portrait(68, 222, sub_unit)
    UI.show_sub_hp_bar(126, 172, sub_unit)
    UI.show_main_portrait(80, 82, player)
    UI.show_main_hp_bar(150, 20, player)
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
    Marine.load_resource()
    Dragoon.load_resource()
    Bullet32.load_resource()
    Zergling.load_resource()
    Zealot.load_resource()
    Mutal.load_resource()
    UI.load_resource()
    Map.load_resource()


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
