import math
import game_world
import play_state


class User_input:
    left_key = False  # 왼쪽으로 가는키가 눌렸는지
    right_key = False
    up_key = False
    down_key = False
    left_button = False


class Sound:
    list = []
    volume_list = []

    current_volume = 50

    def __init__(self):
        self.Marine_shoot = False
        self.Bullet32_hit = False
        self.Zergling_die = False
        self.Zealot_die = False

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


def crash(a, b):
    if a.hit_sx <= 0 or b.hit_sx <= 0:
        return False
    if a.hit_x + (a.hit_sx / 2) >= b.hit_x - (b.hit_sx / 2) and a.hit_x - (a.hit_sx / 2) <= b.hit_x + (
            b.hit_sx / 2) and a.hit_y + (a.hit_sy / 2) >= b.hit_y - (b.hit_sy / 2) and a.hit_y - (
            a.hit_sy / 2) <= b.hit_y + (b.hit_sy / 2):
        return True
    else:
        return False


def bullet_crash(a, b):
    if a.exist == False:
        return False
    if b.hp <= 0:
        return False

    if a.x < b.hit_x - b.hit_sx:
        return False
    if a.x > b.hit_x + b.hit_sx:
        return False
    if a.y < b.hit_y - b.hit_sy:
        return False
    if a.y > b.hit_y + b.hit_sy:
        return False

    return True


def tir_rect_crash(bullet, unit):
    if unit.hp <= 0:
        return False

    if unit.get_hit_bottom() > bullet.get_top(0):
        return False
    if unit.get_hit_top() < bullet.get_bottom(0):
        return False
    if unit.get_hit_left() > bullet.get_right(1):
        return False
    if unit.get_hit_right() < bullet.get_left(1):
        return False

    # 이제 이 안에선 충돌할 확률이 더 높음.
    if unit.get_hit_right() >= bullet.get_left(0) and unit.get_hit_left() <= bullet.get_right(0):
        return True
    if unit.get_hit_top() >= bullet.get_bottom(1) and unit.get_hit_bottom() <= bullet.get_top(1):
        return True
    if unit.get_hit_right() >= bullet.get_left(2) and unit.get_hit_left() <= bullet.get_right(2):
        if unit.get_hit_top() >= bullet.get_bottom(2) and unit.get_hit_bottom() <= bullet.get_top(2):
            return True

    return False


def cheak_collision_min_move(unit1, unit2):  # unit1이 움직인놈
    if unit1 == unit2:  # 자기 자신인가
        return False

    bottom = unit1.get_bottom() - unit2.get_top()
    if bottom > 0:
        return False
    max = bottom
    top = unit2.get_bottom() - unit1.get_top()
    if top > 0:
        return False
    if max < top:
        max = top
    left = unit1.get_left() - unit2.get_right()
    if left > 0:
        return False
    if max < left:
        max = left
    right = unit2.get_left() - unit1.get_right()
    if right > 0:
        return False
    if max < right:
        max = right

    # top,bottom,right,left가 모두 음수이며 최대값인 놈으로 밀어냄,(가장 조금만 밀어도 되는 쪽으로 밀기 위함)
    if max == right:
        unit1.x_move(right)
    elif max == left:
        unit1.x_move(-left)
    elif max == top:
        unit1.y_move(top)
    else:
        unit1.y_move(-bottom)
    return True


def cheak_collision(unit1, unit2):  # unit1이 움직인놈
    if unit1 == unit2:  # 자기 자신인가
        return False

    if unit1.get_bottom() - unit2.get_top() > 0:
        return False
    if unit2.get_bottom() - unit1.get_top() > 0:
        return False
    if unit1.get_left() - unit2.get_right() > 0:
        return False
    if unit2.get_left() - unit1.get_right() > 0:
        return False

    return True


def change_character(key):
    sx, sy = play_state.player.stand_x, play_state.player.stand_y
    if key == 1:
        play_state.player = game_world.Marine[0]
        play_state.player.shoot_able = False
        play_state.player.move_able = True
    elif key == 3:
        play_state.player = game_world.Dragoon[0]
        play_state.player.state = 1
    play_state.player.x_move_point(sx)
    play_state.player.y_move_point(sy)


def update_enemy_list():
    for em in game_world.ground_enemy:  # 적들
        em.update()
        if em.exist == False:  # 1이면 밑으로 이미 내려간거
            game_world.remove_enemy(em)
        else:
            # em.direction = 0
            for other in game_world.ground_enemy:
                if cheak_collision_min_move(em, other):
                    pass
    game_world.ground_enemy.sort(key=lambda x: x.stand_y,reverse=True)


def show_enemy_list():
    for de in game_world.die_list:
        de.show()
    for em in game_world.enemy_list():
        em.show()


def effect_anim():
    for ef in game_world.effect_list:
        ef.anim()


def get_rad(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


def get_dir(rad):
    if rad >= 0:  # 1, 2 사분면
        if rad < 0.1963:  # 우측
            return 8
        elif rad < 0.589:
            return 6
        elif rad < 1.0517:
            return 4
        elif rad < 1.3844:
            return 2
        elif rad < 1.8:
            return 0
        elif rad < 2.0898:
            return 30
        elif rad < 2.5525:
            return 28
        elif rad < 2.9452:
            return 26
        else:  # rad <= 3.1415:
            return 24
    else:  # 3,4분면
        if rad > -0.0663:  # 우측
            return 8
        elif rad > -0.31:
            return 10
        elif rad > -0.7017:
            return 12
        elif rad > -1.2044:
            return 14
        elif rad > -1.5708:
            return 16
        elif rad > -1.9371:
            return 17
        elif rad > -2.4398:
            return 18
        elif rad > -2.8315:
            return 20
        elif rad > -3.0752:
            return 22
        else:  # rad >= -3.1415:
            return 24
