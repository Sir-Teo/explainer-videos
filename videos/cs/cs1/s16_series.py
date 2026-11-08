from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs import LAYER_COLOR
from videos.cs.cs1.common import CODE, COST, CTRL, DATA, HEAD, LIMIT, PART, YES, live_int, load

ACT_LAYERS = [
    (r"I. \ The Machine", ("physics", "gates", "arith", "isa")),
    (r"II. \ Making It Fast", ("uarch",)),
    (r"III. \ Speaking to the Machine", ("code", "lang")),
    (r"IV. \ Algorithms", ("algo",)),
    (r"V. \ Limits and Secrets", ("limits",)),
    (r"VI. \ One Machine, Many Programs", ("os", "data")),
    (r"VII. \ Many Machines", ("net", "dist")),
    (r"VIII--IX. \ Building Software, \ Systems at Scale", ("cloud", "practice")),
    (r"X. \ Horizons and Trust", ("apps",)),
]


class Series(VoiceoverScene):
    def construct(self):
        self.card()
        self.lesson()
        self.tower_tour()
        self.pebble()
        self.job()
        self.practice()

    def card(self):
        card = chapter_card(15, r"What we will build", r"From Turing's paper machine to a real one", part=PART,
                            layers=tuple(k for k, _ in __import__("explainer.cs", fromlist=["LAYERS"]).LAYERS))
        with self.voiceover("Chapter fifteen. What we will build."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lesson(self):
        lines = VGroup(*[label(t, font_size=34, color=c) for t, c in (
            (r"to compute is to follow finite rules on symbols", DATA),
            (r"one machine, given a description, can do what any machine does", CODE),
            (r"and some questions no machine can answer", LIMIT),
        )]).arrange(DOWN, buff=0.55).move_to(UP * 0.3)
        with self.voiceover(
            "Here is what this part found. <bookmark mark='a'/> Computing is following finite rules on symbols, and every "
            "reasonable way of saying that precisely gives the same answer. <bookmark mark='b'/> One machine, given a "
            "description, can do what any machine does. <bookmark mark='c'/> And some questions, including whether a "
            "program halts, no machine can answer."
        ) as vo:
            for mk, l in zip("abc", lines):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tower_tour(self):
        tw = tower(lit=("math", "limits"), labels="all", height=6.6, width=4.2, font_size=20).move_to(LEFT * 2.6)
        acts = VGroup()
        for name, keys in ACT_LAYERS:
            ys = [tw.layer[k].get_y() if k in tw.layer else tw.column[k].get_y() for k in keys]
            t = label(name, font_size=22, color=LAYER_COLOR.get(keys[0], C.CS_LIMIT if keys[0] == "limits"
                                                                  else C.CS_PRACTICE))
            t.move_to([3.0, float(np.mean(ys)), 0]).set_x(1.6 + t.width / 2 + 0.5)
            acts.add(t)
        acts.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tw, RIGHT, buff=1.0)
        research = label(r"XI. \ The Research Frontier (56--61)", font_size=22, color=HEAD)
        research.next_to(acts, DOWN, buff=0.35).align_to(acts, LEFT)
        here = label(r"Part 1 stands here: \ the ground floor of ideas", font_size=24, color=C.CS_INF)
        here.next_to(tw.layer["math"], DOWN, buff=0.15)

        def lit_tower(keys):
            return tower(lit=keys, labels="all", height=6.6, width=4.2, font_size=20).move_to(tw)

        with self.voiceover(
            "Now we build. This is the tower the series climbs. <bookmark mark='a'/> At the bottom, mathematics and logic, "
            "where this part stands, with the limits beside it. <bookmark mark='b'/> Act one builds a computer from "
            "switches: gates, arithmetic, memory, an instruction set. <bookmark mark='c'/> Act two makes it fast. "
            "<bookmark mark='d'/> Act three teaches it languages. <bookmark mark='e'/> Act four is algorithms. "
            "<bookmark mark='f'/> Act five returns to the limits, and turns them into cryptography. "
            "<bookmark mark='g'/> Act six shares one machine among many programs, act seven connects many machines, "
            "<bookmark mark='h'/> acts eight and nine are how industry builds and runs software at scale, "
            "<bookmark mark='i'/> and act ten looks at the horizons, and at whether we can trust the whole thing. "
            "<bookmark mark='j'/> Act eleven revisits these ideas at research depth: spectral graphs, learning theory, "
            "semantics, distributed computing, specialized hardware, and how to do research."
        ) as vo:
            self.play(FadeIn(tw))
            vo.wait_until("a")
            self.play(FadeIn(here))
            lit = ["math", "limits"]
            for k, mk in enumerate("bcdefghi"):
                vo.wait_until(mk)
                lit += list(ACT_LAYERS[k][1])
                if mk == "i":
                    lit += list(ACT_LAYERS[8][1])
                    self.play(Transform(tw, lit_tower(tuple(lit))), FadeIn(acts[k]), FadeIn(acts[8]), run_time=0.8)
                else:
                    self.play(Transform(tw, lit_tower(tuple(lit))), FadeIn(acts[k]), run_time=0.8)
            vo.wait_until("j")
            self.play(FadeIn(research, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pebble(self):
        d = load("pebble")
        src = d["source"]
        code = code_block(src, font_size=24, color=GREY_A)
        code.to_edge(LEFT, buff=0.9).set_y(0.2)
        for row, ln in zip(code, src):  # dim the comments, colour the labels
            if "#" in ln:
                k = len(ln[:ln.index("#")].replace(" ", ""))
                row[k:].set_color(GREY_C)
            if ":" in ln.split("#")[0]:
                row[:ln.index(":") + 1].set_color(CTRL)
        pc = Triangle(color=HEAD, fill_opacity=1, stroke_width=0).rotate(-PI / 2).scale_to_fit_height(0.2)
        pc.next_to(code[0], LEFT, buff=0.2)
        regs = VGroup()
        vals = {}
        for name, col in (("a0", DATA), ("a1", DATA), ("t0", GREY_A)):
            n = live_int(0, 34, col)
            vals[name] = n
            row = VGroup(Text(name, font="DejaVu Sans Mono", font_size=26, color=GREY_B), n).arrange(RIGHT, buff=0.4)
            n.add_updater(lambda m, row=row: m.next_to(row[0], RIGHT, buff=0.4))
            regs.add(row)
        regs.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 5.3 + UP * 0.8)
        rbox = SurroundingRectangle(regs, buff=0.3, color=GREY_C, corner_radius=0.12)
        rl = label(r"registers", font_size=22, color=GREY_B).next_to(rbox, UP, buff=0.12)
        sc = VGroup(label(r"instructions run:", font_size=24, color=GREY_A), live_int(0, 30, COST)).arrange(RIGHT, buff=0.2)
        sc.next_to(rbox, DOWN, buff=0.4)
        sc[1].add_updater(lambda m: m.next_to(sc[0], RIGHT, buff=0.2))
        head = label(r"Pebble-32, \ the computer of Part 6, \ running Euclid", font_size=32).to_edge(UP, buff=0.35)
        tag = note(r"computed: \ this series' emulator; \ Part 6 builds the same machine from NAND gates",
                   font_size=22).to_edge(DOWN, buff=0.35)
        tr = d["trace"]
        with self.voiceover(
            "The machine we build has a name: Pebble, after the calculi of the opening. Here is a preview. "
            "<bookmark mark='a'/> This is Euclid's algorithm from chapter one, in Pebble's own machine language: load "
            "the two numbers, then subtract, compare and swap, in a loop. <bookmark mark='b'/> The program runs on "
            "this series' Pebble emulator. Watch the registers: a zero and a one hold the two numbers, and t zero is "
            f"scratch. <bookmark mark='c'/> After {d['steps']} instructions, a zero holds {d['result']}: the same twenty-one "
            "the rectangle gave us. In Part 6 we build this exact machine out of NAND gates, and it runs this exact "
            "program."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(pc), FadeIn(rbox), FadeIn(regs), FadeIn(rl), FadeIn(sc), FadeIn(tag))
            vo.wait_until("b")
            line_of = {}
            for i, s in enumerate(src):
                line_of[i + 2] = i  # the assembler counts the source's leading blank line as line 1
            for k, step in enumerate(tr):
                rt = 0.45 if k < 14 else 0.12
                tgt = code[line_of[step["line"]]]
                anims = [pc.animate(run_time=rt).next_to(tgt, LEFT, buff=0.2),
                         sc[1].tracker.animate(run_time=rt).set_value(k + 1)]
                for r in ("a0", "a1", "t0"):
                    anims.append(vals[r].tracker.animate(run_time=rt).set_value(step[r]))
                self.play(*anims)
            vo.wait_until("c")
            self.play(Indicate(regs[0], color=YES))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def job(self):
        head = label(r"The Job: \ count the words of thirty novels, \ and list the twenty most common", font_size=32)
        head.to_edge(UP, buff=0.35)
        rows = [{"part": p, "label": t} for p, t in (
            (6, r"Pebble at gate level"), (7, r"a pipeline"), (9, r"caches"), (10, r"four cores"),
            (13, r"an optimizing compiler"), (16, r"sort, then count"), (17, r"a hash table"),
            (20, r"a sketch, in kilobytes"), (24, r"engineered"), (35, r"one line of SQL"), (37, r"over our own TCP"),
            (39, r"on a cluster that loses a node"), (45, r"its bill in dollars"), (49, r"a million books a day"))]
        led = ledger_table(rows, shown=0, font_size=23, row_h=0.38, label_width=5.6).move_to(DOWN * 0.4)
        for r in led.rows:  # nothing is measured yet, but the plan should be readable
            r.name.set_color(GREY_A)
        q = label(r"which matters more: \ better hardware, \ or better ideas?", font_size=28, color=HEAD)
        q.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And one task will travel with us through every layer. The Job: count the words in thirty novels, the same "
            "thirty that AI, Built reads, and list the twenty most common. <bookmark mark='a'/> Each part that changes how "
            "fast or how cheaply the Job can be done adds a row to this ledger, with the time it takes: first on Pebble, "
            "gate by gate, in Part 6, then with pipelines, caches and more cores, a compiler, better algorithms, a "
            "database, a network, and finally a cluster and a cloud bill. <bookmark mark='b'/> The ledger will settle a "
            "question with data: which matters more, better hardware or better ideas?"
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.08), run_time=2.4)
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(r.name, color=HEAD, scale_factor=1.06) for r in led.rows], lag_ratio=0.12),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        card = practice_card([
            (r"emulators and VMs", r"QEMU, \ game-console emulators, \ the Java virtual machine, \ WebAssembly: \ "
                                   r"universal machines in software"),
            (r"interpreters", r"Python, \ JavaScript, \ spreadsheets with formulas: \ a description and a machine "
                              r"that runs it"),
            (r"Turing-completeness", r"surprisingly common, \ and a security risk: \ anything universal can run "
                                     r"code nobody intended (Part 55)"),
            (r"undecidability", r"why linters, \ static analyzers and malware scanners must approximate"),
        ])
        with self.voiceover(
            "In practice, the ideas of this part are everywhere. Emulators and virtual machines are universal machines "
            "in software. Every interpreter is a description and a machine that runs it. Universality turns up in "
            "places nobody planned, which is a security problem, because anything universal can be made to run code "
            "nobody intended; we come back to that in Part 55. And undecidability is why every tool "
            "that checks programs has to approximate."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()
