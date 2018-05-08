import os
import re
import shutil
import argparse


def copy_files(path, dis_path):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            os.mkdir(os.path.join(dis_path, file))
            copy_files(os.path.join(path, file), os.path.join(dis_path, file))
        else:
            name, ext = os.path.splitext(file)
            if ext != '.webp':
                ma = re.match(r'.*_big$', name)
                if ma:
                    shutil.copy(os.path.join(path, file), os.path.join(dis_path, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", help="image path")
    parser.add_argument("--dp", help="image save path")
    args = parser.parse_args()

    if args.p:
        image_path = args.p
    if args.dp:
        dis_path = args.dp

    copy_files(image_path, dis_path)
