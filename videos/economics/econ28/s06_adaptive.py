from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Adaptive(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Adaptive expectations", r"How well does looking back predict inflation?", "Chapter five. "
             "Adaptive expectations.", lit={1956: r"Cagan"}, scale=("person",), horizon=("a year",))
        self.rule()
        self.fit()

    def rule(self):
        rows = VGroup(
            label(r"adaptive expectations: \ correct last year's forecast by part of last year's error",
                  font_size=24, color=E.ACCENT),
            MathTex(r"\pi^e_{t+1} = \pi^e_t + \lambda\,(\pi_t - \pi^e_t)", font_size=44, color=EXPECT),
            label(r"$\lambda = 1$: \ expect whatever happened last year", font_size=23, color=INFL),
            label(r"$\lambda$ small: \ a long, \ slow average of the past", font_size=23, color=SURPRISE),
            label(r"Cagan used it for hyperinflations \ (Part 25); \ your forecast of 1973 was probably a version "
                  r"of it", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The simplest model of how people forecast is the one you probably used. <bookmark mark='a'/> Adaptive "
            "expectations: each year, correct last year's forecast by a fraction lambda of last year's error. "
            "<bookmark mark='b'/> With lambda equal to one, you simply expect whatever happened last year. "
            "<bookmark mark='c'/> With a small lambda, your forecast is a long, slow average of the past. "
            "<bookmark mark='d'/> Phillip Cagan used it in his study of hyperinflations, in Part twenty-five, and "
            "your forecast for 1973 was probably some version of it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            for mk, r_ in zip("bcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def fit(self):
        A = load("adaptive")
        ys = np.array(A["years"])
        x = np.array(A["inflation"])
        f1, f2 = A["fits"]["1.0"], A["fits"]["0.2"]
        ax = plane([1960, 2026], [-1, 14], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 4, 8, 12], ylabel=r"inflation, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        act = path(ax, ys, x, color=INFL, width=4, smooth=False)
        l1 = path(ax, ys[1:], f1["forecast"], color=EXPECT, width=2, smooth=False)
        l2 = path(ax, ys[1:], f2["forecast"], color=SURPRISE, width=2, smooth=False)
        side = VGroup(
            label(r"red: \ what happened", font_size=19, color=INFL),
            label(rf"last year's rule: \\ typical error {f1['rmse']:.1f} points", font_size=19, color=EXPECT),
            label(rf"a slow average ($\lambda = 0.2$): \\ {f2['rmse']:.1f} points", font_size=19, color=SURPRISE),
            label(rf"1966--80: \ too low, \ by {A['mean_err_70s']:.1f} a year; \\ 1981--86: \ too high, \ by "
                  rf"{-A['mean_err_80s']:.1f}", font_size=19, color=HOLD),
            label(r"errors that run in one direction \\ for years: \ a rule nobody \\ would keep using", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BLS: \ the CPI, \ annual averages, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "How well does it work on America's inflation since 1960? <bookmark mark='a'/> In red, what happened. "
            "<bookmark mark='b'/> In gold, last year's rule: its typical error is about "
            f"{f1['rmse']:.1f} points. <bookmark mark='c'/> In violet, a slow average, with lambda at a fifth: worse, "
            f"{f2['rmse']:.1f} points, because it is always late. <bookmark mark='d'/> Worse still is the pattern. "
            f"From 1966 to 1980, even last year's rule was too low, by {A['mean_err_70s']:.1f} points a year on "
            f"average; from 1981 to 1986, as inflation fell, it was too high, by {-A['mean_err_80s']:.1f}. "
            "<bookmark mark='e'/> A rule whose mistakes run the same way, year after year, is one that nobody "
            "sensible would keep using. That was the opening for a very different idea."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(act), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(side[2]), run_time=1.5)
            for mk, r_ in zip("de", side[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
