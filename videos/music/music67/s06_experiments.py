from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Experiments(SoundScene):
    def construct(self):
        chapter(self, 5, r"Experiments and their literatures", r"How can a field believe an effect that is not there?")
        self.mechanism()
        self.funnel()
        self.numbers()
        self.phack()
        self.remedies()

    # ------------------------------------------------------------------
    def mechanism(self):
        items = [
            (r"small studies: \ 30 people a group measures an effect of 0.1 standard deviations with an error of 0.26", WHITE),
            (r"selection: \ journals, \ and authors, \ prefer results that cross $p < 0.05$", WHITE),
            (r"so the published studies are the lucky ones: \ the first to cross is usually an overestimate \ (the winner's curse)", WHITE),
            (r"Monochord simulates such a literature: \ a true effect of 0.1, \ 120 studies, \ the significant ones published, \ others mostly not", TUNE),
        ]
        rows_scene(self, r"how a literature misleads", items,
                   "How can a field believe an effect that is not there, or much smaller than it seems? <bookmark mark='b'/> Small "
                   "studies: thirty people a group measure an effect of a tenth of a standard deviation with an error more than "
                   "twice as large. <bookmark mark='c'/> Selection: journals, and authors, prefer results that cross the line of "
                   "significance. <bookmark mark='d'/> So the published studies are the lucky ones, and the first to cross is usually "
                   "an overestimate: the winner's curse. <bookmark mark='e'/> Monochord simulates such a literature, with Statistics, "
                   "Built's tools: a true effect of a tenth, a hundred and twenty studies, the significant ones published and the "
                   "others mostly not.", marks="bcde")

    # ------------------------------------------------------------------
    def funnel(self):
        d = load("meta")
        est, se, pub = np.array(d["est"]), np.array(d["se"]), np.array(d["published"])
        ax = frame_axes(width=7.0, height=4.2, xlo=-1.0, xhi=1.6, ylo=0, yhi=1 / se.min() * 1.05, center=DOWN * 0.3 + LEFT * 1.6)
        ticks = VGroup()
        for x in (-1.0, -0.5, 0.0, 0.5, 1.0, 1.5):
            ticks.add(label(f"{x:g}", font_size=11, color=GREY_A).move_to(ax.to(x, 0) + DOWN * 0.16))
        for y in (0, 2, 4, 6, 8):
            if y <= 1 / se.min() * 1.05:
                ticks.add(label(f"{y:g}", font_size=11, color=GREY_A).move_to(ax.to(-1.0, y) + LEFT * 0.18))
        ax.add(ticks)
        pr = 1 / se
        dots_un = VGroup(*[Dot(ax.to(e, p), radius=0.05, color=GREY_D) for e, p, k in zip(est, pr, pub) if not k])
        dots_pub = VGroup(*[Dot(ax.to(e, p), radius=0.06, color=TUNE) for e, p, k in zip(est, pr, pub) if k])
        true = DashedLine(ax.to(d["true"], 0), ax.to(d["true"], pr.max()), color=WHITE, stroke_width=2)
        ys = np.linspace(0.5, pr.max(), 40)
        line = VMobject(stroke_color=EAR, stroke_width=2).set_points_as_corners([ax.to(1.96 / y, y) for y in ys if 1.96 / y < 1.6])
        xl = label(r"estimated effect \ (standard deviations)", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"precision \ (1 / standard error): \ big studies at the top", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(r"grey: \ unpublished", font_size=16, color=GREY_B), label(r"gold: \ published", font_size=16, color=TUNE),
                      label(r"red: \ the edge of significance", font_size=16, color=EAR), label(r"white: \ the true effect", font_size=16, color=WHITE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        head = label(r"a funnel with a bite out of it", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Plot each study's estimate against its precision: a funnel, wide at the bottom where studies are small, narrow at "
            "the top. <bookmark mark='a'/> All one hundred and twenty studies scatter symmetrically around the true effect. "
            "<bookmark mark='b'/> Now keep only the published ones. The small studies that survive are those that happened to "
            "land right of the red line, in the region selected by this simulation's significance rule; the funnel's lower left is missing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(side), Create(true), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(dots_un), FadeIn(dots_pub), run_time=1.2)
            vo.wait_until("b")
            self.play(dots_un.animate.set_opacity(0.08), run_time=1.0)
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("meta")
        rows = [(r"the true effect", d["true"], GREY_A), (r"the first published significant study", d["first"]["est"], EAR),
                (r"pooled, \ the published studies", d["fe_published"], BLUE), (r"pooled, \ all 120 studies \ (unseeable in practice)", d["fe_all"], TUNE),
                (r"one large, \ preregistered replication \ (2,000 a group)", d["replication"]["est"], TUNE)]
        top = max(r[1] for r in rows)
        g = VGroup()
        for name, v, col in rows:
            g.add(VGroup(label(name, font_size=18, color=col), Rectangle(width=max(0.03, 4.6 * v / top), height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85),
                         label(f"{v:.2f}", font_size=17, color=WHITE)))
        g.arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(LEFT * 1.2 + DOWN * 0.2)
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(g, LEFT).shift(RIGHT * 5.4)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        baseline = min(r[1].get_left()[0] for r in g)
        for r in g:
            r[1].shift(RIGHT * (baseline - r[1].get_left()[0]))
            r[2].next_to(r[1], RIGHT, buff=0.2)
        g.scale(min(1.0, 12.6 / g.width)).move_to(DOWN * 0.2)
        eg = d["egger"]
        note = label(rf"Egger's test for the missing corner: \ intercept {eg['intercept']:.2f}, \ p = {eg['p']:.2f}; \ PET's estimate at infinite precision {eg['slope']:.2f}", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"what each reader would believe", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"What would a reader believe? <bookmark mark='a'/> The first published significant study, {say(d['first']['n'])} "
            f"people a group, found an effect of {say(d['first']['est'], 2)}, more than eight times the truth. "
            f"<bookmark mark='b'/> Pooling all {say(d['n_published'])} published studies gives {say(d['fe_published'], 2)}, still "
            f"more than double. Pooling all hundred and twenty, which no reader can see, gives {say(d['fe_all'], 2)}. "
            f"<bookmark mark='c'/> One large preregistered replication finds {say(d['replication']['est'], 2)}. Egger's test, "
            f"which looks for the missing corner, gives p of {say(eg['p'], 2)}: suggestive, not conclusive, from {say(d['n_published'])} "
            "studies; and the regression it rests on estimates the effect at infinite precision as "
            f"{say(eg['slope'], 2)}, near the truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]), FadeIn(g[3]))
            vo.wait_until("c")
            self.play(FadeIn(g[4]), FadeIn(note))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def remedies(self):
        items = [
            (r"preregistration: \ say the hypothesis, \ the sample and the analysis before collecting data", WHITE),
            (r"registered reports: \ the journal accepts the study before the results exist", WHITE),
            (r"power: \ plan the sample for the effect you expect to be small \ (next chapter)", WHITE),
            (r"replication, \ many labs at once, \ and meta-analysis that models the selection", WHITE),
            (r"music psychology has increasingly adopted all four since the Mozart effect", TUNE),
        ]
        rows_scene(self, r"remedies", items,
                   "The remedies are known. <bookmark mark='b'/> Preregistration: state the hypothesis, the sample and the analysis "
                   "before collecting data. <bookmark mark='c'/> Registered reports: the journal accepts the study before the results "
                   "exist, so it cannot prefer the lucky ones. <bookmark mark='d'/> Power: plan the sample for the effect you expect, "
                   "which is usually small. <bookmark mark='e'/> Replication, by many laboratories at once, and meta-analysis that "
                   "models the selection. <bookmark mark='f'/> Music psychology has increasingly taken up all four since the Mozart effect.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def phack(self):
        d = load("phack")["rates"]
        rows = [("none", r"one planned test"), ("A", r"choose among two measures and their mean"), ("B", r"add 10 people a group if not yet significant"),
                ("C", r"control for gender, \ or for its interaction"), ("D", r"compare any two of three conditions"), ("ABCD", r"all of these together")]
        top = max(d.values())
        g = VGroup()
        for k, name in rows:
            v = d[k]
            g.add(VGroup(label(name, font_size=17, color=WHITE), Rectangle(width=max(0.03, 4.4 * v / top), height=0.38, stroke_width=0, fill_color=EAR if k != "none" else TUNE, fill_opacity=0.85),
                         label(rf"{100 * v:.0f}\%", font_size=17, color=WHITE)))
        g.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(LEFT * 1.2 + DOWN * 0.2)
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(g, LEFT).shift(RIGHT * 5.6)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        baseline = min(r[1].get_left()[0] for r in g)
        for r in g:
            r[1].shift(RIGHT * (baseline - r[1].get_left()[0]))
            r[2].next_to(r[1], RIGHT, buff=0.2)
        g.scale(min(1.0, 12.6 / g.width)).move_to(DOWN * 0.2)
        note = label(r"no true effect anywhere: \ the share of studies that find one at $p < 0.05$ \ (Simmons, \ Nelson and Simonsohn, \ 2011)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"how choices make effects", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Selection by journals is one road to a false result; choices by authors are another. Joseph Simmons, Leif Nelson "
            "and Uri Simonsohn simulated studies with no effect at all. <bookmark mark='a'/> With one planned test, "
            f"{say(round(100 * d['none']))} per cent find an effect, as they should. <bookmark mark='b'/> Each reasonable-looking "
            "choice raises it: two measures to pick from, ten more people if the first look fails, a covariate, a different "
            f"comparison. <bookmark mark='c'/> All together, {say(round(100 * d['ABCD']))} per cent of studies of nothing find "
            "something. Preregistration makes planned choices visible and helps distinguish confirmatory analyses from exploration."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g[1:5]], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(g[5]))
        self.wait(0.6)
        self.clear_scene()
