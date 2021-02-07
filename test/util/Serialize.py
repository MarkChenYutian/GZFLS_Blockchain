"""
Author: Mark Chen
Date: 2021 / 1 / 18
Description: Define the abstract class Serializable with serialize and load.
"""
import abc

class Serializable(metaclass=abc.ABCMeta):
    """
    The Serializable Class acts as a abstract class to make sure the serialize methods (serialize, load) is implemented
    """

    @abc.abstractmethod
    def serialize(self):
        """
        :return: json.dumps, string
        """
        pass

    @abc.abstractmethod
    def load(self, serialize):
        """
        :param serialize: dict
        :return:
        """
        pass