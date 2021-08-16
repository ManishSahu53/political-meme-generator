# importing the module
import os

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from src import util
from src import click_event_util

path_base = 'data'
path_data = util.list_list(path_base, '')


# reading the image
img = cv2.imread(path_data[0], 1)
clone = img.copy()

# displaying the image
# cv2.imshow('image', img)

# # setting mouse hadler for the image
# # and calling the click_event() function
# cv2.setMouseCallback('image', click_event_util.click_event, img)
# # wait for a key to be pressed to exit
# cv2.waitKey(0)
# # close the window
# cv2.destroyAllWindows()

rectangle = []
# img = np.zeros((100, 500, 3), np.uint8)
cv2.imshow('image', img)
p0 = -1, -1
p1 = -1, -1

while 1:
    cv2.setMouseCallback('image', click_event_util.draw_rectangle, (img, rectangle))
    k = cv2.waitKey(0)
    print('key: ', k)

    if k == 27:
        # Esc
        print('ESC')
        cv2.destroyAllWindows()
        break

    elif k == ord('r'):
        # reset
        print('Reset')
        rectangle = []
        img = clone.copy()

    else:
        break

print(f'Rectangle: {rectangle}')
cv2.destroyAllWindows()
