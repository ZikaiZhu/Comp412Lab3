#!/usr/bin/python
import sys, getopt
from FlagHandler import FlagHandler

def main(argv):
    flag_handler = FlagHandler(argv[0])
    flag_handler.schedule()
    sys.exit()

    if argv[0].isdigit():
        flag_handler = FlagHandler(argv[1])
        flag_handler.number_handler(int(argv[0]))
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "hs:p:r:x:")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    if len(opts) > 1:
        print("Cannot take multiple command-line flags, will implement in the order of -h, -r, -p, -s")
        flag_dict = {}
        for opt in opts:
            flag_dict[opt[0]] = opt[1]
        if "-h" in flag_dict.keys():
            flag_handler = FlagHandler(None)
            flag_handler.h_handler()
            sys.exit()
        elif "-r" in flag_dict.keys():
            flag_handler = FlagHandler(flag_dict["-r"])
            flag_handler.r_handler()
            sys.exit()
        elif "-p" in flag_dict:
            flag_handler = FlagHandler(flag_dict["-p"])
            flag_handler.p_handler()
            sys.exit()
        elif "-s" in flag_dict:
            flag_handler = FlagHandler(flag_dict["-s"])
            flag_handler.s_handler()
            sys.exit()
    for o, a in opts:
        if o == "-h":
            flag_handler = FlagHandler(None)
            flag_handler.h_handler()
            sys.exit()
        elif o == "-r":
            flag_handler = FlagHandler(a)
            flag_handler.r_handler()
            sys.exit()
        elif o == "-x":
            flag_handler = FlagHandler(a)
            flag_handler.x_handler()
            sys.exit()
        elif o == "-p":
            flag_handler = FlagHandler(a)
            flag_handler.p_handler()
            sys.exit()
        elif o == "-s":
            flag_handler = FlagHandler(a)
            flag_handler.s_handler()
            sys.exit()
    flag_handler = FlagHandler(argv[0])
    flag_handler.p_handler()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])


