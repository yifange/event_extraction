class Commonwords:
    commonwords = []
    def __init__(self, path):
        raw_msg = open(path, "r").read()
        self.commonwords = raw_msg.split("\n")

    def get_commonwords(self):
        return self.commonwords
