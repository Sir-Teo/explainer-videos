from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class Prevalence(VoiceoverScene):
    def construct(self):
        self.card()
        self.study()
        self.model()
        self.reply()

    def card(self):
        card = chapter_card(10, r"When targets are rare", r"Do searchers miss more when there is less to find?",
                            lit={2005: r"Wolfe, Horowitz and Kenner"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter ten. When targets are rare."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def study(self):
        d = load("prevalence")
        src = archive.WOLFE_2005
        head = heading(r"A search lab, \ 2005: \ the rarer the target, \ the more it is missed")
        A = axes([-0.5, 2.5], [0, 0.6], x_length=6.0, y_length=4.0, xticks=[], yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"", ylabel=r"share of targets missed", center=[-3.0, -0.2, 0])
        ax = A.ax
        bars, names = VGroup(), VGroup()
        for i, (p, m) in enumerate(zip(d["published_prev"], d["published_miss"])):
            bars.add(Rectangle(width=0.9, height=ax.c2p(0, float(m))[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=MISS,
                               fill_opacity=0.85).move_to(ax.c2p(i, 0), aligned_edge=DOWN))
            names.add(VGroup(label(rf"present on {100 * p:g}\%", font_size=22, color=GREY_A),
                             label(r"of displays", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.06)
                      .next_to(ax.c2p(i, 0), DOWN, buff=0.15))
            names.add(label(rf"{100 * m:.0f}\%", font_size=26, color=MISS).next_to(bars[-1], UP, buff=0.08))
        rows = rows_of([
            (r"observers look for a tool among overlapping objects, \ like a baggage X-ray", WHITE),
            (r"only the prevalence changes: \ how often a target is there at all", SIGNALC),
            (r"misses climb from 11\% to 52\%; \ false alarms stay very rare", MISS),
            (r"airport screeners and radiologists search for targets that are rare", THRESH),
        ], 5.0, 27, 0.3).move_to([4.2, 0.0, 0])
        keep_in_frame(rows)
        tag = published_tag(src.cite)
        with self.voiceover(
            "The radar observer's targets were rare. So are a weapon in a suitcase and a tumour on a scan. In 2005 "
            "Jeremy Wolfe, Todd Horowitz and Naomi Kenner asked what rarity itself does to a searcher. "
            "<bookmark mark='a'/> Observers looked for a tool among overlapping objects, a little like a baggage "
            "X-ray. <bookmark mark='b'/> The only thing that changed was how often a target was there at all: on "
            "half the displays, a tenth, or one in a hundred. <bookmark mark='c'/> Misses climbed from eleven percent "
            "to twenty-five, to fifty-two percent, while false alarms stayed very rare. <bookmark mark='d'/> The "
            "people whose job is to find rare things were, in the laboratory at least, worst at finding the rarest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(names[0::2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.4), FadeIn(names[1::2]), FadeIn(rows[2]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def model(self):
        d = load("prevalence")
        head = heading(r"A criterion that follows the base rate")
        A = axes([-2, np.log10(0.5)], [0, 0.8], x_length=6.4, y_length=4.0, xticks=[-2, -1], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 xfmt=lambda v: {-2: r"1\%", -1: r"10\%"}[int(v)], yfmt=lambda v: rf"{100 * v:.0f}\%",
                 xlabel=r"how often a target is present (log scale)", ylabel=r"share missed", center=[-3.0, -0.2, 0])
        ax = A.ax
        lx = np.log10(d["prevalence"])
        cs = VGroup(curve(ax, lx, d["miss_none"], GREY_B, stroke_width=3), curve(ax, lx, d["miss_half"], CRIT, stroke_width=4),
                    curve(ax, lx, d["miss_full"], MISS, stroke_width=4))
        pub = VGroup(*[Dot(ax.c2p(float(np.log10(p)), float(m)), radius=0.09, color=DATA)
                       for p, m in zip(d["published_prev"], d["published_miss"])])
        lg = legend([(GREY_B, r"criterion fixed"), (CRIT, r"moved half way to the ideal"), (MISS, r"moved all the way"),
                     (DATA, r"2005 misses (dots)")], font_size=21).move_to(ax.c2p(-1.0, 0.7))
        rows = rows_of([
            (r"chapter 5: \ as targets grow rare, \ the ideal criterion rises", CRIT),
            (r"a searcher whose criterion follows the base rate misses more, \ by design", MISS),
            (r"the published misses lie between a half-way and a full move", DATA),
            (r"the shape, \ not a fit: \ Psyche's $d' = 2.5$ is a choice", GREY_A),
        ], 4.8, 27, 0.3).move_to([4.3, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $d' = 2.5$")
        with self.voiceover(
            "Signal detection offers an account. <bookmark mark='a'/> Chapter five showed that as targets get rarer, "
            "the ideal criterion moves up: more evidence is needed before yes pays. <bookmark mark='b'/> A searcher "
            "who lets the criterion follow the base rate will miss more of the rare targets, not from worse eyes but "
            "by design. Here's Psyche with its criterion fixed, moved half way to the ideal, and moved all the way. "
            "<bookmark mark='c'/> The published misses fall between the half-way and the full move. "
            "<bookmark mark='d'/> This is the shape, not a fit: Psyche's sensitivity was chosen, not estimated. "
            "But it shows that a missed target need not be an unseen one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(cs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(lg), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(pub), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def reply(self):
        src = archive.FLECK_MITROFF_2007
        head = heading(r"Or quitting too soon?")
        rows = rows_of([
            (r"Fleck and Mitroff (2007): \ let observers take back an answer they had just given", WHITE),
            (r"most of the extra misses disappeared: \ the answer had come before the looking was done", HIT),
            (r"so part of the effect is speed: \ with targets rare, \ ``absent'' becomes a habit given fast", CRIT),
            (r"criterion, \ search that ends early, \ and a fast motor habit all contribute; \ the shares are argued",
             THRESH),
            (r"the practical fix used in airports: \ add fake targets to the stream, \ so they are never too rare",
             MODEL),
        ], 11.6, 30, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(src.cite)
        with self.voiceover(
            "Not everyone accepts that account. <bookmark mark='a'/> In 2007 the psychologists Fleck and Mitroff let "
            "observers take back an answer they had just given. <bookmark mark='b'/> Most of the extra misses "
            "vanished. Observers had often answered absent before they had finished looking. "
            "<bookmark mark='c'/> So part of the prevalence effect is speed: when targets are rare, absent becomes a "
            "habit, given fast. <bookmark mark='d'/> A shifting criterion, searches that end too early and a fast "
            "habit all seem to contribute, and how much each does is still argued. <bookmark mark='e'/> The "
            "practical answer, in airport screening, is to project fake threat images into the stream, so that "
            "targets are never quite so rare and a screener's performance can be measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i]))
        self.clear_scene()
