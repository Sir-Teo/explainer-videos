from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

SMOL_COL = "#C9A0FF"

PROBLEMS = [
    r"The contraction: \ with $\beta = 0.96$ and a first change of 10, \ how many rounds of value iteration bring "
    r"the change below $10^{-6}$? \ With $\beta = 0.99$?",
    r"Blackwell: \ show that the growth model's Bellman operator satisfies discounting, \ $T(V + a) = TV + \beta a$, "
    r"\ and monotonicity.",
    r"Policy evaluation: \ a policy sends state 1 to state 2 and keeps state 2 where it is; \ utilities are 1 and 2, "
    r"\ $\beta = 0.9$. \ Solve $V = u + \beta P V$.",
    r"The endogenous grid by hand: \ $u = \log c$, \ $\beta R = 1$, \ $R = 1.05$, \ $y = 1$, \ and tomorrow's rule "
    r"$c(a') = 0.05\,a' + 1$. \ For $a' = 2$, \ find today's $c$ and the assets $a$ that choose it.",
    r"Collocation: \ fit $c_0 + c_1 x$ to $e^x$ at the Chebyshev nodes $\pm 1/\sqrt{2}$. \ Find the coefficients and "
    r"the error at $x = 0$.",
    r"Perturbation: \ for Brock and Mirman's economy, \ $k' = \alpha\beta k^{\alpha}$. \ Show that $g_1 = \alpha$, "
    r"\ and find the speed of convergence for $\alpha = 0.36$.",
    r"Euler errors: \ a rule's error is $10^{-3}$ for a household that consumes 50,000 a year. \ What is the mistake "
    r"in money, \ and is it worth a better method?".replace("50,000", "50{,}000"),
    r"$\bigstar$ \ Smolyak: \ show that the level-2 sparse grid in $d$ dimensions has $1 + 4d + 2d(d - 1)$ points.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"By turning it into a fixed point and iterating towards it, \ or into equations that hold "
                          r"at chosen points, \ or into a series around a steady state; \ fast when the method fits "
                          r"the problem. \ And you know it is right only by measuring: \ Euler errors, \ known "
                          r"answers, \ seeds, \ and a report with every result.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1971, 2021], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["log10"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, VALUE, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: how is an economy that has no formula solved, and how do you know the answer is right? <bookmark "
            "mark='a'/> By turning it into a fixed point and iterating towards it, which Blackwell's conditions "
            "guarantee will work; or into equations that must hold at well-chosen points; or into a series around "
            "the steady state. Each is fast when it fits the problem: grids and endogenous grids where there are "
            "kinks, polynomials where the rule is smooth, perturbation near home. And you know the answer is right "
            "only by measuring it: Euler-equation errors, known answers, fixed seeds, and a report with every "
            "result."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=16.0, rate_func=linear)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        G, Gr, It, Hh, P, Pt, C, Z, D = (load(x) for x in (
            "growth", "grids", "interp", "household", "projection", "perturb", "hjb", "zlb", "dimension"))
        items = [
            (rf"the Bellman operator: \ a contraction with modulus $\beta$; \ {G['vfi_iters']} rounds to $10^{{-6}}$",
             VALUE),
            (rf"policy iteration: \ {G['howard_iters']} rounds, \ the same answer; \ the policy settles first", HOWARD),
            (rf"grids: \ 30 points put the steady state {100 * (1 - Gr['rows'][0]['steady']):.0f}\% too low; \ "
             r"measure, \ do not guess", ERR),
            (rf"interpolation: \ a spline or Chebyshev, \ errors near $10^{{{It['cubic']['ee']['max']:.0f}}}$; \ "
             r"Runge's warning", POLICY),
            (rf"endogenous grids: \ no root finding; \ {Hh['vfi'][-1]['seconds'] / Hh['egm_seconds']:.0f} times "
             r"faster, \ and more accurate", EGM),
            (rf"projection: \ about four times more accurate per degree; \ $10^{{{P['rows'][-1]['ee']:.0f}}}$ at "
             r"degree 10", PROJ),
            (rf"perturbation: \ exact at home; \ blind to risk at first order \ ({Pt['precaution']['gap_at_2']:.2f} "
             r"of precaution)", PERT),
            (r"accuracy: \ Euler errors, \ unit-free, \ needing no true answer", ERR),
            (r"expectations: \ Rouwenhorst for persistence; \ seven quadrature nodes beat $10^5$ draws", GRID),
            (rf"continuous time: \ {C['iters']} sparse steps; \ {100 * C['at_limit']:.1f}\% at the limit", HJB),
            (rf"the zero bound: \ guess and verify; \ the recession twice as deep \ ({say_num(Z['x'][0], 1)}\%)"
             .replace("minus ", "{-}"), ERR),
            (rf"dimensions: \ Smolyak's {D['counts']['smolyak2'][-1]} points against $10^{{14}}$; \ reports and "
             r"known answers", SMOL_COL),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 51, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part fifty-one in twelve lines. <bookmark mark='r1'/> The Bellman operator is a contraction, so "
            "iterating it converges, at the rate beta. <bookmark mark='r2'/> Policy iteration gets the same answer "
            "in a handful of rounds. <bookmark mark='r3'/> Coarse grids bias the answer; measure the error, do not "
            "guess it. <bookmark mark='r4'/> Interpolate between grid points, and put the points where the function "
            "bends. <bookmark mark='r5'/> The endogenous grid method needs no root finding. <bookmark mark='r6'/> "
            "Projection makes a policy a handful of numbers, more accurate with every degree. <bookmark mark='r7'/> "
            "Perturbation is exact at home, and at first order blind to risk. <bookmark mark='r8'/> Euler errors "
            "measure accuracy without knowing the answer. <bookmark mark='r9'/> Discretize persistent shocks with "
            "Rouwenhorst, and integrate with quadrature. <bookmark mark='r10'/> In continuous time the household "
            "is a sparse linear system. <bookmark mark='r11'/> Constraints that bind sometimes need methods that "
            "find the regime. <bookmark mark='r12'/> And many dimensions need sparse grids, or networks, and every "
            "answer needs its report."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. How many rounds a contraction needs; Blackwell's conditions; evaluating a policy by one "
            "linear solve; the endogenous grid by hand; a collocation at two nodes; perturbation of Brock and "
            "Mirman's economy; what an Euler error means in money; and a starred problem counting the points of a "
            "Smolyak grid. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Kenneth Judd, \emph{Numerical Methods in Economics} (1998)",
             r"Nancy Stokey and Robert Lucas, with Edward Prescott, \emph{Recursive Methods in Economic Dynamics} "
             r"(1989), \ chapters 3, 4 and 9",
             r"Thomas Sargent and John Stachurski, \emph{Dynamic Programming} and the QuantEcon lectures",
             r"Jesús Fernández-Villaverde, Juan Rubio-Ramírez and Frank Schorfheide, \ `Solution and estimation "
             r"methods for DSGE models', \emph{Handbook of Macroeconomics} (2016)"],
            [r"Bellman (1957); \ Howard (1960); \ Blackwell (1965); \ Smolyak (1963); \ Tauchen (1986)",
             r"Judd (1992); \ Den Haan and Marcet (1994); \ Rouwenhorst (1995); \ Krueger and Kubler (2004)",
             r"Schmitt-Grohé and Uribe (2004); \ Carroll (2006); \ Aruoba, Fernández-Villaverde and Rubio-Ramírez "
             r"(2006)",
             r"Kopecky and Suen (2010); \ Guerrieri and Iacoviello (2015); \ Maliar, Maliar and Winant (2021)",
             r"Achdou, Han, Lasry, Lions and Moll (2022); \ Azinovic, Gaegauf and Scheidegger (2022)"])
        with self.voiceover(
            "The reading: Kenneth Judd's Numerical Methods in Economics; Stokey and Lucas, with Prescott, for the "
            "theory of recursive methods; Sargent and Stachurski's lectures, with code; and the handbook chapter by "
            "Fernández-Villaverde, Rubio-Ramírez and Schorfheide. Then the papers, from Bellman to the neural "
            "networks."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1998, r"Per Krusell and Anthony Smith", r"solve an economy with a whole distribution of "
                          r"households, \ and find that its average behaves almost as if there were one",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 52 \ $\cdot$ \ Act X, \ The Graduate Core", font_size=30, color=GREY_B),
                     label(r"Many Agents", font_size=46),
                     label(r"what does macroeconomics get wrong by treating a country as one household?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from one household \ to a distribution", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"the household", EGM), (r"the distribution", HJB),
                                        (r"the interest rate", POLICY), (r"monetary policy", ERR))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the methods of this part go to work on a whole population. <bookmark mark='a'/> In 1998 Per "
            "Krusell and Anthony Smith solved an economy with a distribution of households, and found, to general "
            "relief, that its average behaves almost as if there were one household. <bookmark mark='b'/> Part "
            "fifty-two asks what macroeconomics gets wrong by treating a country as one household: the "
            "household, the distribution, the interest rate that clears the market, <bookmark mark='c'/> and why "
            "later models with realistic inequality changed the account of how monetary policy works."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)

