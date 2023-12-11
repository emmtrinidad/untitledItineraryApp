#counter class for making ids

class Counter():

    def __init__(self, val):
        self.val = val

    def increment(self):
        self.val += 1

    def get(self):
        return self.val