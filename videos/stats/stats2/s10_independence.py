from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

R_, G_, B_ = "#F26D6D", "#7BD88F", "#5DADEC"


def tetra_faces():
    """A regular tetrahedron: four vertices and its faces (vertex indices) with their paint."""
    v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / np.sqrt(3) * 2.4
    faces = [((1, 2, 3), "R"), ((0, 2, 3), "G"), ((0, 1, 3), "B"), ((0, 1, 2), "RGB")]
    return v, faces


def rot(angle, tilt):
    ca, sa, ct, st = np.cos(angle), np.sin(angle), np.cos(tilt), np.sin(tilt)
    rz = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
    return rx @ rz


def face_mob(pts, paint):
    if paint == "RGB":
        # three stripes, one of each colour
        p0, p1, p2 = pts
        g = VGroup()
        for k, c in enumerate((R_, G_, B_)):
            a, b = k / 3, (k + 1) / 3
            quad = [p0 + (p1 - p0) * a, p0 + (p1 - p0) * b, p0 + (p2 - p0) * b, p0 + (p2 - p0) * a]
            g.add(Polygon(*quad, stroke_width=0, fill_color=c, fill_opacity=0.95))
        g.add(Polygon(*pts, stroke_color=WHITE, stroke_width=2, fill_opacity=0))
        return g
    col = {"R": R_, "G": G_, "B": B_}[paint]
    return Polygon(*pts, stroke_color=WHITE, stroke_width=2, fill_color=col, fill_opacity=0.9)


