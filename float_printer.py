#!/usr/bin/env python3

import sys
from termcolor import colored
from math import ceil
import struct

def print_usage():
    print("Usage: %s [32|64] [value in hex]" % sys.argv[0])
    exit(0)

if len(sys.argv) != 3:
    print_usage()

try:
    val = int(sys.argv[2], base=16)
except ValueError:
    print_usage()
    quit()

def bitcast_to_float(bits, val):
    if bits == 32:
        return struct.unpack('!f', struct.pack('!I', val))[0]
    elif bits == 64:
        return struct.unpack('!d', struct.pack('!Q', val))[0]
    else:
        print_usage()
        quit()

def do_op(bits, exponent_bits, mantissa_bits):
    sign = (val >> (exponent_bits + mantissa_bits)) & 1
    sign_s = format(sign, "#d")

    exponent = (val >> mantissa_bits) & ((1 << exponent_bits) - 1)
    exponent_s_hex = format(exponent, "#0" + str(int(ceil(exponent_bits / 4)) + 2) + "x")
    exponent_s_bin = format(exponent, "#0" + str(exponent_bits + 2) + "b")

    mantissa = val & ((1 << mantissa_bits) - 1)
    mantissa_s_hex = format(mantissa, "#0" + str(int(ceil(mantissa_bits / 4)) + 2) + "x")
    mantissa_s_bin = format(mantissa, "#0" + str(mantissa_bits + 2) + "b")

    print("value:    ", bitcast_to_float(bits, val))
    print("sign:     ", sign_s)
    print("exponent: ", exponent_s_hex, " " * (len(mantissa_s_hex) - len(exponent_s_hex) - 1), exponent_s_bin)
    print("mantissa: ", mantissa_s_hex, mantissa_s_bin)

    print(
        colored(str(sign), "red"),
        colored(exponent_s_bin[2:], "green"),
        colored(mantissa_s_bin[2:], "blue")
    )

if sys.argv[1] == "32":
    do_op(32, 8, 23)
elif sys.argv[1] == "64":
    do_op(64, 11, 52)
else:
    print_usage()
