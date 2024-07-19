from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from dates import Day
from read_write_csv import write_csv
from utils import add9, orgli


def collect_subs_data(item: str) -> str:
    sdata = ''
    optionsi = Options()
    optionsi.add_argument("--log-level=3")
    optionsi.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    service = Service(executable_path='msedgedriver')
    driver = webdriver.Chrome(service=service, options=optionsi)
    driver.get(item)
    try:
        WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//div[@id="profile_show_subscriber_count"]')))
        elem = driver.find_element(by='xpath', value='//div[@id="profile_show_subscriber_count"]')
        sdata = elem.text
    except TimeoutException:
        try:
            WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//span[@class="yt-subscription-button-subscriber-count-branded-horizontal subscribed"]')))
            elem2 = driver.find_element(by='xpath', value='//span[@class="yt-subscription-button-subscriber-count-branded-horizontal subscribed"]')
            sdata = elem2.text
        except TimeoutException:
            try:
                WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, '//span[@class="stat-value"]')))
                elem3 = driver.find_element(by='xpath', value='//span[@class="stat-value"]')
                sdata = elem3.text
            except TimeoutException:
                try:
                    WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
                        (By.XPATH, '//strong[@id="user-profile-subscriber-count"]')))
                    elem4 = driver.find_element(by='xpath', value='//strong[@id="user-profile-subscriber-count"]')
                    sdata = elem4.text
                except TimeoutException:
                    pass
    return sdata.replace(',', '').replace('.', '').replace(' ', '')


def search_youtube_page(user: str, name: str):
    optionsi = Options()
    optionsi.add_argument("--log-level=3")
    optionsi.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    service = Service(executable_path='msedgedriver')
    driver = webdriver.Chrome(service=service, options=optionsi)
    website = f'https://web.archive.org/web/*/http://youtube.com/user/{user}'
    dates = []
    subs = []
    years = []
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    start_year = 2010
    final_year = 2015
    driver.get(website)
    try:
        WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//span[@class="sparkline-year-label"]')))
    except TimeoutException:
        start_year = final_year
    year = driver.find_elements(by='xpath', value='//span[@class="sparkline-year-label"]')
    for c in year:
        years.append(c.text)
    while final_year >= start_year:
        year[years.index(str(final_year))].click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="month-day-container "]/div/a')))
        except TimeoutException:
            final_year -= 1
            continue
        links = driver.find_elements(by='xpath', value='//div[@class="month-day-container "]/div/a')
        links.reverse()
        for i in range(0, len(links)):
            f = links[i].get_property('parentElement').get_property('parentElement').get_property(
                'parentElement').get_property('parentElement').get_property('parentElement').get_property('firstChild')
            dates.append(Day(final_year, months.index(f.text) + 1, int(links[i].text)))
            subs.append(collect_subs_data(links[i].get_attribute('href')))
        final_year -= 1
        # k = 0
        dates = [dates[x] for x in range(0, len(subs)) if subs[x] != '']
        subs = [x for x in subs if x != '']
        '''
        for c in range(0, len(subs)):
            if subs[c - k] == '':
                dates.pop(c - k)
                subs.pop(c - k)
                k += 1'''
    driver.quit()
    dates.reverse()
    subs.reverse()
    subs = [int(a) for a in subs]
    e = [*add9(dates, subs)]
    e[1] = orgli(e[1])
    write_csv('test01.csv', e[0], [e[1]], [[name, '']])
    '''
    try:
        prochannel(name)
    except:
        print(f'Não foi pessivel pesquisar o canal {name}')'''


if __name__ == '__main__':
    j = ['AuthenticGames']
    names = ['AuthenticGames']
    for i in range(0, len(j)):
        search_youtube_page(j[i], names[i])
