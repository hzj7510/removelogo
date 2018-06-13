import os
import time
import shutil

all_img_path = '/Users/swift/Desktop/WorkPic/shop库里的图片处理/800/xunmall-shop-upload'
is_convert_img_path = '/Users/swift/Desktop/WorkPic/shop库里的图片处理/800/shopremovelogo800/nologoimages'
purpose_path = '/Users/swift/Desktop/shopimgwoker800'


def read_images(f_path):
    files = os.listdir(f_path)
    for file in files:
        if file == '.DS_Store':
            continue
        if ext == '.webp':
            continue
        #修改名字:
        if os.path.isdir(os.path.join(f_path, file)):
            yield from read_images(os.path.join(f_path, file))
        else:
            yield (file, f_path)


if __name__ == '__main__':
    is_convert_img_list = os.listdir(is_convert_img_path)
    is_convert_img_set = set(is_convert_img_list)
    # is_convert_img_set = set()
    # for f in read_images(is_convert_img_path):
    #     img, _ = f
    #     is_convert_img_set.add(img)
    # time.sleep(70)
    for f in read_images(all_img_path):
        img, f_path = f
        if img not in is_convert_img_set:
            # 放到 purpose 文件夹内
            shutil.copy(os.path.join(f_path, img), purpose_path)


