"""The λ-core VM written in the Pebble language (Part 15): bytecode, a stack, a heap and Cheney's collector, compiled
by Part 13's compiler and run on the Pebble emulator.

    c = build(semispace=40000)                    # compile the VM (-O2)
    m = run(c, bytecode.job_program(), text)      # the loader reads the bytecode, then the VM reads the text
    m.output, m.steps                             # what it printed, and Pebble instructions executed
    stats(m, c)                                   # collections and words copied, read out of the VM's globals

The VM is the same machine as :class:`explainer.cs.runtime.vm.VM` with :class:`~explainer.cs.runtime.vm.Cheney`:
the same value tags, object layout, frame layout and collection order, so the two agree not only on the output but
on the number of collections and the words each one copies (checked in Part 15's compute).  It supports only calls
of exact arity, which is all the Job makes; the Python VM also builds partial applications.

The Pebble language has no ``switch`` and no shifts, so dispatch is a chain of ``if``s, tested in the order given
(the most frequent opcodes first, by default), and tags are taken apart with ``/`` and ``%``.
"""
from __future__ import annotations

from explainer.cs.runtime.bytecode import OP, OPS

# the order of the dispatch chain: most frequent first (from the Job's opcode counts in the Python VM)
DEFAULT_ORDER = ["LOCAL", "SETLOCAL", "JNIL", "CONST", "JF", "HEAD", "TAIL", "GLOBAL", "CALL", "RET", "TAILCALL",
                 "SND", "FST", "CONS", "EQ", "GE", "LE", "ADD", "PAIR", "JMP", "GETC", "LT", "SUB", "PUTC", "FREE",
                 "DIV", "MOD", "MUL", "GT", "NE", "NOT", "CLOSURE", "SELF", "SETGLOBAL", "POP", "HALT"]

