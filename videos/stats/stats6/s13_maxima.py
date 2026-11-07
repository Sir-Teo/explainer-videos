from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Maxima(VoiceoverScene):
    def construct(self):
        self.card()
        self.power()
        self.gumbel()
        self.seen()
        self.families()
        self.gev()

    def card(self):
        card = chapter_card(12, r"The law of maxima", r"Not the typical value, \ but the largest", lit=(1928,), part=PART)
        with self.voiceover("Chapter twelve. The law of maxima."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def power(self):
        A = axes([0, 9], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$P(\max \le x) = F(x)^n$", xticks=[0, 2, 4, 6, 8],
                 yticks=[0, 0.5, 1], center=[-2.2, -0.5, 0])
        ax = A.ax
        xs = np.linspace(0, 9, 200)
        cols = {1: GREY_B, 10: S.LIK, 100: SIM, 1000: S.PRIOR}
        cvs = VGroup(*[curve(ax, xs, (1 - np.exp(-xs)) ** n, c, 3) for n, c in cols.items()])
        leg = legend([(c, rf"$n = {n}$") for n, c in cols.items()], font_size=22).move_to([4.6, 0.4, 0])
        rows = VGroup(MathTex(r"P(\max_i X_i \le x) = P(\text{all } X_i \le x) = F(x)^n", font_size=28),
                      label(r"exponential waiting times: \ the curve slides right by $\log 10 \approx 2.3$ for each tenfold $n$",
                            font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.4)
        intro = label('The largest of independent draws', font_size=36)
        with self.voiceover(
            "Averages are not the only thing we need to predict. A sea wall has to survive the highest tide of the "
            "century, not the average one; a bridge, the heaviest load; an insurer, the worst year. These are "
            "maxima, and they have their own law. <bookmark mark='a'/> The largest of n independent values is below "
            "x exactly when all of them are, so its CDF is F of x to the n-th power. <bookmark mark='b'/> For "
            "exponential waiting times: one value, ten, a hundred, a thousand. As n grows the curve slides to the "
            "right, by about two point three for every tenfold increase, but its shape stops changing. That's a hint "
            "that, once we follow it, the maximum has a limiting shape of its own."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.4), FadeIn(leg), FadeIn(rows[1]), run_time=3.0)
        self.clear_scene()

    def gumbel(self):
        rows = [
            cmath(r"P(\max - \log n \le x)", r"=", r"\big(1 - e^{-(x + \log n)}\big)^n", font_size=32),
            cmath(r"P(\max - \log n \le x)", r"=", r"\Big(1 - \frac{e^{-x}}{n}\Big)^n", font_size=32),
            cmath(r"P(\max - \log n \le x)", r"\to", r"\exp\big(-e^{-x}\big)", font_size=34),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"i.i.d. Exp(1); $x\ge-\log n$: subtract $\log n$"), why(r"$e^{-\log n} = 1/n$"),
                why(r"$(1 + y/n)^n \to e^y$: \ the Gumbel distribution")]
        hc = history_card(1958, r"Emil Gumbel, \ \emph{Statistics of Extremes}", r"the standard text for engineers designing for "
                          r"floods, \ droughts and gales", color=S.MUSEUM, width=5.6, font_size=22).to_edge(DOWN, buff=0.5)
        intro = label('Follow an exponential maximum', font_size=36)
        with self.voiceover(
            "Follow it, and the limit appears. <bookmark mark='a'/> Subtract log n from the maximum of n "
            "exponentials. <bookmark mark='b'/> e to the minus log n is one over n, so the CDF becomes one minus e "
            "to the minus x over n, to the n-th power. <bookmark mark='c'/> And that's the limit that defines e: it "
            "tends to e to the minus e to the minus x. This is the Gumbel distribution, named for Emil Gumbel, "
            "whose 1958 book taught a generation of engineers to design for floods."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            self.play(FadeIn(hc))
        self.clear_scene()

    def seen(self):
        d = load("maxima")
        ed = np.asarray(d["exp_edges"])
        A = axes([-3, 6], [0, 0.42], x_length=7.6, y_length=4.4, xlabel=r"$\max - \log n$", xticks=[-2, 0, 2, 4, 6],
                 yticks=[0, 0.2, 0.4], center=[-1.8, -0.5, 0])
        ax = A.ax
        cur = hist_bars(ax, ed, np.asarray(d["exp_10"]), color=SIM, opacity=0.7)
        gum = curve(ax, np.asarray(d["gumbel_x"]), np.asarray(d["gumbel"]), EXACT, 3)
        nl = MathTex(r"n = 10", font_size=36).move_to([4.8, 1.6, 0])
        rows = VGroup(label(r"gold: \ Gumbel, \ $e^{-x}\exp(-e^{-x})$", font_size=24, color=EXACT),
                      label(r"skewed to the right: \ the maximum's long upper tail", font_size=22, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r in rows:
            if r.width > 4.2:
                r.width = 4.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.7, 0.5, 0])
        tag = note(r"simulated: 20,000 maxima of each size").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here it is. <bookmark mark='a'/> Twenty thousand maxima of ten exponentials, shifted by log ten. "
            "<bookmark mark='b'/> The gold curve is the Gumbel density. <bookmark mark='c'/> A hundred: "
            "<bookmark mark='d'/> a thousand. The histogram sits on the curve. Notice that it isn't symmetric: the "
            "maximum has a long upper tail, because occasionally one value in the batch is very large."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(nl))
            vo.wait_until("b")
            self.play(Create(gum), FadeIn(rows))
            for n, m in ((100, "c"), (1000, "d")):
                vo.wait_until(m)
                self.play(Transform(cur, hist_bars(ax, ed, np.asarray(d[f"exp_{n}"]), color=SIM, opacity=0.7)),
                          Transform(nl, MathTex(rf"n = {n}", font_size=36).move_to(nl)))
        self.clear_scene()

    def families(self):
        d = load("maxima")
        specs = [("Gumbel", r"light tails: \ exponential, \ normal", "exp", d["exp_edges"], d["gumbel_x"], d["gumbel"], [-3, 6], 0.42, SIM,
                  r"$\max - \log n$"),
                 ("Fr\\'echet", r"heavy tails: \ Pareto, \ Cauchy", "par", d["par_edges"], d["frechet_x"], d["frechet_pdf"], [0, 6], 1.0,
                  S.POST, r"$\max / \sqrt n$ \ (Pareto, $\alpha = 2$)"),
                 ("Weibull (reversed)", r"a hard ceiling: \ uniform, \ beta", "unif", d["unif_edges"], d["unif_x"], d["unif_pdf"], [0, 5],
                  1.05, S.LIK, r"$n(1 - \max)$ \ (uniform)")]
        panels = VGroup()
        for k, (nm, sub, key, ed, cx_, cy_, xr, ymax, c, xl) in enumerate(specs):
            cx = -4.5 + 4.5 * k
            A = axes(xr, [0, ymax], x_length=3.8, y_length=2.6, xlabel=xl, center=[cx, -0.8, 0], font_size=18)
            h = hist_bars(A.ax, np.asarray(ed), np.asarray(d[f"{key}_1000"]), color=c, opacity=0.7)
            cv = curve(A.ax, np.asarray(cx_), np.asarray(cy_), EXACT, 2.5)
            t = VGroup(label(nm, font_size=28, color=c), label(sub, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.1)
            t.move_to([cx, 1.7, 0])
            panels.add(VGroup(t, A, h, cv))
        tag = note(r"simulated: 20,000 maxima of 1,000 each").to_corner(DR, buff=0.25)
        intro = label('Three domains of attraction', font_size=36)
        with self.voiceover(
            "The Gumbel isn't the only possible limit. What happens depends on the tail of the original "
            "distribution. <bookmark mark='a'/> Light tails, like the exponential or the normal, give the Gumbel, "
            "after appropriate centring and scaling. <bookmark mark='b'/> Heavy, power-law tails, like the Pareto, give a different law, "
            "named for Maurice Fréchet: here the maximum must be scaled, not shifted, by root n for a Pareto with "
            "index two, and its limit has a power-law tail of its own. <bookmark mark='c'/> And a distribution with "
            "an endpoint with a power-law approach, as for the uniform or beta, gives a third, a reversed Weibull: the maximum creeps up to the "
            "ceiling, and its distance below it, times n, has an exponential limit."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(panels[k]))
        self.clear_scene()

    def gev(self):
        thm = theorem_card(r"Fisher--Tippett--Gnedenko", r"for i.i.d. $X_i$, $a_n>0$: if $(\max_i X_i - b_n)/a_n$ converges to a non-degenerate law, \ it is the "
                           r"GEV law ($\sigma>0$, $1+\xi(x-\mu)/\sigma>0$): $G(x) = \exp\big\{-[1 + \xi(x - \mu)/\sigma]^{-1/\xi}\big\}$",
                           who=r"Fisher \& Tippett 1928; \ Gnedenko 1943", color=S.ACCENT, width=10.4, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            MathTex(r"\xi > 0:\ \text{Fr\'echet (heavy tails)}", font_size=30, color=S.POST),
            MathTex(r"\xi = 0:\ \text{Gumbel},\ \ G(x) = \exp\{-e^{-(x - \mu)/\sigma}\}", font_size=30, color=SIM),
            MathTex(r"\xi < 0:\ \text{Weibull (a finite upper limit at } \mu - \sigma/\xi)", font_size=30, color=S.LIK),
            label(r"the central limit theorem of maxima: \ three shapes, \ one formula, \ one new parameter $\xi$", font_size=24,
                  color=S.ACCENT),
            label(r"a caution: \ maxima of normals approach the Gumbel only at the rate $1/\log n$", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.5)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> In 1928 Ronald Fisher and Leonard Tippett, studying the strength of cotton "
            "threads, found that these three are the only possibilities: if the maximum, suitably shifted and scaled, "
            "converges to anything, it's one of the three. Boris Gnedenko proved it rigorously in 1943. "
            "<bookmark mark='b'/> They combine into one family, the generalized extreme value law, with a shape "
            "parameter xi. Positive xi gives Fréchet's heavy tail; <bookmark mark='c'/> xi equal to zero, the "
            "Gumbel; <bookmark mark='d'/> negative xi, the Weibull, with a ceiling. <bookmark mark='e'/> It's the "
            "central limit theorem for maxima, with one extra parameter to estimate. <bookmark mark='f'/> And one "
            "caution: for normal data the convergence is painfully slow, at the rate one over log n."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k, m in enumerate("bcdef"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
