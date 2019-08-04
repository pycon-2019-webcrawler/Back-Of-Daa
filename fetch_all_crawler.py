from selenium import webdriver
import selenium
import time
from bs4 import BeautifulSoup

def crawl(hashtag, option = False):
    '''
    지금 쓰는 chrome의 버전과 같은 버전의 chrome driver 다운로드 받아주세요! => https://chromedriver.chromium.org/downloads
    chrome driver가 있는 주소로 driver_addr 수정해주세요!
    #빼고 해시태그 내용을 파라미터로 받아서 크롤링된 내용을 리스트로 리턴합니다.
    option 파라미터에 true값을 넣으면 chrome 창 없이 크롤러가 돌아갑니다.
    사진이 없는 게시물의 경우(동영상) 크롤링이 오래걸립니다.

    :param hashtag:
    :param option = False:
    :return: crawled_list
    '''
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

    for i in user_link_list[9:]:
        element_list = []
        driver.get(i)
        html = driver.page_source
        bs = BeautifulSoup(html, 'lxml')

        user_id = driver.find_element_by_css_selector('h2._6lAjh > a')
        element_list.append({'username': user_id.get_attribute('title')})

        try:
            user_profile_img = driver.find_element_by_css_selector('a._2dbep.qNELH.kIKUG > img')
            element_list.append({'profile_img': user_profile_img.get_attribute('src')})
        except selenium.common.exceptions.NoSuchElementException:
            element_list.append({'profile_img': None})

        div = bs.find('div', class_='C4VMK')
        span = div.find('span')
        element_list.append({'text': span.text})

        try:
            img = driver.find_element_by_css_selector('div.KL4Bh > img')
            element_list.append({'img': img.get_attribute('src')})
        except selenium.common.exceptions.NoSuchElementException:
            element_list.append({'img': None})

        full_list.append(element_list)

    driver.close()
    return full_list
