import func
Marine = None
Dragoon = None
import play_state
Player = [Marine, Dragoon]


MAP_FRONT, FLOOR_EFFECT, GROUND_BULLET, GROUND_OBJ, BOMB_EFFECT, GROUND_CRASH_EFFECT, GROUND_TO_AIR, FLY_OBJ, FLY_CRASH_EFFECT = range(
    9)
ground_obj = []
ground_bullet = []
ground_crash_effect = []
air_bullet = []

del_ground_obj  = []
del_ground_bullet = []
del_ground_crash_effect = []
del_air_bullet = []

objects = [ground_bullet, ground_obj, ground_crash_effect, air_bullet]

def all_objects():
    for layer in objects:
        for o in layer:
            yield o

def set_clean_list():
    global del_ground_obj, del_ground_bullet, del_ground_crash_effect, del_air_bullet
    del_ground_obj = []
    del_ground_bullet = []
    del_ground_crash_effect = []
    del_air_bullet = []

def update_game_world():
    update_bullet()# 총알들 먼저
    update_air_bullet()# 총알들 먼저
    update_ground_obj()
    update_ground_crash_effect()



def update_bullet():
    for i in range(len(ground_bullet)):  # 적들
        blt = ground_bullet[i]
        blt.update()
        if not blt.exist:
            del_ground_bullet.append(i)

def update_ground_obj():
    ground_obj.sort(key=lambda x: x.stand_y, reverse=True)
    for i in range(len(ground_obj)): # 주인공과 지상 적 유닛, 이펙트
        em = ground_obj[i]
        if not em.exist:  #
            del_ground_obj.append(i)
        else:
            em.update() # 총알들이 먼저 업데이트 되므로 여기서 해도 됨
            for other in ground_obj:
                func.cheak_collision_min_move(em, other)

def update_ground_crash_effect():
    for i in range(len(ground_crash_effect)):
        eft = ground_crash_effect[i]
        eft.update()
        if not eft.exist:  #
            del_ground_crash_effect.append(i)

def update_air_bullet():
    for i in range(len(air_bullet)):
        ablt = air_bullet[i]
        ablt.update()
        if not ablt.exist:  #
            del_air_bullet.append(i)

def clean_objects():
    del_ground_bullet.sort(reverse=True)
    for i in del_ground_bullet:
        del ground_bullet[i]

    del_air_bullet.sort(reverse=True)
    for i in del_air_bullet:
        del air_bullet[i]

    del_ground_obj.sort(reverse=True)
    for i in del_ground_obj:
        ground_obj[i].die()
        del ground_obj[i]

    del_ground_crash_effect.sort(reverse=True)
    for i in del_ground_crash_effect:
        del ground_crash_effect[i]










# def add_object(o, depth = 0):
#     objects[depth].append(o)
#
# def add_objects(ol, depth = 0):# 객체 여러개(리스트인채로) 추가
#     objects[depth] += ol
#
# def remove_enemy(o):
#     for layer in enemies:
#         if o in layer:
#             layer.remove(o)
#             del o
#             return
#     print('없')