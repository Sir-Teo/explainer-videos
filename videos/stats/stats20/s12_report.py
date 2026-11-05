from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403


class Report(VoiceoverScene):
    def construct(self):
        self.card()
        self.sentences()
        self.page()
        self.integrity()
        self.appendix()

    def card(self):
        card = chapter_card(11, r"Communicating", r"One page, \ one honest sentence", part=PART)
        with self.voiceover("Chapter eleven. Communicating the result."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sentences(self):
        d = load("report")
        bad = VGroup(label(r"three ways to report it badly", font_size=26, color=RES),
                     label(r"``Salt has no effect on blood pressure'' \ (p = 0.81)", font_size=22),
                     label(r"``A non-significant trend toward higher pressure''", font_size=22),
                     label(r"``After adjustment, the effect rose to 0.60 mm Hg per gram''", font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        good = VGroup(label(r"one way to report it well", font_size=26, color=HIT),
                      label(rf"Among US adults not taking BP medicine (2017--18, $n = {d['n']:,}$), each extra gram of", font_size=21),
                      label(rf"sodium on the recall day went with {d['est']:+.2f} mm Hg systolic pressure (95\% CI {d['lo']:+.2f} to {d['hi']:+.2f}).", font_size=21),
                      label(r"A single day's recall is too noisy to detect the 2--3 mm Hg per gram found in trials,", font_size=21),
                      label(r"so this survey neither confirms nor contradicts them.", font_size=21)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        VGroup(bad, good).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(ORIGIN)
        crosses = VGroup(*[Cross(r, stroke_color=RES, stroke_width=2).scale(0.98) for r in bad[1:]])
        with self.voiceover(
            "The analysis is done; now it has to be said. <bookmark mark='a'/> Here are three ways to say it badly. Salt "
            "has no effect on blood pressure: a causal claim, from an absence of evidence. <bookmark mark='b'/> A "
            "non-significant trend toward higher pressure: a phrase that dresses noise up as a finding. <bookmark mark='c'/> "
            "After adjustment, the effect rose to point six: an unplanned, hopelessly imprecise number promoted to a "
            "headline. <bookmark mark='d'/> And one way to say it well: who, when and how many; the estimate in its units, "
            "with its interval; and the one limitation that changes how to read it, stated plainly, with what it means for "
            "the trials."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(bad[0]), FadeIn(bad[1]))
            self.play(Create(crosses[0]))
            vo.wait_until("b")
            self.play(FadeIn(bad[2]), Create(crosses[1]))
            vo.wait_until("c")
            self.play(FadeIn(bad[3]), Create(crosses[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in good], lag_ratio=0.4), run_time=4.0)
        self.wait(1.5)
        self.clear_scene()

    def page(self):
        d = load("report")
        sheet = RoundedRectangle(width=7.4, height=7.4, corner_radius=0.08, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_color="#f3efe6", fill_opacity=1).move_to([-2.6, 0, 0])
        ink = "#1b1f27"
        title = label(r"Sodium and blood pressure in US adults, \ 2017--18", font_size=22, color=ink)
        sec = lambda h, t: VGroup(label(h, font_size=15, color="#8a5a20"), label(t, font_size=13, color=ink)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)  # noqa: E731
        blocks = VGroup(
            sec(r"QUESTION", r"How does systolic pressure vary with usual sodium intake, among adults alike in age, sex, BMI and energy?"),
            sec(r"DATA", rf"NHANES 2017--18; \ {d['n']:,} adults 20+ not on BP medicine; \ design-weighted, \ 15 df."),
            sec(r"FINDING", rf"{d['est']:+.2f} mm Hg per g/day (95\% CI {d['lo']:+.2f} to {d['hi']:+.2f}); \ 64 alternative analyses: \ all near 0."),
            sec(r"BUT", rf"one day's recall: \ reliability {d['reliability']:.2f}, \ about 0.06 given energy; \ corrected: \ $-1.9$ to $+3.1$."),
            sec(r"SO", r"Consistent with no effect and with the trials' 2--3 mm Hg per g. \ The survey cannot decide."),
            sec(r"NOT", r"Evidence that salt is harmless. \ Causal claims rest on randomized trials."),
        )
        for b in blocks:
            for r in b:
                if r.width > 6.6:
                    r.width = 6.6
        blocks.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fig = VGroup()
        ax0 = Line([-0.0, 0, 0], [3.0, 0, 0], color=ink, stroke_width=1.2)
        x = lambda v: (v + 1) / 5 * 3.0  # noqa: E731
        fig.add(ax0, Line([x(d["lo"]), 0.25, 0], [x(d["hi"]), 0.25, 0], color="#b07a1e", stroke_width=4),
                Dot([x(d["est"]), 0.25, 0], radius=0.05, color="#b07a1e"),
                Rectangle(width=x(3) - x(2), height=0.35, stroke_width=0, fill_color="#3a9a5b", fill_opacity=0.35).move_to([(x(2) + x(3)) / 2, 0.25, 0]),
                DashedLine([x(0), -0.05, 0], [x(0), 0.55, 0], color=GREY_C, stroke_width=1),
                *[label(str(v), font_size=11, color=ink).move_to([x(v), -0.16, 0]) for v in (-1, 0, 1, 2, 3, 4)])
        body = VGroup(title, blocks, fig).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        body.move_to(sheet)
        notes = fit_rows(VGroup(
            label(r"the question, \ in the estimand's words", font_size=22, color=SALT),
            label(r"the data, \ and who is excluded", font_size=22, color=NH),
            label(r"the estimate, \ in units, \ with its interval", font_size=22, color=DES),
            label(r"the limitation that changes the reading", font_size=22, color=RES),
            label(r"what it does not show", font_size=22, color=OBS),
            label(r"one figure: \ the estimate beside the trials", font_size=22, color=HIT),
        ), 4.6, 0.42, [4.2, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The full report fits on one page. <bookmark mark='b'/> It starts with the question in the "
            "estimand's own words. <bookmark mark='c'/> Then the data, including who was excluded and why. <bookmark mark='d'/> "
            "Then the finding, in millimetres per gram, with its interval and the sixty-four alternatives. <bookmark mark='e'/> "
            "Then the limitation that changes everything: the reliability of one day's recall, and the corrected interval. "
            "<bookmark mark='f'/> Then what the result does not show. <bookmark mark='g'/> And a single figure: the survey's "
            "estimate beside the trials' range, which says more than any table."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(sheet), FadeIn(title))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                idx = {0: [0], 1: [1], 2: [2], 3: [3, 4], 4: [5]}[k]
                self.play(*[FadeIn(blocks[i]) for i in idx], FadeIn(notes[k]))
            vo.wait_until("g")
            self.play(FadeIn(fig), FadeIn(notes[5]))
        self.wait(1.5)
        self.clear_scene()

    def integrity(self):
        dec = load("explore")["deciles"]
        xs = np.arange(1, 11)
        ys = np.array([r["sbp"] for r in dec])
        A = axes([0.5, 10.5], [117, 125], x_length=5.2, y_length=3.8, xlabel=r"sodium decile", ylabel=r"mean systolic",
                 xticks=[1, 5, 10], yticks=[117, 119, 121, 123, 125], center=[-3.4, 0.2, 0], font_size=18)
        B = axes([0.5, 10.5], [0, 140], x_length=5.2, y_length=3.8, xlabel=r"sodium decile", ylabel=r"mean systolic",
                 xticks=[1, 5, 10], yticks=[0, 40, 80, 120], center=[3.4, 0.2, 0], font_size=18)
        la = VGroup(polyline(A.ax, xs, ys, RES, 3), *[Dot(A.ax.c2p(a, b), radius=0.07, color=RES) for a, b in zip(xs, ys)])
        lb = VGroup(polyline(B.ax, xs, ys, HIT, 3), *[Dot(B.ax.c2p(a, b), radius=0.07, color=HIT) for a, b in zip(xs, ys)])
        ta = label(r"axis from 117: \ drama from noise", font_size=22, color=RES).next_to(A, UP, buff=0.2)
        tb = label(r"axis from 0: \ flat, \ as it is", font_size=22, color=HIT).next_to(B, UP, buff=0.2)
        foot = label(r"Part 1's rule: \ the axis should not manufacture the finding", font_size=24, color=OBS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> The figures need the same honesty as the sentences, Part 1's rules of graphic integrity. "
            "Chapter four's decile means, plotted on an axis from a hundred and seventeen to a hundred and twenty-five, become "
            "a jagged mountain range. A reader sees structure: a peak in the fourth decile, a rise at the top. "
            "<bookmark mark='b'/> On an axis from zero, the same ten numbers are a flat line, which is what they are. Neither "
            "axis is always right; for blood pressure a range of clinical interest is reasonable. <bookmark mark='c'/> But the "
            "axis should never manufacture the finding, and every plot should show its uncertainty."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), Create(la), FadeIn(ta), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(lb), FadeIn(tb), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def appendix(self):
        rows = fit_rows(VGroup(
            label(r"the appendix holds everything else:", font_size=26),
            label(r"the decision log, \ with every count", font_size=24, color=OBS),
            label(r"the analysis plan, \ and every deviation from it", font_size=24, color=SALT),
            label(r"all 64 analyses, \ and the exploratory interaction, \ flagged", font_size=24, color=DES),
            label(r"the checks of chapter six; \ the World's replay of chapter ten", font_size=24, color=WLD),
            label(r"the code, \ and how to rerun it", font_size=24, color=HIT),
        ), 12.4, 0.48, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The page is short because the appendix is long. <bookmark mark='b'/> It holds the decision "
            "log, <bookmark mark='c'/> the analysis plan and any deviation from it, <bookmark mark='d'/> all sixty-four analyses "
            "and the exploratory interaction, clearly labelled, <bookmark mark='e'/> the model checks and the replay on the "
            "World, <bookmark mark='f'/> and the code, which is the subject of the next chapter."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
