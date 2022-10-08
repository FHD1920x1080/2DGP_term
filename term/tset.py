from pico2d import *
import math
open_canvas()
head = load_image('head.png')
leg = load_image('leg.png')

x = 400
y = 300

#76 76
while True:
    for f in range(0,10):
        clear_canvas()
        #leg.clip_draw(76 * 8, 760 - 76 - 76 * f, 76, 76, x, y)
        #head.clip_draw(76 * 8, 760 - 76 - 76 * f, 76, 76, x, y)
        head.clip_draw(76 * 0, 760 - 76 - 76 * 7, 76, 76, x, y)
        update_canvas()
        delay(0.05)
        head.clip_draw(76 * 0, 760 - 76 - 76 * 9, 76, 76, x, y)
        update_canvas()
        delay(0.05)
        print(f)

close_canvas()