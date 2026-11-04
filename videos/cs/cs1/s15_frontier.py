from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LIMIT, NO, PART, YES, fmt, load, say,
                                  spacetime_mob)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): how BB(5) was settled, BB(6) and Antihydra, and the smallest
    machines whose behaviour set theory cannot decide."""

    def construct(self):
        self.card()
        self.proof()
        self.arrows()
        self.antihydra()
        self.walk()
        self.odds()
        self.zfc()

    def card(self):
        card = chapter_card(14, r"Frontier: \ the edge of the knowable", r"Where does mechanical certainty run out?",
                            lit=(2016, 2024, 2025), part=PART,
                            extra=((2016, r"a 7{,}910-state machine beyond ZFC"), (2024, r"BB(5) proved; Antihydra"),
                                   (2025, r"BB(6) $> 10\uparrow\uparrow 10\uparrow\uparrow 10\uparrow\uparrow 8$")))
        with self.voiceover("Chapter fourteen. Frontier: the edge of the knowable."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def proof(self):
        head = label(r"How do you prove a machine never halts?", font_size=36).to_edge(UP, buff=0.35)
        inv = MathTex(r"c_0 \in I", r",\qquad", r"\mathrm{step}(I) \subseteq I", r",\qquad",
                      r"I \cap \mathrm{Halt} = \varnothing", r"\quad\Longrightarrow\quad", r"\text{never halts}",
                      font_size=34).move_to(UP * 1.6)
        inv[0].set_color(DATA)
        inv[2].set_color(CTRL)
        inv[4].set_color(LIMIT)
        inv[6].set_color(YES)
        il = label(r"a certificate: \ a set $I$ of configurations that contains the start, \ is closed under a step, \\ "
                   r"and contains no halting one \ (Part 2's invariants, \ for machines)", font_size=22,
                   color=GREY_A).next_to(inv, DOWN, buff=0.3)
        rows = [
            (r"cyclers", r"the whole configuration repeats"),
            (r"translated cyclers", r"it repeats, shifted along the tape"),
            (r"n-gram, \ repeated words", r"the tape is always made of a finite set of pieces"),
            (r"finite automata reduction", r"a finite automaton recognises a set $I$ like the one above"),
            (r"13 sporadic machines", r"each needed a proof of its own"),
        ]
        tab = VGroup()
        for k, (n, d) in enumerate(rows):
            c = LIMIT if k == 4 else CTRL
            tab.add(VGroup(label(n, font_size=22, color=c), label(d, font_size=20, color=GREY_A)))
        for k, r in enumerate(tab):
            r[0].move_to([-3.2, -0.5 - 0.5 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([-2.9, -0.5 - 0.5 * k, 0], aligned_edge=LEFT)
        foot = label(r"about 100 million five-state machines, \ every one decided, \ the whole proof checked by the "
                     r"Coq proof assistant \ (bbchallenge, \ 2024)", font_size=20, color=HIST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Chapter thirteen ended on the proof that the five-state busy beaver is forty-seven million, one hundred "
            "and seventy-six thousand, eight hundred and seventy. How do you prove that a machine never halts, when "
            "running it cannot? <bookmark mark='a'/> With a certificate: a set of configurations that contains the "
            "starting one, is closed under taking a step, and contains no halting configuration. If such a set exists, "
            "the machine is trapped in it forever. It is the invariant method of Part 2, applied to machines. "
            "<bookmark mark='b'/> The bbchallenge collaboration built deciders that search for certificates of "
            "different shapes: a configuration that repeats; one that repeats shifted along the tape; tapes always built "
            "from a finite set of pieces; and, most powerful, sets of tapes recognised by a finite automaton, which "
            "Part 12 will build. <bookmark mark='c'/> Of about a hundred million five-state machines, all but thirteen "
            "fell to these deciders, and the thirteen sporadic machines each needed an argument of its own. Every step "
            "of the proof was checked by a proof assistant, which Part 54 explains."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(inv), run_time=2.0)
            self.play(FadeIn(il))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tab[:4]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arrows(self):
        f = load("frontier")
        head = label(r"Six states: \ beyond ordinary notation", font_size=36).to_edge(UP, buff=0.35)
        defs = VGroup(
            MathTex(r"10 \uparrow 3 = 10^{3}", font_size=34, color=GREY_A),
            MathTex(r"10 \uparrow\uparrow 3 = 10^{10^{10}}", font_size=34, color=DATA),
            MathTex(r"10 \uparrow\uparrow 15 = \underbrace{10^{10^{\cdot^{\cdot^{10}}}}}_{15 \text{ tens}}",
                    font_size=34, color=COST),
        ).arrange(RIGHT, buff=0.8).move_to(UP * 1.7)
        rows = VGroup()
        for k, (yr, who, s) in enumerate(f["bb6"]):
            y = 0.3 - 0.52 * k
            rows.add(VGroup(label(str(yr), font_size=22, color=HIST).move_to([-5.0, y, 0]),
                            label(who, font_size=22, color=GREY_A).move_to([-3.6, y, 0], aligned_edge=LEFT),
                            MathTex(r"S(6) > " + s, font_size=30, color=COST if k == len(f["bb6"]) - 1 else WHITE
                                    ).move_to([0.2, y, 0], aligned_edge=LEFT)))
        note_ = label(r"each $\uparrow$ iterates the one before: \ $a \uparrow\uparrow b$ \ is a tower of $b$ copies of $a$",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "At six states, ordinary notation fails. <bookmark mark='a'/> Donald Knuth's arrows climb it: one arrow is "
            "a power, ten to the three; two arrows are a tower of powers, so ten double-arrow three is ten to the ten "
            "to the ten. <bookmark mark='b'/> The six-state record was four hundred and thirty-six steps in 1964, thirteen "
            "billion in 1990, and a number of twenty-one thousand digits in 2010. In 2022 Pavel Kropitz found a machine "
            "that runs for more than a tower of fifteen tens. <bookmark mark='c'/> And in June 2025 a contributor known "
            "as mxdys found one whose running time is a tower of tens whose height is itself a tower whose height is a "
            "tower, ten double-arrow ten double-arrow ten double-arrow eight. Nobody will ever run it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in defs], lag_ratio=0.4), FadeIn(note_), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[:-1]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[-1], shift=RIGHT * 0.1))
            self.play(Indicate(rows[-1][2], color=COST))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def antihydra(self):
        f = load("frontier")
        head = label(r"Antihydra, \ a six-state cryptid", font_size=36).to_edge(UP, buff=0.3)
        code = f["table"].split("_")
        cells = [[MathTex(r"\text{state}", font_size=26, color=GREY_B), MathTex(r"\text{read } 0", font_size=26,
                                                                               color=GREY_B),
                  MathTex(r"\text{read } 1", font_size=26, color=GREY_B)]]
        for st, row in zip("ABCDEF", code):
            ents = [row[:3], row[3:]]
            cells.append([MathTex(st, font_size=30, color=CTRL)] + [
                MathTex(r"\text{halt}" if e == "---" else rf"\mathrm{{{e[0]}\,{e[1]}\,{e[2]}}}", font_size=30,
                        color=LIMIT if e == "---" else GREY_A) for e in ents])
        tab = VGroup(*[VGroup(*r) for r in cells])
        for i, r in enumerate(tab):
            for j, c in enumerate(r):
                c.move_to([j * 1.6, -i * 0.55, 0])
        tab.move_to(LEFT * 4.2 + UP * 0.4)
        early = np.asarray(f["early"]).astype(np.int8)
        eh = np.asarray(f["early_heads"])
        st = np.where(early > 0, 1, 0).astype(np.int8)
        for t in range(len(st)):
            if 0 <= eh[t] < st.shape[1]:
                st[t, eh[t]] = 3
        pic = spacetime_mob(st, width=2.6, height=4.8).move_to(RIGHT * 0.2 + DOWN * 0.3)
        pf = SurroundingRectangle(pic, buff=0, color=GREY_C, stroke_width=1)
        pl = label(r"the first 6{,}000 steps", font_size=20, color=GREY_B).next_to(pic, UP, buff=0.12)
        runs = label(rf"run here for ${fmt(f['tm_steps'])}$ steps: \\ no halt, \ {fmt(f['tm_cells'])} cells of tape",
                     font_size=20, color=COST).next_to(pic, DOWN, buff=0.15)
        rule = VGroup(
            label(r"its behaviour, \ decoded \ (Racheline, \ 2024):", font_size=22, color=GREY_A),
            MathTex(r"h \leftarrow 8,\quad c \leftarrow 0", font_size=32, color=DATA),
            MathTex(r"c \leftarrow c + \begin{cases} +2 & h \text{ even} \\ -1 & h \text{ odd} \end{cases}", font_size=32,
                    color=CTRL),
            MathTex(r"h \leftarrow h + \lfloor h/2 \rfloor", font_size=32, color=DATA),
            MathTex(r"\text{halts} \iff c = -1", font_size=32, color=LIMIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.6 + UP * 0.3)
        with self.voiceover(
            "BB(6) cannot be settled the way BB(5) was, because of machines like this one. <bookmark mark='a'/> "
            "It is called Antihydra: six states, one missing transition that would halt it, found by mxdys in June "
            "2024. <bookmark mark='b'/> We ran it here for a hundred million steps. It has not halted, and its tape has "
            "grown to fourteen thousand cells. <bookmark mark='c'/> Racheline decoded what it is doing. It keeps two "
            "numbers, h starting at eight, and a counter c at zero. Each round, if h is even the counter goes up by two, "
            "and if h is odd it goes down by one; then h grows by half of itself, rounded down. The machine halts "
            "exactly when the counter reaches minus one. Each round takes the machine longer than the last, so our "
            "hundred million steps are only about twenty rounds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pic), Create(pf), FadeIn(pl))
            self.play(FadeIn(runs))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rule], lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walk(self):
        f = load("frontier")
        head = label(r"A million rounds", font_size=36).to_edge(UP, buff=0.3)
        first = VGroup()
        hdr = VGroup(*[MathTex(t, font_size=24, color=GREY_B) for t in ("h", r"\text{parity}", "c")])
        for j, m in enumerate(hdr):
            m.move_to([-5.6 + 1.3 * j, 2.4, 0])
        first.add(hdr)
        for i, (h, par, c) in enumerate(f["first"][:10]):
            y = 2.0 - 0.36 * i
            first.add(VGroup(MathTex(str(h), font_size=22, color=DATA).move_to([-5.6, y, 0]),
                             MathTex(r"\text{odd}" if par else r"\text{even}", font_size=22,
                                     color=NO if par else YES).move_to([-4.3, y, 0]),
                             MathTex(str(c), font_size=22, color=CTRL).move_to([-3.0, y, 0])))
        path = np.array(f["c_path"], float)
        n = f["iterations"]
        xs = np.arange(1, len(path) + 1) * 1000
        dev = path - xs / 2
        ax = Axes(x_range=[0, n, n // 4], y_range=[-3000, 3000, 1000], x_length=6.4, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(RIGHT * 2.4 + DOWN * 0.2)
        xt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(x, -3000), DOWN, buff=0.12)
                      for x, t in ((n // 2, r"500{,}000"), (n, r"1{,}000{,}000"))])
        yt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.12)
                      for y, t in ((-2000, r"$-2{,}000$"), (0, r"0"), (2000, r"2{,}000"))])
        xl = note(r"rounds $n$", font_size=18).next_to(xt, DOWN, buff=0.05)
        yl = note(r"$c - n/2$: \ the counter, \ minus a fair coin's average", font_size=18).next_to(ax, UP, buff=0.1
                                                                                            ).align_to(ax, LEFT)
        curve = VMobject(color=CTRL, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(x, y) for x, y in zip(xs[::2], dev[::2])])
        band = VGroup(*[VMobject(color=GREY_B, stroke_width=1.5).set_points_as_corners(
            [ax.c2p(x, sgn * 1.5 * np.sqrt(x)) for x in np.linspace(1, n, 120)]) for sgn in (1, -1)])
        band = VGroup(*[DashedVMobject(b, num_dashes=50) for b in band])
        dl = label(r"$\pm 1.5\sqrt{n}$: \ a random walk's typical wobble", font_size=18, color=GREY_B).next_to(
            ax.c2p(n * 0.5, 1.5 * np.sqrt(n * 0.5)), UP, buff=0.25)
        res = label(rf"after ${fmt(n)}$ rounds: \ $c = {fmt(f['c_final'])}$, \ even {100 * f['even_final']:.2f}\% of "
                    rf"the time; \ $h$ has ${fmt(f['h_bits'])}$ bits", font_size=20, color=COST).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Simulating the rule instead of the machine, a million rounds take half a minute. <bookmark mark='a'/> "
            "Here are the first ten: eight, twelve, eighteen, twenty-seven, forty. Even, even, even, odd. The counter "
            "climbs. <bookmark mark='b'/> If h were even half the time, the counter would rise by half a step per round "
            "on average. So plot what is left when that average is taken away. Over a million rounds the remainder "
            "wanders like a random walk, inside the dashed band where a fair coin's walk usually stays. "
            "<bookmark mark='c'/> After a million rounds the counter stands at nearly half a million, h is even "
            "forty-nine point nine five percent of the time, and h itself has grown to five hundred and eighty-five "
            "thousand bits. Antihydra halts only if, somewhere ahead, odd numbers come so often that this lead is "
            "wiped out."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in first], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(band), FadeIn(dl))
            self.play(Create(curve), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def odds(self):
        f = load("frontier")
        head = label(r"If the parities were coin tosses", font_size=36).to_edge(UP, buff=0.35)
        steps = VGroup(
            MathTex(r"q = P(\text{the counter ever falls by one})", font_size=32, color=GREY_A),
            MathTex(r"q = \tfrac12 \cdot 1 \;+\; \tfrac12 \cdot q^3", font_size=36, color=CTRL),
            MathTex(r"q^3 - 2q + 1 = (q - 1)(q^2 + q - 1) = 0", font_size=36, color=CTRL),
            MathTex(r"q = \frac{\sqrt5 - 1}{2} = \frac{1}{\varphi} \approx 0.618", font_size=40, color=HEAD),
            MathTex(rf"P(\text{{halt}} \mid c) = q^{{\,c+1}} \approx 10^{{-{fmt(round(-f['log10_p']))}}}", font_size=40,
                    color=LIMIT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.3)
        why = VGroup(
            label(r"down one step: \ immediately, \ probability $\tfrac12$; \ or up two, \ and then down three", font_size=20,
                  color=GREY_B),
            label(r"but the parities of $h$ are not random, \ they are determined: \ proving they behave like coins \\ "
                  r"is a problem of the family of Collatz's, \ and of Mahler's $3/2$ problem \ (1968), \ all open",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How likely is that? Pretend the parities are fair coin tosses, and ask for q, the probability that the "
            "counter ever falls by one below where it stands. <bookmark mark='a'/> Either the first toss takes it down "
            "at once, or it goes up two, and must then fall three times, each with probability q. So q equals a half, "
            "plus a half q cubed. <bookmark mark='b'/> The cubic factors, and the root below one is the golden ratio's "
            "reciprocal, zero point six one eight. <bookmark mark='c'/> To reach minus one from a counter at c, it must "
            "fall c plus one times: probability q to the c plus one, which after our million rounds is ten to the "
            "minus one hundred and four thousand. <bookmark mark='d'/> Antihydra almost certainly never halts. But "
            "the parities are not coin tosses: they are fixed by arithmetic. Proving that they behave like coins is a "
            "problem of the same family as the Collatz conjecture and Kurt Mahler's three-halves problem of 1968, and "
            "nobody knows how to do it. Until somebody does, BB(6) is unknown."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(Write(steps[1]), FadeIn(why[0]))
            vo.wait_until("b")
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
            vo.wait_until("c")
            self.play(Write(steps[4]))
            vo.wait_until("d")
            self.play(FadeIn(why[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zfc(self):
        f = load("frontier")
        head = label(r"Where proof itself runs out", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[2015, 2026, 2], y_range=[2, 4, 1], x_length=5.4, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 3.2 + DOWN * 0.2)
        ax.x_axis.add_numbers([2016, 2018, 2020, 2022, 2024], font_size=16, num_decimal_places=0, group_with_commas=False)
        yt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(2015, v), LEFT, buff=0.1)
                      for v, t in ((2, r"100"), (3, r"1{,}000"), (4, r"10{,}000"))])
        yl = note(r"states \ (log scale)", font_size=18).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pts = [ax.c2p(y, np.log10(s)) for y, s, _ in f["zfc"]]
        line = VMobject(color=LIMIT, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, color=LIMIT, radius=0.07) for p in pts])
        dirs = [RIGHT, UP, RIGHT, DOWN]
        tags = VGroup(*[label(rf"{fmt(s)} \ ({w})", font_size=18, color=GREY_A).next_to(p, d, buff=0.12)
                        for (y, s, w), p, d in zip(f["zfc"], pts, dirs)])
        side = VGroup(
            label(r"a machine that halts \ iff \ ZFC is inconsistent: \\ ZFC cannot prove it runs forever \ (G\"odel, "
                  r"Part 25)", font_size=20, color=GREY_A),
            label(r"so BB(432) can never be determined in ZFC, \\ if the 2025 construction checks out \ (it is not yet "
                  r"formally verified)", font_size=20, color=LIMIT),
            label(r"BB(5) is known; \ somewhere between 6 and 432 \\ the values become unknowable: \ where?",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.25).shift(UP * 0.2)
        with self.voiceover(
            "Somewhere above six states, knowledge does not merely become hard; it becomes impossible. "
            "<bookmark mark='a'/> A Turing machine can search through every proof that follows from the axioms of set "
            "theory, halting if it ever finds a contradiction. If the axioms are consistent it never halts, and Gödel's "
            "theorem, which Part 25 proves, says the axioms cannot prove that. So its busy-beaver value can never be "
            "proved. <bookmark mark='b'/> In 2016 Adam Yedidia and Scott Aaronson built such a machine with seven "
            "thousand nine hundred and ten states. Since then, smaller ones: seven hundred and forty-five in 2023, six "
            "hundred and thirty-six in 2024, and four hundred and thirty-two in 2025, though the newest constructions "
            "have not yet been formally verified. <bookmark mark='c'/> So the busy-beaver function is known up to five, "
            "unknown at six, and unknowable by 432. Exactly where the line falls is one of the open questions at the "
            "border of computer science and logic, and a problem in this part's set."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()
