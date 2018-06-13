from removelogo import read_image, change_image, check_white_point_number, fill_image_with_white  #, SIFE_images
from fileexecute import read_files, make_dir, get_file_path, all_files
from multiprocessing import Process, Pool, Queue, Manager, Value, Array, Lock

import numpy as np
import cv2
import argparse
import time


execute_files = Value('i', 0)
error_files = Value('i', 0)
g_lock = Lock()
MIN_MATCH_COUNT = 4


"""
/Users/swift/Desktop/logonologo/logo/product_SJ1447914214_800 绵竹大曲.jpg
/Users/swift/Desktop/logonologo/logo/product_SJ1448863824_800 天立 350.jpg
/Users/swift/Desktop/logonologo/logo/御青绿茶礼盒904652.jpg
/Users/swift/Desktop/logonologo/logo/1513131260800162557318.jpeg
# 没有logo
/Users/swift/Desktop/logonologo/nologo/1512711500833842271778.jpeg
"""


def SIFE_images():

    # img1 = cv2.imread('/Users/swift/Desktop/logonologo/logo/big1.jpg')
    origin_img1 = read_image('/Users/swift/Desktop/logonologo/logo/big1.jpg')
    img_arr1 = change_image(origin_img1)
    cv2.imwrite('logo.png', img_arr1)
    img1 = cv2.imread('logo.png')
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)


    # img2 = cv2.imread('/Users/swift/Downloads/xunmall-shop-upload/20171225/20171225084226227_big.jpg')
    # /Users/swift/Downloads/xunmall-shop-upload/20171225/20171225084226227_big.jpg
    origin_img2 = read_image('/Users/swift/Downloads/xunmall-shop-upload/20171228/20171228022705460_big.jpg')
    img_arr2 = change_image(origin_img2)
    cv2.imwrite('img.png', img_arr2)
    img2 = cv2.imread('img.png')
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


    # gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    ## (2) Create SIFT object
    sift = cv2.xfeatures2d.SIFT_create()

    ## (3) Create flann matcher
    matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), {})

    ## (4) Detect keypoints and compute keypointer descriptors
    kpts1, descs1 = sift.detectAndCompute(gray1, None)
    kpts2, descs2 = sift.detectAndCompute(gray2, None)

    ## (5) knnMatch to get Top2
    matches = matcher.knnMatch(descs1, descs2, 2)
    # Sort by their distance.
    matches = sorted(matches, key=lambda x: x[0].distance)

    ## (6) Ratio test, to get good matches.
    good = [m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]

    canvas = img2.copy()

    ## (7) find homography matrix
    ## 当有足够的健壮匹配点对（至少4个）时
    if len(good) > MIN_MATCH_COUNT:
        ## 从匹配中提取出对应点对
        ## (queryIndex for the small object, trainIndex for the scene )
        src_pts = np.float32([kpts1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kpts2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        ## find homography matrix in cv2.RANSAC using good match points
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        ## 掩模，用作绘制计算单应性矩阵时用到的点对
        # matchesMask2 = mask.ravel().tolist()
        ## 计算图1的畸变，也就是在图2中的对应的位置。
        h, w = img1.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        ## 绘制边框
        cv2.polylines(canvas, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))

    ## (8) drawMatches
    matched = cv2.drawMatches(img1, kpts1, canvas, kpts2, good, None)  # ,**draw_params)

    ## (9) Crop the matched region from scene
    h, w = img1.shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    # print(dst)
    perspectiveM = cv2.getPerspectiveTransform(np.float32(dst), pts)
    found = cv2.warpPerspective(img2, perspectiveM, (w, h))



    ## (10) save and display
    # cv2.imwrite("matched.png", matched)
    # cv2.imwrite("found.png", found)
    # found_im = cv2.imread('found.png')

    # print(found)
    left_col = found[:, 0]
    # print(left_col)
    # print(found[:, -1])

    for x in left_col:
        if np.array_equal(x, [0, 0, 0]):
            print('0')
        else:
            print('not all black ~ ')
            break

    print(check_white_point_number(origin_img1, [[[[0, 0]], [[0, 148]], [[155, 0]], [[155, 148]]]]))
    print(check_white_point_number(found, [[[[0, 0]], [[0, 148]], [[155, 0]], [[155, 148]]]]))
    #
    # cv2.imshow("matched", matched);
    # cv2.imshow("found", found);
    # cv2.waitKey();
    # cv2.destroyAllWindows()


# def convert_image(img1, gray1,image_file):
#     # while True:
#     #     if q.empty():
#     #         time.sleep(60)
#     #         #如果等待一秒还没有数据说明已经为空  退出程序
#     #         if q.empty():
#     #             break
#     #     image_file = q.get()
#     #     try:
#     origin_img2 = read_image(image_file)
#     img_arr2 = change_image(origin_img2)
#     cv2.imwrite('img.png', img_arr2)
#     img2 = cv2.imread('img.png')
#     gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#
#     SIFE_images(img1, gray1=gray1, gray2=gray2)
        #     if dst is not None:
        #         num = check_white_point_number(img2, [np.int32(dst)])
        #         # 保存到处理目录
        #         if num > 0.4:
        #             fill_image_with_white(origin_img2, np.int32(dst))
        #             cv2.imwrite(get_file_path(nologo_path, image_file), origin_img2)
        #         else:
        #             # 有图处理不了的
        #             cv2.imwrite(get_file_path(logo_path, image_file), origin_img2)
        #     else:
        #         # 保存到处理目录
        #         cv2.imwrite(get_file_path(nologo_path, image_file), origin_img2)
        #     global excute_files, g_lock
        #     with g_lock:
        #         execute_files.value += 1
        # except Exception as e:
        #     cv2.imwrite(get_file_path(error_path, image_file), origin_img2)
        #     global error_files
        #     with g_lock:
        #         error_files.value += 1


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

    # image_path = '/Users/swift/Downloads/xunmall-shop-upload'
    # save_path = '/Users/swift/Desktop/shopremovelogo'
    # try:
    # nologo_path, logo_path, error_path = make_dir(save_path)
    # except Exception as e:
    #     print(e)
    # image_files = read_files(image_path, q)

    # origin_img1 = read_image('/Users/swift/Desktop/logonologo/logo/big1.jpg')
    # img_arr1 = change_image(origin_img1)
    # cv2.imwrite('logo.png', img_arr1)
    # img1 = cv2.imread('logo.png')
    # gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    SIFE_images()


    # convert_image(img1, gray1, '/Users/swift/Downloads/xunmall-shop-upload/20171225/20171225084226227_big.jpg')
    # q = Manager().Queue()
    # # 创建锁
    # lock = Manager().Lock()
    # # 创建进程池
    # p = Pool(processes=4)
    # # 添加读取数据进程
    # p.apply_async(read_files, args=(image_path, q, lock))
    # # read_files(image_path, q, lock)
    # # 添加数据转换的进程
    # p.apply_async(convert_image, args=(img1, nologo_path, logo_path, error_path, q, lock))
    # p.apply_async(convert_image, args=(img1, nologo_path, logo_path, error_path, q, lock))
    # p.apply_async(convert_image, args=(img1, nologo_path, logo_path, error_path, q, lock))
    # p.close()
    # p.join()

    # print('all files num {}'.format(all_files.value))
    # print('execute files num {}'.format(execute_files.value))
    # print('error files num {}'.format(error_files.value))
    # for image_file in image_files:
