#!/usr/bin/python3
import argparse
from os.path import isfile, isdir, join
from os.path import exists as path_exists
from os import system as shell
from os import remove, makedirs, listdir
from sys import exit as sys_exit
from shutil import make_archive, rmtree, copyfile
from filecmp import cmp

from re import findall
from random import randint as rnd

TEST_DIR = "./tests"
FAILED_DIR = "./failed"
IN_FILES = TEST_DIR + "/in"
OUT_FILES = TEST_DIR + "/out"


def error(text):
    CRED = "\033[91m"
    CEND = "\033[0m"
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
        "tests",  # output name
        "zip",  # file format
        root_dir=TEST_DIR,
    )


def input_file_write(i, inp):
    print("writing to input file ")
    file_add = IN_FILES + f"/input{i}.txt"
    in_file = open(file_add, "w")
    in_file.write(inp)
    in_file.close()


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

    for f in to_delete_files:
        if isfile(f):
            copyfile(f, f"{FAILED_DIR}/{f}")
            remove(f)
    print(f"failed on test {i}")
    print(f"deleted out files for test{i}")
    sys_exit()


def out_file_write(i, sols):
    inp_file = IN_FILES + f"/input{i}.txt"
    out_file = OUT_FILES + f"/output{i}.txt"

    out_file_temp = OUT_FILES + f"/output{i}.tmp"
    shell(f"cat {inp_file} | {sols[0]} > {out_file}")

    passed = isfile(out_file)
    print("running solutions..")
    for sol in sols:
        shell(f"cat {inp_file} | {sol} > {out_file_temp}")
        passed = passed and isfile(out_file_temp) and cmp(out_file, out_file_temp)
        if not passed:
            error(f"error on test {i} sol={sol}")

    if passed:
        print(f"test {i} passed")
        remove(out_file_temp)
    else:
        fail_test(i, (inp_file, out_file, out_file_temp))


def get_options():
    parser = argparse.ArgumentParser(
        prog="./gen.py",
        description="generate or test test cases",
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
    print(">> deleting old tests")
    if isdir(TEST_DIR):
        rmtree(TEST_DIR)
    else:
        error("test dir isnt available")
    zip_add = TEST_DIR + ".zip"
    if isfile(zip_add):
        remove(zip_add)
    else:
        error("zip file isn't here")


def closed_range(start, stop, step=1):
    d = 1 if (step > 0) else -1
    return range(start, stop + d, step)


def create(tests_count, sols):
    make_dirs()

    if sols is None:
        error("not enough sols")
        sys_exit()

    start_index = get_last_file_number() + 1

    for i in closed_range(start_index, tests_count):
        print(f"-----------\ni:{i}")
        inp = input_rand()
        input_file_write(i, inp)
        out_file_write(i, sols)

    make_zip()
    print("done!")


def validate_i(i, sols):
    inp_file = IN_FILES + f"/input{i}.txt"
    out_file_main = OUT_FILES + f"/output{i}.txt"
    out_file_1 = OUT_FILES + f"/output{i}.txt1"
    out_file_2 = OUT_FILES + f"/output{i}.txt2"

    print("running solutions..")
    shell(f"cat {inp_file} | {sols[0]} > {out_file_1}")
    shell(f"cat {inp_file} | {sols[1]} > {out_file_2}")

    passed = (
        cmp(out_file_main, out_file_1)
        and cmp(out_file_main, out_file_2)
        and isfile(out_file_1)
        and isfile(out_file_2)
    )
    if passed:
        print(f"test {i} passed")
        remove(out_file_1)
        remove(out_file_2)
    else:
        fail_test(i, (out_file_1, out_file_2))


def validate(sols):
    end_index = get_last_file_number()
    for i in closed_range(1, end_index):
        validate_i(i, sols)


#################################################################333


def input_rand():
    print("generating random")

    MAX_N = 3
    MIN_N = 1
    N = rnd(MIN_N, MAX_N)
    ans = f"{N}\n"
    for _ in range(N):
        temp = rnd(1, 10)
        ans += f"{temp}\n"

    print("random input gen done")
    return ans


if __name__ == "__main__":

    opt = get_options()
    if opt.job == "delete" or opt.clear:
        clear_tests()

    if opt.job == "validate":
        validate(opt.sol)
    elif opt.job == "create":
        create(opt.tests, opt.sol)
