from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

REGIME = {"Malthusian": WAGE, "post-Malthusian": GREY_B, "modern": GDP}


class Unified(VoiceoverScene):
    def construct(self):
        card(self, 9, r"One model for the whole story", r"Can one set of equations produce the trap, \ the escape "
             r"and the transition?", "Chapter nine. One model for the whole story.",
             lit={1993: r"Kremer", 2000: r"Galor and Weil", 2011: r"Galor's book"}, scale=("household", "world"),
             horizon=("a century",))
        self.scale_effect()
        self.run()

    def scale_effect(self):
        rows = VGroup(
            label(r"Michael Kremer, \ 1993: \ more people, \ more inventors, \ faster technology", font_size=24),
            label(r"in the Malthusian world, \ faster technology means more people: \ a loop", font_size=23,
                  color=TECH),
            label(r"so population growth itself should speed up, \ for thousands of years", font_size=23, color=POP),
            label(r"it did, \ until the 1960s: \ and regions cut off from others \ (Tasmania) \ fell behind",
                  font_size=22, color=GREY_A),
            label(r"Galor and Weil, \ 2000: \ add the parents' choice between quantity and quality", font_size=23,
                  color=EDU),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kremer, QJE 108(3) (1993); \ Galor and Weil, AER 90(4) (2000)", corner=DR, font_size=13)
        with self.voiceover(
            "Can one model produce the trap, the escape and the transition? Two ideas make it possible. "
            "<bookmark mark='a'/> Michael Kremer argued in 1993 that more people means more potential inventors, so "
            "technology improves faster in bigger populations. <bookmark mark='b'/> In a Malthusian world, better "
            "technology means more people: a loop. <bookmark mark='c'/> So population growth itself should speed up "
            "over thousands of years. <bookmark mark='d'/> It did, until the 1960s, and regions cut off from the "
            "rest, like Tasmania, fell behind. <bookmark mark='e'/> Oded Galor and David Weil added the parents' "
            "choice from chapter eight."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def run(self):
        u = load("unified")
        rows_ = u["rows"]
        yrs = [r["year"] for r in rows_]
        panels = [("y", r"income per head", (0.9, 1.7), [1.0, 1.2, 1.4, 1.6]),
                  ("L", r"population", (0, 7), [0, 2, 4, 6]),
                  ("n", r"children per adult", (0.95, 1.15), [1.0, 1.05, 1.1]),
                  ("e", r"schooling per child", (0, 0.06), [0, 0.02, 0.04])]
        axes = VGroup()
        curves = VGroup()
        for k, (key, name, yr, ticks) in enumerate(panels):
            cx = -3.4 if k % 2 == 0 else 3.0
            cy = 1.15 if k < 2 else -1.95
            ax = plane([1000, 2030], list(yr), center=[cx, cy, 0], x_length=5.6, y_length=2.1,
                       xticks=[1000, 1250, 1500, 1750, 2000], yticks=ticks, ylabel=name, xfmt=lambda v: f"{v:.0f}",
                       yfmt=lambda v: f"{v:g}", font_size=14)
            axes.add(ax)
            segs = VGroup()
            for a, b in zip(rows_, rows_[1:]):
                segs.add(Line(ax.ax.c2p(a["year"], a[key]), ax.ax.c2p(b["year"], b[key]),
                              color=REGIME[a["regime"]], stroke_width=3.5))
            curves.add(segs)
        leg = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.35, color=c, stroke_width=4), label(n, font_size=17, color=c))
                       .arrange(RIGHT, buff=0.1) for n, c in REGIME.items()]).arrange(RIGHT, buff=0.5).to_edge(
            UP, buff=0.12)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Agora runs a small version, one generation at a time, from the year 1000. <bookmark mark='a'/> For "
            "centuries it is Malthusian: income hovers just above subsistence, technology creeps forward, and every "
            "gain becomes more people. <bookmark mark='b'/> As the population grows, technology speeds up, until "
            f"around {u['takeoff_year']} income starts to rise faster than the population can catch it: the "
            "post-Malthusian take-off, with population growing faster than ever. <bookmark mark='c'/> Faster change "
            "makes schooling pay. Parents begin to educate, and fertility, after peaking around "
            f"{u['peak_year']}, falls towards replacement. <bookmark mark='d'/> From then on, gains go to income per "
            "head, not to numbers: modern growth. One set of equations, three eras. The model is a cartoon, its "
            "dates set by its parameters, but its order of events is the one history shows."
        ) as vo:
            self.play(FadeIn(axes), FadeIn(leg), FadeIn(tag))
            n = len(rows_) - 1
            i1 = next(k for k, r in enumerate(rows_) if r["regime"] != "Malthusian")
            i2 = next(k for k, r in enumerate(rows_) if r["regime"] == "modern")
            vo.wait_until("a")
            self.play(*[Create(VGroup(*c[:i1])) for c in curves], run_time=3)
            vo.wait_until("b")
            self.play(*[Create(VGroup(*c[i1:i2])) for c in curves], run_time=3)
            vo.wait_until("c")
            self.play(*[Create(VGroup(*c[i2:n])) for c in curves], run_time=3)
            vo.wait_until("d")
            self.play(Indicate(axes[0], color=GDP, scale_factor=1.03))
        self.clear_scene()
