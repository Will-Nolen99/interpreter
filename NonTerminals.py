from typing import ValuesView
from Node import Node
from tokenizer import Tokenizer


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


class Program(Node):

    indentation_level = 0
    mode = "Declaration"

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


    def print(self, out):
        
        print("program", file=out)
        #print(file=out)
        Program.indent()

        self.__decl_seq.print(out)

        Program.unindent()
        #print(file=out)

        print("begin", file=out)
        #print(file=out)
        Program.indent()

        self.__stmnt_seq.print(out)

        Program.unindent()
        #print(file=out)
        print("end", file=out)
        #print(file=out)


    def execute(self):
        self.__decl_seq.execute()
        Program.changeToStatements()
        self.__stmnt_seq.execute()

    @staticmethod
    def indent():
        Program.indentation_level += 1

    @staticmethod
    def unindent():
        Program.indentation_level -= 1

    @staticmethod
    def changeToStatements():
        Program.mode = "statements"



    @staticmethod
    def __parseError(expectedToken, recievedToken, line):
            print("Invalid token found in parse program.")
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
            self.__alternative = 1
            self.__declSeq = DeclSeq()
            self.__declSeq.parse(tokenizer)
        else:
            self.__alternative = 0


    def print(self, out):
        self.__decl.print(out)
        if self.__alternative == 1:
            self.__declSeq.print(out)

        

    def execute(self):
        self.__decl.execute()
        if self.__alternative == 1:
            self.__declSeq.execute()


class StmntSeq(Node):

    def __init__(self):
        
        self.__stmnt = None
        self.__stmntSeq = None
        self.__alternative = None

    def parse(self, tokenizer):
        self.__stmnt = Stmnt()
        self.__stmnt.parse(tokenizer)

        token = tokenizer.getToken()
        
        if token == TOKEN_MAP.get("end") or token == TOKEN_MAP.get("else"):  #Stmnt Seq are always followed by end or else
            self.__alternative == 0
        else:
            self.__stmntSeq = StmntSeq()
            self.__stmntSeq.parse(tokenizer)
            self.__alternative = 1



    def print(self, out):
        
        self.__stmnt.print(out)
        if self.__alternative == 1:
            self.__stmntSeq.print(out)

        

    def execute(self):
        self.__stmnt.execute()
        if self.__alternative == 1:
            self.__stmntSeq.execute()


