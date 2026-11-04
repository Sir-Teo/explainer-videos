from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, COST, CTRL, DATA, HEAD, NO, PART, WIRE, YES, gate, load, wire


class Simulator(VoiceoverScene):
    def construct(self):
        self.card()
        self.netlist()
        self.bitparallel()
        self.nandify()
        self.verify()

    def card(self):
        card = chapter_card(12, r"Our hardware layer", r"How will this series simulate a computer, gate by gate?",
                            part=PART)
        with self.voiceover("Chapter twelve. Our hardware layer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def netlist(self):
        head = label(r"A circuit is a list", font_size=38).to_edge(UP, buff=0.35)
        code = code_block([
            'c = Circuit("full adder")',
            'a, b, cin = c.input("a"), c.input("b"), c.input("cin")',
            "s1 = c.xor(a, b)",
            'c.output("sum", c.xor(s1, cin))',
            'c.output("cout", c.or_(c.and_(a, b), c.and_(s1, cin)))',
        ], font_size=24).move_to(UP * 1.2)
        table = VGroup()
        rows = [("0", "INPUT", "", "a"), ("1", "INPUT", "", "b"), ("2", "INPUT", "", "cin"), ("3", "XOR", "0, 1", "s1"),
                ("4", "XOR", "3, 2", "sum"), ("5", "AND", "0, 1", ""), ("6", "AND", "3, 2", ""),
                ("7", "OR", "5, 6", "cout")]
        for i, (w, k, args, nm) in enumerate(rows):
            r = VGroup(Text(w, font="DejaVu Sans Mono", font_size=20, color=GREY_B),
                       Text(k, font="DejaVu Sans Mono", font_size=20, color=CTRL),
                       Text(args, font="DejaVu Sans Mono", font_size=20, color=DATA),
                       Text(nm, font="DejaVu Sans Mono", font_size=20, color=YES))
            for j, m in enumerate(r):
                m.move_to([-6.0 + 1.45 * j, -0.6 - 0.36 * i, 0], aligned_edge=LEFT)
            table.add(r)
        hdr = VGroup(*[note(t, font_size=20).move_to([-6.0 + 1.45 * j, -0.25, 0], aligned_edge=LEFT)
                       for j, t in enumerate((r"wire", r"kind", r"reads wires", r"name"))])
        rule = label(r"a gate may only read wires that already exist: \\ creation order is a topological order, \ "
                     r"and one pass evaluates everything", font_size=24, color=HEAD).move_to(RIGHT * 3.4 + DOWN * 1.6)
        with self.voiceover(
            "Every circuit in this series, from this part's comparators to Pebble itself in Part 6, runs on one small "
            "piece of code, and it is worth seeing how it works. <bookmark mark='a'/> A circuit is built by calling "
            "functions: make three inputs, an exclusive-or, another, two ands and an or. That is a full adder, Part "
            "4's first circuit. <bookmark mark='b'/> Underneath, the circuit is just a numbered list of wires: each "
            "entry says what kind of gate drives it and which earlier wires it reads. <bookmark mark='c'/> Because a "
            "gate can only read wires that already exist, the list is in an order where every gate comes after its "
            "inputs. So evaluating the whole circuit is one pass down the list."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bitparallel(self):
        head = label(r"64 tests at once", font_size=38).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(3)
        a = rng.integers(0, 2, 24)
        b = rng.integers(0, 2, 24)
        c = a & b

        def row(bits, color, y, name):
            g = VGroup(*[Square(0.26, stroke_width=0.8, stroke_color=GREY_D, fill_color=color if v else "#121722",
                                fill_opacity=0.9 if v else 1).move_to([-3.2 + 0.28 * i, y, 0]) for i, v in enumerate(bits)])
            t = MathTex(name, font_size=28, color=color).next_to(g, LEFT, buff=0.3)
            dots = MathTex(r"\cdots", font_size=30, color=GREY_B).next_to(g, RIGHT, buff=0.15)
            return VGroup(g, t, dots)

        ra = row(a, DATA, 1.2, r"a")
        rb = row(b, DATA, 0.6, r"b")
        rc = row(c, YES, -0.4, r"a \,\&\, b")
        cap = VGroup(label(r"each wire holds a 64-bit word: \ bit $j$ is its value in test $j$", font_size=26,
                           color=GREY_A),
                     label(r"one machine instruction \ $=$ \ 64 AND gates evaluated", font_size=26, color=HEAD),
                     label(r"all $2^{16}$ inputs of the 8-bit comparator: \ 1{,}024 words per wire", font_size=26,
                           color=COST)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The other trick makes it fast. <bookmark mark='a'/> Each wire does not hold one bit. It holds a 64-bit "
            "machine word, and bit number j of that word is the wire's value in test number j. <bookmark mark='b'/> So "
            "a single and instruction on two words evaluates an and gate on sixty-four different inputs at once. "
            "<bookmark mark='c'/> Checking the eight-bit comparator on all sixty-five thousand of its inputs takes "
            "a thousand and twenty-four words per wire, one pass, and a fraction of a second. This is bit-parallel "
            "simulation, and chip companies use the same idea, on far bigger machines, before they build anything."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ra), FadeIn(rb), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in rc[0]], lag_ratio=0.03), FadeIn(rc[1]), FadeIn(rc[2]),
                      FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nandify(self):
        d = load("blocks")
        head = label(r"Rewriting a circuit in NANDs", font_size=38).to_edge(UP, buff=0.35)
        rules = VGroup()
        for name, k in ((r"NOT", 1), (r"AND", 2), (r"OR", 3), (r"XOR", 4)):
            src = gate(name, size=0.6)
            arr = MathTex(r"\longrightarrow", font_size=32, color=GREY_C)
            nands = VGroup(*[gate("NAND", size=0.45) for _ in range(k)]).arrange(RIGHT, buff=0.12)
            cnt = MathTex(rf"\times {k}", font_size=28, color=COST)
            rules.add(VGroup(src, arr, nands, cnt).arrange(RIGHT, buff=0.35))
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(LEFT * 3.0 + DOWN * 0.2)
        rows = {r["name"]: r for r in d["rows"]}
        ex = VGroup(*[label(rf"{n}: \ {rows[n]['gates']} gates $\to$ {rows[n]['nands']} NANDs", font_size=24,
                            color=GREY_A) for n in ("4-bit comparator", "8-bit barrel shifter (left)",
                                                    "8-to-3 priority encoder")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.25)
        ex.move_to(RIGHT * 3.6 + UP * 0.6)
        txt = VGroup(label(r"each rule is chapter five's construction", font_size=24, color=HEAD),
                     label(r"the rewritten circuit is simulated again, \ and must still match the specification",
                           font_size=24, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ex, DOWN,
                                                                                                    buff=0.5)
        with self.voiceover(
            "The library can also rewrite a circuit. <bookmark mark='a'/> Every gate is replaced by its construction "
            "from chapter five: a not by one NAND, an and by two, an or by three, an exclusive-or by four. "
            "<bookmark mark='b'/> The comparator's twenty-one gates become fifty-three NANDs; the barrel shifter's "
            "ninety-six become a hundred and ninety-two. <bookmark mark='c'/> And then the rewritten circuit goes "
            "through the same exhaustive check as the original. That is how Part 6 can honestly say that Pebble runs "
            "on nothing but NAND gates: the claim is checked, not assumed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rules], lag_ratio=0.3), run_time=2.2)
            vo.wait_until("b")
            self.play(FadeIn(ex, lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verify(self):
        head = label(r"Specification against implementation", font_size=36).to_edge(UP, buff=0.35)
        left = VGroup(label(r"specification", font_size=28, color=CTRL),
                      code_block(["lt = (a < b)", "eq = (a == b)"], font_size=24)).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"implementation", font_size=28, color=CTRL),
                       label(r"45 gates, \ depth 10", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=2.4).move_to(UP * 0.8)
        arrow = MathTex(r"\overset{?}{=}", font_size=50).move_to((left.get_center() + right.get_center()) / 2)
        ok = label(r"equal on all 65{,}536 inputs \ $\checkmark$", font_size=30, color=YES).next_to(VGroup(left, right),
                                                                                                DOWN, buff=0.7)
        lim = VGroup(label(r"exhaustive checking stops at about 30 input bits", font_size=26, color=GREY_A),
                     label(r"beyond that: \ BDDs (chapter 8), \ SAT solvers (Part 26), \ proofs (Part 54)",
                           font_size=26, color=HEAD)).arrange(DOWN, buff=0.2).next_to(ok, DOWN, buff=0.5)
        with self.voiceover(
            "So every block in this series is checked the same way. <bookmark mark='a'/> On one side, the "
            "specification, written as plain arithmetic. On the other, the gate-level implementation. "
            "<bookmark mark='b'/> Run both on every possible input, and compare. For the comparator, sixty-five "
            "thousand inputs, all equal. <bookmark mark='c'/> This only works for small blocks: at thirty-two input "
            "bits there are four billion cases, and a sixty-four-bit adder has two to the hundred and twenty-eight. "
            "Beyond that, verification needs the decision diagrams of chapter eight, the satisfiability solvers of "
            "Part 26, or the machine-checked proofs of Part 54."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), FadeIn(arrow))
            vo.wait_until("b")
            self.play(FadeIn(ok))
            vo.wait_until("c")
            self.play(FadeIn(lim))
        self.wait(0.3)
        self.clear_scene()
