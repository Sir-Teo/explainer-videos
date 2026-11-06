from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load)


class Puzzles(VoiceoverScene):
    def construct(self):
        self.card()
        self.keys()
        self.puzzles()
        self.secret_history()

    def card(self):
        card = chapter_card(1, r"Key distribution and Merkle's puzzles", r"Can two strangers ever share a secret?",
                            lit=(1974, 1976), extra=((1974, r"Merkle's puzzles"),), part=PART)
        with self.voiceover("Chapter one. Key distribution, and Merkle's puzzles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def keys(self):
        head = label(r"Every pair needs its own key", font_size=34).to_edge(UP, buff=0.3)
        n = 8
        pts = [np.array([-3.0 + 1.9 * math.cos(2 * math.pi * i / n + 0.3), 0.6 + 1.9 * math.sin(2 * math.pi * i / n +
                                                                                                 0.3), 0])
               for i in range(n)]
        dots = VGroup(*[Dot(p, radius=0.13, color=DATA) for p in pts])
        edges = VGroup(*[Line(pts[i], pts[j], stroke_width=1.6, color=HEAD) for i in range(n) for j in range(i + 1, n)])
        notes = VGroup(
            label(r"$n$ people: \ $\binom{n}{2} = n(n-1)/2$ keys", font_size=24, color=HEAD),
            label(r"8 people: \ 28 keys; \ a million: \\ 500 billion", font_size=22, color=WHITE),
            label(r"each delivered in person, \\ by courier, \ in advance", font_size=22, color=GREY_A),
            label(r"a trusted centre helps \\ \ (Kerberos, \ Part 55), \\ but it can read everything", font_size=22,
                  color=NO),
            label(r"the internet: \ billions of strangers \\ who need a key \textbf{now}", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.3, 0])
        with self.voiceover(
            "Everything in Part 29 assumed that the two sides already shared a key. Where does it come from? "
            "<bookmark mark='a'/> If every pair of people needs its own key, n people need n times n minus one over "
            "two keys. Eight people need twenty-eight; a million need five hundred billion. <bookmark mark='b'/> For "
            "most of history each key was carried by hand, by courier, before any message could be sent. Governments "
            "ran fleets of couriers carrying key material. <bookmark mark='c'/> A trusted centre that shares a key "
            "with everyone reduces the count, and Kerberos, in Part 55, works this way; but the centre can read "
            "everything. <bookmark mark='d'/> On the internet, strangers meet billions of times a day, and need a "
            "key immediately."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(notes[0]), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def puzzles(self):
        d = load("puzzles")
        head = label(r"Merkle's puzzles: \ the first public key exchange", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ Alice makes $n$ puzzles, \ each a (number, key) pair locked under a weak key that takes $n$ "
                  r"tries to find", font_size=21, color=WHITE),
            label(r"2. \ Bob picks one puzzle at random and solves it: \ about $n$ work; \ he announces its number",
                  font_size=21, color=HEAD),
            label(r"3. \ Alice looks the number up: \ both now hold that puzzle's key", font_size=21, color=DATA),
            label(r"4. \ Eve doesn't know which puzzle: \ she must solve about half of them: \ $n^2/4$ work",
                  font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.45)
        tab = grid_table([r"puzzles $n$", r"Bob's tries \ (measured)", r"Eve's work \ ($n^2/4$)", r"agreed?"],
                         [[f"{r['n']:,}", f"{r['bob']:,}", f"{r['eve']:,}", "yes" if r["agreed"] else "no"]
                          for r in d["rows"]], widths=[2.0, 3.0, 3.0, 1.4], row_h=0.5, font_size=21,
                         mono_cols=(0, 1, 2, 3))
        tab.next_to(steps, DOWN, buff=0.45)
        lines = VGroup(
            label(r"only a \textbf{quadratic} gap: \ a billion puzzles for Bob means a billion billion for Eve",
                  font_size=21, color=YES),
            label(r"Barak and Mahmoody \ (2009): \ with hash functions alone, \ quadratic is the best possible",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1974 Ralph Merkle, an undergraduate at Berkeley, proposed a way out, in a course project his "
            "professor didn't understand. <bookmark mark='a'/> Alice makes many puzzles. Each holds an identifying "
            "number and a key, locked under a deliberately weak key that takes some effort to find. <bookmark "
            "mark='b'/> Bob picks one puzzle at random, solves it, and announces its number in public. <bookmark "
            "mark='c'/> Alice looks up which key that number belongs to. Now they share it. <bookmark mark='d'/> Eve "
            "hears the number, but doesn't know which puzzle it came from, so she has to solve puzzles until she finds "
            "it: about half of them. <bookmark mark='e'/> We ran it. Bob does work proportional to n; Eve's work grows "
            "as n squared. <bookmark mark='f'/> That gap is only quadratic: a determined Eve with a big computer "
            "catches up. <bookmark mark='g'/> And it cannot be improved using only hash-like functions, as Boaz Barak "
            "and Mohammad Mahmoody proved in 2009. A real public-key system needs mathematical structure."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(tab))
            vo.wait_until("f")
            self.play(FadeIn(lines[0]))
            vo.wait_until("g")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def secret_history(self):
        head = label(r"Discovered twice", font_size=34).to_edge(UP, buff=0.35)
        rows = [(r"1970", r"James Ellis, \ GCHQ: \ ``non-secret encryption'' is possible", GREY_A),
                (r"1973", r"Clifford Cocks, \ GCHQ: \ a scheme with primes: \ RSA, \ four years early", NO),
                (r"1974", r"Malcolm Williamson, \ GCHQ: \ the Diffie--Hellman exchange", HEAD),
                (r"1976", r"Diffie and Hellman, \ Stanford: \ \textit{New Directions in Cryptography}", DATA),
                (r"1977", r"Rivest, \ Shamir and Adleman, \ MIT: \ RSA", YES),
                (r"1997", r"GCHQ declassifies its work", LAM)]
        tl = VGroup()
        for i, (y, t, c) in enumerate(rows):
            tl.add(VGroup(label(y, font_size=24, color=c), label(t, font_size=22, color=WHITE)).arrange(RIGHT, buff=0.5))
        tl.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        note = label(r"public-key cryptography: \ a key you can publish, \ for a secret only you can open",
                     font_size=23, color=YES).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The structure was found twice. <bookmark mark='a'/> At GCHQ, the British signals agency, James Ellis "
            "argued in 1970 that encryption without a shared secret was possible. Clifford Cocks, a young "
            "mathematician, found a way in 1973: essentially RSA. Malcolm Williamson found the Diffie-Hellman exchange "
            "in 1974. All of it stayed classified. <bookmark mark='b'/> In public, Diffie and Hellman published in "
            "1976, and Rivest, Shamir and Adleman at MIT found RSA in 1977. GCHQ told its story only in 1997. "
            "<bookmark mark='c'/> The idea in both: a key you can publish to the world, which locks a secret that "
            "only you can open. The next two chapters build the mathematics it needs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tl[:3]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tl[3:]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
