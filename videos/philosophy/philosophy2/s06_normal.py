from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403


class Normal(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Normal forms", r"Can every formula be put in one standard shape?",
                            lit=(1968,), part=PART)
        with self.voiceover("Chapter five. Normal forms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cnf()
        self.blowup()
        self.tseitin()
        self.horn()

    def cnf(self):
        tt = TruthTable(["p <-> q"], font_size=36).scale(1.2).move_to([-4.2, 0.2, 0])
        false_rows = [i for i, v in enumerate(tt.values) if not v[-1]]
        boxes = VGroup(*[tt.row_box(i, color=BAD) for i in false_rows])
        cls = {1: r"(\lnot p \lor q)", 2: r"(p \lor \lnot q)"}
        why_ = {1: r"not (T, F)", 2: r"not (F, T)"}
        ms = VGroup()
        for i in false_rows:
            m = VGroup(MathTex(cls[i], font_size=40, color=WHITE), label(why_[i], font_size=22, color=BAD))
            m.arrange(RIGHT, buff=0.3).next_to(tt.rows_bg[i], RIGHT, buff=0.6)
            ms.add(m)
        cnf = MathTex(r"p \leftrightarrow q", r"\;\equiv\;", r"(\lnot p \lor q)", r"\land", r"(p \lor \lnot q)",
                      font_size=46).move_to([1.8, -2.3, 0])
        cnf[0].set_color(GOAL)
        names = VGroup(brace_note(cnf[2], r"a clause", font_size=24), brace_note(cnf[4], r"a clause", font_size=24))
        dfn = definition_card(r"Conjunctive normal form", r"an `and' of clauses; a clause is an `or' of literals; a "
                              r"literal is an atom or its negation", width=6.4, font_size=22).to_corner(UR, buff=0.35)
        with self.voiceover(
            "Chapter three built a formula from a table's true rows: an 'or' of 'and's, the disjunctive normal form. "
            "Turn the recipe around. <bookmark mark='a'/>Look at the false rows instead. <bookmark mark='b'/>For each, "
            "write a clause that says 'not this row': for p true and q false, not p or q. <bookmark mark='c'/>The "
            "'and' of those clauses is true exactly where no false row holds: the conjunctive normal form, an 'and' "
            "of 'or's."
        ) as vo:
            self.play(FadeIn(tt), FadeIn(dfn))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in ms], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(TransformFromCopy(VGroup(ms[0][0], ms[1][0]), VGroup(cnf[2], cnf[4])), FadeIn(cnf[0:2]),
                      FadeIn(cnf[3]))
        with self.voiceover(
            "Each clause is a constraint that any satisfying valuation must meet, so a formula in this form is just a "
            "list of constraints. <bookmark mark='a'/>This is the form every SAT solver reads, in a plain text format "
            "called DIMACS: one clause per line, atoms as numbers, a minus sign for not. Problems from chip design, "
            "scheduling and mathematics all arrive at the solver as lists like this one."
        ) as vo:
            self.play(FadeIn(names))
            vo.wait_until("a")
            dim = code_block(["p cnf 2 2", "-1 2 0", "1 -2 0"], font_size=26).next_to(cnf, UP, buff=0.5).set_x(
                cnf.get_x())
            self.play(FadeIn(dim, shift=UP * 0.2))
        self.clear_scene()

    def blowup(self):
        d = load("blowup")["rows"]
        f = MathTex(r"(x_1 \land y_1) \lor (x_2 \land y_2) \lor \cdots \lor (x_n \land y_n)", font_size=40)
        f.to_edge(UP, buff=0.45)
        ex = MathTex(r"n=2:\quad (x_1 \lor x_2)(x_1 \lor y_2)(y_1 \lor x_2)(y_1 \lor y_2)", font_size=34,
                     color=GREY_A).next_to(f, DOWN, buff=0.3)
        G = axes([0.5, 12.5], [0, 4.2], x_length=6.2, y_length=4.3, xticks=[1, 4, 8, 12], yticks=[0, 1, 2, 3, 4],
                 yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=r"pairs $n$", ylabel=r"clauses",
                 center=[-3.0, -1.2, 0])
        ax = G.ax
        ns = [r["n"] for r in d]
        dist = curve(ax, ns, [np.log10(r["dist_clauses"]) for r in d], BAD, stroke_width=4)
        ts = curve(ax, ns, [np.log10(r["tseitin_clauses"]) for r in d], OK, stroke_width=4)
        ddots = VGroup(*[Dot(ax.c2p(r["n"], np.log10(r["dist_clauses"])), radius=0.05, color=BAD) for r in d])
        tdots = VGroup(*[Dot(ax.c2p(r["n"], np.log10(r["tseitin_clauses"])), radius=0.05, color=OK) for r in d])
        r10 = next(r for r in d if r["n"] == 10)
        r12 = d[-1]
        dl = label(r"distributing: $2^n$", font_size=26, color=BAD).next_to(ax.c2p(8.5, 3.9), LEFT, buff=0.1)
        tl = label(rf"Tseitin: {r12['tseitin_clauses']} at $n = 12$", font_size=26, color=OK).next_to(
            ax.c2p(11.5, np.log10(r12["tseitin_clauses"])), DOWN, buff=0.3)
        nums = VGroup(MathTex(rf"n = 10:\ \ {r10['dist_clauses']:,}".replace(",", "{,}") + r"\text{ clauses}",
                              font_size=32, color=BAD),
                      MathTex(r"n = 40:\ \ \approx 10^{12}", font_size=32, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, -0.6, 0])
        with self.voiceover(
            "But getting into this form by algebra can explode. <bookmark mark='a'/>Take x one and y one, or x two "
            "and y two, and so on, n pairs. To write it as clauses, distribute 'or' over 'and', the way you multiply "
            "out brackets. <bookmark mark='b'/>Each clause picks one letter from every pair, so there are two to the "
            f"n of them. <bookmark mark='c'/>Ten pairs: {r10['dist_clauses']:,} clauses. Forty pairs: about a "
            "trillion. A formula that fits on one line becomes a list no computer can hold."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(FadeIn(G), Create(dist), FadeIn(ddots), FadeIn(dl), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(nums))
        self.G, self.ts, self.tdots, self.tl, self.r10 = G, ts, tdots, tl, r10
        self.play(FadeOut(ex), FadeOut(nums))

    def tseitin(self):
        G, ts, tdots, tl, r10 = self.G, self.ts, self.tdots, self.tl, self.r10
        hc = history_card(1968, r"Grigori Tseitin", r"name every subformula; write what the name means",
                          width=4.8, color=HIST).move_to([4.3, 1.4, 0])
        defs = VGroup(MathTex(r"t \leftrightarrow (x \land y):", font_size=34, color=CONN),
                      MathTex(r"(\lnot t \lor x)\ \ (\lnot t \lor y)\ \ (t \lor \lnot x \lor \lnot y)", font_size=32))
        defs.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(hc, DOWN, buff=0.35).align_to(hc, LEFT)
        if defs.width > 5.0:
            defs.width = 5.0
        defs.align_to(hc, LEFT)
        res = label(rf"$n=10$: \ {r10['tseitin_clauses']} clauses, not {r10['dist_clauses']:,}", font_size=26,
                    color=OK).next_to(defs, DOWN, buff=0.35).align_to(defs, LEFT)
        eq = label(r"not equivalent, but \emph{equisatisfiable}", font_size=26, color=GREY_A).next_to(res, DOWN,
                                                                                                     buff=0.2)
        eq.align_to(res, LEFT)
        with self.voiceover(
            "In 1968 Grigori Tseitin showed the way around. Don't distribute. <bookmark mark='a'/>Give every "
            "subformula a fresh name, and write a few clauses saying the name means what it should. For t standing "
            "for x and y: if t then x; if t then y; and if x and y, then t. Three clauses for each connective, plus "
            "one saying that the whole formula's name is true. <bookmark mark='b'/>The size now grows in a straight "
            f"line: for ten pairs, {r10['tseitin_clauses']} clauses instead of {r10['dist_clauses']:,}."
        ) as vo:
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(Write(defs))
            vo.wait_until("b")
            self.play(Create(ts), FadeIn(tdots), FadeIn(tl), FadeIn(res), run_time=2)
        with self.voiceover(
            "The new formula is not equivalent to the old one: it has new letters. But it is satisfiable exactly "
            "when the old one is, which is all a solver needs. <bookmark mark='a'/>So from now on, every question is a "
            "list of clauses, and 'is this argument valid?' becomes 'are these clauses, together with the negation of "
            "the conclusion, unsatisfiable?' That is the question the solvers of Chapters nine to eleven answer."
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(Indicate(tl, color=OK))
        self.clear_scene()

    def horn(self):
        from explainer.philosophy.reasoner import prop

        rules = [("rain -> wet", r"$\mathit{rain} \to \mathit{wet}$", r"$(\lnot \mathit{rain} \lor \mathit{wet})$"),
                 ("wet & cold -> ice", r"$\mathit{wet} \land \mathit{cold} \to \mathit{ice}$",
                  r"$(\lnot \mathit{wet} \lor \lnot \mathit{cold} \lor \mathit{ice})$"),
                 ("ice -> slippery", r"$\mathit{ice} \to \mathit{slippery}$",
                  r"$(\lnot \mathit{ice} \lor \mathit{slippery})$")]
        facts = ["rain", "cold"]
        known = list(facts)
        derived = []
        changed = True
        while changed:  # forward chaining: fire every rule whose body is known
            changed = False
            for src, _, _ in rules:
                body, head = src.split("->")
                b = [x.strip() for x in body.split("&")]
                h = head.strip()
                if all(x in known for x in b) and h not in known:
                    known.append(h)
                    derived.append(h)
                    changed = True
        fs = [prop.parse(r[0]) for r in rules] + [prop.parse(f) for f in facts]
        chain = ", then ".join(derived)
        for h in derived:
            assert prop.entails(fs, prop.parse(h))[0]
        dfn = definition_card(r"Horn clause", r"at most one un-negated atom: \ a rule `if these, then that', or a "
                              r"fact", width=6.2, font_size=24, color=P.WORLD).to_corner(UL, buff=0.4)
        rows = VGroup()
        for _, r, c in rules:
            rows.add(VGroup(label(r, font_size=30), MathTex(r"\equiv", font_size=30, color=GREY_C),
                            label(c, font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(dfn, DOWN, buff=0.5).align_to(dfn, LEFT)
        fact = label(r"facts: \ $\mathit{rain}$, \ $\mathit{cold}$", font_size=30, color=ATOM)
        fact.next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        chain = VGroup(*[label(rf"$\Rightarrow\ \mathit{{{h}}}$", font_size=34, color=OK) for h in derived])
        chain.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.0, 0])
        cplx = VGroup(label(r"Horn clauses: \ linear time (Dowling \& Gallier 1984)", font_size=24, color=OK),
                      label(r"two literals per clause: \ polynomial (Aspvall, Plass \& Tarjan 1979)", font_size=24,
                            color=OK),
                      label(r"three literals per clause: \ NP-complete (Chapter 12)", font_size=24, color=BAD))
        cplx.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Not every list of clauses is equally hard. <bookmark mark='a'/>A clause with at most one un-negated atom "
            "is called a Horn clause, after the logician Alfred Horn, and it is just a rule: not rain, or wet, says "
            "'if it rains, the streets are wet'. <bookmark mark='b'/>Given facts, rain and cold, a solver needs no "
            f"search at all. It fires every rule whose conditions are known, and keeps going: {chain}. "
            "<bookmark mark='c'/>That is unit propagation from the last chapter's toolbox, and for Horn clauses it "
            "decides satisfiability in linear time. It is the engine of the programming language Prolog and of the "
            "rule-based expert systems of the 1980s. Clauses of two literals are easy too. With three literals per "
            "clause, the problem becomes as hard as any problem whose answers can be checked quickly, as we will "
            "see in Chapter twelve."
        ) as vo:
            self.play(FadeIn(dfn))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(fact))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chain], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cplx], lag_ratio=0.4))
        self.clear_scene()
