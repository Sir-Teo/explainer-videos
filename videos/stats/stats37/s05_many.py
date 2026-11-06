from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Many(VoiceoverScene):
    def construct(self):
        self.card()
        self.thirty()
        self.hist()
        self.fake()
        self.board()
        self.mr_graph()
        self.mr_plot()

    def card(self):
        card = chapter_card(4, r"Many instruments; \ Mendelian randomization", r"More instruments, \ more bias",
                            lit=(1995, 2003, 2015), part=PART)
        with self.voiceover("Chapter four. Many instruments, and Mendelian randomization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def thirty(self):
        d = load("many")
        rows = fit_rows(VGroup(
            label(r"Angrist \& Krueger also interacted quarter with year and state of birth: \ up to 180 instruments", font_size=26),
            label(r"in the World: \ quarter $\times$ region, \ 30 instruments \ (only quarter 1 matters)", font_size=26, color=IVC),
            label(rf"full survey: \ 2SLS {d['full30']['beta']:.3f}, \ $F$ = {d['full30']['F']:.1f}; \ LIML {d['full30_liml']['beta']:.3f}", font_size=26, color=TAUC),
            label(r"each extra instrument adds noise to the first stage, \ and the noise is correlated with the confounder", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> To gain precision, Angrist and Krueger also interacted the quarter of birth with year and "
            "state of birth, up to a hundred and eighty instruments. <bookmark mark='b'/> In the World, interact quarter "
            "with region: thirty instruments, of which only the first-quarter effect is real. <bookmark mark='c'/> In the full "
            "survey, two-stage least squares gives " + say(d["full30"]["beta"], 3) + ", with an F statistic of only "
            + say(d["full30"]["F"], 1) + ", because the F is averaged over thirty instruments, most useless. "
            "<bookmark mark='d'/> The problem is that the first stage fits noise as well as signal, and the fitted noise in "
            "schooling is correlated with ability, the confounder, so it drags the estimate towards ordinary least squares."
        ) as vo:
            self.add(survey_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def hist(self):
        d = load("weak")
        e = np.asarray(d["edges"], float)
        h30, hl = np.asarray(d["h30"], float), np.asarray(d["hl"], float)
        A = axes([-0.3, 0.5], [0, 0.25], x_length=8.0, y_length=4.0, xlabel=r"estimate of the return, \ 30 instruments, \ $n = 5{,}000$",
                 ylabel=r"share", xticks=[-0.2, 0, 0.075, 0.2, 0.4], yticks=[0, 0.1, 0.2], xfmt=lambda v: f"{v:g}",
                 yfmt=lambda v: f"{v:g}", center=[-1.6, 0.3, 0])
        ax = A.ax
        b30 = hist_bars(ax, e, h30 / h30.sum(), color=MISSC, opacity=0.55)
        bl = hist_bars(ax, e, hl / hl.sum(), color=BANDC, opacity=0.45)
        truth = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 0.25), color=TRUEC, stroke_width=3)
        ols = DashedLine(ax.c2p(d["med_ols"], 0), ax.c2p(d["med_ols"], 0.25), color=GREY_A, stroke_width=3)
        side = fit_rows(VGroup(
            label(rf"red: \ 2SLS, \ median {d['med30']:.3f}", font_size=22, color=MISSC),
            label(rf"grey line: \ OLS, \ {d['med_ols']:.3f}", font_size=22, color=GREY_A),
            label(rf"green: \ LIML, \ median {d['medl']:.3f}", font_size=22, color=BANDC),
            label(r"gold: \ the truth, \ 0.075", font_size=22, color=TRUEC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Across a thousand surveys of five thousand, with thirty instruments, two-stage least "
            "squares clusters tightly, around " + say(d["med30"], 2) + ". <bookmark mark='b'/> That is almost exactly where "
            "ordinary least squares sits. With many weak instruments the method collapses back into the bias it was meant to "
            "remove, and now it looks precise. <bookmark mark='c'/> Limited-information maximum likelihood, a close relative "
            "from 1949 that is nearly median-unbiased with many instruments, is centred near the truth, with honest width. "
            "<bookmark mark='d'/> The truth is seven and a half percent."
        ) as vo:
            self.add(survey_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(b30), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ols), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(truth), FadeIn(side[3]))
        self.clear_scene()

    def fake(self):
        d = load("many")
        rows = fit_rows(VGroup(
            label(r"Bound, \ Jaeger \& Baker (1995): \ replace the real quarters of birth with random ones", font_size=26, color=TAUC),
            label(r"the instruments are now pure noise: \ they cannot identify anything", font_size=26, color=MISSC),
            label(rf"in the World: \ fake quarters $\times$ region, \ full survey: \ 2SLS {d['fake_full']['beta']:.3f} \ (SE {d['fake_full']['se']:.3f}), \ $F$ = {d['fake_full']['F']:.2f}", font_size=26, color=IVC),
            label(r"2SLS with useless instruments estimates OLS, \ with a respectable standard error", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1995, John Bound, David Jaeger and Regina Baker did something devastating. They replaced "
            "the real quarters of birth with randomly generated ones, and reran the estimation. <bookmark mark='b'/> The new "
            "instruments are pure noise and cannot identify anything. <bookmark mark='c'/> Yet two-stage least squares still "
            "returned an estimate close to the original, with a respectable standard error. In the World, fake quarters "
            "interacted with region give " + say(d["fake_full"]["beta"], 2) + ", with a standard error of "
            + say(d["fake_full"]["se"], 2) + " and an F of " + say(d["fake_full"]["F"], 2) + ". <bookmark mark='d'/> With "
            "useless instruments, two-stage least squares estimates ordinary least squares, and its standard error does not "
            "warn you. The first-stage F does."
        ) as vo:
            self.add(survey_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("weak instruments", "Anderson")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board: two-stage least squares with the thirty weak instruments, in five "
                   "hundred surveys of five thousand. Its ninety percent interval covers the truth "
                   + f"{100 * rows[0].achieved:.0f}" + " percent of the time: broken. <bookmark mark='b'/> The "
                   "Anderson-Rubin set, with the same instruments: kept.",
                   [("a", [0]), ("b", [1])])

    def mr_graph(self):
        G = CausalGraph({"G": (-3.2, 0), "B": (-0.6, 0), "P": (2.0, 0), "U": (0.7, 1.8)},
                        [("G", "B"), ("B", "P"), ("U", "B"), ("U", "P")], center=[-2.0, 0.0, 0], scale=0.95,
                        colors={"G": IVC, "B": Y1C, "P": Y0C, "U": MISSC},
                        labels={"G": r"gene", "B": r"BMI", "P": r"SBP", "U": r"$U$"}, font_size=22)
        side = fit_rows(VGroup(
            label(r"Davey Smith \& Ebrahim (2003): \ genes as instruments", font_size=22, color=TAUC),
            label(r"alleles are assigned at conception: \ Mendel's lottery", font_size=22, color=IVC),
            label(r"each variant gives a ratio: \ its effect on SBP over its effect on BMI", font_size=22),
            label(r"danger: \ pleiotropy, \ a gene acting through other paths", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Epidemiology found its own instruments in the genome. George Davey Smith and Shah Ebrahim "
            "named the idea Mendelian randomization in 2003. <bookmark mark='b'/> The alleles a person inherits are assigned "
            "at conception, by Mendel's lottery, independently of most later confounders. A variant that raises body mass "
            "index is an instrument for its effect on blood pressure. <bookmark mark='c'/> Genome-wide studies report, for "
            "each variant, its association with the exposure and with the outcome; the ratio of the two is a Wald "
            "estimate. <bookmark mark='d'/> The danger is pleiotropy: a gene that affects blood pressure through some other "
            "path breaks the exclusion restriction."
        ) as vo:
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def mr_plot(self):
        d = load("many")["mr"]
        bx, by = np.asarray(d["bx"], float), np.asarray(d["by"], float)
        pl = set(int(i) for i in d["pleio"])
        A = axes([0, 0.12], [0, 0.05], x_length=7.0, y_length=4.2, xlabel=r"variant's effect on BMI (SD)", ylabel=r"effect on SBP (SD)",
                 xticks=[0, 0.05, 0.1], yticks=[0, 0.025, 0.05], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.0, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=MISSC if i in pl else IVC) for i, (x, y) in enumerate(zip(bx, by))])
        ivw = Line(ax.c2p(0, 0), ax.c2p(0.12, 0.12 * d["ivw"]["beta"]), color=TAUC, stroke_width=3)
        eg = Line(ax.c2p(0, d["egger"]["intercept"]), ax.c2p(0.12, d["egger"]["intercept"] + 0.12 * d["egger"]["beta"]),
                  color=BANDC, stroke_width=3)
        truth = DashedLine(ax.c2p(0, 0), ax.c2p(0.12, 0.12 * d["beta"]), color=TRUEC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"40 variants; \ 10 with a direct effect (red)", font_size=22),
            label(rf"IVW (through the origin): \ {d['ivw']['beta']:.3f}", font_size=22, color=TAUC),
            label(rf"MR-Egger slope: \ {d['egger']['beta']:.3f} \ ({d['egger']['se']:.3f})", font_size=22, color=BANDC),
            label(rf"Egger intercept {d['egger']['intercept']:.4f}: \ the pleiotropy", font_size=22, color=BANDC),
            label(rf"the truth: \ {d['beta']:.2f}", font_size=22, color=TRUEC),
        ), 3.8, 0.4, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Forty simulated variants, ten of them with a direct effect on blood pressure, all in the "
            "same direction. <bookmark mark='b'/> The inverse-variance-weighted estimate fits a line through the origin: "
            + say(d["ivw"]["beta"], 2) + ", pulled up by the pleiotropic variants. <bookmark mark='c'/> MR-Egger, proposed by "
            "Jack Bowden, Davey Smith and Stephen Burgess in 2015, allows an intercept, which absorbs pleiotropy that is the "
            "same on average for every variant: slope " + say(d["egger"]["beta"], 2) + ", with a wider interval. <bookmark "
            "mark='d'/> The intercept itself estimates the average direct effect. <bookmark mark='e'/> The truth is point "
            "three. Each fix trades one untestable assumption for another, slightly weaker one."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ivw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(eg), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(truth), FadeIn(side[4]))
        self.clear_scene()
