import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver  # selenium은 webdriver api를 통해 브라우저를 제어함
from selenium.webdriver.common.by import By  # https://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL및 드라이버 가동
main_url = 'http://search.mt.co.kr/'
keyword = '삼성전자'  # 요부분은 나중에 인풋값으로 받도록 수정
driver = webdriver.Chrome("C:/0.ITstudy/chromedriver.exe")
driver.get(main_url)

# 검색창에 키워드 입력
search = driver.find_element_by_xpath('//*[@id="kwd"]')
search.clear()
search.send_keys(keyword)
time.sleep(2)

# 검색 버튼 다시 클릭
btn_search = driver.find_element_by_xpath('//*[@id="mt_header"]/div/form/div/fieldset/input[2]')
btn_search.click()
btn_search.click()

time.sleep(1)
moreview_btn = driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[3]/span/a')
moreview_btn.click()

data1 = {"TIME": []}
data2 = {"TITLE": []}
data3 = {"BODY": []}


def getnews():
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        p1 = soup.find("div", {"class": "section"})
        items = p1.findAll("li", {"class": "bundle"})  # 리스트가 아니거나 없거나

        for item in items:
            global data2
            title = item.findAll("strong", {"class": "subject"})[0].text.strip()
            title1 = title.strip()

            data2['TITLE'].extend([title1])

            global data3
            body_date = item.find("p", {"class": "txt"})
            body = body_date.find('a').text.strip().replace(',', '').replace('\n', '').replace('\t', '')

            data3['BODY'].extend([body])

            global data1
            date_pre = body_date.find("span", {"class": "etc"}).text
            date = re.sub(r'[A-힣(\>\|\s\/\,\:\=)]', '', date_pre)

            data1['TIME'].extend([date])

        data3.update(data2)
        data1.update(data3)

        dataframe1 = pd.DataFrame(data1, columns=["TITLE", "BODY", "TIME"])
        dataframe1 = dataframe1.replace(',', '')

        newsfile = "C:/0.ITStudy/newsfile/" + keyword + ".csv"
        dataframe1.to_csv(newsfile, index=False)
        return dataframe1


    except WebDriverException as e:
        print("또 드라이버  에러....")
        pass

    finally:
        time.sleep(5)


def Paging():
    try:
        for i in range(2, 11):
            getnews()
            driver.find_element_by_xpath('//*[@id="paging_t17"]/span/a[' + str(i) + ']').click()
            time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="paging_t17"]/button[3]').click()
        time.sleep(0.5)
    except error as e:
        print("루핑 중 에러발생")


for i in range(11):
    Paging()