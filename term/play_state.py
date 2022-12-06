from obj_class.marine import Marine
from obj_class.goliath import Goliath
from obj_class.dragoon import Dragoon
from obj_class.bullet import *
from obj_class.zergling import *
from obj_class.zealot import *
from obj_class.mutal import *
from map import Map
from cursor import Cursor
from ui import UI
from sound import Sound
import camera # 얘는 객체가 아님

import game_world
import game_framework


# 1. 게임 초기화
window_size = [1920, 1080]
#window_size = [1600, 900]
frame = None  # 현재 프레임
sound = None
cursor = None
player = None
sub_unit1 = None
sub_unit2 = None

change_character_cool_time = 300
cur_change_character_cool_time = 0

def enter():
    global frame, sound, cursor, player, sub_unit1, sub_unit2
    sound = Sound()
    Sound.volume_set_up()
    frame = 0
    game_world.Marine = Marine()
    game_world.Goliath = Goliath()
    game_world.Dragoon = Dragoon()
    player = game_world.Marine
    sub_unit1 = game_world.Goliath
    sub_unit2 = game_world.Dragoon
    game_world.ground_obj.append(player)
    camera.enter()
    Zergling.zm = 0.01
    BombZergling.zm = 0.002
    Zealot.zm = 0.004
    Mutal.zm = 0.0015
    # UnitState.red = load_image('red.png')


def handle_events():
    global player, cur_change_character_cool_time
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_MOUSEMOTION:
            cursor.x, cursor.y = event.x, window_size[1] - 1 - event.y
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_1:
                if player.unit_type != 0 and cur_change_character_cool_time == 0:
                    change_character(1)
                    cur_change_character_cool_time = change_character_cool_time
            elif event.key == SDLK_2:
                if player.unit_type != 1 and cur_change_character_cool_time == 0:
                    change_character(2)
                    cur_change_character_cool_time = change_character_cool_time
            elif event.key == SDLK_3:
                if player.unit_type != 2 and cur_change_character_cool_time == 0:
                    change_character(3)
                    cur_change_character_cool_time = change_character_cool_time
            elif event.key == SDLK_o:
                Zergling.zm = 0.01
                BombZergling.zm = 0.002
                Zealot.zm = 0.004
                Mutal.zm = 0.0015
            elif event.key == SDLK_p:
                Zergling.zm = 0.1
                BombZergling.zm = 0.02
                Zealot.zm = 0.04
                Mutal.zm = 0.03
                game_world.Marine.magazine_gun = True
                game_world.Marine.AD = 10
                game_world.Marine.nfs = 3
                game_world.Marine.n_shot = 1
                game_world.Marine.speed = 4
                game_world.Marine.drag_bull_size = 2.0
                game_world.Marine.drag_bull_cool_time = 100
                #game_world.Dragoon.speed = 6
                game_world.Dragoon.bull_size = 5
                game_world.Dragoon.AD = 30
                game_world.Goliath.AD = 4
                game_world.Goliath.nfs = 6
                game_world.Goliath.n_shot = 4
                game_world.Goliath.n_shot_m = 6
                #game_world.Goliath.speed = 5
        player.handle_events(event)


def update():
    # print(len(game_world.ground_obj))
    if len(game_world.ground_obj) < 140:
        Zergling.make_zergling()
        BombZergling.make_zergling()
        Zealot.make_zealot()
    Mutal.make_mutal()
    game_world.set_clean_list()
    game_world.update_game_world()
    game_world.clean_objects()

    global cur_change_character_cool_time
    cur_change_character_cool_time = max(cur_change_character_cool_time - 1, 0)
    game_world.Marine.cur_dash_cool_time = max(game_world.Marine.cur_dash_cool_time - 1, 0)
    game_world.Marine.cur_drag_bull_cool_time = max(game_world.Marine.cur_drag_bull_cool_time - 1, 0)
    if game_world.Goliath.cur_save_missile < game_world.Goliath.max_save_missile:
        game_world.Goliath.missile_charge_time -= 1
        if game_world.Goliath.missile_charge_time == 0:
            game_world.Goliath.missile_charge_time = game_world.Goliath.max_missile_charge_time
            game_world.Goliath.cur_save_missile = min(game_world.Goliath.cur_save_missile + 1, game_world.Goliath.max_save_missile)
    global frame
    if frame % 40 == 0:
        player.hp += 1
        player.hp = clamp(0, player.hp, player.max_hp)
    if frame % 20 == 0:
        sub_unit1.hp += 1
        sub_unit1.hp = clamp(0, sub_unit1.hp, sub_unit1.max_hp)
        sub_unit2.hp += 1
        sub_unit2.hp = clamp(0, sub_unit2.hp, sub_unit2.max_hp)
    camera.moving()


def draw_world():
    for obj in game_world.all_objects():
        obj.show()

    UI.show()
    cursor.show()


def draw():
    global frame
    global sound
    clear_canvas()
    draw_world()

    if passive_cursor(cursor):
        player.show_passive()
    elif right_cursor(cursor):
        player.show_right()
    elif left_cursor(cursor):
        player.show_left()

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
