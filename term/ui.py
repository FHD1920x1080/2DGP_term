from pico2d import*

class UI:
    red = None

    hp_bar_max = 200
    @staticmethod
    def draw_hp_bar(x, y, unit):
        UI.red.draw_to_origin(x, y, UI.hp_bar_max*unit.hp/unit.max_hp, 20)
        pass

    def hp(self, unit):
        return unit.hp

    @staticmethod
    def load_resource():
        UI.red = load_image('red.png')