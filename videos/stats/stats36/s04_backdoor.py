from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class Backdoor(VoiceoverScene):
    def construct(self):
        self.card()
        self.criterion()
        self.berkson()
        self.mbias()
        self.mediator()
        self.rules()

    def card(self):
        card = chapter_card(3, r"The back door", r"What to adjust for, \ and what not to", lit=(1946, 1995), part=PART)
        with self.voiceover("Chapter three. The back door."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def criterion(self):
        rows = [
            cmath(r"Z \text{ satisfies the back-door criterion}", r":", r"\text{no } Z \text{ is a descendant of } T", font_size=28),
            cmath(r"", r"\text{and}\;", r"Z \text{ blocks every path into } T \text{ from } Y", font_size=28),
            cmath(r"P(y \mid do(t))", r"=", r"\textstyle\sum_z P(y \mid t, z)\, P(z)", font_size=32),
            cmath(r"\text{the same as}", r":", r"\text{chapter 1's adjustment formula}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"never adjust for consequences of treatment"), why(r"every back-door path"),
                why(r"Pearl (1995): \ the back-door adjustment"), why(r"the graph says when it is valid")]
        with self.voiceover(
            "<bookmark mark='a'/> Pearl's back-door criterion says when a set of covariates Z is enough. First, nothing in Z "
            "may be a consequence of the treatment. <bookmark mark='b'/> Second, Z must block every back-door path from T to "
            "Y. <bookmark mark='c'/> If so, the distribution of the outcome under an intervention that sets T to t, written "
            "with Pearl's do-operator, is the conditional distribution given t and z, averaged over the population "
            "distribution of z. <bookmark mark='d'/> That is the adjustment formula of chapter one. The graph tells us when "
            "it is valid, and, as the next three examples show, when adjusting makes things worse."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def berkson(self):
        d = load("colliders")["berkson"]
        G = CausalGraph({"A": (-1.8, 1.0), "B": (1.8, 1.0), "H": (0, -0.8)}, [("A", "H"), ("B", "H")], center=[-3.2, 0.3, 0],
                        colors={"H": MISSC}, labels={"A": r"$D_1$", "B": r"$D_2$", "H": r"$H$"})
        side = fit_rows(VGroup(
            label(r"Joseph Berkson (1946): \ two independent diseases", font_size=22),
            label(r"$H$: \ admitted to hospital \ (either is severe)", font_size=22, color=MISSC),
            label(rf"everyone: \ correlation {d['all']:.2f}", font_size=22, color=BANDC),
            label(rf"hospital patients: \ {d['admitted']:.2f}", font_size=22, color=MISSC),
            label(r"conditioning on a collider manufactures an association", font_size=22, color=TAUC),
        ), 5.4, 0.4, [3.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1946 the Mayo Clinic statistician Joseph Berkson noticed that two diseases could appear "
            "related among hospital patients when they are unrelated in the population. <bookmark mark='b'/> Being admitted "
            "is a collider: either disease, if severe enough, puts you in hospital. <bookmark mark='c'/> Simulate two "
            "independent diseases: correlation zero. <bookmark mark='d'/> Among those admitted, the correlation is "
            + say(d["admitted"]) + ": a patient admitted without one disease must, almost surely, have the other. "
            "<bookmark mark='e'/> Conditioning on a collider, here by studying only hospital patients, manufactures an "
            "association out of nothing."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
                if k == 1:
                    self.play(Create(G.condition(["H"], MISSC)))
        self.clear_scene()

    def mbias(self):
        d = load("colliders")["mbias"]
        G = CausalGraph({"A": (-2.0, 1.4), "B": (2.0, 1.4), "M": (0, 0.4), "T": (-2.0, -1.2), "Y": (2.0, -1.2)},
                        [("A", "T"), ("A", "M"), ("B", "M"), ("B", "Y"), ("T", "Y")], center=[-3.0, 0.2, 0],
                        colors={"T": Y1C, "Y": Y0C, "M": MISSC})
        side = fit_rows(VGroup(
            label(r"M-bias: \ $M$ looks like a confounder", font_size=22),
            label(r"it precedes $T$ and correlates with both", font_size=22, color=GREY_A),
            label(rf"truth 1.00; \ unadjusted {d['unadjusted']:.2f}", font_size=22, color=BANDC),
            label(rf"adjusting for $M$: \ {d['adjust_M']:.2f}", font_size=22, color=MISSC),
            label(rf"for $M$ and $A$: \ {d['adjust_M_A']:.2f}", font_size=22, color=BANDC),
        ), 5.0, 0.4, [3.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A subtler trap is M-bias, named for the shape of its graph. A pre-treatment variable M is "
            "caused by two unmeasured variables, one of which affects the treatment and the other the outcome. <bookmark "
            "mark='b'/> M comes before treatment and is correlated with both T and Y, so it looks exactly like a confounder. "
            "<bookmark mark='c'/> But the only path through it is closed, because M is a collider: the unadjusted estimate is "
            "already right. <bookmark mark='d'/> Adjusting for M opens the path, and the estimate falls from one to "
            + say(d["adjust_M"]) + ". <bookmark mark='e'/> Adjusting for A as well blocks the path again. The rule 'adjust "
            "for everything measured before treatment' is not safe."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
                if k == 3:
                    self.play(Create(G.condition(["M"], MISSC)), FadeIn(G.path(["T", "A", "M", "B", "Y"], MISSC)))
        self.clear_scene()

    def mediator(self):
        d = load("colliders")["mediator"]
        G = CausalGraph({"T": (-2.0, -0.6), "M": (0, 1.2), "Y": (2.0, -0.6)}, [("T", "M"), ("M", "Y"), ("T", "Y")],
                        center=[-3.0, 0.2, 0], colors={"T": Y1C, "Y": Y0C, "M": TAUC})
        side = fit_rows(VGroup(
            label(r"a mediator: \ the drug works partly through $M$", font_size=22),
            label(rf"total effect: \ truth 2.00, \ unadjusted {d['total']:.2f}", font_size=22, color=BANDC),
            label(rf"adjusting for $M$: \ {d['adjusted']:.2f}, \ the direct part only", font_size=22, color=MISSC),
            label(r"never adjust for consequences of treatment \ (unless you want a direct effect)", font_size=22, color=TAUC),
        ), 5.0, 0.42, [3.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And a mediator: the treatment works partly through an intermediate variable M, such as a "
            "lab value that the drug changes. <bookmark mark='b'/> The unadjusted comparison estimates the total effect, "
            "two. <bookmark mark='c'/> Adjusting for M removes the part that flows through it, leaving one, the direct "
            "effect. <bookmark mark='d'/> Neither number is wrong, but they answer different questions, and adjusting for "
            "the consequences of treatment by habit answers the wrong one. Separating direct and indirect effects properly "
            "is mediation analysis, in Part 62."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def rules(self):
        rows = fit_rows(VGroup(
            label(r"adjust for confounders: \ common causes of $T$ and $Y$", font_size=26, color=BANDC),
            label(r"do not adjust for colliders, \ or for mediators and other consequences of $T$", font_size=26, color=MISSC),
            label(r"VanderWeele \& Shpitser (2011): \ adjust for causes of $T$, \ of $Y$, \ or both", font_size=26, color=GREY_A),
            label(r"a data set cannot tell you which is which; \ a graph can", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: adjust for confounders, the common causes of treatment and outcome. <bookmark "
            "mark='b'/> Do not adjust for colliders, nor for mediators or anything else the treatment affects. <bookmark "
            "mark='c'/> When the full graph is uncertain, Tyler VanderWeele and Ilya Shpitser's disjunctive cause criterion "
            "is a safe default: adjust for every pre-treatment variable that is a cause of the treatment, the outcome, or "
            "both. <bookmark mark='d'/> The data alone cannot tell confounders from colliders; they have the same "
            "correlations. Only knowledge of the causal structure can."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
