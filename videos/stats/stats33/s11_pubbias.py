from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class PubBias(VoiceoverScene):
    def construct(self):
        self.card()
        self.drawer()
        self.funnel()
        self.egger()
        self.pcurve_def()
        self.pcurve_plot()
        self.selection()

    def card(self):
        card = chapter_card(10, r"Publication bias", r"The literature is a filtered sample", lit=(1997,), part=PART)
        with self.voiceover("Chapter ten. Publication bias."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def drawer(self):
        rows = fit_rows(VGroup(
            label(r"Rosenthal (1979): \ the file-drawer problem", font_size=26),
            label(r"significant results are published; \ null results stay in the drawer", font_size=26, color=FALSEC),
            label(r"a meta-analysis of the published record then measures the filter, \ not the effect", font_size=26, color=SIGC),
            label(r"Part 25's meta-analysis, \ fed a biased sample", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Robert Rosenthal named it in 1979: the file-drawer problem. <bookmark mark='b'/> Studies "
            "with significant results are published; studies without them stay in the file drawer. <bookmark mark='c'/> A "
            "meta-analysis of the published record then partly measures the filter rather than the effect. "
            "<bookmark mark='d'/> Part 25's careful pooling, fed a biased sample."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def funnel(self):
        d = load("pub")
        est, se, pub = np.asarray(d["est"]), np.asarray(d["se"]), np.asarray(d["pub"], bool)
        A = axes([-0.8, 1.6], [0, 0.48], x_length=7.4, y_length=4.6, xlabel=r"estimated effect",
                 ylabel=r"standard error \ (precise studies at the top)", xticks=[-0.5, 0, 0.5, 1, 1.5],
                 yticks=[0.08, 0.28, 0.48], yfmt=lambda v: f"{0.48 - v:.1f}", center=[-2.0, 0.2, 0])
        ax = A.ax

        def P(e, s):
            return ax.c2p(e, 0.48 - s)

        unp = VGroup(*[Dot(P(e, s), radius=0.035, color=GREY_D) for e, s, b in zip(est, se, pub) if not b])
        pb = VGroup(*[Dot(P(e, s), radius=0.045, color=SIGC) for e, s, b in zip(est, se, pub) if b])
        tline = DashedLine(P(0.2, 0.0), P(0.2, 0.47), color=TRUEC, stroke_width=2.5)
        ss = np.linspace(0.01, 0.46, 50)
        fun = VGroup(polyline(ax, 0.2 + 1.96 * ss, 0.48 - ss, GREY_B, 1.5), polyline(ax, 0.2 - 1.96 * ss, 0.48 - ss, GREY_B, 1.5))
        sig = polyline(ax, 1.96 * ss, 0.48 - ss, FALSEC, 2)
        rows = fit_rows(VGroup(
            label(rf"{d['k']} studies of a true effect 0.2 \ (green)", font_size=22, color=TRUEC),
            label(r"every positive significant study; \ 10\% of all others", font_size=22),
            label(rf"gold: \ the {d['n_pub']} published", font_size=22, color=SIGC),
            label(r"red: \ where $p = 0.05$; \ positive-significance boundary", font_size=22, color=FALSEC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulated literature: eight hundred studies of an effect whose true size is point"
            " two, with sample sizes from ten to two hundred per group, so standard errors from point one to point "
            "four five. The funnel plot shows each study's estimate against its standard error, precise studies at "
            "the top. <bookmark mark='b'/> Every study significant in the positive direction is published, along with"
            " one in ten of all others. <bookmark mark='c'/> The two hundred and seventy-eight published studies, in "
            "gold. <bookmark mark='d'/> The red line marks p equal to point oh five: small, imprecise studies are "
            "preferentially published to its right, with large estimates; ten percent of the other studies are still "
            "published. The funnel is hollowed out on the left at the bottom."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(fun), Create(tline))
            vo.wait_until("a")
            self.play(FadeIn(unp), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeOut(unp), FadeIn(pb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(sig), FadeIn(rows[3]))
        self.clear_scene()

    def egger(self):
        d = load("pub")
        ea, ep = d["egger_all"], d["egger_pub"]
        hdr = [r"\textbf{true effect 0.2}", r"\textbf{all 800}", r"\textbf{the 278 published}"]
        body = [[r"inverse-variance pooled estimate", f"{d['fe_all']:.3f}", f"{d['fe_pub']:.3f}"],
                [r"Egger intercept \ ($p$)", rf"{ea['intercept']:.2f} \ ({ea['p']:.2f})", rf"{ep['intercept']:.2f} \ ($10^{{-5}}$)"],
                [r"PET: \ slope, \ the effect at SE $= 0$", f"{ea['slope']:.3f}", f"{ep['slope']:.3f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.32, colors=[GREY_A, None, FALSEC, BHC])
        tb.move_to([0, 1.0, 0])
        rows = [
            cmath(r"\hat\theta_i / s_i", r"=", r"b_0 + b_1 (1/s_i) + e_i", font_size=30),
        ]
        rows[0].move_to([0, -1.3, 0])
        foot = fit_rows(VGroup(
            label(r"Egger et al. (1997): \ common effect, no selection: $b_0=0$; asymmetry has other causes; \ PET (Stanley \& Doucouliagos): \ $b_1$ estimates the effect", font_size=22),
            label(r"the published record overstates the effect by half; \ PET recovers most of the truth", font_size=22, color=BHC),
        ), 12.0, 0.2, [0, -2.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The consequences. Pooling all eight hundred studies recovers point one nine four, "
            "close to the truth. Pooling only the published ones gives point three oh one, half as large again. "
            "<bookmark mark='b'/> Matthias Egger's regression test of 1997 detects the asymmetry: regress each "
            "study's z statistic on its precision; in this common-effect simulation without selection the intercept "
            "is zero. Heterogeneity and other small-study effects can also cause asymmetry. For the published studies"
            " it is one, with a p-value of ten to the minus five. <bookmark mark='c'/> And the slope of that "
            "regression, the PET estimate, extrapolates to a perfectly precise study: point one seven six, closer to "
            "the truth here. This extrapolation depends on the regression model and does not generally remove "
            "publication bias."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]))
            vo.wait_until("b")
            self.play(FadeIn(tb[2]), FadeIn(rows[0]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tb[3]), FadeIn(foot[1]))
        self.clear_scene()

    def pcurve_def(self):
        rows = [
            cmath(r"\text{look only at}", r":", r"\text{significant results, \ } p < 0.05", font_size=30),
            cmath(r"\text{no effect}", r":", r"p \text{ uniform on } (0, 0.05): \ \text{flat}", font_size=30),
            cmath(r"\text{real effect}", r":", r"\text{more very small } p\text{'s: \ right-skewed}", font_size=30),
            cmath(r"p\text{-hacking}", r":", r"\text{may create excess near }0.05;\ \text{not diagnostic alone}", font_size=30),
        ]
        rows[2][-1].set_color(SIGC)
        whys = [why(r"Simonsohn, \ Nelson \& Simmons (2014)"), why(r"chapter one's histogram, \ zoomed"),
                why(r"the evidential value"), why(r"forking paths stop at the first success")]
        with self.voiceover(
            "<bookmark mark='a'/> A different diagnostic uses only the significant results, which is all the "
            "published record may contain: the p-curve of Simonsohn, Nelson and Simmons. <bookmark mark='b'/> If "
            "there is no effect, significant p-values are uniform between zero and point oh five: the curve is flat. "
            "<bookmark mark='c'/> If the effect is real, very small p-values are more common: the curve is skewed to "
            "the right. <bookmark mark='d'/> Some forms of p-hacking can produce excess mass near the threshold; "
            "neither a bump nor right skew uniquely identifies the mechanism."
        ) as vo:
            intro=label('A significant-result histogram is conditional on passing a threshold',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pcurve_plot(self):
        d = load("pcurve")
        cs = d["curves"]
        A = axes([0, 0.05], [0, 0.8], x_length=7.4, y_length=4.4, xlabel=r"significant $p$-value", ylabel=r"share in each bin",
                 xticks=[0.01, 0.02, 0.03, 0.04, 0.05], yticks=[0, 0.2, 0.4, 0.6], center=[-2.0, 0.3, 0])
        ax = A.ax
        cols = {"0.0": NULLC, "0.3": BHC, "0.7": SIGC}
        lines = {}
        for k, c in cols.items():
            pr = np.asarray(cs[k]["probs"])
            xs = np.array([0.005, 0.015, 0.025, 0.035, 0.045])
            lines[k] = VGroup(polyline(ax, xs, pr, c, 3), *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(xs, pr)])
        rows = fit_rows(VGroup(
            label(r"two-sided $z$-tests, known variance; 30 per group", font_size=22),
            label(r"grey: \ no effect: \ 20\% in every bin", font_size=22, color=NULLC),
            label(rf"blue: \ $d = 0.3$, \ power {100 * cs['0.3']['power']:.0f}\%: \ {100 * cs['0.3']['probs'][0]:.0f}\% below 0.01", font_size=22, color=BHC),
            label(rf"gold: \ $d = 0.7$, \ power {100 * cs['0.7']['power']:.0f}\%: \ {100 * cs['0.7']['probs'][0]:.0f}\% below 0.01", font_size=22, color=SIGC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Exact p-curves under two-sided z-tests with known variance and thirty subjects per "
            "group. <bookmark mark='b'/> No effect: twenty percent of significant p-values in each bin of width point"
            " oh one. <bookmark mark='c'/> A modest effect, with only twenty-one percent power: already thirty-seven "
            "percent of significant results fall below point oh one. <bookmark mark='d'/> A large effect: seventy-two"
            " percent. A literature whose significant p-values pile up near point oh five, rather than near zero, "
            "deserves suspicion."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines["0.0"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lines["0.3"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(lines["0.7"]), FadeIn(rows[3]))
        self.clear_scene()

    def selection(self):
        rows = fit_rows(VGroup(
            label(r"selection models: \ model the filter, \ $P(\text{published} \mid p)$, \ and correct for it", font_size=26, color=BHC),
            label(r"Hedges (1984); \ Vevea \& Hedges (1995); \ Andrews \& Kasy (2019)", font_size=26),
            label(r"trim-and-fill \ (Duval \& Tweedie 2000): \ impute the missing studies", font_size=26, color=GREY_A),
            label(r"none fully repairs a filtered record: \ register the studies instead", font_size=26, color=FALSEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The most principled corrections model the filter directly: the probability that a study is "
            "published, as a function of its p-value, estimated jointly with the effect. <bookmark mark='b'/> Larry Hedges "
            "proposed this in 1984; Isaiah Andrews and Maximilian Kasy recently showed how to identify the filter from "
            "replications. <bookmark mark='c'/> Trim-and-fill imputes the missing studies to make the funnel symmetric. "
            "<bookmark mark='d'/> None of these fully repairs a filtered record. The real cure is to make the record "
            "complete: register every study before it is run."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
