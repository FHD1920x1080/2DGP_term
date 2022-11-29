import obj_class.marine
import obj_class.goliath
import obj_class.dragoon
import obj_class.bullet
import obj_class.zergling
import obj_class.zealot
import obj_class.mutal
import ui
import map


def load_resource():
    obj_class.marine.Marine.load_resource()
    obj_class.goliath.Goliath.load_resource()
    obj_class.dragoon.Dragoon.load_resource()
    obj_class.bullet.Bullet32.load_resource()
    obj_class.zergling.Zergling.load_resource()
    obj_class.zealot.Zealot.load_resource()
    obj_class.mutal.Mutal.load_resource()
    ui.UI.load_resource()
    map.Map.load_resource()


from pico2d import *
import game_framework
import play_state

class Title_State:
    def __init__(self):
        self.image = load_image('resource\\image\\starkraft_tag.png')
        self.font48 = load_font('resource\\ui\\DOSIyagiBoldface.ttf', 48)
        self.music = load_music('resource\\music\\The_Twelve_Days_of_Christmas.wav')
        self.music.set_volume(8)
        self.frame = 0
        self.font_frame = 0
        self.font_color = 255
        self.timer = 1





ts = None


def enter():
    clear_canvas()
    hide_cursor()
    play_state.cursor = ui.Cursor()
    global ts
    ts = Title_State()
    ts.image.draw_to_origin(0, 0, play_state.window_size[0], play_state.window_size[1])
    ts.music.repeat_play()
    update_canvas()
    load_resource()
    pass


def exit():
    del ts.music
    del ts.image
    del ts.font48
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or event.key == SDLK_ESCAPE:
            game_framework.quit()
        if event.type == SDL_MOUSEMOTION:
            play_state.cursor.x, play_state.cursor.y = event.x, play_state.window_size[1] - 1 - event.y
        if ts.timer < 0:
            if event.type == SDL_KEYDOWN or (event.button == SDL_BUTTON_LEFT):
                game_framework.change_state(play_state)


def draw():
    clear_canvas()
    ts.image.draw_to_origin(0, 0, play_state.window_size[0], play_state.window_size[1])
    if ts.timer < 0:
        ts.font48.draw(play_state.window_size[0] // 2 - 290, 50, 'P R E S S  A N Y  K E Y',
                               (255, 255, ts.font_color))
        ts.font_frame = (ts.font_frame + 1) % 256
        if ts.font_frame < 128:
            ts.font_color -= 2
        else:
            ts.font_color += 2
    play_state.cursor.show()
    if ts.frame % 10 == 0:
        play_state.cursor.frame = (play_state.cursor.frame + 1) % 5  # 커서 프레임
    update_canvas()


def update():
    global ts
    ts.frame += 1
    ts.timer -= 1


def pause():
    pass


def resume():
    pass
