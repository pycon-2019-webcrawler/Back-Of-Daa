from selenium import webdriver
import time
from bs4 import BeautifulSoup
import multiprocessing

# 새로 refresh해서 얻어온 값과 전에 얻어온 값을 비교하기 위해 선언한 변수
new_user = ''
last_user = ''


def crawl(hashtag, option = False):
    count = 0
    global new_user, last_user

    # 크롤링을 할 url 설정
    url = 'https://www.instagram.com/explore/tags/' + hashtag
    # chromedriver 설치해서 다음과 같은 경로에 두세요.
    driver_addr = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chromedriver.exe'

    # 크롬 창 안 띄우기
    if option:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(driver_addr, chrome_options=options)

    # 크롬 창 띄우기
    else:
        driver = webdriver.Chrome(driver_addr)

    # 페이지 로딩을 위한 대기
    driver.implicitly_wait(5)

    # 해당 url로 접속하기
    driver.get(url)

    # html 코드에서 게시물 등록한 user의 link 값 리스트로 얻어오기
    user_link_list = driver.find_elements_by_css_selector('div.v1Nh3.kIKUG._bz0w > a')
    # 9 번째 요소(가장 최신에 글을 등록한 유저의 link) 값 따와서 new_user에 저장하기 (이 작업은 값을 비교하기 전에 default 같은 개념으로 한 것이다.)
    new_user = user_link_list[9].get_attribute('href')

    # 무한 반복
    while True:
        # 계속 refresh하면 튕겨져서 refresh 횟수 테스트용 변수
        count = count + 1
        print(f'{count}번 째: ', end='')

        # new_user(전 while문에서 가져온 값을 last_user값에 대입한다.)
        last_user = new_user
        # 그리고 페이지 refresh
        driver.refresh()

        # 가장 최신으로 등록된 게시물의 user link 값을 받아와서 new_user값에 대입(while문 전 코드와 동일)
        user_link_list = driver.find_elements_by_css_selector('div.v1Nh3.kIKUG._bz0w > a')
        new_user = user_link_list[9].get_attribute('href')

        # 만약 이번 while문에서 받아온 new_user값과 저번 while문에서 받아온 last_user값을 비교해서 같으면 최신 게시물이 없다고 판단.
        if new_user == last_user:
            print('최신 게시물 없음')

        # 하지만 두 값이 서로 다르다면, 최신 게시물이 등록됬다고 판단하여 그 게시물에 대한 정보를 따온다.
        # 근데 이게 문제가 되는게 가장 최신 게시물이 삭제되면 그 전 게시물이 최신 게시물인 것으로 판단되어서 전 게시물에 대한 정보를 출력하는데,
        # 이건 등록된 시간 따와서 현재 시간이랑 비교하면서 해야 될 것 같음.
        else:
            print('최신 게시물 등록됨!')

            driver.get(new_user)
            html = driver.page_source
            bs = BeautifulSoup(html, 'lxml')

            user_id = driver.find_element_by_css_selector('h2._6lAjh > a').get_attribute('title')
            print(user_id)

            # 유저 이미지가 없을 경우의 예외처리 (근데 유저 이미지가 없던 적을 못봄, 이미지 기본 값이면 기본 이미지라도 반환됨)
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

            # 게시물에 대한 값 다 따왔으면 다시 게시물으로 돌아가는 코드
            driver.get(url)

        # Dos공격으로 인식 받기 싫으면 이 코드 써야됨!
        time.sleep(1.5)


if __name__ == '__main__':
    crawl('pycon', option=False)
