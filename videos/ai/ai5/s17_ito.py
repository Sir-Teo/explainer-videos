from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, HIST, MODEL, PART, WALK, curve, load

LPT = C.BITS  # Itô: the left point
MID = C.INTERVAL  # Stratonovich: the midpoint
CORR = C.SURPRISE  # the extra term


class Ito(VoiceoverScene):
    def construct(self):
        self.card()
        self.integral()
        self.lemma()
        self.history()

    def card(self):
        card = chapter_card(15, r"It\^o's lemma", r"What is the chain rule for a path with no slope?", lit=(1944,),
                            part=PART)
        with self.voiceover("Chapter fifteen. Ito's lemma."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def integral(self):
        d = load("ito")
        ns = np.asarray(d["ns"], float)
        le, se = np.asarray(d["left_err"]), np.asarray(d["strat_err"])
        lm, sm, w2 = float(d["left_mean"]), float(d["strat_mean"]), float(d["w2_mean"])
        M = int(d["M"])
        q = cmath(r"\int_0^1 W\, dW", "=", r"\;?", font_size=42).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"\textstyle\sum_k W_k\, \Delta W_k", "=", r"\tfrac12 \textstyle\sum_k \big(W_{k+1}^2 - W_k^2\big) - "
                  r"\tfrac12 \textstyle\sum_k (\Delta W_k)^2", font_size=32),
            cmath(r"\textstyle\sum_k W_k\, \Delta W_k", "=", r"\tfrac12 W_1^2 - \tfrac12 \textstyle\sum_k (\Delta W_k)^2",
                  font_size=32),
            cmath(r"\textstyle\sum_k W_k\, \Delta W_k", r"\to", r"\tfrac12 W_1^2 -", r"\tfrac12", font_size=34,
                  colors={r"\tfrac12": CORR}),
        ]
        whys = [why(r"$a(b - a) = \tfrac12(b^2 - a^2) - \tfrac12(b - a)^2$", font_size=22),
                why(r"the first sum telescopes", font_size=22),
                why(r"quadratic variation \ (Chapter 14)", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-2.4, buff=0.4, edge=6.8)
        ax = CornerAxes(x_range=[1, 4, 1], y_range=[-16, 0, 4], x_length=5.6, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.2, -2.0, 0])
        xt = VGroup(*[MathTex(f"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, -16), DOWN, buff=0.08) for v in (1, 2, 3, 4)])
        lx = np.log10(ns)
        lc = VGroup(curve(ax, lx, np.log10(le), color=LPT, stroke_width=3),
                    *[Dot(ax.c2p(a, math.log10(b)), radius=0.05, color=LPT) for a, b in zip(lx, le)])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(1, v), LEFT, buff=0.08)
                      for t, v in (("1", 0), ("10^{-8}", -8), ("10^{-16}", -16))])
        exact_mid = bool(np.all(se < 1e-10))
        mc = (DashedLine(ax.c2p(1, -16), ax.c2p(4, -16), color=MID, stroke_width=3) if exact_mid else
              curve(ax, lx, np.log10(np.maximum(se, 1e-16)), color=MID, stroke_width=3))
        al = VGroup(label(r"left points: \ error against $\tfrac12(W_1^2 - 1)$", font_size=20, color=LPT),
                    label(r"midpoints: \ against $\tfrac12 W_1^2$ \ (to rounding)", font_size=20, color=MID))
        al.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax, UP, buff=0.08)
        xl = label(r"steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.06)
        means = VGroup(label(rf"over ${M:,}$ paths:".replace(",", "{,}"), font_size=22, color=GREY_A),
                       label(rf"left-point sums average ${lm:+.3f}$", font_size=22, color=LPT),
                       label(rf"midpoint sums average ${sm:.3f}$", font_size=22, color=MID),
                       label(rf"ordinary calculus, $\tfrac12 W_1^2$: \ ${w2 / 2:.3f}$", font_size=22, color=GREY_A))
        means.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, -2.4, 0])
        path, run = np.asarray(d["path"]), np.asarray(d["ito_run"])
        tt = np.linspace(0, 1, len(path))
        pa = Axes(x_range=[0, 1, 0.25], y_range=[-2, 2, 1], x_length=7.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.6, -2.2, 0])
        wp = curve(pa, tt, np.clip(path, -2, 2), color=WALK, stroke_width=2.5)
        marks = VGroup(*[Line(pa.c2p(tt[i], 0), pa.c2p(tt[i], path[i]), color=LPT, stroke_width=1.5).set_stroke(opacity=0.6)
                         for i in range(0, len(path) - 1, 5)])
        rl = curve(pa, tt, np.clip(run, -2, 2), color=LPT, stroke_width=3)
        ex = curve(pa, tt, np.clip(0.5 * path ** 2 - 0.5 * tt, -2, 2), color=CORR, stroke_width=2).set_stroke(opacity=0.8)
        pl = VGroup(label(r"one path $W_t$; \ the bars: \ $W$ at the left of each step", font_size=20, color=WALK),
                    label(r"running left-point sum", font_size=20, color=LPT),
                    label(r"$\tfrac12 W_t^2 - \tfrac12 t$", font_size=20, color=CORR)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        pl.next_to(pa, RIGHT, buff=0.3)
        ppic = VGroup(pa, wp, marks, pl[0])
        verdict = ("and the midpoints give one half W squared exactly" if exact_mid else
                   "and the midpoints approach one half W squared")
        with self.voiceover(
            "Ordinary calculus says the integral of W d W is one half W squared. For Brownian motion, it depends on "
            "where in each little step you evaluate W. <bookmark mark='a'/> Take the left point, the value before "
            "the step. A little algebra splits the sum in two. <bookmark mark='b'/> The first part telescopes to "
            "one half W squared. <bookmark mark='c'/> The second is half the sum of squared steps, which chapter "
            "fourteen showed is t, not zero. So the left-point integral is one half W squared minus one half. "
            f"<bookmark mark='d'/> Over {M:,} paths the left-point sums close in on it as the steps shrink, "
            f"{verdict}: their averages are {lm:.2f} and {sm:.2f}. The choice of point matters, which never "
            "happens for smooth curves."
        ) as vo:
            self.play(Write(q), Create(pa), Create(wp), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(marks), FadeIn(pl[0]))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Create(rl), Create(ex), FadeIn(pl[1:]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeOut(VGroup(pa, wp, marks, pl, rl, ex)))
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(al), Create(lc), Create(mc))
            self.play(LaggedStart(*[FadeIn(m) for m in means], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lemma(self):
        d = load("ito")
        ns = np.asarray(d["ns"], float)
        lr, nr = np.asarray(d["lemma_rms"]), np.asarray(d["naive_rms"])
        em, eh, sl = float(d["e_mean"]), float(d["e_half"]), float(d["lemma_slope"])
        colors = {r"\tfrac12 f''(W)\,dt": CORR, r"\tfrac12 f''(W)\,(dW)^2": CORR}
        rows = [
            cmath(r"df", "=", r"f'(W)\,dW", "+", r"\tfrac12 f''(W)\,(dW)^2", "+", r"\dots", colors=colors, font_size=36),
            cmath(r"df", "=", r"f'(W)\,dW", "+", r"\tfrac12 f''(W)\,dt", colors=colors, font_size=36),
            cmath(r"df(X)", "=", r"\big(f'\mu + \tfrac12 f''\sigma^2\big)\,dt + f'\sigma\, dW", font_size=34),
        ]
        whys = [why(r"Taylor, \ to second order"), why(r"$(dW)^2 = dt$; \ higher terms vanish"),
                why(r"for $dX = \mu\,dt + \sigma\,dW$")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-1.4, buff=0.45, edge=6.8)
        ax = CornerAxes(x_range=[1, 4, 1], y_range=[-2, 0.5, 1], x_length=5.6, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.0, -1.9, 0])
        xt = VGroup(*[MathTex(f"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, -2), DOWN, buff=0.08) for v in (1, 2, 3, 4)])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(1, v), LEFT, buff=0.08)
                      for t, v in (("1", 0), ("0.1", -1), ("0.01", -2))])
        lx = np.log10(ns)
        c1 = VGroup(curve(ax, lx, np.log10(lr), color=CORR, stroke_width=3),
                    *[Dot(ax.c2p(a, math.log10(b)), radius=0.05, color=CORR) for a, b in zip(lx, lr)])
        c2 = VGroup(curve(ax, lx, np.log10(nr), color=GREY_B, stroke_width=3),
                    *[Dot(ax.c2p(a, math.log10(b)), radius=0.05, color=GREY_B) for a, b in zip(lx, nr)])
        tl = label(r"$f(W) = e^W$: \ the gap between $e^{W_1} - 1$ and the sums, \ path by path", font_size=20,
                   color=GREY_A).next_to(ax, UP, buff=0.1)
        lg = VGroup(label(rf"with the $\tfrac12 f''\,dt$ term: \ slope ${sl:.2f}$", font_size=20, color=CORR),
                    label(r"without it \ (ordinary calculus)", font_size=20, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        lg.next_to(ax, RIGHT, buff=0.3).align_to(ax, UP)
        mean = label(rf"and on average: \ $\mathbb{{E}}[e^{{W_1}}] = {em:.4f}$, \ $e^{{1/2}} = {eh:.4f}$", font_size=22,
                     color=CORR).next_to(lg, DOWN, buff=0.35).align_to(lg, LEFT)
        mn = label(r"the drift $\tfrac12 e^W$ at work", font_size=20, color=GREY_A).next_to(mean, DOWN, buff=0.1).align_to(lg, LEFT)
        with self.voiceover(
            "The same thing changes the chain rule. Expand a function of W to second order. <bookmark mark='a'/> In "
            "ordinary calculus the squared term is negligible. Here dW squared is dt, the same size as everything "
            "else we keep: <bookmark mark='b'/> the chain rule gains a term, one half f double prime dt. That is "
            "Ito's lemma, <bookmark mark='c'/> and for any process with drift mu and noise sigma it reads like "
            "this. <bookmark mark='d'/> Check it on e to the W, path by path. With the extra term the gap closes "
            f"as the steps shrink, at a slope of {sl:.2f}; without it, it stalls at about {nr[-1]:.2f}. And on "
            f"average, e to the W at time one is {em:.3f}, not one: the square root of e, {eh:.3f}, as the extra "
            "drift predicts."
        ) as vo:
            step(0)
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(tl))
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(Create(c2), Create(c1), FadeIn(lg))
            self.play(FadeIn(mean), FadeIn(mn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1940, r"Wolfgang Doeblin", r"a soldier in the French army sends the Academy of Sciences a "
                         r"sealed envelope with a version of the formula; \ opened in 2000", width=4.3, font_size=24),
            history_card(r"1944, 1951", r"Kiyosi It\^o", r"the stochastic integral, \ written in wartime Japan; \ "
                         r"then its chain rule", width=4.3, font_size=24),
            history_card(1973, r"Black, Scholes, Merton", r"It\^o's lemma prices options; \ today it is how "
                         r"diffusion models are run backwards \ (Part 21)", width=4.3, font_size=24),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.3)
        head = label(r"A calculus for random motion", font_size=38).to_edge(UP, buff=0.4)
        strat = label(r"midpoints instead: \ Stratonovich's integral (1966), \ ordinary chain rule, \ but it peeks at "
                      r"the future", font_size=22, color=MID).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This calculus has a dramatic history. <bookmark mark='a'/> In 1940, Wolfgang Doeblin, a young "
            "mathematician serving in the French army, mailed the Academy of Sciences a sealed envelope; he died "
            "that June, and when it was opened in 2000 it held a version of the same formula. <bookmark mark='b'/> Kiyosi Ito "
            "published the stochastic integral in 1944 and the formula in 1951. <bookmark mark='c'/> Black, Scholes "
            "and Merton priced options with it in 1973, and it is the working tool for running diffusion models in "
            "part twenty-one. <bookmark mark='d'/> Midpoints give Stratonovich's integral, with the ordinary chain "
            "rule, but they peek at the future; the left point is what a simulation can actually compute."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(strat))
        self.wait(0.3)
        self.clear_scene()
