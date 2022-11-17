from pico2d import*


open_canvas()
img = load_image('gol_face.png')
while True:
    clear_canvas()
    img.draw_to_origin(400, 300)
    update_canvas()
close_canvas()