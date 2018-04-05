#!/usr/bin/env python3
# stage 2: sorting and merging data

import pandas as pd

from glob import glob

STAGE1_GLOB = 'stage1.*.csv'

def load_csv(csv_fname):
    return pd.read_csv(csv_fname,
                       parse_dates=['date'],
                       encoding='utf-8')

def inner_sort(dfs):
    for df in dfs:
        assert all(~df['date'].isna())
        df.sort_values('date', inplace=True)

def outer_sort(dfs):
    # If the first incident in one file took place earlier than the first incident in another,
    # we assume all incidents in the former took place earlier than all incidents in the latter.
    dfs.sort(key=lambda df: df.loc[0].date)

def main():
    # Sort the dataframes by ascending date, then sort by ascending date *within* each dataframe,
    # then merge into 1 giant CSV.
    dfs = [load_csv(fname) for fname in glob(STAGE1_GLOB)]
    inner_sort(dfs)
    outer_sort(dfs)

    giant_df = pd.concat(dfs, ignore_index=True)
    giant_df.to_csv('stage2.csv',
                    index=False,
                    encoding='utf-8')

if __name__ == '__main__':
    main()
