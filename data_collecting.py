from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utils import orglist, orgli, exn, add9
from time import sleep
from dates import Day, Month, greater_or_equal, lower_or_equal, where
import numpy
import pandas


service = Service(executable_path='/home/ruanv/Documentos/youtube/msedgedriver')


def take_data(website: str, viewsorsubs: int) -> tuple[list[Day], list[int]]:
    subs = []
    dates = []
    string0 = 'TotalSubscribers'
    string1 = 'TotalVideoViews'
    subsdata = ''
    string2 = 'graphdivtotalsubs'
    string3 = 'graphdivtotalviews'
    string = ''
    gj = False
    optionsi = Options()
    optionsi.add_argument("--log-level=3")
    optionsi.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2,
                                               'profile.managed_default_content_settings.javascript': 2})
    driver = Edge(service=service, options=optionsi)
    driver.get(website)
    try:
        WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located((By.XPATH, '//th')))
        yy = driver.find_elements(by='xpath', value='//th')
        for eleme in yy:
            if eleme.text == 'Goal Date':
                gj = True
                break
    except TimeoutException:
        pass
    elements = driver.find_elements(by='xpath', value='//script[@type="text/javascript"]')
    if viewsorsubs == 0 and gj:
        string = string2
    elif viewsorsubs == 1 and gj:
        string = string3
    elif viewsorsubs == 0 and not gj:
        string = string0
    elif viewsorsubs == 1 and not gj:
        string = string1
    for elem in elements:
        b = elem.get_property('firstChild')
        if b is not None:
            if string in b['nodeValue']:
                subsdata = b['nodeValue']
    driver.quit()
    if gj:
        c = subsdata.split(' +')[1:-2]
        c[0] = c[0][1:]
        for i, bag in enumerate(c):
            c[i] = bag.split('\\n"')[0]
        for j in range(0, len(c)):
            if '+"' in c[j]:
                c[j] = c[j].split('+"')[1]
            elif '"' in c[j]:
                c[j] = c[j].split('"')[1]
        for k in c:
            lds = k.split(',')
            subs.append(int(lds[1]))
            dates.append(Day(int(lds[0][0:4]), int(lds[0][4:6]), int(lds[0][6:8])))
    if not gj:
        ccc = subsdata.split(' ')
        for i in ccc:
            dates.append(i)
        dates = list(filter(lambda x: x != '+', dates))
        dates = [i[1:-3] for i in dates]
        i = 0
        for g in range(0, len(dates)):
            for n in dates[g - i]:
                if n not in '0123456789-,':
                    dates.pop(g - i)
                    i += 1
            if dates[g - i] == '':
                dates.pop(g - i)
                i += 1
        for c in range(0, len(dates)):
            a = dates[c].split(',')
            b = a[0].split('-')
            dates[c] = Day(int(b[0]), int(b[1]), int(b[2]))
            subs.append(int(a[1]))
    return dates, subs


def search_channel_link(channel_name: str):
    try:
        optionsi = Options()
        optionsi.add_argument("--log-level=3")
        optionsi.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
        driver = Edge(service=service, options=optionsi)
        driver.get(f'https://google.com/search?q={channel_name.replace(" ", "+")}+youtube+channel')
        WebDriverWait(driver, 4).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//cite')))
        chan = driver.find_elements(By.XPATH, '//cite')
        for t in chan:
            if 'youtube.com' in t.get_property('firstChild')['textContent']:
                t.click()
                break
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//link[@rel="image_src"]')))
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//meta[@itemprop="name"]')))
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//meta[@itemprop="identifier"]')))
        ico = driver.find_element(By.XPATH, '//link[@rel="image_src"]').get_property('href')
        na = driver.find_element(By.XPATH, '//meta[@itemprop="name"]').get_property('content')
        oi = driver.find_element(By.XPATH, '//meta[@itemprop="identifier"]').get_property('content')
        driver.quit()
        return oi, ico, na
    except TimeoutException:
        return 0, 0, 0


