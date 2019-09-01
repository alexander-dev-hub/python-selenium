#-*- coding: utf-8 -*-
from selenium import webdriver
 
# firefox 웹 드라이버를 연다 
browser = webdriver.Firefox()
 
# 구글에 '파이썬 공부'로 검색어 조회
browser.get("http://sci-hub.tw/10.1063/1.3149495")





"""
# 결과 div 태그를 클래스 기준으로 검색해 다 가져옴.
results = browser.find_elements_by_css_selector('li.b_algo')
 
# 인자를 담을 리스트
hrefs = []
 
# div 중 최초 5개를 가져와서, 그 안에서 a 태그를 찾고, a 태그 안의 href 속성을 찾는다. 
for i in range(0, 5):
   link = results[i].find_element_by_tag_name("a")
   hrefs.append(link.get_attribute("href"))
 
# 화면에 그냥 프린트 해봄
for href in hrefs:
   print(href)
 
# 각 링크에 대해서 새 탭에서 연다
for href in hrefs:
   browser.execute_script('window.open("' + href + '","_blank");')
"""