from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, PART, WORD, fit_right, load

SHOW = ["likely to be measured", "considerable period", "patient", "extended period", "exceptionally low levels",
        "highly accommodative", "some time", "gradual", "transitory", "ongoing increases", "pandemic"]


def _yr(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 0.5) / 12


class Form(VoiceoverScene):
    def construct(self):
        f = load("form")
        p = load("phrases")
        self.card()
        self.length(f)
        self.fog(f)
        self.guidance(p)
        self.question()

    def card(self):
        c = chapter_card(4, r"Length, readability and forward guidance", r"How did the statement learn to talk about "
                         r"the future?", part=PART)
        with self.voiceover("Chapter four. Before asking what the statements say, look at how they say it: how long "
                            "they are, how hard they are to read, and the phrases they use to talk about the future."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def length(self, f):
        x = _yr(f["dates"])
        w = np.asarray(f["words"], float)
        top = float(np.ceil(w.max() / 200) * 200)
        g = axes([1997, 2026], [0, top], x_length=9.4, y_length=4.4, xlabel=r"", ylabel=r"words in the statement",
                 xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 0.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, b), color=WORD if a < 2021 else GREY_C, stroke_width=2.2)
                        for a, b in zip(x, w)])
        tags = VGroup(*[label(t_, font_size=15, color=GREY_A).move_to(ax.c2p(a, top * 0.93))
                        for a, t_ in ((1999.3, r"Greenspan: a paragraph"), (2008.8, r"crisis: policy tools spelled out"),
                                      (2013.2, r"guidance by dates, then thresholds"))])
        with self.voiceover(
            "Here is every statement, as a bar of its length in words. <bookmark mark='a'/> In the late 1990s a "
            f"statement was a paragraph: the median before 2002 is {f['first5']:.0f} words. <bookmark mark='b'/> The "
            "crisis changed that. As the committee cut to zero and began buying bonds, it had to explain tools that "
            "could not be summarised by one number, and to say what it would do next. Since 2016 the median is "
            f"{f['last5']:.0f} words. The statement became the policy instrument."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01), FadeIn(tags[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tags[1]), FadeIn(tags[2]))
        self.wait(0.4)
        self.clear_scene()

    def fog(self, f):
        rows = [cmath(r"\text{fog}", r"=", r"0.4\Big(\frac{\text{words}}{\text{sentences}} + 100\cdot\frac{\text{words of 3+ "
                      r"syllables}}{\text{words}}\Big)", font_size=30, colors={r"\text{fog}": HURDLE}),
                cmath(r"\text{fog}", r"\approx", rf"{f['fog_first']:.0f}\ \text{{(before 2002)}},\quad "
                      rf"{f['fog_last']:.0f}\ \text{{(since 2016)}}", font_size=32, colors={r"\text{fog}": HURDLE}),
                cmath(r"\text{readability}", r"\ne", r"\text{information}", font_size=34)]
        whys = [why(r"Gunning's fog index (1952): roughly the years of schooling a reader needs"),
                why(r"the statements read at the level of a graduate textbook, then and now; length grew far faster than "
                    r"difficulty"),
                why(r"Loughran and McDonald (2014) found fog a poor measure for filings (long technical words are easy "
                    r"for their readers) and proposed file size instead; here, the readers are bond traders")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "And how hard are they to read? <bookmark mark='a'/> The fog index, from 1952, adds the average sentence "
            "length to the share of long words: roughly the years of schooling a reader needs. <bookmark mark='b'/> "
            f"Before 2002 the median statement scored about {f['fog_first']:.0f}; since 2016, about "
            f"{f['fog_last']:.0f}: graduate-school prose both times. Length grew much faster than difficulty. "
            "<bookmark mark='c'/> Loughran and McDonald later argued that fog misjudges financial documents, whose long "
            "words are easy for their intended readers, and proposed something as blunt as file size. Readability is "
            "not information."
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

    def guidance(self, p):
        d = np.asarray(p["dates"])
        x = _yr(d)
        rows = VGroup()
        y0 = 2.6
        g = axes([1997, 2026], [0, len(SHOW)], x_length=9.0, y_length=5.4, xlabel=r"", ylabel=r"",
                 xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[], font_size=14).move_to(RIGHT * 1.1 + DOWN * 0.15)
        ax = g.ax
        names = VGroup()
        ticks = VGroup()
        for k, ph in enumerate(SHOW):
            r = p["rows"].get(ph)
            if r is None:
                continue
            yy = len(SHOW) - k - 0.5
            names.add(label(rf"`{ph}'", font_size=16, color=GREY_A).next_to(ax.c2p(1997, yy), LEFT, buff=0.15))
            for a, hit in zip(x, r["hits"]):
                if hit:
                    ticks.add(Line(ax.c2p(a, yy - 0.3), ax.c2p(a, yy + 0.3), color=WORD if a < 2021 else GREY_B,
                                   stroke_width=2.4))
        VGroup(g, names).move_to(DOWN * 0.15)
        ticks.move_to(ticks.get_center())  # positions already on the axes
        first = {ph: p["rows"][ph]["first"] for ph in SHOW if p["rows"].get(ph)}
        with self.voiceover(
            "The words that carry the most weight are the ones about the future. <bookmark mark='a'/> Each row is a "
            "phrase; each tick, a statement that used it. Likely to be measured, from the 2004 tightening, promised "
            "quarter-point steps; considerable period, extended period and exceptionally low levels promised the "
            "opposite. "
            "<bookmark mark='b'/> Patient, some time, gradual: each phrase lives for a few years, and its removal is "
            "itself the news. <bookmark mark='c'/> Transitory, the committee's word for the inflation of 2021, was "
            "dropped in December of that year, and by March ongoing increases had taken its place. A dictionary cannot "
            "know any of "
            "this: these phrases mean what the committee's history has made them mean."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(t_) for t_ in ticks], lag_ratio=0.003), run_time=3)
            vo.wait_until("b")
            self.wait(0.1)
            vo.wait_until("c")
            self.play(*[Indicate(names[k], color=WORD) for k, ph in enumerate(SHOW) if ph in ("transitory", "ongoing increases")])
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the committee drops `patient' from its statement but changes nothing else. Which way should the "
                       r"two-year move?")
        with self.voiceover(
            "Pause and predict. The committee drops the word patient from its statement and changes nothing else. "
            "Which way should the two-year yield move?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
