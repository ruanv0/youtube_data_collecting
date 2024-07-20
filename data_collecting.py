from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utils import join_dates_values, interpolate_9, fix_value, add9
from time import sleep
from dates import Day, Month, greater_or_equal, lower_or_equal, where
import numpy
import pandas


driver_service = Service(executable_path='/home/ruanv/Documentos/youtube/msedgedriver')


# 'subs_or_views' variable may be 0 (zero) or 1 (one).
# if 'subs_or_views' variable is 0, take subscribers data
# else if 'subs_or_views' variable is 1, take views data
def take_data(website: str, subs_or_views: int) -> tuple[list[Day], list[int]]:
    subs = []
    data = []
    string0 = 'TotalSubscribers'
    string1 = 'TotalVideoViews'
    subscribers_string = ''
    string2 = 'graphdivtotalsubs'
    string3 = 'graphdivtotalviews'
    string = ''
    boolean_0 = False
    driver_options = Options()
    driver_options.add_argument("--log-level=3")
    driver_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2,
                                               'profile.managed_default_content_settings.javascript': 2})
    driver = Edge(service=driver_service, options=driver_options)
    driver.get(website)
    try:
        WebDriverWait(driver, 4).until(expected_conditions.presence_of_element_located((By.XPATH, '//th')))
        elements_0 = driver.find_elements(by='xpath', value='//th')
        for element in elements_0:
            if element.text == 'Goal Date':
                boolean_0 = True
                break
    except TimeoutException:
        pass
    elements_0 = driver.find_elements(by='xpath', value='//script[@type="text/javascript"]')
    if subs_or_views == 0 and boolean_0:
        string = string2
    elif subs_or_views == 1 and boolean_0:
        string = string3
    elif subs_or_views == 0 and not boolean_0:
        string = string0
    elif subs_or_views == 1 and not boolean_0:
        string = string1
    for element in elements_0:
        date = element.get_property('firstChild')
        if date is not None:
            if string in date['nodeValue']:
                subscribers_string = date['nodeValue']
    driver.quit()
    if boolean_0:
        split_list_0 = subscribers_string.split(' +')[1:-2]
        split_list_0[0] = split_list_0[0][1:]
        for index_, string_object in enumerate(split_list_0):
            split_list_0[index_] = string_object.split('\\n"')[0]
        for index_ in range(0, len(split_list_0)):
            if '+"' in split_list_0[index_]:
                split_list_0[index_] = split_list_0[index_].split('+"')[1]
            elif '"' in split_list_0[index_]:
                split_list_0[index_] = split_list_0[index_].split('"')[1]
        for string_object in split_list_0:
            split_list_1 = string_object.split(',')
            subs.append(int(split_list_1[1]))
            data.append(Day(int(split_list_1[0][0:4]), int(split_list_1[0][4:6]), int(split_list_1[0][6:8])))
    if not boolean_0:
        split_list_2 = subscribers_string.split(' ')
        for string_object in split_list_2:
            data.append(string_object)
        data = list(filter(lambda x: x != '+', data))
        data = [i[1:-3] for i in data]
        index_0 = 0
        for index_1 in range(0, len(data)):
            for string_object in data[index_1 - index_0]:
                if string_object not in '0123456789-,':
                    data.pop(index_1 - index_0)
                    index_0 += 1
            if data[index_1 - index_0] == '':
                data.pop(index_1 - index_0)
                index_0 += 1
        for index_ in range(0, len(data)):
            data_splitted = data[index_].split(',')
            date = data_splitted[0].split('-')
            data[index_] = Day(int(date[0]), int(date[1]), int(date[2]))
            subs.append(int(data_splitted[1]))
    return data, subs


