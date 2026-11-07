from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class SDID(VoiceoverScene):
    def construct(self):
        self.card()
        self.two()
        self.formula()
        self.weights()
        self.table()
        self.lesson()

    def card(self):
        card = chapter_card(12, r"Synthetic difference-in-differences", r"Weights for units, \ and for years", lit=(2021,), part=PART)
        with self.voiceover("Chapter twelve. Synthetic difference-in-differences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two(self):
        rows = [[r"", r"units", r"periods", r"matches"],
                [r"DiD", r"all equal", r"all pre-periods equal", r"trends, \ on average"],
                [r"synthetic control", r"chosen weights", r"levels compared directly", r"levels"],
                [r"synthetic DiD", r"chosen weights", r"chosen weights", r"trends, \ locally"]]
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.36, colors=[GREY_A, Y0C, Y1C, BANDC]).move_to([0, 0.6, 0])
        foot = label(r"Arkhangelsky, \ Athey, \ Hirshberg, \ Imbens \& Wager (2021)", font_size=24, color=GREY_A).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Differences-in-differences and the synthetic control look like rivals, but they are two "
            "corners of one idea. <bookmark mark='b'/> DiD weights all control units equally and all pre-periods equally, "
            "and asks only that the average trend be parallel. <bookmark mark='c'/> The synthetic control chooses unit "
            "weights to match the treated unit's levels, and then compares levels directly. <bookmark mark='d'/> In 2021, "
            "Dmitry Arkhangelsky, Susan Athey, David Hirshberg, Guido Imbens and Stefan Wager combined them: choose unit "
            "weights, as the synthetic control does, but match trends rather than levels; and choose weights for the "
            "pre-periods too, emphasizing the years that look most like the post-period."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def formula(self):
        rows = [
            cmath(r"\hat\omega", r"=", r"\arg\min_{\omega_0,\ \omega \in \Delta} \textstyle\sum_{t<T_0} (\omega_0 + \sum_j \omega_j Y_{jt} - Y_{1t})^2 + \zeta^2 T_0 \|\omega\|^2", font_size=26),
            cmath(r"\hat\lambda", r"=", r"\arg\min_{\lambda_0,\ \lambda \in \Delta} \textstyle\sum_j (\lambda_0 + \sum_{t<T_0} \lambda_t Y_{jt} - \bar Y_{j,\text{post}})^2", font_size=26),
            cmath(r"\hat\tau", r"=", r"(\bar Y_{1,\text{post}} - \textstyle\sum_t \hat\lambda_t Y_{1t}) - \sum_j \hat\omega_j (\bar Y_{j,\text{post}} - \sum_t \hat\lambda_t Y_{jt})", font_size=26),
            cmath(r"\text{inference}", r":", r"\text{placebo: \ treat each control in turn}", font_size=28),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"the intercept: \ match trends, \ not levels"), why(r"years that resemble the post-period"),
                why(r"a weighted DiD"), why(r"the SD of placebo estimates")]
        with self.voiceover(
            "<bookmark mark='a'/> The unit weights solve a synthetic-control problem with two changes: an intercept, "
            "so that the weighted controls need only run parallel to California, not at the same level; and a small "
            "ridge penalty, which spreads the weight over more states. <bookmark mark='b'/> The time weights do the "
            "same across years: they find the mix of pre-period years whose outcomes best predict the controls' "
            "post-period average. <bookmark mark='c'/> The estimate is then a difference-in-differences, weighted "
            "both ways. <bookmark mark='d'/> With one treated unit, the standard error comes from placebos: pretend "
            "each control state was treated, re-estimate, and take the spread. Interpreting this as sampling "
            "uncertainty requires comparable untreated-state shocks and the relevant model conditions; a single "
            "treated state does not supply unrestricted cluster asymptotics."
        ) as vo:
            intro=label('Synthetic DiD weights both units and pre-treatment periods',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weights(self):
        d = load("sdid")
        sc = {n: w for n, w in d["w_sc"]}
        sdw = {n: w for n, w in d["omega"]}
        keep = [n for n, _ in d["omega"][:7]] + [n for n, w in d["w_sc"] if w > 0.04 and n not in dict(d["omega"][:7])]
        om = sorted([(n, sdw.get(n, 0.0)) for n in keep], key=lambda t: -(t[1] + 1e-3 * sc.get(t[0], 0.0)))
        A = axes([0, len(om) + 0.6], [0, 0.45], x_length=6.8, y_length=3.6, xlabel=r"", ylabel=r"unit weight",
                 xticks=[], yticks=[0, 0.2, 0.4], yfmt=lambda v: f"{v:g}", center=[-3.0, 0.5, 0])
        ax = A.ax
        bo = VGroup()
        bs = VGroup()
        names = VGroup()
        for i, (n, w) in enumerate(om):
            x = i + 0.7
            if w > 0:
                bo.add(Rectangle(width=0.32 * 0.8, height=max(1e-3, ax.c2p(0, w)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                                 fill_color=BANDC, fill_opacity=0.85).move_to(ax.c2p(x - 0.18, 0), aligned_edge=DOWN))
            ws = sc.get(n, 0.0)
            if ws > 0:
                bs.add(Rectangle(width=0.32 * 0.8, height=max(1e-3, ax.c2p(0, ws)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                                 fill_color=Y0C, fill_opacity=0.85).move_to(ax.c2p(x + 0.18, 0), aligned_edge=DOWN))
            names.add(label(n, font_size=16, color=GREY_A).rotate(PI / 5).next_to(ax.c2p(x, 0), DOWN, buff=0.35))
        lam = d["lam"]
        lrows = VGroup(label(r"SDID time weights:", font_size=22, color=TAUC),
                       *[label(rf"{y}: \ {v:.2f}", font_size=22, color=GREY_A) for y, v in lam],
                       label(rf"{d['n_omega']} states with weight; \ green: \ SDID, \ blue: \ SC", font_size=22, color=BANDC))
        side = fit_rows(lrows, 3.8, 0.3, [4.6, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For Proposition 99, the synthetic DiD unit weights, in green, are spread over "
            + str(d["n_omega"]) + " states, led by Nevada, New Hampshire, Connecticut and Delaware. <bookmark mark='b'/> The "
            "synthetic control's weights, in blue, concentrate on a few: Utah, Montana and Nevada. <bookmark mark='c'/> The "
            "time weights fall entirely on the last three years before the law, 1986 to 1988: the years most like what "
            "came after."
        ) as vo:
            self.add(prop99_tag())
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(bo), FadeIn(side[-1]))
            vo.wait_until("b")
            self.play(FadeIn(bs))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in side[:-1]], lag_ratio=0.2))
        self.clear_scene()

    def table(self):
        d = load("sdid")
        se = d["se"]
        rows = [[r"estimator", r"effect (packs)", r"placebo SE", r"paper's estimate (SE)"],
                [r"DiD", f"{d['did']:.1f}", f"{se['did']:.1f}", r"$-$27.3 \ (17.7)"],
                [r"synthetic control", f"{d['sc']:.1f}", f"{se['sc']:.1f}", r"$-$19.6 \ (9.9)"],
                [r"synthetic DiD", f"{d['tau']:.1f}", f"{se['sdid']:.1f}", r"$-$15.6 \ (8.4)"]]
        for r in rows[1:]:
            r[1] = r[1].replace("-", "$-$")
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.36, colors=[GREY_A, Y0C, Y1C, BANDC]).move_to([0, 0.6, 0])
        foot = label(r"Arkhangelsky et al. (2021), \ Table 1; \ our placebo SEs use the 38 controls alone", font_size=22, color=GREY_A).move_to([0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The three estimates of the law's average effect, per person per year, from 1989 to 2000. "
            "<bookmark mark='b'/> Plain difference-in-differences: minus " + say(-d["did"], 1) + " packs, with a placebo "
            "standard error of about seventeen; it credits the law with California's earlier decline. <bookmark mark='c'/> "
            "The synthetic control: minus " + say(-d["sc"], 1) + ". <bookmark mark='d'/> Synthetic DiD: minus "
            + say(-d["tau"], 1) + ", with the smallest standard error. The statistics kit reproduces the paper's "
            "estimates to the decimal; our placebo standard errors are close to theirs."
        ) as vo:
            self.add(prop99_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"in the paper's simulations, \ SDID was never far behind the better of the two, \ and often ahead", font_size=26, color=BANDC),
            label(r"but with one treated state, \ every estimate is within two SEs of every other", font_size=26, color=MISSC),
            label(r"point estimates suggest lower sales; \ 15--25 packs is not a confidence interval", font_size=26, color=TAUC),
            label(r"next: \ panels with many treated units, \ and their fixed effects", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the paper's simulations, built on real panel data, synthetic DiD was rarely far "
            "behind the better of the other two and often ahead of both. <bookmark mark='b'/> But with one treated "
            "state, every estimate lies within two standard errors of every other. <bookmark mark='c'/> The point "
            "estimates suggest lower cigarette sales under the fitted counterfactual models. Fifteen to twenty-five "
            "packs describes the approximate range of these point estimates, not a confidence interval. Sampling "
            "uncertainty is much wider, and causal attribution needs assumptions about comparable trends, other "
            "policies and spillovers. <bookmark mark='d'/> Next, panels with many units, and what their fixed effects"
            " do and do not remove."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
