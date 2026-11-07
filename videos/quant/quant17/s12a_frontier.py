from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, load

GROUPS = [
    (r"Simulators of whole option markets", [14, 16], OPT, [
        r"SANOS (Buehler, Horvath, Kratsios, Limmer, Saqur, 2026): smooth, strictly arbitrage-free option surfaces; "
        r"calibration is a linear program",
        r"DYSANOS (Buehler, Horvath, Kratsios, Wiese, 2026): a generative model of those surfaces, day by day; 891 "
        r"S\&P surfaces, 2022--2025; no numerical dynamic arbitrage on 100{,}000 paths",
        r"GROMM (Wiese, Buehler, Horvath, 2026): statically and dynamically arbitrage-free; the initial state within "
        r"bid/ask for more than 95\% of relevant prices",
    ]),
    (r"Is the deep hedger hedging?", [11, 12], BAD, [
        r"Fran\c{c}ois, Gauthier, Godin and P\'erez Mendoza (2024): the gap to delta hedging is a speculative overlay "
        r"unless the risk measure weighs adverse outcomes enough",
        r"Zernikov (2026): TD3 agents on S\&P 500 options, 2015--2023, usually learn a systematic delta haircut, which "
        r"fails in some regimes (2022)",
        r"Godin (2026): deep hedging is Monte Carlo policy search, so it falls within reinforcement learning",
    ]),
    (r"Making it train, and making it real", [13, 14], NET, [
        r"Mueller et al.\ (2024) report, for their cliquet benchmark, about a quarter of the optimizer "
        r"steps",
        r"Arzel and Lehdili (2026): structural Whalley--Wilmott priors and a differentiable soft clamp; chapter 14 uses a different hard clamp",
        r"Fran\c{c}ois, Gauthier, Godin and P\'erez-Mendoza (2025): deep hedging of index option books with the whole "
        r"implied-volatility surface as input, against delta-gamma hedging",
    ]),
    (r"Stopping, duals and generators", [10, 16], GOOD, [
        r"Reppen, Soner and Tissot-Daguette (2022): learn the stopping boundary itself",
        r"Bayer, Pelizzari and Schoenmakers (2023): primal and dual bounds with signatures; Ye and Wong (2025): the "
        r"dual martingale learned",
        r"Issa, Horvath, Lemercier and Salvi (2023): generators trained by signature-kernel scores, without an "
        r"adversary (Part 5 trains one)",
    ]),
]


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.map_(load("band_prior"))

    def card(self):
        c = chapter_card(18, r"The frontier, 2023 to 2026", r"Where is the field now?", part=PART)
        with self.voiceover("Chapter eighteen. The frontier, from 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def map_(self, bp):
        panels = VGroup()
        for title, chs, col, lines in GROUPS:
            head = label(title, font_size=21, color=col)
            tag = label(r"extends chapters " + r" and ".join(str(c) for c in chs), font_size=15, color=GREY_B)
            body = VGroup(*[wrapped_label(t, 5.8, 15, GREY_A) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            inner = VGroup(VGroup(head, tag).arrange(RIGHT, buff=0.25, aligned_edge=DOWN), body).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15)
            box = RoundedRectangle(width=6.4, height=inner.height + 0.3, corner_radius=0.1, stroke_color=col,
                                   stroke_width=1.5).move_to(inner)
            panels.add(VGroup(box, inner))
        grid = VGroup(VGroup(panels[0], panels[1]).arrange(RIGHT, buff=0.2, aligned_edge=UP),
                      VGroup(panels[2], panels[3]).arrange(RIGHT, buff=0.2, aligned_edge=UP)).arrange(DOWN, buff=0.2)
        if grid.height > 7.4:
            grid.scale_to_fit_height(7.4)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "This map summarizes research claims, not deployment audits. In 2026 SANOS, DYSANOS and GROMM address simulated option surfaces and their arbitrage constraints; any theorem or numerical check applies within the paper's construction. <bookmark mark='a'/> Empirical hedging studies ask what policies actually learn. Zernikov's walk-forward S&P study reports delta haircuts whose results change with regime. A return objective can rationally include an investment overlay; that is different from proving better replication. <bookmark mark='b'/> Mueller and coauthors report roughly one quarter as many optimizer steps on their cliquet benchmark, not a universal fourfold wall-time improvement. Arzel and Lehdili combine a structural Whalley–Wilmott prior with a differentiable soft clamp; our hard-clamped experiment is related, not a paper replication. Other work includes richer option hedges. <bookmark mark='c'/> Learned stopping boundaries, signature-based primal and dual methods, and signature-kernel generators expand the toolkit. Their assumptions, computational costs and validation still have to match the intended application."
        ) as vo:
            self.play(FadeIn(panels[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(panels[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(panels[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(panels[3], shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()
        runs_d = np.array([bp["runs"][f"default_{s}"]["curve"] for s in (0, 1)])
        runs_w = np.array([bp["runs"][f"ww_{s}"]["curve"] for s in (0, 1)])
        early = int(runs_d.shape[1] * 0.15)
        a_d, a_w = float(runs_d[:, :early].mean()), float(runs_w[:, :early].mean())
        if a_w < a_d:
            verdict = "the hard-clamped structural prior has lower early mean empirical risk in these two seeds"
        else:
            verdict = "the hard-clamped structural prior is not ahead by early mean empirical risk in these two seeds"
        box = VGroup(label(r"A related small experiment, not a replication", font_size=30, color=QC.IDEA),
                     wrapped_label(r"Arzel and Lehdili (2026): a Whalley--Wilmott prior makes band networks converge "
                                   r"faster", 10.0, 24, GREY_A),
                     wrapped_label(rf"chapter 14, two seeds each, 0.5\% costs: average risk over the first "
                                   rf"{early} steps {a_w:.3f} with the structural prior, {a_d:.3f} with the default",
                                   10.0, 24, NET)).arrange(DOWN, buff=0.4)
        q = ask(r"which is harder to build: a hedger, or the simulator it trains on?")
        with self.voiceover(
            f"Chapter fourteen compares a related structural prior, with a different clamp and persistent width limits. In its two seeds, {verdict}. This early average mixes training objectives from changing weights; it does not establish convergence speed at matched accuracy or reproduce the paper. <bookmark mark='a'/> The displayed averages use the first {early} saved training points, with identical budgets. <bookmark mark='b'/> Which is harder to build, a hedger or its simulator? There is no universal ranking. A precise question is whether an evaluation stresses errors shared by both. Chapter nineteen sets out that test design."
        ) as vo:
            self.play(FadeIn(box[0]), FadeIn(box[1]))
            vo.wait_until("a")
            self.play(FadeIn(box[2]))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.6)
        self.clear_scene()
