from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import BUDGET_COLORS, curve, load


class Chinchilla(VoiceoverScene):
    def construct(self):
        self.card()
        self.isoflop()
        self.history()
        self.twoterm()

    def card(self):
        card = chapter_card(2, r"Size or data?", r"How should a fixed budget be spent?", part=10, lit=(2020, 2022))
        with self.voiceover("Chapter two. Size or data?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def isoflop(self):
        d = load("isoflop")
        budgets = [float(b) for b in d["budgets"]]
        allf = np.concatenate([np.asarray(d[f"finals{b:.0e}"]) for b in budgets])
        allf = allf[np.isfinite(allf)]
        lo, hi = float(np.floor(allf.min() * 10) / 10 - 0.05), float(np.ceil(allf.max() * 10) / 10 + 0.05)
        allp = np.concatenate([np.asarray(d[f"params{b:.0e}"]) for b in budgets])
        x0, x1 = math.floor(np.log10(allp.min()) * 2) / 2, math.ceil(np.log10(allp.max()) * 2) / 2
        ax = Axes(x_range=[x0, x1, 0.5], y_range=[lo, hi, 0.1], x_length=7.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xl = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.c2p(k, lo), DOWN, buff=0.1)
                      for k in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.1)
                      for v in np.arange(math.ceil(lo * 5) / 5, hi + 1e-9, 0.2)])
        xn = label(r"parameters", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yn = label(r"held-out bits per character", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        groups, mins = VGroup(), VGroup()
        for b, col in zip(budgets, BUDGET_COLORS):
            p, f = np.asarray(d[f"params{b:.0e}"], float), np.asarray(d[f"finals{b:.0e}"])
            ok = np.isfinite(f)
            groups.add(VGroup(curve(ax, np.log10(p[ok]), f[ok], col, 3.5),
                              *[Dot(ax.c2p(math.log10(pp), ff), radius=0.06, color=col) for pp, ff in zip(p[ok], f[ok])]))
            # the valley's bottom: a parabola in log N through the lowest points (the same fit as the chart that follows)
            lp, ff = np.log10(p[ok]), f[ok]
            i = int(np.argmin(ff))
            sl = slice(max(0, i - 2), min(len(ff), i + 3))
            a2, a1, a0 = np.polyfit(lp[sl], ff[sl], 2)
            xv = -a1 / (2 * a2)
            mins.add(Star(n=5, outer_radius=0.13, color=WHITE, fill_opacity=1).move_to(ax.c2p(xv, np.polyval([a2, a1, a0], xv))))
        key = VGroup(*[label(rf"budget ${b / 1e12:g}\times10^{{12}}$ operations", font_size=24, color=c)
                       for b, c in zip(budgets, BUDGET_COLORS)])
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, 1.6, 0])
        colors = {r"N": C.BITS, r"D": C.TRUE_P}
        rule = cmath(r"C", r"\approx", r"6", r"\,N", r"\,D", colors=colors, font_size=40).next_to(key, DOWN, buff=0.5)
        rl = label(r"$N$ parameters, \ $D$ training tokens", font_size=24, color=GREY_A).next_to(rule, DOWN, buff=0.15)
        best = label(r"too small: \ underfits; \\ too big: \ undertrained", font_size=26, color=GREY_A).next_to(rl, DOWN, buff=0.4)
        starl = label(r"stars: \ each valley's bottom, \\ a parabola fitted through it", font_size=20, color=GREY_B)
        # a budget is an area: N wide, D tall; the same area can be a wide, short block or a narrow, tall one
        area, corner = 2.0, np.array([3.2, -3.3, 0])
        wv = ValueTracker(1.4)

        def block():
            w = wv.get_value()
            r_ = Rectangle(width=w, height=area / w, stroke_color=WHITE, stroke_width=2, fill_color=C.BITS, fill_opacity=0.25)
            r_.move_to(corner, aligned_edge=DL)
            return VGroup(r_, MathTex(r"N", font_size=30, color=C.BITS).next_to(r_, DOWN, buff=0.08),
                          MathTex(r"D", font_size=30, color=C.TRUE_P).next_to(r_, LEFT, buff=0.08))

        still = block()
        bl_ = label(r"one budget: \\ the same area", font_size=22, color=GREY_A).move_to([5.6, -1.3, 0])
        with self.voiceover(
            "Suppose you can afford a fixed amount of computation. Training costs about six operations per "
            "parameter per training token, so a budget fixes the product of model size and data. You can have a "
            "big model that sees little data, or a small one that sees a lot. <bookmark mark='a'/> Here's the "
            f"experiment, on our character model. For each budget, try {len(d['widths'])} sizes, each trained on exactly the data "
            "the budget allows. <bookmark mark='b'/> Each budget gives a valley. Too small a model can't hold the "
            "patterns it sees: it underfits. Too big a model barely gets to see anything, so it can't finish "
            "learning: it's undertrained. <bookmark mark='c'/> And the bigger the budget, "
            "the further right the best size moves."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yt), FadeIn(xn), FadeIn(yn), Write(rule), FadeIn(rl))
            self.play(FadeIn(still), FadeIn(bl_))
            self.remove(still)
            live = always_redraw(block)  # added only after the fade-in: a self-rebuilding group can't be faded in
            self.add(live)
            self.play(wv.animate.set_value(3.0), run_time=2.0)  # a big model, little data
            self.play(wv.animate.set_value(0.8), run_time=2.5)  # a small model, lots of data
            self.play(wv.animate.set_value(1.4), run_time=1.5)
            vo.wait_until("a")
            live.clear_updaters()
            self.play(FadeOut(live), FadeOut(bl_), FadeIn(key))
            vo.wait_until("b")
            for g_ in groups:
                self.play(Create(g_), run_time=1.2)
            self.play(FadeIn(best))
            vo.wait_until("c")
            starl.next_to(best, DOWN, buff=0.35)
            self.play(LaggedStart(*[FadeIn(s_, scale=0.4) for s_ in mins], lag_ratio=0.3), FadeIn(starl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        # our compute-optimal sizes: each budget's curve fitted by a parabola in log N near its lowest point (as
        # Chinchilla's second method does); its vertex is the best size for that budget
        d = load("isoflop")
        budgets = [float(b) for b in d["budgets"]]
        lc, ln = [], []
        for b in budgets:
            N, L = np.log10(np.asarray(d[f"params{b:.0e}"], float)), np.asarray(d[f"finals{b:.0e}"])
            i = int(np.argmin(L))
            sl = slice(max(0, i - 2), min(len(L), i + 3))
            a2, a1, _ = np.polyfit(N[sl], L[sl], 2)
            lc.append(math.log10(b))
            ln.append(-a1 / (2 * a2))
        lc, ln = np.array(lc), np.array(ln)
        slope, icept = np.polyfit(lc, ln, 1)
        tpp = float(np.mean([b / 6 / 10 ** v / 10 ** v for b, v in zip(budgets, ln)]))  # characters per parameter
        xm, ym = float(lc.mean()), float(ln.mean())
        x0, x1 = lc[0] - 0.3, lc[-1] + 0.3
        y0, y1 = math.floor((ym - 0.6) * 4) / 4, math.ceil((ym + 0.6) * 4) / 4
        ax = CornerAxes(x_range=[x0, x1, 0.5], y_range=[y0, y1, 0.25], x_length=5.6, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.9, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.1)
                      for t, v in ((r"3\times10^{11}", math.log10(3e11)), (r"10^{12}", 12.0), (r"3\times10^{12}", math.log10(3e12)))
                      if x0 <= v <= x1])
        yv = [v for v in (1e4, 3e4, 1e5, 3e5, 1e6) if y0 <= math.log10(v) <= y1]
        yt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=22, color=GREY_B).next_to(ax.c2p(x0, math.log10(v)), LEFT,
                                                                                                buff=0.1) for v in yv])
        xn = label(r"compute budget \ (operations)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"the best number of parameters", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)

        def through(k, col, dashed=True):
            a_, b_ = ax.c2p(x0, ym + k * (x0 - xm)), ax.c2p(x1, ym + k * (x1 - xm))
            return (DashedLine(a_, b_, dash_length=0.1, color=col, stroke_width=2.5) if dashed else
                    Line(a_, b_, color=col, stroke_width=3.5))

        kap, chi = through(0.73, GREY_B), through(0.5, C.TRUE_P)
        ours = Line(ax.c2p(x0, icept + slope * x0), ax.c2p(x1, icept + slope * x1), color=C.BITS, stroke_width=3.5)
        stars = VGroup(*[Star(n=5, outer_radius=0.14, color=c, fill_opacity=1, stroke_width=0).move_to(ax.c2p(x, y))
                         for x, y, c in zip(lc, ln, BUDGET_COLORS)])
        def entry(line, text, col):
            return VGroup(line.copy().set_length(0.5).set_angle(0), label(text, font_size=22, color=col)).arrange(RIGHT, buff=0.15)

        kl = entry(kap, r"Kaplan (2020): \ $N \propto C^{0.73}$", GREY_B)
        cl = entry(chi, r"Chinchilla (2022): \ $N \propto C^{0.5}$", C.TRUE_P)
        ol = entry(ours, rf"ours: \ $N \propto C^{{{slope:.2f}}}$", C.BITS)
        legend = VGroup(kl, cl, ol).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.move_to(ax.c2p(x0, y1) + np.array([0.25, -0.2, 0]), aligned_edge=UL)
        rows = VGroup(
            label(r"Kaplan: \ grow the model \\ faster than the data", font_size=22, color=GREY_B),
            label(r"Chinchilla: \ grow both together, \\ about $20$ tokens per parameter", font_size=22, color=C.TRUE_P),
            label(rf"ours: \ about ${tpp:.0f}$ characters \\ per parameter", font_size=22, color=C.BITS),
            label(r"Chinchilla, $70$ billion parameters, \\ beat Gopher, $280$ billion, \\ on the same budget", font_size=22,
                  color=WHITE),
            label(r"today: \ far more tokens than that, \\ because a model is trained once \\ and then used billions of times",
                  font_size=22, color=GREY_A))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.5, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"best size per budget: \ a parabola through each curve's lowest points").to_corner(DL, buff=0.25)
        with self.voiceover(
            "This experiment, at enormous scale, changed how models are built. In 2020, Kaplan and colleagues "
            "concluded that model size should grow much faster than data. <bookmark mark='a'/> In 2022, DeepMind's "
            "Chinchilla paper redid it more carefully and found that size and data should grow together: about "
            "twenty training tokens for every parameter. <bookmark mark='o'/> Our small experiment lands close to "
            f"Chinchilla: the best size grows as the budget to the power {slope:.2f}, with about {tpp:.0f} "
            "characters of training per parameter. <bookmark mark='b'/> Their seventy-billion-parameter Chinchilla "
            "beat their own two-hundred-and-eighty-billion-parameter Gopher on the same budget. "
            "<bookmark mark='c'/> Today's models train on far more data than even that, because a model is trained "
            "once and then run billions of times, so a smaller, longer-trained model is cheaper to use."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(kap), FadeIn(kl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(chi), FadeIn(cl), FadeIn(rows[1]))
            vo.wait_until("o")
            self.play(LaggedStart(*[GrowFromCenter(st) for st in stars], lag_ratio=0.3), FadeIn(tag))
            self.play(Create(ours), FadeIn(ol), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twoterm(self):
        from scipy.optimize import least_squares

        d = load("isoflop")
        N, D, L = [], [], []
        for b in d["budgets"]:
            n, t, f = (np.asarray(d[f"{k}{float(b):.0e}"], float) for k in ("params", "tokens", "finals"))
            ok = np.isfinite(f)
            N, D, L = N + list(n[ok]), D + list(t[ok]), L + list(f[ok])
        N, D, L = np.array(N), np.array(D), np.array(L)

        def res(p):
            return p[0] + np.exp(p[1]) * N ** -p[2] + np.exp(p[3]) * D ** -p[4] - L

        fits = [least_squares(res, [1.5, 3, a0, 3, b0], loss="huber", f_scale=0.02,
                              bounds=([0, -10, 0.01, -10, 0.01], [3, 30, 2, 30, 2])) for a0 in (0.2, 0.4, 0.7) for b0 in (0.2, 0.4, 0.7)]
        fit = min(fits, key=lambda r: r.cost)
        E, A, al, B, be = fit.x[0], math.exp(fit.x[1]), fit.x[2], math.exp(fit.x[3]), fit.x[4]
        err = float(np.sqrt(np.mean(res(fit.x) ** 2)))
        ex = be / (al + be)
        # the best split of the largest budget, and what a smaller model must pay to match it
        C0 = float(max(d["budgets"]))
        Nopt = (al * A / (be * B)) ** (1 / (al + be)) * (C0 / 6) ** ex
        Dopt = C0 / 6 / Nopt
        Lstar = E + A * Nopt ** -al + B * Dopt ** -be
        kmin = (A / (Lstar - E)) ** (1 / al) / Nopt

        def cost(k):  # training compute, relative, for a model k times the best size to reach the same loss
            r = Lstar - E - A * (k * Nopt) ** -al
            return 6 * k * Nopt * (B / r) ** (1 / be) / C0

        colors = {r"E": GREY_A, r"\alpha": C.BITS, r"\beta": C.TRUE_P}
        f1 = cmath(r"L(N, D) = ", r"E", r"+ \frac{A}{N^{", r"\alpha", r"}} + \frac{B}{D^{", r"\beta", r"}}", colors=colors, font_size=36)
        f1.move_to([-3.4, 2.4, 0])
        vals = label(rf"fit to our ${len(L)}$ runs: \ $E = {E:.2f}$, \ $\alpha = {al:.2f}$, \ $\beta = {be:.2f}$ \\ "
                     rf"(off by ${err:.2f}$ bits on average)", font_size=20, color=GREY_A).next_to(f1, DOWN, buff=0.15)
        ab = VGroup(label(r"$\alpha$: \ how fast more parameters help", font_size=20, color=C.BITS),
                    label(r"$\beta$: \ how fast more data helps", font_size=20, color=C.TRUE_P)).arrange(RIGHT, buff=0.4)
        ab.next_to(vals, DOWN, buff=0.15)
        f2 = MathTex(r"\min_{N}\ L\big(N, \tfrac{C}{6N}\big) \;\Rightarrow\; N_{\text{opt}} \propto C^{\,\beta / (\alpha + \beta)}",
                     font_size=32).next_to(ab, DOWN, buff=0.35)
        f3 = MathTex(rf"\beta / (\alpha + \beta) = {ex:.2f}", font_size=32, color=C.BITS).next_to(f2, DOWN, buff=0.25)
        f3l = label(rf"the parabolas gave about the same; \\ the best split here: \ ${Dopt / Nopt:.0f}$ characters per parameter",
                    font_size=20, color=GREY_A).next_to(f3, DOWN, buff=0.12)
        # right: the price of a smaller model
        ks = np.linspace(max(kmin * 1.04, 0.2), 1.0, 120)
        cs = np.array([cost(k) for k in ks])
        top = 16.0
        ax = CornerAxes(x_range=[0.2, 1.0, 0.2], y_range=[0, math.log10(top), 0.5], x_length=5.0, y_length=3.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, -0.2, 0])
        ok = cs <= top
        line = VMobject(color=C.SURPRISE, stroke_width=3.5).set_points_smoothly([ax.c2p(k, math.log10(c)) for k, c in zip(ks[ok], cs[ok])])
        yt = VGroup(*[MathTex(rf"{v}\times", font_size=20, color=GREY_B).next_to(ax.c2p(0.2, math.log10(v)), LEFT, buff=0.08)
                      for v in (1, 2, 4, 8, 16)])
        xt = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v, t_ in ((0.25, r"\tfrac14"), (0.5, r"\tfrac12"), (0.75, r"\tfrac34"), (1.0, r"1"))])
        xn = label(r"model size, \ relative to the best for the budget", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"training compute for the same loss", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.15)
        marks = VGroup()
        for k in (0.75, 0.5):
            c = cost(k)
            marks.add(VGroup(Dot(ax.c2p(k, math.log10(c)), radius=0.07, color=C.BITS),
                             MathTex(rf"+{100 * (c - 1):.0f}\%", font_size=24, color=C.BITS).next_to(ax.c2p(k, math.log10(c)), UR, buff=0.08)))
        wall = DashedLine(ax.c2p(kmin, 0), ax.c2p(kmin, math.log10(top)), dash_length=0.06, stroke_width=2, color=GREY_B)
        wl = label(r"below this size: \\ never, \ at any budget", font_size=18, color=GREY_B).next_to(wall, RIGHT, buff=0.08).shift(UP * 1.2)
        foot = label(r"Llama 3, $8$ billion parameters: \ $15$ trillion tokens, \ about $1{,}900$ per parameter \ (as published)",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        cite_ = cite(r"J.~Hoffmann et al.\ (2022), \ approach 3; \ N.~Sardana \& J.~Frankle, \textit{Beyond Chinchilla-Optimal} (2023)",
                     corner=UR)
        c75, c50 = cost(0.75), cost(0.5)
        with self.voiceover(
            "Chinchilla's third method fits one formula to every run at once. <bookmark mark='a'/> The loss is a floor, "
            "plus a term that shrinks with the parameters, at a rate set by alpha, plus one that shrinks with the data, "
            "at a rate set by beta: how fast more parameters help, and how fast more data helps. Fit to our eighteen "
            f"runs, it's off by only {err:.2f} bits on average. <bookmark mark='b'/> Minimize it for a fixed budget, "
            f"and the best size grows as the budget to the power beta over alpha plus beta: {ex:.2f} here, close to "
            "what the parabolas said: the budget goes to whichever pays off faster. <bookmark mark='c'/> The same formula prices over-training. To match the best "
            f"model's loss with a model three quarters its size costs {100 * (c75 - 1):.0f} percent more training; "
            f"with half the size, {100 * (c50 - 1):.0f} percent more; and below about {kmin:.2f} of the size, no amount "
            "of data will do. <bookmark mark='d'/> Since every query afterwards is cheaper with the smaller model, "
            "that extra training is often worth it: Llama 3's eight-billion-parameter model saw about nineteen hundred "
            "tokens per parameter, a hundred times Chinchilla's ratio."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(vals), FadeIn(ab))
            vo.wait_until("b")
            self.play(Write(f2))
            self.play(Write(f3), FadeIn(f3l))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xn), FadeIn(yn))
            self.play(Create(line), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.4), Create(wall), FadeIn(wl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
