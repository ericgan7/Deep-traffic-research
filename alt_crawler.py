from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import urllib
from urllib.parse import urlsplit, quote_plus
from selenium.webdriver.common.by import By as WebBy
from selenium.webdriver.support.ui import Select as WebSelect
import time
import datetime
import threading
import os
import numpy as np
import cv2 as cv

"""
"http://www.dot.ca.gov/d4/d4cameras/ct-cam-pop-S101_at_Poplar_Av.html",
            "http://www.dot.ca.gov/d4/d4cameras/ct-cam-pop-W4_JWO_Hillcrest_Av.html",
            "http://www.dot.ca.gov/d4/d4cameras/ct-cam-pop-W4_JWO_Railroad_Av.html",
            "http://www.dot.ca.gov/d4/d4cameras/ct-cam-pop-W4_JWO_Railroad_Av.html",
            "http://www.dot.ca.gov/d4/d4cameras/ct-cam-pop-W4_JWO_Railroad_Av.html",
            "http://www.dot.ca.gov/d4/d4cameras/Wowza-Camera-Popup.html",
            """

class Crawler():
    def __init__(self):
        self.urls = [
            "http://www.dot.ca.gov/dist8/tmc/cctvhtm/cctv809409.html"
        ]
        self.width = 300
        self.height = 500

        prefs = {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
            "PluginsAllowedForUrls": self.urls
        }
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", prefs)
        self.iterations = 10
        self.threads = []
        try:
            os.mkdir('data')
        except:
            pass
        try:
            os.mkdir('data/video')
        except:
            pass

    def Start(self):
        self.GetCropDim()
        try:
            for i, u in enumerate(self.urls):
                t = Screenshot(i, u, self.options, self.width, self.height, self.dim)
                self.threads.append(t)
                t.start()
            
            print("Finished starting")
            for t in self.threads:
                t.join()
            print("Finished data collection")
        except KeyboardInterrupt:
            print("Interrupt")
            for t in self.threads:
                t.driver.close()

    ## TODO MODIFY CROP DIMENSIONS
    def GetCropDim(self):
        temp = Screenshot(0, self.urls[0], self.options, self.width, self.height, dim = None)
        temp.initialize_browser()
        img = temp.get_image()

        #Assuming video is somewhat centered
        x_mid = img.shape[1] // 2
        y_start, x_start = 0, 0
        y_end, x_end = img.shape[0] - 1, img.shape[1] - 1
        self.dim = [y_start, y_end, x_start, x_end]
        
        #find y_start
        while (img.item((y_start, x_mid, 0)) == 255):
            y_start += 1
        self.dim[0] = y_start
        #find y_end
        y_end = y_start
        while(img.item((y_end, x_mid, 0)) != 255):
            y_end += 1
        self.dim[1] = y_end
        #find x_start and x_end
        for i in range(y_start, y_start +100):
            while (img.item(i, x_start, 0) == 255):
                x_start += 1
            while (img.item(i, x_end,0) == 255):
                x_end -= 1
        self.dim[2], self.dim[3] = x_start, x_end
        print(self.dim)
        temp.driver.close()

class Screenshot(threading.Thread):
    def __init__(self, id, url, options, width, height, dim):
        threading.Thread.__init__(self)
        self.thread_ID = id
        self.url = url
        self.options = options
        self.w = width
        self.h = height
        self.dim = dim

    def allow_flash(self, driver, url):
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

    def run(self):
        self.initialize_browser()
        while (True):
            t = datetime.datetime.now()
            name = "data/video/{7},{0}-{1}-{2},{3}-{4}-{5}-{6}.png".format(t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond, "test")
            img = self.get_image()
            self.crop(img, self.dim[0], self.dim[1], self.dim[2], self.dim[3], name)
            

    def get_image(self):
        png = self.driver.get_screenshot_as_png()
        nppng = np.frombuffer(png, np.uint8)
        img = cv.imdecode(nppng, cv.IMREAD_COLOR)
        return img

    def initialize_browser(self, blocking = False):
        print("init thread at {0}".format(self.url[35:]))
        if (blocking):
            barrier.wait()
        self.driver = webdriver.Chrome(chrome_options = self.options)
        self.allow_flash(self.driver, self.url)
        self.driver.set_window_size(self.w, self.h)
        self.driver.get(self.url)
        self.driver.find_element_by_tag_name("embed").click()
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("video")).perform()
        time.sleep(1.0)
        ActionChains(self.driver).move_by_offset( -140,103).click().perform()
        while(not self.ready()):
            pass
        print("{0} Ready".format(self.thread_ID))
        if (blocking):
            barrier.wait()

    def crop(self, image, y0, y1, x0,x1, image_name):
        crop_image = image[y0:y1, x0:x1]
        if (self.valid(crop_image)):
            #cv.imwrite(image_name, crop_image)
            print("save at {0}".format(image_name))
        else:
            self.driver.close()
            self.initialize_browser()

    def valid(self, image):
        return np.sum(image) > 100

    def ready(self):
        png = self.driver.get_screenshot_as_png()
        nppng = np.frombuffer(png, np.uint8)
        img = cv.imdecode(nppng, cv.IMREAD_COLOR)
        if (not self.dim):
            return True
        else:
            crop_image = img[self.dim[0]:self.dim[1], self.dim[2]:self.dim[3]]
            return self.valid(crop_image)
    
if __name__ == '__main__':
    crawler = Crawler()
    barrier = threading.Barrier(len(crawler.urls))
    crawler.Start()


