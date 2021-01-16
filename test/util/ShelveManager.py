"""
Author: Mark Chen
Date: 2021/1/11
Description:
The ShelveManager class is used to control the storage of data by module 'shelve'.
A ShelveManager is used to read & write data.
"""
import shelve

class ShelveManager:
    def __init__(self, dataPath):
        self.dataPath = dataPath

    def read(self, key: str):
        """
        :param key is a string as the key of dictionary
        :return: the corresponding value (also a string)
        """
        with shelve.open(self.dataPath) as database:
            return database[key]

    def write(self, key: str, value: str):
        """
        :param key: a string that represent the key
        :param value:  a string that represent the corresponding value
        :raise KeyError - The key does not exist in the shelve object
        :return: None
        """
        with shelve.open(self.dataPath, writeback=True) as database:
            database[key] = value

    def delItem(self, key:str):
        """
        :param key: a string that represent the key to delete
        :return: None
        """
        with shelve.open(self.dataPath) as database:
            database.pop(key)

    def getAll(self):
        """
        :return: all the key-value pair in the shelve in form of tuples.
        """
        with shelve.open(self.dataPath) as database:
            return list(database.items())

    def wipeData(self, silent=False):
        if not silent:
            response = input("YOU ARE TRYING TO WIPE ALL DATA IN SHELVE {}, press y if you want to do this: ".format(self.dataPath))
            if response != 'y':
                print("Wiping terminated, data remained in shelve")
                return
        with shelve.open(self.dataPath) as database:
            database.clear()
            print("Shelve {} cleared.".format(self.dataPath))