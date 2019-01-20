#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3

import argparse
import sys
import random

parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument("output", nargs='?', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument("-d", "--delim", help="Delimiter to use for separating line in output", default="\n")
args = parser.parse_args()

buffer = []
for line in args.input:
    buffer.append(line.rstrip('\n\r'))

random.shuffle(buffer)

for line in buffer:
    args.output.write(line)
    args.output.write(args.delim)

