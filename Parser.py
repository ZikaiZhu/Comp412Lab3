from DoublyLinkedList import DoublyLinkedList
import sys
pattern_dict = {0 : "MEMOP", 1 : "LOADI", 2 : "ARITHOP", 3 : "OUTPUT", 4 : "NOP", 5 : "CONSTANT", 6 : "REGISTER", 7 : "COMMA", 8 : "INTO", 9 : "ENDFILE"}
operation_dict = {"load" : 0, "store": 1, "loadI": 2, "add": 3, "sub": 4,
                  "mult": 5, "lshift": 6, "rshift": 7, "output": 8, "nop": 9, "constant": 10, "register": 11, "comma": 12, "into": 13}
class Parser:
    def __init__(self):
        self.line = None
        self.index = 0
        self.error = []

    def parse_line(self, line):
        if line == []:
            return None
        self.index = 0
        self.line = line
        first_token = line[self.index]
        #This is the case for end file token
        if first_token[0] == 9:
            return None
        #This is the case for all invalid starting token
        elif first_token[0] == 8 or first_token[0] == 7 or first_token[0] == 6 or first_token[0] == 5:
            print("Grammar Error: This line cannot start with this type of operation: line" + str(first_token[2]), file=sys.stderr)
        #This is the case for NOP
        elif first_token[0] == 4:
            if len(line) > 1:
                print("Grammar Error: Nop cannot be followed by anything else: line" + str(first_token[2]), file=sys.stderr)
                return None
            else:
                cur_node = DoublyLinkedList()
                cur_node.set_nop(9)
                return cur_node
        # This is the case for "OUTPUT"
        elif first_token[0] == 3:
            if len(line) == 2:
                second_token = line[1]
                if second_token[0] == 5:
                    cur_node = DoublyLinkedList()
                    cur_node.set_output(8, second_token[1])
                    return cur_node
                print ("Grammar Error: Expect OUTPUT token to have a constant argument: line" + str(second_token[2]), file=sys.stderr)
                return None
            else:
                print("Grammar Error: Expect OUTPUT token to a length of two: line" + str(first_token[2]), file=sys.stderr)
                return None
        # This is the case for "ARITHOP"
        elif first_token[0] == 2:
            spec_type = first_token[1]
            if len(line) == 6:
                if spec_type == "add":
                    if self.arithop_handler(line):
                        cur_node = DoublyLinkedList()
                        cur_node.set_arithop(3, line[1][1], line[3][1], line[5][1])
                        return cur_node
                    print("Grammar Error: Grammar error when trying to parse add: line" + str(first_token[2]), file=sys.stderr)
                    return None
                elif spec_type == "sub":
                    if self.arithop_handler(line):
                        cur_node = DoublyLinkedList()
                        cur_node.set_arithop(4, line[1][1], line[3][1], line[5][1])
                        return cur_node
                    print("Grammar Error: Grammar error when trying to parse subtract: line" + str(first_token[2]), file=sys.stderr)
                    return None
                elif spec_type == "mult":
                    if self.arithop_handler(line):
                        cur_node = DoublyLinkedList()
                        cur_node.set_arithop(5, line[1][1], line[3][1], line[5][1])
                        return cur_node
                    print("Grammar Error: Grammar error when trying to parse multiply: line" + str(first_token[2]), file=sys.stderr)
                    return None
                elif spec_type == "lshift":
                    if self.arithop_handler(line):
                        cur_node = DoublyLinkedList()
                        cur_node.set_arithop(6, line[1][1], line[3][1], line[5][1])
                        return cur_node
                    print("Grammar Error: Grammar error when trying to parse lshift: line" + str(first_token[2]), file=sys.stderr)
                    return None
                elif spec_type == "rshift":
                    if self.arithop_handler(line):
                        cur_node = DoublyLinkedList()
                        cur_node.set_arithop(7, line[1][1], line[3][1], line[5][1])
                        return cur_node
                    print("Grammar Error: Grammar error when trying to parse rshift: line" + str(first_token[2]), file=sys.stderr)
                    return None
            print("Grammar Error: Invalid number of arguments for arithop: line" + str(first_token[2]), file=sys.stderr)
        # This is the case for "LOADI"
        elif first_token[0] == 1:
            if len(line) == 4:
                if line[1][0] == 5:
                    if line[2][0] == 8:
                        if line[3][0] == 6:
                            cur_node = DoublyLinkedList()
                            cur_node.set_loadI(2, line[3][1], line[1][1])
                            return cur_node
                        print("Grammar Error: loadI expect a register here: line" + str(first_token[2]), file=sys.stderr)
                        return None
                    print("Grammar Error: loadI expect a INTO here: line" + str(first_token[2]), file=sys.stderr)
                    return None
                print("Grammar Error: loadI expect a constant here: line" + str(first_token[2]), file=sys.stderr)
                return None
            print("Grammar Error: The number of arguments for loadI is wrong: line" + str(first_token[2]), file=sys.stderr)
            return None
        # This is the case for "MEMOP"
        elif first_token[0] == 0:
            spec_type = first_token[1]
            if len(line) == 4:
                if line[1][0] == 6:
                    if line[2][0] == 8:
                        if line[3][0] == 6:
                            cur_node = DoublyLinkedList()
                            if spec_type == "load":
                                cur_node.set_memop(0, line[1][1], line[3][1])
                                return cur_node
                            else:
                                cur_node.set_memop(1, line[1][1], line[3][1])
                                return cur_node
                        print("Grammar Error: MEMOP expects a register here: line" + str(first_token[2]), file=sys.stderr)
                        return None
                    print("Grammar Error: MEMOP expects a INTO here: line" + str(first_token[2]), file=sys.stderr)
                    return None
                print("Grammar Error: MEMOP expects a register here: line" + str(first_token[2]), file=sys.stderr)
                return None
            print("Grammar Error: The number of arguments for MEMOP is wrong: line" + str(first_token[2]), file=sys.stderr)
            return None




    def arithop_handler(self, line):
        if line[1][0] == 6:
            if line[2][0] == 7:
                if line[3][0] == 6:
                    if line[4][0] == 8:
                        if line[5][0] == 6:
                            return True
                        return False
                    return False
                return False
            return False
        return False