def tiradas(website: str, vos: int) -> tuple[list[Day], list[int], str]:
    def convert2m(lista):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        for i0, thg in enumerate(lista):
            jh = thg.split(' ')
            lista[i0] = Month(int(jh[3]), months.index(jh[2].split(',')[0]) + 1)
        return lista

    optionsi = Options()
    optionsi.add_argument("--log-level=3")
    optionsi.add_argument("start-maximized")
    optionsi.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    driver = Edge(service=service, options=optionsi)
    driver.get('https://socialblade.com')
    driver.switch_to.window(driver.window_handles[0])
    WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
        (By.XPATH, '//input[@placeholder="Enter YouTube Username"]')))
    g = driver.find_element(
        By.XPATH, '//input[@placeholder="Enter YouTube Username"]')
    g.send_keys(website, Keys.ENTER)
    WebDriverWait(driver, 30).until(
        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@id="YouTubeUserMenu"]')))
    driver.get(f'{driver.current_url}/monthly')
    list_dates = []
    list_data = []
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'g[class="highcharts-markers '
                                                                          'highcharts-series-0 highcharts-line-series '
                                                                          'highcharts-tracker"]')))
    txts2 = driver.find_elements(by='css selector',
                                 value='g[class="highcharts-markers highcharts-series-0 highcharts-line-series '
                                       'highcharts-tracker"]')
    sit = f'https://web.archive.org/web/*/{driver.current_url}'
    items = []
    if vos == 0:
        items = txts2[0].get_property('childNodes')
    elif vos == 1:
        items = txts2[1].get_property('childNodes')
    for hg in items:
        if hg == items[0]:
            ActionChains(driver).move_to_element(hg).click().perform()
        ActionChains(driver).move_to_element(hg).click().perform()
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'tspan[style="font-weight: bold;"]')))
        txt = driver.find_element(by='css selector', value='tspan[style="font-weight: bold;"]')
        txtt = driver.find_element(by='css selector', value='tspan[style="font-size: 5pt;"]')
        ljs = int(''.join((txt.text.split(" ")[0].split(","))))
        list_dates.append(ljs)
        list_data.append(txtt.text)
    fday = driver.find_elements(By.XPATH,
                                '//div[@style="width: 860px; height: 32px; line-height: 32px; background: #fcfcfc; padding: 0px 20px; color:#444; font-size: 9pt; border-bottom: 1px solid #eee;"]')
    fday2 = driver.find_elements(By.XPATH,
                                 '//div[@style="width: 860px; height: 32px; line-height: 32px; background: #f8f8f8;; padding: 0px 20px; color:#444; font-size: 9pt; border-bottom: 1px solid #eee;"]')
    for it in fday:
        if it.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text == '2023-11-01':
            if vos == 0:
                list_dates.insert(0, exn(it.find_element(By.XPATH, './div[@style="float: left; width: 205px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                list_data.insert(0, it.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
            elif vos == 1:
                list_dates.insert(0, exn(it.find_element(By.XPATH, './div[@style="float: left; width: 240px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                list_data.insert(0, it.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
    for it in fday2:
        if it.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text == '2023-11-01':
            if vos == 0:
                list_dates.insert(0, exn(it.find_element(By.XPATH, './div[@style="float: left; width: 205px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                list_data.insert(0, it.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
            elif vos == 1:
                list_dates.insert(0, exn(it.find_element(By.XPATH, './div[@style="float: left; width: 240px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                list_data.insert(0, it.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
    driver.quit()
    list_data = [list_data[0]] + convert2m(list_data[1:])
    a = list_data[0].split('-')
    list_data[0] = Month(int(a[0]), int(a[1]))
    list_data.reverse()
    list_dates.reverse()
    if vos == 0:
        som = list_dates.copy()
        old_va = ''
        count = 0
        for i, jc in enumerate(som):
            if i == 0:
                old_va = jc
            elif i == len(som) - 1:
                pass
            elif i > 0:
                if old_va == jc:
                    list_data.pop(i - count)
                    list_dates.pop(i - count)
                    count += 1
                elif old_va != jc:
                    old_va = jc
    for i in range(0, len(list_data)):
        a = list_data[i].splitted
        list_data[i] = Day(a[0], a[1], 1)
    le = add9(list_data, list_dates)
    return le[0], orgli(le[1]), sit


def search_page2(website: str, start=Day(2010, 1, 1), final=Day(2019, 9, 16), suborview=0) -> tuple[list[Day], list[int]]:
    data_0 = tiradas(website, suborview)
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    ye = final.splitted[0]
    ye1 = start.splitted[0]
    jklh = start
    data0 = []
    optionsi = Options()
    optionsi.add_argument("--log-level=3")
    driver = Edge(service=service, options=optionsi)
    driver.get(data_0[2])
    try:
        WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//span[@class="sparkline-year-label"]')))
    except TimeoutException:
        ye = ye1 - 1
    year = driver.find_elements(by='xpath', value='//span[@class="sparkline-year-label"]')
    years = [x.text for x in year]
    while ye >= ye1:
        if ye == 2011:
            break
        year[years.index(str(ye))].click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="month-day-container "]/div/a')))
        except TimeoutException:
            ye -= 1
            continue
        links = driver.find_elements(by='xpath', value='//div[@class="month-day-container "]/div/a')
        links.reverse()
        for i in range(0, len(links)):
            f = links[i].get_property('parentElement').get_property('parentElement').get_property(
                'parentElement').get_property('parentElement').get_property('parentElement').get_property('firstChild')
            str0 = Day(ye, months.index(f.text) + 1, int(links[i].text))
            if greater_or_equal(final + 1, str0) and greater_or_equal(str0, Day(2012, 3, 1)):
                data0.append(take_data(links[i].get_attribute('href'), suborview))
                break
        ye -= 1
    driver.quit()
    driver = Edge(service=service, options=optionsi)
    driver.get(data_0[2][:-8])
    ano = 2013
    try:
        WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//span[@class="sparkline-year-label"]')))
    except TimeoutException:
        ano = ye1 - 1
    yearf = driver.find_elements(by='xpath', value='//span[@class="sparkline-year-label"]')
    yearsf = [x.text for x in yearf]
    while ano >= ye1:
        if ano == 2011:
            break
        yearf[yearsf.index(str(ano))].click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="month-day-container "]/div/a')))
        except TimeoutException:
            ano -= 1
            continue
        links = driver.find_elements(by='xpath', value='//div[@class="month-day-container "]/div/a')
        links.reverse()
        for i in range(0, len(links)):
            f = links[i].get_property('parentElement').get_property('parentElement').get_property(
                'parentElement').get_property('parentElement').get_property('parentElement').get_property('firstChild')
            str0 = Day(ano, months.index(f.text) + 1, int(links[i].text))
            if lower_or_equal(str0, Day(2013, 9, 30)):
                data0.append(take_data(links[i].get_attribute('href'), suborview))
                break
        ano -= 1
    driver.quit()
    bb = []
    if len(data0) > 1:
        for i in range(1, len(data0)):
            if not data0[i][0]:
                continue
            if i == 1:
                bb = orglist(data0[i][0], data0[i - 1][0], data0[i][1], data0[i - 1][1])
            else:
                bb = orglist(bb[0], data0[i][0], bb[1], data0[i][1])
        bb = [*bb]
    elif len(data0) == 1:
        bb = data0[0]
    if bb and bb[0]:
            jhk = orglist(bb[0], data_0[0], bb[1], data_0[1])
            dates = jhk[0]
            subs = jhk[1]
            if where(jklh - 1, dates) != -1:
                z = where(jklh, dates)
                dates = dates[z:]
                subs = subs[z:]
            return dates, subs
    elif not bb or not bb[0]:
        dates = data_0[0]
        subs = orgli(data_0[1])
        if where(jklh - 1, dates) != -1:
            z = where(jklh, dates)
            dates = dates[z:]
            subs = subs[z:]
        return dates, subs


def take_data_from_comparison(website: str):
    optionsi = Options()
    optionsi.add_argument("--log-level=3")
    optionsi.add_argument("start-maximized")
    optionsi.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    driver = Edge(service=service, options=optionsi)
    driver.get(website)
    dates_ = []
    data0 = []
    data1 = []
    data2 = []
    data0_ = []
    data1_ = []
    data2_ = []
    while True:
        sleep(0.1)
        try:
            if 'google' in driver.current_url:
                driver.quit()
                break
            e = driver.find_element(By.XPATH, value='//div[@class="dygraph-legend"]')
            f = e.text.split(': ')
            print(len(dates_), 'de 718')
            if len(f) == 5:
                j = f[0].replace('/', '-')
                if j not in dates_:
                    dates_.append(j)
                    data0.append(exn(f[2].split(' ')[0]))
                    data1.append(exn(f[3].split(' ')[0]))
                    data2.append(exn(f[4]))
        except TimeoutException:
            pass
    dates_ = numpy.asarray(dates_, dtype='datetime64')
    dates = numpy.sort(dates_)
    for _ in numpy.arange(0, len(dates_)):
        m = numpy.where(dates_ == numpy.min(dates_))[0][0]
        data0_.append(data0[m])
        data1_.append(data1[m])
        data2_.append(data2[m])
        dates_[m] = numpy.datetime64('9999-12-31')
    l0 = 0
    dates_ = numpy.arange('2020-09-29', '2022-09-17', dtype='datetime64')
    for y in numpy.arange(0, numpy.size(dates_)):
        if dates_[y] not in dates:
            data0_.insert(y + l0, 999999999999999)
            data1_.insert(y + l0, 999999999999999)
            data2_.insert(y + l0, 999999999999999)
            l0 += 1
    data0_ = orgli(data0_)
    data1_ = orgli(data1_)
    data2_ = orgli(data2_)
    dict0 = {'Mantovani': data0_, 'TABINHO': data1_, 'ALDO TV': data2_}
    dados = pandas.DataFrame(dict0, index=dates_).transpose()
    dados.to_csv('part12-sg.csv')


'''
if __name__ == '__main__':
    take_data_from_comparison('https://socialblade.com/youtube/compare/mantovani/tabinho/aldo%20tv')
'''
