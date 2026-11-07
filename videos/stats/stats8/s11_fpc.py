from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class FPC(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.curve_()
        self.planning()
        self.surprise()

    def card(self):
        card = chapter_card(10, r"Finite populations", r"When the sample is a sizeable share of everyone", part=PART)
        with self.voiceover("Chapter ten. Finite populations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"\mathrm{Cov}(x_i, x_j)", r"=", r"-\frac{\sigma^2}{N - 1}", r"\quad (i \ne j,\ \text{without replacement})", font_size=32),
            cmath(r"\mathrm{Var}(\bar x)", r"=", r"\frac{\sigma^2}{n} + \frac{n(n - 1)}{n^2}\Big(-\frac{\sigma^2}{N - 1}\Big)", font_size=32),
            cmath(r"\mathrm{Var}(\bar x)", r"=", r"\frac{\sigma^2}{n}\cdot\frac{N - n}{N - 1}", font_size=34),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"$\sigma^2=N^{-1}\sum(x-\mu)^2$; SRS without replacement, $N>1$"),
                why(r"Part 4's variance of a sum, \ with the covariances"), why(r"the finite-population correction")]
        intro = label('Sampling from a finite list without replacement', font_size=36)
        with self.voiceover(
            "Many preceding sampling formulas assumed independent draws, as if sampling from an infinite population or with "
            "replacement. Real surveys sample without replacement from a finite list. <bookmark mark='a'/> Then the "
            "draw values have negative covariance: drawing a high value leaves a lower average among the remaining values. Here sigma squared uses the population divisor N. The covariance between two draws is minus "
            "sigma squared over N minus one. <bookmark mark='b'/> Put that into the variance of a sum. "
            "<bookmark mark='c'/> The variance of the mean is the usual sigma squared over n, times a correction: N "
            "minus n over N minus one, the finite-population correction."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def curve_(self):
        d = load("fpc")
        ns = np.asarray(d["ns"])
        A = axes([0, 400], [0, 3.4], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$ \ (population $N = 400$)",
                 ylabel=r"SE of $\bar x$ (cm)", xticks=[0, 100, 200, 300, 400], yticks=[0, 1, 2, 3], center=[-2.0, -0.4, 0])
        ax = A.ax
        keep = ns >= 10
        wr = curve(ax, ns[keep], np.asarray(d["se_wr"])[keep], GREY_B, 2.5)
        wor = curve(ax, ns[keep], np.asarray(d["se_wor"])[keep], EXACT, 3.5)
        sims = VGroup(*[Dot(ax.c2p(n, v), radius=0.08, color=SIM) for n, v in zip(d["sim_ns"], d["sim"])])
        leg = legend([(GREY_B, r"$\sigma/\sqrt n$: \ with replacement"), (EXACT, r"with the correction"), (SIM, r"simulated")],
                     font_size=22).move_to([4.6, 1.8, 0])
        rows = fit_rows(VGroup(label(r"at $n = N$: \ zero, \ you have measured everyone", font_size=24, color=EXACT),
                               label(r"at $n/N = 1\%$: \ a correction of 0.5\%, \ negligible", font_size=24, color=GREY_A)),
                        4.8, 0.3, [4.6, -0.6, 0])
        tag = simulated_tag(r"simulated: 4,000 samples without replacement at each $n$")
        with self.voiceover(
            "<bookmark mark='a'/> Here's a population of four hundred heights. The grey curve is the usual standard "
            "error. <bookmark mark='b'/> The gold curve includes the correction, and falls to zero at four hundred, "
            "since a sample of everyone has no sampling error at all. <bookmark mark='c'/> The blue dots are simulated "
            "samples without replacement: they sit on the gold curve. When the sample is one percent of the population "
            "or less, the correction is negligible, which is why it's usually ignored."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(wr), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(wor), FadeIn(leg[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in sims], lag_ratio=0.15), FadeIn(leg[2]), FadeIn(rows[1]))
        self.clear_scene()

    def surprise(self):
        rows = fit_rows(VGroup(
            label(r"a surprise: \ precision depends on $n$, \ almost not on $N$", font_size=28, color=S.ACCENT),
            MathTex(r"n = 1{,}000:\ \ \mathrm{SE}(\hat p) \le \tfrac{1}{2\sqrt{1000}} = 1.6\% \ \text{ for a city, a country, or the world}",
                    font_size=28),
            label(r"a spoonful tastes the soup, \ whatever the size of the pot \ \textemdash{} \ if the soup is stirred", font_size=26,
                  color=GREY_A),
            label(r"stirring is random sampling: \ Part 18 (and the \emph{Literary Digest}'s 2.4 million unstirred replies)",
                  font_size=24, color=RESID),
        ), 12.6, 0.4, [0, 0.2, 0])
        intro = label('Precision depends mainly on sample size', font_size=36)
        with self.voiceover(
            "The formula hides a surprise that puzzles people about opinion polls. <bookmark mark='a'/> The precision of "
            "a sample depends on its size, n, and hardly at all on the size of the population, N. "
            "<bookmark mark='b'/> A random sample of a thousand has a proportion standard error of at most about one point six "
            "percentage points; an approximate ninety-five-percent margin is about three point one points, whether the population is a city, a country, or the whole world. "
            "<bookmark mark='c'/> A spoonful tastes the soup, whatever the size of the pot, provided the soup is "
            "stirred. <bookmark mark='d'/> Stirring is random sampling. Part 18 tells the story of a poll that got "
            "two point four million unstirred replies, and missed the election by twenty points. Size is no substitute for "
            "randomness: a huge biased sample only measures its own bias very precisely."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def planning(self):
        d = load("extras")["samplesize"]
        rows = [
            cmath(r"1.96\sqrt{\frac{p(1 - p)}{n}}", r"\le", r"e", r"\ \Rightarrow\ n_0 = \frac{1.96^2\,p(1-p)}{e^2}", font_size=32),
            cmath(r"p = \tfrac12,\ e = 3\%", r":\ ", rf"n_0={d['n0']:.2f},\quad \lceil n_0\rceil={int(np.ceil(d['n0']))}", font_size=32),
            cmath(r"n", r"=", r"\frac{n_0}{1 + (n_0 - 1)/N}", font_size=34),
            cmath(r"N = 2{,}000:\ " + f"{int(np.ceil(d['N']['2000']))}" + r",\quad N = 10{,}000:\ " + f"{int(np.ceil(d['N']['10000']))}", r",\quad",
                  r"N = 10^7:\ " + f"{int(np.ceil(d['N']['10000000']))}", font_size=30),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"SRS normal approximation for a margin; \ $p=1/2$ worst case; round required $n$ up"), why(r"the famous ``about a thousand''"),
                why(r"with the correction: \ solve for $n$"), why(r"a small population needs fewer; \ a large one, no more")]
        intro = label('Plan and round up a survey sample size', font_size=36)
        with self.voiceover(
            "The correction matters most when planning a survey. <bookmark mark='a'/> To estimate a proportion to within "
            "a margin e with ninety-five percent confidence, set one point nine six standard errors equal to e, and "
            "solve for n, then round upward. This is a normal-approximation planning rule. <bookmark mark='b'/> The worst case is p equal to a half, and a three-point margin needs "
            "about a thousand and sixty-eight people: the familiar size of opinion polls. <bookmark mark='c'/> With the "
            "finite-population correction, the required sample shrinks. <bookmark mark='d'/> From a population of two "
            "thousand, you need about seven hundred; from ten thousand, nine hundred and sixty-five; from ten million, "
            "essentially the full thousand and sixty-seven."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
