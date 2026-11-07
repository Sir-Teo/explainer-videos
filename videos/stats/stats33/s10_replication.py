from __future__ import annotations

from explainer.stats.kit.multiple import ppv
from videos.stats.stats33.common import *  # noqa: F403


class Replication(VoiceoverScene):
    def construct(self):
        self.card()
        self.ioannidis()
        self.derive()
        self.table()
        self.power()
        self.osc()
        self.others()
        self.reading()

    def card(self):
        card = chapter_card(9, r"Replication", r"How many published findings are true?", lit=(2005, 2015), part=PART)
        with self.voiceover("Chapter nine. Replication."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ioannidis(self):
        rows = fit_rows(VGroup(
            label(r"2005: \ John Ioannidis, \ `Why most published research findings are false'", font_size=26),
            label(r"a calculation, \ not a measurement", font_size=26, color=GREY_A),
            label(r"an influential analysis of priors, power and bias", font_size=26, color=SIGC),
            label(r"its logic is Bayes's rule \ and this part's multiple comparisons", font_size=26, color=BHC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2005 the physician and epidemiologist John Ioannidis published an essay with a "
            "provocative title: Why Most Published Research Findings Are False. <bookmark mark='b'/> It was a "
            "calculation, not a measurement. <bookmark mark='c'/> It became an influential discussion of how prior "
            "plausibility and power affect positive findings. <bookmark mark='d'/> Its logic is Bayes's rule, Part "
            "15, applied to the stream of hypotheses a field tests."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"R", r"=", r"\text{pre-study odds that a tested effect is real}", font_size=30),
            cmath(r"P(\text{true positive})", r"\propto", r"(1 - \beta) R, \ \ P(\text{false positive}) \propto \alpha", font_size=30),
            cmath(r"\text{PPV}", r"=", r"\dfrac{(1 - \beta) R}{(1 - \beta) R + \alpha}", font_size=34),
            cmath(r"\text{with bias } u", r":", r"\text{a share } u \text{ of initially negative analyses made positive}}", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"the field's prior"), why(r"power $1 - \beta$, \ level $\alpha$"),
                why(r"the positive predictive value"), why(r"forking paths, \ selective reporting")]
        with self.voiceover(
            "<bookmark mark='a'/> Let R be the pre-study odds that an effect a field tests is real. <bookmark mark='b'/> "
            "Real effects come out significant with probability equal to the power, one minus beta; null effects with "
            "probability alpha. <bookmark mark='c'/> So the share of significant findings that are real, the positive "
            "predictive value, is power times R over power times R plus alpha: the same formula as a medical screening "
            "test in Part 3. <bookmark mark='d'/> Ioannidis added bias: a share u of analyses that should have been "
            "negative are turned positive by the forking paths of chapter eight."
        ) as vo:
            intro=label('Prior plausibility and power determine positive predictive value',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        hdr = [r"\textbf{a field}", r"\textbf{prior}", r"\textbf{power}", r"\textbf{bias $u$}", r"\textbf{PPV}"]
        cases = [(r"confirmatory trial", 0.5, 0.8, 0.0), (r"well-powered, \ plausible", 0.25, 0.8, 0.1),
                 (r"exploratory, \ underpowered", 0.1, 0.2, 0.2), (r"discovery genomics, \ uncorrected", 0.01, 0.2, 0.2)]
        def pct(v):
            return f"{100 * v:.1f}\\%" if v < 0.1 else f"{100 * v:.0f}\\%"

        body = [[nm, f"{pr:g}", f"{pw:g}", f"{u:g}", pct(ppv(pr, pw, 0.05, u))] for nm, pr, pw, u in cases]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, TRUEC, BHC, SIGC, FALSEC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"$\alpha = 0.05$; \ prior = the share of tested effects that are real", font_size=22),
            label(r"low priors and low power make most positive findings false, \ before any misconduct", font_size=22, color=FALSEC),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Some cases. A confirmatory trial of a plausible treatment, with even odds, good power and "
            "no bias: ninety-four percent of positive results are true. A well-powered field with a quarter of tested "
            "effects real and some bias: about two thirds. An exploratory, underpowered field: one in seven. "
            "Uncorrected discovery among thousands of candidates: under two percent. <bookmark mark='b'/> Low priors and "
            "low power make most positive findings false, with no misconduct at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.4), FadeIn(foot[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def osc(self):
        hdr = [r"\textbf{Reproducibility Project: \ Psychology (2015)}", r"\textbf{original}", r"\textbf{replication}"]
        body = [[r"studies", "100", "100"], [r"significant at $p < 0.05$", r"97\%", r"36\%"],
                [r"mean effect size $r$", "0.40", "0.20"], [r"original effect inside the replication's 95\% CI", "", r"47\%"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.32, colors=[GREY_A, None, FALSEC, SIGC, None])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"270 authors re-ran 100 studies from three leading psychology journals of 2008", font_size=22),
            label(r"high-powered, \ preregistered replications, \ materials from the original authors", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Then it was measured. The Open Science Collaboration, two hundred and seventy researchers, "
            "re-ran a hundred studies from three leading psychology journals of 2008, with larger samples, preregistered "
            "plans and the original materials. <bookmark mark='b'/> Ninety-seven of the originals had been significant; "
            "thirty-six percent of the replications were. The average effect size halved, from a correlation of point four "
            "to point two. Fewer than half of the original effect sizes fell inside the replication's ninety-five percent "
            "interval."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[2:]], lag_ratio=0.4), run_time=3.0)
        self.clear_scene()

    def others(self):
        rows = fit_rows(VGroup(
            label(r"Camerer et al. (2018): \ 21 social-science experiments in \emph{Nature} and \emph{Science}: \ 13 replicated", font_size=24),
            label(r"replication effect sizes about half the originals", font_size=24, color=FALSEC),
            label(r"Camerer et al. (2016), \ economics: \ 11 of 18", font_size=24),
            label(r"prediction markets of researchers guessed which would replicate, \ well", font_size=24, color=SIGC),
            label(r"cancer biology \ (Errington et al. 2021): \ 50 experiments, \ median effect 85\% smaller", font_size=24, color=FALSEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Other fields followed. Colin Camerer and colleagues replicated twenty-one "
            "social-science experiments published in Nature and Science between 2010 and 2015; thirteen replicated, "
            "<bookmark mark='b'/> with effects about half their original size. <bookmark mark='c'/> In experimental "
            "economics, eleven of eighteen. <bookmark mark='d'/> Strikingly, prediction markets among researchers "
            "forecast which studies would replicate rather well: researchers’ forecasts contained useful predictive "
            "information. <bookmark mark='e'/> In preclinical cancer biology, the median replication effect across "
            "fifty experiments was eighty-five percent smaller."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def reading(self):
        rows = fit_rows(VGroup(
            label(r"a failed replication does not prove the original false", font_size=26),
            label(r"but shrinking effect sizes are what selection predicts: \ the winner's curse", font_size=26, color=FALSEC),
            label(r"significance filters exaggerate: \ `type M' errors \ (Gelman \& Carlin 2014)", font_size=26, color=SIGC),
            label(r"the cure is in design and reporting, \ not just in thresholds", font_size=26, color=BHC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How to read this. A single failed replication does not prove the original false; both are "
            "noisy. <bookmark mark='b'/> But effect sizes that shrink on replication are exactly what selection predicts: "
            "Part 32's winner's curse. <bookmark mark='c'/> Andrew Gelman and John Carlin call it a type M error, an error of "
            "magnitude: when power is low, the significant estimates are the exaggerated ones. <bookmark mark='d'/> The "
            "cures lie in design and reporting, the subject of the next two chapters."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def power(self):
        rows = [
            cmath(r"\text{neuroscience}", r":", r"\text{median power} \approx 21\%", font_size=32),
            cmath(r"\text{power } 20\%", r":", r"\text{Gaussian two-sided example: selected magnitudes often exceed }2\times", font_size=28),
            cmath(r"\text{type S}", r":", r"\text{the wrong sign, \ when power is very low}", font_size=30),
            cmath(r"\text{fix}", r":", r"\text{larger studies, \ planned for the effect you expect}", font_size=30),
        ]
        rows[1][-1].set_color(FALSEC)
        whys = [why(r"Button et al. (2013)"), why(r"type M: \ the exaggeration ratio"), why(r"Gelman \& Carlin (2014)"), why(r"Part 10's power analysis")]
        with self.voiceover(
            "<bookmark mark='a'/> How low is power in practice? Katherine Button and colleagues estimated the median "
            "statistical power of studies in neuroscience meta-analyses at about twenty-one percent. <bookmark "
            "mark='b'/> For a two-sided Gaussian test near twenty percent power, selected absolute estimates can "
            "average more than twice the true effect: a type M error. <bookmark mark='c'/> When power is very low, a "
            "significant estimate can even have the wrong sign, a type S error. <bookmark mark='d'/> A central remedy"
            " is larger, well-designed studies, planned with Part 10's power analysis for the effect one "
            "realistically expects."
        ) as vo:
            intro=label('Low power can exaggerate selected effect estimates',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
