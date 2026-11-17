from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Hundred(VoiceoverScene):
    def construct(self):
        self.card()
        self.project()
        self.argument()
        self.model()

    def card(self):
        card = chapter_card(9, r"One hundred replications", r"What happens when a hundred published studies are "
                            r"run again?", lit={2015: r"the Reproducibility Project"}, part=PART,
                            scale=("group", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter nine. One hundred replications."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def project(self):
        d = archive.OSC_2015.data
        n = d["studies"]
        head = heading(rf"2015: \ {n} published studies, each run again")
        left = tiles(n, round(n * d["original_significant"]), ORIG, size=0.31, buff=0.07, cols=10)
        right = tiles(n, round(n * d["replication_significant"]), REP, size=0.31, buff=0.07, cols=10)
        left.move_to([-4.95, 0.35, 0])
        right.move_to([-0.45, 0.35, 0])
        lcap = VGroup(label(r"the originals", font_size=28, color=WHITE),
                      label(rf"{pct(d['original_significant'])} significant", font_size=34, color=ORIG))
        rcap = VGroup(label(r"the replications", font_size=28, color=WHITE),
                      label(rf"{pct(d['replication_significant'])} significant", font_size=34, color=REP))
        for cap, g in ((lcap, left), (rcap, right)):
            cap.arrange(DOWN, buff=0.08).next_to(g, DOWN, buff=0.25)
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.2, color=GREY_B, stroke_width=4)
        side = VGroup(
            VGroup(label(r"effects", font_size=24, color=GREY_A),
                   label(r"about half the size", font_size=30, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(wrapped_label(r"original effect inside the replication's margin of error", 4.6, 23, GREY_A),
                   label(pct(d["original_in_replication_ci"]), font_size=30, color=WHITE)).arrange(
                       DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(wrapped_label(r"judged a success by the replicating team", 4.6, 23, GREY_A),
                   label(pct(d["rated_replicated"]), font_size=30, color=WHITE)).arrange(
                       DOWN, aligned_edge=LEFT, buff=0.06),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        side.move_to([2.2, 0.35, 0], aligned_edge=LEFT)
        src = published_tag(archive.OSC_2015.cite)
        with self.voiceover(
            "Arguments about methods can go on for ever. What settles them is data, and the field went and got "
            "some. A large collaboration of psychologists took "
            f"a hundred studies published in three leading journals and ran each of them again, once, using the "
            "original materials where they could get them, with a sample chosen to give a good chance of "
            f"detecting the effect that had been reported. <bookmark mark='a'/> Of the originals, "
            f"{100 * d['original_significant']:.0f} per cent had reported a significant result. "
            f"<bookmark mark='b'/> Of the replications, {100 * d['replication_significant']:.0f} per cent did. "
            "<bookmark mark='c'/> The effects that the replications found were, on average, about half the size "
            "of the ones in print. <bookmark mark='d'/> By a second yardstick, whether the original effect fell "
            f"inside the replication's margin of error, {100 * d['original_in_replication_ci']:.0f} per cent "
            f"passed. And when the teams were asked for their own verdict, they said that "
            f"{100 * d['rated_replicated']:.0f} per cent had replicated. Whichever yardstick you prefer, fewer "
            "than half. The result was published in Science in 2015, and it turned an argument about methods "
            "into a public one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(left, lag_ratio=0.01), FadeIn(lcap[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(lcap[1], scale=1.2))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(right, lag_ratio=0.01), FadeIn(rcap), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(side[1], shift=UP * 0.1))
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def argument(self):
        head = heading(r"What does 36\% mean? \ The exchange of 2016")
        a = VGroup(
            label(r"the critique", font_size=34, color=ORIG),
            wrapped_label(r"Some replications differed from the originals. \ Chance alone makes some replications "
                          r"fail. \ ``The data are consistent with the opposite conclusion.''", 6.1, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        b = VGroup(
            label(r"the reply", font_size=34, color=REP),
            wrapped_label(r"The critique's own estimates rest on choices that can be disputed. \ Optimistic and "
                          r"pessimistic readings are both possible, and neither is yet warranted.", 6.1, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        pair = VGroup(a, b).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.95, 0])
        agreed = VGroup(
            label(r"What neither side disputes", font_size=34, color=P.ACCENT),
            wrapped_label(r"A single replication does not settle a single finding. \ And the effects in print "
                          r"are too big: \ about half survives, in this project and in the ones that followed.",
                          12.2, 29, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.75)
        src = published_tag(rf"{archive.OSC_2015.cite}; \ and the exchange in the same journal a year later")
        with self.voiceover(
            "It didn't go unanswered, and the answer deserves a hearing. <bookmark mark='a'/> The next year "
            "a critique appeared in the same journal. Some of the replications, it said, had differed from the "
            "originals in ways that could matter, in whom they tested and how. And even "
            "a perfectly true finding will fail some replications by chance alone. Allow for those two things, "
            "the critics argued, and the data are consistent with the opposite conclusion: that reproducibility "
            "is high. <bookmark mark='b'/> The project's authors replied that the critique's own numbers "
            "rested on disputable choices, and that both the optimistic and the pessimistic reading were "
            "possible, and neither was yet warranted. <bookmark mark='c'/> Notice what the two sides share. "
            "Nobody claims that one failed replication proves a finding false; a single study settles "
            "nothing, in either direction. And nobody disputes the second number. The effects in print are too "
            "big. About half survives, here and in the projects that followed. So let's stop asking what "
            "share of psychology is true, and ask a question the lab can answer. What kind of literature "
            "produces numbers like these?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(b, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(agreed, shift=UP * 0.15))
        self.clear_scene()

    def model(self):
        d = load("rpp")
        near, osc = d["nearest"], d["osc"]
        head = heading(r"A literature that is mostly true, and mostly fails to replicate")
        recipe = wrapped_label(rf"The recipe: \ one hypothesis in {round(1 / near['prior'])} is true, with an "
                               rf"effect of {near['d']}; \ {d['n']} people a group; \ only significant results are "
                               r"printed; \ each is then run again, with a sample planned from the printed effect.",
                               12.6, 26, GREY_A).next_to(head, DOWN, buff=0.3)
        nums = VGroup(
            big_number(pct(near["true_share_published"]), r"of the printed findings are true", TRUTH, font_size=64,
                       width=3.6, cap_size=24),
            big_number(pct(near["rate"]), r"of the replications are significant", REP, font_size=64, width=3.6,
                       cap_size=24),
            big_number(r2(near["ratio"]), r"replication effect, as a share of the printed one", ORIG, font_size=64,
                       width=3.6, cap_size=24),
        ).arrange(DOWN, buff=0.32).move_to([-4.6, -1.0, 0])
        real = VGroup(label(rf"the project: \ {pct(osc['replication_significant'])}", font_size=24, color=GREY_A),
                      label(rf"the project: \ about {r2(osc['effect_ratio'])}", font_size=24, color=GREY_A))
        real[0].next_to(nums[1], RIGHT, buff=0.3)
        real[1].next_to(nums[2], RIGHT, buff=0.3)
        # the grid: replication rate by (share of hypotheses true, size of the true effect)
        priors, ds = sorted({g["prior"] for g in d["grid"]}), sorted({g["d"] for g in d["grid"]})
        cell = 1.15
        grid = VGroup()
        for g in d["grid"]:
            i, j = priors.index(g["prior"]), ds.index(g["d"])
            is_near = g["prior"] == near["prior"] and g["d"] == near["d"]
            sq = Square(cell, stroke_color=(WHITE if is_near else BACKGROUND), stroke_width=4 if is_near else 3,
                        fill_color=interpolate_color(ManimColor("#1B2333"), ManimColor(REP), g["rate"]),
                        fill_opacity=1).move_to([j * cell, -i * cell, 0])
            grid.add(VGroup(sq, label(pct(g["rate"]), font_size=28, color=WHITE).move_to(sq)))
        grid.move_to([3.6, -1.35, 0])
        gl, gt = grid.get_left()[0], grid.get_top()[1]
        rows_l = VGroup(*[label(rf"1 in {round(1 / p_)} true", font_size=22, color=GREY_A).next_to(
            [gl, gt - (i + 0.5) * cell, 0], LEFT, buff=0.15) for i, p_ in enumerate(priors)])
        cols_l = VGroup(*[label(rf"$d = {v}$", font_size=22, color=GREY_A).next_to(
            [gl + (j + 0.5) * cell, gt, 0], UP, buff=0.12) for j, v in enumerate(ds)])
        gcap = label(r"share of replications that are significant", font_size=22, color=GREY_A).next_to(
            VGroup(grid, cols_l), UP, buff=0.15)
        table = VGroup(grid, rows_l, cols_l, gcap)
        tag = note(r"simulated: the false-positive lab; \ 60,000 hypotheses in each cell").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Build one. <bookmark mark='a'/> Suppose one hypothesis in four that psychologists test is true, "
            f"with an effect of {near['d']}. Thirty people a group, which was ordinary. Print only what's "
            "significant. Then replicate every printed finding, choosing the sample as the project did, from the "
            "effect in print. <bookmark mark='b'/> In this literature, "
            f"{100 * near['true_share_published']:.0f} per cent of the printed findings are true. Four in five. "
            f"<bookmark mark='c'/> And {100 * near['rate']:.0f} per cent replicate. <bookmark mark='d'/> At "
            f"{100 * near['ratio']:.0f} per cent of the printed size. Those are close to the project's numbers, "
            "from a literature in which nobody cheated and most findings are real. How? You've seen both "
            "halves. The printed effects are inflated, by the winner's curse. So a replication planned from the "
            "printed effect is too small for the true one, and misses it. A low replication rate doesn't mean "
            "that most findings are false. <bookmark mark='e'/> But don't take comfort too quickly. Change the "
            "recipe and the rate moves from under a fifth to nearly two thirds, and the project's numbers can't "
            "tell you which recipe is ours. One replication rate has two unknowns behind it: how often "
            "psychologists test true ideas, and how big the true effects are. It measures a literature's power "
            "and its filter as much as its truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(recipe))
            vo.wait_until("b")
            self.play(FadeIn(nums[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(nums[1], shift=UP * 0.15), FadeIn(real[0]))
            vo.wait_until("d")
            self.play(FadeIn(nums[2], shift=UP * 0.15), FadeIn(real[1]))
            vo.wait_until("e")
            self.play(FadeIn(table, lag_ratio=0.05), run_time=2.5)
        self.clear_scene()
