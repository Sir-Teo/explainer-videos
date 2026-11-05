from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, code,
                                   grid_table, load, mono, words)


class Bytecode(VoiceoverScene):
    def construct(self):
        self.card()
        self.isa()
        self.bump()
        self.mix()
        self.registers()

    def card(self):
        card = chapter_card(4, r"A bytecode virtual machine", r"Why not run the tree?", lit=(1973,),
                            extra=((1973, r"Pascal's P-code"),), part=PART)
        with self.voiceover("Chapter four. A bytecode virtual machine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def isa(self):
        head = label(r"Our machine's instruction set", font_size=34).to_edge(UP, buff=0.3)
        groups = [
            (r"values", LAM, "CONST LOCAL SETLOCAL FREE GLOBAL SETGLOBAL SELF POP"),
            (r"arithmetic", FUNC, "ADD SUB MUL DIV MOD EQ NE LT LE GT GE NOT"),
            (r"data", DATA, "CONS PAIR HEAD TAIL FST SND"),
            (r"control", CTRL, "JMP JF JNIL"),
            (r"functions", YES, "CLOSURE CALL TAILCALL RET"),
            (r"the world", GREY_A, "GETC PUTC HALT"),
        ]
        rows = VGroup()
        for name, c, ops in groups:
            rows.add(VGroup(label(name, font_size=22, color=c), mono(ops, 19, c)).arrange(RIGHT, buff=0.4))
        for r in rows:
            r[0].set(width=r[0].width)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        tags = VGroup(
            label(r"a value is one 32-bit word, \ tagged in its lowest bit:", font_size=21, color=GREY_A),
            MathTex(r"2n + 1 \;=\; \text{the integer } n \qquad 2a \;=\; \text{a pointer to address } a \qquad 0 "
                    r"\;=\; [\,]", font_size=28, color=WHITE),
            label(r"so the collector can tell every pointer from every number, \ without types", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "An interpreter that walks the tree asks, at every node, what kind of node it is, and chases pointers "
            "to find the children. Compiling the tree first, into a flat list of simple instructions for an "
            "imaginary machine, removes most of that. <bookmark mark='a'/> Here is the whole instruction set of the "
            "machine we built for the lambda core: thirty-six instructions. They push values, do arithmetic, build "
            "and take apart lists and pairs, jump, and make, call and return from closures. <bookmark mark='b'/> "
            "Every value is one thirty-two-bit word. The lowest bit says what it is: odd words are integers, even "
            "words are pointers, and zero is the empty list. <bookmark mark='c'/> That one bit is what will let "
            "the garbage collector tell every pointer from every number, by looking, with no types at run time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(tags[:2]))
            vo.wait_until("c")
            self.play(FadeIn(tags[2]))
        self.wait(0.3)
        self.clear_scene()

    def bump(self):
        d = load("vm")
        head = label(r"\texttt{bump}, \ compiled", font_size=34).to_edge(UP, buff=0.3)
        src = code(["let rec bump w table =", "  match table with", "    [] -> [(w, 1)]",
                    "  | p :: rest ->", "      if fst p = w", "      then (w, snd p + 1) :: rest",
                    "      else p :: bump w rest"], size=18, color=CODE).to_edge(LEFT, buff=0.5).shift(UP * 0.8)
        lst = [l.strip() for l in d["listing"]]
        half = (len(lst) + 1) // 2
        c1 = code(lst[:half], size=14, color=GREY_A)
        c2 = code(lst[half:], size=14, color=GREY_A)
        cols = VGroup(c1, c2).arrange(RIGHT, buff=0.45, aligned_edge=UP).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        notes = VGroup(
            label(r"\texttt{match}: \ test for \texttt{[]} \ (\texttt{JNIL}), \ then take the cell apart \ "
                  r"(\texttt{HEAD}, \texttt{TAIL})", font_size=19, color=DATA),
            label(rf"{len(lst)} instructions; \ the whole Job is {words(d['code_size'])}, \ in "
                  rf"{d['functions']} functions", font_size=19, color=GREY_A),
            label(r"the recursive call is not in tail position: \ \texttt{CONS} still waits for its result",
                  font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Here is bump, from Part 14, and the bytecode our compiler makes of it. <bookmark mark='a'/> Locals live "
            "in numbered slots: w is slot zero, table slot one. The match stores the table, tests it against the "
            "empty list with JNIL, and if it is a cell, takes it apart with HEAD and TAIL into slots for p and "
            "rest. <bookmark mark='b'/> The comparison fst p equals w is FST, LOCAL, EQ, and a conditional jump. "
            "<bookmark mark='c'/> And at the end, the recursive call, followed by a CONS that is waiting for its "
            "result. That waiting CONS is why bump, unlike words, needs a stack frame for every entry of the table "
            "it walks past. Thirty-seven instructions; the whole Job, with its driver, is under four hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(c2))
            vo.wait_until("c")
            self.play(FadeIn(notes[1:]))
        self.wait(0.3)
        self.clear_scene()

    def mix(self):
        d = load("vm")
        head = label(r"What the machine spends its time on", font_size=34).to_edge(UP, buff=0.3)
        mix = d["mix"][:12]
        tot = d["ops"]
        vals = [100 * v / tot for _, v in mix]
        cols = [LAM if n in ("LOCAL", "SETLOCAL", "GLOBAL", "CONST") else DATA if n in (
            "CONS", "HEAD", "TAIL", "FST", "SND", "PAIR") else CTRL if n in ("JF", "JNIL", "JMP") else YES if n in (
            "CALL", "RET", "TAILCALL") else FUNC for n, _ in mix]
        ch = bar_chart(vals, [n for n, _ in mix], cols, height=3.4, bar_w=0.62, gap=0.32, fmt_=lambda v: f"{v:.0f}\\%",
                       font_size=16).move_to(DOWN * 0.2)
        cap = label(rf"the Job on a {words(d['bytes'])}-byte passage: \ {words(tot)} bytecodes executed",
                    font_size=20, color=GREY_B).next_to(ch, UP, buff=0.4)
        moves = sum(v for n, v in d["mix"] if n in ("LOCAL", "SETLOCAL"))
        note = VGroup(
            label(rf"\texttt{{LOCAL}} and \texttt{{SETLOCAL}} alone: \ {100 * moves / tot:.0f}\% \ --- \ copying "
                  r"values between slots and the stack", font_size=21, color=LAM),
            label(r"every one of them pays the dispatch: \ fetch, \ decode, \ jump to the handler", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where does the time go? <bookmark mark='a'/> We counted every instruction the VM executed on a "
            "passage of thirteen hundred bytes: four hundred and sixty thousand. <bookmark mark='b'/> The biggest "
            "bar is not arithmetic or list building. It is LOCAL: pushing a local variable onto the stack. With "
            "SETLOCAL, its opposite, it is more than half of everything the machine does. <bookmark mark='c'/> A "
            "stack machine spends most of its effort shuffling values to where the next instruction can find them, "
            "and every shuffle pays the full price of an instruction: fetch it, decode it, jump to its handler."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(ch.names), FadeIn(ch[0]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.08), FadeIn(ch.vals))
            vo.wait_until("b")
            self.play(Indicate(VGroup(ch.bars[0], ch.bars[1]), color=HEAD), FadeIn(note[0]))
            vo.wait_until("c")
            self.play(FadeIn(note[1]))
        self.wait(0.3)
        self.clear_scene()

    def registers(self):
        d = load("vm")
        head = label(r"Stack machines and register machines", font_size=34).to_edge(UP, buff=0.3)
        dis = [l for l in d["cpython_dis"] if l.strip()][:22]
        dis = [l[:60] for l in dis]
        left = VGroup(label(r"CPython 3.12 compiles Python to a stack bytecode \ (\texttt{dis}, \ on this machine)",
                            font_size=19, color=GREY_B),
                      code(dis, size=12, color=CODE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        left.to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
        stack = VGroup(label(r"stack:", font_size=20, color=LAM), mono("LOCAL 1 ; LOCAL 2 ; ADD ; SETLOCAL 3", 18,
                                                                       LAM)).arrange(RIGHT, buff=0.2)
        reg = VGroup(label(r"register:", font_size=20, color=YES), mono("ADD r3, r1, r2", 18, YES)).arrange(
            RIGHT, buff=0.2)
        cmp_ = VGroup(stack, reg).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        pts = VGroup(
            label(r"Lua 5.0 \ (2003) \ moved from a stack to registers \ (Ierusalimschy et al., \ 2005)",
                  font_size=20, color=GREY_A),
            label(r"47\% fewer instructions executed, \ 25\% more bytes of code \ (Shi et al., \ 2008)",
                  font_size=20, color=YES),
            label(r"stack code is compact and easy to generate: \ the JVM, \ CPython, \ WebAssembly", font_size=20,
                  color=GREY_A),
            label(r"register code does more per dispatch: \ Lua, \ Dalvik, \ V8's Ignition", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        right = VGroup(cmp_, pts).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Real languages make the same choice. <bookmark mark='a'/> This is CPython's bytecode for bump written "
            "in Python, printed by the dis module on this machine: LOAD_FAST, LOAD_CONST, BINARY_SUBSCR. It is a "
            "stack machine, like ours. <bookmark mark='b'/> The alternative is a register machine, where one "
            "instruction names its operands: add register one to register two into register three, instead of "
            "four stack instructions. <bookmark mark='c'/> Lua made that switch in version five in 2003, and a "
            "careful study by Shi and colleagues found a register machine executes forty-seven percent fewer "
            "instructions, for code a quarter larger. <bookmark mark='d'/> Both survive. Stack code is compact and "
            "trivial to generate, which is why the JVM, CPython and WebAssembly use it. Register code does more "
            "work per dispatch, which is why Lua, Android's Dalvik and V8's interpreter use registers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(cmp_))
            vo.wait_until("c")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()
