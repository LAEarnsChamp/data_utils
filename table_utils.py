#!/usr/bin/python
# -*- coding: UTF-8 -*-
# table data utils

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
