from pico2d import*
import play_state

class UI:
    green = None
    lime = None
    yellow = None
    orenge = None
    red = None
    deep_red = None
    hp_bar_frame = None
    terran_portrait_frame = None # 재생하는 변수가 아니라, 이미지임
    terran_portrait_frame_g = None  # 재생하는 변수가 아니라, 이미지임
    protoss_portrait_frame = None
    warning = None
    skill_icon = None
    black_50 = None
    black_30 = None
    infinite = None
    font64 = None
    font32 = None
    font22 = None
    font16 = None
    font_korean22 = None
    hp_bar_max = 250
    sub = 0.8 # 항상 일정한 값 계산중이라서 최종적으론 다 상수로 대체할 예정

    warning_frame = 0
    warning_img_now = 0


    @staticmethod
    def show():
        play_state.player.show_main_ui()
        UI.show_sub_portrait(68, 352, play_state.sub_unit1)
        UI.show_sub_hp_bar(126, 302, play_state.sub_unit1)
        UI.show_sub_portrait(68, 222, play_state.sub_unit2)
        UI.show_sub_hp_bar(126, 172, play_state.sub_unit2)
        UI.show_main_portrait(80, 82, play_state.player)
        UI.show_main_hp_bar(150, 20, play_state.player)

    @staticmethod
    def show_main_portrait(x, y, unit):
        unit.portrait.clip_draw(unit.portrait_frame * 60, unit.portrait_state * 56, 60, 56, x, y, 124, 115)
        if unit.unit_type == 0:
            UI.terran_portrait_frame.draw(x, y, 130, 128)
        elif unit.unit_type == 1:
            UI.terran_portrait_frame_g.draw(x, y, 130, 128)
        else:
            UI.protoss_portrait_frame.draw(x, y, 130, 128)
        unit.portrait_anim()

    @staticmethod
    def show_sub_portrait(x, y, unit):
        unit.portrait.clip_draw(unit.portrait_frame * 60, unit.portrait_state * 56, 60, 56, x, y, 124 * UI.sub, 115 * UI.sub)
        if play_state.cur_change_character_cool_time > 0:
            UI.black_30.draw_to_origin(x - (124 * UI.sub)//2, y - (115 * UI.sub)//2, 124 * UI.sub, 115 * UI.sub)
            UI.black_50.draw_to_origin(x - (124 * UI.sub)//2, y - (115 * UI.sub)//2, 124 * UI.sub, play_state.cur_change_character_cool_time / play_state.change_character_cool_time * 115 * UI.sub)
            UI.font32.draw(x - (124 * UI.sub)//2 + 22, y - (115 * UI.sub)//2 + 40, f'{play_state.cur_change_character_cool_time*0.01:1.1f}', (255, 255, 255))
        if unit.unit_type == 0:
            UI.terran_portrait_frame.draw(x, y, 130 * UI.sub, 128 * UI.sub)
        elif unit.unit_type == 1:
            UI.terran_portrait_frame_g.draw(x, y, 130 * UI.sub, 128 * UI.sub)
        else:
            UI.protoss_portrait_frame.draw(x, y, 130 * UI.sub, 128 * UI.sub)
        unit.portrait_anim()

    @staticmethod
    def show_main_hp_bar(x, y, unit):
        UI.hp_bar_frame.draw_to_origin(x, y, 259, 38)
        hp = unit.hp/unit.max_hp
        if hp > 0.3:
            if hp > 0.85:
                UI.green.draw_to_origin(x+4, y+4, UI.hp_bar_max * hp, 30)
            elif hp > 0.7:
                UI.lime.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
            elif hp > 0.5:
                UI.yellow.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
            else:
                UI.orenge.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
                UI.warning.clip_draw_to_origin(UI.warning_img_now * 320, 0, 320, 180, 0, 0, 1920, 1080)
            UI.warning_anim_off()
        else:
            if hp > 0.15:
                UI.red.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
            else:
                UI.deep_red.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
            UI.warning.clip_draw_to_origin(UI.warning_img_now * 320, 0, 320, 180, 0, 0, 1920, 1080)
            UI.warning_anim()
        UI.font22.draw(x+170, y+19, f'{unit.hp:3.0f}/{unit.max_hp}', (255, 255, 255))

    @staticmethod
    def show_sub_hp_bar(x, y, unit):
        UI.hp_bar_frame.draw_to_origin(x, y, 259 * UI.sub, 38 * UI.sub)
        hp = unit.hp / unit.max_hp
        if hp > 0.85:
            UI.green.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp * UI.sub, 30 * UI.sub)
        elif hp > 0.7:
            UI.lime.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp * UI.sub, 30 * UI.sub)
        elif hp > 0.5:
            UI.yellow.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp * UI.sub, 30 * UI.sub)
        elif hp > 0.3:
            UI.orenge.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp * UI.sub, 30 * UI.sub)
        elif hp > 0.15:
            UI.red.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp * UI.sub, 30 * UI.sub)
        else:
            UI.deep_red.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp * UI.sub, 30 * UI.sub)
        UI.font16.draw(x + 140, y + 15, f'{unit.hp:3.0f}/{unit.max_hp}', (255, 255, 255))


    @staticmethod
    def warning_anim():
        if play_state.frame % 6 == 0:
            UI.warning_frame = (UI.warning_frame + 1) % 40
            if UI.warning_frame < 20:
                UI.warning_img_now += 1
            else:
                UI.warning_img_now -= 1

    @staticmethod
    def warning_anim_off():
        if play_state.frame % 6 == 0:
            UI.warning_frame -= 1
            UI.warning_img_now -= 1
            if UI.warning_img_now < 0:
                UI.warning_frame = 0
                UI.warning_img_now = 0


    @staticmethod
    def load_resource():
        UI.green = load_image('resource\\ui\\green.png')
        UI.lime = load_image('resource\\ui\\lime.png')
        UI.yellow = load_image('resource\\ui\\yellow.png')
        UI.orenge = load_image('resource\\ui\\orenge.png')
        UI.red = load_image('resource\\ui\\red.png')
        UI.deep_red = load_image('resource\\ui\\deep_red.png')
        UI.hp_bar_frame = load_image('resource\\ui\\hp_bar_frame.png')
        UI.warning = load_image('resource\\ui\\warning.png')
        UI.infinite = load_image('resource\\ui\\infinite_white.png')
        UI.skill_icon = load_image('resource\\ui\\skill_icon_v3.png')
        UI.black_50 = load_image('resource\\ui\\black_a50.png')
        UI.black_30 = load_image('resource\\ui\\black_a30.png')
        UI.terran_portrait_frame = load_image('resource\\ui\\terran_portrait_frame.png')
        UI.terran_portrait_frame_g = load_image('resource\\ui\\terran_portrait_frame_green.png')
        UI.protoss_portrait_frame = load_image('resource\\ui\\protoss_portrait_frame.png')

        UI.font64 = load_font('resource\\ui\\DOSIyagiBoldface.ttf', 64)
        UI.font32 = load_font('resource\\ui\\DOSIyagiBoldface.ttf', 32)
        UI.font22 = load_font('resource\\ui\\DOSIyagiBoldface.ttf', 22)
        UI.font16 = load_font('resource\\ui\\DOSIyagiBoldface.ttf', 16)
        UI.font_korean22 = load_font('resource\\ui\\NeoDunggeunmoPro-Regular.ttf', 16)

class Cursor:
    img = None
    cross_hair_img = None

    def __init__(self):
        if Cursor.img == None:
            Cursor.img = load_image('resource\\ui\\arrowx200.png')
        self.img_now = [2, 2]  # 스프라이트 좌표
        self.x = round(play_state.window_size[0] / 2)
        self.y = round(play_state.window_size[1] / 2)
        self.frame = 0

    def show(self):
        self.img.clip_draw(self.img_now[0] + self.frame * 44, self.img_now[1], 40, 42, self.x + 20, self.y - 21)