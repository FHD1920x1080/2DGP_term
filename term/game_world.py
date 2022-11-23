import func

Marine = None
Dragoon = None
import play_state

Player = [Marine, Dragoon]

MAP_FLOOR, FLOOR_EFFECT, GROUND_BULLET, GROUND_OBJ, BOMB_EFFECT, GROUND_CRASH_EFFECT, AIR_BULLET, FLY_OBJ, AIR_CRASH_EFFECT = range(
    9)

map_floor = []
floor_effect = []
ground_bullet = []
ground_obj = []
bomb_effect = []
ground_crash_effect = []
air_bullet = []
fly_obj = []
air_crash_effect = []

del_map_floor = []
del_floor_effect = []
del_ground_bullet = []
del_ground_obj = []
del_bomb_effect = []
del_ground_crash_effect = []
del_air_bullet = []
del_fly_obj = []
del_air_crash_effect = []
#밑에 있는 set_clean_list()에 꼭 등록 해주어야함

objects = [map_floor, floor_effect, ground_bullet, ground_obj, bomb_effect, ground_crash_effect, air_bullet, fly_obj, air_crash_effect]


def all_objects():
    for layer in objects:
        for o in layer:
            yield o


def set_clean_list():
    global del_ground_obj, del_ground_bullet, del_ground_crash_effect, del_bomb_effect, del_air_bullet, del_floor_effect, del_fly_obj, del_air_crash_effect
    del_floor_effect = []
    del_ground_bullet = []
    del_ground_obj = []
    del_bomb_effect = []
    del_ground_crash_effect = []
    del_air_bullet = []
    del_fly_obj = []
    del_air_crash_effect = []

def update_game_world():
    # 여기 문제인게 생성되고 바로 update를 하는 애들과, 다음 루프때가 되어야 첫 update를 하는 애들(내가 원하는 상황)이 나뉘었음
    # 그래서 이펙트 생성하고 바로 업데이트를 하는경우, 첫번째 스프라이트 이미지가 스킵됨.
    # 그래서 이펙트를 생성해야 하는 경우는 전부 die()에서 만들어 주기로 함.
    # 그래서 이펙트들은 생성 된 후 play_state.frame이 1 올라가기 때문에 다음 루프때 수행하는 update()에서 바로 애니메이션 조건에 해당되지 않아
    # 이펙트의 첫번째 스프라이트가 스킵되는 현상을 막음.

    # 이 밑의 3개의 순서는 고정 불릿이 먼저 서로 상호작용이 있기 때문
    update_ground_bullet()  # 총알들 먼저 # 이펙트 생성, 적 유닛 존재변수 False 등 발생 가능
    update_air_bullet()  # 총알들 먼저
    update_ground_obj()  # 아직 시체를 만들이 않고 존재변수만 0으로 만듦, 시체는 claen 되는 순간에 자신의 die()에서 만들고 자신의 존재를 지움
    update_fly_obj()

    update_ground_crash_effect()
    update_floor_effect()
    update_bomb_effect()
    update_air_crash_effect()


def update_floor_effect():
    for i in range(len(floor_effect)):  # 바닥에 남아있는 시체, 효과
        eft = floor_effect[i]
        eft.update()
        if not eft.exist:
            del_floor_effect.insert(0, i)


def update_ground_bullet():
    for i in range(len(ground_bullet)):  # 마린 이 지상 유닛에게 쏘는 총알
        blt = ground_bullet[i]
        blt.update()
        if not blt.exist:
            del_ground_bullet.insert(0, i)


def update_bomb_effect():
    for i in range(len(bomb_effect)):
        eft = bomb_effect[i]
        eft.update()
        if not eft.exist:
            del_bomb_effect.insert(0, i)


def update_ground_obj():
    ground_obj.sort(key=lambda o: o.stand_y, reverse=True)
    length = len(ground_obj)
    for i in range(length):  # 주인공과 지상 적 유닛, 이펙트
        obj = ground_obj[i]
        if not obj.exist:
            del_ground_obj.insert(0, i)
        else:
            obj.update()  # 총알들이 먼저 업데이트 되므로 여기서 해도 됨
            first = max(i - 14, 0)
            last = min(i + 14, length)
            for j in range(first, i):
                other = ground_obj[j]
                func.cheak_collision_min_move(obj, other)
            for j in range(i+1, last):
                other = ground_obj[j]
                func.cheak_collision_min_move(obj, other)


def update_ground_crash_effect():
    for i in range(len(ground_crash_effect)):
        eft = ground_crash_effect[i]
        eft.update()
        if not eft.exist:
            del_ground_crash_effect.insert(0, i)


def update_air_bullet():
    for i in range(len(air_bullet)):
        ablt = air_bullet[i]
        ablt.update()
        if not ablt.exist:  #
            del_air_bullet.insert(0, i)

def update_fly_obj():
    for i in range(len(fly_obj)):
        obj = fly_obj[i]
        obj.update()
        if not obj.exist:
            del_fly_obj.insert(0, i)

def update_air_crash_effect():
    for i in range(len(air_crash_effect)):
        eft = air_crash_effect[i]
        eft.update()
        if not eft.exist:
            del_air_crash_effect.insert(0, i)

def clean_objects():  # 얘네는 별도의 레이어이며 리스트이기 때문에 지우는 순서는 상관 없음.
    for i in del_ground_bullet:  # 먼저 넣은걸 뒤로 미는 insert를 했기 때문에 정렬 필요없이, 뒷쪽 인덱스부터 접근 가능->
        ground_bullet[i].die()
        del ground_bullet[i]  # 뒤에것들부터 지울 수 있음. 뒤에것부터 지우지 않으면 반복문 도는 동안 엉뚱한게 지워짐.

    for i in del_air_bullet:
        air_bullet[i].die()
        del air_bullet[i]

    for i in del_ground_obj:
        ground_obj[i].die()
        del ground_obj[i]

    for i in del_fly_obj:
        fly_obj[i].die()
        del fly_obj[i]

    for i in del_ground_crash_effect:
        del ground_crash_effect[i]

    for i in del_floor_effect:
        del floor_effect[i]

    for i in del_bomb_effect:
        del bomb_effect[i]

    for i in del_air_crash_effect:
        del air_crash_effect[i]

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
