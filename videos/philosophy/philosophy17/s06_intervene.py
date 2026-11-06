from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Intervene(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Causes as handles", r"What would happen if we wiggled it?", lit=(1913, 2003),
                            part=PART)
        with self.voiceover("Chapter five. Causes as handles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.russell()
        self.woodward()
        self.invariance()

    def russell(self):
        hc = history_card(1913, r"Bertrand Russell", r"`On the Notion of Cause'", width=5.4, color=HIST).to_corner(
            UL, buff=0.35)
        eq = MathTex(r"m\,\ddot{x} = F(x) \qquad\Longleftrightarrow\qquad x(t) \text{ fixes } x(t') \text{ for } t' "
                     r"< t \text{ and } t' > t", font_size=30, color=WHITE).next_to(hc, DOWN, buff=0.5).set_x(0)
        rows = stack([(r"fundamental laws are differential equations: \ symmetric, \ functional, \ no `causes'", BAD),
                      (r"they relate whole states, \ not an event to its effect", GREY_A),
                      (r"yet medicine, \ engineering and policy run on causal claims", WHITE),
                      (r"Cartwright \ (1979): \ we need causes to choose \textit{strategies}", OK)], font_size=22).next_to(
            eq, DOWN, buff=0.5)
        with self.voiceover(
            "Russell's challenge was this. <bookmark mark='a'/>The fundamental laws of physics are differential "
            "equations. They relate the state of a system at one time to its state at others, forwards and backwards "
            "alike. <bookmark mark='b'/>They mention no causes, and no asymmetry between cause and effect. "
            "<bookmark mark='c'/>Yet medicine, engineering and policy all run on causal claims. "
            "<bookmark mark='d'/>The answer that won came from Cartwright's observation: we need causal knowledge to "
            "choose strategies. Causes are what we can use to change things."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def woodward(self):
        hc = history_card(2003, r"James Woodward", r"\textit{Making Things Happen}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        pos = {"Z": [-4.8, 1.0, 0], "X": [-3.0, -0.6, 0], "Y": [-0.6, -0.6, 0]}
        g = CausalGraph(pos, [("Z", "X"), ("Z", "Y"), ("X", "Y")], colors={"X": CAUSE, "Y": EFFECT})
        I = VGroup(RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1, color=DOC, stroke_width=3),
                   label(r"$I$", font_size=22, color=DOC)).move_to([-3.0, 1.4, 0])
        I[1].move_to(I[0])
        iarr = Arrow(I.get_bottom(), g.node["X"].get_top(), buff=0.05, color=DOC, stroke_width=4)
        defs = stack([(r"$X$ causes $Y$ iff some possible intervention on $X$ would change $Y$", WHITE),
                      (r"an intervention $I$:", DOC),
                      (r"sets $X$, \ cutting every other arrow into $X$", DOC),
                      (r"affects $Y$ only through $X$", DOC),
                      (r"is not correlated with $Y$'s other causes", DOC)], font_size=21, aligned_edge=LEFT,
                     width=6.4).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "James Woodward made the idea precise. <bookmark mark='a'/>X causes Y if some possible intervention on "
            "X would change Y, or its probability. <bookmark mark='b'/>An intervention is a special kind of cause. "
            "<bookmark mark='c'/>It sets the value of X, breaking every other influence on X: here the arrow from "
            "Z is cut. <bookmark mark='d'/>It affects Y only through X, <bookmark mark='e'/>and it is independent of "
            "Y's other causes. A randomized experiment is exactly such an intervention: the coin decides the "
            "treatment, and nothing else does."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(I), GrowArrow(iarr), FadeIn(defs[1]))
            vo.wait_until("c")
            self.play(g.edge[("Z", "X")].animate.set_opacity(0.12), FadeIn(defs[2]))
            vo.wait_until("d")
            self.play(FadeIn(defs[3]))
            vo.wait_until("e")
            self.play(FadeIn(defs[4]))
        self.clear_scene()

    def invariance(self):
        head = label(r"Invariance, \ and an old worry", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"invariance", r"a causal generalization stays true when we intervene on its variables: \ Ohm's law "
                            r"survives setting the voltage; \ the barometer-storm link does not", OK),
            (r"explanation", r"to explain is to say what would have happened had things been different", EFFECT),
            (r"manipulability", r"Collingwood \ (1940), \ von Wright \ (1971), \ Menzies and Price \ (1993)", GREY_A),
            (r"the worry", r"no one can manipulate an earthquake: \ is causation anthropocentric?", BAD),
            (r"the reply", r"\textit{possible} interventions, \ not human ones: \ what would happen if the plate "
                           r"were moved", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.4)
        with self.voiceover(
            "Two further ideas complete the picture. <bookmark mark='a'/>Invariance: a causal generalization stays "
            "true when we intervene on its variables. Ohm's law survives our setting the voltage; the link between "
            "barometer and storm does not survive our setting the barometer. <bookmark mark='b'/>And explanation: to "
            "explain an event is to say what would have happened had things been different. "
            "<bookmark mark='c'/>The view descends from the manipulability theories of Collingwood, von Wright, and "
            "Peter Menzies and Huw Price. <bookmark mark='d'/>The old worry is that it makes causation "
            "anthropocentric: no one can manipulate an earthquake. <bookmark mark='e'/>Woodward's reply is that "
            "the definition uses possible interventions, not human ones: what would happen if the tectonic plate "
            "were moved, by anything at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
