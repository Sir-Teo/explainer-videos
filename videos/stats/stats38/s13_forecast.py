from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Forecast(VoiceoverScene):
    def construct(self):
        self.card()
        self.competitions()
        self.pretrained()
        self.rolling()
        self.table()
        self.leakage()
        self.lesson()

    def card(self):
        card = chapter_card(12, r"The forecasting frontier", r"Big models, \ and honest evaluation", lit=(2018, 2020, 2024), part=PART)
        with self.voiceover("Chapter twelve. The forecasting frontier."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def competitions(self):
        rows = fit_rows(VGroup(
            label(r"Part 17: \ the M-competitions found simple methods hard to beat", font_size=26, color=GREY_A),
            label(r"M4 (2018): \ 100,000 series; \ a hybrid of exponential smoothing and a neural network won", font_size=26, color=TAUC),
            label(r"M5 (2020): \ Walmart sales; \ gradient-boosted trees across many related series dominated", font_size=26, color=BANDC),
            label(r"the lesson: \ learning across many series pays; \ combinations beat single models", font_size=26, color=Y0C),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part seventeen told the story of Spyros Makridakis's competitions, in which simple methods "
            "proved hard to beat. <bookmark mark='b'/> The fourth competition, in 2018, with a hundred thousand series, was "
            "won by Slawek Smyl's hybrid of exponential smoothing and a recurrent neural network. <bookmark mark='c'/> The "
            "fifth, in 2020, on Walmart's sales, was dominated by gradient-boosted trees, Part thirty-four's machinery, "
            "trained across thousands of related series at once. <bookmark mark='d'/> The lesson was that learning across "
            "many series pays, and that combinations of forecasts beat single models."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def pretrained(self):
        rows = fit_rows(VGroup(
            label(r"the next step: \ one model pretrained on a huge corpus of series, \ used without fitting", font_size=26, color=TAUC),
            label(r"TimeGPT, \ Lag-Llama, \ TimesFM, \ Chronos, \ Moirai \ (2023--24), \ and successors", font_size=26),
            label(r"``zero-shot'': \ give it a history, \ get a forecast distribution", font_size=26, color=BANDC),
            label(r"benchmarks: \ often competitive, \ sometimes beaten by seasonal naive; \ check current results", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The next step borrows from language models: train one large model on a huge corpus of time "
            "series, then use it on new series without fitting anything. <bookmark mark='b'/> Nixtla's TimeGPT, Lag-Llama, "
            "Google's TimesFM, Amazon's Chronos and Salesforce's Moirai appeared in 2023 and 2024, and successors keep "
            "coming. <bookmark mark='c'/> Given a history, they return a forecast distribution, zero-shot. <bookmark "
            "mark='d'/> On public benchmarks they are often competitive with tuned statistical methods, and sometimes "
            "beaten by a seasonal naive forecast. The rankings change quickly; what does not change is how to evaluate them."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rolling(self):
        rows = [
            cmath(r"\text{rolling origin}", r":", r"\text{fit on } y_{1:o}, \text{ forecast } y_{o+1:o+h}, \text{ move } o, \text{ repeat}", font_size=28),
            cmath(r"\text{scale-free}", r":", r"\text{MASE: \ error relative to the seasonal naive in-sample}", font_size=28),
            cmath(r"\text{probabilistic}", r":", r"\text{CRPS or quantile loss, \ and interval coverage (Parts 24, 34)}", font_size=28),
            cmath(r"\text{no leakage}", r":", r"\text{nothing from the test period touches training or tuning}", font_size=28),
        ]
        rows[3][-1].set_color(MISSC)
        whys = [why(r"never one split"), why(r"Hyndman \& Koehler (2006)"), why(r"forecasts are distributions"),
                why(r"pretraining corpora may contain the test series")]
        with self.voiceover(
            "<bookmark mark='a'/> Honest evaluation has four rules. Use a rolling origin: fit on the data up to some time, "
            "forecast the next stretch, move the origin forward, repeat, and average. <bookmark mark='b'/> Use a "
            "scale-free error such as Rob Hyndman and Anne Koehler's MASE, the error relative to the seasonal naive "
            "forecast. <bookmark mark='c'/> Score the whole forecast distribution, by the continuous ranked probability "
            "score of Part twenty-four, and check interval coverage. <bookmark mark='d'/> And allow no leakage: nothing from "
            "the test period may touch training or tuning. For pretrained models that is hard to guarantee, because their "
            "training corpora may already contain the benchmark series."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("forecast")
        m = d["mase"]
        rows = [[r"method", r"MASE, \ 2 years ahead, \ 11 origins"],
                [r"naive \ (last value)", f"{m['naive']:.2f}"],
                [r"seasonal naive \ (last year)", f"{m['snaive']:.2f}"],
                [r"seasonal naive plus last year's trend", f"{m['drift']:.2f}"],
                [r"Holt--Winters \ (Part 17)", f"{m['hw']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.32, colors=[GREY_A, MISSC, GREY_B, TAUC, BANDC]).move_to([0, 0.7, 0])
        foot = label(r"Mauna Loa CO$_2$, \ monthly, \ origins 1990--2000; \ below 1 beats the seasonal naive's in-sample error",
                     font_size=22, color=GREY_A).move_to([0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A small honest evaluation, on Mauna Loa's carbon dioxide record: eleven origins, a year "
            "apart, each forecasting two years ahead. <bookmark mark='b'/> The naive forecast and the seasonal naive score "
            "above one. <bookmark mark='c'/> Adding last year's trend to the seasonal pattern brings it to " + say(m["drift"], 2)
            + ". <bookmark mark='d'/> Holt-Winters exponential smoothing, from Part seventeen, scores " + say(m["hw"], 2)
            + ". Any new method, pretrained or not, should be put through exactly this, on data it cannot have seen."
        ) as vo:
            self.add(co2_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]))
        self.clear_scene()

    def leakage(self):
        d = load("forecast")
        rows = fit_rows(VGroup(
            label(r"leakage in miniature: \ make 50 small tweaks of the Holt--Winters forecast", font_size=26),
            label(r"and keep the one that scores best on the test period itself", font_size=26, color=MISSC),
            label(rf"its MASE: \ {d['leak_best']:.2f}, \ against the honest {d['leak_honest']:.2f}", font_size=26, color=MISSC),
            label(r"a better score, \ and a worse method: \ Part 28's optimism, \ in time", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Leakage in miniature. Take the Holt-Winters forecast at the last origin and make fifty "
            "small random adjustments to it. <bookmark mark='b'/> Keep whichever scores best on the test period itself. "
            "<bookmark mark='c'/> Its error is " + say(d["leak_best"], 2) + ", against the honest " + say(d["leak_honest"], 2)
            + ". <bookmark mark='d'/> The score improved and the method did not: the adjustments are noise, and the next "
            "period will not reward them. It is Part twenty-eight's optimism of the training error, in time."
        ) as vo:
            self.add(co2_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"big models change what is possible, \ not how to judge it", font_size=26, color=TAUC),
            label(r"rolling origins, \ scale-free errors, \ probabilistic scores, \ no leakage, \ strong baselines", font_size=26, color=BANDC),
            label(r"and the structure of this part still matters: \ unit roots, \ volatility, \ breaks, \ long memory", font_size=26, color=GREY_A),
            label(r"Part 64 returns to statistics in the age of large models", font_size=26, color=Y0C),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Big models change what is possible, not how to judge it. <bookmark mark='b'/> Rolling "
            "origins, scale-free errors, scores for the whole forecast distribution, no leakage, and strong simple baselines. "
            "<bookmark mark='c'/> And the structure of this part still matters: a forecaster that ignores a unit root, a "
            "volatility cluster, a break or long memory will be confidently wrong. <bookmark mark='d'/> Part sixty-four "
            "returns to statistics in the age of large models."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
