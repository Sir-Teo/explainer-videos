from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import DOVE, GOOD, HAWK, HURDLE, PART, WORD, fit_right, load

THETA_C = {"0.2": QC.LOSS, "0.5": QC.DELTA, "1.0": QC.GAIN}


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.lemma()
        self.chebyshev()
        self.theorem()
        self.limits(t)
        self.recovery(t)
        self.statements(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Why screening finds the words", r"When does counting co-occurrences with returns recover the "
                          r"sentiment words, and how many documents does it take?", part=PART)
        with self.voiceover("For the researcher: Chapter five's screen kept words whose appearances sided with rising "
                            "yields more often than chance. Why should that find the true sentiment words at all? And how "
                            "many documents does it need? We can answer under explicit generative and asymptotic assumptions, then inspect a finite diagnostic without treating it as a guarantee."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lemma(self):
        rows = [cmath(r"q_j(p)", r"=", r"\Pr(\text{word } j \in \text{article} \mid p) = 1 - \big(1 - p\,O_{+,j} - (1 - p)\,O_{-,j}\big)^{s},\quad j\in S",
                      font_size=28, colors={r"q_j(p)": WORD}),
                cmath(r"f_j", r"\xrightarrow{\ n \to \infty\ }", r"\Pr(y > 0 \mid j \in \text{article}) = \frac{\mathbb E[g(p)\,q_j(p)]}"
                      r"{\mathbb E[q_j(p)]}", font_size=30, colors={r"f_j": HURDLE}),
                cmath(r"j \in N", r"\Rightarrow", r"f_j \to \mathbb E[g(p)] = \pi", font_size=32),
                cmath(r"O_{+,j} > O_{-,j}", r"\Rightarrow", r"q_j \uparrow \text{ in } p\ \Rightarrow\ f_j \to \pi + "
                      r"\frac{\operatorname{Cov}(g(p), q_j(p))}{\mathbb E\,q_j(p)} \ge \pi", font_size=28, colors={r"O_{+,j} > O_{-,j}": HAWK})]
        whys = [why(r"in the model, a charged word appears in an article with probability rising in $p$ if it is a "
                    r"positive word ($O_{+,j} > O_{-,j}$), falling if negative"),
                why(r"by the law of large numbers and Bayes' rule, the screening statistic converges to the chance of a "
                    r"positive return given that the word appears"),
                why(r"a neutral word's appearance is independent of $p$, so it carries no information: its limit is the "
                    r"overall share $\pi$"),
                why(r"the covariance is nonnegative; strict separation additionally needs a strictly concordant pair with positive probability")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Assume independent or suitably ergodic articles, positive word-presence probability, finite expectations, and conditional independence of label sign and word presence given tone. Fix charged-word length, or integrate an independent length law. <bookmark mark='a'/> In SESTM's model, a charged word appears in an "
            "article with a probability q that rises with the article's tone if the word is positive, and falls if it "
            "is negative. <bookmark mark='b'/> As the number of articles grows, the screening statistic converges to "
            "the probability of a positive return given that the word appears: by Bayes' rule, the expectation of g "
            "times q, over the expectation of q. <bookmark mark='c'/> A neutral word's appearance does not depend on "
            "tone, so its limit is just the overall share of positive returns. <bookmark mark='d'/> For a positive "
            "word, the limit exceeds that share by a covariance between two functions of the tone, g and q, both "
            "nondecreasing. Strict separation also needs nondegenerate tone and a product of differences positive with positive probability; otherwise the inequality can be an equality."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def chebyshev(self):
        rows = [cmath(r"\operatorname{Cov}(g(p), q(p))", r"=", r"\tfrac12\,\mathbb E\big[(g(p) - g(p'))(q(p) - q(p'))\big]",
                      font_size=32, colors={r"\operatorname{Cov}(g(p), q(p))": HURDLE}),
                cmath(r"(g(p) - g(p'))(q(p) - q(p'))", r"\ge", r"0 \quad \text{for all } p, p'", font_size=32),
                cmath(r"\lim f_j", r":", r"\ge\pi\ (q_j\uparrow),\quad \le\pi\ (q_j\downarrow),\quad =\pi\ (q_j\text{ constant})", font_size=28)]
        whys = [why(r"take $p'$ an independent copy of $p$ and expand: the covariance is half the expected product of "
                    r"differences"),
                why(r"Chebyshev's association inequality: two increasing functions move together, so each product is "
                    r"non-negative (strictly positive when both are strictly increasing)"),
                why(r"exact recovery needs a strictly positive common gap, positive occurrence probabilities and an LLN; weak monotonicity alone permits equality")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "That covariance is nonnegative, by a two-line argument. <bookmark mark='a'/> Take an independent copy of the "
            "tone, p prime. The covariance equals half the expected product of the differences, g of p minus g of p "
            "prime, times q of p minus q of p prime. <bookmark mark='b'/> Both functions increase, so the two "
            "differences always have the same sign, and every product is non-negative: Chebyshev's association "
            "inequality. <bookmark mark='c'/> So, in the limit, positive words sit above the overall share, negative "
            "words below only with a strict population gap. Neutral occurrence must be independent of tone; tone-dependent document lengths can break that conclusion. Finite-vocabulary recovery also needs a common gap and sufficient word frequencies; monotonicity alone is not a sample-size theorem."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"n\,\theta^2 \min_{j \in S}\frac{(O_{+,j} - O_{-,j})^2}{(O_{+,j} + O_{-,j})^2} \ \ge\ "
                            r"\frac{\log^2 m}{\min\{1,\ \bar s\min_{j \in S}(O_{+,j} + O_{-,j}),\ \min_{j \in N}\bar\Omega_j\}}",
                            font_size=30),
                    wrapped_label(r"Under model (1)--(4), balance/neutrality conditions (C.6)--(C.9), and the displayed scaling, with $\alpha_\pm \propto \sqrt{\log m \log\log m}\,/\sqrt{n \min\{\cdot\}}$, "
                                  r"$P(\hat S = S) \to 1$ as $n, m \to \infty$. $\theta$: how strongly returns respond to "
                                  r"tone; the minimum: how often the rarest words appear in an article; schematic sufficient scaling, subject to all assumptions",
                                  9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Sure screening (Ke, Kelly and Xiu, Theorem C.2)", st, r"Ke, Kelly and Xiu (2019), Appendix C",
                            width=11.4, font_size=22)
        with self.voiceover(
            "With finitely many documents, the question is how many. <bookmark mark='a'/> Ke, Kelly and Xiu prove that "
            "the screen recovers exactly the right words, with probability tending to one, once the number of "
            "articles times the squared sensitivity of returns to tone, times the words' squared sentiment contrast, "
            "exceeds the square of the log of the vocabulary size, divided by how often the rarest words appear. "
            "<bookmark mark='b'/> Three things decide it: how strongly returns respond to tone, theta; how "
            "different the two topics are; and how long the articles are. Short articles and weak returns need many "
            "more documents. The displayed result requires the paper's document, frequency, balance and neutrality assumptions, with centring at one half rather than our helper's sample share. Its theta is the weighted association defined in equation C point ten, not the simulation's slope parameter; it is not a calibrated finite-sample guarantee for these dependent statements."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def limits(self, t):
        fb = t["f_big"]
        lim = fb["limit"]
        g = axes([0.3, 0.7], [0, 1], x_length=8.4, y_length=3.8, xlabel=r"$f_j$, on 20{,}000 simulated articles",
                 ylabel=r"", xticks=[0.3, 0.4, 0.5, 0.6, 0.7], yticks=[], font_size=15).move_to(LEFT * 0.8 + DOWN * 0.1)
        ax = g.ax
        rugs = VGroup()
        for key, col, y0 in (("f_pos", HAWK, 0.75), ("f_neutral", GREY_B, 0.45), ("f_neg", DOVE, 0.15)):
            for v in fb[key]:
                rugs.add(Line(ax.c2p(v, y0 - 0.08), ax.c2p(v, y0 + 0.08), color=col, stroke_width=1.6, stroke_opacity=0.8))
        marks = VGroup()
        for key, col, y0 in (("pos", HAWK, 0.75), ("neutral", GREY_B, 0.45), ("neg", DOVE, 0.15)):
            v = lim[key]
            marks.add(Triangle(color=col, fill_opacity=1).scale(0.09).rotate(PI).move_to(ax.c2p(v, y0 + 0.17)))
        names = VGroup(label(r"20 positive words", font_size=16, color=HAWK).move_to(ax.c2p(0.33, 0.75)),
                       label(r"200 neutral", font_size=16, color=GREY_B).move_to(ax.c2p(0.33, 0.45)),
                       label(r"20 negative", font_size=16, color=DOVE).move_to(ax.c2p(0.33, 0.15)))
        side = wrapped_label(rf"triangles: population limits {lim['pos']:.3f}, $\pi$ = {lim['neutral']:.3f} and "
                             rf"{lim['neg']:.3f}; means of the simulated $f_j$: {fb['pos']:.3f}, {fb['neutral']:.3f}, "
                             rf"{fb['neg']:.3f}; sample positive-label share {fb['pi']:.3f} ($\theta = 0.5$, five charged words an article)", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Check the lemma on a simulated world with a thousand words, forty of them charged, and twenty thousand "
            "articles. <bookmark mark='a'/> Each tick is one word's screening statistic. <bookmark mark='b'/> The "
            f"triangles are the limits the lemma predicts: {lim['pos']:.3f} for positive words, the overall share for "
            f"neutral ones, {lim['neg']:.3f} for negative. The simulated words gather around them: means of "
            f"{fb['pos']:.3f}, {fb['neutral']:.3f} and {fb['neg']:.3f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r_) for r_ in rugs], lag_ratio=0.004), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(marks), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def recovery(self, t):
        ns = np.asarray(t["ns"], float)
        g = axes([2, 3.75], [0, 1], x_length=8.0, y_length=4.4, xlabel=r"training articles $n$ (log scale)",
                 ylabel=r"share of the true sentiment words found", xticks=[2, 3, np.log10(5000)], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for th in ("0.2", "0.5", "1.0"):
            for s_len, dash in (("20", False), ("5", True)):
                rows = t["recovery"][f"{th}_{s_len}"]
                y = [r["tpr"] for r in rows]
                c = curve(ax, np.log10(ns), y, THETA_C[th], stroke_width=3)
                if dash:
                    c = DashedVMobject(c, num_dashes=30)
                lines.add(c)
        n_st = t["data"]["n"]
        fomc = DashedLine(ax.c2p(np.log10(n_st), 0), ax.c2p(np.log10(n_st), 1), color=WORD)
        ftag = label(rf"{n_st} original FOMC training statements", font_size=22, color=WORD).to_edge(UP, buff=0.45)
        leg = legend([(THETA_C["1.0"], r"$\theta = 1$: $\Pr(y>0\mid p)=p$"), (THETA_C["0.5"], r"$\theta = 0.5$"),
                      (THETA_C["0.2"], r"$\theta = 0.2$: weaker chosen simulation slope"), (GREY_A, r"solid: 20 charged words an "
                                                                                  r"article; dashed: 5")],
                     font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.3)
        fit_right(leg)
        side = wrapped_label(rf"screen: $|f_j - \pi| \ge z\sqrt{{\pi(1 - \pi)/k_j}}$ with $z = \sqrt{{2\log m}} = "
                             rf"{t['z_screen']:.2f}$; heuristic simulation screen, not finite FWER control. Eight seeds per point", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r10 = t["recovery"]["1.0_20"]
        r05 = t["recovery"]["0.5_20"]
        with self.voiceover(
            "Now count how many documents it takes. <bookmark mark='a'/> With a heuristic threshold that lets few "
            "neutral words pass in these fixed simulations, plot the share of the true sentiment words found against the number of training "
            "articles. <bookmark mark='b'/> At the strongest simulated slope, with longer charged-word sequences, a thousand articles "
            f"find {100 * r10[3]['tpr']:.0f} percent of the words. At half that sensitivity it takes five thousand. "
            "With short articles, more again. <bookmark mark='c'/> And at a sensitivity of one fifth, a weaker "
            "association in this chosen world, five thousand articles find almost nothing. <bookmark mark='d'/> The FOMC "
            f"statements are here, at {n_st}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[2]), Create(lines[3]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[4]), Create(lines[5]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(fomc), FadeIn(ftag))
        self.wait(0.4)
        self.clear_scene()

    def statements(self, t):
        d = t["data"]
        h = np.asarray(d["null_hist"], float)
        overflow = 500 - int(h.sum())
        h = np.r_[h, overflow]
        g = axes([0, 62], [0, max(h.max() * 1.15, 1)], x_length=7.6, y_length=4.0, xlabel=r"words kept by Chapter 5's screen",
                 ylabel=r"shuffled-label runs", xticks=[0, 20, 40, 60], xfmt=lambda x: r"\ge60" if x == 60 else str(int(x)), yticks=[], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001),
                                  stroke_width=0, fill_color=GREY_B, fill_opacity=0.8).move_to(
            [(ax.c2p(k, 0)[0] + ax.c2p(k + 1, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0]) for k, v in enumerate(h)])
        real = Line(ax.c2p(d["n_real"], 0), ax.c2p(d["n_real"], ax.y_range[1]), color=HURDLE, stroke_width=4)
        rtag = label(rf"the real labels: {d['n_real']}", font_size=17, color=HURDLE).next_to(real, UP, buff=0.05)
        dz = t["data_z"]
        side = wrapped_label(rf"500 runs with the yield moves shuffled among the {d['n']} statements: mean "
                             rf"{d['null_mean']:.0f} words kept, so $p = {d['p_perm']:.2f}$. The word-by-word screen keeps "
                             rf"{dz['n_real']} words on the real labels. Fixed selected thresholds, no retuning; exchangeability required. "
                             rf"Last bar aggregates {overflow} runs with 60 or more words; all 500 runs shown.", 3.6, 16, GREY_A).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "So, on the statements, test the screen against chance. <bookmark mark='a'/> Shuffle the two-year moves "
            "among the statements five hundred times and screen again using the previously selected thresholds. Under this unrestricted-shuffle diagnostic, the screen keeps "
            f"{d['null_mean']:.0f} words on average. <bookmark mark='b'/> On the real labels it kept {d['n_real']}: "
            f"a permutation p-value of {d['p_perm']:.2f}. And the word-by-word screen of the simulation, which lets "
            f"few neutral words through in our fixed simulation, keeps {dz['n_real']}. These are empirical exceedance fractions over five hundred draws, not an exact universal p-value or proof that the selected words are all noise. Exchangeability is questionable across policy regimes, and the selected thresholds are not reselected inside each shuffle. The simulated sample sizes are illustrations, not a calibrated century-long requirement for the Fed."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(real), FadeIn(rtag), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: screening when labels are dependent", r"statement days share regimes and articles share "
                          r"news; obtain guarantees under a specified dependence structure rather than importing an IID rate",
                          width=12.4, font_size=18),
            desk_question(r"open: phrases and context", r"the model is a bag of words; screening $n$-grams or "
                          r"contextual embeddings increases $m$ and changes frequencies and dependencies; assess the full rate, not only its logarithm",
                          width=12.4, font_size=18),
            desk_question(r"open: borrowing strength", r"a prior from a large corpus (a dictionary, an LLM) could shrink "
                          r"what a small labelled one must learn; how to combine them with guarantees is open",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The theorem assumes independent documents; statement days share "
            "regimes and news articles share stories; this result does not supply a dependence-adjusted rate for our application. "
            "<bookmark mark='b'/> Screening phrases or contextual embeddings multiplies the vocabulary, and the price "
            "grows with its log squared. <bookmark mark='c'/> And a prior from a large corpus, a dictionary or a "
            "language model, could shrink what a small labelled set must learn; how to combine them with guarantees "
            "is open."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k > 0:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"$g(p) = \frac12$ for every $p$: returns ignore tone. What is the limit of $f_j$ for a positive "
                       r"word, and what does the screen find?")
        with self.voiceover(
            "Pause and predict. Suppose returns ignore tone entirely: g of p is one half for every p. What is the limit "
            "of the screening statistic for a positive word, and what does the screen find?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
