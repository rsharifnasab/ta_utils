#!/usr/bin/python3
import argparse
from os.path import isfile, isdir, join, basename
from os.path import exists as path_exists
from os import system as shell
from os import remove, makedirs, listdir
from sys import exit as sys_exit
from shutil import make_archive, rmtree, copyfile
from filecmp import cmp

from re import findall


from user import test_input_gen

TEST_DIR = "./tests"
FAILED_DIR = "./failed"
IN_FILES = TEST_DIR + "/in"
OUT_FILES = TEST_DIR + "/out"
ZIP_NAME = "t"


CRED = "\033[91m"
CEND = "\033[0m"


def error(text):
    print(CRED + text + CEND)


def file_name_2_number(file_name):
    name = file_name.split(".")[0]
    number = findall(r"\d+", name)[-1]
    return int(number)


def get_last_file_number():
    files = [f for f in listdir(IN_FILES) if isfile(join(IN_FILES, f))]
    files.sort(key=file_name_2_number)
    last_file = files[-1] if len(files) > 0 else "input0.txt"  # empty
    last_num = file_name_2_number(last_file)
    print(f"last test is: {last_num}")
    return last_num


def make_zip():
    print("creating zip file")
    make_archive(
        base_name=ZIP_NAME,
        format="zip",  # file format
        root_dir=TEST_DIR,
    )


def input_file_write(i, inp):
    file_add = IN_FILES + f"/input{i}.txt"
    with open(file_add, "w", encoding="UTF-8") as in_file:
        in_file.write(inp)


def make_dirs():
    required_dirs = [IN_FILES, OUT_FILES]
    for directory in required_dirs:
        if not path_exists(directory):
            makedirs(directory)
            print(f"Created {directory}")
        else:
            print(f"{directory} already exists")


def fail_test(i, to_delete_files):
    if path_exists(FAILED_DIR):
        rmtree(FAILED_DIR)
    makedirs(FAILED_DIR)

    for del_file in to_delete_files:
        print(f"attemp to delete {del_file}")
        if isfile(del_file):
            copyfile(del_file, f"{FAILED_DIR}/{basename(del_file)}")
            remove(del_file)
            print("deleted")
    print(f"failed on test {i}")
    print(f"deleted out files for test{i}")
    sys_exit()


def execute(i, sols, validation=False):
    inp = IN_FILES + f"/input{i}.txt"
    out = OUT_FILES + f"/output{i}.txt"

    out_chk = OUT_FILES + f"/output{i}.tmp"
    if not validation:
        shell(f"cat {inp} | {sols[0]}  > {out}")

    passed = isfile(out)
    # print("running solutions..")
    for sol in sols:
        shell(f"cat {inp} | {sol}  > {out_chk}")
        passed = passed and isfile(out_chk) and cmp(out, out_chk)
        if not passed:
            error(f"error on test {i}, sol: {sol}")
            if not validation:
                fail_test(i, (inp, out, out_chk))

    if passed:
        print(f"test {i} passed")
    remove(out_chk)


def get_options():
    parser = argparse.ArgumentParser(
        prog="./gen.py",
        description="generate or validate test cases",
        epilog="enjoy creating tests.. :)",
    )
    parser.add_argument(
        "-n", "--tests", type=int, default=10, help="number of all tests"
    )
    parser.add_argument("--clear", "-c", action="store_true")
    parser.add_argument("job", choices=["create", "validate", "delete"])
    parser.add_argument("--sol", "--solution", type=str, action="append")
    options = parser.parse_args()
    return options


def clear_tests():
    for del_file in (TEST_DIR, ZIP_NAME + ".zip", FAILED_DIR):
        if isdir(del_file):
            rmtree(del_file)
        if isfile(del_file):
            remove(del_file)
        print(".", end="")
    print(" deleted old tests")


def closed_range(start, stop, step=1):
    offset = 1 if (step > 0) else -1
    return range(start, stop + offset, step)


def create(tests_count, sols, func):
    make_dirs()

    if sols is None:
        error("not enough sols")
        sys_exit()

    start_index = get_last_file_number() + 1

    for i in closed_range(start_index, tests_count):
        print(f"- - - i:{i} - - - ")
        inp = func()
        input_file_write(i, inp)
        execute(i, sols, validation=False)

    make_zip()
    print("done!")


def validate(sols):
    end_index = get_last_file_number()
    for i in closed_range(1, end_index):
        execute(i, sols, validation=True)


if __name__ == "__main__":

    opt = get_options()
    if opt.job == "delete" or opt.clear:
        clear_tests()

    if opt.job == "validate":
        validate(opt.sol)
    elif opt.job == "create":
        create(opt.tests, opt.sol, func=test_input_gen)
