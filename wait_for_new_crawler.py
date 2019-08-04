from selenium import webdriver
import time
from bs4 import BeautifulSoup


new_user = ''
last_user = ''

def crawl_one(hashtag, option = False):
    global new_user, last_user

    url = 'https://www.instagram.com/explore/tags/' + hashtag
    driver_addr = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chromedriver.exe'

    if option:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(driver_addr, chrome_options=options)

    else:
        driver = webdriver.Chrome(driver_addr)

    driver.implicitly_wait(5)

    driver.get(url)

    user_link_list = driver.find_elements_by_css_selector('div.v1Nh3.kIKUG._bz0w > a')
    new_user = user_link_list[9].get_attribute('href')

    while True:
        last_user = new_user
        driver.refresh()

        user_link_list = driver.find_elements_by_css_selector('div.v1Nh3.kIKUG._bz0w > a')
        new_user = user_link_list[9].get_attribute('href')

        if new_user == last_user:
            print('최신 게시물 없음')
        else:
            print('최신 게시물 등록됨!')

        time.sleep(1)




crawl_one('pycon', option=False)