from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Island(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The same paper on the Island", r"What would this method find if the truth were known?",
             "Chapter ten. The same paper on the Island.", scale=("city",), horizon=("a year",))
        self.trials()

    def trials(self):
        I = load("island")
        ax = plane([-8, 0], [0, 4], center=RIGHT * 0.9 + DOWN * 0.2, x_length=8.6, y_length=4.4,
                   xticks=[-8, -6, -4, -2, 0], yticks=[], xlabel=r"estimated effect, \ \%",
                   xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        truth = vline(ax, 100 * I["clean"]["truth"], 0, 4, TRUE, 2.6)
        tl = label(rf"the truth: \ {100 * I['clean']['truth']:.0f}\%".replace("-", "{-}"), font_size=16,
                   color=TRUE).next_to(ax.ax.c2p(100 * I["clean"]["truth"], 4), UP, buff=0.06)
        cases = [(3.3, I["clean"], "mean", r"parallel trends hold", CTRL),
                 (2.4, I["divert"], "mean", r"30\% of lost trips divert \\ to the comparison crossings", ROW),
                 (1.5, I["trend"], "mean", r"the tunnels drift \\ 1.5\% a year", TOLL),
                 (0.6, I["trend"], "adjusted", r"the same, \ net of \\ the placebo year", BUS)]
        rows, names = VGroup(), VGroup()
        for y, R, key, nm, col in cases:
            m = 100 * R[key]
            s = 100 * (R["adjusted_sd"] if key == "adjusted" else R["sd"])
            bar = Line(ax.ax.c2p(m - 1.645 * s, y), ax.ax.c2p(m + 1.645 * s, y), stroke_color=col, stroke_width=9,
                       stroke_opacity=0.5)
            d = Dot(ax.ax.c2p(m, y), radius=0.09, color=WHITE)
            t = label(rf"{m:.1f}\%".replace("-", "{-}"), font_size=16, color=col).next_to(bar, UP, buff=0.06)
            rows.add(VGroup(bar, d, t))
            names.add(label(nm, font_size=16, color=col).next_to(ax.ax.c2p(-8, y), LEFT, buff=0.2))
        if names.get_left()[0] < -6.9:
            VGroup(ax, truth, tl, rows, names).shift(RIGHT * (-6.9 - names.get_left()[0]))
        foot = label(r"400 Islands each: \ the mean estimate, \ and the range of 90\% of them", font_size=16,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = island_tag(r"computed: \ agora.congestion.island\_study", corner=UL, font_size=12)
        with self.voiceover(
            "This series has always checked a method where the truth is known. So run the same paper on the "
            "Island: two tolled crossings, eight others, a shared season, and a charge that truly removes four "
            "percent of the tolled crossings' traffic. <bookmark mark='a'/> When the crossings would have moved in "
            f"parallel, the method finds {say_pct(-I['clean']['mean'], 1)} on average: right, though any single "
            "Island can miss by a couple of points. <bookmark mark='b'/> When thirty percent of the lost trips "
            "divert to the comparison crossings, the comparison group grows and the method overstates the effect: "
            f"{say_pct(-I['divert']['mean'], 1)}. <bookmark mark='c'/> When the tolled crossings were already "
            "drifting down one and a half percent a year, the plain comparison finds "
            f"{say_pct(-I['trend']['mean'], 1)}, the effect plus the drift. <bookmark mark='d'/> Subtracting the "
            f"placebo year recovers {say_pct(-I['trend']['adjusted'], 1)}, and more precisely. That is the "
            "correction chapter five applied to New York, checked where the answer is known."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(truth), FadeIn(tl), FadeIn(tag), FadeIn(foot))
            for mk, r_, n_ in zip("abcd", rows, names):
                vo.wait_until(mk)
                self.play(FadeIn(n_), GrowFromCenter(r_[0]), FadeIn(r_[1]), FadeIn(r_[2]))
        self.clear_scene()
