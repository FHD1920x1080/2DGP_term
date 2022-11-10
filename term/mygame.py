import pico2d
import game_framework
import play_state

pico2d.open_canvas(play_state.window_size[0], play_state.window_size[1], sync=True)#,full=True)
game_framework.run(play_state)
pico2d.clear_canvas()