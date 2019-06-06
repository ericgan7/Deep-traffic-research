from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
from datetime import datetime
import xlsxwriter

def webcrawler(url, content):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.download.folderList", 2);
    profile.set_preference("browser.download.dir", "/home/ao1385@ubuntu/Downloads")

    #start a remote browser
    browser = webdriver.Firefox(profile)
    URL = url


    browser.get(URL + content)

    #login
    browser.find_element_by_id("username").send_keys("ao1385@nyu.edu")
    browser.find_element_by_id ("password").send_keys("11green!*Wca")
    browser.find_element_by_name("login").click()


    page_specific(browser)
    browser.quit()

def page_specific(browser):
    table = browser.find_element_by_name("xls").click()

    pass

def main():
    webcrawler("http://pems.dot.ca.gov/?dnode=Freeway&", "&fwy=10&dir=E")

if __name__ == '__main__':
    main()
