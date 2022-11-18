from pico2d import*
class UI:
    green = None
    yellow = None
    orenge = None
    red = None
    deep_red = None
    hp_bar_frame = None
    terran_portrait_frame = None
    protoss_portrait_frame = None
    hp_bar_max = 250

    @staticmethod
    def draw_portrait(x, y, unit):
        if unit.unit_type == 0:
            unit.portrait.clip_draw(unit.portrait_frame * 60, unit.portrait_state * 56, 60, 56, x, y, 126, 117)
            UI.terran_portrait_frame.draw(x, y, 130, 128)
            unit.portrait_anim()
            pass
        elif unit.unit_type == 2:
            unit.portrait.clip_draw(unit.portrait_frame * 60, unit.portrait_state * 56, 60, 56, x, y, 126, 117)
            UI.protoss_portrait_frame.draw(x, y, 130, 128)
            unit.portrait_anim()
            pass
    @staticmethod
    def draw_terran_portrait_frame():

        pass
    @staticmethod
    def draw_protoss_portrait_frame():
        pass

    @staticmethod
    def draw_hp_bar(x, y, unit):
        UI.hp_bar_frame.draw_to_origin(x, y, 259, 38)
        hp = unit.hp/unit.max_hp
        if hp > 0.8:
            UI.green.draw_to_origin(x+4, y+4, UI.hp_bar_max * hp, 30)
        elif hp > 0.6:
            UI.yellow.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
        elif hp > 0.4:
            UI.orenge.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
        elif hp > 0.2:
            UI.red.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
        else:
            UI.deep_red.draw_to_origin(x + 4, y + 4, UI.hp_bar_max * hp, 30)
        pass

    def hp(self, unit):
        return unit.hp

    @staticmethod
    def load_resource():
        UI.green = load_image('resource\\ui\\green.png')
        UI.yellow = load_image('resource\\ui\\yellow.png')
        UI.orenge = load_image('resource\\ui\\orenge.png')
        UI.red = load_image('resource\\ui\\red.png')
        UI.deep_red = load_image('resource\\ui\\deep_red.png')
        UI.hp_bar_frame = load_image('resource\\ui\\hp_bar_frame.png')
        UI.terran_portrait_frame = load_image('resource\\ui\\terran_portrait_frame.png')
        UI.protoss_portrait_frame = load_image('resource\\ui\\protoss_portrait_frame.png')