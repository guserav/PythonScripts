#! /usr/bin/env python3

import pypdftk
import argparse
import re
import json

def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return None

def dump_data(pdf):
    reTagBegin = re.compile("^([a-zA-Z]+)Begin$")
    cmd = "{:s} {:s} dump_data".format("pdftk", pdf)
    data = [x.decode("utf-8") for x in pypdftk.run_command(cmd, True)]

    data_grouped_by_key = {}
    if not len(data):
        print("No data received from pdftk")
        return None
    match = reTagBegin.match(data.pop(0))
    counter = 0
    while match:
        counter += 1
        entry = {}
        tag = match.group(1)
        nextElement = data.pop(0)
        tagEnded = False
        while not reTagBegin.match(nextElement):
            split = nextElement.split(': ', 1)
            if len(split) != 2:
                break
            key = remove_prefix(split[0], tag)
            # Still no new Begin but no longer part of the current tag
            if key and not tagEnded:
                entry[remove_prefix(split[0], tag)] = split[1]
            else:
                tagEnded = True
                data_grouped_by_key[split[0]] = split[1]
            nextElement = data.pop(0)
        if entry != {}:
            if data_grouped_by_key.get(tag, None):
                data_grouped_by_key[tag].append(entry)
            else:
                data_grouped_by_key[tag] = [entry]
        match = reTagBegin.match(nextElement)

    if len(data):
        print("Not all data was parsed. Only got {:d} missing {:d}. Failed at {:s}".format(counter, len(data), data[0]))
        return data_grouped_by_key
    return data_grouped_by_key

class Bookmark:
    def __init__(self, parent, title, page_number):
        self.parent = parent
        self.title = title
        self.page_number = page_number

        if parent:
            self.previous = parent.get_last()
            parent.add_child(self)
            if self.previous: self.previous.add_next(self)
        else:
            self.previous = None
        self.next = None
        self.childs = []

    def add_child(self, child):
        self.childs.append(child)

    def add_next(self, n):
        self.next = n

    def get_last(self):
        if len(self.childs) > 0:
            return self.childs[-1]
        return None

    def get_end_page(self):
        if self.next:
            return self.next.page_number
        elif self.parent:
            return self.parent.get_end_page()
        else:
            return None

    def print_ancestry(self):
        print("{:s} -> {}".format(self.title, self.next))
        if self.parent:
            self.parent.print_ancestry()

    def print_tree(self, indent="  ", prefix=""):
        print("{:s}{:s}".format(prefix, self.title))
        for i in self.childs:
            i.print_tree(prefix=indent+prefix, indent=indent)

    def extract(self, pdf, prefix, sub_level, dry_run=False):
        if sub_level == 0 or not len(self.childs):
            new_pdf = prefix + self.title.replace(" ", "_")
            start = self.page_number
            end = self.get_end_page()
            if not end: end = "end"
            cmd = "{:s} {:s} cat {:s}-{:s} output {:s}.pdf".format("pdftk", pdf, start, end, new_pdf)
            if dry_run:
                print(cmd)
            else:
                pypdftk.run_command(cmd, True)
        else:
            i = 1
            for elem in self.childs:
                new_prefix = "{:s}{:02d}_".format(prefix, i)
                elem.extract(pdf, new_prefix, sub_level - 1, dry_run=dry_run)
                i+=1


def generate_bookmarks_from_dump(data):
    root = Bookmark(None, "root", "0")
    array = [root]
    parents = [root]
    for i in data:
        if len(parents) < int(i["Level"]):
            raise Exception("Integrity of Bookmarks not given")
        while len(parents) > int(i["Level"]):
            parents.pop(-1)
        elem = Bookmark(parents[-1], i["Title"], i["PageNumber"])
        parents.append(elem)
        array.append(elem)
    return array

def split_pdf(pdf, out, level, dry_run=False):
    data = dump_data(pdf)
    tree = generate_bookmarks_from_dump(data["Bookmark"])
    tree[0].extract(pdf, out, level, dry_run=dry_run)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=str, help='Path to pdf to split')
    parser.add_argument("out", type=str, help='Prefix for output filename (including path)')
    parser.add_argument("-d", "--dry-run", action='store_true', dest='dry_run', default=1, help='Only print out pdftk commands to produce pdf splits. Don\'t produce any files')
    parser.add_argument("-l", "--level", nargs='?', type=int, default=1, help='Specify level on which to split pdfs (default: 1)')
    args = parser.parse_args()
    split_pdf(args.pdf, args.out, args.level, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
