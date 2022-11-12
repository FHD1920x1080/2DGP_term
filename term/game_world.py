Marine = []
Dragoon = []
Player = [Marine, Dragoon]

ground_enemy = []
sky_enemy = []
enemies = [ground_enemy, sky_enemy]
bullet_list = []
explosive_bullet_list = []
die_list = []
effect_list = []
objects = [[], [], []]

def enemy_list():
    for layer in enemies:
        for o in layer:
            yield o

def all_objects():
    for layer in objects:
        for o in layer:
            yield o
#
# def my_all_objects():
#     for o in Zergling.list:
#         yield o

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):# 객체 여러개(리스트인채로) 추가
    objects[depth] += ol

def remove_enemy(o):
    for layer in enemies:
        if o in layer:
            layer.remove(o)
            del o
            return
    print('없')