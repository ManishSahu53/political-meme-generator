import cv2
import numpy as np


# function to display the coordinates of
# of the points clicked on the image 
def click_event(event, x, y, flags, img):
  
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
  
    # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)


def draw_rectangle(event, x, y, flags, params):
    # params = (img, rectangle)
    img, rectangle = params
    RED = (0, 0, 255)
    global p0, p1
    
    if event == cv2.EVENT_LBUTTONDOWN:
        p0 = x, y
        # print('EVENT_LBUTTONDOWN', p0)

    elif event == cv2.EVENT_MOUSEMOVE and flags == 1:
        p1 = x, y
        # print('EVENT_MOUSEMOVE', p1)

    elif event == cv2.EVENT_LBUTTONUP:
        p1 = x, y
        rectangle.append([p0, p1])
        # print('EVENT_LBUTTONUP', p1)
        cv2.rectangle(img, p0, p1, RED, 2)
        cv2.imshow('image', img)