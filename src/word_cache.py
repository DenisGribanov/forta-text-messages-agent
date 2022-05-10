import os
import sys


class WordCache(object):
    words = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WordCache, cls).__new__(cls)
        return cls.instance

    def exists_assault_world(self, text):
        file_path = os.path.join(sys.path[0], 'assault_word.txt')

        if len(self.words) == 0 and os.path.exists(file_path):
            file = open(file_path, "r")
            self.words = file.read().splitlines()

        for word in self.words:
            find = text.find(word.strip())

            if find != -1:
                return True
            else:
                continue

        return  False


wordCache = WordCache()
