from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class BlockBootstrap(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.blocks()
        self.numbers()
        self.nile()
        self.choose_b()
        self.board()

    def card(self):
        card = chapter_card(11, r"The block bootstrap", r"Resampling without breaking the memory", lit=(1989, 1994), part=PART)
        with self.voiceover("Chapter eleven. The block bootstrap."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"Part 16's bootstrap resamples observations independently", font_size=26, color=GREY_A),
            label(r"for a series, \ that shuffles away the dependence: \ the resamples are white noise", font_size=26, color=MISSC),
            label(r"so it estimates the variance the mean would have if the data were independent", font_size=26),
            label(r"positive autocorrelation: \ that is too small", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part sixteen's bootstrap resamples the observations independently, with replacement. "
            "<bookmark mark='b'/> Applied to a time series, it shuffles the order away: every resampled series is white "
            "noise, whatever the original was. <bookmark mark='c'/> So it estimates the variability the mean would have if "
            "the observations were independent. <bookmark mark='d'/> With positive autocorrelation, that is too small, just "
            "as the naive standard error was in Part seventeen."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def blocks(self):
        d = load("bootstrap")
        x = np.asarray(d["x"], float)[:150]
        A = axes([0, 150], [-4, 4], x_length=10.4, y_length=1.8, xlabel=r"", ylabel=r"", xticks=[], yticks=[], center=[0, 2.0, 0])
        B = axes([0, 150], [-4, 4], x_length=10.4, y_length=1.8, xlabel=r"", ylabel=r"", xticks=[], yticks=[], center=[0, -0.6, 0])
        orig = series_line(A.ax, np.arange(150), x, Y0C, 1.8)
        g = np.random.default_rng(1)
        b = 15
        starts = g.integers(0, 150 - b, 10)
        pieces = VGroup()
        cols = [Y0C, TAUC, BANDC, SPECC, MISSC]
        for i, s in enumerate(starts):
            seg = x[s:s + b]
            src = Rectangle(width=A.ax.c2p(b, 0)[0] - A.ax.c2p(0, 0)[0], height=1.8, stroke_color=cols[i % 5], stroke_width=2,
                            fill_opacity=0).move_to(A.ax.c2p(s + b / 2, 0))
            dst = series_line(B.ax, np.arange(i * b, (i + 1) * b), seg, cols[i % 5], 1.8)
            pieces.add(VGroup(src, dst))
        lab = VGroup(label(r"the series", font_size=22, color=GREY_A).next_to(A, LEFT, buff=0.2),
                     label(r"a resample", font_size=22, color=GREY_A).next_to(B, LEFT, buff=0.2))
        foot = fit_rows(VGroup(
            label(r"K\"unsch (1989): \ glue together randomly chosen overlapping blocks of length $b$", font_size=24, color=TAUC),
            label(r"Politis \& Romano (1994): \ random geometric lengths, \ wrapping round: \ the stationary bootstrap", font_size=24, color=BANDC),
            label(r"$b$ grows with $n$, \ like $n^{1/3}$ for the variance of a mean", font_size=24, color=GREY_A),
        ), 12.4, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The fix, published by Hans Künsch in 1989, is to resample blocks instead of points. "
            "<bookmark mark='b'/> Choose a block length, pick blocks of consecutive observations at random, and glue them "
            "together to make a series of the original length. Within each block the dependence survives; only at the joins "
            "is it broken. <bookmark mark='c'/> Dimitris Politis and Joseph Romano's stationary bootstrap of 1994 draws the "
            "block lengths at random, so that the resampled series are themselves stationary. <bookmark mark='d'/> The block "
            "length must grow with the sample, but slowly, about as the cube root of n for the variance of a mean."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(B), Create(orig), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(p[0]), Create(p[1])) for p in pieces], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def numbers(self):
        d = load("bootstrap")
        rows = [[r"standard error of the mean, \ AR(1), \ $\phi = 0.5$, \ $n = 500$", r"SE"],
                [r"i.i.d.\ bootstrap", f"{d['sd_iid']:.3f}"],
                [r"moving-block bootstrap, \ $b = 30$", f"{d['sd_block']:.3f}"],
                [r"stationary bootstrap, \ mean block 30", f"{d['sd_stat']:.3f}"],
                [r"Newey--West \ (Part 17)", f"{d['nw']:.3f}"],
                [r"the truth", f"{d['true_sd']:.3f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.3, colors=[GREY_A, MISSC, BANDC, BANDC, TAUC, TRUEC]).move_to([0, 0.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One series of five hundred from an autoregression with coefficient a half. <bookmark "
            "mark='b'/> The ordinary bootstrap's standard error for the mean is " + say(d["sd_iid"], 3) + ". <bookmark "
            "mark='c'/> The moving-block and stationary bootstraps give about " + say(d["sd_block"], 3) + ", <bookmark "
            "mark='d'/> close to Newey and West's estimate from Part seventeen <bookmark mark='e'/> and to the true value, "
            + say(d["true_sd"], 3) + ". The ordinary bootstrap was off by a factor of the square root of three, the ratio "
            "that the autocorrelation implies."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]))
            vo.wait_until("e")
            self.play(FadeIn(tab[5]))
        self.clear_scene()

    def nile(self):
        d = load("bootstrap")
        nb = d["nile_block"]
        bs = [5, 20, 50, 100]
        A = axes([0, 110], [0, 60], x_length=7.4, y_length=4.0, xlabel=r"block length (years)", ylabel=r"bootstrap SE of the mean",
                 xticks=[0, 25, 50, 75, 100], yticks=[0, 20, 40, 60], center=[-1.8, 0.2, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(b, nb[str(b)]), radius=0.09, color=BANDC) for b in bs])
        ln = polyline(ax, [0] + bs, [d["nile_iid"]] + [nb[str(b)] for b in bs], BANDC, 2.5)
        lm = DashedLine(ax.c2p(0, d["nile_lm"]), ax.c2p(110, d["nile_lm"]), color=LMC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(rf"the Nile minima: \ i.i.d.\ {d['nile_iid']:.1f}", font_size=22, color=GREY_A),
            label(rf"blocks of 5, \ 20, \ 50, \ 100: \ {nb['5']:.1f}, \ {nb['20']:.1f}, \ {nb['50']:.1f}, \ {nb['100']:.1f}", font_size=22, color=BANDC),
            label(rf"gold: \ the ARFIMA answer, \ {d['nile_lm']:.0f}", font_size=22, color=LMC),
            label(r"no plateau: \ under long memory, \ no block is long enough", font_size=22, color=MISSC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now try it on the Nile minima. With short memory, the block bootstrap's standard error "
            "rises with the block length and then levels off, once the blocks are longer than the memory. <bookmark "
            "mark='b'/> Here it keeps rising: " + say(nb["5"], 1) + " with blocks of five years, " + say(nb["100"], 1)
            + " with blocks of a century. <bookmark mark='c'/> The long-memory calculation of chapter six says about "
            + str(round(d["nile_lm"])) + ". <bookmark mark='d'/> There is no plateau because, under long memory, no block "
            "is long enough. The block bootstrap assumes the memory is short, and that assumption, like every other in this "
            "part, has to be checked."
        ) as vo:
            self.add(minima_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(pts), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def board(self):
        rows = board_rows("bootstrap CI")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, five hundred autoregressive series of length five hundred. The "
                   "ordinary bootstrap's ninety percent interval for the mean covers " + f"{100 * rows[0].achieved:.0f}"
                   + " percent of the time: broken. <bookmark mark='b'/> The moving-block bootstrap with blocks of thirty: "
                   + f"{100 * rows[1].achieved:.0f}" + " percent, kept.",
                   [("a", [0]), ("b", [1])])

    def choose_b(self):
        rows = fit_rows(VGroup(
            label(r"too short a block: \ the dependence is cut, \ the SE too small; \ too long: \ few blocks, \ noisy", font_size=26, color=MISSC),
            label(r"Politis \& White (2004): \ choose $b$ automatically from the estimated autocorrelations", font_size=26, color=TAUC),
            label(r"alternatives: \ subsampling, \ the sieve bootstrap \ (fit an AR, \ resample its residuals)", font_size=26, color=BANDC),
            label(r"all assume short memory: \ the Nile breaks them all", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Choosing the block length is the bootstrap's own bias-variance trade. Too short, and the "
            "dependence is cut at too many joins, so the standard error is too small. Too long, and there are few distinct "
            "blocks, so it is noisy. <bookmark mark='b'/> Dimitris Politis and Halbert White proposed in 2004 a rule that "
            "chooses the length from the estimated autocorrelations. <bookmark mark='c'/> Alternatives include subsampling, "
            "which recomputes the statistic on shorter stretches of the series, and the sieve bootstrap, which fits a long "
            "autoregression and resamples its residuals. <bookmark mark='d'/> All of them assume the memory is short, which "
            "the Nile's minima do not respect."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
