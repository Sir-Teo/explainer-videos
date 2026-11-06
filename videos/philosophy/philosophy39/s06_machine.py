from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Machine(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Arrow by machine", r"Can a computer prove an impossibility?", lit=(1951, 2009), part=PART)
        with self.voiceover("Chapter five. Arrow by machine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.encoding()
        self.solve()
        self.price()
        self.proofs()
        self.verified()

    def proofs(self):
        head = label(r"Theorems checked by machine", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Tang--Lin \ (2009)", r"an induction lemma reduces Arrow's theorem to 2 voters and 3 candidates; \ SAT does the rest", MACH),
                (r"Nipkow \ (2009)", r"Arrow and Gibbard--Satterthwaite, \ formally verified in Isabelle/HOL", TRUTH),
                (r"Geist--Endriss \ (2011)", r"a computer search found 84 new impossibility theorems about ranking sets of objects", CYC),
                (r"Brandt--Geist \ (2016)", r"SAT proves that no majoritarian rule can be both efficient and strategy-proof in a key setting", SCORE)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Computer-aided social choice is now a field of its own. <bookmark mark='a'/>Tang and Lin's induction "
            "lemma shows that if the theorem holds for two voters and three candidates, it holds for every number of "
            "each. <bookmark mark='b'/>Tobias Nipkow formally verified Arrow's theorem and Gibbard and "
            "Satterthwaite's in the proof assistant Isabelle in 2009. <bookmark mark='c'/>Christian Geist and Ulle "
            "Endriss had a computer search for impossibility theorems about ranking sets of objects, and it found "
            "eighty four new ones, in 2011. <bookmark mark='d'/>And Felix Brandt and Geist used SAT solvers to prove "
            "new impossibilities about efficient, strategy-proof rules, in 2016. Theorems that once took years can "
            "now be searched for."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def encoding(self):
        a = load("arrow")
        assert (a["n_vars"], a["profiles"], a["total_clauses"]) == (108, 36, 992)
        assert a["clauses"] == {"ORDER": 72, "PARETO": 54, "IIA": 864, "ND1": 1, "ND2": 1}
        head = label(r"Arrow's theorem as a satisfiability problem", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        var = MathTex(r"v_{P,\,xy} \;=\; \text{at profile } P,\ \text{society ranks } x \text{ above } y", font_size=30,
                      color=WHITE).move_to([0, 2.2, 0])
        sub = label(r"2 voters, \ 3 candidates: \ $6 \times 6 = 36$ profiles, \ 3 pairs each: \ 108 variables",
                    font_size=21, color=GREY_A).next_to(var, DOWN, buff=0.25)
        hd = [r"\text{condition}", r"\text{clauses}", r"\text{example}"]
        rows = [(r"ORDER", a["clauses"]["ORDER"], r"no cycle: \ $\neg v_{ab} \vee \neg v_{bc} \vee v_{ac}$", MAJ),
                (r"PARETO", a["clauses"]["PARETO"], r"both rank $a$ over $b$ at $P$: \ $v_{P,ab}$", SCORE),
                (r"IIA", a["clauses"]["IIA"], r"$P, Q$ agree on $a, b$: \ $v_{P,ab} \leftrightarrow v_{Q,ab}$", TRUTH),
                (r"ND1, \ ND2", a["clauses"]["ND1"] + a["clauses"]["ND2"],
                 r"somewhere, \ society differs from voter 1; \ and from voter 2", CYC)]
        cells = [[label(r0, font_size=20, color=c), label(str(n), font_size=20), label(ex, font_size=19, color=GREY_A)]
                 for r0, n, ex, c in rows]
        grid = ValueGrid(hd, cells, col_w=[2.6, 1.6, 7.6], cell_h=0.55, font_size=19).move_to([0, -0.6, 0])
        tot = label(rf"{a['total_clauses']} clauses in all", font_size=22, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Arrow's theorem can also be proved by machine. In 2009 Pingzhong Tang and Fangzhen Lin showed that the "
            "whole theorem reduces to its smallest case, two voters and three candidates, and checked that case with "
            "a SAT solver, the tool of Part 2. The Reasoner rebuilds it. <bookmark mark='a'/>A social welfare "
            "function is a choice, for each of the thirty six profiles, of a social ranking. One variable says "
            "whether society ranks x above y at profile P: a hundred and eight variables. <bookmark mark='b'/>Each of "
            "Arrow's conditions becomes clauses. Social rankings must have no cycles: seventy two clauses. Pareto "
            "fixes some variables: fifty four. Independence ties together profiles that agree on a pair: eight "
            "hundred and sixty four. Non-dictatorship says that somewhere society disagrees with voter one, and "
            "somewhere with voter two. <bookmark mark='c'/>Nine hundred and ninety two clauses in all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(var), FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(tot))
        self.clear_scene()

    def solve(self):
        a = load("arrow")
        assert not a["satisfiable"] and a["models_opi"]["models"] == 2 and a["models_pi"]["models"] == 64
        assert a["models_opi"]["dictator_of_each"] == [[1], [2]] and a["subsets_checked"] == 32
        head = label(r"What the solver finds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = stack([(rf"all five conditions: \ \textbf{{unsatisfiable}}, \ after {a['decisions']} decision and "
                        rf"{a['conflicts']} conflicts", BAD),
                       (r"ORDER, \ PARETO, \ IIA: \ exactly 2 solutions, \ found by blocking each in turn", MAJ),
                       (r"and each is a dictatorship: \ of voter 1, \ and of voter 2", CYC),
                       (r"PARETO and IIA without ORDER: \ 64 solutions, \ each pair decided on its own", TRUTH),
                       (r"all 32 subsets of the conditions checked: \ drop any one, \ and a rule exists", GOAL)],
                      font_size=23, buff=0.42).move_to([0, 0.1, 0])
        with self.voiceover(
            "Then the solver runs. <bookmark mark='a'/>With all five conditions, it reports unsatisfiable, after a "
            "single decision and two conflicts: Pareto and independence propagate through the formula almost by "
            "themselves. <bookmark mark='b'/>Drop non-dictatorship, and ask for every solution, blocking each one as "
            "it is found: there are exactly two. <bookmark mark='c'/>One copies voter one's ranking at every profile; "
            "the other copies voter two's. Independence and Pareto leave room for nothing but a dictator. <bookmark "
            "mark='d'/>Drop the ordering condition as well, and there are sixty four solutions, each deciding every "
            "pair on its own, and most of them producing cycles. <bookmark mark='e'/>The Reasoner checks all thirty "
            "two subsets of the conditions: drop any one, and a rule exists. That is the Price List."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def price(self):
        a = load("arrow")
        assert a["mus"] == [["IIA", "ND1", "ND2", "ORDER", "PARETO"]]
        assert sorted(a["mcs"]) == [["IIA"], ["ND1"], ["ND2"], ["ORDER"], ["PARETO"]]
        claims = [("ORDER", r"society's ranking is complete and transitive"),
                  ("PARETO", r"unanimous preferences are respected"),
                  ("IIA", r"each pair is judged on its own"),
                  ("ND1", r"voter 1 is not a dictator"),
                  ("ND2", r"voter 2 is not a dictator")]
        pl = PriceList(claims, mus=[tuple(m) for m in a["mus"]], radius=2.6, width=3.4, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ Arrow's conditions")
        positions = [(("ORDER",), r"allow cycles", r"pairwise majority, \ as Condorcet proposed"),
                     (("IIA",), r"give up independence", r"Borda; \ Kemeny; \ instant runoff; \ every real ranked "
                                                         r"rule"),
                     (("PARETO",), r"give up Pareto", r"a ranking imposed regardless of votes"),
                     (("ND1",), r"accept a dictator", r"one voter's ranking, \ always")]
        dom = label(r"unrestricted domain, \ built into the encoding, \ is a sixth way out: \ chapter seven",
                    font_size=20, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Five conditions cannot all hold. <bookmark mark='a'/>A complete and transitive social ranking; respect "
            "for unanimity; each pair judged on its own; and no dictator, voter one or voter two. <bookmark "
            "mark='b'/>Every voting system pays somewhere. <bookmark mark='c'/>Allow cycles, and pairwise majority "
            "voting satisfies the rest, as Condorcet proposed. <bookmark mark='d'/>Give up independence, as the Borda "
            "count, Kemeny's rule, instant runoff and every ranked rule in real use do. <bookmark mark='e'/>Give up "
            "Pareto, and impose a ranking regardless of the votes. <bookmark mark='f'/>Or accept a dictator. "
            "<bookmark mark='g'/>And the encoding quietly assumed a sixth condition, that any profile can occur; "
            "chapter seven shows what happens when it cannot."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
            vo.wait_until("g")
            self.play(FadeIn(dom))
        self.clear_scene()

    def verified(self):
        head = label(r"Verified counting", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"election software", r"counting rules for real elections are complex: \ single transferable vote has many variants", VOTE),
                (r"bugs", r"an error in counting code can change a result without anyone noticing; \ a rule is only as good as its implementation", BAD),
                (r"verified counters", r"Ghale, \ Goré, \ Pattinson and Tiwari \ (2018): \ STV counting with machine-checked certificates", MACH),
                (r"certificates", r"the counter outputs a proof that its result follows the rule, \ checkable by anyone", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The same tools now check real elections. <bookmark mark='a'/>Counting rules are complex: the single "
            "transferable vote used in Ireland, Malta and Australia's Senate comes in many variants. <bookmark "
            "mark='b'/>An error in counting code can change a result without anyone noticing, and a rule is only as good as its "
            "implementation. <bookmark mark='c'/>Milad Ghale, Rajeev Goré, Dirk Pattinson and Mukesh Tiwari built, in "
            "2018, single transferable vote counters verified in a proof assistant. <bookmark mark='d'/>Their "
            "counters output a certificate, a proof that the result follows the rule, which anyone can check "
            "independently of the software that produced it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
