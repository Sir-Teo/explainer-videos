from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import NEG, PART, POS, UNC, WORD, comma, fit_right, load


class Dictionaries(VoiceoverScene):
    def construct(self):
        t = load("tone")
        self.card()
        self.tetlock()
        self.lm(t)
        self.statements(t)
        self.misfit(t)
        self.question()

    def card(self):
        c = chapter_card(2, r"Dictionaries", r"Which words count as bad news, and who decides?", part=PART)
        with self.voiceover("Chapter two. The oldest way to read text at scale: a list of words that count as good "
                            "news and a list that count as bad. Which words, and who decides?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tetlock(self):
        card = firm_card(r"Tetlock (2007)", r"`Giving content to investor sentiment': the Wall Street Journal's daily "
                         r"`Abreast of the Market' column, 1984--1999, scored with the Harvard General Inquirer's word "
                         r"categories and summarised by principal components into one pessimism factor",
                         numbers=((r"\downarrow", r"high pessimism predicts downward pressure on the Dow the next day"),
                                  (r"\uparrow", r"followed by a reversion to fundamentals within the week"),
                                  (r"\Uparrow", r"unusually high or low pessimism predicts high volume")),
                         source=r"Tetlock, \textit{Journal of Finance} 62 (2007)", kind=r"Paper file", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "In 2007 Paul Tetlock took one newspaper column, the Wall Street Journal's daily Abreast of the Market, from "
            "1984 to 1999, and counted its words in the categories of the Harvard General Inquirer, a dictionary built "
            "by psychologists in the 1960s. <bookmark mark='a'/> One pessimism factor came out. When it was high, the "
            "Dow fell the next day, and then came back within the week. <bookmark mark='b'/> A temporary push and a "
            "reversal is what noise traders' sentiment should do, not news about fundamentals; and extreme pessimism "
            "in either direction predicted heavy trading. Media words, it turned out, move prices, if only for a while."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def lm(self, t):
        words = [r"tax", r"cost", r"capital", r"board", r"liability", r"foreign", r"vice"]
        harvard = VGroup(label(r"Harvard negative, in a 10-K", font_size=22, color=GREY_A),
                         *[label(rf"\texttt{{{w}}}", font_size=24, color=NEG) for w in words]).arrange(DOWN, buff=0.16)
        fin = VGroup(label(r"Loughran--McDonald negative", font_size=22, color=GREY_A),
                     *[label(rf"\texttt{{{w}}}", font_size=24, color=NEG) for w in
                       (r"felony", r"litigation", r"restated", r"misstatement", r"unanticipated", r"impairment", r"default")]
                     ).arrange(DOWN, buff=0.16)
        pair = VGroup(harvard, fin).arrange(RIGHT, buff=2.2).move_to(LEFT * 1.5 + DOWN * 0.1)
        cross = VGroup(*[Line(m.get_left() + LEFT * 0.1, m.get_right() + RIGHT * 0.1, color=GREY_B, stroke_width=3)
                         for m in harvard[1:]])
        stat = VGroup(MathTex(r"73.8\%", font_size=64, color=NEG),
                      wrapped_label(r"of the Harvard list's negative word counts in 50{,}000 10-Ks, 1994--2008, come "
                                    r"from words that are not negative in finance", 3.3, 18, GREY_A)).arrange(DOWN, buff=0.2)
        stat.to_edge(RIGHT, buff=0.5)
        sizes = wrapped_label(rf"today's lists: {comma(t['n_lm']['negative'])} negative, {t['n_lm']['positive']} positive, "
                              rf"{t['n_lm']['uncertainty']} uncertainty words (the 1993--2025 master dictionary)", 3.3, 16,
                              GREY_B).next_to(stat, DOWN, buff=0.4)
        fit_right(VGroup(stat, sizes))
        with self.voiceover(
            "Four years later, Tim Loughran and Bill McDonald pointed out what goes wrong when a psychologist's "
            "dictionary reads a company's annual report. <bookmark mark='a'/> To the Harvard list, tax, cost, capital, "
            "board, liability, foreign and vice are negative words. In a ten-K they are simply the business: the board "
            "of directors, the vice president, capital expenditure. <bookmark mark='b'/> Across fifty thousand annual "
            "reports, almost three quarters of the Harvard list's negative counts came from words like these. "
            "<bookmark mark='c'/> So they built their own lists from the filings themselves: felony, litigation, "
            "restated, impairment. Their dictionary is now the default in finance, updated ever since, with "
            f"{t['n_lm']['negative']:,} negative words, {t['n_lm']['positive']} positive and {t['n_lm']['uncertainty']} "
            "for uncertainty."
        ) as vo:
            self.play(FadeIn(harvard))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in cross], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(stat))
            vo.wait_until("c")
            self.play(FadeIn(fin), FadeIn(sizes))
        self.wait(0.4)
        self.clear_scene()

    def statements(self, t):
        d = np.asarray(t["dates"])
        yr = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        g = axes([1997, 2021], [0, 6], x_length=9.0, y_length=4.2, xlabel=r"", ylabel=r"share of a statement's words, \%",
                 xticks=[2000, 2005, 2010, 2015, 2020], yticks=[0, 2, 4, 6], font_size=15).move_to(LEFT * 1.2 + DOWN * 0.3)
        ax = g.ax
        lines = {}
        for key, col in (("neg", NEG), ("pos", POS), ("unc", UNC)):
            y = np.clip(100 * np.asarray(t[key]), 0, 6)
            lines[key] = curve(ax, yr, y, col, stroke_width=2.5)
        shade = VGroup(*[Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.y_length, stroke_width=0,
                                   fill_color=GREY_D, fill_opacity=0.35).move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2,
                                                                                  ax.c2p(0, 3)[1], 0])
                         for a, b in ((2001.2, 2001.9), (2007.95, 2009.5), (2020.1, 2020.35))])
        leg = legend([(NEG, r"negative"), (POS, r"positive"), (UNC, r"uncertainty"), (GREY_D, r"recessions (NBER)")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "Run the dictionary over every FOMC statement. <bookmark mark='a'/> The negative share jumps in the "
            "recessions of 2001, 2008 and 2020, as you would hope. <bookmark mark='b'/> The positive share drifts and "
            "the uncertainty share sits near a steady floor, set by the committee's habit of saying what it "
            "anticipates and what risks it sees, whatever the weather."
        ) as vo:
            self.play(FadeIn(g), FadeIn(shade), FadeIn(leg[3]))
            vo.wait_until("a")
            self.play(Create(lines["neg"]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["pos"]), Create(lines["unc"]), FadeIn(leg[1]), FadeIn(leg[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def misfit(self, t):
        cols = VGroup()
        for title, key, col in ((r"negative", "top_neg", NEG), (r"positive", "top_pos", POS), (r"uncertainty", "top_unc", UNC)):
            rows = VGroup(label(rf"most counted {title}", font_size=20, color=col))
            for w, n in t[key][:8]:
                rows.add(label(rf"\texttt{{{w}}}\ \ {n}", font_size=19))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            cols.add(rows)
        cols.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(UP * 0.4)
        w0 = t["top_neg"][0][0]
        p0 = t["top_pos"][0][0]
        foot = wrapped_label(rf"\texttt{{{w0}}} is half of the Fed's mandate, not bad news, and \texttt{{{p0}}} is the "
                             r"other half's goal (price stability): the finance dictionary misreads a central bank the way "
                             r"the Harvard list misread a 10-K", 11.4, 18, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "But look at which words do the counting. <bookmark mark='a'/> The most counted negative word in the "
            f"statements is {w0}, and the most counted positive word is {p0}. <bookmark mark='b'/> In a central "
            "bank's statement, those are not news at all: they are the two halves of its mandate, maximum employment "
            "and stable prices, named in nearly every paragraph. The finance dictionary misreads a central bank the "
            "way the psychologists' dictionary misread an annual report. Every dictionary is fitted to a genre, and "
            "this one was fitted to filings."
        ) as vo:
            self.play(FadeIn(cols))
            vo.wait_until("a")
            self.play(Indicate(cols[0][1], color=NEG), Indicate(cols[1][1], color=POS))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"`The Committee will not hesitate to act if the outlook weakens.' Count its Loughran--McDonald "
                       r"negative words. Is the sentence hawkish or dovish?")
        with self.voiceover(
            "Pause and predict. The Committee will not hesitate to act if the outlook weakens. How many negative "
            "words would the dictionary count, and is the sentence hawkish or dovish?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
