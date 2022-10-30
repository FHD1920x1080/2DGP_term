from obj_class.obj import*
from func import*
import play_state
import random
import math

class Bullet_anim:
    def __init__(self):
        self.frame = random.randint(0, 4)
        self.x, self.y = 0, 0  # 좌표
        self.x1, self.y1 = 0, 0  # 좌표
        self.x2, self.y2 = 0, 0  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.speed = 5
        self.t = 0

    def put_img(self, file):
        self.img = load_image(file)
        self.img_now = [0, 0]  # 스프라이트 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈

    def move(self):
        i = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** (1 / 2)
        self.t += 1 * (self.speed / i)
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)

    def add_hit_size(self, x, y):
        self.hit_sx, self.hit_sy = x, y

    def anim(self):
        self.img_now[0] = self.frame * self.sx
        self.frame = (self.frame + 1) % 5


class Bullet_32:
    img = []
    def __init__(self, marine, x2, y2):
        self.x1, self.y1 = self.get_bullet_start(marine)  # x1, y1  # 시작 좌표
        self.x2, self.y2 = x2, y2  # 가야할 좌표, 지나치고 계속 가도 됨.
        self.x, self.y = self.x1, self.x2  # 현재 좌표
        self.speed = marine.bullet_speed  # 생성되는 곳에서 마린의 탄속으로 초기화해주고 있음.
        self.t = 0  # 브리즌헴 직선 변수
        self.r = math.dist([self.x1, self.y1], [self.x2, self.y2])  # 두 점 사이의 거리

        self.num = self.get_bullet_num(get_rad(self.x1, self.y1, self.x2, self.y2))
        self.img = Bullet_32.img[self.num]
        #self.sx, self.sy = self.get_bullet_size(self.num)
        self.exist = True #충돌 수 False로 바꿔줄 변수

    def put_img(self, file):
        self.img = load_image(file)  # 지금은 총알 하나씩 읽어들이고 있어서 크게 나쁘지 않은데, 전체 스프라이트 하나 읽고 좌표값만 바꾸는게 나은지 아직 모름.
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈


    def x_move(self, x):
        self.x += x
        self.x1 += x
        self.x2 += x

    def y_move(self, y):
        self.y += y
        self.y1 += y
        self.y2 += y

    def move(self):
        self.t += 1 * (self.speed / self.r)
        self.x = (1 - self.t) * self.x1 + self.t * self.x2
        self.y = (1 - self.t) * self.y1 + self.t * self.y2
        pass

    def show(self):
        self.img.draw(self.x, self.y)

    def get_bullet_start(self, marine):
        x, y = marine.stand_x, marine.stand_y + 14
        if marine.look_now < 10:
            x += 8
            y += 4
        elif marine.look_now > 26:
            x -= 6
            y += 4

        return x, y

    def get_bullet_num(self, rad):
        # a5625 = 0.09817477
        if rad >= 0:  # 1, 2 사분면
            if rad <= 1.7089711:  # 1사분면
                if rad > 1.40262156:  # -0.07
                    return 0
                elif rad > 1.15627201:  # -0.12
                    return 1
                elif rad > 0.89992247:  # -0.18
                    return 2
                elif rad > 0.70357293:  # -0.18
                    return 3
                elif rad > 0.50722339:  # -0.18
                    return 4
                elif rad > 0.41087385:  # -0.08
                    return 5
                elif rad > 0.29452431:
                    return 6
                elif rad > 0.09817477:
                    return 7
                else:  # >0 오른쪽
                    return 8
            else:  # 2사분면
                if rad < 1.93532064:
                    return 31
                elif rad < 2.20167018:
                    return 30
                elif rad < 2.41801972:
                    return 29
                elif rad < 2.65436926:
                    return 28
                elif rad < 2.7807188:
                    return 27
                elif rad < 2.88706834:
                    return 26
                elif rad < 3.04341788:
                    return 25
                else:  # >0 왼쪽
                    return 24
        else:  # rad < 0 3,4분면
            if rad >= -1.6689711:  # 4사분면
                if rad < -1.47262156:
                    return 16
                elif rad < -1.15627201:
                    return 15
                elif rad < -0.92992247:
                    return 14
                elif rad < -0.70357293:
                    return 13
                elif rad < -0.52722339:
                    return 12
                elif rad < -0.36087385:
                    return 11
                elif rad < -0.22452431:
                    return 10
                elif rad < -0.09817477:
                    return 9
                else:  # 오른쪽
                    return 8
            else:  # 3사분면
                if rad > -1.98532064:  # -0.12
                    return 17
                elif rad > -2.24167018:  # 18
                    return 18
                elif rad > -2.43801972:  # 18
                    return 19
                elif rad > -2.63436926:  # 18
                    return 20
                elif rad > -2.7307188:  # 08
                    return 21
                elif rad > -2.90706834:  # 06
                    return 22
                elif rad > -3.04341788:
                    return 23
                else:  # 왼쪽
                    return 24

    @staticmethod
    def move_crash_chack():
        for marine in play_state.Marine.list:
            db_list = []
            dz_list = []
            for i in range(len(marine.bullet_list)):  # 불릿을 이동 시킨 후 범위탈출 및 충돌 체크
                blt = marine.bullet_list[i]
                blt.move()
                if blt.y > play_state.window_size[1] + 60 or blt.y < - 60 or blt.x > play_state.window_size[
                    0] + 60 or blt.x < - 60:  # 지금은 화면 밖인데 나중에 벽으로 바꿀 예정, 화면 밖 멀리에 벽을 둘 예정, 또 벽에 충돌하면 먼지 이펙트같은것도 추가 예정
                    db_list.append(i)  # 총알이 범위 밖으로 나갔으니 삭제 리스트에 추가
                else:  # 나간 총알이랑은 충돌 체크 할 필요 없으니 안나간 것만 충돌체크
                    for j in range(len(play_state.Zergling.list)):
                        zgl = play_state.Zergling.list[j]
                        if bullet_crash(blt, zgl) == True:
                            attack_effect = Effect(blt.x, blt.y)
                            marine.effect_list.append(attack_effect)
                            # marine.play_hit_sound()
                            play_state.sound.Marine_hit = True
                            db_list.append(i)
                            blt.exist = False  # 아직 삭제 시킬 수 없으므로 존재변수를 0으로 함, 겹쳐있는 저글링 동시에 패는걸 막기 위해,
                            zgl.hp -= marine.AD
                            if zgl.hp <= 0:
                                play_state.Zergling.sum -= 1
                                dz_list.append(j)
                                # zgl.hit_sx = 0  # 저글링의 크기도 0으로 만듦, 동시에 여러발 흡수하느걸 막기 위해, 충돌체크 조건문에서 걸러짐 # hp 검사로 조건 바꿈
                            break  # 이제 사라진 불릿이기 때문에 다른 저글링이랑 체크 할 필요 없음
                        # elif 다른 유닛 충돌 체크 할 구문
            dz_list.sort(reverse=True)
            for dz in dz_list:
                die_zergling = play_state.Die_Zergling(play_state.Zergling.list[dz].stand_x, play_state.Zergling.list[dz].stand_y - 5)
                # die_zergling.play_sound()
                play_state.sound.Zergling_die = True
                play_state.Die_Zergling.list.append(die_zergling)  # 죽은 저글링 리스트에 추가함
                del play_state.Zergling.list[dz]  # 실제 저글링은 삭제
            db_list.sort(reverse=True)
            for db in db_list:
                del marine.bullet_list[db]  # 충돌하거나 나갔던 불릿들 삭제

class Effect(Obj):
    crash_img = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_now_y = random.randint(3, 14) * 80  # 1120  # 스프라이트 좌표
        self.frame = 0  # 100이 되면 저글링 시체 사라짐

    def anim(self):
        if self.frame < 4:
            self.img_now_y -= 80
        self.frame += 1

    def show(self):
        Effect.crash_img.clip_draw(0, self.img_now_y, 80, 80, self.x, self.y)