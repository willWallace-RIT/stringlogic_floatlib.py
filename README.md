StringLogicFloatLib

> Ever run into a situation where you have string reggies but no numeric ones? I got you covered, boi.



StringLogicFloatLib is a weird little low-level Python library for environments where:

everything is a string register,

arithmetic operators are unavailable or restricted,

numeric conversion functions are banned,

and you still somehow need binary math, float packing, hex conversion, and gate logic.


This library builds arithmetic from:

if statements,

boolean gate logic,

ripple carry adders,

two's complement subtraction,

and symbolic string transformations.


Designed for:

emulator projects,

constrained VMs,

experimental languages,

educational CPU simulations,

cursed architectures,

game scripting systems,

and “I wonder if this is possible” moments.



---

Features

Gate Logic

Implemented entirely with conditional branching:

NOT

AND

OR

XOR



---

Arithmetic

String-based binary arithmetic:

Half Adder

Full Adder

Ripple Carry Adder

Two’s Complement

Binary Subtraction



---

Encoding

Convert string numerics into:

Binary

Hexadecimal

Simplified Float Layouts


And back again.


---

Example

from stringlogic_floatlib import StringLogicFloat

slf = StringLogicFloat()

encoded = slf.encode_decimal("1234")

print(encoded)

Output:

{
    'decimal': '1234',
    'binary': '0001001000110100',
    'hex': '1234',
    'float_bits': '01000000000100100011010000000000'
}


---

Binary Arithmetic Example

print(
    slf.add(
        "00001111",
        "00000001"
    )
)

Output:

00010000


---

Subtraction Example

print(
    slf.sub(
        "00001111",
        "00000001"
    )
)

Output:

00001110


---

Float Packing

The float packer creates a simplified symbolic float structure:

[ sign ][ exponent ][ mantissa ]

This is:

educational,

VM-friendly,

deterministic,

string-safe,


but not true IEEE754 arithmetic.


---

Why?

Because sometimes you:

inherit cursed legacy systems,

write interpreters inside interpreters,

emulate impossible hardware,

build fantasy CPUs,

abuse scripting languages,

or simply want to see how far string logic can go.



---

Design Philosophy

This library intentionally avoids:

int()

float()

hex()

bin()


Core arithmetic is synthesized manually using:

gates,

carries,

conditional logic,

and symbolic bit manipulation.



---

Potential Uses

Retro console emulators

Fantasy CPUs

Educational architecture demos

Sandbox VMs

Obfuscated systems

Procedural logic engines

Game development experiments

Cellular automata tooling

Digital logic teaching



---

Future Ideas

IEEE754 compatibility layer

String-based multiplication/division

ALU simulation

Register banks

Stack machine support

VM bytecode layer

Soft-FPU implementation

Logic timing simulation

Bitwise memory arrays



---

License

Do whatever. Break things responsibly.
