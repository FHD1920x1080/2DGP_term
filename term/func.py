import math
import game_world

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
    if (a.x >= b.hit_x - b.hit_sx / 2) and (a.x <= b.hit_x + b.hit_sx / 2) and (a.y >= b.hit_y - b.hit_sy / 2) and (
            a.y <= b.hit_y + b.hit_sy / 2):
        return True
    else:
        return False


def cheak_collision(unit1, unit2):
    if unit1 == unit2:
        return False
    left = unit1.get_left() - unit2.get_right()
    right = unit2.get_left() - unit1.get_right()

    bottom = unit1.get_bottom() - unit2.get_top()
    top = unit2.get_bottom() - unit1.get_top()

    if right <= 0 and left <= 0 and top <= 0 and bottom <= 0:
        if right >= left and right >= top and right >= bottom:
            unit1.x_move(right)
        elif left >= right and left >= top and left >= bottom:
            unit1.x_move(-left)
        elif top >= right and top >= left and top >= bottom:
            unit1.y_move(top)
        else:
            unit1.y_move(-bottom)
        return True
    return False


def move_enemy_list():
    for em in game_world.enemy_list():  # 적들
        if em.move() == 1:
            game_world.remove_enemy(em)
def show_enemy_list():
    for de in game_world.die_list:
        de.show()
    for em in game_world.enemy_list():
        em.show()

def get_rad(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)