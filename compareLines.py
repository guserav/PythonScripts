#! /usr/bin/env python3

import argparse
import sys

def filter(base, fil):
    for i in base:
        for x in fil:
            if x == i:
                break
        else:
            print(i.rstrip())

def compare(f1, f2):
    f1 = list(f1)
    f2 = list(f2)
    print("In 1 but not in 2")
    filter(f1, f2)
    print("In 2 but not in 1")
    filter(f2, f1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("f1", type=argparse.FileType('r'))
    parser.add_argument("f2", type=argparse.FileType('r'))
    args = parser.parse_args()
    compare(args.f1, args.f2)

if __name__ == "__main__":
    main()
