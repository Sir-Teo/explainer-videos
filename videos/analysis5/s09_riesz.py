from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, interval_band, layer_cake, level_runs, load, plain_axes, polyline
from videos.analysis5.compute import trap


class RieszRepresentation(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.urysohn()
        self.construction()
        self.slicing()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Every positive functional is an integral", r"Where do measures come from?", lit=(),
                            part=5)
        with self.voiceover("Chapter eight: where measures come from. The answer is the Riesz representation theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def machine(self):
        box = RoundedRectangle(corner_radius=0.25, width=3.4, height=1.8, color=C.FUNCTIONAL, stroke_width=3)
        box.set_fill(C.FUNCTIONAL, 0.1).move_to([0, 0.6, 0])
        bl = MathTex(r"\Lambda", font_size=60, color=C.FUNCTIONAL).move_to(box)
        ax = plain_axes([0, 1, 0.5], [0, 1.1, 0.5], 2.8, 1.6).move_to([-4.6, 0.6, 0])
        x = np.linspace(0, 1, 400)
        f = np.clip(1 - 9 * (x - 0.45) ** 2, 0, None)
        fg = polyline(ax, x, f, color=C.FUNC, stroke_width=3)
        inp = Arrow(ax.get_right() + RIGHT * 0.1, box.get_left(), buff=0.1, color=GREY_B)
        out = Arrow(box.get_right(), box.get_right() + RIGHT * 1.6, buff=0.1, color=GREY_B)
        val = MathTex(rf"{trap(f, x):.4f}", font_size=40, color=C.MEASURE).next_to(out, RIGHT, buff=0.15)
        rules = VGroup(label(r"linear: \ $\Lambda(af + bg) = a\Lambda f + b\Lambda g$", font_size=26),
                       label(r"positive: \ $f \ge 0 \Rightarrow \Lambda f \ge 0$", font_size=26),
                       label(r"on $C_c(X)$: \ continuous functions vanishing outside a compact set", font_size=24,
                             color=GREY_A)).arrange(DOWN, buff=0.12).next_to(box, DOWN, buff=0.7)
        exs = VGroup(MathTex(r"\Lambda f = \int_0^1 f(x)\,dx", font_size=30),
                     MathTex(r"\Lambda f = f(a)", font_size=30),
                     MathTex(r"\Lambda f = \sum c_k f(x_k),\ c_k > 0", font_size=30)).arrange(RIGHT, buff=0.8)
        exs.to_edge(DOWN, buff=0.3)
        # each example run through the machine on the same f: the area, a point value, a weighted set of points
        a0, xk, ck = 0.3, [0.2, 0.45, 0.7], [0.5, 0.3, 0.2]

        def fv(t):
            return max(0.0, 1 - 9 * (t - 0.45) ** 2)

        outs = [float(trap(f, x)), fv(a0), sum(c_ * fv(t_) for c_, t_ in zip(ck, xk))]
        assert abs(outs[1] - 0.7975) < 1e-12 and abs(outs[2] - 0.60625) < 1e-12
        blabs = [MathTex(r"\int_0^1", font_size=50, color=C.FUNCTIONAL), MathTex(r"\delta_{0.3}", font_size=50,
                 color=C.FUNCTIONAL), MathTex(r"\textstyle\sum c_k \delta_{x_k}", font_size=44, color=C.FUNCTIONAL)]
        for b_ in blabs:
            b_.move_to(box)
        vals = [MathTex(rf"{v_:.4f}", font_size=40, color=C.MEASURE).next_to(out, RIGHT, buff=0.15) for v_ in outs]
        marks = [area_under(ax, x, f, C.MEASURE, 0.35),
                 VGroup(DashedLine(ax.c2p(a0, 0), ax.c2p(a0, fv(a0)), color=C.EPS, stroke_width=2),
                        Dot(ax.c2p(a0, fv(a0)), radius=0.07, color=C.EPS)),
                 VGroup(*[VGroup(DashedLine(ax.c2p(t_, 0), ax.c2p(t_, fv(t_)), color=C.EPS, stroke_width=2),
                                 Dot(ax.c2p(t_, fv(t_)), radius=0.05 + 0.12 * c_, color=C.EPS)) for c_, t_ in zip(ck, xk)])]
        thm = VGroup(label(r"The Riesz representation theorem", font_size=34),
                     MathTex(r"\Lambda f = \int_X f\,d\mu \quad \text{for one regular Borel measure } \mu", font_size=34,
                             color=C.EPS),
                     note(r"\textbf{RCA 2.14} \ (F.~Riesz 1909, \ Markov, \ Kakutani)")).arrange(DOWN, buff=0.12)
        thm.to_edge(UP, buff=0.3)
        assert thm.get_bottom()[1] > box.get_top()[1] + 0.2
        with self.voiceover(
            "<bookmark mark='a'/> Think of an integral as a machine: a function goes in, a number comes out, and the "
            "machine is linear and positive. <bookmark mark='b'/> The Riemann integral is one such machine. "
            "Evaluating at a point is another, and so is any positive combination of point evaluations. "
            "<bookmark mark='c'/> The Riesz representation theorem says that every such machine on the continuous "
            "functions with compact support is integration against exactly one regular measure. The measure is hidden "
            "inside the functional, and the theorem pulls it out."
        ) as vo:
            self.play(Create(box), FadeIn(bl), Create(ax), Create(fg))
            vo.wait_until("a")
            self.play(GrowArrow(inp), GrowArrow(out), FadeIn(val), FadeIn(rules))
            vo.wait_until("b")
            self.play(FadeIn(exs[0]), FadeIn(marks[0]), ReplacementTransform(bl, blabs[0]), FadeTransform(val, vals[0]))
            self.play(FadeIn(exs[1]), FadeOut(marks[0]), FadeIn(marks[1]), ReplacementTransform(blabs[0], blabs[1]),
                      FadeTransform(vals[0], vals[1]))
            self.play(FadeIn(exs[2]), FadeOut(marks[1]), FadeIn(marks[2]), ReplacementTransform(blabs[1], blabs[2]),
                      FadeTransform(vals[1], vals[2]))
            vo.wait_until("c")
            bl2 = MathTex(r"\Lambda", font_size=60, color=C.FUNCTIONAL).move_to(box)
            self.play(FadeIn(thm), FadeOut(marks[2]), ReplacementTransform(blabs[2], bl2), FadeTransform(vals[2], val))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def urysohn(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.2, 0.5], 9.0, 3.2).move_to([-0.5, -0.4, 0])
        x = np.linspace(0, 1, 1201)
        K = (0.35, 0.55)
        V = (0.22, 0.71)

        def ramp(t, a, b):
            return np.clip((t - a) / (b - a), 0, 1)

        m = 0.04  # f vanishes a little inside V, so its support [V0 + m, V1 - m] is a compact subset of V
        f = np.minimum(ramp(x, V[0] + m, K[0]), 1 - ramp(x, K[1], V[1] - m))
        fg = polyline(ax, x, f, color=C.FUNC, stroke_width=3.5)
        Kb = interval_band(ax, [K], ax.c2p(0, 0)[1] - 0.3, C.COMPACT_SET, height=0.16)
        Vb = interval_band(ax, [V], ax.c2p(0, 0)[1] - 0.55, C.OPEN_SET, height=0.16, opacity=0.5)
        Kl = MathTex("K", font_size=28, color=C.COMPACT_SET).next_to(Kb, RIGHT, buff=0.1)
        Vl = MathTex("V", font_size=28, color=C.OPEN_SET).next_to(Vb, RIGHT, buff=0.1)
        assert np.all(f[(x >= K[0]) & (x <= K[1])] == 1) and np.all(f[(x <= V[0] + m) | (x >= V[1] - m)] == 0)
        head = VGroup(label(r"Urysohn's lemma", font_size=34),
                      label(r"\textbf{RCA 2.12} \ compact $K \subset$ open $V$ $\Rightarrow$ a continuous $f$ with",
                            font_size=26),
                      MathTex(r"K \prec f \prec V: \quad f = 1 \text{ on } K,\ \ 0 \le f \le 1,\ \ f = 0 \text{ off a "
                              r"compact subset of } V", font_size=30, color=C.EPS)).arrange(DOWN, buff=0.12)
        head.to_edge(UP, buff=0.3)
        # the plateau over K, picked out when the narration reaches it
        onK = (x >= K[0]) & (x <= K[1])
        plat = polyline(ax, x[onK], f[onK], color=C.COMPACT_SET, stroke_width=7).set_stroke(opacity=0.85)
        note_ = label(r"the tool that lets a functional ``see'' sets: \ plateaus over $K$, \ fading out inside $V$",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The functional only sees continuous functions, so the proof needs continuous "
            "functions that imitate sets. Urysohn's lemma provides them: for a compact set inside an open set, "
            "<bookmark mark='b'/> there's a continuous plateau, equal to one on the compact set and fading to zero "
            "before it leaves the open set."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), FadeIn(Kb), FadeIn(Kl), FadeIn(Vb), FadeIn(Vl))
            vo.wait_until("a")
            self.play(FadeIn(head[1:]), Create(fg))
            vo.wait_until("b")
            self.play(Create(plat), FadeIn(note_))
            self.play(Indicate(fg, color=C.EPS, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def construction(self):
        d = load("riesz")
        trials, ks = d["trials"], d["ks"]
        L = float(trials[0, 0])
        rng = np.random.default_rng(2)
        a = np.sort(rng.uniform(0, 1, 8))
        iv = [(a[i], a[i + 1]) for i in range(0, 8, 2)]
        assert abs(sum(b - c for c, b in iv) - L) < 1e-12
        ax = plain_axes([0, 1, 0.25], [0, 1.2, 0.5], 7.6, 3.0).move_to([-2.6, -0.3, 0])
        x = np.linspace(0, 1, 4001)
        Vb = interval_band(ax, iv, ax.c2p(0, 0)[1] - 0.3, C.OPEN_SET, height=0.16, opacity=0.6)
        Vl = MathTex("V", font_size=28, color=C.OPEN_SET).next_to(Vb, LEFT, buff=0.15)

        def trapz_f(k):
            y = np.zeros_like(x)
            for c, b in iv:  # zero within col of each end, then a ramp of width col: support inside V
                col = min(1 / k, (b - c) / 4)
                y = np.maximum(y, np.clip(np.minimum((x - c - col) / col, (b - col - x) / col), 0, 1))
            return y

        frames = []
        for k, lam in zip((5, 20, 100, 1000), trials[0, 1:5]):
            y = trapz_f(k)
            assert abs(np.sum((y[1:] + y[:-1]) / 2) * (x[1] - x[0]) - lam) < 1e-6  # the drawn f_k has integral Lambda f_k
            frames.append(VGroup(area_under(ax, x, y, C.MEASURE, 0.4), polyline(ax, x, y, color=C.FUNC, stroke_width=3)))
        head = VGroup(label(r"Rudin's construction, \ run for $\Lambda f = \int_0^1 f$", font_size=34),
                      MathTex(r"\mu(V) = \sup\{\Lambda f : f \prec V\}, \qquad \mu(E) = \inf\{\mu(V) : E \subset V "
                              r"\text{ open}\}", font_size=32, color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"\text{collar}", r"\quad \Lambda f", font_size=28, color=GREY_A))
        for k, v in zip(ks, trials[0, 1:]):
            tab.add(MathTex(rf"1/{int(k)}" if k < 10**6 else r"10^{-8}", rf"\quad {v:.7f}", font_size=28))
        tab.add(MathTex(r"\text{length}(V)", rf"\quad {L:.7f}", font_size=28, color=C.OPEN_SET))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -0.5, 0])
        regrid(tab)
        note_ = label(r"six random open sets: \ all within $10^{-6}$ of their length", font_size=24,
                      color=GREY_A).next_to(tab, DOWN, buff=0.3)
        if note_.get_right()[0] > 6.6:
            note_.shift((6.6 - note_.get_right()[0]) * RIGHT)
        assert np.all(np.abs(trials[:, -1] - trials[:, 0]) < 1e-6)
        with self.voiceover(
            "<bookmark mark='a'/> Now the construction. For an open set V, let mu of V be the largest value the "
            "functional gives to plateau functions living inside V. For other sets, approximate from outside by open "
            "sets. <bookmark mark='b'/> Run it for the Riemann integral. The open set is four random intervals; the "
            "plateaus have collars of width one fifth, one twentieth, one hundredth, and so on. "
            "<bookmark mark='c'/> Their integrals climb to the total length of V. The machine has produced length."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), FadeIn(Vb), FadeIn(Vl))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(frames[0]))  # one plateau function living inside V: f < V
            vo.wait_until("b")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            cur = frames[0]
            for k in range(1, 4):
                self.play(ReplacementTransform(cur, frames[k]), FadeIn(tab[k + 1]), run_time=1.0)
                cur = frames[k]
            vo.wait_until("c")
            self.play(FadeIn(tab[5:]), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slicing(self):
        pm = ProofMap([r"$\mu$ on open sets: \ sup of $\Lambda f$", r"$\mu$ on all sets: \ outer approximation",
                       r"a $\sigma$-algebra where $\mu$ is countably additive", r"$\Lambda f = \int f\,d\mu$: \ slice "
                       r"$f$ into layers"], font_size=20, width=3.1, buff=0.28).to_edge(UP, buff=0.2)
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.25], 6.0, 4.0).move_to([-3.4, -0.75, 0])
        x = np.linspace(0, 1, 1601)
        f = 0.5 + 0.4 * np.sin(6 * x) * np.exp(-x)
        assert 0 < f.min() and f.max() < 1  # inside the window: nothing to clip
        fg = polyline(ax, x, f, color=WHITE, stroke_width=3)
        eps = 0.125
        # layers of thickness eps over the level sets of their midpoints: they hug the graph
        layers = layer_cake(ax, x, f, eps, n=int(np.ceil(f.max() / eps)))
        approx = layers.area
        I = trap(f, x)
        assert abs(approx - I) < 0.005 * I
        # step 1 of the proof in the picture: a level set {f > t} of the continuous f is open; its measure is a
        # layer's width
        t1 = 0.6
        lvl = DashedLine(ax.c2p(0, t1), ax.c2p(1, t1), color=C.OPEN_SET, stroke_width=2)
        Ob = interval_band(ax, level_runs(x, f > t1), ax.c2p(0, 0)[1] - 0.3, C.OPEN_SET, height=0.16, opacity=0.7)
        Ol = MathTex(r"\{f > t\}: \text{ open}", font_size=24, color=C.OPEN_SET).next_to(Ob, RIGHT, buff=0.2)
        Ol.set_x(ax.c2p(1, 0)[0] + 0.2 + Ol.width / 2)
        tl_ = MathTex("t", font_size=26, color=C.OPEN_SET).next_to(lvl, RIGHT, buff=0.1)
        rows = VGroup(MathTex(r"\Lambda f \approx \sum_i \varepsilon\, \mu(\{f > t_i\})", font_size=32),
                      MathTex(rf"\varepsilon = \tfrac18: \ {approx:.4f} \quad \text{{vs}} \quad \Lambda f = {I:.4f}",
                              font_size=30, color=C.MEASURE),
                      label(r"the layer picture from the opening: \ now inside Rudin's proof", font_size=24,
                            color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.7, -1.0, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to([0.15, -1.0, 0], RIGHT, buff=0)
        with self.voiceover(
            "<bookmark mark='a'/> The rest of the proof has four steps: define mu on open sets, extend it to all sets "
            "by approximating from outside, <bookmark mark='b'/> find a sigma-algebra on which it is countably "
            "additive, <bookmark mark='c'/> and finally show the functional is integration against mu. That last step "
            "slices f into horizontal layers of thickness epsilon: the functional of f is close to the sum of epsilon "
            "times the measure of each level set. <bookmark mark='d'/> Lebesgue's layer picture from the opening, now "
            "doing honest work inside the proof."
        ) as vo:
            self.play(FadeIn(pm), *pm.light(0), Create(ax), Create(fg))
            self.play(Create(lvl), FadeIn(tl_), FadeIn(Ob), FadeIn(Ol))
            vo.wait_until("a")
            self.play(*pm.light(1))
            vo.wait_until("b")
            self.play(*pm.light(2))
            vo.wait_until("c")
            self.play(*pm.light(3), FadeOut(VGroup(lvl, tl_, Ob, Ol)))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in layers], lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), *pm.done())
        self.wait(0.4)
        self.clear_scene()
