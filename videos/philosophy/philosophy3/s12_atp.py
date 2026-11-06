from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


def tt(s: str) -> str:
    """A term or atom in Reasoner syntax as TeX (a bare term is shown through a one-place wrapper)."""
    if s[0].isupper():
        return fol.show(fol.parse(s), tex=True)
    return fol.show(fol.parse(f"W({s})"), tex=True)[len(r"\mathrm{W}("):-1]


class ATP(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Machines that prove", r"How do automated provers search?", lit=(1965,),
                            part=PART)
        with self.voiceover("Chapter eleven. Machines that prove."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.skolem()
        self.unify()
        self.lover()
        self.herbrand()
        self.robbins()
        self.today()

    def skolem(self):
        hc = history_card(1965, r"J.\ Alan Robinson", r"resolution with unification: \ one rule for all of "
                          r"first-order logic", width=6.4, color=HIST).to_corner(UL, buff=0.35)
        a = MathTex(r"\forall x\, \exists y\ \mathrm{L}(x, y)", font_size=42).move_to([-3.2, 0.6, 0])
        b = MathTex(r"\forall x\ \mathrm{L}(x, f(x))", font_size=42, color=GOAL).move_to([3.2, 0.6, 0])
        ar = Arrow(a.get_right(), b.get_left(), buff=0.3, color=GREY_B)
        al = label(r"Skolemize", font_size=22, color=GREY_A).next_to(ar, UP, buff=0.1)
        fl = label(r"$f(x)$: \ `the one $x$ loves', \ a witness that depends on $x$", font_size=24,
                   color=GREY_A).next_to(b, DOWN, buff=0.3)
        steps = VGroup(label(r"1. \ negate the conclusion, \ add it to the premises", font_size=24),
                       label(r"2. \ remove $\exists$ by Skolem functions; \ drop $\forall$: \ free variables mean `all'",
                             font_size=24),
                       label(r"3. \ write the result as clauses, \ as in Part 2", font_size=24),
                       label(r"4. \ resolve, \ until the empty clause $\Box$ appears", font_size=24,
                             color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In Part 2, resolution refuted propositional clauses. In 1965 J. Alan Robinson extended it to all of "
            "first-order logic, and it became the engine of automated reasoning. <bookmark mark='a'/>First the "
            "quantifiers must go. 'Everyone loves someone' becomes 'everyone loves f of x', where f is a new "
            "function naming, for each x, someone x loves. It is the witness of Chapter nine, now a function, and "
            "it is called a Skolem function. <bookmark mark='b'/>Then the recipe: negate the conclusion, remove the "
            "existentials this way, read every remaining variable as 'for all', write everything as clauses, and "
            "resolve until the empty clause appears."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(a))
            self.play(GrowArrow(ar), FadeIn(al), Write(b), FadeIn(fl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in steps], lag_ratio=0.3))
        self.clear_scene()

    def unify(self):
        d = load("atp")
        u, o = d["unify"], d["occurs"]
        head = label(r"Unification: \ make two expressions identical by substituting for variables", font_size=28,
                     color=CONN).to_edge(UP, buff=0.4)
        pair = VGroup(MathTex(tt(u["a"]), font_size=40), MathTex(r"\overset{?}{=}", font_size=40, color=GREY_B),
                      MathTex(tt(u["b"]), font_size=40)).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.5)
        rows = VGroup(*[MathTex(rf"{v} \;\mapsto\; {tt(t)}", font_size=36, color=OK) for v, t in u["steps"]]).arrange(
            DOWN, buff=0.2).next_to(pair, DOWN, buff=0.4)
        res = MathTex(r"\mathrm{Knows}(\mathrm{john}, \mathrm{mother}(\mathrm{john}))", font_size=38,
                      color=GOAL).next_to(rows, DOWN, buff=0.35)
        pair2 = VGroup(MathTex(tt(o["a"]), font_size=36), MathTex(r"\overset{?}{=}", font_size=36, color=GREY_B),
                       MathTex(tt(o["b"]), font_size=36)).arrange(RIGHT, buff=0.4).next_to(res, DOWN, buff=0.6)
        fail = label(rf"${o['steps'][0][0]} \mapsto {o['steps'][0][1]}$, \ then ${o['steps'][1][1]} \mapsto "
                     rf"{tt(o['steps'][1][2])}$: \ a term containing itself, \ fail", font_size=24,
                     color=BAD).next_to(pair2, DOWN, buff=0.25)
        assert u["ok"] and not o["ok"]
        with self.voiceover(
            "Resolution needs one new operation: unification. <bookmark mark='a'/>Can 'John knows x' and 'y knows "
            "y's mother' be made identical? <bookmark mark='b'/>Match them piece by piece. The first arguments: y "
            "must be John. The second: x must be the mother of y, which is now the mother of John. "
            "<bookmark mark='c'/>Both become 'John knows John's mother'. That substitution is the most general "
            "unifier, and Robinson proved it is unique up to renaming. <bookmark mark='d'/>Now try 'x knows x' "
            "against 'y knows y's mother'. x must be y, and then y must be the mother of y: a term that contains "
            "itself. The occurs check fails, and rightly: no finite term is its own mother."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pair))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in rows], lag_ratio=0.6), run_time=2)
            vo.wait_until("c")
            self.play(Write(res))
            vo.wait_until("d")
            self.play(FadeIn(pair2))
            self.play(FadeIn(fail))
        self.clear_scene()

    def lover(self):
        d = load("atp")
        tab = load("tableaux")["romeo"]
        pr = d["proof"]
        readings = [r"everybody loves a lover", r"Romeo loves Juliet", r"denied: \ I love you",
                    r"everyone loves Romeo \ (from 1, 2)", r"you love no one \ (from 1, 3)",
                    r"contradiction \ (from 4, 5)"]
        rows = VGroup()
        for (n, c, ps, u), rd in zip(pr, readings):
            ctex = r"\Box" if c == "□" else fol.show(fol.parse(c.replace("¬", "~").replace(" ∨ ", " | ")),
                                                     tex=True)
            num = MathTex(rf"{n}.", font_size=30, color=GREY_B)
            cl = MathTex(ctex, font_size=34, color=GOAL if n == len(pr) else WHITE).next_to(num, RIGHT, buff=0.3)
            rows.add(VGroup(num, cl))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-2.4, 0.4, 0])
        jx = max(r[1].get_right()[0] for r in rows) + 0.6
        for r, rd in zip(rows, readings):
            lab_ = label(rd, font_size=22, color=GREY_A)
            r.add(lab_.move_to([jx + lab_.width / 2, r[1].get_y(), 0]))
        bar = Line(rows[2].get_corner(DL) + DOWN * 0.13, rows[2].get_corner(DL) + DOWN * 0.13 + RIGHT * 9.0,
                   color=GREY_C, stroke_width=1.5)
        cmp_ = bar_row([3, tab["n_steps"]], [r"resolution: \ resolvents used", r"Chapter 4's tableau: \ steps"],
                       [OK, BAD], width=5.0, height=0.34, font_size=22, log=True).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the Reasoner's new resolution prover on the lover argument from Chapter four. "
            "<bookmark mark='a'/>Three clauses: everybody loves a lover, written 'if y loves z then x loves y'; Romeo "
            "loves Juliet; and the denied conclusion, I do not love you. <bookmark mark='b'/>Resolve the first two, "
            "unifying y with Romeo and z with Juliet: everyone loves Romeo. <bookmark mark='c'/>Resolve the first "
            "with the denial, unifying x with me and y with you: you love no one. <bookmark mark='d'/>And those two "
            "clash, with x as you: the empty clause. <bookmark mark='e'/>Three resolution steps, where the blind "
            f"tableau took {tab['n_steps']}. Unification chooses the instances for us: it is lazy, and binds a "
            "variable only when a match forces it."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3), Create(bar))
            for mk, i in zip("bcd", (3, 4, 5)):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i], shift=DOWN * 0.15))
            self.play(Indicate(rows[5][1], color=GOAL))
            vo.wait_until("e")
            for r in cmp_:
                self.play(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value), run_time=0.7)
        self.clear_scene()

    def herbrand(self):
        thm = theorem_card(r"Herbrand's theorem (1930)", r"a set of clauses is unsatisfiable \ if and only if \ some "
                           r"\textit{finite} set of its ground instances is unsatisfiable \textit{propositionally}",
                           width=9.4, font_size=24).move_to([0, 1.5, 0])
        ex = VGroup(MathTex(r"\mathrm{D}(x),\ \ \lnot \mathrm{D}(f(x))", font_size=36),
                    label(r"the drinker principle, denied and Skolemized", font_size=22, color=GREY_A),
                    MathTex(r"\mathrm{D}(a),\ \ \lnot \mathrm{D}(f(a)),\ \ \mathrm{D}(f(a))", font_size=36, color=GOAL),
                    label(r"three ground instances: \ already a propositional contradiction", font_size=22,
                          color=OK)).arrange(DOWN, buff=0.15).move_to([0, -0.9, 0])
        moral = label(r"first-order proving = generate instances + SAT: \ the engine of modern SMT and instance-based "
                      r"provers", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why does this work at all? <bookmark mark='a'/>Jacques Herbrand proved in 1930 that a set of clauses is "
            "unsatisfiable exactly when some finite collection of its instances, with variables replaced by "
            "variable-free terms, is already unsatisfiable as propositional logic. <bookmark mark='b'/>Take the "
            "drinker principle. Denied and Skolemized, it becomes: everyone drinks, and for every x, f of x does not "
            "drink. <bookmark mark='c'/>Three instances, D of a, not D of f of a, and D of f of a, already "
            "contradict each other. <bookmark mark='d'/>So a first-order prover can generate instances and hand them "
            "to a SAT solver, and many modern provers do exactly that. The undecidability of Chapter ten lives in "
            "one place: no one can say in advance how many instances will be needed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ex[:2]))
            vo.wait_until("c")
            self.play(Write(ex[2]), FadeIn(ex[3]))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def robbins(self):
        hcs = VGroup(history_card(1933, r"Herbert Robbins", r"conjecture: \ these three equations define Boolean "
                                  r"algebra", width=5.4, color=HIST),
                     history_card(1996, r"William McCune, Argonne", r"the prover EQP finds the proof after about "
                                  r"eight days", width=5.4, color=HIST)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.4)
        ax = VGroup(MathTex(r"x + y = y + x", font_size=38),
                    MathTex(r"(x + y) + z = x + (y + z)", font_size=38),
                    MathTex(r"\overline{\overline{x + y} + \overline{x + \overline{y}}} = x", font_size=42,
                            color=GOAL)).arrange(DOWN, buff=0.25).move_to([0, -0.6, 0])
        al = label(r"Robbins's equation: \ open for 63 years, \ including to Tarski and his students", font_size=24,
                   color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Can such machines prove things people could not? <bookmark mark='a'/>In 1933 Herbert Robbins asked "
            "whether three equations, commutativity, associativity, and a strange third one, are enough to define "
            "Boolean algebra, the algebra of Part 2. <bookmark mark='b'/>Tarski and his students worked on it; "
            "nobody could prove it. <bookmark mark='c'/>In 1996 William McCune's prover EQP, at Argonne National "
            "Laboratory, found the proof after about eight days of search. The New York Times reported it. A "
            "problem open for sixty-three years, settled by equational reasoning with unification at its heart."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2), LaggedStart(*[FadeIn(a) for a in ax], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2), Indicate(ax[2], color=GOAL))
        self.clear_scene()

    def today(self):
        head = label(r"Automated reasoning today", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            VGroup(label(r"saturation provers", font_size=26, color=GOAL),
                   label(r"Vampire, E: \ resolution and superposition; \ the CASC competition and the TPTP library "
                         r"of test problems", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"proof assistants", font_size=26, color=GOAL),
                   label(r"Lean, Isabelle, Coq: \ every step checked by a small kernel; \ the Four Colour Theorem "
                         r"(Coq, 2005), \ the Kepler conjecture (2014)", font_size=22, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"hammers", font_size=26, color=GOAL),
                   label(r"Sledgehammer: \ translate a goal into first-order logic, call the provers, check their "
                         r"proof", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"learning to prove", font_size=26, color=GOAL),
                   label(r"AlphaProof (2024): \ reinforcement learning on Lean proofs; \ with AlphaGeometry 2, four "
                         r"of six olympiad problems", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).next_to(head, DOWN, buff=0.45)
        fwd = label(r"what machines that reason should be trusted to do: \ Part 42", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Automated reasoning is now an industry and a research field. <bookmark mark='a'/>Saturation provers "
            "such as Vampire and E compete every year on thousands of problems from the TPTP library. "
            "<bookmark mark='b'/>Proof assistants such as Lean, Isabelle and Coq check every step of a "
            "human-written proof against a small trusted kernel; they have verified the Four Colour Theorem and the "
            "Kepler conjecture. <bookmark mark='c'/>Hammers connect the two: they translate a goal into "
            "first-order logic, call the automatic provers, and check whatever proof comes back. "
            "<bookmark mark='d'/>And learning systems now search for proofs themselves. In 2024 DeepMind's "
            "AlphaProof, trained by reinforcement learning on Lean proofs, together with a geometry system, solved "
            "four of the six problems at the International Mathematical Olympiad. <bookmark mark='e'/>Leibniz's "
            "calculemus has become a working technology, inside the limits of Chapter ten."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(fwd))
        self.clear_scene()
