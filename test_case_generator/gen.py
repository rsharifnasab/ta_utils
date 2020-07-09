#!/usr/bin/python3

from os.path import isfile, join
from os.path import exists as path_exists
from os import system as shell
from os import remove, makedirs, listdir
from shutil import make_archive
from filecmp import cmp

from re import findall
from random import randint as rnd

TEST_DIR = "./tests"
IN_FILES = TEST_DIR + "/in"
OUT_FILES = TEST_DIR + "/out"

def file_name_2_number(file_name):
    name = file_name.split(".")[0]
    number = findall(r'\d+', name)[-1]
    return int(number)

def get_last_file_number():
    files = [f for f in listdir(IN_FILES) if isfile(join(IN_FILES, f))]
    files.sort(key = file_name_2_number)
    last_file = files[-1] if len(files)>0  else "input0.txt" # empty
    last_num = file_name_2_number(last_file)
    print(f"last test is: {last_num}")
    return last_num

def make_zip():
    print("creaiting zip file")
    make_archive(
        'tests', #output name
        'zip', # file format
        root_dir= TEST_DIR,
    )

def input_file_write(i, inp):
    print("writing to input file ")
    file_add = IN_FILES+f"/input{i}.txt"
    in_file = open(file_add,"w")
    in_file.write(inp)
    in_file.close()

def make_dirs():
    required_dirs = [IN_FILES, OUT_FILES]
    for dir in required_dirs:
        if not path_exists(dir):
            makedirs(dir)
            print(f"Created {dir}")
        else:
            print(f"{dir} already exists")

def cleanup_failed_test(i,to_delete_files):
    for file in to_delete_files:
        try: remove(file)
        except: pass
    print(f"failed on test {i}")
    print(f"deleted out files for test{i}")
    exit()


def out_file_write(i,sol1,sol2):
    inp_file = IN_FILES + f"/input{i}.txt"
    out_file = OUT_FILES + f"/output{i}.txt"
    out_file_2 = OUT_FILES + f"/output{i}.txt2"

    print("running solutions..")
    shell( f"cat {inp_file} | {sol1} > {out_file}" )
    shell( f"cat {inp_file} | {sol2} > {out_file_2}" )

    ok = cmp(out_file, out_file_2)
    try:
        assert ok
        print(f"test {i} passed")
        remove(out_file_2)
        print(f"deleted junk {out_file_2}")
    except:
        cleanup_failed_test(i, (inp_file,out_file,out_file_2) )

#################################################################333

def input_rand():
    print("generating random")

    MAX_N = 3
    MIN_N = 1
    N = rnd(MIN_N,MAX_N)
    ans = f"{N}\n"
    for i in range(N) :
        temp = rnd(1, 10)
        ans += f"{temp}\n"

    print("random input gen done")
    return ans


make_dirs()
start = get_last_file_number()
END = 5 # number of tests

solution1 = "./a.out"
solution2 = "python3 test.py"

for i in range(start+1, END+1):
    print(f"-----------\ni:{i}")
    inp = input_rand()
    input_file_write(i,inp)
    out_file_write(i,solution1,solution2)

make_zip()
print("done!")
