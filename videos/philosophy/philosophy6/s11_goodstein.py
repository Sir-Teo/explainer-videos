from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Goodstein(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"A sequence that must come home", r"Can numbers that grow for ages be proved to stop?",
                            lit=(1982,), part=PART)
        with self.voiceover("Chapter ten. A sequence that must come home."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hereditary()
        self.three()
        self.four()
        self.proof()

    def hereditary(self):
        hc = history_card(1944, r"Reuben Goodstein", r"`On the restricted ordinal theorem'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            MathTex(r"266 = 2^8 + 2^3 + 2^1", font_size=40),
            MathTex(r"266 = 2^{2^{2+1}} + 2^{2+1} + 2", font_size=44, color=GOAL),
            label(r"hereditary base 2: \ even the exponents, \ and theirs, \ are written in base 2", font_size=24,
                  color=GREY_A)).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        game = VGroup(label(r"the game:", font_size=26, color=CONN),
                      label(r"1. \ write the number in hereditary base $b$", font_size=24),
                      label(r"2. \ replace every $b$ by $b + 1$", font_size=24),
                      label(r"3. \ subtract one; \ repeat with base $b + 1$", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is a theorem about ordinary numbers that needs the infinite ordinals to prove. "
            "<bookmark mark='a'/>Write a number in base two, as a sum of powers of two. <bookmark mark='b'/>Then "
            "write the exponents in base two as well, and their exponents, all the way down: this is hereditary "
            "base two. <bookmark mark='c'/>Reuben Goodstein's game, from 1944: write the number in hereditary base "
            "b. Replace every b by b plus one. Subtract one. Then repeat, with the next base."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g) for g in game], lag_ratio=0.3))
        self.clear_scene()

    def table(self, seq, n_rows, font_size=28):
        hd = [label(r"base", font_size=22, color=P.CLAIM), label(r"value", font_size=22, color=P.CLAIM),
              label(r"hereditary form", font_size=22, color=P.CLAIM), label(r"its ordinal", font_size=22,
                                                                           color=P.CLAIM)]
        rows = []
        for t in seq[:n_rows]:
            rows.append([MathTex(str(t["base"]), font_size=font_size), MathTex(str(t["value"]), font_size=font_size),
                         MathTex(t["tex"], font_size=font_size), MathTex(t["ordinal"], font_size=font_size, color=ORD)])
        return ValueGrid(hd, rows, col_w=[1.3, 1.5, 4.8, 4.6], cell_h=0.56, font_size=font_size)

    def three(self):
        d = load("goodstein")
        g = self.table(d["g3"], len(d["g3"])).move_to([0, 0.4, 0])
        cap = label(r"from 3: \ home in five steps", font_size=26, color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Start with three. <bookmark mark='a'/>In base two, three is two plus one. Bump the base to three: three "
            "plus one, which is four. Subtract one: three. <bookmark mark='b'/>In base three, it is just three, a "
            "single digit. Bumping the base changes nothing now, and each step subtracts one: two, one, zero. "
            "<bookmark mark='c'/>The sequence from three reaches zero in five steps."
        ) as vo:
            self.play(FadeIn(g.head), FadeIn(g.rows_bg), FadeIn(g.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in g.cell[0] + g.cell[1]])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*g.cell[r])) for r in range(2, len(g.cell))], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.clear_scene()

    def four(self):
        d = load("goodstein")
        g = self.table(d["g4"], 8, font_size=26).move_to([0, 0.6, 0])
        big = VGroup(label(r"from 4: \ the values climb for an astronomically long time", font_size=26, color=BAD),
                     MathTex(r"\text{and reach } 0 \text{ after } 3 \cdot 2^{402\,653\,211} - 2 \text{ steps}",
                             font_size=32, color=GOAL)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now start with four. <bookmark mark='a'/>Four is two to the two. Bump the base: three to the three, "
            "twenty-seven, minus one is twenty-six. Then forty-one, sixty, eighty-three, one hundred and nine. "
            "<bookmark mark='b'/>The values keep climbing. In fact they climb for an unimaginably long time: the "
            "sequence from four reaches zero only after three times two to the power four hundred and two million, "
            "minus two steps. <bookmark mark='c'/>And yet Goodstein proved that every such sequence, from every "
            "starting number, eventually comes back to zero. Look at the last column for the reason."
        ) as vo:
            self.play(FadeIn(g.head), FadeIn(g.rows_bg), FadeIn(g.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*g.cell[r][:3])) for r in range(len(g.cell))], lag_ratio=0.25),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(big))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g.cell[r][3]) for r in range(len(g.cell))], lag_ratio=0.2))
        self.clear_scene()

    def proof(self):
        d = load("goodstein")
        head = label(r"Why it must stop: \ replace the base by $\omega$", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        ords = VGroup(*[MathTex(t["ordinal"], font_size=32, color=ORD) for t in d["g4"][:6]])
        gts = []
        chain = VGroup()
        for i, o in enumerate(ords):
            chain.add(o)
            if i < len(ords) - 1:
                chain.add(MathTex(r">", font_size=34, color=GREY_B))
        chain.arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.7)
        if chain.width > 13.2:
            chain.width = 13.2
        steps = VGroup(label(r"bumping the base leaves the ordinal unchanged; \ subtracting one makes it smaller",
                             font_size=26),
                       label(r"a strictly decreasing sequence of ordinals must stop \ (well-ordering)", font_size=26,
                             color=GOAL),
                       label(r"so every Goodstein sequence reaches 0 \ $\checkmark$ \ (checked: the ordinals fall at "
                             r"every step shown)", font_size=24, color=OK)).arrange(DOWN, buff=0.3).next_to(chain, DOWN,
                                                                                                    buff=0.6)
        kp = VGroup(history_card(1982, r"Laurie Kirby \& Jeff Paris", r"Goodstein's theorem is not provable in Peano "
                                 r"arithmetic", width=7.4, color=HIST),
                    label(r"it needs induction up to $\varepsilon_0$: \ a true statement about numbers that arithmetic "
                          r"cannot prove \ (Part 7)", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Here is Goodstein's proof. <bookmark mark='a'/>Take each term in hereditary base, and replace the base "
            "by omega everywhere. Each number becomes an ordinal below epsilon zero. <bookmark mark='b'/>Bumping the "
            "base does not change this ordinal at all. Subtracting one always makes it smaller. So the ordinals "
            "form a strictly decreasing sequence. <bookmark mark='c'/>But the ordinals are well-ordered: there is no "
            "infinite descending sequence. So the ordinals must reach zero, and so must the numbers. "
            "<bookmark mark='d'/>In 1982 Laurie Kirby and Jeff Paris proved something remarkable: this theorem, "
            "though it is about ordinary numbers, cannot be proved from the usual axioms of arithmetic. It needs "
            "the infinite. Part 7 explains how such a thing is possible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in chain], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(kp))
        self.clear_scene()