HANDLERS = {
    "LOCAL": "stack[sp] = stack[bp + arg]; sp = sp + 1;",
    "SETLOCAL": "sp = sp - 1; stack[bp + arg] = stack[sp];",
    "CONST": "stack[sp] = arg; sp = sp + 1;",
    "FREE": "stack[sp] = heap[stack[bp - 1] / 2 + 2 + arg]; sp = sp + 1;",
    "GLOBAL": "stack[sp] = glob[arg]; sp = sp + 1;",
    "SETGLOBAL": "sp = sp - 1; glob[arg] = stack[sp];",
    "POP": "sp = sp - 1;",
    "JMP": "pc = arg;",
    "JF": "sp = sp - 1; if stack[sp] == 1 { pc = arg; }",
    "JNIL": "sp = sp - 1; if stack[sp] == 0 { pc = arg; }",
    "HEAD": "stack[sp - 1] = heap[stack[sp - 1] / 2 + 1];",
    "TAIL": "stack[sp - 1] = heap[stack[sp - 1] / 2 + 2];",
    "FST": "stack[sp - 1] = heap[stack[sp - 1] / 2 + 1];",
    "SND": "stack[sp - 1] = heap[stack[sp - 1] / 2 + 2];",
    "ADD": "sp = sp - 1; stack[sp - 1] = stack[sp - 1] + stack[sp] - 1;",
    "SUB": "sp = sp - 1; stack[sp - 1] = stack[sp - 1] - stack[sp] + 1;",
    "MUL": "sp = sp - 1; stack[sp - 1] = 2 * (((stack[sp - 1] - 1) / 2) * ((stack[sp] - 1) / 2)) + 1;",
    "DIV": "sp = sp - 1; stack[sp - 1] = 2 * (((stack[sp - 1] - 1) / 2) / ((stack[sp] - 1) / 2)) + 1;",
    "MOD": "sp = sp - 1; stack[sp - 1] = 2 * (((stack[sp - 1] - 1) / 2) % ((stack[sp] - 1) / 2)) + 1;",
    "EQ": "sp = sp - 1; if eq(stack[sp - 1], stack[sp]) { stack[sp - 1] = 3; } else { stack[sp - 1] = 1; }",
    "NE": "sp = sp - 1; if eq(stack[sp - 1], stack[sp]) { stack[sp - 1] = 1; } else { stack[sp - 1] = 3; }",
    "LT": "sp = sp - 1; if stack[sp - 1] < stack[sp] { stack[sp - 1] = 3; } else { stack[sp - 1] = 1; }",
    "LE": "sp = sp - 1; if stack[sp - 1] <= stack[sp] { stack[sp - 1] = 3; } else { stack[sp - 1] = 1; }",
    "GT": "sp = sp - 1; if stack[sp - 1] > stack[sp] { stack[sp - 1] = 3; } else { stack[sp - 1] = 1; }",
    "GE": "sp = sp - 1; if stack[sp - 1] >= stack[sp] { stack[sp - 1] = 3; } else { stack[sp - 1] = 1; }",
    "NOT": "if stack[sp - 1] == 1 { stack[sp - 1] = 3; } else { stack[sp - 1] = 1; }",
    "CONS": """if hfree + 3 > limit { collect(sp); if hfree + 3 > limit { oom(); return; } }
            a = hfree; heap[a] = 33; heap[a + 1] = stack[sp - 2]; heap[a + 2] = stack[sp - 1]; hfree = a + 3;
            sp = sp - 1; stack[sp - 1] = 2 * a;""",
    "PAIR": """if hfree + 3 > limit { collect(sp); if hfree + 3 > limit { oom(); return; } }
            a = hfree; heap[a] = 34; heap[a + 1] = stack[sp - 2]; heap[a + 2] = stack[sp - 1]; hfree = a + 3;
            sp = sp - 1; stack[sp - 1] = 2 * a;""",
    "CLOSURE": """n = arg / 65536;
            if hfree + 2 + n > limit { collect(sp); if hfree + 2 + n > limit { oom(); return; } }
            a = hfree; heap[a] = (1 + n) * 16 + 3; heap[a + 1] = 2 * (arg % 65536) + 1;
            k = 0; while k < n { heap[a + 2 + k] = stack[sp - n + k]; k = k + 1; }
            hfree = a + 2 + n; sp = sp - n; stack[sp] = 2 * a; sp = sp + 1;""",
    "CALL": """fi = (heap[stack[sp - arg - 1] / 2 + 1] - 1) / 2;
            if farity[fi] != arg { putc('?'); return; }
            k = sp; nbp = sp - arg; sp = nbp + fnloc[fi];
            while k < sp { stack[k] = 1; k = k + 1; }
            stack[sp] = 2 * bp + 1; stack[sp + 1] = 2 * pc + 1; sp = sp + 2;
            bp = nbp; pc = fentry[fi];
            if sp > maxsp { maxsp = sp; }""",
    "TAILCALL": """n = arg % 256; k = arg / 256;
            fi = (heap[stack[sp - n - 1] / 2 + 1] - 1) / 2;
            if farity[fi] != n { putc('?'); return; }
            sb = stack[bp + k]; rt = stack[bp + k + 1];
            k = 0; while k <= n { stack[bp - 1 + k] = stack[sp - n - 1 + k]; k = k + 1; }
            sp = bp + n; k = bp + fnloc[fi];
            while sp < k { stack[sp] = 1; sp = sp + 1; }
            stack[sp] = sb; stack[sp + 1] = rt; sp = sp + 2; pc = fentry[fi];""",
    "RET": """a = stack[sp - 1]; sb = stack[bp + arg]; rt = stack[bp + arg + 1];
            sp = bp - 1; stack[sp] = a; sp = sp + 1; bp = (sb - 1) / 2; pc = (rt - 1) / 2;""",
    "SELF": "stack[sp] = stack[bp - 1]; sp = sp + 1;",
    "GETC": "a = getc(); stack[sp] = 2 * a + 1; sp = sp + 1;",
    "PUTC": "putc((stack[sp - 1] - 1) / 2); stack[sp - 1] = 1;",
    "HALT": "return;",
}


