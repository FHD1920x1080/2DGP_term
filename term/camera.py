import game_world
import play_state

center_y = None


def enter():
    global center_y
    center_y = play_state.window_size[1] / 2 - 100


def moving():
    global center_y
    gap_y = center_y - play_state.player.stand_y
    if gap_y < 0:
        play_state.player.y_move(gap_y)
        game_world.ground_obj.remove(play_state.player)
        for ob in game_world.all_objects():
            ob.y_move(gap_y)
        game_world.ground_obj.append(play_state.player)