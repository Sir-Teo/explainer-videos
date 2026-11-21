from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Perturbation(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Perturbation, \ and when certainty equivalence misleads",
             r"How far from the steady state can a Taylor series be trusted?",
             "Chapter seven. Perturbation, and when certainty equivalence misleads.",
             lit={1980: r"Blanchard and Kahn", 2004: r"Schmitt-Grohé and Uribe"}, scale=("nation", "household"),
             horizon=("a century",))
        self.taylor()
        self.away()
        self.certainty()

    def taylor(self):
        P = load("perturb")
        eq = MathTex(r"k' \;\approx\; k^* + g_1\,(k - k^*) + \tfrac12\, g_2\,(k - k^*)^2", font_size=44,
                     color=PERT).move_to(UP * 1.8)
        rows = VGroup(
            label(r"$g_1$: \ differentiate the Euler equation once at the steady state; \ a quadratic, \ take the "
                  r"stable root", font_size=21, color=WHITE),
            label(rf"$g_1 = {P['g1']:.3f}$: \ the gap to the steady state closes by {100 * (1 - P['g1']):.1f}\% a "
                  r"year", font_size=22, color=PERT),
            label(r"$g_2$: \ differentiate twice; \ now the equation is linear", font_size=21, color=WHITE),
            label(rf"$g_2 = {P['g2']:.4f}$".replace("-", "{-}"), font_size=22, color=PERT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eq, DOWN, buff=0.6)
        foot = label(r"what central banks' models mostly use: \ fast, \ and exact at the steady state", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The third family of methods works from a single point. <bookmark mark='a'/> Write next year's "
            "capital as a Taylor series around the steady state. <bookmark mark='b'/> The first coefficient comes "
            "from differentiating the Euler equation once at the steady state, which gives a quadratic; the stable "
            f"root is {P['g1']:.3f}, <bookmark mark='c'/> so the gap to the steady state closes by about "
            f"{100 * (1 - P['g1']):.1f} percent a year, the speed of convergence of Part twenty. <bookmark "
            "mark='d'/> The second coefficient comes from differentiating twice, and the equation for it is linear. "
            "<bookmark mark='e'/> This is perturbation, the workhorse of central banks' models: fast, and exact at "
            "the point it starts from."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def away(self):
        P = load("perturb")
        k = np.array(P["k"])
        acc = np.array(P["accurate"])
        d1 = 100 * (np.array(P["first"]) - acc)
        d2 = 100 * (np.array(P["second"]) - acc)
        lim = float(np.ceil(max(np.abs(d1).max(), np.abs(d2).max())))
        ax = plane([0.3, 1.7], [-lim, lim], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8, y_length=4.4,
                   xticks=[0.3, 0.6, 1.0, 1.4, 1.7], yticks=[-lim, 0, lim],
                   xlabel=r"capital now, \ share of steady state",
                   ylabel=r"error in next year's capital, \ \% of steady state", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        zero = DashedLine(ax.ax.c2p(0.3, 0), ax.ax.c2p(1.7, 0), color=WHITE, stroke_width=1.6)
        c1 = path(ax, k, d1, ERR, 2.6)
        c2 = path(ax, k, d2, PERT, 2.6)
        side = VGroup(
            label(r"white: \ the accurate rule \\ (collocation, \ degree 10)", font_size=17, color=WHITE),
            label(r"red: \ first order", font_size=18, color=ERR),
            label(r"orange: \ second order", font_size=18, color=PERT),
            label(rf"worst Euler error \\ on 0.6--1.4: \\ $10^{{{P['ee_first']['max']:.1f}}}$ and "
                  rf"$10^{{{P['ee_second']['max']:.1f}}}$", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "How far can the series be trusted? Measure each approximation's mistake in next year's capital, "
            "against the accurate rule, across a wide range. <bookmark mark='a'/> At the steady state both are "
            "exact. <bookmark mark='b'/> The first-order rule, a straight line, drifts away as capital moves far "
            "from the steady state; <bookmark mark='c'/> the second-order rule bends with the truth and stays "
            "closer for longer. <bookmark mark='d'/> Within the range an economy usually visits, both are good; "
            "measured by Euler errors, first order is right to about one part in two hundred, second order to "
            "about one in eight hundred. Far from home, after a war or in a deep crisis, a local method can "
            "mislead."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(zero, color=PERT))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def certainty(self):
        P = load("perturb")["precaution"]
        a = np.array(P["a"])
        ax = plane([0, 10], [0, 2.2], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel=r"assets \ (mean income = 1)",
                   ylabel=r"consumption, \ middle income", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        safe = path(ax, a, P["safe"], GREY_B, 2.6)
        risky = path(ax, a, P["risky"], EGM, 2.8)
        gap = DoubleArrow(ax.ax.c2p(2, float(np.interp(2, a, P["risky"]))),
                          ax.ax.c2p(2, float(np.interp(2, a, P["safe"]))), color=WHITE, buff=0, stroke_width=2.4,
                          tip_length=0.15)
        side = VGroup(
            label(r"grey: \ income known \\ for certain", font_size=18, color=GREY_B),
            label(r"green: \ the same \\ average income, \\ but uncertain", font_size=18, color=EGM),
            label(rf"at assets of 2: \\ {P['gap_at_2']:.2f} less consumed, \\ a fifth of a year's \\ income saved "
                  r"for safety", font_size=18, color=WHITE),
            label(r"first-order perturbation \\ cannot see this gap: \\ certainty equivalence", font_size=18,
                  color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now the deeper trap. A first-order approximation of a model with uncertainty has a property called "
            "certainty equivalence: the rule depends on the average of future shocks, never on their size. "
            "<bookmark mark='a'/> Solve the household twice. Once with its income known for certain, at the same "
            "average; <bookmark mark='b'/> once with the income uncertain, as it is. <bookmark mark='c'/> The "
            f"uncertain household consumes less at every level of wealth: at assets of two, {P['gap_at_2']:.2f} "
            "less, about a fifth of a year's income, saved against bad years. This is precautionary saving, the "
            "buffer stock of Part twenty-two. <bookmark mark='d'/> A first-order perturbation cannot see the gap "
            "at all; a second-order one sees part of it, as a constant shift. When risk itself drives behaviour, "
            "as with saving, asset prices or default, a method must see the risk."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(safe), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(risky), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowFromCenter(gap), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
