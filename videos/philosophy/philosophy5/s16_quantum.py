from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


def line_through(angle_deg, length=5.0, color=WHITE, center=ORIGIN, width=4):
    a = np.deg2rad(angle_deg)
    v = np.array([np.cos(a), np.sin(a), 0]) * length / 2
    c = np.asarray(center, float)
    return Line(c - v, c + v, color=color, stroke_width=width)


class Quantum(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Is logic empirical?", r"Could physics refute a law of logic?", lit=(1936,),
                            part=PART)
        with self.voiceover("Chapter fifteen. Is logic empirical?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.birkhoff()
        self.distributivity()
        self.polarizers()
        self.putnam()

    def birkhoff(self):
        hc = history_card(1936, r"Garrett Birkhoff \& John von Neumann", r"`The logic of quantum mechanics'",
                          width=7.0, color=HIST).to_corner(UL, buff=0.35)
        rows = [(r"a proposition", r"a subspace of the state space: \ the states in which it is certain"),
                (r"$A \land B$", r"the intersection"),
                (r"$A \lor B$", r"the span: \ the smallest subspace containing both"),
                (r"$\lnot A$", r"the orthogonal complement")]
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.0 - 0.8 * i
            l1 = label(a, font_size=28, color=GOAL)
            l2 = label(b, font_size=26)
            l1.move_to([-5.6 + l1.width / 2, y, 0])
            l2.move_to([-2.6 + l2.width / 2, y, 0])
            tab.add(VGroup(l1, l2))
        note_ = label(r"the span contains states in \textit{neither} subspace: \ superpositions", font_size=26,
                      color=BAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1936 Garrett Birkhoff and John von Neumann asked what logic quantum mechanics obeys. "
            "<bookmark mark='a'/>A quantum proposition, such as 'the particle is in this region', corresponds to a "
            "subspace of the space of states: the states in which a measurement would certainly confirm it. "
            "<bookmark mark='b'/>'And' is intersection, as for sets. <bookmark mark='c'/>But 'or' is not union. "
            "It is the span, the smallest subspace containing both, and the span contains superpositions, states "
            "in neither of the two subspaces. <bookmark mark='d'/>And 'not' is the orthogonal complement."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]))
        self.clear_scene()

    def distributivity(self):
        d = load("quantum")
        c = np.array([-3.2, -0.3, 0])
        plane = Square(side_length=5.2, stroke_width=0, fill_color=P.WORLD, fill_opacity=0.0).move_to(c)
        p = line_through(0, color=GOAL, center=c)
        q = line_through(90, color=P.CLAIM, center=c)
        r = line_through(45, color=BOTH, center=c)
        lp = MathTex("p", font_size=36, color=GOAL).next_to(p.get_end(), RIGHT, buff=0.1)
        lq = MathTex("q", font_size=36, color=P.CLAIM).next_to(q.get_end(), UP, buff=0.1)
        lr = MathTex("r", font_size=36, color=BOTH).next_to(r.get_end(), UR, buff=0.05)
        lab = label(r"polarization at $0^\circ$, $90^\circ$, $45^\circ$: \ three lines in a plane", font_size=22,
                    color=GREY_A).next_to(plane, DOWN, buff=0.2)
        eqs = VGroup(
            MathTex(r"q \lor r", r"= \text{the whole plane}", font_size=34),
            MathTex(r"p \land (q \lor r)", r"= p", font_size=34),
            MathTex(r"p \land q = 0, \quad p \land r = 0", font_size=34),
            MathTex(r"(p \land q) \lor (p \land r)", r"= 0", font_size=34),
            MathTex(r"p \land (q \lor r) \ \neq\ (p \land q) \lor (p \land r)", font_size=36, color=BAD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.2, 0])
        chk = label(rf"the Reasoner: \ dimensions {d['lhs_dim']} and {d['rhs_dim']} \ $\checkmark$", font_size=22,
                    color=OK).next_to(eqs, DOWN, buff=0.35)
        assert not d["equal"] and d["q_or_r_dim"] == 2
        with self.voiceover(
            "Now a classical law breaks. Take the polarization of a photon, whose states form a plane. "
            "<bookmark mark='a'/>Let p be 'polarized horizontally', q 'polarized vertically', and r 'polarized at "
            "forty-five degrees'. Each is a line through the origin. <bookmark mark='b'/>q or r is the span of two "
            "different lines: the whole plane. <bookmark mark='c'/>So p and, q or r, is just p. "
            "<bookmark mark='d'/>But p and q meet only at zero, and so do p and r. <bookmark mark='e'/>So p and q, "
            "or p and r, is zero. <bookmark mark='f'/>The distributive law, which holds in every Boolean algebra "
            "and every truth table, fails. The Reasoner computes the subspaces directly: one dimension on the left, "
            "zero on the right."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(p), Create(q), Create(r), FadeIn(lp), FadeIn(lq), FadeIn(lr), FadeIn(lab))
            vo.wait_until("b")
            self.play(plane.animate.set_fill(opacity=0.15), FadeIn(eqs[0]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[1]), Indicate(p, color=GOAL))
            vo.wait_until("d")
            self.play(FadeIn(eqs[2]), plane.animate.set_fill(opacity=0.0),
                      Flash(c, color=WHITE, line_length=0.25))
            vo.wait_until("e")
            self.play(FadeIn(eqs[3]))
            vo.wait_until("f")
            self.play(FadeIn(eqs[4]), FadeIn(chk))
        self.clear_scene()

    def polarizers(self):
        head = label(r"Three polarizers \ (Malus's law: \ a filter at angle $\theta$ passes $\cos^2\theta$)",
                     font_size=28, color=CONN).to_edge(UP, buff=0.45)

        def setup(angles, y):
            g = VGroup()
            inten = 0.5
            xs = np.linspace(-4.6, 2.2, len(angles) + 1)
            beam = [1.0]
            prev = None
            for a in angles:
                inten = 0.5 if prev is None else inten * np.cos(np.deg2rad(a - prev)) ** 2
                inten = 0.0 if inten < 1e-12 else inten
                beam.append(inten)
                prev = a
            for i, a in enumerate(angles):
                f = VGroup(Rectangle(width=0.25, height=1.3, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_D,
                                     fill_opacity=0.5),
                           line_through(a + 90, 1.0, color=GOAL, width=3)).move_to([xs[i + 1], y, 0])
                g.add(f, label(rf"${a}^\circ$", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.12))
            for i in range(len(angles) + 1):
                x0 = xs[i] + (0.2 if i else -0.9)
                x1 = xs[i + 1] - 0.2 if i < len(angles) else 4.0
                g.add(Line([x0, y, 0], [x1, y, 0], color=HALF, stroke_width=2 + 14 * beam[i],
                           stroke_opacity=0.25 + 0.75 * beam[i]))
            g.add(MathTex(rf"{beam[-1]:.3f}".rstrip("0").rstrip(".") if beam[-1] else "0", font_size=34,
                          color=OK if beam[-1] else BAD).move_to([4.8, y, 0]))
            return g, beam[-1]

        a, ia = setup([0, 90], 1.0)
        b, ib = setup([0, 45, 90], -1.6)
        la = label(r"crossed: \ nothing passes", font_size=22, color=BAD).next_to(a, DOWN, buff=0.1).set_x(4.8)
        lb = label(r"add a filter between them: \ one eighth passes", font_size=22, color=OK).next_to(b, DOWN,
                                                                                                buff=0.1).set_x(3.6)
        assert ia == 0 and abs(ib - 0.125) < 1e-9
        with self.voiceover(
            "You can see this structure on a desk, with three polarizing filters. <bookmark mark='a'/>Light "
            "through a horizontal filter, then a vertical one: nothing gets through. <bookmark mark='b'/>Now slide "
            "a third filter, at forty-five degrees, between them. Light passes: one eighth of it. Adding an "
            "obstacle lets more through. <bookmark mark='c'/>Classically that is absurd. In the geometry of "
            "subspaces it is just Malus's law, applied twice: each filter projects the state onto its own line."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(Indicate(b[-1], color=OK))
        self.clear_scene()

    def putnam(self):
        hc = history_card(1968, r"Hilary Putnam", r"`Is logic empirical?'", width=5.2, color=HIST).to_corner(
            UL, buff=0.35)
        rows = VGroup(label(r"Putnam: \ as Euclid's geometry gave way to Einstein's, \ classical logic should give way "
                            r"to quantum logic", font_size=24),
                      label(r"Dummett (1976): \ the quantum `or' is not our `or'; \ the dispute is about meaning",
                            font_size=24),
                      label(r"today: \ the lattice of subspaces is standard mathematics \ (orthomodular lattices);",
                            font_size=24),
                      label(r"few physicists or philosophers think it replaces the logic we reason with", font_size=24),
                      label(r"Part 26: \ Kochen--Specker, \ Bell, \ and what the quantum world is like", font_size=24,
                            color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hc, DOWN, buff=0.5)
        rows.set_x(0)
        with self.voiceover(
            "In 1968 Hilary Putnam drew a radical conclusion. <bookmark mark='a'/>Euclid's geometry was once "
            "thought a priori, and physics overturned it. Quantum mechanics, he argued, overturns classical logic "
            "in the same way: distributivity is simply false of the world. <bookmark mark='b'/>Michael Dummett "
            "replied that the quantum 'or' is not the 'or' we reason with, so the dispute is about meaning, not "
            "about facts. <bookmark mark='c'/>Today the lattice of subspaces is standard mathematics, studied as "
            "orthomodular lattices, but few think it replaces the logic in which physicists themselves argue. "
            "<bookmark mark='d'/>Putnam later abandoned the view. Part 26 returns to the quantum world, and to "
            "theorems about what it can and cannot be like."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
