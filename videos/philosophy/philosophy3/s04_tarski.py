from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Tarski(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Truth in a structure", r"What makes a sentence with `all' true?", lit=(1933,),
                            part=PART)
        with self.voiceover("Chapter three. Truth in a structure."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.convention()
        self.structure()
        self.clauses()
        self.forall_exists()
        self.exists_forall()
        self.counting()
        self.validity()

    def convention(self):
        hc = history_card(1933, r"Alfred Tarski, Warsaw", r"`The concept of truth in formalized languages'",
                          width=6.0, color=HIST).to_corner(UL, buff=0.4)
        t = VGroup(label(r"Convention T:", font_size=28, color=GOAL),
                   label(r"`Snow is white' is true \ if and only if \ snow is white.", font_size=34)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, 0.2, 0])
        lv = VGroup(label(r"object language: \ the sentence in quotes", font_size=24, color=P.CLAIM),
                    label(r"metalanguage: \ the language we use to talk about it", font_size=24, color=P.AGENT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "In 1933 Alfred Tarski, in Warsaw, published a long paper on the concept of truth in formalized "
            "languages. <bookmark mark='a'/>It begins from a platitude. 'Snow is white' is true if and only if snow "
            "is white. Any adequate definition of truth, Tarski said, must yield every sentence of this form. "
            "<bookmark mark='b'/>Notice the two levels. The sentence in quotation marks belongs to the language we "
            "are talking about, the object language. The sentence after 'if and only if' belongs to the language we "
            "are talking in, the metalanguage. Tarski's achievement was to define truth for a formal language, "
            "recursively, inside a metalanguage, and his definition is the one every logic textbook still uses."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(lv))
        self.clear_scene()

    def graph(self, center=(-3.4, -0.4, 0)):
        d = load("love")
        names = d["people"]
        g = relation_graph(names, [tuple(p) for p in d["loves"]], radius=1.9, center=center)
        return d, g

    def structure(self):
        d, g = self.graph()
        dom = MathTex(r"D = \{\mathrm{Ann}, \mathrm{Bo}, \mathrm{Cy}, \mathrm{Di}\}", font_size=36, color=OBJ)
        rel = MathTex(r"\mathrm{L}^{\mathcal{M}} = \{(\mathrm{Ann},\mathrm{Bo}), (\mathrm{Bo},\mathrm{Cy}), "
                      r"(\mathrm{Cy},\mathrm{Ann}), (\mathrm{Di},\mathrm{Cy})\}", font_size=30, color=REL)
        defn = definition_card(r"structure $\mathcal{M}$", r"a non-empty domain $D$ of objects, and for each "
                               r"relation symbol a relation on $D$ (and an object for each constant, a function for "
                               r"each function symbol)", width=6.2, font_size=22, color=OBJ)
        right = VGroup(defn, dom, rel).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.3, 0.2, 0])
        if right.get_right()[0] > 6.9:
            right.shift(LEFT * (right.get_right()[0] - 6.9))
        with self.voiceover(
            "Truth for a first-order sentence is truth in a structure. <bookmark mark='a'/>A structure is a "
            "non-empty collection of objects, the domain, together with an interpretation: for each relation symbol, "
            "which objects stand in that relation. <bookmark mark='b'/>Here is a small one. Four people, Ann, Bo, Cy "
            "and Di. <bookmark mark='c'/>And one relation, loves, drawn as arrows: Ann loves Bo, Bo loves Cy, Cy "
            "loves Ann, and Di loves Cy. Notice that nobody's love is returned."
        ) as vo:
            self.play(FadeIn(defn))
            vo.wait_until("a")
            self.play(Indicate(defn, color=P.CLAIM))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n, scale=0.8) for n in g.nodes], lag_ratio=0.2), Write(dom))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in g.arrows], lag_ratio=0.3), Write(rel))
        self.wait(0.5)
        self.clear_scene()

    def clauses(self):
        head = label(r"Tarski's clauses: \ $\mathcal{M}, g \models \varphi$, \ `$\varphi$ is true in $\mathcal{M}$ "
                     r"when the variables are assigned by $g$'", font_size=26, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            MathTex(r"\mathcal{M}, g \models \mathrm{L}(x, y)", r"\iff", r"(g(x), g(y)) \in \mathrm{L}^{\mathcal{M}}"),
            MathTex(r"\mathcal{M}, g \models \lnot \varphi", r"\iff", r"\mathcal{M}, g \not\models \varphi"),
            MathTex(r"\mathcal{M}, g \models \varphi \land \psi", r"\iff",
                    r"\mathcal{M}, g \models \varphi \text{ and } \mathcal{M}, g \models \psi"),
            MathTex(r"\mathcal{M}, g \models \forall x\, \varphi", r"\iff",
                    r"\text{for every } d \in D:\ \mathcal{M}, g[x \mapsto d] \models \varphi"),
            MathTex(r"\mathcal{M}, g \models \exists x\, \varphi", r"\iff",
                    r"\text{for some } d \in D:\ \mathcal{M}, g[x \mapsto d] \models \varphi"))
        for r in rows:
            r.scale(0.8)
            r[0].set_color(WHITE)
            r[2].set_color(GREY_A)
        rows[3][0].set_color(QUANT)
        rows[4][0].set_color(QUANT)
        rows.arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        x0 = max(r[1].get_x() for r in rows)
        for r in rows:
            r.shift(RIGHT * (x0 - r[1].get_x()))
        note_ = label(r"$g[x \mapsto d]$: \ the same assignment, except that $x$ now names $d$", font_size=24,
                      color=VAR).to_edge(DOWN, buff=0.9)
        rec = label(r"each clause uses only smaller formulas: \ a definition by recursion, like Part 2's tree "
                    r"evaluation", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the definition. Because formulas may have free variables, Tarski defines truth relative to an "
            "assignment, which says what object each variable names. <bookmark mark='a'/>An atomic formula is true "
            "when the objects its terms name stand in the relation. <bookmark mark='b'/>Negation and conjunction work "
            "exactly as in Part 2. <bookmark mark='c'/>And the new clauses: 'for all x, phi' is true when phi is true "
            "however we reassign x to an object of the domain, every single one. <bookmark mark='d'/>'There exists "
            "an x' is true when at least one reassignment works. <bookmark mark='e'/>Every clause refers only to "
            "smaller formulas, so this is a definition by recursion, exactly like evaluating a formula tree from the "
            "leaves up. The difference is that a quantifier node now asks a question about every object in the "
            "domain."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rec))
        self.clear_scene()

    def forall_exists(self):
        d, g = self.graph()
        names = d["people"]
        f = MathTex(r"\forall x", r"\, \exists y", r"\ \mathrm{L}(x, y)", font_size=44).move_to([3.3, 2.6, 0])
        f[0].set_color(QUANT)
        f[1].set_color(QUANT)
        gl = label(r"`everyone loves someone'", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.15)
        rows = VGroup()
        for x in range(4):
            y = d["witness"][str(x)]
            rows.add(MathTex(rf"x = \mathrm{{{names[x]}}}:", rf"\ \ y = \mathrm{{{names[y]}}}", r"\ \checkmark",
                             font_size=32))
            rows[-1][0].set_color(VAR)
            rows[-1][2].set_color(OK)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(gl, DOWN, buff=0.45)
        verdict = label(r"every $x$ has a witness: \ \textbf{true}", font_size=30, color=OK).next_to(rows, DOWN,
                                                                                                buff=0.45)
        self.add(g)
        with self.voiceover(
            "Now evaluate 'for every x there is a y such that x loves y' on our four people. <bookmark mark='a'/>The "
            "outer quantifier says: go through every choice of x. <bookmark mark='x0'/>x is Ann. Is there a y she "
            "loves? Yes, Bo. <bookmark mark='x1'/>x is Bo: he loves Cy. <bookmark mark='x2'/>x is Cy: she loves Ann. "
            "<bookmark mark='x3'/>x is Di: she loves Cy. <bookmark mark='b'/>Every choice of x found a witness, so the "
            "sentence is true in this structure. Notice that the witness depends on x: for Ann it is Bo, for Cy it is "
            "Ann."
        ) as vo:
            self.play(Write(f), FadeIn(gl))
            vo.wait_until("a")
            self.play(Indicate(f[0], color=QUANT))
            for x in range(4):
                vo.wait_until(f"x{x}")
                y = d["witness"][str(x)]
                ar = g.amap[(x, y)]
                self.play(g.nodes[x][0].animate.set_stroke(VAR, width=6), FadeIn(rows[x][0]), run_time=0.6)
                self.play(ar.animate.set_color(GOAL).set_stroke(width=6), g.nodes[y][0].animate.set_fill(GOAL, 0.35),
                          FadeIn(rows[x][1:]), run_time=0.8)
                self.play(g.nodes[x][0].animate.set_stroke(OBJ, width=2.5), g.nodes[y][0].animate.set_fill(
                    "#0B0F17", 1), ar.animate.set_color(OK).set_stroke(width=3), run_time=0.4)
            vo.wait_until("b")
            self.play(FadeIn(verdict, shift=UP * 0.2))
        self.clear_scene()

    def exists_forall(self):
        d, g = self.graph()
        names = d["people"]
        f = MathTex(r"\exists y", r"\, \forall x", r"\ \mathrm{L}(x, y)", font_size=44).move_to([3.3, 2.6, 0])
        f[0].set_color(QUANT)
        f[1].set_color(QUANT)
        gl = label(r"`someone is loved by everyone'", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.15)
        loves = {tuple(p) for p in d["loves"]}
        rows = VGroup()
        for y in range(4):
            by = [names[x] for x in range(4) if (x, y) in loves]
            who = r",\ ".join(rf"\mathrm{{{n}}}" for n in by) if by else r"\text{nobody}"
            rows.add(MathTex(rf"y = \mathrm{{{names[y]}}}:", rf"\ \ \text{{loved by }} {who}", r"\ \times",
                             font_size=30))
            rows[-1][0].set_color(VAR)
            rows[-1][2].set_color(BAD)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(gl, DOWN, buff=0.45)
        verdict = label(r"no $y$ is loved by all four: \ \textbf{false}", font_size=30, color=BAD).next_to(
            rows, DOWN, buff=0.45)
        assert d["loved_by_all"] == []
        self.add(g)
        with self.voiceover(
            "Swap the quantifiers: there is a y such that every x loves y. <bookmark mark='a'/>Now the outer choice is "
            "y, and it must work for every x at once. <bookmark mark='y0'/>y is Ann: only Cy loves her. "
            "<bookmark mark='y1'/>y is Bo: only Ann. <bookmark mark='y2'/>y is Cy: Bo and Di, but not Ann, and not "
            "Cy herself. <bookmark mark='y3'/>y is Di: nobody at all. <bookmark mark='b'/>No choice survives, so this "
            "sentence is false here. Same words, same relation, a different order of quantifiers, and a different "
            "truth value."
        ) as vo:
            self.play(Write(f), FadeIn(gl))
            vo.wait_until("a")
            self.play(Indicate(f[0], color=QUANT))
            for y in range(4):
                vo.wait_until(f"y{y}")
                into = [g.amap[(x, y)] for x in range(4) if (x, y) in loves]
                self.play(g.nodes[y][0].animate.set_stroke(VAR, width=6), FadeIn(rows[y][:2]),
                          *[a.animate.set_color(GOAL).set_stroke(width=6) for a in into], run_time=0.8)
                self.play(FadeIn(rows[y][2]), run_time=0.4)
                self.play(g.nodes[y][0].animate.set_stroke(OBJ, width=2.5),
                          *[a.animate.set_color(REL).set_stroke(width=3) for a in into], run_time=0.4)
            vo.wait_until("b")
            self.play(FadeIn(verdict, shift=UP * 0.2))
        self.clear_scene()

    def counting(self):
        d = load("love")
        n, R = d["n"], d["relations"]
        head = label(rf"Every possible `loves' among {n} people: \ $2^{{{n * n}}} = {R}$ structures", font_size=32,
                     color=CONN).to_edge(UP, buff=0.5)
        bars = bar_row([d["count_ae"], d["count_ea"]], [r"$\forall x\, \exists y\ \mathrm{L}(x, y)$ true",
                                                       r"$\exists y\, \forall x\ \mathrm{L}(x, y)$ true"],
                       [P.CLAIM, P.AGENT], width=6.0, height=0.5, font_size=26, vmax=R).move_to([0, 1.0, 0])
        assert d["count_ae"] == 7 ** 3 and d["count_ea"] == R - 7 ** 3 and d["count_both"] == d["count_ea"]
        why = VGroup(
            MathTex(r"343 = 7^3", font_size=34, color=P.CLAIM),
            label(r"each person loves a non-empty set of the 3: \ $2^3 - 1 = 7$ ways each", font_size=24,
                  color=GREY_A),
            MathTex(r"169 = 512 - 7^3", font_size=34, color=P.AGENT),
            label(r"switch every arrow on or off and reverse it: \ `no one is loved by all' becomes `everyone loves "
                  r"someone'", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        why.next_to(bars, DOWN, buff=0.6)
        imp = label(rf"in all {d['count_ea']} structures where the second is true, so is the first: \ checked one "
                    r"by one", font_size=26, color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How different are the two sentences? With three people there are nine possible arrows, so two to the "
            f"nine, {R}, possible love relations. The Reasoner checked both sentences on all of them. "
            f"<bookmark mark='a'/>'Everyone loves someone' is true in {d['count_ae']}. 'Someone is loved by "
            f"everyone' is true in only {d['count_ea']}. <bookmark mark='b'/>Both numbers have a reason. "
            "Three hundred and forty-three is seven cubed: each person must love some non-empty set of the three "
            "people, and there are seven of those. <bookmark mark='c'/>And one hundred and sixty-nine is five hundred "
            "and twelve minus seven cubed: switch every arrow on or off and reverse it, and 'no one is loved by "
            "everyone' turns into 'everyone loves someone', so the two are counted alike. <bookmark mark='d'/>Finally, in every structure where the second sentence is "
            "true, the first is true too. That is the entailment, checked one structure at a time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for r in bars:
                self.play(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value), run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(why[:2]))
            vo.wait_until("c")
            self.play(FadeIn(why[2:]))
            vo.wait_until("d")
            self.play(FadeIn(imp, shift=UP * 0.2))
        self.clear_scene()

    def validity(self):
        defs = VGroup(
            MathTex(r"\models \varphi", r"\iff", r"\varphi \text{ is true in every structure}", font_size=36),
            MathTex(r"\Gamma \models \varphi", r"\iff",
                    r"\text{every structure that makes } \Gamma \text{ true makes } \varphi \text{ true}",
                    font_size=36)).arrange(DOWN, buff=0.4).move_to([0, 1.6, 0])
        for r in defs:
            r[0].set_color(GOAL)
        x0 = defs[0][1].get_x()
        defs[1].shift(RIGHT * (x0 - defs[1][1].get_x()))
        sizes = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"structures of size 1, 2, 3, \dots", GREY_A), (r"infinite structures: \ $\mathbb{N}$, $\mathbb{Q}$, "
                                                              r"$\mathbb{R}$, \dots", GREY_A),
            (r"no truth table can list them all", BAD))]).arrange(DOWN, buff=0.22).move_to([0, -1.0, 0])
        q = label(r"so how could validity ever be checked? \ Chapters 5--10", font_size=28, color=GOAL).to_edge(
            DOWN, buff=0.45)
        with self.voiceover(
            "With truth in a structure, validity is defined as before. <bookmark mark='a'/>A sentence is valid when "
            "it is true in every structure, and an argument is valid when every structure that makes the premises "
            "true makes the conclusion true. <bookmark mark='b'/>But look at what 'every structure' now means. "
            "Structures of every finite size, and infinite ones: the natural numbers, the rationals, the reals, and "
            "far larger. <bookmark mark='c'/>There is no truth table with a row for each. So it is not at all "
            "obvious that validity can be checked by anything finite. That question drives the rest of this part."
        ) as vo:
            self.play(FadeIn(defs[0]))
            vo.wait_until("a")
            self.play(Indicate(defs[0], color=P.CLAIM))
            self.play(FadeIn(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(sizes[:2]))
            vo.wait_until("c")
            self.play(FadeIn(sizes[2]), FadeIn(q))
        self.clear_scene()