#parser = Parser()
#print (parser.parse_line([(0, "load", "1"), (6, "r12", "1"), (8, "=>", "1"), (6, "r13", "1")]))

#print (parser.parse_line([(2, 'add', 3), (6, 'r1', 3), (6, 'r2', 3), (8, 'into', 3), (6, "r3", 3)]))

#print (parser.parse_line([(0, 'load', 4), (6, 'r1', 4), (8, 'into', 4), (6, 'r2', 4)]))

#print (parser.parse_line(([(0, 'store', 5), (6, 'r1', 5), (8, 'into', 5), (6, 'r2', 5)])))

#print (parser.parse_line([(1, 'loadI', 6), (5, '110', 6), (8, 'into', 6), (6, 'r2', 6)]))

#print (parser.parse_line([(2, 'sub', 8), (6, 'r1', 8), (7, 'comma', 8), (6, 'r2', 8), (8, 'into', 8), (6, 'r3', 8)]))

#print(parser.parse_line([(2, 'mult', 9), (6, 'r1', 9), (7, 'comma', 9), (6, 'r2', 9), (8, 'into', 9), (6, 'r3', 9)]))

#print(parser.parse_line([(2, 'lshift', 10), (6, 'r1', 10), (7, 'comma', 10), (6, 'r2', 10), (8, 'into', 10), (6, 'r3', 10)]))

#print(parser.parse_line([(2, 'rshift', 10), (6, 'r1', 10), (7, 'comma', 10), (6, 'r2', 10), (8, 'into', 10), (6, 'r3', 10)]))

#print(parser.parse_line([(3, 'output', 12), (5, '123', 12)]))

#print (parser.parse_line([(4, 'nop', 13)]))

#print(parser.parse_line([(9, '', 14)]))
