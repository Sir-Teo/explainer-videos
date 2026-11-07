from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class GlivenkoCantelli(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.sequences()
        self.symmetrization()
        self.chart()
        self.finite()

    def card(self):
        card = chapter_card(1, r"Glivenko--Cantelli classes", r"A law of large numbers for a whole class at once", lit=(1933,), part=PART)
        with self.voiceover("Chapter one. Glivenko–Cantelli classes: a law of large numbers for a whole class at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\|P_n - P\|_{\mathcal F}", r"=", r"\sup_{f \in \mathcal F} |P_n f - P f|", font_size=36),
            cmath(r"\mathcal F \text{ is Glivenko--Cantelli}", r":", r"\|P_n - P\|_{\mathcal F} \to 0 \ \text{almost surely}", font_size=32),
            cmath(r"\{\mathbf 1\{\cdot \le t\}\}", r":", r"\sup_t |F_n(t) - F(t)| \to 0 \ \text{a.s.}", font_size=34),
            cmath(r"\{\mathbf 1_A : A \text{ finite}\}", r":", r"\sup_A |P_n(A) - P(A)| = 1 \ \text{always}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"the sup over the class"), why(r"the definition"), why(r"Glivenko, \ Cantelli (1933)"), why(r"take $A$ = the sample")]
        heading = label('Uniform convergence is a property of the entire function class', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Write P n f for the sample average of f and P f for its true mean, and take the largest gap "
            "between them over a class of functions F. <bookmark mark='b'/> The class is called Glivenko–Cantelli if that "
            "largest gap goes to zero almost surely: a law of large numbers holding uniformly over the class. <bookmark "
            "mark='c'/> The class of indicators of half-lines is the original example. Valery Glivenko and Francesco "
            "Cantelli proved in 1933 that the empirical distribution function converges to the true one uniformly. "
            "<bookmark mark='d'/> But not every class works. Take indicators of all finite sets. For continuous data the "
            "true probability of any finite set is zero, while the sample itself is a finite set with empirical probability "
            "one. The gap is one, always. The class is too rich: it can fit any sample exactly."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sequences(self):
        d = load("gc")
        cp = np.log10(np.asarray(d["checkpoints"], float))
        A = axes([0, 3.7], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\sup_t |F_n(t) - t|$",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = [EMPC, S.ALT, S.PRIOR]
        cs = [clip_curve(ax, cp, d["seqs"][str(s)], c, 3, ymin=0, ymax=1) for s, c in enumerate(cols)]
        nn = np.logspace(0.3, 3.7, 100)
        env = polyline(ax, np.log10(nn), np.sqrt(np.log(np.log(nn) + 1.0) / (2 * nn)) * 1.2, BOUNDC, 2.5)
        side = fit_rows(VGroup(
            label(r"three sequences of uniform draws", font_size=22),
            label(r"each line: \ one sample path of $D_n$", font_size=22, color=EMPC),
            label(r"all tend to 0: \ almost sure convergence", font_size=22, color=GOODC),
            label(r"purple: \ a $\sqrt{\log\log n / n}$ envelope", font_size=22, color=BOUNDC),
            label(r"Chung (1949): \ the LIL for $D_n$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the theorem happening. Three long sequences of uniform draws. <bookmark mark='b'/> "
            "For each, follow the largest gap as the sample grows from one to five thousand. <bookmark mark='c'/> Every path "
            "goes to zero: almost sure convergence, path by path, not just in probability. <bookmark mark='d'/> The paths "
            "shrink at about the rate of root log log n over n, <bookmark mark='e'/> which is Kai Lai Chung's law of the "
            "iterated logarithm for this statistic, from Part forty-four's family of results."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(c) for c in cs], FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(env), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def symmetrization(self):
        rows = [
            cmath(r"E\|P_n - P\|_{\mathcal F}", r"\le", r"E\|P_n - P_n'\|_{\mathcal F}", font_size=36),
            cmath(r"P_n f - P_n' f", r"=", r"\tfrac1n \textstyle\sum_i (f(X_i) - f(X_i')) \overset{d}{=} \tfrac1n \sum_i \varepsilon_i (f(X_i) - f(X_i'))", font_size=30),
            cmath(r"E\|P_n - P\|_{\mathcal F}", r"\le", r"2\,E \sup_f \big|\tfrac1n \textstyle\sum_i \varepsilon_i f(X_i)\big| = 2\,\mathcal R_n(\mathcal F)", font_size=32),
            cmath(r"\text{conditionally on the } X_i", r":", r"\text{for indicators: finitely many binary patterns } (f(X_1), \dots, f(X_n))", font_size=28),
        ]
        rows[2][-1].set_color(CLASSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a ghost sample $X'$, \ Jensen"), why(r"swapping $X_i \leftrightarrow X_i'$: \ random signs"), why(r"the Rademacher average"), why(r"the key reduction")]
        heading = label('A ghost sample turns sampling error into random-sign complexity', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> How is such a theorem proved? By symmetrization, an idea that goes back to Vapnik and Chervonenkis in 1971. Introduce a ghost sample, an independent copy of the data. By Jensen's inequality the expected gap is at most the expected gap between the two empirical measures. <bookmark mark='b'/> Now the difference for each i is symmetric: swapping X i with its ghost changes nothing in law. So we may multiply each term by an independent random sign. <bookmark mark='c'/> Splitting the two halves, the expected gap is at most twice the Rademacher average of the class: the expected largest correlation between the class and pure noise. <bookmark mark='d'/> The gain is that, with the data held fixed, the supremum is over the finite set of patterns the class can produce on the sample. For indicator classes there are at most two to the n binary patterns. Real-valued classes can have infinitely many sample vectors and need metric approximations instead."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("gc")
        ln = np.log10(np.asarray(d["ns"], float))
        A = axes([0.9, 3.4], [-1.9, 0], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$",
                 xticks=[1, 2, 3], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-1.5, -1, -0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        ce = VGroup(polyline(ax, ln, np.log10(d["ed"]), EMPC, 4), *[Dot(ax.c2p(a, np.log10(b)), radius=0.08, color=EMPC) for a, b in zip(ln, d["ed"])])
        cr = VGroup(polyline(ax, ln, np.log10(d["two_rad"]), CLASSC, 4), *[Dot(ax.c2p(a, np.log10(b)), radius=0.08, color=CLASSC) for a, b in zip(ln, d["two_rad"])])
        i = d["ns"].index(1000)
        side = fit_rows(VGroup(
            label(r"half-lines, \ uniform data", font_size=22),
            label(rf"blue: \ $E\,D_n$, \ simulated; \ {d['ed'][i]:.4f} at $n$ = 1,000", font_size=22, color=EMPC),
            label(rf"gold: \ $2\mathcal R_n$, \ exact: \ {d['two_rad'][i]:.4f}", font_size=22, color=CLASSC),
            label(r"slope $-1/2$: \ both are $\asymp 1/\sqrt n$", font_size=22, color=GOODC),
            label(r"$\sqrt n\,E D_n \to \sqrt{\pi/2}\log 2 = 0.869$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> For half-lines the Rademacher average can be computed exactly. With the data sorted, the patterns are the n plus one prefixes, so the supremum is the largest partial sum of n random signs, a random walk's maximum, which a killed-walk spectral sum evaluates without simulation. <bookmark mark='b'/> In blue, the expected Kolmogorov distance, simulated: at a thousand observations, {say(d['ed'][i], 3)}. <bookmark mark='c'/> In gold, twice the Rademacher average: {say(d['two_rad'][i], 3)}, above it as promised. <bookmark mark='d'/> On log scales both are straight lines of slope minus a half: the uniform law holds at the root n rate. <bookmark mark='e'/> And root n times the expected distance converges to the mean of Kolmogorov's law, root pi over two times log two."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"blue simulated; \ gold exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cr), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def finite(self):
        rows = [
            cmath(r"|\mathcal F| = k, \ |f| \le 1", r":", r"\mathcal R_n(\mathcal F) \le \sqrt{2 \log(2k) / n}", font_size=34),
            cmath(r"\text{indicator class: at most } \Pi(n) \text{ patterns}", r":", r"\mathcal R_n \le \sqrt{2 \log(2\Pi(n)) / n}", font_size=34),
            cmath(r"\Pi(n) \text{ polynomial}", r"\Rightarrow", r"E\|P_n - P\|_{\mathcal F} \lesssim \sqrt{\log n / n} \to 0", font_size=32),
            cmath(r"\Pi(n) = 2^n", r"\Rightarrow", r"\text{this bound need not vanish}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"Massart's finite-class lemma"), why(r"conditionally on the sample"), why(r"then a.s., \ by concentration"), why(r"the finite sets")]
        heading = label('Finite indicator patterns yield a uniform law', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> To bound the Rademacher average of a finite class, Pascal Massart's lemma: for k functions bounded by one it is at most the root of two log two k over n. The price of k candidates is only logarithmic. <bookmark mark='b'/> Conditionally on the sample, an indicator class has finitely many binary patterns. If there are at most pi of n patterns on n points, the same bound holds with pi of n in place of k. <bookmark mark='c'/> So if the number of patterns grows only polynomially in n, the expected gap is of order root log n over n, and the class is Glivenko–Cantelli. <bookmark mark='d'/> If it grows like two to the n, every labelling is possible, the class can fit noise, and this counting bound need not tend to zero. Infinite VC dimension alone does not imply failure for every fixed distribution. Counting patterns is the subject of chapter two."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
