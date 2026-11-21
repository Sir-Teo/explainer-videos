from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403

THR_COL = {60: "#7EC8F5", 70: "#7FD1B9", 80: "#7BD88F", 90: "#F2C14E", 100: "#F2A65A", 120: "#F25F5C"}


class Reproduce(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Reproducing papers", r"With the same data and the same code, \ do you get the same "
             r"numbers, \ and what if you make other reasonable choices?", "Chapter three. Reproducing papers.",
             lit={2010: "Reinhart and Rogoff", 2018: "the AEA Data Editor"}, scale=("world",),
             horizon=("a decade",))
        self.ladder()
        self.projects()
        self.multiverse()

    def ladder(self):
        ch = flow_chain([(r"reproduce: \\ same data, \ same code", FIRST), (r"robust: \\ same data, \\ other choices",
                                                                           PUB),
                         (r"replicate: \\ new data, \ same design", TRUE), (r"generalize: \\ new place, \ new time",
                                                                          STATE)],
                        box_w=2.9, box_h=1.25, font_size=18).move_to(UP * 0.9)
        rows = VGroup(
            label(r"each step can fail for a different reason", font_size=21, color=GREY_A),
            label(r"chapter two was the third step; \ this chapter is the first two", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ch, DOWN, buff=0.8)
        with self.voiceover(
            "Replication has a ladder, and the words are used loosely, so fix them. <bookmark mark='a'/> To "
            "reproduce a result is to get the same numbers from the same data and the same code. <bookmark "
            "mark='b'/> To test its robustness is to keep the data and make other reasonable choices. <bookmark "
            "mark='c'/> To replicate it is to run the same design on new data, as the laboratories did in chapter "
            "two. <bookmark mark='d'/> And to generalize it is to find it in another place and time. <bookmark "
            "mark='e'/> Each step can fail for its own reasons. This chapter climbs the first two."
        ) as vo:
            self.play(FadeIn(ch.boxes[0]))
            for mk, k in zip("bcd", (1, 2, 3)):
                vo.wait_until(mk)
                self.play(Create(ch.arrows[k - 1]), FadeIn(ch.boxes[k]))
            vo.wait_until("e")
            self.play(FadeIn(rows))
        self.clear_scene()

    def projects(self):
        D = tables.REPLICATION_67.data
        cards = point_cards([
            (r"Chang and Li, \ 2015", rf"67 papers in 13 journals: \ {D['cl_alone'][0]} reproduced from the files "
             rf"alone; \ {D['cl_help'][0]} of {D['cl_help'][1]} with the authors' help \ (49\%)", FAIL),
            (r"the AEA Data Editor, \ since 2018", r"the code is run before publication: \ data, \ programs and a "
             r"guide to rebuild every table", TRUE),
            (rf"the Institute for Replication, \ 2024", rf"{D['i4r_papers']} papers: \ over "
             rf"{100 * D['i4r_repro']:.0f}\% computationally reproducible, \ coding errors in about a quarter", PUB),
            (r"robustness", rf"5,511 re-analyses by other teams: \ about {100 * D['i4r_robust']:.0f}\% kept the "
             r"original's significance", FIRST),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"same data, \ same code?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Chang and Li, \ FEDS 2015-083 / \emph{CFR} (2022); \ Brodeur et al., \ IZA DP 16912 "
                            r"(2024); \ the AEA's Data and Code Availability Policy", corner=DL, font_size=12)
        with self.voiceover(
            "The first rung sounds trivial. It was not. <bookmark mark='a'/> In a 2015 Federal Reserve working paper, "
            "Andrew Chang and Phillip Li tried to reproduce sixty-seven papers from thirteen "
            "journals. From the posted files alone they managed twenty-two; with the authors' help, twenty-nine of "
            "the fifty-nine they could attempt, under half. Most failures were missing files. <bookmark mark='b'/> "
            "Since 2018 the American Economic Association has had a data editor, whose team runs each paper's code "
            "before it is published. <bookmark mark='c'/> In 2024 the Institute for Replication reported on a "
            "hundred and ten recent papers in economics and political science: more than eighty-five percent "
            "reproduced from their files, but about a quarter contained coding errors. <bookmark mark='d'/> And "
            "when other teams made other reasonable choices, in five and a half thousand re-analyses, about seventy "
            "percent kept the original's statistical significance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def multiverse(self):
        M = load("multiverse")
        rows = M["rows"]
        n = len(rows)
        ax = plane([0, n + 1], [-6.5, 1.0], center=UP * 0.75 + LEFT * 0.5, x_length=10.6, y_length=3.6, xticks=[],
                   yticks=[-6, -4, -2, 0], ylabel=r"growth above the threshold minus below, \ points",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        zero = seg(ax, 0, 0, n + 1, 0, GREY_C, 1.5)
        pts = VGroup(*[Dot(ax.ax.c2p(k + 1, r_["gap"]), radius=0.06, color=THR_COL[r_["threshold"]])
                       for k, r_ in enumerate(rows)])
        rr = [k for k, r_ in enumerate(rows) if r_["threshold"] == 90 and r_["weight"] == "country"
              and r_["start"] == 1946 and r_["drop"]][0]
        ring = Circle(radius=0.15, stroke_color=WHITE, stroke_width=2.4).move_to(pts[rr])
        rrl = label(r"closest to Reinhart and Rogoff's choices", font_size=14, color=WHITE).next_to(ring, UP,
                                                                                                   buff=0.1)
        # the choices, as a grid under the curve
        grid = VGroup()
        names = (r"country weights", r"start in 1950", r"their exclusions")
        tests = (lambda r_: r_["weight"] == "country", lambda r_: r_["start"] == 1950, lambda r_: r_["drop"])
        y0 = ax.ax.c2p(0, -6.5)[1] - 0.35
        for j, (nm, f) in enumerate(zip(names, tests)):
            yy = y0 - 0.3 * j
            grid.add(label(nm, font_size=13, color=GREY_A).move_to([ax.ax.c2p(0, 0)[0] - 1.2, yy, 0]))
            for k, r_ in enumerate(rows):
                if f(r_):
                    x = ax.ax.c2p(k + 1, 0)[0]
                    grid.add(Rectangle(width=0.12, height=0.16, fill_color=GREY_B, fill_opacity=0.9,
                                       stroke_width=0).move_to([x, yy, 0]))
        key = VGroup(*[VGroup(Dot(radius=0.07, color=c_), label(rf"{t}\%", font_size=14, color=c_)).arrange(
            RIGHT, buff=0.1) for t, c_ in THR_COL.items()]).arrange(RIGHT, buff=0.3)
        key = VGroup(label(r"threshold:", font_size=14, color=GREY_A), key).arrange(RIGHT, buff=0.2)
        key.next_to(ax.ax, UP, buff=0.15).align_to(ax.ax, LEFT).shift(RIGHT * 0.8)
        side = label(rf"{n} analyses: \ {100 * M['share_neg']:.0f}\% find slower growth above the threshold; \ the "
                     rf"gap runs from {M['lo']:.1f} to {M['hi']:+.1f} points".replace("-", "{-}"), font_size=18,
                     color=E.ACCENT).to_edge(DOWN, buff=0.35)
        tag = data_tag(r"Reinhart and Rogoff's data as processed by Herndon, \ Ash and Pollin, \ 20 advanced "
                       r"economies, \ 1946--2009", corner=DR, font_size=12)
        with self.voiceover(
            "The second rung, on a famous case. In Part thirty-two, Thomas Herndon, a graduate student, found a "
            "spreadsheet error in Carmen Reinhart and Kenneth Rogoff's study of public debt and growth. The data "
            "are public now, so ask their question many ways. <bookmark mark='a'/> Does growth fall when debt "
            "passes a threshold? Try six thresholds, from sixty to a hundred and twenty percent of GDP; average "
            "country by country, or count every year once; start in 1946 or in 1950; keep or drop the early "
            "postwar years they dropped. Forty-eight analyses, each one defensible, sorted from the most negative "
            "gap to the least. <bookmark mark='b'/> The ring marks the analysis closest to their own choices. "
            "<bookmark mark='c'/> The grid underneath shows the other choices each analysis made. The threshold, in "
            "colour, moves the answer most, then the exclusions; the most negative gap combines the highest "
            "threshold, country-by-country averages and their exclusions. <bookmark mark='d'/> "
            f"{round(M['share_neg'] * n)} of the {n} find slower growth above the threshold. But the gap runs from {say_num(M['lo'], 1)} points to "
            f"{say_num(M['hi'], 1)}, and not one of the forty-eight can say whether debt slows growth or slow "
            "growth piles up debt. A robust correlation can still be the wrong answer to a causal question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(rrl))
            vo.wait_until("c")
            self.play(FadeIn(grid), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side, shift=UP * 0.1))
        self.clear_scene()
