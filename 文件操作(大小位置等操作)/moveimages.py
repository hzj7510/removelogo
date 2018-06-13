import os
import shutil


path = '/Users/swift/Desktop/removelogothumbnail'
save_path = '/Users/swift/Desktop/logothumbwebps'


if __name__ == '__main__':
    files = os.listdir(path)
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.webp':
            shutil.move(os.path.join(path, file), os.path.join(save_path, file))
