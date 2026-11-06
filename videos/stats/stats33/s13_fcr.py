from __future__ import annotations

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats33.common import *  # noqa: F403


class FCR(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.definition()
        self.whyRm()
        self.sim()
        self.board()
        self.beyond()

    def card(self):
        card = chapter_card(12, r"The false coverage rate", r"Intervals for the effects you selected", lit=(2005,), part=PART)
        with self.voiceover("Chapter twelve. The false coverage rate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\text{select}", r":", r"\text{the genes BH calls discoveries}", font_size=32),
            cmath(r"\text{then}", r":", r"\text{report a } 90\% \text{ interval for each selected effect}", font_size=30),
            cmath(r"\text{each interval}", r":", r"\text{correct for a gene chosen in advance}", font_size=30),
            cmath(r"\text{selected}", r"\Rightarrow", r"\text{biased away from 0: \ coverage falls}", font_size=30),
        ]
        rows[3][-1].set_color(FALSEC)
        whys = [why(r"$R$ of $m$"), why(r"what readers want"), why(r"marginally"), why(r"the winner's curse once more")]
        with self.voiceover(
            "<bookmark mark='a'/> After the discoveries come the estimates. Select the genes BH calls discoveries, "
            "<bookmark mark='b'/> and report a ninety percent interval for the effect of each. <bookmark mark='c'/> Each "
            "interval would be right for a gene chosen in advance. <bookmark mark='d'/> But these genes were chosen because "
            "their estimates were large, so they are biased away from zero and the intervals cover less often than "
            "promised."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def definition(self):
        rows = [
            cmath(r"\text{FCR}", r"=", r"E\big(\#\{\text{selected intervals missing their } \theta\} / \max(R, 1)\big)", font_size=28),
            cmath(r"\text{BY (2005)}", r":", r"\text{level } 1 - R\alpha/m \text{ for each selected interval}", font_size=30),
            cmath(r"\text{FCR}", r"\le", r"\alpha \ \ \text{for any selection rule, \ independent estimates}", font_size=30),
            cmath(r"R = m", r":", r"\text{no adjustment; \ } R = 1: \ \text{Bonferroni's } \alpha/m", font_size=30),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"the false coverage rate"), why(r"Benjamini \& Yekutieli"), why(r"the FDR's analogue for intervals"),
                why(r"the adjustment scales with selection")]
        with self.voiceover(
            "<bookmark mark='a'/> Benjamini and Yekutieli defined the false coverage rate in 2005: the expected share of "
            "the reported intervals that miss their parameter. <bookmark mark='b'/> Their remedy is to widen each selected "
            "interval, building it at level one minus R alpha over m, where R is the number selected. "
            "<bookmark mark='c'/> That controls the false coverage rate at alpha for any selection rule, with independent "
            "estimates. <bookmark mark='d'/> If everything is selected, no adjustment; if one thing is, Bonferroni's."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sim(self):
        d = load("fcr")
        hdr = [r"\textbf{1,000 effects, \ 100 real}", r"\textbf{$z$ multiplier}", r"\textbf{coverage of selected}"]
        body = [[r"unadjusted 90\% intervals", f"{d['z_unadj']:.2f}", f"{100 * d['unadj']:.1f}\\%"],
                [r"FCR-adjusted \ (BY 2005)", f"{d['z_adj']:.2f}", f"{100 * d['adj']:.1f}\\%"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.35, colors=[GREY_A, FALSEC, BHC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(rf"BH at $q = 0.1$ selects about {d['R_mean']:.0f} effects per study", font_size=22),
            label(r"adjusted intervals are 75\% wider, \ and keep their promise", font_size=22, color=BHC),
        ), 12.0, 0.22, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulation: a thousand effects, a hundred of them real, one estimate each. BH at ten "
            "percent selects about forty-one per study. <bookmark mark='b'/> Unadjusted ninety percent intervals for the "
            "selected effects cover only seventy-nine percent of the time. <bookmark mark='c'/> The FCR-adjusted intervals "
            "use a multiplier of two point eight eight instead of one point six four, three quarters wider, and cover "
            "ninety-one percent."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]))
            vo.wait_until("c")
            self.play(FadeIn(tb[2]), FadeIn(foot[1]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=33) if r.part == 33][4:]
        b = coverage_board(rows, lit_part=33, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board: unadjusted intervals for selected effects, broken; <bookmark mark='b'/> "
            "FCR-adjusted intervals, kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"FCR intervals are wide, \ and centred on the biased estimates", font_size=26),
            label(r"shrinkage helps: \ Tweedie's formula corrects selection bias \ (Efron 2011; \ Part 25)", font_size=26, color=BHC),
            label(r"conditional intervals given selection: \ Fithian, \ Sun \& Taylor (2014)", font_size=26, color=SIGC),
            label(r"inference after selection, \ in full: \ Part 56", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> FCR intervals are honest but wide, and still centred on the biased estimates. "
            "<bookmark mark='b'/> Empirical Bayes shrinkage, through Tweedie's formula from Part 25, corrects the "
            "selection bias of the estimates themselves, as Efron showed in 2011. <bookmark mark='c'/> And intervals that "
            "condition on the selection event, from William Fithian, Dennis Sun and Jonathan Taylor, are exact for the "
            "selected model. <bookmark mark='d'/> Part 56 develops inference after selection in full."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def whyRm(self):
        rows = [
            cmath(r"\text{selected}", r":", r"R \text{ intervals, \ each at level } 1 - R\alpha/m", font_size=30),
            cmath(r"E\big[\tfrac{V_{\text{CI}}}{R}\big]", r"\le", r"\textstyle\sum_i \sum_k \tfrac1k P(i \text{ selected}, R = k, \ \theta_i \notin I_i)", font_size=26),
            cmath(r"", r"\le", r"\textstyle\sum_i \sum_k \tfrac1k \cdot \tfrac{k\alpha}{m} P(R^{(i)} = k)", font_size=28),
            cmath(r"", r"=", r"\alpha \ \ \text{(independent estimates)}", font_size=32),
        ]
        rows[3][-1].set_color(BHC)
        whys = [why(r"the BY construction"), why(r"split by $i$ and $R$"), why(r"the BH proof's trick, \ again"), why(r"each estimate contributes $\alpha/m$")]
        with self.voiceover(
            "<bookmark mark='a'/> Why R alpha over m? The proof follows chapter three's. Split the expected share of "
            "non-covering intervals by parameter and by the number selected. <bookmark mark='b'/> For each parameter, "
            "the chance that it is selected with k selections and its interval misses <bookmark mark='c'/> is at most "
            "the interval's miss rate, k alpha over m, times the chance of k selections computed without it, by the "
            "same independence trick as in the BH proof. <bookmark mark='d'/> The k's cancel and the sum over "
            "parameters gives exactly alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
