from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403

COLS = {"capital goods": ARCH, "cars and parts": FISH, "consumer goods": CLOTH}


class Intra(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Cars for cars", r"Why does a country import what it exports?", "Chapter one. Cars for cars.",
             lit={1965: r"the Auto Pact", 1975: r"Grubel and Lloyd"}, scale=("market", "nation"),
             horizon=("a decade",))
        self.index()

    def index(self):
        I_ = load("intra")
        ax = plane([1967, 2026], [0, 1.05], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   ylabel=r"Grubel-Lloyd index of two-way trade", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        lines = {k: path(ax, v["years"], v["gl"], COLS[k], 3.0, smooth=False) for k, v in I_.items()}
        key = VGroup(*[label(k, font_size=16, color=COLS[k]) for k in I_]).arrange(RIGHT, buff=0.5).next_to(
            ax, UP, buff=0.12)
        eq = MathTex(r"GL = 1 - \frac{|X - M|}{X + M}", font_size=34).to_edge(UP, buff=0.25).shift(RIGHT * 3.6)
        cg, cars = I_["capital goods"], I_["cars and parts"]
        side = VGroup(
            label(r"1 when exports \\ equal imports; \\ 0 when trade \\ runs one way", font_size=17, color=GREY_A),
            label(rf"cars, \ 1967: \ {cars['gl1967']:.2f}: \\ the US-Canada Auto Pact \\ of 1965", font_size=17,
                  color=FISH),
            label(rf"capital goods, \ 2025: \\ \${cg['x2025']:.0f}bn out, \\ \${cg['m2025']:.0f}bn in", font_size=17,
                  color=ARCH),
            label(r"Grubel and Lloyd (1975): \\ much of rich countries' \\ trade is two-way", font_size=17,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BEA, \ NIPA table 4.2.5, \ via FRED; \ Grubel and Lloyd (1975)", corner=DR, font_size=12)
        with self.voiceover(
            "Part thirty-five ended on a fact that its theories could not explain. <bookmark mark='a'/> Measure how "
            "much of a country's trade in a category runs both ways: the Grubel-Lloyd index, one when exports equal "
            "imports and zero when trade runs one way. <bookmark mark='b'/> Here it is for America's trade in "
            "capital goods, cars and consumer goods since 1967. In 1967, two years after the Auto Pact with "
            f"Canada, America's trade in cars and parts scored {cars['gl1967']:.2f}: it shipped cars north and "
            "bought cars back. <bookmark mark='c'/> In 2025 America exported "
            f"{cg['x2025']:.0f} billion dollars of capital goods and imported {cg['m2025']:.0f} billion. "
            "<bookmark mark='d'/> Herbert Grubel and Peter Lloyd showed in 1975 that much of rich countries' trade "
            "is like this, and that it is not an artefact of lumping different goods together. Neither Ricardo nor "
            "Heckscher and Ohlin predicts it: a country should not export and import the same thing."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(key))
            self.play(*[Create(ln) for ln in lines.values()], run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Indicate(lines["cars and parts"], color=WHITE, scale_factor=1.0), FadeIn(side[1]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
