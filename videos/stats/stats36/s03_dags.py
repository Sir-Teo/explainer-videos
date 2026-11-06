from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class DAGs(VoiceoverScene):
    def construct(self):
        self.card()
        self.wright()
        self.graph()
        self.three()
        self.dsep()
        self.world()
        self.lesson()

    def card(self):
        card = chapter_card(2, r"Causal diagrams", r"Arrows for causes, \ paths for associations", lit=(1921, 1995), part=PART)
        with self.voiceover("Chapter two. Causal diagrams."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def wright(self):
        rows = fit_rows(VGroup(
            label(r"Sewall Wright (1921): \ path diagrams for the inheritance of coat colour in guinea pigs", font_size=26, color=Y0C),
            label(r"ignored by statisticians for half a century", font_size=26, color=GREY_A),
            label(r"Judea Pearl (1995, \ 2000): \ directed acyclic graphs, \ d-separation, \ the do-operator", font_size=26, color=TAUC),
            label(r"a causal graph is an assumption: \ which variables cause which", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1921 the geneticist Sewall Wright drew diagrams of arrows to describe how coat colour "
            "was inherited in guinea pigs, and showed how to read correlations off them. <bookmark mark='b'/> Statisticians, "
            "Fisher among them, largely ignored the idea for half a century. <bookmark mark='c'/> In the 1990s the computer "
            "scientist Judea Pearl rebuilt it as a theory of directed acyclic graphs, with rules for reading off which "
            "variables are independent, and an operator for interventions. <bookmark mark='d'/> A causal graph is an "
            "assumption made explicit: which variables directly cause which. Everything else follows from it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def graph(self):
        G = CausalGraph({"X": (0, 1.6), "T": (-2.4, -0.6), "Y": (2.4, -0.6)}, [("X", "T"), ("X", "Y"), ("T", "Y")],
                        center=[-2.2, 0.0, 0], scale=1.0, colors={"T": Y1C, "Y": Y0C, "X": TAUC})
        side = fit_rows(VGroup(
            label(r"$T$: \ the drug; \ $Y$: \ the pressure", font_size=22),
            label(r"$X$: \ baseline pressure, \ age, \ BMI", font_size=22, color=TAUC),
            label(r"$X \to T$: \ doctors use them", font_size=22),
            label(r"$X \to Y$: \ they also affect the outcome", font_size=22),
            label(r"$T \to Y$: \ the effect we want", font_size=22, color=Y0C),
        ), 4.6, 0.4, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's observational study as a graph. The drug T and the twelve-week pressure Y. "
            "<bookmark mark='b'/> X, the baseline pressure, age and weight. <bookmark mark='c'/> An arrow from X to T, because "
            "the doctors use them to decide. <bookmark mark='d'/> An arrow from X to Y, because they also affect the outcome. "
            "<bookmark mark='e'/> And an arrow from T to Y: the effect we want. The absence of an arrow is the strong claim: "
            "no unrecorded variable points into both T and Y."
        ) as vo:
            self.add(obs_tag())
            self.play(FadeIn(G.node("T")), FadeIn(G.node("Y")), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(G.node("X")), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowArrow(G.arrows[("X", "T")]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowArrow(G.arrows[("X", "Y")]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(GrowArrow(G.arrows[("T", "Y")]), FadeIn(side[4]))
        self.clear_scene()

    def three(self):
        chain = CausalGraph({"A": (-1.4, 0), "B": (0, 0), "C": (1.4, 0)}, [("A", "B"), ("B", "C")], center=[-4.4, 1.0, 0], scale=0.9, radius=0.3)
        fork = CausalGraph({"A": (-1.4, -0.6), "B": (0, 0.6), "C": (1.4, -0.6)}, [("B", "A"), ("B", "C")], center=[0, 1.0, 0], scale=0.9, radius=0.3)
        coll = CausalGraph({"A": (-1.4, 0.6), "B": (0, -0.6), "C": (1.4, 0.6)}, [("A", "B"), ("C", "B")], center=[4.4, 1.0, 0], scale=0.9, radius=0.3)
        names = VGroup(label(r"chain: \ a mediator", font_size=22, color=Y0C).next_to(chain, UP, buff=0.3),
                       label(r"fork: \ a confounder", font_size=22, color=TAUC).next_to(fork, UP, buff=0.3),
                       label(r"collider", font_size=22, color=MISSC).next_to(coll, UP, buff=0.3))
        rules = VGroup(label(r"open; \ closed by conditioning on $B$", font_size=20).next_to(chain, DOWN, buff=0.4),
                       label(r"open; \ closed by conditioning on $B$", font_size=20).next_to(fork, DOWN, buff=0.4),
                       label(r"closed; \ \emph{opened} by conditioning on $B$", font_size=20, color=MISSC).next_to(coll, DOWN, buff=0.4))
        boxes = VGroup(chain.condition(["B"]), fork.condition(["B"]), coll.condition(["B"], MISSC))
        with self.voiceover(
            "<bookmark mark='a'/> Every path in a graph is built from three kinds of junction. In a chain, A causes B "
            "causes C, and B is a mediator. Association flows along the chain, and conditioning on B blocks it. <bookmark "
            "mark='b'/> In a fork, B causes both A and C: a confounder. Again association flows, and conditioning on B "
            "blocks it. <bookmark mark='c'/> In a collider, A and C both cause B. Now the path is closed: A and C are "
            "independent. <bookmark mark='d'/> But conditioning on the collider opens it. That last rule is the surprising "
            "one, and the source of some famous paradoxes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(chain), FadeIn(names[0]), FadeIn(rules[0]))
            self.play(Create(boxes[0]))
            vo.wait_until("b")
            self.play(FadeIn(fork), FadeIn(names[1]), FadeIn(rules[1]))
            self.play(Create(boxes[1]))
            vo.wait_until("c")
            self.play(FadeIn(coll), FadeIn(names[2]))
            vo.wait_until("d")
            self.play(FadeIn(rules[2]), Create(boxes[2]))
        self.clear_scene()

    def dsep(self):
        rows = [
            cmath(r"\text{a path is blocked by } Z", r"\iff", r"\text{it has a non-collider in } Z", font_size=28),
            cmath(r"", r"\text{or}\;", r"\text{a collider not in } Z \text{ with no descendant in } Z", font_size=28),
            cmath(r"X \perp_d Y \mid Z", r"\iff", r"\text{every path between them is blocked}", font_size=30),
            cmath(r"\text{then}", r":", r"X \perp\!\!\!\perp Y \mid Z \ \text{in every distribution the graph allows}", font_size=28),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"a chain or fork node we conditioned on"), why(r"a collider we left alone"),
                why(r"d-separation"), why(r"Verma \& Pearl (1988); \ Geiger et al. (1990)")]
        with self.voiceover(
            "<bookmark mark='a'/> The rules combine into d-separation. A path is blocked by a set Z if it passes through a "
            "chain or fork node that is in Z, <bookmark mark='b'/> or through a collider that is not in Z and has no "
            "descendant in Z. <bookmark mark='c'/> Two variables are d-separated by Z if every path between them is blocked. "
            "<bookmark mark='d'/> And then, as Thomas Verma, Pearl and others proved, they are independent given Z in every "
            "probability distribution consistent with the graph. Independence, a statistical property, is read off a "
            "picture of causes."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def world(self):
        G = CausalGraph({"X": (0, 1.6), "T": (-2.4, -0.6), "Y": (2.4, -0.6), "U": (0, -2.0)},
                        [("X", "T"), ("X", "Y"), ("T", "Y"), ("U", "T"), ("U", "Y")],
                        center=[-2.2, 0.3, 0], colors={"T": Y1C, "Y": Y0C, "X": TAUC, "U": MISSC})
        back1 = G.path(["T", "X", "Y"], TAUC)
        back2 = G.path(["T", "U", "Y"], MISSC)
        side = fit_rows(VGroup(
            label(r"two back-door paths from $T$ to $Y$", font_size=22),
            label(r"$T \leftarrow X \to Y$: \ blocked by adjusting for $X$", font_size=22, color=TAUC),
            label(r"$T \leftarrow U \to Y$: \ $U$ unmeasured, \ e.g. frailty", font_size=22, color=MISSC),
            label(r"if $U$ exists, \ no adjustment for $X$ suffices", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Apply the rules to the treatment and outcome. Association between T and Y can flow along "
            "the causal arrow, and along back-door paths, which start with an arrow into T. <bookmark mark='b'/> The path "
            "through X is a fork, blocked by adjusting for X. <bookmark mark='c'/> But suppose the doctors also judge an "
            "unrecorded frailty U, which also affects the outcome. <bookmark mark='d'/> That path stays open whatever we do "
            "with X. The graph shows exactly what unconfoundedness requires: no open back-door path once X is adjusted for."
        ) as vo:
            self.play(FadeIn(VGroup(G.nodes["X"], G.nodes["T"], G.nodes["Y"], G.arrows[("X", "T")], G.arrows[("X", "Y")], G.arrows[("T", "Y")])))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(back1), FadeIn(G.condition(["X"])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(G.nodes["U"]), GrowArrow(G.arrows[("U", "T")]), GrowArrow(G.arrows[("U", "Y")]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(back2), FadeIn(side[3]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the graph is built from knowledge, \ not from the data", font_size=26, color=TAUC),
            label(r"its testable implications: \ the d-separations it predicts", font_size=26, color=GREY_A),
            label(r"its untestable core: \ the arrows it leaves out", font_size=26, color=MISSC),
            label(r"next: \ what to adjust for, \ and what to leave alone", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The graph comes from knowledge of the subject, not from the data. <bookmark mark='b'/> Some "
            "of its implications can be tested, because it predicts particular independences. <bookmark mark='c'/> Its core "
            "cannot: the arrows it leaves out, especially to and from unmeasured variables. <bookmark mark='d'/> Next, how "
            "the graph tells us what to adjust for, and what to leave alone."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
