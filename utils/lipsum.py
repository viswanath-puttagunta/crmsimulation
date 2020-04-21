import random


class Lipsum(object):
    def __init__(self):
        self.file = None
        self.wordstring = ""
        self.words = []
        self.maxwords = 0

        with open('./utils/hipster-ipsum.txt', 'r') as self.file:
            self.wordstring = self.file.read().replace('\n', '')
            self.words = self.wordstring.split(" ")
            self.maxwords = len(self.words) - 1
            self.file.close()

    def get_name(self):
        name = ""
        for x in range(1, 4):
            name = name + " " + self.words[random.randint(0, self.maxwords)]

        return name.strip()  # Strip removes leading and training whitespace
