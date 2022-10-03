def handle_events():
    global SB
    for event in get_events():
        if event.type == SDL_QUIT:
            SB = 1
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                marine.left_move = True
            elif event.key == SDLK_RIGHT:
                marine.right_move = True
            elif event.key == SDLK_UP:
                marine.up_move = True
            elif event.key == SDLK_DOWN:
                marine.down_move = True
            elif event.key == SDLK_SPACE:
                marine.shoot = True
                shoot_frame = 0
                # marine.move_able = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                marine.left_move = False
            elif event.key == SDLK_RIGHT:
                marine.right_move = False
            elif event.key == SDLK_UP:
                marine.up_move = False
            elif event.key == SDLK_DOWN:
                marine.down_move = False
            elif event.key == SDLK_SPACE:
                marine.shoot = False
                marine.move_able = True