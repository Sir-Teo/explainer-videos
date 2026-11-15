from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Types(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.bell()
        self.retest()

    def card(self):
        card = chapter_card(4, r"Types against traits", r"What does sorting people into types throw away?",
                            lit={1921: r"Jung", 1962: r"the MBTI manual"}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter four. Types against traits."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def history(self):
        head = heading(r"Sixteen types")
        letters = VGroup(*[VGroup(word_chip(a, color=c, font_size=30, width=0.9), label(r"or", font_size=18,
                                                                                         color=GREY_B),
                                  word_chip(b, color=c, font_size=30, width=0.9)).arrange(DOWN, buff=0.1)
                           for a, b, c in (("E", "I", E_), ("S", "N", O_), ("T", "F", A_), ("J", "P", C_))])
        letters.arrange(RIGHT, buff=0.5).move_to([-4.0, 0.3, 0])
        rows = rows_of([
            (r"Carl Jung, \ \emph{Psychological Types}, \ 1921: \ introverts and extraverts, \ and functions of "
             r"thinking, \ feeling, \ sensing and intuition", WHITE),
            (r"Katharine Cook Briggs and her daughter Isabel Briggs Myers built a questionnaire on it during the "
             r"Second World War, \ to help women entering industrial work choose jobs", O_),
            (r"its first manual was published in 1962; \ it sorts people on four two-way dimensions into sixteen "
             r"types", C_),
            (r"the question for a measurement: \ are people really of two kinds on each dimension?", YOU),
        ], 7.0, 21, 0.36).move_to([2.6, -0.2, 0])
        tag = historical_tag(r"Jung (1921); \ Myers \& Briggs (1962)")
        with self.voiceover(
            "The best-known personality test isn't built on the five at all. <bookmark mark='a'/> In 1921, in "
            "Psychological Types, Carl Jung described introverts and extraverts, and four functions: thinking, "
            "feeling, sensing and intuition. <bookmark mark='b'/> Katharine Cook Briggs and her daughter Isabel "
            "Briggs Myers built a questionnaire on Jung's ideas during the Second World War, to help women entering "
            "industrial work choose jobs. <bookmark mark='c'/> Its first manual was published in 1962. It sorts "
            "people on four two-way dimensions into sixteen types. <bookmark mark='d'/> The question for a "
            "measurement is simple. Are people really of two kinds on each dimension?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(l_) for l_ in letters], lag_ratio=0.2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bell(self):
        d = load("types")
        head = heading(r"Extraversion in 2{,}800 people")
        e = d["edges"]
        mids = (e[:-1] + e[1:]) / 2
        share = d["hist"] / d["hist"].sum()
        A = axes([0.75, 6.25], [0, 0.22], x_length=6.4, y_length=3.8, xticks=[1, 2, 3, 4, 5, 6],
                 yticks=[0, 0.1, 0.2], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"extraversion score \ (mean of five items)", ylabel=r"share of people",
                 center=[-2.9, -0.3, 0], font_size=15)
        hb = bars(A.ax, mids, share, E_, width=0.54)
        med = DashedLine(A.ax.c2p(d["median"], 0), A.ax.c2p(d["median"], 0.22), color=WHITE, stroke_width=3)
        ml = label(r"the median: \ E above, \ I below", font_size=16, color=WHITE).next_to(A.ax.c2p(d["median"], 0.22),
                                                                                       UP, buff=0.05)
        band = Rectangle(width=abs(A.ax.c2p(d["median"] + 0.5 * d["sd"], 0)[0] - A.ax.c2p(d["median"] - 0.5 * d["sd"],
                                                                                        0)[0]),
                         height=A.ax.c2p(0, 0.22)[1] - A.ax.c2p(0, 0)[1], stroke_width=0, fill_color=LOST,
                         fill_opacity=0.18).move_to(A.ax.c2p(d["median"], 0.11))
        rows = rows_of([
            (r"one hump, \ highest in the middle: \ not two kinds of people", E_),
            (rf"cut at the median, \ and {pct(d['near'])} of people sit within half a standard deviation of the cut", LOST),
            (r"for them a small change in mood or wording moves them across the line, \ and changes their ``type''",
             WHITE),
            (rf"and a median split keeps only $\sqrt{{2/\pi}} \approx {d['keep']:.2f}$ of any correlation the trait has",
             MODEL),
        ], 5.6, 21, 0.36).move_to([3.6, -0.3, 0])
        tag = published_tag(r"data: \ Revelle et al.\ (SAPA, \ 2010), \ recomputed")
        with self.voiceover(
            "Here is extraversion in the SAPA sample. <bookmark mark='a'/> One hump, highest in the middle. Not two "
            "kinds of people. <bookmark mark='b'/> Cut it at the median, as a type does, and "
            f"{spct(d['near'])} of people sit within half a standard deviation of the cut. <bookmark mark='c'/> For "
            "them a small change in mood, or in the wording of a question, moves them across the line, and changes "
            "their type. <bookmark mark='d'/> And a median split throws information away. For normal data, the "
            "split keeps only the square root of two over pi, about point eight, of any correlation the trait has."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.08), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(med), FadeIn(ml), FadeIn(band), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def retest(self):
        d = load("types")
        head = heading(r"The same type, \ twice?")
        A = axes([-0.6, 2.6], [0, 1.0], x_length=6.0, y_length=4.0, xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share with the same type on retest", center=[-2.9, -0.4, 0],
                 font_size=15)
        one = bars(A.ax, np.arange(3) - 0.2, d["one"], E_, width=0.36)
        four = bars(A.ax, np.arange(3) + 0.2, d["all4"], LOST, width=0.36)
        names = VGroup(*[label(rf"reliability {r:.1f}", font_size=16, color=GREY_A).next_to(A.ax.c2p(i, 0), DOWN,
                                                                                            buff=0.2)
                         for i, r in enumerate(d["rel"])])
        vals = VGroup(*[label(pct(v), font_size=15, color=LOST).next_to(four[i], UP, buff=0.05)
                        for i, v in enumerate(d["all4"])])
        key = legend([(E_, r"one dimension"), (LOST, r"all four dimensions")], font_size=16).move_to(A.ax.c2p(0.7, 0.93))
        rows = rows_of([
            (r"test a continuous trait twice: \ the scores correlate with the test's reliability $r$", WHITE),
            (r"the chance of landing on the same side of the median both times is $\tfrac12 + \arcsin(r)/\pi$", MODEL),
            (rf"at $r = 0.8$: \ {pct(d['one'][1])} on one dimension, \ but only {pct(d['all4'][1])} on all four", LOST),
            (r"so a four-letter type changes for many people within weeks, \ though their trait scores barely move: \ "
             r"the instability comes from the cutting", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.type\_agreement}")
        with self.voiceover(
            "Now test people twice. <bookmark mark='a'/> A continuous trait's two scores correlate at the test's "
            "reliability. <bookmark mark='b'/> The chance of landing on the same side of the median both times is a "
            "half, plus the arcsine of the reliability over pi. That follows from the normal distribution, and Psyche "
            f"checks it by simulation. <bookmark mark='c'/> At a reliability of 0.8, "
            f"{spct(d['one'][1])} get the same letter on one dimension, but only {spct(d['all4'][1])} keep all "
            "four. <bookmark mark='d'/> So a four-letter type changes for many people within weeks, though their "
            "trait scores barely move. The instability comes from the cutting, not from the people. That answers "
            "your third number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(one), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(four), FadeIn(vals), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
