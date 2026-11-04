from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, PART, WORD, comma, fit_right, load

SAMPLE = r"The Committee decided today to keep its target for the federal funds rate at 5-1/4 percent."


class Words(VoiceoverScene):
    def construct(self):
        c = load("corpus")
        self.card()
        self.bag()
        self.matrix(c)
        self.zipf(c)
        self.heaps(c)
        self.tfidf()
        self.question()

    def card(self):
        c = chapter_card(1, r"Words as numbers", r"How does a statement become a row of a matrix?", part=PART)
        with self.voiceover("Chapter one. Before any model can read, words have to become numbers. How does a "
                            "statement become a row of a matrix?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bag(self):
        sent = label(SAMPLE, font_size=26).to_edge(UP, buff=0.9)
        toks = ["the", "committee", "decided", "today", "to", "keep", "its", "target", "for", "the", "federal", "funds",
                "rate", "at", "percent"]
        chips = VGroup(*[label(rf"\texttt{{{w}}}", font_size=22, color=WORD) for w in toks]).arrange(RIGHT, buff=0.18)
        if chips.width > 13.0:
            chips.scale_to_fit_width(13.0)
        chips.next_to(sent, DOWN, buff=0.6)
        from collections import Counter
        cnt = Counter(toks)
        words = sorted(cnt)
        bars = VGroup()
        for k, w in enumerate(words):
            b = Rectangle(width=0.55, height=0.45 * cnt[w], stroke_width=0, fill_color=WORD, fill_opacity=0.8)
            t = label(rf"\texttt{{{w}}}", font_size=15, color=GREY_A).rotate(PI / 2.6)
            bars.add(VGroup(b, t))
        for k, g in enumerate(bars):
            g[0].move_to([-6.0 + 0.85 * k, -2.0 + g[0].height / 2, 0])
            g[1].next_to(g[0], DOWN, buff=0.12).shift(LEFT * 0.15)
        note_ = wrapped_label(r"lower case, numbers and punctuation dropped, then counted: the order is thrown away. "
                              r"That is the \emph{bag of words}", 5.2, 18, GREY_A).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Take one sentence from a statement. <bookmark mark='a'/> Split it into words, lower-case them, and drop "
            "the numbers and punctuation. <bookmark mark='b'/> Then count. The order is thrown away: this is the bag "
            "of words, and for thirty years most of text analysis in finance started, and ended, here. It loses "
            "grammar, negation and context, and keeps something surprisingly useful: which words were chosen, how often."
        ) as vo:
            self.play(FadeIn(sent))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(ch, shift=DOWN * 0.2) for ch in chips], lag_ratio=0.08), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in bars], lag_ratio=0.06),
                      FadeIn(VGroup(*[g[1] for g in bars])), FadeIn(note_), run_time=1.8)
        self.wait(0.4)
        self.clear_scene()

    def matrix(self, c):
        rows = [cmath(r"D", r"\in", r"\mathbb N^{n \times m},\qquad D_{ij} = \#\{\text{word } j \text{ in document } i\}",
                      font_size=32, colors={r"D": WORD}),
                cmath(r"n", r"=", rf"{c['n_statements']}\ \text{{statements}} + {c['n_minutes']}\ \text{{minutes}},\quad "
                      rf"m = {comma(c['n_types'])}\ \text{{distinct words}}", font_size=30),
                cmath(r"\text{sparse}", r":", rf"\text{{a statement uses about }} {c['median_statement_words']:.0f}"
                      r"\text{ words; the minutes about }" + comma(c['median_minutes_words']), font_size=28)]
        whys = [why(r"each document becomes a row of counts over a fixed vocabulary; every method in this part starts "
                    r"from this matrix or from the word sequence it summarises"),
                why(rf"the corpus here: every FOMC statement and every set of minutes, {c['first_minutes'] // 10000} to "
                    rf"2020 for research ({comma(c['n_tokens'])} words in all)"),
                why(r"almost every entry of $D$ is zero: text is high-dimensional and sparse, the regime of Parts 25 and 27")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Do that for every document and stack the counts. <bookmark mark='a'/> The document-term matrix: one row "
            "per document, one column per word, each entry a count. <bookmark mark='b'/> Our corpus is every statement "
            f"the Federal Open Market Committee has released since 1997, {c['n_statements']} of them through 2020, and "
            f"every set of minutes since {c['first_minutes'] // 10000}, {c['n_minutes']} more: in all about "
            f"{c['n_tokens'] / 1e6:.0f} million words and {c['n_types']:,} distinct ones. <bookmark mark='c'/> Almost "
            "every entry is zero. Text is the extreme case of the problem Parts twenty-five and twenty-seven kept "
            "meeting: far more columns than anyone can estimate one at a time."
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

    def zipf(self, c):
        r = np.asarray(c["zipf_rank"], float)
        f = np.asarray(c["zipf_freq"], float)
        g = axes([0, np.log10(r[-1]) + 0.2], [0, np.log10(f[0]) + 0.3], x_length=7.2, y_length=4.4,
                 xlabel=r"rank of the word (log scale)", ylabel=r"how often it is used (log scale)",
                 xticks=list(range(0, int(np.log10(r[-1])) + 1)), yticks=list(range(0, int(np.log10(f[0])) + 1)),
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).move_to(LEFT * 2.0 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.035, color=WORD) for a, b in zip(r, f)])
        xs = np.linspace(0, np.log10(r[-1]), 50)
        fit = curve(ax, xs, c["zipf_intercept"] / np.log(10) + c["zipf_slope"] * xs, HURDLE, stroke_width=3)
        top = c["top"][:10]
        side = VGroup(label(r"the ten most common", font_size=20, color=GREY_A),
                      *[label(rf"\texttt{{{w}}}\ \ {n:,}".replace(",", "{,}"), font_size=17) for w, n in top],
                      wrapped_label(rf"slope {c['zipf_slope']:.2f} between ranks 10 and 1{{,}}000: Zipf's law, frequency "
                                    r"about proportional to 1/rank", 3.6, 16, HURDLE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side.to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Sort the words by how often they appear and plot frequency against rank, both on log scales. "
            "<bookmark mark='a'/> A straight line, with a slope near minus one: Zipf's law, which holds in nearly "
            f"every language and corpus ever measured. Here the slope is {c['zipf_slope']:.2f}. <bookmark mark='b'/> "
            "The head is a handful of function words, the and of and to, which carry almost no meaning; the tail is "
            "tens of thousands of words used once or twice. Everything interesting lives in between, and every method "
            "is a different way of deciding which of those middle words matter."
        ) as vo:
            self.play(FadeIn(g))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02), run_time=2)
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side[-1]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*side[:-1])))
        self.wait(0.4)
        self.clear_scene()

    def heaps(self, c):
        yrs = np.asarray(c["years"], float)
        gr = np.asarray(c["growth"], float)
        top = float(np.ceil(gr.max() / 2000) * 2000)
        g = axes([yrs[0], yrs[-1]], [0, top], x_length=8.0, y_length=4.2, xlabel=r"",
                 ylabel=r"distinct words seen in the minutes so far", xticks=[2000, 2005, 2010, 2015, 2020],
                 yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, yrs, gr, WORD, stroke_width=3)
        k08 = int(np.searchsorted(yrs, 2008))
        k07 = max(k08 - 1, 0)
        new08 = int(gr[min(k08 + 2, len(gr) - 1)] - gr[k07])
        side = wrapped_label(rf"{comma(gr[0])} distinct words in the {int(yrs[0])} minutes; {comma(gr[-1])} by 2020. "
                             rf"2008--2010 added {comma(new08)}: the words of a new policy", 3.5, 16, GREY_A).to_edge(RIGHT, buff=0.35)
        mark = DashedLine(ax.c2p(2008, 0), ax.c2p(2008, top), color=HURDLE)
        with self.voiceover(
            "The vocabulary never stops growing. <bookmark mark='a'/> Count the distinct words the minutes have used, "
            f"year by year: {int(gr[0]):,} in the first year, {int(gr[-1]):,} by 2020. This is Heaps' law, the "
            "companion of Zipf's: new documents keep bringing new words, more slowly but without end. "
            "<bookmark mark='b'/> From 2008 to 2010 alone, the committee wrote "
            f"{new08:,} words it had never used before. A model frozen in 2007 has never seen them: hold on to that "
            "for Chapter twelve."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()


    def tfidf(self):
        rows = [cmath(r"\mathrm{tf}_{ij}", r"=", r"D_{ij} \big/ \textstyle\sum_k D_{ik}", font_size=34, colors={r"\mathrm{tf}_{ij}": WORD}),
                cmath(r"\mathrm{idf}_j", r"=", r"\log\frac{1 + n}{1 + \#\{i : D_{ij} > 0\}} + 1", font_size=34,
                      colors={r"\mathrm{idf}_j": HURDLE}),
                cmath(r"x_{ij}", r"=", r"\mathrm{tf}_{ij}\,\mathrm{idf}_j \big/ \|\cdot\|", font_size=34, colors={r"x_{ij}": WORD})]
        whys = [why(r"term frequency: counts become shares, so long documents do not dominate"),
                why(r"inverse document frequency: a word in every document (\emph{committee}) gets weight near 1; a "
                    r"word in a few (\emph{pandemic}) gets much more"),
                why(r"each row scaled to unit length: cosine similarity between documents is then a dot product")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The simplest reweighting is called t f i d f. <bookmark mark='a'/> Turn counts into shares, so long "
            "documents do not dominate. <bookmark mark='b'/> Then weight each word by how rare it is across documents: "
            "a word that appears everywhere, like committee, gets almost nothing; a word in a few documents, like "
            "pandemic, gets a lot. <bookmark mark='c'/> Scale each row to unit length, and the similarity of two "
            "statements is a single dot product. Search engines ran on this for decades."
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

    def question(self):
        q = pause_card(r"a word appears in every FOMC statement but in no other document. What is its idf weight "
                       r"within the statements, and is it useless?")
        with self.voiceover(
            "Pause and predict. A word appears in every FOMC statement and nowhere else. What is its weight within the "
            "statements, and is it useless?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
