from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Iteration(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Value and policy iteration, \ timed", r"Can the same answer be reached in fewer rounds?",
             "Chapter two. Value and policy iteration, timed.", lit={1960: r"Howard"}, scale=("nation",),
             horizon=("a century",))
        self.settles()
        self.howard()
        self.why()

    def settles(self):
        G = load("growth")
        d = np.array(G["dist"])
        n = len(d)
        ax = plane([0, n], [-7, 1], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.6,
                   xticks=[0, 100, 200, 300], yticks=[-6, -4, -2, 0], xlabel=r"round of value iteration",
                   ylabel=r"change in the values, \ $\log_{10}$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        curve = path(ax, np.arange(1, n + 1), np.log10(d), VFI, 3.0, smooth=False)
        ps = G["policy_settled"]
        mark = vline(ax, ps, -7, 1, POLICY)
        ml = label(rf"round {ps}: \\ the policy \\ stops changing", font_size=16, color=POLICY).next_to(
            ax.ax.c2p(ps, 0.2), RIGHT, buff=0.15)
        side = VGroup(
            label(rf"{G['vfi_iters']} rounds, \\ {1000 * G['vfi_seconds']:.0f} milliseconds", font_size=20,
                  color=VFI),
            label(r"the values crawl in \\ at the rate $\beta$; \\ the decisions \\ settle much sooner", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Value iteration has a weakness the last chapter exposed: it crawls. <bookmark mark='a'/> Each round "
            "the values improve by only the factor beta, so with a patient household they creep towards the answer, "
            f"{G['vfi_iters']} rounds here. <bookmark mark='b'/> But look at the decisions instead of the values. "
            f"After round {ps}, the best choice of next year's capital at every grid point never changes again. "
            "<bookmark mark='c'/> More than three quarters of the work only polishes numbers whose decisions are "
            "already right. That suggests a better plan."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def howard(self):
        G = load("growth")
        ch = G["howard_changes"]
        n = len(ch)
        ax = plane([0, n + 1], [0, 320], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.6,
                   xticks=[1, 5, 10, 15], yticks=[0, 100, 200, 300], xlabel=r"round of policy iteration",
                   ylabel=r"grid points whose choice changed", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for i, c in enumerate(ch):
            p0, p1 = ax.ax.c2p(i + 1 - 0.35, 0), ax.ax.c2p(i + 1 + 0.35, max(c, 0.5))
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=HOWARD,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
        steps = VGroup(
            label(r"1. \ evaluate: \ the value of \\ following this policy \\ forever, \ exactly", font_size=18,
                  color=WHITE),
            label(r"2. \ improve: \ one \\ Bellman step", font_size=18, color=WHITE),
            label(r"3. \ stop when no \\ choice changes", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        res = VGroup(
            label(rf"{G['howard_iters']} rounds, \ {1000 * G['howard_seconds']:.0f} ms", font_size=22,
                  color=HOWARD),
            label(rf"against {G['vfi_iters']} rounds, \ {1000 * G['vfi_seconds']:.0f} ms", font_size=20, color=VFI),
            label(r"the same policy, \ to the last grid point" if G["same_policy"] else r"a different policy",
                  font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        tag = published_tag(r"Howard, \ \emph{Dynamic Programming and Markov Processes} (1960)", corner=DL,
                            font_size=11)
        with self.voiceover(
            "Ronald Howard's policy iteration, from 1960, works on the decisions. <bookmark mark='a'/> Take a "
            "policy, and work out the value of following it forever, not one round at a time but exactly, in one "
            "step. <bookmark mark='b'/> Then improve the policy with a single Bellman step, <bookmark mark='c'/> "
            "and stop when no choice changes. <bookmark mark='d'/> The bars count the grid points whose choice "
            "changed in each round: all three hundred at first, then fewer and fewer, then none. <bookmark "
            f"mark='e'/> {G['howard_iters']} rounds instead of {G['vfi_iters']}, and the same policy at every grid "
            f"point. Even with each round doing more work, it is about {G['vfi_seconds'] / G['howard_seconds']:.0f} "
            "times as fast here, and the gain grows "
            "with patience, because value iteration slows as beta approaches one and policy iteration barely "
            "notices."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(res, shift=DOWN * 0.1))
        self.clear_scene()

    def why(self):
        eq = MathTex(r"V_\sigma \;=\; u_\sigma + \beta\, P_\sigma V_\sigma \quad\Longrightarrow\quad "
                     r"V_\sigma = (I - \beta P_\sigma)^{-1}\, u_\sigma", font_size=40, color=THEORY).move_to(UP * 2.0)
        n = 8
        cells = VGroup()
        pick = [1, 2, 3, 4, 4, 5, 6, 6]
        for i in range(n):
            for j in range(n):
                on = (i == j) or (j == pick[i])
                sq = Square(side_length=0.36, stroke_width=0.8, stroke_color=GREY_D,
                            fill_color=HOWARD if (j == pick[i] and i != j) else (WHITE if i == j else BLACK),
                            fill_opacity=0.85 if on else 0.0)
                sq.move_to([j * 0.38, -i * 0.38, 0])
                cells.add(sq)
        cells.move_to(LEFT * 3.0 + DOWN * 0.9)
        cap = label(r"$I - \beta P_\sigma$: \ two entries a row", font_size=18, color=GREY_A).next_to(cells, DOWN,
                                                                                                    buff=0.25)
        side = VGroup(
            label(r"$P_\sigma$: \ where the policy sends \\ each capital stock", font_size=20, color=HOWARD),
            label(r"a sparse linear system: \\ solved in one step, \\ it replaces hundreds \\ of rounds of value "
                  r"iteration", font_size=20, color=WHITE),
            label(r"Howard's method is \\ Newton's method \\ on the Bellman equation", font_size=20, color=POLICY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 2.8 + DOWN * 0.8)
        with self.voiceover(
            "Why is it so much faster? <bookmark mark='a'/> Fix a policy sigma. Its value satisfies a linear "
            "equation: this year's utility under the policy, plus beta times the value wherever the policy sends "
            "you. <bookmark mark='b'/> The matrix P sigma records where that is, so each row has a single one in "
            "it, and the system has just two entries a row. <bookmark mark='c'/> A computer solves such a sparse "
            "system in one step, and that one step does the work of hundreds of rounds of value iteration. "
            "<bookmark mark='d'/> In fact policy iteration is Newton's method applied to the Bellman equation, "
            "which is why it converges in a handful of rounds where value iteration needs hundreds."
        ) as vo:
            self.play(Write(eq), run_time=1.8)
            vo.wait_until("a")
            self.play(Indicate(eq, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cells), FadeIn(cap), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()
