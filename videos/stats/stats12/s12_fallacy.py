from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Fallacy(VoiceoverScene):
    def construct(self):
        self.card()
        self.galton1886()
        self.both_ways()
        self.treatment()
        self.medicine()
        self.secrist()

    def card(self):
        card = chapter_card(11, r"The regression fallacy", r"Part 5's regression to the mean, \ revisited", lit=(1886,), part=PART)
        with self.voiceover("Chapter eleven. The regression fallacy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def both_ways(self):
        d = load("fallacy")
        rows = [
            cmath(r"\text{fathers above } +1.5\sigma", r":", rf"\text{{mean }} {d['tall_fathers']:+.2f}\sigma \ \to\ \text{{their children }} {d['their_children']:+.2f}\sigma",
                  font_size=30),
            cmath(r"\text{fathers below } -1.5\sigma", r":", rf"\text{{mean }} {d['short_fathers']:+.2f}\sigma \ \to\ \text{{their children }} {d['their_children_s']:+.2f}\sigma",
                  font_size=30),
            cmath(r"\text{children above } +1.5\sigma", r":", rf"\text{{mean }} {d['tall_children']:+.2f}\sigma \ \to\ \text{{their fathers }} {d['their_fathers']:+.2f}\sigma",
                  font_size=30),
            cmath(r"\mathrm{SD}", r":", rf"\text{{fathers}}\ {d['sd_f']:.2f},\quad \text{{children}}\ {d['sd_c']:.2f}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        rows[3][2].set_color(FIT)
        whys = [why(r"tall fathers: \ children closer to average"), why(r"short fathers: \ the same, upward"),
                why(r"read backwards: \ tall children's fathers regress too"), why(r"and the population does not shrink at all")]
        tag = simulated_tag(r"the World: \ 50,000 families", corner=UR)
        intro = label('Selection creates regression toward the mean in either direction', font_size=36)
        with self.voiceover(
            "Part 5 met regression to the mean. With regression in hand, here's how it fools people. "
            "<bookmark mark='a'/> In the World, fathers more than one and a half standard deviations above average have children "
            "only point seven seven above. <bookmark mark='b'/> Short fathers' children are closer to average too. It looks as "
            "if the population is converging on mediocrity, as Galton first feared. <bookmark mark='c'/> But read the data "
            "backwards: the fathers of very tall children are only point seven six above average. Regression goes both ways, "
            "which does not establish a causal shrinking of the population. Causal relationships can still underlie the association. <bookmark mark='d'/> And the spread is approximately one in each generation's own standardized units: nothing is shrinking. Regression to the mean is what imperfect correlation looks like, in "
            "either direction."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=4, top=2.4, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def treatment(self):
        d = load("fallacy")
        A = axes([0, 3], [-3, 0], x_length=5.6, y_length=4.4, ylabel=r"mean test score (raw units; \ population SD $= \sqrt2$)", yticks=[-3, -2, -1, 0], center=[-3.0, -0.3, 0])
        ax = A.ax
        bars = VGroup(
            Rectangle(width=1.0, height=abs(ax.c2p(0, d["worst_t1"])[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=RES, fill_opacity=0.8)
            .move_to(ax.c2p(1, 0), aligned_edge=UP),
            Rectangle(width=1.0, height=abs(ax.c2p(0, d["worst_t2"])[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=FIT, fill_opacity=0.8)
            .move_to(ax.c2p(2, 0), aligned_edge=UP))
        labs = VGroup(label(r"test 1", font_size=22).next_to(bars[0], DOWN, buff=0.15), label(r"test 2", font_size=22).next_to(bars[1], DOWN, buff=0.15),
                      MathTex(f"{d['worst_t1']:.2f}", font_size=26, color=RES).next_to(bars[0], DOWN, buff=0.55),
                      MathTex(f"{d['worst_t2']:.2f}", font_size=26, color=FIT).next_to(bars[1], DOWN, buff=0.55))
        rows = fit_rows(VGroup(
            label(r"the worst 10\% on a noisy test get a ``remedy'' that does nothing", font_size=24),
            MathTex(rf"\text{{``improvement'': }} {d['gain']:+.2f}\ \text{{score units}} = {d['gain_sd']:.2f}\ \text{{test SD}}", font_size=30, color=OBS),
            label(r"luck was part of why they scored so low; \ it does not repeat", font_size=24, color=GREY_A),
            label(r"the cure: \ a randomized control group, \ selected the same way (Part 13)", font_size=24, color=FIT),
            label(r"Kahneman's flight instructors: \ praise after a great landing ``fails'', \ criticism after a bad one ``works''", font_size=22,
                  color=GREY_A),
        ), 5.8, 0.36, [3.6, -0.3, 0])
        tag = simulated_tag(r"simulated: \ 10,000 students", corner=DR)
        with self.voiceover(
            "The fallacy has a costly form. <bookmark mark='a'/> Give ten thousand students a noisy test. Take the worst ten "
            "percent, give them a remedy that does absolutely nothing, and test them again. <bookmark mark='b'/> Their average "
            "rises by one point three raw score units, about point nine two standard deviations of a test score. It looks like a spectacular success. <bookmark mark='c'/> But part of "
            "why they scored so badly the first time was bad luck on the day, and luck doesn't repeat. "
            "<bookmark mark='d'/> A direct way to handle it is a control group, chosen the same way and randomly denied "
            "the remedy. Then both groups regress equally in expectation, and the difference is the effect. <bookmark mark='e'/> Daniel "
            "Kahneman told of flight instructors convinced that praise after a great landing made pilots worse and criticism "
            "after a bad one made them better: regression to the mean, both times."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], UP), FadeIn(labs[0]), FadeIn(labs[2]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], UP), FadeIn(labs[1]), FadeIn(labs[3]), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def secrist(self):
        hc = history_card(1933, r"Horace Secrist, \ \emph{The Triumph of Mediocrity in Business}", r"468 pages showing that firms with the best "
                          r"and worst profits drift toward the average over time: \ evidence, \ he argued, \ of competition levelling business",
                          color=GREY_B, width=9.6, font_size=24).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"Harold Hotelling's review (\emph{JASA}, 1933): \ the result is a statistical necessity, \ ``and proves nothing''",
                  font_size=24, color=OBS),
            label(r"the same sorting, \ read backwards in time, \ shows divergence", font_size=24),
            label(r"sports' ``sophomore slump'', \ ``hot'' fund managers, \ the ``Sports Illustrated jinx'': \ the same arithmetic", font_size=22,
                  color=GREY_A),
        ), 12.6, 0.34, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The most famous casualty was Horace Secrist, a professor of statistics, whose 1933 book, The "
            "Triumph of Mediocrity in Business, spent four hundred and sixty-eight pages showing that the most and least "
            "profitable firms drift toward the average over time, and concluded that competition was levelling business. "
            "<bookmark mark='b'/> Harold Hotelling's review pointed out that the result was a statistical necessity, and proved "
            "nothing. <bookmark mark='c'/> Sorting firms by later profits and looking backward would show them diverging. "
            "<bookmark mark='d'/> The sophomore slump in sport, the fading of last year's star fund manager: the same "
            "arithmetic, mistaken for a cause. Whenever a group is selected for being extreme, expect it to look less extreme "
            "next time, and ask for a comparison group before believing in a cause."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def galton1886(self):
        T = np.asarray(museum.GALTON_TABLE)
        P, C = np.asarray(museum.GALTON_PARENT), np.asarray(museum.GALTON_CHILD)
        xs, ys = [], []
        for i, p_ in enumerate(P):
            for j, c in enumerate(C):
                xs += [p_] * int(T[i, j])
                ys += [c] * int(T[i, j])
        xs, ys = np.asarray(xs), np.asarray(ys)
        b, a = np.polyfit(xs, ys, 1)
        A = axes([63.5, 73.5], [61, 74.5], x_length=6.0, y_length=5.0, xlabel=r"mid-parent (inches)", ylabel=r"child (inches)",
                 xticks=[64, 66, 68, 70, 72], yticks=[62, 66, 70, 74], center=[-3.0, -0.3, 0])
        ax = A.ax
        cells = VGroup()
        for i, p_ in enumerate(P):
            for j, c in enumerate(C):
                if T[i, j] > 0:
                    cells.add(Dot(ax.c2p(p_, c), radius=0.028 * np.sqrt(T[i, j]), color=DATA, fill_opacity=0.7))
        diag = DashedLine(ax.c2p(63.5, 63.5), ax.c2p(73.5, 73.5), color=GREY_B, stroke_width=1.5)
        ln = fit_line(ax, a, b, 63.5, 73.5)
        rows = fit_rows(VGroup(
            label(r"Galton's own table, \ 928 children (1886)", font_size=24, color=DATA),
            MathTex(rf"\hat b = {b:.3f}", font_size=32, color=FIT),
            label(r"Galton's estimate: \ about $\tfrac23$", font_size=24, color=GREY_A),
            label(r"the dashed line: \ children exactly like their parents", font_size=22, color=GREY_A),
            label(r"he called it ``regression towards mediocrity'', \ and the word stuck to the method", font_size=22, color=OBS),
        ), 5.0, 0.32, [4.0, -0.3, 0])
        src = historical_tag(r"Galton (1886), \ via HistData", corner=DR)
        with self.voiceover(
            "And here's where the word regression came from. <bookmark mark='a'/> Galton's own table of nine hundred and "
            "twenty-eight children and their parents, from 1886, each dot sized by its count. <bookmark mark='b'/> The least "
            "squares slope is point six five. Galton estimated about two thirds, drawing ellipses by hand. "
            "<bookmark mark='c'/> If children were exactly like their parents, the points would follow the dashed diagonal. "
            "They follow a flatter line instead: regression toward the mean. <bookmark mark='d'/> Galton called it regression "
            "towards mediocrity, and the name of the phenomenon became the name of the method."
        ) as vo:
            self.play(FadeIn(A), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cells, lag_ratio=0.01), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(Create(diag), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def medicine(self):
        rows = fit_rows(VGroup(
            label(r"regression to the mean in medicine", font_size=30, color=OBS),
            label(r"patients enrol in a trial because their blood pressure is high \emph{today}", font_size=24),
            label(r"next month, \ untreated, \ it is lower on average: \ partly real variation, \ partly regression", font_size=24),
            label(r"a before--after comparison credits the drug with all of it", font_size=24, color=MISS),
            label(r"the placebo arm of a randomized trial regresses by the same amount in expectation, \ and subtracts it out", font_size=24, color=FIT),
            label(r"Bland \& Altman, \ ``Regression towards the mean'' (\emph{BMJ}, 1994)", font_size=22, color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In medicine the stakes are concrete. <bookmark mark='b'/> Patients often enrol in a trial "
            "because a measurement, say blood pressure, is high on the day they're tested. <bookmark mark='c'/> A month later, "
            "even untreated, it's lower on average, partly because the high reading was partly chance. <bookmark mark='d'/> A "
            "before-and-after comparison credits the drug with all of that fall. <bookmark mark='e'/> The placebo arm of a "
            "randomized trial regresses by the same amount in expectation, so comparing arms subtracts it out. <bookmark mark='f'/> Martin "
            "Bland and Douglas Altman's short note on this, in the British Medical Journal in 1994, is still worth reading."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
