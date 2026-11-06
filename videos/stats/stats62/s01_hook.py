from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403

# HIV-CAUSAL Collaboration (Cain et al., Ann. Intern. Med. 2011): hazard ratios against starting at CD4 < 500
HRS = [("start at 350: \\ death", 1.01, 0.84, 1.22), ("start at 200: \\ death", 1.20, 0.97, 1.48),
       ("start at 350: \\ AIDS or death", 1.38, 1.23, 1.56), ("start at 200: \\ AIDS or death", 1.90, 1.67, 2.15)]


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.forest()
        self.clone()
        self.start_trial()
        self.lesson()
        self.taxonomy()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(2011,)).to_edge(UP, buff=0.35)
        hc = history_card(2011, r"The HIV-CAUSAL Collaboration (L. Cain et al.), \ \emph{Annals of Internal Medicine}",
                          r"20{,}971 people with HIV in Europe and the US, \ never treated: \ when should combined "
                          r"antiretroviral therapy start, \ as soon as the CD4 count falls below 500, \ below 350, \ or "
                          r"below 200? \ No trial had compared them", color=TRTC, width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"the question is a rule, \ not a treatment: \ a dynamic regime", font_size=26, color=GREY_A),
            label(r"the data are observational, \ and treatment depends on a changing CD4 count", font_size=26, color=HIDC),
            label(r"the answer needed every tool of this part's predecessors, \ and some new ones", font_size=26, color=IDC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2011 the HIV-CAUSAL Collaboration, led in this analysis by Lauren Cain, asked a "
            "question no trial had answered: when should people with HIV start combined antiretroviral therapy? As soon "
            "as their CD4 count falls below 500, below 350, or below 200? They had records of 20,971 untreated people in "
            "Europe and the United States. <bookmark mark='b'/> The question is about a rule, not a treatment: a dynamic "
            "regime, whose action depends on a measurement that changes over time. <bookmark mark='c'/> The data are "
            "observational, and doctors start treatment because the CD4 count falls, which itself predicts death. "
            "<bookmark mark='d'/> Answering it needed Part thirty-six's tools and more."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def forest(self):
        A = axes([np.log10(0.7), np.log10(2.5)], [0, 4.6], x_length=7.0, y_length=4.2, xlabel=r"hazard ratio against starting at 500 (log scale)",
                 ylabel=r"", xticks=[np.log10(v) for v in (0.8, 1, 1.5, 2)], xfmt=lambda v: f"{10 ** v:g}", center=[1.2, 0.0, 0])
        ax = A.ax
        one = DashedLine(ax.c2p(0, 0), ax.c2p(0, 4.6), color=GREY_B, stroke_width=2)
        rows = VGroup()
        for k, (name, hr, lo, hi) in enumerate(HRS):
            yy = 4 - k
            c = NAIVEC if lo > 1 else GREY_A
            seg = Line(ax.c2p(np.log10(lo), yy), ax.c2p(np.log10(hi), yy), color=c, stroke_width=4)
            dot = Dot(ax.c2p(np.log10(hr), yy), radius=0.09, color=c)
            lab = label(rf"{name}", font_size=22, color=c).next_to(ax.c2p(np.log10(0.7), yy), LEFT, buff=0.3)
            val = label(rf"{hr:.2f} \ ({lo:.2f}--{hi:.2f})", font_size=20, color=c).next_to(ax.c2p(np.log10(hi), yy), RIGHT, buff=0.15)
            rows.add(VGroup(seg, dot, lab, val))
        side = label(r"waiting is not worse for death alone, \ but is for AIDS or death", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "<bookmark mark='a'/> Their estimates, as hazard ratios against starting at 500, with ninety-five percent "
            "intervals. <bookmark mark='b'/> For death alone, waiting until 350 gave a ratio of 1.01, and waiting until 200 "
            "gave 1.20, with an interval that just includes one. <bookmark mark='c'/> For AIDS or death, waiting was "
            "clearly worse: 1.38 for 350, and 1.90 for 200. <bookmark mark='d'/> Starting earlier looked better. But it "
            "was an observational analysis, and the authors themselves said a randomized trial should settle it."
        ) as vo:
            self.play(FadeIn(A), Create(one), FadeIn(museum_tag(r"HIV-CAUSAL Collaboration (2011)")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def start_trial(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The trial came. INSIGHT START randomized 4,685 people whose CD4 counts were above 500 to "
            "start at once or to wait until 350. <bookmark mark='b'/> It was stopped early, in 2015: immediate treatment cut "
            "serious AIDS-related and non-AIDS events, a hazard ratio of 0.43. <bookmark mark='c'/> The observational "
            "emulation had pointed the same way, years earlier, for a rule that no trial could have tested first. "
            "<bookmark mark='d'/> The lesson of this part: when the textbook assumptions fail, there is still a lot that "
            "can be identified and estimated, if one is precise about what is assumed.",
            [(r"\text{START}", r":", r"4{,}685 \text{ with CD4} > 500, \ \text{immediate vs deferred}", 38),
             (r"\text{result}", r":", r"\mathrm{HR} = 0.43, \ \text{stopped early (2015)}", 40),
             (r"\text{the emulation}", r":", r"\text{pointed the same way, \ earlier}", 40),
             (r"\text{lesson}", r":", r"\text{precise assumptions, \ honest answers}", 40)],
            [r"\emph{NEJM} 373 (2015)", r"AIDS-related HR 0.28", r"target-trial emulation", r"this part"],
            colors=[(1, IDC)])

    def lesson(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Parts thirty-five to thirty-seven assumed one of three things: randomization, no "
            "unmeasured confounding, or a natural experiment. <bookmark mark='b'/> This part asks what remains when those "
            "fail. <bookmark mark='c'/> Some effects are identified from a graph in surprising ways; some can only be "
            "bounded; some need proxies for what is hidden. <bookmark mark='d'/> And the questions themselves grow: effects "
            "that spill between people, rules instead of treatments, graphs learned from data, and results carried from one "
            "population to another.",
            [(r"\text{so far}", r":", r"\text{randomized, \ unconfounded, \ or a natural experiment}", 38),
             (r"\text{when they fail}", r":", r"\text{identify, \ bound, \ or use proxies}", 40),
             (r"\text{new questions}", r":", r"\text{interference, \ regimes, \ discovery, \ transport}", 40),
             (r"\text{throughout}", r":", r"\text{say exactly what is assumed}", 40)],
            [r"Parts 35--37", r"chapters 1--3", r"chapters 4--9", r"the discipline"],
            colors=[(1, IDC)])

    def taxonomy(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The plan. <bookmark mark='b'/> Chapters one to three: identification theory, "
            "sensitivity analysis and partial identification, and proximal inference. <bookmark mark='c'/> Chapters four to "
            "six: interference, policy learning, and dynamic treatment regimes. <bookmark mark='d'/> Chapters seven to "
            "nine: causal discovery, data fusion and transportability, and surrogate outcomes.",
            [(r"the plan:", GREY_A),
             (r"1--3: \ identification, \ sensitivity, \ proximal inference", IDC),
             (r"4--6: \ interference, \ policy learning, \ dynamic regimes", TRTC),
             (r"7--9: \ discovery, \ transportability, \ surrogates", HIDC)])

    def upgrade(self):
        cards = [
            upgrade_card(36, r"no unmeasured confounding, \ then weighting and double robustness", r"every confounder is measured",
                         r"chapters 2--3: \ bounds without it, \ and proxies for it"),
            upgrade_card(61, r"transport one population's distribution onto another's", r"no causal model of the difference",
                         r"chapter 8: \ when an effect can be transported"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part thirty-six assumed every confounder was measured; chapters two "
            "and three bound the effect without that assumption, and replace it with proxies. <bookmark mark='b'/> Part "
            "sixty-one moved distributions without a causal model; chapter eight says when an effect itself can be carried "
            "to a new population."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 62", font_size=34, color=GREY_B), label(r"Frontiers of Causal Inference", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the front door; \ sensitivity bounds on the NSW job-training data; \ proximal inference",
            r"spillovers on a network; \ learning and evaluating treatment rules; \ Q-learning",
            r"what causal discovery can and cannot do; \ transporting a trial; \ surrogate outcomes",
            r"four Board rows; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 35, \ 36, \ 37, \ 49").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.frontier}, \ the exposure map").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-two: frontiers of causal inference. <bookmark mark='b'/> The front door; "
            "sensitivity bounds on the National Supported Work data; proximal inference; spillovers on a network; learning "
            "and honestly evaluating treatment rules; Q-learning for dynamic regimes; what causal discovery can and cannot "
            "do; transporting a trial to its target population; surrogate outcomes; and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def clone(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> How does one compare rules in observational data? <bookmark mark='b'/> At the moment a "
            "patient's CD4 count first falls below 500, they are compatible with all three rules: start at 500, at 350, or "
            "at 200. So clone them, one copy per rule. <bookmark mark='c'/> Follow each clone, and censor it the moment the "
            "real patient deviates from that clone's rule. <bookmark mark='d'/> Censoring depends on the changing CD4 count, "
            "so weight the uncensored clones by the inverse probability of remaining compatible, Part thirty-six's "
            "marginal structural model weights. The result compares the rules as a trial would.",
            [(r"\text{time zero}", r":", r"\text{CD4 first} < 500", 40),
             (r"\text{clone}", r":", r"\text{one copy per rule}", 40),
             (r"\text{censor}", r":", r"\text{when the patient deviates from the rule}", 40),
             (r"\text{weight}", r":", r"1/P(\text{still compatible} \mid \text{history})", 40)],
            [r"no immortal time", r"compatible with all", r"artificial censoring", r"Part 36's IPW"],
            colors=[(3, IDC)])
