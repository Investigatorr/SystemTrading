import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver # selenium은 webdriver api를 통해 브라우저를 제어함
from selenium.webdriver.common.by import By #https://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

'''
conn = MongoClient('localhost', 27017)
db = conn['hkDB']
collection = db['hk']
collection.drop()
'''

main_url = 'http://search.hankookilbo.com/v2/?sword=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&stype=&ssort=1&sdate=&edate=&sfield=&cate_str=&PID=dreamwiz&ptn_name=hankookilbo&cddtc=hankookilbo'
driver = webdriver.Chrome("C:/0.ITstudy/chromedriver.exe")
driver.get(main_url)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, "html.parser" ) 


p1 = soup.find("ul", {"class" : "article-list"})
#print(p1)
items = p1.findAll("li", {"class" : "item"})     # 리스트가 아니거나 없거나
#print(items)


try:
    for item in items:
        title = item.findAll("p", {"class" : "title"})[0].text
        #print(title)
        
        body = item.findAll("p", {"class" : "preview"})[0].text
        #print(body)
        
        date = item.find("span", {"class" : "time"}).text
        print(date)
        
except Exception as e:
    print("---페이지 파싱 에러", e)

finally:
    driver.close()