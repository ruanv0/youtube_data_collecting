from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from dates import Day
from read_write_csv import write_csv
from utils import add9, interpolate_9


def collect_subs_data(item: str) -> str:
    string_data = ''
    driver_options = Options()
    driver_options.add_argument("--log-level=3")
    driver_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    service = Service(executable_path='msedgedriver')
    driver = webdriver.Chrome(service=service, options=driver_options)
    driver.get(item)
    try:
        WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//div[@id="profile_show_subscriber_count"]')))
        element_0 = driver.find_element(by='xpath', value='//div[@id="profile_show_subscriber_count"]')
        string_data = element_0.text
    except TimeoutException:
        try:
            WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//span[@class="yt-subscription-button-subscriber-count-branded-horizontal subscribed"]')))
            element_1 = driver.find_element(by='xpath', value='//span[@class="yt-subscription-button-subscriber-count-branded-horizontal subscribed"]')
            string_data = element_1.text
        except TimeoutException:
            try:
                WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, '//span[@class="stat-value"]')))
                elem3 = driver.find_element(by='xpath', value='//span[@class="stat-value"]')
                string_data = elem3.text
            except TimeoutException:
                try:
                    WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located(
                        (By.XPATH, '//strong[@id="user-profile-subscriber-count"]')))
                    elem4 = driver.find_element(by='xpath', value='//strong[@id="user-profile-subscriber-count"]')
                    string_data = elem4.text
                except TimeoutException:
                    pass
    return string_data.replace(',', '').replace('.', '').replace(' ', '')


def search_youtube_page(user_id: str, name: str):
    driver_options = Options()
    driver_options.add_argument("--log-level=3")
    driver_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    service = Service(executable_path='msedgedriver')
    driver = webdriver.Chrome(service=service, options=driver_options)
    website = f'https://web.archive.org/web/*/http://youtube.com/user/{user_id}'
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
    years_elements = driver.find_elements(by='xpath', value='//span[@class="sparkline-year-label"]')
    for element in years_elements:
        years.append(element.text)
    while final_year >= start_year:
        years_elements[years.index(str(final_year))].click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="month-day-container "]/div/a')))
        except TimeoutException:
            final_year -= 1
            continue
        links_elements = driver.find_elements(by='xpath', value='//div[@class="month-day-container "]/div/a')
        links_elements.reverse()
        for i in range(0, len(links_elements)):
            f = links_elements[i].get_property('parentElement').get_property('parentElement').get_property(
                'parentElement').get_property('parentElement').get_property('parentElement').get_property('firstChild')
            dates.append(Day(final_year, months.index(f.text) + 1, int(links_elements[i].text)))
            subs.append(collect_subs_data(links_elements[i].get_attribute('href')))
        final_year -= 1
        dates = [dates[x] for x in range(0, len(subs)) if subs[x] != '']
        subs = [x for x in subs if x != '']
        '''
        count = 0
        for index_ in range(0, len(subs)):
            if subs[index_ - count] == '':
                dates.pop(index_ - count)
                subs.pop(index_ - count)
                count += 1'''
    driver.quit()
    dates.reverse()
    subs.reverse()
    subs = [int(a) for a in subs]
    e = [*add9(dates, subs)]
    e[1] = interpolate_9(e[1])
    write_csv('test01.csv', e[0], [e[1]], [[name, '']])
    '''
    try:
        search_channel(name)
    except:
        print(f'Unable to find the channel {name}')'''


if __name__ == '__main__':
    users_ids = ['AuthenticGames']
    names = ['AuthenticGames']
    for index_ in range(0, len(users_ids)):
        search_youtube_page(users_ids[index_], names[index_])
