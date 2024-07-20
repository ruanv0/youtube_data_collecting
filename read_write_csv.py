from dates import Day


def read_csv(path: str) -> tuple[list[str], list[list[str]], list[list[str]]]:
    with open(path, 'r') as file:
        text = file.read().split('\n')
        file.close()
        dates = text[0].split(',')[2:]
        data = []
        images_links = []
        for index_ in range(1, len(text)):
            data.append(text[index_].split(',')[2:])
            images_links.append(text[index_].split(',')[0:2])
        return dates, data, images_links


def write_csv(path: str, dates: list[Day], data: list[list[int]], images_links: list[list[str]]):
    with open(path, 'w') as file:
        file.write(',photos,')
        for index_0 in range(0, len(dates)):
            file.write(dates[index_0].day)
            if not index_0 == len(dates) - 1:
                file.write(',')
            elif index_0 == len(dates) - 1:
                file.write('\n')
        for index_0 in range(0, len(data)):
            file.write(images_links[index_0][0] + ',' + images_links[index_0][1] + ',')
            for index_1 in range(0, len(data[index_0])):
                file.write(str(data[index_0][index_1]))
                if index_1 < len(data[index_0]) - 1:
                    file.write(',')
            file.write('\n')
