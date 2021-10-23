# This file contains the abstract class used by each terminal in the BNF Grammar of core
# The class is mostly for my own error fixing to make sure I do not forget anything
from abc import ABC, abstractmethod


# Base class to be used by each non-terminal
class Node(ABC):


    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def execute(self):
        pass
