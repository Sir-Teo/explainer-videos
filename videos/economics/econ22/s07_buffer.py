from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Buffer(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Precautionary saving and the buffer stock", r"What does income risk do to saving, \ and to "
             r"the share of a windfall that is spent?", "Chapter six. Precautionary saving and the buffer stock.",
             lit={1989: r"Zeldes", 1991: r"Deaton", 1997: r"Carroll", 2006: r"the endogenous grid"},
             scale=("household",), horizon=("a year", "a lifetime"))
        self.prudence()
        self.problem()
        self.egm()
        self.function()
        self.population()

    def prudence(self):
        ax = plane([0.3, 2.0], [0, 8], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.2, y_length=4.8,
                   xticks=[0.5, 1.0, 1.5, 2.0], yticks=[0, 2, 4, 6, 8], xlabel=r"consumption $c$",
                   ylabel=r"marginal utility $u'(c) = c^{-2}$", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                   font_size=16)
        cs = np.linspace(0.36, 2.0, 120)
        curve = path(ax, cs, cs ** -2.0, color=SPEND, width=4)
        lo, hi = 0.5, 1.5
        chord = seg(ax, lo, lo ** -2, hi, hi ** -2, color=RISK, width=3)
        mean_pt = dot(ax, 1.0, (lo ** -2 + hi ** -2) / 2, color=RISK, r=0.09)
        sure_pt = dot(ax, 1.0, 1.0, color=SPEND, r=0.09)
        lab1 = label(r"$\mathbb{E}\,u'(c)$ \ when $c$ is $0.5$ or $1.5$: \ " + f"{(lo ** -2 + hi ** -2) / 2:.2f}",
                     font_size=19, color=RISK).next_to(mean_pt, UR, buff=0.12)
        lab2 = label(r"$u'(1) = 1$", font_size=19, color=SPEND).next_to(sure_pt, DR, buff=0.12)
        side = VGroup(
            label(r"risk raises the expected value \\ of a dollar tomorrow \\ when $u'$ is convex", font_size=21,
                  color=GREY_A),
            label(r"$u''' > 0$: \ prudence \\ (Miles Kimball, \ 1990)", font_size=21, color=E.ACCENT),
            label(r"so a prudent household \\ saves more when its income \\ is uncertain: \ precautionary \\ "
                  r"saving", font_size=21, color=SAVE),
            label(r"Hall's quadratic utility has \\ $u''' = 0$, \ and no such motive", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Hall's households have no reason to fear risk in what they spend. To get his random walk exactly, he "
            "gave them quadratic utility, whose marginal utility is a straight line. Real marginal utility curves. "
            "<bookmark mark='a'/> Here it falls with consumption as one over c squared. <bookmark mark='b'/> If "
            "consumption tomorrow is a sure one, a dollar tomorrow is worth one. If it is half or one and a half "
            "with equal chances, the average marginal utility is "
            f"{(lo ** -2 + hi ** -2) / 2:.2f}: the bad state's high value outweighs the good state's low one. "
            "<bookmark mark='c'/> Risk raises the value of a dollar saved, so a household with a convex marginal "
            "utility saves more when its income is uncertain. Miles Kimball called that curvature prudence. "
            "<bookmark mark='d'/> Its saving is precautionary: a buffer against bad years."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), Create(curve), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(sure_pt), FadeIn(lab2))
            self.play(Create(chord), FadeIn(mean_pt), FadeIn(lab1))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def problem(self):
        b = load("buffer")
        P = b["params"]
        rows = VGroup(
            label(r"the buffer-stock household \ (Angus Deaton, \ 1991; \ Christopher Carroll, \ 1997)", font_size=25,
                  color=E.ACCENT),
            MathTex(r"y_t = P_t\,\theta_t, \qquad P_{t+1} = G\,P_t\,\psi_{t+1}", font_size=38, color=INCOME),
            label(rf"permanent shocks $\psi$ and transitory shocks $\theta$, \ each with a spread of "
                  rf"{100 * P['perm_sd']:.0f}\%; \ a {100 * P['p_zero']:.1f}\% chance a year of no income at all",
                  font_size=21, color=RISK),
            label(r"no borrowing; \ impatient: \ it would like to borrow against its rising income", font_size=21,
                  color=GREY_A),
            MathTex(r"m = \frac{\text{cash on hand}}{P}, \qquad c(m)^{-\gamma} = \beta R\; \mathbb{E}\big[(G\psi'\, "
                    r"c(m'))^{-\gamma}\big], \qquad m' = \frac{R\,(m - c)}{G\psi'} + \theta'", font_size=34),
            label(rf"$\beta = {P['beta']}$, \ $R = {P['R']}$, \ $\gamma = {P['gamma']:g}$, \ income growth "
                  rf"$G = {P['G']}$: \ a year a period", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Zeldes, QJE 104(2) (1989); \ Deaton, Econometrica 59(5) (1991); \ Carroll, QJE "
                            r"112(1) (1997)", corner=DR, font_size=12)
        with self.voiceover(
            "Stephen Zeldes showed in 1989 that prudence bends the consumption function. Angus Deaton and "
            "Christopher Carroll built the household that bears its name. <bookmark mark='a'/> Income is a "
            "permanent part, which grows and takes permanent shocks, times a transitory part. "
            "<bookmark mark='b'/> The shocks have a spread of about ten percent each, and there is a small chance, "
            "half a percent a year, of no income at all: a lost job, an illness. <bookmark mark='c'/> The household "
            "cannot borrow, and it is impatient: with its income rising, it would like to borrow against the future "
            "if it could. <bookmark mark='d'/> Measure everything relative to permanent income. Cash on hand, m, is "
            "what it has to spend this year. The Euler equation now has an expectation over next year's shocks, and "
            "next year's cash depends on what it saves. <bookmark mark='e'/> These are the Island's planted "
            "parameters."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def egm(self):
        b = load("buffer")
        steps = VGroup(
            label(r"the endogenous grid method \ (Carroll, \ 2006)", font_size=27, color=E.ACCENT),
            label(r"1. \ fix a grid of what is carried forward, \ $a = m - c$", font_size=24, color=SAVE),
            label(r"2. \ for each $a$, \ average the right side over next year's shocks, \ using the last guess of "
                  r"$c(\cdot)$", font_size=24, color=RISK),
            label(r"3. \ invert: \ $c = \big(\beta R\, \mathbb{E}[\ldots]\big)^{-1/\gamma}$, \ \ and set $m = a + c$",
                  font_size=24, color=SPEND),
            label(r"4. \ the pairs $(m, c)$ are the new consumption function; \ repeat until it stops changing",
                  font_size=24, color=WHITE),
            label(rf"no equation solved numerically: \ {b['iterations']} rounds, \ a fraction of a second", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Carroll, Economics Letters 91(3) (2006): \ 312--320", corner=DR, font_size=12)
        with self.voiceover(
            "How do you solve it? The obvious way, for each level of cash, searches for the consumption that "
            "satisfies the Euler equation, a root found again and again. <bookmark mark='a'/> In 2006 Carroll "
            "found a shortcut, the endogenous grid method. Fix a grid, not of cash, but of what the household "
            "carries forward. <bookmark mark='b'/> For each amount carried forward, next year's cash is known in "
            "every state, so the right side of the Euler equation is just an average. <bookmark mark='c'/> Invert "
            "marginal utility to get the consumption that makes the equation hold, and add it to what was carried "
            "forward: that is the cash the household must have had. <bookmark mark='d'/> The pairs of cash and "
            "consumption are the new consumption function. Repeat until it stops changing. <bookmark mark='e'/> "
            f"No equation solved numerically. Here it takes {b['iterations']} rounds and a fraction of a second. "
            "Part fifty-two solves economies of a hundred thousand such households this way."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", steps[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def function(self):
        b = load("buffer")
        m = np.array(b["m"])
        ax = plane([0, 5], [0, 2.0], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.4, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.5, 1.0, 1.5, 2.0],
                   xlabel=r"cash on hand $m$ \ (years of permanent income)", ylabel=r"consumption $c(m)$",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        diag = seg(ax, 0, 0, 2.0, 2.0, color=GREY_B, width=2, dashed=True)
        dlab = label(r"spend it all", font_size=16, color=GREY_B).next_to(ax.ax.c2p(1.75, 1.95), LEFT, buff=0.1)
        sure = path(ax, m, b["sure_c"], color=INCOME, width=3, yr=(0, 2.0))
        risky = path(ax, m, b["c"], color=SPEND, width=4, yr=(0, 2.0))
        tgt = DashedLine(ax.ax.c2p(b["target"], 0), ax.ax.c2p(b["target"], b["c_target"]), color=SAVE,
                         stroke_width=2)
        tlab = label(rf"target $m^* = {b['target']:.2f}$", font_size=17, color=SAVE).next_to(
            ax.ax.c2p(b["target"], 0.2), RIGHT, buff=0.1)
        at = b["at"]
        side = VGroup(
            label(r"no income risk", font_size=20, color=INCOME),
            label(r"with income risk", font_size=20, color=SPEND),
            label(r"share of an extra dollar spent:", font_size=19, color=GREY_A),
            *[label(rf"$m = {k}$: \ {at[k]['mpc']:.2f}", font_size=20, color=SPEND) for k in ("0.5", "1", "1.5", "5")],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the answer. Cash on hand, in years of permanent income, along the bottom. Consumption up the "
            "side. <bookmark mark='a'/> Without income risk, the impatient household spends everything it has until "
            "its cash passes a year's income, and then saves only a little: the blue line. "
            "<bookmark mark='b'/> With risk, the green line: it holds back at every level of cash, and the line "
            "bends. That bend is Zeldes's point. <bookmark mark='c'/> Where the line is steep, at low cash, an extra "
            f"dollar is mostly spent: {at['0.5']['mpc']:.2f} of it at half a year's income, {at['1']['mpc']:.2f} at a "
            f"year's. <bookmark mark='d'/> Where it is flat, among households with a cushion, almost none: "
            f"{at['5']['mpc']:.2f} at five years. <bookmark mark='e'/> And there is a target, cash of about "
            f"{b['target']:.2f} years of income, where impatience, which pulls the stock down, just balances "
            "prudence, which builds it up. A household below the target saves toward it; one above spends down. "
            "The buffer stock."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(dlab), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(sure), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(risky), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]), FadeIn(side[6]))
            vo.wait_until("e")
            self.play(Create(tgt), FadeIn(tlab))
        self.clear_scene()

    def population(self):
        b = load("buffer")
        m_ = load("mpc")
        ms = np.array(m_["m_sample"])
        ax = plane([0, 4], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.8,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"cash on hand $m$", ylabel=r"share of a month's windfall spent within the year",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        h, e = np.histogram(ms, bins=np.linspace(0, 4, 41), density=True)
        scale = 0.9 / h.max()
        hist = VGroup()
        for k, v in enumerate(h):
            if v <= 0:
                continue
            x0, x1 = e[k], e[k + 1]
            hist.add(Rectangle(width=ax.ax.c2p(x1, 0)[0] - ax.ax.c2p(x0, 0)[0],
                               height=ax.ax.c2p(0, v * scale)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0,
                               fill_color=CASH, fill_opacity=0.35).move_to(
                [(ax.ax.c2p(x0, 0)[0] + ax.ax.c2p(x1, 0)[0]) / 2, ax.ax.c2p(0, 0)[1], 0], aligned_edge=DOWN))
        mm = np.array(b["m"])
        windfall = 1 / 12
        mpc_w = (np.interp(mm + windfall, b["m_grid"], b["c_grid"]) - np.interp(mm, b["m_grid"], b["c_grid"])) / windfall
        curve = path(ax, mm, mpc_w, color=SPEND, width=4, xr=(0.05, 4), yr=(0, 1.0))
        side = VGroup(
            label(r"where the Island's 20{,}000 \\ households sit \ (shaded)", font_size=19, color=CASH),
            label(r"the share each would spend", font_size=19, color=SPEND),
            label(rf"average: \ {m_['mean_mpc']:.2f}", font_size=26, color=SPEND),
            label(rf"poorest tenth in cash: \ {m_['mpc_by_decile'][0]:.2f}; \\ richest: \ "
                  rf"{m_['mpc_by_decile'][-1]:.2f}", font_size=19, color=GREY_A),
            label(rf"permanent income: \ {m_['pih_year']:.3f}", font_size=20, color=INCOME),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now give the Island twenty thousand such households, and let them live long enough that their cash "
            "settles into its long-run spread. <bookmark mark='a'/> The shaded hills show where they sit: most near "
            "the target, some below after bad years. <bookmark mark='b'/> The green line is the share of a windfall "
            "worth a month's income that each would spend within the year. <bookmark mark='c'/> Averaged over the "
            f"Island, {m_['mean_mpc']:.2f}. <bookmark mark='d'/> For the tenth of households with the least cash, "
            f"{m_['mpc_by_decile'][0]:.2f}; for the tenth with the most, {m_['mpc_by_decile'][-1]:.2f}. "
            "<bookmark mark='e'/> The permanent-income household would spend "
            f"{m_['pih_year']:.3f}. Prudence and impatience together give a propensity to spend eight times larger, "
            "and far larger for those short of cash. It is still below what the rebates showed in a single quarter. "
            "Keep that gap in mind."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in hist], lag_ratio=0.03), FadeIn(side[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
