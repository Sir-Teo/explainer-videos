from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class Lindley(VoiceoverScene):
    def construct(self):
        self.card()
        self.pear()
        self.two_answers()
        self.why()
        self.growth()
        self.bound()
        self.lessons()

    def card(self):
        card = chapter_card(7, r"Lindley's paradox", r"Significant, \ and evidence for the null", lit=(1957,), part=PART)
        with self.voiceover("Chapter seven. Lindley's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pear(self):
        d = load("lindley")
        hc = history_card(1987, r"Princeton Engineering Anomalies Research",
                          r"operators sat before an electronic random event generator and tried, \ by intention alone, \ to "
                          r"push its output towards 1. \ Over years of sessions the machine produced 104,490,000 binary "
                          r"events.", color=PATH, width=11.0, font_size=23).move_to([0, 1.4, 0])
        rows = fit_rows(VGroup(
            label(rf"successes: \ {d['s']:,} \ of \ {d['n']:,}", font_size=26),
            label(rf"proportion: \ {d['phat']:.7f}", font_size=26, color=PATH),
            label(r"chance alone: \ 0.5", font_size=26, color=GREY_A),
        ), 12.0, 0.3, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> At Princeton in the 1980s, the Engineering Anomalies Research laboratory sat volunteers in "
            "front of an electronic random event generator and asked them to push its output towards ones, by intention "
            "alone. Over years of sessions the machine produced a hundred and four million, four hundred and ninety thousand "
            "binary events. <bookmark mark='b'/> The share of ones was point five zero zero one seven seven, <bookmark mark='c'/> "
            "against the point five that chance predicts."
        ) as vo:
            self.add(pear_tag())
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def two_answers(self):
        d = load("lindley")
        rows = [
            cmath(r"z", r"=", rf"\frac{{s - n/2}}{{\sqrt{{n/4}}}} = {d['z']:.2f}", font_size=32),
            cmath(r"p", r"=", rf"{d['p']:.4f}: \ \text{{reject chance, \ emphatically}}", font_size=30),
            cmath(r"BF_{01}", r"=", rf"\frac{{\binom{{n}}{{s}} 2^{{-n}}}}{{1/(n + 1)}} = {d['bf01']:.1f}", font_size=30),
            cmath(r"P(H_0 \mid y)", r"=", rf"{d['post_h0']:.2f} \ \text{{from even prior odds}}", font_size=30),
        ]
        rows[1][2].set_color(RES)
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"the binomial's normal approximation"), why(r"two-sided"),
                why(r"Jefferys (1990): \ uniform prior on $p$ under $H_1$"), why(r"the same data favour the null 12 to 1")]
        with self.voiceover(
            "<bookmark mark='a'/> The significance test. The excess of ones is three point six one standard errors above "
            "chance. <bookmark mark='b'/> A two-sided p-value of point oh oh oh three: reject chance, emphatically. "
            "<bookmark mark='c'/> The Bayesian test, as William Jefferys computed it in 1990: under the alternative, let the "
            "machine's true proportion be anything between zero and one, uniformly. The Bayes factor is twelve, in favour of "
            "the null. <bookmark mark='d'/> Starting from even odds, the probability that the operators did nothing is "
            "point nine two. The same data, overwhelming evidence against the null by one reckoning, twelve to one for it by "
            "another."
        ) as vo:
            self.add(pear_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why(self):
        A = axes([0.4995, 0.5005], [0, 1.1], x_length=8.6, y_length=4.2, xlabel=r"the machine's proportion $p$",
                 ylabel=r"scaled", xticks=[0.4995, 0.5, 0.5005], yticks=[], center=[-1.6, 0.3, 0],
                 xfmt=lambda v: f"{v:.4f}")
        ax = A.ax
        d = load("lindley")
        se = 0.5 / np.sqrt(d["n"])
        xs = np.linspace(0.4995, 0.5005, 400)
        like = np.exp(-0.5 * ((xs - d["phat"]) / se) ** 2)
        lc = curve(ax, xs, like, LIKE, 3.5)
        null = Line(ax.c2p(0.5, 0), ax.c2p(0.5, 1.05), color=TRUE, stroke_width=4)
        unif = Line(ax.c2p(0.4995, 0.05), ax.c2p(0.5005, 0.05), color=PRIOR, stroke_width=4)
        rows = fit_rows(VGroup(
            label(r"green: \ the likelihood, \ SE 0.00005", font_size=22, color=LIKE),
            label(r"gold: \ $H_0$ puts all its mass at 0.5", font_size=22, color=TRUE),
            label(r"purple: \ $H_1$ spreads its mass over $[0, 1]$", font_size=22, color=PRIOR),
            label(r"only about 2 parts in 10{,}000 of it land under the likelihood", font_size=22, color=RES),
            label(r"$H_0$ predicted the data better than $H_1$ did", font_size=22, color=SHRUNK),
        ), 3.8, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why? With a hundred million trials, the likelihood is extremely narrow, a few ten-thousandths "
            "wide around point five zero zero one eight. <bookmark mark='b'/> The null puts all its probability at exactly a "
            "half, close by: near the likelihood's edge, but near it. <bookmark mark='c'/> The alternative spreads its "
            "probability over every proportion from zero to one, <bookmark mark='d'/> so only a couple of parts in ten "
            "thousand of it fall anywhere near the data. <bookmark mark='e'/> Judged as predictions, the null did far better: it "
            "said 'very close to a half', and that is what happened. The alternative said 'anything at all'."
        ) as vo:
            self.add(pear_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(lc), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(null), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(unif), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def growth(self):
        d = load("lindley")
        ns, bf = np.asarray(d["ns"]), np.asarray(d["bf_n"])
        A = axes([1, 8], [-1, 3], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$ \ (log scale)", ylabel=r"$BF_{01}$ at $p = 0.05$ \ (log scale)",
                 xticks=[1, 2, 3, 4, 5, 6, 7, 8], yticks=[-1, 0, 1, 2, 3], xfmt=lambda v: f"10^{{{int(v)}}}",
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        c = curve(ax, np.log10(ns), np.log10(bf), SHRUNK, 3.5)
        one = DashedLine(ax.c2p(1, 0), ax.c2p(8, 0), color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"hold the result at exactly $p = 0.05$ \ ($z = 1.96$)", font_size=22),
            label(r"let $n$ grow; \ $H_1$: \ $\mu \sim N(0, \sigma^2)$", font_size=22, color=GREY_A),
            label(r"$BF_{01} \approx \sqrt n\, e^{-1.92}$: \ grows without bound", font_size=22, color=SHRUNK),
            label(r"Lindley (1957): \ with enough data, \ `significant' favours $H_0$", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Dennis Lindley's 1957 paper made the point in general. Hold the test result fixed at "
            "exactly p equals point oh five, <bookmark mark='b'/> and let the sample size grow, with a fixed normal prior "
            "under the alternative. <bookmark mark='c'/> The Bayes factor for the null grows like the square root of n, "
            "without bound. <bookmark mark='d'/> At ten observations a p of point oh five mildly favours the alternative; "
            "by a thousand it favours the null; by ten million, hundreds to one. A fixed significance level means very "
            "different evidence at different sample sizes."
        ) as vo:
            self.play(FadeIn(A), Create(one))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bound(self):
        d = load("lindley")
        hdr = [r"\textbf{$p$-value}", r"\textbf{$BF_{01}$ at least}", r"\textbf{$P(H_0 \mid y)$ at least}"]
        body = [[f"{p:g}", f"{b:.3f}", f"{m:.2f}"] for p, b, m in zip(d["ps"], d["sbb"], d["min_post"])]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[2].set_color(RES)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"Sellke, Bayarri \& Berger (2001): \ $BF_{01} \ge -e\,p\log p$ \ over a wide class of alternatives", font_size=22),
            label(r"even the most favourable prior leaves $p = 0.05$ with a 29\% chance the null is true", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Could a cleverer prior rescue the p-value? Thomas Sellke, Susie Bayarri and James Berger "
            "found a bound over a wide class of alternatives: the Bayes factor for the null is at least minus e times p times "
            "log p. <bookmark mark='b'/> A p-value of point oh five gives a Bayes factor of at least point four one, so from "
            "even odds the null keeps at least a twenty-nine percent chance. Point oh one leaves at least eleven percent; "
            "point oh oh one, about two percent. <bookmark mark='c'/> 'Significant at five percent' is much weaker evidence "
            "than the words suggest; this is one reason behind the 2016 statement of the American Statistical Association "
            "that Part 10 described."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(foot[0]), FadeIn(tb[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"the two answers ask different questions", font_size=24, color=PATH),
            label(r"$p$: \ is the data surprising if $H_0$ is exactly true?", font_size=24, color=RES),
            label(r"BF: \ which hypothesis predicted the data better?", font_size=24, color=SHRUNK),
            label(r"PEAR: \ a real but tiny bias, \ $1.8 \times 10^{-4}$, \ is also possible: \ machines drift", font_size=24),
            label(r"so report the size of the effect, \ always", font_size=24, color=HIT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Neither answer is a mistake; they answer different questions. <bookmark mark='b'/> The "
            "p-value asks whether the data would be surprising if the null were exactly true. <bookmark mark='c'/> The Bayes "
            "factor asks which hypothesis predicted the data better, and depends on what the alternative predicted. "
            "<bookmark mark='d'/> For PEAR, both readings are compatible with a third story: a real but tiny bias, two "
            "parts in ten thousand, that could come from the equipment rather than the operators. <bookmark mark='e'/> Which "
            "is why the size of an effect, with its interval, should always be reported alongside any test."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
