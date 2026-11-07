from __future__ import annotations

import numpy as np

from explainer.stats.kit import learn as L
from videos.stats.stats19.common import *  # noqa: F403
from videos.stats.stats19.compute import fed_matrix


class NaiveBayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_ways()
        self.poisson_model()
        self.weights()
        self.loo()
        self.curves()
        self.overconfident()

    def card(self):
        card = chapter_card(5, r"Naive Bayes vs logistic regression", r"Model the words, \ or model the author?", part=PART)
        with self.voiceover("Chapter five. Naive Bayes versus logistic regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two_ways(self):
        rows = [
            cmath(r"\text{generative}", r":", r"\text{model } p(x \mid y) \text{ and } p(y);\ \ \text{then Bayes's rule}", font_size=30),
            cmath(r"P(y \mid x)", r"=", r"\frac{p(x \mid y)\,p(y)}{\sum_{y'} p(x \mid y')\,p(y')}", font_size=30),
            cmath(r"\text{discriminative}", r":", r"\text{model } P(y \mid x) \text{ directly}", font_size=30),
            cmath(r"\text{logistic}", r":", r"\log\frac{P(y = 1 \mid x)}{P(y = 0 \mid x)} = \beta_0 + \beta' x", font_size=30),
        ]
        rows[1][2].set_color(HAM)
        rows[3][2].set_color(MAD)
        whys = [why(r"how each author's words are produced"), why(r"Part 2, \ Part 15"), why(r"only the boundary matters"),
                why(r"Part 14's model")]
        intro = label('Model the features or model the conditional class probability', font_size=36)
        with self.voiceover(
            "There are two ways to build a classifier. <bookmark mark='a'/> The generative way models how the data are produced "
            "within each class: how Hamilton's word counts are distributed, how Madison's are, and how common each author is. "
            "<bookmark mark='b'/> Bayes's rule, from Parts 2 and 15, then turns that into the probability of each author given "
            "the words. <bookmark mark='c'/> The discriminative way skips the words' distribution and models the probability "
            "of the class given the words directly. <bookmark mark='d'/> Part 14's logistic regression is the standard example."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def poisson_model(self):
        rows = [
            cmath(r"x_w \mid \text{author } a", r"\sim", r"\text{Poisson}(r_{a,w}\, t)\ \ \text{independently}", font_size=30),
            cmath(r"\log\frac{P(M \mid x)}{P(H \mid x)}", r"=", r"\textstyle\sum_w x_w \log\frac{r_{M,w}}{r_{H,w}} - t \sum_w (r_{M,w} - r_{H,w}) + \text{prior}",
                  font_size=28),
            cmath(r"\text{``naive''}", r":", r"\text{the words are treated as independent}", font_size=30),
            cmath(r"\text{fit}", r":", r"\text{each author's rate of each word, \ from the known papers}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"$t$: \ the paper's length; \ $r$: \ uses per word"), why(r"a weighted sum of word counts"),
                why(r"false, \ and often harmless"), why(r"91 rates per author: \ 70 function words and 21 markers")]
        intro = label('Poisson word counts yield a linear log-likelihood ratio', font_size=36)
        with self.voiceover(
            "Mosteller and Wallace's model was generative. In its simplest form: <bookmark mark='a'/> each word's count in a "
            "paper of length t is Poisson, with a rate that depends on the author, and the words are independent of each other. "
            "<bookmark mark='b'/> Then the log odds of Madison against Hamilton is a weighted sum of the word counts, each "
            "weighted by the log ratio of the two authors' rates, minus a term for the paper's length, plus the prior log odds. "
            "<bookmark mark='c'/> Treating the words as independent is the naive part, and it's false: words come in phrases. "
            "<bookmark mark='d'/> Fitting means estimating each author's rate for each of ninety-one words from the papers "
            "whose authors are known."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def weights(self):
        words, C, n, a, no = fed_matrix()
        known = (a == "HAMILTON") | (a == "MADISON")
        nb = L.PoissonNB().fit(C[known], n[known], (a[known] == "MADISON").astype(int))
        lr = np.log(nb.rates[1] / nb.rates[0])
        order = np.argsort(lr)
        pick = list(order[:6]) + list(order[-6:])
        A = axes([-0.6, 11.6], [-4.5, 4.5], x_length=10.4, y_length=4.2, xlabel=r"", ylabel=r"$\log(r_M / r_H)$",
                 yticks=[-4, -2, 0, 2, 4], center=[0.2, 0.6, 0])
        ax = A.ax
        bars = VGroup()
        names = VGroup()
        for k, j in enumerate(pick):
            v = float(lr[j])
            top, bot = ax.c2p(k, max(v, 0)), ax.c2p(k, min(v, 0))
            bars.add(Rectangle(width=ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0], height=max(0.01, top[1] - bot[1]), stroke_width=0,
                               fill_color=MAD if v > 0 else HAM, fill_opacity=0.9).move_to((top + bot) / 2))
            nm = label(rf"\emph{{{words[j]}}}", font_size=20, color=GREY_A).rotate(35 * DEGREES)
            names.add(nm.move_to(ax.c2p(k, -4.5) + DOWN * 0.12 + RIGHT * 0.1, aligned_edge=UR))
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(11.6, 0), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"blue: \ evidence for Madison; \ red: \ for Hamilton", font_size=22),
            label(r"each use of \emph{upon} multiplies the odds on Hamilton by about 17", font_size=22, color=HAM),
        ), 12.4, 0.2, [0, -3.05, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the weights for the twelve words that discriminate most. Blue words are evidence for "
            "Madison: whilst, although, consequently, innovation. Red ones for Hamilton: while, enough, kind, upon. <bookmark mark='b'/> Each use "
            "of upon in a disputed paper multiplies the odds in favour of Hamilton by about seventeen, so a single occurrence "
            "counts for a lot. Common words like on and by carry smaller weights, but appear so often that they add up."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if lr[j] > 0 else UP) for b_, j in zip(bars, pick)], lag_ratio=0.08), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def loo(self):
        d = load("nbvslr")
        rows = [
            cmath(r"\text{leave-one-out}", r":", r"\text{fit on 64 known papers, \ classify the 65th}", font_size=30),
            cmath(r"\text{Poisson naive Bayes}", r":", rf"{int(round(d['nb_err'] * d['m']))}\ \text{{errors of}}\ {d['m']}", font_size=30),
            cmath(r"\text{ridge logistic regression}", r":", rf"{int(round(d['lr_err'] * d['m']))}\ \text{{errors of}}\ {d['m']}", font_size=30),
            cmath(r"\text{both}", r":", r"\text{perfect on the papers we can check}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"cross-validation with 65 folds"), why(r"word rates as features"),
                why(r"91 rates, \ a ridge penalty (chapter seven)"), why(r"the function words really are fingerprints")]
        intro = label('Leave one known paper out before fitting each classifier', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> How good are they? Leave one known paper out, fit on the other sixty-four, and classify the "
            "one left out, sixty-five times. <bookmark mark='b'/> Poisson naive Bayes makes no errors. <bookmark mark='c'/> "
            "Logistic regression on the ninety-one word rates, with a ridge penalty to keep its ninety-two coefficients "
            "tame, also makes none. <bookmark mark='d'/> On the papers we can check, both are perfect: the function words really "
            "are fingerprints."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def curves(self):
        d = load("nbvslr")
        s = np.asarray(d["sizes"], float)
        A = axes([0, 58], [0, 0.17], x_length=8.4, y_length=4.2, xlabel=r"known papers used for training",
                 ylabel=r"error on the rest", xticks=[6, 16, 24, 34, 44, 54], yticks=[0, 0.05, 0.1, 0.15], center=[-1.6, 0.3, 0])
        ax = A.ax
        nb = polyline(ax, s, d["curves"]["nb"], HAM, 3.5)
        lr = polyline(ax, s, d["curves"]["lr"], MAD, 3.5)
        dn = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=HAM) for a, b in zip(s, d["curves"]["nb"])])
        dl = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=MAD) for a, b in zip(s, d["curves"]["lr"])])
        rows = fit_rows(VGroup(
            label(r"red: \ naive Bayes", font_size=22, color=HAM),
            label(r"blue: \ ridge logistic", font_size=22, color=MAD),
            MathTex(rf"6\ \text{{papers}}: {100 * d['curves']['nb'][0]:.1f}\%\ \text{{vs}}\ {100 * d['curves']['lr'][0]:.1f}\%", font_size=26),
            label(r"Ng \& Jordan (2002):", font_size=20, color=GREY_A),
            label(r"different sample-complexity regimes; model-dependent", font_size=20, color=GREY_A),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        tag = simulated_tag(r"200 random splits per size", corner=DR)
        with self.voiceover(
            "With fewer training papers, the two differ. <bookmark mark='a'/> Train naive Bayes, and <bookmark "
            "mark='b'/> logistic regression, on a few random known papers and test on the rest, two hundred times at "
            "each size. <bookmark mark='c'/> With six papers to learn from, naive Bayes misclassifies six percent, "
            "logistic regression eleven. <bookmark mark='d'/> Andrew Ng and Michael Jordan showed in 2002 that "
            "particular generative and discriminative models can have different sample-complexity regimes. Our "
            "fixed-penalty learning curves illustrate a possibility, not a guarantee that all generative models learn"
            " faster or all discriminative models eventually win."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(nb), FadeIn(dn), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lr), FadeIn(dl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def overconfident(self):
        d = load("decided")
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{naive Bayes, \ disputed papers}}: \log_{{10}}\text{{odds up to}}\ {max(d['log10_odds']):.0f}", font_size=28),
            label(r"odds of $10^{20}$ to 1: \ not credible", font_size=24, color=RES),
            label(r"independence counts correlated words as separate evidence", font_size=22),
            label(r"the ranking can be right while the probabilities are wildly overconfident", font_size=22, color=OBS),
            label(r"Mosteller \& Wallace: \ negative binomial rates, \ careful priors, \ sensitivity analysis", font_size=22, color=HIT),
        ), 12.4, 0.45, [0, 0, 0])
        intro = label('Classification accuracy does not establish calibration', font_size=36)
        with self.voiceover(
            "A warning before we use it. <bookmark mark='a'/> On the disputed papers, our naive Bayes gives log odds,"
            " base ten, as large as twenty: <bookmark mark='b'/> odds of a hundred billion billion to one, which "
            "nobody should believe. <bookmark mark='c'/> Independence counts words that travel together as separate "
            "pieces of evidence, so the evidence is multiplied many times over. <bookmark mark='d'/> Naive Bayes "
            "often classifies well while its probabilities are wildly overconfident. <bookmark mark='e'/> Mosteller "
            "and Wallace knew this, and used negative binomial rates, careful priors and extensive checks of "
            "sensitivity, to assess how sensitive their odds were to the modelling assumptions. Our plug-in "
            "calculation also omits uncertainty in the estimated word rates."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
