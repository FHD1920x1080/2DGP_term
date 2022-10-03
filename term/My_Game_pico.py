from pico2d import *

import random

# 1. 게임 초기화
window_size = [400, 900]
open_canvas(window_size[0], window_size[1])


# 2. 게임창 옵션 설정

# 3. 게임 내 필요한 설정
class Obj:
    def __init__(self):
        self.x, self.y = 0, 0  # 좌표
        self.hit_x, self.hit_y = self.x, self.y  # 히트박스 시작 좌표인데 좌우 비대칭 아니면 필요 없는듯
        self.speed = 0

    def put_img(self, file):
        self.img = load_image(file)
        self.img_now = [0, 0]  # 스프라이트 좌표
        self.sx, self.sy = 0, 0  # 한칸 씩 자른 이미지 사이즈
        self.hit_sx, self.hit_sy = self.sx, self.sy  # 히트박스 사이즈

    def x_move(self, x):
        self.x += x
        self.hit_x += x

    def y_move(self, y):
        self.y += y
        self.hit_y += y

    def show(self):
        self.img.clip_draw(self.img_now[0], self.img_now[1], self.sx, self.sy, self.x, self.y)


class RealObj(Obj):
    def __init__(self):
        super().__init__()
        self.stand_x, self.stand_y = 0, 0  # 서있는 좌표의 중앙 그리는건 중앙점과 서있는점의 차이를 더해줌.
        self.stand_sx, self.stand_sy = 0, 0  # 유닛이 지나갈 수 있는 발판 크기
        self.look_now = 0

    def x_move(self, x):
        self.x += x
        self.stand_x += x
        self.hit_x += x

    def y_move(self, y):
        self.y += y
        self.stand_y += y
        self.hit_y += y


class Marine(RealObj):
    bullet_list = []
    def __init__(self):
        super().__init__()
        self.put_img('marine250x2_blue.png')
        self.sx, self.sy = 100, 85
        self.img_now = 30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)
        self.hit_sx, self.hit_sy = 48, 72
        # marine.img = load_image('marine.png')
        # marine.re_size(48,72)
        self.stand_x = round(window_size[0] / 2)
        self.stand_y = round(self.sy / 2)
        self.x = self.stand_x
        self.y = self.stand_y + 20
        self.stand_sx = 36
        self.stand_sy = 36
        self.hit_x = self.x
        self.hit_y = self.y
        self.speed = 5
        self.left_move = False
        self.right_move = False
        self.up_move = False
        self.down_move = False
        self.shoot = False
        self.move_able = True
        self.Wmove_able = True
        self.Hmove_able = True
        self.shoot_frame = 0
        self.move_frame = 0
class Zergling(RealObj):
    sum = 0
    list = []
    die_list = []
    sx = 44
    sy = 54
    move_frame = 0
    def __init__(self, x, y):
        super().__init__()
        self.put_img("zerglingx200.png")
        self.img_now = 710, 1220-62
        self.sx = Zergling.sx
        self.sy = Zergling.sy
        self.stand_x = x
        self.stand_y = y
        self.x = self.stand_x
        self.y = self.stand_y
        self.hit_x = self.x
        self.hit_y = self.y
        self.hit_sx = self.sx
        self.hit_sy = self.sy - 20
        self.speed = 3
        self.die_frame = 0

    def die_anim(self):
        if self.die_frame == 0:
            self.sx = 128
            self.sy = 106
            self.speed = 0
            self.x += 6
        elif self.die_frame == 4:
            self.x += 2
        elif self.die_frame == 5:
            self.x -= 2
        if self.die_frame < 7:
            self.y -= 4
            self.img_now = 5 + self.die_frame * 136, 1220 - 1202
        self.die_frame += 1
    def show_All(self):
        for zg in Zergling.die_list:
            zg.show()
        for zg in Zergling.list:
            zg.show()

def crash(a, b):
    if a.hit_sx <= 0 or b.hit_sx <= 0:
        return False
    if a.hit_x + (a.hit_sx / 2) >= b.hit_x - (b.hit_sx / 2) and a.hit_x - (a.hit_sx / 2) <= b.hit_x + (
            b.hit_sx / 2) and a.hit_y + (a.hit_sy / 2) >= b.hit_y - (b.hit_sy / 2) and a.hit_y - (
            a.hit_sy / 2) <= b.hit_y + (b.hit_sy / 2):
        return True
    else:
        return False


