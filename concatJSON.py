#! /usr/bin/env python3

import argparse
import sys
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pretty", action="store_true", help="Concatenate with line breaks")
    parser.add_argument("-o", "--output", nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("input", nargs='+', type=argparse.FileType('r'), default=[sys.stdin])
    args = parser.parse_args()

    data = []
    for i in args.input:
        d = json.loads(i.read())
        if isinstance(d, list):
            data.extend(d)
        else:
            data.append(d)
    json.dump(data, args.output, indent=4 if args.pretty else None)
