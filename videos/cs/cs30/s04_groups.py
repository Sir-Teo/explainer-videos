from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class Groups(VoiceoverScene):
    def construct(self):
        self.card()
        self.cycle()
        self.lagrange()
        self.scatter()

    def card(self):
        card = chapter_card(3, r"Groups and the discrete logarithm", r"Which problems are easy one way only?",
                            lit=(1801, 1832), extra=((1832, r"Galois: \ groups"),), part=PART)
        with self.voiceover("Chapter three. Groups, and the discrete logarithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cycle(self):
        d = load("groups")
        p, g = d["p"], d["g"]
        head = label(rf"Powers of {g}, \ mod {p}", font_size=34).to_edge(UP, buff=0.3)
        c0 = np.array([-3.0, -0.2, 0])
        R = 2.5
        pos = {v: c0 + R * np.array([math.sin(2 * math.pi * (v - 1) / (p - 1)), math.cos(2 * math.pi * (v - 1) /
                                                                                       (p - 1)), 0])
               for v in range(1, p)}
        dots = VGroup(*[Dot(pos[v], radius=0.07, color=GREY_B) for v in range(1, p)])
        nums = VGroup(*[mono(str(v), 17, GREY_A).move_to(c0 + 1.13 * (pos[v] - c0)) for v in range(1, p)])
        powers = d["powers"]
        arrows = VGroup()
        for a, b in zip(powers, powers[1:] + powers[:1]):
            arrows.add(Arrow(pos[a], pos[b], buff=0.1, stroke_width=2, color=HEAD, max_tip_length_to_length_ratio=0.08))
        seq = mono(" ".join(str(x) for x in powers[:12]) + " ...", 20, HEAD)
        notes = VGroup(
            label(rf"$Z_{{{p}}}^*$: \ the nonzero numbers mod {p}, \\ under multiplication: \ a \textbf{{group}}",
                  font_size=22, color=WHITE),
            label(rf"${g}^0, {g}^1, {g}^2, \ldots$ \ visits all {p - 1} of them: \\ {g} is a \textbf{{generator}}",
                  font_size=22, color=HEAD),
            label(r"for every prime $p$, \ $Z_p^*$ is \textbf{cyclic}: \\ some $g$ generates it \ (Gauss)", font_size=22,
                  color=YES),
            label(r"$g^x$ is easy \ (chapter 2); \\ getting $x$ back from $g^x$ \\ is the \textbf{discrete logarithm}",
                  font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.0, 0])
        fit_right(notes)
        seq.next_to(notes, UP, buff=0.3).align_to(notes, LEFT)
        with self.voiceover(
            "Take the nonzero numbers modulo a prime, twenty-three, with multiplication. Any two multiply to another "
            "one, and every one has an inverse: this is a group. <bookmark mark='a'/> Start at one and keep "
            "multiplying by five: five, two, ten, four, twenty, and so on, jumping around the circle. <bookmark "
            "mark='b'/> After twenty-two steps every number has been visited, and we are back at one. Five generates "
            "the whole group. <bookmark mark='c'/> Gauss proved that for every prime the group is cyclic like this: "
            "some number generates all of it. <bookmark mark='d'/> Going forward, from x to five to the x, is easy "
            "even for huge numbers, by repeated squaring. Going back, from five to the x to x, is the discrete "
            "logarithm. The jumps are what make it hard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(nums), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(seq), LaggedStart(*[GrowArrow(a) for a in arrows[:6]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows[6:]], lag_ratio=0.2), FadeIn(notes[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def lagrange(self):
        d = load("groups")
        p = d["p"]
        head = label(r"Orders divide the group's size", font_size=34).to_edge(UP, buff=0.3)
        orders = {int(k): v for k, v in d["orders"].items()}
        cols = {1: GREY_B, 2: LAM, 11: DATA, 22: HEAD}
        cells = VGroup()
        for a in range(1, p):
            o = orders[a]
            sq = Square(side_length=0.5, stroke_color=GREY_D, fill_color=cols[o], fill_opacity=0.3)
            cells.add(VGroup(sq, mono(str(a), 18, WHITE).move_to(sq),
                             label(str(o), font_size=15, color=cols[o]).next_to(sq, DOWN, buff=0.06)))
        cells.arrange(RIGHT, buff=0.06).next_to(head, DOWN, buff=0.7)
        key = VGroup(*[VGroup(Square(side_length=0.25, stroke_width=0, fill_color=c, fill_opacity=0.6),
                              label(rf"order {o}", font_size=18, color=c)).arrange(RIGHT, buff=0.1)
                       for o, c in cols.items()]).arrange(RIGHT, buff=0.5).next_to(cells, DOWN, buff=0.5)
        lines = VGroup(
            label(r"the \textbf{order} of $a$: \ the first $k$ with $a^k = 1$", font_size=22, color=WHITE),
            label(rf"in $Z_{{{p}}}^*$ every order is 1, \ 2, \ 11 or 22: \ the divisors of {p - 1}", font_size=22,
                  color=DATA),
            label(r"\textbf{Lagrange}: \ in a finite group, \ every element's order divides the group's size",
                  font_size=22, color=YES),
            label(r"so $a^{p-1} = 1$ for every $a$: \ \textbf{Fermat's little theorem}, \ in one line", font_size=22,
                  color=HEAD),
            label(r"and $a^{\varphi(n)} \equiv 1 \pmod n$ \ when $\gcd(a, n) = 1$: \ \textbf{Euler}: \ RSA's engine",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Not every number generates the group. <bookmark mark='a'/> The order of a number is how many steps it "
            "takes to come back to one. <bookmark mark='b'/> Here are all twenty-two, coloured by order. Every order "
            "is one, two, eleven or twenty-two: exactly the divisors of twenty-two. <bookmark mark='c'/> That is "
            "Lagrange's theorem: in any finite group, the order of every element divides the size of the group. "
            "<bookmark mark='d'/> It proves Fermat's little theorem at once. The group has p minus one elements, so "
            "every a raised to the p minus one is one. <bookmark mark='e'/> The same argument for the numbers coprime "
            "to n, of which there are phi of n, gives Euler's theorem. Chapter five builds RSA on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[c[:2] for c in cells])))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[c[2] for c in cells])), FadeIn(key), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def scatter(self):
        d = load("groups")
        q, gq = d["q"], d["gq"]
        head = label(rf"$x \mapsto {gq}^x \bmod {q}$", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, q, 200], y_range=[0, q, 200], x_length=5.4, y_length=4.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.4).to_edge(
            LEFT, buff=1.2)
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.022, color=DATA) for x, y in enumerate(d["scatter"])])
        xl = label(r"exponent $x$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(rf"${gq}^x \bmod {q}$", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        notes = VGroup(
            label(r"forward: \ smooth growth, \\ then the remainder scatters it", font_size=21, color=WHITE),
            label(r"backward: \ given a height, \\ find its exponent", font_size=21, color=NO),
            label(r"no pattern to follow: \ the best \\ general methods take about \\ $\sqrt{p}$ steps \ (chapter 8)",
                  font_size=21, color=HEAD),
            label(r"a \textbf{one-way function}, \ as far as \\ anyone knows: \ easy forward, \\ hard to invert",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Here is what makes the discrete logarithm hard, for the prime one thousand and nineteen. <bookmark "
            "mark='a'/> Plot two to the x, modulo the prime, for every exponent. At first the powers grow smoothly, "
            "two, four, eight; then reduction wraps them around, and the points scatter like noise. <bookmark "
            "mark='b'/> Going backward means taking a height and finding which exponent produced it. <bookmark "
            "mark='c'/> There is no trend to follow. The best general methods, which chapter eight builds, take "
            "about the square root of p steps, and for a two-thousand-bit prime better methods exist but are still "
            "far too slow. <bookmark mark='d'/> So the map from x to g to the x is, as far as anyone knows, a one-way "
            "function: easy forward, hard to invert. Part 29 showed that one-way functions give all of symmetric "
            "cryptography. This one has extra structure, and that structure gives public keys."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.003), FadeIn(notes[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
