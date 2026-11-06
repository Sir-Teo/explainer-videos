from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class Smoking(VoiceoverScene):
    def construct(self):
        self.card()
        self.doll()
        self.cohort()
        self.fisher()
        self.cornfield()
        self.hill()
        self.lesson()

    def card(self):
        card = chapter_card(13, r"Smoking and lung cancer", r"The argument that settled it", lit=(1950, 1958, 1959, 1965), part=PART)
        with self.voiceover("Chapter thirteen. Smoking and lung cancer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def doll(self):
        d = load("smoking")
        rows = fit_rows(VGroup(
            label(r"Richard Doll \& Austin Bradford Hill (1950): \ patients in twenty London hospitals", font_size=26),
            label(rf"men with lung cancer: \ {d['cases_smokers']} of {d['cases']} smokers", font_size=26, color=MISSC),
            label(rf"men with other diseases: \ {d['controls_smokers']} of {d['controls']}", font_size=26, color=Y0C),
            label(rf"odds ratio \ $\approx {d['odds_ratio']:.0f}$; \ and the risk rose with the amount smoked", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1950 Richard Doll and Austin Bradford Hill interviewed patients in London hospitals, "
            "comparing those with lung cancer with patients admitted for other diseases. <bookmark mark='b'/> Of six hundred "
            "and forty-nine men with lung cancer, six hundred and forty-seven were smokers. <bookmark mark='c'/> Of six "
            "hundred and forty-nine men with other diseases, six hundred and twenty-two. Almost everyone smoked, but the "
            "difference was decisive: <bookmark mark='d'/> an odds ratio of about fourteen, and the risk climbed steadily "
            "with the amount smoked. Ernst Wynder and Evarts Graham published similar findings in America the same year."
        ) as vo:
            self.add(historical_tag(r"Doll \& Hill, \ \emph{BMJ} (1950)"))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cohort(self):
        rows = fit_rows(VGroup(
            label(r"a case-control study could be biased by who is asked and how they remember", font_size=26, color=GREY_A),
            label(r"so in 1951 Doll and Hill wrote to every doctor in Britain", font_size=26),
            label(r"the British Doctors Study: \ 40,000 doctors, \ followed for fifty years", font_size=26, color=Y0C),
            label(r"lung cancer deaths rose with cigarettes per day; \ stopping cut the risk", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A comparison of hospital patients could be biased by who is admitted, who is asked, and "
            "how they remember their habits; Berkson's warning from chapter three applies. <bookmark mark='b'/> So in 1951 "
            "Doll and Hill wrote to every doctor in Britain, asking about their smoking. <bookmark mark='c'/> About forty "
            "thousand replied, and their deaths were followed for half a century: the British Doctors Study. <bookmark "
            "mark='d'/> Deaths from lung cancer rose with the number of cigarettes smoked, and doctors who stopped had lower "
            "risks than those who continued."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def fisher(self):
        G = CausalGraph({"G": (0, 1.4), "S": (-2.2, -0.6), "C": (2.2, -0.6)}, [("G", "S"), ("G", "C")],
                        center=[-3.0, 0.2, 0], colors={"G": MISSC, "S": Y1C, "C": Y0C},
                        labels={"G": r"genes", "S": r"smoke", "C": r"cancer"})
        side = fit_rows(VGroup(
            label(r"R. A. Fisher (1957, \ 1958): \ correlation is not causation", font_size=22),
            label(r"his constitutional hypothesis: \ a genotype causes both", font_size=22, color=MISSC),
            label(r"evidence: \ identical twins smoke alike more than fraternal ones", font_size=22, color=GREY_A),
            label(r"he was right that it was possible; \ the question was whether it was plausible", font_size=22, color=TAUC),
        ), 5.0, 0.42, [3.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The most famous dissent came from Fisher. Correlation, he wrote in 1957 and 1958, is not "
            "causation; <bookmark mark='b'/> perhaps an inherited constitution makes some people both crave tobacco and "
            "develop cancer. <bookmark mark='c'/> He cited twin studies showing that identical twins are more alike in their "
            "smoking than fraternal twins, so smoking is partly heritable. <bookmark mark='d'/> Fisher was right that such a "
            "confounder was possible; no observational study can rule it out. The question was whether it was plausible, and "
            "that is a question sensitivity analysis can answer. Fisher, it should be said, was also a smoker and a "
            "consultant to the tobacco industry."
        ) as vo:
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def cornfield(self):
        d = load("smoking")
        rows = [
            cmath(r"RR_{\text{smoking}}", r"\approx", r"9 \ \text{for lung cancer deaths}", font_size=32),
            cmath(r"\text{if } U \text{ explains it}", r"\Rightarrow", r"P(U \mid \text{smoker}) / P(U \mid \text{non}) \ge 9", font_size=30),
            cmath(r"\text{heavy smokers}", r":", r"\text{higher risks still: \ more lopsided still}", font_size=30),
            cmath(r"E\text{-value of } 9", r"=", rf"{d['e_value_9']:.1f}", font_size=34),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"from the cohort studies"), why(r"Cornfield et al. (1959)"),
                why(r"no known trait is so lopsided"), why(r"the same argument, \ in modern form")]
        with self.voiceover(
            "<bookmark mark='a'/> Jerome Cornfield and five colleagues answered in 1959. Smokers' risk of dying of lung "
            "cancer was about nine times that of non-smokers. <bookmark mark='b'/> If a hidden factor explained all of it, "
            "they proved, the factor would have to be at least nine times as common among smokers as among non-smokers. "
            "<bookmark mark='c'/> For heavy smokers, whose risks were higher still, it would have to be more lopsided still. "
            "No known inherited trait is distributed so unevenly between smokers and non-smokers. <bookmark mark='d'/> In "
            "modern terms, the E-value of a risk ratio of nine is about " + say(d["e_value_9"], 1) + ". Cornfield's "
            "inequality was the first sensitivity analysis, and it is why the scientific argument was considered settled."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hill(self):
        items = [r"strength", r"consistency", r"specificity", r"temporality", r"biological gradient", r"plausibility",
                 r"coherence", r"experiment", r"analogy"]
        cells = VGroup(*[label(rf"{i + 1}. \ {t}", font_size=26, color=TAUC if t in ("strength", "temporality", "biological gradient", "experiment") else GREY_A)
                         for i, t in enumerate(items)])
        grid = VGroup(VGroup(*cells[:5]).arrange(DOWN, aligned_edge=LEFT, buff=0.35),
                      VGroup(*cells[5:]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.5, 0])
        head = label(r"Austin Bradford Hill (1965): \ nine viewpoints, \ not criteria", font_size=28).to_edge(UP, buff=0.8)
        foot = label(r"`none of my nine viewpoints can bring indisputable evidence for or against the cause-and-effect hypothesis'",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.9)
        if foot.width > 12.6:
            foot.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> In 1965 Bradford Hill listed the considerations that had persuaded him. <bookmark "
            "mark='b'/> Strength of association; consistency across studies; specificity; temporality, the cause preceding "
            "the effect; a biological gradient, more exposure, more disease; plausibility; coherence with other knowledge; "
            "experimental evidence, such as the fall in risk after stopping; and analogy. <bookmark mark='c'/> He called them "
            "viewpoints, not criteria, and wrote that none of them could bring indisputable evidence on its own. Strength is "
            "Cornfield's argument; the gradient and the effect of stopping are the closest an observational study comes to "
            "an experiment."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.4), run_time=6.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"no randomized trial of smoking was ever run, \ or could be", font_size=26),
            label(r"the case was made by triangulation: \ many designs, \ many populations, \ a sensitivity argument", font_size=26, color=TAUC),
            label(r"1964: \ the US Surgeon General's report", font_size=26, color=BANDC),
            label(r"next: \ when the treatment itself changes over time", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> No randomized trial of smoking was ever run, or ever could be. <bookmark mark='b'/> The case "
            "was made by triangulation: case-control and cohort studies in many countries, a dose-response gradient, the "
            "benefit of stopping, and Cornfield's argument that no plausible confounder could explain it. <bookmark "
            "mark='c'/> In 1964 the United States Surgeon General's report concluded that cigarette smoking causes lung "
            "cancer. <bookmark mark='d'/> Next, treatments that are not a single decision but a sequence of them."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
