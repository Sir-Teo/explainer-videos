from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation, Slerp

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

CUBE_EDGES = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]
CORNERS = np.array([[(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1] for i in range(8)], dtype=float)


class Derand(VoiceoverScene):
    def construct(self):
        self.card()
        self.maxcut()
        self.pairwise()
        self.randu()
        self.sources()

    def card(self):
        card = chapter_card(15, r"Removing the coins, \ and where they come from", r"Can we do without randomness?",
                            lit=(1968,), extra=((1968, r"RANDU's planes"),), part=PART)
        with self.voiceover("Chapter fifteen. Removing the coins, and where they come from."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def maxcut(self):
        d = load("derand")
        head = label(r"The method of conditional expectations", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"MAX-CUT: \ split the vertices in two, \ cutting as many edges as possible \ (NP-hard, Part 26)",
                  font_size=21, color=WHITE),
            label(r"a random split cuts each edge with probability $\tfrac12$: \ $\mathbb{E}[\text{cut}] = m/2$",
                  font_size=21, color=LAM),
            label(r"place the vertices one at a time, \ each on the side that cuts more edges to those already "
                  r"placed", font_size=21, color=WHITE),
            MathTex(r"\mathbb{E}[\text{cut} \mid \text{choices so far}] \text{ never decreases} \quad\Longrightarrow"
                    r"\quad \text{cut} \ge \frac{m}{2}", font_size=32, color=YES),
            label(r"each choice is the better of two branches, \ and their average is the current expectation",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.4)
        res = VGroup(
            label(rf"a random graph: \ {d['n']} vertices, \ {d['m']} edges, \ $m/2 = {d['half']}$", font_size=21,
                  color=GREY_A),
            label(rf"2{{,}}000 random splits: \ mean {d['rand_mean']:.1f}, \ best {d['rand_max']}", font_size=21,
                  color=LAM),
            label(rf"conditional expectations, \ no coins at all: \ {d['cut']}", font_size=23, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Can the coins be removed? Sometimes, mechanically. <bookmark mark='a'/> Take MAX-CUT: split the "
            "vertices of a graph into two sides so that as many edges as possible cross. It is NP-hard, as Part 26 "
            "will show. <bookmark mark='b'/> A random split cuts each edge with probability a half, so on average "
            "it cuts half of them. <bookmark mark='c'/> Now place the vertices one at a time, and put each on the "
            "side that cuts more edges to the vertices already placed. <bookmark mark='d'/> At every step, the "
            "expected cut, given the choices so far, is the average of the two possible choices, so the better "
            "choice can't be below it. It starts at m over two and never falls, so the final cut, which is no "
            "longer random, is at least m over two. <bookmark mark='e'/> On a random graph with two hundred and "
            "sixty-five edges, random splits averaged half, and the best of two thousand cut one hundred and "
            "sixty-two. The deterministic walk through the expectations cut one hundred and seventy-six."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcd", lines[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            self.play(FadeIn(lines[4]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    def pairwise(self):
        head = label(r"Fewer coins: \ pairwise independence", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"the MAX-CUT argument only looks at one edge at a time: \ two vertices' coins", font_size=21,
                  color=WHITE),
            label(r"so the coins need only be \textbf{pairwise} independent", font_size=21, color=WHITE),
            MathTex(r"s \in \{0,1\}^{k} \text{ at random}, \qquad b_i = \langle \mathrm{bin}(i), s \rangle \bmod 2,"
                    r"\quad i = 1, \dots, 2^k - 1", font_size=32, color=LAM),
            label(r"any two $b_i, b_j$ are independent fair bits: \ $2^k - 1$ coins from $k$", font_size=21,
                  color=YES),
            label(r"so try all $2^k \approx n$ seeds, \ deterministically, \ and keep the best cut", font_size=21,
                  color=HEAD),
            label(r"the general tools: \ $k$-wise independence, \ small-bias spaces, \ expander walks \ (Part 56)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "There is a second way. <bookmark mark='a'/> The MAX-CUT argument looks at one edge at a time, which "
            "involves only two vertices' coins. <bookmark mark='b'/> So the coins don't need to be fully "
            "independent, only pairwise independent. <bookmark mark='c'/> Pairwise independent bits are cheap. Pick "
            "k truly random bits s, and give vertex i the parity of the bits of s where i's binary expansion has a "
            "one. <bookmark mark='d'/> Any two of these bits are independent and fair, so k coins become about two "
            "to the k. <bookmark mark='e'/> With only about n possible seeds, we can try every one, "
            "deterministically, and keep the best cut: the expectation guarantees one of them reaches m over two. "
            "<bookmark mark='f'/> Limited independence, small-bias spaces and walks on expander graphs, Part 56, are "
            "the general tools for stretching a few random bits a long way."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def randu(self):
        d = load("derand")
        pts = np.array(d["randu"][:2500]) - 0.5
        n = np.array([9.0, -6.0, 1.0])
        n /= np.linalg.norm(n)
        r0 = Rotation.from_euler("xyz", [-60, 0, 30], degrees=True)
        # the final view looks along a direction inside the planes: put the planes' normal along the screen's x-axis
        u = n
        v = np.cross(n, [0, 0, 1.0])
        v /= np.linalg.norm(v)
        w = np.cross(u, v)
        r1 = Rotation.from_matrix(np.array([u, v, w]))
        slerp = Slerp([0, 1], Rotation.concatenate([r0, r1]))
        mats = slerp(np.linspace(0, 1, 241)).as_matrix()          # plain arrays: the updaters stay hashable
        t = ValueTracker(0.0)
        S = 3.4
        center = np.array([-2.6, -0.4, 0])

        def proj(P):
            R = mats[int(round(min(max(t.get_value(), 0.0), 1.0) * 240))]
            Q = P @ R.T
            return Q[:, :2] * S

        dots = VGroup(*[Dot(radius=0.018, color=HEAD) for _ in range(len(pts))])

        def upd(g):
            q = proj(pts)
            for dt, (x, y) in zip(g, q):
                dt.move_to(center + np.array([x, y, 0]))
        dots.add_updater(upd)
        upd(dots)
        cube = VGroup(*[Line(ORIGIN, RIGHT, stroke_width=1.2, color=GREY_C) for _ in CUBE_EDGES])

        def cupd(g):
            q = proj(CORNERS - 0.5)
            for ln, (a, b) in zip(g, CUBE_EDGES):
                ln.put_start_and_end_on(center + np.array([*q[a], 0]), center + np.array([*q[b], 0]))
        cube.add_updater(cupd)
        cupd(cube)
        head = label(r"Where do the coins come from?", font_size=34).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"RANDU, \ IBM's generator from the 1960s:", font_size=21, color=WHITE),
            MathTex(r"x_{k+1} = 65539\, x_k \bmod 2^{31}", font_size=32, color=LAM),
            label(r"triples $(x_k, x_{k+1}, x_{k+2})$, \ plotted in a cube", font_size=20, color=GREY_A),
            MathTex(r"65539 = 2^{16} + 3: \quad x_{k+2} = 6x_{k+1} - 9x_k \pmod{2^{31}}", font_size=28, color=HEAD),
            MathTex(r"9u - 6v + w \in \mathbb{Z}", font_size=32, color=YES),
            label(rf"every triple lies on one of {len(d['planes'])} planes", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.28)
        if side.width > 5.6:
            side.width = 5.6
        side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Every algorithm in this part assumed fair, independent coins. Computers usually have none, and use "
            "pseudorandom generators instead. <bookmark mark='a'/> In the 1960s and 70s, many scientific programs "
            "used IBM's RANDU: multiply by sixty-five thousand five hundred and thirty-nine, modulo two to the "
            "thirty-one. <bookmark mark='b'/> Here are two and a half thousand consecutive triples of its outputs, "
            "plotted as points in a cube. They look random. <bookmark mark='c'/> Now turn the cube. <bookmark "
            "mark='d'/> The multiplier is two to the sixteen plus three, and squaring it shows that each output "
            "is six times the previous one minus nine times the one before, modulo two to the thirty-one. "
            f"<bookmark mark='e'/> So nine u minus six v plus w is always a whole number, and every point lies on "
            f"one of just {len(d['planes'])} planes. Any simulation that sampled points in space with RANDU was "
            "sampling fifteen sheets. Donald Knuth called it truly horrible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.add(cube)
            self.play(FadeIn(dots), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(t.animate.set_value(1.0), run_time=7.0, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        dots.clear_updaters()
        cube.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def sources(self):
        head = label(r"Better generators", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup(
            VGroup(label(r"\textbf{Mersenne Twister} \ (Matsumoto and Nishimura, 1998)", font_size=22, color=DATA),
                   label(r"period $2^{19937} - 1$, \ passes the usual statistical tests; \ Python's \texttt{random}",
                         font_size=19, color=GREY_A),
                   label(r"but linear over $\mathbb{F}_2$: \ 624 outputs reveal the whole state", font_size=19,
                         color=NO)),
            VGroup(label(r"\textbf{PCG}, \ \textbf{xoshiro}", font_size=22, color=LAM),
                   label(r"small, \ fast, \ statistically strong: \ numpy's default is PCG64", font_size=19,
                         color=GREY_A)),
            VGroup(label(r"\textbf{cryptographic generators}: \ ChaCha20, \ AES in counter mode", font_size=22,
                         color=YES),
                   label(r"no efficient test can tell them from coins, \ if the cipher is secure: \ Part 29",
                         font_size=19, color=GREY_A)),
            VGroup(label(r"\textbf{physical entropy}: \ timing jitter, \ thermal noise, \ \texttt{RDRAND}", font_size=22,
                         color=HEAD),
                   label(r"the operating system pools it and seeds a cryptographic generator: \ "
                         r"\texttt{/dev/urandom}", font_size=19, color=GREY_A)),
        )
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Modern generators are far better. <bookmark mark='a'/> The Mersenne Twister, from 1998, behind "
            "Python's random module, passes the usual statistical tests, but it is linear: six hundred and "
            "twenty-four outputs reveal every future one. Fine for simulations, useless for secrets. <bookmark "
            "mark='b'/> PCG and xoshiro are smaller and faster; numpy uses PCG. <bookmark mark='c'/> Cryptographic "
            "generators such as ChaCha20 are designed so that no efficient test can tell them from coins, if the "
            "cipher is secure; Part 29 builds them. <bookmark mark='d'/> And the seed comes from physical noise, "
            "pooled by the operating system."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
