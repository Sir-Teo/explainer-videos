from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Scale(VoiceoverScene):
    def construct(self):
        self.card()
        self.copper()
        self.mad_def()
        self.masking1d()
        self.qn_def()
        self.mscale()
        self.table()
        self.why_scale()

    def card(self):
        card = chapter_card(6, r"Robust scale", r"MAD, \ $Q_n$, \ $S_n$", lit=(1993,), part=PART)
        with self.voiceover("Chapter six. Robust measures of scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def copper(self):
        d = load("scale")
        x = np.sort(np.asarray(d["x"]))
        A = axes([0, 30], [-0.5, 1.5], x_length=10.4, y_length=2.4, xlabel=r"copper in wholemeal flour (ppm)", ylabel=r"",
                 xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[], center=[-0.4, 1.4, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(v, 0.3 + 0.12 * (k % 4)), radius=0.07, color=WHITE) for k, v in enumerate(x)])
        rows = fit_rows(VGroup(
            label(rf"{d['n']} determinations; \ one reads 28.95", font_size=24),
            label(rf"mean {d['mean']:.2f}, \ SD {d['sd']:.2f}", font_size=24, color=MEANC),
            label(rf"median {d['median']:.3f}, \ MAD {d['mad']:.3f}, \ $Q_n$ {d['qn']:.3f}", font_size=24, color=MEDC),
            label(rf"Huber {d['huber']:.3f}, \ Hodges--Lehmann {d['hl']:.3f}", font_size=24, color=HUBC),
            label(rf"without 28.95: \ mean {d['clean_mean']:.2f}, \ SD {d['clean_sd']:.2f}", font_size=24, color=GREY_A),
        ), 12.0, 0.3, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Analytical Methods Committee's copper data: twenty-four determinations of copper in "
            "wholemeal flour, one of which reads twenty-nine parts per million, nine times the rest. "
            "<bookmark mark='b'/> It pulls the mean to four point two eight and inflates the standard deviation to five "
            "point three. <bookmark mark='c'/> The median, three point three nine, and the robust scales, MAD point five "
            "three and Qn point six three, ignore it. <bookmark mark='d'/> Huber and Hodges–Lehmann sit at three point two. "
            "<bookmark mark='e'/> Removing the stray by hand gives a mean of three point two one and an SD of point six "
            "nine: the robust answers, without anyone having to decide what to delete."
        ) as vo:
            self.add(chem_tag())
            self.play(FadeIn(A), LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.05))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def mad_def(self):
        rows = [
            cmath(r"\mathrm{MAD}", r"=", r"1.4826 \cdot \mathrm{median}_i |x_i - \mathrm{median}_j\, x_j|", font_size=30),
            cmath(r"1.4826", r"=", r"1/\Phi^{-1}(3/4)", font_size=32),
            cmath(r"\text{breakdown}", r":", r"50\%", font_size=32),
            cmath(r"\text{efficiency}", r":", r"37\% \ \text{at the normal}", font_size=32),
        ]
        rows[0][2].set_color(MEDC)
        whys = [why(r"Hampel (1974); \ Gauss had used it"), why(r"consistent for $\sigma$ at the normal"),
                why(r"the most possible"), why(r"Gaussian normalization; \ also defined for skewed distributions")]
        with self.voiceover(
            "<bookmark mark='a'/> The median absolute deviation: the median of the distances from the median, "
            "Hampel's choice, used by Gauss long before. <bookmark mark='b'/> Multiplying by one point four eight two"
            " six makes it estimate sigma at the normal. <bookmark mark='c'/> Its breakdown is fifty percent, the "
            "most possible. <bookmark mark='d'/> But it is only thirty-seven percent efficient at the normal, and it "
            "is a scale functional about the median for skewed distributions too; the multiplier is calibrated "
            "specifically to Gaussian standard deviation."
        ) as vo:
            intro=label('Normal calibration turns median absolute deviation into a scale estimate',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def qn_def(self):
        rows = [
            cmath(r"Q_n", r"=", r"2.2219\, \{|x_i - x_j| : i < j\}_{(k)}, \ \ k = \tbinom{h}{2}, \ h = \lfloor n/2 \rfloor + 1", font_size=26),
            cmath(r"S_n", r"=", r"1.1926\, \mathrm{lowmed}_i\, \mathrm{highmed}_j |x_i - x_j|", font_size=30),
            cmath(r"\text{no centre}", r":", r"\text{pairwise distances only}", font_size=30),
            cmath(r"\text{efficiency}", r":", r"Q_n \ 82\%, \ \ S_n \ 58\%, \ \ \text{both } 50\% \text{ breakdown}", font_size=28),
        ]
        rows[0][2].set_color(HLC)
        whys = [why(r"about the first quartile of the pairwise gaps"), why(r"low outer / high inner median; finite corrections included"),
                why(r"centre-free; \ normalization is distribution-specific"), why(r"Rousseeuw \& Croux (1993)")]
        with self.voiceover(
            "<bookmark mark='a'/> Peter Rousseeuw and Christophe Croux proposed two better ones in 1993. Qn is a low "
            "order statistic, roughly the first quartile, of all pairwise distances, scaled by two point two two. "
            "<bookmark mark='b'/> Sn is low outer / high inner median; finite corrections included of pairwise distances. <bookmark mark='c'/> Neither "
            "explicitly estimates a centre. Their Gaussian consistency constants do not make them estimators of "
            "standard deviation for arbitrary skewed laws. <bookmark mark='d'/> Both keep fifty percent breakdown, "
            "and Qn is eighty-two percent efficient at the normal, more than twice the MAD."
        ) as vo:
            intro=label('Pairwise gaps define center-free resistant scales',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("scale")
        hdr = [r"\textbf{scale}", r"\textbf{copper data}", r"\textbf{efficiency, \ $n = 100$}", r"\textbf{breakdown}"]
        spec = (("sd", r"standard deviation"), ("iqr", r"IQR / 1.349"), ("mad", r"MAD"), ("sn", r"$S_n$"), ("qn", r"$Q_n$"))
        body = [[t, f"{d[k]:.3f}", f"{d['eff'][k]:.2f}", f"{100 * d['breakdown'][k]:.0f}\\%"] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A, MEANC, TRIMC, MEDC, BIWC, HLC])
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"efficiency: \ variance of $\log s$ over that of the estimator, \ 3,000 normal samples", font_size=22),
            label(r"$Q_n$: \ efficient selection can be $O(n \log n)$; this teaching implementation stores all pairs", font_size=22, color=HLC),
        ), 12.0, 0.22, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The scale estimators side by side, with efficiencies measured on three thousand "
            "normal samples of a hundred. The standard deviation: five point three on the copper data, full "
            "efficiency, zero breakdown. The interquartile range and MAD: about point six, thirty-seven percent "
            "efficient. Sn: about fifty-eight percent. <bookmark mark='b'/> Qn: seventy-seven percent at this sample "
            "size, eighty-two in the limit, and fifty percent breakdown, computable fast."
        ) as vo:
            self.add(chem_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:5]], lag_ratio=0.3), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(tb[5]), FadeIn(foot[1]))
        self.clear_scene()

    def why_scale(self):
        rows = fit_rows(VGroup(
            label(r"M-estimates need a scale to judge `far': \ it must be robust too", font_size=24),
            label(r"outlier rules: \ $|x - \mathrm{median}| > 3\, \mathrm{MAD}$, \ not 3 SD", font_size=24, color=MEDC),
            label(r"the SD hides the outliers that inflate it: \ masking", font_size=24, color=RES),
            label(r"next: \ the same problems, \ worse, \ in regression", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Robust scale matters beyond reporting spread. Every M-estimate needs a scale to "
            "decide what counts as far, and that scale must be robust too. <bookmark mark='b'/> Median and MAD can "
            "give useful resistant diagnostic thresholds; a three-MAD rule is not a universal test, especially for "
            "skewed or rounded data, <bookmark mark='c'/> because outliers inflate the standard deviation and so hide"
            " themselves: masking. <bookmark mark='d'/> In regression the same problems return, in a worse form."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mscale(self):
        rows = [
            cmath(r"\tfrac1n \textstyle\sum_i \rho\bigl(\tfrac{r_i}{s}\bigr)", r"=", r"b", font_size=32),
            cmath(r"\rho", r":", r"\text{bounded, \ e.g.\ the biweight's}", font_size=30),
            cmath(r"\min(b/\max\rho,1-b/\max\rho)", r"=", r"\varepsilon^*: \ b = \tfrac12 \text{ gives } 50\%", font_size=30),
            cmath(r"\text{use}", r":", r"\text{the scale inside S- and MM-estimators}", font_size=30),
        ]
        rows[0][2].set_color(HUBC)
        whys = [why(r"an M-estimate of scale"), why(r"so a huge residual counts at most 1"),
                why(r"Huber (1981): \ breakdown set by $b$"), why(r"chapter seven")]
        with self.voiceover(
            "<bookmark mark='a'/> A third kind: an M-estimate of scale, the s that makes the average of rho of the "
            "standardized residuals equal a constant b. <bookmark mark='b'/> With a bounded rho, like the biweight's,"
            " a huge residual counts at most one. <bookmark mark='c'/> For fixed-center scale estimation under the "
            "regular setup, both explosion and implosion matter: the asymptotic breakdown is the smaller of b over "
            "maximum rho and one minus that ratio. Choosing one half balances them. <bookmark mark='d'/> This M-scale"
            " is the engine inside the S- and MM-regression estimators of the next chapter."
        ) as vo:
            intro=label('Bounded loss balances scale explosion and implosion',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def masking1d(self):
        from explainer.stats.kit import robust as RR
        x = museum.newcomb()
        m, s = x.mean(), x.std(ddof=1)
        z = x[x > -40]
        m2, s2 = z.mean(), z.std(ddof=1)
        md, ma = np.median(x), RR.mad(x)
        A = axes([-50, 45], [-0.5, 3.5], x_length=10.4, y_length=3.2, xlabel=r"Newcomb's 66 values", ylabel=r"",
                 xticks=[-40, -20, 0, 20, 40], yticks=[], center=[-0.4, 1.0, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(v, 0.0), radius=0.06, color=RES if v <= 0 else WHITE) for v in x])

        def band(c, w, y, col, txt):
            return VGroup(Line(ax.c2p(max(c - 3 * w, -50), y), ax.c2p(c + 3 * w, y), color=col, stroke_width=5),
                          label(txt, font_size=20, color=col).next_to(ax.c2p(45, y), RIGHT, buff=0.1))

        b1 = band(m, s, 1.0, MEANC, r"mean $\pm$ 3 SD")
        b2 = band(m2, s2, 2.0, MEANC, r"after removing $-44$")
        b3 = band(md, ma, 3.0, MEDC, r"median $\pm$ 3 MAD")
        rows = fit_rows(VGroup(
            label(rf"pass 1: \ mean {m:.1f}, \ SD {s:.1f}: \ $-44$ is {abs((-44 - m) / s):.1f} SD out, \ $-2$ only {abs((-2 - m) / s):.1f}", font_size=22, color=MEANC),
            label(rf"pass 2: \ SD {s2:.1f}: \ now $-2$ is {abs((-2 - m2) / s2):.1f} SD out", font_size=22, color=MEANC),
            label(rf"median and MAD: \ both flagged at once \ ({abs((-44 - md) / ma):.0f} and {abs((-2 - md) / ma):.1f} MADs)", font_size=22, color=MEDC),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Masking happens in one dimension too. Apply the three-standard-deviation rule to Newcomb's "
            "data. The minus forty-four inflates the standard deviation to ten point seven, so it is flagged, at six and a "
            "half SDs, but minus two, at two point six, is not. <bookmark mark='b'/> Remove minus forty-four and recompute: "
            "the standard deviation drops to six point two, and now minus two is four point seven SDs out. One outlier hid "
            "another. <bookmark mark='c'/> With the median and three MADs, both are flagged in a single pass, at sixteen and "
            "six and a half MADs, because the MAD is not inflated by the points it judges."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(b1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(b2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(b3), FadeIn(rows[2]))
        self.clear_scene()
