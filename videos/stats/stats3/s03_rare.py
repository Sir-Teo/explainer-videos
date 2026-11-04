from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Rare(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.derive()
        self.converge()
        self.lecam()
        self.moments()
        self.tree_voiceover("The second arrow: <bookmark mark='t'/> a binomial with many trials and a small chance of "
                            "success, n times p held at lambda, becomes a Poisson.", 2)

    def card(self):
        card = chapter_card(2, r"The law of rare events", r"Many chances, each tiny: \ why horse kicks are Poisson",
                            lit=(1898,), part=PART)
        with self.voiceover("Chapter two. The law of rare events."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"P(X = k)", r"=", r"\binom{n}{k} \left(\frac{\lambda}{n}\right)^k \left(1 - \frac{\lambda}{n}\right)^{n-k}",
                  font_size=36),
            cmath(r"P(X = k)", r"=", r"\frac{n(n-1)\cdots(n-k+1)}{n^k}", r"\cdot", r"\frac{\lambda^k}{k!}", r"\cdot",
                  r"\left(1 - \frac{\lambda}{n}\right)^{n}", r"\cdot", r"\left(1 - \frac{\lambda}{n}\right)^{-k}",
                  font_size=32),
            cmath(r"P(X = k)", r"\to", r"1", r"\cdot", r"\frac{\lambda^k}{k!}", r"\cdot", r"e^{-\lambda}", r"\cdot", r"1",
                  font_size=36),
            cmath(r"P(X = k)", r"\to", r"\frac{\lambda^k e^{-\lambda}}{k!}", font_size=42),
        ]
        rows[3][2].set_color(EXACT)
        whys = [why(r"binomial with $p = \lambda / n$"), why(r"regroup"), why(r"$n \to \infty$, \ $k$ fixed; \ "
                                                                         r"$(1 - \lambda/n)^n \to e^{-\lambda}$"),
                why(r"Poisson (1837)")]
        intro = label(r"$n$ trials, \ each with chance $\lambda / n$: \ expected count $\lambda$, \ fixed", font_size=28,
                      color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why should horse kicks follow Poisson's formula? Think of each soldier on each day as a trial, with a "
            "tiny chance of a fatal kick. <bookmark mark='a'/> Many trials, each with a small chance, the expected "
            "number fixed at lambda. That's a binomial with n trials and success chance lambda over n. "
            "<bookmark mark='b'/> Regroup it into four factors. <bookmark mark='c'/> As n grows with k fixed, the "
            "first factor, k terms each nearly n over n, goes to one. The second doesn't depend on n. The third is "
            "one minus lambda over n, to the n, which goes to e to the minus lambda, the definition of the "
            "exponential. And the last goes to one. <bookmark mark='d'/> What's left is Poisson's formula. It's "
            "called the law of rare events: count many independent rare chances, and you get a Poisson, whatever "
            "the details."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.4, buff=0.55, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.clear_scene()

    def converge(self):
        d = load("rare")
        ks = np.asarray(d["ks"])
        pois = np.asarray(d["pois"])
        A = axes([-0.6, 10.6], [0, 0.42], x_length=8.4, y_length=4.4, xlabel=r"$k$", xticks=list(range(0, 11)),
                 yticks=[0, 0.2, 0.4], center=[-1.4, -0.4, 0])
        ax = A.ax
        dots = pmf_dots(ax, ks, pois, EXACT, radius=0.08)
        rows = d["rows"]
        bars = [pmf_bars(ax, ks, np.asarray(r["pmf"]), DISC, width=0.6) for r in rows]
        lab = [MathTex(rf"\text{{binomial}}\left({r['n']}, \tfrac{{2}}{{{r['n']}}}\right)", font_size=32, color=DISC)
               .move_to([4.6, 2.4, 0]) for r in rows]
        tv = [MathTex(rf"\text{{total variation}} = {r['tv']:.4f}", font_size=28, color=GREY_A).move_to([4.6, 1.6, 0])
              for r in rows]
        leg = legend([(EXACT, r"Poisson$(2)$")], font_size=24).move_to([4.6, 0.6, 0])
        dfn = definition_card(r"Total variation distance", r"the largest difference the two distributions give to any "
                              r"event: \ $\tfrac12 \sum_k |p_k - q_k|$", color=GREY_B, width=5.0, font_size=21)
        dfn.move_to([4.5, -1.7, 0])
        with self.voiceover(
            "Watch it happen. <bookmark mark='a'/> The gold dots are the Poisson with lambda two. "
            "<bookmark mark='b'/> A binomial with four trials, each with chance a half, is a poor match. "
            "<bookmark mark='c'/> Ten trials with chance a fifth is closer; <bookmark mark='d'/> fifty trials, "
            "closer still; <bookmark mark='e'/> and a thousand trials with chance one in five hundred is "
            "indistinguishable. <bookmark mark='f'/> To measure the gap we use total variation distance: the "
            "biggest difference the two distributions could give to the probability of any event. It falls from "
            f"{rows[0]['tv']:.2f} to {rows[-1]['tv']:.4f}."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(leg))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(lab[0]), FadeIn(tv[0]))
            cur, cl, ct = bars[0], lab[0], tv[0]
            for k, m in zip(range(1, 4), "cde"):
                vo.wait_until(m)
                self.play(Transform(cur, bars[k]), Transform(cl, lab[k]), Transform(ct, tv[k]), run_time=1.4)
            vo.wait_until("f")
            self.play(FadeIn(dfn))
        self.clear_scene()

    def lecam(self):
        d = load("rare")
        grid = np.asarray(d["grid"])
        A = axes([0.3, 3.4], [-4, 0.2], x_length=7.4, y_length=4.4, xlabel=r"trials $n$ (log scale)",
                 ylabel=r"distance (log scale)", xticks=[1, 2, 3], yticks=[-4, -3, -2, -1, 0],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.2, -0.3, 0])
        ax = A.ax
        tvc = curve(ax, np.log10(grid), np.log10(np.asarray(d["tvs"])), DISC, 3)
        bd = curve(ax, np.log10(grid), np.log10(np.asarray(d["bounds"])), EXACT, 3)
        th = theorem_card(r"Le Cam's inequality", r"for independent Bernoulli$(p_i)$, \ the total variation between "
                          r"$\sum X_i$ and Poisson$(\sum p_i)$ is at most $\sum p_i^2$", who=r"L. Le Cam, 1960",
                          color=EXACT, width=5.4, font_size=22).move_to([4.2, 1.7, 0])
        ex = MathTex(r"\sum p_i^2 = n \left(\tfrac{\lambda}{n}\right)^2 = \frac{\lambda^2}{n}", font_size=30,
                     color=EXACT).move_to([4.2, -0.4, 0])
        more = label(r"the $p_i$ need not be equal: \ any many small, independent chances", font_size=22,
                     color=GREY_A).move_to([4.2, -1.4, 0])
        if more.width > 5.6:
            more.width = 5.6
        leg = legend([(DISC, r"actual distance"), (EXACT, r"Le Cam's bound")], font_size=22).move_to([4.2, -2.6, 0])
        with self.voiceover(
            "How fast does the binomial approach the Poisson? <bookmark mark='a'/> On log scales, the actual "
            "distance, blue, falls in a straight line: one over n. <bookmark mark='b'/> Lucien Le Cam proved in 1960 "
            "a bound that holds far more generally. For independent trials with different chances p i, the "
            "distance between their total and a Poisson with the same mean is at most the sum of the squared "
            "chances. <bookmark mark='c'/> For our equal chances that's lambda squared over n, the gold line, "
            "always above the truth. <bookmark mark='d'/> And it's why the law of rare events is so robust: the "
            "soldiers needn't have equal risks. As long as each chance is small and they're independent, the count "
            "is nearly Poisson."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(tvc), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(th, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(Create(bd), Write(ex), FadeIn(leg))
            vo.wait_until("d")
            self.play(FadeIn(more))
        self.clear_scene()

    def moments(self):
        rows = [
            cmath(r"E X", r"=", r"\sum_{k \ge 1} k\, \frac{\lambda^k e^{-\lambda}}{k!}", r"=",
                  r"\lambda \sum_{k \ge 1} \frac{\lambda^{k-1} e^{-\lambda}}{(k-1)!}", r"=", r"\lambda", font_size=32),
            cmath(r"E\, X(X-1)", r"=", r"\lambda^2 \sum_{k \ge 2} \frac{\lambda^{k-2} e^{-\lambda}}{(k-2)!}", r"=",
                  r"\lambda^2", font_size=32),
            cmath(r"\mathrm{Var}\, X", r"=", r"\lambda^2 + \lambda - \lambda^2", r"=", r"\lambda", font_size=36),
        ]
        rows[0][6].set_color(EXACT)
        rows[2][4].set_color(EXACT)
        whys = [why(r"cancel one $k$; \ the sum is a whole Poisson"), why(r"cancel two"),
                why(r"$E X^2 = E X(X-1) + E X$")]
        bk = label(r"Bortkiewicz's corps-years: \ mean $0.61$, \ variance $0.61$", font_size=26, color=S.MUSEUM)
        bk.to_edge(DOWN, buff=0.9)
        od = label(r"a variance well above the mean signals something more: \ chapter 12", font_size=22, color=GREY_B)
        od.next_to(bk, DOWN, buff=0.2)
        with self.voiceover(
            "One more property of the Poisson, and it's the one Bortkiewicz checked. <bookmark mark='a'/> Its mean: "
            "cancel one k against the factorial, and what's left is lambda times a whole Poisson distribution, "
            "which sums to one. <bookmark mark='b'/> Cancel two, and the expectation of X times X minus one is "
            "lambda squared. <bookmark mark='c'/> So the variance is lambda too: for a Poisson, mean and variance are "
            "equal. <bookmark mark='d'/> The horse kicks pass this test, point six one and point six one. When real "
            "counts have a variance far above their mean, something else is going on, and chapter twelve says what."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(bk), FadeIn(od))
        self.clear_scene()
