from tokenizer import Tokenizer
from NonTerminals import *


def interpret():

    tokenizer = Tokenizer("test.txt")

    core_program = Program()
    core_program.parse(tokenizer)

    outputFile = open("output.txt", 'w')
    core_program.print(outputFile)
    outputFile.close()


if __name__ == "__main__":
    interpret()