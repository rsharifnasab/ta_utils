#!/bin/env python3

from sys import argv


def load_std_map(std_file):
    with open(std_file, "r", encoding="UTF-8") as f:
        students = {}
        for line in f:
            line_split = line.split()
            if len(line_split) == 0:
                continue
            std_id = line_split[-1]
            std_name = " ".join(line_split[:-1])
            students[std_id] = std_name
        return students


def one_student(std_map):
    std_id = input().strip()
    print(std_map.get(std_id, std_id))


def main(std_file):
    std_map = load_std_map(std_file)
    while True:
        try:
            one_student(std_map)
        except EOFError:
            break


if __name__ == "__main__":
    main(argv[1])
