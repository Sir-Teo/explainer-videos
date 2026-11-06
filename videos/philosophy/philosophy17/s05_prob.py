from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Prob(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Raising the probability", r"Do causes make their effects more likely?",
                            lit=(1970, 1979), part=PART)
        with self.voiceover("Chapter four. Raising the probability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.suppes()
        self.hesslow()
        self.cartwright()

    def suppes(self):
        hc = history_card(1970, r"Patrick Suppes", r"\textit{A Probabilistic Theory of Causality}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        defs = VGroup(
            label(r"prima facie cause:", font_size=22, color=CAUSE),
            MathTex(r"C \text{ precedes } E \quad\text{and}\quad P(E \mid C) > P(E)", font_size=32, color=CAUSE),
            label(r"spurious, \ if an earlier $F$ screens it off:", font_size=22, color=BAD),
            MathTex(r"P(E \mid C \wedge F) = P(E \mid F)", font_size=32, color=BAD),
        ).arrange(DOWN, buff=0.22).next_to(hc, DOWN, buff=0.45).set_x(-2.4)
        g = CausalGraph({"pressure": [3.6, 1.4, 0], "barometer": [2.2, -0.4, 0], "storm": [5.0, -0.4, 0]},
                        [("pressure", "barometer"), ("pressure", "storm")], radius=0.6, font_size=16,
                        colors={"barometer": CAUSE, "storm": EFFECT, "pressure": HIDDEN})
        gl = label(r"the barometer raises the probability of a storm; \ pressure screens it off", font_size=19,
                   color=GREY_A).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "Causes need not be followed by their effects every time; smoking does not always produce cancer. So "
            "Patrick Suppes proposed that causes raise the probability of their effects. <bookmark mark='a'/>C is a "
            "prima facie cause of E if C comes first and the probability of E given C exceeds the probability of E. "
            "<bookmark mark='b'/>A prima facie cause is spurious if some earlier factor screens it off, so that once "
            "that factor is known, C makes no further difference. <bookmark mark='c'/>The falling barometer raises "
            "the probability of a storm, but the earlier drop in air pressure screens it off: given the pressure, "
            "the barometer adds nothing."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), Write(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]), Write(defs[3]))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(gl))
        self.clear_scene()

    def hesslow(self):
        d = load("prob")
        head = label(r"Hesslow's pills: \ a cause that does not raise the probability", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        g = CausalGraph({"pill": [-4.6, 0.2, 0], "pregnant": [-2.4, 1.8, 0], "thrombosis": [-0.2, 0.2, 0]},
                        [("pill", "pregnant"), ("pregnant", "thrombosis"), ("pill", "thrombosis")], radius=0.66,
                        font_size=16, colors={"pill": CAUSE, "thrombosis": EFFECT, "pregnant": WHITE})
        signs = VGroup(label(r"$-$", font_size=30, color=BAD).move_to([-3.8, 1.3, 0]),
                       label(r"$+$", font_size=30, color=OK).move_to([-1.0, 1.3, 0]),
                       label(r"$+$", font_size=30, color=OK).move_to([-2.4, -0.15, 0]))
        side = stack([(r"the pill raises thrombosis directly", OK),
                      (r"and prevents pregnancy, \ which raises it", BAD),
                      (r"the Reasoner's model: \ $P(T \mid \text{pill}) = " + f"{d['P(T|pill)']:.2f}" +
                       r"$, \ $P(T \mid \text{no pill}) = " + f"{d['P(T|no pill)']:.2f}" + r"$", WHITE),
                      (r"yet among women who are not pregnant, \ the pill adds " +
                       f"{d['direct_effect_given_not_pregnant']:.2f}", CAUSE),
                      (r"the paths cancel: \ a cause with no correlation", GOAL)], font_size=21, aligned_edge=LEFT,
                     width=6.0).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "Germund Hesslow found a case that breaks the probability-raising idea. <bookmark mark='a'/>Birth-control "
            "pills raise the risk of thrombosis directly. <bookmark mark='b'/>But they also prevent pregnancy, which "
            "itself raises the risk of thrombosis. <bookmark mark='c'/>In the Reasoner's model, with numbers chosen "
            "so the paths cancel, the probability of thrombosis is point three with the pill and point three "
            "without. <bookmark mark='d'/>Yet among women who are not pregnant, the pill raises the risk by point "
            "two. <bookmark mark='e'/>A genuine cause can fail to raise the probability of its effect, when two "
            "paths cancel. Chapter eleven gives the assumption that rules this out, and calls it faithfulness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.node["pill"]), FadeIn(g.node["thrombosis"]), FadeIn(g.node["pregnant"]))
            vo.wait_until("a")
            self.play(GrowArrow(g.edge[("pill", "thrombosis")]), FadeIn(signs[2]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowArrow(g.edge[("pill", "pregnant")]), GrowArrow(g.edge[("pregnant", "thrombosis")]),
                      FadeIn(signs[0]), FadeIn(signs[1]), FadeIn(side[1]))
            for mk, r in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cartwright(self):
        hc = history_card(1979, r"Nancy Cartwright", r"`Causal Laws and Effective Strategies'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"effective strategies", r"we need causes, \ not correlations, \ to know what to \textit{do}", CAUSE),
            (r"contextual unanimity", r"$C$ causes $E$ only if it raises $P(E)$ in every causally homogeneous "
                                      r"background", EFFECT),
            (r"Simpson again", r"partition by the right factors, \ and the reversal disappears", OK),
            (r"but which factors?", r"`causally homogeneous' needs causal knowledge: \ no causes in, \ no causes out",
             BAD),
        ]
        g = rows_table(rows, top=1.2, gap=0.55, width=8.2, x_text=-2.0)
        with self.voiceover(
            "Nancy Cartwright drew the moral in 1979. <bookmark mark='a'/>We need causal laws, not just correlations, "
            "because we need to know which strategies will work. <bookmark mark='b'/>She proposed that C causes E "
            "only if C raises the probability of E in every background context that is causally homogeneous. "
            "<bookmark mark='c'/>Partition the population by the right factors, and Simpson's reversals disappear. "
            "<bookmark mark='d'/>But which factors are the right ones? Causally homogeneous contexts are defined by "
            "causes. Probabilities can test causal claims, but only once some causal knowledge has been put in: no "
            "causes in, no causes out."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
