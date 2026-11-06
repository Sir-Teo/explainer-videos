from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

RULES = [("Reflexivity", r"A \mathrel{|\!\sim} A"),
         ("And", r"A \mathrel{|\!\sim} B,\ A \mathrel{|\!\sim} C \ / \ A \mathrel{|\!\sim} B \land C"),
         ("Or", r"A \mathrel{|\!\sim} C,\ B \mathrel{|\!\sim} C \ / \ A \lor B \mathrel{|\!\sim} C"),
         ("Cautious Monotonicity", r"A \mathrel{|\!\sim} B,\ A \mathrel{|\!\sim} C \ / \ A \land B \mathrel{|\!\sim} C"),
         ("Cut", r"A \land B \mathrel{|\!\sim} C,\ A \mathrel{|\!\sim} B \ / \ A \mathrel{|\!\sim} C"),
         ("Rational Monotonicity", r"A \mathrel{|\!\sim} C,\ A \mathrel{|\!\not\sim} \lnot B \ / \ A \land B "
                                   r"\mathrel{|\!\sim} C"),
         ("Monotonicity", r"A \mathrel{|\!\sim} C \ / \ A \land B \mathrel{|\!\sim} C")]


class KLM(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The logic of normality", r"Which rules does defeasible inference obey?",
                            lit=(1990,), part=PART)
        with self.voiceover("Chapter eleven. The logic of normality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.preferential()
        self.rules()
        self.epsilon()
        self.systemz()
        self.unity()

    def preferential(self):
        hc = history_card(1990, r"Kraus, \ Lehmann \ and Magidor", r"`Nonmonotonic Reasoning, Preferential Models "
                                                                   r"and Cumulative Logics'", width=7.4,
                          color=HIST).to_corner(UL, buff=0.35)
        defn = MathTex(r"A \mathrel{|\!\sim} B \iff B \text{ holds in the most normal } A\text{-worlds}", font_size=34,
                       color=NEW).next_to(hc, DOWN, buff=0.5).set_x(0)
        rank = {"b f ~p": 0, "b ~f p": 1, "b f p": 2}
        sp = SphereView({"bf": 0, "b~fp": 1, "bfp": 2}, center=[-3.4, -1.6, 0], step=0.75, font_size=18,
                        names={"bf": r"\text{bird, flies}", "b~fp": r"\text{penguin, can't}",
                               "bfp": r"\text{flying penguin}"})
        del rank
        rows = stack([
            (r"a preferential model: \ worlds ordered by normality", WHITE),
            (r"bird $\mathrel{|\!\sim}$ flies: \ the most normal bird-world flies", OK),
            (r"penguin $\mathrel{|\!\sim}$ $\lnot$flies: \ the most normal penguin-world doesn't", OK),
            (r"the same picture as Grove's spheres", BEL),
        ], font_size=22, aligned_edge=LEFT, width=6.6).move_to([3.3, -1.5, 0])
        with self.voiceover(
            "Sarit Kraus, Daniel Lehmann and Menachem Magidor asked what all reasonable defeasible inference has in "
            "common. <bookmark mark='a'/>Their semantics: A defeasibly implies B when B holds in the most normal "
            "A-worlds. <bookmark mark='b'/>A preferential model orders the worlds by normality. "
            "<bookmark mark='c'/>The most normal bird-worlds have flying birds, so bird defeasibly implies flies. "
            "<bookmark mark='d'/>The most normal penguin-worlds have flightless penguins. <bookmark mark='e'/>It is "
            "Grove's picture of spheres again."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(defn))
            vo.wait_until("b")
            self.play(FadeIn(sp), FadeIn(rows[0]))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rules(self):
        d = load("systemz")
        head = label(r"System P, \ and rational monotonicity, \ checked", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        hd = [label(r"rule", font_size=21, color=P.CLAIM), label(r"form", font_size=21, color=P.CLAIM),
              label(r"ranked", font_size=21, color=P.CLAIM), label(r"preferential", font_size=21, color=P.CLAIM)]
        rows = []
        for name, form in RULES:
            rk = True if name == "Reflexivity" else d["klm"]["ranked"][name]
            pf = True if name == "Reflexivity" else d["klm"]["preferential"][name]
            rows.append([label(name, font_size=20, color=BAD if name == "Monotonicity" else WHITE),
                         MathTex(form, font_size=22), mark(rk, 24), mark(pf, 24)])
        grid = ValueGrid(hd, rows, col_w=[3.6, 6.2, 1.5, 2.0], cell_h=0.55, font_size=20).next_to(head, DOWN,
                                                                                               buff=0.35)
        notes = stack([(r"System P: \ the core every preferential model obeys", OK),
                       (r"ranked models add rational monotonicity \ (Lehmann and Magidor, \ 1992)", BEL),
                       (r"no model obeys monotonicity: \ that is the point", BAD)], font_size=21,
                      width=12.4).next_to(grid, DOWN, buff=0.3)
        with self.voiceover(
            "From that semantics come the rules. <bookmark mark='a'/>The Reasoner checks them on two small models, "
            "one ranked, where normality comes in levels, and one merely preferential, where some worlds are "
            "incomparable. <bookmark mark='b'/>Reflexivity, And, Or, Cautious Monotonicity and Cut hold in both. "
            "Together they make System P, the core of defeasible inference. <bookmark mark='c'/>Rational "
            "monotonicity, which says you may keep a conclusion when you learn something you didn't expect to be "
            "false, holds in the ranked model and fails in the preferential one. <bookmark mark='d'/>And plain "
            "monotonicity fails in both, as it should."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(len(rows)):
                self.play(FadeIn(grid.cell[r][0]), FadeIn(grid.cell[r][1]), run_time=0.4)
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(5) for c in (2, 3)], FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[5][c]) for c in (2, 3)], FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[6][c]) for c in (2, 3)], FadeIn(notes[2]))
        self.clear_scene()

    def epsilon(self):
        hc = history_card(1975, r"Ernest Adams", r"\textit{The Logic of Conditionals}", width=4.8,
                          color=HIST).to_corner(UL, buff=0.35)
        defn = MathTex(r"A \Rightarrow B \ \text{ means } \ P(B \mid A) \geq 1 - \varepsilon", font_size=36,
                       color=NEW).next_to(hc, DOWN, buff=0.5).set_x(0)
        rows = stack([
            (r"a default is a high conditional probability", WHITE),
            (r"p-entailment: \ as the premises' probabilities approach 1, \ so must the conclusion's", BEL),
            (r"Adams's p-valid rules \ $=$ \ System P \ (Pearl and Geffner)", OK),
            (r"monotonicity fails: \ $P(\text{flies} \mid \text{bird})$ high, \ "
             r"$P(\text{flies} \mid \text{bird} \land \text{penguin})$ low", BAD),
            (r"the probabilities of Part 13 \ and the orderings of this part \ give the same logic", GOAL),
        ], font_size=23, buff=0.3, width=12.4).next_to(defn, DOWN, buff=0.5)
        with self.voiceover(
            "System P has a second, probabilistic, foundation. <bookmark mark='a'/>Ernest Adams read a default, A "
            "normally B, as: the probability of B given A is close to one. <bookmark mark='b'/>A conclusion "
            "follows, in his sense, if its probability can be made as close to one as you like by making the "
            "premises' probabilities close enough to one. <bookmark mark='c'/>Judea Pearl and Hector Geffner showed "
            "that the rules Adams's semantics validates are exactly System P. <bookmark mark='d'/>Monotonicity fails, "
            "as it should: flies is likely given bird, and unlikely given bird and penguin. "
            "<bookmark mark='e'/>The probabilities of Part 13 and the orderings of this part arrive at the same logic "
            "of normality."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(defn))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                if mk == "b":
                    self.play(FadeIn(rows[0]))
                self.play(FadeIn(r))
        self.clear_scene()

    def systemz(self):
        d = load("systemz")["penguins"]
        hc = history_card(1990, r"Judea Pearl", r"System Z", width=3.8, color=HIST).to_corner(UL, buff=0.35)
        dnames = {("b", "f"): r"birds fly", ("p", "b"): r"penguins are birds", ("p", "~f"): r"penguins don't fly",
                  ("b", "w"): r"birds have wings"}
        layers = VGroup()
        for k, layer in enumerate(d["layers"]):
            g = VGroup(label(rf"layer {k}", font_size=22, color=BEL),
                       *[label(dnames[tuple(d["defaults"][i])], font_size=21) for i in layer]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12)
            layers.add(g)
        layers.arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(hc, DOWN, buff=0.4).set_x(-2.2)
        expl = label(r"layer 0: \ tolerated by all; \ layer 1: \ only once layer 0 is set aside", font_size=19,
                     color=GREY_A).next_to(layers, DOWN, buff=0.2)
        qtex = {("b", "f"): r"bird $\mathrel{|\!\sim}$ flies", ("p", "~f"): r"penguin $\mathrel{|\!\sim}$ $\lnot$flies",
                ("p", "b"): r"penguin $\mathrel{|\!\sim}$ bird", ("b & r", "f"): r"red bird $\mathrel{|\!\sim}$ flies",
                ("p", "w"): r"penguin $\mathrel{|\!\sim}$ wings", ("p", "~w"): r"penguin $\mathrel{|\!\sim}$ $\lnot$wings"}
        qs = VGroup(*[VGroup(label(qtex[(q["a"], q["b"])], font_size=22), mark(q["holds"], 24)).arrange(RIGHT,
                                                                                                         buff=0.3)
                      for q in d["queries"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -0.3, 0])
        foot = stack([(r"the drowning problem: \ the penguin's exceptional flight drowns its normal wings", BAD),
                      (r"lexicographic closure \ (Lehmann, \ 1995) \ counts violated defaults, \ and recovers them",
                       GREY_A)], font_size=21, width=12.4).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Which defeasible conclusions follow from a set of defaults? Judea Pearl's System Z gives a canonical "
            "answer, the same as Lehmann and Magidor's rational closure. <bookmark mark='a'/>Sort the defaults into "
            "layers. Birds fly, and birds have wings, can be satisfied together with everything else: layer zero. "
            "Penguins are birds, and penguins don't fly, can be satisfied only once those are set aside: layer one. "
            "<bookmark mark='b'/>Then rank each world by the highest layer it violates, and read off conclusions from "
            "the most normal worlds. <bookmark mark='c'/>The Reasoner's answers: birds fly; penguins don't; penguins "
            "are birds; red birds fly, since redness is irrelevant. <bookmark mark='d'/>But do penguins have wings? "
            "System Z doesn't say. The penguin is exceptional in one respect, and the exception drowns the other "
            "inheritance. This is the drowning problem. <bookmark mark='e'/>Lehmann's lexicographic closure, which "
            "counts violated defaults instead of just their highest layer, gets the wings back."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in layers], lag_ratio=0.5), FadeIn(expl))
            vo.wait_until("b")
            self.play(Indicate(layers, color=BEL, scale_factor=1.02))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(q) for q in qs[:4]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(qs[4]), FadeIn(qs[5]), FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def unity(self):
        head = label(r"One structure, \ three subjects", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"A \mathrel{|\!\sim} B \iff B \in K * A \iff A > B \in K", font_size=40, color=NEW).next_to(
            head, DOWN, buff=0.6)
        rows = stack([
            (r"defeasible inference \ (KLM)", WHITE),
            (r"belief revision \ (AGM)", WHITE),
            (r"conditionals \ (the Ramsey test)", WHITE),
            (r"Makinson and Gärdenfors \ (1991): \ the rational consequence relations are the AGM revisions", GOAL),
            (r"and one ordering of worlds, \ spheres or ranks, \ underlies all three", BEL),
        ], font_size=25, buff=0.32, width=12.4).next_to(eq, DOWN, buff=0.55)
        with self.voiceover(
            "Step back. <bookmark mark='a'/>A defeasibly implies B, B is in the revision of K by A, and K believes if "
            "A then B: <bookmark mark='b'/>three subjects, defeasible inference, <bookmark mark='c'/>belief "
            "revision, <bookmark mark='d'/>and conditionals. <bookmark mark='e'/>David Makinson and Peter Gärdenfors "
            "showed in 1991 that the first two are one theory seen from two sides: the rational consequence relations "
            "are exactly the AGM revisions of a fixed belief set. <bookmark mark='f'/>One ordering of worlds, drawn as "
            "spheres or written as ranks, underlies all three, and Gärdenfors's theorem marks the one place where "
            "they cannot be fully merged."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
