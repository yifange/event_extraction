#!/usr/bin/python
import tokenizer
import email
import pickle
import os
from math import sqrt
from stoplist import Commonwords
from tokenizer import Tokenizer
from settings import *
import tagger

class Classifier:
    # event_freq = {}
    # other_freq = {}
    # todo_freq = {}
    # event_freq_sq = 0
    # other_freq_sq = 0
    # todo_freq_sq = 0
    # event_sim_numrt = 0
    # other_sim_numrt = 0
    # todo_sim_numrt = 0
    def __init__(self, tagger, common=None):
        self.common = common
        self.event_freq = {}
        self.other_freq = {}
        self.todo_freq = {}
        self.event_freq_sq = 0
        self.other_freq_sq = 0
        self.todo_freq_sq = 0
        self.event_sim_numrt = 0
        self.other_sim_numrt = 0
        self.todo_sim_numrt = 0
        self.tagger = tagger

        self.event_freq = pickle.load(open(os.path.join(output_event_dir, "freq"), "r"))
        self.event_freq_sq = self.compute_freq_sq(self.event_freq)
        self.other_freq = pickle.load(open(os.path.join(output_other_dir, "freq"), "r"))
        self.other_freq_sq = self.compute_freq_sq(self.other_freq)
        self.todo_freq = pickle.load(open(os.path.join(output_todo_dir, "freq"), "r"))
        self.todo_freq_sq = self.compute_freq_sq(self.todo_freq)

    def classify(self, msg): # read
        my_freq = Tokenizer(msg, self.tagger, self.common).get_freq()
        cls = self.__cos_sim(my_freq)
        return cls


    def __cos_sim(self, freq): # compute numerator and denominator
        # msg = open(os.path.join(test_dir, filename), "r").read()
        freq_sq = self.compute_freq_sq(freq)
        for key, value in freq.items():
            if key in self.event_freq:
                self.event_sim_numrt += value * self.event_freq[key];
            if key in self.other_freq:
                self.other_sim_numrt += value * self.other_freq[key];
            if key in self.todo_freq:
                self.todo_sim_numrt += value * self.todo_freq[key];

        # print "============================="
        # print self.event_freq
        # print "============================="
        # print self.other_freq
        # print "============================="
        # print freq
        # print "============================="

        event_sim = self.event_sim_numrt / (sqrt(self.event_freq_sq) * sqrt(freq_sq))
        other_sim = self.other_sim_numrt / (sqrt(self.other_freq_sq) * sqrt(freq_sq))
        todo_sim = self.todo_sim_numrt / (sqrt(self.todo_freq_sq) * sqrt(freq_sq))
        max_sim = max(event_sim, todo_sim, other_sim)
        print "event_sim", event_sim
        print "todo_sim", todo_sim
        print "other_sim", other_sim
        if max_sim == event_sim:
            return "EVENT"
        elif max_sim == todo_sim:
            return "TODO"
        else:
            return "OTHER"

    def compute_freq_sq(self, freq):
        sqsum = 0
        for key, value in freq.items():
            sqsum += value * value
        return sqsum


if __name__ == "__main__":
    common = Commonwords(commonwords_path)
    tag = tagger.Tagger()
    filenames = [f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]
    classifier = Classifier(tag, common)
    for filename in filenames:
        if filename == "freq":
            continue
        classifier.classify(open(os.path.join(test_dir, filename), "r").read())

