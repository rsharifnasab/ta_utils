#!/usr/bin/env python3
from pathlib import Path
from os.path import isdir
from sys import argv
from re import sub as re_sub

from stdid import load_std_map, STD_FILE


def single_file(file_path, replace_func):
    if file_path.endswith('.gif') or file_path.endswith('.png'):
        return

    print(f"->{file_path}")
    with open(file_path, 'r') as f:
        content = f.read()
    result = re_sub(r'([0-9]{5,14})', replace_func, content)
    with open(file_path, 'w') as f:
        f.write(result)
        f.flush()


def traverse(path, func):
    if not isdir(path):
        func(path)
    else:
        for sub in Path(path).iterdir():
            traverse(path + "/" + sub.name, func)


def main():
    map = load_std_map(STD_FILE)

    def repl(match):
        s = match.group(0)
        if s in map:
            #print(f"{s} -> {map[s]}")
            return map[s]
        else:
            #print(f"{s} not found in {STD_FILE}")
            return s

    for path in argv[1:]:
        traverse(path, lambda p: single_file(p, repl))


if __name__ == "__main__":
    main()
