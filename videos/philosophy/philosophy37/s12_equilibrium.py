from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Equilibrium(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Reflective equilibrium", r"How should principles and judgments correct each other?",
                            lit=(1955, 1971), part=PART)
        with self.voiceover("Chapter eleven. Reflective equilibrium."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.method()
        self.network()
        self.shift()
        self.singer()
        self.progress()

    def method(self):
        head = label(r"The method", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Goodman \ (1955)", r"rules of inference and particular inferences are justified by being brought "
                                      r"into agreement with each other", IS),
                (r"Rawls \ (1971)", r"adjust principles and considered judgments, \ each against the other, \ until "
                                    r"they cohere: \ reflective equilibrium", REAL),
                (r"wide \ (Daniels, \ 1979)", r"bring in background theories too: \ of persons, \ of society, \ of "
                                              r"human nature", OUGHT),
                (r"built here", r"weighted commitments and the links between them; \ keep the heaviest consistent "
                                r"set: \ weighted MaxSAT, \ with Part 2's solver", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Whatever moral claims are, we have to decide which ones to believe. <bookmark mark='a'/>Nelson Goodman "
            "suggested in 1955 that rules of inference and particular inferences are justified by being brought into "
            "agreement with each other. <bookmark mark='b'/>John Rawls applied the idea to ethics in 1971: adjust "
            "principles and considered judgments, each against the other, until they cohere. He called the result "
            "reflective equilibrium. <bookmark mark='c'/>Norman Daniels's wide version, of 1979, brings in background "
            "theories too, of persons, society and human nature. <bookmark mark='d'/>The Reasoner builds it as an "
            "optimization: weighted commitments, logical links between them, and the heaviest set that is "
            "consistent, found with the satisfiability solver of Part 2. Computer scientists call this problem weighted "
            "MaxSAT."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def _net(self, d, keep):
        com = {k: (kind, text, w) for k, kind, text, w in load("equilibrium")["commitments"]}
        pos = {"U": [-4.6, 1.3, 0], "D": [-4.6, -0.9, 0], "DDE": [-1.6, 2.2, 0], "S": [-0.4, 0.4, 0],
               "F": [-1.8, -1.6, 0], "H": [1.0, -1.7, 0]}
        nodes, labels = {}, VGroup()
        for k, (kind, text, w) in com.items():
            col = REAL if kind == "principle" else OUGHT
            c = Circle(radius=0.34 + 0.05 * w, color=col, stroke_width=3, fill_color=col,
                       fill_opacity=0.25 if k in keep else 0.05).move_to(pos[k])
            nodes[k] = c
            labels.add(VGroup(label(k, font_size=20, color=col).move_to(c),
                              label(f"{w}", font_size=15, color=GREY_A).next_to(c, DR, buff=0.0)))
        edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), color=BAD, stroke_width=2,
                              stroke_opacity=0.7, buff=0.42) for a, b in d["conflicts"]])
        return nodes, labels, edges

    def network(self):
        e = load("equilibrium")
        d = e["base"]
        head = label(r"Six commitments, \ in conflict", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["keep"] == ["DDE", "S", "F", "H"] and d["drop"] == ["U", "D"] and d["weight"] == 16
        assert d["ties"] == [["DDE", "S", "F", "H"]] and len(d["conflicts"]) == 6
        nodes, labels, edges = self._net(d, keep=set(d["keep"]) | {"U", "D"})
        legend = stack([(r"U: \ maximize total welfare \ (3)", REAL), (r"D: \ never kill an innocent to save more \ (3)",
                                                                     REAL),
                        (r"DDE: \ double effect \ (2)", REAL), (r"S: \ switching is permitted \ (4)", OUGHT),
                        (r"F: \ pushing is forbidden \ (5)", OUGHT), (r"H: \ the surgeon may not harvest \ (5)", OUGHT),
                        (r"red: \ the pairs that cannot both be kept, \ given what each principle implies", BAD)],
                       font_size=17, aligned_edge=LEFT, buff=0.16).move_to([4.4, 0.2, 0])
        drop = VGroup(*[Cross(nodes[k], stroke_color=BAD, stroke_width=4, scale_factor=0.8) for k in d["drop"]])
        res = label(r"the heaviest consistent set: \ DDE, \ S, \ F, \ H: \ weight 16 of 22", font_size=19,
                    color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a small equilibrium problem, from Part 35's trolleys. <bookmark mark='a'/>Three principles: "
            "maximize total welfare; never kill an innocent, even to save more; and the doctrine of double effect. "
            "Three judgments: switching is permitted; pushing the man is forbidden; the surgeon may not harvest one "
            "patient's organs for five. Each has a weight: how confident we are. <bookmark mark='b'/>The links say "
            "what each principle implies about the cases, and the red lines join the pairs that cannot both be kept: "
            "six conflicts. <bookmark mark='c'/>The Reasoner checks all sixty four subsets for consistency. The "
            "heaviest consistent set drops both absolute principles and keeps double effect with all three "
            "judgments: weight sixteen out of twenty two, and no ties. <bookmark mark='d'/>The equilibrium says "
            "that our confident judgments outweigh both simple principles, and that only a principle with structure, "
            "like double effect, fits them all."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], FadeIn(labels))
            vo.wait_until("a")
            self.play(FadeIn(legend[:6]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in edges], lag_ratio=0.2), FadeIn(legend[6]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in drop], lag_ratio=0.3), FadeIn(res))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def shift(self):
        e = load("equilibrium")
        g = e["greene"]
        head = label(r"Change the weights, \ and the equilibrium moves", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert g["weights"]["F"] == 1 and g["weights"]["H"] == 2 and g["weights"]["U"] == 6
        assert g["keep"] == ["U", "S"] and g["weight"] == 10 and g["ties"] == [["U", "S"]]
        nodes, labels, edges = self._net(g, keep=set(g["keep"]))
        for k, n in nodes.items():
            r = 0.34 + 0.05 * g["weights"][k]
            n.scale_to_fit_width(2 * r)
            labels[list(nodes).index(k)][1].become(label(f"{g['weights'][k]}", font_size=15, color=GREY_A).next_to(
                n, DR, buff=0.0))
        drop = VGroup(*[Cross(nodes[k], stroke_color=BAD, stroke_width=4, scale_factor=0.8) for k in g["drop"]])
        side = stack([(r"after Greene's argument: \ footbridge 5 $\to$ 1, \ surgeon 5 $\to$ 2, \ welfare 3 $\to$ 6",
                       MIND),
                      (r"now the heaviest consistent set is U and S: \ weight 10", GOAL),
                      (r"equilibrium is only as good as its weights: \ the method cannot supply them", BAD),
                      (r"Kelly and McGrath \ (2010): \ is reflective equilibrium enough for justification?", GREY_A)],
                     font_size=18, aligned_edge=LEFT, width=5.0, buff=0.3).move_to([4.3, -0.2, 0])
        with self.voiceover(
            "Now change the weights, as Greene's argument from the last chapter urges. <bookmark mark='a'/>Suppose our "
            "confidence in the footbridge verdict falls from five to one, in the surgeon verdict from five to two, "
            "and in the principle of welfare rises from three to six. <bookmark mark='b'/>The heaviest consistent set "
            "is now just two commitments: maximize welfare, and switching is permitted, with weight ten. "
            "<bookmark mark='c'/>So the method's verdict is only as good as its weights, and the method itself cannot "
            "supply them. <bookmark mark='d'/>Thomas Kelly and Sarah McGrath asked in 2010 whether reflective "
            "equilibrium is enough for justification at all, or only for consistency. That question sends us back to "
            "the metaethics of the whole part."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], FadeIn(labels), FadeIn(edges))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in drop], lag_ratio=0.2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def singer(self):
        head = label(r"Against equilibrium \ (Singer, \ 1974)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the worry", r"considered judgments may be the residue of discarded religion, \ class interest and evolutionary history", BAD),
                (r"the alternative", r"Sidgwick's way: \ start from a few self-evident axioms, \ and let them overrule the cases", REAL),
                (r"the reply", r"axioms are judgments too, \ and chosen by the same minds: \ coherence is all any method has", EXPR),
                (r"in the Reasoner", r"the weights are where this argument lives: \ debunking lowers some weights, \ self-evidence raises others", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Peter Singer attacked the method in 1974. <bookmark mark='a'/>Our considered judgments, he argued, may "
            "be the residue of discarded religion, of class interest and of evolutionary history; why give them any "
            "weight? <bookmark mark='b'/>He preferred Sidgwick's way: start from a few self-evident axioms, such as "
            "that the good of one person counts as much as the equal good of another, and let them overrule the "
            "cases. <bookmark mark='c'/>Defenders reply that axioms are judgments too, made by the same minds, so "
            "coherence is all that any method has. <bookmark mark='d'/>In the Reasoner's model, this whole argument "
            "lives in the weights: debunking lowers some, claims of self-evidence raise others."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def progress(self):
        head = label(r"What would moral progress be?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"realism", r"getting closer to the moral truth, \ as science gets closer to the physical truth", REAL),
                (r"expressivism", r"change our improved attitudes endorse: \ progress by our own lights, \ which is "
                                  r"all the quasi-realist says any progress is", EXPR),
                (r"constructivism", r"better outputs of the right procedure, \ or a more coherent valuing point of "
                                    r"view", OUGHT),
                (r"error theory", r"no progress in truth; \ perhaps progress in usefulness", ANTI),
                (r"the cases", r"abolition, \ the widening circle of concern: \ every view must say why they are not "
                               r"mere change", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.42, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "A last test for each view: what would moral progress be? <bookmark mark='a'/>For the realist, getting "
            "closer to the moral truth, as science gets closer to the physical truth. <bookmark mark='b'/>For the "
            "expressivist, change that our improved attitudes endorse: progress by our own lights, which, the "
            "quasi-realist says, is all that progress anywhere ever was. <bookmark mark='c'/>For the constructivist, "
            "better outputs of the right procedure, or a more coherent valuing point of view. "
            "<bookmark mark='d'/>For the error theorist, no progress in truth; perhaps progress in usefulness. "
            "<bookmark mark='e'/>And every view must explain the cases that seem most clearly to be progress, like "
            "the abolition of slavery and the widening circle of concern, as more than mere change."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
