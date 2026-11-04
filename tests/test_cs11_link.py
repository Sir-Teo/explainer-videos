"""Part 11's linker and loader: relocation, the strong/weak rules, and argv on the stack."""

import unittest

from explainer.cs.pebble.link import LinkError, assemble_object, link, load

MAIN = """
        .globl _start
        .text
_start: la   a0, msg
        call puts
        la   t0, counter
        lw   a0, 0(t0)
        addi a0, a0, 1
        sw   a0, 0(t0)
        halt
        .data
msg:    .asciiz "hello, linker\\n"
        .align 4
ptr:    .word msg
"""

LIB = """
        .globl puts
        .globl counter
        .text
puts:   li   t1, 0xFFFF0000
loop:   lbu  t2, 0(a0)
        beqz t2, done
        sb   t2, 0(t1)
        addi a0, a0, 1
        j    loop
done:   ret
        .bss
counter: .space 4
"""

ECHO = """
        .globl _start
        .text
_start: lw   a0, 4(a1)          # argv[1]
        call puts
        halt
"""


def run(objs, argv=()):
    m = load(link(objs), argv=list(argv))
    m.run()
    return m


class TestLink(unittest.TestCase):
    def test_hello(self):
        exe = link([assemble_object(MAIN, "main.o"), assemble_object(LIB, "lib.o")])
        m = load(exe)
        m.run()
        self.assertEqual(bytes(m.output), b"hello, linker\n")
        self.assertEqual(m.word(exe.symbols["counter"]), 1)
        ptr = next(p for p in exe.patches if p["kind"] == "abs32")
        self.assertEqual(m.word(ptr["at"]), ptr["target"])

    def test_order_independent(self):
        m = run([assemble_object(LIB, "lib.o"), assemble_object(MAIN, "main.o")])
        self.assertEqual(bytes(m.output), b"hello, linker\n")

    def test_undefined(self):
        with self.assertRaises(LinkError):
            link([assemble_object(MAIN, "main.o")])

    def test_duplicate_strong(self):
        with self.assertRaises(LinkError):
            link([assemble_object(MAIN, "main.o"), assemble_object(LIB, "lib.o"), assemble_object(LIB, "lib2.o")])

    def test_weak(self):
        weak = LIB.replace(".globl puts", ".weak puts").replace("hello", "")
        noisy = """
        .globl puts
        .text
puts:   li t1, 0xFFFF0000
        li t2, 33
        sb t2, 0(t1)
        ret
"""
        exe = link([assemble_object(MAIN, "main.o"), assemble_object(weak, "weak.o"), assemble_object(noisy, "n.o")])
        self.assertEqual(exe.resolution["puts"], "n.o")
        m = load(exe)
        m.run()
        self.assertEqual(bytes(m.output), b"!")

    def test_argv(self):
        exe = link([assemble_object(ECHO, "echo.o"), assemble_object(LIB, "lib.o")])
        m = load(exe, argv=["echo", "pebble"])
        self.assertEqual(m.regs[3], 2)  # a0 = argc
        self.assertEqual(m.regs[2] % 16, 0)  # sp aligned
        m.run()
        self.assertEqual(bytes(m.output), b"pebble")


if __name__ == "__main__":
    unittest.main()
