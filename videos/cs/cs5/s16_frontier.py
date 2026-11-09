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
        head = label('Reported thresholds: 2014 and 2020 experiments', font_size=36).to_edge(UP, buff=0.3)
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
            "Chapter twelve met Rowhammer: activate one row of memory often enough and bits flip in its "
            "neighbours. The research since is an arms race. <bookmark mark='a'/> In 2014 it took a hundred and "
            "thirty-nine thousand activations. By 2020, a study of more than fifteen hundred chips, with "
            "mitigations disabled, found some newer DDR4 thresholds around ten thousand. The most vulnerable "
            "tested device flipped after about four thousand eight hundred activations to each of two aggressors, "
            "nine thousand six hundred total. <bookmark mark='b'/> Smaller cells hold less charge and sit closer "
            "together, and many tested devices became more vulnerable; this is a measured trend, not a universal "
            "rule for every generation. <bookmark mark='c'/> And an attacker has plenty to spend: in the "
            "sixty-four milliseconds between refreshes, the idealized per-bank budget is almost one point four "
            "million activations, ignoring refresh and mitigation overhead. <bookmark mark='d'/> That is more "
            "than a hundred times what it needs."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(yl), FadeIn(dots), FadeIn(tags))
            vo.wait_until("a")
            self.play(Indicate(dots, scale_factor=1.1))
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
        head = label('Coin-toss model, inspired by PARA (2014)', font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            label(r"toy model: refresh all victim neighbours with independent probability $p$", font_size=23, color=CTRL),
            MathTex(r"(1-p)^T\approx e^{-pT};\quad P_{\mathrm{year}}\le N(1-p)^T\le10^{-2}", font_size=32, color=GREY_A),
            MathTex(r"N=\left\lceil\frac{\mathrm{year}}{t_{RC}}\right\rceil,\quad p\ge1-(10^{-2}/N)^{1/T}", font_size=32, color=HEAD),
        ).arrange(DOWN, buff=0.3).move_to(UP*1.3)
        rows = VGroup()
        for k, r in enumerate(d["para"]):
            y = -0.9 - 0.42 * (k % 4)
            x = -4.6 if k < 4 else 1.0
            rows.add(VGroup(MathTex(rf"T = {fmt(r['t'])}", font_size=28, color=GREY_A).move_to([x, y, 0],
                                                                                            aligned_edge=LEFT),
                            MathTex(rf"p = {100 * r['p']:.2f}\%", font_size=28,
                                    color=YES if r["p"] < 0.01 else NO).move_to([x + 3.0, y, 0], aligned_edge=LEFT)))
        foot = label('no per-row counters; every activation can end a run; refresh cost grows as $T$ falls',
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The simplest defence, proposed with the discovery, is a coin toss. <bookmark mark='a'/> In our "
            "simplified variant, refresh all modeled victim neighbors with independent probability p on each "
            "activation. Original PARA selects an adjacent row; its selection probability must also be included. "
            "<bookmark mark='b'/> An attacker who needs T activations in a row without a refresh succeeds with "
            "probability one minus p to the T, about e to the minus p T. <bookmark mark='c'/> For a conservative "
            "one-percent annual bound per bank in this model, count every possible ending activation: at most "
            "seconds per year divided by the row-cycle time. Multiply that budget by the probability of one "
            "unrefreshed run. This union bound also covers overlapping runs; it does not assume those runs are "
            "independent. <bookmark mark='d'/> At a hundred and thirty-nine thousand, p is about three hundredths "
            "of a percent. At ten thousand it is about four tenths of a percent, and at a thousand, nearly four "
            "percent of all activations. Each successful coin toss refreshes the modeled victim neighbors. This "
            "union-bound calculation assumes the stated trial and timing model. It illustrates a "
            "storage-versus-refresh tradeoff, not a certificate for arbitrary physical disturbance patterns."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(Indicate(eqs[0], scale_factor=1.03))
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
            label(r"$k$ positive counters; a bounded-window teaching model", font_size=20, color=CTRL),
            label(r"tracked row: add one", font_size=20, color=GREY_A),
            label(r"new row, free slot: insert count one", font_size=20, color=GREY_A),
            label(r"full table: decrement all; remove zero entries", font_size=20, color=GREY_A),
            label(r"after modeled victim refresh: remove that row's counter", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT*3.2+UP*1.2)
        proof = VGroup(
            label(r"each decrement consumes $k+1$ events; at most $\lfloor W/(k+1)\rfloor$", font_size=20, color=GREY_A),
            MathTex(r"\text{true count}-\text{estimate}\le\left\lfloor\frac{W}{k+1}\right\rfloor", font_size=32, color=HEAD),
            label(r"since last modeled victim refresh, within one aligned window", font_size=19, color=GREY_B),
            label(r"immediate refresh at $T/2$; $k\ge2W/T$ is sufficient, not necessary", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT*2.6+DOWN*1.3)
        tab = VGroup()
        for k, r in enumerate(d["counters"]):
            y = 1.5 - 0.5 * k
            tab.add(VGroup(MathTex(rf"T = {fmt(r['t'])}", font_size=28, color=GREY_A).move_to([3.0, y, 0],
                                                                                           aligned_edge=LEFT),
                           MathTex(rf"k = {fmt(r['k'])}", font_size=28, color=COST).move_to([5.3, y, 0],
                                                                                         aligned_edge=LEFT)))
        th = label(rf"counters per bank, \ $W = {fmt(d['window'])}$", font_size=20, color=GREY_B).next_to(
            tab, UP, buff=0.2)
        gr = label(r"Graphene \ (Park et al., \ 2020): \\ related counting, with a spillover table", font_size=20,
                   color=HIST).next_to(tab, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "The other way is to count. Exact counts for every row would need a counter per row, millions of "
            "them. But the problem is one Part 20 will study, finding the frequent items of a stream, and Jayadev "
            "Misra and David Gries solved it in 1982 with a handful of counters. <bookmark mark='a'/> Keep k "
            "counters. A row that has one adds one; a new row takes a free counter; and when none is free, every "
            "counter goes down by one and zero entries are removed. After a modeled victim refresh, remove that "
            "row's counter too, so no occupied zero can become negative. <bookmark mark='b'/> Each such decrement "
            "cancels k plus one activations, so in a window of W activations there are at most W over k plus one "
            "of them, and no row's estimate falls further below its true count. <bookmark mark='c'/> Refresh a "
            "row's neighbours when its estimate reaches half the threshold, and the count stays below threshold "
            "in this bounded-window, immediate-refresh teaching model if k is at least two W over T. This is a "
            "sufficient choice, not a minimum-counter theorem. <bookmark mark='d'/> At the 2014 threshold that is "
            "twenty counters per bank. At ten thousand it is two hundred and seventy-seven; at a thousand, nearly "
            "three thousand. Graphene, by Park and colleagues in 2020, also builds on frequent-item counting, but "
            "uses a spillover-counter implementation and accounts for refresh-window alignment and multiple "
            "contributing aggressors. Our toy tracker is not its full physical guarantee."
        ) as vo:
            self.play(FadeIn(head), FadeIn(alg))
            vo.wait_until("a")
            self.play(Indicate(alg, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(proof[0]), Write(proof[1]))
            vo.wait_until("c")
            self.play(FadeIn(proof[2]), FadeIn(proof[3]))
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
                            r, label(rf"${fmt(s['max_unrefreshed'])}$" + (r" \ above T" if s["flips"] else r" \ below T"),
                                     font_size=20, color=NO if s["flips"] else YES).next_to(r, RIGHT, buff=0.12)))
        tl = DashedLine([-3.0 + 7.0 * d["sim_t"] / top, 1.5, 0], [-3.0 + 7.0 * d["sim_t"] / top, -1.9, 0],
                        color=LIMIT, stroke_width=2)
        tll = label(r"threshold", font_size=18, color=LIMIT).next_to(tl, DOWN, buff=0.08)
        notes = VGroup(
            label(r"TRRespass (Frigo et al., 2020): many-sided patterns defeated several deployed trackers; \\ this simulation is a teaching model, not a reproduction of those implementations", font_size=19, color=GREY_A),
            label(r"64 counters passed this trace; $k=277$ is sufficient for this bounded-window model", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What happens with too few counters? <bookmark mark='a'/> We simulated an attacker who hammers twenty "
            "rows in turn, with ordinary traffic mixed in, for one refresh window, against trackers of different "
            "sizes. <bookmark mark='b'/> With four or sixteen counters, the twenty rows keep knocking each other "
            "out of the table, nothing is ever refreshed, and each aggressor reaches sixty thousand activations, "
            "six times the threshold. <bookmark mark='c'/> This illustrates the many-sided idea investigated by "
            "TRRespass in 2020, rather than reproducing its proprietary hardware trackers: the manufacturers' "
            "trackers had only a few counters, and hammering many rows at once broke them. <bookmark mark='d'/> "
            "Sixty-four counters happened to survive this particular pattern; two hundred and seventy-seven is a "
            "sufficient choice from our conservative bound for this one-window model. A passed trace alone is not "
            "a guarantee, and a sufficient bound does not prove smaller trackers impossible. Measured luck is not "
            "a guarantee; a proof is."
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
            label(r"\textbf{physics.} Half-Double (2021), RowPress (2023): \\ neighbour range and row-open time matter", font_size=21, color=NO),
            label(r"\textbf{PRAC.} DDR5 framework (2024): row counts and back-off; \\ safety depends on updates, resets, queues and refresh timing", font_size=21, color=CTRL),
            label(r"\textbf{CoMeT (2024).} Count-min estimates never undercount under specified rules; \\ collisions can increase refresh cost", font_size=21, color=DATA),
            label(r"\textbf{verify the model.} AutoPRAC (June 2026 preprint): reported reset-policy flaw. \\ Research: validated guarantees with affordable area, time, energy and refresh cost", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN*0.15)
        with self.voiceover(
            "Where the research stands. <bookmark mark='a'/> Half-Double in 2021 and RowPress in 2023 show why "
            "the physical model matters: disturbance can reach farther rows, and long row-open times can reduce "
            "the activation count needed for a flip. <bookmark mark='b'/> PRAC is a framework added to the DDR5 "
            "specification in 2024, combining per-row activation counting and controller back-off. Safety still "
            "depends on counting, reset, queuing and refresh choices; support is not a universal deployment "
            "guarantee. <bookmark mark='c'/> CoMeT in 2024 uses count-min sketches that can overcount but do not "
            "undercount under their specified update and reset rules. Hash collisions can increase refresh cost; "
            "randomness here does not simply exchange safety for space. <bookmark mark='d'/> As of November 2026, "
            "a concrete research task is verifying complete implementations against explicit disturbance and "
            "timing models. The June 2026 AutoPRAC preprint reports using model checking to find a reset-policy "
            "flaw in a proposed PRAC design. Its result is attributed here, not independently proved. The "
            "challenge is a sound guarantee with affordable area, delay, energy and refresh cost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(Indicate(r, scale_factor=1.02) if mk == "a" else FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
