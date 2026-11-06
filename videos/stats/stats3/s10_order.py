from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403

K_COLS = {"1": "#7EC8F5", "3": "#7BD88F", "8": "#F2C14E", "10": "#FF9F5A"}


class Order(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.density()
        self.beta()
        self.median()
        self.tanks()
        self.tree_voiceover("Two arrows into the beta: <bookmark mark='t'/> the order statistics of uniforms, and the "
                            "share X over X plus Y of two independent gammas with the same scale.", 9)

    def card(self):
        card = chapter_card(9, r"Order statistics", r"The smallest, the largest, and everything in between",
                            lit=(), part=PART)
        with self.voiceover("Chapter nine. Order statistics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def density(self):
        line = NumberLine(x_range=[0, 1, 0.25], length=10, include_numbers=False, color=GREY_C).move_to([0, 2.0, 0])
        g = np.random.Generator(np.random.PCG64(8))
        u = np.sort(g.random(10))
        dots = VGroup(*[Dot(line.n2p(x), radius=0.08, color=SIM) for x in u])
        labs = VGroup(*[MathTex(rf"X_{{({i + 1})}}", font_size=22, color=SIM).next_to(dt, UP if i % 2 else DOWN,
                                                                                      buff=0.15)
                        for i, dt in enumerate(dots)])
        k = 3
        win = Rectangle(width=0.32, height=0.6, stroke_color=S.ACCENT, stroke_width=2).move_to(dots[k - 1])
        rows = [
            cmath(r"P\big(X_{(k)} \in [x, x + dx]\big)", r"\approx", r"\frac{n!}{(k-1)!\,1!\,(n-k)!}\,"
                  r"F(x)^{k-1}\, f(x)\,dx\, \big(1 - F(x)\big)^{n-k}", font_size=30),
            cmath(r"f_{(k)}(x)", r"=", r"\frac{n!}{(k-1)!\,(n-k)!}\, F(x)^{k-1} \big(1 - F(x)\big)^{n-k} f(x)", font_size=32),
        ]
        rows[1][0].set_color(EXACT)
        whys = [why(r"$k - 1$ below, \ one in the window, \ $n - k$ above: \ a multinomial"), why(r"divide by $dx$")]
        with self.voiceover(
            "Sort a sample, and its values become order statistics: the smallest, the second smallest, up to the "
            "largest. <bookmark mark='a'/> Here are ten uniform draws, sorted. <bookmark mark='b'/> What's the "
            "distribution of the k-th smallest, say the third? <bookmark mark='c'/> For it to sit in a tiny window "
            "at x, we need k minus one of the draws below x, one in the window, and the rest above. That's a "
            "multinomial count, from Part 2: <bookmark mark='d'/> n factorial over the three factorials, times the "
            "chance of each part. Divide by the window's width and you have the density of the k-th order "
            "statistic, for independent, identically distributed draws from a distribution with a density."
        ) as vo:
            self.play(Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.1), FadeIn(labs))
            vo.wait_until("b")
            self.play(Create(win), Indicate(dots[k - 1], color=S.ACCENT, scale_factor=1.6))
            step = ladder(self, rows, whys, keep=2, top=0.6, x=-0.6, buff=0.7, edge=6.9)
            vo.wait_until("c")
            step(0, transform=False)
            vo.wait_until("d")
            step(1, transform=False)
        self.clear_scene()

    def beta(self):
        d = load("order")
        xs = np.asarray(d["xs"])
        A = axes([0, 1], [0, 10.5], x_length=7.6, y_length=4.4, xlabel=r"$x$", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 5, 10], center=[-2.2, -0.4, 0])
        ax = A.ax
        ed = np.linspace(0, 1, 41)
        hs = VGroup()
        cs = VGroup()
        for k in ("1", "3", "8", "10"):
            hs.add(hist_bars(ax, ed, np.clip(np.asarray(d["hists"][k]), 0, 10.5), color=K_COLS[k], opacity=0.35))
            cs.add(curve(ax, xs, np.clip(np.asarray(d["beta"][k]), 0, 10.5), K_COLS[k], 3))
        leg = legend([(K_COLS[k], rf"$X_{{({k})}}$ of 10") for k in ("1", "3", "8", "10")], font_size=22)
        leg.move_to([4.6, 2.4, 0])
        f = MathTex(r"U_{(k)}", r"\sim", r"\text{beta}(k,\ n + 1 - k)", font_size=34, color=EXACT).move_to([4.4, 0.9, 0])
        f2 = MathTex(r"f(x) \propto x^{k-1}(1 - x)^{n-k}", font_size=28).next_to(f, DOWN, buff=0.25)
        mean = MathTex(r"E\, U_{(k)} = \frac{k}{n+1}", font_size=30).next_to(f2, DOWN, buff=0.3)
        gb = VGroup(label(r"also: \ $\Gamma_a / (\Gamma_a + \Gamma_b)$", font_size=22, color=GREY_B),
                    label(r"independent gammas with the same scale", font_size=22, color=GREY_B))
        gb.arrange(DOWN, buff=0.12).next_to(mean, DOWN, buff=0.35)
        tag = note(r"simulated: 20,000 samples of 10 uniforms").to_corner(DR, buff=0.3)
        with self.voiceover(
            "For uniform draws, F of x is just x, and the formula becomes a polynomial: x to the k minus one times "
            "one minus x to the n minus k. <bookmark mark='a'/> That's the beta distribution. <bookmark mark='b'/> "
            "Here are twenty thousand simulated samples of ten: the smallest, the third, the eighth and the largest "
            "of each, against the beta densities. The smallest hugs zero, the largest hugs one, and the k-th "
            "averages k over n plus one, as if the ten points split the interval into eleven equal gaps on "
            "average. <bookmark mark='c'/> The beta has another parent too: if X and Y are independent gammas with the same scale, X "
            "over X plus Y is beta. That's the arrow from gamma, and it's why the beta returns in Part 15 as the "
            "natural prior for a probability."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(f2))
            vo.wait_until("b")
            self.play(FadeIn(hs), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), FadeIn(leg), run_time=3.0)
            self.play(Write(mean))
            vo.wait_until("c")
            self.play(FadeIn(gb))
        self.clear_scene()

    def median(self):
        from scipy import stats as st
        A = axes([0, 1], [0, 12], x_length=7.0, y_length=4.2, xlabel=r"the sample median of $n$ uniforms",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 5, 10], center=[-2.6, -0.5, 0])
        ax = A.ax
        xs = np.linspace(0.001, 0.999, 300)
        cols = {5: S.EST, 21: S.ACCENT, 101: S.POST}
        cvs = VGroup(*[curve(ax, xs, np.clip(st.beta.pdf(xs, (n + 1) // 2, (n + 1) // 2), 0, 12), c, 3) for n, c in cols.items()])
        leg = legend([(c, rf"$n = {n}$: \ SD ${st.beta.std((n + 1) // 2, (n + 1) // 2):.3f}$") for n, c in cols.items()],
                     font_size=22).move_to([4.2, 1.8, 0])
        f = MathTex(r"n = 2m + 1:\quad U_{(m+1)} \sim \text{beta}(m+1,\ m+1)", font_size=30, color=EXACT).move_to([3.8, 0.2, 0])
        sd = MathTex(r"\mathrm{SD} \approx \frac{1}{2\sqrt n}", font_size=32).move_to([4.0, -0.9, 0])
        nxt = label(r"the median's own law: \ robust estimation, \ Part 30", font_size=22, color=GREY_B).move_to([4.0, -1.9, 0])
        intro = label('The median has a sampling law', font_size=36)
        with self.voiceover(
            "Put k in the middle and you get the law of the sample median. <bookmark mark='a'/> For an odd number "
            "of uniform draws, n equals two m plus one, the median is the m plus first order statistic, a symmetric "
            "beta. <bookmark mark='b'/> With five draws it's broad; with twenty-one, narrower; with a hundred and "
            "one, sharply peaked at a half. Its standard deviation shrinks like one over twice the square root of "
            "n, the same root n rate as the mean. The median has a sampling distribution of its own, and Part 30 "
            "uses it to build estimators that heavy tails can't break."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A), Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.4), FadeIn(leg), run_time=3.0)
            self.play(FadeIn(sd), FadeIn(nxt))
        self.clear_scene()

    def tanks(self):
        d = load("order")
        serial = np.asarray(d["serial"])
        hc = history_card(1943, r"Allied statisticians, \ the German tank problem", r"estimate production from the "
                          r"serial numbers on captured tanks; \ after the war, the estimates proved far closer to the "
                          r"German records than intelligence reports (Ruggles \& Brodie, 1947)", color=S.MUSEUM,
                          width=6.4, font_size=22).move_to([-3.2, 2.2, 0])
        line = NumberLine(x_range=[0, 320, 40], length=12, include_numbers=False, color=GREY_C).move_to([0, -0.2, 0])
        tk = VGroup(*[MathTex(str(v), font_size=20, color=GREY_B).next_to(line.n2p(v), DOWN, buff=0.12)
                      for v in range(0, 321, 80)])
        dots = VGroup(*[Dot(line.n2p(v), radius=0.08, color=SIM) for v in serial])
        sl = VGroup(*[MathTex(str(v), font_size=20, color=SIM).next_to(dt, UP, buff=0.15 + 0.35 * (i % 3))
                      for i, (v, dt) in enumerate(zip(serial, dots))])
        mx = serial.max()
        est = d["est"]
        el = Line(line.n2p(est) + DOWN * 0.3, line.n2p(est) + UP * 0.5, color=S.EST, stroke_width=4)
        tl = Line(line.n2p(d["N"]) + DOWN * 0.3, line.n2p(d["N"]) + UP * 0.5, color=S.TRUTH, stroke_width=4)
        f = MathTex(r"\hat N", r"=", r"\max\Big(1 + \frac1k\Big) - 1", r"=", rf"{mx} \cdot \tfrac98 - 1", r"=",
                    rf"{est:.0f}", font_size=32).move_to([0, -1.8, 0])
        f[6].set_color(S.EST)
        why_ = label(r"$k+1$ unobserved gaps share $N-k$ missing serials: \ estimate $N$ from the maximum",
                     font_size=22, color=GREY_B).next_to(f, DOWN, buff=0.2)
        res = MathTex(rf"N = {d['N']}:\ \ 5{{,}}000\text{{ repetitions: estimate averages }} {d['ests_mean']:.1f};\ \ "
                      rf"\text{{the maximum alone }} {d['max_mean']:.1f}", font_size=26, color=SIM).to_edge(DOWN, buff=0.35)
        intro = label('Estimating from serial numbers', font_size=36)
        with self.voiceover(
            "Order statistics once helped win a war. <bookmark mark='a'/> During the Second World War the Allies "
            "wanted to know how many tanks Germany was producing. Captured tanks carried serial numbers, numbered "
            "in sequence. Here are eight serials from a factory that, in our simulation, built three hundred. "
            f"<bookmark mark='b'/> The largest serial, {mx}, is a lower bound. But the sorted serials split the "
            "range into k plus one gaps of missing serials, with expected size N minus k over k plus one. In particular the expected maximum is k times N plus one over k plus one. "
            f"<bookmark mark='c'/> Solve that expectation identity: the unbiased estimate is the maximum times one plus one over k, minus one, here "
            f"{est:.0f}. <bookmark mark='d'/> Over five thousand repetitions it averages {d['ests_mean']:.0f}, "
            "unbiased, while the maximum alone falls short. After the war, the statisticians' estimates turned out "
            "to be far closer to Germany's own records than the intelligence reports had been. Part 9 proves that "
            "this estimator is the best unbiased one."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc), Create(line), FadeIn(tk))
            self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.15), FadeIn(sl))
            vo.wait_until("b")
            self.play(Indicate(dots[-1], color=S.ACCENT, scale_factor=1.8))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(why_), Create(el))
            vo.wait_until("d")
            self.play(Create(tl), FadeIn(res))
        self.clear_scene()
