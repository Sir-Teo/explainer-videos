from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


def dome_y(x, k=0.55, top=1.2):
    """The dome's profile, h = top - k |x|^(3/2), in screen units."""
    return top - k * np.abs(x) ** 1.5


class Dome(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Norton's dome", r"Can Newton's laws leave the future open?", lit=(2003,),
                            part=PART)
        with self.voiceover("Chapter six. Norton's dome."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.shape()
        self.solutions()
        self.animate_balls()
        self.lipschitz()

    def shape(self):
        hc = history_card(2003, r"John D. Norton", r"`Causation as Folk Science'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        cx = np.array([0.0, -1.2, 0])
        dome = ParametricFunction(lambda u: cx + np.array([u, dome_y(u), 0]), t_range=[-2.4, 2.4],
                                  color=LAW, stroke_width=4)
        ground = Line(cx + np.array([-3.2, dome_y(2.4), 0]), cx + np.array([3.2, dome_y(2.4), 0]), color=GREY_C)
        ball = Dot(cx + np.array([0, dome_y(0) + 0.13, 0]), radius=0.13, color=GOAL)
        f1 = MathTex(r"h(r) = \frac{2}{3g}\, r^{3/2}", font_size=34, color=LAW).move_to([4.6, 1.8, 0])
        f2 = MathTex(r"\frac{d^2 r}{dt^2} = \sqrt{r}", font_size=40, color=OK).move_to([4.6, 0.6, 0])
        rows = stack([(r"$r$: \ distance from the top, \ along the surface", WHITE),
                      (r"the slope's pull grows like $\sqrt r$", WHITE),
                      (r"one solution: \ the ball sits at the top forever, \ $r(t) = 0$", OK)], font_size=20,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -1.0, 0])
        with self.voiceover(
            "In 2003 John Norton described a simple system on which Newton's laws do not fix the future. "
            "<bookmark mark='a'/>A frictionless dome, shaped so that its height falls off with the distance from "
            "the top raised to the power three halves. <bookmark mark='b'/>Put a ball exactly at the top, at rest. "
            "<bookmark mark='c'/>Measure r as the distance from the top along the surface. On this shape the pull "
            "of gravity along the surface grows like the square root of r, so Newton's second law, in suitable "
            "units, says that the acceleration of r equals the square root of r. <bookmark mark='d'/>One solution "
            "is obvious: r is always zero. The ball sits at the top forever."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(ground), Create(dome), Write(f1))
            vo.wait_until("b")
            self.play(FadeIn(ball, scale=0.5))
            vo.wait_until("c")
            self.play(Write(f2), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def solutions(self):
        d = load("dome")
        head = label(r"Infinitely many solutions", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"r(t) = \begin{cases} 0 & t \le T \\ \dfrac{(t-T)^4}{144} & t \ge T \end{cases}", font_size=34,
                    color=OK).move_to([3.9, 1.5, 0])
        chk = MathTex(r"\ddot r = \frac{12\,(t-T)^2}{144} = \frac{(t-T)^2}{12} = \sqrt{r}", font_size=30,
                      color=ABS).move_to([3.9, -0.1, 0])
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 9, 2], x_length=6.0, y_length=4.2,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-3.3, -0.4, 0])
        xl = label(r"time $t$", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"distance $r$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        cols = [GOAL, CHANCE, ENT, TIME]
        curves = VGroup(*[series_plot(ax, s["r"], c, xs=d["t"], width=3.5) for s, c in zip(d["solutions"], cols)])
        tags = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4),
                               label(rf"$T = {s['T']:.0f}$", font_size=18, color=c)).arrange(RIGHT, buff=0.12)
                        for s, c in zip(d["solutions"], cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tags.move_to(ax.c2p(1.3, 7.0))
        err = max(s["max_error"] for s in d["solutions"])
        fd = d["finite_difference_check"]
        man, ex = f"{err:.1e}".split("e")
        side = stack([(rf"checked at all {len(d['t'])} time steps: \ largest error ${man} \times 10^{{{int(ex)}}}$",
                       OK),
                      (rf"a finite-difference check at $t = {fd[1]['t']}$: \ $\ddot r = {fd[1]['rdd']:.4f}$, \ "
                       rf"$\sqrt r = {fd[1]['sqrt_r']:.4f}$", ABS),
                      (r"any $T$ works, \ and $T = \infty$: \ the ball may stay forever", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=5.4).move_to([3.9, -1.9, 0])
        with self.voiceover(
            "But there are others. <bookmark mark='a'/>For any time T, let the ball sit still until T, and after T "
            "let r grow as t minus T, to the fourth power, over a hundred and forty-four. <bookmark mark='b'/>Check "
            "it: the second derivative is twelve times t minus T squared, over a hundred and forty-four, which is t "
            "minus T squared over twelve; and the square root of r is exactly the same. Newton's law holds at "
            "every moment, including the moment T itself, where position, velocity and acceleration are all zero. "
            "<bookmark mark='c'/>The Reasoner checks the solutions numerically, for T equal to zero, one, two and "
            "three, and by finite differences. <bookmark mark='d'/>Every T gives a solution, and so does never. "
            "The ball may begin to slide at any moment, in any direction, or not at all, and Newton's laws do not "
            "say which."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Write(chk))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tags), FadeIn(side[0]),
                      FadeIn(side[1]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def animate_balls(self):
        d = load("dome")
        head = label(r"Four histories from one present", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cols = [GOAL, CHANCE, ENT, TIME]
        dirs = [1, -1, 1, -1]
        Ts = [s["T"] for s in d["solutions"]]
        centres = [np.array([-5.25 + 3.5 * i, 0.2, 0]) for i in range(4)]
        k, top, half = 0.42, 0.7, 1.45
        domes = VGroup(*[ParametricFunction(lambda u, c=c: c + np.array([u, dome_y(u, k, top), 0]),
                                            t_range=[-half, half], color=LAW, stroke_width=3) for c in centres])
        t = ValueTracker(0.0)

        def pos(c, T, sgn):
            tt = t.get_value()
            r = (tt - T) ** 4 / 144 if tt > T else 0.0
            x = sgn * min(r, half)
            return c + np.array([x, dome_y(x, k, top) + 0.12, 0])

        balls = VGroup(*[always_redraw(lambda c=c, T=T, s=s, col=col: Dot(pos(c, T, s), radius=0.12, color=col))
                         for c, T, s, col in zip(centres, Ts, dirs, cols)])
        tags = VGroup(*[label(rf"history {i + 1}: \ starts at $T = {T:.0f}$", font_size=19, color=col).next_to(
            dm, DOWN, buff=0.3) for i, (dm, T, col) in enumerate(zip(domes, Ts, cols))])
        clock = always_redraw(lambda: label(rf"$t = {t.get_value():.1f}$", font_size=26, color=TIME).move_to(
            [0, 1.9, 0]))
        d_pairs = d["pairs"]
        side = stack([(r"all four agree at every time up to $T = 0$: \ the same position, \ velocity and force",
                       WHITE),
                      (r"after it, \ they part: \ Earman's test fails", BAD),
                      (r"Newtonian mechanics, \ even here, \ is not deterministic", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.25).to_edge(DOWN, buff=0.4)
        assert not d["deterministic"] and all(p["differ_after"] for p in d_pairs)
        with self.voiceover(
            "Watch four of these histories side by side. <bookmark mark='a'/>Four copies of the same ball, at the "
            "top of the same dome. In the first history it starts to slide at time zero, in the second at time "
            "one, then two, then three, each in its own direction. <bookmark mark='b'/>Until the first departure, "
            "every history is identical: same position, same velocity, same forces. <bookmark mark='c'/>Afterwards "
            "they part. <bookmark mark='d'/>By Earman's definition, the theory that allows these four histories is "
            "not deterministic. Nothing in the state of the ball at the top, and nothing in Newton's laws, fixes when "
            "or whether it will move."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[Create(x) for x in domes], lag_ratio=0.15), FadeIn(balls),
                      FadeIn(clock))
            vo.wait_until("a")
            self.play(FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(t.animate.set_value(8.0), run_time=7, rate_func=linear)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        for b in balls:
            b.clear_updaters()
        clock.clear_updaters()
        self.clear_scene()

    def lipschitz(self):
        head = label(r"How can a law fail to fix the future?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.05, 0.25], x_length=4.6, y_length=3.4,
                  axis_config={"color": GREY_B, "font_size": 16}).move_to([-4.0, -0.6, 0])
        g = ax.plot(lambda r: np.sqrt(max(r, 0)), x_range=[0, 1], color=OK, stroke_width=3.5)
        gl = MathTex(r"f(r) = \sqrt r", font_size=26, color=OK).next_to(ax.c2p(0.7, 0.85), UP, buff=0.1)
        tang = Line(ax.c2p(0, 0), ax.c2p(0.03, 1.0), color=BAD, stroke_width=3)
        tl = label(r"infinitely steep at $r = 0$", font_size=18, color=BAD).next_to(ax.c2p(0.05, 1.0), RIGHT,
                                                                                 buff=0.15)
        rows = [
            (r"Picard--Lindelöf", r"if the force is Lipschitz, \ $|f(a) - f(b)| \le K |a - b|$, \ the solution is "
                                  r"unique", ABS),
            (r"the dome", r"$\sqrt r$ is not Lipschitz at the top: \ uniqueness is not guaranteed, \ and fails", BAD),
            (r"run it backwards", r"a ball pushed up with just the right speed reaches the top in finite time and "
                                  r"stops: \ reversed, \ that is the spontaneous slide", TIME),
            (r"the replies", r"Malament, \ Korolev: \ an idealization, \ not physics; \ Norton: \ but it is Newton's "
                             r"theory", CHANCE),
        ]
        g2 = rows_table(rows, x_label=-1.2, x_text=1.4, top=1.6, gap=0.42, width=5.5, label_size=20, text_size=19)
        with self.voiceover(
            "How can a law fail to fix the future? <bookmark mark='a'/>The theory of differential equations has a "
            "uniqueness theorem, Picard and Lindelöf's: if the force changes no faster than in proportion to the "
            "change in position, a Lipschitz condition, then from any starting state there is exactly one solution. "
            "<bookmark mark='b'/>The square root of r fails the condition at the top of the dome: its graph is "
            "infinitely steep at zero. So uniqueness is not guaranteed there, and it fails. "
            "<bookmark mark='c'/>Norton offers a better way to see it. Push a ball up the dome with exactly the right "
            "speed and it will reach the top in a finite time and stop there, which is unremarkable. Run that film "
            "backwards and you have a ball at rest that, at some moment, begins to slide. "
            "<bookmark mark='d'/>David Malament and Alexandre Korolev replied that the dome is an idealization no "
            "real surface obeys, and that a well-posed Newtonian theory should exclude it. Norton's answer: perhaps, "
            "but then determinism is something we add to Newton's physics, not something we find in it."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(g), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(g2[0]))
            vo.wait_until("b")
            self.play(Create(tang), FadeIn(tl), FadeIn(g2[1]))
            vo.wait_until("c")
            self.play(FadeIn(g2[2]))
            vo.wait_until("d")
            self.play(FadeIn(g2[3]))
        self.clear_scene()
