import sys
pattern_dict = {-2: "SPACE", -1 : "ERROR", 0 : "MEMOP", 1 : "LOADI", 2 : "ARITHOP", 3 : "OUTPUT", 4 : "NOP", 5 : "CONSTANT", 6 : "REGISTER", 7 : "COMMA", 8 : "INTO", 9 : "ENDFILE"}
operation_dict = {"load" : 0, "store": 0, "loadI": 1, "add": 2, "sub": 2,
                  "mult": 2, "lshift": 2, "rshift": 2, "output": 3, "nop": 4, "constant": 5, "register": 6, "comma": 7, "into": 8}
class Scanner:
    def __init__(self, filename):
        self.filename = filename
        self.buffer = ""
        self.index = 0
        self.error = []

    def scan_big(self):
        file = open(self.filename)
        res = []
        line = file.readline()
        line_count = 1
        while line:
            while line[0] == "/" and len(line) > 2 and line[1] == "/":
                line = file.readline()
                line_count += 1
                if not line:
                    res.append((9, "", line_count - 1))
                    return res
            if line[-1] != '\n':
                line = line + '\n'
            self.buffer = line
            while self.buffer[self.index] != "\n":
                word_pair = self.scan_word(line_count)
                if word_pair[0] == -1:
                    self.error.append(word_pair)
                    break
                if word_pair[0] != -2:
                    res.append(word_pair)
                if self.index == len(self.buffer):
                    break
            self.buffer = ""
            self.index = 0
            line = file.readline()
            line_count += 1
            #print(line_count, line)
        res.append((9, "", line_count - 1))
        file.close()
        return res

    def scan_word(self, line_count):
        cur_char = self.buffer[self.index]
        # case for first char being s
        if cur_char == "s":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "u":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "b":
                    self.index += 1
                    return 2, "sub", line_count
                print ("Lexical Error: Found error when trying to complete word sub on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            elif next_char == "t":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "o":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "r":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "e":
                            self.index += 1
                            return 0, "store", line_count
                        print ("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print ("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being comma
        elif cur_char == ",":
            self.index += 1
            return 7, "comma", line_count
        # case for first char being space
        elif cur_char.isspace():
            self.index += 1
            return -2, "space", line_count
        elif cur_char == "/":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "/":
                self.index = len(self.buffer) - 1
                return -2, "space", line_count
            print ("Lexicla Error: / cannot be not followed by another /")
            return -1, str(line_count), line_count
        #case for first char being l
        elif cur_char == "l":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "o":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "a":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "d":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "I":
                            self.index += 1
                            return 1, "loadI", line_count
                        return 0, "load", line_count
                    print("Lexical Error: Found error when trying to complete word loadI on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete word loadI on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            elif next_char == "s":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "h":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "i":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "f":
                            self.index += 1
                            next_char = self.buffer[self.index]
                            if next_char == "t":
                                self.index += 1
                                return 2, "lshift", line_count
                            print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                            return -1, str(line_count), line_count
                        print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being m
        elif cur_char == "m":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "u":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "l":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "t":
                        self.index += 1
                        return 2, "mult", line_count
                    print("Lexical Error: Found error when trying to complete the word mult on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete the word mult on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete the word mult on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being a
        elif cur_char == "a":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "d":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "d":
                    self.index += 1
                    return 2, "add", line_count
                print("Lexical Error: Invalid word ad" + next_char + " on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Invalid word a" + next_char + " on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being n
        elif cur_char == "n":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "o":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "p":
                    self.index += 1
                    return 4, "nop", line_count
                print("Lexical Error: Found error when trying to complete the word nop on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete the word nop on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being o
        elif cur_char == "o":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "u":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "t":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "p":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "u":
                            self.index += 1
                            next_char = self.buffer[self.index]
                            if next_char == "t":
                                self.index += 1
                                return 3, "output", line_count
                            print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                            return -1, str(line_count), line_count
                        print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: o"  + next_char + " is not a valid word on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being =
        elif cur_char == "=":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == ">":
                self.index += 1
                return 8, "into", line_count
            else:
                print("Lexical Error: The second parameter for into should be >, line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
        # case for the first char being r
        elif cur_char == "r":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "s":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "h":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "i":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "f":
                            self.index += 1
                            next_char = self.buffer[self.index]
                            if next_char == "t":
                                self.index += 1
                                return 2, "rshift", line_count
                            print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                            return -1, str(line_count), line_count
                        print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            if next_char.isdigit():
                if '0' <= next_char <= '9':
                    total = int(next_char)
                    self.index += 1
                    next_char = self.buffer[self.index]
                    while "0" <= next_char <= "9":
                        num = int(next_char)
                        total = total * 10 + num
                        self.index += 1
                        next_char = self.buffer[self.index]
                    return 6, "r" + str(total), line_count
                print("Lexical Error: Register does not support leading zeros on line" + line_count, file=sys.stderr)
                return -1, str(line_count), line_count
        # case when this is a number
        elif cur_char.isdigit():
            if cur_char == "0":
                self.index += 1
                return 5, cur_char, line_count
            elif '1' <= cur_char <= '9':
                cur_total = int(cur_char)
                self.index += 1
                next_char = self.buffer[self.index]
                while "0" <= next_char <= "9":
                    num = int(next_char)
                    cur_total = cur_total * 10 + num
                    self.index += 1
                    next_char = self.buffer[self.index]
                return 5, str(cur_total), line_count
            print("Lexical Error: Constant does not support leading zeros on line" + line_count, file=sys.stderr)
            return -1, str(line_count), line_count
        # case when all the above opcode recognization failed
        print ("Lexical Error: letter " + cur_char + " is not a valid word: line" + str(line_count), file=sys.stderr)
        return -1, str(line_count), line_count

test_scanner = Scanner("test_file.txt")
#print (test_scanner.scan_big())











