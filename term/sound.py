import play_state


class Sound:
    list = []
    volume_list = []

    current_volume = 50

    def __init__(self):
        self.Marine_shoot = False
        self.Bullet32_hit = False
        self.Zergling_die = False
        self.Zergling_hit = False
        self.Zealot_die = False
        self.Zealot_hit = False
        self.Dragoon_bull_bomb = False

    def play(self):
        if play_state.frame % 6 == 0:
            if self.Marine_shoot:
                play_state.Marine.play_shoot_sound()
                self.Marine_shoot = False
            if self.Bullet32_hit:
                play_state.Bullet32_Effect.play_hit_sound()
                self.Bullet32_hit = False
            if self.Dragoon_bull_bomb:
                play_state.DragBullEffect.play_bomb_sound()
                self.Dragoon_bull_bomb = False
        elif (play_state.frame + 3) % 6 == 0:
            if self.Zergling_die:
                play_state.DieZergling.play_sound()
                self.Zergling_die = False
            if self.Zergling_hit:
                play_state.Zergling.play_hit_sound()
                self.Zergling_hit = False
            if self.Zealot_die:
                play_state.Die_Zealot.play_sound()
                self.Zealot_die = False
            if self.Zealot_hit:
                play_state.Zealot.play_hit_sound()
                self.Zealot_hit = False

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
