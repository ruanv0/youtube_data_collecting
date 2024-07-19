m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Day:
    def __init__(self, year: int, month: int, day: int):
        self.splitted = [year, month, day]
        if day < 10:
            day = '0' + str(day)
        if month < 10:
            month = '0' + str(month)
        self.day = f'{year}-{month}-{day}'

    def __add__(self, num: int):
        r = self.splitted
        c = False
        while True:
            if num + r[2] > m[r[1] - 1]:
                if r[1] + 1 > 12:
                    r[0] += 1
                    num -= m[r[1] - 1] - r[2]
                    r[2] = 0
                    r[1] = 1
                else:
                    v = m[r[1] - 1]
                    if r[0] % 4 == 0 and r[1] == 2:
                        v += 1
                    num -= v - r[2]
                    r[1] += 1
                    r[2] = 0
            else:
                r[2] += num
                c = True
            if c:
                break
        return Day(r[0], r[1], r[2])

    def __sub__(self, num: int):
        r = self.splitted
        c = False
        while True:
            if r[2] - num < 1:
                if r[1] - 1 < 1:
                    r[0] -= 1
                    r[1] = 12
                    num -= r[2]
                    r[2] = m[r[1] - 1]
                else:
                    r[1] -= 1
                    v = m[r[1] - 1]
                    if r[1] == 2 and r[0] % 4 == 0:
                        v += 1
                    num -= r[2]
                    r[2] = v
            else:
                r[2] -= num
                c = True
            if c:
                break
        return Day(r[0], r[1], r[2])


class Month:
    def __init__(self, year: int, month: int):
        self.splitted = [year, month]
        if month > 9:
            self.month = f'{year}-{month}'
        elif month < 10:
            self.month = f'{year}-0{month}'

    def __add__(self, other: int):
        r = self.splitted
        while True:
            if r[1] + other > 12:
                r[0] += 1
                other -= 12 - r[1]
                r[1] = 1
            else:
                break
        return r

    def __sub__(self, other: int):
        r = self.splitted
        while True:
            if r[1] - other < 1:
                r[0] -= 1
                other -= r[1]
                r[1] = 12
            else:
                break
        return r


def lrange(d0: Day, d1: Day) -> list[Day]:
    d0 = d0.splitted
    d1 = d1.splitted
    lista = []
    for x in range(d0[0], d1[0] + 1):
        me = 1
        mi = 12
        if x == d0[0]:
            me = d0[1]
        if x == d1[0]:
            mi = d1[1]
        for y in range(me, mi + 1):
            v1 = m[y - 1]
            v0 = 1
            if x % 4 == 0 and y == 2:
                v1 += 1
            if x == d0[0] and y == d0[1]:
                v0 = d0[2]
            if x == d1[0] and y == d1[1]:
                v1 = d1[2]
            for z in range(v0, v1 + 1):
                lista.append(Day(x, y, z))
    return lista


def sub_dates(day0: Day, day1: Day) -> int:
    x = 0
    if day1.splitted[0] > day0.splitted[0]:
        x = 1
    elif day1.splitted[0] == day0.splitted[0]:
        if day1.splitted[1] > day0.splitted[1]:
            x = 1
        elif day1.splitted[1] == day0.splitted[1]:
            if day1.splitted[2] > day0.splitted[2]:
                x = 1
    if x == 0:
        return len(lrange(day1, day0)) - 1
    elif x == 1:
        return len(lrange(day0, day1)) - 1


def greater(day0: Day, day1: Day) -> bool:
    x = False
    if day0.splitted[0] > day1.splitted[0]:
        x = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] > day1.splitted[1]:
            x = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] > day1.splitted[2]:
                x = True
    return x
    

def lower(day0: Day, day1: Day) -> bool:
    x = False
    if day0.splitted[0] < day1.splitted[0]:
        x = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] < day1.splitted[1]:
            x = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] < day1.splitted[2]:
                x = True
    return x


def greater_or_equal(day0: Day, day1: Day) -> bool:
    x = False
    if day0.splitted[0] >= day1.splitted[0]:
        x = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] >= day1.splitted[1]:
            x = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] >= day1.splitted[2]:
                x = True
    return x


def lower_or_equal(day0: Day, day1: Day) -> bool:
    x = False
    if day0.splitted[0] <= day1.splitted[0]:
        x = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] <= day1.splitted[1]:
            x = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] <= day1.splitted[2]:
                x = True
    return x


def where(obj: Day, dates: list[Day]):
    x = -1
    for c in range(0, len(dates)):
        if dates[c].day == obj.day:
            x = c
            break
    return x
