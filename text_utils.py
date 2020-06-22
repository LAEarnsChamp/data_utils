#!/usr/bin/python
# -*- coding: UTF-8 -*-
# text data utils

import os
import getpass

# create some config folders
foldername = "C:\\Users\\{}\\.datautils\\stopwords".format(getpass.getuser())
if not os.path.exists(foldername):
    os.makedirs(foldername)


def getstopwords(stopwords="./", addition=None):
    '''
    stopwords: stopwords file path
    addition: stopwords list or None

    return: list of stopwords
    '''
    if isinstance(addition, list) is not True and addition is not None:
        raise TypeError("argument 'addition' must be string list or None")
    # stopwords list
    list_sw = []

    # if stopwords file is not found
    try:
        with open("{}".format(stopwords), 'r', encoding='UTF-8') as sw_f:
            for line in sw_f.readlines():
                list_sw.append(line.strip())
        list_sw += addition
    except FileNotFoundError as e:
        raise e
    return list_sw


def experiment_gensim_text2corpus(text, cuttool="jieba", stopwords="cn_stopwords", self_stopwords=[]):
    '''
    quick experiment for transform text to gensim's corpus

    text: input text, shape is (texts num, text)
    cuttool: the tool for cutting text into words
    stopwords: list of stopwords,
    can be "cn_stopwords"/"hit_stopwords"/"baidu_stopwords"/"scu_stopwords" or None
    self_stopwords: list of stopwords from yourself

    return: dictionary, corpus
    '''

    from gensim import corpora
    import urllib

    def cut_jieba(texts, list_sw):
        import jieba
        words_ls = []
        for text in texts:
            words_ls.append([word for word in jieba.lcut(text) if word not in list_sw])
        return words_ls

    cuttools = {"jieba": cut_jieba}
    # get stopwords list
    list_sw = []

    if stopwords is not None:
        stopwords_files_download = {
            "cn_stopwords": "https://github.com/goto456/stopwords/raw/master/cn_stopwords.txt"
        }
        # if stopwords file is not found
        if not os.path.exists("C:\\Users\\{}\\.datautils\\stopwords\\{}.txt".format(getpass.getuser(), stopwords)):
            print("Downloading stopwords file")
            urllib.request.urlretrieve(stopwords_files_download[stopwords],
                       "C:\\Users\\{}\\.datautils\\stopwords\\{}.txt".format(getpass.getuser(), stopwords),
                       lambda num, size, all_: print(num * size / all_))
            print("Download completely")
        # if stopwords file existed
        with open("C:\\Users\\{}\\.datautils\\stopwords\\{}.txt".format(getpass.getuser(), stopwords),
                    'r',
                    encoding='UTF-8') as sw_f:
            for line in sw_f.readlines():
                list_sw.append(line.strip())
    else:
        pass

    # cut word with stop words list
    list_sw.extend(self_stopwords)
    words_ls = cuttools[cuttool](text, list_sw)

    dictionary = corpora.Dictionary(words_ls)
    corpus = [dictionary.doc2bow(words) for words in words_ls]

    return dictionary, corpus


