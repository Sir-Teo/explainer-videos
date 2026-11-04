from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import COST, CTRL, DATA, HEAD, HIST, NO, PART, YES

MACHINES = [
    (1937, r"Stibitz's Model K", r"a relay adder on a kitchen table, \ Bell Labs"),
    (1938, r"Zuse's Z1", r"binary, \ mechanical, \ Berlin"),
    (1941, r"Zuse's Z3", r"2{,}600 relays: \ the first working programmable computer"),
    (1942, r"Atanasoff--Berry", r"vacuum tubes, \ binary arithmetic, \ capacitor memory"),
    (1944, r"Colossus", r"Bletchley Park: \ tubes, \ breaking Lorenz ciphers"),
    (1945, r"ENIAC", r"17{,}468 tubes, \ 150 kW"),
]

CHIPS = [(1971, 2300, r"4004"), (1978, 29000, r"8086"), (1985, 275000, r"386"), (1993, 3.1e6, r"Pentium"),
         (2000, 4.2e7, r"Pentium 4"), (2006, 2.91e8, r"Core 2"), (2011, 2.27e9, r"Core i7"), (2020, 1.6e10, r"M1"),
         (2022, 8.0e10, r"H100"), (2024, 2.08e11, r"B200")]


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.z3()
        self.moore()

    def card(self):
        card = chapter_card(13, r"Machines of switches", r"Who built the first computers out of switches?",
                            lit=(1941, 1944, 1945, 1947, 1958, 1965), part=PART)
        with self.voiceover("Chapter thirteen. Machines of switches."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def machines(self):
        head = label(r"Relays, \ then tubes", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup()
        for i, (y, name, what) in enumerate(MACHINES):
            r = VGroup(label(str(y), font_size=30, color=HIST), label(name, font_size=28, color=CTRL),
                       label(what, font_size=24, color=GREY_A))
            r[0].move_to([-6.0, 2.1 - 0.85 * i, 0], aligned_edge=LEFT)
            r[1].move_to([-4.6, 2.1 - 0.85 * i, 0], aligned_edge=LEFT)
            r[2].move_to([-0.8, 2.1 - 0.85 * i, 0], aligned_edge=LEFT)
            rows.add(r)
        foot = note(r"each was built from the same three ideas: \ binary, \ switches, \ and Boole's algebra",
                    font_size=24, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Shannon's thesis arrived just as people started building computers from switches. "
            "<bookmark mark='a'/> In 1937 George Stibitz at Bell Labs wired a relay adder on his kitchen table. In "
            "Berlin, Konrad Zuse built the Z1, binary and mechanical, and then in 1941 the Z3, with two thousand six "
            "hundred relays, the first working programmable computer. In Iowa, John Atanasoff and Clifford Berry built "
            "an electronic calculator with vacuum tubes. At Bletchley Park, Colossus used tubes to break German "
            "teleprinter ciphers. And in Philadelphia, ENIAC used seventeen and a half thousand of them and a hundred "
            "and fifty kilowatts. <bookmark mark='b'/> Different countries, different purposes, mostly in secret, and "
            "all built on the same ideas: binary, switches, and Boole's algebra."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def z3(self):
        head = label(r"Two machines, \ closer up", font_size=38).to_edge(UP, buff=0.35)
        z = VGroup(label(r"Zuse's Z3 \ (1941)", font_size=30, color=CTRL),
                   label(r"22-bit binary floating point", font_size=24, color=GREY_A),
                   label(r"about 5 additions a second", font_size=24, color=GREY_A),
                   label(r"programs on punched cinema film", font_size=24, color=GREY_A),
                   label(r"destroyed in a 1943 air raid;", font_size=22, color=GREY_B),
                   label(r"shown Turing-complete in 1998 \ (Rojas), \ in principle", font_size=22, color=GREY_B)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        z.move_to(LEFT * 3.6 + UP * 0.3, aligned_edge=LEFT).to_edge(LEFT, buff=0.6)
        e = VGroup(label(r"ENIAC \ (1945)", font_size=30, color=CTRL),
                   label(r"decimal, \ 5{,}000 additions a second", font_size=24, color=GREY_A),
                   label(r"programmed by plugging cables \ and setting switches:", font_size=24, color=GREY_A),
                   label(r"days per program", font_size=24, color=GREY_A),
                   label(r"its first programmers:", font_size=22, color=HIST),
                   label(r"Kay McNulty, \ Betty Jennings, \ Betty Snyder,", font_size=22, color=HIST),
                   label(r"Marlyn Wescoff, \ Fran Bilas, \ Ruth Lichterman", font_size=22, color=HIST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        e.move_to(RIGHT * 0.6 + UP * 0.3, aligned_edge=LEFT)
        z.align_to(e, UP)
        sep = DashedLine(UP * 1.8 + RIGHT * 0.1, DOWN * 1.6 + RIGHT * 0.1, color=GREY_D, stroke_width=1.5)
        foot = label(r"what both lacked: \ the program stored in the machine's own memory \ (Part 6)", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two of these machines are worth a closer look. <bookmark mark='a'/> Zuse's Z3 worked in binary floating "
            "point, twenty-two bits per number, and managed about five additions a second. Its program was punched "
            "into discarded cinema film. It was destroyed in an air raid in 1943, and in 1998 Raúl Rojas showed that, "
            "with some contortions, it could in principle compute anything a Turing machine can. "
            "<bookmark mark='b'/> ENIAC was decimal and a thousand times faster, but it was programmed by plugging "
            "cables and setting switches, which could take days. The six women who first worked out how to do that, "
            "Kay McNulty, Betty Jennings, Betty Snyder, Marlyn Wescoff, Fran Bilas and Ruth Lichterman, were for decades "
            "left out of its history. <bookmark mark='c'/> What both machines lacked was the idea of Part 1's "
            "universal machine: a program stored as data in the computer's own memory. Part 6 gives Pebble exactly that."
        ) as vo:
            self.play(FadeIn(head), Create(sep))
            vo.wait_until("a")
            self.play(FadeIn(z, lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(e, lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moore(self):
        head = label(r"Moore's law", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[1970, 2026, 10], y_range=[3, 12, 1], x_length=8.2, y_length=4.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18},
                  x_axis_config={"numbers_to_include": [1970, 1980, 1990, 2000, 2010, 2020],
                                 "decimal_number_config": {"group_with_commas": False, "num_decimal_places": 0}},
                  y_axis_config={"numbers_to_include": list(range(3, 13))}).move_to(LEFT * 1.4 + DOWN * 0.3)
        yl = note(r"$\log_{10}$ transistors per chip", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        dots = VGroup()
        labs = VGroup()
        for y, n, nm in CHIPS:
            p = ax.c2p(y, np.log10(n))
            dots.add(Dot(p, radius=0.08, color=COST))
            labs.add(label(nm, font_size=18, color=GREY_A).next_to(p, UL, buff=0.05))
        trend = ax.plot(lambda t: np.log10(2300) + (t - 1971) * np.log10(2) / 2, x_range=[1971, 2024],
                        color=YES, stroke_width=2.5)
        tl = label(r"doubling every two years", font_size=26, color=YES).next_to(ax.c2p(2004, 7.0), DR, buff=0.1)
        hc = history_card(1965, r"Gordon Moore", r"``Cramming more components onto integrated circuits'': \ the count "
                          r"doubles every year \ (revised in 1975 to every two)", width=3.9, font_size=22).move_to(
            RIGHT * 4.8 + UP * 1.0)
        end = note(r"2,300 transistors in 1971; \ about 200 billion in 2024: \ every one a switch from chapter three",
                   font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Then came the transistor in 1947 and the integrated circuit in 1958, and the switches started shrinking. "
            "<bookmark mark='a'/> In 1965 Gordon Moore, later a founder of Intel, noticed that the number of "
            "transistors on a chip was doubling every year, and predicted it would continue; in 1975 he revised it to "
            "every two years. <bookmark mark='b'/> Here are some landmark chips on a logarithmic scale, from Intel's "
            "4004 in 1971, with two thousand three hundred transistors, to GPUs of 2024 with about two hundred billion. "
            "<bookmark mark='c'/> Half a century of doubling every two years, almost exactly on the line. Each of those "
            "transistors is the switch of chapter three, and each chip is, at heart, Shannon's algebra."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.15), FadeIn(labs), run_time=2.4)
            vo.wait_until("c")
            self.play(Create(trend), FadeIn(tl), FadeIn(end))
        self.wait(0.3)
        self.clear_scene()
