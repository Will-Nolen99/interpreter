from Node import Node


# list of set tokens used in the core programming language
TOKEN_MAP = {"program": 1, 
             "begin": 2,
             "end": 3,
             "int": 4,
             "if": 5,
             "then": 6,
             "else": 7,
             "while": 8,
             "loop": 9,
             "read": 10,
             "write": 11,
             ";": 12,
             ",": 13,
             "=": 14,
             "!": 15,
             "[": 16,
             "]": 17,
             "&&": 18,
             "||": 19,
             "(": 20, 
             ")": 21, 
             "+": 22, 
             "-": 23,
             "*": 24, 
             "!=": 25, 
             "==": 26, 
             "<": 27, 
             ">": 28, 
             "<=": 29,
             ">=": 30,
             "integer": 31,
             "id": 32,
             "EOF": 33 }

             #Token 31 is integers
             #Token 32 is Identifiers
             #Token 33 is EOF





class Program(Node):

    def __init__(self):

        self.__decl_seq = None
        self.__stmnt_seq = None


    def parse(self, tokenizer):
        
        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("program"):
            Program.__parseError("program", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__decl_seq = DeclSeq()
        self.__decl_seq.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("begin"):
            Program.__parseError("begin", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__stmnt_seq = StmntSeq()
        self.__stmnt_seq.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("end"):
            Program.__parseError("end", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()


    def print(self):
        pass

    def execute(self):
        pass


    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse program")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()



class DeclSeq(Node):

    def __init__(self):
        
        self.__decl = None
        self.__declSeq = None
        self.__alternative = None

    def parse(self, tokenizer):

        self.__decl = Decl()
        self.__decl.parse(tokenizer)


        token = tokenizer.getToken()
        if token == TOKEN_MAP.get("int"):
            self.declSeq = DeclSeq()
            self.declSeq.parse()
            self.__alternative = 1
        else:
            self.__alternative = 0
        



    def print(self):
        pass

    def execute(self):
        pass


class StmntSeq(Node):

    def __init__(self):
        
        self.__stmnt = None
        self.__stmntSeq = None
        self.__alternative = None

    def parse(self, tokenizer):
        self.__stmnt = Stmnt
        self.__stmnt.parse()

        token = tokenizer.getToken()
        
        if token == TOKEN_MAP.get("end") or token == TOKEN_MAP.get("else"):
            self.__alternative == 0
        else:
            self.__stmntSeq = StmntSeq()
            self.__stmntSeq.parse(tokenizer)
            self.__alternative = 1



    def print(self):
        pass

    def execute(self):
        pass


class Decl(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class IdList(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Stmnt(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Assign(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class If(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Loop(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class In(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Out(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Cond(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Comp(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Exp(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Fac(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass

class Op(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class CompOp(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Id(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Let(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Int(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass


class Digit(Node):

    def parse(self):
        pass

    def print(self):
        pass

    def execute(self):
        pass
    



if __name__ == "__main__":
    p = Program()