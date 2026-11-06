from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import pebble_pile
from videos.cs.cs1.compute import load as load1
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

ACTS = [(r"I", r"The Machine", r"gates, \ arithmetic, \ memory, \ a computer"),
        (r"II", r"Making It Fast", r"pipelines, \ out of order, \ caches, \ many cores"),
        (r"III", r"Speaking to the Machine", r"languages, \ compilers, \ types, \ runtimes"),
        (r"IV", r"Algorithms", r"sorting, \ structures, \ graphs, \ paradigms"),
        (r"V", r"Limits and Secrets", r"undecidability, \ NP, \ proofs, \ codes, \ keys"),
        (r"VI", r"One Machine, Many Programs", r"kernels, \ memory, \ concurrency, \ storage"),
        (r"VII", r"Many Machines", r"networks, \ consensus, \ scale"),
        (r"VIII", r"Building Software", r"engineering, \ builds, \ the web, \ services"),
        (r"IX", r"Systems at Scale", r"people, \ the cloud, \ data, \ search, \ design"),
        (r"X", r"Horizons and Trust", r"pixels, \ numerics, \ quantum, \ proof, \ trust")]


class Outro(VoiceoverScene):
    def construct(self):
        self.pebbles()
        self.acts()
        self.ledger()
        self.problems()
        self.goodbye()

    def pebbles(self):
        d = load1("pebbles")
        steps = d["steps"]
        L, R = np.array([-3.4, -1.9, 0]), np.array([3.4, -1.9, 0])
        head = label(r"The pebble again", font_size=36).to_edge(UP, buff=0.3)
        left = pebble_pile(steps[0][0], L, cols=6, seed=1, radius=0.2)
        right = pebble_pile(steps[0][1], R, cols=6, seed=40, radius=0.2)
        cl = Integer(steps[0][0], font_size=54, color=DATA).move_to(L + UP * 2.8)
        cr = Integer(steps[0][1], font_size=54, color=DATA).move_to(R + UP * 2.8)
        rule = label(r"if the piles differ, \ take from the bigger as many as the smaller has", font_size=24,
                     color=GREY_A).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Part 1 began with two piles of pebbles and one rule: if the piles differ, take from the bigger as many "
            "as the smaller has, and stop when they are equal. <bookmark mark='a'/> Twenty-four and eighteen became "
            "six and six, and six was the greatest common divisor, found by someone who knew nothing about numbers. "
            "<bookmark mark='b'/> That rule was an algorithm, and Hilbert's question, whether every such question "
            "could be settled by a rule, led to Turing's machine, and Turing's machine to everything this series "
            "built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule), FadeIn(left), FadeIn(right), FadeIn(cl), FadeIn(cr))
            vo.wait_until("a")
            for a, b in steps[1:]:
                nl = pebble_pile(a, L, cols=6, seed=1, radius=0.2)
                nr = pebble_pile(b, R, cols=6, seed=40, radius=0.2)
                self.play(Transform(left, nl), Transform(right, nr),
                          Transform(cl, Integer(a, font_size=54, color=DATA).move_to(cl)),
                          Transform(cr, Integer(b, font_size=54, color=DATA).move_to(cr)), run_time=0.8)
            self.play(cl.animate.set_color(YES), cr.animate.set_color(YES))
            vo.wait_until("b")
            self.play(Indicate(rule, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def acts(self):
        head = label(r"Ten acts, \ one tower", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        cols = (DATA, HEAD, YES, KERN, NO, LAM, DATA, HEAD, YES, KERN)
        for (num, name, what), c in zip(ACTS, cols):
            box = Rectangle(width=12.4, height=0.5, stroke_color=c, stroke_width=1.5, fill_color=BG, fill_opacity=1)
            t = VGroup(label(rf"Act {num}", font_size=18, color=c), label(name, font_size=19, color=WHITE),
                       label(what, font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.4)
            t.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.2)
            rows.add(VGroup(box, t))
        rows.arrange(UP, buff=0.07).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Ten acts built one tower. <bookmark mark='a'/> Gates and arithmetic and memory became a computer, and "
            "pipelines and caches made it fast. Languages and compilers let us speak to it; algorithms told it what "
            "to do; and the limits of computation and the mathematics of secrets told us what it can never do and "
            "what it can keep hidden. <bookmark mark='b'/> A kernel let one machine run many programs; networks and "
            "consensus joined many machines; engineering, services and the cloud let people build on them at scale; "
            "and the last act looked outward, to pixels, numbers, quantum machines, proofs, and trust. "
            "<bookmark mark='c'/> Every layer rested on the one below it, and every one of them was built here, from "
            "nothing but the layer below."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows[:5]], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows[5:]], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(*[r[0].animate.set_fill(cols[i], opacity=0.12) for i, r in enumerate(rows)])
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        head = label(r"The ledger, \ row 20", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.24,
                           label_width=4.8).scale(0.8).move_to(UP * 0.6)
        first, last = led[0], led[-1]
        notes = VGroup(
            label(rf"Part 6's single-cycle Pebble: \ {first['seconds']:.0f} s; \ Part 15's $\lambda$-core: \ hours",
                  font_size=19, color=GREY_A),
            label(rf"row 20: \ one line of Python on this machine, \ {last['seconds']:.2f} s", font_size=19,
                  color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And the Job, counting the words of thirty novels, kept its ledger the whole way. <bookmark mark='a'/> "
            f"Part 6's single-cycle Pebble took {first['seconds']:.0f} seconds; Part 15's lambda-calculus machine took "
            "hours; caches, cores, compilers, algorithms, networks and services moved the bar back and forth across "
            "the axis. <bookmark mark='b'/> Row twenty is the plainest of all: one line of Python on this machine, "
            f"about {last['seconds']:.1f} seconds. Every layer of the series is inside that one line, which is the "
            "point of building the tower: so that one line is all you need to write."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Compute the entropy of a 30-bit ASLR offset, \\ and the expected attempts with and without "
            r"re-randomization.",
            r"Find the gadgets for a ROP chain that writes one byte to the console on Pebble.",
            r"Trace Lowe's attack on Needham--Schroeder, \\ and show why naming $B$ in message 2 stops it.",
            r"Show that SQL with bound parameters cannot be injected, \\ by an argument about the parser.",
            r"\\textit{Build.} \\ Trojan our compiler in a new way, \\ and show diverse double-compiling still "
            r"detects it.",
            r"$\\bigstar$ \\textit{Research.} \\ A provably correct, \\ reproducible stack from an auditable seed.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: hide a different trojan in our compiler and show that diverse double-compiling still catches "
            "it. The last, marked with a star, is a research problem: a whole software stack, grown from a seed "
            "small enough to read, with every step proved."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def goodbye(self):
        card = reference_card(
            [r"Anderson, \\ \\textit{Security Engineering} \\ (3rd ed.); \\ Bishop, \\ \\textit{Computer Security}",
             r"Abelson and Sussman; \\ Bryant and O'Hallaron; \\ Hennessy and Patterson; \\ Sipser; \\ CLRS"],
            [r"Thompson \\ (1984); \\ Wheeler \\ (2009); \\ Saltzer and Schroeder \\ (1975)",
             r"Shacham \\ (2007); \\ Kocher et al. \\ (2019); \\ Lowe \\ (1996)",
             r"Lampson \\ (1974); \\ Harrison, \\ Ruzzo and Ullman \\ (1976)",
             r"Szekeres et al. \\ (2013); \\ Jung et al. \\ (2018)"])
        nxt = label(r"Next: \\ Act XI, \\ the research frontier", font_size=30, color=HEAD).to_edge(UP, buff=0.3)
        credit = note(rf"narration: \\ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "This is where the degree ends. The final reading list is on screen and in the notes: the books that "
            "this whole series has leaned on, and the papers behind this part. Act Eleven goes on to the research "
            "frontier, six parts at the level of a first year of a doctorate, for anyone who wants to keep "
            "climbing. Thank you for building it with me."
        ):
            self.play(FadeIn(card), FadeIn(credit), FadeIn(nxt))
        self.wait(3.0)


_ = (NO, YES, KERN, LAM, DATA, PART)