def source(semispace: int = 40000, order=None, stack_words: int = 24576, code_words: int = 2048) -> str:
    order = list(order or DEFAULT_ORDER)
    assert sorted(order) == sorted(OPS), set(OPS) ^ set(order)
    chain = []
    for k, name in enumerate(order):
        kw = "if" if k == 0 else "} else if"
        chain.append(f"        {kw} op == {OP[name]} {{   // {name}\n            {HANDLERS[name]}")
    chain.append("        }")
    dispatch = "\n".join(chain)
    return f"""// The λ-core's virtual machine, in the Pebble language (Part 15).
// Values: 2n+1 is the integer n; 2a points at the heap object at word a; 0 is the empty list.
// A heap object is a header (fields * 16 + kind) and its fields; kind 15 marks a forwarded object.

var opv: [{code_words}]int;
var argv: [{code_words}]int;
var fentry: [256]int;
var farity: [256]int;
var fnloc: [256]int;
var glob: [256]int;
var nglob: int = 0;
var stack: [{stack_words}]int;
var heap: [{1 + 2 * semispace}]int;
var semi: int = {semispace};
var base: int = 1;
var hfree: int = 1;
var limit: int = {1 + semispace};
var gcs: int = 0;
var copied: int = 0;
var maxsp: int = 0;

fn rd32() -> int {{
    var b0: int = getc();
    var b1: int = getc();
    var b2: int = getc();
    var b3: int = getc();
    if b3 >= 128 {{ b3 = b3 - 256; }}
    return b0 + 256 * b1 + 65536 * b2 + 16777216 * b3;
}}

fn oom() {{
    putc('O'); putc('O'); putc('M'); putc('\\n');
}}

// Cheney (1970): copy an object the first time it is reached, leave a forwarding address behind.
fn forward(v: int) -> int {{
    if v % 2 != 0 || v == 0 {{ return v; }}
    var a: int = v / 2;
    var h: int = heap[a];
    if h % 16 == 15 {{ return heap[a + 1]; }}
    var n: int = h / 16;
    var k: int = 0;
    while k <= n {{ heap[hfree + k] = heap[a + k]; k = k + 1; }}
    heap[a] = 15;
    var nv: int = 2 * hfree;
    heap[a + 1] = nv;
    hfree = hfree + n + 1;
    return nv;
}}

fn collect(sp: int) {{
    var to: int = 1;
    if base == 1 {{ to = 1 + semi; }}
    hfree = to;
    var i: int = 0;
    while i < sp {{ stack[i] = forward(stack[i]); i = i + 1; }}
    i = 0;
    while i < nglob {{ glob[i] = forward(glob[i]); i = i + 1; }}
    var scan: int = to;
    while scan < hfree {{
        var n: int = heap[scan] / 16;
        var j: int = scan + 1;
        while j <= scan + n {{ heap[j] = forward(heap[j]); j = j + 1; }}
        scan = scan + n + 1;
    }}
    copied = copied + (hfree - to);
    gcs = gcs + 1;
    base = to;
    limit = to + semi;
}}

// polymorphic structural equality; the last field (a list's tail) is followed in a loop
fn eq(a: int, b: int) -> int {{
    while 1 {{
        if a == b {{ return 1; }}
        if a % 2 != 0 || b % 2 != 0 || a == 0 || b == 0 {{ return 0; }}
        var pa: int = a / 2;
        var pb: int = b / 2;
        if heap[pa] != heap[pb] {{ return 0; }}
        var n: int = heap[pa] / 16;
        var j: int = 1;
        while j < n {{
            if eq(heap[pa + j], heap[pb + j]) == 0 {{ return 0; }}
            j = j + 1;
        }}
        a = heap[pa + n];
        b = heap[pb + n];
    }}
    return 0;
}}

fn run(nlocals: int) {{
    var pc: int = 0;
    var bp: int = 0;
    var sp: int = nlocals;
    var op: int = 0;
    var arg: int = 0;
    var a: int = 0;
    var n: int = 0;
    var k: int = 0;
    var fi: int = 0;
    var nbp: int = 0;
    var sb: int = 0;
    var rt: int = 0;
    while k < sp {{ stack[k] = 1; k = k + 1; }}
    while 1 {{
        op = opv[pc];
        arg = argv[pc];
        pc = pc + 1;
{dispatch}
    }}
}}

fn main() -> int {{
    var ncode: int = rd32();
    var nf: int = rd32();
    nglob = rd32();
    var mloc: int = rd32();
    var i: int = 0;
    while i < nf {{
        fentry[i] = rd32();
        farity[i] = rd32();
        fnloc[i] = rd32();
        i = i + 1;
    }}
    i = 0;
    while i < ncode {{
        opv[i] = getc();
        argv[i] = rd32();
        i = i + 1;
    }}
    i = 0;
    while i < nglob {{ glob[i] = 1; i = i + 1; }}
    run(mloc);
    return 0;
}}
"""


def build(semispace: int = 40000, order=None, level: int = 2, **kw):
    from explainer.cs.lang.compiler import driver as D
    return D.compile_program(source(semispace, order, **kw), level)


def run(c, prog, text: bytes, max_steps: int = 2_000_000_000, **kw):
    """``mem_size`` (bytes) gives the emulator more than Pebble's 1 MiB, for a VM built with a huge heap."""
    from explainer.cs.lang.compiler import driver as D
    return D.run(c, prog.encode() + text, max_steps=max_steps, **kw)


def read_global(m, c, name: str) -> int:
    """A global int of the VM, read out of the emulator's memory after the run."""
    a = c.program.labels[name]
    return int.from_bytes(m.mem[a:a + 4], "little", signed=True)


def stats(m, c) -> dict:
    return {g: read_global(m, c, g) for g in ("gcs", "copied", "maxsp")}
