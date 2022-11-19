import pico2d
import game_world
import play_state

class Map:
    mud = None

    def __init__(self, y):
        self.img = Map.mud
        self.y = y
        game_world.map_floor.append(self)

    def show(self):
        self.img.draw_to_origin(0, self.y)

    def y_move(self, y):
        self.y += y
    @staticmethod
    def create_floor():
        Map(play_state.window_size[1])
        del game_world.map_floor[0]
        print(len(game_world.map_floor))


    @staticmethod
    def load_resource():
        Map.mud = pico2d.load_image('resource\\map\\mud.png')