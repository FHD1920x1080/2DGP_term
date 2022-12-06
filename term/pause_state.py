from pico2d import *
from func import *
import game_framework
import play_state
from ui import UI
# fill here
x = 0
y = 0
def enter():
    global x, y
    x = play_state.window_size[0]//2
    y = play_state.window_size[1]
    pass


def exit():
    # fill here
    pass

def update():
    play_state.frame += 1
    if play_state.frame == 1000000:
        play_state.frame = 0
    pass

def draw():
    clear_canvas()
    play_state.draw_world()
    if passive_cursor(play_state.cursor):
        play_state.player.show_passive()
    elif right_cursor(play_state.cursor):
        play_state.player.show_right()
    elif left_cursor(play_state.cursor):
        play_state.player.show_left()
    UI.font22.draw(x, y - 15, "도움말.", (255, 255, 255))
    UI.font22.draw(x, y - 50, "[저글링] 체력:12 공격력:2", (255, 255, 255))
    UI.font22.draw(x, y - 75, "[폭발 저글링] 체력:12 공격력:20.", (255, 255, 255))
    UI.font22.draw(x, y - 100, "[질럿] 체력:24 공격력:2", (255, 255, 255))
    UI.font22.draw(x, y - 125, "위 세 유닛은 플레이어를 발견하거나 피격당하면, 플레이어를 추격하며 이동속도가 빨라진다", (255, 255, 255))
    UI.font22.draw(x, y - 175, "[뮤탈] 체력:24 공격력:6", (255, 255, 255))
    UI.font22.draw(x, y - 200, "뮤탈은 광역피해는 절반만 받음. 폭발 저글링의 피해는 받지 않음.", (255, 255, 255))
    UI.font22.draw(x, y - 240, "플레이어의 스펙을 올려주는 매커니즘을 생략하는것이 아쉽다. 일단 키입력으로 조절한다.", (255, 255, 255))
    UI.font22.draw(x, y - 275, "기본 조작키 W,A,S,D, 마우스 좌클릭, 마우스 우클릭, 마린의 경우 스페이스바 있음.", (255, 255, 255))
    UI.font22.draw(x, y - 325, "[마린] 대쉬 스킬이 있음, 발사모드를 변경하면 연사력도 달라짐", (255, 255, 255))
    UI.font22.draw(x, y - 350, "[O, P] 공격력, [K, L] 연사력, [N, M] 산탄량", (255, 255, 255))
    UI.font22.draw(x, y - 400, "[골리앗] 미사일은 연사력이 있지만 직접 누르면 누르는대로 나감. ", (255, 255, 255))
    UI.font22.draw(x, y - 425, "[O, P] 공격력, [K, L] 기관총 연사력, [N, M] 기관총 산탄량, [<, >] 미사일 산탄량.", (255, 255, 255))
    UI.font22.draw(x, y - 475, "[드라군] 드라군은 미구현된 부분이 많음.", (255, 255, 255))
    UI.font22.draw(x, y - 500, "[O, P] 공격력, [K, L] 에너지볼 크기.", (255, 255, 255))
    UI.font22.draw(x, y - 550, "0번키를 누르면 적 스폰량이 10배 많아지고", (255, 255, 255))
    UI.font22.draw(x, y - 575, " 플레이어블 유닛들이 제작자가 세팅한 수준으로 강화됨", (255, 255, 255))
    UI.font22.draw(x, y - 600, "9번을 누르면 원래 스폰량으로 돌아감.", (255, 255, 255))
    UI.font22.draw(x, y - 650, "플레이어블 유닛들의 죽음상태 미구현, 현재는 그냥 갖고 노는 장난감같은 게임", (255, 255, 255))
    UI.font22.draw(x, y - 700, "ESC 밑의 ~ 키 입력 시 게임 종료.", (255, 255, 255))
    update_canvas()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            play_state.cursor.x, play_state.cursor.y = event.x, play_state.window_size[1] - 1 - event.y
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                User_input.left_button = True
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                User_input.left_button = False
            if event.button == SDL_BUTTON_RIGHT:
                User_input.right_button = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_BACKQUOTE:
                game_framework.quit()
            elif event.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif event.key == SDLK_a:
                User_input.left_key = True
            elif event.key == SDLK_d:
                User_input.right_key = True
            elif event.key == SDLK_w:
                User_input.up_key = True
            elif event.key == SDLK_s:
                User_input.down_key = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                User_input.left_key = False
            elif event.key == SDLK_d:
                User_input.right_key = False
            elif event.key == SDLK_w:
                User_input.up_key = False
            elif event.key == SDLK_s:
                User_input.down_key = False

def pause():
    pass

def resume():
    pass

def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    game_framework.run(this_module)
    pico2d.close_canvas()

if __name__ == '__main__':
    test_self()