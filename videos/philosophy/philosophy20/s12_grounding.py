from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Grounding(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Grounding", r"What holds in virtue of what?", lit=(2001, 2010), part=PART)
        with self.voiceover("Chapter eleven. Grounding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.examples()
        self.graph()
        self.logic()
        self.debate()

    def examples(self):
        head = label(r"`In virtue of'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"sets", r"$\{\text{Socrates}\}$ exists because Socrates exists, \ not the other way round", ABS),
            (r"disjunctions", r"`Socrates exists or Zeus exists' is true because Socrates exists", UNIV),
            (r"truth", r"`snow is white' is true because snow is white \ (Aristotle)", OK),
            (r"wholes", r"the table exists because its particles are arranged table-wise", WHOLE),
            (r"the mental?", r"pain because of a brain state? \ the question of Part 30", NOM),
            (r"not causation", r"synchronic, \ non-causal, \ metaphysical explanation", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Some facts hold in virtue of others. <bookmark mark='a'/>The set containing Socrates exists because "
            "Socrates exists, and not the other way round. <bookmark mark='b'/>The disjunction Socrates exists or Zeus "
            "exists is true because Socrates exists. <bookmark mark='c'/>Snow is white is true because snow is white, "
            "as Aristotle noted. <bookmark mark='d'/>The table exists because its particles are arranged table-wise. "
            "<bookmark mark='e'/>Perhaps a pain exists because of a brain state, the question of Part 30. "
            "<bookmark mark='f'/>None of these is causation. The relation is simultaneous and non-causal: "
            "metaphysical explanation. Kit Fine, Jonathan Schaffer and Gideon Rosen called it grounding."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def graph(self):
        d = load("grounding")
        head = label(r"A grounding graph, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        lv = d["levels"]
        top = max(lv.values())
        by = {}
        for f, l in lv.items():
            by.setdefault(l, []).append(f)
        pos = {}
        for l, fs in by.items():
            y = -2.4 + 2.0 * l
            for k, f in enumerate(fs):
                x = -6.0 + (k + 0.5) * (8.4 / len(fs))
                pos[f] = np.array([x, y, 0])
        boxes = VGroup()
        for f, p in pos.items():
            t = label(f, font_size=13, color=OK if lv[f] == 0 else (ABS if lv[f] == 1 else WHOLE))
            if t.width > 1.6:
                t.width = 1.6
            b = SurroundingRectangle(t, buff=0.07, corner_radius=0.06, color=t.get_color(), stroke_width=1.5)
            boxes.add(VGroup(b, t).move_to(p))
        idx = {f: i for i, f in enumerate(pos)}
        arrows = VGroup(*[Arrow(boxes[idx[g]].get_top(), boxes[idx[f]].get_bottom(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.12) for g, f in d["edges"]])
        lvl = VGroup(*[label(r"level " + f"{l}", font_size=15, color=GREY_A).move_to([-6.6, -2.4 + 2.0 * l, 0])
                       for l in range(top + 1)])
        rows = stack([(r"irreflexive: \ " + (r"yes" if d["irreflexive"] else r"no"), OK if d["irreflexive"] else BAD),
                      (r"asymmetric: \ " + (r"yes" if d["asymmetric"] else r"no"), OK if d["asymmetric"] else BAD),
                      (r"transitive \ (after closure): \ " + (r"yes" if d["transitive"] else r"no"), OK),
                      (r"fundamental facts: \ " + f"{len(d['fundamental'])}", GOAL),
                      (r"add `the table grounds its particles' arrangement': \ a cycle, \ no longer an order", BAD)],
                     font_size=18, aligned_edge=LEFT, width=3.8).move_to([5.0, 0.0, 0])
        with self.voiceover(
            "Grounding is usually taken to be a strict partial order. <bookmark mark='a'/>The Reasoner builds a "
            "small graph of facts, with arrows from grounds to what they ground. Fundamental facts sit at the bottom. "
            "<bookmark mark='b'/>It checks the order: nothing grounds itself; no two facts ground each other; and "
            "grounds of grounds are grounds, once the relation is closed under chaining. "
            "<bookmark mark='c'/>Five facts are fundamental, grounded in nothing; every other fact sits at a level, "
            "the length of its longest chain down to them. <bookmark mark='d'/>Add one arrow, saying that the table "
            "grounds the arrangement of its own particles, and the order breaks: there is a cycle. "
            "<bookmark mark='e'/>Grounding is also hyperintensional: p and p-or-p are necessarily equivalent, yet p "
            "grounds p-or-p and not the reverse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lvl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.08), run_time=2)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), *[Indicate(boxes[idx[f]], color=OK) for f in d["fundamental"]])
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def debate(self):
        head = label(r"What grounding is for", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Fine \ (2001, \ 2012)", r"grounding is the notion of metaphysical explanation; \ `reality' is what is "
                                       r"fundamental", ABS),
            (r"Schaffer \ (2009)", r"`On What Grounds What': \ be permissive about what exists, \ strict about what is "
                                   r"fundamental", GOAL),
            (r"Rosen \ (2010)", r"grounding as the metaphysical analogue of entailment", UNIV),
            (r"Wilson \ (2014)", r"`No Work for a Theory of Grounding': \ specific relations \ (part, \ set "
                                 r"membership, \ realization) \ do the work; \ `big-G' grounding adds nothing", BAD),
            (r"the payoff", r"a way to state physicalism: \ every fact is grounded in the physical facts", OK),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "What is grounding for? <bookmark mark='a'/>Kit Fine treats it as the central notion of metaphysical "
            "explanation, and reality as what is fundamental. <bookmark mark='b'/>Jonathan Schaffer's slogan "
            "reverses Quine: be permissive about what exists, since numbers, tables and sets may all exist, but strict "
            "about what is fundamental. Ontology asks what grounds what. <bookmark mark='c'/>Gideon Rosen compares "
            "grounding to entailment: a metaphysical analogue of logical consequence. <bookmark mark='d'/>Jessica "
            "Wilson objects that the specific relations, parthood, set membership, realization, do all the work, and "
            "a general relation of grounding adds nothing. <bookmark mark='e'/>One payoff is a clean statement of "
            "physicalism: every fact is grounded in the physical facts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def logic(self):
        d = load("ground")
        head = label(r"A logic of ground \ (Fine, \ 2012)", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        rules = VGroup(
            MathTex(r"A \;\Rightarrow\; A \lor B", font_size=26), MathTex(r"A,\, B \;\Rightarrow\; A \land B", font_size=26),
            MathTex(r"A \;\Rightarrow\; \lnot\lnot A", font_size=26),
            MathTex(r"\lnot A \;\Rightarrow\; \lnot(A \land B)", font_size=26),
            MathTex(r"\lnot A,\, \lnot B \;\Rightarrow\; \lnot(A \lor B)", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to([-4.6, 0.2, 0])
        for r in rules:
            r.set_color(ABS)
        rl = label(r"true grounds $\Rightarrow$ what they ground", font_size=16, color=GREY_A).next_to(rules, UP,
                                                                                                 buff=0.2)
        v = d["valuation"]
        vl = label(r"valuation: \ " + ", \\ ".join(f"${k}$ " + (r"true" if b else r"false") for k, b in v.items()),
                   font_size=17, color=GREY_A).move_to([2.2, 2.3, 0])
        T = d["f1"]
        by = {}
        for i, n in enumerate(T["nodes"]):
            by.setdefault(n["depth"], []).append(i)
        pos = {}
        for dep, ids in by.items():
            for k, i in enumerate(ids):
                pos[i] = np.array([2.2 + (k - (len(ids) - 1) / 2) * 2.0, 1.3 - 1.25 * dep, 0])
        nodes = VGroup()
        for i, n in enumerate(T["nodes"]):
            m = MathTex(n["f"], font_size=28, color=OK if n["literal"] else WHITE).move_to(pos[i])
            nodes.add(m)
        arrows = VGroup(*[Arrow(nodes[a].get_top(), nodes[b].get_bottom(), buff=0.08, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.15) for a, b, _ in T["edges"]])
        rows = stack([(r"two alternative full grounds at the top: \ $p \land q$, \ or $\lnot r$", WHITE),
                      (r"the literals are fundamental: \ $" + "$, \\ $".join(T["fundamental"]) + r"$", OK),
                      (r"$p \lor p$ has $p$ as a ground twice over: \ grounding is not entailment", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=6.4).move_to([2.4, -2.6, 0])
        with self.voiceover(
            "Kit Fine gave grounding a logic, starting with truth-functions. <bookmark mark='a'/>A true disjunct "
            "grounds a disjunction. Two true conjuncts together ground a conjunction. A truth grounds its double "
            "negation. A false conjunct grounds the negation of a conjunction, and two false disjuncts together ground "
            "the negation of a disjunction. <bookmark mark='b'/>The Reasoner applies the rules to a formula under a "
            "valuation: p and q true, r false. <bookmark mark='c'/>The disjunction has two alternative full grounds, p "
            "and q together, or not r. The conjunction in turn is grounded in p and q. <bookmark mark='d'/>The "
            "unfolding stops at the literals, which are fundamental. <bookmark mark='e'/>Notice that p or p is "
            "grounded in p, twice over, though the two are logically equivalent: grounding is finer than entailment."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(vl), FadeIn(nodes[0]))
            vo.wait_until("c")
            self.play(FadeIn(nodes[1:]), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
                      FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
