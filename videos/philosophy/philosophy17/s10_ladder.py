from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


SQUAD = {"U": [-4.0, 2.2, 0], "C": [-4.0, 1.0, 0], "A": [-5.2, -0.2, 0], "B": [-2.8, -0.2, 0], "D": [-4.0, -1.4, 0]}
DO0 = "P(y|do x')"
SQUAD_E = [("U", "C"), ("C", "A"), ("C", "B"), ("A", "D"), ("B", "D")]


class Ladder(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"The ladder of causation", r"Seeing, doing, imagining", lit=(1994, 2018), part=PART)
        with self.voiceover("Chapter nine. The ladder of causation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rungs()
        self.squad()
        self.twin()
        self.necessity()
        self.hierarchy()

    def rungs(self):
        head = label(r"Three rungs \ (Pearl and Mackenzie, \ 2018)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rails = VGroup(Line([-6.0, -2.9, 0], [-6.0, 2.3, 0], color=GREY_B, stroke_width=5),
                       Line([-4.6, -2.9, 0], [-4.6, 2.3, 0], color=GREY_B, stroke_width=5))
        data = [(r"1. \ association: \ \textit{seeing}", r"P(y \mid x)",
                 r"what does a symptom tell me about the disease?", EFFECT, -2.0),
                (r"2. \ intervention: \ \textit{doing}", r"P(y \mid do(x))",
                 r"what happens if I take the aspirin?", DOC, -0.2),
                (r"3. \ counterfactuals: \ \textit{imagining}", r"P(y_{x'} \mid x, y)",
                 r"was it the aspirin that cured my headache?", CAUSE, 1.6)]
        rungs = VGroup()
        for t, f, q, c, y in data:
            bar = Line([-6.0, y, 0], [-4.6, y, 0], color=c, stroke_width=7)
            tt = label(t, font_size=24, color=c).move_to([-3.9, y + 0.3, 0], aligned_edge=LEFT)
            ff = MathTex(f, font_size=32, color=c).move_to([3.6, y + 0.3, 0])
            qq = label(q, font_size=20, color=GREY_A).move_to([-3.9, y - 0.2, 0], aligned_edge=LEFT)
            rungs.add(VGroup(bar, tt, ff, qq))
        foot = label(r"each rung answers questions the one below cannot", font_size=22, color=GOAL).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Pearl arranges causal questions on a ladder of three rungs. <bookmark mark='a'/>The first is "
            "association, seeing: what does a symptom tell me about a disease? Its language is conditional "
            "probability. <bookmark mark='b'/>The second is intervention, doing: what will happen if I take the "
            "aspirin? Its language is the do-operator. <bookmark mark='c'/>The third is counterfactuals, "
            "imagining: my headache is gone; was it the aspirin? This asks about a world that did not happen, given "
            "what did. <bookmark mark='d'/>Each rung answers questions that the one below cannot."
        ) as vo:
            self.play(FadeIn(head), Create(rails))
            for mk, r in zip("abc", rungs):
                vo.wait_until(mk)
                self.play(Create(r[0]), FadeIn(r[1]), Write(r[2]), FadeIn(r[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def squad(self):
        d = load("ladder")["squad"]
        head = label(r"The firing squad", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g = CausalGraph(SQUAD, SQUAD_E, radius=0.4, font_size=20, colors={"U": HIDDEN, "A": CAUSE, "D": EFFECT})
        key = label(r"$U$ court order \ ($p = " + f"{d['p_order']:.1f}" + r"$), \ $C$ captain, \ $A, B$ riflemen, \ "
                    r"$D$ death", font_size=19, color=GREY_A).next_to(g, DOWN, buff=0.35)
        rows = stack([
            (r"rung 1: \ $P(D \mid A) = " + f"{d['rung1_P(D|A)']:.1f}" + r"$, \ \ $P(D \mid \lnot A) = " +
             f"{d['rung1_P(D|not A)']:.1f}" + r"$", EFFECT),
            (r"\ \ \ \ A's shooting is a perfect sign of death", GREY_A),
            (r"rung 2: \ $P(D \mid do(\lnot A)) = " + f"{d['rung2_P(D|do A=0)']:.1f}" + r"$", DOC),
            (r"\ \ \ \ restrain A, \ and the prisoner still dies whenever the court orders it", GREY_A),
            (r"rung 3: \ the prisoner is dead; \ had A not shot? \ \ $P(D_{\lnot A} \mid D) = " +
             f"{d['rung3_dead_had_A_not_shot']:.1f}" + r"$", CAUSE),
            (r"\ \ \ \ B shot too: \ A's shot was not necessary, \ in this very case", GREY_A),
        ], font_size=21, aligned_edge=LEFT, buff=0.2, width=7.4).move_to([2.6, -0.1, 0])
        with self.voiceover(
            "Pearl's firing squad puts all three rungs on one model. <bookmark mark='a'/>A court may order an "
            "execution. If it does, the captain signals; both riflemen, A and B, shoot; and the prisoner dies. "
            "<bookmark mark='b'/>On rung one: the prisoner dies whenever A shoots, and survives whenever A does "
            "not. A's shot is a perfect sign. <bookmark mark='c'/>On rung two: if we restrain A, the prisoner still "
            "dies with probability point seven, whenever the court orders it, because B obeys the signal. "
            "<bookmark mark='d'/>On rung three: the prisoner is dead. Had A not shot, would he be alive? No, with "
            "certainty: the death tells us there was an order, so B shot too. This counterfactual is about this "
            "very case, and no experiment on other prisoners could answer it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(g.edge[("C", "A")].animate.set_opacity(0.12), g.node["A"][0].animate.set_color(DOC),
                      FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def twin(self):
        head = label(r"Computing a counterfactual: \ three steps", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        left = {k: [v[0] + 1.2, v[1] + 0.25, 0] for k, v in SQUAD.items() if k != "U"}
        right = {k + "'": [v[0] + 5.6, v[1] + 0.25, 0] for k, v in SQUAD.items() if k != "U"}
        pos = {**left, **right, "U": [-0.6, 2.5, 0]}
        edges = [(a, b) for a, b in SQUAD_E if a != "U"] + [(a + "'", b + "'") for a, b in SQUAD_E if a != "U"]
        edges += [("U", "C"), ("U", "C'")]
        g = CausalGraph(pos, edges, radius=0.36, font_size=17, colors={"U": HIDDEN, "D": EFFECT, "A'": DOC,
                                                                        "D'": CAUSE})
        tags = VGroup(label(r"actual world", font_size=20, color=GREY_A).next_to(g.node["D"], LEFT, buff=0.3),
                      label(r"hypothetical world", font_size=20, color=GREY_A).next_to(g.node["D'"], RIGHT, buff=0.3))
        steps = stack([(r"1. \ abduction: \ from the evidence $D = 1$, \ infer $U = 1$", HIDDEN),
                       (r"2. \ action: \ in a copy of the model, \ set $A' := 0$", DOC),
                       (r"3. \ prediction: \ solve the copy: \ $B' = 1$, \ so $D' = 1$", CAUSE),
                       (r"the twin network \ (Balke and Pearl, \ 1994): \ two worlds sharing one $U$", GOAL)],
                      font_size=21, aligned_edge=LEFT).to_edge(DOWN, buff=0.35)
        a_new = label(r"$:= 0$", font_size=18, color=DOC).next_to(g.node["A'"], LEFT, buff=0.1)
        with self.voiceover(
            "How is a counterfactual computed? Draw two copies of the model, the actual world and the hypothetical "
            "one, sharing the same background conditions. <bookmark mark='a'/>Step one, abduction: use the "
            "evidence to update what we know about the background. The prisoner died, so there was an order. "
            "<bookmark mark='b'/>Step two, action: in the hypothetical copy, set A to not shooting, cutting the "
            "arrow from the captain. <bookmark mark='c'/>Step three, prediction: solve the copy. The order still "
            "reaches B, B still shoots, and the prisoner still dies. <bookmark mark='d'/>This twin network, due to "
            "Alexander Balke and Pearl, turns every counterfactual query into an ordinary calculation on a larger "
            "graph."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), Indicate(g.node["D"], color=EFFECT),
                      g.node["U"][0].animate.set_color(OK))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), g.edge[("C'", "A'")].animate.set_opacity(0.12), FadeIn(a_new))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), Indicate(g.node["B'"], color=CAUSE), Indicate(g.node["D'"], color=CAUSE))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.clear_scene()

    def necessity(self):
        d = load("ladder")["pnps"]
        head = label(r"Necessity and sufficiency", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        types = [(r"responders", 0.3, CAUSE), (r"always", 0.2, EFFECT), (r"never", 0.5, HIDDEN)]
        bars, x = VGroup(), -6.2
        for name, w, c in types:
            r = Rectangle(width=w * 7.0, height=0.6, stroke_color=c, fill_color=c, fill_opacity=0.35).move_to(
                [x + w * 3.5, 1.8, 0])
            t = label(name + f" {w:.1f}", font_size=18, color=c).next_to(r, DOWN, buff=0.12)
            bars.add(VGroup(r, t))
            x += w * 7.0
        bl = label(r"three kinds of patient: \ $Y = X$, \ $Y = 1$, \ $Y = 0$", font_size=20, color=GREY_A).next_to(
            bars, UP, buff=0.2)
        eqs = VGroup(
            MathTex(r"\mathrm{PN} = P(Y_{x'} = 0 \mid X = 1, Y = 1) = " + f"{d['PN']:.2f}", font_size=30, color=CAUSE),
            MathTex(r"\mathrm{PS} = P(Y_{x} = 1 \mid X = 0, Y = 0) = " + f"{d['PS']:.3f}", font_size=30, color=EFFECT),
            MathTex(r"\mathrm{PNS} = P(y \mid do(x)) - P(y \mid do(x')) = " + f"{d['P(y|do x)']:.1f} - "
                    + f"{d[DO0]:.1f} = {d['PNS']:.1f}", font_size=30, color=GOAL),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(bars, DOWN, buff=0.55).set_x(-0.6)
        law = stack([(r"PN is the law's question: \ `but for' the exposure, \ would the harm have occurred?", WHITE),
                      (r"civil courts ask whether PN exceeds one half: \ `more probable than not'", GREY_A),
                      (r"Tian and Pearl \ (2000): \ PN is bounded by experimental and observational data together; "
                       r"\ here the lower bound is " + f"{d['pn_lower']:.2f}" + r", \ and exact", OK)],
                     font_size=20, aligned_edge=LEFT, width=12.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Rung three has practical uses. <bookmark mark='a'/>Imagine three kinds of patient: responders, who "
            "recover exactly when treated; those who recover always; and those who never do. "
            "<bookmark mark='b'/>The probability of necessity asks, of a patient who was treated and recovered: "
            "would they not have recovered without treatment? Here it is point six. <bookmark mark='c'/>The "
            "probability of sufficiency asks, of an untreated patient who did not recover: would treatment have "
            "helped? Point three seven five. <bookmark mark='d'/>The probability of being both necessary and "
            "sufficient is the share of responders, and with no defiers it equals the difference of two "
            "interventional probabilities. <bookmark mark='e'/>The probability of necessity is the law's question. "
            "But for the exposure, would the harm have occurred? Civil courts ask whether it exceeds one half. "
            "<bookmark mark='f'/>Jin Tian and Pearl showed how to bound it by combining experimental and "
            "observational data. Here the bound is tight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3))
            for mk, e in zip("bcd", eqs):
                vo.wait_until(mk)
                self.play(Write(e))
            vo.wait_until("e")
            self.play(FadeIn(law[0]), FadeIn(law[1]))
            vo.wait_until("f")
            self.play(FadeIn(law[2]))
        self.clear_scene()

    def hierarchy(self):
        head = label(r"The ladder does not collapse", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the theorem", r"Bareinboim, \ Correa, \ Ibeling and Icard \ (2022): \ for almost every model, \ "
                             r"rung-1 data leave rung-2 answers undetermined, \ and rung-2 data rung-3 answers", OK),
            (r"the cost", r"climbing needs assumptions: \ a graph to climb to rung 2, \ functional equations to "
                          r"climb to rung 3", BAD),
            (r"Pearl's critique", r"a learner fitting $P(y \mid x)$, \ however large, \ stays on the first rung", CAUSE),
            (r"the reply", r"text about the world is full of causal claims; \ a model can learn them second-hand, \ "
                           r"and experiments can be run", EFFECT),
            (r"Parts 33 and 41", r"an agent that chooses acts needs rung 2 \ (causal decision theory); \ one that "
                                 r"blames, \ regrets or judges fairness needs rung 3", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.42, width=9.0, x_text=-3.2)
        with self.voiceover(
            "Is the ladder real, or could a clever enough analysis of the lower rungs answer the upper questions? "
            "<bookmark mark='a'/>Elias Bareinboim, Juan Correa, Duligur Ibeling and Thomas Icard proved the causal "
            "hierarchy theorem: for almost every model, data from one rung leave the answers on the next rung "
            "undetermined. <bookmark mark='b'/>Climbing therefore costs assumptions: a graph to reach rung two, and "
            "functional equations, not only a graph, to reach rung three. <bookmark mark='c'/>Pearl draws a moral "
            "for machine learning: a system that only fits conditional probabilities, however large, stays on the "
            "first rung. <bookmark mark='d'/>The reply is that human text is full of causal claims, which a model "
            "can absorb second-hand, and a system that can act can also experiment. <bookmark mark='e'/>Later parts "
            "return to agents. One that chooses among acts needs rung two, as causal decision theory in Part "
            "thirty-three will show; one that regrets, assigns blame, or judges fairness needs rung three, as in "
            "Part forty-one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
