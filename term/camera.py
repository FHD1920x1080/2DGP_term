import game_world
import play_state
import map

center_y = None
total_y = 0
create_map_y = 0

def enter():
    global center_y, total_y, create_map_y
    center_y = play_state.window_size[1] / 2 - 100
    total_y = center_y
    create_map_y = 0
    map.Map(0)
    map.Map(play_state.window_size[1])
    print(len(game_world.map_floor))


def moving():
    global center_y, total_y, create_map_y
    gap_y = center_y - play_state.player.stand_y


    #print(total_y)
    if gap_y < 0:
        total_y -= gap_y
        create_map_y -= gap_y
        if create_map_y >= play_state.window_size[1]:
            create_map_y -= play_state.window_size[1]
            map.Map.create_floor()
        for ob in game_world.all_objects():
            ob.y_move(gap_y)