#! /usr/bin/env python3
import argparse

# Calculate the ouput voltage
# convertUp == True: for GRD - R1 - inV - R2 - outV
# convertUp == False: for GRD - R1 - outV - R2 - inV
def calculateVoltage(inV, r1, r2, convertUp=True):
    if convertUp:
        return inV / r1 * r2;
    else:
        return inV / (r1 + r2) * r1;

def getListOfPossibleVoltageDividers(inV, outV, resistors):
    out = []
    for r1 in resistors:
        for r2 in resistors:
            out.append((r1, r2, calculateVoltage(inV, r1, r2, inV < outV)))
    out.sort(key=lambda x: abs(x[2] - outV))
    return out


def main():
    parser = argparse.ArgumentParser(description='Tool to detemine how to make a voltage divider')
    parser.add_argument('--in', dest='inV', required=True, type=float, help='Input fixed voltage')
    parser.add_argument('--out', dest='outV', required=True, type=float, help='Output voltage we try to match')
    parser.add_argument('--head', default=-1, type=int, help='Only show this amount of entries')
    parser.add_argument('resistor', type=float, nargs='+', help='List of resistor values')
    args = parser.parse_args()
    dividers = getListOfPossibleVoltageDividers(args.inV, args.outV, args.resistor)
    dividers = dividers[0:args.head] if args.head > 0 else dividers
    for i in dividers:
        print(i)

if __name__ == "__main__":
    main()
