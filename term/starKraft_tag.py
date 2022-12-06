import pico2d
import game_framework
import play_state
import title_state
#STARㅋRAFT_TAG
#pico2d.open_canvas(play_state.window_size[0], play_state.window_size[1])
pico2d.open_canvas(play_state.window_size[0], play_state.window_size[1], sync=False, full=True)
game_framework.run(title_state)
pico2d.close_canvas()