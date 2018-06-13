import cv2
import os
import numpy as np


def read_images(f_path):
    files = os.listdir(f_path)
    for file in files:
        if file == '.DS_Store' or file == '.gitkeep':
            continue
        #修改名字:
        if os.path.isdir(os.path.join(f_path, file)):
            yield from read_images(os.path.join(f_path, file))
        else:
            yield (file, f_path)


def read_image(path):
    return cv2.imread(path)


def imageRGBtonum(img):
    read_img_num = []
    for row in img:
        row_num = [sum(x) for x in row]
        read_img_num.append(row_num)
    return np.array(read_img_num)


def col_white_line(img):
    isfirst = True
    isallwhite = True
    for index, col_num in enumerate(range(len(img[0]))):
        isallwhite = True
        for x in img[:,col_num]:
            if(x < 660):
                isallwhite = False
                isfirst = False
                break
        if not isfirst and isallwhite:
            return index


def col_splite(img, index):
    return img[:, index:]


def row_white_line(img):
    isfirst = True
    isallwhite = True
    for index, row_num in enumerate(range(len(img))):
        isallwhite = True
        for x in img[row_num]:
            if(x < 660):
                isallwhite = False
                isfirst = False
                break
        if not isfirst and isallwhite:
            return index


def row_splite(img, index):
    return img[:index, :]


if __name__ == '__main__':
    for x in read_images('/Users/swift/Desktop/imgworker/shopimgwoker800'):
        try:
            f, fp = x
            read_img = read_image(os.path.join(fp, f))
            read_image_num = imageRGBtonum(read_img)
            total_col = len(read_image_num[0])
            total_row = len(read_image_num)
            col_index = col_white_line(read_image_num)
            splite_img = col_splite(read_image_num, col_index)
            row_index = row_white_line(splite_img)
            if col_index > 0 and col_index > 300 and row_index > 0 and row_index < 300:
                cv2.rectangle(read_img, (col_index, 0), (total_row, row_index), (255, 255, 255), -1)
                cv2.imwrite(os.path.join('/Users/swift/Desktop/imgworker/colimg800', f), read_img)
                print(col_index, row_index)
            else:
                print(False)
        except Exception as e:
            print(e)
