from dates import Day


def read_csv(path: str) -> tuple[list[str], list[list[str]], list[list[str]]]:
    with open(path, 'r') as a:
        txt = a.read().split('\n')
        a.close()
        dates = txt[0].split(',')[2:]
        data = []
        p = []
        for c in range(1, len(txt)):
            data.append(txt[c].split(',')[2:])
            p.append(txt[c].split(',')[0:2])
        return dates, data, p


def write_csv(path: str, dates: list[Day], data: list[list[int]], profiles: list[list[str]]):
    with open(path, 'w') as a:
        a.write(',photos,')
        for c in range(0, len(dates)):
            a.write(dates[c].day)
            if not c == len(dates) - 1:
                a.write(',')
            elif c == len(dates) - 1:
                a.write('\n')
        for c in range(0, len(data)):
            a.write(profiles[c][0] + ',' + profiles[c][1] + ',')
            for y in range(0, len(data[c])):
                a.write(str(data[c][y]))
                if y < len(data[c]) - 1:
                    a.write(',')
            a.write('\n')
