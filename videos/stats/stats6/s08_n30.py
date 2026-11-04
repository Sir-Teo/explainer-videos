from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Thirty(VoiceoverScene):
    def construct(self):
        self.card()
        self.folklore()
        self.incomes()
        self.coverage()
        self.berry_esseen()
        self.lesson()

    def card(self):
        card = chapter_card(7, r"Is thirty enough?", r"How fast the bell arrives", part=PART)
        with self.voiceover("Chapter seven. Is thirty enough?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def panel(self, d, key, n, cx, color, title):
        ed = np.asarray(d["edges"])
        A = axes([-4, 4], [0, 0.62], x_length=3.8, y_length=2.6, xticks=[-2, 0, 2], center=[cx, -0.9, 0])
        h = hist_bars(A.ax, ed, np.clip(np.asarray(d[key][str(n)]["hist"]), 0, 0.62), color=color, opacity=0.75)
        xs = np.linspace(-4, 4, 200)
        cv = curve(A.ax, xs, normal_pdf(xs), EXACT, 2.5)
        t = MathTex(rf"n = {n}", font_size=30).next_to(A, UP, buff=0.15)
        s = MathTex(rf"\sup|F - \Phi| = {d[key][str(n)]['sup']:.3f}", font_size=22, color=GREY_A).next_to(A, DOWN, buff=0.15)
        return VGroup(A, h, cv, t, s), title

    def folklore(self):
        d = load("n30")
        panels = VGroup(*[self.panel(d, "height", n, -4.4 + 4.4 * k, S.EST, "")[0] for k, n in enumerate((5, 30, 300))])
        head = label(r"standardized means of $n$ of the World's adult heights", font_size=28).to_edge(UP, buff=0.5)
        folk = label(r"the folklore: \ ``with $n \ge 30$ the sample mean is normal''", font_size=26, color=S.ACCENT)
        folk.next_to(head, DOWN, buff=0.35)
        tag = note(r"simulated: 20,000 samples of each size from the World").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Every introductory course has a rule: once the sample has thirty observations, you may treat its mean "
            "as normal. <bookmark mark='a'/> Where does thirty come from? Nobody quite knows; one story is that printed "
            "tables of Student's t stopped at thirty degrees of freedom. Let's test it. <bookmark mark='b'/> Draw samples of the World's "
            "adult heights, of five, thirty and three hundred people, twenty thousand samples of each, and "
            "standardize the means. Heights are close to normal already, so even at five the means are "
            "indistinguishable from the bell: the largest gap between the CDFs is under one percent. For heights, "
            "thirty is generous."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(folk))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.3), run_time=2.5)
        self.clear_scene()

    def incomes(self):
        d = load("n30")
        panels = VGroup(*[self.panel(d, "income", n, -4.4 + 4.4 * k, WORLD, "")[0] for k, n in enumerate((5, 30, 1000))])
        head = label(r"standardized means of $n$ of the World's incomes", font_size=28).to_edge(UP, buff=0.5)
        facts = label(rf"skewness of one income: \ {d['skew_income']:.0f}; \ the top 1\% earn {100 * d['top_share']:.1f}\% of all "
                      r"income; \ a Pareto tail with $\alpha = 2.1$", font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.3)
        if facts.width > 12.8:
            facts.width = 12.8
        tag = simulated_tag(r"simulated: 20,000 samples of each size from the World")
        with self.voiceover(
            "Now do the same with incomes. <bookmark mark='a'/> The World's incomes are far from normal: a skewed "
            "body and a Pareto tail, so that the top one percent earn about a fifteenth of all the income. "
            "<bookmark mark='b'/> With five people, the means are piled on the left, with a long tail to the right: "
            "most samples miss the rare high earners, and a few catch one. <bookmark mark='c'/> With thirty, it's "
            "hardly better. <bookmark mark='d'/> Even with a thousand people the histogram still leans, and the gap "
            "between the CDFs is still nearly seven percent. The central limit theorem holds, since the variance is "
            "finite; it's just very slow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(facts))
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k]))
        self.clear_scene()

    def coverage(self):
        d = load("n30")
        ns = d["ns"]
        A = axes([0.5, 3.2], [0.8, 1.0], x_length=7.0, y_length=4.4, xlabel=r"sample size $n$ (log scale)",
                 ylabel=r"coverage of the nominal 95\% $t$-interval", xticks=[1, 2, 3], yticks=[0.8, 0.85, 0.9, 0.95, 1.0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.4, -0.4, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0.5, 0.95), ax.c2p(3.2, 0.95), color=GREY_B, stroke_width=1.5)
        lines = VGroup()
        for key, c in (("height", S.EST), ("lognormal", S.PRIOR), ("income", WORLD)):
            ys = [d[key][str(n)]["cover"] for n in ns]
            lines.add(VGroup(polyline(ax, np.log10(ns), ys, c, 3),
                             *[Dot(ax.c2p(np.log10(n), y), radius=0.06, color=c) for n, y in zip(ns, ys)]))
        leg = legend([(S.EST, r"heights"), (S.PRIOR, r"lognormal, \ $\sigma = 0.55$"), (WORLD, r"the World's incomes")],
                     font_size=22).move_to([4.4, 1.9, 0])
        inc = d["income"]
        rows = VGroup(
            MathTex(rf"n = 30:\ \ {100 * inc['30']['cover']:.1f}\%", font_size=28, color=WORLD),
            MathTex(rf"n = 1000:\ \ {100 * inc['1000']['cover']:.1f}\%", font_size=28, color=WORLD),
            label(rf"misses: \ {100 * inc['30']['miss_lo']:.1f}\% too low, \ {100 * inc['30']['miss_hi']:.1f}\% too high (at $n = 30$)",
                  font_size=22, color=GREY_A),
            label(r"the interval is usually too low: \ the sample has missed the top earners", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r in rows:
            if r.width > 5.2:
                r.width = 5.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.3, -0.6, 0])
        tag = simulated_tag(r"simulated: 20,000 samples of each size")
        with self.voiceover(
            "What does this do to a confidence interval? Part 11 will build them properly; for now take the usual "
            "one, the mean plus or minus about two standard errors, which promises ninety-five percent. "
            "<bookmark mark='a'/> For heights the promise is kept at every sample size. <bookmark mark='b'/> For a "
            "lognormal with the World's spread, it's a little short for small samples and fine by a hundred. "
            "<bookmark mark='c'/> For the World's incomes, the interval covers the true mean only "
            f"{100 * inc['30']['cover']:.0f} percent of the time with thirty people, and "
            f"{100 * inc['1000']['cover']:.0f} percent with a thousand. <bookmark mark='d'/> And the misses are lopsided: "
            "nearly always the interval is too low, because the sample has missed the rare high incomes that pull "
            "the true mean up."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(Create(lines[k]), FadeIn(leg[k]))
            self.play(FadeIn(rows[:2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def berry_esseen(self):
        d = load("n30")
        ns = np.asarray(d["ns"], float)
        thm = theorem_card(r"Berry--Esseen", r"if $\rho = E|X - \mu|^3 < \infty$: \ $\sup_x |F_n(x) - \Phi(x)| \le C\,\dfrac{\rho}{\sigma^3\sqrt n}$, "
                           r"\ with $C \le 0.4748$", who=r"Berry 1941, \ Esseen 1942; \ the constant, Shevtsova 2011", color=BOUND,
                           width=6.4, font_size=22).move_to([3.6, 2.2, 0])
        A = axes([0.5, 3.2], [-3.2, 0], x_length=6.0, y_length=4.4, xlabel=r"$n$ (log scale)",
                 ylabel=r"$\sup|F_n - \Phi|$ (log scale)", xticks=[1, 2, 3], yticks=[-3, -2, -1, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", center=[-3.0, -0.6, 0])
        ax = A.ax
        be = VGroup(polyline(ax, np.log10(ns), np.log10(d["be"]), BOUND, 3))
        ln = VGroup(polyline(ax, np.log10(ns), np.log10([d["lognormal"][str(int(n))]["sup"] for n in ns]), S.PRIOR, 3))
        inc = VGroup(polyline(ax, np.log10(ns), np.log10([d["income"][str(int(n))]["sup"] for n in ns]), WORLD, 3))
        leg = legend([(BOUND, r"the bound, \ for the lognormal"), (S.PRIOR, r"the lognormal, \ simulated"),
                      (WORLD, r"incomes: \ $\rho = \infty$, \ no bound")], font_size=22).move_to([3.7, -0.4, 0])
        rows = VGroup(label(r"a guarantee for every $n$, \ but a cautious one", font_size=24, color=GREY_A),
                      label(r"the World's incomes have no third moment: \ the theorem says nothing", font_size=24, color=WORLD))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, -2.3, 0])
        for r in rows:
            if r.width > 6.0:
                r.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, -2.3, 0])
        with self.voiceover(
            "Is there a guarantee? <bookmark mark='a'/> Yes, if the third absolute moment is finite: the "
            "Berry–Esseen theorem, proved by Andrew Berry in 1941 and Carl-Gustav Esseen in 1942. The gap between "
            "the CDFs is at most a constant times the third absolute moment over sigma cubed, over root n. Irina "
            "Shevtsova showed in 2011 that the constant can be taken below point four eight. <bookmark mark='b'/> For "
            "the lognormal, the bound, in red, falls like one over root n. <bookmark mark='c'/> The truth, in purple, "
            "is far below it: the bound is safe but cautious. <bookmark mark='d'/> For the World's incomes, whose "
            "Pareto tail makes the third moment infinite, the theorem offers nothing at all, and the green curve "
            "crawls down at its own slow pace."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(be), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(leg[1]), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(Create(inc), FadeIn(leg[2]), FadeIn(rows[1]))
        self.clear_scene()

    def lesson(self):
        d = load("n30")
        rows = [
            cmath(r"\text{skewness}(\bar X_n)", r"=", r"\frac{\text{skewness}(X)}{\sqrt n}", font_size=34),
            cmath(r"\text{heights: }\ \frac{0.0}{\sqrt n},\qquad \text{lognormal: }\ \frac{" + f"{d['skew_ln']:.1f}" + r"}{\sqrt n}",
                  r"\quad", r"\text{incomes: }\ \frac{" + f"{d['skew_income']:.0f}" + r"\,(\text{sample})}{\sqrt n}", font_size=30),
        ]
        rows[0][2].set_color(S.ACCENT)
        whys = [why(r"chapter four's cumulants"), why(r"to make it $0.2$, \ $n$ must be $(\text{skewness}/0.2)^2$")]
        recs = VGroup(label(r"no magic number: \ how fast depends on the skewness and the tails", font_size=26, color=S.ACCENT),
                      label(r"for skewed data: \ transform (Part 1's logarithms), \ resample (the bootstrap, Part 16), \ "
                            r"or model the tail (chapter 12)", font_size=22, color=GREY_A),
                      label(r"a heavy tail is a warning: \ the sample may not have seen it yet", font_size=22, color=GREY_A))
        recs.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        for r in recs:
            if r.width > 12.6:
                r.width = 12.6
        recs.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So what's the right rule? <bookmark mark='a'/> Chapter four told us: the skewness of the mean is the "
            "skewness of one observation divided by root n. <bookmark mark='b'/> Heights have none to speak of. The "
            "lognormal's is about two, so a few dozen observations bring it down to a third. The World's incomes "
            "have a sample skewness in the seventies, and since their third moment is infinite, even that number is "
            "an underestimate that grows with the sample. <bookmark mark='c'/> There is no magic number. For "
            "skewed data, transform first, as Part 1 did with logarithms; or resample, with the bootstrap of Part "
            "16; or model the tail directly, as chapter twelve begins to. And remember that a heavy tail is a "
            "warning: your sample may simply not have met it yet."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.9, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in recs], lag_ratio=0.4))
        self.clear_scene()
