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
    def __init__(self):
        self.Marine_shoot = False
        self.Marine_hit = False
        self.Zergling_die = False
        self.Zealot_die = False

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


def cheak_collision(unit1, unit2):
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


def move_enemy_list():
    for em in game_world.enemy_list():  # 적들
        if em.move() == 1:
            game_world.remove_enemy(em)
        for other in game_world.enemy_list():
            cheak_collision(em, other)
        cheak_collision(em, play_state.player)


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
