from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403

COLS = {"capital goods": ARCH, "cars and parts": FISH, "consumer goods": CLOTH}


class Intra(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Cars for cars", r"Why does a country import what it exports?", "Chapter one. Cars for cars.",
             lit={1965: r"the Auto Pact", 1975: r"Grubel and Lloyd"}, scale=("market", "nation"),
             horizon=("a decade",))
        self.index()
        self.worked()

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

    def worked(self):
        I_ = load("intra")
        rows = []
        for k in ("cars and parts", "capital goods", "consumer goods"):
            v = I_[k]
            rows.append((k, v["x2025"], v["m2025"], COLS[k]))
        bars = VGroup()
        sc = 4.6 / max(max(x, m) for _, x, m, _ in rows)
        for j, (k, x, m, col) in enumerate(rows):
            y = 1.3 - 1.45 * j
            bx = Rectangle(width=x * sc, height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to(
                np.array([-1.5 + x * sc / 2, y + 0.21, 0]))
            bm = Rectangle(width=m * sc, height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.4).move_to(
                np.array([-1.5 + m * sc / 2, y - 0.21, 0]))
            ov = Rectangle(width=min(x, m) * sc, height=0.8, stroke_color=WHITE, stroke_width=2,
                           fill_opacity=0).move_to(np.array([-1.5 + min(x, m) * sc / 2, y, 0]))
            gl = 2 * min(x, m) / (x + m)
            bars.add(VGroup(label(k, font_size=19, color=col).next_to(np.array([-1.6, y, 0]), LEFT, buff=0.15),
                            bx, label(rf"out \${x:.0f}bn", font_size=15, color=WHITE).next_to(bx, RIGHT, buff=0.1),
                            bm, label(rf"in \${m:.0f}bn", font_size=15, color=GREY_A).next_to(bm, RIGHT, buff=0.1),
                            ov, label(rf"GL = 2 $\times$ {min(x, m):.0f} / {x + m:.0f} = {gl:.2f}", font_size=17,
                                      color=E.ACCENT).move_to(np.array([4.8, y, 0]))))
        eq = MathTex(r"GL = 1 - \frac{|X - M|}{X + M} = \frac{2\min(X, M)}{X + M}", font_size=34).to_edge(UP, buff=0.4)
        foot = label(r"the white box: \ the part of trade that runs both ways", font_size=18, color=GREY_A).to_edge(
            DOWN, buff=0.5)
        tag = data_tag(r"BEA, \ NIPA table 4.2.5, \ via FRED", corner=DR, font_size=12)
        car = rows[0]
        with self.voiceover(
            "Work one out. <bookmark mark='a'/> In 2025 America exported "
            f"{car[1]:.0f} billion dollars of cars and parts and imported {car[2]:.0f} billion. The smaller of the "
            f"two, {car[1]:.0f}, is matched by an equal flow the other way; that overlap, counted on both sides, is "
            "two-way trade, and its share of the total is the index: "
            f"{2 * min(car[1], car[2]) / (car[1] + car[2]):.2f}. <bookmark mark='b'/> Capital goods score higher: "
            "America sells machines and aircraft and buys other machines and aircraft. <bookmark mark='c'/> "
            "Consumer goods score lower, because imports far exceed exports. Two-way trade within an industry means "
            "countries trade varieties, not just different goods. The next chapter asks why anyone would."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), FadeIn(bars[0][:5]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(bars[0][5]), FadeIn(bars[0][6]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(bars[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(bars[2], shift=UP * 0.1))
        self.clear_scene()
