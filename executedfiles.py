import shutil
import os

from fileexecute import get_file_path

big_image_path = '/Users/swift/Downloads/big'
big_execute_image_path = '/Users/swift/Downloads/exebig'
have_execute_image_path = '/Users/swift/Desktop/removelogo'

files_list = []


def read_files(path):
    files = os.listdir(path)
    files = files[1:]
    for f in files:
        if os.path.isdir(os.path.join(path, f)):
            # 递归
            read_files(os.path.join(path, f))
        else:
            files_list.append(f)
    return files_list


if __name__ == '__main__':
    # all_files = read_files(big_image_path)
    # all_exe_files = read_files(have_execute_image_path)

    # for file in all_exe_files:
        # shutil.move(os.path.join(big_image_path, file), os.path.join(big_execute_image_path, file))
    files = read_files(big_image_path)
    for file in files:
        if os.path.splitext(file)[1] == '.webp':
            os.remove(os.path.join(big_image_path, file))
