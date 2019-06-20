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
    browser.find_element_by_id("username").send_keys("")
    browser.find_element_by_id ("password").send_keys("")
    browser.find_element_by_name("login").click()

    page_specific(browser, tab)
    browser.quit()

def page_specific(browser, tab, start_time = "01/2019", end_time = "06/2019", lane_type = "All", quantity = "Vehicle Miles Traveled (VMT)"):
    #wait until the table fully loads
    element = WebDriverWait(browser, 10).until(lambda x:    x.find_element_by_id('rpt_vars'))

    # start period (format: MM/YYYY)
    # browser.find_element_by_id("s_time_id_f").send_keys(start_time)
    # #end period (format: MM/YYYY)
    # browser.find_element_by_id("e_time_id_f").send_keys(end_time)

    #select lane type
    # ltype = Select(browser.find_element_by_name("ltype"))
    # ltype.select_by_visible_text(lane_type)

    #select quantity reported
    # q = Select(browser.find_element_by_name("q"))
    # q.select_by_visible_text(quantity)

    #select all routes
    select_route = browser.find_element_by_id("available_routes")
    all_options = select_route.find_elements_by_tag_name("option")

    # Create an new Excel file and add a worksheet.
    timestamp = str(datetime.now()).split('.')[0]
    workbook = xlsxwriter.Workbook('{}{}.xlsx'.format(tab, timestamp))
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 2, quantity)

    first_write = True

    # for option in all_options:
        # option.click()

    for j in range(0, int(len(all_options)/15)):
        unselect_route = browser.find_element_by_id("selected_routes")
        unselect = unselect_route.find_elements_by_tag_name("option")

        for u in unselect:
            u.click()

        browser.find_element_by_id("removeRoute").click()

        select_route = browser.find_element_by_id("available_routes")
        all_options = select_route.find_elements_by_tag_name("option")

        if j > 0:
            for i in range((j-1)*15,(j-1)*15+15):
                all_options[i].click()

        for i in range(j*15,j*15+15):
            all_options[i].click()

        browser.find_element_by_id("addRoute").click()
        browser.find_element_by_name("html").click()
        element = WebDriverWait(browser, 10).until(lambda x:    x.find_element_by_id('bts_report_results'))

        #extract data from the table
        soup = BS(browser.page_source, "html5lib")
        table = soup.find("div", {"id": 'bts_report_results'});
        headings = table.findAll('th')

        if first_write == True:
            c = 0

            for i in range(2,len(headings)):
                worksheet.write(1, c, headings[i].text)
                c += 1

            c = 0
            r = 2
            first_write = False

        rows = table.findAll('tr')
        for row in range(2, len(rows)):
            cols = rows[row].find_all('td')
            for col in cols:
                worksheet.write(r, c, col.text)
                c += 1
            r += 1
            c = 0

    print("written in {}{}.xlsx".format(tab, timestamp))
    workbook.close()

def main():
    webcrawler("http://pems.dot.ca.gov/?dnode=State&", "routes", "route_time_comparison")

if __name__ == '__main__':
    main()
