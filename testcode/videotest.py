from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains
import time

import urllib
from urllib.parse import urlsplit
from urllib.parse import quote_plus
from selenium.webdriver.common.by import By as WebBy
from selenium.webdriver.support.ui import Select as WebSelect

import cv2
import numpy as np

x_pos = 20
y_pos = 223

def allow_flash(driver, url):
    def _base_url(url):
        if url.find("://")==-1:
            url = "http://{}".format(url)
        urls = urlsplit(url)
        return "{}://{}".format(urls.scheme, urls.netloc)

    def _shadow_root(driver, element):
        return driver.execute_script("return arguments[0].shadowRoot", element)

    base_url = _base_url(url)
    driver.get("chrome://settings/content/siteDetails?site={}".format(quote_plus(base_url)))

    root1 = driver.find_element(WebBy.TAG_NAME, "settings-ui")
    shadow_root1 = _shadow_root(driver, root1)
    root2 = shadow_root1.find_element(WebBy.ID, "container")
    root3 = root2.find_element(WebBy.ID, "main")
    shadow_root3 = _shadow_root(driver, root3)
    root4 = shadow_root3.find_element(WebBy.CLASS_NAME, "showing-subpage")
    shadow_root4 = _shadow_root(driver, root4)
    root5 = shadow_root4.find_element(WebBy.ID, "advancedPage")
    root6 = root5.find_element(WebBy.TAG_NAME, "settings-privacy-page")
    shadow_root6 = _shadow_root(driver, root6)
    root7 = shadow_root6.find_element(WebBy.ID, "pages")
    root8 = root7.find_element(WebBy.TAG_NAME, "settings-subpage")
    root9 = root8.find_element(WebBy.TAG_NAME, "site-details")
    shadow_root9 = _shadow_root(driver, root9)
    root10 = shadow_root9.find_element(WebBy.ID, "plugins")  # Flash
    shadow_root10 = _shadow_root(driver, root10)
    root11 = shadow_root10.find_element(WebBy.ID, "permission")
    WebSelect(root11).select_by_value("allow")

def crop(image, y0, y1, x0,x1, image_name):
    #crop_image = image[y0:y1, x0:x1]
    #print(checkValid(crop_image))
    cv2.imwrite(image_name, image)

def checkValid(image):
    return np.sum(image) > 500

url = "http://www.dot.ca.gov/dist8/tmc/cctvhtm/cctv809409.html"
width = 300
height = 450
prefs = {
    "profile.default_content_setting_values.plugins": 1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
    "PluginsAllowedForUrls": url
}

dim = None
options = webdriver.ChromeOptions()
#options.add_argument("headless")
options.add_experimental_option("prefs",prefs)
#binary = FirefoxBinary('driver/geckodriver')
"""
profile = FirefoxProfile()
profile.set_preference("plugin.state.flash", 2)
with webdriver.Firefox(firefox_profile=profile) as driver:
"""
with webdriver.Chrome(chrome_options=options) as driver:
    allow_flash(driver, url)
    driver.set_window_size(width, height)
    driver.get(url)
    #time.sleep(3)
    video = driver.find_element_by_tag_name("embed")
    print(video.location)
    video.click()
    time.sleep(1.0)
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element_by_id("video")).move_by_offset( -140,103).click().perform()
    print("click_play")
    time.sleep(10)

    png = driver.get_screenshot_as_png()
    
    img = np.frombuffer(png, np.uint8)
    mat = cv2.imdecode(img, cv2.IMREAD_COLOR)
    print(type(img))
    name = 'data/test4.png'
    crop(mat,  12,311,29, 428,  name)

#driver.close()
