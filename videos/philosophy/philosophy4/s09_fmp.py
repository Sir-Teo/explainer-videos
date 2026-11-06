from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class FMP(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Finite models and decidability", r"Can a machine decide modal validity?",
                            lit=(1977,), part=PART)
        with self.voiceover("Chapter eight. Finite models, and decidability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.filtration()
        self.decide()
        self.tableau()
        self.counter()

    def filtration(self):
        d = load("filtration")
        n = d["n"]
        cols = [P.CLAIM, P.AGENT, GOAL, OK, P.WORLD]
        blk = {w: i for i, b in enumerate(d["blocks"]) for w in b}
        xs = np.linspace(-6.0, 6.0, n)
        dots = VGroup(*[Circle(radius=0.24, stroke_color=cols[blk[w]], stroke_width=3, fill_color="#0B0F17",
                               fill_opacity=1).move_to([xs[w], 1.2, 0]) for w in range(n)])
        ps = VGroup(*[MathTex("p", font_size=22, color=PROP).move_to(dots[w]) for w in range(n) if w % 3 == 0])
        arrows = VGroup(*[Arrow(dots[w].get_right(), dots[w + 1].get_left(), buff=0.03, color=ACC, stroke_width=2,
                                max_tip_length_to_length_ratio=0.3) for w in range(n - 1)])
        loop = Arc(radius=0.18, start_angle=-PI / 6, angle=4 * PI / 3, color=ACC, stroke_width=2).move_to(
            dots[-1].get_top() + UP * 0.12)
        f = VGroup(label(r"filter through the subformulas of", font_size=24, color=GREY_A),
                   MathTex(d["formula"].replace("□", r"\Box ").replace("◇", r"\Diamond ").replace("→", r"\to"),
                           font_size=34, color=GOAL)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
        sub = label(rf"{len(d['subformulas'])} subformulas: \ at most $2^{{{len(d['subformulas'])}}} = {d['bound']}$ "
                    r"kinds of world", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.15)
        qpos = {0: (-1.6, 0.0, 0), 1: (0.0, 0.9, 0), 2: (1.6, 0.0, 0), 3: (0.0, -0.9, 0)}
        nq = len(d["blocks"])
        Q = WorldGraph(list(range(nq)), [tuple(x) for x in d["R"]], {"p": {blk[0]}},
                       pos={i: qpos[i] for i in range(nq)}, center=[0, -1.7, 0], scale_pos=1.0,
                       names={i: rf"[{d['blocks'][i][0]}]" for i in range(nq)}, font_size=22)
        for i in range(nq):
            Q.world[i][0].set_stroke(cols[i], width=4)
        cap = label(rf"{n} worlds $\to$ {nq}: \ the formula has the same truth value at each world and its class",
                    font_size=22, color=OK).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Bisimulation merges worlds that no formula can tell apart. Filtration goes further, and merges "
            "worlds that one particular formula cannot tell apart. <bookmark mark='a'/>Here is a model of twelve "
            "worlds in a line, with p true at every third one. <bookmark mark='b'/>Take a formula, here McKinsey's "
            "axiom, and list its subformulas: six of them. Two worlds that agree on all six are, as far as this "
            "formula is concerned, the same. <bookmark mark='c'/>The Reasoner colours the worlds by what they make "
            "true: four kinds. <bookmark mark='d'/>Merge each kind into one world. The formula has the same truth "
            "value at every world as at its class. Whatever the size of the original model, even infinite, the "
            "filtered one has at most two to the six worlds."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.05), FadeIn(ps),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), Create(loop))
            for dd in dots:
                dd.set_stroke(WORLD)
            vo.wait_until("b")
            self.play(FadeIn(f), FadeIn(sub))
            vo.wait_until("c")
            self.play(*[dots[w].animate.set_stroke(cols[blk[w]], width=4) for w in range(n)])
            vo.wait_until("d")
            self.play(FadeIn(Q), FadeIn(cap))
        self.clear_scene()

    def decide(self):
        head = label(r"So modal logic is decidable", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        steps = VGroup(
            label(r"finite model property: \ if $\varphi$ fails somewhere, it fails in a model of at most "
                  r"$2^{|\mathrm{sub}(\varphi)|}$ worlds", font_size=24),
            label(r"so search every model up to that size: \ a decision procedure", font_size=24, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.5)
        cx = VGroup(
            VGroup(label(r"S5", font_size=28, color=GOAL), label(r"NP-complete, \ like SAT (Ladner 1977)",
                                                                 font_size=24)),
            VGroup(label(r"K, T, S4", font_size=28, color=GOAL), label(r"PSPACE-complete (Ladner 1977)",
                                                                       font_size=24)),
            VGroup(label(r"first-order logic", font_size=28, color=BAD), label(r"undecidable (Part 3)",
                                                                               font_size=24))).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3)
        for r in cx:
            r.arrange(RIGHT, buff=0.4)
        cx.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cx.next_to(steps, DOWN, buff=0.6)
        why = label(r"why the difference? \ modal formulas only look along arrows: \ the guarded fragment of Part 3",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This gives an algorithm. <bookmark mark='a'/>If a modal formula fails anywhere, it fails in a finite "
            "model, of size bounded by the number of its subformulas. <bookmark mark='b'/>So to decide validity, "
            "search every model up to that size. It is slow, but it always halts. <bookmark mark='c'/>Richard "
            "Ladner measured the true cost in 1977: S5 is NP-complete, like SAT, and K, T and S4 are PSPACE-complete. "
            "First-order logic, which contains all of them, is undecidable. <bookmark mark='d'/>The reason is that a "
            "modal formula can only look along the arrows: it lives in the guarded fragment that Chapter ten of "
            "Part 3 found decidable. Modal logic is a decidable island in first-order logic, and that is why "
            "machines use it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in cx], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    LINES = [(0, r"\lnot(\Box(p \to q) \to (\Box p \to \Box q))", r"denied"),
             (0, r"\Box(p \to q)", r"$\alpha$"), (0, r"\lnot(\Box p \to \Box q)", r"$\alpha$"),
             (0, r"\Box p", r"$\alpha$"), (0, r"\lnot\Box q", r"$\alpha$"),
             (1, r"\lnot q", r"$\pi$: \ a new world $w_1$, \ $w_0 R w_1$"),
             (1, r"p", r"$\nu$: \ $\Box p$ reaches $w_1$"), (1, r"p \to q", r"$\nu$: \ $\Box(p \to q)$ reaches $w_1$")]

    def tableau(self):
        d = load("tableau")["K"]
        head = label(r"A tableau with worlds: \ every line is labelled with the world it is about", font_size=28,
                     color=CONN).to_edge(UP, buff=0.35)
        rows = VGroup()
        for w, f, why in self.LINES:
            rows.add(VGroup(MathTex(rf"w_{w}:", font_size=28, color=WORLD), MathTex(f, font_size=30),
                            label(why, font_size=20, color=GREY_B)))
        for i, r in enumerate(rows):
            y = 2.4 - 0.5 * i
            r[0].move_to([-6.0, y, 0])
            r[1].move_to([-5.5 + r[1].width / 2, y, 0])
            r[2].move_to([-0.4 + r[2].width / 2, y, 0])
        y = 2.4 - 0.5 * len(rows) - 0.25
        split = VGroup(Line([-4.2, y + 0.15, 0], [-5.2, y - 0.35, 0], color=GREY_C),
                       Line([-4.2, y + 0.15, 0], [-3.2, y - 0.35, 0], color=GREY_C))
        leaves = VGroup(VGroup(MathTex(r"w_1: \lnot p", font_size=30, color=BAD),
                               MathTex(r"\times", font_size=34, color=BAD)).arrange(DOWN, buff=0.05).move_to(
                            [-5.4, y - 0.75, 0]),
                        VGroup(MathTex(r"w_1: q", font_size=30, color=BAD),
                               MathTex(r"\times", font_size=34, color=BAD)).arrange(DOWN, buff=0.05).move_to(
                            [-3.0, y - 0.75, 0]))
        g = WorldGraph([0, 1], {(0, 1)}, {}, pos={0: (0, 0, 0), 1: (2.2, 0, 0)}, center=[3.4, -1.6, 0])
        res = label(rf"closed: \ K's axiom is valid \ ({len(d['steps'])} steps)", font_size=24, color=OK).next_to(
            g, UP, buff=0.4)
        assert d["valid"]
        with self.voiceover(
            "Part 3 promised that the tableau method would return for necessity and possibility. Here it is: "
            "a tableau in which every line is labelled with a world. <bookmark mark='a'/>To test K's axiom, deny it "
            "at world zero, and break it into pieces there: necessarily, if p then q; necessarily p; and not "
            "necessarily q. <bookmark mark='b'/>A new kind of rule: 'not necessarily q' demands a world where q "
            "fails. Create it, world one, visible from world zero. <bookmark mark='c'/>And the boxes at world zero "
            "now reach world one: p is true there, and if p then q. <bookmark mark='d'/>Split on the conditional. "
            "Not p contradicts p; q contradicts not q. Both branches close: the axiom is valid. The tree creates a "
            "world only when a diamond demands one, so for K it always stops: another decision procedure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:5]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[5]), FadeIn(g.world[0]), FadeIn(g.world[1]), GrowArrow(g.arrows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[6]), FadeIn(rows[7]))
            vo.wait_until("d")
            self.play(Create(split), FadeIn(leaves), FadeIn(res))
        self.clear_scene()

    def counter(self):
        d = load("tableau")
        dia, tk = d["dia"], d["T_in_K"]
        left = VGroup(mf(dia["formula"], font_size=36, color=GOAL),
                      label(r"`if $p$ is possible and $q$ is possible, \ then $p$ and $q$ together are possible'?",
                            font_size=22, color=GREY_A)).arrange(DOWN, buff=0.2).move_to([-3.2, 2.2, 0])
        M = dia["model"]
        g = WorldGraph(M["worlds"], [tuple(x) for x in M["R"]], {k: set(v) for k, v in M["V"].items()},
                       pos={0: (0, 0.9, 0), 1: (-1.4, -0.9, 0), 2: (1.4, -0.9, 0)}, center=[-3.2, -0.6, 0])
        gl = label(r"the open branch: \ one world with $p$, \ another with $q$", font_size=22, color=BAD).next_to(
            g, DOWN, buff=0.3)
        right = VGroup(mf(tk["formula"], font_size=36, color=GOAL),
                       label(r"in K: \ open, \ a world that sees nothing", font_size=22, color=BAD),
                       label(r"in T (every world sees itself): \ closed \ $\checkmark$", font_size=22,
                             color=OK)).arrange(DOWN, buff=0.3).move_to([3.4, 0.8, 0])
        lone = WorldGraph([0], set(), {}, pos={0: (0, 0, 0)}, center=[3.4, -1.6, 0])
        assert not dia["valid"] and not tk["valid"] and d["T_in_T"]["valid"]
        with self.voiceover(
            "When a branch stays open, it is a countermodel, as in Part 3. <bookmark mark='a'/>Test: if p is "
            "possible and q is possible, are p and q possible together? <bookmark mark='b'/>The tableau creates one "
            "world for each diamond: one where p holds and one where q holds, and nothing forces them to be the same "
            "world. The open branch is the model: invalid. <bookmark mark='c'/>And T's axiom in plain K: the branch "
            "stays open, with a single world that sees nothing, where necessarily p is vacuously true and p is false. "
            "Add the rule that every world sees itself, and the same tree closes. Each frame condition is a tableau "
            "rule."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(gl))
            vo.wait_until("c")
            self.play(FadeIn(right[:2]), FadeIn(lone))
            self.play(FadeIn(right[2]))
        self.clear_scene()
