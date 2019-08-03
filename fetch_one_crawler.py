from selenium import webdriver
import time
from bs4 import BeautifulSoup

def crawl_one(hashtag, option = False):
    url = 'https://www.instagram.com/explore/tags/' + hashtag

    driver_addr = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    if option:
        driver = webdriver.Chrome(driver_addr, chrome_options=options)
    else:
        driver = webdriver.Chrome(driver_addr)

    driver.implicitly_wait(15)

    driver.get(url)

    user_link_list = []
    full_list = []

    time.sleep(1)
    link = driver.find_elements_by_css_selector('div.v1Nh3.kIKUG._bz0w > a')
    for i in link:
        user_link_list.append(i.get_attribute('href'))

    element_list = []

    driver.get(user_link_list[9])
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')

    user_id = driver.find_element_by_css_selector('h2._6lAjh > a')
    element_list.append({'username': user_id.get_attribute('title')})

    try:
        user_profile_img = driver.find_element_by_css_selector('a._2dbep.qNELH.kIKUG > img')
        element_list.append({'profile_img': user_profile_img.get_attribute('src')})
    except:
        element_list.append({'profile_img': None})

    div = bs.find('div', class_='C4VMK')
    span = div.find('span')
    element_list.append({'text': span.text})

    img = driver.find_elements_by_css_selector('div.KL4Bh > img')
    img_list = {'img_url': []}
    for j in img:
        img_list['img_url'].append(j.get_attribute('src'))
    element_list.append(img_list)

    full_list.append(element_list)

    driver.close()
    return full_list
