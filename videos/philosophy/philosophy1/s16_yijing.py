from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403


class Yijing(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Leibniz and the Yijing", r"Did an old Chinese diagram contain binary arithmetic?",
                            lit=(1703,), part=PART)
        with self.voiceover("Chapter fifteen. Leibniz and the Yijing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.binary()
        self.hexes()
        self.trigrams()
        self.meaning()

    def binary(self):
        hc = history_card(1679, r"Leibniz, `De progressione dyadica'", r"all numbers from 0 and 1", width=5.4,
                          color=HIST).to_corner(UL, buff=0.4)
        rows = VGroup()
        for n in range(9):
            rows.add(MathTex(rf"{n}", r"\ =\ ", rf"{n:04b}", font_size=36))
        for r in rows:
            r[2].set_color(GOAL)
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.12).move_to([2.6, -0.3, 0])
        add = MathTex(r"0101 + 0011 = 1000", font_size=38, color=P.CLAIM).next_to(hc, DOWN, buff=0.8).align_to(hc, LEFT)
        al = label(r"$5 + 3 = 8$, by carrying", font_size=26, color=GREY_A).next_to(add, DOWN, buff=0.2).align_to(add,
                                                                                                         LEFT)
        boole = label(r"Boole's $x^2 = x$ (Part 2): the same two values", font_size=24, color=GREY_A).to_edge(DOWN,
                                                                                                     buff=0.4)
        with self.voiceover(
            "Leibniz had another idea that would outlive him. <bookmark mark='a'/>In 1679 he worked out arithmetic in "
            "base two: every number written with only zeros and ones. One is one; two is one-zero; three is "
            "one-one; four is one-zero-zero. <bookmark mark='b'/>Addition is just carrying: five plus three, "
            "zero-one-zero-one plus zero-zero-one-one, is one-zero-zero-zero, eight. He even sketched a machine "
            "that would calculate with marbles falling through holes. <bookmark mark='c'/>Two values, and rules "
            "for combining them: the same structure Boole would find in logic in 1854."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(add), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(boole))
        self.clear_scene()

    def hexes(self):
        d = load("hexagrams")["hexagrams"]
        grid = VGroup()
        for h in d:
            grid.add(hexagram(h["bits"], width=0.62, gap=0.07, stroke=0.06, color=WHITE))
        grid.arrange_in_grid(rows=8, cols=8, buff=(0.22, 0.2)).move_to([-2.8, -0.3, 0])
        nums = VGroup(*[MathTex(str(h["n"]), font_size=18, color=GOAL).move_to(g) for h, g in zip(d, grid)])
        hc = history_card(1701, r"Joachim Bouvet, Jesuit in Beijing", r"sends Leibniz Shao Yong's diagram of the 64 "
                          r"hexagrams (11th century)", width=5.2, color=HIST).to_corner(UR, buff=0.35)
        key = VGroup(VGroup(hexagram([1], width=0.8, stroke=0.1), MathTex(r"= 1", font_size=32)).arrange(RIGHT),
                     VGroup(hexagram([0], width=0.8, stroke=0.1), MathTex(r"= 0", font_size=32)).arrange(RIGHT)).arrange(
            DOWN, buff=0.3).next_to(hc, DOWN, buff=0.4)
        kl = label(r"yang (solid) $= 1$, \ yin (broken) $= 0$", font_size=22, color=GREY_A).next_to(key, DOWN, buff=0.2)
        pub = label(r"1703: \ \textit{Explication de l'arithmétique binaire}", font_size=24, color=HIST).next_to(
            kl, DOWN, buff=0.4)
        with self.voiceover(
            "In 1701 a Jesuit missionary in Beijing, Joachim Bouvet, sent Leibniz a Chinese diagram: the sixty-four "
            "hexagrams of the Yijing, the Book of Changes, in an order devised by the eleventh-century philosopher "
            "Shao Yong. <bookmark mark='a'/>Each hexagram is six lines, solid or broken. <bookmark mark='b'/>Leibniz "
            "saw at once that if a solid line is one and a broken line is zero, Shao Yong's order counts in binary, "
            "from zero to sixty-three. <bookmark mark='c'/>Here are all sixty-four, computed from the binary numerals "
            "themselves, with the number each one encodes. In 1703 Leibniz published his binary arithmetic, with the "
            "Chinese figures beside it."
        ) as vo:
            self.play(FadeIn(hc))
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.02), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(key), FadeIn(kl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Indicate(g, color=GOAL, scale_factor=1.15) for g in grid[:8]], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(*[g.animate.set_opacity(0.25) for g in grid], FadeIn(nums), FadeIn(pub))
        self.clear_scene()

    def meaning(self):
        claims = VGroup(
            label(r"what is exact: \ Shao Yong's order is the binary sequence $0 \dots 63$", font_size=28, color=OK),
            label(r"what is not: \ that the ancient sage Fuxi `knew' binary arithmetic", font_size=28, color=BAD),
            label(r"the Yijing is a book of divination; its order was a cosmological pattern", font_size=26,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.9, 0])
        cre = quote_card(r"One suffices to derive all out of nothing.", r"Leibniz's motto for binary "
                         r"(\textit{omnibus ex nihilo ducendis sufficit unum})", width=8.4, font_size=30)
        cre.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "What should we make of it? <bookmark mark='a'/>The correspondence is exact: Shao Yong's arrangement is "
            "the binary sequence. <bookmark mark='b'/>Leibniz went further, and claimed the legendary sage Fuxi had "
            "known binary arithmetic. That reading is not supported: the Yijing is a book of divination, and its "
            "order expressed a cosmology of yin and yang, not a numeral system. <bookmark mark='c'/>Leibniz loved "
            "binary for a theological reason too: one and nothing suffice to make everything, as God made the world "
            "from nothing. Three centuries later every computer runs on his two digits, and on Boole's two truth "
            "values."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(claims[0]))
            vo.wait_until("b")
            self.play(FadeIn(claims[1]), FadeIn(claims[2]))
            vo.wait_until("c")
            self.play(FadeIn(cre, shift=UP * 0.2))
        self.clear_scene()

    def trigrams(self):
        names = {7: "乾", 6: "兑", 5: "离", 4: "震", 3: "巽", 2: "坎", 1: "艮", 0: "坤"}
        en = {7: r"heaven", 6: r"lake", 5: r"fire", 4: r"thunder", 3: r"wind", 2: r"water", 1: r"mountain",
              0: r"earth"}
        from explainer.zh_text import cjk_font

        cards = VGroup()
        for n in range(7, -1, -1):
            bits = [(n >> 2) & 1, (n >> 1) & 1, n & 1]        # bottom line first, most significant
            h = hexagram(bits[::-1], width=0.8, gap=0.12, stroke=0.1)  # draw top line first
            t = VGroup(data_text(names[n], font=cjk_font(), font_size=28), label(en[n], font_size=18, color=GREY_A),
                       MathTex(f"{n:03b} = {n}", font_size=24, color=GOAL)).arrange(DOWN, buff=0.08)
            cards.add(VGroup(h, t).arrange(DOWN, buff=0.2))
        cards.arrange(RIGHT, buff=0.45).move_to([0, 0.2, 0])
        head = label(r"the eight trigrams, in Shao Yong's order: \ bottom line first, yang $= 1$", font_size=28,
                     color=GOAL).to_edge(UP, buff=0.5)
        cnt = label(r"$2^3 = 8$ trigrams; \ two of them stacked: $2^6 = 64$ hexagrams", font_size=26).to_edge(DOWN,
                                                                                                     buff=0.6)
        with self.voiceover(
            "The hexagrams are built from smaller pieces, the eight trigrams of three lines each: heaven, lake, fire, "
            "thunder, wind, water, mountain, earth. <bookmark mark='a'/>Read the bottom line as the first binary "
            "digit, a solid line as one, and Shao Yong's order runs seven, six, five, down to zero. "
            "<bookmark mark='b'/>Two trigrams stacked make a hexagram: two to the three is eight, two to the six is "
            "sixty-four."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c[0]) for c in cards], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cards], lag_ratio=0.12))
            vo.wait_until("b")
            self.play(FadeIn(cnt))
        self.clear_scene()
