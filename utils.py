from dates import lrange, Day, where, lower_or_equal, greater


def add9(dates: list[Day], data: list[int]) -> tuple[list[Day], list[int]]:
    a = lrange(dates[0], dates[-1])
    for i in range(0, len(a)):
        if a[i].day != dates[i].day:
            data.insert(i, 999999999999999)
            dates.insert(i, Day(*a[i].splitted))
    return dates, data


def interpolate_9(list_0: list[int]) -> list[int]:
    nines = 999999999999999
    boolean_0 = False
    boolean_1 = False
    counter = 0
    for index, object in enumerate(list_0):
        if object == 999999999999999:
            if not boolean_0:
                nines = index-1
                boolean_0 = True
            if index == len(list_0)-1:
                if counter == 0:
                    counter = list_0[nines] - list_0[nines - 1]
                for number in range(nines+1, index+1):
                    list_0[number] = list_0[number - 1] + list_0[number - 1] - list_0[number - 2]
                    boolean_0 = False
                    boolean_1 = False
        if boolean_0 and object != 999999999999999:
            boolean_1 = True
        if boolean_1:
            counter = list_0[index] - list_0[nines]
            f = counter / (index - nines)
            for number in range(nines + 1, index):
                list_0[number] = list_0[nines] + int(f * (number - nines))
                boolean_0 = False
                boolean_1 = False
    return list_0


def join_dates_values(dates_0: list[Day], dates_1: list[Day], values_0: list[int], values_1: list[int]) -> tuple[list[Day], list[int]]:
    united_dates = []
    united_values = []
    dates_0_with_nines = add9(dates_0, values_0)
    dates_1_with_nines = add9(dates_1, values_1)
    dates_0 = dates_0_with_nines[0]
    values_0 = interpolate_9(dates_0_with_nines[1])
    dates_1 = dates_1_with_nines[0]
    values_1 = interpolate_9(dates_1_with_nines[1])
    if lower_or_equal(dates_0[0], dates_1[0]) & lower_or_equal(dates_1[0], dates_0[-1]) & lower_or_equal(dates_0[-1], dates_1[-1]):
        united_dates = lrange(dates_0[0], dates_1[-1])
        i = where(dates_1[0], dates_0)
        united_values = values_0[:i] + values_1
    elif lower_or_equal(dates_1[0], dates_0[0]) & lower_or_equal(dates_0[0], dates_1[-1]) & lower_or_equal(dates_1[-1], dates_0[-1]):
        united_dates = lrange(dates_1[0], dates_0[-1])
        i = where(dates_0[0], dates_1)
        united_values = values_1[:i] + values_0
    elif greater(dates_1[-1], dates_0[0]):
        united_dates = lrange(dates_0[0], dates_1[-1])
        united_values = values_0 + values_1
        for i in range(0, len(united_dates) - len(united_values)):
            united_values.insert(len(values_0) + i, 999999999999999)
        united_values = interpolate_9(united_values)
    elif greater(dates_0[-1], dates_1[0]):
        united_dates = lrange(dates_1[0], dates_0[-1])
        united_values = values_1 + values_0
        for i in range(0, len(united_dates) - len(united_values)):
            united_values.insert(len(values_0) + i, 999999999999999)
        united_values = interpolate_9(united_values)
    return united_dates, united_values


def fix_value(value: str) -> int:
    if '--\n' in value:
        value = value[3:]
    if 'K' in value:
        if '.' in value:
            if len(value) == 4:
                value = value.replace('.', '').replace('K', '00')
            elif '.' in value[1] and len(value) == 5:
                value = value.replace('.', '').replace('K', '0')
            elif '.' in value[2] and len(value) == 5:
                value = value.replace('.', '').replace('K', '00')
        else:
            value = value.replace('.', '').replace('K', '000')
    if 'M' in value:
        if '.' in value:
            if value[2] == '.':
                value = value.replace('.', '').replace('M', '00000')
            elif value[1] == '.':
                if len(value) == 5:
                    value = value.replace('.', '').replace('M', '0000')
                elif len(value) == 4:
                    value = value.replace('.', '').replace('M', '00000')
        else:
            value = value.replace('M', '000000')
    return int(value)
