import cv2
import numpy as np
def miss_line(img,border_size = 20):
    cropped_img_with_border = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, 
                                             cv2.BORDER_CONSTANT, value=(255, 255, 255))
    return cropped_img_with_border

    