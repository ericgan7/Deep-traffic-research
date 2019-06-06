from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
import xlsxwriter

#start a remote browser
browser = webdriver.Firefox()
URL = "http://pems.dot.ca.gov/?dnode=State&"
content = "routes"
tab = "route_list"

browser.get(URL + "content=" + content + "&tab=" + tab)

#login
browser.find_element_by_id("username").send_keys("ao1385@nyu.edu")
browser.find_element_by_id ("password").send_keys("11green!*Wca")
browser.find_element_by_name("login").click()

#wait until the table fully loads
element = WebDriverWait(browser, 10).until(lambda x:    x.find_element_by_id('routesTable'))

# #extract data from the table
soup = BS(browser.page_source, "html5lib")

i = 1

# Create an new Excel file and add a worksheet.
# workbook = xlsxwriter.Workbook('route_list.xlsx')
# worksheet = workbook.add_worksheet()

# labels = soup.find_all("span", "yui-dt-label")
# for l in labels:
#     print(l.text)
#     worksheet.write('A'+str(i), l.text)
#     i += 1

liners = soup.find_all("div", "yui-dt-liner")
for l in liners:
    print(l.text, end=" ")

# workbook.close()
browser.quit()
