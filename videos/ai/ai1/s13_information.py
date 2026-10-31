from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import PART, load


class Information(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.processing()
        self.memory()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Mutual information: what the past tells the future",
                            r"How much does knowing one thing tell you about another?", lit=(1948,), part=PART)
        with self.voiceover("Chapter twelve. What the past tells you about the future."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        d = load("dpi")
        Hx, Hc, I = float(d["H_next"]), float(d["H_cond"]), float(d["I_xy"])
        I2, Isk = float(d["I_two"]), float(d["I_skip"])
        head = label(r"Mutual information", font_size=38).to_edge(UP, buff=0.35)
        df_body = VGroup(MathTex(r"= H(X) - H(X \mid Y) = H(Y) - H(Y \mid X)", font_size=30, color=GREY_A),
                         MathTex(r"= D_{\mathrm{KL}}\big(p(x, y) \,\|\, p(x)\,p(y)\big) \ge 0", font_size=30,
                                 color=GREY_A),
                         label(r"the bits that knowing $Y$ saves when you guess $X$, \\ and the other way round",
                               font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        df = definition_card(r"$I(X; Y)$", df_body, width=6.6, color=C.BITS)
        df.to_corner(UL, buff=0.4).shift(DOWN * 0.7)
        r = 1.45
        a = Circle(radius=r, stroke_color=C.ENTROPY, stroke_width=3, fill_color=C.ENTROPY, fill_opacity=0.15)
        b = Circle(radius=r, stroke_color=C.CONTEXT, stroke_width=3, fill_color=C.CONTEXT, fill_opacity=0.15)
        a.move_to([3.2, 0.3, 0])
        b.move_to([4.9, 0.3, 0])
        la = MathTex(r"H(X)", font_size=30, color=C.ENTROPY).next_to(a, UP, buff=0.1).shift(LEFT * 0.6)
        lb = MathTex(r"H(Y)", font_size=30, color=C.CONTEXT).next_to(b, UP, buff=0.1).shift(RIGHT * 0.6)
        mid = MathTex(r"I", font_size=36, color=C.BITS).move_to([4.05, 0.3, 0])
        cap = VGroup(
            label(r"$X$: \ the next letter; \ $Y$: \ the letter before it", font_size=24, color=GREY_A),
            label(rf"$H(X) = {Hx:.2f}$, \ $H(X \mid Y) = {Hc:.2f}$", font_size=26),
            label(rf"$I(X; Y) = {I:.2f}$ bits", font_size=30, color=C.BITS),
        ).arrange(DOWN, buff=0.14).move_to([4.05, -2.3, 0])
        two = label(rf"two letters back: \ ${I2:.2f}$ bits; \ the second one alone: \ ${Isk:.2f}$", font_size=24,
                    color=GREY_A).to_corner(DL, buff=0.45)
        tag = computed_tag()
        with self.voiceover(
            "In chapter seven, knowing X lowered the entropy of Y, on average. That drop is the mutual "
            "information. <bookmark mark='a'/> It's the bits that knowing one thing saves you when you guess the "
            "other, and it's symmetric. It's also a divergence, of the joint distribution from independence, so "
            "it's never negative. <bookmark mark='b'/> In our books, the next letter carries "
            f"{Hx:.2f} bits; knowing the letter before it, {Hc:.2f}. <bookmark mark='c'/> So neighbouring letters "
            f"share {I:.2f} bits. <bookmark mark='d'/> Two letters back share {I2:.2f}, though the second one on its "
            f"own shares only {Isk:.2f}: together, letters say more than apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(df, shift=RIGHT * 0.2), FadeIn(mid))
            vo.wait_until("b")
            self.play(FadeIn(cap[0]), FadeIn(cap[1]), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]), Indicate(mid, color=C.BITS, scale_factor=1.5))
            vo.wait_until("d")
            self.play(FadeIn(two))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def processing(self):
        d = load("dpi")
        I, Ig = float(d["I_xy"]), float(d["I_group"])
        eps, In, Ib = np.asarray(d["eps"]), np.asarray(d["I_noise"]), np.asarray(d["I_both"])
        head = label(r"The data-processing inequality", font_size=36).to_edge(UP, buff=0.35)
        chain = mtex(r"X \;\to\; Y \;\to\; Z = f(Y,\ \text{noise})", font_size=36).next_to(head, DOWN, buff=0.3)
        chain_n = label(r"$Z$ is computed from $Y$ alone: \ given $Y$, it knows nothing more about $X$", font_size=24,
                        color=GREY_A).next_to(chain, DOWN, buff=0.15)
        rows = [
            cmath(r"I(X; Y, Z)", r"=", r"I(X; Y) + I(X; Z \mid Y)", font_size=36),
            cmath(r"I(X; Y, Z)", r"=", r"I(X; Z) + I(X; Y \mid Z)", font_size=36),
            cmath(r"I(X; Z)", r"\le", r"I(X; Y)", font_size=40, colors={r"I(X; Z)": C.BITS}),
        ]
        whys = [why(r"the chain rule; \ the last term is $0$"), why(r"the chain rule, the other way"),
                why(r"$I(X; Y \mid Z) \ge 0$")]
        step = ladder(self, rows, whys, keep=3, top=1.0, x=-2.4, buff=0.4, edge=6.9)
        # the chain, pictured: what Z can know about X has to pass through Y
        nodes = VGroup(*[VGroup(Circle(radius=0.38, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.15),
                                MathTex(n_, font_size=34, color=col)) for n_, col in
                         (("X", C.ENTROPY), ("Y", C.CONTEXT), ("Z", C.BITS))]).arrange(RIGHT, buff=2.6)
        for nd in nodes:
            nd[1].move_to(nd[0])
        nodes.move_to(DOWN * 2.75)
        links = VGroup(*[Arrow(nodes[k][0].get_right(), nodes[k + 1][0].get_left(), buff=0.1, color=GREY_B,
                               stroke_width=3, max_tip_length_to_length_ratio=0.12) for k in range(2)])
        names = VGroup(*[label(t, font_size=22, color=GREY_A).next_to(nd, DOWN, buff=0.15) for t, nd in zip(
            (r"the next letter", r"the letter before it", r"its kind, or a noisy copy"), nodes)])
        f_l = label(r"$f(\cdot,\ \text{noise})$", font_size=22, color=C.BITS).next_to(links[1], UP, buff=0.08)
        bypass = CurvedArrow(nodes[0][0].get_top() + UP * 0.05, nodes[2][0].get_top() + UP * 0.05, angle=-PI / 5,
                             color=C.BITS, stroke_width=2.5)
        by_l = label(r"no more than $Y$ knew", font_size=22, color=C.BITS).next_to(bypass, UP, buff=0.06)
        pipe = VGroup(nodes, links, names, f_l)
        with self.voiceover(
            "Now process what you know. Suppose Z is computed from Y, by any function at all, even a noisy one. "
            "<bookmark mark='a'/> The chain rule splits what Y and Z together say about X in two ways: first Y, "
            "then whatever Z adds, which is nothing. <bookmark mark='b'/> Or first Z, then whatever Y adds. "
            "<bookmark mark='c'/> Compare the two, and Z can never tell you more about X than Y did. No amount of "
            "processing creates information."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chain), FadeIn(chain_n))
            self.play(LaggedStart(*[FadeIn(m) for m in (nodes[0], links[0], nodes[1], links[1], nodes[2])],
                                  lag_ratio=0.3), FadeIn(names), FadeIn(f_l), run_time=1.8)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Create(bypass), FadeIn(by_l))
            self.play(Create(SurroundingRectangle(rows[2], color=C.BITS, buff=0.12, corner_radius=0.08)))
        self.wait(0.3)
        self.clear_scene()
        # the check: process the previous letter
        a = axes([0, 1], [0, 0.8], x_length=7.0, y_length=4.0, xlabel=r"share of letters replaced by a random one",
                 ylabel=r"bits the processed letter tells you about the next", xticks=[0, 0.5, 1], yticks=[0, 0.25, 0.5, 0.75],
                 center=[-2.0, -0.6, 0], font_size=20)
        ax = a.ax
        c1 = curve(ax, eps, In, C.CONTEXT, 4)
        c2 = curve(ax, eps, Ib, C.BITS, 4)
        top = DashedLine(ax.c2p(0, I), ax.c2p(1, I), color=GREY_B, stroke_width=2)
        tl = label(rf"the letter itself: \ ${I:.2f}$", font_size=22, color=GREY_B).next_to(ax.c2p(1, I), UP, buff=0.08)
        tl.align_to(top, RIGHT)
        key = VGroup(label(r"the previous letter, \\ after noise", font_size=24, color=C.CONTEXT),
                     label(r"only its kind \\ (space, vowel, consonant), \\ after noise", font_size=24, color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.6, 0])
        g0 = Dot(ax.c2p(0, Ig), radius=0.08, color=C.BITS)
        gl = label(rf"${Ig:.2f}$", font_size=24, color=C.BITS).next_to(g0, RIGHT, buff=0.12)
        head2 = label(r"Processing the previous letter", font_size=34).to_edge(UP, buff=0.35)
        tag = computed_tag()
        take = label(r"a model's features, computed \\ from the context, can't know more \\ about the next token than "
                     r"the context did", font_size=24, color=GREY_A).move_to([4.7, -1.9, 0])
        with self.voiceover(
            "Let's watch it happen in our books. <bookmark mark='a'/> Keep only the kind of the previous letter: "
            f"space, vowel or consonant. Of the {I:.2f} bits, {Ig:.2f} survive. <bookmark mark='b'/> Or garble it: "
            "replace a share of the letters with random ones. The more noise, the less it tells, down to nothing. "
            "<bookmark mark='c'/> Do both, and you lose more: each curve stays under the one before. "
            "<bookmark mark='d'/> A law for learning machines too: whatever a network computes from its context "
            "can't know more about the next token than the context itself."
        ) as vo:
            self.play(FadeIn(head2), FadeIn(a), FadeIn(tag), Create(top), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(g0, scale=0.5), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(key[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        d = load("mi")
        ds, mi = np.asarray(d["d"], float), np.asarray(d["mi"], float)
        shuffled = np.asarray(d["shuffled_mi"], float)
        corpus = load("corpus")
        far, last, control = int(ds[-1]), float(mi[-1]), float(shuffled[-1])
        fit_ds = np.asarray(d["fit_d"], float)
        has_fit = d["slope"] is not None and len(fit_ds) >= 2
        head = label(r"How far back does the past tell you about the future?", font_size=32).to_edge(UP, buff=0.3)
        defn = mtex(r"I(X_t; X_{t+d}) = D_{\mathrm{KL}}\big(p(x, y) \,\|\, p(x)\,p(y)\big)", font_size=30,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        positives = np.concatenate((mi[mi > 0], shuffled[shuffled > 0]))
        lower = min(-6, math.floor(math.log10(float(positives.min()))) - 1) if len(positives) else -6
        ax = CornerAxes(x_range=[0, math.log10(far), 1], y_range=[lower, 0, 1], x_length=8.0, y_length=4.2,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                 "stroke_width": 2}).move_to([-1.7, -0.65, 0])
        xl = VGroup(*[MathTex(rf"10^{{{v}}}" if v else "1", font_size=23, color=GREY_B)
                      .next_to(ax.c2p(v, lower), DOWN, buff=0.15) for v in range(int(math.log10(far)) + 1)])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B)
                      .next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in range(lower, 1, 2)])
        axl = VGroup(label(r"distance $d$, in letters", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.5),
                     label(r"estimated mutual information, bits", font_size=22, color=GREY_A)
                     .next_to(ax, UP, buff=0.15).align_to(ax, LEFT))

        def log_points(values):
            # Keep gaps: a nonpositive corrected estimate has no log coordinate.
            # Its signed value is retained in the cache and disclosed on screen.
            ys = np.full(len(values), np.nan)
            positive = values > 0
            ys[positive] = np.log10(values[positive])
            return positive, ys

        ok, ys = log_points(mi)
        curve_ = curve(ax, np.log10(ds), ys, C.CONTEXT, 3.5)
        dots = VGroup(*[Dot(ax.c2p(math.log10(x), y), radius=0.045, color=C.CONTEXT)
                        for x, y in zip(ds[ok], ys[ok])])
        shuffle_ok, shuffle_y = log_points(shuffled)
        shuffle_dots = VGroup(*[Dot(ax.c2p(math.log10(x), y), radius=0.035, color=GREY_A)
                                for x, y in zip(ds[shuffle_ok], shuffle_y[shuffle_ok])])
        key = legend([(C.CONTEXT, r"book pairs"), (GREY_A, r"one shuffled control")], font_size=21)
        key.move_to([-1.1, 2.1, 0])
        omitted = int((~ok).sum() + (~shuffle_ok).sum())
        disclosure = wrapped_label(rf"nonpositive estimates omitted from log axes: ${omitted}$", 8.4,
                                   font_size=18, color=GREY_B).next_to(axl[0], DOWN, buff=0.15)

        def scientific(value):
            if value == 0:
                return "0"
            exponent = math.floor(math.log10(abs(value)))
            return rf"{value / 10 ** exponent:.2f}\times 10^{{{exponent}}}"

        side = VGroup(
            label(r"at the furthest measured lag", font_size=22, color=GREY_A),
            MathTex(rf"d = {far}", font_size=28),
            label(r"book pairs", font_size=21, color=C.CONTEXT),
            MathTex(rf"\widehat I = {scientific(last)}", font_size=26, color=C.CONTEXT),
            label(r"one shuffled control", font_size=21, color=GREY_A),
            MathTex(rf"\widehat I = {scientific(control)}", font_size=26, color=GREY_A),
            wrapped_label(r"one permutation, not an uncertainty interval", 3.8, font_size=19, color=GREY_B),
            wrapped_label(r"approximate bias correction; estimates may be negative", 3.8,
                          font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.8, 0.6, 0])
        fit = VGroup()
        if has_fit:
            slope = float(d["slope"])
            fit_x = np.log10([fit_ds[0], fit_ds[-1]])
            fit = DashedLine(ax.c2p(fit_x[0], d["intercept"] + slope * fit_x[0]),
                             ax.c2p(fit_x[1], d["intercept"] + slope * fit_x[1]),
                             color=C.BITS, stroke_width=2.5)
            fit_l = VGroup(label(r"log-log fit, positive estimates", font_size=20, color=C.BITS),
                           MathTex(rf"\widehat I \propto d^{{{slope:.2f}}}", font_size=25, color=C.BITS),
                           wrapped_label(r"descriptive fit, not proof of a power law", 3.8,
                                         font_size=19, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        else:
            fit_l = wrapped_label(r"not enough positive estimates for a log-log fit", 3.8,
                                  font_size=20, color=C.BITS)
        fit_l.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        tag = computed_tag(rf"computed: ${corpus['train27_chars'] / 1e6:.1f}$ million letters of the ${corpus['n_books']}$ "
                           r"books")
        fit_said = ("The gold line is a descriptive least-squares fit to the positive estimates from twenty to "
                    "one thousand letters. It is not a test that proves a power law." if has_fit else
                    "There are not enough positive estimates here for a log-log fit.")
        with self.voiceover(
            "How far back does that reach? Measure pairs of letters at distance d across our books. These are "
            "finite-sample estimates, with an approximate bias correction. <bookmark mark='a'/> The neighbouring "
            f"letter estimate is {mi[0]:.2f} bits. <bookmark mark='b'/> At our largest measured distance, "
            f"{far} letters, the corrected estimate is {last:.2g} bits; one shuffled version of the same letters "
            f"gives {control:.2g}. The shuffled control is a reference realization, not an uncertainty interval. "
            "Both axes are logarithmic. Nonpositive estimates cannot appear on them; their signed values are "
            "retained, including the control shown at the right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defn), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve_), FadeIn(dots), FadeIn(shuffle_dots), FadeIn(key), run_time=2.5)
            self.play(FadeIn(disclosure))
            vo.wait_until("b")
            self.play(FadeIn(side))
        with self.voiceover(
            "A fit is a summary, not a law. " + fit_said + " <bookmark mark='a'/> Bias correction is approximate, especially for overlapping pairs "
            "from text. Corrected estimates can fluctuate below zero, even though true mutual information is "
            "nonnegative. <bookmark mark='b'/> Our measurement stops at this distance. It does not establish what "
            "happens beyond it, or prove that memory helps at every distance. Long context remains a question "
            "for models to test: attention, in Part 13."
        ) as vo:
            self.play(Create(fit), FadeIn(fit_l))
            vo.wait_until("a")
            self.play(Indicate(side[-1], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Indicate(side[1], color=C.CONTEXT, scale_factor=1.06))
        self.wait(0.3)
        self.clear_scene()
