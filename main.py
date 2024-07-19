from dc import propag2, prolin
from read_write_csv import write_csv


def prochannel(*args: str):
    lins = []
    profiles = []
    data = []
    for ch in args:
        jd = prolin(ch)
        profiles.append([jd[2], jd[1]])
        lins.append(jd[0])
    leng = []
    for i, j in enumerate(lins):
        print('Pesquisando: ', profiles[i][0])
        a = propag2(website=j, suborview=0)
        data.append(a[1])
        if len(a[1]) > len(leng):
            leng = a[0].copy()
    for i in range(0, len(data)):
        if len(data[i]) < len(leng):
            data[i] = [0] * (len(leng) - len(data[i])) + data[i]
    write_csv('test7.csv', leng, data, profiles)


if __name__ == '__main__':
    print('Iniciando...')
    prochannel('Jazzghost')
