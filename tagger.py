#!/usr/bin/python
import os
import subprocess
import pyner
import time
from settings import *
class Tagger:
    def __init__(self, classifier="all.ser.gz", port=1234):
        self.classifier = classifier
        self.port = port
        self.server = self.launch_ner_server()
        time.sleep(1)
        print "done"
        self.tagger = self.get_tagger()

    def __del__(self):
        self.server.terminate()

    def launch_ner_server(self):
        cmd = ["java", "-mx1000m", "-cp", os.path.join(ner_tagger_dir, "stanford-ner.jar"), "edu.stanford.nlp.ie.NERServer", "-loadClassifier", os.path.join(ner_classifier_dir, self.classifier), "-port", str(self.port)]
        return subprocess.Popen(cmd, shell=False)

    def get_tagger(self):
        return pyner.SocketNER(host='localhost', port=self.port)

    def __merge_cls(self, toks):
        i = 0
        j = 0
        tagged_tokens = []
        while i < len(toks):
            cur_cls = toks[i]["class"]
            cur_words = toks[i]["content"]
            j = i + 1
            if cur_cls:
                while j < len(toks) and toks[j]["class"] == cur_cls:
                    cur_words += (" " + toks[j]["content"])
                    j = j + 1
            i = j
            tagged_tokens.append({"content": cur_words, "class": cur_cls})
        return tagged_tokens

    def __get_cls(self, tagged_word):
        # print tagged_word
        elems = tagged_word.split("/")
        cls = elems[-1]
        word = "/".join(elems[:-1])

        # word, cls = tagged_word.split("/")
        if cls in ["ORGANIZATION", "TIME", "DATE", "PERSON", "LOCATION"]:
            return {"content": word, "class": cls}
        else:
            return {"content": word, "class": None}

    def tag_text(self, text):
        tagged_text = self.tagger.tag_text(text)
        # print tagged_text
        tagged_words = [self.__get_cls(i) for i in tagged_text.split()]
        merged_tagged_tokens = self.__merge_cls(tagged_words)
        return merged_tagged_tokens

if __name__ == "__main__":
    text = open("./ner/sample.txt").read()
    tagger = Tagger()
    print tagger.tag_text(text)


