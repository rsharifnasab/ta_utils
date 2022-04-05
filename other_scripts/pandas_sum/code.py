#!/usr/bin/env python3
import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", help="file path")
args = parser.parse_args()
FILE_PATH = args.file


def score_ok(df, row):
    effective_row = row*5 + 1
    col = df[f"Unnamed: {effective_row}"]
    assert col[0] == "نمره داوری با تاخیر"
    score_judge = col[1:].astype(float).fillna(0)

    col = df[f"Unnamed: {effective_row-2}"]
    assert col[0] == "نمره استاد با تاخیر"
    score_teacher = col[1:].replace("None", "0").astype(float).fillna(0)

    if sum(score_teacher) == 0:
        return score_judge
    elif sum(score_judge) == 0:
        return score_teacher
    else:
        return score_judge.combine(score_teacher, lambda _, y: y)


def main():
    df = pd.read_excel(FILE_PATH)
    st_numbers = df['Unnamed: 1'][1:].astype(str)
    counter = 1
    scores = None
    while True:
        try:
            score_cur = score_ok(df, counter)
            if scores is None:
                scores = score_cur
            else:
                scores += score_cur
            counter += 1
        except KeyError:
            break

    scores_final = []
    scores_map = {}
    for st_id, score in zip(st_numbers, scores, strict=True):
        st_id = st_id.replace('\u200c', '').strip()
        if np.isnan(float(st_id)):
            continue
        scores_final.append((st_id, score))
        scores_map[st_id] = score

    with open("./students.txt", "r") as f:
        for student in f.readlines():
            student = student.strip().replace('\u200c', '')
            score = scores_map.get(student, 0)
            #print(f"{student} {score}")
            print(f"{score}")


if __name__ == "__main__":
    main()
