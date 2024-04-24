import subprocess as sp
import sys

input_path = ""
output_path = ""


def make_ls_list():
    global input_path
    ls_cmd = "ls %s" % input_path
    proc = sp.Popen(ls_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    std_out, std_err = proc.communicate()
    ls_file_name = std_out.decode('utf-8').rstrip().split('\n')
    print(ls_cmd)
    return ls_file_name


def super_resolution(input_path, output_path, file_name):
    input_path = input_path + file_name
    output_path = output_path + file_name
    output_path = output_path.replace('JPG', 'png')
    super_resolution_cmd = "exiftool -api largefilesupport=1 -tagsfromfile %s -all:all -overwrite_original %s" % (input_path, output_path)
    print(super_resolution_cmd)
    proc = sp.Popen(super_resolution_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    std_out, std_err = proc.communicate()
    print(input_path, output_path)
    print(super_resolution_cmd)
    print(std_out.decode('utf-8').rstrip())
    print(std_err.decode('utf-8').rstrip())
    return True


def get_args():
    global input_path, output_path
    args = sys.argv
    if len(args) == 3:
        input_arg = args[1]
        output_args = args[2]
        input_path = "./images/input_images/%s/" % (input_arg)
        output_path = "./images/output_images/%s/" % (output_args)
        print(input_path, output_path)
        return input_path, output_path
    else:
        print("Usage: python3 copy_exif.py [type] [magnification]")


def main():
    input_path, output_path = get_args()
    ls_file_name = make_ls_list()
    for file_name in ls_file_name:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(file_name)
        super_resolution(input_path, output_path, file_name)


if __name__ == '__main__':
    main()