def marien_rotate():  # 현재 이미지와 움직임을 입력할때 바뀔 이미지의 갭을 메꾸기 위한 함수 자연스럽게 회전하둣이,근데 절대 오래걸리면 안됨, 항상 0.1초가 걸리게 조절해도 됨.
    pass  # 양쪽 회전 해야할 정도를 비교해서 짧은쪽 우선, 180도 회전해야하면 항상 우회전


def handle_events():
    global shoot_frame
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
                marine.shoot_frame = 0
                marine.move_able = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                marine.left_move = False
                marine.img_now = 30 + 320 * marine.look_now, 2100
            elif event.key == SDLK_RIGHT:
                marine.right_move = False
                marine.img_now = 30 + 320 * marine.look_now, 2100
            elif event.key == SDLK_UP:
                marine.up_move = False
                marine.img_now = 30 + 320 * marine.look_now, 2100
            elif event.key == SDLK_DOWN:
                marine.down_move = False
                marine.img_now = 30 + 320 * marine.look_now, 2100
            elif event.key == SDLK_SPACE:
                marine.shoot = False
                marine.move_able = True
                marine.img_now = 30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)


def marine_move():
    if marine.move_able == True:
        if (marine.left_move == True and marine.right_move == False) or (
                marine.left_move == False and marine.right_move == True):
            marine.Wmove_able = True
        else:
            marine.Wmove_able = False
        if (marine.up_move == True and marine.down_move == False) or (
                marine.up_move == False and marine.down_move == True):
            marine.Hmove_able = True
        else:
            marine.Hmove_able = False
        if marine.Wmove_able == True and marine.Hmove_able == True:
            speed = 0.707
        else:
            speed = 1
        if marine.Wmove_able == True:
            if marine.left_move == True:
                if marine.stand_x - marine.speed * speed <= round(marine.stand_sx / 2):
                    marine.x_move(round(marine.stand_sx / 2) - marine.stand_x)
                else:
                    marine.x_move(- marine.speed * speed)
                    marine.look_now = 12
                    marine.img_now = 30 + 320 * 12, 1460 - (160 * marine.move_frame)
            else:
                if marine.stand_x + marine.speed * speed >= window_size[0] - round(marine.stand_sx / 2):
                    marine.x_move(window_size[0] - (marine.stand_x + round(marine.stand_sx / 2)))
                else:
                    marine.look_now = 4
                    marine.img_now = 30 + 320 * 4, 1460 - (160 * marine.move_frame)
                    marine.x_move(marine.speed * speed)
        if marine.Hmove_able == True:
            if marine.up_move == True:
                if marine.stand_y >= window_size[1] - round(marine.stand_sy / 2):
                    marine.y_move(window_size[1] - (marine.stand_y + round(marine.stand_sy / 2)))
                else:
                    marine.y_move(marine.speed * speed)
                    if marine.left_move == True:
                        marine.look_now = 14
                        marine.img_now = 30 + 320 * 14, 1460 - (160 * marine.move_frame)
                    elif marine.right_move == True:
                        marine.look_now = 2
                        marine.img_now = 30 + 320 * 2, 1460 - (160 * marine.move_frame)
                    else:
                        marine.look_now = 0
                        marine.img_now = 30, 1460 - (160 * marine.move_frame)
            else:
                if marine.stand_y <= round(marine.stand_sy / 2):
                    marine.y_move(round(marine.stand_sy / 2) - marine.stand_y)
                else:
                    marine.y_move(- marine.speed * speed)
                    if marine.left_move == True:
                        marine.look_now = 10
                        marine.img_now = 30 + 320 * 10, 1460 - (160 * marine.move_frame)
                    elif marine.right_move == True:
                        marine.look_now = 6
                        marine.img_now = 30 + 320 * 6, 1460 - (160 * marine.move_frame)
                    else:
                        marine.look_now = 8
                        marine.img_now = 30 + 320 * 8, 1460 - (160 * marine.move_frame)



