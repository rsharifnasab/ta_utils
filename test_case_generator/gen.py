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
from random import randint as rnd

TEST_DIR = "./tests"
FAILED_DIR = "./failed"
IN_FILES = TEST_DIR + "/in"
OUT_FILES = TEST_DIR + "/out"
ZIP_NAME = "t"


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
        base_name=ZIP_NAME, 
        format="zip",  # file format
        root_dir=TEST_DIR,
    )


def input_file_write(i, inp):
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
        print(f"attemp to delete {f}")
        if isfile(f):
            copyfile(f, f"{FAILED_DIR}/{basename(f)}")
            remove(f)
            print("deleted")
    print(f"failed on test {i}")
    print(f"deleted out files for test{i}")
    sys_exit()


def execute(i, sols, validate=False):
    inp = IN_FILES + f"/input{i}.txt"
    out = OUT_FILES + f"/output{i}.txt"

    out_chk = OUT_FILES + f"/output{i}.tmp"
    if not validate: 
        shell(f"cat {inp} | {sols[0]} | tr -d '[:space:]'  > {out}")

    passed = isfile(out)
    #print("running solutions..")
    for sol in sols:
        shell(f"cat {inp} | {sol} | tr -d '[:space:]'  > {out_chk}")
        passed = passed and isfile(out_chk) and cmp(out, out_chk)
        if not passed:
            error(f"error on test {i} sol : {sol}")
            if validate:
                fail_test(i, (out_chk,))
            else:
                fail_test(i, (inp, out, out_chk))

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
    for f in (TEST_DIR, ZIP_NAME+".zip", FAILED_DIR):
        if isdir(f):
            rmtree(f)
        if isfile(f):
            remove(f)
        print(".", end="")
    print(" deleted old tests")

def closed_range(start, stop, step=1):
    d = 1 if (step > 0) else -1
    return range(start, stop + d, step)


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
        execute(i, sols, validate=False)

    make_zip()
    print("done!")


def validate(sols):
    end_index = get_last_file_number()
    for i in closed_range(1, end_index):
        execute(i, sols, validate=True)



#################################################################333

def input_rand():

    MAX_N = 3
    MIN_N = 1
    N = rnd(MIN_N, MAX_N)
    ans = f"{N}\n"
    for _ in range(N):
        temp = rnd(1, 10)
        ans += f"{temp}\n"

    return ans if 0 else input()

if __name__ == "__main__":

    opt = get_options()
    if opt.job == "delete" or opt.clear:
        clear_tests()

    if opt.job == "validate":
        validate(opt.sol)
    elif opt.job == "create":
        create(opt.tests, opt.sol, func=input_rand)
