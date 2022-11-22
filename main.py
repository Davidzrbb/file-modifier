import argparse
import os
import sys
import shutil
from datetime import datetime

from KeyValue import KeyValue
from validator import args_validator

parser = argparse.ArgumentParser()

parser.add_argument('--target', type=str, required=True, nargs='+', help='The target to replace')

parser.add_argument('--replace', type=str, required=True, nargs='+', action=KeyValue, help='replace the target with '
                                                                                           'this value')
parser.add_argument('--save', type=str, required=True, nargs='+',
                    help='directory to save the file before modified')

parser.add_argument('--file', type=str, required=True, nargs='+',
                    help='file to modified')

args = parser.parse_args(sys.argv[1:])

COUNT_FILE_MODIFIED = 0


def search_file(list_file, args_parameter):
    for files_information in list_file:
        if files_information['name'] == '*':
            # we search all file in the path with the same extension
            files_in_path = os.listdir(files_information['path'])
            for file in files_in_path:
                file_extension = os.path.splitext(file)[1]
                if file_extension == files_information['extension']:
                    files_information['all_file_name'] = file
                    replace_target(get_path_file(files_information))
        else:
            replace_target(get_path_file(files_information))


def save_file(path_file):
    global COUNT_FILE_MODIFIED
    COUNT_FILE_MODIFIED += 1
    now = datetime.now()
    date_of_save = now.strftime("%d-%m-%Y-%H-%M-%S-%f")[:-1]
    file_name = os.path.splitext(os.path.basename(path_file))[0]
    name_file = os.path.splitext(os.path.basename(path_file))[0]
    extension = os.path.splitext(os.path.basename(path_file))[1]
    path_save = args.save[0]

    shutil.copy2(path_file, path_save + '/' + name_file + date_of_save + extension)

    # we check if the save is working
    if os.path.exists(path_save + '/' + name_file + date_of_save + extension) is False:
        print(f'Error when copy the file {file_name} in {path_save}')
        exit(1)
    return path_file


def replace_target(path_file):
    target = args.target
    replace = args.replace

    with open(path_file, 'r') as file:
        data = file.read()
        for replace_value, replace_key, target_value in zip(replace.values(), replace.keys(), target):
            # we save the file if the target is found
            if target_value in data:
                if replace_key == 'chaine':
                    # we replace just the target with the replacement value
                    data = data.replace(target_value, replace_value[0])
                    write_target(path_file, data)
                if replace_key == 'ligne':
                    # we replace the line of target with the replacement value
                    for line in data.splitlines():
                        if target_value in line:
                            data = data.replace(line, replace_value[0])
                            write_target(path_file, data)


def write_target(path_file, data):
    save_file(path_file)
    with open(path_file, 'w') as file:
        file.write(data)


def get_path_file(files_information):
    original_name = files_information['name']
    path = files_information['path']
    file = files_information['all_file_name']
    if original_name == '*':
        path_file = path + '/' + file
    else:
        path_file = path

    return path_file


if __name__ == '__main__':
    search_file(args_validator(args), args)
    print(f'---------END OF PROGRAM---------')
    print(f'{COUNT_FILE_MODIFIED} file(s) modified')
    print(f'{COUNT_FILE_MODIFIED} file(s) saved in path {args.save[0]}')
