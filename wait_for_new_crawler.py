from selenium import webdriver
import time
from bs4 import BeautifulSoup
import multiprocessing


new_user = ''
last_user = ''


def crawl(hashtag, option = False):
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

            element_list = []
            driver.get(new_user)
            html = driver.page_source
            bs = BeautifulSoup(html, 'lxml')

            user_id = driver.find_element_by_css_selector('h2._6lAjh > a').get_attribute('title')
            print(user_id)

            try:
                user_profile_img = driver.find_element_by_css_selector('a._2dbep.qNELH.kIKUG > img').get_attribute('src')
                print(user_profile_img)
            except:
                print('None')

            div = bs.find('div', class_='C4VMK')
            span = div.find('span')
            print(span.text)

            img = driver.find_elements_by_css_selector('div.KL4Bh > img')
            img_link = img[0].get_attribute('src')
            print(img_link)

            driver.get(url)

        time.sleep(1)


if __name__ == '__main__':
    crawl('pycon', option=False)
