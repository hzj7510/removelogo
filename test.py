from removelogo import read_image, change_image, SIFE_images, check_white_point_number, fill_image_with_white

import cv2
import numpy as np

if __name__ == '__main__':

    origin_img1 = read_image('/Users/swift/Desktop/logonologo/logo/big1.jpg')
    h, w = origin_img1.shape[:2]
    dst = [[[0, 0]], [[w, 0]], [[0, h]], [[w, h]]]
    num = check_white_point_number(origin_img1, [np.int32(dst)])
    print(num)