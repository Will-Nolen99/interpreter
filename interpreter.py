from tokenizer import Tokenizer
from NonTerminals import *





def interpret():

    tokenizer = Tokenizer("test.txt")

    core_program = Program()
    core_program.parse(tokenizer)









if __name__ == "__main__":
    interpret()