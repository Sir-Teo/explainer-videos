from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Aiyagari(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The Aiyagari economy", r"How much capital does a nation of self-insurers build?",
             "Chapter three. The Aiyagari economy.", lit={1994: r"Aiyagari"}, scale=("household", "nation"),
             horizon=("a century",))
        self.model()
        self.rules()
        self.market()

    def model(self):
        T = TRUTH["aiyagari"]
        blocks = VGroup(
            VGroup(label(r"households", font_size=26, color=MANY),
                   MathTex(r"\max\ \mathbb{E}\sum_t \beta^t \frac{c_t^{1-\gamma}}{1-\gamma}", font_size=34),
                   MathTex(r"c_t + a_{t+1} = (1 + r)\,a_t + w\,e_t,\quad a_{t+1} \ge 0", font_size=32),
                   label(r"$e_t$: \ a persistent, \ uninsurable wage draw", font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.22),
            VGroup(label(r"firms", font_size=26, color=DEMAND),
                   MathTex(r"r = \alpha K^{\alpha - 1} - \delta,\qquad w = (1 - \alpha) K^{\alpha}", font_size=32),
                   label(r"capital earns its marginal product", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.22),
            VGroup(label(r"the market", font_size=26, color=E.ACCENT),
                   MathTex(r"K = \int a \; d\lambda(a, e)", font_size=34),
                   label(r"$\lambda$: \ the stationary distribution of households", font_size=19,
                         color=GREY_A)).arrange(DOWN, buff=0.22),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(UP * 0.7)
        if blocks.width > 13.2:
            blocks.width = 13.2
        cal = label(rf"a year per period: \ $\beta = {T['beta']}$, \ $\gamma = {T['gamma']:.0f}$, \ wages with "
                    rf"persistence {T['rho']} and spread {T['sd']}, \ $\alpha = {T['alpha']}$, \ "
                    rf"$\delta = {T['delta']}$", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Aiyagari, \ QJE 109(3) (1994)", corner=DR, font_size=12)
        with self.voiceover(
            "In 1994 Rao Aiyagari put such households into the growth model. <bookmark mark='a'/> Households "
            "maximize expected lifetime utility. Each year they earn a wage times a personal draw that is "
            "persistent and cannot be insured, earn interest on their savings, and cannot borrow. <bookmark "
            "mark='b'/> Firms rent capital and labour and pay each its marginal product, as in Part twenty. "
            "<bookmark mark='c'/> And the market for capital clears when the savings of all households, added up "
            "over their stationary distribution, equal the capital firms use. <bookmark mark='d'/> The numbers "
            "here: a discount factor of 0.96 a year, risk aversion of three, wage draws with persistence 0.9, "
            "capital's share 0.36, depreciation eight percent."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, b in zip("abc", blocks):
                vo.wait_until(mk)
                self.play(FadeIn(b, shift=UP * 0.1), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(cal))
        self.clear_scene()

    def rules(self):
        A = load("aiyagari")
        a = np.array(A["a"])
        c = np.array(A["c"])
        ap = np.array(A["ap"])
        e = np.array(A["e"])
        xr = (0, 15)
        ax1 = plane([0, 15], [0, 3.5], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.4, y_length=4.4,
                    xticks=[0, 5, 10, 15], yticks=[0, 1, 2, 3], xlabel=r"wealth", ylabel=r"consumption",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ax2 = plane([0, 15], [0, 15], center=RIGHT * 3.4 + DOWN * 0.4, x_length=5.4, y_length=4.4,
                    xticks=[0, 5, 10, 15], yticks=[0, 5, 10, 15], xlabel=r"wealth this year",
                    ylabel=r"wealth next year", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        idx = [0, 3, len(e) - 1]
        cols = (POOR, MANY, RICH)
        cc = VGroup(*[path(ax1, a, np.minimum(c[:, j], 3.5), col, 2.6, xr=xr) for j, col in zip(idx, cols)])
        aa = VGroup(*[path(ax2, a, ap[:, j], col, 2.6, xr=xr, yr=(0, 15)) for j, col in zip(idx, cols)])
        diag = seg(ax2, 0, 0, 15, 15, GREY_B, 1.4, dashed=True)
        key = VGroup(*[label(t, font_size=16, color=col) for t, col in zip(
            (r"lowest wage", r"middle wage", r"highest wage"), cols)]).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        k1 = label(r"spend everything \\ at the limit", font_size=16, color=POOR).move_to(ax1.ax.c2p(4.5, 0.4))
        k2 = label(r"above the diagonal: \ saving \\ below it: \ running down", font_size=16, color=GREY_A).move_to(
            ax2.ax.c2p(10.5, 3.0))
        with self.voiceover(
            "The household's rules, found by the endogenous grid method of Part fifty-one. <bookmark mark='a'/> On "
            "the left, consumption against wealth for the lowest, middle and highest wage. At the bottom, the "
            "low-wage household spends everything it has: the borrowing limit binds. The curves are steep there "
            "and flatten as wealth grows: the more you have, the less a dollar more changes what you spend. "
            "<bookmark mark='b'/> On the right, next year's wealth against this year's. Above the dashed diagonal "
            "the household saves; below it, it runs its savings down. A good year pushes it up, a bad year pulls "
            "it down: <bookmark mark='c'/> wealth is a buffer, filled in good years and drained in bad ones."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(ax2), Create(diag), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in cc], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(k1))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in aa], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(k2))
        self.clear_scene()

    def market(self):
        A = load("aiyagari")
        cv = A["curve"]
        rs = [100 * x["r"] for x in cv]
        sup = [x["supply"] for x in cv]
        dem = [x["demand"] for x in cv]
        ax = plane([0, 20], [0, 5], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 1, 2, 3, 4, 5], xlabel=r"capital",
                   ylabel=r"interest rate, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        s_curve = path(ax, sup, rs, SUPPLY, 3.2, xr=(0, 20))
        d_curve = path(ax, dem, rs, DEMAND, 3.2, xr=(0, 20))
        rho = 100 * A["rho_time"]
        rep = seg(ax, 0, rho, 20, rho, WHITE, 1.8, dashed=True)
        rep_dot = dot(ax, A["K_rep"], rho, WHITE, 0.1)
        eq_dot = dot(ax, A["K"], 100 * A["r"], E.ACCENT, 0.12)
        side = VGroup(
            label(r"pink: \ firms' demand", font_size=19, color=DEMAND),
            label(r"green: \ households' supply", font_size=19, color=SUPPLY),
            label(rf"one household: \\ {rho:.2f}\%, \ capital {A['K_rep']:.2f}", font_size=19, color=WHITE),
            label(rf"many households: \\ {100 * A['r']:.2f}\%, \ capital {A['K']:.2f}", font_size=19,
                  color=E.ACCENT),
            label(rf"{100 * (A['K'] / A['K_rep'] - 1):.0f}\% more capital: \\ precautionary saving", font_size=21,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now the market for capital. <bookmark mark='a'/> Firms want more capital the cheaper it is: the pink "
            "curve. <bookmark mark='b'/> Households, computed at each interest rate, supply the green curve. It "
            "rises slowly at first, then shoots up as the rate approaches the rate of time preference, for the "
            "reason of the last chapter. <bookmark mark='c'/> A representative household would supply any amount "
            f"at exactly {say_pct(A['rho_time'], 2)}, the dashed line, and the economy would settle at capital of "
            f"{A['K_rep']:.2f}. <bookmark mark='d'/> With many households the curves cross at "
            f"{say_pct(A['r'], 2)}, with capital of {A['K']:.2f}. <bookmark mark='e'/> That is "
            f"{100 * (A['K'] / A['K_rep'] - 1):.0f} percent more capital, built by households saving against risks "
            f"they cannot insure, and a saving rate of {100 * A['saving_rate']:.0f} percent. Aiyagari's question "
            "was how much of a nation's saving is precautionary; in this economy, a good deal."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(d_curve), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(s_curve), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(rep), FadeIn(rep_dot), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(eq_dot, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()
