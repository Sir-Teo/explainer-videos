from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, mono, tag_box,
                                   trace)

# Jane Austen's first sentence, as our tokenizer and stemmer treat it (explainer/cs/search/text.py: tokens, STOP,
# porter); written out here so that the scene does not import the instruments.
SENTENCE = ["it", "is", "a", "truth", "universally", "acknowledged", "that", "a", "single", "man", "in",
            "possession", "of", "a", "good", "fortune", "must", "be", "in", "want", "of", "a", "wife"]
STOPPED = {"it", "is", "a", "that", "in", "of", "be"}
STEMS = {"universally": "univers", "acknowledged": "acknowledg", "single": "singl", "possession": "possess",
         "fortune": "fortun"}


def flow(items, width, hbuff=0.12, vbuff=0.18):
    """Boxes laid out like words in a paragraph: left to right, wrapping at ``width``."""
    rows, cur, w = [], [], 0.0
    for it in items:
        if cur and w + hbuff + it.width > width:
            rows.append(VGroup(*cur).arrange(RIGHT, buff=hbuff))
            cur, w = [], 0.0
        w += (hbuff if cur else 0.0) + it.width
        cur.append(it)
    rows.append(VGroup(*cur).arrange(RIGHT, buff=hbuff))
    return VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=vbuff)


