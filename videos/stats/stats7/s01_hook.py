from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403

EDGE_ON = -0.554  # turn angle at which RANDU's planes 9x - 6y + z = k are seen edge-on (tilt 0.35)


def middle_square(seed: int, n: int) -> list[int]:
    out, x = [], seed
    for _ in range(n):
        x = (x * x // 100) % 10000
        out.append(x)
    return out


class Hook(VoiceoverScene):
    def construct(self):
        self.sin()
        self.middle()
        self.randu()
        self.objectives()

    def sin(self):
        tl = timeline(lit=(1951,)).to_edge(UP, buff=0.35)
        hc = history_card(1951, r"John von Neumann, \ ``Various techniques used in connection with random digits''",
                          r"``Anyone who considers arithmetical methods of producing random digits is, \ of course, \ in a "
                          r"state of sin.''", color=S.MUSEUM, width=8.6, font_size=26).move_to([0, 0.6, 0])
        ctx = label(r"Los Alamos: \ simulating neutrons for the hydrogen bomb on ENIAC, \ which needed random numbers by the "
                    r"million", font_size=22, color=GREY_A).next_to(hc, DOWN, buff=0.5)
        if ctx.width > 12.6:
            ctx.width = 12.6
        with self.voiceover(
            "Every simulation in this series so far, millions of coin tosses, normals, Cauchys and Paretos, ran on a "
            "machine that can only follow instructions. Where did the randomness come from? <bookmark mark='a'/> In "
            "1951 John von Neumann, who needed random numbers by the million to simulate neutrons for the "
            "hydrogen bomb, gave the answer that every generator since has had to live with. <bookmark mark='b'/> "
            "Anyone who considers arithmetical methods of producing random digits, he wrote, is, of course, in a "
            "state of sin. A deterministic generator with a fixed seed has a determined output. We use "
            "a sequence that behaves like random draws, while checking how it might fail."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(ctx))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def middle(self):
        seq = middle_square(1234, 14)
        seq2 = middle_square(2100, 6)
        rows = VGroup(label(r"von Neumann's own method: \ square, \ keep the middle four digits", font_size=26))
        chain = VGroup(MathTex(r"1234", font_size=30, color=GOOD))
        x = 1234
        for v in seq[:7]:
            chain.add(MathTex(rf"\to {v:04d}", font_size=30, color=GOOD))
            x = v
        chain.arrange(RIGHT, buff=0.15)
        sq = MathTex(r"1234^2 = 01\underline{5227}56", font_size=34, color=GREY_A)
        trap = VGroup(MathTex(r"2100", font_size=30, color=BAD), *[MathTex(rf"\to {v:04d}", font_size=30, color=BAD) for v in seq2])
        trap.arrange(RIGHT, buff=0.15)
        lab2 = label(r"but some seeds fall into short cycles, \ and others decay to zero", font_size=24, color=BAD)
        grp = VGroup(rows, sq, chain, lab2, trap).arrange(DOWN, buff=0.45).move_to([0, 0.2, 0])
        intro = label('Arithmetic randomness and short cycles', font_size=36)
        with self.voiceover(
            "Von Neumann's own method shows the danger. <bookmark mark='a'/> Take a four-digit number, square it, "
            "and keep the middle four digits of the eight-digit result: that's the next number. "
            "<bookmark mark='b'/> From twelve thirty-four you get fifty-two twenty-seven, then three two one five, "
            "and the digits look random enough. <bookmark mark='c'/> But from twenty-one hundred you get forty-one "
            "hundred, eighty-one hundred, sixty-one hundred, twenty-one hundred again: a cycle of length four. Other "
            "seeds decay to zero and stay there. Von Neumann knew this; he reportedly liked the method because it was "
            "fast, and because when it failed, it failed obviously. The dangerous failures are the ones you can't see."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(rows), FadeIn(sq))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(lab2), LaggedStart(*[FadeIn(c) for c in trap], lag_ratio=0.25))
        self.clear_scene()

    def randu(self):
        d = load("randu")
        P = np.asarray(d["randu"])[:3000] - 0.5
        Q = np.asarray(d["pcg"])[:3000] - 0.5
        ns = NSpace(scale=4.2, center=[-0.6, -0.3, 0], angle=0.9, tilt=0.35, axis_len=0.6,
                    axis_labels=[r"$u_k$", r"$u_{k+1}$", r"$u_{k+2}$"])
        cl = ns.cloud(P, color=BAD, radius=0.016, opacity=0.8)
        hc = history_card(1968, r"George Marsaglia, \ ``Random numbers fall mainly in the planes''", r"\emph{PNAS} 61: \ every "
                          r"multiplicative generator puts its triples on a few planes; \ RANDU's lie on 15",
                          color=S.MUSEUM, width=5.0, font_size=20).to_corner(UR, buff=0.3)
        f = MathTex(r"x_{k+1} = 65539\, x_k \bmod 2^{31}", font_size=30, color=BAD).to_corner(UL, buff=0.4)
        why_ = MathTex(r"65539 = 2^{16} + 3:\ \ x_{k+2} = 6x_{k+1} - 9x_k \pmod{2^{31}}", font_size=26, color=GREY_A)
        why_.next_to(f, DOWN, buff=0.2).align_to(f, LEFT)
        tag = note(r"3,000 consecutive triples, \ cube centered by subtracting $1/2$").to_corner(DL, buff=0.3)
        good = label(r"PCG32 (2014): \ no visible RANDU-style planes", font_size=26, color=GOOD).to_corner(DR, buff=0.4)
        with self.voiceover(
            "In the 1960s IBM distributed a generator called RANDU with its System/360 computers. "
            "<bookmark mark='a'/> Multiply by sixty-five thousand five hundred and thirty-nine, and take the "
            "remainder after dividing by two to the thirty-one. Each number looks uniform, and passes simple tests. "
            "<bookmark mark='b'/> Now plot consecutive triples as points in a cube. From most angles: a uniform "
            "cloud. <bookmark mark='c'/> Turn it. <bookmark mark='d'/> Every point lies on one of just fifteen "
            "planes. Because sixty-five thousand five hundred and thirty-nine is two to the sixteen plus three, each "
            "number is six times the last minus nine times the one before, so nine x minus six y plus z is always "
            "an integer. George Marsaglia published the general result in 1968: random numbers fall mainly in the "
            "planes. <bookmark mark='e'/> RANDU stayed in wide use for years, in simulations nobody could easily recheck. A modern generator, PCG, "
            "shows no visible RANDU-style planes at this resolution; that picture is not proof of randomness."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(ns.axes3), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(f))
            vo.wait_until("b")
            self.play(FadeIn(cl, lag_ratio=0.0005), run_time=2.0)
            vo.wait_until("c")
            self.play(ns.angle.animate.set_value(EDGE_ON), run_time=5.0)
            vo.wait_until("d")
            self.play(FadeIn(hc), FadeIn(why_))
            vo.wait_until("e")
            cl2 = ns.cloud(Q, color=GOOD, radius=0.016, opacity=0.8)
            self.play(FadeOut(cl), FadeIn(cl2, lag_ratio=0.0005), FadeIn(good), run_time=2.0)
            self.play(ns.angle.animate.set_value(EDGE_ON + 0.9), run_time=3.0)
            cl.clear_updaters()
            cl2.clear_updaters()
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 7", font_size=34, color=GREY_B), label(r"Randomness on Demand", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"pseudo-random generators: \ congruences, \ PCG, \ and how to test them",
            r"samplers: \ the inverse CDF, \ rejection, \ Box--Muller, \ Marsaglia--Tsang, \ the alias method",
            r"Monte Carlo integration: \ $\sigma/\sqrt n$ in any dimension; \ Buffon's needle",
            r"simulation studies done right; \ variance reduction",
            r"Markov chains: \ stationary laws, \ PageRank, \ seven shuffles, \ Metropolis",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 3 and 6").to_corner(DL, buff=0.3)
        built = label(r"Built in this part: \ statkit.random, \ and the simulation-study harness", font_size=28, color=S.ACCENT)
        built.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "<bookmark mark='a'/> Part seven: randomness on demand. <bookmark mark='b'/> We'll build a generator and "
            "learn to test one; turn uniform numbers into any distribution we like; integrate by throwing darts; "
            "learn to run a simulation study honestly, a framework for evaluating statistical methods; make "
            "simulations cheaper; and meet Markov chains, which mix decks of cards and power the algorithms of "
            "modern Bayesian statistics. <bookmark mark='c'/> And we'll build statkit dot random, a library that "
            "later simulations can use."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
            vo.wait_until("c")
            self.play(obj.animate.shift(UP * 0.4), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
