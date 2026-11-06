from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403

KINDS = (("calibrated", r"calibrated: \ $N(\mu_t, 1)$", HIT), ("overconfident", r"overconfident: \ SD 0.5", RES),
         ("underconfident", r"underconfident: \ SD 2", AICC), ("biased", r"biased: \ mean $\mu_t + 0.7$", BICC))


class Calibration(VoiceoverScene):
    def construct(self):
        self.card()
        self.prequential()
        self.pit()
        self.histograms()
        self.scores()
        self.prostate_pit()
        self.proper()
        self.crps()
        self.sharp()

    def card(self):
        card = chapter_card(11, r"Calibrated forecasts", r"Judge a model by what it predicts", lit=(1984,), part=PART)
        with self.voiceover("Chapter eleven. Calibrated forecasts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def prequential(self):
        rows = fit_rows(VGroup(
            label(r"a model is a machine for issuing forecasts", font_size=26),
            label(r"judge it only by its forecasts and what then happened", font_size=26, color=PATH),
            label(r"not by its parameters, \ its story, \ or its likelihood alone", font_size=26, color=GREY_A),
            label(r"two questions: \ calibrated? \ \ sharp?", font_size=26, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Chapter seven ended with Philip Dawid's view: a statistical model is a machine for issuing "
            "forecasts, one observation ahead. <bookmark mark='b'/> His prequential principle says to judge it only by the "
            "forecasts it issued and what then happened, <bookmark mark='c'/> not by its parameters or the story behind it. "
            "<bookmark mark='d'/> Two questions follow. Are its forecasts calibrated, meaning events it calls seventy percent "
            "likely happen seventy percent of the time? And, among calibrated forecasts, how sharp are they?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def pit(self):
        rows = [
            cmath(r"F_t", r":", r"\text{the forecast distribution for } y_t", font_size=30),
            cmath(r"u_t", r"=", r"F_t(y_t)", font_size=34),
            cmath(r"F_t \text{ true}", r"\Rightarrow", r"u_t \sim U(0, 1), \ \text{independent}", font_size=30),
            cmath(r"\text{histogram of } u_t", r":", r"\text{flat if calibrated}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"issued before $y_t$ is seen"), why(r"the probability integral transform"),
                why(r"Part 7's inverse-CDF method, \ backwards"), why(r"Dawid (1984); \ Diebold, Gunther \& Tay (1998)")]
        with self.voiceover(
            "<bookmark mark='a'/> The tool is the probability integral transform. Each forecast is a whole distribution, "
            "issued before the observation arrives. <bookmark mark='b'/> Evaluate it at what happened. "
            "<bookmark mark='c'/> If the forecasts are the true conditional distributions, these values are independent "
            "uniforms: Part 7's inverse-CDF method run backwards. <bookmark mark='d'/> So their histogram should be flat, "
            "Dawid's proposal, made routine for economic forecasts by Francis Diebold, Todd Gunther and Anthony Tay."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def histograms(self):
        d = load("pit")
        panels = VGroup()
        for k, (key, title, col) in enumerate(KINDS):
            h = np.asarray(d[key]["hist"], float)
            dens = h / h.sum() * 10
            A = axes([0, 1], [0, 3.2], x_length=4.6, y_length=1.8, xlabel=r"PIT", ylabel=r"", xticks=[0, 0.5, 1], yticks=[0, 1, 3],
                     center=[-3.3 + 6.6 * (k % 2), 1.75 - 3.35 * (k // 2), 0])
            ax = A.ax
            bars = hist_bars(ax, np.linspace(0, 1, 11), dens, color=col, opacity=0.8)
            flat = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=WHITE, stroke_width=1.5)
            t = label(title, font_size=22, color=col).next_to(A, UP, buff=0.08)
            panels.add(VGroup(A, bars, flat, t))
        with self.voiceover(
            "<bookmark mark='a'/> Two thousand observations from a drifting level with unit noise, and four forecasters who all "
            "know the level. The calibrated one forecasts normal with the right spread: its PIT histogram is flat, within "
            "noise. <bookmark mark='b'/> The overconfident one uses half the spread: too many observations fall in its tails, "
            "and the histogram is U-shaped. <bookmark mark='c'/> The underconfident one doubles it: the observations crowd its "
            "middle, a hump. <bookmark mark='d'/> The biased one is shifted up by point seven: most observations fall below its "
            "median, and the histogram slopes down."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                p = panels[k]
                self.play(FadeIn(p[0]), FadeIn(p[2]), FadeIn(p[3]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in p[1]], lag_ratio=0.05))
        self.clear_scene()

    def scores(self):
        d = load("pit")
        hdr = [r"\textbf{forecaster}", r"\textbf{log score}", r"\textbf{CRPS}", r"\textbf{90\% interval covers}"]
        body = [[title.split(":")[0], f"{d[k]['log']:.3f}", f"{d[k]['crps']:.3f}", f"{100 * d[k]['cover90']:.2f}\\%"]
                for k, title, _ in KINDS]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A] + [c for _, _, c in KINDS])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"log score: \ $-\log f_t(y_t)$; \ CRPS: \ $E|X - y_t| - \tfrac12 E|X - X'|$; \ both lower is better", font_size=22),
            label(r"the calibrated forecaster wins both; \ the underconfident one's intervals \ \emph{over}-cover", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Score them. The log score of Part 24 is minus the log forecast density at the outcome; the "
            "continuous ranked probability score compares the whole forecast distribution with the outcome, in the units of "
            "the data. <bookmark mark='b'/> The calibrated forecaster wins on both. The overconfident one's ninety percent "
            "intervals cover only fifty-eight percent. <bookmark mark='c'/> The underconfident one's cover almost every "
            "observation, which looks safe but is penalized all the same: its forecasts are vaguer than they need be."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def proper(self):
        rows = [
            cmath(r"S(F, y)", r":", r"\text{a penalty for forecast } F \text{ when } y \text{ happens}", font_size=30),
            cmath(r"\text{proper}", r":", r"E_{G}\, S(G, Y) \le E_{G}\, S(F, Y) \ \ \text{for all } F", font_size=30),
            cmath(r"\text{strictly proper}", r":", r"\text{equality only at } F = G", font_size=30),
            cmath(r"\text{log score, \ CRPS}", r":", r"\text{strictly proper; \ squared error of the mean: \ not}", font_size=28),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"a scoring rule"), why(r"honesty is the best policy"), why(r"no other forecast ties the truth"),
                why(r"Gneiting \& Raftery (2007)")]
        with self.voiceover(
            "<bookmark mark='a'/> Why these scores? A scoring rule charges a penalty for a forecast once the outcome is known. "
            "<bookmark mark='b'/> It is proper if a forecaster who believes G minimizes their expected penalty by reporting G "
            "itself: honesty is the best policy. <bookmark mark='c'/> Strictly proper if nothing else ties. "
            "<bookmark mark='d'/> The log score and CRPS are strictly proper, Tilmann Gneiting and Adrian Raftery's survey "
            "explains; squared error of the forecast mean is not, because it ignores the spread entirely. AIC, WAIC and LOO are "
            "all estimates of an expected log score: this part's criteria are forecasters' scores in disguise."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sharp(self):
        rows = fit_rows(VGroup(
            label(r"maximize sharpness, \ subject to calibration \ (Gneiting, Balabdaoui \& Raftery 2007)", font_size=24, color=HIT),
            label(r"a climatological forecast is calibrated, \ and useless", font_size=24, color=GREY_A),
            label(r"check the PIT; \ compare by a proper score", font_size=24, color=PATH),
            label(r"weather services have done this since the 1950s \ (Brier 1950)", font_size=24, color=BICC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Gneiting, Fadoua Balabdaoui and Raftery summed it up: maximize the sharpness of the forecasts, "
            "subject to calibration. <bookmark mark='b'/> Calibration alone isn't enough: forecasting the long-run climate "
            "every day is calibrated and useless. <bookmark mark='c'/> So check the PIT histogram, and compare competing models "
            "by a proper score. <bookmark mark='d'/> Weather forecasters have worked this way since Glenn Brier's score of "
            "1950, and their forecasts improved, by about a day of lead time per decade, because they were scored honestly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def prostate_pit(self):
        d = load("prostate_pit")
        panels = VGroup()
        spec = (("null", r"intercept only", RES), ("two", r"lcavol $+$ lweight", BICC), ("full", r"all eight", AICC))
        for k, (key, title, col) in enumerate(spec):
            h = np.asarray(d[key]["hist"], float)
            dens = h / h.sum() * 5
            A = axes([0, 1], [0, 2.2], x_length=3.6, y_length=2.4, xlabel=r"LOO PIT", ylabel=r"", xticks=[0, 0.5, 1],
                     yticks=[0, 1, 2], center=[-4.4 + 4.4 * k, 1.0, 0])
            ax = A.ax
            bars = hist_bars(ax, np.linspace(0, 1, 6), dens, color=col, opacity=0.8)
            flat = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=WHITE, stroke_width=1.5)
            t = label(title, font_size=22, color=col).next_to(A, UP, buff=0.1)
            s = VGroup(label(rf"KS $p = {d[key]['ks_p']:.2f}$", font_size=20, color=GREY_A),
                       label(rf"LOO log score ${d[key]['lpd']:.2f}$", font_size=22, color=col)).arrange(DOWN, buff=0.12)
            s.next_to(A, DOWN, buff=0.45)
            panels.add(VGroup(A, bars, flat, t, s))
        foot = label(r"all three calibrated; \ the sharper two score far better; \ the extra six predictors add 0.01",
                     font_size=22, color=PATH).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "<bookmark mark='a'/> Real forecasts: predict each of the sixty-seven prostate training men from a model fitted to "
            "the other sixty-six. For a normal linear model with the reference prior, the leave-one-out predictive is a t "
            "distribution, and the PIT is just the t CDF of the externally studentized residual, Part 23's diagnostic in new "
            "clothes. The intercept-only model is calibrated: flat histogram, Kolmogorov–Smirnov p-value point nine six. "
            "<bookmark mark='b'/> The two-predictor model is calibrated too, and much sharper: its log score is half a nat "
            "better. <bookmark mark='c'/> The full model is calibrated and scores only a hundredth better than the pair. "
            "<bookmark mark='d'/> Calibration rules out bad forecasters; sharpness, measured by a proper score, ranks the "
            "good ones."
        ) as vo:
            self.add(prostate_tag())
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                p = panels[k]
                self.play(FadeIn(p[0]), FadeIn(p[2]), FadeIn(p[3]), FadeIn(p[4]),
                          LaggedStart(*[GrowFromEdge(b, DOWN) for b in p[1]], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def crps(self):
        rows = [
            cmath(r"\text{CRPS}(F, y)", r"=", r"\textstyle\int (F(x) - \mathbf 1\{y \le x\})^2\, dx", font_size=30),
            cmath(r"", r"=", r"E|X - y| - \tfrac12 E|X - X'|, \ \ X, X' \sim F", font_size=30),
            cmath(r"F = N(\mu, \sigma^2)", r":", r"\sigma\bigl[z(2\Phi(z) - 1) + 2\phi(z) - 1/\sqrt\pi\bigr]", font_size=28),
            cmath(r"F = \delta_m", r":", r"|m - y|", font_size=32),
        ]
        rows[1][-1].set_color(PATH)
        whys = [why(r"Matheson \& Winkler (1976)"), why(r"accuracy minus a reward for spread"),
                why(r"$z = (y - \mu)/\sigma$; \ Part 24's crps\_normal"), why(r"a point forecast: \ absolute error")]
        with self.voiceover(
            "<bookmark mark='a'/> The CRPS deserves a closer look. It is the integrated squared distance between the forecast "
            "CDF and the step function that jumps at the outcome. <bookmark mark='b'/> Equivalently, the expected distance from "
            "a forecast draw to the outcome, minus half the expected distance between two independent forecast draws: "
            "accuracy, with a rebate for honest spread. <bookmark mark='c'/> For a normal forecast it has a closed form, which "
            "statkit's crps_normal from Part 24 computes. <bookmark mark='d'/> And for a forecast that is a single point it is "
            "just the absolute error, so the CRPS lets point and probabilistic forecasts be compared on one scale."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
