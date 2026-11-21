from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Bounds(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Bounds instead of points", r"What do the data say before we assume anything?",
             "Chapter twelve. Bounds instead of points.", lit={1990: r"Manski"}, scale=("household",),
             horizon=("a year",))
        self.idea()
        self.intervals()

    def idea(self):
        rows = VGroup(
            label(r"every point estimate rests on assumptions the data cannot check", font_size=22, color=WHITE),
            label(r"Manski: \ first ask what the data say with none, \ then add them one at a time", font_size=22,
                  color=THEORY),
            label(r"the answer is an interval, \ which narrows as the assumptions grow stronger", font_size=22,
                  color=EST),
            label(r"the law of decreasing credibility: \ stronger assumptions, \ sharper and less believable",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.3)
        tag = published_tag(r"Manski, \ AER P\&P 80(2) (1990); \ Partial Identification of Probability "
                            r"Distributions (2003)", corner=DR, font_size=12)
        hc = history_card(1990, r"Charles Manski", r"bounds on treatment effects with no assumptions: \ what the "
                          r"data alone can say", color=THEORY, width=10.0, font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Every method so far ended with a point and a standard error. Charles Manski asked what we know before "
            "we assume anything. <bookmark mark='a'/> Every point estimate rests on assumptions the data cannot "
            "check. <bookmark mark='b'/> So start with none, see what the data alone say, and add assumptions one "
            "at a time. <bookmark mark='c'/> The answer is an interval, the set of values consistent with the data "
            "and the assumptions made so far, and it narrows as the assumptions grow stronger. <bookmark "
            "mark='d'/> Manski called the trade-off the law of decreasing credibility: the stronger the "
            "assumptions, the sharper the answer and the less anyone should believe it."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def intervals(self):
        B = load("bounds")
        ax = plane([-0.15, 0.85], [0.3, 5.7], center=RIGHT * 1.3 + DOWN * 0.3, x_length=7.8, y_length=5.0,
                   xticks=[-0.1, 0, 0.2, 0.4, 0.6, 0.8], yticks=[], xlabel=r"share attending, \ or the effect "
                   r"on it", xfmt=lambda v: f"{100 * v:.0f}\\%".replace("-", "{-}"), font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0.3), ax.ax.c2p(0, 5.7), color=GREY_D, stroke_width=1.2)

        def bar(y, lo, hi, color, width=7):
            return Line(ax.ax.c2p(lo, y), ax.ax.c2p(hi, y), color=color, stroke_width=width)

        def name(y, text, color):
            return label(text, font_size=17, color=color).next_to(ax.ax.c2p(-0.15, y), LEFT, buff=0.15)

        a1, a0 = B["arms"]["1"], B["arms"]["0"]
        rows = [
            (5.2, a1, DATA, r"subsidized: \ no assumption"),
            (4.6, a0, CONTROL, r"control: \ no assumption"),
            (3.6, B["effect"], ERR, r"the effect: \ no assumption"),
            (2.6, B["mono_effect"], EST, r"the effect: \ missing attend \\ no more than the rest"),
        ]
        bars = VGroup(*[bar(y, lo, hi, c) for y, (lo, hi), c, _ in rows])
        names = VGroup(*[name(y, t, c) for y, _, c, t in rows])
        mar = Dot(ax.ax.c2p(B["naive_effect"], 1.6), radius=0.1, color=MODEL)
        mar_n = name(1.6, r"the effect: \ missing \\ at random", MODEL)
        truth = VGroup(*[Line(ax.ax.c2p(v, y - 0.22), ax.ax.c2p(v, y + 0.22), color=TRUTHC, stroke_width=3)
                         for v, y in ((B["truth"]["1"], 5.2), (B["truth"]["0"], 4.6), (B["true_effect"], 3.6),
                                      (B["true_effect"], 2.6), (B["true_effect"], 1.6))])
        side = label(r"white ticks: \ the truth", font_size=17, color=TRUTHC).to_corner(UR, buff=0.4)
        tag = island_tag(r"simulated: \ the Island's villages", corner=DR, font_size=13)
        miss = 100 * (B["missing"]["1"] + B["missing"]["0"]) / 2
        with self.voiceover(
            "Back to the Island's school experiment, with a complication: attendance records are missing for "
            f"about {miss:.0f} percent of children, and nobody knows why. <bookmark mark='a'/> With no assumption "
            "at all, a missing child might or might not attend, so the subsidized villages' attendance lies "
            f"between {say_pct(a1[0], 0)} and {say_pct(a1[1], 0)}, <bookmark mark='b'/> and the control villages' "
            f"between {say_pct(a0[0], 0)} and {say_pct(a0[1], 0)}. <bookmark mark='c'/> So the effect lies between "
            f"{say_pct(B['effect'][0], 0)} and {say_pct(B['effect'][1], 0)}: the data alone cannot even say the "
            "subsidy helped. <bookmark mark='d'/> Add one assumption most people would accept: the children with "
            "missing records attend no more often than those with records, since registers tend to lose the "
            f"dropouts. Now the effect lies between {say_pct(B['mono_effect'][0], 0)} and "
            f"{say_pct(B['mono_effect'][1], 0)}: positive. <bookmark mark='e'/> The usual analysis assumes the "
            f"records are missing at random and reports a single number, {say_pct(B['naive_effect'], 0)}. It "
            "happens to be close to the truth here, but its attendance rates are not: they are several points too "
            "high, because the missing are mostly the dropouts. <bookmark mark='f'/> The white ticks are the truth, "
            "inside every interval that only assumed what was true."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(Create(bars[k]), FadeIn(names[k]))
            vo.wait_until("e")
            self.play(FadeIn(mar, scale=1.5), FadeIn(mar_n))
            vo.wait_until("f")
            self.play(FadeIn(truth), FadeIn(side))
        self.clear_scene()
