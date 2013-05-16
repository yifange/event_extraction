import tokenizer
import email
import pickle
import os
from stoplist import Commonwords
from tokenizer import Tokenizer
from settings import *
class Classifier:
    event_freq = {}
    other_freq = {}
    todo_freq = {}
    event_freq_sq = 0
    other_freq_sq = 0
    todo_freq_sq = 0
    event_sim_numrt = 0
    other_sim_numrt = 0
    todo_sim_numrt = 0

    def __init__(self):
        self.event_freq = pickle.load(os.path.join(output_event_dir, "freq"))
        self.event_freq_sq = self.compute_freq_sq(self.event_freq)
        self.other_freq = pickle.load(os.path.join(output_other_dir, "freq"))
        self.other_freq_sq = self.compute_freq_sq(self.other_freq)
        self.todo_freq = pickle.load(os.path.join(ouput_todo_dir, "freq"))
        self.todo_freq_sq = self.compute_freq_sq(self.todo_freq)

    def __read_folder_freq(self):
        self.event_freq = pickle.load(os.path.join(output_event_dir, "freq"))
        self.event_freq_sq = self.compute_freq_sq(self.event_freq)
        self.other_freq = pickle.load(os.path.join(output_other_dir, "freq"))
        self.other_freq_sq = self.compute_freq_sq(self.other_freq)
        self.todo_freq = pickle.load(os.path.join(ouput_todo_dir, "freq"))
        self.todo_freq_sq = self.compute_freq_sq(self.todo_freq)

    def classify(self, freq): # read
        # msg = open(os.path.join(test_dir, filename), "r").read()
        freq_sq = self.compute_freq_sq(freq)
        for key, value in freq.items():
            if key in self.event_freq:
                self.event_sim_numrt += value * self.event_freq[key];
            if key in self.other_freq:
                self.other_sim_numrt += value * self.other_freq[key];
            if key in self.todo_freq:
                self.todo_sim_numrt += value * self.todo_freq[key];

        event_sim = self.event_sim_numrt / sqrt(self.event_freq_sq) * sqrt(freq_sq)
        other_sim = self.other_sim_numrt / sqrt(self.other_freq_sq) * sqrt(freq_sq)
        todo_sim = self.todo_sim_numrt / sqrt(self.todo_freq_sq) * sqrt(freq_sq)
        max(event_sim, other_sim, todo_sim)

    # def __cos_sim(self): # compute numerator and denominator

    def compute_freq_sq(self, freq):
        sqsum = 0
        for key, value in freq.items():
            sasum += value * value
        return sqsum


if __name__ == "__main__":
    common = Commonwords(commonwords_path)
    filenames = [f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]
    for filename in filenames:
        if filename == "freq":
            continue
        freq = Tokenizer(open(os.path.join(test_dir, filename), "r").read(), common).get_freq()
        clsf = Classifier()
        clsf.classify(freq)

