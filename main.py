from data_collecting import search_page, search_channel_link
from read_write_csv import write_csv


def search_channel(*args: str):
    images_links = []
    profiles = []
    data = []
    for channel in args:
        dates_subscribers_photos = search_channel_link(channel)
        profiles.append([dates_subscribers_photos[2], dates_subscribers_photos[1]])
        images_links.append(dates_subscribers_photos[0])
    dates = []
    for i, j in enumerate(images_links):
        print('Searching: ', profiles[i][0])
        a = search_page(website=j, subs_or_views=0)
        data.append(a[1])
        if len(a[1]) > len(dates):
            dates = a[0].copy()
    for i in range(0, len(data)):
        if len(data[i]) < len(dates):
            data[i] = [0] * (len(dates) - len(data[i])) + data[i]
    write_csv('test7.csv', dates, data, profiles)


if __name__ == '__main__':
    print('Iniciando...')
    search_channel('Jazzghost')
