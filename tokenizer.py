#!/usr/bin/python
import email
import re
import os
import porter2
from stoplist import Commonwords
from settings import *


class Tokenizer:
    payload_toks = []
    subject_toks = []
    tok_freq = {}
    payload = ""
    payload_trimmed = ""
    subject = ""
    frm = ""
    to = ""
    msg = None
    commonwords = None
    freq = []

    def __init__(self, raw_msg, commonwords):
        self.msg = email.message_from_string(raw_msg)
        self.frm = self.msg["From"]
        self.to = self.msg["To"]
        self.subject = self.msg["Subject"]
        self.payload = self.msg.get_payload()
        self.commonwords = commonwords

    def __stem(self, tok):
        tok = re.sub(r"[\.|,|:|\?|\"|\'|;|!]+$", "", tok)
        tok = porter2.stem(tok)
        return tok


    def __line_filter(self, line):
        if re.search(r"^[\-|=|~]{4,}", line.lstrip()):
            return True
        if re.search(r"^(to|cc|from|subject):", line.lstrip(), re.IGNORECASE):
            return True

    def __token_filter(self, tok):
        url_regex = re.compile(r"((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-]*)?\??(?:[\-\+=&;%@.\w]*)#?(?:[\w]*))?)")
        if url_regex.search(tok):
            return True
        if re.match(r"[^a-zA-Z]+", tok):
            return True

    def __trim_payload(self):
        lineno = 0
        tag = ""
        trimmed_lines = []
        for line in self.payload.split("\n"):

            lineno += 1

            if lineno == 1 and len(line.split("\s")) <= 3: # skip the salutation
                continue

            if re.search(r"^[\-|=]+\s*forward", line.lstrip(), re.IGNORECASE): # skip forwarded msg
                break

            if re.search(r"^>+", line.lstrip()):
                break

            if self.__line_filter(line.lstrip()):
                continue

            trimmed_lines.append(line)
            for i in range(len(trimmed_lines) - 1, -1, -1):
                if not trimmed_lines[i]:
                    break

            if (i != 0):
                last_block = trimmed_lines[i:]
                sig = True
                if len(last_block) <= 6:
                    for blockline in last_block:
                        if len(blockline.split("\s")) > 5:
                            sig = False

                else:
                    sig = False

                if (sig == True):
                    trimmed_lines = trimmed_lines[:i]
        self.payload_trimmed = "\n".join(trimmed_lines)


    def __tokenizer(self):
        self.__trim_payload()
        common = self.commonwords.get_commonwords() if self.commonwords else []
        # print common
        self.subject_toks = []
        self.payload_toks = []
        for tok in self.subject.split():
            if not tok in common:
                self.subject_toks.append(tok)

        for tok in self.payload_trimmed.split():
            if not tok in common:
                if not self.__token_filter(tok):
                    self.payload_toks.append(self.__stem(tok))



    def __compute_freq(self):
        self.__tokenizer()
        for tok in self.payload_toks:
            # print str(tok)
            if tok.lower() in self.tok_freq:
                # print str(tok) + 'plus'
                self.tok_freq[tok.lower()] += 1
            else:
                self.tok_freq[tok.lower()] = 1

    def get_freq(self):
        self.__compute_freq()
        # print str(self.tok_freq) + '\n'
        return self.tok_freq

