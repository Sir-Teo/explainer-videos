from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (COLOR, HIST, NAME, PART, PIX, SIMCLR, SPOKEN, axes, curve, digit, heat, load, pct,
                                   take_away)

TOP = "#FFB070"
BOT = "#7FD3FF"


class Platonic(VoiceoverScene):
    def construct(self):
        self.card()
        self.cka()
        self.matrix()
        self.hypothesis()
        self.across()
        self.halves()
        self.limits()

    def card(self):
        card = chapter_card(15, r"Do all models see the same world?", r"Comparing representations, \ and the platonic "
                            r"hypothesis", lit=(), part=PART)
        with self.voiceover("Chapter fifteen. Do all models see the same world?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cka(self):
        rows = [
            cmath(r"K = X X^\top", r",\quad", r"L = Y Y^\top", font_size=36),
            cmath(r"\mathrm{HSIC}", r"=", r"\tfrac{1}{(n-1)^2}\,\big\langle HKH,\, HLH \big\rangle_F", font_size=36),
            cmath(r"\mathrm{HSIC}", r"=", r"\tfrac{1}{(n-1)^2}\,\big\| \tilde Y^\top \tilde X \big\|_F^2", font_size=36),
            cmath(r"\mathrm{CKA}", r"=", r"\frac{\| \tilde Y^\top \tilde X \|_F^2}{\| \tilde X^\top \tilde X \|_F\, "
                  r"\| \tilde Y^\top \tilde Y \|_F}", font_size=36),
            cmath(r"X \mapsto c\,XQ", r":", r"\mathrm{CKA}\ \text{unchanged}", font_size=36),
        ]
        whys = [why(r"every pair of inputs, \ compared in each representation"),
                why(r"$H$ centres; \ how alike the two similarity tables are"),
                why(r"$\mathrm{tr}(\tilde X \tilde X^\top \tilde Y \tilde Y^\top) = \|\tilde Y^\top \tilde X\|_F^2$"),
                why(r"normalized: \ $1$ for the same geometry"),
                why(r"$Q Q^\top = I$; \ $c^2$ cancels; \ not for every invertible map")]
        step = ladder(self, rows, whys, keep=5, top=3.0, x=-2.0, buff=0.45, edge=6.9)
        src = cite(r"Kornblith, Norouzi, Lee \& Hinton (2019): \ CKA")
        with self.voiceover(
            "How do you compare what two networks learned? Their coordinates mean nothing by themselves: rotate a "
            "representation and nothing it knows has changed. So compare geometry instead. For a set of inputs, "
            "list how similar every pair is, in each representation. <bookmark mark='a'/> Centre those two tables "
            "and measure how alike they are: a statistic called HSIC. <bookmark mark='b'/> With plain dot products it "
            "becomes the squared size of the cross-product of the two centred representations. <bookmark mark='c'/> "
            "Normalize it, and you have centred kernel alignment, CKA: one when the two have the same geometry. "
            "<bookmark mark='d'/> It ignores rotations and overall scale, but, as Simon Kornblith and his co-authors "
            "argued, not every invertible map: in high dimensions, a measure that forgave every linear map would "
            "find any two networks identical."
        ) as vo:
            step(0)
            self.play(FadeIn(src))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrix(self):
        c = load("compare")
        names = list(c["names"])
        Cm = np.asarray(c["cka"], float)
        n = len(names)
        S = 4.8
        hm = heat(Cm, S, S, vmax=1.0, signed=False, pos=SIMCLR, gamma=1.0).move_to([-1.6, -0.3, 0])
        cell = S / n
        rl = VGroup(*[label(NAME[nm_], font_size=15, color=COLOR[nm_]).next_to(
            hm.get_corner(UL) + DOWN * cell * (i + 0.5), LEFT, buff=0.1) for i, nm_ in enumerate(names)])
        cl = VGroup(*[label(NAME[nm_], font_size=15, color=COLOR[nm_]).rotate(PI / 3).next_to(
            hm.get_corner(UL) + RIGHT * cell * (i + 0.5), UP, buff=0.05) for i, nm_ in enumerate(names)])
        learned = [i for i, nm_ in enumerate(names) if nm_ not in ("random_cnn", "pixels")]
        best, bv, worst, wv = None, -1, None, 2
        for a in learned:
            for b in learned:
                if a < b:
                    if Cm[a, b] > bv:
                        best, bv = (a, b), Cm[a, b]
                    if Cm[a, b] < wv:
                        worst, wv = (a, b), Cm[a, b]
        sc = c["seeds_cka"]
        seeds_line = ", ".join(f"{SPOKEN.get(k, k)} {v:.2f}" for k, v in sc.items())
        side = VGroup(label(r"the same recipe, \ two seeds:", font_size=20, color=GREY_A),
                      *[label(rf"{NAME[k]}: \ ${v:.2f}$", font_size=20, color=COLOR[k]) for k, v in sc.items()])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.0, 0.2, 0])
        a, b = best
        wa, wb = worst
        box_b = Square(cell, color=WHITE, stroke_width=2).move_to(hm.get_corner(UL) + np.array([cell * (b + 0.5),
                                                                                                -cell * (a + 0.5), 0]))
        box_w = Square(cell, color=GREY_A, stroke_width=2).move_to(hm.get_corner(UL) + np.array([cell * (wb + 0.5),
                                                                                                 -cell * (wa + 0.5), 0]))
        tg = tag(r"computed: \ linear CKA on $2{,}000$ test digits, \ seed 0 of each method")
        with self.voiceover(
            "Here is the CKA between every pair of our representations, on the same two thousand test digits; "
            "brighter is more alike. <bookmark mark='a'/> The most alike learned pair is "
            f"{SPOKEN.get(names[a], names[a])} and {SPOKEN.get(names[b], names[b])}, at {bv:.2f}; <bookmark "
            f"mark='b'/> the least alike, {SPOKEN.get(names[wa], names[wa])} and {SPOKEN.get(names[wb], names[wb])}, "
            f"at {wv:.2f}. <bookmark mark='c'/> For scale: the same recipe run from two random starts gives "
            f"{seeds_line}."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(rl), FadeIn(cl), FadeIn(tg))
            vo.wait_until("a")
            self.play(Create(box_b))
            vo.wait_until("b")
            self.play(Create(box_w))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hypothesis(self):
        q = label(r"``We hypothesize that this convergence is driving toward \\ a shared statistical model of "
                  r"reality''", font_size=32).move_to(UP * 1.8)
        who = label(r"Huh, Cheung, Wang \& Isola, \ \textit{The Platonic Representation Hypothesis} \ (ICML 2024)",
                    font_size=22, color=GREY_B).next_to(q, DOWN, buff=0.3)
        ev = VGroup(
            label(r"78 vision models: \ the more tasks a model solves, \ the more it agrees with the others", font_size=22),
            label(r"language models and vision models: \ the better the language model, \ the more it agrees with "
                  r"vision", font_size=22),
            label(r"measured by mutual nearest neighbours: \ the share of each input's $k$ nearest neighbours \\ that "
                  r"two representations have in common \ (about $0.16$ at best, \ across senses)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.3)
        cave = label(r"Plato's cave: \ many shadows, \ one reality", font_size=22, color=HIST).to_corner(DR, buff=0.4)
        with self.voiceover(
            "In 2024 Minyoung Huh, Brian Cheung, Tongzhou Wang and Phillip Isola made a bold claim. Networks "
            "trained on different data, with different objectives, even on different senses, are coming to "
            "represent the world in the same way. In their words: <bookmark mark='a'/> we hypothesize that this "
            "convergence is driving toward a shared statistical model of reality. They called it the platonic "
            "representation hypothesis, after the shadows on the wall of Plato's cave. <bookmark mark='b'/> Their "
            "evidence: among seventy-eight vision models, the more capable agree more with each other; and the "
            "better a language model, the more its picture of a caption agrees with a vision model's picture of "
            "the image. <bookmark mark='c'/> Agreement is measured by shared nearest neighbours, and across senses "
            "it is still low in absolute terms."
        ) as vo:
            self.play(FadeIn(cave))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(who))
            vo.wait_until("b")
            self.play(FadeIn(ev[0]), FadeIn(ev[1]))
            vo.wait_until("c")
            self.play(FadeIn(ev[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def across(self):
        c = load("compare")
        rows = c["rows"]
        al = c["mean_align"]
        names = list(al)
        x = np.array([rows[n]["linear"][0] for n in names])
        y = np.array([al[n] for n in names])
        rho = float(c["spearman"])
        ax = axes([float(np.floor(x.min() * 20) / 20), 1.0], [0, float(np.ceil(y.max() * 10) / 10)], x_length=7.0,
                  y_length=4.2, xlabel=r"linear probe accuracy", ylabel=r"mean agreement with the others \ (mutual "
                  r"$10$-NN)", center=[-1.0, -0.3, 0])
        dots = VGroup()
        for n, a_, b_ in zip(names, x, y):
            d = Dot(ax.ax.c2p(a_, b_), radius=0.08, color=COLOR[n])
            dots.add(VGroup(d, label(NAME[n], font_size=16, color=COLOR[n]).next_to(d, UR, buff=0.04)))
        res = label(rf"Spearman's rank correlation: \ ${rho:.2f}$", font_size=26, color=C.BITS).to_corner(DR, buff=0.5)
        if rho > 0.5:
            v = (f"The more accurate methods do agree more with the rest: a rank correlation of {rho:.2f}. "
                 "As the paper put it: all strong models are alike, each weak model is weak in its own way.")
        elif rho > 0.2:
            v = f"The relation is weak: a rank correlation of {rho:.2f}."
        else:
            v = f"We see no such relation here: the rank correlation is {rho:.2f}."
        tg = tag(r"computed: \ $2{,}000$ test digits, \ $k = 10$, \ after centring", corner=UR)
        with self.voiceover(
            "We can run a small version of their first test on our own models. For each method, its average "
            "agreement with all the others, in shared nearest neighbours, against how good its representation is. "
            f"<bookmark mark='a'/> {v}"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def halves(self):
        h = load("halves")
        v = load("views")
        steps = np.asarray(h["rec_steps"])
        a0, a1 = np.asarray(h["align_s0"]), np.asarray(h["align_s1"])
        d = np.asarray(v["orig"])[3].astype(float) / 255.0
        top = digit(d[:14], 0.9, color=TOP, frame=True)
        bot = digit(d[14:], 0.9, color=BOT, frame=True)
        Group(top, bot).arrange(DOWN, buff=0.4).move_to([-5.6, 0.8, 0])
        lt = label(r"encoder A \\ sees the top", font_size=18, color=TOP).next_to(top, RIGHT, buff=0.2)
        lb = label(r"encoder B \\ sees the bottom", font_size=18, color=BOT).next_to(bot, RIGHT, buff=0.2)
        apart = label(r"trained apart, \\ each by SimCLR", font_size=18, color=GREY_A).next_to(Group(top, bot), DOWN,
                                                                                              buff=0.3)
        ymax = max(a0.max(), a1.max(), float(h["align_cross_seed_top"])) * 1.15
        ax = axes([0, steps[-1]], [0, ymax], x_length=6.2, y_length=3.8, xlabel=r"training step",
                  ylabel=r"A and B agree: \ mutual $10$-NN", xticks=[0, steps[-1]], center=[2.4, -0.2, 0])
        c0 = curve(ax.ax, steps, a0, C.BITS, 3.5)
        c1 = curve(ax.ax, steps, a1, C.BITS, 2).set_stroke(opacity=0.6)
        px = float(h["align_pixels"])
        cs = float(h["align_cross_seed_top"])
        lpx = DashedLine(ax.ax.c2p(0, px), ax.ax.c2p(steps[-1], px), color=PIX, stroke_width=1.5)
        lcs = DashedLine(ax.ax.c2p(0, cs), ax.ax.c2p(steps[-1], cs), color=GREY_A, stroke_width=1.5)
        tpx = label(r"the two halves' raw pixels", font_size=16, color=PIX).next_to(lpx, UP, buff=0.05).align_to(lpx,
                                                                                                         RIGHT)
        tcs = label(r"two top-half encoders, \ different seeds", font_size=16, color=GREY_A).next_to(lcs, UP,
                                                                                              buff=0.05).align_to(
            lcs, RIGHT)
        src = cite(r"Becker \& Hinton (1992): \ modules seeing different parts \ of the input, \ made to agree")
        rose = a0[-1] > a0[0] + 0.05 and a1[-1] > a1[0] + 0.05
        v_ = (f"As each learns, they agree more: from {a0[0]:.2f} at the start to {a0[-1]:.2f} and {a1[-1]:.2f} in the "
              f"two runs, well above the {px:.2f} of the raw pixels, though below the {cs:.2f} of two encoders that "
              "see the same half." if rose else
              f"Their agreement goes from {a0[0]:.2f} to {a0[-1]:.2f} and {a1[-1]:.2f}; the raw pixels' is {px:.2f}.")
        with self.voiceover(
            "A sharper test borrows Becker and Hinton's setting from 1992: two networks that see different parts of "
            "the world. Encoder A sees only the top half of each digit, encoder B only the bottom half. <bookmark "
            "mark='a'/> Each is trained alone, with SimCLR, never told about the other. Do they come to agree "
            "about which digits are alike? <bookmark mark='b'/> " + v_ + " <bookmark mark='c'/> Two senses, trained "
            "apart, drifting toward one picture of the same digits: the hypothesis in miniature."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(lt), FadeIn(lb), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(apart), FadeIn(ax), Create(lpx), FadeIn(tpx), Create(lcs), FadeIn(tcs))
            vo.wait_until("b")
            self.play(Create(c0), Create(c1), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(c0, color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        pts = VGroup(
            label(r"different senses carry different information: \ a caption cannot say everything a photo shows",
                  font_size=24),
            label(r"which similarity to measure is still argued over", font_size=24),
            label(r"convergence could come from shared data, \ shared architectures, \ shared habits of researchers",
                  font_size=24),
            label(r"ours is ten kinds of digit: \ a toy", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.4)
        head = label(r"The caveats, \ several of them the authors' own", font_size=32).to_edge(UP, buff=0.5)
        tk = take_away(r"different objectives, \ different data, \ similar geometry: \ evidence, \ not yet proof")
        with self.voiceover(
            "The authors list the caveats themselves. Different senses carry different information: a caption "
            "cannot say everything a photograph shows. <bookmark mark='a'/> How to measure agreement is still "
            "argued over. <bookmark mark='b'/> Convergence could come from shared training data, shared "
            "architectures, or the shared habits of the people building them. <bookmark mark='c'/> And ours is a toy "
            "with ten kinds of digit. Still, it is a striking idea: that learning without labels, from any angle, "
            "finds the same structure, because the structure is really there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
