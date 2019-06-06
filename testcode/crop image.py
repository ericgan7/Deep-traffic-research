import cv2
import os
def crop(image_name, y0, y1, x0,x1):
    try:
        if not os.path.exists('data/crop image'):
            os.makedirs('data/crop image')
    except OSError:
        print ('Error: Creating directory of data')

    new_image_name = "data/video/"+image_name
    print(new_image_name)

    image = cv2.imread(new_image_name)
    crop_image = image[y0:y1, x0:x1]
    new_name = "data/crop image/" + image_name

    cv2.imwrite(new_name, crop_image)


image_path = os.getcwd() + "/data/video"

for file in os.listdir(image_path):
    print(file)
    crop(file, 12,311,29, 428)


# crop_image = image[25:622, 72:872]