from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Circular(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.from_nothing()
        self.fresh()

    def card(self):
        card = chapter_card(8, r"Choosing voxels by the answer", r"How can a correlation be too good?",
                            lit={2009: r"``voodoo correlations''"}, part=PART, scale=("brain", "person"),
                            marr=("how",))
        with self.voiceover(
            "Chapter eight. Choosing voxels by the answer."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def puzzle(self):
        head = heading(r"2009: \ correlations that were too good")
        v = load("voodoo")
        A = axes([-2.4, 2.4], [-2.4, 2.4], x_length=4.2, y_length=4.2, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 xlabel=r"a person's score on a questionnaire", ylabel=r"activity in one brain region",
                 center=[-4.2, -0.5, 0])
        x, y = v["score"], v["best_activation"]
        x, y = (x - x.mean()) / x.std(), (y - y.mean()) / y.std()
        dots = VGroup(*[Dot(A.ax.c2p(float(a), float(b)), radius=0.09, color=BLOOD) for a, b in zip(x, y)])
        rl = label(rf"$r = {r2(v['best_r'])}$", font_size=40, color=BLOOD).move_to(A.ax.c2p(-1.3, 1.9))
        rows = rows_of([
            (r"a dozen or two people, \ a scanner, \ a questionnaire", WHITE),
            (r"reported: \ activity in one region goes with jealousy, anxiety, or empathy at $r = 0.8$ or more",
             BLOOD),
            (r"but neither measure is that reliable: \ such a correlation should not be possible", THRESH),
            (r"more than half the papers surveyed had picked their voxels by the correlation they reported",
             DATA),
        ], 6.0, 29, 0.3).move_to([3.6, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.VUL_2009.cite)
        tag = psyche_tag(r"the scatter: simulated (Psyche)")
        with self.voiceover(
            "The second way a map misleads is quieter, and in 2009 it caused the loudest row the field has "
            "had. Edward Vul and three colleagues had been reading papers in social neuroscience, and "
            "something didn't add up. <bookmark mark='a'/> The typical study scanned a dozen or two people, "
            "gave them a questionnaire, and reported that activity in some region went with a trait, "
            "jealousy, anxiety, empathy, with a correlation of point eight or higher. <bookmark mark='b'/> "
            "You know from Part 3 that a correlation between two noisy measures has a ceiling, set by "
            "their reliabilities. These were above the ceiling. They were too good to be true. "
            "<bookmark mark='c'/> So Vul's group wrote to the authors and asked how the numbers had been "
            "computed. <bookmark mark='d'/> More than half said, in effect: we correlated every voxel "
            "with the questionnaire, kept the voxels that passed a threshold, and reported the correlation "
            "in those. The draft of their paper was called voodoo correlations. Here's why the name stuck."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.1), FadeIn(rl), FadeIn(rows[0]), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def from_nothing(self):
        v = load("voodoo")
        head = heading(r"The same analysis, \ on a brain of pure noise")
        A = axes([-1, 1], [0, 0.13], x_length=6.4, y_length=3.6, xticks=[-1, -0.5, 0, 0.5, 1], yticks=[],
                 xfmt=lambda t: f"{t:.1f}", xlabel=r"a voxel's correlation with the score", ylabel=r"",
                 center=[-3.3, -0.4, 0])
        ax = A.ax
        h = hist(ax, v["edges"], v["hist"], NOISE, opacity=0.7)
        cut = DashedLine(ax.c2p(v["threshold"], 0), ax.c2p(v["threshold"], 0.125), color=THRESH, stroke_width=3)
        cut_l = label(rf"keep $r > {v['threshold']:.1f}$", font_size=25, color=THRESH).next_to(ax.c2p(v["threshold"], 0.125), UP, buff=0.05)
        hl = label(rf"{fmt_int(v['voxels'])} voxels, \ none related to the score", font_size=25, color=NOISE).next_to(A, UP, buff=0.5).shift(LEFT * 0.6)
        rows = rows_of([
            (rf"{v['subjects']} simulated people; \ their scores and their scans are unrelated", WHITE),
            (rf"{v['selected']} voxels pass the threshold, \ by luck alone", THRESH),
            (rf"their average correlation: \ {r2(v['r_same'])}", BLOOD),
            (r"The threshold did not find a strong effect. \ It manufactured one.", P.ACCENT),
        ], 4.9, 30, 0.32).move_to([4.5, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: noise (Psyche)")
        with self.voiceover(
            f"Take {v['subjects']} simulated people. Give each a score, and a scan of "
            f"{v['voxels']:,} voxels. Scores and scans are pure noise, unrelated by construction. "
            "<bookmark mark='a'/> Correlate every voxel with the score. The correlations pile up around "
            "zero, as they should, but with only sixteen people they spread a long way. "
            f"<bookmark mark='b'/> Now keep the voxels whose correlation is above {v['threshold']:.1f}, "
            "which is about the usual one in a thousand. <bookmark mark='c'/> "
            f"{v['selected']} voxels pass. <bookmark mark='d'/> And their average correlation with the "
            f"score is {v['r_same']:.2f}. It couldn't be anything else. You kept only the voxels above "
            f"{v['threshold']:.1f}, so their average is above {v['threshold']:.1f}. "
            "<bookmark mark='e'/> The selection didn't find a strong relationship. It made one, out of "
            "nothing. And notice that the number carries no information about the brain at all. It's set "
            "by the threshold and the number of people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(h, lag_ratio=0.02), FadeIn(hl), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(cut_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def fresh(self):
        v = load("voodoo")
        k = archive.VUL_2009.data
        head = heading(r"The test, and the cure: \ fresh data")
        cols = [(r"nothing there", v["mean_same"], v["mean_fresh"]),
                (rf"a real effect of {v['signal_true']:.1f} in a few voxels", v["signal_same"], v["signal_fresh"])]
        table = VGroup()
        hx = [-3.6, 1.0, 4.9]
        table.add(label(r"in the data used to choose", font_size=30, color=BLOOD).move_to([hx[1], 2.2, 0]))
        table.add(label(r"in new scans", font_size=30, color=MODEL).move_to([hx[2], 2.2, 0]))
        for i, (name, same, fr) in enumerate(cols):
            y = 1.15 - 1.25 * i
            table.add(wrapped_label(name, 5.6, 33, WHITE).move_to([hx[0], y, 0]))
            table.add(label(r2(same), font_size=64, color=BLOOD).move_to([hx[1], y, 0]))
            table.add(label(r2(fr) if abs(fr) >= 0.005 else r".00", font_size=64, color=MODEL).move_to([hx[2], y, 0]))
        keep_in_frame(table)
        rows = rows_of([
            (r"choose the voxels in one set of scans, \ measure the correlation in another: \ the inflation "
             r"is gone", MODEL),
            (rf"another count that year: \ {k['circular']} of {k['papers']} imaging papers in five leading "
             r"journals made the same circle somewhere", DATA),
            (r"The regions may be real. \ The published numbers were not measurements of them.", P.ACCENT),
        ], 12.6, 29, 0.22).move_to([0, -2.25, 0])
        src = published_tag(archive.VUL_2009.cite)
        tag = psyche_tag(r"simulated, 200 runs each (Psyche)")
        with self.voiceover(
            "There's a clean test for this, and it's also the cure. Scan the same people again, and "
            "measure the correlation in the new scans, in the voxels you chose from the old ones. "
            f"<bookmark mark='a'/> When nothing is there, the chosen voxels show {v['mean_same']:.2f} in "
            "the data they were chosen from, and zero in fresh data. <bookmark mark='b'/> Now put a real "
            f"effect in: a true correlation of {v['signal_true']:.1f}, in a few of the voxels. The "
            f"circular analysis reports {v['signal_same']:.2f} again. It gives nearly the same number "
            "whether the truth is nothing or something. Fresh data gives a small number, because most of "
            "the chosen voxels were still noise. <bookmark mark='c'/> So the rule is one you already know, "
            "from Part 4. Don't test a hypothesis on the data that suggested it. Choose with one half, "
            f"measure with the other. <bookmark mark='d'/> A second group counted that year. Of "
            f"{k['papers']} imaging papers in five leading journals, {k['circular']} had the same circle "
            "in at least one analysis. <bookmark mark='e'/> The authors of the criticized papers objected "
            "that their regions were real. Many probably are. But the size of an effect is a measurement, "
            "and those numbers weren't measurements."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(table[0]), FadeIn(table[1]))
            vo.wait_until("a")
            self.play(FadeIn(table[2]), FadeIn(table[3]), FadeIn(table[4]))
            vo.wait_until("b")
            self.play(FadeIn(table[5]), FadeIn(table[6]), FadeIn(table[7]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()
