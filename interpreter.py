from tokenizer import Tokenizer
from NonTerminals import Program
import sys


def interpret():

    input_file = ""
    core_source = sys.argv[1]
    if len(sys.argv) > 2:
        input_file = sys.argv[2]

    tokenizer = Tokenizer(core_source)

    core_program = Program()
    Program.setInputFile(input_file)
    core_program.parse(tokenizer)
    core_program.print()
    core_program.execute()


if __name__ == "__main__":
    interpret()