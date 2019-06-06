from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
from datetime import datetime
import xlsxwriter

def webcrawler(url, content, tab):
    #start a remote browser
    browser = webdriver.Firefox()
    URL = url
    content = content
    tab = tab

    browser.get(URL + "content=" + content + "&tab=" + tab)

    #login
    browser.find_element_by_id("username").send_keys("ao1385@nyu.edu")
    browser.find_element_by_id ("password").send_keys("11green!*Wca")
    browser.find_element_by_name("login").click()
    page_specific(browser, tab)
    browser.quit()

def page_specific(browser, tab, start_date = "06/05/2019", end_date = "06/05/2019"):
    element = WebDriverWait(browser, 100).until(lambda x:    x.find_elements_by_class_name('inlayTable'))
    get_fwy = BS(browser.page_source, "html5lib")
    filename = get_fwy.findAll("div", {"id": "std_liquid_segment_name"})[0].text.split("Freeway")[1]
    filename = filename.split()[0]

    workbook = xlsxwriter.Workbook('{}{}.xlsx'.format(filename,"-06-04-2019"))
    cell_format = workbook.add_format()
    cell_format.set_bold()      # Turns bold on.

    for i in range(0, 2):
        get_fwy = BS(browser.page_source, "html5lib")
        sheetname = get_fwy.findAll("div", {"id": "std_liquid_segment_name"})[0].text.split("Freeway")[1]
        sheetname = sheetname.split()[0]
        print(sheetname)
        worksheet = workbook.add_worksheet(sheetname)

        # set start date
        browser.find_element_by_id("s_time_id_f").clear()
        browser.find_element_by_id("s_time_id_f").send_keys(start_date)

        browser.find_element_by_id("e_time_id_f").clear()
        browser.find_element_by_id("e_time_id_f").send_keys(end_date)

        browser.find_element_by_name("html").click()

        # wait until table loads
        element = WebDriverWait(browser, 100).until(lambda x:    x.find_elements_by_class_name('inlayTable'))

        # scrape from html
        soup = BS(browser.page_source, "html5lib")
        table = soup.find("table", {"class":"inlayTable"})
        headings = table.find('thead').findAll('th')

        c = 0
        r = 0

        for heading in headings:
            if(heading.text == "Sum Flow by Hour"):
                continue
            worksheet.write(r, c, heading.text, cell_format)
            c += 1

        c = 0
        r += 1

        entries = table.find('tbody').findAll('tr')

        for entry in entries:
            vals = entry.findAll('td')
            for val in vals:
                worksheet.write(r, c, val.text)
                c += 1
            r += 1
            c = 0

        if i == 0:
            sections = browser.find_elements_by_class_name("segmentPanelSection")
            hrefs = sections[2].find_elements_by_tag_name("a")
            hrefs[0].click()

        sections = browser.find_elements_by_class_name("segmentPanelSection")
        # print(sections)
        selects = sections[2].find_elements_by_tag_name("form")
        if(len(selects) > 1):
            options = selects[1].find_elements_by_tag_name("option")
        else:
            options = selects[0].find_elements_by_tag_name("option")
        options[i + 1].click()
        element = WebDriverWait(browser, 100).until(lambda x:    x.find_elements_by_class_name('inlayTable'))
        page_specific(browser, tab)

    workbook.close()


def main():
    webcrawler("http://pems.dot.ca.gov/?dnode=Freeway&", "spatial", "hour&fwy=10&dir=E")

if __name__ == '__main__':
    main()
