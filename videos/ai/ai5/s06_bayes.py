from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, MONO, PART, curve, load
from videos.ai.ai5.plotting import clipped_curve

X0, X1 = -5.6, 5.6  # the plot's horizontal extent on screen
YB, YH = -3.0, 3.3  # its baseline and height
POST = C.BITS


def nice_step(span):
    raw = span / 5
    e = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if m * e >= raw:
            return m * e
    return 10 * e


class Bayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.update()
        self.conjugacy()
        self.map_()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Belief as a distribution", r"How sure can a few letters make you?", part=PART)
        with self.voiceover("Chapter five. Belief as a distribution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def update(self):
        d = load("bayes")
        ns = [int(n) for n in d["ns"]]
        ks = [int(d[f"k{n}"]) for n in ns]
        head = d["head"]
        assert ks[1] == head[:10].count("e")
        pk = (ks[-1] + 1) / (ns[-1] + 2)
        us = [math.log10(n + 1) for n in ns]
        u = ValueTracker(0.0)

        def nk():
            v = u.get_value()
            n = 10 ** v - 1
            k = float(np.interp(v, us, [k_ / max(n_, 1) for k_, n_ in zip(ks, ns)])) * n if v > 0 else 0.0
            return n, k

        def view():
            n, k = nk()
            mean = (k + 1) / (n + 2)
            sd = math.sqrt(mean * (1 - mean) / (n + 3))
            half = min(0.5, 6 * sd)
            lo = min(max(mean - half, 0.0), 1 - 2 * half)
            return n, k, lo, lo + 2 * half

        def logpdf(p, n, k):
            return (math.lgamma(n + 2) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * np.log(p)
                    + (n - k) * np.log1p(-p))

        def X(p, lo, hi):
            return X0 + (X1 - X0) * (p - lo) / (hi - lo)

        def plot():
            n, k, lo, hi = view()
            ps = np.linspace(max(lo, 1e-4), min(hi, 1 - 1e-4), 300)
            dens = np.exp(logpdf(ps, n, k))
            top = max(1.5, float(dens.max()) * 1.15)
            pts = [np.array([X(p, lo, hi), YB + YH * y / top, 0]) for p, y in zip(ps, dens)]
            g = VGroup()
            area = Polygon(np.array([X(ps[0], lo, hi), YB, 0]), *pts, np.array([X(ps[-1], lo, hi), YB, 0]),
                           stroke_width=0, fill_color=POST, fill_opacity=0.22)
            g.add(area, VMobject(color=POST, stroke_width=4).set_points_smoothly(pts))
            g.add(Line([X0 - 0.2, YB, 0], [X1 + 0.2, YB, 0], color=GREY_C, stroke_width=2))
            step = nice_step(hi - lo)
            dec = max(0, -int(math.floor(math.log10(step))) + (1 if step / 10 ** math.floor(math.log10(step)) == 2.5 else 0))
            t0 = math.ceil(lo / step - 1e-9) * step
            t = t0
            while t <= hi + 1e-9:
                x = X(t, lo, hi)
                g.add(Line([x, YB, 0], [x, YB - 0.08, 0], color=GREY_C, stroke_width=2))
                g.add(MathTex(f"{t:.{dec}f}", font_size=24, color=GREY_B).move_to([x, YB - 0.3, 0]))
                t += step
            return g

        pic = always_redraw(plot)
        xl = label(r"the fraction of letters that are e", font_size=24, color=GREY_A).move_to([0, YB - 0.7, 0])
        # the letters, as read
        cells = VGroup()
        for i, ch in enumerate(head[:28]):
            box = Square(0.36, stroke_width=1.2, stroke_color=GREY_D, fill_color=C.BITS if ch == "e" else BACKGROUND,
                         fill_opacity=0.35 if ch == "e" else 0)
            cells.add(VGroup(box, Text(ch, font=MONO, font_size=20, color=C.BITS if ch == "e" else GREY_A).move_to(box)))
        cells.arrange(RIGHT, buff=0.04).to_edge(UP, buff=0.3)
        cl_n, cl_k = label(r"letters read:", font_size=30), label(r"e's:", font_size=30)

        def counter():
            n, k = nk()
            g = VGroup(cl_n.copy(), MathTex(f"{round(n):,}".replace(",", "{,}"), font_size=34), cl_k.copy(),
                       MathTex(f"{round(k):,}".replace(",", "{,}"), font_size=34, color=POST))
            g.arrange(RIGHT, buff=0.15)
            g[2].shift(RIGHT * 0.25)
            g[3].shift(RIGHT * 0.25)
            return g.next_to(cells, DOWN, buff=0.25).to_edge(RIGHT, buff=0.5)

        cnt = always_redraw(counter)
        colors = {r"p(\theta \mid D)": POST, r"p(D \mid \theta)": MODEL, r"p(\theta)": DATA}
        rule = cmath(r"p(\theta \mid D)", r"\;\propto\;", r"p(D \mid \theta)", r"\,", r"p(\theta)", colors=colors,
                     font_size=42).next_to(cells, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        names = VGroup(label(r"belief after", font_size=24, color=POST), MathTex(r"\propto", font_size=28),
                       label(r"how well $\theta$ explains the data $D$", font_size=24, color=MODEL),
                       MathTex(r"\times", font_size=28), label(r"belief before", font_size=24, color=DATA))
        names.arrange(RIGHT, buff=0.15).next_to(rule, DOWN, buff=0.2).align_to(rule, LEFT)
        prop = label(r"$\propto$: \ equal, up to a rescaling that makes the total $1$", font_size=24, color=GREY_A)
        prop.next_to(names, DOWN, buff=0.15).align_to(names, LEFT)
        flat = label(r"before any letters: \ every fraction equally believable", font_size=26, color=DATA)
        flat.move_to([0, YB + YH * (1 / 1.5) + 0.35, 0])
        ci = d["ci10000"]
        e_all = float(d["e_all"])
        assert ci[0] < e_all < ci[1]
        final = label(rf"$95\%$ of the belief: \ ${ci[0]:.3f}$ to ${ci[1]:.3f}$", font_size=28, color=POST)
        final.move_to([3.6, 0.2, 0])
        whole = label(rf"all ${int(d['n_all']):,}$ letters: \ ${e_all:.3f}$".replace(",", "{,}"), font_size=26,
                      color=WHITE).next_to(final, DOWN, buff=0.2)
        cite_ = cite(r"T.~Bayes (1763, \ published by R.~Price); \ P.-S.~Laplace (1774)", corner=DR).set_y(1.75)
        with self.voiceover(
            "How often is a letter an e? Before reading anything, we have no idea: any fraction from zero to one "
            "seems as plausible as any other. That's a belief, and we can draw it, as a flat line over every "
            "possibility. <bookmark mark='a'/> Bayes's rule, from Thomas Bayes's essay of 1763 and found again by "
            "Laplace in 1774, says how to update a belief when evidence arrives. "
            "Multiply what you believed by how well each possibility explains the evidence, then rescale, so the "
            "total is one again. <bookmark mark='b'/> That's what the sign, proportional to, means: equal, up to that "
            "rescaling."
        ) as vo:
            self.play(FadeIn(pic), FadeIn(xl), FadeIn(flat), FadeIn(cells), FadeIn(cnt))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(names), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(prop))
        with self.voiceover(
            f"Read the first ten letters: {ks[1]} e's. <bookmark mark='a'/> The belief leans toward "
            f"{ks[1] / ns[1]:.1f}, but it's still wide. <bookmark mark='b'/> After a hundred letters, it's narrower. "
            "<bookmark mark='c'/> After a thousand, narrower still. <bookmark mark='d'/> After ten thousand, it's a "
            f"sharp peak near {pk:.3f}: ninety-five percent of the belief lies between {ci[0]:.3f} and {ci[1]:.3f}. "
            f"<bookmark mark='e'/> The whole passage, all {int(d['n_all']):,} letters, gives {e_all:.3f}, "
            f"{'inside' if ci[0] < e_all < ci[1] else 'outside'} that range."
        ) as vo:
            self.play(FadeOut(flat), LaggedStart(*[Indicate(c, color=C.BITS, scale_factor=1.15) for c in cells[:10]],
                                                 lag_ratio=0.1), run_time=1.5)
            vo.wait_until("a")
            self.play(u.animate.set_value(us[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(u.animate.set_value(us[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(u.animate.set_value(us[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(u.animate.set_value(us[4]), run_time=2.0)
            self.play(FadeIn(final))
            vo.wait_until("e")
            self.play(FadeIn(whole))
        pic.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def conjugacy(self):
        d = load("bayes")
        ns = [int(n) for n in d["ns"]]
        ks = [int(d[f"k{n}"]) for n in ns]
        colors = {r"\theta^{k}(1-\theta)^{n-k}": MODEL, r"\theta^{a-1}(1-\theta)^{b-1}": DATA}
        rows = [
            cmath(r"p(\theta \mid D)", r"\propto", r"\theta^{k}(1-\theta)^{n-k}", r"\cdot", r"p(\theta)", colors=colors,
                  font_size=36),
            cmath(r"p(\theta \mid D)", r"\propto", r"\theta^{k}(1-\theta)^{n-k}", r"\cdot", r"\theta^{a-1}(1-\theta)^{b-1}",
                  colors=colors, font_size=36),
            cmath(r"p(\theta \mid D)", r"=", r"\operatorname{Beta}(a + k,\; b + n - k)", font_size=36,
                  colors={r"\operatorname{Beta}(a + k,\; b + n - k)": POST}),
            cmath(r"\mathbb{E}[\theta \mid D]", r"=", r"\frac{k + a}{n + a + b}", font_size=36),
        ]
        whys = [why(r"$k$ e's in $n$ letters: \ the binomial likelihood"),
                why(r"a Beta prior: \ the same shape"),
                why(r"the exponents add: \ a Beta again"),
                why(r"$a, b$: \ imagined e's and other letters")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.6, buff=0.45, edge=6.8)
        # three priors updated by the same letters, live
        X0_, X1_, YB_ = -5.8, 1.2, -3.4
        ax = Axes(x_range=[0, 0.6, 0.1], y_range=[0, 1.05, 0.5], x_length=X1_ - X0_, y_length=2.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([(X0_ + X1_) / 2, YB_ + 1.1, 0])
        xt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)])
        priors = [((1, 1), WHITE, r"flat: \ $a = b = 1$"), ((50, 50), C.SURPRISE, r"sure it is near $\tfrac12$: \ "
                                                                                    r"$a = b = 50$"),
                  ((6, 44), C.INTERVAL, r"a good guess: \ $a = 6, \ b = 44$")]
        u = ValueTracker(0.0)
        us = [math.log10(n + 1) for n in ns]
        ps = np.linspace(0.001, 0.6, 300)

        def dens(a, b):
            v = u.get_value()
            n = 10 ** v - 1
            k = float(np.interp(v, us, [k_ / max(n_, 1) for k_, n_ in zip(ks, ns)])) * n if v > 0 else 0.0
            lp = (a + k - 1) * np.log(ps) + (b + n - k - 1) * np.log1p(-ps)
            return np.exp(lp - lp.max())

        curves = VGroup(*[always_redraw(lambda a=a, b=b, col=col: curve(ax, ps, dens(a, b), color=col, stroke_width=3))
                          for (a, b), col, _ in priors])
        leg = VGroup(*[label(t, font_size=20, color=col) for _, col, t in priors]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        leg.next_to(ax, RIGHT, buff=0.3).align_to(ax, UP)
        nv = Integer(0, font_size=28)
        nl = VGroup(label(r"letters read:", font_size=22, color=GREY_A), nv).arrange(RIGHT, buff=0.12)
        nl.next_to(leg, DOWN, buff=0.25).align_to(leg, LEFT)
        nv.add_updater(lambda m: m.set_value(round(10 ** u.get_value() - 1)))
        tag = note(r"each curve scaled to the same height").next_to(nl, DOWN, buff=0.15).align_to(nl, LEFT)
        m_flat = (ks[1] + 1) / (ns[1] + 2)
        with self.voiceover(
            "Why did the belief keep this shape? <bookmark mark='a'/> Each letter multiplies in theta or one minus "
            "theta, so after k e's in n letters the likelihood is theta to the k, times one minus theta to the n "
            "minus k. <bookmark mark='b'/> Start from a prior of the same shape, a Beta distribution, <bookmark mark='c'/> "
            "and the exponents simply add: the belief stays a Beta, and updating is counting. <bookmark mark='d'/> "
            "Its mean is k plus a over n plus a plus b: the prior acts like a imagined e's and b other letters. "
            "With a flat prior that is Laplace's rule of succession from 1774: k plus one over n plus two, "
            f"{m_flat:.2f} after the first ten letters. <bookmark mark='e'/> Different priors start apart, and the "
            "same letters pull them together: by ten thousand letters, they agree."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(leg), FadeIn(nl), FadeIn(tag), *[Create(c) for c in curves])
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            vo.wait_until("e")
            self.play(u.animate.set_value(us[-1]), run_time=6.0, rate_func=linear)
        for m in list(curves) + [nv]:
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def map_(self):
        d = load("map")
        rows = [
            cmath(r"\hat w_{\mathrm{MAP}}", "=", r"\arg\max_w \; \log p(D \mid w) + \log p(w)", font_size=32),
            cmath(r"\log p(w)", "=", r"-\frac{\|w\|^2}{2\tau^2} + c", font_size=32),
            cmath(r"\log p(D \mid w)", "=", r"-\frac{1}{2\sigma^2}\textstyle\sum_i (y_i - f_w(x_i))^2 + c'", font_size=32),
            cmath(r"\hat w_{\mathrm{MAP}}", "=", r"\arg\min_w \textstyle\sum_i (y_i - f_w(x_i))^2 + \lambda \|w\|^2",
                  font_size=32, colors={r"\arg\min_w \textstyle\sum_i (y_i - f_w(x_i))^2 + \lambda \|w\|^2": C.BITS}),
        ]
        whys = [why(r"the peak of the posterior", font_size=22), why(r"a Gaussian prior on the weights", font_size=22),
                why(r"Gaussian noise of spread $\sigma$", font_size=22),
                why(r"$\lambda = \sigma^2/\tau^2$: \ weight decay", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-2.6, buff=0.28, edge=6.8)
        x, y, xt_, = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["xt"])
        ax = Axes(x_range=[0, 1, 0.5], y_range=[-1.6, 1.6, 1], x_length=5.4, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -2.3, 0])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=DATA) for a, b in zip(x, y)])
        truth = curve(ax, xt_, np.sin(2 * np.pi * xt_), color=GREY_B, stroke_width=2).set_stroke(opacity=0.6)
        fm = clipped_curve(ax, xt_, np.asarray(d["fit_mle"]), x_bounds=(0, 1), y_bounds=(-1.6, 1.6),
                           color=C.SURPRISE, stroke_width=3)
        fb = clipped_curve(ax, xt_, np.asarray(d["fit_best"]), x_bounds=(0, 1), y_bounds=(-1.6, 1.6),
                           color=C.BITS, stroke_width=3.5)
        leg = VGroup(label(r"maximum likelihood", font_size=20, color=C.SURPRISE),
                     label(r"MAP, \ best $\lambda$", font_size=20, color=C.BITS),
                     label(r"the truth, \ $\sin 2\pi x$", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.25)
        leg.next_to(ax, UP, buff=0.1)
        lams, med, q25, q75 = (np.asarray(d[k]) for k in ("lams", "med_err", "q25", "q75"))
        bx = Axes(x_range=[-10, 1, 3], y_range=[-2, 1, 1], x_length=5.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.5, -2.3, 0])
        ll = np.log10(lams)
        bb = band(bx, ll, np.log10(q25), np.minimum(np.log10(q75), 1), C.BITS, 0.15)
        bc = curve(bx, ll, np.minimum(np.log10(med), 1), color=C.BITS, stroke_width=3)
        xt = VGroup(*[MathTex(f"10^{{{v}}}", font_size=18, color=GREY_B).next_to(bx.c2p(v, -2), DOWN, buff=0.08)
                      for v in (-10, -7, -4, -1)])
        yt = VGroup(*[MathTex(t, font_size=18, color=GREY_B).next_to(bx.c2p(-10, v), LEFT, buff=0.08)
                      for t, v in (("0.1", -1), ("1", 0))])
        bl = label(r"test error \ (median of $200$ training sets) \ against $\lambda$", font_size=18, color=GREY_A)
        bl.next_to(bx, UP, buff=0.1)
        better = d["best_err"] < d["mle_med"]
        lam_e = -int(math.floor(math.log10(float(d["best_lam"]))))
        lam_m = float(d["best_lam"]) * 10 ** lam_e
        verdict = (f"Over two hundred training sets, maximum likelihood's median test error is {d['mle_med']:.2f}; "
                   f"the best lambda, about {lam_m:.0f} times ten to the minus {lam_e}, brings it to {d['best_err']:.3f}." if better else
                   f"Over two hundred training sets, the prior did not help: {d['best_err']:.3f} against "
                   f"{d['mle_med']:.3f}.")
        with self.voiceover(
            "A belief can also be used to pick a single answer: the peak of the posterior, called MAP, maximum a "
            "posteriori. <bookmark mark='a'/> Put a Gaussian prior on a model's weights, saying small weights are "
            "likelier, <bookmark mark='b'/> and Gaussian noise on its outputs. <bookmark mark='c'/> The MAP answer "
            "minimizes squared error plus lambda times the squared size of the weights: the weight decay used to "
            "train nearly every network, with lambda the noise over the prior's spread, squared. "
            "<bookmark mark='d'/> Ten points from a sine wave, and a polynomial of degree nine. Maximum likelihood "
            f"threads every point and swings wildly between them. The prior tames it. {verdict}"
        ) as vo:
            self.play(Create(ax), Create(truth), FadeIn(dots), FadeIn(leg[2]))
            step(0)
            vo.wait_until("a")
            step(1, transform=False)
            vo.wait_until("b")
            step(2, transform=False)
            vo.wait_until("c")
            step(3, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(leg[:2]))
            self.play(Create(fm), run_time=1.2)
            self.play(Create(fb), run_time=1.2)
            self.play(Create(bx), FadeIn(xt), FadeIn(yt), FadeIn(bl), FadeIn(bb), Create(bc))
        self.wait(0.3)
        self.clear_scene()
