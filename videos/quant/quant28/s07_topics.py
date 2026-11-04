from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, PART, WORD, comma, fit_right, load

# a name for each topic, found by its words (so a re-run that reorders topics keeps the names)
NAMES = [("aggregates", r"money ranges and restraint"), ("disinflation", r"slowdown and disinflation"),
         ("firming", r"firming: removing accommodation"), ("liquidity", r"liquidity facilities"),
         ("guidance", r"asset purchases and guidance"), ("normalization", r"normalisation"),
         ("repo", r"reserves, repo and the framework"), ("pursuant", r"authorisations (procedure)")]
PALETTE = [QC.STRIKE, QC.VEGA, QC.LOSS, QC.SPOT, QC.OPTION, QC.CASH, QC.DELTA, GREY_C]


def _names(top_words):
    out = []
    for words in top_words:
        nm = next((n for key, n in NAMES if key in words), r"other")
        out.append(nm)
    return out


class Topics(VoiceoverScene):
    def construct(self):
        t = load("topics")
        self.card()
        self.nmf(t)
        self.words(t)
        self.river(t)
        self.bybee()
        self.question()

    def card(self):
        c = chapter_card(6, r"Topics, and the news as macro data", r"What is the committee talking about, and when?",
                         part=PART)
        with self.voiceover("Chapter six. Instead of good and bad, ask what a document is about. Can a machine find the "
                            "themes of thirty years of minutes without being told what they are?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def nmf(self, t):
        rows = [cmath(r"X", r"\approx", r"W H,\qquad W \ge 0,\ H \ge 0", font_size=36, colors={r"X": WORD}),
                cmath(r"X_{i\cdot}", r"\approx", r"\sum_{k=1}^{K} W_{ik}\, H_{k\cdot}", font_size=34, colors={r"X_{i\cdot}": WORD}),
                cmath(r"\text{LDA}", r":", r"d_i \sim \text{Multinomial}\big(n_i,\ \textstyle\sum_k \theta_{ik}\,\beta_k\big),"
                      r"\ \theta_i \sim \text{Dirichlet}", font_size=28)]
        whys = [why(rf"factor the tf-idf matrix of the minutes ({t['n_vocab']:,} words after dropping procedure and "
                    rf"function words) into $K = {t['k']}$ non-negative pieces".replace(",", "{,}")),
                why(r"each document is a non-negative mix of topics; each topic, a weighting of words. Non-negativity is "
                    r"what makes the pieces readable"),
                why(r"latent Dirichlet allocation (Blei, Ng and Jordan 2003) is the probabilistic version, the one "
                    r"Bybee et al.\ and Hansen, McMahon and Prat use; its output has the same shape")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A topic model factors the document-term matrix. <bookmark mark='a'/> Take the weighted matrix of the "
            f"minutes and write it as a product of two non-negative matrices, with {t['k']} topics in between. "
            "<bookmark mark='b'/> Each document becomes a mix of topics, each topic a weighting of words, and because "
            "nothing can be negative, each piece reads like a theme. <bookmark mark='c'/> Latent Dirichlet allocation, "
            "from 2003, is the probabilistic version that most of the finance papers use; non-negative factorisation "
            "gives output of the same shape, and fits in twenty lines."
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

    def words(self, t):
        names = _names(t["top_words"])
        cards = VGroup()
        for k, (nm, ws) in enumerate(zip(names, t["top_words"])):
            col = PALETTE[k % len(PALETTE)]
            cards.add(VGroup(label(nm, font_size=17, color=col),
                             label(r"\texttt{" + ", ".join(w.replace("-", "{-}") for w in ws[:6]) + "}", font_size=13,
                                   color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        cards.arrange_in_grid(rows=4, cols=2, buff=(0.8, 0.35), col_alignments="ll").move_to(UP * 0.1)
        if cards.width > 13.0:
            cards.scale_to_fit_width(13.0)
        with self.voiceover(
            "Here are the eight topics, each named by us after reading its top words; the model only found them. "
            "<bookmark mark='a'/> Money ranges and restraint; slowdown and disinflation; firming and removing "
            "accommodation; liquidity facilities; asset purchases and guidance; normalisation; reserves and repo; and "
            "one topic of pure procedure, the authorisations the committee renews at every January meeting. "
            "<bookmark mark='b'/> Notice what kind of themes they are. Not inflation versus employment, but eras."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cards[:4]], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cards[4:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def river(self, t):
        d = np.asarray(t["dates"])
        S = np.asarray(t["share"], float)
        yrs = np.arange(int(d.min() // 10000), int(d.max() // 10000) + 1)
        Y = np.array([S[d // 10000 == y].mean(0) if np.any(d // 10000 == y) else np.full(S.shape[1], np.nan) for y in yrs])
        Y = np.nan_to_num(Y)
        Y = Y / np.maximum(Y.sum(1, keepdims=True), 1e-9)
        names = _names(t["top_words"])
        g = axes([yrs[0], yrs[-1]], [0, 1], x_length=9.2, y_length=4.8, xlabel=r"", ylabel=r"share of the year's minutes",
                 xticks=[2000, 2005, 2010, 2015, 2020], yticks=[0, 0.5, 1], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        cum = np.zeros(len(yrs))
        layers = VGroup()
        for k in range(Y.shape[1]):
            lo, hi = cum.copy(), cum + Y[:, k]
            pts = [ax.c2p(x, v) for x, v in zip(yrs, hi)] + [ax.c2p(x, v) for x, v in zip(yrs[::-1], lo[::-1])]
            layers.add(Polygon(*pts, stroke_width=0, fill_color=PALETTE[k % len(PALETTE)], fill_opacity=0.8))
            cum = hi
        leg = legend([(PALETTE[k % len(PALETTE)], names[k]) for k in range(len(names))], font_size=14).to_edge(RIGHT, buff=0.25)
        fit_right(leg)
        with self.voiceover(
            "Plot each year's mix. <bookmark mark='a'/> The minutes flow from one era to the next: monetary ranges in "
            "the late nineties; the slowdown of 2001; the measured firming of 2004 to 2006; liquidity facilities in "
            "2008, returning in 2020; asset purchases and forward guidance through 2014; normalisation; and then the "
            "plumbing of reserves and repo. <bookmark mark='b'/> The procedure topic is the steady band that never "
            "goes away. An unsupervised model, with no dates and no labels, has written a history of the committee's "
            "agenda."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in layers], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def bybee(self):
        card = firm_card(r"Bybee, Kelly, Manela and Xiu (2024)", r"`Business news and business cycles': a topic model of "
                         r"800{,}000 Wall Street Journal articles, 1984--2017. The share of news attention each topic "
                         r"receives becomes a time series",
                         numbers=((r"\sim", r"news attention closely tracks a wide range of economic activity"),
                                  (r"\rightarrow", r"it forecasts aggregate stock market returns"),
                                  (r"+", r"a text-augmented VAR adds forecasting power for macroeconomic dynamics")),
                         source=r"\textit{Journal of Finance} 79 (2024)", kind=r"Paper file", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "Leland Bybee, Bryan Kelly, Asaf Manela and Dacheng Xiu did this to the business press. "
            "<bookmark mark='a'/> Eight hundred thousand Wall Street Journal articles, 1984 to 2017, turned into the "
            "share of attention each topic received each month. <bookmark mark='b'/> That attention tracks the "
            "economy closely, forecasts the stock market, and adds forecasting power to a standard model of "
            "macroeconomic dynamics. The news is a macro data series, available daily, long before the official "
            "statistics."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the topics here are eras, not themes. If you wanted a topic for `inflation', what would you "
                       r"change: the number of topics, the weighting, or the documents?")
        with self.voiceover(
            "Pause and predict. These topics are eras, not themes. If you wanted a topic for inflation that runs through "
            "every decade, what would you change: the number of topics, the weighting, or the documents?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
