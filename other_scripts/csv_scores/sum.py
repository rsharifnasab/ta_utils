#!/bin/env python3

import pandas as pd
from math import ceil
import sys
from pathlib import Path

SOON_SCORE = 1.05

Q_REGEX = r"(q\d\d)"
SCORES_REGEX = Q_REGEX + "|sum+stdnt_id"


def process_file(inp_file):
    df = pd.read_csv(inp_file, dtype="int")
    df["sum"] = 0
    assert not df.isnull().values.any()
    for _, row in df.iterrows():
        soon = row["s"]
        scores = row.filter(regex=Q_REGEX)
        assert min(scores) >= 0
        assert max(scores) <= 100
        q_count = len(scores)

        score_sum = ceil(sum(scores)/q_count)
        final_score = score_sum * SOON_SCORE if soon == 1 else score_sum
        row["sum"] = final_score

    #df = df.filter(regex=r"q\d\d").astype(str).apply(lambda a: a.str.zfill(3))
    q_cols = df.filter(regex=SCORES_REGEX)
    for col in q_cols.columns:
        df[col] = df[col].astype(str).str.zfill(3)
    print(df.head())

    inp_name = Path(inp_file).stem
    df.to_csv(f"{inp_name}-sum.csv", index=False)
    try:
        df.pop("g")
    except:
        pass
    df.to_excel(f"{inp_name}-sum.xlsx", index=False)


def main():
    INP_FILES = sys.argv[1:]
    if len(INP_FILES) == 0:
        print("No input files")
        sys.exit(1)
    for inp_file in INP_FILES:
        process_file(inp_file)


if __name__ == "__main__":
    main()
