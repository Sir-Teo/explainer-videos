from __future__ import annotations

import math

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Beavers(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Busy beavers", r"How long can a small machine run, and still stop?",
                            lit=(1962, 2024), part=PART)
        with self.voiceover("Chapter ten. Busy beavers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definition()
        self.search()
        self.table()
        self.edge()

    def definition(self):
        hc = history_card(1962, r"Tibor Radó", r"`On non-computable functions'", width=5.6, color=HIST).to_corner(
            UL, buff=0.35)
        dc = definition_card(r"the busy beaver function", r"$\mathrm{BB}(n)$: \ the largest number of steps that an "
                             r"$n$-state machine, \ started on a blank tape, \ can take \ \textit{and then halt}",
                             width=10.0, font_size=26, color=P.CLAIM).move_to([0, 0.4, 0])
        why = VGroup(label(r"if $\mathrm{BB}$ were computable, \ halting would be decidable:", font_size=26),
                     label(r"run an $n$-state machine for $\mathrm{BB}(n)$ steps; \ if it has not stopped, \ it never "
                           r"will", font_size=26, color=GOAL),
                     label(r"so $\mathrm{BB}$ grows faster than every computable function", font_size=26,
                           color=BAD)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1962 Tibor Radó turned the halting problem into a game. <bookmark mark='a'/>Among all machines with n "
            "states, started on a blank tape, find the one that runs longest and then halts. Its number of steps is "
            "the busy beaver number, BB of n. <bookmark mark='b'/>It is a perfectly definite number for each n, yet "
            "no program computes it. If one did, you could decide halting: run any n-state machine for BB of n "
            "steps, and if it has not stopped by then, it never will. <bookmark mark='c'/>So BB grows faster than "
            "every computable function, faster than Ackermann's, faster than anything you can write down a program "
            "for."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(dc))
            vo.wait_until("b")
            self.play(FadeIn(why[0]), FadeIn(why[1]))
            vo.wait_until("c")
            self.play(FadeIn(why[2]))
        self.clear_scene()

    def search(self):
        d = load("tm")["search"]
        head = label(r"The Reasoner plays the game for two states", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(rf"every two-state machine: \ $12^4 = {d['machines']:,}$".replace(",", "{,}"), font_size=30),
            label(rf"run each for 50 steps: \ {d['halting']:,} halt".replace(",", "{,}"), font_size=30),
            label(rf"the longest halting run: \ {d['max_steps']} steps; \ the most ones: \ {d['max_ones']}",
                  font_size=30, color=OK)).arrange(DOWN, buff=0.45).move_to([0, 0.6, 0])
        but = label(r"but why stop at 50? \ a machine still running might halt at step 51, \ or never", font_size=26,
                    color=BAD).to_edge(DOWN, buff=1.0)
        fix = label(r"for two states, \ every non-halting machine can be \textit{proved} to loop: \ BB(2) = 6",
                    font_size=26, color=GOAL).next_to(but, DOWN, buff=0.25)
        with self.voiceover(
            "For two states, the Reasoner can play the game outright. <bookmark mark='a'/>Each of the four rules has "
            "twelve choices, so there are twenty thousand, seven hundred and thirty-six machines. "
            "<bookmark mark='b'/>Run each for fifty steps, and nine thousand, seven hundred and eighty-four of them "
            "halt. <bookmark mark='c'/>The longest halting run is six steps; the most ones, four: the machine of the "
            "last chapter. <bookmark mark='d'/>But this is where the difficulty lives. A machine still running at "
            "step fifty might halt at step fifty-one. To know the champion, you must prove of every other machine "
            "that it never halts. For two states that is easy: each one visibly loops."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(but))
            self.play(FadeIn(fix))
        self.clear_scene()

    def table(self):
        d = load("beavers")
        head = label(r"The champions, \ simulated", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = [(1, 1, 1, r"trivial")]
        for c in d["champions"]:
            rows.append((c["n"], c["steps"], c["ones"], {2: r"Radó 1962", 3: r"Lin \& Radó 1965",
                                                        4: r"Brady 1983", 5: r"bbchallenge 2024"}[c["n"]]))
        bars = VGroup()
        base_y, x0 = -2.4, -5.4
        for i, (n, steps, ones, who) in enumerate(rows):
            h = 0.36 * math.log10(steps) + 0.08
            x = x0 + i * 1.7
            b = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=TAPE if n < 5 else GOAL,
                          fill_opacity=0.8).move_to([x, base_y + h / 2, 0])
            lab_n = MathTex(rf"n = {n}", font_size=26).next_to(b, DOWN, buff=0.15)
            val = MathTex(f"{steps:,}".replace(",", "{,}"), font_size=24 if n < 5 else 26,
                          color=WHITE if n < 5 else GOAL).next_to(b, UP, buff=0.12)
            wl = label(who, font_size=18, color=GREY_B).next_to(lab_n, DOWN, buff=0.1)
            bars.add(VGroup(b, lab_n, val, wl))
        six_x = x0 + 5 * 1.7
        six = VGroup(Arrow([six_x, base_y, 0], [six_x, 2.3, 0], buff=0, color=BAD, stroke_width=6,
                           max_tip_length_to_length_ratio=0.06),
                     MathTex(r"n = 6", font_size=26).move_to([six_x, base_y - 0.32, 0]),
                     label(r"$> 10 \uparrow\uparrow 15$ \ (2022)", font_size=22, color=BAD).move_to(
                         [six_x, 2.65, 0]))
        axis = Line([x0 - 0.8, base_y, 0], [six_x + 0.8, base_y, 0], color=GREY_C)
        sc = label(r"bar height: \ number of digits", font_size=20, color=GREY_B).move_to([-3.6, 2.0, 0])
        five = label(r"BB(5) = 47{,}176{,}870: \ the Reasoner runs the champion in seconds, \ leaving 4{,}098 ones",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.2)
        assert d["champions"][-1]["steps"] == 47176870
        with self.voiceover(
            "Here are the champions, each simulated by the Reasoner. <bookmark mark='a'/>One state: one step. Two "
            "states: six. Three: twenty-one, found by Shen Lin and Radó. Four: a hundred and seven, Brady's "
            "machine. <bookmark mark='b'/>Five: forty-seven million, one hundred and seventy-six thousand, eight "
            "hundred and seventy steps. The machine was found in 1989 by Heiner Marxen and Jürgen Buntrock; that "
            "nothing beats it was proved only in 2024, by an online collaboration, the Busy Beaver Challenge, which "
            "classified every five-state machine and checked the proof in the Coq proof assistant. The Reasoner "
            "runs the champion in a few seconds, and it halts, leaving four thousand and ninety-eight ones. "
            "<bookmark mark='c'/>Six states: a machine found in 2022 runs for more steps than a tower of fifteen "
            "tens. The true value is unknown."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(sc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[:4]], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(bars[4], shift=UP * 0.2), FadeIn(five))
            vo.wait_until("c")
            self.play(GrowArrow(six[0]), FadeIn(six[1]), FadeIn(six[2]))
        self.clear_scene()

    def edge(self):
        head = label(r"The edge of the knowable", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"six states: \ some machines halt iff a Collatz-like problem has a certain answer \ "
                  r"(`Antihydra', 2024)", font_size=24),
            label(r"small machines halt iff Goldbach's conjecture fails, \ or the Riemann hypothesis", font_size=24),
            label(r"Yedidia \& Aaronson (2016): \ a 7{,}918-state machine that halts iff ZFC is inconsistent",
                  font_size=24, color=GOAL),
            label(r"so ZFC cannot determine $\mathrm{BB}(7918)$; \ the bound is now below 750 states", font_size=24,
                  color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.3, 0])
        moral = label(r"a definite number, \ each of whose values is a theorem, \ until the theorems run out",
                      font_size=26, color=SELF).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Beyond five states, the busy beaver runs into open mathematics. <bookmark mark='a'/>Among the six-state "
            "machines are some, nicknamed cryptids, whose halting turns on Collatz-like problems no one can solve. "
            "<bookmark mark='b'/>Small machines can be built that halt if and only if Goldbach's conjecture is false, "
            "or the Riemann hypothesis. <bookmark mark='c'/>And in 2016 Adam Yedidia and Scott Aaronson built a "
            "machine with seven thousand, nine hundred and eighteen states that halts if and only if ZFC is "
            "inconsistent. <bookmark mark='d'/>By Gödel's second theorem, ZFC cannot prove that it never halts, so "
            "ZFC cannot determine that busy beaver number. Later work has brought the bound below seven hundred and "
            "fifty states. <bookmark mark='e'/>Each value of BB is a definite number, and each is a theorem, until, "
            "somewhere between six and seven hundred and fifty, the theorems run out."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()
