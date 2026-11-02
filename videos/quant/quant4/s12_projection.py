from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, INFO, LOSS, MART, P_C, PART, load, real_data

P3 = np.array([0.5, 0.3, 0.2])
X3 = np.array([3.0, 0.0, 1.0])
SQ = np.sqrt(P3)


def coords(v):
    """A random variable on {a, b, c} drawn in the coordinates sqrt(p_i) x_i: Euclidean geometry = L2(P) geometry."""
    return SQ * np.asarray(v, float)


class Projection(VoiceoverScene, ThreeDScene):
    def construct(self):
        c = load("condexp")
        self.card()
        self.definition()
        self.picture(c)
        self.market(c)
        self.lab(c)

    def card(self):
        c = chapter_card(2, r"Conditional expectation is a projection", r"What is the best forecast you can make?",
                         part=PART)
        with self.voiceover("Chapter two. Conditional expectation is a projection."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definition(self):
        cols = {r"\mathbb{E}[X \mid \mathcal{G}]": MART, r"Y": MART}
        rows = [cmath(r"Y = \mathbb{E}[X \mid \mathcal{G}]", r"\iff", r"Y\ \mathcal{G}\text{-measurable},\ "
                      r"\mathbb{E}[X\mathbf{1}_A] = \mathbb{E}[Y\mathbf{1}_A]\ \ \forall A \in \mathcal{G}", font_size=34),
                cmath(r"Y", r"=", r"\sum_j \frac{\mathbb{E}[X\mathbf{1}_{B_j}]}{P(B_j)}\,\mathbf{1}_{B_j}", font_size=36,
                      colors=cols),
                cmath(r"\mathbb{E}[(X - Y)\,Z]", r"=", r"0 \quad \text{for every } \mathcal{G}\text{-measurable } Z",
                      font_size=36),
                cmath(r"\mathbb{E}[(X - Z)^2]", r"=", r"\mathbb{E}[(X - Y)^2] + \mathbb{E}[(Y - Z)^2]", font_size=36),
                cmath(r"\mathbb{E}[ZX \mid \mathcal{G}]", r"=", r"Z\,\mathbb{E}[X \mid \mathcal{G}]", font_size=36),
                cmath(r"\mathbb{E}\big[\mathbb{E}[X \mid \mathcal{G}] \mid \mathcal{H}\big]", r"=",
                      r"\mathbb{E}[X \mid \mathcal{H}] \quad (\mathcal{H} \subset \mathcal{G})", font_size=36),
                cmath(r"\varphi\big(\mathbb{E}[X \mid \mathcal{G}]\big)", r"\le",
                      r"\mathbb{E}[\varphi(X) \mid \mathcal{G}]; \quad \sigma(X) \perp \mathcal{G} \Rightarrow "
                      r"\mathbb{E}[X \mid \mathcal{G}] = \mathbb{E}X", font_size=34)]
        whys = [why(r"Kolmogorov's definition: computable from $\mathcal{G}$, and the right average on every event of "
                    r"$\mathcal{G}$"),
                why(r"on a partition, take $A = B_j$: the average over each block"),
                why(r"true for $Z = \mathbf{1}_A$ by the definition, so for sums of them, and their limits"),
                why(r"expand the square: the cross term is the line above, so $Y$ is the closest point (Pythagoras)"),
                why(r"taking out what is known: check the definition with $Z\mathbf{1}_A$"),
                why(r"the tower: both sides satisfy the definition on every $A \in \mathcal{H} \subset \mathcal{G}$"),
                why(r"Jensen, from the supporting lines of a convex $\varphi$; independent information is no information")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.62, edge=6.9)
        head = label(r"Kolmogorov's conditional expectation", font_size=30, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "What is the best forecast of tomorrow's return, given today's? Kolmogorov's definition answers it. Y is "
            "the conditional expectation of X given G if Y can be computed from G and has the same average as X on "
            "every event of G. <bookmark mark='a'/> On a partition, apply it block by block: Y is the average of X "
            "over each block. <bookmark mark='b'/> The error, X minus Y, is uncorrelated with anything computable "
            "from G: true for indicators by the definition, so for their sums and limits. <bookmark mark='c'/> "
            "Expand the squared distance from X to any computable Z, and the cross term vanishes: Pythagoras. So Y "
            "is the closest computable variable, the best forecast in mean square. <bookmark mark='d'/> What is "
            "known comes out as a constant. <bookmark mark='e'/> Conditioning on more and then on less is "
            "conditioning on less: the tower property. <bookmark mark='f'/> A convex function of a forecast is below "
            "the forecast of the convex function, Jensen's inequality; and independent information teaches nothing."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
            vo.wait_until("f")
            step(6)
        self.wait(0.4)
        self.clear_scene()

    def picture(self, c):
        ax = ThreeDAxes(x_range=[0, 2.5, 0.5], y_range=[0, 2.0, 0.5], z_range=[0, 1.2, 0.5], x_length=6.0,
                        y_length=4.8, z_length=2.9,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        ax.shift(LEFT * 1.6 + DOWN * 0.4)
        o = ax.c2p(0, 0, 0)
        x = coords(X3)
        y = coords(c["toy"])
        h = coords([c["toy_mean"]] * 3)
        u1 = coords([1, 1, 0])
        u2 = coords([0, 0, 1])
        s1, s2 = 2.6 / np.linalg.norm(u1), 1.25 / np.linalg.norm(u2)
        corners = [np.zeros(3), u1 * s1, u1 * s1 + u2 * s2, u2 * s2]
        plane = Polygon(*[ax.c2p(*p_) for p_ in corners], stroke_color=INFO, stroke_width=1.5, fill_color=INFO,
                        fill_opacity=0.18)
        dline = coords([1, 1, 1])
        line = Line(o, ax.c2p(*(dline / np.linalg.norm(dline) * 2.4)), color=DRIFT, stroke_width=4)
        vX = Arrow3D(o, ax.c2p(*x), color=WHITE, resolution=8)
        vY = Arrow3D(o, ax.c2p(*y), color=MART, resolution=8)
        vH = Arrow3D(o, ax.c2p(*h), color=DRIFT, resolution=8)
        err = DashedLine(ax.c2p(*x), ax.c2p(*y), color=GREY_B)
        err2 = DashedLine(ax.c2p(*y), ax.c2p(*h), color=DRIFT)
        err3 = DashedLine(ax.c2p(*x), ax.c2p(*h), color=GREY_C)
        # the right angle at the foot: a small square in the plane spanned by the error and the plane direction
        e_dir = (x - y) / np.linalg.norm(x - y)
        p_dir = (y - h) / np.linalg.norm(y - h)
        k = 0.18
        ra = VMobject(stroke_color=GREY_A, stroke_width=2).set_points_as_corners(
            [ax.c2p(*(y + k * e_dir)), ax.c2p(*(y + k * e_dir + k * p_dir)), ax.c2p(*(y + k * p_dir))])
        head = label(r"$\Omega = \{a, b, c\}$, $P = (0.5, 0.3, 0.2)$; a variable is an arrow with coordinates "
                     r"$\sqrt{p_i}\,x_i$", font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        side = VGroup(
            MathTex(r"X = (3, 0, 1)", font_size=30),
            label(r"plane: what $\mathcal{G} = \sigma(\{a,b\}, \{c\})$ can compute", font_size=20, color=INFO),
            MathTex(rf"\mathbb{{E}}[X \mid \mathcal{{G}}] = ({c['toy'][0]:.3f}, {c['toy'][1]:.3f}, {c['toy'][2]:g})",
                    font_size=30, color=MART),
            label(r"line: the constants (no information)", font_size=20, color=DRIFT),
            MathTex(rf"\mathbb{{E}}X = {c['toy_mean']:.1f}", font_size=30, color=DRIFT),
            label(r"project to the plane, then the line $=$ project to the line: the tower", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.4).shift(UP * 0.4)
        for mob in (head, side):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-40 * DEGREES, zoom=0.9)
        with self.voiceover(
            "Here is that Pythagoras theorem as a picture. Three worlds with probabilities a half, three tenths and a "
            "fifth; a variable is an arrow, each coordinate stretched by the square root of its probability, so length "
            "is root mean square. <bookmark mark='a'/> If you can only tell whether the world is c, what you can "
            "compute is a plane. Drop a perpendicular from X: the foot, one point eight seven five, one point eight "
            "seven five, and one, is the conditional expectation. <bookmark mark='b'/> Turn the picture: a true right "
            "angle. <bookmark mark='c'/> Knowing nothing, you can compute only constants, a line. Project the foot "
            f"onto it, or X directly: both land on {c['toy_mean']:.1f}. The tower property, as geometry."
        ) as vo:
            self.play(Create(ax), FadeIn(head), FadeIn(side[0]))
            self.play(FadeIn(vX))
            vo.wait_until("a")
            self.play(FadeIn(plane), FadeIn(side[1]))
            self.play(Create(err), FadeIn(vY), FadeIn(side[2]))
            self.play(Create(ra))
            vo.wait_until("b")
            self.move_camera(theta=80 * DEGREES, phi=75 * DEGREES, run_time=4)
            vo.wait_until("c")
            self.play(Create(line), FadeIn(side[3]))
            self.play(Create(err2), FadeIn(vH), FadeIn(side[4]))
            self.play(Create(err3), FadeIn(side[5]))
            self.move_camera(theta=-40 * DEGREES, phi=68 * DEGREES, run_time=3)
        self.wait(0.4)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    def market(self, c):
        eras = c["eras"]
        keys = ["19260701", "19750101", "20000101"]
        names = [r"1926--74", r"1975--99", r"2000--20"]
        g = axes([0, 9], [-15, 20], x_length=7.6, y_length=4.4, ylabel=r"tomorrow's mean return, basis points",
                 xticks=[], yticks=[-10, 0, 10, 20], font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(9, 0), color=GREY_C, stroke_width=1.5)
        bars, errs, xl = VGroup(), VGroup(), VGroup()
        bw = ax.c2p(0.9, 0)[0] - ax.c2p(0, 0)[0]
        for i, k in enumerate(keys):
            for j, (side, col) in enumerate((("up", P_C), ("down", LOSS))):
                xc = 3 * i + 1.0 + 1.0 * j
                v = eras[k][side]
                top, bot = ax.c2p(xc, v), ax.c2p(xc, 0)
                r = Rectangle(width=bw, height=abs(top[1] - bot[1]) + 1e-3, stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to((top + bot) / 2)
                bars.add(r)
                lo, hi = eras[k][f"{side}_ci"]
                errs.add(VGroup(Line(ax.c2p(xc, lo), ax.c2p(xc, hi), color=WHITE, stroke_width=2),
                                Line(ax.c2p(xc - 0.2, lo), ax.c2p(xc + 0.2, lo), color=WHITE, stroke_width=2),
                                Line(ax.c2p(xc - 0.2, hi), ax.c2p(xc + 0.2, hi), color=WHITE, stroke_width=2)))
            xl.add(label(names[i], font_size=18, color=GREY_B).next_to(ax.c2p(3 * i + 1.5, -15), DOWN, buff=0.12))
        leg = legend([(P_C, r"after an up day: $\mathbb{E}[r_{t+1} \mid r_t > 0]$"),
                      (LOSS, r"after a down day: $\mathbb{E}[r_{t+1} \mid r_t < 0]$")], font_size=19)
        e0, e1, e2 = (eras[k] for k in keys)
        clear = (e0["down_ci"][1] < 0) and (e2["down_ci"][0] > 0)
        verdict = ("the old continuation and the new reversal both stand clear of zero after down days."
                   if clear else "after down days the bands still reach zero, so the reversal is suggestive, not "
                   "certain.")
        side = VGroup(
            leg,
            label(r"$\mathcal{G}$ = the sign of yesterday: two blocks", font_size=20, color=INFO),
            MathTex(rf"\rho_1:\ {e0['rho1']:.3f},\ {e1['rho1']:.3f},\ {e2['rho1']:.3f}", font_size=28),
            label(r"bars: 95\% of 200 block-bootstrap resamples", font_size=18, color=GREY_B),
            wrapped_label(r"since 2000 the projection has turned around: after a down day the best forecast is up", 4.6,
                          20, MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's daily US market, July 1926 -- December 2020")
        with self.voiceover(
            "Now the market. Let the information be one bit: was yesterday up or down? The conditional expectation "
            "of today's return is then two numbers, the average after up days and the average after down days. "
            f"<bookmark mark='a'/> From 1926 to 1974: {e0['up']:.1f} basis points after an up day, {e0['down']:.1f} "
            "after a down day. Yesterday's sign was today's sign, on average. From 1975 to 1999, the same pattern, "
            f"{e1['up']:.1f} against {e1['down']:.1f}. <bookmark mark='b'/> Since 2000 it has turned around: {e2['up']:.1f} "
            f"after an up day and {e2['down']:.1f} after a down day. The white bars are how far each number moves "
            f"when we resample the years in blocks: {verdict} This is the hook's gambler, as a projection."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(zero), FadeIn(side[1]), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_y() > ax.c2p(0, 0)[1] else UP) for b in bars[:4]],
                                  lag_ratio=0.3), FadeIn(leg), FadeIn(side[2]))
            self.play(FadeIn(errs[:4]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_y() > ax.c2p(0, 0)[1] else UP) for b in bars[4:]],
                                  lag_ratio=0.3), FadeIn(errs[4:]))
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, c):
        card = lab_card(r"conditional expectation on a partition", [
            "def cond_exp(x, labels, p=None):",
            "    \"\"\"E[X | G], G generated by the partition labels.\"\"\"",
            "    x = np.asarray(x, float)",
            "    p = np.ones_like(x) if p is None else np.asarray(p, float)",
            "    out = np.empty_like(x)",
            "    for b in np.unique(labels):",
            "        m = labels == b",
            "        out[m] = (p[m] * x[m]).sum() / p[m].sum()",
            "    return out",
        ], source="explainer/quant/house/martingale.py", width=7.4).to_corner(UL, buff=0.4)
        e2 = c["eras"]["20000101"]
        pred = desk_question(r"2000--2020: after a down day, is the best forecast of today's return up, down, or zero?",
                             rf"Up: {e2['down']:+.1f} bp, the average of the days that followed a down day.",
                             width=5.4, font_size=22).to_corner(DR, buff=0.35)
        with self.voiceover(
            "In the House this is five lines: average X over each block, weighted by probability, and give every "
            "world its block's average. <bookmark mark='a'/> On the three worlds it returns the foot of the "
            "perpendicular; on the market since 2000, with the sign of yesterday as the partition, it returns the two "
            "numbers we just drew. Regression in Part six is this same function with a richer partition. "
            "<bookmark mark='b'/> So, since 2000, after a down day, is the best forecast of today's return up, down or "
            f"zero? {'Up' if e2['down'] > 0 else 'Down'}, by {abs(e2['down']):.1f} basis points."
            " A forecast that the past cannot improve is exactly what defines a fair game. Next: martingales."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["cond_exp([3, 0, 1], [0, 0, 1], p=[.5, .3, .2])",
                                 f"[{c['toy'][0]:.3f} {c['toy'][1]:.3f} {c['toy'][2]:.3f}]",
                                 "cond_exp(r_2000s[1:], np.sign(r_2000s[:-1])) * 1e4",
                                 f"after up: {e2['up']:+.1f} bp   after down: {e2['down']:+.1f} bp"])
            vo.wait_until("b")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
