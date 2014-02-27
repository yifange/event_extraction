#!/usr/bin/python
from settings import *
import email
import sys
import os
import shutil
import re

def trim_payload(msg):
    lineno = 0
    trimmed_lines = []
    for line in msg.split("\n"):
        lineno += 1
        if lineno == 1 and len(line.split("\s")) <= 3:
            continue
        if re.search(r"^[\-|=]+\s*forward", line.lstrip(), re.IGNORECASE): # skip forwarded msg
            break
        if re.search(r"^>+", line.lstrip()):
            break

        if re.search(r"^[\-|=|~]{4,}", line.lstrip()):
            continue
        if re.search(r"^(to|cc|from|subject):", line.lstrip(), re.IGNORECASE):
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

    return "\n".join(trimmed_lines)


def token_filter(tok):
    url_regex = re.compile(r"((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-]*)?\??(?:[\-\+=&;%@.\w]*)#?(?:[\w]*))?)")
    if url_regex.search(tok):
        return True

try:
    filenames = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    for filename in filenames:
        raw_message = open(os.path.join(input_dir, filename), "r").read()
        msg = email.message_from_string(raw_message)
        msg_from = msg["From"].split("@")[0]
        msg_to = msg["To"].split("@")[0]
        print "======================================================"
        print msg.get_payload()
        print "======================================================"
        c = raw_input("Event (e) / Todo (t) / Others (o) / Discard (d)").strip().lower()
        while (not c in ["t", "o", "d", "e", ""]):
            c = raw_input("Event (e) / Todo (t) / Others (o) / Discard (d)").strip().lower()
        if (c == "e"):
            dest = os.path.join(output_event_dir, msg_from + "_" + msg_to + "_" + filename)
            print dest
            shutil.copy2(os.path.join(input_dir, filename), dest)
        elif (c == "t"):
            dest = os.path.join(output_todo_dir, msg_from + "_" + msg_to + "_" + filename)
            print dest
            shutil.copy2(os.path.join(input_dir, filename), dest)
        elif (c == "o"):
            dest = os.path.join(output_other_dir, msg_from + "_" + msg_to + "_" + filename)
            print dest
            shutil.copy2(os.path.join(input_dir, filename), dest)

        print "-------------------------------------------------------"

        if c in ["d", "", "o"]:
            continue


        tagged_out = open(dest + ".tsv", "w")
        trimmed_payload = trim_payload(msg.get_payload())

        for tok in trimmed_payload.split():
            if token_filter(tok):
                continue

            m = re.match(r"^([\"|\']?)([^\.|,|:|\?|\"|\'|;|!]+)([\.|,|:|\?|\"|\'|;|!]*$)", tok)
            if m and m.group(1):
                tagged_out.write(m.group(1) + "\t" + "0" + "\n")

            if m:
                print m.group(2)
            else:
                print tok

            c = raw_input("PERSON: 1\tTIME: 2\tPLACE: 3\tTASK: 4\tREQUEST: 5").strip()

            rep = True
            n = 0
            while rep:
                rep = False
                try:
                    if not c:
                        n = 0
                    else:
                        n = int(c)
                    if n not in [0, 1, 2, 3, 4, 5]:
                        raise Exception
                except:
                    c = raw_input("PERSON: 1\tTIME: 2\tPLACE: 3\tTASK: 4\tREQUEST: 5").strip()
                    rep = True
            if m:
                tagged_out.write(m.group(2) + "\t" + ["0", "PERSON", "TIME", "PLACE", "TASK", "REQUEST"][n] + "\n")
            else:
                tagged_out.write(tok + "\t" + ["0", "PERSON", "TIME", "PLACE", "TASK", "REQUEST"][n] + "\n")


            if m and m.group(3):
                tagged_out.write(m.group(3) + "\t" + "0" + "\n")


        tagged_out.close()




except (KeyboardInterrupt):
    pass
