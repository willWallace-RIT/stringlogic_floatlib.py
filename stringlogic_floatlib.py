"""
stringlogic_floatlib.py

Drop-in string-register arithmetic + float encoding library.

Features:
- Pure string-based register operations
- Gate logic arithmetic
- Binary/hex encode + decode
- Simplified float packing/unpacking
- No int(), float(), bin(), hex() conversions
- Designed for constrained VMs / educational CPUs

NOTE:
This is NOT IEEE754 compliant math.
It is a symbolic/string emulation layer.
"""

# ============================================================
# LOGIC GATES
# ============================================================

def NOT(a):
    if a == "0":
        return "1"
    return "0"


def AND(a, b):
    if a == "1":
        if b == "1":
            return "1"
    return "0"


def OR(a, b):
    if a == "1":
        return "1"

    if b == "1":
        return "1"

    return "0"


def XOR(a, b):
    if a != b:
        return "1"
    return "0"


# ============================================================
# ADDERS
# ============================================================

def HALF_ADDER(a, b):

    s = XOR(a, b)
    c = AND(a, b)

    return s, c


def FULL_ADDER(a, b, cin):

    s1, c1 = HALF_ADDER(a, b)
    s2, c2 = HALF_ADDER(s1, cin)

    carry = OR(c1, c2)

    return s2, carry


def PAD_BITS(a, b):

    while len(a) < len(b):
        a = "0" + a

    while len(b) < len(a):
        b = "0" + b

    return a, b


# ============================================================
# BINARY ADD
# ============================================================

def BINARY_ADD(a, b):

    a, b = PAD_BITS(a, b)

    carry = "0"
    out = ""

    i = len(a) - 1

    while i >= 0:

        s, carry = FULL_ADDER(a[i], b[i], carry)

        out = s + out

        i -= 1

    if carry == "1":
        out = "1" + out

    return out


# ============================================================
# TWOS COMPLEMENT
# ============================================================

def TWOS_COMPLEMENT(bits):

    inv = ""

    i = 0
    while i < len(bits):
        inv += NOT(bits[i])
        i += 1

    one = ""

    i = 0
    while i < len(bits) - 1:
        one += "0"
        i += 1

    one += "1"

    return BINARY_ADD(inv, one)[-len(bits):]


# ============================================================
# SUBTRACTION
# ============================================================

def BINARY_SUB(a, b):

    a, b = PAD_BITS(a, b)

    tb = TWOS_COMPLEMENT(b)

    result = BINARY_ADD(a, tb)

    return result[-len(a):]


# ============================================================
# DIGIT TABLES
# ============================================================

DIGIT_TO_BIN_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001"
}

BIN_TO_DIGIT_TABLE = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9"
}

HEX_TABLE = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F"
}

HEX_TO_BIN_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


# ============================================================
# DECIMAL STRING -> BINARY
# ============================================================

def decimal_to_binary(decimal_string):

    out = ""

    i = 0

    while i < len(decimal_string):

        ch = decimal_string[i]

        if ch in DIGIT_TO_BIN_TABLE:
            out += DIGIT_TO_BIN_TABLE[ch]

        i += 1

    return out


# ============================================================
# BINARY -> DECIMAL STRING
# ============================================================

def binary_to_decimal(binary_string):

    while len(binary_string) % 4 != 0:
        binary_string = "0" + binary_string

    out = ""

    i = 0

    while i < len(binary_string):

        nibble = binary_string[i:i+4]

        if nibble in BIN_TO_DIGIT_TABLE:
            out += BIN_TO_DIGIT_TABLE[nibble]
        else:
            out += "?"

        i += 4

    return out


# ============================================================
# BINARY -> HEX
# ============================================================

def binary_to_hex(binary_string):

    while len(binary_string) % 4 != 0:
        binary_string = "0" + binary_string

    out = ""

    i = 0

    while i < len(binary_string):

        nibble = binary_string[i:i+4]

        out += HEX_TABLE[nibble]

        i += 4

    return out


# ============================================================
# HEX -> BINARY
# ============================================================

def hex_to_binary(hex_string):

    out = ""

    i = 0

    while i < len(hex_string):

        ch = hex_string[i].upper()

        if ch in HEX_TO_BIN_TABLE:
            out += HEX_TO_BIN_TABLE[ch]

        i += 1

    return out


# ============================================================
# SIMPLIFIED FLOAT PACK
# ============================================================

def pack_float(decimal_string):

    sign = "0"

    if len(decimal_string) > 0:
        if decimal_string[0] == "-":
            sign = "1"
            decimal_string = decimal_string[1:]

    raw_binary = decimal_to_binary(decimal_string)

    exponent = "10000000"

    mantissa = raw_binary[:23]

    while len(mantissa) < 23:
        mantissa += "0"

    return sign + exponent + mantissa


# ============================================================
# SIMPLIFIED FLOAT UNPACK
# ============================================================

def unpack_float(float_bits):

    sign = float_bits[0]

    exponent = float_bits[1:9]

    mantissa = float_bits[9:]

    decimal_string = binary_to_decimal(mantissa)

    if sign == "1":
        decimal_string = "-" + decimal_string

    return {
        "sign": sign,
        "exponent": exponent,
        "mantissa": mantissa,
        "decimal_string": decimal_string
    }


# ============================================================
# HIGH LEVEL API
# ============================================================

class StringLogicFloat:

    def encode_decimal(self, decimal_string):

        binary = decimal_to_binary(decimal_string)

        return {
            "decimal": decimal_string,
            "binary": binary,
            "hex": binary_to_hex(binary),
            "float_bits": pack_float(decimal_string)
        }

    def decode_binary(self, binary_string):

        return {
            "binary": binary_string,
            "decimal": binary_to_decimal(binary_string),
            "hex": binary_to_hex(binary_string)
        }

    def decode_hex(self, hex_string):

        binary = hex_to_binary(hex_string)

        return {
            "hex": hex_string,
            "binary": binary,
            "decimal": binary_to_decimal(binary)
        }

    def unpack_float(self, float_bits):

        return unpack_float(float_bits)

    def add(self, a, b):

        return BINARY_ADD(a, b)

    def sub(self, a, b):

        return BINARY_SUB(a, b)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    slf = StringLogicFloat()

    print("======== ENCODE ========")

    result = slf.encode_decimal("1234")

    print(result)

    print()

    print("======== DECODE HEX ========")

    decoded = slf.decode_hex(result["hex"])

    print(decoded)

    print()

    print("======== FLOAT UNPACK ========")

    unpacked = slf.unpack_float(result["float_bits"])

    print(unpacked)

    print()

    print("======== ADD ========")

    print(slf.add("00001111", "00000001"))

    print()

    print("======== SUB ========")

    print(slf.sub("00001111", "00000001"))
