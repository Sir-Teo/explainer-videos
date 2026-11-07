from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def amp_bars(vals, x0, y0, w=0.13, gap=0.05, scale=2.6, mark=None):
    """Real amplitudes as bars on one baseline: blue for positive, red for negative (a half-turn phase), the marked
    item in yellow while positive."""
    g = VGroup()
    for i, v in enumerate(vals):
        col = NO if v < 0 else (HEAD if i == mark else DATA)
        h = max(abs(v) * scale, 0.004)
        r = Rectangle(width=w, height=h, stroke_width=0, fill_color=col, fill_opacity=0.92)
        r.move_to([x0 + i * (w + gap), y0, 0], aligned_edge=DOWN if v >= 0 else UP)
        g.add(r)
    return g


def plane_vec(o, R, ang, color, sw=4):
    return Arrow(o, o + R * np.array([math.cos(ang), math.sin(ang), 0]), buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.06)


class Grover(VoiceoverScene):
    def construct(self):
        self.card()
        self.rotation()
        self.mean()
        self.overshoot()
        self.counting()
        self.optimal()

    def card(self):
        card = chapter_card(10, r"Grover's search", r"How fast can a quantum computer find a needle?",
                            lit=(1996, 1997), extra=((1996, r"Grover: \ search in $\sqrt N$ queries"),
                                                     (1997, r"Bennett et al.: \ and no faster")), part=PART)
        with self.voiceover("Chapter ten. Grover's search. How fast can a quantum computer find a needle?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ two reflections make a rotation
    def rotation(self):
        g = load("grover")
        th, N, best = g["theta"], g["N"], g["best_iters"]
        head = label(r"Two reflections make a rotation", font_size=36).to_edge(UP, buff=0.3)
        o = np.array([-6.1, -2.7, 0])
        R = 4.6
        ax_u = Arrow(o, o + RIGHT * (R + 0.4), buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        ax_w = Arrow(o, o + UP * (R + 0.3), buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        lu = MathTex(r"|s'\rangle", font_size=26, color=GREY_A).next_to(ax_u, DOWN, buff=0.1).align_to(ax_u, RIGHT)
        lw = MathTex(r"|w\rangle", font_size=26, color=YES).next_to(ax_w.get_end(), RIGHT, buff=0.12)
        arc = Arc(radius=R, start_angle=0, angle=PI / 2 + 0.12, arc_center=o, color=GREY_D, stroke_width=1.5)
        mirror = DashedLine(o, o + (R + 0.3) * np.array([math.cos(th), math.sin(th), 0]), color=LAM,
                            dash_length=0.08)
        ml = MathTex(r"|s\rangle", font_size=26, color=LAM).next_to(mirror.get_end(), RIGHT, buff=0.1)
        vec = plane_vec(o, R, th, HEAD)
        ang_ = Arc(radius=1.3, start_angle=0, angle=th, arc_center=o, color=LAM, stroke_width=2.5)
        thl = MathTex(r"\theta", font_size=24, color=LAM).move_to(o + 1.6 * np.array([1, 0.07, 0]))
        cap = label(r"the plane of the marked state and the unmarked ones", font_size=18, color=GREY_B).move_to([-3.4, 2.65, 0])
        fs = 28
        rows = VGroup(
            MathTex(r"|s\rangle", r"=", r"\sin\theta", r"|w\rangle", r"+", r"\cos\theta", r"|s'\rangle",
                    font_size=fs),
            MathTex(r"O", r"=", r"I - 2|w\rangle\langle w|", font_size=fs),
            MathTex(r"D", r"=", r"2|s\rangle\langle s| - I", font_size=fs),
            MathTex(r"(DO)^k|s\rangle", r"=", r"\sin(2k{+}1)\theta", r"|w\rangle", r"+", r"\cos(2k{+}1)\theta",
                    r"|s'\rangle", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        rows.move_to([3.6, 0.5, 0]).align_to([0.5, 0, 0], LEFT)
        rows[1][0].set_color(NO)
        rows[2][0].set_color(LAM)
        rows[3][2].set_color(YES)
        whys = VGroup(label(rf"the even superposition; \ $\sin\theta = 1/\sqrt N$, \ here $N = {N}$", font_size=18,
                            color=GREY_B),
                      label(r"the oracle flips $|w\rangle$: \ a reflection in $|s'\rangle$", font_size=18, color=NO),
                      label(r"the diffusion: \ a reflection in $|s\rangle$", font_size=18, color=LAM),
                      label(r"two mirrors at angle $\theta$: \ a rotation by $2\theta$ per round", font_size=18,
                            color=YES))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.08).align_to(r, LEFT).shift(RIGHT * 0.1)
        trail = VGroup()
        with self.voiceover(
            "Grover's algorithm looks for one marked item w among N, using an oracle that flips the sign of w's "
            "amplitude. <bookmark mark='a'/> Everything happens in a plane: the marked state, and the even "
            "superposition of the unmarked ones. The starting state sits a small angle theta above the unmarked "
            "axis, with sine theta equal to one over root N. <bookmark mark='b'/> The oracle reflects the state in "
            "the unmarked axis. <bookmark mark='c'/> The diffusion step reflects it in the starting state. "
            "<bookmark mark='d'/> Two reflections make a rotation by twice the angle between the mirrors: two "
            "theta. After k rounds the angle is two k plus one, times theta. Here N is sixty-four, and six rounds "
            "carry the state just past vertical."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowArrow(ax_u), GrowArrow(ax_w), FadeIn(lu), FadeIn(lw), Create(arc), FadeIn(cap))
            self.play(Create(mirror), FadeIn(ml), GrowArrow(vec), Create(ang_), FadeIn(thl))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(Rotate(vec, angle=-2 * th, about_point=o), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            self.play(Rotate(vec, angle=4 * th, about_point=o), run_time=1.2)
            trail.add(plane_vec(o, R, 3 * th, HEAD, sw=2).set_opacity(0.35))
            self.add(trail[-1])
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0].copy(), rows[3]), FadeIn(whys[3]))
            phi = 3 * th
            for _ in range(best - 1):
                self.play(Rotate(vec, angle=-2 * phi, about_point=o), run_time=0.45)
                self.play(Rotate(vec, angle=2 * th + 2 * phi, about_point=o), run_time=0.45)
                phi += 2 * th
                trail.add(plane_vec(o, R, phi, HEAD, sw=2).set_opacity(0.35))
                self.add(trail[-1])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ inversion about the mean
    def mean(self):
        g = load("grover")
        snaps, w, N = g["snapshots"], g["marked"], g["N"]
        head = label(rf"The same thing in the {N} amplitudes", font_size=36).to_edge(UP, buff=0.3)
        x0, y0 = -5.65, -0.55
        bars = amp_bars(snaps[0], x0, y0, mark=w)
        base = Line([x0 - 0.15, y0, 0], [x0 + (N - 1) * 0.18 + 0.15, y0, 0], color=GREY_C, stroke_width=1.5)
        wl = label(rf"item {w}, \ the marked one", font_size=17, color=HEAD).move_to([bars[w].get_x(), y0 - 0.65, 0])

        def state(k):
            v = snaps[k]
            return VGroup(label(rf"round {k}", font_size=21, color=WHITE),
                          label(rf"$a_w = {v[w]:.3f}$, \ $P = {v[w] ** 2:.3f}$", font_size=21, color=HEAD)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 2.2, 0])
        cnt = state(0)
        flipped = list(snaps[0])
        flipped[w] = -flipped[w]
        m = sum(flipped) / N
        mline = DashedLine([x0 - 0.15, y0 + m * 2.6, 0], [x0 + (N - 1) * 0.18 + 0.15, y0 + m * 2.6, 0], color=LAM,
                           dash_length=0.07)
        mlab = label(r"the mean", font_size=17, color=LAM).next_to(mline, LEFT, buff=0.08)
        fs = 28
        rows = VGroup(
            MathTex(r"(D a)_x", r"=", r"2\,\langle x|s\rangle\langle s|a\rangle - a_x", font_size=fs),
            MathTex(r"(D a)_x", r"=", r"\frac{2}{N}\sum_y a_y - a_x", font_size=fs),
            MathTex(r"(D a)_x", r"=", r"2\bar a - a_x", font_size=fs),
        ).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=1.05)
        rows[2][2].set_color(LAM)
        whys = VGroup(label(r"$D = 2|s\rangle\langle s| - I$", font_size=18, color=GREY_B),
                      label(r"$\langle x|s\rangle = 1/\sqrt N$ for every $x$", font_size=18, color=GREY_B),
                      label(r"\textbf{inversion about the mean}", font_size=18, color=LAM))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.15)
        with self.voiceover(
            "The same rounds, seen as the sixty-four amplitudes. <bookmark mark='a'/> At the start they are all "
            "equal, one eighth each. <bookmark mark='b'/> The oracle flips the marked amplitude below the axis. "
            "<bookmark mark='c'/> On amplitudes the diffusion step means: replace each one by twice the mean minus "
            "itself, an inversion about the mean. The mean has dropped a little, so the unmarked amplitudes shrink "
            "slightly, while the marked one, far below the mean, jumps far above it. <bookmark mark='d'/> Repeat. "
            "After six rounds the marked amplitude is nought point nine nine eight. <bookmark mark='e'/> Keep going "
            "and it falls again, as the unmarked amplitudes turn negative: the rotation has overshot."
        ) as vo:
            self.play(FadeIn(head), Create(base))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(wl), FadeIn(cnt),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(Transform(bars, amp_bars(flipped, x0, y0, mark=w)), wl.animate.set_color(NO))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Create(mline), FadeIn(mlab))
            self.play(Transform(bars, amp_bars(snaps[1], x0, y0, mark=w)), Transform(cnt, state(1)), run_time=1.5)
            self.play(FadeOut(mline), FadeOut(mlab))
            vo.wait_until("d")
            for k in range(2, 7):
                self.play(Transform(bars, amp_bars(snaps[k], x0, y0, mark=w)), Transform(cnt, state(k)),
                          run_time=0.8)
            vo.wait_until("e")
            for k in range(7, len(snaps)):
                self.play(Transform(bars, amp_bars(snaps[k], x0, y0, mark=w)), Transform(cnt, state(k)),
                          run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ success against rounds; scaling
    def overshoot(self):
        g = load("grover")
        rows_ = load("gscale")["rows"]
        th, P, N = g["theta"], g["probs"], g["N"]
        head = label(r"Overshoot, \ and $\tfrac{\pi}{4}\sqrt N$ rounds", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 20, 2], y_range=[0, 1, 0.25], x_length=6.0, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True})
        ax.move_to([-3.4, 0.55, 0])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, 6, 12, 18)])
        yt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.5, 1)])
        xl = label(r"rounds $k$", font_size=18, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label(rf"P(marked item), \ $N = {N}$", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        curve = ax.plot(lambda k: math.sin((2 * k + 1) * th) ** 2, x_range=[0, 20, 0.05], color=LAM, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(k, p), radius=0.06, color=YES if k == g["best_iters"] else DATA)
                        for k, p in enumerate(P)])
        leg = VGroup(VGroup(Dot(radius=0.06, color=DATA), label(r"our simulator", font_size=16, color=DATA)).arrange(
            RIGHT, buff=0.1), VGroup(Line(ORIGIN, RIGHT * 0.3, color=LAM), label(r"$\sin^2(2k{+}1)\theta$",
                                                                                   font_size=16, color=LAM)).arrange(
            RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.c2p(20, 0.05), UL, buff=0.05)
        kb = g["best_iters"]
        bl = label(rf"$k = {kb}$: \ {P[kb]:.4f}", font_size=17, color=YES).next_to(dots[kb], RIGHT, buff=0.15)
        zl = label(rf"$k = 12$: \ {P[12]:.4f}", font_size=17, color=NO).next_to(dots[12], UP, buff=1.35)
        zp = Line(zl.get_bottom() + DOWN * 0.05, dots[12].get_center() + UP * 0.1, color=NO, stroke_width=1.5)
        fs = 28
        rows = VGroup(
            MathTex(r"(2k+1)\,\theta", r"\approx", r"\frac{\pi}{2}", font_size=fs),
            MathTex(r"k", r"\approx", r"\frac{\pi}{4\theta} - \frac12", font_size=fs),
            MathTex(r"k", r"\approx", r"\frac{\pi}{4}\sqrt N", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to([3.2, 1.7, 0]).align_to([0.9, 0, 0], LEFT)
        rows[2][2].set_color(YES)
        whys = VGroup(label(r"aim at $|w\rangle$", font_size=18, color=GREY_B),
                      label(rf"here {g['predicted_iters']:.2f}: \ round to {kb}", font_size=18, color=GREY_B),
                      label(r"$\theta \approx 1/\sqrt N$", font_size=18, color=GREY_B))
        for w_, r in zip(whys, rows):
            w_.next_to(r, RIGHT, buff=0.4)
        tab = grid_table([r"$N$", r"rounds", r"P(success)", r"classical, \ average"],
                         [[f"{r['N']:,}", f"{r['iterations']}", f"{r['p']:.4f}", f"{r['classical_expected']:,.1f}"]
                          for r in rows_], widths=[1.4, 1.1, 1.5, 1.9], row_h=0.34, font_size=17, mono_cols=())
        tab.next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        for r in range(1, len(rows_) + 1):
            tab.cells[r][1].set_color(YES)
            tab.cells[r][3].set_color(NO)
        with self.voiceover(
            "Our simulator's success probability against the number of rounds follows the formula exactly: sine "
            "squared of two k plus one, times theta. <bookmark mark='a'/> It peaks when the angle reaches a right "
            "angle, after about pi over four times root N rounds: for sixty-four items, six rounds, and success "
            "ninety-nine point seven per cent. <bookmark mark='b'/> Run longer and it falls: after twelve rounds it "
            "is almost zero, and then it climbs again. Unlike a classical search, more work can make the answer "
            "worse. <bookmark mark='c'/> As N grows, the rounds grow like root N, while a classical search in random "
            "order needs about N over two looks on average: for sixty-five thousand items, two hundred and one "
            "rounds against about thirty-two thousand looks."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), FadeIn(leg),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Indicate(dots[kb], color=YES, scale_factor=1.8), FadeIn(bl))
            vo.wait_until("b")
            self.play(Indicate(dots[12], color=NO, scale_factor=1.8), FadeIn(zl), Create(zp))
            vo.wait_until("c")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.3), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ counting, and amplitude amplification
    def counting(self):
        g = load("grover")
        th, N = g["theta"], g["N"]
        head = label(r"Counting solutions, \ amplifying anything", font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-4.4, 0.6, 0])
        R = 1.9
        circ = Circle(radius=R, color=GREY_C, stroke_width=1.8).move_to(c)
        axes_ = VGroup(DashedLine(c + LEFT * (R + 0.25), c + RIGHT * (R + 0.25), color=GREY_D, dash_length=0.07),
                       DashedLine(c + DOWN * (R + 0.25), c + UP * (R + 0.25), color=GREY_D, dash_length=0.07))
        one = Dot(c + RIGHT * R, radius=0.06, color=GREY_B)
        e_plus = Dot(c + R * np.array([math.cos(2 * th), math.sin(2 * th), 0]), radius=0.09, color=YES)
        e_minus = Dot(c + R * np.array([math.cos(2 * th), -math.sin(2 * th), 0]), radius=0.09, color=YES)
        lp = MathTex(r"e^{+2i\theta}", font_size=24, color=YES).next_to(e_plus, UR, buff=0.08)
        lm = MathTex(r"e^{-2i\theta}", font_size=24, color=YES).next_to(e_minus, DR, buff=0.08)
        arc = Arc(radius=0.9, start_angle=0, angle=2 * th, arc_center=c, color=YES, stroke_width=2.5)
        cl = wrapped_label(rf"the Grover step's eigenvalues on the unit circle: \ for $N = {N}$, $M = 1$, \ "
                           rf"$2\theta = {2 * th:.3f}$ rad, \ {th / PI:.4f} of a turn", 4.6, font_size=18,
                           color=GREY_A).next_to(circ, DOWN, buff=0.35)
        fs = 28
        rows = VGroup(
            MathTex(r"\sin^2\theta", r"=", r"\frac{M}{N}", font_size=fs),
            MathTex(r"G", r"=", r"\begin{pmatrix}\cos 2\theta & -\sin 2\theta\\ \sin 2\theta & \cos 2\theta"
                    r"\end{pmatrix}", font_size=fs),
            MathTex(r"\lambda", r"=", r"e^{\pm 2i\theta}", font_size=fs),
            MathTex(r"M", r"=", r"N\sin^2\theta", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        rows.move_to([2.0, 1.0, 0]).align_to([-1.2, 0, 0], LEFT)
        rows[3][2].set_color(YES)
        whys = VGroup(label(r"$M$ of the $N$ items marked: \ the same plane", font_size=18, color=GREY_B),
                      label(r"one round, \ in that plane", font_size=18, color=GREY_B),
                      label(r"a rotation's angle is in its eigenvalues", font_size=18, color=GREY_B),
                      wrapped_label(r"phase estimation \ (chapter 8) \ reads $\theta$: \ \textbf{quantum "
                                    r"counting} \ (Brassard, \ H{\o}yer and Tapp, \ 1998)", 4.4, font_size=18,
                                    color=YES))
        for w_, r in zip(whys, rows):
            w_.next_to(r, RIGHT, buff=0.4)
        if whys[3].get_right()[0] > 6.85:
            whys[3].shift(LEFT * (whys[3].get_right()[0] - 6.85))
        amp = wrapped_label(r"\textbf{amplitude amplification}: \ replace the Hadamards by any algorithm $A$ that "
                            r"succeeds with probability $p$, \ and $|s\rangle$ by $A|0\rangle$: \ about "
                            r"$1/\sqrt p$ rounds instead of $1/p$ repetitions \ (Brassard, \ H{\o}yer, \ Mosca and "
                            r"Tapp, \ 2002)", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Chapter eight promised another use for Grover's rotation. <bookmark mark='a'/> If M of the N items are "
            "marked, the same picture holds, with sine squared theta equal to M over N. Each round is a rotation by "
            "two theta in the plane. <bookmark mark='b'/> A rotation's eigenvalues are e to the plus and minus two "
            "i theta: its angle is written in its phases. <bookmark mark='c'/> So phase estimation applied to the "
            "Grover step reads theta, and N sine squared theta counts the solutions without finding them. This is "
            "quantum counting, from Brassard, Høyer and Tapp in 1998, and it also says how many rounds to run. "
            "<bookmark mark='d'/> Nothing requires the Hadamards. Replace them by any algorithm that succeeds with "
            "probability p, and about one over root p rounds replace one over p repetitions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(Create(circ), FadeIn(axes_), FadeIn(one))
            self.play(FadeIn(e_plus), FadeIn(e_minus), Create(arc), FadeIn(lp), FadeIn(lm), FadeIn(cl))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("d")
            self.play(FadeIn(amp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ BBBV: no faster
    def optimal(self):
        head = label(r"No algorithm does better: \ a sketch", font_size=36).to_edge(UP, buff=0.3)
        n_pts, c_req = 64, 1.0
        c = np.array([-4.5, -0.2, 0])
        unit = 1.9                              # screen length of distance 1
        centre = Dot(c, radius=0.09, color=WHITE)
        cl = MathTex(r"\psi_T", font_size=22, color=WHITE).next_to(centre, DOWN, buff=0.08)
        target = DashedVMobject(Circle(radius=c_req * unit, color=YES, stroke_width=2.5), num_dashes=60).move_to(c)
        tl = label(r"needed: \ distance $c$", font_size=17, color=YES).next_to(target, UP, buff=0.08)

        def ring(T):
            rad = min(2 * T / math.sqrt(n_pts), 1.25) * unit
            return VGroup(*[Dot(c + max(rad, 0.02) * np.array([math.cos(2 * PI * i / n_pts),
                                                               math.sin(2 * PI * i / n_pts), 0]),
                                radius=0.04, color=DATA) for i in range(n_pts)])
        pts = ring(0)
        tq = label(r"queries: \ 0", font_size=20, color=DATA).next_to(target, DOWN, buff=0.55)
        ill = note(rf"illustrative: \ $N = {n_pts}$, \ $c = 1$; \ each dot is the final state for one $w$, \ at the "
                   r"largest average distance allowed", font_size=16).to_edge(DOWN, buff=0.15).to_edge(LEFT, buff=0.4)
        fs = 27
        rows = VGroup(
            MathTex(r"\|\psi^w_{k+1} - \psi_{k+1}\|", r"\le", r"\|\psi^w_k - \psi_k\|", r"+", r"2|\alpha_{w,k}|",
                    font_size=fs),
            MathTex(r"\sum_w \|\psi^w_T - \psi_T\|", r"\le", r"2\sum_{k<T}\sum_w |\alpha_{w,k}|", r"\le",
                    r"2T\sqrt N", font_size=fs),
            MathTex(r"\sum_w \|\psi^w_T - \psi_T\|", r"\ge", r"cN", font_size=fs),
            MathTex(r"T", r"\ge", r"\tfrac{c}{2}\sqrt N", font_size=fs + 4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        rows.move_to([2.6, 0.7, 0]).align_to([-1.6, 0, 0], LEFT)
        rows[3].set_color(YES)
        whys = VGroup(
            label(r"$\psi^w$: \ the oracle marks $w$; \ $\psi$: \ it marks nothing; \ one query flips only "
                  r"$\alpha_w$", font_size=18, color=GREY_B),
            label(r"add over all $w$; \ $\sum_w |\alpha_w|^2 = 1$, \ so $\sum_w |\alpha_w| \le \sqrt N$",
                  font_size=18, color=GREY_B),
            label(r"to name $w$, \ every $\psi^w_T$ must be far from $\psi_T$", font_size=18, color=GREY_B),
            label(r"Bennett, \ Bernstein, \ Brassard and Vazirani, \ 1997", font_size=18, color=YES))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.08).align_to(r, LEFT).shift(RIGHT * 0.1)
        foot = wrapped_label(r"brute force over $n$-bit keys or assignments: \ $2^n$ becomes $2^{n/2}$, \ still "
                             r"exponential \ (chapter 11); \ doubling a symmetric key's length restores the margin",
                             7.6, font_size=18, color=HEAD).next_to(whys[3], DOWN, buff=0.3).align_to(rows, LEFT)
        with self.voiceover(
            "Could a cleverer algorithm beat root N? No. <bookmark mark='a'/> Compare each run with a run whose "
            "oracle marks nothing. One query can push the two apart by at most twice the amplitude the algorithm "
            "puts on w at that moment. <bookmark mark='b'/> Add over all N choices of w. Those amplitudes square to "
            "one in total, so they sum to at most root N, and T queries move all the runs apart by at most two T "
            "root N in total. <bookmark mark='c'/> But to name w, every one of the N runs must end a fixed distance "
            "from the run that marks nothing. <bookmark mark='d'/> So T is at least a constant times root N, as "
            "Bennett, Bernstein, Brassard and Vazirani proved in 1997. <bookmark mark='e'/> Brute-force search over "
            "n-bit keys drops only from two to the n to two to the n over two: still exponential."
        ) as vo:
            self.play(FadeIn(head), FadeIn(centre), FadeIn(cl), FadeIn(pts), FadeIn(tq), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            for T in range(1, 4):
                self.play(Transform(pts, ring(T)), Transform(tq, label(rf"queries: \ {T}", font_size=20,
                                                                         color=DATA).move_to(tq)), run_time=0.7)
            vo.wait_until("c")
            self.play(Create(target), FadeIn(tl))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            self.play(Transform(pts, ring(4)), Transform(tq, label(r"queries: \ 4 \ $= \tfrac{c}{2}\sqrt N$",
                                                                    font_size=20, color=YES).move_to(tq)))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