class Decl(Node):

    def __init__(self):
        self.__id_list = None


    def parse(self, tokenizer):
        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("int"):
            Decl.__parseError("int", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__id_list = IdList()
        self.__id_list.parse(tokenizer)

        token = tokenizer.getToken()

        if token != TOKEN_MAP.get(";"):
            Decl.__parseError(";", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()


    def print(self, out):
        
        for i in range(Program.indentation_level):
            print("\t", file=out, end="")
        print("int", file=out, end=" ")
        self.__id_list.print(out)
        print(";", file=out)

    def execute(self):
        self.__id_list.execute()

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse declaration")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class IdList(Node):

    def __init__(self):
        self.__id = None
        self.__id_list = None
        self.__alternative = None

    def parse(self, tokenizer):
        
        self.__id = Id()
        self.__id.parse(tokenizer)
        self.__alternative = 0
        token = tokenizer.getToken()
        if token == TOKEN_MAP.get(","):

            tokenizer.skipToken()
            self.__alternative = 1
            
            self.__id_list = IdList()
            self.__id_list.parse(tokenizer)


    def print(self, out):
        self.__id.print(out)

        if self.__alternative == 1:
            print(", ", file=out, end="")
            self.__id_list.print(out)

    def execute(self):

        values = []
        values.append(self.__id.execute())
        if self.__alternative == 1:
            values = values + self.__id_list.execute()
        
        return values

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse id list")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class Stmnt(Node):

    def __init__(self):
        self.__assign = None
        self.__if = None
        self.__loop = None
        self.__in = None
        self.__out = None
        self.__alternative = None

    def parse(self, tokenizer):
        
        token = tokenizer.getToken()
        if token == TOKEN_MAP.get("if"):
            self.__if = If()
            self.__if.parse(tokenizer)
            self.__alternative = 1

        elif token == TOKEN_MAP.get("while"):
            self.__loop = Loop()
            self.__loop.parse(tokenizer)
            self.__alternative = 2

        elif token == TOKEN_MAP.get("read"):
            self.__in = In()
            self.__in.parse(tokenizer)
            self.__alternative = 3

        elif token == TOKEN_MAP.get("write"):
            self.__out = Out()
            self.__out.parse(tokenizer)
            self.__alternative = 4

        else:
            self.__assign = Assign()
            self.__assign.parse(tokenizer)
            self.__alternative = 0

    def print(self, out):
        if self.__alternative == 0:
            self.__assign.print(out)
        elif self.__alternative == 1:
            self.__if.print(out)
        elif self.__alternative == 2:
            self.__loop.print(out)
        elif self.__alternative == 3:
            self.__in.print(out)
        elif self.__alternative == 4:
            self.__out.print(out)

    def execute(self):
        if self.__alternative == 0:
            self.__assign.execute()
        elif self.__alternative == 1:
            self.__if.execute()
        elif self.__alternative == 2:
            self.__loop.execute()
        elif self.__alternative == 3:
            self.__in.execute()
        elif self.__alternative == 4:
            self.__out.execute()


class Assign(Node):

    def __init(self):
        self.__id = None
        self.__exp = None

    def parse(self, tokenizer):
        
        self.__id = Id()
        self.__id.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("="):
            Assign.__parseError("=", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__exp = Exp()
        self.__exp.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get(";"):
            Assign.__parseError(";", list(TOKEN_MAP)[token - 1])
        tokenizer.skipToken()


            
    def print(self, out):
        for i in range(Program.indentation_level):
            print("\t", file=out, end="")
        self.__id.print(out)
        print(" = ", file=out, end="")
        self.__exp.print(out)

        print(";", file=out)

    def execute(self):
        variable_name = self.__id.execute()
        value = self.__exp.execute()
        Id.set(variable_name, value)


    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse assign")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class If(Node):

    def __init__(self):
        self.__cond = None
        self.__stmnt_seq = None
        self.__else_stmnt_seq = None
        self.__alternative = 0

    def parse(self, tokenizer):
        
        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("if"):
            If.__parseError("if", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__cond = Cond()
        self.__cond.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("then"):
            If.__parseError("then", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__stmnt_seq = StmntSeq()
        self.__stmnt_seq.parse(tokenizer)

        token = tokenizer.getToken()
        if token == TOKEN_MAP.get("else"):
            self.__alternative = 1
            tokenizer.skipToken()
            self.__else_stmnt_seq = StmntSeq()
            self.__else_stmnt_seq.parse(tokenizer)
            
            token = tokenizer.getToken()

        if token != TOKEN_MAP.get("end"):
            If.__parseError("end", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()



    def print(self, out):
        #print(file=out)
        for i in range(Program.indentation_level):
            print("\t", file=out, end="")

        print("if ", file=out, end="")
        
        self.__cond.print(out)
        print(" then", file=out)

        Program.indent()

        self.__stmnt_seq.print(out)

        Program.unindent()

        if self.__alternative == 1:

            for i in range(Program.indentation_level):
                print("\t", file=out, end="")
            print("else", file=out)
            Program.indent()
            self.__else_stmnt_seq.print(out)
            Program.unindent()

        for i in range(Program.indentation_level):
            print("\t", file=out, end="")
        print("end", file=out)
        

        

    def execute(self):
        
        if self.__cond.execute():
            self.__stmnt_seq.execute()
        elif self.__alternative == 1:
            self.__else_stmnt_seq.execute()

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse if")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class Loop(Node):

    def __init__(self):
        self.__cond = None
        self.__stmnt_seq = None


    def parse(self, tokenizer):
        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("while"):
            Loop.__parseError("while", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__cond = Cond()
        self.__cond.parse(tokenizer)


        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("loop"):
            Loop.__parseError("loop", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__stmnt_seq = StmntSeq()
        self.__stmnt_seq.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("end"):
            Loop.__parseError("end", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()


    def print(self, out):
        #print(file=out)
        for i in range(Program.indentation_level):
            print("\t", file=out, end="")

        print("while ", file=out, end="")
        self.__cond.print(out)
        print(" loop", file=out)
        Program.indent()

        self.__stmnt_seq.print(out)

        Program.unindent()

        for i in range(Program.indentation_level):
            print("\t", file=out, end="")

        print("end", file=out)
        #print(file=out)
        




    def execute(self):
        while self.__cond.execute():
            self.__stmnt_seq.execute()

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse loop")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()

class In(Node):

    def __init__(self):
        self.__id_list = None

    def parse(self, tokenizer):

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("read"):
            In.__parseError("read", list(TOKEN_MAP)[token - 1])
        tokenizer.skipToken()

        self.__id_list = IdList()
        self.__id_list.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get(";"):
            In.__parseError(";", list(TOKEN_MAP)[token - 1])
        tokenizer.skipToken()


    def print(self, out):
        
        for i in range(Program.indentation_level):
            print("\t", file=out, end="")

        print("read ", file=out, end="")
        self.__id_list.print(out)
        print(";", file=out)
        

    def execute(self):
        pass

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse in")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()

class Out(Node):

    def __init__(self):
        self.__id_list = None

    def parse(self, tokenizer):

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("write"):
            In.__parseError("write", list(TOKEN_MAP)[token - 1])
        tokenizer.skipToken()

        self.__id_list = IdList()
        self.__id_list.parse(tokenizer)

        token = tokenizer.getToken()
        if token != TOKEN_MAP.get(";"):
            Out.__parseError(";", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

    def print(self, out):
        
        for i in range(Program.indentation_level):
            print("\t", file=out, end="")

        print("write ", file=out, end="")
        self.__id_list.print(out)
        print(";", file=out)
        

    def execute(self):
        names = self.__id_list.execute()

        for name in names:
            value = Id.get(name)
            print(f"{name} = {value}")

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse out")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class Cond(Node):

    def __init__(self):
        self.__comp = None
        self.__cond = None
        self.__cond2 = None
        self.__alternative = None

    def parse(self, tokenizer):
        
        token = tokenizer.getToken()
        if token == TOKEN_MAP.get("("):
            self.__alternative = 0
            self.__comp = Comp()
            self.__comp.parse(tokenizer)

        elif token == TOKEN_MAP.get("!"):
            tokenizer.skipToken()
            self.__alternative = 1
            self.__cond = Cond()
            self.__cond.parse(tokenizer)
        elif token == TOKEN_MAP.get("["):
            tokenizer.skipToken()
            
            self.__cond = Cond()
            self.__cond.parse(tokenizer)

            token = tokenizer.getToken()
            if token == TOKEN_MAP.get("&&"):
                self.__alternative = 2
                tokenizer.skipToken()
            elif token == TOKEN_MAP.get("||"):
                self.__alternative = 3
                tokenizer.skipToken()
            else:
                Cond.__parseError("&&' or '||'", list(TOKEN_MAP)[token - 1])

            self.__cond2 = Cond()
            self.__cond2.parse(tokenizer)

            token = tokenizer.getToken()
            if token != TOKEN_MAP.get("]"):
                Cond.__parseError("]", list(TOKEN_MAP)[token - 1])
            tokenizer.skipToken()

    def print(self, out):
        
        if self.__alternative == 0:
            self.__comp.print(out)
        elif self.__alternative == 1:
            print("!", file=out, end="")
            self.__cond.print(out)
        elif self.__alternative == 2:
            print("[", file=out, end="")
            self.__cond.print(out)
            print(" && ", file=out, end="")
            self.__cond2.print(out)
            print("]", file=out, end="")

        elif self.__alternative == 3:
            print("[", file=out, end="")
            self.__cond.print(out)
            print(" || ", file=out, end="")
            self.__cond2.print(out)
            print("]", file=out, end="")

    def execute(self):
        condition = True

        if self.__alternative == 0:
            condition = self.__comp.execute()
        elif self.__alternative == 1:
            condition = not self.__cond.execute()
        elif self.__alternative == 2:
            condition = self.__cond.execute() and self.__cond2.execute()
        elif self.__alternative == 3:
            condition = self.__cond.execute() or self.__cond2.execute()

        return condition

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse cond")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()

class Comp(Node):

    def __init__(self):
        self.__op = None
        self.__comp_op = None
        self.__op2 = None


    def parse(self, tokenizer):
        token = tokenizer.getToken()
        if token != TOKEN_MAP.get("("):
            Comp.__parseError("(", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()

        self.__op = Op()
        self.__op.parse(tokenizer)

        self.__comp_op = CompOp()
        self.__comp_op.parse(tokenizer)

        self.__op2 = Op()
        self.__op2.parse(tokenizer)


        token = tokenizer.getToken()
        if token != TOKEN_MAP.get(")"):
            Comp.__parseError(")", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()



    def print(self, out):
        print("(", file=out, end="")
        self.__op.print(out)
        self.__comp_op.print(out)
        self.__op2.print(out)
        print(")", file=out, end="")

    def execute(self):
        
        val1 = self.__op.execute()
        val2 = self.__op2.execute()
        comp_op = self.__comp_op.execute()


        if comp_op == "==":
            return val1 == val2
        elif comp_op == ">":
            return val1 > val2
        elif comp_op == "<":
            return val1 < val2
        elif comp_op == "!=":
            return val1 != val2
        elif comp_op == "<=":
            return val1 <= val2
        elif comp_op == ">=":
            return val1 >= val2

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse comp")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()

class Exp(Node):

    def __init__(self):
        self.__fac = None
        self.__exp = None
        self.__alternative = None


    def parse(self, tokenizer):
        
        self.__fac = Fac()
        self.__fac.parse(tokenizer)

        token = tokenizer.getToken()
        self.__alternative = 0

        if token == TOKEN_MAP.get("+") or token == TOKEN_MAP.get("-"):
            self.__alternative = 1 if token == TOKEN_MAP.get("+") else 2
            tokenizer.skipToken()
            self.__exp = Exp()
            self.__exp.parse(tokenizer)
        

            

    def print(self, out):
        
        self.__fac.print(out)

        if self.__alternative == 1:
            print(" + ", file=out, end="")
            self.__exp.print(out)
        elif self.__alternative == 2:
            print(" - ", file=out, end="")
            self.__exp.print(out)
        


    def execute(self):
        fac = self.__fac.execute()

        if self.__alternative == 0:
            return fac
        elif self.__alternative == 1:
            return fac + self.__exp.execute()
        elif self.__alternative == 2:
            return fac - self.__exp.execute()

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse Exp")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class Fac(Node):

    def __init__(self):
        self.__fac = None
        self.__op = None
        self.__alternative = None

    def parse(self, tokenizer):
        self.__op = Op()
        self.__op.parse(tokenizer)

        token = tokenizer.getToken()

        self.__alternative = 0

        if token == TOKEN_MAP.get("*"):
            self.__alternative = 1
            tokenizer.skipToken()
            self.__fac = Fac()
            self.__fac.parse(tokenizer)


    def print(self, out):
        self.__op.print(out)

        if self.__alternative == 1:
            print(" * ", file=out, end="")
            self.__fac.print(out)

    def execute(self):
        op = self.__op.execute()

        if self.__alternative == 0:
            return op
        elif self.__alternative == 1:
            return op * self.__fac.execute()

class Op(Node):

    def __init__(self):
        self.__alternative = None
        self.__int = None
        self.__id = None
        self.__exp = None

    def parse(self, tokenizer):
        token = tokenizer.getToken()

        if token == TOKEN_MAP.get("integer"):
            self.__alternative = 0
            self.__int = Int()
            self.__int.parse(tokenizer)
        elif token == TOKEN_MAP.get("id"):
            self.__alternative = 1
            self.__id = Id()
            self.__id.parse(tokenizer)
        elif token == TOKEN_MAP.get("("):
            self.__alternative = 2
            tokenizer.skipToken()
            self.__exp = Exp()
            self.__exp.parse(tokenizer)
            token = tokenizer.getToken()
            if token == TOKEN_MAP.get(")"):
                Op.__parse(")", list(TOKEN_MAP)[token - 1])

    def print(self, out):
        if self.__alternative == 0:
            self.__int.print(out)
        elif self.__alternative == 1:
            self.__id.print(out)
        elif self.__alternative == 2:
            print("(", file=out, end="")
            self.__exp.print(out)
            print(")", file=out, end="")

    def execute(self):
        
        if self.__alternative == 0:
            return self.__int.execute()
        elif self.__alternative == 1:
            return Id.get(self.__id.execute())
        elif self.__alternative == 2:
            return self.__exp.execute()
            

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse Op")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()

class CompOp(Node):

    def __init__(self):
        self.__comp = None

    def parse(self, tokenizer):
        
        token = tokenizer.getToken()
        # token values 25 to 31 are the valid comp operators
        if token in list(range(25, 31)):
            self.__comp = list(TOKEN_MAP)[token - 1]
        else:
            CompOp.__parseError("!=', '==', '<', '>', '<=', or '>='", list(TOKEN_MAP)[token - 1])

        tokenizer.skipToken()



    def print(self, out):
        print(f" {self.__comp} ", file=out, end="")

    def execute(self):
        return self.__comp

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse comp op")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()


class Id(Node):

    __variables = {}

    def __init__(self):
        self.__id = None

    def parse(self, tokenizer):
        token = tokenizer.getToken()

        if token != TOKEN_MAP.get("id"):
            Id.__parseError("id", list(TOKEN_MAP)[token - 1])

        self.__id = tokenizer.idName()

        tokenizer.skipToken()
        

    def print(self, out):
        print(self.__id, file=out, end="")

    def execute(self):
        return self.__id

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse id")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()

    @staticmethod
    def set(variable, value=None):
        if Program.mode == "statment":
            if variable in Id.__variables:
                Id.__variables[variable] = value
            else:
                print(f"Variable '{variable}'  is undefined")
                exit()
        else:
            Id.__variables[variable] = value

    @staticmethod
    def get(variable):
        if variable in Id.__variables:
            if Id.__variables[variable] is not None:   
                return Id.__variables[variable]
            else:
                print(f"Variable '{variable}'  has not been initialized")
                exit()
        else:
                print(f"Variable '{variable}'  is undefined")
                exit()



class Int(Node):

    def __init__(self):
        self.__int = None

    def parse(self, tokenizer):
        token = tokenizer.getToken()

        if token != TOKEN_MAP.get("integer"):
            Id.__parseError("integer", list(TOKEN_MAP)[token - 1])

        self.__int = int(tokenizer.intVal())
        

        tokenizer.skipToken()

    def print(self, out):
        print(self.__int, file=out, end="")

    def execute(self):
        return self.__int

    @staticmethod
    def __parseError(expectedToken, recievedToken):
            print("Invalid token found in parse int")
            print(f"Expected '{expectedToken}' found '{recievedToken}'")
            print("Terminating")
            exit()



if __name__ == "__main__":
    p = Program()