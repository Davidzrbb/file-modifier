import os
import sys
from os import path


def args_validator(args):
    size = 0
    list_file = []
    save_path = args.save[0]
    file_path = args.file

    # we check if the size of the target and replace are the same
    for i in args.replace.values():
        size += len(i)
    if len(args.target) != size:
        print('The number of value in --replace is not equal to the number of value in --target')
        sys.exit(1)

    if path.exists(save_path):
        if path.isdir(save_path):
            for file in file_path:
                file_name = os.path.splitext(os.path.basename(file))[0]
                # we check if file name in parameter --file is *, if it is it means we need to check all file in the
                # path with the same extension
                if file_name == '*':
                    list_file.append(verify_name_file(file))
                else:
                    if path.exists(file):
                        if path.isfile(file):
                            list_file.append(verify_name_file(file))
                        else:
                            print(f'The path in --file is not a file : {file}')
                            sys.exit(1)
                    else:
                        print(f'The path in --file does not exist : {file}')
                        sys.exit(1)
        else:
            print(f'The path in --save is not a directory : {save_path}')
            sys.exit(1)
    else:
        print(f"Path of save directory does not exist  : {save_path}")
        sys.exit(1)
    return list_file


def verify_name_file(file):
    all_file_name = os.path.basename(file)
    file_name = os.path.splitext(os.path.basename(file))[0]
    if file_name == '*':
        path_file = os.path.dirname(file)
    else:
        path_file = file
    file_type = os.path.splitext(file)[1]

    return {'name': file_name, 'extension': file_type, 'all_file_name': all_file_name, 'path': path_file}
