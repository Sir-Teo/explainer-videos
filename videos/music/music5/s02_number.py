from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Number(SoundScene):
    def construct(self):
        chapter(self, 1, r"Number", r"Is consonance a property of the ratio?", lit=(-530,), extra=((1739, r"Euler's \textit{Tentamen}"),))
        self.pythagoras()
        self.euler()
        self.table()
        self.test()

    # ------------------------------------------------------------------
    def pythagoras(self):
        line = Line(LEFT * 5.0, RIGHT * 5.0, color=STR, stroke_width=4).move_to(UP * 2.2)
        ends = VGroup(Dot(line.get_start(), radius=0.08, color=GREY_B), Dot(line.get_end(), radius=0.08, color=GREY_B))
        stops = VGroup()
        for frac, name, ratio in ((1 / 2, r"octave", r"2 : 1"), (2 / 3, r"fifth", r"3 : 2"), (3 / 4, r"fourth", r"4 : 3")):
            x = line.get_start() + RIGHT * 10.0 * frac
            stops.add(VGroup(Triangle(color=RATIO, fill_color=RATIO, fill_opacity=0.9).scale(0.14).next_to(x, DOWN, buff=0.02),
                             label(name, font_size=24, color=GREY_A).next_to(x, DOWN, buff=0.4),
                             MathTex(ratio, font_size=30, color=RATIO).next_to(x, DOWN, buff=0.78)))
        dots = VGroup(*[VGroup(*[Dot(radius=0.11, color=RATIO) for _ in range(k)]).arrange(RIGHT, buff=0.22) for k in (1, 2, 3, 4)]).arrange(DOWN, buff=0.2)
        dots.move_to(LEFT * 5.0 + DOWN * 1.4)
        tl = label(r"1, 2, 3, 4: \ the tetractys", font_size=24, color=GREY_A).next_to(dots, DOWN, buff=0.3)
        claim = VGroup(label(r"the Pythagoreans: \ consonance \emph{is} small whole numbers", font_size=30, color=HIST),
                       label(r"by 1558 (Zarlino): \ the numbers up to 6, \\ which adds the thirds, \ 5 : 4 and 6 : 5", font_size=26, color=GREY_A)
                       ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 1.6 + DOWN * 1.5)
        with self.voiceover(
            "Part 1 began where the science of music began: with a string and a movable bridge. "
            "<bookmark mark='a'/> Stop the string at half its length, and the two parts sound an octave apart. At "
            "two thirds, a fifth. At three quarters, a fourth. Two to one, three to two, four to three. "
            "<bookmark mark='b'/> The Pythagoreans noticed that these use only the numbers one, two, three and "
            "four, which add up to ten and can be laid out as a triangle. They concluded that consonance simply "
            "is small whole numbers, and that the universe is built on the same plan. <bookmark mark='c'/> Two "
            "thousand years later, when thirds had become the sweetest sounds in music, theorists stretched the "
            "rule to the numbers up to six, which lets in five to four and six to five. The rule changed. The "
            "idea did not: the simpler the ratio, the sweeter the sound."
        ) as vo:
            self.play(Create(line), FadeIn(ends))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in stops], lag_ratio=0.8), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in dots], lag_ratio=0.3), FadeIn(tl), FadeIn(claim[0]))
            vo.wait_until("c")
            self.play(FadeIn(claim[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def euler(self):
        card = history_card(1739, r"Leonhard Euler, \ St Petersburg",
                            r"\textit{Tentamen novae theoriae musicae}: a number for how sweet an interval is. The lower the number, the sweeter.",
                            width=5.6).to_corner(UL, buff=0.4)
        rule = VGroup(label(r"take the smallest number that both sides of the ratio divide", font_size=26),
                      label(r"split it into primes", font_size=26),
                      label(r"add up each prime, \ less one; \ then add one", font_size=26)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).scale(0.92).move_to(RIGHT * 3.1 + UP * 2.3)
        ex = VGroup(MathTex(r"3:2 \;\longrightarrow\; 6 = 2 \times 3", font_size=36),
                    MathTex(r"(2-1) + (3-1) + 1 \;=\; 4", font_size=36, color=GOOD)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.3 + UP * 0.3)
        ask = pause_card(r"Euler's number for the major third, \ 5 : 4?", width=6.2).move_to(DOWN * 1.9)
        ans = VGroup(MathTex(r"5:4 \;\longrightarrow\; 20 = 2 \times 2 \times 5", font_size=34),
                     MathTex(r"1 + 1 + 4 + 1 \;=\; 7", font_size=36, color=GOOD)).arrange(RIGHT, buff=0.8).move_to(DOWN * 1.9)
        with self.voiceover(
            "In 1739 Leonhard Euler, the most productive mathematician who ever lived, tried to make the idea "
            "exact. He wanted a single number for the sweetness of any interval. <bookmark mark='a'/> His recipe: "
            "take the smallest number that both sides of the ratio divide into. Split it into primes. Add up the "
            "primes, taking one off each, and add one at the end. <bookmark mark='b'/> For the fifth, three to "
            "two, the smallest common multiple is six, which is two times three. One, plus two, plus one: four. "
            "The lower the number, the sweeter the interval. <bookmark mark='c'/> Try it. What is Euler's number "
            "for the major third, five to four?"
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rule], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(ex[0]))
            self.play(FadeIn(ex[1]))
            vo.wait_until("c")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "Five and four both divide twenty, which is two times two times five. One, and one, and four, and "
            "one more: seven. A little less sweet than the fifth, which is what every musician would say."
        ):
            self.play(FadeOut(ask), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("number")
        rows = sorted(d["rows"], key=lambda r: (r["gradus"], r["cents"]))
        kind = {n: k for k, names in d["tradition"].items() for n in names}
        col = {"perfect": GOOD, "imperfect": TUNE, "dissonant": BAD}
        base = DOWN * 2.3 + LEFT * 5.9
        bars = VGroup()
        for i, r in enumerate(rows):
            h = 0.27 * r["gradus"]
            b = Rectangle(width=0.62, height=h, stroke_width=0, fill_color=col[kind[r["name"]]], fill_opacity=0.85).move_to(base + RIGHT * 0.98 * i + UP * h / 2)
            bars.add(VGroup(b, MathTex(rf"{r['p']}{{:}}{r['q']}", font_size=22, color=GREY_A).next_to(b, DOWN, buff=0.12),
                            label(str(r["gradus"]), font_size=24).next_to(b, UP, buff=0.08)))
        leg = VGroup(label(r"what musicians call them:", font_size=22, color=GREY_B), label(r"perfect consonances", font_size=22, color=GOOD),
                     label(r"imperfect consonances", font_size=22, color=TUNE), label(r"dissonances", font_size=22, color=BAD)
                     ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_corner(UL, buff=0.5)
        head = label(r"Euler's number for thirteen intervals", font_size=30, color=GREY_A).to_edge(UP, buff=0.45).shift(RIGHT * 1.5)
        nine = next(b for b, r in zip(bars, rows) if r["name"] == "major second")
        flaw = label(r"a whole tone, \ 9 : 8, \ scores the same as the minor third and the minor sixth", font_size=24, color=BAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here is Euler's number for thirteen intervals, in order, coloured by what musicians have called them "
            "for five hundred years. <bookmark mark='a'/> It is impressive. The octave scores two, the fifth four, "
            "the fourth five. Then come the thirds and sixths, at seven and eight. The dissonances are on the "
            "right, and last of all the tritone, at fourteen. A formula written by a mathematician has put "
            "almost everything in the order that ears had already chosen. <bookmark mark='b'/> Almost. The whole "
            "tone, nine to eight, scores eight: exactly as sweet as a minor third. No musician would agree. But "
            "that is a quibble. There is a much deeper problem, and it is the same for every theory built on "
            "ratios."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.12), run_time=5.0)
            vo.wait_until("b")
            self.play(Indicate(nine[0], color=WHITE, scale_factor=1.15), FadeIn(flaw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def test(self):
        d = load("number")
        c = clip("number.fifths")
        q = listen_card(r"Two fifths, \ A and B. \ One is exactly 3 to 2. \ The other is not. \\ Which is which? \ And how much worse is the other one?",
                        width=9.8).to_edge(UP, buff=0.45)
        bx = boxes(buff=1.8, width=3.0, height=1.5).move_to(DOWN * 0.5)
        with self.voiceover(
            "Here is the test. Two fifths. One of them is exactly three to two. The other is not. Which is "
            "which, and how much worse does the other one sound?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"fifth A, \ then fifth B", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("pure", "wide"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.6)
        p, qq = d["wide_ratio"]
        ans = VGroup(VGroup(MathTex(r"3 : 2", font_size=40, color=GOOD), label(rf"Euler's number: \ {d['pure_gradus']}", font_size=26)).arrange(DOWN, buff=0.15).next_to(bx[0], DOWN, buff=0.3),
                     VGroup(MathTex(rf"\approx {p} : {qq}", font_size=40, color=BAD), label(rf"Euler's number: \ {d['wide_gradus']}", font_size=26),
                            label(rf"{d['wide_cents']:.0f} cents wide: \ a slow swell, \ {d['wide_beat']:.1f} times a second", font_size=22, color=GREY_A)
                            ).arrange(DOWN, buff=0.15).next_to(bx[1], DOWN, buff=0.3))
        moral = label(r"a small change in the sound cannot be a huge change in its sweetness", font_size=30, color=EAR).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A was the pure one. B is five hundredths of a semitone too wide, and if you listened closely you "
            f"heard it swell and fade, about {say(d['wide_beat'], 1)} times a second. But it is plainly still a "
            "fifth, and hardly any worse. <bookmark mark='a'/> Now ask the arithmetic. The nearest simple "
            f"fraction to B's ratio is {p} to {qq}. Euler's number leaps from {d['pure_gradus']} to "
            f"{d['wide_gradus']}. <bookmark mark='b'/> According to every theory of ratios, B should be one of "
            "the ugliest sounds imaginable, and a fifth that was off by a millionth of a semitone would be "
            "uglier still. That cannot be right. A small change in a sound cannot be a huge change in its "
            "sweetness. And no instrument has ever played an exact ratio anyway. Whatever the ear is doing, it is "
            "not arithmetic on whole numbers. It must be something smooth, something that can be a little bit "
            "off. We need a physical cause."
        ) as vo:
            self.play(FadeOut(q), bx.animate.shift(UP * 1.7))
            for a in ans:
                a.shift(UP * 1.7)
            self.play(FadeIn(ans[0]), FadeIn(ans[1][2]))
            vo.wait_until("a")
            self.play(FadeIn(ans[1][0]), FadeIn(ans[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(moral))
        self.wait(0.3)
        self.clear_scene()
