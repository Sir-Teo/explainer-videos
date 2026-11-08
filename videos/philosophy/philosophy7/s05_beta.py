from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Beta(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"An ancient theorem in a modern proof", r"How can one number hold a whole list?",
                            lit=(1247,), part=PART)
        with self.voiceover("Chapter four. An ancient theorem, in a modern proof."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.sunzi()
        self.beta()

    def problem(self):
        head = label(r"The problem: \ recursion needs lists", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        a = MathTex(r"x! = y \iff \text{there is a list } 1, 1, 2, 6, \dots, y \text{ where each term is the last "
                    r"times the next number}", font_size=30).move_to([0, 1.2, 0])
        b = label(r"but the language of arithmetic has only $0, \ \mathsf{S}, \ +, \ \times$: \ no lists", font_size=28,
                  color=BAD).next_to(a, DOWN, buff=0.6)
        c = label(r"Gödel's trick: \ code any finite list by two numbers, \ using remainders", font_size=28,
                  color=GOAL).next_to(b, DOWN, buff=0.6)
        with self.voiceover(
            "To express a recursion in arithmetic, Gödel faced a problem. <bookmark mark='a'/>Saying that y is "
            "x factorial means saying there is a list, one, one, two, six, and so on up to y, in which each term "
            "is the last one times the next number. <bookmark mark='b'/>But the language of arithmetic has zero, "
            "successor, plus and times. It has no lists. <bookmark mark='c'/>His solution was to code any finite "
            "list by just two numbers, using remainders, and the theorem that makes it work is one of the oldest "
            "in mathematics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(c))
        self.clear_scene()

    def sunzi(self):
        d = load("beta")
        x, M = d["sunzi"]["x"], d["sunzi"]["M"]
        hc = history_card(r"c.\ 400", r"\textit{Sunzi Suanjing} \ (The Mathematical Classic of Master Sun)",
                          r"`there are things whose number is unknown'", width=7.4, color=HIST).to_corner(UL, buff=0.35)
        conds = VGroup(*[MathTex(rf"x \equiv {r} \pmod{{{m}}}", font_size=34) for r, m in d["sunzi"]["pairs"]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([-4.2, 0.2, 0])
        # dots 0..34, highlight the solution
        cols = [(3, TAPE), (5, PROV), (7, NUM)]
        rows = VGroup()
        for k, ((r, m), (_, col)) in enumerate(zip(d["sunzi"]["pairs"], cols)):
            dots = VGroup()
            for n in range(0, 36):
                ok = n % m == r
                dots.add(Dot([-1.0 + 0.2 * n, 0.9 - 0.55 * k, 0], radius=0.07 if ok else 0.04,
                             color=col if ok else GREY_D))
            rows.add(dots)
        xs = VGroup(*[MathTex(str(n), font_size=18, color=GREY_B).move_to([-1.0 + 0.2 * n, -0.9, 0])
                      for n in range(0, 36, 5)])
        col_x = Rectangle(width=0.18, height=1.8, stroke_color=GOAL, stroke_width=2.5).move_to(
            [-1.0 + 0.2 * x, 0.35, 0])
        ans = label(rf"answer: \ ${x}$, \ and every number ${x} + {M}k$", font_size=28, color=GOAL).move_to([2.6, -1.3, 0])
        crt = theorem_card(r"the Chinese remainder theorem", r"if the moduli share no factor, \ any remainders "
                           r"can be met at once, \ by exactly one number below their product", width=10.4,
                           font_size=24).to_edge(DOWN, buff=0.2)
        qin = label(r"a general method: \ Qin Jiushao, \ 1247", font_size=22, color=GREY_A).next_to(ans, DOWN,
                                                                                                    buff=0.12)
        with self.voiceover(
            "Around the year 400, the Mathematical Classic of Master Sun posed a puzzle. "
            "<bookmark mark='a'/>There are things whose number is unknown. Counted by threes, two are left over; "
            "by fives, three; by sevens, two. How many things are there? <bookmark mark='b'/>Mark the numbers that "
            "leave two by threes, three by fives, two by sevens. <bookmark mark='c'/>The first number marked in "
            "all three rows is twenty-three, and the pattern repeats every hundred and five. "
            "<bookmark mark='d'/>In general, if the moduli share no common factor, any remainders at all can be met "
            "at once. Qin Jiushao gave a general method in 1247; today it is called the Chinese remainder theorem."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in conds], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), FadeIn(xs), run_time=3)
            vo.wait_until("c")
            self.play(Create(col_x), FadeIn(ans))
            vo.wait_until("d")
            self.play(FadeIn(crt), FadeIn(qin))
        self.clear_scene()

    def beta(self):
        d = load("beta")
        c, dd = d["c"], d["d"]
        head = label(r"Gödel's $\beta$-function", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        f = MathTex(r"\beta(c, d, i) \;=\; c \bmod \bigl(1 + (i + 1)\,d\bigr)", font_size=44, color=NUM).next_to(
            head, DOWN, buff=0.5)
        seq = label(r"to code the list $2, 3, 5$:", font_size=28).next_to(f, DOWN, buff=0.5)
        pick = MathTex(rf"d = 5! = {dd}, \quad \text{{moduli }} {d['mods'][0]},\ {d['mods'][1]},\ {d['mods'][2]}",
                       font_size=32).next_to(seq, DOWN, buff=0.35)
        cc = MathTex(rf"c = {gnum_tex(c)} \quad \text{{(the Chinese remainder theorem)}}", font_size=32,
                     color=GOAL).next_to(pick, DOWN, buff=0.3)
        checks = VGroup(*[MathTex(rf"\beta(c, d, {i}) = {c} \bmod {m} = {v}", font_size=30, color=OK)
                          for i, (m, v) in enumerate(zip(d["mods"], d["check"]))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).next_to(cc, DOWN, buff=0.4)
        moral = label(r"so `there is a list such that \dots' \ becomes \ `there are $c, d$ such that \dots': "
                      r"\ pure arithmetic", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        assert d["check"] == d["seq"]
        with self.voiceover(
            "Gödel turned the theorem into a coding device. <bookmark mark='a'/>His beta function takes two numbers "
            "c and d, and an index i, and returns the remainder of c on division by one plus i plus one times d. "
            "<bookmark mark='b'/>To code the list two, three, five, take d to be five factorial, a hundred and "
            "twenty. The moduli one hundred and twenty-one, two hundred and forty-one and three hundred and "
            "sixty-one share no factor, so the Chinese remainder theorem gives a number c with the right "
            "remainders. <bookmark mark='c'/>The Reasoner finds c, and checks: the remainders are two, three and "
            "five. <bookmark mark='d'/>So 'there is a list such that' becomes 'there are two numbers such that', "
            "and every recursion can be written with plus and times alone. A theorem from Master Sun sits inside "
            "the proof of incompleteness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(seq), FadeIn(pick))
            vo.wait_until("c")
            self.play(FadeIn(cc))
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in checks], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()
