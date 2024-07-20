months_number_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


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
            if num + r[2] > months_number_days[r[1] - 1]:
                if r[1] + 1 > 12:
                    r[0] += 1
                    num -= months_number_days[r[1] - 1] - r[2]
                    r[2] = 0
                    r[1] = 1
                else:
                    v = months_number_days[r[1] - 1]
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
                    r[2] = months_number_days[r[1] - 1]
                else:
                    r[1] -= 1
                    v = months_number_days[r[1] - 1]
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


def days_range(years_months_days_splitted_0: Day, years_months_days_splitted_1: Day) -> list[Day]:
    years_months_days_splitted_0 = years_months_days_splitted_0.splitted
    years_months_days_splitted_1 = years_months_days_splitted_1.splitted
    list_0 = []
    for year in range(years_months_days_splitted_0[0], years_months_days_splitted_1[0] + 1):
        month_0 = 1
        month_1 = 12
        if year == years_months_days_splitted_0[0]:
            month_0 = years_months_days_splitted_0[1]
        if year == years_months_days_splitted_1[0]:
            month_1 = years_months_days_splitted_1[1]
        for month in range(month_0, month_1 + 1):
            day_1 = months_number_days[month - 1]
            day_0 = 1
            if year % 4 == 0 and month == 2:
                day_1 += 1
            if year == years_months_days_splitted_0[0] and month == years_months_days_splitted_0[1]:
                day_0 = years_months_days_splitted_0[2]
            if year == years_months_days_splitted_1[0] and month == years_months_days_splitted_1[1]:
                day_1 = years_months_days_splitted_1[2]
            for z in range(day_0, day_1 + 1):
                list_0.append(Day(year, month, z))
    return list_0


def greater(day0: Day, day1: Day) -> bool:
    boolean_0 = False
    if day0.splitted[0] > day1.splitted[0]:
        boolean_0 = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] > day1.splitted[1]:
            boolean_0 = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] > day1.splitted[2]:
                boolean_0 = True
    return boolean_0
    

def lower(day0: Day, day1: Day) -> bool:
    boolean_0 = False
    if day0.splitted[0] < day1.splitted[0]:
        boolean_0 = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] < day1.splitted[1]:
            boolean_0 = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] < day1.splitted[2]:
                boolean_0 = True
    return boolean_0


def greater_or_equal(day0: Day, day1: Day) -> bool:
    boolean_0 = False
    if day0.splitted[0] >= day1.splitted[0]:
        boolean_0 = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] >= day1.splitted[1]:
            boolean_0 = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] >= day1.splitted[2]:
                boolean_0 = True
    return boolean_0


def lower_or_equal(day0: Day, day1: Day) -> bool:
    boolean_0 = False
    if day0.splitted[0] <= day1.splitted[0]:
        boolean_0 = True
    elif day0.splitted[0] == day1.splitted[0]:
        if day0.splitted[1] <= day1.splitted[1]:
            boolean_0 = True
        elif day0.splitted[1] == day1.splitted[1]:
            if day0.splitted[2] <= day1.splitted[2]:
                boolean_0 = True
    return boolean_0


def where(obj: Day, dates: list[Day]):
    x = -1
    for c in range(0, len(dates)):
        if dates[c].day == obj.day:
            x = c
            break
    return x