def search_channel_link(channel_name: str):
    try:
        driver_options = Options()
        driver_options.add_argument("--log-level=3")
        driver_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
        driver = Edge(service=driver_service, options=driver_options)
        driver.get(f'https://google.com/search?q={channel_name.replace(" ", "+")}+youtube+channel')
        WebDriverWait(driver, 4).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//cite')))
        elements_0 = driver.find_elements(By.XPATH, '//cite')
        for element in elements_0:
            if 'youtube.com' in element.get_property('firstChild')['textContent']:
                element.click()
                break
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//link[@rel="image_src"]')))
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//meta[@itemprop="name"]')))
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//meta[@itemprop="identifier"]')))
        image_link = driver.find_element(By.XPATH, '//link[@rel="image_src"]').get_property('href')
        name = driver.find_element(By.XPATH, '//meta[@itemprop="name"]').get_property('content')
        identifier = driver.find_element(By.XPATH, '//meta[@itemprop="identifier"]').get_property('content')
        driver.quit()
        return identifier, image_link, name
    except TimeoutException:
        return 0, 0, 0


# 'subs_or_views' variable may be 0 (zero) or 1 (one).
# if 'subs_or_views' variable is 0, take subscribers data
# else if 'subs_or_views' variable is 1, take views data
def take_data_2(website: str, subs_or_views: int) -> tuple[list[Day], list[int], str]:
    def convert_months(list_0):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        for index_, object_ in enumerate(list_0):
            splitted_object = object_.split(' ')
            list_0[index_] = Month(int(splitted_object[3]), months.index(splitted_object[2].split(',')[0]) + 1)
        return list_0

    driver_options = Options()
    driver_options.add_argument("--log-level=3")
    driver_options.add_argument("start-maximized")
    driver_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    driver = Edge(service=driver_service, options=driver_options)
    driver.get('https://socialblade.com')
    driver.switch_to.window(driver.window_handles[0])
    WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
        (By.XPATH, '//input[@placeholder="Enter YouTube Username"]')))
    element_0 = driver.find_element(
        By.XPATH, '//input[@placeholder="Enter YouTube Username"]')
    element_0.send_keys(website, Keys.ENTER)
    WebDriverWait(driver, 30).until(
        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@id="YouTubeUserMenu"]')))
    driver.get(f'{driver.current_url}/monthly')
    dates = []
    data = []
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'g[class="highcharts-markers '
                                                                          'highcharts-series-0 highcharts-line-series '
                                                                          'highcharts-tracker"]')))
    elements_1 = driver.find_elements(by='css selector',
                                 value='g[class="highcharts-markers highcharts-series-0 highcharts-line-series '
                                       'highcharts-tracker"]')
    website_1 = f'https://web.archive.org/web/*/{driver.current_url}'
    items = []
    if subs_or_views == 0:
        items = elements_1[0].get_property('childNodes')
    elif subs_or_views == 1:
        items = elements_1[1].get_property('childNodes')
    for item in items:
        if item == items[0]:
            ActionChains(driver).move_to_element(item).click().perform()
        ActionChains(driver).move_to_element(item).click().perform()
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'tspan[style="font-weight: bold;"]')))
        text_0 = driver.find_element(by='css selector', value='tspan[style="font-weight: bold;"]')
        text_1 = driver.find_element(by='css selector', value='tspan[style="font-size: 5pt;"]')
        split_list = int(''.join((text_0.text.split(" ")[0].split(","))))
        dates.append(split_list)
        data.append(text_1.text)
    days_elements_0 = driver.find_elements(By.XPATH,
                                '//div[@style="width: 860px; height: 32px; line-height: 32px; background: #fcfcfc; padding: 0px 20px; color:#444; font-size: 9pt; border-bottom: 1px solid #eee;"]')
    days_elements_1 = driver.find_elements(By.XPATH,
                                 '//div[@style="width: 860px; height: 32px; line-height: 32px; background: #f8f8f8;; padding: 0px 20px; color:#444; font-size: 9pt; border-bottom: 1px solid #eee;"]')
    for element in days_elements_0:
        if element.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text == '2023-11-01':
            if subs_or_views == 0:
                dates.insert(0, fix_value(element.find_element(By.XPATH, './div[@style="float: left; width: 205px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                data.insert(0, element.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
            elif subs_or_views == 1:
                dates.insert(0, fix_value(element.find_element(By.XPATH, './div[@style="float: left; width: 240px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                data.insert(0, element.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
    for element in days_elements_1:
        if element.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text == '2023-11-01':
            if subs_or_views == 0:
                dates.insert(0, fix_value(element.find_element(By.XPATH, './div[@style="float: left; width: 205px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                data.insert(0, element.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
            elif subs_or_views == 1:
                dates.insert(0, fix_value(element.find_element(By.XPATH, './div[@style="float: left; width: 240px;"]/div[@style="width: 140px; float: left;"]').text.replace(',', '')))
                data.insert(0, element.find_element(By.XPATH, './div[@style="float: left; width: 95px;"]').text[:-3])
    driver.quit()
    data = [data[0]] + convert_months(data[1:])
    month = data[0].split('-')
    data[0] = Month(int(month[0]), int(month[1]))
    data.reverse()
    dates.reverse()
    if subs_or_views == 0:
        list_dates_copy = dates.copy()
        old_variable = ''
        count = 0
        for index, object in enumerate(list_dates_copy):
            if index == 0:
                old_variable = object
            elif index == len(list_dates_copy) - 1:
                pass
            elif index > 0:
                if old_variable == object:
                    data.pop(index - count)
                    dates.pop(index - count)
                    count += 1
                elif old_variable != object:
                    old_variable = object
    for index in range(0, len(data)):
        month = data[index].splitted
        data[index] = Day(month[0], month[1], 1)
    data = add9(data, dates)
    return data[0], interpolate_9(data[1]), website_1


# 'subs_or_views' variable may be 0 (zero) or 1 (one).
# if 'subs_or_views' variable is 0, take subscribers data
# else if 'subs_or_views' variable is 1, take views data
def search_page(website: str, start=Day(2010, 1, 1), final=Day(2019, 9, 16), subs_or_views=0) -> tuple[list[Day], list[int]]:
    data_0 = take_data_2(website, subs_or_views)
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    final_year = final.splitted[0]
    start_year = start.splitted[0]
    start_copy = start
    data_1 = []
    driver_options = Options()
    driver_options.add_argument("--log-level=3")
    driver = Edge(service=driver_service, options=driver_options)
    driver.get(data_0[2])
    try:
        WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//span[@class="sparkline-year-label"]')))
    except TimeoutException:
        final_year = start_year - 1
    years_elements = driver.find_elements(by='xpath', value='//span[@class="sparkline-year-label"]')
    years_texts = [x.text for x in years_elements]
    while final_year >= start_year:
        if final_year == 2011:
            break
        years_elements[years_texts.index(str(final_year))].click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="month-day-container "]/div/a')))
        except TimeoutException:
            final_year -= 1
            continue
        links = driver.find_elements(by='xpath', value='//div[@class="month-day-container "]/div/a')
        links.reverse()
        for index_ in range(0, len(links)):
            f = links[index_].get_property('parentElement').get_property('parentElement').get_property(
                'parentElement').get_property('parentElement').get_property('parentElement').get_property('firstChild')
            str0 = Day(final_year, months.index(f.text) + 1, int(links[index_].text))
            if greater_or_equal(final + 1, str0) and greater_or_equal(str0, Day(2012, 3, 1)):
                data_1.append(take_data(links[index_].get_attribute('href'), subs_or_views))
                break
        final_year -= 1
    driver.quit()
    driver = Edge(service=driver_service, options=driver_options)
    driver.get(data_0[2][:-8])
    year_variable = 2013
    try:
        WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//span[@class="sparkline-year-label"]')))
    except TimeoutException:
        year_variable = start_year - 1
    years_elements_1 = driver.find_elements(by='xpath', value='//span[@class="sparkline-year-label"]')
    years_texts_1 = [x.text for x in years_elements_1]
    while year_variable >= start_year:
        if year_variable == 2011:
            break
        years_elements_1[years_texts_1.index(str(year_variable))].click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="month-day-container "]/div/a')))
        except TimeoutException:
            year_variable -= 1
            continue
        links = driver.find_elements(by='xpath', value='//div[@class="month-day-container "]/div/a')
        links.reverse()
        for index_ in range(0, len(links)):
            f = links[index_].get_property('parentElement').get_property('parentElement').get_property(
                'parentElement').get_property('parentElement').get_property('parentElement').get_property('firstChild')
            str0 = Day(year_variable, months.index(f.text) + 1, int(links[index_].text))
            if lower_or_equal(str0, Day(2013, 9, 30)):
                data_1.append(take_data(links[index_].get_attribute('href'), subs_or_views))
                break
        year_variable -= 1
    driver.quit()
    data_copy = []
    if len(data_1) > 1:
        for index_ in range(1, len(data_1)):
            if not data_1[index_][0]:
                continue
            if index_ == 1:
                data_copy = join_dates_values(data_1[index_][0], data_1[index_ - 1][0], data_1[index_][1], data_1[index_ - 1][1])
            else:
                data_copy = join_dates_values(data_copy[0], data_1[index_][0], data_copy[1], data_1[index_][1])
        data_copy = [*data_copy]
    elif len(data_1) == 1:
        data_copy = data_1[0]
    if data_copy and data_copy[0]:
            united_dates_values = join_dates_values(data_copy[0], data_0[0], data_copy[1], data_0[1])
            dates = united_dates_values[0]
            subs = united_dates_values[1]
            if where(start_copy - 1, dates) != -1:
                start_index = where(start_copy, dates)
                dates = dates[start_index:]
                subs = subs[start_index:]
            return dates, subs
    elif not data_copy or not data_copy[0]:
        dates = data_0[0]
        subs = interpolate_9(data_0[1])
        if where(start_copy - 1, dates) != -1:
            start_index = where(start_copy, dates)
            dates = dates[start_index:]
            subs = subs[start_index:]
        return dates, subs


def take_data_from_comparison(website: str):
    driver_options = Options()
    driver_options.add_argument("--log-level=3")
    driver_options.add_argument("start-maximized")
    driver_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    driver = Edge(service=driver_service, options=driver_options)
    driver.get(website)
    dates_0 = []
    data_0 = []
    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []
    data_5 = []
    while True:
        sleep(0.1)
        try:
            if 'google' in driver.current_url:
                driver.quit()
                break
            element_0 = driver.find_element(By.XPATH, value='//div[@class="dygraph-legend"]')
            splitted_element_text_0 = element_0.text.split(': ')
            print(len(dates_0), 'of 718')
            if len(splitted_element_text_0) == 5:
                date_string_0 = splitted_element_text_0[0].replace('/', '-')
                if date_string_0 not in dates_0:
                    dates_0.append(date_string_0)
                    data_0.append(fix_value(splitted_element_text_0[2].split(' ')[0]))
                    data_1.append(fix_value(splitted_element_text_0[3].split(' ')[0]))
                    data_2.append(fix_value(splitted_element_text_0[4]))
        except TimeoutException:
            pass
    dates_0 = numpy.asarray(dates_0, dtype='datetime64')
    dates_1 = numpy.sort(dates_0)
    for _ in numpy.arange(0, len(dates_0)):
        where_index = numpy.where(dates_0 == numpy.min(dates_0))[0][0]
        data_3.append(data_0[where_index])
        data_4.append(data_1[where_index])
        data_5.append(data_2[where_index])
        dates_0[where_index] = numpy.datetime64('9999-12-31')
    count = 0
    dates_0 = numpy.arange('2020-09-29', '2022-09-17', dtype='datetime64')
    for index_ in numpy.arange(0, numpy.size(dates_0)):
        if dates_0[index_] not in dates_1:
            data_3.insert(index_ + count, 999999999999999)
            data_4.insert(index_ + count, 999999999999999)
            data_5.insert(index_ + count, 999999999999999)
            count += 1
    data_3 = interpolate_9(data_3)
    data_4 = interpolate_9(data_4)
    data_5 = interpolate_9(data_5)
    dict0 = {'Mantovani': data_3, 'TABINHO': data_4, 'ALDO TV': data_5}
    data_frame_0 = pandas.DataFrame(dict0, index=dates_0).transpose()
    data_frame_0.to_csv('part12-sg.csv')


'''
if __name__ == '__main__':
    take_data_from_comparison('https://socialblade.com/youtube/compare/mantovani/tabinho/aldo%20tv')
'''
