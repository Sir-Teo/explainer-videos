from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


def surprisal_strip(words, surp, y, color, highlight=None, ymax: float = 22.0, x0: float = -6.2, width: float = 7.4):
    """Words in a row, each with a bar for its surprisal (bits) above it."""
    n = len(words)
    step = width / n
    g = VGroup()
    for k, (w, s) in enumerate(zip(words, surp)):
        x = x0 + step * (k + 0.5)
        h = 1.6 * float(s) / ymax
        col = LOST if highlight is not None and k == highlight else color
        bar = Rectangle(width=step * 0.7, height=max(h, 0.02), stroke_width=0, fill_color=col,
                        fill_opacity=0.85).move_to([x, y + h / 2, 0])
        g.add(VGroup(bar, label(rf"\emph{{{w}}}", font_size=24, color=WHITE).move_to([x, y - 0.25, 0]),
                     label(f"{s:.0f}", font_size=18, color=GREY_A).next_to(bar, UP, buff=0.04)))
    return g


class Sentences(VoiceoverScene):
    def construct(self):
        self.card()
        self.garden()
        self.eyes()
        self.ngram()

    def card(self):
        card = chapter_card(4, r"Sentences in real time", r"Do you understand a sentence word by word?",
                            lit={1970: r"Bever", 1982: r"Frazier \& Rayner", 2001: r"Hale"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter four. Sentences in real time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def garden(self):
        head = heading(r"Garden paths")
        s1 = label(r"\emph{The horse raced past the barn} \ldots", font_size=36, color=WORD).move_to([0, 1.9, 0])
        s1b = label(r"\emph{The horse raced past the barn fell.}", font_size=36, color=WORD).move_to([0, 1.9, 0])
        fell = label(r"?!", font_size=36, color=LOST).next_to(s1b, RIGHT, buff=0.2)
        s2 = label(r"\emph{The horse that was raced past the barn fell.}", font_size=30, color=MODEL).move_to(
            [0, 0.9, 0])
        s3 = label(r"\emph{The old man the boats.}", font_size=32, color=RULE).move_to([0, 0.0, 0])
        rows = rows_of([
            (r"Bever, \ 1970: \ \emph{raced} is read as the main verb, \ so \emph{fell} has nowhere to go", WHITE),
            (r"it is grammatical: \ \emph{raced} can be a passive, \ as in the second sentence", MODEL),
            (r"\emph{the old man} is a noun phrase, \ until it is a verb", RULE),
            (r"readers commit to one analysis as they go, \ and pay when it turns out wrong", STAT),
        ], 12.6, 27, 0.36).move_to([0, -2.1, 0])
        tag = historical_tag(r"Bever (1970)")
        with self.voiceover(
            "Sentences arrive one word at a time, and you understand them as they come, which has a cost. "
            "<bookmark mark='a'/> Read this: the horse raced past the barn. <bookmark mark='b'/> Fell. Most people "
            "stumble, or decide it isn't English. <bookmark mark='c'/> But it is. Raced can be a passive, as in the "
            "horse that was raced past the barn fell. <bookmark mark='d'/> Or: the old man the boats. The old man "
            "is a noun phrase, until man turns out to be the verb. <bookmark mark='e'/> Thomas Bever called these "
            "garden-path sentences. Readers commit to one analysis as they go, and pay when it turns out to be "
            "wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(s1))
            vo.wait_until("b")
            self.play(ReplacementTransform(s1, s1b), FadeIn(fell), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(s2), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(s3), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def eyes(self):
        head = heading(r"Watching the eyes")
        words = ["Since", "Jay", "always", "jogs", "a", "mile", "seems", "like", "a", "short", "distance"]
        row = Tex(*[(r"\ " if k else "") + w for k, w in enumerate(words)], font_size=40, color=WORD)
        row.move_to([0, 2.0, 0])  # one Tex, so the words share a baseline
        # a schematic reader: (word, fixation in ms); the long stop at "seems", then back to "jogs"
        fixes = [(0, 210), (1, 230), (2, 200), (3, 240), (5, 250), (6, 420), (3, 280), (6, 240), (7, 200), (9, 230),
                 (10, 250)]
        y0 = row.get_bottom()[1] - 0.55
        pts, dots = [], VGroup()
        for i, (k, ms) in enumerate(fixes):
            y = y0 if i <= 5 else y0 - 0.75
            pt = np.array([row[k].get_center()[0], y, 0])
            pts.append(pt)
            col = LOST if i == 5 else MODEL
            dots.add(Circle(radius=0.05 + 0.35 * ms / 1000, color=col, stroke_width=2).set_fill(col, 0.35).move_to(pt))
        segs = VGroup(*[Line(pts[i], pts[i + 1], color=LOST if i == 5 else MODEL, stroke_width=2.5,
                             buff=dots[i].width / 2) for i in range(len(pts) - 1)])
        back = label(r"a regression", font_size=22, color=LOST).next_to(segs[5].get_center(), LEFT, buff=0.25)
        longfix = label(r"a long fixation", font_size=22, color=LOST).next_to(dots[5], RIGHT, buff=0.2)
        longfix.shift(UP * 0.1)
        size_key = label(r"circle size: \ time spent on the word", font_size=20, color=GREY_B)
        size_key.next_to(VGroup(*dots), DOWN, buff=0.3).align_to(row, LEFT)
        path = VGroup(segs, dots)
        rows = rows_of([
            (r"an eye tracker shows where the eyes stop, \ for how long, \ and when they jump back", WHITE),
            (r"Frazier \& Rayner, \ 1982: \ at the word that breaks the first analysis, \ fixations lengthen and "
             r"the eyes go back", MODEL),
            (r"\emph{a mile} is first taken as what Jay jogs; \ \emph{seems} forces a new structure", RULE),
            (r"the path drawn here is a schematic of that pattern, \ not a recorded reader", GREY_A),
        ], 12.6, 27, 0.36).move_to([0, -2.0, 0])
        tag = published_tag(r"Frazier \& Rayner (1982)")
        with self.voiceover(
            "How do we know when the cost is paid? <bookmark mark='a'/> By watching the eyes. An eye tracker records "
            "where the eyes stop, for how long, and when they jump backwards. <bookmark mark='b'/> In 1982 Lyn "
            "Frazier and Keith Rayner showed that at the word that breaks the first analysis, fixations get longer "
            "and the eyes often go back to earlier words. <bookmark mark='c'/> Since Jay always jogs a mile seems like a "
            "short distance: a mile is first taken as what Jay jogs, and seems forces a new structure. "
            "<bookmark mark='d'/> The path drawn here is a schematic of that pattern, not a recorded reader."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(row))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(size_key))
            for i in range(6):
                self.play(FadeIn(dots[i], scale=0.5), *([Create(segs[i - 1])] if i else []), run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(longfix), Indicate(dots[5], color=LOST), FadeIn(rows[1]))
            self.play(Create(segs[5]), FadeIn(dots[6], scale=0.5), FadeIn(back))
            for i in range(7, len(dots)):
                self.play(Create(segs[i - 1]), FadeIn(dots[i], scale=0.5), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ngram(self):
        d = load("garden")
        head = heading(r"What a trigram model sees")
        w0, s0 = list(d["words_0"]), d["surp_0"]
        w1, s1 = list(d["words_1"]), d["surp_1"]
        strip0 = surprisal_strip(w0, s0, 1.0, WORD, highlight=len(w0) - 1)
        strip1 = surprisal_strip(w1, s1, -1.4, MODEL, highlight=len(w1) - 1)
        assert abs(s0[-1] - s1[-1]) < 1e-6  # the narration says the two are the same
        eq = MathTex(r"\text{surprisal}(w_t) = -\log_2 P(w_t \mid w_{t-2}, w_{t-1})", font_size=32,
                     color=STAT).move_to([3.6, 2.3, 0])
        rows = rows_of([
            (r"a trigram model trained on the thirty novels, \ surprisal in bits", WHITE),
            (rf"\emph{{fell}} costs {s0[-1]:.0f} bits in both sentences: \ the model sees only \emph{{the barn}}", LOST),
            (r"the garden path lives in structure two words cannot hold", RULE),
            (r"Hale, \ 2001: \ with a probabilistic grammar, \ surprisal does spike at \emph{fell}; \ the next "
             r"chapter measures the cost of surprise in thousands of real words", STAT),
        ], 4.9, 22, 0.32).move_to([4.4, -0.6, 0])
        ptag = psyche_tag(r"\texttt{language.KneserNey}: \ a trigram model of the novels")
        with self.voiceover(
            "One way to measure surprise is with a language model. <bookmark mark='a'/> Psyche trains a trigram "
            "model on the thirty novels: the probability of each word given the two before it. Surprisal is minus "
            "the log of that probability, in bits. <bookmark mark='b'/> Here are the two horse sentences, word by "
            f"word. Fell costs {s0[-1]:.0f} bits in both, exactly the same, because the model sees only the barn. "
            "<bookmark mark='c'/> The garden path lives in structure that two words of context cannot hold. "
            "<bookmark mark='d'/> John Hale showed in 2001 that surprisal computed from a probabilistic grammar does "
            "spike at fell. Better models see more. The next chapter measures the cost of surprise across thousands "
            "of real words, where even a trigram does surprisingly well."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in strip0], lag_ratio=0.15), run_time=2)
            self.play(LaggedStart(*[FadeIn(g) for g in strip1], lag_ratio=0.15), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
