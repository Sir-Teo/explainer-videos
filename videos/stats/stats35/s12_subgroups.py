from __future__ import annotations

import numpy as np

from explainer.stats import museum
from videos.stats.stats35.common import *  # noqa: F403

SIGNS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]


class Subgroups(VoiceoverScene):
    def construct(self):
        self.card()
        self.isis()
        self.zodiac()
        self.simulate()
        self.chart()
        self.why_()
        self.rules()

    def card(self):
        card = chapter_card(11, r"Subgroups", r"Gemini, \ Libra, \ and the garden of forking paths", lit=(1988,), part=PART)
        with self.voiceover("Chapter eleven. Subgroups."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def isis(self):
        a, p = museum.ISIS2["aspirin"], museum.ISIS2["placebo"]
        rows = fit_rows(VGroup(
            label(r"ISIS-2 (1988): \ 17,187 patients with a suspected heart attack, \ aspirin vs placebo", font_size=26),
            label(rf"vascular deaths at five weeks: \ {a[0]} of {a[1]:,} \ ({100 * a[0] / a[1]:.1f}\%) \ vs \ {p[0]:,} of {p[1]:,} \ ({100 * p[0] / p[1]:.1f}\%)", font_size=26, color=BANDC),
            label(r"a cheap drug, \ a quarter fewer deaths: \ one of the great trials", font_size=26, color=TAUC),
            label(r"then the reviewers asked for subgroup analyses", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The second International Study of Infarct Survival, ISIS-2, randomized seventeen thousand "
            "one hundred and eighty-seven patients with a suspected heart attack to aspirin or placebo, among other "
            "comparisons. <bookmark mark='b'/> Five weeks later, eight hundred and four of the aspirin patients had died of "
            "vascular causes, nine point four percent, against a thousand and sixteen on placebo, eleven point eight. "
            "<bookmark mark='c'/> A drug costing pennies cut deaths by about a fifth to a quarter: one of the great trials. "
            "<bookmark mark='d'/> When the paper went to The Lancet, the reviewers asked for analyses by subgroup."
        ) as vo:
            self.add(historical_tag(r"ISIS-2 Collaborative Group, \ \emph{Lancet} (1988)"))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def zodiac(self):
        rows = fit_rows(VGroup(
            label(r"the investigators obliged, \ and added one of their own: \ by star sign", font_size=26),
            label(r"Gemini or Libra: \ " + museum.ISIS2["gemini_libra"].replace("%", r"\%"), font_size=26, color=MISSC),
            label(r"all other signs: \ " + museum.ISIS2["other_signs"].replace("%", r"\%").replace("<", r"$<$"), font_size=26, color=BANDC),
            label(r"so: \ no aspirin for Geminis and Librans?", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The investigators, led by Richard Peto and Rory Collins, obliged, and added a subgroup "
            "analysis of their own, to make a point: by the patients' astrological sign. <bookmark mark='b'/> For patients "
            "born under Gemini or Libra, aspirin appeared slightly harmful, with a nine percent increase in deaths, not "
            "significant. <bookmark mark='c'/> For everyone else, a highly significant twenty-eight percent reduction. "
            "<bookmark mark='d'/> Should Geminis and Librans be denied aspirin? Of course not. Then why believe any other "
            "subgroup found the same way?"
        ) as vo:
            self.add(historical_tag(r"ISIS-2 Collaborative Group, \ \emph{Lancet} (1988)"))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def simulate(self):
        d = load("subgroups")
        rows = [
            cmath(r"\text{a trial like ISIS-2}", r":", r"8{,}600 \text{ per arm}, \ 11.8\% \text{ vs } 9.4\%, \ \text{everyone alike}", font_size=28),
            cmath(r"\text{12 random `signs'}", r":", r"\text{about 700 per arm each}", font_size=30),
            cmath(r"P(\text{some sign: \ no benefit})", r"=", rf"{100 * d['p_any_no_benefit']:.0f}\%", font_size=32),
            cmath(r"P(\text{some `significant' interaction})", r"=", rf"{100 * d['p_any_sig_interaction']:.0f}\%", font_size=30),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"one true effect, \ 2.4 points"), why(r"assigned at random"), why(r"2,000 simulated trials"),
                why(r"$|z| > 1.96$ for one of 12")]
        with self.voiceover(
            "<bookmark mark='a'/> Simulate it. A trial the size of ISIS-2, in which aspirin lowers everyone's risk by the "
            "same two point four points. <bookmark mark='b'/> Split the patients into twelve star signs completely at "
            "random, about seven hundred per arm in each. <bookmark mark='c'/> In " + f"{100 * d['p_any_no_benefit']:.0f}"
            + " percent of such trials, at least one sign shows no benefit at all, or harm. <bookmark mark='d'/> And in "
            + f"{100 * d['p_any_sig_interaction']:.0f}" + " percent, at least one sign's effect differs from the overall "
            "effect significantly at five percent: a publishable interaction, made of noise."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("subgroups")
        diff = 100 * np.asarray(d["example_diff"], float)
        A = axes([0, 12], [-2, 6], x_length=8.4, y_length=4.2, xlabel=r"`sign'", ylabel=r"deaths prevented (points)",
                 xticks=[], yticks=[-2, 0, 2.4, 5], yfmt=lambda v: rf"{v:g}", center=[-1.6, 0.3, 0])
        ax = A.ax
        bw = 0.6 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0])
        bars = VGroup()
        for k, v in enumerate(diff):
            h = max(abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), 0.02)
            r = Rectangle(width=bw, height=h, stroke_width=0, fill_color=BANDC if v > 0 else MISSC, fill_opacity=0.8)
            r.move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN if v > 0 else UP)
            bars.add(r)
        zero = Line(ax.c2p(0, 0), ax.c2p(12, 0), color=GREY_B, stroke_width=1.5)
        labs = VGroup(*[label(s, font_size=16, color=GREY_A).next_to(ax.c2p(k + 0.5, -2), DOWN, buff=0.12) for k, s in enumerate(SIGNS)])
        true = DashedLine(ax.c2p(0, 2.4), ax.c2p(12, 2.4), color=TAUC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"one simulated trial", font_size=22),
            label(r"gold: \ the same true effect in every sign", font_size=22, color=TAUC),
            label(r"red: \ `no benefit'", font_size=22, color=MISSC),
        ), 3.6, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is one simulated trial, sign by sign. <bookmark mark='b'/> The true effect, the dashed "
            "line, is identical in all twelve. <bookmark mark='c'/> The estimates scatter from harm to five points of "
            "benefit, and three signs show none at all. Each would make a headline."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(true), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def why_(self):
        rows = [
            cmath(r"\mathrm{se}(\hat\tau_{\rm subgroup})", r"\approx", r"\sqrt{12}\ \mathrm{se}(\hat\tau)", font_size=32),
            cmath(r"\mathrm{se}(\text{difference of two})", r"\approx", r"\sqrt{2}\sqrt{12}\ \mathrm{se}(\hat\tau)", font_size=30),
            cmath(r"\text{power for an interaction}", r":", r"\text{about a sixteenth of the main effect's}", font_size=28),
            cmath(r"\text{many looks}", r":", r"\text{Part 33's multiplicity}", font_size=32),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"a twelfth of the data"), why(r"comparing two subgroups"),
                why(r"Gelman: \ you need 16 times the sample"), why(r"the garden of forking paths")]
        with self.voiceover(
            "<bookmark mark='a'/> The arithmetic: a subgroup with a twelfth of the patients has a standard error about the "
            "square root of twelve times larger. <bookmark mark='b'/> Comparing two subgroups multiplies it by root two "
            "again. <bookmark mark='c'/> As Andrew Gelman likes to say, estimating an interaction half the size of the main "
            "effect takes sixteen times the sample size. Trials are sized for the main effect, so their subgroup analyses "
            "are almost pure noise. <bookmark mark='d'/> And twelve looks is Part 33's multiplicity problem: something will "
            "turn up."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rules(self):
        rows = fit_rows(VGroup(
            label(r"pre-specify a few subgroups, \ with a biological reason, \ before the data", font_size=26, color=BANDC),
            label(r"test the interaction, \ not significance in each subgroup separately", font_size=26, color=BANDC),
            label(r"believe the overall effect unless the evidence is strong \ (Yusuf et al. 1991)", font_size=26, color=GREY_A),
            label(r"real heterogeneity exists: \ Part 62 estimates it with care", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The rules trialists adopted: pre-specify a few subgroups, with a scientific reason, before "
            "seeing the data. <bookmark mark='b'/> Test whether the effect differs between subgroups, rather than whether it "
            "is significant within each one. <bookmark mark='c'/> And, in Salim Yusuf and colleagues' advice of 1991, "
            "believe the overall effect for everyone unless the evidence of a difference is strong. <bookmark mark='d'/> "
            "Real heterogeneity does exist, as the World's drug shows, and Part 62 estimates it with the care it needs."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
