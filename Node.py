# This file contains the abstract class used by each terminal in the BNF Grammar of core
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
