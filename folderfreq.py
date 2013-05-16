#!/usr/bin/python
import pickle
from tokenizer import Tokenizer
import os
from stoplist import Commonwords
from settings import *

class FolderFreq:
    folderpath = ""
    tok_freq = {}
    common = None
    count = 0.0
    def __init__(self, folderpath, common):
        self.folderpath = folderpath
        self.common = common

    def __compute_freq(self):
        filenames = [f for f in os.listdir(self.folderpath) if os.path.isfile(os.path.join(self.folderpath, f))]
        for filename in filenames:
            if filename == "freq":
                continue
            self.count += 1
            freq = Tokenizer(open(os.path.join(self.folderpath, filename)).read(), self.common).get_freq()
            # print open(os.path.join(self.folderpath, filename)).read()
            # print freq
            for key, value in freq.items():
                if key in self.tok_freq:
                    self.tok_freq[key] += value
                else:
                    self.tok_freq[key] = value

        for key, value in self.tok_freq.items():
            self.tok_freq[key] = self.tok_freq[key] / self.count ;

        print self.tok_freq

    def __dump_freq(self):
        dump_file = open(os.path.join(self.folderpath, "freq"), "w")
        pickle.dump(self.tok_freq, dump_file)

    def get_freq(self):
        self.__compute_freq()
        self.__dump_freq()
        return self.tok_freq


if __name__ == "__main__":
    common = Commonwords(commonwords_path)
    folderfreq = FolderFreq("mail/todo", common)
    folderfreq.get_freq()

