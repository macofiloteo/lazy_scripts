#!/usr/bin/python

import base64
import sys
import getopt


def decode_base64(inputfile, outputfile):
    with open(inputfile, "rb") as ifile:
        decoded_string = base64.b64decode(ifile.read())
    with open(outputfile, "wb") as ofile:
        ofile.write(decoded_string)


def main(argv):
    inputfile = None
    outputfile = None
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('decode_base64.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('decode_base64.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        print(arg)

    if inputfile is not None and outputfile is not None:
        decode_base64(inputfile, outputfile)

    else:
        print("err")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
