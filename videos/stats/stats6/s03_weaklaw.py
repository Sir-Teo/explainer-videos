from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class WeakLaw(VoiceoverScene):
    def construct(self):
        self.card()
        self.proof()
        self.paths()
        self.no_compensation()
        self.bernoulli()
        self.compare()

    def card(self):
        card = chapter_card(2, r"The weak law", r"Why the average settles down", lit=(1713,), part=PART)
        with self.voiceover("Chapter two. The weak law of large numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def proof(self):
        rows = [
            cmath(r"\mathrm{Var}\,\bar X_n", r"=", r"\frac{1}{n^2}\sum_{i=1}^n \mathrm{Var}\,X_i", r"=", r"\frac{\sigma^2}{n}", font_size=34),
            cmath(r"P(|\bar X_n - \mu| \ge \varepsilon)", r"\le", r"\frac{\sigma^2}{n\varepsilon^2}", font_size=34),
            cmath(r"P(|\bar X_n - \mu| \ge \varepsilon)", r"\to", r"0", r"\quad \text{for every } \varepsilon > 0", font_size=34),
        ]
        rows[0][4].set_color(SIM)
        rows[2][2].set_color(EXACT)
        whys = [why(r"independence: \ the covariances vanish (Part 5)"), why(r"Chebyshev, \ with $k\sigma = \varepsilon$"),
                why(r"as $n \to \infty$")]
        thm = theorem_card(r"The weak law of large numbers", r"if $X_1, X_2, \dots$ are independent with mean $\mu$ and finite "
                           r"common variance $\sigma^2<\infty$, \ then $\bar X_n \to \mu$ in probability", who=r"Chebyshev's proof, 1867",
                           color=S.ACCENT, width=8.6, font_size=24).to_edge(DOWN, buff=0.5)
        intro = label('Why the average approaches its mean', font_size=36)
        with self.voiceover(
            "With Chebyshev's inequality the law of large numbers takes three lines. <bookmark mark='a'/> The variance "
            "of an average of n independent variables, each with variance sigma squared, is sigma squared over n: "
            "the covariances vanish, as in Part 5. <bookmark mark='b'/> Apply Chebyshev to the average. The chance "
            "that it misses the mean by epsilon or more is at most sigma squared over n epsilon squared. "
            "<bookmark mark='c'/> For any fixed epsilon, however small, that goes to zero as n grows. "
            "<bookmark mark='d'/> That's the weak law: the average converges to the mean in probability. Notice how "
            "little it needed: a common mean and variance and pairwise zero covariance. For i.i.d. observations, even a finite absolute first moment suffices, as the strong law in chapter three implies."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.8, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.clear_scene()

    def paths(self):
        d = load("paths")
        steps, means = np.asarray(d["steps"], float), np.asarray(d["means"])
        A = axes([0, np.log10(4000)], [0, 1], x_length=8.6, y_length=4.6, xlabel=r"number of tosses, $n$ (log scale)",
                 ylabel=r"share of heads", xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[-1.4, -0.4, 0])
        ax = A.ax
        lx = np.log10(steps)
        lines = VGroup(*[polyline(ax, lx, m, SIM, 1.4, 0.55) for m in means])
        nn = np.logspace(0, np.log10(4000), 120)
        hi = curve(ax, np.log10(nn), np.clip(0.5 + 1 / np.sqrt(nn), 0, 1), EXACT, 2.5)
        lo = curve(ax, np.log10(nn), np.clip(0.5 - 1 / np.sqrt(nn), 0, 1), EXACT, 2.5)
        fl = MathTex(r"\tfrac12 \pm \frac{2 \cdot \tfrac12}{\sqrt n}", font_size=30, color=EXACT).move_to([5.2, 1.6, 0])
        txt = label(r"the funnel narrows like $1/\sqrt n$: \ 100 times the tosses, \ 10 times the precision", font_size=24,
                    color=S.ACCENT).to_edge(DOWN, buff=0.35)
        tag = note(r"simulated: 40 sequences of 4,000 fair tosses").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Here's the law at work. <bookmark mark='a'/> Forty people each toss a fair coin four thousand times, "
            "and track the share of heads so far. The horizontal scale is logarithmic. Early on the shares wander "
            "all over the place. <bookmark mark='b'/> Then they're squeezed into a funnel around a half. The gold "
            "lines are two standard deviations of the share, one over root n either side. <bookmark mark='c'/> The "
            "funnel narrows like one over root n: to be ten times more precise, toss a hundred times as often. That "
            "square root is the exchange rate of all of statistics."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in lines], lag_ratio=0.03), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(hi), Create(lo), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(txt))
        self.clear_scene()

    def no_compensation(self):
        d = load("paths")
        steps, means = np.asarray(d["steps"], float), np.asarray(d["means"])
        excess = (means - 0.5) * steps
        A = axes([0, 4000], [-80, 80], x_length=8.6, y_length=4.4, xlabel=r"number of tosses, $n$",
                 ylabel=r"heads minus $n/2$", xticks=[0, 1000, 2000, 3000, 4000], yticks=[-80, -40, 0, 40, 80],
                 center=[-1.4, -0.4, 0])
        ax = A.ax
        lines = VGroup(*[polyline(ax, steps, e, SIM, 1.4, 0.55) for e in excess[:20]])
        nn = np.linspace(1, 4000, 200)
        hi = curve(ax, nn, np.sqrt(nn) / 2, EXACT, 2.5)
        lo = curve(ax, nn, -np.sqrt(nn) / 2, EXACT, 2.5)
        rows = VGroup(label(r"the \emph{share} of heads converges;", font_size=26),
                      label(r"the \emph{count} of extra heads does not:", font_size=26),
                      label(r"it typically grows like $\sqrt n / 2$", font_size=26, color=EXACT),
                      label(r"no force evens things out: \ the gambler's fallacy", font_size=26, color=BOUND))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.9, 1.0, 0])
        for r in rows:
            if r.width > 3.9:
                r.width = 3.9
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.9, 1.0, 0])  # re-align after clamping
        tag = note(r"simulated: 20 of the 40 sequences").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now a trap. If the share of heads is drawn to a half, surely a run of tails must be made up by extra "
            "heads later? <bookmark mark='a'/> Plot not the share but the count: heads minus half the tosses. "
            "<bookmark mark='b'/> It is not forced to compensate for earlier tosses. It can return to zero, and for a fair coin does so infinitely often; yet at a fixed large n its typical size is about "
            "root n over two, the gold curves. <bookmark mark='c'/> The share converges only because the wandering "
            "count is divided by n, which grows faster. The coin has no memory and owes you nothing. Believing it "
            "does is the gambler's fallacy, and the law of large numbers gives it no support at all."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in lines], lag_ratio=0.05), run_time=3.5)
            vo.wait_until("b")
            self.play(Create(hi), Create(lo), FadeIn(rows[:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bernoulli(self):
        tl = timeline(lit=(1713,)).to_edge(UP, buff=0.35)
        hc = history_card(1713, r"Jacob Bernoulli, \ \emph{Ars Conjectandi} \ (published posthumously)",
                          r"Part IV: \ the ``golden theorem'': \ with enough draws from an urn, the observed share is "
                          r"\emph{morally certain} to be near the true one", color=S.MUSEUM, width=7.6, font_size=24)
        hc.move_to([0, 1.1, 0])
        urn = VGroup(RoundedRectangle(width=1.8, height=2.0, corner_radius=0.3, stroke_color=GREY_B, stroke_width=2))
        for k in range(5):
            urn.add(Dot([(k - 2) * 0.3, -0.4 + 0.25 * (k % 2), 0], radius=0.12, color=WHITE if k < 3 else GREY_D))
        urn.move_to([-4.6, -1.8, 0])
        rows = VGroup(
            label(r"3 white to 2 black: \ $p = 3/5$", font_size=26),
            label(r"within $1/50$ of $3/5$, \ with odds of $1000$ to $1$", font_size=26),
            MathTex(r"n = 25{,}550 \text{ draws}", font_size=36, color=S.MUSEUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([1.0, -1.8, 0])
        with self.voiceover(
            "The first proof of a law of large numbers is far older than Chebyshev's. <bookmark mark='a'/> Jacob "
            "Bernoulli worked on it for twenty years, and it was published in 1713, eight years after his death, in "
            "his Art of Conjecturing. He called it his golden theorem. <bookmark mark='b'/> His example: an urn with "
            "three white tokens to every two black. How many draws, with replacement, before you're morally certain, "
            "which he took to mean odds of a thousand to one, that the observed share is within a fiftieth of three "
            "fifths? <bookmark mark='c'/> His answer: twenty-five thousand five hundred and fifty. It was an "
            "enormous number for the time; historians have wondered whether it is why he left the book unfinished."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(urn), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def compare(self):
        d = load("bernoulli")
        items = [("Chebyshev (1867)", d["chebyshev"], BOUND), ("Bernoulli (1713)", d["bernoulli"], S.MUSEUM),
                 ("Hoeffding (1963)", d["hoeffding"], S.PRIOR), ("normal approximation", d["normal"], EXACT),
                 ("exact binomial", d["exact"], S.LIK)]
        A = axes([3, 6], [0, 5], x_length=7.6, y_length=4.6, xlabel=r"draws needed (log scale)", xticks=[3, 4, 5, 6],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[0.8, -0.6, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, (nm, v, c) in enumerate(items):
            y = 4.4 - i
            lo, hi = ax.c2p(3, y - 0.3), ax.c2p(np.log10(v), y + 0.3)
            r = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=c, fill_opacity=0.8)
            r.move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0])
            bars.add(r)
            labs.add(label(nm, font_size=24, color=c).next_to(ax.c2p(3, y), LEFT, buff=0.2))
            vals.add(MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=26, color=c).next_to(r, RIGHT, buff=0.12))
        head = label(r"draws for $|\hat p - 3/5| \le 1/50$ \ with probability $1000/1001$", font_size=28).to_edge(UP, buff=0.5)
        note_ = label(rf"the exact count is {d['exact']:,} (first reached at {d['exact_first']:,}, \ then held from {d['exact']:,} on)",
                      font_size=20, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How good was his answer? <bookmark mark='a'/> Chebyshev's inequality, applied to the same question, "
            "asks for six hundred thousand draws, worse than Bernoulli by a factor of twenty-three. "
            "<bookmark mark='b'/> Bernoulli's own bound, twenty-five thousand five hundred and fifty, was cleverer: "
            "he bounded the binomial tails directly. <bookmark mark='c'/> Wassily Hoeffding's inequality of 1963, "
            "which we meet in chapter eleven, needs nine and a half thousand. <bookmark mark='d'/> The normal "
            f"approximation says about {int(d['normal']):,}, <bookmark mark='e'/> and summing the binomial exactly, "
            f"{d['exact']:,} is enough. Bernoulli was four times too cautious, but his number was a proof, and "
            "the approximation is not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]), FadeIn(vals[k]))
            self.play(FadeIn(note_))
        self.clear_scene()
