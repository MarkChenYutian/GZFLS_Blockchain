"""
This File contains the shelveManager class, which will encapsulate the interaction with file system and make it easy to
operate a shelve object (like a dictionary).

By Mark, 2021/02/13
"""
import shelve


class ShelveManager(dict):
    def __init__(self, fileName):
        super().__init__()
        self.dataPath = "./Storage/" + fileName
        self.len = 0
        with shelve.open(self.dataPath):
            pass

    def __len__(self):
        return self.len

    def __getitem__(self, item):
        with shelve.open(self.dataPath) as openShelve:
            if item in openShelve:
                return openShelve[item]
            else:
                raise KeyError("Request key {} not in Shelve File {}".format(item, self.dataPath))

    def __setitem__(self, key, item):
        with shelve.open(self.dataPath, writeback=True) as openShelve:
            if key not in self:
                self.len += 1
            openShelve[key] = item

    def __delitem__(self, key):
        with shelve.open(self.dataPath, writeback=True) as openShelve:
            self.len -= 1
            del openShelve[key]

    def __iter__(self):
        with shelve.open(self.dataPath) as openShelve:
            return iter(openShelve.keys())

    def __contains__(self, key):
        with shelve.open(self.dataPath) as openShelve:
            return key in openShelve.keys()

    def __repr__(self):
        with shelve.open(self.dataPath) as openShelve:
            return "<ShelveManager object controls " + repr(openShelve) + " at {} >".format(id(self))

    def __str__(self):
        return repr(self)

    def keys(self):
        with shelve.open(self.dataPath) as openShelve:
            return dict(openShelve).keys()

    def wipeData(self):
        print("The Data in {} is removed.".format(repr(self)))
        shelve.open(self.dataPath, flag="n")
