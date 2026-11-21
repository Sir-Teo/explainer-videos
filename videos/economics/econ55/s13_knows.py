from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Knows(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Forecasts, \ and what macroeconomics knows", r"Which answers survive every method?",
             "Chapter eleven. Forecasts, and what macroeconomics knows.",
             lit={2016: r"Ramey", 2018: r"Nakamura and Steinsson"}, scale=("nation", "world"), horizon=("a decade",))
        self.forecasts()
        self.knows()

    def forecasts(self):
        F = load("forecasts")
        top = label(r"a model that identifies effects should also forecast: \ the toughest test, \ out of sample",
                    font_size=22, color=WHITE).to_edge(UP, buff=0.5)
        specs = [
            (r"growth in 2009, \ \%", r"August 2008: \\ the forecasters", F["g_forecast"], F["g_actual"],
             (-3.5, 2.5), [-3, -2, -1, 0, 1, 2], r"Part 1"),
            (r"inflation in 2022, \ \% \ (PCE, \ Q4 to Q4)", r"June 2021: \\ the Federal Reserve", F["pi_forecast"],
             F["pi_actual"], (0, 7), [0, 2, 4, 6], r"Part 28"),
        ]
        panels = VGroup()
        for k, (ttl, who, fc, ac, yr, yt, part) in enumerate(specs):
            ax = plane([0, 2], list(yr), center=(LEFT if k == 0 else RIGHT) * 3.1 + DOWN * 0.25, x_length=3.6,
                       y_length=3.6, xticks=[], yticks=yt, xlabel=r"", ylabel=ttl,
                       yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
            bars, vals = VGroup(), VGroup()
            for j, (v, col) in enumerate(((fc, GREY_B), (ac, ERR))):
                p0, p1 = ax.ax.c2p(0.25 + j, 0), ax.ax.c2p(0.75 + j, v)
                b = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=col, fill_opacity=0.8,
                              stroke_width=0).move_to((p0 + p1) / 2)
                bars.add(b)
                txt = f"{v:+.1f}".replace("-", "{-}")
                vals.add(label(rf"${txt}$", font_size=20, color=col).next_to(b, UP if v >= 0 else DOWN, buff=0.1))
            names = VGroup(label(who, font_size=15, color=GREY_B), label(r"what \\ happened", font_size=15,
                                                                           color=ERR))
            for j, n_ in enumerate(names):
                n_.move_to(ax.ax.c2p(0.5 + j, yr[0])).shift(DOWN * 0.45)
            src = label(part, font_size=14, color=GREY_B).next_to(ax, RIGHT, buff=0.2).align_to(ax, UP)
            panels.add(VGroup(ax, bars, vals, names, src))
        zero = DashedLine(panels[0][0].ax.c2p(0, 0), panels[0][0].ax.c2p(2, 0), color=GREY_D, stroke_width=1)
        rows = VGroup(
            label(r"models fitted to calm decades are least reliable at the turns that matter most", font_size=21,
                  color=E.ACCENT),
            label(r"Part 57 grades the forecasters, \ and the models, \ properly", font_size=21, color=GAIN),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        tag = data_tag(r"Philadelphia Fed SPF; \ Federal Reserve SEP; \ BEA via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "If a model really knows what causes what, it should also forecast. <bookmark mark='a'/> Forecasting "
            "out of sample is the toughest test there is, because the model never saw the answer. <bookmark "
            "mark='b'/> The record at the turns is sobering. In August 2008 the professional forecasters expected "
            f"the American economy to grow in 2009, by {say_pct(F['g_forecast'] / 100)}; it shrank by "
            f"{say_pct(-F['g_actual'] / 100)}, more than in any year since 1946. <bookmark mark='c'/> In June 2021 "
            f"the Federal Reserve's median projection had inflation falling to {F['pi_forecast']:.1f} percent in "
            f"2022; it was {F['pi_actual']:.1f} percent. <bookmark mark='d'/> Models fitted to calm decades are "
            "least reliable at exactly the turning points that matter most. <bookmark mark='e'/> Part fifty-seven "
            "grades the forecasters, and the models, properly."
        ) as vo:
            self.play(FadeIn(top, shift=DOWN * 0.1))
            vo.wait_until("b")
            p = panels[0]
            self.play(FadeIn(p[0]), FadeIn(zero), FadeIn(p[4]), FadeIn(tag))
            self.play(GrowFromEdge(p[1][0], DOWN), FadeIn(p[2][0]), FadeIn(p[3][0]))
            self.play(GrowFromEdge(p[1][1], UP), FadeIn(p[2][1]), FadeIn(p[3][1]))
            vo.wait_until("c")
            p = panels[1]
            self.play(FadeIn(p[0]), FadeIn(p[4]))
            self.play(GrowFromEdge(p[1][0], DOWN), FadeIn(p[2][0]), FadeIn(p[3][0]))
            self.play(GrowFromEdge(p[1][1], DOWN), FadeIn(p[2][1]), FadeIn(p[3][1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def knows(self):
        cards = point_cards([
            (r"money is not neutral", r"a surprise tightening lowers output for a year or two, \ and prices more "
             r"slowly; \ every method agrees on the sign and the delay", MONEY),
            (r"but its size is contested", r"the estimates differ several times over, \ with the method and the "
             r"decades used \ (the Dial)", ERR),
            (r"regions are not the nation", r"relative multipliers above one; \ national ones near or below one",
             DEMAND),
            (r"identified moments discipline models", r"a model must reproduce what the clean designs found, \ not "
             r"just the averages", THEORY),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.15)
        head = label(r"what macroeconomics knows, \ and how", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Ramey, \ Handbook of Macroeconomics 2 (2016); \ Nakamura and Steinsson, \ JEP 32(3) "
                            r"(2018)", corner=DR, font_size=12)
        books = VGroup(
            history_card(2016, r"Valerie Ramey", r"`Macroeconomic shocks and their propagation': \ what every "
                         r"method says about monetary and fiscal shocks", color=MONEY, width=9.0, font_size=21),
            history_card(2018, r"Emi Nakamura and J\'on Steinsson", r"`Identification in macroeconomics': \ "
                         r"identified moments as the test of a model", color=THEORY, width=9.0, font_size=21),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "So what does macroeconomics know, and how does it know it? Valerie Ramey's survey of the shocks and "
            "their effects, and Nakamura and Steinsson's essay on identification, give a sober answer. <bookmark "
            "mark='a'/> Money is not neutral: a surprise tightening lowers output for a year or two and prices more "
            "slowly, and every credible method agrees on the sign and the delay. <bookmark mark='b'/> How much is "
            "contested: the estimates differ several times over with the method and the decades used, as the "
            "Dial will show. <bookmark mark='c'/> Regions are not the nation: relative multipliers are above one, "
            "national ones near or below it. <bookmark mark='d'/> And the clean findings, which Nakamura and "
            "Steinsson call identified moments, are the test a model must pass: not just matching averages, but "
            "reproducing what the best designs have found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in books],
                                                             lag_ratio=0.5), run_time=2.0)
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(books), run_time=0.6)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
