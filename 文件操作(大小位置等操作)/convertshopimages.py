import os
import re

from PIL import Image


def read_images(f_path):
    files = os.listdir(f_path)
    for file in files:
        if file == '.DS_Store':
            continue
        #修改名字:
        if os.path.isdir(os.path.join(f_path, file)):
            read_images(os.path.join(f_path, file))
        else:
            convert_image(f_path, file)


def convert_image(f_path, file):
    # 打开图片
    try:
        """
        big  600
        small 300   
        thumbnail  150
        """
        im = Image.open(os.path.join(f_path, file))
        file = re.sub(r'_big', '', file)
        # 生成_150的图片
        new_image = im.resize((150, 150), Image.ANTIALIAS)
        new_image.save(save_path(f_path, '_150.', file))
        new_image.save(save_path(f_path, '_thumbnail.', file))
        # 生成_400的图片
        new_image = im.resize((400, 400), Image.ANTIALIAS)
        new_image.save(save_path(f_path, '_400.', file))
        # 生成_small的图片 大小为 300 300
        new_image = im.resize((300, 300), Image.ANTIALIAS)
        new_image.save(save_path(f_path, '_small.', file))
        # 生成_600的图片
        # new_image = im.resize((600, 600), Image.ANTIALIAS)
        # new_image.save(save_path(f_path, '_big.', file))
    except Exception as e:
        print(e)


def save_path(f_path, name, file):
    file = re.sub(r'\.', name, file)
    s_path = os.path.join(f_path, file)
    return s_path


if __name__ == '__main__':
    f_path = '/Users/swift/Desktop/imgworker/originimages600'
    read_images(f_path)

