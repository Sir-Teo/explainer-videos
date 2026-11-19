from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


class Aversion(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Risk aversion", r"How much is a gamble worth for sure, and what decides it?",
             "Chapter five. Risk aversion.", lit={1964: r"Pratt's measure"})
        self.concave()
        self.ladder()
        self.arrow_pratt()
        self.cara_crra()

    def concave(self):
        a = load("aversion")
        xs, u2 = np.array(a["xs"]), np.array(a["u2"])
        lo, hi = a["sea"]
        # utility rescaled for display: u(x) = -1/x, mapped to [0, 1] over the plotted range
        umin, umax = u2.min(), u2.max()

        def U(x):
            return (rk.crra(x, 2.0) - umin) / (umax - umin)

        ax = plane([30, 200], [0, 1.05], center=LEFT * 2.6 + DOWN * 0.2, x_length=7.4, y_length=5.4,
                   xticks=[60, 90, 100, 120, 180], yticks=[], xlabel=r"Ana's money at the end of the day, \ \$",
                   ylabel=r"utility", font_size=17)
        A = ax.ax
        curve = path(ax, xs, U(xs), color=UTIL, width=3.5)
        p_lo, p_hi = A.c2p(lo, U(lo)), A.c2p(hi, U(hi))
        chord = DashedLine(p_lo, p_hi, color=RISKY, stroke_width=2.5)
        mid = A.c2p(a["ev_sea"], (U(lo) + U(hi)) / 2)
        m_dot = Dot(mid, radius=0.08, color=RISKY)
        ce = a["rows"][2]["ce"]
        ce_dot = Dot(A.c2p(ce, U(ce)), radius=0.08, color=WHITE)
        flat = DashedLine(A.c2p(ce, U(ce)), mid, color=GREY_B, stroke_width=2)
        reef = Dot(A.c2p(a["reef"], U(a["reef"])), radius=0.08, color=SAFE)
        drops = VGroup(*[DashedLine(A.c2p(x, 0), A.c2p(x, U(x)), color=GREY_D, stroke_width=1.5)
                         for x in (lo, hi, ce, a["reef"], a["ev_sea"])])
        side = VGroup(
            label(r"Ana's utility: \ $u(x) = -1/x$ \ ($\gamma = 2$)", font_size=25, color=UTIL),
            label(r"the open sea: \ \$60 or \$180; \ on average \$120", font_size=24, color=RISKY),
            label(r"its expected utility: \ the chord's midpoint", font_size=24, color=RISKY),
            label(rf"its certainty equivalent: \ \${ce:.0f}", font_size=26),
            label(rf"its risk premium: \ \$120 $-$ \${ce:.0f} = \${120 - ce:.0f}", font_size=26, color=E.ACCENT),
            label(r"the reef's \$100 for sure beats it: \ Ana stays in", font_size=24, color=SAFE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Bernoulli's insight, in a picture. <bookmark mark='a'/> Here is a utility function that bends: each "
            "extra dollar adds less than the one before. Ana's is minus one over x, the power function with gamma "
            "equal to two. <bookmark mark='b'/> The open sea leaves her with sixty dollars or a hundred and eighty, "
            "a hundred and twenty on average. <bookmark mark='c'/> Its expected utility is the midpoint of the chord "
            "between the two outcomes, and because the curve bends, the chord lies below it. "
            "<bookmark mark='d'/> Slide across to the curve: the sure amount with the same utility is ninety dollars. "
            "That's the certainty equivalent of the gamble. <bookmark mark='e'/> The gap between the average, a "
            "hundred and twenty, and the certainty equivalent, ninety, is the risk premium: thirty dollars Ana would "
            "give up to have the average for sure. <bookmark mark='f'/> The reef gives her a hundred for sure, more "
            "than ninety. She fishes the reef, though the sea pays more on average."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(drops[0]), FadeIn(drops[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(chord), FadeIn(m_dot), FadeIn(drops[4]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(flat), FadeIn(ce_dot), FadeIn(drops[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(reef), FadeIn(drops[3]), FadeIn(side[5]))
        self.clear_scene()

    def ladder(self):
        a = load("aversion")
        rows = a["rows"]
        names = {0.0: r"risk neutral", 1.0: r"Bernoulli's logarithm", 2.0: r"Ana", 4.0: r"more cautious"}
        head = VGroup(label(r"$\gamma$", font_size=28, color=GREY_B), label(r"who", font_size=26, color=GREY_B),
                      label(r"the sea is worth, for sure", font_size=26, color=GREY_B),
                      label(r"risk premium", font_size=26, color=GREY_B), label(r"fishes", font_size=26, color=GREY_B))
        table = [head]
        for r in rows:
            c = RISKY if r["takes"] == "sea" else SAFE
            table.append(VGroup(MathTex(f"{r['gamma']:g}", font_size=32), label(names[r["gamma"]], font_size=25),
                                label(rf"\${r['ce']:.2f}", font_size=28, color=c),
                                label(rf"\${r['premium']:.2f}", font_size=28),
                                label(r"the open sea" if r["takes"] == "sea" else r"the reef", font_size=27,
                                      color=c)))
        xs = [-5.4, -3.4, 0.3, 3.0, 5.2]
        grid = VGroup()
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.2 - 0.8 * i, 0])
            grid.add(row)
        rule = Line([-6.4, 1.8, 0], [6.4, 1.8, 0], color=GREY_C, stroke_width=1.5)
        foot = VGroup(
            MathTex(r"u(x) = \frac{x^{1-\gamma}}{1-\gamma}", font_size=34, color=UTIL),
            label(rf"Ana switches to the reef once $\gamma$ passes {a['g_star']:.2f}", font_size=27, color=E.ACCENT),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How much a gamble is worth depends on how fast the utility function bends, its curvature gamma. "
            "<bookmark mark='a'/> A risk-neutral fisher values the sea at its average, a hundred and twenty. With "
            "Bernoulli's logarithm, gamma equal to one, it's worth a hundred and three ninety-two for sure: still "
            "more than the reef. Ana, at gamma two, values it at ninety, and someone more cautious, at gamma four, "
            "at seventy-four sixty-eight. <bookmark mark='b'/> Somewhere between one and two the choice flips: "
            "Ana's neighbours with a gamma below one point two six fish the open sea, and the rest the reef. The same "
            "two options, the same chances, different people, different choices: risk preference is a taste, like "
            "the taste for fish."
        ) as vo:
            self.play(FadeIn(head), Create(rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in grid[1:]], lag_ratio=0.6), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def arrow_pratt(self):
        a = load("aversion")
        hs, ex, ap = np.array(a["hs"]), np.array(a["exact"]), np.array(a["approx"])
        ax = plane([0, 80], [0, 32], center=RIGHT * 2.9 + DOWN * 0.6, x_length=5.8, y_length=4.6,
                   xticks=[0, 20, 40, 60, 80], yticks=[0, 10, 20, 30],
                   xlabel=r"a 50--50 bet of $\pm h$ around \$120, \ $u = \log x$", ylabel=r"risk premium, \ \$",
                   font_size=16)
        e_c = path(ax, hs, ex, color=WHITE, width=3)
        a_c = DashedVMobject(path(ax, hs, ap, color=E.ACCENT, width=3), num_dashes=30)
        el = label(r"exact", font_size=19).next_to(ax.ax.c2p(80, ex[-1]), LEFT, buff=0.1).shift(UP * 0.3)
        al = label(r"$\tfrac12 A\,h^2$", font_size=21, color=E.ACCENT).next_to(ax.ax.c2p(76, ap[-3]), DOWN, buff=0.3)
        left = VGroup(
            label(r"Arrow (1965) and Pratt (1964):", font_size=27),
            MathTex(r"A(x) = -\frac{u''(x)}{u'(x)}", font_size=40, color=UTIL),
            label(r"absolute risk aversion: \ dollars", font_size=22, color=GREY_A),
            MathTex(r"R(x) = x\,A(x)", font_size=40, color=UTIL),
            label(r"relative risk aversion: \ $\gamma$ for the power function", font_size=22, color=GREY_A),
            MathTex(r"\text{risk premium} \;\approx\; \tfrac12\, A(x)\,\sigma^2", font_size=38, color=E.ACCENT),
            label(r"for small risks: \ aversion times variance", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "In the 1960s Kenneth Arrow and John Pratt, separately, turned curvature into a measure. "
            "<bookmark mark='a'/> Absolute risk aversion is minus the second derivative of utility over the first: "
            "how fast marginal utility falls, per dollar. <bookmark mark='b'/> Relative risk aversion multiplies by "
            "wealth, so it's measured per percent instead of per dollar. For the power function it's just gamma, "
            "the same at every level of wealth. <bookmark mark='c'/> Their result: for a small risk, the premium a "
            "person would pay to avoid it is about half their absolute risk aversion times the variance of the "
            "risk. <bookmark mark='d'/> On the right, the premium Bernoulli's logarithm puts on even bets of plus or "
            "minus h dollars around a hundred and twenty. For small bets the formula is almost exact; for a bet of "
            "eighty dollars either way it is a little low, but still a decent guide. Risk aversion matters to the "
            "second order: for tiny risks, the premium vanishes faster than the risk."
        ) as vo:
            self.play(FadeIn(left[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[1]), FadeIn(left[2]))
            vo.wait_until("b")
            self.play(FadeIn(left[3]), FadeIn(left[4]))
            vo.wait_until("c")
            self.play(FadeIn(left[5]), FadeIn(left[6]))
            vo.wait_until("d")
            self.play(FadeIn(ax), Create(e_c), Create(a_c), FadeIn(el), FadeIn(al))
        self.clear_scene()

    def cara_crra(self):
        a = load("aversion")
        ws, ca, cr = np.array(a["ws"]), np.array(a["cara"]), np.array(a["crra"])
        ax = plane([40, 400], [0, 11], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=[40, 120, 200, 300, 400], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"wealth, \ \$",
                   ylabel=r"premium for a 50--50 $\pm$\$20 bet, \ \$", font_size=17)
        c1 = path(ax, ws, ca, color=FAN, width=3.5)
        c2 = path(ax, ws, cr, color=UTIL, width=3.5)
        l1 = label(r"CARA: \ $-e^{-ax}$", font_size=21, color=FAN).next_to(ax.ax.c2p(400, ca[-1]), UP, buff=0.12).shift(
            LEFT * 0.9)
        l2 = label(r"CRRA: \ $x^{1-\gamma}/(1-\gamma)$", font_size=21, color=UTIL).next_to(ax.ax.c2p(400, cr[-1]), UP,
                                                                                           buff=0.12).shift(LEFT * 1.4)
        side = VGroup(
            label(r"both set to Ana's aversion at \$120", font_size=24, color=GREY_A),
            label(r"constant absolute aversion: \\ the same premium at any wealth", font_size=24, color=FAN),
            label(r"constant relative aversion: \\ the premium falls as wealth grows", font_size=24, color=UTIL),
            label(r"the evidence favours falling absolute aversion: \\ the rich take more dollar risks", font_size=23),
            label(r"CARA is convenient (normal risks: \\ mean minus a variance penalty); \\ CRRA is the "
                  r"workhorse of macro", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Two families of utility do almost all the work in economics. <bookmark mark='a'/> Set both to Ana's "
            "risk aversion at a hundred and twenty dollars, and ask what each would pay to avoid an even bet of "
            "twenty dollars as wealth grows. <bookmark mark='b'/> Constant absolute risk aversion, the exponential "
            "family, pays the same premium at any wealth: the bet looks the same to a pauper and to a millionaire. "
            "<bookmark mark='c'/> Constant relative risk aversion, the power family, pays less as wealth grows, "
            "because twenty dollars is a smaller share of a larger fortune. <bookmark mark='d'/> The evidence "
            "favours the second pattern: richer people take larger risks in dollars. <bookmark mark='e'/> The "
            "exponential family survives because it's convenient: with normally distributed risks, it turns a "
            "choice into the mean minus a penalty for variance. The power family is the workhorse of "
            "macroeconomics and finance, and its gamma is one of this part's two dials."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(l1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(l2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