class Independence(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.tetrahedron()
        self.conditional()
        self.lesson()

    def card(self):
        card = chapter_card(9, r"Independence", r"When does knowing one thing tell you nothing about another?",
                            lit=(1933,), part=PART)
        with self.voiceover("Chapter nine. Independence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        dfn = definition_card(r"Independent events", r"$P(A \cap B) = P(A)\,P(B)$; \ equivalently, \ when "
                              r"$P(B) > 0$, \ $P(A \mid B) = P(A)$: \ learning $B$ does not change the chance of $A$",
                              color=EXACT, width=6.6, font_size=24).move_to([-3.2, 1.6, 0])
        grid = outcome_grid(size=0.5, buff=0.05, dice_size=0.18).move_to([3.6, 0.4, 0])
        ev_a = lambda i, j: i % 2 == 0  # noqa: E731
        ev_b = lambda i, j: j >= 5  # noqa: E731
        la = MathTex(r"A: \text{ first die even}", font_size=28, color=SIM).move_to([-3.4, -0.6, 0])
        lb = MathTex(r"B: \text{ second die} \ge 5", font_size=28, color=EVENT).next_to(la, DOWN, buff=0.25)
        chk = MathTex(r"P(A \cap B) = \tfrac{6}{36}", r"=", r"\tfrac12 \cdot \tfrac13", font_size=32)
        chk.next_to(lb, DOWN, buff=0.4)
        chk[2].set_color(EXACT)
        warn = label(r"independent is \emph{not} disjoint: \ disjoint events with positive probability are "
                     r"dependent", font_size=24, color=S.RESID).to_edge(DOWN, buff=0.35)
        intro = label('What independence means', font_size=36)
        with self.voiceover(
            "Squaring one in eight thousand five hundred assumed independence. So what is it, exactly? "
            "<bookmark mark='a'/> Two events are independent if the probability that both happen is the product of "
            "their probabilities. Equivalently, learning that one happened leaves the other's probability unchanged. "
            "<bookmark mark='b'/> On the two-dice grid, let A be the first die showing an even number, half the "
            "columns, <bookmark mark='c'/> and B the second die showing five or six, a third of the rows. "
            "<bookmark mark='d'/> Their overlap is six cells of thirty-six: exactly a half times a third. The dice "
            "don't influence each other, and the arithmetic says so. <bookmark mark='e'/> Don't confuse independent "
            "with disjoint. Disjoint events can't both happen, so learning that one happened changes the other's "
            "probability to zero. When both have positive probability, they are dependent, though the dependence "
            "need not be perfect."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(dfn, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01), FadeIn(la))
            self.play(*[grid.cell[k][0].animate.set_fill(SIM, opacity=0.45) for k in grid.cell if ev_a(*k)])
            vo.wait_until("c")
            self.play(FadeIn(lb), *[grid.cell[k][0].animate.set_stroke(EVENT, width=3) for k in grid.cell if ev_b(*k)])
            vo.wait_until("d")
            self.play(*[Indicate(grid.cell[k], color=WHITE, scale_factor=1.15) for k in grid.cell
                        if ev_a(*k) and ev_b(*k)])
            self.play(Write(chk))
            vo.wait_until("e")
            self.play(FadeIn(warn))
        self.clear_scene()

    def tetrahedron(self):
        d = load("independence")
        v, faces = tetra_faces()
        angle = ValueTracker(0.4)
        center = np.array([-3.4, -0.2, 0])

        def draw():
            M = rot(angle.get_value(), -1.05)
            P = v @ M.T
            order = sorted(faces, key=lambda f: np.mean(P[list(f[0]), 2]))  # far faces first
            g = VGroup()
            for idx, paint in order:
                pts = [center + np.array([P[i, 0], P[i, 1], 0]) for i in idx]
                g.add(face_mob(pts, paint))
            return g

        tet = always_redraw(draw)
        hc = theorem_card(r"Bernstein's tetrahedron", r"one face red, one green, one blue, \ and one painted with "
                          r"all three", who=r"S. N. Bernstein", color=S.MUSEUM, width=5.6, font_size=22,
                          kind=r"Example")
        hc.move_to([3.6, 2.4, 0])
        rows = VGroup(
            MathTex(r"P(R) = P(G) = P(B)", r"=", r"\tfrac12", font_size=32),
            MathTex(r"P(R \cap G) = P(R \cap B) = P(G \cap B)", r"=", r"\tfrac14", r"= \tfrac12 \cdot \tfrac12",
                    font_size=30),
            MathTex(r"P(R \cap G \cap B)", r"=", r"\tfrac14", r"\ne \tfrac18", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.3, 0])
        for r in rows:
            r[2].set_color(EXACT)
        rows[2][3].set_color(S.RESID)
        cap = label(r"$R$: \ the face it lands on shows red \ (two of four faces)", font_size=22, color=GREY_B)
        cap.next_to(rows, UP, buff=0.3)
        take = label(r"pairwise independent, \ \emph{not} mutually independent", font_size=28,
                     color=S.ACCENT).to_edge(DOWN, buff=0.6)
        dfn = label(r"mutual: \ the product rule for \emph{every} subcollection", font_size=22, color=GREY_B)
        dfn.next_to(take, DOWN, buff=0.15)
        with self.voiceover(
            "For three events, independence is subtler than it looks. Here's an example from the Russian "
            "mathematician Sergei Bernstein. <bookmark mark='a'/> Take a tetrahedron, a four-sided die. Paint one "
            "face red, one green, one blue, and the fourth with all three colours. Roll it, and look at the face it "
            "lands on. <bookmark mark='b'/> Red appears on two of the four faces, so the chance of seeing red is a "
            "half; the same for green and for blue. <bookmark mark='c'/> Red and green together appear only on the "
            "striped face: a quarter, which is a half times a half. The same for every pair. So every pair of "
            f"colours is independent. <bookmark mark='d'/> But all three together also appear only on the striped "
            "face: a quarter, not an eighth. If you know you see red and green, you know you see blue. "
            "<bookmark mark='e'/> The three events are pairwise independent, but not mutually independent. Mutual "
            "independence demands the product rule for every subcollection, pairs, triples and all. When this "
            "series says independent, it means mutually."
        ) as vo:
            self.add(tet)
            self.play(angle.animate.set_value(0.4 + TAU), run_time=6.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(hc), angle.animate.set_value(0.4 + 1.5 * TAU), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(cap), Write(rows[0]), angle.animate.set_value(0.4 + 2 * TAU), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(Write(rows[1]), angle.animate.set_value(0.4 + 2.5 * TAU), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(Write(rows[2]), angle.animate.set_value(0.4 + 3 * TAU), run_time=3.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(take), FadeIn(dfn), angle.animate.set_value(0.4 + 3.5 * TAU), run_time=3.0,
                      rate_func=linear)
        _ = d
        tet.clear_updaters()
        self.clear_scene()

    def conditional(self):
        d = load("independence")
        A = axes([0, 4], [0, 1.0], x_length=6.4, y_length=4.4, ylabel=r"P(test B positive)", yticks=[0, 0.5, 1.0],
                 center=[-3.3, -0.4, 0])
        ax = A.ax
        pairs = [(r"all adults", d["pb"], d["pb_a"]), (r"with the condition", d["pb_sick"], d["pb_a_sick"]),
                 (r"without it", d["pb_well"], d["pb_a_well"])]
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        xs = [0.6, 2.0, 3.4]
        for x, (name, p, pa) in zip(xs, pairs):
            for dx, val, col in ((-0.22, p, GREY_B), (0.22, pa, POS)):
                h = max(val, 0.004)
                b = Rectangle(width=0.4, height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to(ax.c2p(x + dx, h / 2))
                bars.add(b)
                vals.add(MathTex(f"{val:.2f}", font_size=22, color=col).next_to(b, UP, buff=0.08))
            labs.add(label(name, font_size=22, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.2))
        leg = legend([(GREY_B, r"overall"), (POS, r"given test A positive")], font_size=22).move_to([3.0, 2.3, 0])
        notes = VGroup(
            label(r"overall: \ test A positive makes B \emph{three times} likelier", font_size=24, color=WHITE),
            label(r"given the condition, \ or its absence: \ A tells you nothing", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.5, 0])
        for n_ in notes:
            if n_.width > 5.8:
                n_.width = 5.8
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.5, 0])
        dfn = definition_card(r"Conditional independence", r"$P(A \cap B \mid C) = P(A \mid C)\, P(B \mid C)$: \ "
                              r"independent once $C$ is known", color=EXACT, width=5.6, font_size=22)
        dfn.move_to([3.7, -1.9, 0])
        tag = simulated_tag()
        with self.voiceover(
            "Independence can also appear and disappear when you condition. <bookmark mark='a'/> Go back to the "
            "World's two screening tests. Overall, among all adults, a positive result on test A makes a positive on "
            f"test B three times likelier: {d['pb_a']:.2f} instead of {d['pb']:.2f}. The tests are strongly "
            "dependent. <bookmark mark='b'/> But look within the people who have the condition: test B is positive "
            f"{100 * d['pb_sick']:.0f} percent of the time whatever test A said. <bookmark mark='c'/> And among those "
            f"without it, {100 * d['pb_well']:.0f} percent, whatever test A said. <bookmark mark='d'/> Once you know "
            "whether someone has the condition, the tests tell you nothing about each other. They're conditionally "
            "independent given the condition, and dependent overall, because both depend on it. "
            "<bookmark mark='e'/> That's exactly the assumption we used to multiply two likelihood ratios of "
            "eighteen. Conditional independence is the workhorse of statistical modelling, from naive Bayes to "
            "hierarchical models to causal graphs, where a common cause makes its effects dependent; Part 36 is "
            "built on that observation."
        ) as vo:
            self.play(FadeIn(A), FadeIn(labs), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(vals[0]), FadeIn(vals[1]))
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN), FadeIn(vals[2]), FadeIn(vals[3]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[4], DOWN), GrowFromEdge(bars[5], DOWN), FadeIn(vals[4]), FadeIn(vals[5]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(dfn, shift=UP * 0.2))
        self.clear_scene()

    def lesson(self):
        lines = VGroup(
            label(r"independence is a strong, specific claim: \ $P(A \cap B) = P(A)P(B)$", font_size=30),
            label(r"pairwise is not mutual \ (Bernstein)", font_size=30),
            label(r"dependence can vanish given a common cause, \ and appear given a common effect", font_size=30),
            label(r"the World's tests, \ a family's two cot deaths: \ check it, don't assume it", font_size=30,
                  color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        with self.voiceover(
            "So independence is a strong and specific claim, not a default. <bookmark mark='a'/> It's a product "
            "rule. <bookmark mark='b'/> For many events, it must hold for every subcollection, not just in pairs. "
            "<bookmark mark='c'/> And it depends on what you condition on: dependence can vanish once you know a "
            "common cause, and, as we'll see in Part 36, appear once you condition on a common effect. "
            "<bookmark mark='d'/> Two screening tests, two deaths in one family: whenever a calculation multiplies "
            "probabilities, ask whether independence has been checked, or only assumed."
        ) as vo:
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(lines[k], shift=RIGHT * 0.2))
        self.clear_scene()
