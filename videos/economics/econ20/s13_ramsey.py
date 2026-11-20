from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Ramsey(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Ramsey's problem: \ saving chosen", r"If the islanders choose how much to save, \ looking "
             r"ahead for ever, \ what do they choose?", "Chapter eleven. Ramsey's problem: saving chosen.",
             lit={1928: r"Ramsey", 1965: r"Cass; \ Koopmans"}, scale=("household", "nation"),
             horizon=("a century",))
        self.problem()
        self.euler()
        self.phase()
        self.shooting()
        self.result()

    def problem(self):
        rows = VGroup(
            MathTex(r"\max_{c(t)} \int_0^\infty e^{-\beta t}\, \frac{c^{1-\theta}}{1-\theta}\, dt, \quad "
                    r"\beta = \rho - n - (1-\theta)g", font_size=44),
            MathTex(r"\text{subject to}\quad \dot k = k^{\alpha} - c - (n+g+\delta)\,k", font_size=44),
        ).arrange(DOWN, buff=0.55).move_to(UP * 1.3)
        notes = VGroup(
            label(r"$\rho$: \ impatience \ $\cdot$ \ $\theta$: \ how much a smooth path matters \ $\cdot$ \ "
                  r"$c$ per effective worker", font_size=22, color=GREY_A),
            label(r"what is not eaten becomes capital", font_size=22, color=CAPITAL),
        )
        notes[0].next_to(rows[0], DOWN, buff=0.15)
        notes[1].next_to(rows[1], DOWN, buff=0.15)
        q = quote_card(r"it is assumed that we do not discount later enjoyments in comparison with earlier ones, a "
                       r"practice which is ethically indefensible and arises merely from the weakness of the "
                       r"imagination", r"Frank Ramsey, \ \emph{A Mathematical Theory of Saving}, \ Economic Journal "
                       r"(1928)", width=11.6, font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Solow took the saving rate as given. In 1928, nearly thirty years earlier, the young Cambridge "
            "mathematician Frank Ramsey had asked how much a nation ought to save. <bookmark mark='a'/> The islanders "
            "choose a path of consumption to maximize the discounted sum of their utility, for ever. Written per "
            "effective worker, the discount rate beta is impatience, rho, less the growth of the population and an "
            "allowance for technology. "
            "<bookmark mark='b'/> subject to the same accumulation as before: what is not eaten becomes capital. "
            "<bookmark mark='c'/> Ramsey himself refused to discount the future. To do so, he wrote, is a practice "
            "which is ethically indefensible and arises merely from the weakness of the imagination. David Cass and "
            "Tjalling Koopmans, in 1965, put the discount rate back, and the model now carries all three names."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()

    def euler(self):
        rows = VGroup(
            MathTex(r"H = \frac{c^{1-\theta}}{1-\theta} + \mu\,\big[k^{\alpha} - c - (n+g+\delta)k\big]",
                    font_size=42),
            MathTex(r"\frac{\partial H}{\partial c} = 0:\quad c^{-\theta} = \mu", font_size=40),
            MathTex(r"\dot\mu = \beta\mu - \frac{\partial H}{\partial k} = \mu\,\big[\beta + n + g + \delta - "
                    r"\alpha k^{\alpha-1}\big]", font_size=38),
            MathTex(r"\frac{\dot c}{c} = \frac{\alpha k^{\alpha-1} - \delta - \rho - \theta g}{\theta}",
                    font_size=54, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.4)
        notes = VGroup(
            label(r"$\mu$: \ what a unit of capital is worth, \ in utility", font_size=20, color=GREY_A),
            label(r"eat until a unit of consumption is worth what a unit of capital is", font_size=20,
                  color=GREY_A),
            label(r"with $\beta = \rho - n - (1-\theta) g$, \ $-\theta\,\dot c/c = \dot\mu/\mu$", font_size=18,
                  color=GREY_B),
            label(r"the Euler equation: \ consumption grows when capital earns more than impatience demands",
                  font_size=21, color=E.ACCENT),
        )
        notes[0].next_to(rows, DOWN, buff=0.35)
        notes[3].next_to(rows, DOWN, buff=0.35)
        with self.voiceover(
            "The tool is the Hamiltonian, the dynamic version of a Lagrangian. <bookmark mark='a'/> It adds to "
            "today's utility the value of today's addition to capital, with mu the shadow value of a unit of capital. "
            "<bookmark mark='b'/> Choosing consumption: eat until the marginal utility of consumption equals the "
            "value of capital. <bookmark mark='c'/> The shadow value then changes over time at the rate of "
            "the discount rate, less what capital earns. <bookmark mark='d'/> Differentiate the first condition, "
            "substitute beta, and out comes the Euler equation of part seven, now with production in it. "
            "Consumption per effective worker grows when the net return on capital exceeds the rate of impatience "
            "plus theta times technology's growth, and shrinks when it falls short."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(Write(r))
            self.play(FadeOut(notes[0]), FadeIn(notes[3]))
        self.clear_scene()

    def axes_(self, r):
        return plane([0, 2.2 * r["k_ss"]], [0, 2.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=5.2,
                     xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0, 1.5, 2.0],
                     xlabel=r"capital per effective worker $k$", ylabel=r"consumption $c$", font_size=16)

    def phase(self):
        r = load("ramsey")
        ax = self.axes_(r)
        kdot = path(ax, r["kdot0_k"], r["kdot0_c"], color=CAPITAL, width=4, yr=(0, 2.0))
        cdot = DashedLine(ax.ax.c2p(r["k_ss"], 0), ax.ax.c2p(r["k_ss"], 2.0), color=CONS, stroke_width=3)
        lk = label(r"$\dot k = 0$", font_size=20, color=CAPITAL).next_to(ax.ax.c2p(r["k_gold"], 1.42), UP, buff=0.1)
        lc = label(r"$\dot c = 0$: \ $\alpha k^{\alpha-1} = \delta + \rho + \theta g$", font_size=19,
                   color=CONS).next_to(ax.ax.c2p(r["k_ss"], 1.95), RIGHT, buff=0.1)
        star = Dot(ax.ax.c2p(r["k_ss"], r["c_ss"]), radius=0.1, color=WHITE)
        gold = VGroup(DashedLine(ax.ax.c2p(r["k_gold"], 0), ax.ax.c2p(r["k_gold"], 1.4), color=GREY_B,
                                 stroke_width=1.5),
                      label(r"golden rule", font_size=17, color=GREY_B).next_to(ax.ax.c2p(r["k_gold"], 0), UP,
                                                                                buff=0.1).shift(RIGHT * 0.6))
        arrows = VGroup()
        for (kk, cc, dk, dc) in ((0.25, 0.25, 1, 1), (0.25, 0.75, -1, 1), (0.75, 0.25, 1, -1), (0.75, 1.0, -1, -1)):
            x0 = kk * 2.2 * r["k_ss"] * 0.9
            y0 = cc * 1.6
            p0 = ax.ax.c2p(x0, y0)
            arrows.add(VGroup(Arrow(p0, p0 + RIGHT * 0.5 * dk, buff=0, color=GREY_A, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.3),
                              Arrow(p0, p0 + UP * 0.5 * dc, buff=0, color=GREY_A, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.3)))
        with self.voiceover(
            "Two equations, two variables: draw them in the plane of capital and consumption. "
            "<bookmark mark='a'/> Capital stands still along a hump: consumption equal to output less break-even "
            "investment. Its peak is the golden rule. Above the hump capital shrinks; below it, capital grows. "
            "<bookmark mark='b'/> Consumption stands still along a vertical line, where the marginal product of "
            "capital just covers depreciation, impatience and growth. To its left consumption rises; to its right "
            "it falls. <bookmark mark='c'/> Where they cross is the steady state. <bookmark mark='d'/> The arrows "
            "show the trouble. Almost every starting point runs away: towards no capital at all, or towards too "
            "much capital and nothing to eat."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(kdot), FadeIn(lk), FadeIn(gold))
            vo.wait_until("b")
            self.play(Create(cdot), FadeIn(lc))
            vo.wait_until("c")
            self.play(FadeIn(star))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a_) for g_ in arrows for a_ in g_], lag_ratio=0.15), run_time=2)
        self.clear_scene()

    def shooting(self):
        r = load("ramsey")
        ax = self.axes_(r)
        kdot = path(ax, r["kdot0_k"], r["kdot0_c"], color=CAPITAL, width=3, yr=(0, 2.0)).set_stroke(opacity=0.5)
        cdot = DashedLine(ax.ax.c2p(r["k_ss"], 0), ax.ax.c2p(r["k_ss"], 2.0), color=CONS,
                          stroke_width=2).set_opacity(0.6)
        star = Dot(ax.ax.c2p(r["k_ss"], r["c_ss"]), radius=0.09, color=WHITE)
        start = DashedLine(ax.ax.c2p(r["k0"], 0), ax.ax.c2p(r["k0"], 2.0), color=GREY_B, stroke_width=1.5)
        sl = label(r"$k_0 = \tfrac12 k^\ast$", font_size=18, color=GREY_B).next_to(ax.ax.c2p(r["k0"], 2.0), RIGHT,
                                                                                buff=0.1)
        hi = path(ax, r["high_k"], r["high_c"], color=LABOUR, width=3, xr=(0, 2.2 * r["k_ss"]), yr=(0, 2.0),
                  smooth=False)
        lo = path(ax, r["low_k"], r["low_c"], color=HUMAN, width=3, xr=(0, 2.2 * r["k_ss"]), yr=(0, 2.0),
                  smooth=False)
        good = path(ax, r["path_k"], r["path_c"], color=E.ACCENT, width=5, smooth=False)
        side = VGroup(
            label(r"guess $c_0$ and integrate:", font_size=20, color=GREY_A),
            label(r"6\% too high: \ capital runs out", font_size=19, color=LABOUR),
            label(r"6\% too low: \ too much capital", font_size=19, color=HUMAN),
            label(r"bisect between them, \ 80 times", font_size=19, color=GREY_A),
            label(rf"the saddle path: \ $c_0 = {r['c0']:.3f}$", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Only one path leads to the steady state, the saddle path, and the islanders must jump onto it. Agora "
            "finds it by shooting. <bookmark mark='a'/> Start with half the steady state's capital. Guess a level "
            "of consumption, and integrate the two equations forward. <bookmark mark='b'/> Guess six percent too "
            "high, and the islanders eat their capital: the path curls left and runs out. <bookmark mark='c'/> Six "
            "percent too low, and they overshoot, piling up capital they will never eat. <bookmark mark='d'/> The "
            "right guess lies between, so bisect: halve the interval, see which way the path misses, and repeat. "
            f"<bookmark mark='e'/> After eighty halvings, consumption starts at {r['c0']:.3f}, and the path rides "
            "into the steady state."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(kdot), FadeIn(cdot), FadeIn(star), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(start), FadeIn(sl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(hi), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lo), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(good), FadeIn(side[4]), run_time=3)
        self.clear_scene()

    def result(self):
        r = load("ramsey")
        rows = VGroup(
            label(r"the modified golden rule", font_size=30, color=E.ACCENT),
            MathTex(r"f'(k^\ast) - \delta = \rho + \theta g", font_size=48),
            label(rf"island: \ $\rho = {r['rho']}$, \ $\theta = {r['theta']:g}$, \ $g = 0.02$ \ $\Rightarrow$ \ "
                  rf"$r = {pc(r['r_ss'], 0)}$", font_size=24, color=RATE),
            label(rf"capital: \ $k^\ast = {r['k_ss']:.2f}$, \ against the golden rule's {r['k_gold']:.2f}",
                  font_size=24, color=CAPITAL),
            label(rf"saving: \ {pc(r['s_ramsey'], 0)}, \ against the golden rule's 33\%", font_size=24, color=SAVE),
            label(r"impatient people stop short of the golden rule, \ and never pass it: \ no dynamic inefficiency",
                  font_size=22, color=GREY_A),
            label(r"the same machinery runs the climate models of Part 48", font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        with self.voiceover(
            "What does the island choose? <bookmark mark='a'/> In the steady state the Euler equation says the "
            "interest rate, the net marginal product of capital, equals impatience plus theta times growth: the "
            "modified golden rule. <bookmark mark='b'/> With these parameters, the interest rate is "
            f"{100 * r['r_ss']:.0f} percent. <bookmark mark='c'/> Capital per effective worker settles at "
            f"{r['k_ss']:.2f}, well short of the golden rule's {r['k_gold']:.2f}. <bookmark mark='d'/> The islanders "
            f"save about {100 * r['s_ramsey']:.0f} percent, not a third. <bookmark mark='e'/> Because they are "
            "impatient, they stop short of the consumption-maximizing capital stock, and an optimizing economy can "
            "never overshoot it into dynamic inefficiency. <bookmark mark='f'/> The same machinery, with the climate "
            "added, is how economists put a price on carbon."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, m in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(m, shift=UP * 0.1))
        self.clear_scene()
