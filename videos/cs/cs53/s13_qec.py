from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def cross(p, size=0.13, color=NO, sw=4):
    p = np.asarray(p)
    return VGroup(Line(p + np.array([-size, -size, 0]), p + np.array([size, size, 0]), color=color, stroke_width=sw),
                  Line(p + np.array([-size, size, 0]), p + np.array([size, -size, 0]), color=color, stroke_width=sw))


def surface_lattice(d, origin, sp):
    """The rotated surface code of distance d: data qubits on a d-by-d grid; faces measure the parity of their
    corners, Z-type (blue, catching bit flips) and X-type (purple, catching phase flips) in a checkerboard, with
    two-qubit half-faces on the boundary (X on top and bottom, Z on left and right): d^2 - 1 checks in all.
    Returns (qubit positions, faces as [(kind, qubits, mobject)])."""
    o = np.asarray(origin, dtype=float)
    q = {(i, j): o + np.array([i * sp, j * sp, 0]) for i in range(d) for j in range(d)}
    faces = []
    for a in range(-1, d):
        for b in range(-1, d):
            t = (a + b) % 2                      # 0: Z check, 1: X check
            bulk = 0 <= a <= d - 2 and 0 <= b <= d - 2
            tb = b in (-1, d - 1) and 0 <= a <= d - 2
            lr = a in (-1, d - 1) and 0 <= b <= d - 2
            if not (bulk or (tb and t == 1) or (lr and t == 0)):
                continue
            qs = [(x, y) for x in (a, a + 1) for y in (b, b + 1) if 0 <= x < d and 0 <= y < d]
            col = DATA if t == 0 else LAM
            if bulk:
                pts = [q[(a, b)], q[(a + 1, b)], q[(a + 1, b + 1)], q[(a, b + 1)]]
            else:
                p1, p2 = q[qs[0]], q[qs[1]]
                mid = (p1 + p2) / 2
                u = (p2 - p1) / np.linalg.norm(p2 - p1)
                v = (UP if b == d - 1 else DOWN) if tb else (RIGHT if a == d - 1 else LEFT)
                pts = [mid + sp / 2 * (math.cos(f) * u + math.sin(f) * v)
                       for f in np.linspace(0, PI, 16)]
                if np.cross(u, v)[2] > 0:
                    pts = pts[::-1]
            poly = Polygon(*pts, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.22)
            faces.append(("Z" if t == 0 else "X", qs, poly))
    return q, faces


