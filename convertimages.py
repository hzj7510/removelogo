from fileexecute import get_file_path


def is_big_image(im):
    w, h = im.size
    if int(w) == int(h):
        return True
    return False


def convert_image(im, path, file, img_size, type):
    new_image = im.resize(img_size, type)
    new_image.save(get_file_path(path, file))
