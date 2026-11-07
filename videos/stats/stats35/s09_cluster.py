from __future__ import annotations

from videos.stats.stats35.common import *  # noqa: F403


class Cluster(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_()
        self.schools()
        self.deff()
        self.result()
        self.board()
        self.analysis()

    def card(self):
        card = chapter_card(8, r"Cluster randomization", r"When whole groups are assigned", lit=(1978,), part=PART)
        with self.voiceover("Chapter eight. Cluster randomization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def why_(self):
        rows = fit_rows(VGroup(
            label(r"some treatments can only be given to groups: \ a teaching method, \ a village's water, \ a ward's protocol", font_size=26),
            label(r"or should be, \ to keep the control group uncontaminated", font_size=26, color=GREY_A),
            label(r"so randomize schools, \ villages, \ hospitals: \ clusters", font_size=26, color=TAUC),
            label(r"the unit of randomization is the cluster, \ not the pupil", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Some treatments can only be given to groups: a teaching method to a school, clean water to "
            "a village, a hygiene protocol to a hospital ward. <bookmark mark='b'/> Others could be given to individuals, "
            "but if neighbours share information, randomizing groups keeps the controls uncontaminated. <bookmark mark='c'/> "
            "So we randomize clusters: whole schools, villages or hospitals. <bookmark mark='d'/> The unit of randomization "
            "is then the cluster, and that fact must carry through to the analysis."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def schools(self):
        d = load("cluster")
        rows = fit_rows(VGroup(
            label(rf"the World's {d['k']} schools, \ {d['n']:,} pupils, \ about {d['mean_size']:.0f} per school", font_size=26),
            label(r"a tutoring programme, \ randomized to half the schools", font_size=26, color=Y1C),
            label(rf"its true effect: \ $+{d['effect']:.0f}$ points on every pupil's score", font_size=26, color=TAUC),
            label(rf"schools differ: \ intraclass correlation {d['icc']:.3f}", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World has four hundred schools, from Parts 23 and 25, with about sixty pupils "
            "each. <bookmark mark='b'/> A tutoring programme is randomized to half of them. <bookmark mark='c'/> In "
            "the World's science, it raises every pupil's score by twenty points, a fifth of a standard deviation. "
            "<bookmark mark='d'/> And schools differ: pupils in the same school resemble each other, through shared "
            "school effects and background. The unadjusted model's intraclass correlation includes both sources."
        ) as vo:
            self.add(schools_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def deff(self):
        d = load("cluster")
        rows = [
            cmath(r"\mathrm{Var}(\bar Y_{\rm cluster})", r"=", r"\dfrac{\sigma^2}{m}\big(1 + (m - 1)\rho\big)", font_size=32),
            cmath(r"\text{deff}", r"=", r"1 + (m - 1)\rho", font_size=34),
            cmath(r"m \approx 60, \ \rho \approx 0.171", r":", rf"\text{{deff}} \approx {d['deff']:.1f}", font_size=32),
            cmath(r"\text{so}", r":", rf"{d['n']:,} \text{{ pupils}} \approx {d['n'] / d['deff']:,.0f} \text{{ independent ones}}", font_size=30),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"$m$ pupils, \ correlation $\rho$"), why(r"Kish's design effect, \ Part 18"),
                why(r"the World's schools"), why(r"equal-size approximation; \ school sizes vary")]
        with self.voiceover(
            "<bookmark mark='a'/> The mean of m correlated pupils varies more than the mean of m independent ones, by"
            " a factor of one plus m minus one times the intraclass correlation. <bookmark mark='b'/> That factor is "
            "Kish's design effect, from Part 18. <bookmark mark='c'/> Including school and pupil background "
            "variation, the unadjusted intraclass correlation is about point one seven. With about sixty pupils per "
            "school, it is about " + say(d["deff"], 1) + ". <bookmark mark='d'/> So the trial's twenty-four thousand pupils carry information on the scale of only"
            " a few thousand independent ones. This equal-size formula is an approximation for these varying school "
            "sizes. The correlation looks small; its consequence is not."
        ) as vo:
            intro=label('The equal-size design effect depends on the unadjusted ICC',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def result(self):
        d = load("cluster")
        rows = [[r"analysis", r"mean SE", r"90\% coverage"],
                [r"pupils as if independent", rf"{d['se_naive']:.2f}", rf"{100 * d['cover_naive']:.1f}\%"],
                [r"school means, \ 400 units", rf"{d['se_cluster']:.2f}", rf"{100 * d['cover_cluster']:.1f}\%"]]
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.35, colors=[GREY_A, MISSC, BANDC]).move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(r"1,000 re-randomizations of the programme across the same 400 schools", font_size=24, color=GREY_A),
            label(r"the pupil-level standard error is three times too small", font_size=24, color=MISSC),
        ), 12.4, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Re-randomize the programme across the same four hundred schools a thousand times, and "
            "analyse each trial two ways. <bookmark mark='b'/> Treating the pupils as independent, the standard error "
            "averages " + say(d["se_naive"], 2) + " points, and ninety percent intervals cover the true effect only "
            + f"{100 * d['cover_naive']:.0f}" + " percent of the time. <bookmark mark='c'/> Treating each school's mean as one "
            "observation, the standard error is " + say(d["se_cluster"], 2) + ", and the coverage is "
            + say(100 * d["cover_cluster"], 1) + " percent. <bookmark mark='d'/> The pupil-level standard error is about three times too small: roughly "
            "the square root of the design effect. School-level and pupil-level averages are different estimands in "
            "general; the constant treatment effect makes their targets equal here."
        ) as vo:
            self.add(schools_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def board(self):
        rows = board_rows("school-randomized", "school-level")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board: the pupil-level analysis of a school-randomized trial, broken. "
                   "<bookmark mark='b'/> The school-level analysis: kept.",
                   [("a", [0]), ("b", [1])])

    def analysis(self):
        rows = fit_rows(VGroup(
            label(r"Cornfield (1978): \ randomizing by cluster and analysing by individual", font_size=26),
            label(r"`is an exercise in self-deception'", font_size=28, color=MISSC),
            label(r"valid analyses: \ cluster means, \ cluster-robust SEs (Part 23), \ mixed models (Part 25)", font_size=26, color=BANDC),
            label(r"design: \ count clusters, \ not people; \ with few clusters, \ the wild cluster bootstrap", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Jerome Cornfield wrote in 1978 that randomizing by cluster and then analysing as if"
            " individuals had been randomized <bookmark mark='b'/> is an exercise in self-deception. <bookmark "
            "mark='c'/> Valid analyses use the cluster means, or cluster-robust standard errors from Part 23, or the "
            "mixed models of Part 25. <bookmark mark='d'/> And at the design stage, the number that matters is the "
            "number of clusters, not of people; with only a handful of clusters, conventional cluster-robust "
            "approximations can be unreliable. Small-sample corrections, design-based randomization tests or a "
            "suitable wild cluster bootstrap need careful assessment."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
