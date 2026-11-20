from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


def mat_tex(M, nd=3):
    rows = [" & ".join(f"{v:.{nd}f}".replace("-0.000", "0.000") for v in r) for r in M]
    return r"\begin{pmatrix}" + r" \\ ".join(rows) + r"\end{pmatrix}"


class Linear(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Solving the model: \ the saddle path", r"How do you solve a whole economy at once?",
             "Chapter eight. Solving the model: the saddle path.", lit={1980: r"Blanchard and Kahn",
                                                                        2000: r"Klein"},
             scale=("nation",), horizon=("a quarter", "a decade"))
        self.conditions()
        self.linearize()
        self.roots()
        self.saddle()

    def conditions(self):
        eqs = VGroup(
            MathTex(r"\frac{1}{c_t} = \beta\, \mathbb{E}_t\Big[\frac{1}{c_{t+1}}\Big(\alpha \frac{y_{t+1}}{k_{t+1}} "
                    r"+ 1 - \delta\Big)\Big]", font_size=34),
            MathTex(r"A\, c_t = (1 - \alpha)\, \frac{y_t}{n_t}", font_size=34),
            MathTex(r"k_{t+1} = (1 - \delta)\, k_t + y_t - c_t, \qquad y_t = z_t\, k_t^{\alpha} n_t^{1-\alpha}",
                    font_size=34),
            MathTex(r"\log z_{t+1} = \rho \log z_t + \varepsilon_{t+1}", font_size=34),
        ).arrange(DOWN, buff=0.4).move_to(LEFT * 1.6 + UP * 0.2)
        notes = VGroup(
            label(r"save: \ a unit saved \\ must pay its way", font_size=19, color=VALUE),
            label(r"work: \ the wage buys \\ what an hour costs", font_size=19, color=HOURS),
            label(r"build: \ what is not \\ eaten becomes capital", font_size=19, color=INVEST),
            label(r"luck: \ technology \\ wanders", font_size=19, color=TECH),
        )
        for e, n_ in zip(eqs, notes):
            n_.next_to(e, RIGHT, buff=0.5).set_x(5.2)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Value function iteration works, but with capital, technology and hours it gets slow, and real models "
            "have many more variables. The standard alternative starts from the conditions an equilibrium must "
            "satisfy. <bookmark mark='a'/> First, saving: giving up a unit of consumption today must pay, in "
            "expectation, as much as it costs, through capital's return. <bookmark mark='b'/> Second, work: the "
            "wage an extra hour earns must buy exactly what the hour costs in leisure. <bookmark mark='c'/> Third, "
            "building: whatever is not eaten becomes next quarter's capital. <bookmark mark='d'/> Fourth, luck: "
            "technology wanders at random, drifting back towards normal. Four equations, holding for every quarter, "
            "with an expectation of the future inside."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, e, n_ in zip("abcd", eqs, notes):
                vo.wait_until(mk)
                self.play(Write(e), FadeIn(n_), run_time=1.2)
        self.clear_scene()

    def linearize(self):
        R = load("rbc")
        A, B = (np.array(x) for x in R["AB"])
        idea = MathTex(r"\hat x_t = \log x_t - \log \bar x \qquad f(x_{t+1}, x_t) \approx "
                       r"f_1\, \hat x_{t+1} + f_2\, \hat x_t", font_size=32).to_edge(UP, buff=0.5)
        system = MathTex(mat_tex(A), r"\mathbb{E}_t", r"\begin{pmatrix} \hat k_{t+1} \\ \hat z_{t+1} \\ \hat c_{t+1}"
                         r"\end{pmatrix}", r"=", mat_tex(B), r"\begin{pmatrix} \hat k_t \\ \hat z_t \\ \hat c_t"
                         r"\end{pmatrix}", font_size=32).move_to(UP * 0.2)
        notes = VGroup(
            label(r"hats: \ percentage gaps from the steady state", font_size=21, color=GREY_A),
            label(r"close to the steady state, \ the economy is linear: \ one matrix equation", font_size=21,
                  color=E.ACCENT),
            label(r"hours and output drop out: \ given capital, \ technology and consumption, \ the labour "
                  r"condition fixes them", font_size=20, color=HOURS),
            label(r"capital and technology are given each quarter; \ consumption is free to jump", font_size=21,
                  color=INVEST),
        ).arrange(DOWN, buff=0.3).next_to(system, DOWN, buff=0.55)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Next, make the system linear. <bookmark mark='a'/> Measure every variable as its percentage gap from "
            "the steady state, the hats, and replace each equation by its first-order Taylor expansion. "
            "<bookmark mark='b'/> Near the steady state, the whole economy becomes one matrix equation. Here it is "
            "for the Island, with the numbers the computer found by differentiating the four conditions. "
            "<bookmark mark='c'/> Hours and output have been eliminated: given capital, technology and consumption, "
            "the labour condition pins them down. <bookmark mark='d'/> Notice the difference between the "
            "variables. Capital and technology are given at the start of each quarter: they are predetermined. "
            "Consumption is chosen, and can jump to anything. The solution must say how."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(idea), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(system), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.clear_scene()

    def roots(self):
        R = load("rbc")
        mods = R["eig"]
        ax = plane([-1.3, 1.3], [-1.3, 1.3], center=LEFT * 3.0 + DOWN * 0.2, x_length=5.0, y_length=5.0,
                   xticks=[-1, 0, 1], yticks=[-1, 0, 1], xlabel=r"real part", ylabel=r"imaginary part",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        o = ax.ax.c2p(0, 0)
        circ = Circle(radius=ax.ax.c2p(1, 0)[0] - o[0], stroke_color=GREY_B, stroke_width=2).move_to(o)
        xa = seg(ax, -1.3, 0, 1.3, 0, GREY_D, 1)
        ya = seg(ax, 0, -1.3, 0, 1.3, GREY_D, 1)
        dots = VGroup(*[dot(ax, m, 0, VALUE if m < 1 else TECH, 0.09) for m in sorted(mods)])
        names = VGroup(*[label(f"{m:.3f}", font_size=16, color=VALUE if m < 1 else TECH) for m in sorted(mods)])
        for k_, (d, n_) in enumerate(zip(dots, names)):
            n_.next_to(d, UP if k_ != 1 else DOWN, buff=0.15)
        side = VGroup(
            label(r"the system's three roots", font_size=21, color=E.ACCENT),
            label(rf"two inside the unit circle: \ {sorted(mods)[0]:.3f} and {sorted(mods)[1]:.3f} \\ (stable: "
                  r"gaps that die out)", font_size=19, color=VALUE),
            label(rf"one outside: \ {sorted(mods)[2]:.3f} \\ (unstable: \ a gap that grows 7\% a quarter)",
                  font_size=19, color=TECH),
            label(r"Blanchard and Kahn, \ 1980: \ a unique stable solution \\ when the unstable roots number "
                  r"the jump variables", font_size=19, color=E.ACCENT),
            label(r"one unstable root, \ one jump variable \ (consumption): \\ exactly one path", font_size=20,
                  color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Blanchard and Kahn, \ \emph{Econometrica} 48(5) (1980); \ Klein, \ \emph{JEDC} 24(10) "
                            r"(2000)", corner=DR, font_size=12)
        with self.voiceover(
            "How does the matrix decide? Through its roots, the generalized eigenvalues of the two matrices, which "
            "say how fast each combination of gaps grows or shrinks. <bookmark mark='a'/> The Island's system has "
            "three. <bookmark mark='b'/> Two lie inside the unit circle: combinations that shrink each quarter, "
            "towards the steady state. <bookmark mark='c'/> One lies outside, at about one point oh seven: a "
            "combination that grows seven percent a quarter, for ever, if it is ever set off. "
            "<bookmark mark='d'/> Olivier Blanchard and Charles Kahn proved in 1980 that such a system has exactly "
            "one stable solution when the number of unstable roots equals the number of variables free to jump. "
            "<bookmark mark='e'/> Here there is one of each: one unstable root, and consumption. Consumption must "
            "jump to the one value that keeps the explosive combination at exactly zero. Counting roots tells you "
            "whether a model has an answer, and how many."
        ) as vo:
            self.play(FadeIn(ax), Create(circ), FadeIn(xa), FadeIn(ya), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(dots[0]), GrowFromCenter(dots[1]), FadeIn(names[:2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(dots[2]), FadeIn(names[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def saddle(self):
        R = load("rbc")
        F, P = np.array(R["F"]), np.array(R["P"])
        ax = plane([-0.45, 0.45], [-0.2, 0.06], center=LEFT * 2.4 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[-0.2, -0.1, 0], xlabel=r"capital, \ $\hat k$ \ (\% gap)",
                   ylabel=r"consumption, \ $\hat c$ \ (\% gap)", xfmt=lambda v: f"{100 * v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}", font_size=15)
        ss = dot(ax, 0, 0, WHITE, 0.08)
        paths_ = []
        for p in R["phase"]:
            good = abs(p["offset"]) < 1e-12
            col = OUTPUT if good else (TECH if p["offset"] > 0 else INVEST)
            m = path(ax, p["k"], p["c"], col, 4 if good else 2.5, smooth=False, xr=(-0.45, 0.45), yr=(-0.2, 0.06))
            paths_.append((p, m, good))
        starts = VGroup(*[dot(ax, p["k"][0], p["c"][0], WHITE, 0.05) for p, _, _ in paths_])
        side = VGroup(
            label(r"capital starts 20\% below normal; \\ five choices of consumption", font_size=19,
                  color=GREY_A),
            label(r"too little: \ capital piles up \\ beyond any use", font_size=19, color=INVEST),
            label(r"too much: \ capital runs out", font_size=19, color=TECH),
            label(r"just right: \ the saddle path, \\ into the steady state", font_size=19, color=OUTPUT),
            MathTex(rf"\hat c_t = {F[0, 0]:.2f}\, \hat k_t + {F[0, 1]:.2f}\, \hat z_t", font_size=28,
                    color=POLICY),
            MathTex(rf"\hat k_{{t+1}} = {P[0, 0]:.3f}\, \hat k_t + {P[0, 1]:.3f}\, \hat z_t", font_size=28,
                    color=INVEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"the Island; \ solved by the QZ decomposition \ (Klein 2000)", corner=DR, font_size=12)
        with self.voiceover(
            "Here is what the unstable root means. <bookmark mark='a'/> Start the Island with capital twenty "
            "percent below normal, and try five different choices of consumption. <bookmark mark='b'/> Eat too "
            "little, and capital piles up past any sensible level, with consumption eventually collapsing. "
            "<bookmark mark='c'/> Eat too much, and capital runs out. <bookmark mark='d'/> Only one choice leads "
            "into the steady state: the saddle path. A rational household, looking ahead, chooses it. "
            f"<bookmark mark='e'/> The computer finds it exactly. Consumption's gap is {F[0, 0]:.2f} times "
            f"capital's gap plus {F[0, 1]:.2f} times technology's. <bookmark mark='f'/> And capital's gap shrinks "
            f"by a factor of {P[0, 0]:.3f} a quarter, the stable root from before. Paul Klein's method of 2000 does "
            "this for any number of variables, using a matrix factorization called QZ, and it is inside every "
            "modern model-solving package."
        ) as vo:
            self.play(FadeIn(ax), GrowFromCenter(ss), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(starts), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(m) for p, m, g in paths_ if p["offset"] < 0], FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(*[Create(m) for p, m, g in paths_ if p["offset"] > 0], FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(*[Create(m) for p, m, g in paths_ if g], FadeIn(side[3]), run_time=2)
            vo.wait_until("e")
            self.play(Write(side[4]))
            vo.wait_until("f")
            self.play(Write(side[5]))
        self.clear_scene()
