import math
import game_world
import play_state
import ui

class User_input:
    left_key = False  # 왼쪽으로 가는키가 눌렸는지
    right_key = False
    up_key = False
    down_key = False
    left_button = False
    right_button = False


def dummy_func():
    pass


def crash(a, b):
    if a.hit_sx <= 0 or b.hit_sx <= 0:
        return False
    if a.hit_x + (a.hit_sx / 2) >= b.hit_x - (b.hit_sx / 2) and a.hit_x - (a.hit_sx / 2) <= b.hit_x + (
            b.hit_sx / 2) and a.hit_y + (a.hit_sy / 2) >= b.hit_y - (b.hit_sy / 2) and a.hit_y - (
            a.hit_sy / 2) <= b.hit_y + (b.hit_sy / 2):
        return True
    else:
        return False


def bullet_crash(bullet, obj):
    if bullet.exist == False or obj.collision == False:
        return False

    if bullet.x < obj.hit_x() - obj.hit_sx:
        return False
    if bullet.x > obj.hit_x() + obj.hit_sx:
        return False
    if bullet.y < obj.hit_y() - obj.hit_sy:
        return False
    if bullet.y > obj.hit_y() + obj.hit_sy:
        return False

    return True


def tir_rect_crash(bullet, unit):
    if unit.collision == False:
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
    if unit1.collision == False or unit2.collision == False:
        return False

    bottom = unit1.get_stand_bottom() - unit2.get_stand_top()
    if bottom > 0:
        return False
    max = bottom
    top = unit2.get_stand_bottom() - unit1.get_stand_top()
    if top > 0:
        return False
    if max < top:
        max = top
    left = unit1.get_stand_left() - unit2.get_stand_right()
    if left > 0:
        return False
    if max < left:
        max = left
    right = unit2.get_stand_left() - unit1.get_stand_right()
    if right > 0:
        return False
    if max < right:
        max = right

    # if unit1 == unit2:
    #     return False

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
    game_world.ground_obj.remove(play_state.player)
    if key == 1:
        if play_state.sub_unit1 == game_world.Marine:
            play_state.sub_unit1, play_state.player = play_state.player, play_state.sub_unit1
        else:
            play_state.sub_unit2, play_state.player = play_state.player, play_state.sub_unit2
        play_state.player.shoot_frame = 0  # 연사력과, 점사구현을 위한 프레임
        play_state.player.move_frame = 0  # 마린의 걸어다니는 애니메이션을 위한 프레임
        play_state.player.idle_frame = 0  # 아무것도 안한 시간만큼의 프레임
        play_state.player.shoot_able = False
        play_state.player.move_able = True
        play_state.player.dash_state = False
        if User_input.left_button:
            if play_state.player.magazine_gun:
                play_state.player.shoot_frame = 0
                play_state.player.shoot_able = True
                if not play_state.player.moving_attack:
                    play_state.player.move_able = False
    elif key == 2:
        if play_state.sub_unit1 == game_world.Goliath:
            play_state.sub_unit1, play_state.player = play_state.player, play_state.sub_unit1
        else:
            play_state.sub_unit2, play_state.player = play_state.player, play_state.sub_unit2
        play_state.player.state = 1
        play_state.player.shoot_state = False
        if User_input.left_button:
            play_state.player.shoot_state = True
    elif key == 3:
        if play_state.sub_unit1 == game_world.Dragoon:
            play_state.sub_unit1, play_state.player = play_state.player, play_state.sub_unit1
        else:
            play_state.sub_unit2, play_state.player = play_state.player, play_state.sub_unit2
        play_state.player.state = 1
        if User_input.left_button:
            if play_state.player.state < 3:
                play_state.player.bull_x2, play_state.player.bull_y2 = play_state.cursor.x, play_state.cursor.y
                play_state.player.open_frame = 0
                play_state.player.state = 3
    play_state.player.x_move_point(sx)
    play_state.player.y_move_point(sy)
    game_world.ground_obj.append(play_state.player)
    ui.UI.warning_frame = 0
    ui.UI.warning_img_now = 0


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
