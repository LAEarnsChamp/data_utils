#!/usr/bin/python
# -*- coding: UTF-8 -*-
# table data utils

import pandas as pd
import numpy as np
from collections import Counter


def cats_to_num(id_start=1, **kwargs):
    '''
    convert cats var to num var.
    suggest that carefully replace the dataframe before replaced by new values as to avoid index problem

    **kwargs: var name and values, e.g, type=df["type"]

    return: maps dict, encodeds dict
    '''
    maps = dict()
    encodeds = dict()
    for key, value in kwargs.items():
        map_ = {str(key): str(id_+id_start) for id_, key in enumerate(set(value))}
        encoded = value.map(map_)

        maps[key] = map_
        encodeds[key] = encoded

    return maps, encodeds


def check_nan_scale(df):
    '''
    df: pandas DataFrame

    return: DataFrame recorded nan scale
    '''
    null = pd.DataFrame(df.isnull().sum(), columns=['count_null'])
    null['proportion_null'] = (null['count_null'] / df.shape[0])
    null['proportion_null'] = null['proportion_null'].apply(lambda x: format(x, '.2%'))
    return null


def string_to_integer(col):
    '''
    convert pandas object to integer type

    col: DataFrame[col]

    return: converted col
    '''
    try:
        col = col.astype("float")
    except ValueError as e:
        raise ValueError("some values cannot be converted to numerical data\n{}".format(str(e)))
    except Exception as others:
        raise others

    max_ = col.max()
    min_ = col.min()

    if min_ >= 0:
        if max_ <= 255:
            col = col.astype(np.uint8)
        elif max_ <= 65535:
            col = col.astype(np.uint16)
        elif max_ <= 4294967295:
            col = col.astype(np.uint32)
        else:
            col = col.astype(np.uint64)
    else:
        if min_ > np.iinfo(np.int8).min and max_ < np.iinfo(np.int8).max:
            col = col.astype(np.int8)
        elif min_ > np.iinfo(np.int16).min and max_ < np.iinfo(np.int16).max:
            col = col.astype(np.int16)
        elif min_ > np.iinfo(np.int32).min and max_ < np.iinfo(np.int32).max:
            col = col.astype(np.int32)
        elif min_ > np.iinfo(np.int64).min and max_ < np.iinfo(np.int64).max:
            col = col.astype(np.int64)

    return col


def check_onetomany(df, key_col):
    '''
    check if it is One to One or One to Many relation between key col and others

    df: pandas dataframe
    key_col: name of primary col
    for example, One to One relation is one id related to one object's name or one person

    return: dataframe for the entity correspondences between primary key and other columns
    '''
    combined = df.dropna(axis=0)

    combined_unique = combined.groupby(key_col).\
                    agg({lambda x: Counter(list(x)).most_common(1)[0][0], "nunique"}).\
                    rename(columns={"<lambda_0>": "most_frequent"})

    return combined_unique
