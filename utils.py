from dates import lrange, Day, where, lower_or_equal, greater


def add9(dates: list[Day], data: list[int]) -> tuple[list[Day], list[int]]:
    a = lrange(dates[0], dates[-1])
    for i in range(0, len(a)):
        if a[i].day != dates[i].day:
            data.insert(i, 999999999999999)
            dates.insert(i, Day(*a[i].splitted))
    return dates, data


def orgli(alist: list[int]) -> list[int]:
    la = 999999999999999
    k = False
    j = False
    n = 0
    for i, y in enumerate(alist):
        if y == 999999999999999:
            if not k:
                la = i-1
                k = True
            if i == len(alist)-1:
                if n == 0:
                    n = alist[la] - alist[la - 1]
                for jkh in range(la+1, i+1):
                    alist[jkh] = alist[jkh-1] + alist[jkh-1] - alist[jkh-2]
                    k = False
                    j = False
        if k and y != 999999999999999:
            j = True
        if j:
            n = alist[i] - alist[la]
            f = n / (i - la)
            for jkh in range(la + 1, i):
                alist[jkh] = alist[la] + int(f * (jkh - la))
                k = False
                j = False
    return alist


def orglist(dates1: list[Day], dates2: list[Day], data1: list[int], data2: list[int]) -> tuple[list[Day], list[int]]:
    dates0 = []
    data0 = []
    a = add9(dates1, data1)
    b = add9(dates2, data2)
    dates1 = a[0]
    data1 = orgli(a[1])
    dates2 = b[0]
    data2 = orgli(b[1])
    if lower_or_equal(dates1[0], dates2[0]) & lower_or_equal(dates2[0], dates1[-1]) & lower_or_equal(dates1[-1], dates2[-1]):
        dates0 = lrange(dates1[0], dates2[-1])
        i = where(dates2[0], dates1)
        data0 = data1[:i] + data2
    elif lower_or_equal(dates2[0], dates1[0]) & lower_or_equal(dates1[0], dates2[-1]) & lower_or_equal(dates2[-1], dates1[-1]):
        dates0 = lrange(dates2[0], dates1[-1])
        i = where(dates1[0], dates2)
        data0 = data2[:i] + data1
    elif greater(dates2[-1], dates1[0]):
        dates0 = lrange(dates1[0], dates2[-1])
        data0 = data1 + data2
        for i in range(0, len(dates0) - len(data0)):
            data0.insert(len(data1) + i, 999999999999999)
        data0 = orgli(data0)
    elif greater(dates1[-1], dates2[0]):
        dates0 = lrange(dates2[0], dates1[-1])
        data0 = data2 + data1
        for i in range(0, len(dates0) - len(data0)):
            data0.insert(len(data1) + i, 999999999999999)
        data0 = orgli(data0)
    return dates0, data0


def exn(jf: str) -> int:
    if '--\n' in jf:
        jf = jf[3:]
    if 'K' in jf:
        if '.' in jf:
            if len(jf) == 4:
                jf = jf.replace('.', '').replace('K', '00')
            elif '.' in jf[1] and len(jf) == 5:
                jf = jf.replace('.', '').replace('K', '0')
            elif '.' in jf[2] and len(jf) == 5:
                jf = jf.replace('.', '').replace('K', '00')
        else:
            jf = jf.replace('.', '').replace('K', '000')
    if 'M' in jf:
        if '.' in jf:
            if jf[2] == '.':
                jf = jf.replace('.', '').replace('M', '00000')
            elif jf[1] == '.':
                if len(jf) == 5:
                    jf = jf.replace('.', '').replace('M', '0000')
                elif len(jf) == 4:
                    jf = jf.replace('.', '').replace('M', '00000')
        else:
            jf = jf.replace('M', '000000')
    return int(jf)