class Text(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokens()
        self.porter()
        self.zipf()
        self.heaps()

    def card(self):
        card = chapter_card(1, r"Words, \ stems and Zipf", r"What is a word, \ to a search engine?",
                            lit=(1949, 1980), extra=((1949, r"Zipf: \ the principle of least effort"),
                                                     (1978, r"Heaps: \ vocabulary growth"),
                                                     (1980, r"Porter: \ suffix stripping")), part=PART)
        with self.voiceover("Chapter one. Words, stems and Zipf."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tokens(self):
        head = label(r"From characters to terms", font_size=36).to_edge(UP, buff=0.3)
        sent = wrapped_label(r"``It is a truth universally acknowledged, \ that a single man in possession of a good "
                             r"fortune, \ must be in want of a wife.''", 12.4, font_size=24,
                             color=GREY_A).next_to(head, DOWN, buff=0.55)
        src = note(r"Jane Austen, \ \textit{Pride and Prejudice} \ (1813), \ the first sentence", font_size=17).next_to(
            sent, DOWN, buff=0.12)
        boxes = [tag_box(w, color=DATA, size=22, h=0.58) for w in SENTENCE]
        toks = flow(boxes, 12.4, hbuff=0.14, vbuff=0.24).next_to(src, DOWN, buff=0.75).set_x(0)
        notes = VGroup(
            wrapped_label(r"\textbf{tokens}: \ runs of letters and digits \ (an inner apostrophe kept), \ lower-cased; \ case folding makes "
                          r"\textit{Whale} and \textit{whale} one term, \ but also \textit{US} and \textit{us}", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"\textbf{stop words}: \ 48 short, \ common words; \ here 12 of the 23 tokens; \ our index "
                          r"keeps them \ (phrases need them), \ our ranked queries drop them", 12.4, font_size=20,
                          color=GREY_A),
            wrapped_label(r"\textbf{stems}: \ \textit{acknowledged}, \ \textit{acknowledges} and "
                          r"\textit{acknowledging} \ all become the one term \texttt{acknowledg}", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(toks, DOWN, buff=0.9).set_x(0)
        stop = [b for b, w in zip(boxes, SENTENCE) if w in STOPPED]
        stems = []
        for b, w in zip(boxes, SENTENCE):
            if w in STEMS:
                nb = tag_box(STEMS[w], color=HEAD, size=22, w=b[0].width, h=0.58).move_to(b)
                stems.append((b, nb))
        with self.voiceover(
            "A search engine sees characters, and its first job is to decide what the words are. "
            "<bookmark mark='a'/> Our tokenizer keeps runs of letters and digits and folds them to lower case, so "
            "that Whale at the start of a sentence and whale in the middle become one term. Folding has a price: it "
            "also merges US, the country, with us. <bookmark mark='b'/> Next come stop words, forty-eight short "
            "words such as the, of and a. In Jane Austen's first sentence they are twelve of the twenty-three tokens. "
            "Our index keeps them, because phrases need them, but ranked queries drop them. <bookmark mark='c'/> "
            "Last, stemming cuts each word down to a stem, so that acknowledged, acknowledges and acknowledging all "
            "become one term."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sent), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in boxes], lag_ratio=0.08), run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(*[b[0].animate.set_stroke(GREY_D) for b in stop], *[b[1].animate.set_color(GREY_D) for b in stop],
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(*[Transform(b, nb) for b, nb in stems], FadeIn(notes[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def porter(self):
        p = load("porter")
        s = p["samples"]
        n_ok = sum(1 for v in p["published"].values() if v[2])
        head = label(r"Porter's stemmer", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"1a", r"plural \texttt{-s}", "generalization"),
                 (r"1b", r"\texttt{-ed}, \ \texttt{-ing}: \ none", "generalization"),
                 (r"1c", r"\texttt{-y} to \texttt{-i}: \ none", "generalization"),
                 (r"2", r"\texttt{-ization} to \texttt{-ize}", "generalize"),
                 (r"3", r"\texttt{-alize} to \texttt{-al}", "general"),
                 (r"4", r"\texttt{-al} removed", "gener"),
                 (r"5", r"tidy \texttt{-e}, \ \texttt{-ll}: \ none", "gener")]
        tab = grid_table([r"step", r"rule that fires", r"word"], [[a, b, c] for a, b, c in steps],
                         widths=[1.0, 4.0, 2.6], row_h=0.56, font_size=22, mono_cols=(2,))
        start = label(r"input: \ \texttt{generalizations}", font_size=24, color=DATA)
        left = VGroup(start, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        left.to_edge(LEFT, buff=0.4)
        for r in range(1, len(steps) + 1):
            if steps[r - 1][1].endswith("none"):
                tab.cells[r][1].set_color(GREY_B)
            else:
                tab.cells[r][2].set_color(HEAD)
        meas = VGroup(
            wrapped_label(r"a rule fires only if enough of the word would remain: \ the \textbf{measure} $m$ counts "
                          r"the vowel--consonant pairs of the stem", 5.6, font_size=21, color=WHITE),
            wrapped_label(r"\texttt{gener}: \ g\,(en)(er), \ $m = 2$, \ so \texttt{-al} may go; \ \texttt{riv}: \ "
                          r"r\,(iv), \ $m = 1$, \ so \texttt{rival} stays", 5.6, font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        good = VGroup(
            label(rf"\texttt{{whaling}}, \ \texttt{{whales}} $\to$ \texttt{{{s['whaling']}}}", font_size=21,
                  color=YES),
            label(rf"\texttt{{connection}}, \ \texttt{{connected}}, \ \texttt{{connecting}} $\to$ "
                  rf"\texttt{{{s['connecting']}}}", font_size=21, color=YES),
            label(rf"\texttt{{harpooned}} $\to$ \texttt{{{s['harpooned']}}}, \ \texttt{{happiness}} $\to$ "
                  rf"\texttt{{{s['happiness']}}}", font_size=21, color=YES),
            label(rf"{n_ok} of Porter's {len(p['published'])} published examples reproduced", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        bad = VGroup(
            label(r"\texttt{general}, \ \texttt{generous} $\to$ \texttt{gener}", font_size=21, color=NO),
            label(rf"\texttt{{running}} $\to$ \texttt{{{s['running']}}}, \ but \texttt{{ran}} $\to$ "
                  rf"\texttt{{{s['ran']}}}", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        right = VGroup(meas, good, bad).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        right.next_to(head, DOWN, buff=0.6).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Martin Porter published his stemmer in 1980, and it is still in wide use for English. "
            "<bookmark mark='a'/> It uses no dictionary: about sixty suffix rules in five steps, applied in order. "
            "Follow generalizations. Step one strips the plural. Step two turns ization into ize, step three turns "
            "alize into al, and step four removes the al, leaving gener. <bookmark mark='b'/> A rule may fire only "
            "if enough of the word would remain. Porter measures a stem by counting its vowel-consonant pairs: gener "
            "has two, so its al can go, but riv has only one, so rival keeps its ending. <bookmark mark='c'/> Our "
            "implementation reproduces all twenty of the published examples. It merges whaling and whales into "
            "whale, and connection, connected and connecting into connect. <bookmark mark='d'/> It also errs: "
            "general and generous both become gener, and ran never meets run. A lemmatizer, with a dictionary of "
            "word forms, would fix both, at a price."
        ) as vo:
            self.play(FadeIn(head), FadeIn(start), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            for r in range(1, len(steps) + 1):
                self.play(FadeIn(VGroup(*tab.cells[r]), shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(meas))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g) for g in good], lag_ratio=0.4), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(bad))
        self.wait(0.4)
        self.clear_scene()

    def zipf(self):
        z = load("zipf")
        head = label(r"Zipf's law", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 4.6, 1], [0, 5.8, 1], x_length=6.2, y_length=4.4, x_label=r"rank \ (log scale)",
                 y_label=r"occurrences \ (log scale)", xticks=range(0, 5), yticks=range(1, 6),
                 fx=lambda v: f"{10 ** int(v):,}", fy=lambda v: f"{10 ** int(v):,}").move_to([-2.9, -0.45, 0])
        ax = g.ax
        pts = [(math.log10(r), math.log10(f)) for r, f in z["rank_freq"]]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.065, color=DATA) for x, y in pts])
        slope = z["zipf_slope"]
        mid = [(x, y) for (r, _), (x, y) in zip(z["rank_freq"], pts) if 10 <= r <= 10_000]
        b0 = sum(y - slope * x for x, y in mid) / len(mid)       # the line through the fitted range's centre
        x_in = max(0.0, (5.4 - b0) / slope)                      # start where the line enters the axes
        fit = DashedLine(ax.c2p(x_in, b0 + slope * x_in), ax.c2p(4.5, b0 + slope * 4.5), color=HEAD, stroke_width=3)
        fl = label(rf"slope ${slope:.2f}$ \ (least squares, \ ranks 10 to 10,000)", font_size=18,
                   color=HEAD).next_to(ax.c2p(2.0, b0 + slope * 2.0), UR, buff=0.15)
        top = z["top"][:8]
        fmax = top[0][1]
        bars = VGroup()
        for k, (w, f) in enumerate(top):
            y = -k * 0.34
            word = mono(w, size=17, color=WHITE).move_to([0, y, 0]).align_to([0.6, 0, 0], RIGHT)
            bar = Rectangle(width=3.0 * f / fmax, height=0.22, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
            bar.move_to([0.75 + bar.width / 2, y, 0])
            num = label(f"{f:,}", font_size=16, color=GREY_A).next_to(bar, RIGHT, buff=0.1)
            bars.add(VGroup(word, bar, num))
        btitle = label(r"the commonest words", font_size=19, color=GREY_A)
        right = VGroup(btitle, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        notes = VGroup(
            wrapped_label(rf"\texttt{{the}}: \ {top[0][1]:,} of {z['tokens']:,} tokens, \ "
                          rf"{100 * top[0][1] / z['tokens']:.1f}\%; \ the top 20 words: \ "
                          rf"{100 * sum(f for _, f in z['top'][:20]) / z['tokens']:.0f}\%", 5.0, font_size=19,
                          color=WHITE),
            wrapped_label(rf"{z['hapax']:,} of the {z['types']:,} different words, \ "
                          rf"{100 * z['hapax'] / z['types']:.0f}\%, \ occur exactly once", 5.0, font_size=19,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        side = VGroup(right, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.4)
        side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now count. The thirty novels hold four and a half million tokens, and sixty-one thousand seven hundred "
            "and twenty different words. <bookmark mark='a'/> The commonest, the, occurs two hundred and thirty "
            "thousand times: one token in twenty. The top twenty words make up almost a third of all the text. "
            "<bookmark mark='b'/> Plot frequency against rank, both on logarithmic scales, and the points fall close "
            "to a straight line. That is Zipf's law: George Kingsley Zipf described it in the 1930s and 1940s, with "
            "frequency roughly proportional to one over the rank. Fitted between ranks ten and ten thousand, our "
            "line has slope minus one point two one. <bookmark mark='c'/> At the other end, twenty-two thousand "
            "eight hundred and eighty-eight words, more than a third of the vocabulary, occur exactly once. So an "
            "index must handle a few enormous postings lists and a vast number of tiny ones, both cheaply."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(btitle), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in bars], lag_ratio=0.2),
                      run_time=2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.12), run_time=2)
            self.play(Create(fit), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(dots[-1], color=LAM), Indicate(dots[-2], color=LAM))
        self.wait(0.4)
        self.clear_scene()

    def heaps(self):
        z = load("zipf")
        ix = load("index")
        head = label(r"Heaps' law", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 4.8, 1], [0, 70, 10], x_length=6.4, y_length=4.4, x_label=r"tokens read \ (millions)",
                 y_label=r"different words \ (thousands)", xticks=range(0, 5), yticks=range(10, 61, 10)).move_to(
            [-2.8, -0.45, 0])
        ax = g.ax
        data = [(n / 1e6, v / 1e3) for n, v in z["heaps"]]
        seen = trace(ax, data, DATA, width=4)
        K, beta = z["heaps_K"], z["heaps_beta"]
        fitp = [(n / 1e6, K * n ** beta / 1e3) for n in [20_000 * 1.12 ** k for k in range(48)] if n <= 4.6e6]
        fit = DashedVMobject(trace(ax, fitp, HEAD, width=3), num_dashes=60)
        end = ax.c2p(*data[-1])
        ul = label(r"\textit{Ulysses}, \ last in our order", font_size=18, color=LAM).move_to(ax.c2p(2.3, 60))
        uarrow = Arrow(ul.get_right(), end, buff=0.12, stroke_width=2.5, color=LAM, max_tip_length_to_length_ratio=0.15)
        law = MathTex(r"V = K\,n^{\beta}", font_size=40, color=HEAD)
        notes = VGroup(
            wrapped_label(rf"least squares on log scales: \ $K = {K:.1f}$, \ $\beta = {beta:.3f}$", 5.2,
                          font_size=20, color=HEAD),
            wrapped_label(r"$\beta$ close to $\tfrac12$: \ a hundred times the text, \ about ten times the words; \ "
                          r"the vocabulary never stops growing", 5.2, font_size=20, color=WHITE),
            wrapped_label(rf"stemming: \ {z['types']:,} words become {ix['terms']:,} terms, \ "
                          rf"{100 * (1 - ix['terms'] / z['types']):.0f}\% fewer", 5.2, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(law, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35).shift(
            DOWN * 0.2)
        with self.voiceover(
            "How fast does the vocabulary grow as we read? <bookmark mark='a'/> Here is the number of different "
            "words seen, against the number of tokens read, novel after novel. It climbs steeply, then ever more "
            "slowly, but it never levels off: every book brings new names and new words. <bookmark mark='b'/> "
            "Gustav Herdan, and later Harold Heaps, described this as a power law: the vocabulary grows as a "
            "constant times the number of tokens to a power beta. Our fit gives beta of nought point four eight "
            "five, close to a half, so a hundred times the text brings about ten times the vocabulary. "
            "<bookmark mark='c'/> The jump at the end is Ulysses, last in our order, and the richest in new words. "
            "<bookmark mark='d'/> Stemming cuts the vocabulary by a third, to forty thousand six hundred and "
            "ninety-two terms. Those terms are the dictionary of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(seen), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(law), Create(fit), FadeIn(notes[0]), run_time=1.5)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(ul), GrowArrow(uarrow))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
