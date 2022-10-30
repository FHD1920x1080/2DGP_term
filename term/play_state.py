from obj_class.marine import *
from obj_class.zergling import *
from obj_class.cursor import *
import game_framework
import camera

# 1. 게임 초기화
window_size = [1600, 1200]
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

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_MOUSEMOTION:
            cursor.x, cursor.y = event.x, window_size[1] - 1 - event.y
            cursor.draw_x = cursor.x + 20
            cursor.draw_y = cursor.y - 21
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

    if (frame + every_3frame) % 4 == 0:  # 3프레임마다 저글링 사망 애니메이션 프레임 증가하는 구간
        dz2_list = []
        for i in range(len(Die_Zergling.list)):
            Die_Zergling.list[i].die_anim()
            if Die_Zergling.list[i].die_frame > FPS:  # 일정 시간이 지난 시체 3초
                dz2_list.append(i)
        dz2_list.sort(reverse=True)
        for dz2 in dz2_list:
            del Die_Zergling.list[dz2]

    if (frame + every_6frame) % 6 == 0:
        for zgl in Zergling.list:
            zgl.move_frame = (zgl.move_frame + 1) % 7  # 저글링 무브 프레임
        for marine in Marine.list:
            de_list = []
            for i in range(len(marine.effect_list)):
                marine.effect_list[i].anim()
                if marine.effect_list[i].frame > 4:  # 마린 공격 이펙트 프레임
                    de_list.append(i)
            de_list.sort(reverse=True)
            for de in de_list:
                del marine.effect_list[de]

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


def load_resource():
    global background_img
    background_img = load_image('resource\\image\\tile.png')
    Cursor.arrow_img = load_image('resource\\image\\arrowx200.png')

    Marine.img = load_image('resource\\marine\\marine250x2.png')
    Effect.crash_img = load_image('resource\\marine\\attack_effect_blue.png')
    Marine.hit_sound = load_wav('resource\\bullet\\hit_sound\\06.wav')
    Marine.hit_sound.set_volume(6)
    Marine.shoot_sound00 = load_wav('resource\\marine\\shoot_sound\\00.wav')
    Marine.shoot_sound00.set_volume(16)
    Marine.shoot_sound01 = load_wav('resource\\marine\\shoot_sound\\01.wav')
    Marine.shoot_sound01.set_volume(16)
    Marine.shoot_sound02 = load_wav('resource\\marine\\shoot_sound\\02.wav')
    Marine.shoot_sound02.set_volume(16)
    Marine.shoot_sound03 = load_wav('resource\\marine\\shoot_sound\\03.wav')
    Marine.shoot_sound03.set_volume(16)

    for i in range(0, 32):
        Bullet_32.img.append(load_image("resource\\bullet\\" + str(i) + ".png"))
        # Bullet_32.img[i] = load_image("resource\\bullet\\" + str(i) + ".png")

    Zergling.img = load_image("resource\\zergling\\zerglingx200x2.png")
    Die_Zergling.img = load_image("resource\\zergling\\die_zergling.png")
    Die_Zergling.sound = load_wav('resource\\zergling\\zzedth01.wav')
    Die_Zergling.sound.set_volume(8)



def enter():
    global FPS, frame, sound, cursor, every_6frame, every_3frame, zm
    Zergling.zm = 0.03
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
    del Zergling.list
    del Die_Zergling.list
    del cursor
    del sound


def update():
    SDL_Delay(6)
    for marine in Marine.list:
        marine.check_magazine()
        marine.state_update()
    # 확률에 따른 적 생성 및 이동

    Zergling.make_zergling()
    Zergling.list_move()
    # 주인공의 공격과 적 충돌체크
    Bullet_32.move_crash_chack()
    # camera.camera()


def show_All():
    Zergling.show_All()
    for marine in Marine.list:
        for blt in marine.bullet_list:
            blt.show()

    for marine in Marine.list:
        marine.show()
    for marine in Marine.list:
        for eft in marine.effect_list:
            eft.show()
    cursor.show()


def draw_woral():
    background_img.draw(window_size[0] // 2, window_size[1] // 2)
    show_All()


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
