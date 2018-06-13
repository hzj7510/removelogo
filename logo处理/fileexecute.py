import os
from multiprocessing import Value, Lock

all_files = Value('i', 0)
g_lock = Lock()

files_list = []


def read_files(path, q, lock):
    pic_type = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
    files = os.listdir(path)
    files = files[1:]
    for f in files:
        if os.path.isdir(os.path.join(path, f)):
            # 递归
            read_files(os.path.join(path, f), q, lock)
        else:
            if os.path.splitext(f)[1] in pic_type:
                # 加入文件集
                global all_files, g_lock
                with g_lock:
                    all_files.value += 1
                lock.acquire()
                q.put(os.path.join(path, f))
                lock.release()
    print(q.qsize())
    print(q.full())
    # return files_list


def make_dir(path):
    nologo_path = os.path.join(path, 'nologoimages')
    logo_path = os.path.join(path, 'logoimages')
    error_path = os.path.join(path, 'errorimages')
    os.mkdir(nologo_path)
    os.mkdir(logo_path)
    os.mkdir(error_path)
    return nologo_path, logo_path, error_path


def get_file_path(path, name):
    return os.path.join(path, os.path.basename(name))
