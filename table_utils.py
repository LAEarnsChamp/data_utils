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


def numstring_to_integer(col):
    '''
    convert pandas number like string object to integer type

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
    check the entity quantity relationship

    df: pandas dataframe
    key_col: name of primary col
    for example, one id related to one object's name or one person

    return: entity quantity relationship dataframe
    '''
    sub = df.dropna(axis=0)

    def most_frequent(x):
        return Counter(list(x)).most_common(1)[0][0]

    def entity_set(x):
        return set(x)

    unique = sub.groupby(key_col).agg({'nunique', most_frequent, entity_set})

    return unique


def fillna_dict(df, keycol, fillcol, dict_):
    '''
    fillna nans by dict, if there are some determined mapping relationship that can be inferred from other rows

    df: pandas DataFrame, a sub df is suggested
    dict_: dictionary used, keys are from cols, and values are determined mapping relationship
    keycol: dict_,keys come from
    fillcol: row with nan to be filled
    '''
    # search nan rows
    tofill_index = df[df[fillcol].isnull().values==True].index
    # record failed
    found = 0
    for tf_i in tofill_index:
        try:
            df[fillcol][tf_i] = dict_[df[keycol][tf_i]]
            found += 1
        except KeyError:
            continue

    print("name: {}, nan rows: {}, filled rows: {}".format(fillcol, len(tofill_index), found))
    return df
