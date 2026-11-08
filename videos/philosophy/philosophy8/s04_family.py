from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Family(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"A family of paradoxes", r"Is there one pattern behind them all?", lit=(1908,),
                            part=PART)
        with self.voiceover("Chapter three. A family of paradoxes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.grelling()
        self.richard()
        self.inclosure()

    def grelling(self):
        d = load("grelling")
        hc = history_card(1908, r"Kurt Grelling \& Leonard Nelson", r"autological and heterological words",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        hd = [label(r"adjective", font_size=22, color=P.CLAIM), label(r"does it describe itself?", font_size=22,
                                                                       color=P.CLAIM)]
        rows = []
        for a, kind in d["table"].items():
            rows.append([label(rf"`{a}'", font_size=26),
                         label(kind, font_size=24, color=OK if kind == "autological" else GOAL)])
        rows.append([label(r"`heterological'", font_size=26, color=SELF),
                     label(r"autological iff heterological: \ no consistent answer", font_size=22, color=BAD)])
        grid = ValueGrid(hd, rows, col_w=[3.6, 6.0], cell_h=0.48, font_size=24).move_to([0.6, -0.55, 0])
        assert d["heterological_consistent"] == []
        with self.voiceover(
            "In 1908 Kurt Grelling and Leonard Nelson found the liar inside the dictionary. "
            "<bookmark mark='a'/>Call an adjective autological if it describes itself, and heterological if it "
            "does not. 'Short' is a short word, so it is autological; 'long' is not long, so it is heterological. "
            "'Polysyllabic' is polysyllabic; 'monosyllabic' is not. 'English' is English; 'German' is not. The "
            "Reasoner checks each with a little test of length, syllables and spelling. "
            "<bookmark mark='b'/>Now ask about 'heterological'. If it is heterological, it describes itself, so it "
            "is autological. If it is autological, it describes itself, so it is heterological. The Reasoner tries "
            "both answers, and neither is consistent."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows) - 1)], lag_ratio=0.3),
                      run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[len(rows) - 1])))
        self.clear_scene()

    def richard(self):
        hc = history_card(1905, r"Jules Richard", r"the paradox of definable reals", width=5.4, color=HIST).to_corner(
            UL, buff=0.35)
        rows = VGroup(label(r"list every English phrase that defines a real number between 0 and 1", font_size=26),
                      label(r"there are countably many: \ $r_1, r_2, r_3, \dots$", font_size=26),
                      label(r"`the real whose $n$-th digit is one more than $r_n$'s, \ mod 10'", font_size=26,
                            color=SELF),
                      label(r"is defined by an English phrase, \ yet differs from every $r_n$: \ Cantor's diagonal "
                            r"(Part 6) turned on language", font_size=26, color=BAD)).arrange(
            DOWN, buff=0.35).move_to([0, -0.2, 0])
        berry = label(r"and Berry's paradox, \ made exact in Part 7", font_size=24, color=GREY_A).to_edge(DOWN,
                                                                                                          buff=0.4)
        with self.voiceover(
            "Jules Richard, a schoolteacher in Dijon, gave another in 1905. <bookmark mark='a'/>List every English "
            "phrase that defines a real number between zero and one. There are only countably many phrases, so "
            "the numbers they define form a list. <bookmark mark='b'/>Now take the real whose n-th digit is one "
            "more than the n-th digit of the n-th number on the list. <bookmark mark='c'/>That number has just been "
            "defined by an English phrase, yet it differs from every number on the list: Cantor's diagonal, turned "
            "against language. <bookmark mark='d'/>Berry's paradox, which Part 7 made exact, is a third member of "
            "the family."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(berry))
        self.clear_scene()

    def inclosure(self):
        hc = history_card(1994, r"Graham Priest", r"`The structure of the paradoxes of self-reference'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        schema = VGroup(label(r"a totality $\Omega$, \ and a way $\delta$ of going beyond any part of it:",
                              font_size=26),
                        label(r"applied to $\Omega$ itself, \ $\delta(\Omega)$ is both inside $\Omega$ and outside it",
                              font_size=26, color=SELF)).arrange(DOWN, buff=0.2).next_to(hc, DOWN, buff=0.4).to_edge(
            LEFT, buff=0.8)
        hd = [label(r"paradox", font_size=22, color=P.CLAIM), label(r"the totality $\Omega$", font_size=22,
                                                                     color=P.CLAIM),
              label(r"the diagonaliser $\delta(\Omega)$", font_size=22, color=P.CLAIM)]
        rows = [[label(a, font_size=24, color=GOAL), label(b, font_size=22), label(c, font_size=22)]
                for a, b, c in Tr.INCLOSURE]
        grid = ValueGrid(hd, rows, col_w=[2.6, 4.0, 5.8], cell_h=0.52, font_size=22).to_edge(DOWN, buff=0.45)
        moral = label(r"Priest: \ one structure, \ so one solution", font_size=24, color=OK).next_to(
            schema, DOWN, buff=0.3).align_to(schema, LEFT)
        with self.voiceover(
            "Graham Priest argued in 1994 that these are one paradox. <bookmark mark='a'/>Each has a totality, and "
            "a way of going beyond any part of it. Applied to the totality itself, the result must be both inside "
            "and outside it. <bookmark mark='b'/>Russell's set, beyond the sets; the ordinal above all ordinals, "
            "beyond the ordinals; the liar, beyond the true sentences; Berry's number, beyond the definable ones; "
            "the word heterological, beyond the autological. <bookmark mark='c'/>If they share a structure, Priest "
            "argued, they deserve one solution. Many logicians agree about the structure, and disagree about the "
            "solution."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(schema))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.4),
                      run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()
