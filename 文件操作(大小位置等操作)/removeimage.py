import os

if __name__ == '__main__':
    # 所有的image文件夹
    image_path = '/Users/swift/Desktop/imgworker/shopimgwoker800'
    # 待删除image文件夹
    remove_image_path = '/Users/swift/Desktop/imgworker/colimg800'

    files = os.listdir(remove_image_path)
    for file in files:
        if file == '.DS_Store':
            continue
        os.remove(os.path.join(image_path, file))