class Qec(VoiceoverScene):
    def construct(self):
        self.card()
        self.obstacles()
        self.three()
        self.continuous()
        self.nine()
        self.surface()
        self.threshold()

    def card(self):
        card = chapter_card(12, r"Quantum error correction",
                            r"How do we protect a state we may neither copy nor look at?", lit=(1995, 2024),
                            extra=((1995, r"Shor: \ the nine-qubit code"),
                                   (2024, r"Google: \ below threshold")), part=PART)
        with self.voiceover("Chapter twelve. Quantum error correction. How do we protect a state we may neither copy "
                            "nor look at?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ why it seemed impossible
    def obstacles(self):
        c3 = load("code3")["cases"][0]
        al, be = c3["alpha"], c3["beta"]
        head = label(r"Why it seemed impossible", font_size=36).to_edge(UP, buff=0.3)

        def panel(content, cap, col):
            fr = RoundedRectangle(width=4.0, height=3.6, corner_radius=0.15, stroke_color=col, stroke_width=1.8)
            content.move_to(fr.get_center() + UP * 0.45)
            c = wrapped_label(cap, 3.6, font_size=19, color=col).next_to(content, DOWN, buff=0.35)
            return VGroup(fr, content, c)
        clone = MathTex(r"|\psi\rangle \;\mapsto\; |\psi\rangle|\psi\rangle", font_size=36, color=GREY_A)
        clone_x = VGroup(clone, cross(clone.get_center(), size=0.55, sw=5))
        bars = VGroup(*[Rectangle(width=0.5, height=v * 1.6, stroke_width=0, fill_color=DATA, fill_opacity=0.9)
                        for v in (al, be)]).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        bl = VGroup(*[MathTex(t, font_size=22, color=GREY_A).next_to(b, DOWN, buff=0.08)
                      for t, b in zip((r"|0\rangle", r"|1\rangle"), bars)])
        bv = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=DATA).next_to(b, UP, buff=0.06)
                      for v, b in zip((al, be), bars)])
        after = Rectangle(width=0.5, height=1.6, stroke_width=0, fill_color=NO, fill_opacity=0.9)
        meas = VGroup(VGroup(bars, bl, bv), MathTex(r"\to", font_size=34, color=GREY_B),
                      VGroup(after, MathTex(r"|1\rangle", font_size=22, color=GREY_A).next_to(after, DOWN,
                                                                                             buff=0.08))).arrange(
            RIGHT, buff=0.3, aligned_edge=DOWN)
        ring = Circle(radius=0.9, color=GREY_C, stroke_width=1.8)
        a0 = Arrow(ORIGIN, UP * 0.9, buff=0, color=DATA, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        a1 = Arrow(ORIGIN, 0.9 * np.array([math.sin(0.35), math.cos(0.35), 0]), buff=0, color=NO, stroke_width=4,
                   max_tip_length_to_length_ratio=0.2)
        eps = MathTex(r"\varepsilon", font_size=26, color=NO).move_to(0.55 * np.array([math.sin(0.17), math.cos(0.17),
                                                                                     0]) + RIGHT * 0.15 + UP * 0.12)
        drift = VGroup(ring, a0, a1, eps)
        panels = VGroup(
            panel(clone_x, r"no copies to vote with: \ no-cloning \ (chapter 3)", NO),
            panel(meas, rf"looking destroys it: \ ${al}|0\rangle + {be}|1\rangle$ becomes $|0\rangle$ or "
                  r"$|1\rangle$", HEAD),
            panel(drift, r"errors are continuous: \ a drift by any small angle, \ not just a flip", LAM),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.45)
        foot = wrapped_label(r"the way out \ (Shor, \ 1995; \ Steane, \ 1996): \ spread the state by entanglement, "
                             r"\ not copying, \ and measure only \textbf{parities}, \ which reveal the error but "
                             r"nothing about the state", 12.4, font_size=21, color=YES).next_to(panels, DOWN, buff=0.7)
        with self.voiceover(
            "Part 28 protected bits by copying them and reading the copies. For qubits all three ideas seemed to "
            "fail, and some leading physicists doubted that quantum computers could be made reliable. "
            "<bookmark mark='a'/> First, chapter three's no-cloning theorem forbids copies. <bookmark mark='b'/> "
            "Second, reading a qubit destroys it: measure a superposition, and you are left "
            "with zero or one. <bookmark mark='c'/> Third, errors are continuous: a qubit can drift by any "
            "small angle. <bookmark mark='d'/> In 1995 Peter Shor found a way round all three, and Andrew Steane "
            "another in 1996: spread the state by entanglement, and measure only parities, which reveal the error "
            "but nothing about the state."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abc", panels):
                vo.wait_until(mk)
                self.play(FadeIn(p[0]), FadeIn(p[1]), FadeIn(p[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the three-qubit code
    def three(self):
        cases = load("code3")["cases"]
        al, be = cases[0]["alpha"], cases[0]["beta"]
        head = label(r"The three-qubit code and its syndromes", font_size=36).to_edge(UP, buff=0.3)
        fs = 30
        rows = VGroup(
            MathTex(rf"{al}|0\rangle + {be}|1\rangle", r"\;\to\;", rf"{al}|000\rangle", r"+", rf"{be}|111\rangle",
                    font_size=fs),
            MathTex(r"X_2:", r"\;\;", rf"{al}|010\rangle", r"+", rf"{be}|101\rangle", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        rows.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        rows[1].align_to(rows[0][1], LEFT).shift(LEFT * 0.75)
        whys = VGroup(label(r"two CNOTs: \ one entangled state, \ not three copies", font_size=18, color=GREY_B),
                      label(r"the middle qubit flips, \ in both terms", font_size=18, color=NO))
        for w_, r in zip(whys, rows):
            w_.next_to(r, RIGHT, buff=0.45)
        # the qubits and their two parity checks
        y = -1.05
        qx = [-5.4, -3.4, -1.4]
        qs = VGroup(*[Circle(radius=0.36, color=WHITE, stroke_width=2.4).move_to([x, y, 0]) for x in qx])
        ql = VGroup(*[MathTex(rf"q_{i + 1}", font_size=22, color=GREY_A).next_to(c, DOWN, buff=0.12)
                      for i, c in enumerate(qs)])
        checks = VGroup(*[Square(side_length=0.55, stroke_color=KERN, stroke_width=2, fill_color=BG,
                                 fill_opacity=1).move_to([(qx[i] + qx[i + 1]) / 2, y + 1.0, 0]) for i in range(2)])
        cl = VGroup(*[MathTex(t, font_size=20, color=KERN).next_to(s, UP, buff=0.08)
                      for t, s in zip((r"Z_1Z_2", r"Z_2Z_3"), checks)])
        links = VGroup(*[Line(checks[i].get_corner(DL if k == 0 else DR), qs[i + k].get_top(), color=KERN,
                              stroke_width=1.5) for i in range(2) for k in range(2)])
        bits = VGroup(*[MathTex("0", font_size=24, color=KERN).move_to(s) for s in checks])
        tab = grid_table([r"error", r"syndrome", r"fix", r"restored"],
                         [[r"none" if c["flip"] is None else rf"$X_{c['flip'] + 1}$",
                           f"{c['syndrome'][0]}{c['syndrome'][1]}",
                           r"---" if c["corrected"] is None else rf"$X_{c['corrected'] + 1}$",
                           r"yes" if c["restored"] else r"no"] for c in cases],
                         widths=[1.2, 1.3, 1.0, 1.3], row_h=0.44, font_size=19, mono_cols=(1,))
        tab.move_to([3.85, -1.15, 0])
        for r in range(1, 5):
            tab.cells[r][1].set_color(KERN)
            tab.cells[r][3].set_color(YES)
        foot = wrapped_label(r"both terms give the same parities, \ so measuring them learns the error and nothing "
                             r"about $\alpha$ and $\beta$: \ Part 28's syndrome, \ for qubits", 12.4, font_size=19,
                             color=YES).to_edge(DOWN, buff=0.3)

        def show(case):
            f = case["flip"]
            anims = [Transform(bits[i], MathTex(str(case["syndrome"][i]), font_size=24,
                                                color=NO if case["syndrome"][i] else KERN).move_to(checks[i]))
                     for i in range(2)]
            anims += [checks[i].animate.set_fill(NO if case["syndrome"][i] else BG, opacity=0.6 if
                                                 case["syndrome"][i] else 1) for i in range(2)]
            anims += [qs[i].animate.set_color(NO if i == f else WHITE) for i in range(3)]
            return anims
        with self.voiceover(
            "The simplest code protects against bit flips. <bookmark mark='a'/> Two CNOTs spread one qubit over "
            "three, as one entangled state, not three copies. <bookmark mark='b'/> Suppose the middle qubit flips. "
            "<bookmark mark='c'/> Measure two parities, using extra qubits: does the first agree with the second, "
            "and the second with the third? Both terms give the same answers, so we learn where the error is and "
            "nothing about the amplitudes. <bookmark mark='d'/> Each single flip lights a different pattern, the "
            "syndrome, as with Part 28's Hamming code. Flip the culprit back, and our simulator recovers the "
            "original amplitudes in all four cases."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(qs), FadeIn(ql))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(qs[1].animate.set_color(NO), Indicate(qs[1], color=NO))
            vo.wait_until("c")
            self.play(FadeIn(checks), FadeIn(cl), Create(links), FadeIn(bits))
            self.play(*show(cases[2]))
            self.play(FadeIn(foot))
            vo.wait_until("d")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            for k, case in enumerate(cases):
                self.play(*show(case), FadeIn(VGroup(*tab.cells[k + 1])), run_time=0.9)
                self.wait(0.3)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ continuous errors become discrete
    def continuous(self):
        head = label(r"Measuring the syndrome makes errors discrete", font_size=36).to_edge(UP, buff=0.3)
        fs = 30
        rows = VGroup(
            MathTex(r"e^{-i\varepsilon X_1}", r"=", r"\cos\varepsilon\, I", r"-", r"i\sin\varepsilon\, X_1",
                    font_size=fs),
            MathTex(r"e^{-i\varepsilon X_1}|\psi_L\rangle", r"=", r"\cos\varepsilon\, |\psi_L\rangle", r"-",
                    r"i\sin\varepsilon\, X_1|\psi_L\rangle", font_size=fs),
            MathTex(r"E", r"=", r"a\,I + b\,X + c\,Z + d\,XZ", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        rows.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.7)
        whys = VGroup(label(r"a small unwanted rotation of qubit 1, \ written out", font_size=18, color=GREY_B),
                      label(r"on the encoded state: \ no error, \ plus a whole flip", font_size=18, color=GREY_B),
                      wrapped_label(r"any error on one qubit: \ correct $X$ and $Z$, \ and everything is corrected",
                                    6.0, font_size=18, color=YES))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.12).align_to(r, LEFT).shift(RIGHT * 0.1)
        rows[1][2].set_color(YES)
        rows[1][4].set_color(NO)
        # the fork: measuring the syndrome picks one branch
        eps = 0.1
        root = Dot([2.6, -0.2, 0], radius=0.08, color=WHITE)
        rl = label(r"measure the syndrome", font_size=19, color=KERN).next_to(root, LEFT, buff=0.15)
        ends = [np.array([5.6, 1.0, 0]), np.array([5.6, -1.4, 0])]
        br = VGroup(*[Line(root.get_center(), e, color=c, stroke_width=3) for e, c in zip(ends, (YES, NO))])
        el = VGroup(
            VGroup(label(r"syndrome 00: \ no error", font_size=19, color=YES),
                   MathTex(rf"\cos^2\varepsilon = {math.cos(eps) ** 2:.3f}", font_size=24, color=YES)).arrange(
                DOWN, buff=0.08).next_to(ends[0], UP, buff=0.1),
            VGroup(label(r"syndrome 10: \ a whole $X_1$, \ fix it", font_size=19, color=NO),
                   MathTex(rf"\sin^2\varepsilon = {math.sin(eps) ** 2:.3f}", font_size=24, color=NO)).arrange(
                DOWN, buff=0.08).next_to(ends[1], DOWN, buff=0.1))
        for g in el:
            if g.get_right()[0] > 6.85:
                g.shift(LEFT * (g.get_right()[0] - 6.85))
        ill = note(rf"illustrative: \ $\varepsilon = {eps}$ rad", font_size=16).next_to(root, DOWN, buff=0.25)
        with self.voiceover(
            "The third obstacle, continuous error, dissolves when the syndrome is measured. <bookmark mark='a'/> A "
            "small unwanted rotation by epsilon is a combination of doing nothing and a full bit flip. "
            "<bookmark mark='b'/> Applied to the encoded state, it makes a superposition of no error and one whole "
            "flip. <bookmark mark='c'/> Measuring the syndrome forces a choice: with probability cosine squared "
            "epsilon, no error; with sine squared epsilon, a whole flip, which we know how to undo. "
            "<bookmark mark='d'/> And any error on one qubit is a combination of four: nothing, a bit flip, a phase "
            "flip, or both. Correct bit flips and phase flips, and everything else is corrected."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(root), FadeIn(rl), FadeIn(ill))
            self.play(Create(br), FadeIn(el), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ phase flips and Shor's nine qubits
    def nine(self):
        head = label(r"Phase flips, \ and Shor's nine qubits", font_size=36).to_edge(UP, buff=0.3)
        fs = 30
        rows = VGroup(
            MathTex(r"Z\,|{+}\rangle = |{-}\rangle", r",\quad", r"Z\,|{-}\rangle = |{+}\rangle", font_size=fs),
            MathTex(r"|0_L\rangle", r"=", r"\tfrac{1}{2\sqrt2}", r"\big(|000\rangle + |111\rangle\big)^{\otimes 3}",
                    font_size=fs),
            MathTex(r"|1_L\rangle", r"=", r"\tfrac{1}{2\sqrt2}", r"\big(|000\rangle - |111\rangle\big)^{\otimes 3}",
                    font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        rows.move_to([2.9, 1.25, 0]).align_to([-0.4, 0, 0], LEFT)
        whys = VGroup(label(r"in the Hadamard basis a phase flip is a bit flip", font_size=18, color=GREY_B),
                      label(r"three blocks against phase flips, \ three qubits each against bit flips",
                            font_size=18, color=GREY_B))
        whys[0].next_to(rows[0], DOWN, buff=0.1).align_to(rows[0], LEFT).shift(RIGHT * 0.1)
        whys[1].next_to(rows[2], DOWN, buff=0.1).align_to(rows[2], LEFT).shift(RIGHT * 0.1)
        # the 3 x 3 grid
        sp = 0.85
        o = np.array([-5.3, 1.35, 0])
        pos = [[o + np.array([c * sp, -r * 1.25, 0]) for c in range(3)] for r in range(3)]
        dots = VGroup(*[Circle(radius=0.2, color=WHITE, stroke_width=2.2).move_to(pos[r][c]) for r in range(3)
                        for c in range(3)])
        zl = VGroup(*[Line(pos[r][c] + RIGHT * 0.2, pos[r][c + 1] + LEFT * 0.2, color=DATA, stroke_width=3)
                      for r in range(3) for c in range(2)])
        blocks = VGroup(*[SurroundingRectangle(VGroup(*dots[3 * r:3 * r + 3]), color=GREY_C, buff=0.14,
                                               stroke_width=1.5) for r in range(3)])
        xs = VGroup(*[VGroup(Line(blocks[r].get_right() + RIGHT * 0.3, blocks[r + 1].get_right() + RIGHT * 0.3,
                                  color=LAM, stroke_width=4),
                             Square(side_length=0.36, stroke_color=LAM, stroke_width=2, fill_color=BG,
                                    fill_opacity=1).move_to((blocks[r].get_right() + blocks[r + 1].get_right()) / 2
                                                            + RIGHT * 0.3)) for r in range(2)])
        leg = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=DATA, stroke_width=3),
                   label(r"$ZZ$: \ bit-flip checks within a block", font_size=18, color=DATA)).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.25, stroke_color=LAM, stroke_width=2),
                   label(r"$X^{\otimes 6}$: \ compares the signs of two blocks", font_size=18, color=LAM)).arrange(
                RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(blocks, DOWN, buff=0.4).align_to(
            blocks, LEFT)
        stab = wrapped_label(r"\textbf{stabilizers} \ (Gottesman, \ 1997): \ every check is a product of Paulis that "
                             r"leaves each codeword unchanged; \ $9$ qubits, \ $6 + 2 = 8$ checks, \ $9 - 8 = 1$ "
                             r"logical qubit", 6.6, font_size=19, color=YES).next_to(whys[1], DOWN, buff=0.45).align_to(
            rows, LEFT)
        with self.voiceover(
            "Qubits suffer a second kind of error: a phase flip, which turns plus into "
            "minus. <bookmark mark='a'/> In the Hadamard basis a phase flip is a bit flip, so the same code, turned "
            "sideways, catches it. <bookmark mark='b'/> Shor nested the two: three blocks against phase flips, and "
            "each block three qubits against bit flips, nine in all. <bookmark mark='c'/> A phase flip anywhere in a "
            "block changes that block's sign, and the checks comparing neighbouring blocks light up. "
            "<bookmark mark='d'/> Every check is a product of Pauli operators that leaves each codeword alone. "
            "Daniel Gottesman's stabilizer formalism of 1997 describes whole families of codes this way: here eight "
            "checks on nine qubits leave one logical qubit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(whys[1]))
            self.play(FadeIn(dots), Create(blocks), Create(zl), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(FadeIn(xs), FadeIn(leg[1]))
            self.play(dots[4].animate.set_color(NO), blocks[1].animate.set_color(NO))
            self.play(*[x[1].animate.set_fill(NO, opacity=0.7) for x in xs], Indicate(dots[4], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(stab))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the surface code
    def surface(self):
        d = 5
        head = label(r"The surface code: \ syndromes on a lattice", font_size=36).to_edge(UP, buff=0.3)
        sp = 0.95
        q, faces = surface_lattice(d, [-5.5, -2.55, 0], sp)
        assert len(faces) == d * d - 1
        polys = VGroup(*[f[2] for f in faces])
        dots = VGroup(*[Dot(p, radius=0.08, color=WHITE) for p in q.values()])

        def lights(errs):
            return [i for i, (k, qs, _) in enumerate(faces) if k == "Z" and sum(x in errs for x in qs) % 2]

        def light(errs):
            on = set(lights(errs))
            return [f[2].animate.set_fill(NO if i in on else (DATA if f[0] == "Z" else LAM),
                                          opacity=0.75 if i in on else 0.22) for i, f in enumerate(faces)]
        e1 = [(2, 2)]
        e2 = [(1, 1), (1, 2), (1, 3)]
        e3 = [(3, j) for j in range(d)]
        notes = VGroup(
            wrapped_label(r"data qubits on the corners; \ each face measures the parity of its four \ (or two) "
                          r"corners: \ blue faces catch bit flips, \ purple faces phase flips; \ "
                          r"every check is local", 6.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"one bit flip lights the blue faces beside it", 6.4, font_size=19, color=NO),
            wrapped_label(r"a chain lights only its two ends; \ a decoder pairs lit faces by the shortest chains "
                          r"that explain them \ (minimum-weight matching)", 6.4, font_size=19, color=HEAD),
            wrapped_label(rf"a chain right across the lattice lights nothing: \ a logical error, \ needing $d = {d}$ "
                          rf"flips; \ any ${(d - 1) // 2}$ are corrected \ (Part 28's $\lfloor (d-1)/2 \rfloor$)",
                          6.4, font_size=19, color=YES),
            wrapped_label(rf"Kitaev \ (1997); \ Dennis et al. \ (2002); \ Fowler et al. \ (2012); \ distance $d$ "
                          rf"costs $2d^2 - 1$ physical qubits: \ {2 * d * d - 1} here", 6.4, font_size=18,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.1, 0])
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        marks = VGroup()
        with self.voiceover(
            "The leading design today is the surface code, from Alexei Kitaev's toric code of 1997, developed by "
            "Dennis, Kitaev, Landahl and Preskill, and by Fowler and colleagues in 2012. <bookmark mark='a'/> Data "
            "qubits sit on the corners of a grid. Each face measures the parity of its corners: blue faces catch "
            "bit flips, purple faces phase flips, and every check touches only near neighbours. "
            "<bookmark mark='b'/> A bit flip lights the blue faces beside it. <bookmark mark='c'/> A chain of flips "
            "lights only its two ends, and a decoder pairs the lit faces by the shortest chains that explain them. "
            "<bookmark mark='d'/> Only a chain right across the lattice goes unseen: at distance five that takes "
            "five errors, and any two are corrected."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in polys], lag_ratio=0.04), FadeIn(dots), FadeIn(notes[0]),
                      run_time=2)
            vo.wait_until("b")
            marks.add(*[cross(q[e]) for e in e1])
            self.play(FadeIn(marks), *light(e1), FadeIn(notes[1]))
            vo.wait_until("c")
            new = VGroup(*[cross(q[e]) for e in e2])
            self.play(FadeOut(marks), FadeIn(new), *light(e2), FadeIn(notes[2]))
            marks = new
            vo.wait_until("d")
            new = VGroup(*[cross(q[e]) for e in e3])
            self.play(FadeOut(marks), FadeIn(new), *light(e3), FadeIn(notes[3]))
            self.play(Indicate(new, color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the threshold
    def threshold(self):
        rep = load("repetition")
        lam = rep["lambda"]["0.01"][0]
        head = label(r"Below threshold, \ bigger is better", font_size=36).to_edge(UP, buff=0.3)
        ax0 = Axes(x_range=[0, 2, 1], y_range=[0, 10, 2], x_length=5.6, y_length=4.6,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True})
        ax0.move_to([-3.4, 0.15, 0])

        def c2p(x, y):                    # log10 coordinates: x = log10 p in [-2, 0], y = log10 p_L in [-10, 0]
            return ax0.c2p(x + 2, y + 10)
        xt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(c2p(v, -10), DOWN, buff=0.1)
                      for t, v in ((r"10^{-2}", -2), (r"10^{-1}", -1), (r"1", 0))])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(c2p(-2, v), LEFT, buff=0.1)
                      for v in (-10, -8, -6, -4, -2)])
        xl = label(r"physical error rate $p$", font_size=18, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label(r"logical error rate", font_size=18, color=GREY_B).next_to(ax0, UP, buff=0.12).align_to(ax0, LEFT)
        ds = sorted({r["d"] for r in rep["rows"]})
        cols = [GREY_B, DATA, LAM, YES, HEAD, KERN]
        curves, dots, dl = VGroup(), VGroup(), VGroup()
        for dd, col in zip(ds, cols):
            rr = [r for r in rep["rows"] if r["d"] == dd]
            pts = [c2p(math.log10(r["p"]), math.log10(r["exact"])) for r in rr]
            curves.add(VMobject(color=col, stroke_width=2.5).set_points_as_corners(pts))
            dots.add(VGroup(*[Dot(c2p(math.log10(r["p"]), math.log10(r["simulated"])), radius=0.05, color=col)
                              for r in rr if r["simulated"] > 0]))
            dl.add(MathTex(rf"d = {dd}", font_size=18, color=col).next_to(pts[0], DR, buff=0.06))
        thr = DashedLine(c2p(math.log10(0.5), -10), c2p(math.log10(0.5), 0), color=NO, dash_length=0.07)
        thl = label(r"threshold, \ $p = \tfrac12$", font_size=17, color=NO).next_to(thr, UP, buff=0.08).shift(
            LEFT * 0.5)
        src = note(r"lines: \ the exact sum; \ dots: \ our simulator, \ 200{,}000 trials per point", font_size=16
                   ).next_to(xl, DOWN, buff=0.08)
        fs = 28
        rows = VGroup(
            MathTex(r"p_L", r"=", r"\sum_{k > d/2} \binom{d}{k} p^k (1-p)^{d-k}", font_size=fs),
            MathTex(r"p_L", r"\approx", r"\binom{d}{(d+1)/2}\, p^{(d+1)/2}", font_size=fs),
            MathTex(r"\Lambda", r"=", r"\frac{p_L(d)}{p_L(d+2)}", r"\approx", rf"{lam:.0f}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.move_to([3.4, 1.45, 0]).align_to([0.5, 0, 0], LEFT)
        rows[2][4].set_color(YES)
        whys = VGroup(label(r"majority vote fails when more than half flip", font_size=18, color=GREY_B),
                      label(r"small $p$: \ the first term dominates", font_size=18, color=GREY_B),
                      label(r"at $p = 1\%$, \ $d = 3 \to 5$: \ the error divided by $\Lambda$", font_size=18,
                            color=YES))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.08).align_to(r, LEFT).shift(RIGHT * 0.1)
        notes = VGroup(
            wrapped_label(r"above threshold a bigger code is \textit{worse}; \ the repetition code catches only bit "
                          r"flips, \ so its threshold is generous", 6.3, font_size=19, color=WHITE),
            wrapped_label(r"surface codes under realistic noise: \ thresholds near 1\% \ (Fowler et al., \ 2012); \ "
                          r"Google Quantum AI \ (2024): \ distance 3 to 5 to 7 on a chip, \ $\Lambda \approx 2$, \ "
                          r"clearly below threshold", 6.3, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(whys[2], DOWN, buff=0.4).align_to(rows, LEFT)
        with self.voiceover(
            "Take the simplest case: the repetition code against independent bit flips. "
            "<bookmark mark='a'/> With distance d and a majority vote, the code fails only if more than half the "
            "bits flip. <bookmark mark='b'/> For small p the first failing term dominates, so the logical error "
            "falls like p to the power d plus one over two. <bookmark mark='c'/> Below the threshold, here one half, "
            "a bigger code is better: at one per cent, each step in distance divides the error by about thirty. "
            "Above it, bigger is worse. <bookmark mark='d'/> Real codes under real noise have thresholds near one "
            "per cent. In 2024 Google's team grew a surface code from distance three to five to seven, and each "
            "step roughly halved the logical error: clearly below threshold, in hardware."
        ) as vo:
            self.play(FadeIn(head), Create(ax0), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(dots), FadeIn(dl),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(thl))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
