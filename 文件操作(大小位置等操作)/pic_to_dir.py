import shutil
import os
import re

def mk_dir(o_path, d_path):
    files = os.listdir(o_path)
    files_out_dir = []
    files_in_tem_dir = []
    for file in files:
        if os.path.isdir(os.path.join(o_path, file)):
            try:
                if file == 'tmp':
                    files_in_tem_dir = os.listdir(os.path.join(o_path, file))
                os.mkdir(os.path.join(d_path, file))
            except Exception as e:
                pass
        else:
            files_out_dir.append(file)
    return set(files_out_dir[1:]), set(files_in_tem_dir[1:])


if __name__ == '__main__':
    # /Users/swift/Downloads/xunmall-shop-upload800
    o_path = '/Users/swift/Downloads/xunmall-shop-upload'
    d_path = '/Users/swift/Desktop/imgworker/originimages600'
    exe_path = '/Users/swift/Desktop/imgworker/newexcuteimages/colimg600'
    # copy_path = '/Users/swift/Desktop/fuben'

    files_out_dir, files_in_tem_dir = mk_dir(o_path, d_path)
    files = os.listdir(exe_path)
    for file in files[1:]:
        if file in files_out_dir:
            # 粘贴到 根目录
            shutil.copy(os.path.join(exe_path, file), d_path)
        elif file in files_in_tem_dir:
            # 粘贴到 tmp下
            shutil.copy(os.path.join(exe_path, file), os.path.join(d_path, 'tmp'))
        else:
            # 粘贴到对应的目录下
            file_date = file[:8]
            shutil.copy(os.path.join(exe_path, file), os.path.join(d_path, file_date))



