from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import DATA, MODEL, MONO, load

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

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Belief as a distribution", r"How sure can a few letters make you?", part=4)
        with self.voiceover("Chapter three. Belief as a distribution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def update(self):
        d = load("bayes")
        ns = [int(n) for n in d["ns"]]
        ks = [int(d[f"k{n}"]) for n in ns]
        head = d["head"]
        assert ks[1] == head[:10].count("e") == 3
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
        flat = label(r"before any letters: \ every fraction equally believable", font_size=26, color=DATA)
        flat.move_to([0, YB + YH * (1 / 1.5) + 0.35, 0])
        ci = d["ci10000"]
        e_all = float(d["e_all"])
        assert ci[0] < e_all < ci[1]
        final = label(rf"$95\%$ of the belief: \ ${ci[0]:.3f}$ to ${ci[1]:.3f}$", font_size=28, color=POST)
        final.move_to([3.6, 0.2, 0])
        whole = label(rf"all ${int(d['n_all']):,}$ letters: \ ${e_all:.3f}$".replace(",", "{,}"), font_size=26,
                      color=WHITE).next_to(final, DOWN, buff=0.2)
        lap = label(r"Laplace (1774): \ best guess $\dfrac{k + 1}{n + 2}$", font_size=30, color=GREY_A)
        lap.next_to(whole, DOWN, buff=0.35)
        with self.voiceover(
            "How often is a letter an e? Before reading anything, we have no idea: any fraction from zero to one "
            "seems as plausible as any other. That's a belief, and we can draw it, as a flat line over every "
            "possibility. <bookmark mark='a'/> Bayes's rule says how to update a belief when evidence arrives. "
            "Multiply what you believed by how well each possibility explains the evidence, then rescale, so the "
            "total is one again."
        ) as vo:
            self.play(FadeIn(pic), FadeIn(xl), FadeIn(flat), FadeIn(cells), FadeIn(cnt))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(names))
        with self.voiceover(
            "Read the first ten letters: three e's. <bookmark mark='a'/> The belief leans toward a third, but it's "
            "still wide. <bookmark mark='b'/> After a hundred letters, it's narrower. <bookmark mark='c'/> After a "
            "thousand, narrower still. <bookmark mark='d'/> After ten thousand, it's a sharp peak near 0.127: "
            "ninety-five percent of the belief lies between 0.120 and 0.134. <bookmark mark='e'/> The whole "
            "passage, all sixteen thousand letters, gives 0.122, inside that range."
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
        with self.voiceover(
            "So the answer isn't one number. It's a distribution: a best guess with its uncertainty attached, "
            "narrowing like one over the square root of the evidence. <bookmark mark='a'/> Laplace worked this out "
            "in 1774. His best guess after k e's in n letters is k plus one, over n plus two. Before any evidence, "
            "that's one half."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(lap))
        pic.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
