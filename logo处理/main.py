from removelogo import read_image, change_image, SIFE_images, check_white_point_number, fill_image_with_white
from fileexecute import read_files, make_dir, get_file_path, all_files
from multiprocessing import Process, Pool, Queue, Manager, Value, Array, Lock

import numpy as np
import cv2
import argparse
import time


execute_files = Value('i', 0)
error_files = Value('i', 0)
g_lock = Lock()


"""
/Users/swift/Desktop/logonologo/logo/product_SJ1447914214_800 绵竹大曲.jpg
/Users/swift/Desktop/logonologo/logo/product_SJ1448863824_800 天立 350.jpg
/Users/swift/Desktop/logonologo/logo/御青绿茶礼盒904652.jpg
/Users/swift/Desktop/logonologo/logo/1513131260800162557318.jpeg
# 没有logo
/Users/swift/Desktop/logonologo/nologo/1512711500833842271778.jpeg
"""


def convert_image(img1, nologo_path, logo_path, error_path, q, lock):
    while True:
        if q.empty():
            time.sleep(60)
            #如果等待一秒还没有数据说明已经为空  退出程序
            if q.empty():
                break
        image_file = q.get()
        try:
            origin_img2 = read_image(image_file)
            img_arr2 = change_image(origin_img2)
            cv2.imwrite('img.png', img_arr2)
            img2 = cv2.imread('img.png')
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            dst, is_all_white = SIFE_images(img1, img2, gray1=gray1, gray2=gray2)
            if dst is not None:
                # num = check_white_point_number(img2, [np.int32(dst)])
                # 保存到处理目录
                if is_all_white:
                    fill_image_with_white(origin_img2, np.int32(dst))
                    cv2.imwrite(get_file_path(nologo_path, image_file), origin_img2)
                else:
                    # 有图处理不了的
                    cv2.imwrite(get_file_path(logo_path, image_file), origin_img2)
            else:
                # 保存到处理目录
                cv2.imwrite(get_file_path(nologo_path, image_file), origin_img2)
            global excute_files, g_lock
            with g_lock:
                execute_files.value += 1
        except Exception as e:
            print(e)
            cv2.imwrite(get_file_path(error_path, image_file), origin_img2)
            global error_files
            with g_lock:
                error_files.value += 1


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--ip", help="image to be processed")
    # parser.add_argument("--sp", help="image save path")
    # args = parser.parse_args()
    #
    # if args.ip:
    #     image_path = args.ip
    # if args.sp:
    #     save_path = args.sp

    # /Users/swift/Downloads/xunmall-shop-upload/

    image_path = '/Users/swift/Downloads/xunmall-shop-upload800/'
    save_path = '/Users/swift/Desktop/shopremovelogo800'
    # image_path = '/Users/swift/Desktop/ttttt'
    # save_path = '/Users/swift/Desktop/shoptest'
    # try:
    nologo_path, logo_path, error_path = make_dir(save_path)
    # except Exception as e:
    #     print(e)
    # image_files = read_files(image_path, q)

    origin_img1 = read_image('/Users/swift/Desktop/logonologo/logo/shop800.png')
    img_arr1 = change_image(origin_img1)
    cv2.imwrite('logo.png', img_arr1)
    img1 = cv2.imread('logo.png')
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    q = Manager().Queue()
    # 创建锁
    lock = Manager().Lock()
    # 创建进程池
    p = Pool(processes=4)
    # 添加读取数据进程
    p.apply_async(read_files, args=(image_path, q, lock))
    # read_files(image_path, q, lock)
    # 添加数据转换的进程
    p.apply_async(convert_image, args=(img1, nologo_path, logo_path, error_path, q, lock))
    p.apply_async(convert_image, args=(img1, nologo_path, logo_path, error_path, q, lock))
    p.apply_async(convert_image, args=(img1, nologo_path, logo_path, error_path, q, lock))
    p.close()
    p.join()

    print('all files num {}'.format(all_files.value))
    print('execute files num {}'.format(execute_files.value))
    print('error files num {}'.format(error_files.value))
    # for image_file in image_files:
