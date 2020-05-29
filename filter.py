#! /usr/bin/env python3

import argparse
import sys

def filter(fil, inp, out, delim="\t"):
    fil = list(fil)
    for line in inp:
        for f in fil:
            f = f.split(delim)
            for i in f:
                i = i.strip()
                if line.lower().find(i.lower()) < 0:
                    break
            else:
                break # all elements of f matched
        else:
            continue # no element of fil matched
        print(line, file=out, end="") # line already contains a \n

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", required=True, type=argparse.FileType('r'))
    parser.add_argument("input", type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("-o", "--output", nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("-d", "--delim", help="Delimiter to use for separating the elements in filer", default="\t")
    args = parser.parse_args()
    filter(args.filter, args.input, args.output, delim=args.delim)

if __name__ == "__main__":
    main()
