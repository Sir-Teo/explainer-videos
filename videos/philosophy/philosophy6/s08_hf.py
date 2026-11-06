from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class HF(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Sets from nothing", r"Can everything be built from the empty set?", lit=(1923,),
                            part=PART)
        with self.voiceover("Chapter seven. Sets from nothing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.numerals()
        self.coding()
        self.stages()
        self.coding_math()

    def numerals(self):
        d = load("hf")
        head = label(r"von Neumann's numbers \ (1923): \ each number is the set of the numbers before it",
                     font_size=28, color=CONN).to_edge(UP, buff=0.45)
        cols = VGroup()
        for item in d["von_neumann"][:4]:
            n = item["n"]
            box = set_box(S.von_neumann(n), unit=0.34)
            cols.add(VGroup(MathTex(str(n), font_size=44, color=GOAL), box,
                            MathTex(item["tex"], font_size=26)).arrange(DOWN, buff=0.35))
        cols.arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(head, DOWN, buff=0.6)
        if cols.width > 13.0:
            cols.width = 13.0
        succ = MathTex(r"n + 1 \;=\; n \cup \{n\}", font_size=40, color=GOAL).to_edge(DOWN, buff=1.0)
        prop_ = label(r"$m < n$ \ iff \ $m \in n$; \ \ $n$ has exactly $n$ members", font_size=26,
                      color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Set theory can start from nothing at all. <bookmark mark='a'/>Zero is the empty set: a box with "
            "nothing in it. <bookmark mark='b'/>One is the set whose only member is zero. Two is the set of zero and "
            "one. Three is the set of zero, one and two. John von Neumann proposed these in 1923: each number is the "
            "set of all the numbers before it. <bookmark mark='c'/>The next number is always n together with n "
            "itself. <bookmark mark='d'/>Then 'less than' is just membership, and the number n has exactly n members."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cols[1:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(Write(succ))
            vo.wait_until("d")
            self.play(FadeIn(prop_))
        self.clear_scene()

    def coding(self):
        d = load("hf")
        hc = history_card(1937, r"Wilhelm Ackermann", r"every number codes a finite set, \ and every finite set a number",
                          width=7.2, color=HIST).to_corner(UL, buff=0.3)
        items = d["sets"]
        cells = VGroup()
        for it in items:
            s = S.ackermann_decode(it["code"])
            c = VGroup(MathTex(str(it["code"]), font_size=30, color=GOAL),
                       MathTex(it["bits"] + r"_2", font_size=20, color=GREY_B),
                       set_box(s, unit=0.2)).arrange(DOWN, buff=0.14)
            cells.add(c)
        cells.arrange_in_grid(2, 8, buff=(0.45, 0.45), cell_alignment=UP).next_to(hc, DOWN, buff=0.45)
        if cells.width > 13.2:
            cells.width = 13.2
        cells.set_x(0)
        rule = MathTex(r"n \;\longleftrightarrow\; \{\, \text{the set coded by } i \ :\ \text{bit } i \text{ of } n "
                       r"\text{ is } 1 \,\}", font_size=30).to_edge(DOWN, buff=0.95)
        ex = MathTex(r"11 = 1011_2:\ \text{bits } 0, 1, 3 \ \longrightarrow\ \{\varnothing,\ \{\varnothing\},\ "
                     r"\{\varnothing, \{\varnothing\}\}\} = 3", font_size=28, color=GOAL).to_edge(DOWN, buff=0.4)
        chk = label(r"a bijection: \ checked for every $n < 4096$", font_size=20, color=OK).next_to(rule, UP, buff=0.2)
        assert d["von_neumann"][3]["code"] == 11
        with self.voiceover(
            "There is a beautiful way to list all the finite sets built from nothing. <bookmark mark='a'/>Wilhelm "
            "Ackermann noticed in 1937 that each natural number can code one of them. Write the number in binary; "
            "the set has a member for each digit one, namely the set coded by that digit's position. "
            "<bookmark mark='b'/>Zero codes the empty set. One codes the set containing the empty set. Each number "
            "codes a different set, and every hereditarily finite set gets a number. <bookmark mark='c'/>Eleven is "
            "one, zero, one, one in binary: positions zero, one and three, and the set of the sets they code is "
            "von Neumann's three. The Reasoner confirms the bijection for every number below four thousand and "
            "ninety-six."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cells], lag_ratio=0.12), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(ex), FadeIn(chk), Indicate(cells[11], color=GOAL))
        self.clear_scene()

    def stages(self):
        d = load("hf")
        head = label(r"Stage by stage: \ $V_0 = \varnothing$, \ \ $V_{n+1} = \mathcal{P}(V_n)$", font_size=32,
                     color=CONN).to_edge(UP, buff=0.5)
        sz = d["V_sizes"]
        rows = VGroup()
        for k in range(6):
            v = MathTex(rf"|V_{k}| = {sz[k]:,}".replace(",", "{,}"), font_size=34,
                        color=interpolate_color(ManimColor(SETC), ManimColor(CARD), k / 5))
            rows.add(v)
        rows.add(MathTex(r"|V_6| = 2^{65536}, \ \text{a number with 19{,}729 digits}", font_size=32, color=CARD))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.2, -0.5, 0])
        v3 = VGroup(*[set_box(x, unit=0.3) for x in sorted(S.V(3), key=S.ackermann_code)]).arrange(RIGHT, buff=0.4)
        v3l = label(r"the four members of $V_3$", font_size=24, color=GREY_A)
        g3 = VGroup(v3l, v3).arrange(DOWN, buff=0.35).move_to([3.4, 0.4, 0])
        hfl = label(r"their union: \ the hereditarily finite sets, \ $V_\omega$", font_size=26, color=GOAL).move_to(
            [3.4, -1.8, 0])
        with self.voiceover(
            "Stack the sets in stages. <bookmark mark='a'/>Stage zero is empty. Each next stage is the set of all "
            "subsets of the one before. <bookmark mark='b'/>The sizes explode: zero, one, two, four, sixteen, sixty-"
            "five thousand five hundred and thirty-six, and then two to that power, a number with almost twenty "
            "thousand digits. <bookmark mark='c'/>Here are the four sets of stage three, drawn as boxes. "
            "<bookmark mark='d'/>All the finite stages together give the hereditarily finite sets, the ones "
            "Ackermann numbered. With them, all of finite mathematics can be done."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[:3]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(g3))
            vo.wait_until("d")
            self.play(FadeIn(hfl))
        self.clear_scene()

    def coding_math(self):
        d = load("hf")
        head = label(r"Everything is a set", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"ordered pair \ (Kuratowski 1921)", r"(a, b) = \{\{a\}, \{a, b\}\}"),
                (r"function", r"\text{a set of pairs, one for each input}"),
                (r"integers, rationals", r"\text{pairs of naturals; pairs of integers, up to equivalence}"),
                (r"real numbers \ (Dedekind 1872)", r"\text{cuts: downward-closed sets of rationals}")]
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.9 - 0.8 * i
            l1 = label(a, font_size=24, color=GOAL)
            l2 = MathTex(b, font_size=30)
            l1.move_to([-6.2 + l1.width / 2, y, 0])
            l2.move_to([-1.4 + l2.width / 2, y, 0])
            tab.add(VGroup(l1, l2))
        k = d["kuratowski"]
        chk = label(rf"the Reasoner: \ $(a, b) = (c, d)$ only if $a = c$ and $b = d$, \ on all {k['pairs']} pairs of "
                    rf"the first {k['n']} sets $\checkmark$", font_size=22, color=OK).next_to(tab, DOWN, buff=0.4)
        chk.set_x(0)
        zv = VGroup(label(r"but which sets \textit{are} the numbers?", font_size=26, color=BAD),
                    MathTex(r"\text{von Neumann: } 2 = \{\varnothing, \{\varnothing\}\} \qquad "
                            r"\text{Zermelo: } 2 = \{\{\varnothing\}\}", font_size=30),
                    label(r"both work; \ Benacerraf (1965) asks what that means \ (Part 9)", font_size=22,
                          color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        assert k["ok"]
        with self.voiceover(
            "With sets in hand, the rest of mathematics follows. <bookmark mark='a'/>An ordered pair a, b can be "
            "coded as the set of a alone and a with b: Kuratowski's trick of 1921, which the Reasoner checks on all "
            f"{k['pairs']} pairs of the first sixteen sets. <bookmark mark='b'/>A function is a set of pairs. "
            "Integers and fractions are pairs, up to equivalence. And real numbers are Dedekind's cuts, sets of "
            "rationals. <bookmark mark='c'/>But notice something strange. Zermelo had his own numbers: two was the "
            "set containing the set containing nothing. Both codings work perfectly. So which set is the number "
            "two? Paul Benacerraf turned that question into an argument, in 1965, and Part 9 takes it up."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(chk))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tab[1:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(zv))
        self.clear_scene()
