from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Spectra(VoiceoverScene):
    def construct(self):
        self.card()
        self.herglotz()
        self.sunspots()
        self.inconsistent()
        self.welch_mt()
        self.sun_spectrum()
        self.lesson()

    def card(self):
        card = chapter_card(2, r"Spectra", r"A series, \ one frequency at a time", lit=(1967, 1982), part=PART)
        with self.voiceover("Chapter two. Spectra."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def herglotz(self):
        rows = [
            cmath(r"\gamma(h)", r"=", r"\int_{-1/2}^{1/2} e^{2\pi i f h}\, dF(f)", font_size=32),
            cmath(r"s(f)", r"=", r"\textstyle\sum_{h} \gamma(h)\, e^{-2\pi i f h}", font_size=32),
            cmath(r"\text{AR}(p)", r":", r"s(f) = \dfrac{\sigma^2}{|1 - \sum_k \phi_k e^{-2\pi i f k}|^2}", font_size=30),
            cmath(r"\int s(f)\, df", r"=", r"\gamma(0): \ \text{the variance, \ shared among frequencies}", font_size=30),
        ]
        rows[1][-1].set_color(SPECC)
        whys = [why(r"Herglotz: \ every autocovariance"), why(r"the spectral density"), why(r"a peak near a pseudo-cycle"),
                why(r"Part 17's ACF, \ in another basis")]
        with self.voiceover(
            "<bookmark mark='a'/> Gustav Herglotz's theorem says that every stationary autocovariance function is the Fourier "
            "transform of a non-decreasing function on the frequencies from minus a half to a half cycle per observation. "
            "<bookmark mark='b'/> When the autocovariances are summable, that function has a density, the spectrum, which "
            "is the Fourier transform of the autocovariances. <bookmark mark='c'/> For an autoregression it is the noise "
            "variance divided by the squared modulus of the autoregressive polynomial on the unit circle, with a peak at the "
            "frequency of any pseudo-cycle. <bookmark mark='d'/> The spectrum integrates to the variance: it says how the "
            "variance is shared among frequencies. It holds the same information as the autocorrelations, arranged by "
            "frequency rather than by lag."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sunspots(self):
        d = load("spectra")["sun"]
        yrs, x = np.asarray(d["years"], float), np.asarray(d["x"], float)
        A = axes([1700, 2010], [0, 200], x_length=10.4, y_length=3.8, xlabel=r"year", ylabel=r"sunspot number",
                 xticks=[1700, 1800, 1900, 2000], yticks=[0, 100, 200], xfmt=lambda v: f"{v:.0f}", center=[0, 0.4, 0])
        line = series_line(A.ax, yrs, x, TAUC, 1.8)
        foot = fit_rows(VGroup(
            label(r"Schwabe (1843): \ a cycle of about ten years; \ Yule (1927): \ an AR(2) fits it \ (Part 17)", font_size=24, color=GREY_A),
            label(rf"Yule's AR(2) here: \ $\phi$ = ({d['ar2'][0]:.2f}, \ {d['ar2'][1]:.2f}), \ a pseudo-period of {d['ar2_period']:.1f} years", font_size=24, color=SPECC),
        ), 12.4, 0.3, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Yearly sunspot numbers, 1700 to 2008. The apothecary Heinrich Schwabe noticed a cycle of "
            "about ten years in 1843, and in Part seventeen we fitted Yule's autoregression of 1927 to it. <bookmark "
            "mark='b'/> An autoregression of order two, fitted here, has a pseudo-period of " + say(d["ar2_period"], 1)
            + " years. Where in frequency does the variance live?"
        ) as vo:
            self.add(sun_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def inconsistent(self):
        d = load("spectra")["wn"]
        A = axes([0, 0.5], [0, 6], x_length=5.4, y_length=3.4, xlabel=r"frequency", ylabel=r"periodogram",
                 xticks=[0, 0.25, 0.5], yticks=[0, 2, 4, 6], xfmt=lambda v: f"{v:g}", center=[-3.6, 0.2, 0])
        B = axes([0, 0.5], [0, 6], x_length=5.4, y_length=3.4, xlabel=r"frequency", ylabel=r"",
                 xticks=[0, 0.25, 0.5], yticks=[0, 2, 4, 6], xfmt=lambda v: f"{v:g}", center=[2.8, 0.2, 0])
        f1, I1 = np.asarray(d["f_small"], float), np.clip(np.asarray(d["I_small"], float), 0, 6)
        f2, I2 = np.asarray(d["f_big"], float), np.clip(np.asarray(d["I_big"], float), 0, 6)
        d1 = VGroup(*[Dot(A.ax.c2p(a, b), radius=0.035, color=SPECC) for a, b in zip(f1, I1)])
        d2 = VGroup(*[Dot(B.ax.c2p(a, b), radius=0.02, color=SPECC, fill_opacity=0.6) for a, b in zip(f2, I2)])
        t1 = DashedLine(A.ax.c2p(0, 1), A.ax.c2p(0.5, 1), color=TRUEC, stroke_width=2.5)
        t2 = DashedLine(B.ax.c2p(0, 1), B.ax.c2p(0.5, 1), color=TRUEC, stroke_width=2.5)
        w = polyline(B.ax, d["f_w"], d["S_w"], BANDC, 3)
        lab = VGroup(label(r"white noise, \ $n = 128$", font_size=22, color=GREY_A).next_to(A, UP, buff=0.1),
                     label(r"$n = 2{,}048$", font_size=22, color=GREY_A).next_to(B, UP, buff=0.1))
        foot = fit_rows(VGroup(
            label(rf"spread around the true flat spectrum: \ {d['sd_small']:.2f} with 128 points, \ {d['sd_big']:.2f} with 2,048", font_size=22, color=MISSC),
            label(rf"Welch: \ average {d['k']} tapered segments: \ spread {d['sd_w']:.2f} \ (green)", font_size=22, color=BANDC),
        ), 12.4, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The natural estimate of the spectrum is the periodogram: the squared size of the series' "
            "Fourier coefficient at each frequency. For white noise, the true spectrum is flat, at one. <bookmark mark='b'/> "
            "With a hundred and twenty-eight observations, the periodogram scatters wildly around it. <bookmark mark='c'/> "
            "With sixteen times as many, it scatters just as wildly; there are just more points. Each ordinate is "
            "asymptotically the true spectrum times an exponential variable, with a standard deviation equal to its mean, "
            "however long the series. The periodogram is unbiased and inconsistent. <bookmark mark='d'/> The cure is to "
            "average. Peter Welch, in 1967, cut the series into overlapping segments, tapered each to reduce leakage, and "
            "averaged their periodograms: the spread falls to " + say(d["sd_w"], 2) + "."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(B), FadeIn(lab), Create(t1), Create(t2))
            vo.wait_until("b")
            self.play(FadeIn(d1))
            vo.wait_until("c")
            self.play(FadeIn(d2), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(Create(w), FadeIn(foot[1]))
        self.clear_scene()

    def welch_mt(self):
        rows = [
            cmath(r"I(f_j)", r"\approx", r"s(f_j)\, \tfrac{1}{2}\chi^2_2 \quad \text{(independent over } j)", font_size=30),
            cmath(r"\text{Welch}", r":", r"\text{average segments: \ less variance, \ coarser frequencies}", font_size=30),
            cmath(r"\text{multitaper}", r":", r"\text{average over } K \text{ orthogonal Slepian tapers of the whole series}", font_size=30),
            cmath(r"\text{the trade}", r":", r"\text{bias (resolution) against variance, \ as in Part 29}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"why it never settles"), why(r"Welch (1967)"), why(r"Thomson (1982)"), why(r"a smoothing problem")]
        with self.voiceover(
            "<bookmark mark='a'/> The arithmetic: each periodogram ordinate is the true spectrum times a chi-square on two "
            "degrees of freedom, halved, and different Fourier frequencies are nearly independent. <bookmark mark='b'/> "
            "Welch's averages reduce the variance, at the cost of resolution, because each segment is shorter. <bookmark "
            "mark='c'/> David Thomson's multitaper method of 1982 instead multiplies the whole series by several orthogonal "
            "tapers, the Slepian sequences that concentrate their energy best in a narrow band, and averages those "
            "periodograms. <bookmark mark='d'/> Either way it is Part twenty-nine's trade between bias and variance: "
            "spectral estimation is a smoothing problem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sun_spectrum(self):
        d = load("spectra")["sun"]
        f, I = np.asarray(d["f"], float), np.asarray(d["I"], float)
        fw, Sw = np.asarray(d["f_w"], float), np.asarray(d["S_w"], float)
        fm, Sm = np.asarray(d["f_mt"], float), np.asarray(d["S_mt"], float)
        ar = np.asarray(d["ar2_spec"], float)
        lg = lambda v: np.clip(np.log10(np.maximum(v, 1.0)), 0, 5.5)
        A = axes([0, 0.5], [0, 5.5], x_length=8.0, y_length=4.2, xlabel=r"frequency (cycles per year)", ylabel=r"spectrum (log scale)",
                 xticks=[0, 0.09, 0.25, 0.5], yticks=[1, 3, 5], xfmt=lambda v: f"{v:g}", yfmt=lambda v: rf"10^{int(v)}",
                 center=[-1.6, 0.2, 0])
        ax = A.ax
        pd = VGroup(*[Dot(ax.c2p(a, b), radius=0.025, color=GREY_B, fill_opacity=0.6) for a, b in zip(f, lg(I))])
        cw = polyline(ax, fw, lg(Sw), BANDC, 3)
        cm = polyline(ax, fm, lg(Sm), SPECC, 3)
        ca = polyline(ax, f, lg(ar), TAUC, 2.5)
        side = fit_rows(VGroup(
            label(rf"grey: \ periodogram, \ peak at {d['peak_I']:.1f} years", font_size=22, color=GREY_B),
            label(rf"green: \ Welch, \ {d['peak_w']:.1f} years", font_size=22, color=BANDC),
            label(rf"purple: \ multitaper, \ {d['peak_mt']:.1f} years", font_size=22, color=SPECC),
            label(rf"gold: \ Yule's AR(2) spectrum, \ {d['ar2_period']:.1f}", font_size=22, color=TAUC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The sunspot spectrum, on a log scale. The raw periodogram, in grey, has its highest point at "
            + say(d["peak_I"], 1) + " years, surrounded by noise. <bookmark mark='b'/> Welch's estimate smooths it into a "
            "single clear peak near frequency nought point nine, about eleven years. <bookmark mark='c'/> The multitaper "
            "estimate agrees, with finer detail. <bookmark mark='d'/> And the two-parameter autoregression's spectrum puts a "
            "smooth peak in the same place: Yule's model is a smoothed spectrum."
        ) as vo:
            self.add(sun_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(pd), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ca), FadeIn(side[3]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the spectrum and the ACF are one object in two bases", font_size=26, color=SPECC),
            label(r"periodograms need smoothing; \ peaks need a null to be judged against", font_size=26, color=MISSC),
            label(r"a unit root puts infinite power at frequency zero; \ long memory, \ a pole there", font_size=26, color=LMC),
            label(r"next: \ the series with no mean to return to", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The spectrum and the autocorrelation function are one object, written in two bases. "
            "<bookmark mark='b'/> Periodograms need smoothing, and an apparent peak needs a null spectrum to be judged "
            "against, or every noisy series seems to cycle. <bookmark mark='c'/> And the frequency view shows the next two "
            "departures at a glance: a random walk puts infinite power at frequency zero, and long memory a pole there that "
            "can still be integrated. <bookmark mark='d'/> Next, the series with no mean to return to."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
