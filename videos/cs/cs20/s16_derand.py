from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation, Slerp

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, draw_graph, grid_table, load, mono, words)

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
        with self.voiceover((
            'Chapter fifteen. Removing the coins, and where they come from.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def maxcut(self):
        d = load("derand")
        head = label(r"The method of conditional expectations", font_size=34).to_edge(UP, buff=0.35)
        example_edges = [(0,1),(1,2),(2,3),(3,0),(0,2)]
        graph, nodes, edges = draw_graph({0:(-5.3,1.4),1:(-3.6,1.4),2:(-3.6,-0.3),3:(-5.3,-0.3)},
                                         example_edges, r=0.28)
        for vertex, side in enumerate((0,1,0,1)):
            nodes[vertex][0].set_fill(DATA if side==0 else LAM, opacity=0.35)
        for (u,v),edge in edges.items():
            edge.set_color(YES if (u%2)!=(v%2) else GREY_D)
        example = label(r"worked graph: \ 5 edges; \ final cut 4", font_size=19, color=YES).next_to(graph, DOWN, buff=0.2)
        trace = grid_table([r"fixed vertex",r"choose 0",r"choose 1",r"keep"],
                           [["0","2.5","2.5","0"],["1","2","3","1"],
                            ["2","3","3","0"],["3","2","4","1"]],
                           widths=[1.7,1.7,1.7,1.1], row_h=0.36, font_size=19, mono_cols=(),
                           colors=[[GREY_A,DATA,LAM,YES]]*4).move_to(RIGHT*2.4+UP*0.6)
        trace_caption = label(r"conditional expected cut in each branch", font_size=18, color=GREY_A).next_to(trace, UP, buff=0.16)
        lines = VGroup(
            label(r"MAX-CUT: \ maximize crossing edges; \ finding the optimum is NP-hard", font_size=20, color=WHITE),
            MathTex(r"\mathbb E[\mathrm{cut}]=m/2;\qquad\text{unfixed edges contribute }1/2", font_size=28, color=LAM),
            label(r"fix one vertex: \ keep the larger branch value; \ ties may choose either side", font_size=20, color=WHITE),
            MathTex(r"2.5\ \longrightarrow\ 2.5\ \longrightarrow\ 3\ \longrightarrow\ 3\ \longrightarrow\ 4\ge5/2",
                    font_size=31, color=YES),
        ).arrange(DOWN, buff=0.16).move_to(DOWN*1.75)
        res = label(rf"separate measured graph: \ {d['n']} vertices, \ {d['m']} edges; \ random mean {d['rand_mean']:.1f}, "
                    rf"best of 2000: {d['rand_max']}; \ deterministic: {d['cut']}", font_size=18,
                    color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Can the coins be removed? Sometimes, mechanically. <bookmark mark='a'/> MAX-CUT splits a graph's "
            "vertices to maximize crossing edges. Finding the optimum is NP-hard. <bookmark mark='b'/> Independent "
            'fair sides cut each edge with probability one half, so the expected cut is m over two. The small worked'
            " graph has five edges and expectation two and a half. <bookmark mark='c'/> Fix vertices one at a time, "
            'choosing the side with the larger conditional expectation. Edges to unassigned vertices still '
            "contribute one half each. <bookmark mark='d'/> The two branch values average to the current "
            'expectation, so the better branch cannot lower it. Our worked trace rises to a deterministic cut of '
            "four. It does not claim the optimum in general. <bookmark mark='e'/> The separate sixty-vertex "
            'experiment compares the deterministic result with two thousand sampled random cuts. Its measured values'
            ' are shown below the worked proof.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(graph), FadeIn(example), FadeIn(trace), FadeIn(trace_caption))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
            vo.wait_until("e")
            self.play(FadeIn(res))
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
            (
            "There is a second way. <bookmark mark='a'/> The MAX-CUT argument looks at one edge at a time, which "
            "involves only two vertices' coins. <bookmark mark='b'/> So the coins don't need to be fully "
            "independent, only pairwise independent. <bookmark mark='c'/> Pairwise independent bits are cheap. Pick "
            "k truly random bits s, and give vertex i the parity of the bits of s where i's binary expansion has a "
            "one. <bookmark mark='d'/> Any two of these bits are independent and fair, so k coins become about two "
            "to the k. <bookmark mark='e'/> With only about n possible seeds, we can try every one, "
            'deterministically, and keep the best cut: the expectation guarantees one of them reaches m over two. '
            "<bookmark mark='f'/> Limited independence, small-bias spaces and walks on expander graphs, Part 56, are"
            ' the general tools for stretching a few random bits a long way.'
        )
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
            (
            (
            f'The probabilistic guarantees use ideal randomness, with limited independence sufficient for some '
            f"arguments. Our reproducible experiments use seeded generators. <bookmark mark='a'/> In the 1960s and "
            f"70s, many scientific programs used IBM's RANDU: multiply by sixty-five thousand five hundred and "
            f"thirty-nine, modulo two to the thirty-one. <bookmark mark='b'/> Here are two and a half thousand "
            f"consecutive triples of its outputs, plotted as points in a cube. They look random. <bookmark mark='c'/>"
            f' Now turn the cube slowly. A projection can hide structure: watch how a cloud of points collapses into '
            f"evenly spaced sheets as the viewpoint changes. <bookmark mark='d'/> The multiplier is two to the "
            f'sixteen plus three, and squaring it shows that each output is six times the previous one minus nine '
            f"times the one before, modulo two to the thirty-one. <bookmark mark='e'/> So nine u minus six v plus w "
            f'is always a whole number, and every point lies on one of just '
            f"{len(d['planes'])}"
            f' planes. Any simulation that sampled points in space with RANDU was sampling fifteen sheets. Donald '
            f'Knuth called it truly horrible.'
        )
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), FadeIn(side[1]), FadeIn(cube), FadeIn(dots))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(t.animate.set_value(1.0), run_time=min(7.0, max(0.3, vo.until("d", minimum=0)-0.2)), rate_func=smooth)
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
                   label('linear over $\\mathbb{F}_2$: \\ full observed outputs allow state recovery; \\ not for secrets', font_size=19,
                         color=NO)),
            VGroup(label(r"\textbf{PCG}, \ \textbf{xoshiro}", font_size=22, color=LAM),
                   label(r"small, \ fast, \ statistically strong: \ numpy's default is PCG64", font_size=19,
                         color=GREY_A)),
            VGroup(label(r"\textbf{cryptographic generators}: \ ChaCha20, \ AES in counter mode", font_size=22,
                         color=YES),
                   label(r"no efficient test can tell them from coins, \ if the cipher is secure: \ Part 29",
                         font_size=19, color=GREY_A)),
            VGroup(label('\\textbf{entropy sources and hardware generators}: \\ distinct trust assumptions', font_size=22,
                         color=HEAD),
                   label('the OS collects and conditions entropy, then seeds a cryptographic generator', font_size=19, color=GREY_A)),
        )
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            (
            "Modern generators have different goals. <bookmark mark='a'/> Python's Mersenne Twister is a "
            'deterministic simulation generator, linear over the two-element field. Enough suitably observed full '
            'outputs expose its state; it is unsuitable for secrets. Passing a statistical test does not prove '
            "independence. <bookmark mark='b'/> PCG and xoshiro offer other simulation tradeoffs; NumPy's default "
            "generator uses a PCG variant. <bookmark mark='c'/> Cryptographic generators aim at computational "
            'indistinguishability for bounded attackers, conditional on their construction and a secret, '
            'sufficiently unpredictable seed. ChaCha20 is one building block, revisited in Part 29. <bookmark '
            "mark='d'/> Operating systems collect and condition entropy from available sources. A physical source, a"
            ' seeded generator and a mathematical independent-coin model are three different objects.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
