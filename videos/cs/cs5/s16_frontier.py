from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LIMIT, NO, PART, YES, fmt,
                                  load, say)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): defending memory against Rowhammer, by probability (PARA) and
    by counting (Misra-Gries), against thresholds that keep falling; and the open problem of a provably safe, cheap
    defence."""

    def construct(self):
        self.card()
        self.falling()
        self.para()
        self.counting()
        self.attack()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ defending memory", r"How do you protect memory that leaks?",
                            lit=(1982, 2014, 2020, 2024), part=PART,
                            extra=((1982, r"Misra and Gries: frequent items"), (2014, r"Rowhammer"),
                                   (2020, r"TRRespass; \ Graphene"), (2024, r"DDR5 adds PRAC")))
        with self.voiceover("Chapter fifteen. Frontier: defending memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def falling(self):
        d = load("hammerdefence")
        head = label(r"The threshold keeps falling", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[2012, 2026, 2], y_range=[3, 6, 1], x_length=6.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.6 + DOWN * 0.3)
        ax.x_axis.add_numbers([2014, 2018, 2022], font_size=16, num_decimal_places=0, group_with_commas=False)
        yt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(2012, v), LEFT, buff=0.1)
                      for v, t in ((3, r"1{,}000"), (4, r"10{,}000"), (5, r"100{,}000"))])
        yl = note(r"activations of one row before a neighbour flips \ (log scale)", font_size=18).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        dots, tags = VGroup(), VGroup()
        for k, (yr, t, who) in enumerate(d["thresholds"]):
            p = ax.c2p(yr + 0.25 * k, np.log10(t))
            dots.add(Dot(p, radius=0.08, color=NO))
            tags.add(label(rf"{fmt(t)}: \ {who}", font_size=18, color=GREY_A).next_to(p, RIGHT if k != 1 else LEFT,
                                                                                    buff=0.12))
        side = VGroup(
            label(r"smaller cells hold less charge, \\ and sit closer to their neighbours", font_size=22, color=GREY_A),
            label(rf"one bank can activate a row \\ ${fmt(d['window'])}$ times \ between refreshes \\ (64 ms $\div$ "
                  r"46 ns)", font_size=22, color=COST),
            label(r"so an attacker has a hundred times \\ more activations than it needs", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Chapter twelve met Rowhammer: activate one row of memory often enough and bits flip in its neighbours. "
            "The research since is an arms race. <bookmark mark='a'/> In 2014 it took a hundred and thirty-nine "
            "thousand activations. By 2020, testing more than fifteen hundred chips, the same group found new DDR4 "
            "chips flipping after about ten thousand, and the most vulnerable after four thousand eight hundred per "
            "aggressor row. <bookmark mark='b'/> Smaller cells hold less charge and sit closer together, so every new "
            "generation is weaker. <bookmark mark='c'/> And an attacker has plenty to spend: in the sixty-four "
            "milliseconds between refreshes, one bank can activate a row almost one point four million times. "
            "<bookmark mark='d'/> That is more than a hundred times what it needs."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def para(self):
        d = load("hammerdefence")
        head = label(r"Defence by coin toss \ (PARA, \ 2014)", font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            label(r"on every activation, \ refresh the neighbours with probability $p$", font_size=24, color=CTRL),
            MathTex(r"P(\text{$T$ activations, \ no refresh}) = (1 - p)^{T} \approx e^{-pT}", font_size=36, color=GREY_A),
            MathTex(r"\frac{\text{seconds per year}}{T \cdot t_{RC}} \, e^{-pT} \le 10^{-2}"
                    r"\ \Rightarrow\ p \approx \frac{\ln(\text{attempts}) + \ln 100}{T}", font_size=32, color=HEAD),
        ).arrange(DOWN, buff=0.3).move_to(UP * 1.3)
        rows = VGroup()
        for k, r in enumerate(d["para"]):
            y = -0.9 - 0.42 * (k % 4)
            x = -4.6 if k < 4 else 1.0
            rows.add(VGroup(MathTex(rf"T = {fmt(r['t'])}", font_size=28, color=GREY_A).move_to([x, y, 0],
                                                                                            aligned_edge=LEFT),
                            MathTex(rf"p = {100 * r['p']:.2f}\%", font_size=28,
                                    color=YES if r["p"] < 0.01 else NO).move_to([x + 3.0, y, 0], aligned_edge=LEFT)))
        foot = label(r"no counters, \ no memory: \ but the cost grows like $1/T$, \ and every refresh steals time",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The simplest defence, proposed with the discovery, is a coin toss. <bookmark mark='a'/> On every activation, "
            "refresh the row's neighbours with a small probability p. <bookmark mark='b'/> An attacker who needs T "
            "activations in a row without a refresh succeeds with probability one minus p to the T, about e to the "
            "minus p T. <bookmark mark='c'/> Ask that a year of non-stop hammering succeed with probability below one "
            "percent, and solve for p: the logarithm of the number of attempts, over T. <bookmark mark='d'/> At a "
            "hundred and thirty-nine thousand, p is two hundredths of a percent, almost free. At ten thousand it is "
            "three tenths of a percent, and at a thousand, three percent of all activations, which starts to cost real "
            "performance. Probability buys safety without memory, but its price grows as the threshold falls."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting(self):
        d = load("hammerdefence")
        head = label(r"Defence by counting: \ Misra and Gries \ (1982)", font_size=36).to_edge(UP, buff=0.3)
        alg = VGroup(
            label(r"$k$ counters, \ for the rows seen most often", font_size=22, color=CTRL),
            label(r"a row with a counter: \ add one", font_size=22, color=GREY_A),
            label(r"a new row, \ a free counter: \ take it, \ start at one", font_size=22, color=GREY_A),
            label(r"a new row, \ no free counter: \ subtract one from \textit{every} counter", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 3.2 + UP * 1.2)
        proof = VGroup(
            label(r"each decrement throws away $k + 1$ activations, \ so at most $W/(k + 1)$ decrements:",
                  font_size=22, color=GREY_A),
            MathTex(r"\text{true count} - \text{estimate} \;\le\; \frac{W}{k + 1}", font_size=36, color=HEAD),
            label(r"refresh at $T/2$; \ safe if \ $W/(k + 1) \le T/2$, \ that is \ $k \ge 2W/T$", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 2.6 + DOWN * 1.3)
        tab = VGroup()
        for k, r in enumerate(d["counters"]):
            y = 1.5 - 0.5 * k
            tab.add(VGroup(MathTex(rf"T = {fmt(r['t'])}", font_size=28, color=GREY_A).move_to([3.0, y, 0],
                                                                                           aligned_edge=LEFT),
                           MathTex(rf"k = {fmt(r['k'])}", font_size=28, color=COST).move_to([5.3, y, 0],
                                                                                         aligned_edge=LEFT)))
        th = label(rf"counters per bank, \ $W = {fmt(d['window'])}$", font_size=20, color=GREY_B).next_to(
            tab, UP, buff=0.2)
        gr = label(r"Graphene \ (Park, Litz and Kasikci, \ 2020) \ builds this \\ into the memory controller", font_size=20,
                   color=HIST).next_to(tab, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "The other way is to count. Exact counts for every row would need a counter per row, millions of them. "
            "But the problem is one Part 20 will study, finding the frequent items of a stream, and Jayadev Misra and "
            "David Gries solved it in 1982 with a handful of counters. <bookmark mark='a'/> Keep k counters. A row that "
            "has one adds one; a new row takes a free counter; and when none is free, every counter goes down by one. "
            "<bookmark mark='b'/> Each such decrement cancels k plus one activations, so in a window of W activations "
            "there are at most W over k plus one of them, and no row's estimate falls further below its true count. "
            "<bookmark mark='c'/> Refresh a row's neighbours when its estimate reaches half the threshold, and the true "
            "count stays below the threshold as long as k is at least two W over T. <bookmark mark='d'/> At the 2014 "
            "threshold that is twenty counters per bank. At ten thousand it is two hundred and seventy-seven; at a "
            "thousand, nearly three thousand. Graphene, from 2020, puts exactly this tracker in the memory controller."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in alg], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(proof[0]), Write(proof[1]))
            vo.wait_until("c")
            self.play(FadeIn(proof[2]))
            vo.wait_until("d")
            self.play(FadeIn(th), LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(gr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attack(self):
        d = load("hammerdefence")
        head = label(r"Too few counters: \ the many-sided attack", font_size=36).to_edge(UP, buff=0.3)
        sub = label(rf"simulated: \ {d['sim_aggressors']} aggressor rows in turn, \ one benign access in eight, \ "
                    rf"threshold ${fmt(d['sim_t'])}$, \ one refresh window", font_size=20,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        bars = VGroup()
        top = max(s["max_unrefreshed"] for s in d["sim"])
        for k, s in enumerate(d["sim"]):
            y = 1.1 - 0.85 * k
            w = 7.0 * s["max_unrefreshed"] / top
            r = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=NO if s["flips"] else YES,
                          fill_opacity=0.75).move_to([-3.0 + w / 2, y, 0])
            bars.add(VGroup(label(rf"$k = {s['k']}$", font_size=22, color=GREY_A).next_to([-3.1, y, 0], LEFT, buff=0.1),
                            r, label(rf"${fmt(s['max_unrefreshed'])}$" + (r" \ flips" if s["flips"] else r" \ safe"),
                                     font_size=20, color=NO if s["flips"] else YES).next_to(r, RIGHT, buff=0.12)))
        tl = DashedLine([-3.0 + 7.0 * d["sim_t"] / top, 1.5, 0], [-3.0 + 7.0 * d["sim_t"] / top, -1.9, 0],
                        color=LIMIT, stroke_width=2)
        tll = label(r"threshold", font_size=18, color=LIMIT).next_to(tl, DOWN, buff=0.08)
        notes = VGroup(
            label(r"TRRespass \ (Frigo et al., \ 2020): \ the in-DRAM trackers of real DDR4 had only a few counters; \\ "
                  r"hammering many rows at once defeated them", font_size=20, color=GREY_A),
            label(r"64 counters survived this pattern by luck; \ only $k \ge 2W/T = 277$ is guaranteed against every "
                  r"pattern", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What happens with too few counters? <bookmark mark='a'/> We simulated an attacker who hammers twenty rows "
            "in turn, with ordinary traffic mixed in, for one refresh window, against trackers of different sizes. "
            "<bookmark mark='b'/> With four or sixteen counters, the twenty rows keep knocking each other out of the "
            "table, nothing is ever refreshed, and each aggressor reaches sixty thousand activations, six times the "
            "threshold. <bookmark mark='c'/> This is what the TRRespass researchers found in real DDR4 chips in 2020: "
            "the manufacturers' trackers had only a few counters, and hammering many rows at once broke them. "
            "<bookmark mark='d'/> Sixty-four counters happened to survive this particular pattern; only the two hundred "
            "and seventy-seven of the bound survive every pattern. Measured luck is not a guarantee; a proof is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(Create(tl), FadeIn(tll))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                                    for b in bars[:2]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                                    for b in bars[2:]], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        head = label(r"Where the research stands", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"\textbf{new physics.} \ Half-Double \ (Google, \ 2021): \ rows two away flip too; \ RowPress \ (2023): "
                  r"\\ keeping a row open \textit{longer} disturbs its neighbours with far fewer activations",
                  font_size=21, color=NO),
            label(r"\textbf{counting inside the chip.} \ DDR5's 2024 update adds PRAC: \ a counter beside every row, \\ "
                  r"and a signal that tells the controller to pause for refreshes \ (and new timing side channels)",
                  font_size=21, color=CTRL),
            label(r"\textbf{cheaper trackers.} \ count-min sketches \ (Part 20) \ instead of Misra--Gries \ (CoMeT, \ "
                  r"2024): \\ fewer bits, \ a probabilistic guarantee", font_size=21, color=DATA),
            label(r"\textbf{open:} \ a defence that is provably safe against every access pattern, \\ for thresholds of a "
                  r"few hundred, \ at a cost that does not grow as $1/T$", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.15)
        with self.voiceover(
            "Where the research stands. <bookmark mark='a'/> The physics keeps surprising: Google's Half-Double showed "
            "in 2021 that rows two away from the aggressor flip too, and RowPress in 2023 that holding a row open "
            "longer, rather than opening it more often, disturbs its neighbours with far fewer activations. "
            "<bookmark mark='b'/> The industry has moved the counting into the chip. The 2024 update to the DDR5 "
            "standard adds a counter beside every single row, and a way for the memory to ask the controller for time "
            "to refresh, which researchers have already shown leaks timing information. <bookmark mark='c'/> Others "
            "replace Misra and Gries with the count-min sketch of Part 20, trading certainty for space. "
            "<bookmark mark='d'/> The open problem: a defence that is provably safe against every pattern of access, "
            "at thresholds of a few hundred, whose cost does not grow as the threshold falls. Memory that remembers "
            "reliably is, once again, a research question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
