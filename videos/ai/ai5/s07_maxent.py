from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, PART, curve, hist_shape, load, normal_pdf

ENT = C.SURPRISE  # entropy
LAM = C.BITS  # the multiplier


def entropy(p):
    p = np.asarray(p)
    return float(-(p * np.log(p)).sum())


class MaxEnt(VoiceoverScene):
    def construct(self):
        self.card()
        self.die()
        self.derive()
        self.fit()
        self.family()

    def card(self):
        card = chapter_card(6, r"Maximum entropy", r"What should you believe when all you know is an average?", part=PART)
        with self.voiceover("Chapter six. Maximum entropy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bars(self, p, x=0.0, base=-2.4, h=6.0, col=DATA):
        lb = LiveBars(p, max_value=0.5, height=h * 0.5, bar_width=0.6, gap=0.25, colors=col,
                      labels=[str(k) for k in range(1, 7)], label_font=26)
        return lb.place(base, x=x)

    # ------------------------------------------------------------------
    def die(self):
        d = load("maxent")
        others = np.asarray(d["others"])
        p_star = np.asarray(d["p"])
        bars = self.bars(np.ones(6) / 6, x=-3.0)
        head = label(r"A die whose faces average $4.5$, \ not $3.5$", font_size=34).to_edge(UP, buff=0.4)
        hv = DecimalNumber(math.log(6), num_decimal_places=3, font_size=34, color=ENT)
        hl = VGroup(label(r"entropy:", font_size=28), hv, label(r"nats", font_size=28)).arrange(RIGHT, buff=0.15)
        mv = DecimalNumber(3.5, num_decimal_places=2, font_size=34, color=DATA)
        ml = VGroup(label(r"average:", font_size=28), mv).arrange(RIGHT, buff=0.15)
        read = VGroup(ml, hl).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 1.3, 0])
        q = label(r"which of the many dice with average $4.5$?", font_size=26, color=GREY_A).next_to(read, DOWN, buff=0.5)
        rule = label(r"the one that assumes the least: \\ maximum entropy \ (Part 1's uncertainty)", font_size=26,
                     color=ENT).next_to(q, DOWN, buff=0.4)
        hc = history_card(r"1957, 1962", r"E.~T.~Jaynes", r"statistical mechanics as inference: \ the Brandeis dice "
                          r"problem", width=4.2).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is a puzzle from the physicist Edwin Jaynes. A die is loaded so that its faces average four and "
            "a half instead of three and a half. What is the chance of each face? <bookmark mark='a'/> Infinitely "
            "many dice have that average: this one, this one, this one. <bookmark mark='b'/> Jaynes's answer: pick "
            "the one that assumes nothing else, the one with the most uncertainty left, measured by part one's "
            "entropy. Anything less spread out claims knowledge we do not have."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(read))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for o in others[:4]:
                self.play(*bars.to(o), mv.animate.set_value(4.5), hv.animate.set_value(entropy(o)), run_time=0.9)
                self.wait(0.2)
            vo.wait_until("b")
            self.play(*bars.to(p_star), hv.animate.set_value(entropy(p_star)), FadeIn(rule), FadeIn(hc), run_time=1.5)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\lambda": LAM, r"Z(\lambda)": LAM}
        rows = [
            cmath(r"\max_p \;", r"-\textstyle\sum_k p_k \log p_k", r"\quad", r"\textstyle\sum_k p_k = 1,\;\;"
                  r"\sum_k k\, p_k = 4.5", font_size=32),
            cmath(r"\mathcal{L}", "=", r"-\textstyle\sum_k p_k \log p_k + \alpha\big(\sum_k p_k - 1\big) + ",
                  r"\lambda", r"\big(\textstyle\sum_k k\,p_k - 4.5\big)", colors=colors, font_size=32),
            cmath(r"\frac{\partial \mathcal{L}}{\partial p_k}", "=", r"-\log p_k - 1 + \alpha +", r"\lambda", r"\,k = 0",
                  colors=colors, font_size=32),
            cmath(r"p_k", "=", r"\frac{e^{\lambda k}}{Z(\lambda)}", colors=colors, font_size=36),
            cmath(r"\frac{d \log Z}{d\lambda}", "=", r"\textstyle\sum_k k\, p_k = 4.5", colors=colors, font_size=34),
        ]
        rows[0] = cmath(r"\max_p", "-", r"\textstyle\sum_k p_k \log p_k \;\;\text{given}\;\; \sum_k p_k = 1,\;\; "
                        r"\sum_k k\, p_k = 4.5", font_size=30)
        whys = [why(r"the most uncertain die \\ with the given average"),
                why(r"Lagrange multipliers \ (Part 4)"),
                why(r"set each derivative to zero"),
                why(r"$Z$ makes them add to $1$"),
                why(r"one equation for $\lambda$")]
        step = ladder(self, rows, whys, keep=5, top=3.25, x=-1.6, buff=0.42, edge=6.8)
        res = label(r"an exponential tilt: \ the exponential family", font_size=28, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Finding it is part four's constrained optimization. <bookmark mark='a'/> Maximize the entropy, subject "
            "to two constraints: the chances add to one, and they average four and a half. <bookmark mark='b'/> "
            "Give each constraint a Lagrange multiplier. <bookmark mark='c'/> Setting the derivative to zero makes "
            "the log of each chance a straight line in the face: <bookmark mark='d'/> the chance of face k is e to "
            "the lambda k, divided by a normalizer, Z. <bookmark mark='e'/> The only unknown is lambda, and the "
            "derivative of log Z is the average, so one equation fixes it."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fit(self):
        d = load("maxent")
        path = np.asarray(d["path"])
        lam, H, Hmax = float(d["lam"]), float(d["H"]), float(d["H_others_max"])
        bars = self.bars(path[0, 1:], x=-3.4, base=-2.6, col=MODEL)
        t = ValueTracker(0)
        k = np.arange(1, 7)

        def at(i):
            return path[min(int(round(i)), len(path) - 1)]

        lv = DecimalNumber(0, num_decimal_places=3, font_size=32, color=LAM)
        lv.add_updater(lambda m: m.set_value(at(t.get_value())[0]))
        mv = DecimalNumber(3.5, num_decimal_places=3, font_size=32, color=DATA)
        mv.add_updater(lambda m: m.set_value(float(at(t.get_value())[1:] @ k)))
        sv = Integer(0, font_size=32)
        sv.add_updater(lambda m: m.set_value(int(round(t.get_value()))))
        read = VGroup(VGroup(label(r"step", font_size=26), sv).arrange(RIGHT, buff=0.15),
                      VGroup(MathTex(r"\lambda =", font_size=32, color=LAM), lv).arrange(RIGHT, buff=0.15),
                      VGroup(label(r"average:", font_size=26), mv).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        read.move_to([-3.4, 2.5, 0])
        upd = cmath(r"\lambda \leftarrow \lambda + \eta\,\big(4.5 - \mathbb{E}_\lambda[k]\big)", font_size=30,
                    colors={r"\lambda \leftarrow \lambda + \eta\,\big(4.5 - \mathbb{E}_\lambda[k]\big)": LAM})
        upd.next_to(read, RIGHT, buff=0.6).align_to(read, UP)
        # the entropies of 20,000 other dice with the same average
        hh = np.asarray(d["H_hist"], float)
        lo = float(d["H_lo"])
        hx = Axes(x_range=[lo, H + 0.02, 0.1], y_range=[0, 1.05, 0.5], x_length=5.4, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, -1.5, 0])
        edges = np.linspace(lo, H, len(hh) + 1)
        hist = hist_shape(hx, edges, hh / hh.max(), color=GREY_B, opacity=0.4)
        star = DashedLine(hx.c2p(H, 0), hx.c2p(H, 1.05), color=ENT, stroke_width=3)
        sl = label(rf"maximum entropy: \ ${H:.4f}$", font_size=22, color=ENT).next_to(hx.c2p(H, 1.05), UP, buff=0.1).shift(LEFT * 0.6)
        hl = label(rf"${int(d['n_others']):,}$ other dice with average $4.5$: \ entropies".replace(",", "{,}"),
                   font_size=22, color=GREY_A).next_to(hx, DOWN, buff=0.15)
        verdict = (f"the highest of them reaches {Hmax:.4f}, just under" if Hmax < H else f"one of them reaches {Hmax:.4f}, at the maximum's level")
        with self.voiceover(
            "Solving that one equation is a tiny training run. Start from the fair die, with lambda zero, and nudge "
            "lambda by how far the average is from four and a half. <bookmark mark='a'/> The die tilts toward its "
            f"high faces, and settles at lambda {lam:.3f}: the chance of each face is about {math.exp(lam):.2f} "
            f"times the one below it. <bookmark mark='b'/> Its entropy is {H:.4f} nats. Twenty thousand other dice "
            f"with the same average, made at random: {verdict}."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(read), Write(upd))
            vo.wait_until("a")
            for i in range(len(bars.trackers)):
                bars.trackers[i].add_updater(lambda m, i=i: m.set_value(float(at(t.get_value())[1 + i])))
            self.add(*bars.trackers)
            self.play(t.animate.set_value(len(path) - 1), run_time=5.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(hx), FadeIn(hist), FadeIn(hl))
            self.play(Create(star), FadeIn(sl))
        for m in (lv, mv, sv, *bars.trackers):
            m.clear_updaters()
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        d = load("maxent")
        x = np.asarray(d["x"])
        gfit, lfit = np.asarray(d["gauss_fit"]), np.asarray(d["lap_fit"])
        head = label(r"Fix an average, \ get an exponential", font_size=36).to_edge(UP, buff=0.35)

        def panel(fitted, exact, col, title, cap):
            ax = Axes(x_range=[-4, 4, 2], y_range=[0, 0.55, 0.25], x_length=3.6, y_length=1.9, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False})
            xs = np.linspace(-4, 4, 200)
            ex = curve(ax, xs, exact(xs), color=GREY_B, stroke_width=6).set_stroke(opacity=0.45)
            m = (x >= -4) & (x <= 4)
            fc = curve(ax, x[m], fitted[m], color=col, stroke_width=3)
            t_ = label(title, font_size=22, color=col).next_to(ax, UP, buff=0.12)
            c_ = label(cap, font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
            return VGroup(ax, ex, fc, t_, c_)

        p1 = panel(gfit, lambda v: normal_pdf(v), MODEL, r"fix $\mathbb{E}[x]$ and $\mathbb{E}[x^2]$", r"the bell")
        p2 = panel(lfit, lambda v: 0.5 * np.exp(-np.abs(v)), C.INTERVAL, r"fix $\mathbb{E}|x|$", r"Laplace's double exponential")
        # Gibbs / softmax
        z = np.array([2.0, 1.2, 0.6, 0.1, -0.6])
        sm = np.exp(z) / np.exp(z).sum()
        ax3 = VGroup(*[Rectangle(width=0.4, height=2.4 * v, stroke_width=0, fill_color=LAM, fill_opacity=0.85)
                       for v in sm]).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        p3 = VGroup(ax3, label(r"fix the average energy", font_size=22, color=LAM).next_to(ax3, UP, buff=0.12),
                    label(r"Gibbs: \ $p_i \propto e^{-E_i/T}$ \ = \ softmax", font_size=20, color=GREY_A).next_to(ax3, DOWN, buff=0.12))
        panels = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to(UP * 0.4)
        fam = cmath(r"p(x)", "=", r"h(x)\, \exp\!\big(", r"\theta", r"\cdot T(x) - A(\theta)\big)", font_size=36,
                    colors={r"\theta": LAM}).to_edge(DOWN, buff=1.05)
        famn = label(r"the exponential family: \ $\nabla A(\theta) = \mathbb{E}[T(x)]$; \ Bernoulli, \ softmax, \ "
                     r"Gaussian, \ Poisson", font_size=22, color=GREY_A).next_to(fam, DOWN, buff=0.15)
        cite_ = cite(r"L.~Boltzmann (1877); \ J.~W.~Gibbs (1902); \ E.~T.~Jaynes (1957)", corner=UR)
        with self.voiceover(
            "The same recipe gives the distributions this series keeps meeting. <bookmark mark='a'/> On the line, "
            "fix the mean and the variance, solve numerically, and out comes the bell: it is the most uncertain "
            "distribution with a given spread. <bookmark mark='b'/> Fix the average distance from zero instead, and "
            "you get Laplace's double exponential. <bookmark mark='c'/> Fix the average energy of a physical "
            "system, and you get Boltzmann and Gibbs's distribution, e to the minus energy over temperature, where "
            "the temperature is the Lagrange multiplier. With scores in place of energies, that is the softmax at "
            "the end of every language model. <bookmark mark='d'/> All of them are one family, the exponential "
            "family, and in it the gradient of the log normalizer is the average. So fitting one by maximum "
            "likelihood just matches the data's averages."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(p1))
            vo.wait_until("b")
            self.play(FadeIn(p2))
            vo.wait_until("c")
            self.play(FadeIn(p3))
            vo.wait_until("d")
            self.play(Write(fam), FadeIn(famn))
        self.wait(0.3)
        self.clear_scene()
