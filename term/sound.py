from pico2d import*
import play_state

class Sound:
    list = []
    volume_list = []

    current_volume = 50

    music = [None, None]
    def __init__(self):
        self.Marine_shoot = False
        self.Marine_shoot2 = False
        self.Goliath_shoot = False
        self.Goliath_shoot2 = False
        self.Bullet32_hit = False
        self.Dragoon_shoot = False
        self.Dragoon_bull_bomb = False
        self.Zergling_die = False
        self.Zergling_hit = False
        self.Zealot_die = False
        self.Zealot_hit = False
        self.Mutal_die = False
        self.Mutal_shoot = False
        self.Zerg_Bomb = False

    def play(self):
        if play_state.frame % 6 == 0:
            if self.Marine_shoot:
                play_state.Marine.play_shoot_sound()
                self.Marine_shoot = False
            if self.Marine_shoot2:
                play_state.Marine.play_shoot2_sound()
                self.Marine_shoot2 = False
            if self.Goliath_shoot:
                play_state.Goliath.play_shoot_sound()
                self.Goliath_shoot = False
            if self.Goliath_shoot2:
                play_state.Goliath.play_shoot2_sound()
                self.Goliath_shoot2 = False
            if self.Bullet32_hit:
                play_state.Bullet32.play_hit_sound()
                self.Bullet32_hit = False
            if self.Dragoon_shoot:
                play_state.Dragoon.play_shoot_sound()
                self.Dragoon_shoot = False
            if self.Dragoon_bull_bomb:
                play_state.DragBullEffect.play_bomb_sound()
                self.Dragoon_bull_bomb = False
        if play_state.frame % 10 == 0:
            if self.Zealot_die:
                play_state.DieZealot.play_sound()
                self.Zealot_die = False
            if self.Zealot_hit:
                play_state.Zealot.play_hit_sound()
                self.Zealot_hit = False
            if self.Mutal_die:
                play_state.DieMutal.play_sound()
                self.Mutal_die = False
            if self.Mutal_shoot:
                play_state.Mutal.play_shoot_sound()
                self.Mutal_shoot = False
        elif (play_state.frame + 5) % 10 == 0:
            if self.Zergling_die:
                play_state.DieZergling.play_sound()
                self.Zergling_die = False
            if self.Zergling_hit:
                play_state.Zergling.play_hit_sound()
                self.Zergling_hit = False
            if self.Zerg_Bomb:
                play_state.ZergBomb.play_bomb_sound()
                self.Zerg_Bomb = False
    @staticmethod
    def volume_set_up():
        for i in range(len(Sound.list)):
            Sound.list[i].set_volume(int(Sound.volume_list[i] * (Sound.current_volume / 100)))

    @staticmethod
    def volume_up():
        Sound.current_volume += 1
        if Sound.current_volume > 100:
            Sound.current_volume = 100
        Sound.volume_set_up()

    @staticmethod
    def volume_down():
        Sound.current_volume -= 1
        if Sound.current_volume < 0:
            Sound.current_volume = 0
        Sound.volume_set_up()

    @staticmethod
    def load_resource():
        Sound.music[0] = load_music('resource\\music\\terran1.ogg')
        Sound.music[0].set_volume(10)
        Sound.music[1] = load_music('resource\\music\\zerg2.ogg')
        Sound.music[1].set_volume(10)
        pass