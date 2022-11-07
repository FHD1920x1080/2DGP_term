import play_state


gap_x = None
gap_y = None
center_x = None
center_y = None

def enter():
    global center_x, center_y
    center_x = play_state.window_size[0] / 2
    center_y = play_state.window_size[1] / 2 - 100




def camera():
    global gap_x, gap_y
    gap_x = center_x - play_state.Marine.list[0].stand_x
    gap_y = center_y - play_state.Marine.list[0].stand_y

    #마린은 센터로 보내고
    #다른 모든 오브젝트는 gap만큼 이동
    play_state.Marine.list[0].x_move(gap_x)
    play_state.Marine.list[0].y_move(gap_y)
    b_list = play_state.Marine.list[0].bullet_list
    for b in b_list:
        b.x_move(gap_x)
        b.y_move(gap_y)
    for z in play_state.Zergling.list:
        z.x_move(gap_x)
        z.y_move(gap_y)
    for z in play_state.Die_Zergling.list:
        z.x_move(gap_x)
        z.y_move(gap_y)