def marine_shoot():
    if marine.shoot == True:
        if marine.shoot_frame % 6 == 0:
            marine.img_now = 30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 3)
            bullet = Obj()
            bullet.put_img("bullet_blue.png")
            bullet.sx = 9
            bullet.sy = 51
            bullet.x = marine.x + 5
            bullet.y = marine.y + 10
            bullet.hit_x = bullet.x
            bullet.hit_y = bullet.y + 22
            bullet.hit_sx = 5
            bullet.hit_sy = 2
            bullet.speed = 20
            # bullet.show()
            marine.bullet_list.append(bullet)
            #print(bullet.hit_x, bullet.hit_y, bullet.hit_sx, bullet.hit_sy)
        elif marine.shoot_frame % 6 == 3:
            marine.img_now = 30 + (2 * 160 * 0), 2180 - 80 - (1 * 160 * 2)



def make_zergling():
    if random.random() > 0.95:
        Zergling.sum+=1
        zergling = Zergling(random.randrange(round(Zergling.sx / 2), window_size[0] - round(Zergling.sx / 2)),window_size[1] + Zergling.sy)
        #zergling.put_img("zerglingx200.png")
        # bullet.show()
        Zergling.list.append(zergling)
        #print(zergling.hit_x, zergling.hit_y, zergling.hit_sx, zergling.hit_sy)
        #print(Zergling.sum)


SB = 0
FPS = 60
frame = 0
marine = Marine()
while SB == 0:
    for frame in range(0, FPS):
        # 4-1. FPS 설정
        clear_canvas()
        # delay(0.01)
        SDL_Delay(12)
        # 4-2. 각종 입력 감지
        # events = get_events()
        handle_events()
        marine_move()
        marine_shoot()
        # print(event)
        marine.shoot_frame = (marine.shoot_frame + 1) % FPS  # 0~59
        if (frame % 2 == 0):
            marine.move_frame = (marine.move_frame + 1) % 9

        Zergling.move_frame = (Zergling.move_frame + 1) % FPS
        make_zergling()

        bd_list = []
        for i in range(len(marine.bullet_list)):  # 총알 전진
            blt = marine.bullet_list[i]
            blt.y_move(blt.speed)
            if blt.y > window_size[1] + blt.sy:
                bd_list.append(i)
        for d in bd_list:
            del marine.bullet_list[d]

        zd_list = []
        for i in range(len(Zergling.list)):  # 저글링 다운
            zgl = Zergling.list[i]
            zgl.y_move(- zgl.speed)
            if zgl.y < -zgl.sy:
                zd_list.append(i)
                Zergling.sum-=1
        for d in zd_list:
            del Zergling.list[d]

        db_list = []
        dz_list = []
        for j in range(len(marine.bullet_list)):  # 충돌 체크
            for i in range(len(Zergling.list)):
                blt = marine.bullet_list[j]
                zgl = Zergling.list[i]
                if crash(zgl, blt) == True:
                    db_list.append(j)
                    blt.hit_sx = 0 #불릿 크기를 0으로 만듦
                    #zgl.hit_sx = 0 #저글링도 크기 0으로 만듦
                    Zergling.sum -= 1
                    dz_list.append(i)


        dz_list = list(set(dz_list))
        db_list = list(set(db_list))
        try:
            dz_list.reverse()
            db_list.reverse()
            for dz in dz_list:
                die_zergling = Zergling(Zergling.list[dz].stand_x, Zergling.list[dz].stand_y)
                Zergling.die_list.append(die_zergling)
                del Zergling.list[dz]
            for db in db_list:
                del marine.bullet_list[db]
        except:
            pass
        if frame % 3 == 0:
            dz2_list = []
            #print(len(Zergling.die_list))
            for i in range(len(Zergling.die_list)):
                Zergling.die_list[i].die_anim()
                if Zergling.die_list[i].die_frame > 60: #일정 시간이 지난 시체 3초
                    dz2_list.append(i)
            try:
                dz2_list.reverse()
                for dz2 in dz2_list:
                    del Zergling.die_list[dz2]
                    print(len(Zergling.die_list))
            except:
                pass
        # 4-4. 그리기
        # screen.fill(color)
        Zergling.show_All(Zergling)
        # for zg in Zergling.die_list:
        #     zg.show()
        # for zg in Zergling.list:
        #     zg.show()
        for blt in marine.bullet_list:
            blt.show()
        marine.show()
        update_canvas()

# 5. 게임 종료
close_canvas()
