#!/usr/bin/python
from settings import *
import email
import sys
import os
import shutil

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
        c = raw_input("Event (e) / Todo (t) / Others (n) / Discard (d)").strip().lower()
        while (not c in ["t", "n", "d", "e", ""]):
            c = raw_input("Event (e) / Todo (t) / Others (n) / Discard (d)").strip().lower()
        if (c == "e"):
            print os.path.join(output_event_dir, msg_from + "_" + msg_to + "_" + filename)
            shutil.copy2(os.path.join(input_dir, filename), os.path.join(output_event_dir, msg_from + "_" + msg_to + "_" + filename))
        elif (c == "t"):
            print os.path.join(output_todo_dir, msg_from + "_" + msg_to + "_" + filename)
            shutil.copy2(os.path.join(input_dir, filename), os.path.join(output_todo_dir, msg_from + "_" + msg_to + "_" + filename))
        elif (c == "n"):
            print os.path.join(output_other_dir, msg_from + "_" + msg_to + "_" + filename)
            shutil.copy2(os.path.join(input_dir, filename), os.path.join(output_other_dir, msg_from + "_" + msg_to + "_" + filename))

except (KeyboardInterrupt):
    pass
