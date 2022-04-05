import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", help="file path")
args = parser.parse_args()
FILE_PATH = args.file


def score_ok(df):
    col = df["نمره/10.00"]
    score = col[:].astype(float).fillna(0)

    return score


def main():
    df = pd.read_excel(FILE_PATH)
    st_numbers = df["کد شناسائی"][:].astype(
        float).fillna(0).astype(int).astype(str)
    print(st_numbers)
    scores = score_ok(df)

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
