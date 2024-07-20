months_number_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Day:
    def __init__(self, year: int, month: int, day: int):
        self.splitted = [year, month, day]
        if day < 10:
            day = '0' + str(day)
        if month < 10:
            month = '0' + str(month)
        self.day = f'{year}-{month}-{day}'

    def __add__(self, int_for_addition: int):
        day_splitted = self.splitted
        boolean_0 = False
        while True:
            if int_for_addition + day_splitted[2] > months_number_days[day_splitted[1] - 1]:
                if day_splitted[1] + 1 > 12:
                    day_splitted[0] += 1
                    int_for_addition -= months_number_days[day_splitted[1] - 1] - day_splitted[2]
                    day_splitted[2] = 0
                    day_splitted[1] = 1
                else:
                    v = months_number_days[day_splitted[1] - 1]
                    if day_splitted[0] % 4 == 0 and day_splitted[1] == 2:
                        v += 1
                    int_for_addition -= v - day_splitted[2]
                    day_splitted[1] += 1
                    day_splitted[2] = 0
            else:
                day_splitted[2] += int_for_addition
                boolean_0 = True
            if boolean_0:
                break
        return Day(day_splitted[0], day_splitted[1], day_splitted[2])

    def __sub__(self, num: int):
        day_splitted = self.splitted
        boolean_0 = False
        while True:
            if day_splitted[2] - num < 1:
                if day_splitted[1] - 1 < 1:
                    day_splitted[0] -= 1
                    day_splitted[1] = 12
                    num -= day_splitted[2]
                    day_splitted[2] = months_number_days[day_splitted[1] - 1]
                else:
                    day_splitted[1] -= 1
                    v = months_number_days[day_splitted[1] - 1]
                    if day_splitted[1] == 2 and day_splitted[0] % 4 == 0:
                        v += 1
                    num -= day_splitted[2]
                    day_splitted[2] = v
            else:
                day_splitted[2] -= num
                boolean_0 = True
            if boolean_0:
                break
        return Day(day_splitted[0], day_splitted[1], day_splitted[2])


class Month:
    def __init__(self, year: int, month: int):
        self.splitted = [year, month]
        if month > 9:
            self.month = f'{year}-{month}'
        elif month < 10:
            self.month = f'{year}-0{month}'

    def __add__(self, int_for_addition: int):
        month_splitted = self.splitted
        while True:
            if month_splitted[1] + int_for_addition > 12:
                month_splitted[0] += 1
                int_for_addition -= 12 - month_splitted[1]
                month_splitted[1] = 1
            else:
                break
        return month_splitted

    def __sub__(self, int_for_subtraction: int):
        r = self.splitted
        while True:
            if r[1] - int_for_subtraction < 1:
                r[0] -= 1
                int_for_subtraction -= r[1]
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
