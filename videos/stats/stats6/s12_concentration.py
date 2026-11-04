from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Concentration(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.proof()
        self.compare()
        self.union()
        self.large_dev()

    def card(self):
        card = chapter_card(11, r"Concentration", r"Guarantees for every $n$, \ not just in the limit", part=PART)
        with self.voiceover("Chapter eleven. Concentration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        thm = theorem_card(r"Hoeffding's inequality", r"if $X_1, \dots, X_n$ are independent with $a \le X_i \le b$: \ "
                           r"$P\big(|\bar X_n - \mu| \ge \varepsilon\big) \le 2\exp\!\Big(-\dfrac{2n\varepsilon^2}{(b - a)^2}\Big)$",
                           who=r"Wassily Hoeffding, 1963", color=S.PRIOR, width=10.2, font_size=26).move_to([0, 1.6, 0])
        rows = VGroup(label(r"Chebyshev: \ the tail falls like $1/n$", font_size=26, color=BOUND),
                      label(r"the CLT: \ like $e^{-n\varepsilon^2/2\sigma^2}$, \ but only in the limit", font_size=26, color=EXACT),
                      label(r"Hoeffding: \ exponentially, \ for \emph{every} $n$, \ if the variables are bounded", font_size=26,
                            color=S.PRIOR)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.6)
        with self.voiceover(
            "The central limit theorem is a statement about the limit. Chebyshev's inequality holds for every n, but "
            "it's weak. Can we have both: a guarantee at every sample size, as sharp as the normal tail? "
            "<bookmark mark='a'/> For bounded variables, yes. Wassily Hoeffding proved in 1963 that if each variable "
            "lies between a and b, the chance that the mean misses by epsilon is at most twice e to the minus two n "
            "epsilon squared over b minus a squared. <bookmark mark='b'/> Chebyshev's bound falls like one over n. "
            "<bookmark mark='c'/> The normal tail falls exponentially, but the central limit theorem only promises it "
            "eventually. <bookmark mark='d'/> Hoeffding's falls exponentially and holds for every n, with no "
            "approximation at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"P(S_n - ES_n \ge t)", r"\le", r"e^{-\lambda t}\, E\, e^{\lambda(S_n - ES_n)}", r"\quad (\lambda > 0)", font_size=30),
            cmath(r"E\,e^{\lambda(S_n - ES_n)}", r"=", r"\prod_i E\,e^{\lambda(X_i - \mu)}", r"\le",
                  r"e^{n\lambda^2(b - a)^2/8}", font_size=30),
            cmath(r"P(S_n - ES_n \ge t)", r"\le", r"\min_\lambda e^{-\lambda t + n\lambda^2(b-a)^2/8}", r"=",
                  r"e^{-2t^2/n(b - a)^2}", font_size=30),
            cmath(r"t = n\varepsilon:\quad P(\bar X_n - \mu \ge \varepsilon)", r"\le", r"e^{-2n\varepsilon^2/(b - a)^2}", font_size=28),
        ]
        rows[2][4].set_color(S.PRIOR)
        rows[3][2].set_color(S.PRIOR)
        whys = [why(r"Markov, \ applied to $e^{\lambda(S_n - ES_n)}$: \ Chernoff's trick (1952)"),
                why(r"independence; \ then Hoeffding's lemma for one bounded variable"),
                why(r"choose the best $\lambda = 4t/n(b - a)^2$"), why(r"same for the lower tail: \ the 2")]
        with self.voiceover(
            "The proof is Markov's inequality with a twist. <bookmark mark='a'/> Exponentiate first: the event that "
            "the sum exceeds its mean by t is the event that e to the lambda times the excess exceeds e to the "
            "lambda t. Apply Markov to that. This is Herman Chernoff's trick. <bookmark mark='b'/> By independence "
            "the expectation factors into one MGF per variable, and Hoeffding's lemma bounds the MGF of any variable "
            "confined to an interval of width b minus a by e to the lambda squared b minus a squared over eight. "
            "<bookmark mark='c'/> Now choose lambda to make the bound as small as possible: a quadratic in the "
            "exponent, minimized in one line. <bookmark mark='d'/> Put t equal to n epsilon and you have Hoeffding's "
            "inequality, for one tail; double it for both."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.4, buff=0.62, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("hoeffding")
        ns = np.asarray(d["ns"], float)
        A = axes([0, 1000], [-4, 0], x_length=7.4, y_length=4.6, xlabel=r"$n$",
                 ylabel=r"$P(|\hat p - 0.6| \ge 0.05)$ (log scale)", xticks=[0, 250, 500, 750, 1000], yticks=[-4, -3, -2, -1, 0],
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.2, -0.4, 0])
        ax = A.ax
        lines = {}
        for key, c in (("chebyshev", BOUND), ("hoeffding", S.PRIOR), ("clt", EXACT), ("exact", S.LIK)):
            y = np.log10(np.clip(np.asarray(d[key]), 1e-4, 1))
            lines[key] = polyline(ax, ns, y, c, 3)
        leg = legend([(BOUND, r"Chebyshev: \ $pq/n\varepsilon^2$"), (S.PRIOR, r"Hoeffding: \ $2e^{-2n\varepsilon^2}$"),
                      (EXACT, r"normal approximation"), (S.LIK, r"exact binomial")], font_size=22).move_to([4.5, 1.6, 0])
        i = list(ns).index(1000)
        rows = VGroup(MathTex(rf"n = 1000:\ \ \text{{exact}}\ {d['exact'][i]:.4f}", font_size=26, color=S.LIK),
                      MathTex(rf"\text{{Hoeffding}}\ {d['hoeffding'][i]:.4f},\ \ \text{{Chebyshev}}\ {d['chebyshev'][i]:.3f}", font_size=26,
                              color=GREY_A),
                      MathTex(rf"n = 200:\ \text{{simulated}}\ {d['sim200']:.3f}", font_size=24, color=GREY_B))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, -1.2, 0])
        with self.voiceover(
            "Compare them on a coin with p equal to point six, asking for the chance that the sample proportion "
            "misses by five points or more. The scale is logarithmic. <bookmark mark='a'/> Chebyshev's bound "
            "creeps down slowly: a straight line here would mean exponential decay, and its curve flattens. "
            "<bookmark mark='b'/> Hoeffding's is a straight line, falling a factor of ten every four hundred and "
            "sixty tosses. <bookmark mark='c'/> The exact probability, and the normal approximation that tracks it, "
            "fall faster still, because Hoeffding uses only the bounds of the variable, not its variance. "
            "<bookmark mark='d'/> At a thousand tosses: the truth is about one in seven hundred; Hoeffding guarantees "
            "one in seventy-four; Chebyshev, only one in ten."
        ) as vo:
            self.play(FadeIn(A))
            for k, (m, key) in enumerate(zip("abc", ("chebyshev", "hoeffding", "exact"))):
                vo.wait_until(m)
                self.play(Create(lines[key]), FadeIn(leg[[0, 1, 3][k]]))
            self.play(Create(lines["clt"]), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows))
        self.clear_scene()

    def union(self):
        rows = [
            cmath(r"P\big(\text{any of } m \text{ means is off by } \ge \varepsilon\big)", r"\le", r"m \cdot 2e^{-2n\varepsilon^2}",
                  font_size=30),
            cmath(r"\le \delta \quad \text{when}\quad n", r"\ge", r"\frac{\log(2m/\delta)}{2\varepsilon^2}", font_size=32),
            cmath(r"m = 10 \to 10^6:\ \ n", r"=", r"1{,}199 \to 3{,}501", r"\qquad (\varepsilon = 0.05,\ \delta = 0.05)", font_size=30),
        ]
        rows[1][2].set_color(S.PRIOR)
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"the union bound: \ add the failure chances"), why(r"solve for $n$: \ only $\log m$"),
                why(r"a million questions cost less than three times ten")]
        uses = label(r"the engine of learning theory (Part 54), \ bandits and anytime-valid tests (Part 58), \ and every "
                     r"``with high probability'' you will read", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        if uses.width > 12.8:
            uses.width = 12.8
        with self.voiceover(
            "Exponential tails have a remarkable consequence. <bookmark mark='a'/> Suppose you estimate m different "
            "proportions at once, and want all of them right. The chance that any one fails is at most the sum of "
            "the individual chances: m times Hoeffding's bound. <bookmark mark='b'/> To keep that below delta, n "
            "need only grow like the logarithm of m. <bookmark mark='c'/> Ten proportions to within five points, "
            "all at once, with ninety-five percent confidence: twelve hundred observations. A million proportions: "
            "only thirty-five hundred. With Chebyshev's polynomial tail it would be millions. <bookmark mark='d'/> "
            "That logarithm is the engine of machine-learning theory in Part 54, and of every result you'll read "
            "that holds with high probability."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.4, buff=0.9, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(uses))
        self.clear_scene()

    def large_dev(self):
        p = 0.9
        A = axes([0.55, 1.0], [0, 0.6], x_length=6.0, y_length=4.0, xlabel=r"$a$", ylabel=r"rate $I(a)$",
                 xticks=[0.6, 0.7, 0.8, 0.9, 1.0], yticks=[0, 0.2, 0.4, 0.6], center=[-3.2, -0.6, 0])
        ax = A.ax
        a = np.linspace(0.56, 0.995, 200)
        kl = a * np.log(a / p) + (1 - a) * np.log((1 - a) / (1 - p))
        ho = 2 * (a - p) ** 2
        nm = (a - p) ** 2 / (2 * p * (1 - p))
        c1 = curve(ax, a, kl, S.LIK, 3.5)
        c2 = curve(ax, a, ho, S.PRIOR, 3)
        c3 = curve(ax, a, np.clip(nm, 0, 0.6), EXACT, 2.5)
        leg = legend([(S.LIK, r"Cram\'er: \ $\mathrm{KL}(a \,\|\, p)$"), (S.PRIOR, r"Hoeffding: \ $2(a - p)^2$"),
                      (EXACT, r"normal: \ $(a - p)^2/2pq$")], font_size=22).move_to([3.6, 1.8, 0])
        rows = VGroup(MathTex(r"P(\bar X_n \ge a) = e^{-n I(a) + o(n)}", font_size=30),
                      MathTex(r"I(a) = a\log\frac{a}{p} + (1 - a)\log\frac{1 - a}{1 - p}", font_size=28, color=S.LIK),
                      label(r"Harald Cram\'er (1938): \ the exact exponential rate", font_size=22, color=GREY_A),
                      label(r"the Kullback--Leibler divergence appears: \ Part 22", font_size=22, color=GREY_B))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -0.6, 0])
        for r in rows:
            if r.width > 6.0:
                r.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "How fast, exactly, do such tails fall? <bookmark mark='a'/> Harald Cramér answered in 1938. Take a coin "
            "that lands heads nine times in ten. The chance that the share of heads in n tosses reaches a level a "
            "decays like e to the minus n times a rate, I of a. "
            "<bookmark mark='b'/> For coins the rate is this expression, which Part 22 will recognize as the "
            "Kullback–Leibler divergence between a coin with chance a and one with chance p. <bookmark mark='c'/> "
            "Hoeffding's exponent, in purple, sits below it everywhere: a bound must be cautious. The normal "
            "approximation, in gold, matches Cramér's rate near p, but far from it, it's wrong in both directions: "
            "too optimistic below p, too pessimistic above. The central limit theorem describes typical deviations; "
            "large deviations need their own theory."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(leg[0]), FadeIn(rows[1]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(Create(c2), Create(c3), FadeIn(leg[1:]))
        self.clear_scene()
