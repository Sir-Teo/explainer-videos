from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Fission(VoiceoverScene):
    def construct(self):
        self.card()
        self.splitting()
        self.fission()
        self.thinning()
        self.regression()
        self.trade()
        self.compare()
        self.counts()
        self.board()

    def card(self):
        card = chapter_card(5, r"Data fission and thinning", r"Splitting a single observation", lit=(2023,), part=PART)
        with self.voiceover("Chapter five. Data fission and data thinning: splitting a single observation in two."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def splitting(self):
        rows = [
            cmath(r"\text{sample splitting}", r":", r"\text{select on one half, \ infer on the other}", font_size=36),
            cmath(r"\text{valid}", r":", r"\text{the second half is independent of the selection}", font_size=34),
            cmath(r"\text{costs}", r":", r"\text{half the data each; \ needs replicates}", font_size=32),
            cmath(r"\text{question}", r":", r"\text{can a single } X \text{ be split into two independent pieces?}", font_size=34),
        ]
        rows[1][-1].set_color(HYBC)
        rows[2][-1].set_color(NAIVEC)
        whys = [why(r"Cox (1975)"), why(r"by independence"), why(r"one pixel, \ one count, \ one region"), why(r"Leiner, \ Duan, \ Wasserman \& Ramdas")]
        with self.voiceover(
            "<bookmark mark='a'/> The oldest fix is sample splitting, studied by David Cox in 1975: select on one half of the "
            "data and infer on the other. <bookmark mark='b'/> It is valid for any selection rule, because the second half "
            "is independent of what was selected. <bookmark mark='c'/> But it halves the data for each job, and it is "
            "impossible when there is only one observation per unit: one count per region, one measurement per gene. "
            "<bookmark mark='d'/> James Leiner, Boyan Duan, Larry Wasserman and Aaditya Ramdas asked whether a single "
            "observation could itself be split into two independent pieces."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fission(self):
        rows = [
            cmath(r"X \sim N(\mu, \sigma^2), \ Z \sim N(0, \sigma^2)", r":", r"f = X + \tau Z, \ \ g = X - Z/\tau", font_size=34),
            cmath(r"\mathrm{Cov}(f, g)", r"=", r"\sigma^2 - \tau\cdot\tfrac1\tau\,\sigma^2 = 0 \ \Rightarrow \ f \perp g", font_size=34),
            cmath(r"f \sim N(\mu, (1 + \tau^2)\sigma^2)", r",", r"g \sim N(\mu, (1 + \tau^{-2})\sigma^2)", font_size=34),
            cmath(r"\text{use}", r":", r"\text{select with } f, \ \text{infer with } g: \ \text{exactly valid, \ any rule}", font_size=34),
        ]
        rows[1][-1].set_color(PROOFC)
        rows[3][-1].set_color(SPLITC)
        whys = [why(r"add and subtract the same noise"), why(r"jointly Gaussian"), why(r"both carry $\mu$"), why(r"data fission (2025)")]
        with self.voiceover(
            "<bookmark mark='a'/> For a normal observation, the answer is a short calculation. Draw independent noise Z with "
            "the same variance; let f be X plus tau Z and g be X minus Z over tau. <bookmark mark='b'/> Their covariance is "
            "sigma squared minus tau times one over tau times sigma squared: zero. They are jointly Gaussian, so they are "
            "independent. <bookmark mark='c'/> Both carry the same mean, with variances inflated by one plus tau squared and "
            "one plus one over tau squared. <bookmark mark='d'/> So select with f, and infer with g: the inference is "
            "exactly valid, whatever the selection rule."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def thinning(self):
        d = load("fission")["thin"]
        rows = [
            cmath(r"X \sim \mathrm{Poisson}(\lambda)", r":", r"X_1 \mid X \sim \mathrm{Bin}(X, \varepsilon), \ \ X_2 = X - X_1", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"X_1 \sim \mathrm{Poisson}(\varepsilon\lambda) \perp X_2 \sim \mathrm{Poisson}((1 - \varepsilon)\lambda)", font_size=34),
            cmath(r"\text{general}", r":", r"\text{convolution-closed families}", font_size=32),
            cmath(r"\text{check}", r":", rf"\varepsilon = \tfrac12, \ \lambda = 8: \ \text{{means }} {d['mean_a']:.2f}, {d['mean_b']:.2f}; \ \text{{correlation }} {d['corr']:+.4f}", font_size=32),
        ]
        rows[1][-1].set_color(PROOFC)
        whys = [why(r"thinning a Poisson process"), why(r"a classical fact"), why(r"Neufeld, \ Dharamshi, \ Gao \& Witten (2024)"), why(r"100,000 simulated counts")]
        with self.voiceover(
            "<bookmark mark='a'/> For counts, the analogue is thinning. Given a Poisson count, keep each event independently "
            "with probability epsilon. <bookmark mark='b'/> The kept and discarded counts are independent Poisson variables, "
            "a classical fact about thinning a Poisson process. <bookmark mark='c'/> Anna Neufeld, Ameer Dharamshi, Lucy Gao "
            f"and Daniela Witten extended the idea to every convolution-closed family. <bookmark mark='d'/> A check: with "
            f"epsilon a half and a mean of eight, the two pieces have means {say(d['mean_a'], 2)} and {say(d['mean_b'], 2)}, "
            f"and a correlation of {say(d['corr'], 4)}."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def regression(self):
        rows = [
            cmath(r"\text{fixed-design regression}", r":", r"y_i = \mu(x_i) + \varepsilon_i, \ \ \varepsilon \sim N(0, \sigma^2 I)", font_size=34),
            cmath(r"\text{fission}", r":", r"f = y + \tau Z, \ \ g = y - Z/\tau: \ \text{select a model with } f", font_size=34),
            cmath(r"\text{infer with } g", r":", r"\hat\beta_{\hat M}(g) \text{: \ ordinary OLS intervals, \ for the projection of } \mu", font_size=32),
            cmath(r"\text{beyond}", r":", r"\text{GLMs, \ trend filtering, \ interactive selection}", font_size=34),
        ]
        rows[2][-1].set_color(HYBC)
        whys = [why(r"Leiner et al., \ Section 4"), why(r"any selection: \ lasso, \ stepwise, \ eyeballing"), why(r"PoSI's target, \ no constant needed"), why(r"the paper's examples")]
        with self.voiceover(
            "<bookmark mark='a'/> Fission works for whole regressions. With a fixed design and Gaussian noise, "
            "<bookmark mark='b'/> fission the response vector into f and g, and choose a model with f by any means: "
            "the lasso, stepwise, or looking at plots. <bookmark mark='c'/> Then fit the chosen model to g by least "
            "squares; its ordinary intervals are valid for the projection of the mean onto the chosen columns, PoSI's "
            "target, with no inflation constant at all. <bookmark mark='d'/> Leiner and colleagues extend this to "
            "generalized linear models, to trend filtering, and to interactive procedures where an analyst selects in "
            "several rounds."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trade(self):
        d = load("fission")
        tr = d["trade"]
        lt = np.log2([r["tau"] for r in tr])
        A = axes([-2.3, 2.3], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$\tau$ \ (log scale): \ more noise in $f$ to the right", ylabel=r"",
                 xticks=[-2, -1, 0, 1, 2], xfmt=lambda v: f"{2 ** v:g}", yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ch = VGroup(polyline(ax, lt, [r["hit"] for r in tr], SELC, 4), *[Dot(ax.c2p(a, r["hit"]), radius=0.07, color=SELC) for a, r in zip(lt, tr)])
        mx = max(r["len"] for r in tr)
        cl = VGroup(polyline(ax, lt, [r["len"] / mx for r in tr], CONDC, 4), *[Dot(ax.c2p(a, r["len"] / mx), radius=0.07, color=CONDC) for a, r in zip(lt, tr)])
        side = fit_rows(VGroup(
            label(rf"select the largest of {d['K']} means", font_size=22),
            label(rf"gold: \ $f$ picks the best: \ {tr[0]['hit']:.2f} $\to$ {tr[-1]['hit']:.2f}", font_size=22, color=SELC),
            label(rf"blue: \ $g$'s interval: \ {tr[0]['len']:.1f} $\to$ {tr[-1]['len']:.1f} \ (scaled)", font_size=22, color=CONDC),
            label(r"$\tau$ trades selection for precision", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Fission has a dial, tau. Select the largest of twenty means, with true values two, one, a "
            f"half and zeros. <bookmark mark='b'/> In gold, how often the selection made with f picks the truly largest: "
            f"{say(tr[0]['hit'], 2)} with tau a quarter, falling to {say(tr[-1]['hit'], 2)} with tau four, because f then "
            f"carries more noise. <bookmark mark='c'/> In blue, the length of the interval made with g: long for small tau, "
            f"{say(tr[0]['len'], 1)}, and close to the ordinary {say(tr[-1]['len'], 1)} for large tau. <bookmark mark='d'/> "
            f"Tau trades the quality of the selection against the precision of the inference, the same trade as choosing "
            f"how to split a sample."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 2,000 runs per point")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def compare(self):
        d = load("fission")["methods"]
        hdr = [r"method", r"picks the largest", r"coverage", r"interval length"]
        names = {"naive": r"reuse all the data", "split": r"split the sample in half", "fission": r"fission, \ $\tau = 1$"}
        cols = {"naive": NAIVEC, "split": SPLITC, "fission": HYBC}
        body = [[names[k], f"{100 * d[k]['hit']:.1f}\\%", f"{100 * d[k]['coverage']:.1f}\\%", f"{d[k]['len']:.2f}"] for k in ("naive", "split", "fission")]
        tab = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.3, colors=[GREY_B] + [cols[k] for k in ("naive", "split", "fission")]).move_to([0, 0.5, 0])
        foot = fit_rows(VGroup(
            label(r"20 means, \ the largest 2; \ 3,000 runs", font_size=22, color=GREY_A),
            label(r"splitting and fission with $\tau = 1$ are equivalent here: \ both halve the information", font_size=24, color=SPLITC),
            label(r"fission's point: \ it works when a sample cannot be split", font_size=24, color=HYBC),
        ), 12.4, 0.25, [0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The three approaches side by side. <bookmark mark='b'/> Reusing all the data picks the "
            f"truly largest mean most often, {100 * d['naive']['hit']:.0f} percent of the time, but its intervals cover only "
            f"{100 * d['naive']['coverage']:.1f} percent. <bookmark mark='c'/> Splitting the sample covers "
            f"{100 * d['split']['coverage']:.1f} percent, and fission {100 * d['fission']['coverage']:.1f}, both with "
            f"intervals longer by a factor of root two. <bookmark mark='d'/> In this Gaussian problem splitting and fission "
            f"with tau one are equivalent; fission's value is that it still works when there is nothing to split."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def counts(self):
        rows = [
            cmath(r"\text{single-cell RNA}", r":", r"\text{counts } X_{ij}: \ \text{cluster cells, \ then find marker genes}", font_size=34),
            cmath(r"\text{count splitting}", r":", r"\text{thin each count: \ cluster on } X^{(1)}, \text{ test on } X^{(2)}", font_size=34),
            cmath(r"\text{Poisson}", r":", r"\text{exact; \ negative binomial needs the dispersion}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the double dipping of chapter 9, \ avoided by construction}", font_size=34),
        ]
        rows[1][-1].set_color(SPLITC)
        rows[3][-1].set_color(HYBC)
        whys = [why(r"a common pipeline"), why(r"Neufeld et al. (2022)"), why(r"convolution-closed only"), why(r"a preview")]
        with self.voiceover(
            "<bookmark mark='a'/> The most popular application is in single-cell genomics. Counts of each gene in each "
            "cell are clustered into cell types, and then the same counts are tested to find the genes that mark each "
            "type. <bookmark mark='b'/> Count splitting, by Neufeld and colleagues, thins every count into two: "
            "cluster on one, test on the other. <bookmark mark='c'/> For Poisson counts the pieces are exactly "
            "independent; for negative binomial counts, the overdispersion must be known or estimated. <bookmark "
            "mark='d'/> It avoids by construction the double dipping that chapter nine attacks by conditioning."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("fission"),
                   f"<bookmark mark='a'/> On the Board: the fission interval for the selected largest of twenty means covers "
                   f"{100 * br[5]['achieved']:.1f} percent: kept, with no conditioning and no model of the selection rule.",
                   [("a", [0])])
