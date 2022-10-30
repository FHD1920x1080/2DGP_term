
class obj1:
    def __init__(self):
        self.x = 1
        self.y = 1

class obj2:
    def __init__(self):
        self.x = 2
        self.y = 2

a_list = []

b_list = []
def append_list():
    ob1 = obj1()
    a_list.append(ob1)
    b_list.append(ob1)

append_list()
print(a_list[0].x)
print(b_list[0].x)
del b_list[0]
print(a_list[0].x)
#print(b_list[0].x)