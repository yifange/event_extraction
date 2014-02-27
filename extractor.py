#!/usr/bin/python
import tagger
import os
from stoplist import Commonwords
from classifier import Classifier
from settings import *
import tokenizer
class Extractor:
    toks = []
    def __init__(self, toks):
        self.toks = toks
        self.time_ind = self.find_time()
        self.location_ind = self.find_location()
        self.event_ind = self.find_event()


    def dumpTokens(self):
        print self.toks
        for pair in self.toks:
            print pair["class"], "\t", pair["content"]
    def find_time(self):
        time_ind = []
        for ind in range(len(self.toks)):
            if self.toks[ind]["class"] == "TIME":
                time_ind.append(ind)
        return time_ind

    def find_location(self):
        loc_ind = []
        for ind in range(len(self.toks)):
            if self.toks[ind]["class"] == "LOCATION":
                loc_ind.append(ind)
        return loc_ind

    def find_event(self):
        event_ind = []
        for ind in range(len(self.toks)):
            if self.toks[ind]["class"] == "EVENT":
                event_ind.append(ind)
        return event_ind

    def dump_information(self):
        print "---------------------------"
        for pair in self.toks:
            if pair["class"]:
                print pair["class"], "\t", pair["content"]
        print "---------------------------"

class EventExtractor(Extractor):
    def __init__(self, toks):
        Extractor.__init__(self, toks)

    def extract_event(self):
        self.dump_information()

class TodoExtractor(Extractor):
    def __init__(self, toks):
        Extractor.__init__(self, toks)

    def extract_todo(self):
        self.dump_information()


if __name__ == "__main__":
    common = Commonwords(commonwords_path)

    event_tagger = tagger.Tagger(classifier="event.ser.gz", port=1111)
    todo_tagger = tagger.Tagger(classifier="todo.ser.gz", port=2222)
    all_tagger = tagger.Tagger(classifier="all.ser.gz", port=3333)

    filenames = [f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]
    classifier = Classifier(all_tagger, common)
    for filename in filenames:
        if filename == "freq":
            continue
        msg = open(os.path.join(test_dir, filename), "r").read()
        print "++++++++++++++++++++++++++++++++++++++++"
        print msg
        print "++++++++++++++++++++++++++++++++++++++++"
        cls = classifier.classify(msg)
        # print cls
        if cls == "EVENT":
            t = tokenizer.Tokenizer(msg, event_tagger)
            e = EventExtractor(t.get_toks())
            e.extract_event()
        elif cls == "TODO":
            t = tokenizer.Tokenizer(msg, todo_tagger)
            e = TodoExtractor(t.get_toks())
            e.extract_todo()
        print "++++++++++++++++++++++++++++++++++++++++"
