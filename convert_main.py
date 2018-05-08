from PIL import Image
from convertimages import is_big_image, convert_image
from fileexecute import get_file_path
import os


path = '/Users/swift/Desktop/removelogo/nologoimages'
save_path = '/Users/swift/Desktop/removelogothumbnail'

if __name__ == '__main__':
    files = os.listdir(path)
    for file in files[1:]:
        print(file)
        im = Image.open(get_file_path(path, file))
        if is_big_image(im):
            convert_image(im, save_path, file, (150, 150), Image.ANTIALIAS)
