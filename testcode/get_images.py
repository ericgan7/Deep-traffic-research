from pattern.web import URL, DOM, extension, MIMETYPE_IMAGE
from pattern.web import Element, download
import urllib
import datetime

#libraries to check urllib (legacy vs not), pattern, requests
url = URL("http://www.dot.ca.gov/dist1/d1tmc/allcams.php")
dom = DOM(url.download(cached = True))
i = 0
try :
    for e in dom.by_tag('img'):
        if (extension(e.attr['src']) == '.jpg'):
            print(e.attr['src'])
            urllib.request.urlretrieve(e.attr['src'], "data/test/urllib{0}.jpg".format(i))
            #image = download(e.attr['src'], unicode= False, timeout= 5)
            #f = open("data/test/pattern{0}.jpg".format(i), 'wb')
            #f.write(image)
            i += 1
except:
    print ("error")
        
"""
image = "http://www1.dot.ca.gov/cwwp2/data/d1/cctv/image/us101northofcushingcreeklookingsouth/us101northofcushingcreeklookingsouth.jpg"
url = URL(image)
print (url.mimetype in MIMETYPE_IMAGE)
urllib.request.urlretrieve(image, 'data/test2.jpg')
"""

