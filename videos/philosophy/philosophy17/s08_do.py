from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Do(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Seeing and doing", r"When does observing tell us what intervening would do?",
                            lit=(1993, 1995), part=PART)
        with self.voiceover("Chapter seven. Seeing and doing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.surgery()
        self.backdoor()
        self.frontdoor()
        self.nonid()

    def surgery(self):
        head = label(r"The do-operator: \ graph surgery", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        pos = {"age": [-4.4, 1.4, 0], "drug": [-5.6, -0.4, 0], "recover": [-3.2, -0.4, 0]}
        g = CausalGraph(pos, [("age", "drug"), ("age", "recover"), ("drug", "recover")], radius=0.58, font_size=16,
                        colors={"drug": CAUSE, "recover": EFFECT})
        pos2 = {k: [v[0] + 6.2, v[1], 0] for k, v in pos.items()}
        g2 = CausalGraph(pos2, [("age", "drug"), ("age", "recover"), ("drug", "recover")], radius=0.58, font_size=16,
                         colors={"drug": DOC, "recover": EFFECT})
        l1 = label(r"seeing: \ $P(\text{recover} \mid \text{drug})$", font_size=21, color=WHITE).next_to(g, DOWN,
                                                                                                    buff=0.35)
        l2 = label(r"doing: \ $P(\text{recover} \mid do(\text{drug}))$", font_size=21, color=DOC).next_to(g2, DOWN,
                                                                                                      buff=0.35)
        rule = stack([(r"$do(X = x)$: \ replace $X$'s equation by $X := x$, \ and delete the arrows into $X$", DOC),
                      (r"the patients who \textit{choose} the drug differ in age; \ those \textit{assigned} it do not",
                       GREY_A)], font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Pearl's central distinction is between seeing and doing. <bookmark mark='a'/>Seeing: among patients who "
            "took the drug, how many recovered? Here age influences both who takes the drug and who recovers. "
            "<bookmark mark='b'/>Doing: if we made patients take the drug, how many would recover? "
            "<bookmark mark='c'/>The do-operator answers by surgery on the model: replace the drug's equation by a "
            "constant, and delete the arrows into it. Age no longer influences who is treated. "
            "<bookmark mark='d'/>The difference is the difference between patients who choose a drug and patients "
            "assigned to it, which is why randomized trials work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(l2))
            vo.wait_until("c")
            self.play(g2.edge[("age", "drug")].animate.set_opacity(0.1), FadeIn(rule[0]))
            vo.wait_until("d")
            self.play(FadeIn(rule[1]))
        self.clear_scene()

    def backdoor(self):
        d = load("adjust")
        b, smp = d["backdoor"], d["sample"]
        head = label(r"The back-door criterion", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        crit = stack([(r"$Z$ satisfies the back-door criterion for $(X, Y)$ if", WHITE),
                      (r"no member of $Z$ is a descendant of $X$, \ and", GREY_A),
                      (r"$Z$ blocks every path from $X$ to $Y$ that begins with an arrow \textit{into} $X$", GREY_A)],
                     font_size=21, aligned_edge=LEFT).next_to(head, DOWN, buff=0.3).set_x(0)
        eq = MathTex(r"P(y \mid do(x)) = \sum_z P(y \mid x, z)\, P(z)", font_size=36, color=GOAL).next_to(crit, DOWN,
                                                                                                        buff=0.35)
        hd = [r"", r"\text{naive } P(r \mid d) - P(r \mid \lnot d)", r"\text{adjusted for age}",
              r"\text{truth, by } do"]
        rows = [[MathTex(r"\text{exact}", font_size=22), MathTex(f"{b['naive']:.3f}", font_size=24, color=BAD),
                 MathTex(f"{b['adjusted']:.3f}", font_size=24, color=OK),
                 MathTex(f"{b['truth']:.3f}", font_size=24, color=OK)],
                [MathTex(f"n = {smp['n']:,}".replace(",", "{,}"), font_size=22),
                 MathTex(f"{smp['naive']:.3f}", font_size=24, color=BAD),
                 MathTex(f"{smp['adjusted']:.3f}", font_size=24, color=OK),
                 MathTex(f"{smp['rct']:.3f}" + r"\ (\text{RCT})", font_size=24, color=OK)]]
        grid = ValueGrid(hd, rows, col_w=[2.2, 3.8, 2.6, 2.8], cell_h=0.55, font_size=20).next_to(eq, DOWN, buff=0.4)
        grid.set_x(0)
        ck = label(r"the Reasoner: \ $\{\text{age}\}$ satisfies the criterion: \ " +
                   (r"$\checkmark$" if b["criterion_A"] else r"$\times$") + r"; \ \ the empty set: \ " +
                   (r"$\checkmark$" if b["criterion_empty"] else r"$\times$"), font_size=20, color=GREY_A).next_to(
            grid, DOWN, buff=0.2)
        with self.voiceover(
            "When can the effect of doing be computed from data about seeing? Pearl's first answer is the back-door "
            "criterion. <bookmark mark='a'/>A set of variables Z qualifies if it contains no descendant of the "
            "treatment, and blocks every path from treatment to outcome that begins with an arrow into the "
            "treatment: every back door. <bookmark mark='b'/>Then the effect of doing is a weighted average of "
            "conditional probabilities: adjust for Z. <bookmark mark='c'/>On the drug model, the naive comparison "
            "of treated and untreated says the drug raises recovery by twelve points. Adjusting for age gives "
            "twenty, exactly the effect under intervention. <bookmark mark='d'/>From two hundred thousand simulated "
            "patients, the naive estimate is still twelve, the adjusted estimate twenty, matching a simulated "
            "randomized trial. The Reasoner confirms that age satisfies the criterion and the empty set does not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in crit], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[1])), FadeIn(ck))
        self.clear_scene()

    def frontdoor(self):
        d = load("adjust")["frontdoor"]
        head = label(r"The front door: \ smoking, \ tar and a hidden gene", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        g = CausalGraph({"smoking": [-5.4, -0.2, 0], "tar": [-3.2, -0.2, 0], "cancer": [-1.0, -0.2, 0],
                         "gene": [-3.2, 1.6, 0]},
                        [("smoking", "tar"), ("tar", "cancer"), ("gene", "smoking"), ("gene", "cancer")],
                        hidden=("gene",), radius=0.6, font_size=15, colors={"smoking": CAUSE, "cancer": EFFECT},
                        dashed=(("gene", "smoking"), ("gene", "cancer")))
        eq = MathTex(r"P(c \mid do(s)) = \sum_t P(t \mid s) \sum_{s'} P(c \mid t, s')\, P(s')", font_size=30,
                     color=GOAL).move_to([3.4, 1.0, 0])
        side = stack([(r"the gene is unobserved: \ no back-door adjustment", BAD),
                      (r"but smoking acts only through tar, \ and tar's link to cancer is unconfounded", WHITE),
                      (r"naive difference: \ " + f"{d['naive']:.2f}", BAD),
                      (r"front-door formula: \ " + f"{d['front']:.3f}", OK),
                      (r"truth, \ by $do$: \ " + f"{d['truth']:.3f}", OK)], font_size=21, aligned_edge=LEFT,
                     width=6.4).next_to(eq, DOWN, buff=0.4)
        with self.voiceover(
            "Fisher's smoking objection has a surprising answer. <bookmark mark='a'/>Suppose a hidden gene causes "
            "both smoking and cancer, as Fisher proposed. The gene is unobserved, so no back-door adjustment is "
            "possible. <bookmark mark='b'/>But suppose smoking causes cancer only by depositing tar in the lungs, "
            "and the gene does not affect tar directly. <bookmark mark='c'/>Pearl's front-door formula then "
            "recovers the causal effect from observational data alone, in two steps: smoking's effect on tar, and "
            "tar's effect on cancer, adjusting for smoking. <bookmark mark='d'/>In the Reasoner's model, the naive "
            "difference is point six two, mostly the gene. <bookmark mark='e'/>The front-door formula gives point "
            "three four, exactly the effect under intervention, which the Reasoner also computes directly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Indicate(g.node["tar"], color=GOAL), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Write(eq))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def nonid(self):
        d = load("nonid")
        head = label(r"When data cannot decide", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        g1 = CausalGraph({"X": [-5.0, 0.6, 0], "Y": [-2.6, 0.6, 0]}, [("X", "Y")], colors={"X": CAUSE, "Y": EFFECT})
        g2 = CausalGraph({"X": [2.6, 0.6, 0], "Y": [5.0, 0.6, 0], "U": [3.8, 2.0, 0]}, [("U", "X"), ("U", "Y")],
                         hidden=("U",), colors={"X": CAUSE, "Y": EFFECT}, dashed=(("U", "X"), ("U", "Y")))
        cells = sorted((tuple(int(t) for t in k.strip("()").split(",")), v) for k, v in d["obs1"].items())
        same_ok = all(abs(d["obs1"][k] - d["obs2"][k]) < 1e-12 for k in d["obs1"])
        obs = r", \ ".join(f"$P({a}, {b}) = {v:.1f}$" for (a, b), v in cells)
        same = label(r"both models: \ " + obs + (r" \ \ (identical)" if same_ok else ""), font_size=20,
                     color=WHITE).move_to([0, -0.8, 0])
        e1 = label(r"effect of $do(X)$: \ " + f"{d['do1']:.1f}", font_size=22, color=OK).next_to(g1, DOWN, buff=0.4)
        e2 = label(r"effect of $do(X)$: \ " + f"{d['do2']:.1f}", font_size=22, color=BAD).next_to(g2, DOWN, buff=0.4)
        foot = stack([(r"no amount of passive data distinguishes them", GOAL),
                      (r"identification theory says exactly when assumptions plus data suffice \ (next chapter)",
                       GREY_A)], font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Sometimes no formula exists. <bookmark mark='a'/>In one model, X causes Y directly. "
            "<bookmark mark='b'/>In another, X has no effect at all on Y, and a hidden common cause produces their "
            "correlation. <bookmark mark='c'/>The Reasoner computes both observational distributions: they are "
            "identical, cell for cell. <bookmark mark='d'/>But the effect of intervening on X is point six in the "
            "first model and zero in the second. <bookmark mark='e'/>No quantity of passive data can tell them "
            "apart. Which causal effects can be computed, from which assumptions, is the subject of identification "
            "theory, and the next chapter gives its complete answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1))
            vo.wait_until("b")
            self.play(FadeIn(g2))
            vo.wait_until("c")
            self.play(FadeIn(same))
            vo.wait_until("d")
            self.play(FadeIn(e1), FadeIn(e2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
