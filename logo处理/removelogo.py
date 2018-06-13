import cv2
import numpy as np


MIN_MATCH_COUNT = 4
fill_color = (255, 255, 255)


# def read_image(img_name, isLogo):
#     origin_img = cv2.imread(img_name)
#     img_arr = change_image(origin_img)
#     if isLogo:
#         cv2.imwrite('logo.png', img_arr)
#         img1 = cv2.imread('logo.png')
#     else:
#         cv2.imwrite('image.png', img_arr)
#         img1 = cv2.imread('image.png')
#     gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     return gray

def read_image(img_name):
    return cv2.imread(img_name)


def change_image(img):
    img_arr = []
    for x in img:
        sub_img = []
        for y in x:
            if sum(y) > 660:
                sub_img.append([255, 255, 255])
            else:
                sub_img.append([0, 0, 0])
        img_arr.append(sub_img)
    return np.array(img_arr)


def SIFE_images(img1, img2, gray1, gray2):
    sift = cv2.xfeatures2d.SIFT_create()
    matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), {})
    kpts1, descs1 = sift.detectAndCompute(gray1, None)
    kpts2, descs2 = sift.detectAndCompute(gray2, None)

    matches = matcher.knnMatch(descs1, descs2, 2)
    matches = sorted(matches, key=lambda x: x[0].distance)

    good = [m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]
    # canvas = img2.copy()

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
        if dst is not None:
        ## 绘制边框
        # cv2.polylines(canvas, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
            perspectiveM = cv2.getPerspectiveTransform(np.float32(dst), pts)
            found = cv2.warpPerspective(img2, perspectiveM, (w, h))
            left_col = found[:, 0]
            # print(left_col)
            is_all_white = True
            # print(len(left_col))
            for x in left_col:
                if not np.sum(x) > 660:
                    is_all_white = False
                    break
            return dst, is_all_white
        else:
            return dst, False
    else:
        # print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        return None, False


#canvas -> img_rgb
#[np.int32(dst)] -> template_img_loc
def fill_image_with_white(img_rgb, template_img_loc):
    x_list = []
    y_list = []
    for x in template_img_loc:
        x_list.append(x[0][0])
        y_list.append(x[0][1])
    x_min, x_max = min(x_list), max(x_list)
    y_min, y_max = min(y_list), max(y_list)
    cv2.rectangle(img_rgb, (x_min, y_min), (x_max, y_max), fill_color, -1)


#canvas -> img_rgb
#[np.int32(dst)] -> template_img_loc
def check_white_point_number(img_rgb, template_img_loc):
    x_list = []
    y_list = []
    for x in template_img_loc[0]:
        x_list.append(x[0][0])
        y_list.append(x[0][1])
    x_min, x_max = min(x_list), max(x_list)
    y_min, y_max = min(y_list), max(y_list)
    num_white_point = 0
    for x in range(0, x_max - x_min):
        for y in range(0, y_max - y_min):
            arr = img_rgb[y_min + y, x_min + x]
            if np.array_equal(arr, [255, 255, 255]):
                num_white_point += 1
    print(num_white_point)
    print(float(num_white_point) / ((x_max - x_min) * (y_max - y_min)))
    return float(num_white_point) / ((x_max - x_min) * (y_max - y_min))


