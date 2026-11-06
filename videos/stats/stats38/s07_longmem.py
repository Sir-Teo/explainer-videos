from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class LongMemory(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.acfs()
        self.estimate()
        self.mean()
        self.elsewhere()
        self.caveat()

    def card(self):
        card = chapter_card(6, r"Long memory", r"Correlations that fade like a power, \ not an exponential", lit=(1980, 1981), part=PART)
        with self.voiceover("Chapter six. Long memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"(1 - B)^d X_t", r"=", r"\varepsilon_t, \quad (1 - B)^d = \textstyle\sum_k \pi_k B^k", font_size=30),
            cmath(r"\pi_k", r"=", r"\pi_{k-1}\, \dfrac{k - 1 - d}{k} \ \sim \ k^{-d-1}", font_size=30),
            cmath(r"\rho_k", r"=", r"\textstyle\prod_{j=1}^k \dfrac{j - 1 + d}{j - d} \ \sim \ c\, k^{2d - 1}", font_size=30),
            cmath(r"0 < d < \tfrac12", r":", r"\text{stationary, \ } \textstyle\sum_k \rho_k = \infty; \ H = d + \tfrac12", font_size=30),
        ]
        rows[2][-1].set_color(LMC)
        whys = [why(r"Granger \& Joyeux (1980); \ Hosking (1981)"), why(r"fractional differencing"),
                why(r"a power law, \ not $\phi^k$"), why(r"Hurst's exponent")]
        with self.voiceover(
            "<bookmark mark='a'/> Clive Granger and Roselyne Joyeux, in 1980, and Jonathan Hosking, in 1981, found a model "
            "with Hurst's behaviour: difference the series a fractional number of times. Differencing once gives a random "
            "walk's increments; differencing d times, with d between zero and a half, is defined by the binomial series. "
            "<bookmark mark='b'/> Its weights decay like a power of the lag. <bookmark mark='c'/> So do its "
            "autocorrelations: like the lag to the power two d minus one, rather than geometrically. <bookmark mark='d'/> "
            "For d below a half the series is stationary, but its autocorrelations sum to infinity, and Hurst's exponent is d "
            "plus a half. Combined with autoregressive and moving-average terms it is called ARFIMA."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def acfs(self):
        d = load("longmem")
        lags = np.asarray(d["lags"], float)
        A = axes([0, 60], [-0.1, 1], x_length=7.6, y_length=4.2, xlabel=r"lag (years)", ylabel=r"autocorrelation",
                 xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1], yfmt=lambda v: f"{v:g}", center=[-1.8, 0.2, 0])
        ax = A.ax
        sm = VGroup(*[Line(ax.c2p(k, 0), ax.c2p(k, v), color=GREY_B, stroke_width=3) for k, v in zip(lags[1:], np.asarray(d["acf_sample"], float)[1:])])
        cf = polyline(ax, lags, d["acf_frac"], LMC, 3.5)
        ca = polyline(ax, lags, d["acf_ar"], Y0C, 3.5)
        side = fit_rows(VGroup(
            label(r"grey: \ the Nile minima's sample ACF", font_size=22, color=GREY_B),
            label(r"blue: \ an AR(1) with the same lag-one value", font_size=22, color=Y0C),
            label(r"gold: \ ARFIMA, \ $d = 0.4$", font_size=22, color=LMC),
            label(r"at lag 60: \ the AR(1) has forgotten; \ ARFIMA has not", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Nile minima's sample autocorrelations, in grey, for lags up to sixty years. They start "
            "near point six and stay positive for decades. <bookmark mark='b'/> An autoregression with the same first "
            "autocorrelation, in blue, has forgotten within ten years. <bookmark mark='c'/> A fractionally integrated "
            "series with d equal to point four, in gold, decays like a power, and still remembers at lag sixty. <bookmark "
            "mark='d'/> The river looks like the gold curve."
        ) as vo:
            self.add(minima_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(sm), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ca), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def estimate(self):
        d = load("longmem")
        g = d["gph_range"]
        rows = fit_rows(VGroup(
            label(r"near frequency zero, \ $s(f) \propto f^{-2d}$: \ estimate $d$ from the lowest frequencies only", font_size=26, color=SPECC),
            label(r"Geweke \& Porter-Hudak (1983): \ regress $\log I(f_j)$ on $-\log(4\sin^2 \pi f_j)$", font_size=26),
            label(rf"on the minima: \ $\hat d$ from {min(g.values()):.2f} to {max(g.values()):.2f}, \ depending on how many frequencies", font_size=26, color=MISSC),
            label(rf"Robinson's local Whittle (1995), \ $m = n^{{0.65}}$: \ $\hat d$ = {d['d']:.2f} \ (SE {d['se']:.2f}), \ $H$ = {d['H']:.2f}", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Long memory is a statement about the lowest frequencies: near zero, the spectrum grows like "
            "the frequency to the power minus two d. So d can be estimated from the lowest frequencies alone, whatever the "
            "short-run dynamics. <bookmark mark='b'/> John Geweke and Susan Porter-Hudak, in 1983, regressed the log "
            "periodogram on the log of the frequency term. <bookmark mark='c'/> On the Nile minima their estimate moves from "
            + say(min(g.values()), 2) + " to " + say(max(g.values()), 2) + " as the number of frequencies changes: the "
            "bandwidth matters, as always. <bookmark mark='d'/> Peter Robinson's local Whittle estimator is more efficient: d "
            "is " + say(d["d"], 2) + ", with a standard error of " + say(d["se"], 2) + ", so Hurst's exponent is about "
            + say(d["H"], 2) + "."
        ) as vo:
            self.add(minima_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mean(self):
        d = load("longmem")
        rows = [
            cmath(r"\text{Var}(\bar X_n)", r"=", r"\tfrac{\gamma_0}{n} \textstyle\sum_{|h| < n} (1 - \tfrac{|h|}{n}) \rho_h \ \sim \ c\, n^{2d - 1}", font_size=30),
            cmath(r"\text{i.i.d.\ SE}", r":", rf"s/\sqrt{{n}} = {d['se_naive']:.1f}", font_size=30),
            cmath(r"\text{with } d = {d:.2f}".replace("{d:.2f}", f"{d['d']:.2f}"), r":", rf"\text{{SE}} = {d['se_lm']:.0f}, \ \text{{about }} {d['se_lm'] / d['se_naive']:.0f} \text{{ times larger}}", font_size=30),
            cmath(r"\text{effective } n", r"=", rf"{d['neff']:.1f} \ \text{{of }} {d['n']} \text{{ years}}", font_size=30),
        ]
        rows[3][-1].set_color(MISSC)
        whys = [why(r"slower than $1/n$"), why(r"what Part 8 would report"), why(r"if the ARFIMA model holds"),
                why(r"six centuries, \ a handful of observations")]
        with self.voiceover(
            "<bookmark mark='a'/> The consequence is stark. With long memory, the variance of a sample mean shrinks like n "
            "to the power two d minus one, not like one over n. <bookmark mark='b'/> For the six hundred and sixty-three "
            "years of minima, the textbook standard error of the mean level is " + say(d["se_naive"], 1) + ". <bookmark "
            "mark='c'/> If the fractional model with d of " + say(d["d"], 2) + " holds, the honest standard error is about "
            + str(round(d["se_lm"])) + ", " + str(round(d["se_lm"] / d["se_naive"])) + " times larger. <bookmark mark='d'/> "
            "Six centuries of measurements carry about as much information about the long-run mean as "
            + str(round(d["neff"])) + " independent years. That is what Hurst's reservoir was telling him."
        ) as vo:
            self.add(minima_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def caveat(self):
        rows = fit_rows(VGroup(
            label(r"but: \ shifts in the mean, \ or slowly changing regimes, \ mimic long memory", font_size=26, color=MISSC),
            label(r"Diebold \& Inoue (2001): \ regime switching produces Hurst-like statistics", font_size=26),
            label(r"so ``long memory'' and ``occasional breaks'' are hard to tell apart in one series", font_size=26, color=TAUC),
            label(r"either way: \ the mean is far less certain than $s/\sqrt{n}$ says", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A caveat. Occasional shifts in the mean, or regimes that change slowly, produce the same "
            "statistics. <bookmark mark='b'/> Francis Diebold and Atsushi Inoue showed in 2001 that switching models generate "
            "Hurst-like behaviour. <bookmark mark='c'/> With a single series, a fractional process and a stationary series "
            "with occasional breaks are hard to tell apart; the Nile itself fell abruptly around 1899, as chapter seven will "
            "show. <bookmark mark='d'/> Either way, the practical lesson stands: the long-run mean is far less certain than "
            "the textbook standard error claims."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def elsewhere(self):
        rows = fit_rows(VGroup(
            label(r"internet traffic \ (Leland, \ Taqqu, \ Willinger \& Wilson 1994): \ bursty at every time scale", font_size=26, color=LMC),
            label(r"the absolute returns of chapter 5: \ their autocorrelations decay like a power", font_size=26, color=VOLC),
            label(r"temperature records, \ river flows, \ inflation rates", font_size=26, color=Y0C),
            label(r"in each, \ the variance of averages shrinks more slowly than $1/n$", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Long memory turned up far from the Nile. Will Leland, Murad Taqqu, Walter Willinger and "
            "Daniel Wilson found in 1994 that Ethernet traffic is bursty at every time scale, from milliseconds to hours, "
            "which changed how networks were designed. <bookmark mark='b'/> The absolute returns of chapter five have "
            "autocorrelations that decay like a power rather than geometrically, which is why GARCH's persistence comes out "
            "so close to one. <bookmark mark='c'/> Temperature records, river flows and inflation rates show it too. "
            "<bookmark mark='d'/> In each case, averages are less precise than independent-data formulas say, and "
            "averaging over longer periods helps less than one would hope."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
