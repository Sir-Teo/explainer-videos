from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, gate, load

GAIN = 6.0


def inv(v):
    return 0.5 * (1 - np.tanh(GAIN * (v - 0.5)))


class Dynamics(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.portrait()
        self.saddle()

    def card(self):
        card = chapter_card(2, r"Two wells and a saddle", r"Why does a latch settle, and where can it get stuck?",
                            part=PART)
        with self.voiceover("Chapter two. Two wells and a saddle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def model(self):
        head = label(r"Look closer: \ two inverters, \ two voltages", font_size=36).to_edge(UP, buff=0.35)
        g1 = gate("NOT", size=0.9).move_to(LEFT * 4.2 + UP * 1.4)
        g2 = gate("NOT", size=0.9).rotate(PI).move_to(LEFT * 4.2 + UP * 0.0)
        w = VGroup(
            VMobject(color=WIRE, stroke_width=3).set_points_as_corners([g1.out(), g1.out() + RIGHT * 0.5,
                                                                       g2.inp[0]() + RIGHT * 0.5, g2.inp[0]()]),
            VMobject(color=WIRE, stroke_width=3).set_points_as_corners([g2.out(), g2.out() + LEFT * 0.5,
                                                                       g1.inp[0]() + LEFT * 0.5, g1.inp[0]()]))
        l1 = MathTex("v_1", font_size=32, color=DATA).next_to(g1.out() + RIGHT * 0.5, RIGHT, buff=0.1)
        l2 = MathTex("v_2", font_size=32, color=FUNC).next_to(g2.out() + LEFT * 0.5, LEFT, buff=0.1)
        eqs = VGroup(MathTex(r"\tau\, \dot v_1 = f(v_2) - v_1", font_size=38, color=CODE),
                     MathTex(r"\tau\, \dot v_2 = f(v_1) - v_2", font_size=38, color=CODE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT * 3.6 + DOWN * 1.8)
        why = note(r"each output charges its wire toward $f$ of its input, \\ with Part 3's $RC$ time constant $\tau$",
                   font_size=22).next_to(eqs, DOWN, buff=0.25).align_to(eqs, LEFT)
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=3.6, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(RIGHT * 3.4 + UP * 0.4)
        fc = ax.plot(inv, x_range=[0, 1], color=CTRL, stroke_width=3)
        fl = MathTex(r"f(v)", font_size=28, color=CTRL).next_to(ax.c2p(0.2, 0.95), RIGHT, buff=0.1)
        sl = note(r"an inverter's transfer curve: \ slope $-3$ at the threshold, \\ gentler than Part 3's, \ to see",
                  font_size=20).next_to(ax, DOWN, buff=0.3)
        with self.voiceover(
            "To see what really happens inside a latch, stop thinking in zeros and ones. <bookmark mark='a'/> The "
            "heart of it is two inverters, each driving the other, and each output is a voltage, v one and v two. "
            "<bookmark mark='b'/> An inverter's output does not jump; as Part 3 showed, it charges its wire towards "
            "the value its transfer curve f says, with a time constant tau. So the voltages obey two differential "
            "equations: each one relaxes towards f of the other. <bookmark mark='c'/> Here f is a smooth inverter "
            "curve, a little gentler than a real one so that the picture is easy to see. The latch is now a "
            "dynamical system with two variables, and we can draw its whole behaviour at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), Create(w), FadeIn(l1), FadeIn(l2))
            vo.wait_until("a")
            self.play(Indicate(VGroup(g1, g2, w), scale_factor=1.03))
            vo.wait_until("b")
            self.play(Write(eqs), FadeIn(why))
            vo.wait_until("c")
            self.play(Create(ax), Create(fc), FadeIn(fl), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=5.6, y_length=5.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 2.6 + DOWN * 0.3)
        xl = MathTex("v_1", font_size=28, color=DATA).next_to(ax.c2p(1, 0), RIGHT, buff=0.25)
        yl = MathTex("v_2", font_size=28, color=FUNC).next_to(ax.c2p(0, 1), UP, buff=0.2)
        return ax, VGroup(xl, yl)

    def portrait(self):
        d = load("phase")
        head = label(r"The phase portrait", font_size=38).to_edge(UP, buff=0.3)
        ax, labs = self.plane()
        arrows = VGroup()
        for a, b, da, db in d["arrows"]:
            m = np.hypot(da, db)
            if m < 1e-6:
                continue
            L = 0.17
            p = ax.c2p(a, b)
            dirn = np.array([da, db, 0]) / m
            arrows.add(Arrow(p - dirn * L / 2, p + dirn * L / 2, buff=0, stroke_width=1.6, color=GREY_C,
                             max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
        v = np.linspace(0, 1, 200)
        null1 = VMobject(color=DATA, stroke_width=3).set_points_as_corners([ax.c2p(inv(y), y) for y in v])
        null2 = VMobject(color=FUNC, stroke_width=3).set_points_as_corners([ax.c2p(x, inv(x)) for x in v])
        nl = VGroup(MathTex(r"\dot v_1 = 0", font_size=24, color=DATA).next_to(ax.c2p(inv(0.85), 0.85), RIGHT, buff=0.1),
                    MathTex(r"\dot v_2 = 0", font_size=24, color=FUNC).next_to(ax.c2p(0.85, inv(0.85)), UP, buff=0.1))
        trajs = VGroup()
        for tr in d["trajs"]:
            trajs.add(VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners([ax.c2p(x, y) for x, y in tr]))
        st = VGroup(*[Dot(ax.c2p(*p), radius=0.11, color=YES) for p in d["stable"]])
        sad = Dot(ax.c2p(0.5, 0.5), radius=0.11, color=NO)
        side = VGroup(
            label(r"two stable states: \ approximately $(0, 1)$ and $(1, 0)$", font_size=26, color=YES),
            label(r"one saddle: \ $v_1 = v_2 = \tfrac12$", font_size=26, color=NO),
            label(r"the diagonal is the watershed: \\ start above it and you end at $(0, 1)$, \\ below it at $(1, 0)$",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + UP * 0.4)
        with self.voiceover(
            "Every point of this square is a possible state of the latch: a voltage on each wire. <bookmark "
            "mark='a'/> At every point, the equations give a direction of motion, drawn as a small arrow. "
            "<bookmark mark='b'/> The two curves where one voltage stops changing cross in three places, and "
            "those are the equilibria. <bookmark mark='c'/> Start the latch anywhere and follow the arrows. "
            "Almost every start ends in one of two corners: v one low and v two high, or the reverse. Those are "
            "the two stable states, the zero and the one. <bookmark mark='d'/> The third crossing, in the middle, "
            "is a saddle: the arrows lead into it along the diagonal and away from it in every other direction. "
            "The diagonal is the watershed between the two basins. A latch that starts exactly on it, as an "
            "exactly symmetric analog release would, unlike the digital model's oscillation, slides into the "
            "saddle and has no reason to leave."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(labs), FadeIn(arrows))
            vo.wait_until("a")
            self.play(Indicate(arrows, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(null1), Create(null2), FadeIn(nl), run_time=1.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in trajs], lag_ratio=0.08), run_time=4.0)
            self.play(FadeIn(st), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(sad), FadeIn(side[1]))
            self.play(Create(DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=NO, stroke_width=2)), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def saddle(self):
        d = load("phase")
        head = label(r"Near the saddle", font_size=38).to_edge(UP, buff=0.35)
        J = MathTex(r"J = \begin{pmatrix} -1 & f'(\tfrac12) \\ f'(\tfrac12) & -1 \end{pmatrix}, \qquad f'(\tfrac12) = -3",
                    font_size=38, color=CODE).move_to(UP * 1.8)
        eig = VGroup(
            MathTex(r"\lambda = -1 - |f'| = -4 \quad \text{along } v_1 + v_2: \ \text{common-mode perturbations decay}",
                    font_size=32, color=YES),
            MathTex(r"\lambda = |f'| - 1 = +2 \quad \text{along } v_1 - v_2: \ \text{voltage imbalance grows}", font_size=32,
                    color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.2)
        grow = MathTex(r"v_1 - v_2 \approx \delta\, e^{\lambda t / \tau} \quad \Rightarrow \quad t_{\text{resolve}} "
                       r"\approx \frac{\tau}{\lambda} \ln \frac{\Delta}{|\delta|}", font_size=38, color=HEAD).move_to(
            DOWN * 1.4)
        foot = label(r"a tiny imbalance $\delta$ takes a long time to grow: \ as $\delta \to 0$, \ $t \to \infty$",
                     font_size=28, color=NO).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Zoom in on the saddle, where everything about metastability is decided. <bookmark mark='a'/> Near it "
            "the equations are almost linear, and their matrix has the inverter's slope off the diagonal. "
            "<bookmark mark='b'/> Its two eigenvalues, measured in units of the gate RC time, tell the story. "
            "Along the diagonal, where both voltages move together, the eigenvalue is minus four: any common "
            "motion dies out. Across the diagonal, along the difference of the voltages, it is plus two: any "
            "imbalance grows exponentially. <bookmark mark='c'/> So an imbalance delta grows like delta times e "
            "to the lambda t, and the time to reach a clean zero or one is the logarithm of one over delta, "
            "divided by lambda. A latch that starts a little off balance resolves quickly. One that starts very "
            "nearly balanced takes longer, and as the imbalance shrinks to zero the time grows without bound. A "
            "steeper inverter, a larger lambda, makes it faster, but never instant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(J))
            vo.wait_until("a")
            self.play(Indicate(J, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(eig[0]))
            self.play(FadeIn(eig[1]))
            vo.wait_until("c")
            self.play(Write(grow))
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
