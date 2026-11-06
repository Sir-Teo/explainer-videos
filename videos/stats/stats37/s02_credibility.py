from __future__ import annotations

from videos.stats.stats37.common import *  # noqa: F403


class Credibility(VoiceoverScene):
    def construct(self):
        self.card()
        self.con()
        self.design()
        self.designs()
        self.local()
        self.nobel()

    def card(self):
        card = chapter_card(1, r"The credibility revolution", r"Design before regression", lit=(1983, 2010), part=PART)
        with self.voiceover("Chapter one. The credibility revolution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def con(self):
        rows = fit_rows(VGroup(
            label(r"Edward Leamer (1983): \ \emph{Let's Take the Con out of Econometrics}", font_size=26, color=TAUC),
            label(r"a regression's answer depended on which controls the analyst chose to include", font_size=26),
            label(r"and the analyst chose after seeing the answers: \ Part 33's garden of forking paths", font_size=26, color=MISSC),
            label(r"few took anyone else's observational regressions seriously", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1983 the econometrician Edward Leamer published a paper called Let's Take the Con out "
            "of Econometrics. <bookmark mark='b'/> His complaint was that the answer an observational regression gave "
            "depended on which control variables the analyst chose to include, and that the reported specification was one "
            "of many tried. <bookmark mark='c'/> The analyst chose after seeing the answers: the garden of forking paths of "
            "Part thirty-three. <bookmark mark='d'/> His proposed cure was to report how the estimate moved across all "
            "reasonable specifications. But his diagnosis stuck: few people took anyone else's observational regressions "
            "seriously."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def design(self):
        rows = [
            cmath(r"\text{model-based}", r":", r"\text{adjust for } X \text{ and hope nothing is left out}", font_size=30),
            cmath(r"\text{design-based}", r":", r"\text{find variation in } T \text{ that is as good as random}", font_size=30),
            cmath(r"\text{then}", r":", r"\text{a simple comparison, \ and checks of the design}", font_size=30),
            cmath(r"\text{the claim}", r":", r"\text{about the design, \ not about a model of } Y", font_size=30),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"Part 36"), why(r"Angrist \& Pischke (2010)"), why(r"placebos, \ balance, \ pre-trends"),
                why(r"Snow argued about the pipes, \ not the bodies")]
        with self.voiceover(
            "<bookmark mark='a'/> The response, which Joshua Angrist and Jörn-Steffen Pischke named the credibility "
            "revolution in 2010, changed the question. The model-based approach of Part thirty-six adjusts for measured "
            "confounders and hopes nothing important is left out. <bookmark mark='b'/> The design-based approach looks first "
            "for variation in the treatment that is as good as random: a lottery, a birthday, a rule, a border. <bookmark "
            "mark='c'/> Then the analysis is a simple comparison, surrounded by checks that the design is what it claims. "
            "<bookmark mark='d'/> The argument moves from a model of the outcome to the design itself. Snow argued about "
            "how the pipes were laid, not about what made people sick."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def designs(self):
        rows = [[r"design", r"the accident", r"the assumption", r"the effect, \ for whom"],
                [r"instrument", r"a lottery or rule nudges $T$", r"exclusion: \ only through $T$", r"compliers (LATE)"],
                [r"discontinuity", r"a cutoff in a score", r"continuity at the cutoff", r"people at the cutoff"],
                [r"diff.-in-diff.", r"a policy starts here, \ not there", r"parallel trends", r"the treated"],
                [r"synthetic control", r"one unit treated", r"a weighted mix tracks it", r"that unit"]]
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.34, colors=[GREY_A, IVC, CUTC, Y0C, BANDC]).move_to([0, 0.5, 0])
        if tab.width > 13:
            tab.width = 13
        with self.voiceover(
            "<bookmark mark='a'/> This part covers four designs. <bookmark mark='b'/> An instrument: something as good as "
            "random, such as a draft lottery, that nudges some people into treatment. It assumes the nudge affects the "
            "outcome only through the treatment, and it identifies the effect for those who were nudged, the compliers of "
            "Part thirty-five. <bookmark mark='c'/> A discontinuity: a rule gives treatment above a cutoff. It assumes "
            "nothing else jumps at the cutoff, and identifies the effect for people near it. <bookmark mark='d'/> "
            "Differences-in-differences: a policy starts in some places and not others. It assumes the places would have "
            "moved in parallel, and identifies the effect on the treated. <bookmark mark='e'/> And the synthetic control: one "
            "treated unit, compared with a weighted mix of others that tracked it before."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def local(self):
        rows = fit_rows(VGroup(
            label(r"each design trades unconfoundedness for a narrower, \ more checkable assumption", font_size=26, color=BANDC),
            label(r"and each identifies a narrower effect: \ for compliers, \ at a cutoff, \ for the treated", font_size=26, color=TAUC),
            label(r"credibility is bought with generality: \ internal against external validity", font_size=26, color=MISSC),
            label(r"Part 35's transport and Part 36's sensitivity analysis still apply", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The trade is always the same. Each design replaces unconfoundedness, which cannot be "
            "checked, with an assumption that is narrower and partly checkable. <bookmark mark='b'/> And each identifies a "
            "narrower effect: for the compliers, for people at the cutoff, for the places that were treated. <bookmark "
            "mark='c'/> Credibility is bought with generality, internal validity with external. Critics such as Angus Deaton "
            "have argued the price is sometimes too high. <bookmark mark='d'/> So the tools of Part thirty-five for "
            "transporting effects, and of Part thirty-six for sensitivity, still matter."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def nobel(self):
        rows = fit_rows(VGroup(
            label(r"2021: \ the Nobel memorial prize in economics", font_size=28, color=TAUC),
            label(r"David Card: \ empirical contributions to labour economics \ (the minimum wage, \ chapter 7)", font_size=26),
            label(r"Joshua Angrist and Guido Imbens: \ the analysis of causal relationships \ (LATE, \ Part 35)", font_size=26),
            label(r"next: \ the oldest design, \ the instrument", font_size=26, color=IVC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2021 the economics Nobel went to the movement. <bookmark mark='b'/> Half to David Card, "
            "for empirical contributions to labour economics, including the minimum-wage study of chapter seven. <bookmark "
            "mark='c'/> Half to Joshua Angrist and Guido Imbens, for methodological contributions to the analysis of causal "
            "relationships, including the local average treatment effect of Part thirty-five. <bookmark mark='d'/> We begin "
            "with the oldest of the designs, the instrument."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
