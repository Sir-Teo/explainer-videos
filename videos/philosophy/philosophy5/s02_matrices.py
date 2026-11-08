from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


def tables_row(d, name, ops=("not", "and", "or", "imp"), size=0.56, font_size=24, buff=0.55):
    T = d[name]
    g = VGroup(*[ConnTable(op, T["values"], T[op], designated=T["designated"], size=size, font_size=font_size)
                 for op in ops]).arrange(RIGHT, buff=buff, aligned_edge=UP)
    return g


class Matrices(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Three values", r"What could a third truth value be?", lit=(1920, 1938), part=PART)
        with self.voiceover("Chapter one. Three values."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lukasiewicz()
        self.kleene()
        self.bochvar()
        self.definition()

    def lukasiewicz(self):
        d = load("tables")
        hc = history_card(1920, r"Jan Łukasiewicz", r"`On three-valued logic': \ the future is not yet true or false",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        vals = VGroup(VGroup(vmob("1", 40), label(r"true", font_size=24, color=OK)).arrange(DOWN, buff=0.15),
                      VGroup(vmob("1/2", 40), label(r"possible: \ not yet settled", font_size=24, color=HALF)).arrange(
                          DOWN, buff=0.15),
                      VGroup(vmob("0", 40), label(r"false", font_size=24, color=BAD)).arrange(DOWN, buff=0.15)).arrange(
            RIGHT, buff=1.2).to_corner(UR, buff=0.5).shift(DOWN * 0.15)
        tabs = tables_row(d, "Ł3").move_to([0, -1.4, 0])
        imp_note = label(r"$\tfrac12 \to \tfrac12 \;=\; 1$: \ `if p then p' is true even when p is unsettled",
                         font_size=24, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1920 the Polish logician Jan Łukasiewicz published a short paper on three-valued logic. "
            "<bookmark mark='a'/>His motive was Aristotle's sea battle. If 'there will be a battle tomorrow' is "
            "already true, the future is fixed. So give such sentences a third value, one half: possible, not yet "
            "settled. <bookmark mark='b'/>Then he needed tables. Negation flips true and false and leaves one half "
            "alone. 'And' takes the smaller value, 'or' the larger. <bookmark mark='c'/>And the conditional: one, "
            "if the antecedent is no truer than the consequent; otherwise one minus the drop. "
            "<bookmark mark='d'/>So 'if p then p' is true even when p is unsettled. Łukasiewicz wanted that: "
            "whatever happens tomorrow, if there is a battle, there is a battle."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.15) for v in vals], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[FadeIn(t) for t in tabs[:3]])
            vo.wait_until("c")
            self.play(FadeIn(tabs[3]))
            vo.wait_until("d")
            self.play(Indicate(tabs[3].cell[1][1], color=GOAL), FadeIn(imp_note))
        self.clear_scene()

    def kleene(self):
        d = load("tables")
        hc = history_card(1938, r"Stephen Kleene", r"`On notation for ordinal numbers': \ a computation that has not "
                          r"halted has no value yet", width=6.8, color=HIST).to_corner(UL, buff=0.35)
        k = tables_row(d, "K3", ops=("imp",), size=0.7, font_size=28)[0]
        lk = tables_row(d, "Ł3", ops=("imp",), size=0.7, font_size=28)[0]
        pair = VGroup(VGroup(label(r"Kleene's strong K3", font_size=26, color=P.CLAIM), k).arrange(DOWN, buff=0.4),
                      VGroup(label(r"Łukasiewicz's Ł3", font_size=26, color=P.CLAIM), lk).arrange(DOWN, buff=0.4)
                      ).arrange(RIGHT, buff=1.6).move_to([0, -0.5, 0])
        diff = VGroup(SurroundingRectangle(k.cell[1][1], color=GOAL, buff=0.03),
                      SurroundingRectangle(lk.cell[1][1], color=GOAL, buff=0.03))
        same = label(r"$\lnot$, $\land$, $\lor$: \ the same tables in both", font_size=24, color=GREY_A).next_to(
            pair, DOWN, buff=0.4)
        rule = label(r"Kleene's rule: \ if the known inputs already settle the value, give it; \ otherwise unknown",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Eighteen years later, Stephen Kleene arrived at almost the same tables for a different reason. "
            "<bookmark mark='a'/>He was studying partial functions, computations that may never halt. A test whose "
            "computation has not halted has no value yet, so the middle value means 'undefined' or 'unknown'. "
            "<bookmark mark='b'/>His rule: if the inputs that are known already settle the answer, give it; "
            "'false and unknown' is false, whatever the unknown turns out to be. Otherwise the answer is unknown. "
            "<bookmark mark='c'/>That gives exactly Łukasiewicz's negation, conjunction and disjunction. "
            "<bookmark mark='d'/>The only cell that differs is unknown implies unknown: Kleene says unknown, "
            "Łukasiewicz says true."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(pair[0]))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(pair[1]), FadeIn(same))
            vo.wait_until("d")
            self.play(Create(diff))
        self.clear_scene()

    def bochvar(self):
        d = load("tables")
        hc = history_card(1938, r"Dmitri Bochvar", r"the third value is \textit{meaningless}, \ and it infects",
                          width=6.0, color=HIST).to_corner(UL, buff=0.35)
        wk = tables_row(d, "B3", ops=("and", "or"), size=0.66, font_size=28, buff=1.0).move_to([-2.6, -0.4, 0])
        ex = VGroup(label(r"`Paris is in France, \ and the number 7 is sleepy'", font_size=24),
                    label(r"one meaningless part: \ the whole is meaningless", font_size=24, color=HALF)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, 0.3, 0])
        sql = VGroup(label(r"SQL's NULL follows Kleene, not Bochvar:", font_size=24, color=P.CLAIM),
                     label(r"\texttt{NULL AND FALSE} \ is \ \texttt{FALSE}", font_size=22),
                     label(r"\texttt{WHERE} keeps only the rows that are \texttt{TRUE}", font_size=22, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -1.6, 0])
        with self.voiceover(
            "In the same year, Dmitri Bochvar in Moscow read the third value as 'meaningless'. "
            "<bookmark mark='a'/>A meaningless part makes the whole meaningless, so in his tables the middle value "
            "spreads to everything it touches: these are the weak Kleene tables. <bookmark mark='b'/>Paris is in "
            "France, and the number seven is sleepy: not false, but nonsense. <bookmark mark='c'/>You use one of "
            "these logics every day. The NULL of database languages is Kleene's strong unknown: NULL and FALSE is "
            "FALSE. And a query keeps only the rows whose condition comes out TRUE, which, as we will see, means "
            "that only the value one is designated."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(wk))
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(FadeIn(sql))
        self.clear_scene()

    def definition(self):
        d = load("compare")
        dc = definition_card(r"logical matrix", r"a set of values; \ a subset of \textit{designated} values, the ones "
                             r"that count as holding; \ and a table for each connective", width=9.6, font_size=24,
                             color=P.CLAIM).to_edge(UP, buff=0.4)
        cons = MathTex(r"\Gamma \models \varphi", r"\iff", r"\text{every valuation that designates all of }\Gamma"
                       r"\text{ designates }\varphi", font_size=32).next_to(dc, DOWN, buff=0.5)
        cons[0].set_color(GOAL)
        who = label(r"Łukasiewicz and Tarski (1930); \ Łoś and Suszko (1958): \ every structural logic has its matrices",
                    font_size=22, color=GREY_A).next_to(cons, DOWN, buff=0.3)
        rows = VGroup(*[MathTex(rf"{k} \text{{ atom{'s' if k > 1 else ''}}}:\ \ 3^{{{k}}} = "
                                + f"{3 ** k:,}".replace(",", "{,}") + r" \text{ rows}", font_size=28, color=GREY_A)
                        for k in (1, 2, 3, 10)]).arrange_in_grid(2, 2, buff=(1.2, 0.25), col_alignments="ll").next_to(
            who, DOWN, buff=0.5)
        rows[-1].set_color(BAD)
        dec = label(r"so consequence in any finite matrix is decidable: \ the Reasoner simply enumerates",
                    font_size=26, color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Behind all three is one idea, made precise by Łukasiewicz and Tarski in 1930. "
            "<bookmark mark='a'/>A logical matrix is a set of values, a subset of designated values, the ones that "
            "count as 'holding', and a table for each connective. <bookmark mark='b'/>An argument is valid when "
            "every valuation that gives all the premises a designated value gives the conclusion one too. "
            "Classical logic is the matrix with two values and one designated. <bookmark mark='c'/>In 1958 Łoś "
            "and Suszko showed that matrices are enough: every well-behaved propositional logic, however strange, is "
            "characterized by them, though the values may have to be infinitely many. <bookmark mark='d'/>For a finite matrix, there are finitely many rows: three "
            "to the power of the number of atoms. <bookmark mark='e'/>So consequence is decidable, and the "
            "Reasoner's new module does it the obvious way: it writes down every row."
        ) as vo:
            self.play(FadeIn(dc))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Write(cons))
            vo.wait_until("c")
            self.play(FadeIn(who))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(dec))
        self.clear_scene()
