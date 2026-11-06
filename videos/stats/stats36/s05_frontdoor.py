from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class Frontdoor(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.formula()
        self.numbers()
        self.docalc()
        self.swig()

    def card(self):
        card = chapter_card(4, r"The front door and do-calculus", r"Identification beyond adjustment", lit=(1995,), part=PART)
        with self.voiceover("Chapter four. The front door, and the do-calculus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_(self):
        G = CausalGraph({"U": (0, 1.6), "T": (-2.4, -0.6), "M": (0, -0.6), "Y": (2.4, -0.6)},
                        [("U", "T"), ("U", "Y"), ("T", "M"), ("M", "Y")], center=[-2.6, 0.2, 0],
                        colors={"T": Y1C, "Y": Y0C, "M": TAUC, "U": MISSC},
                        labels={"U": r"$U$", "T": r"$T$", "M": r"$M$", "Y": r"$Y$"})
        side = fit_rows(VGroup(
            label(r"Fisher's objection, \ as a graph:", font_size=22),
            label(r"$U$: \ a genotype causing both smoking and cancer", font_size=22, color=MISSC),
            label(r"$T$: \ smoking; \ $M$: \ tar in the lungs; \ $Y$: \ cancer", font_size=22),
            label(r"no back-door adjustment: \ $U$ is unmeasured", font_size=22, color=MISSC),
            label(r"but smoking acts only through tar, \ and tar has no other cause from $U$", font_size=22, color=TAUC),
        ), 5.0, 0.4, [3.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Sometimes no adjustment set exists, and the effect is still identified. Pearl's example is "
            "Fisher's objection to the smoking evidence, drawn as a graph. <bookmark mark='b'/> Suppose a genotype U causes "
            "both a craving for tobacco and cancer. <bookmark mark='c'/> Smoking T deposits tar M in the lungs, which causes "
            "cancer Y. <bookmark mark='d'/> U is unmeasured, so the back door from smoking to cancer through it cannot be "
            "closed. <bookmark mark='e'/> But if smoking affects cancer only through tar, and the genotype has no direct "
            "effect on tar, there is another way in: through the front door."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def formula(self):
        rows = [
            cmath(r"P(m \mid do(t))", r"=", r"P(m \mid t)", font_size=32),
            cmath(r"P(y \mid do(m))", r"=", r"\textstyle\sum_{t'} P(y \mid m, t')\, P(t')", font_size=32),
            cmath(r"P(y \mid do(t))", r"=", r"\textstyle\sum_m P(m \mid t) \sum_{t'} P(y \mid m, t')\, P(t')", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{no unmeasured confounding of } T \to M \text{ or } M \to Y \text{ given } T", font_size=26),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"no back door from $T$ to $M$"), why(r"$T$ blocks the back door from $M$ to $Y$"),
                why(r"chain the two: \ the front-door formula"), why(r"Pearl (1995)")]
        with self.voiceover(
            "<bookmark mark='a'/> The argument has two steps. The effect of smoking on tar has no back door, since the only "
            "path from T to M through U is blocked by the collider at Y: so it is just the conditional distribution. "
            "<bookmark mark='b'/> The effect of tar on cancer has a back door, M from T from U to Y, but conditioning on "
            "smoking blocks it: adjust for T. <bookmark mark='c'/> Chain the two, and the effect of smoking on cancer is "
            "identified, though the confounder was never measured. <bookmark mark='d'/> The price is two strong assumptions "
            "about the mediator, which real tar rarely satisfies; the front door is rare in practice, but it showed that "
            "adjustment is not the only route to identification."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("frontdoor")
        rows = fit_rows(VGroup(
            label(r"a simulated population of 400,000: \ 30\% carry the genotype", font_size=26),
            label(rf"naive: \ smokers' cancer risk minus non-smokers': \ {d['naive']:.3f}", font_size=26, color=MISSC),
            label(rf"the truth, \ $P(Y \mid do(T = 1)) - P(Y \mid do(T = 0))$: \ {d['truth']:.3f}", font_size=26, color=TRUEC),
            label(rf"the front-door formula, \ from $T$, $M$, $Y$ alone: \ {d['front']:.3f}", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulated population of four hundred thousand, thirty percent of whom carry the "
            "genotype. <bookmark mark='b'/> The naive comparison of smokers with non-smokers gives a difference in cancer "
            "risk of " + say(d["naive"], 3) + ", nearly double the truth, because carriers both smoke more and get more "
            "cancer. <bookmark mark='c'/> The true causal difference is " + say(d["truth"], 3) + ". <bookmark mark='d'/> The "
            "front-door formula, using only smoking, tar and cancer, gives " + say(d["front"], 3) + "."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def docalc(self):
        rows = [
            cmath(r"\text{rule 1}", r":", r"\text{delete an observation that is d-separated}", font_size=30),
            cmath(r"\text{rule 2}", r":", r"\text{exchange } do(z) \text{ for conditioning on } z", font_size=30),
            cmath(r"\text{rule 3}", r":", r"\text{delete an intervention that has no effect}", font_size=30),
            cmath(r"\text{complete}", r":", r"\text{if these cannot identify it, \ nothing can}", font_size=30),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"in a graph with arrows into $do$-nodes removed"), why(r"when the back doors are blocked"),
                why(r"when no path carries its effect"), why(r"Shpitser \& Pearl (2006); \ Huang \& Valtorta (2006)")]
        with self.voiceover(
            "<bookmark mark='a'/> Both the back-door and front-door formulas are special cases of Pearl's do-calculus, three "
            "rules for rewriting expressions with interventions. The first deletes or adds an observation when the graph "
            "makes it irrelevant. <bookmark mark='b'/> The second exchanges an intervention for a mere observation when no "
            "back door is open. <bookmark mark='c'/> The third deletes an intervention that cannot affect the outcome. "
            "<bookmark mark='d'/> In 2006 Ilya Shpitser and Pearl, and independently Yimin Huang and Marco Valtorta, proved "
            "the rules complete: if they cannot turn an interventional quantity into an observational one, no method can. "
            "Identification became a solved algorithmic problem, given the graph."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def swig(self):
        rows = fit_rows(VGroup(
            label(r"graphs and potential outcomes are two languages for one theory", font_size=26),
            label(r"single-world intervention graphs: \ split $T$ into the value set and the value it would take", font_size=26, color=TAUC),
            label(r"Richardson \& Robins (2013): \ read $Y(t) \perp\!\!\!\perp T \mid X$ straight off the graph", font_size=26, color=BANDC),
            label(r"next: \ an old paradox, \ resolved by drawing it", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The graphical language and the potential-outcomes language of Part 35 are two notations "
            "for one theory. <bookmark mark='b'/> Thomas Richardson and James Robins's single-world intervention graphs make "
            "the bridge explicit: they split the treatment node into the value we set and the value it would naturally take, "
            "<bookmark mark='c'/> so that statements like unconfoundedness, the independence of Y of t from T given X, can be "
            "read straight off the picture. <bookmark mark='d'/> Next, an old paradox, resolved by drawing it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
