import numpy as np
import pandas as pd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", help="file path")
args = parser.parse_args()
FILE_PATH = args.file


def score_ok(df, row):
    effective_row = row*5 + 1
    col = df[f"Unnamed: {effective_row}"]
    assert col[0] == "نمره داوری با تاخیر"
    score = col[1:].astype(float).fillna(0)

    return score


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
            #print(f"{student} {scores_map[student]}")
            print(f"{scores_map[student]}")


if __name__ == "__main__":
    main()
