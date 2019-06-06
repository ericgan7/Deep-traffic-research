import cv2
import numpy as np

image = cv2.imread("data/test2/ct-cam-pop-E4_at_Laurel_Rd.html,2019-6-4,14-52-39.png", 1)
image2 = cv2.imread("data/test2/ct-cam-pop-N680_Before_N680_W780_Split.html,2019-6-4,14-55-56.png", 1)
# cv2.imshow("test", image)
# cv2.waitKey(0)
# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
# contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# cnt = contours[0]
# x,y,w,h = cv2.boundingRect(cnt)
# print(x,y,w,h)
# print(image.shape)

print(image.shape)
print(image2.shape)

x_list = [654,0]
count1 = 0
for i in range(len(image)):
    count = 0
    for j in range(len(image[i])):
        if np.array_equal(image[i][j], image2[i][j]) == True:
            count+=1
            # print(i,j)
    if count < 900:
        if i < x_list[0]:
            x_list[0] = i
        elif i > x_list[1]:
            x_list[1] = i

print(x_list)

y_list = [1000, 0]
for j in range(len(image[35])):

    if np.array_equal(image[35][j], image2[35][j]) != True:

        if j < y_list[0]:
            y_list[0] = j
        elif j > y_list[1]:
            y_list[1] = j
print(y_list)






