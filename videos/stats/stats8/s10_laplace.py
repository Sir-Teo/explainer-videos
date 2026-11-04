from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class Laplace(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.ratio()
        self.delta()
        self.design()
        self.world()

    def card(self):
        card = chapter_card(9, r"Standard errors for ratios", r"Laplace counts France", lit=(1802,), part=PART)
        with self.voiceover("Chapter nine. Standard errors for ratios, and Laplace's census of France."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        d = load("laplace")["laplace"]
        tl = timeline(lit=(1802,)).to_edge(UP, buff=0.35)
        hc = history_card(1802, r"Pierre-Simon Laplace, \ for Napoleon's government", r"no census of France had been taken; "
                          r"\ but every parish registered its births", color=S.MUSEUM, width=7.4, font_size=24).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"sampled communes in 30 d\'epartements, \ counted on 22 September 1802:", font_size=24),
            MathTex(r"2{,}037{,}615 \text{ people}, \quad 215{,}599 \text{ births in 3 years} = 71{,}866 \text{ a year}", font_size=28,
                    color=S.MUSEUM),
            MathTex(rf"\text{{people per birth}} = \frac{{2{{,}}037{{,}}615}}{{71{{,}}866}} = {d['ratio']:.3f}", font_size=30),
            MathTex(r"\text{France registered about } 1{,}000{,}000 \text{ births a year} \ \Rightarrow\ \hat N \approx 28.35 \text{ million}",
                    font_size=28, color=EXACT),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "In 1802 France had no census, but every parish registered its births. <bookmark mark='a'/> Pierre-Simon "
            "Laplace proposed to count the nation from a sample. <bookmark mark='b'/> In communes spread across thirty "
            "departments, officials counted the people: two million, thirty-seven thousand, six hundred and fifteen. "
            "Those communes had registered two hundred and fifteen thousand, five hundred and ninety-nine births over "
            "three years, about seventy-one thousand eight hundred a year. <bookmark mark='c'/> So there were about "
            "twenty-eight point three five people for every annual birth. <bookmark mark='d'/> France as a whole "
            "registered about a million births a year, so its population was about twenty-eight point three five "
            "million. Laplace went further: he gave a measure of the estimate's uncertainty, more than a century "
            "before sampling became a profession."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[[slice(0, 2), slice(2, 3), slice(3, 4)][k]]))
        self.clear_scene()

    def ratio(self):
        rows = [
            cmath(r"\hat N", r"=", r"B \cdot \frac{\sum_{\text{sample}} \text{people}}{\sum_{\text{sample}} \text{births}}", r"=", r"B\,\frac{\bar y}{\bar x}",
                  font_size=32),
            cmath(r"\text{a ratio of two means}", r":\ ", r"\text{the delta method (Part 6) for } g(a, b) = a/b", font_size=30),
        ]
        rows[0][4].set_color(SIM)
        whys = [why(r"$B$: \ the known national births; \ the ratio estimator"), why(r"its error: \ how both means wobble, \ together")]
        with self.voiceover(
            "In modern terms. <bookmark mark='a'/> The estimate is the known national total of births, times the ratio "
            "of two sample means: people per commune over births per commune. This is the ratio estimator, still used "
            "by every statistics office. <bookmark mark='b'/> Its uncertainty comes from how both means wobble, and "
            "how they wobble together: exactly the job of Part 6's delta method for a function of two means."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.0, x=-1.2, buff=1.1, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
        self.clear_scene()

    def delta(self):
        rows = [
            cmath(r"\frac{\bar y}{\bar x} - R", r"=", r"\frac{\bar y - R\bar x}{\bar x}", r"\approx", r"\frac{1}{\mu_x}\,\overline{(y - Rx)}", font_size=32),
            cmath(r"\mathrm{SE}\Big(\frac{\bar y}{\bar x}\Big)", r"\approx", r"\frac{1}{\bar x}\sqrt{\frac{1}{k}\cdot\frac{\sum_i (y_i - \hat R x_i)^2}{k - 1}}",
                  font_size=32),
            cmath(r"\mathrm{SE}(\hat N)", r"=", r"B \cdot \mathrm{SE}\Big(\frac{\bar y}{\bar x}\Big)", font_size=32),
        ]
        rows[1][2].set_color(EXACT)
        whys = [why(r"linearize: \ the error is an average of residuals $e_i = y_i - R x_i$"),
                why(r"the standard error of that average: \ $k$ sampled communes"), why(r"scale up")]
        foot = label(r"the same formula gives SEs for survey ratios (Part 18) \ and for odds ratios (Part 14)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Write the error of the ratio as an average of residuals: each commune's people minus "
            "the ratio times its births, divided by the average births. To first order, that's all there is. "
            "<bookmark mark='b'/> So the ratio's standard error is the standard error of an average of residuals, over "
            "the mean number of births. Communes whose population is far from the ratio's prediction add uncertainty; "
            "communes that fit the ratio well add almost none. <bookmark mark='c'/> Multiply by the national births, "
            "and you have the standard error of France's population. <bookmark mark='d'/> Survey statisticians use "
            "this every day."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def world(self):
        d = load("laplace")["world"]
        pop, bir = np.asarray(d["pop"]), np.asarray(d["bir"])
        A = axes([0.5, 3.7], [2.5, 5.6], x_length=4.6, y_length=4.4, xlabel=r"births in the year (log)", ylabel=r"people (log)",
                 xticks=[1, 2, 3], yticks=[3, 4, 5], xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}",
                 center=[-4.4, -0.3, 0])
        ax = A.ax
        ok = bir > 0
        pts = VGroup(*[Dot(ax.c2p(np.log10(b), np.log10(p)), radius=0.04, color=S.WORLD) for b, p in zip(bir[ok], pop[ok])])
        rl = Line(ax.c2p(0.6, 0.6 + np.log10(d["ratio_true"])), ax.c2p(3.6, 3.6 + np.log10(d["ratio_true"])), color=EXACT, stroke_width=2.5)
        ests = np.asarray(d["ests"]) / 1e3
        B = axes([880, 1120], [0, 0.018], x_length=4.6, y_length=3.4, xlabel=r"$\hat N$ (thousands), \ 30 towns", xticks=[900, 1000, 1100],
                 center=[1.0, -0.6, 0])
        ed = np.linspace(880, 1120, 41)
        h = hist_bars(B.ax, ed, np.histogram(ests, ed, density=True)[0], color=SIM, opacity=0.7)
        tr = DashedLine(B.ax.c2p(d["N"] / 1e3, 0), B.ax.c2p(d["N"] / 1e3, 0.018), color=EXACT, stroke_width=2)
        rows = fit_rows(VGroup(
            MathTex(rf"N = {d['N']:,.0f}".replace(",", "{,}"), font_size=26, color=EXACT),
            MathTex(rf"\text{{SD of }} \hat N:\ {d['sd_est']:,.0f}".replace(",", "{,}"), font_size=26, color=SIM),
            MathTex(rf"\text{{average delta SE}}:\ {d['mean_se']:,.0f}".replace(",", "{,}"), font_size=26, color=S.POST),
            MathTex(rf"\hat N \pm 1.96\,\mathrm{{SE}} \text{{ covers }} {100 * d['cover']:.1f}\%", font_size=26, color=S.RESID),
            label(r"30 towns from a Zipf island: \ a skewed ratio, \ so first order is not quite enough", font_size=20, color=GREY_A),
        ), 3.6, 0.28, [5.2, -0.2, 0])
        tag = simulated_tag(r"simulated: 10,000 samples of 30 of the World's 200 towns")
        with self.voiceover(
            "We can't rerun Laplace's survey, but we can run his method on the World. <bookmark mark='a'/> Each of its "
            "two hundred towns has a population and a number of babies born in the past year; people per birth is "
            "about sixty-seven, and it varies from town to town. <bookmark mark='b'/> Sample thirty towns, form the "
            "ratio, scale up by the island's births, ten thousand times. The estimates centre on the true million, "
            "with a standard deviation of about twenty-four thousand. <bookmark mark='c'/> The delta-method standard "
            "error averages twenty-three thousand: close, but a little small, and an interval of plus or minus one "
            "point nine six standard errors covers the truth ninety-one and a half percent of the time, not "
            "ninety-five. With only thirty towns of very different sizes, the ratio's distribution is still skewed. "
            "First-order approximations need checking, which is exactly what the Coverage Board is for."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.01), Create(rl))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(h), Create(tr), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def design(self):
        rows = fit_rows(VGroup(
            label(r"Laplace chose his communes deliberately, \ for good registers and a spread of climates", font_size=24),
            label(r"his error formula treated the sample as if drawn at random from a ``super-population''", font_size=24,
                  color=GREY_A),
            label(r"the theory of random sampling from a finite list: \ Bowley (1906), \ Neyman (1934)", font_size=24),
            label(r"Neyman showed that \emph{purposive} selection can fail badly, \ and randomization guarantees the SE", font_size=24,
                  color=RESID),
            label(r"chapter 10, \ and Part 18", font_size=24, color=S.ACCENT),
        ), 12.6, 0.36, [0, 0.2, 0])
        with self.voiceover(
            "There's a subtlety in Laplace's survey that took another century to resolve. <bookmark mark='a'/> He didn't "
            "pick his communes at random: he chose them for reliable registers and a spread of regions. "
            "<bookmark mark='b'/> His error calculation imagined them as a random draw from a larger hypothetical "
            "population. <bookmark mark='c'/> The theory of random sampling from an actual finite list came with Arthur "
            "Bowley in 1906 and Jerzy Neyman in 1934. <bookmark mark='d'/> Neyman showed that hand-picked samples can "
            "fail badly, and that random selection is what makes a standard error trustworthy. "
            "<bookmark mark='e'/> The next chapter and Part 18 take this up."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
