from pico2d import *
from func import *
import game_world
from obj_class.bullet import Bullet32, Bullet32_Effect, Drag_Bull
from obj_class.marine import Marine
from obj_class.dragoon import Dragoon
from obj_class.zergling import Zergling, Die_Zergling
from obj_class.zealot import Zealot, Die_Zealot
from obj_class.cursor import Cursor
import game_framework
import camera

# 1. 게임 초기화
window_size = [1200, 900]
background_img = None
FPS = None # 초당 프레임 90~100 생각 하고 있음.
frame = None # 현재 프레임 0 ~ (FPS-1) 사이값
sound = None
cursor = None
player = None
every_6frame = 0 # 6프레임마다 해줄 일들 FPS로 나누어 떨어지는 애들은 필요 없음
every_3frame = 0 # 3프레임마다 해줄 일들


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
                Zergling.zm = 0.3
        player.handle_events(event)

def animation(frame):
    if frame % 4 == 0:
        if player.unit_type == 0:
            player.move_frame = (player.move_frame + 1) % 8
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

        effect_anim()

    if frame % 10 == 0:
        cursor.frame = (cursor.frame + 1) % 5  # 커서 프레임


def play_sound(frame):
    if (frame + every_6frame) % 6 == 0:
        if sound.Marine_shoot:
            Marine.play_shoot_sound()
            sound.Marine_shoot = False
        if sound.Bullet32_hit:
            Bullet32_Effect.play_hit_sound()
            sound.Bullet32_hit = False
        if sound.Zergling_die:
            Die_Zergling.play_sound()
            sound.Zergling_die = False
        if sound.Zealot_die:
            Die_Zealot.play_sound()
            sound.Zealot_die = False


def load_resource():
    global background_img
    background_img = load_image('resource\\image\\tile.png')

    Marine.load_resource()
    Dragoon.load_resource()
    Bullet32.load_resource()
    Zergling.load_resource()
    Zealot.load_resource()


def enter():
    global FPS, frame, sound, cursor, every_6frame, every_3frame, player
    load_resource()
    hide_cursor()
    cursor = Cursor()
    sound = Sound()
    FPS = 100
    frame = 0
    for asdasd in range(1):
        marine1 = Marine()
        marine1.x_move(40 * asdasd)
        #Marine.list.append(marine1)
        game_world.Marine.append(marine1)
    dragoon1 = Dragoon()
    game_world.Dragoon.append(dragoon1)
    player = game_world.Marine[0]
    #player = game_world.Dragoon[0]
    every_6frame = 0
    every_3frame = 0
    camera.enter()


def exit():
    global cursor, sound
    del game_world.Player
    del game_world.enemy_list
    del game_world.die_list
    del Zealot.list
    del Die_Zealot.list
    del cursor
    del sound


def update():
    #SDL_Delay(25)
    global player
    # for marine in Marine.list:
    #     marine.update()
    player.update()
    Bullet32.list_move_crash_chack()
    Drag_Bull.list_move()
    # 확률에 따른 적 생성 및 이동

    Zergling.make_zergling()
    Zealot.make_zealot()

    move_enemy_list()
    #Zergling.list_move()
    #Zealot.list_move()

    # 주인공의 공격과 적 충돌체크
    #camera.camera()



def draw_world():
    background_img.draw(window_size[0] // 2, window_size[1] // 2)
    # Zergling.show_All()
    # Zealot.show_All()
    show_enemy_list()
    for blt in game_world.bullet_list:
        blt.show()
    player.show()
    for blt in game_world.explosive_bullet_list:
        blt.show()
    for eft in game_world.effect_list:
        eft.show()
    cursor.show()


def draw():
    global frame
    global every_6frame, every_3frame, player
    # if player.unit_type == 2:
    #     if player.shoot_frame//6 == 2:
    #         print(player.shoot_frame)
    # 게임 월드 렌더링
    clear_canvas()
    # print_fps()
    draw_world()
    update_canvas()

    animation(frame)  # 애니메이션 재생 출력은 아님 상태값만 변경
    play_sound(frame)
    frame += 1
    if frame == FPS:
        frame = 0
    #     every_6frame = (FPS + every_6frame) % 6
    #     every_3frame = (FPS + every_3frame) % 3
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
