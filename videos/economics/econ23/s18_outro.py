from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403

PROBLEMS = [
    r"Gordon: \ derive $P = D_1/(r-g)$ from $\sum_t D_1(1+g)^{t-1}/(1+r)^t$, \ and show that $-\frac{dP/P}{dr} = "
    r"\frac{1}{r-g}$.",
    r"Hayashi: \ with cost $I + \frac{\phi}{2}I^2/K$ and shadow value $q$, \ show that $I/K = (q-1)/\phi$, \ and find "
    r"$q$ in a steady state.",
    r"The option to wait: \ with $dV = \mu V dt + \sigma V dW$, \ show that waiting's value $AV^\beta$ solves "
    r"$\frac12\sigma^2\beta(\beta-1) + \mu\beta - r = 0$, \ and derive the threshold $\frac{\beta}{\beta-1}I$.",
    r"Modigliani--Miller: \ show that $r_E = r_A + \frac{D}{E}(r_A - r_D)$ leaves the weighted average cost of "
    r"capital equal to $r_A$.",
    r"The discount factor: \ from $p = \mathbb{E}[mx]$, \ derive $R_f = 1/\mathbb{E}[m]$ and $\mathbb{E}[R] - R_f = "
    r"-R_f\operatorname{cov}(m, R)$.",
    r"Hansen--Jagannathan: \ from the last result and $|\operatorname{corr}| \le 1$, \ derive $\sigma(m)/\mathbb{E}(m) "
    r"\ge |\mathbb{E}[R - R_f]|/\sigma(R - R_f)$.",
    r"Rational bubbles: \ show that $b_t = \mathbb{E}_t[m_{t+1}b_{t+1}]$ rules out a bubble on an asset with a final "
    r"date $T$.",
    r"$\bigstar$ \ Disasters: \ with growth $e^{g + \sigma z}(1-b)^{\mathbb{1}[\text{disaster}]}$ and probability "
    r"$p$, \ derive $R_f$ and the price of a claim to consumption under power utility.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"It is the expected value of what it pays, \ weighted by how much people will need it "
                          r"when it pays: \ risk is priced by its covariance with bad times. \ Firms build until the "
                          r"market values capital at its cost, \ slowly, \ and wait when the future is uncertain. \ "
                          r"But stocks have paid far more than smooth consumption can explain, \ prices swing more "
                          r"than dividends, \ and bubbles form even in the laboratory.", 11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        f = load("film")
        mini = plane([1871, 2013], [0, np.log10(10000)], x_length=4.2, y_length=1.3)
        logo = VGroup(path(mini, f["years"], np.log10(f["stock"]), STOCK, width=4, smooth=False),
                      path(mini, f["years"], np.log10(f["bill"]), BILL, width=4, smooth=False))
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: what is a claim on the future worth, and how does that decide what gets built? "
            "<bookmark mark='a'/> It is the expected value of what it pays, weighted by how much people will need "
            "it when it pays: risk is priced by its covariance with bad times. Firms build until the market values "
            "capital at what it costs, slowly, and wait when the future is uncertain. But stocks have paid far "
            "more than smooth consumption can explain, prices swing more than dividends, and bubbles form even in "
            "the laboratory."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        mo, g, f, o, r, h, d, v, hs = (load(k) for k in ("moments", "gordon", "firm", "option", "region", "hj",
                                                         "disasters", "volatility", "housing"))
        items = [
            (rf"the two numbers: \ the model's {100 * mo['published']['model_max_premium']:.2f}\% \ against the "
             rf"record's {100 * mo['published']['premium_mean']:.2f}\%", STOCK),
            (rf"present value: \ one point on $r$ takes {100 * g['fall_per_point']:.0f}\% off a long-lived asset",
             STOCK),
            (rf"the user cost and $q$: \ $q$ jumps to {f['q0']:.2f}, \ capital follows slowly", FIRM),
            (rf"the option to wait: \ build at {o['rows'][1]['multiple']:.0f} times the cost when volatility is 20\%",
             FIRM),
            (r"Modigliani--Miller: \ the pie, \ not the slices; \ and what breaks it", BILL),
            (r"Play it: \ the coconut tree is worth 8, \ the insurance tree 12", STOCK),
            (r"the Lucas tree: \ $p = \mathbb{E}[mx]$ prices every asset", SDF),
            (rf"the puzzle: \ Hansen--Jagannathan needs $\gamma \ge {h['needed_gamma']:.1f}$; \ the safe rate would "
             rf"be {100 * h['rf_at_need']:.0f}\%", RISK),
            (r"repairs: \ habits, \ long-run risk, \ disasters \ (5\% with $\gamma = 3.5$)", RISK),
            (rf"excess volatility: \ s.d.\ of price {v['sd_P']:.0f} \ against $P^*$'s {v['sd_Pstar']:.0f}", VALUE),
            (r"bubbles: \ 14 of 22 laboratory markets; \ Fisher's plateau, \ wrong", HOLD),
            (rf"housing at {hs['peak']:.2f} times its 2000 ratio to rents in {hs['peak_when'][:4]}; \ two dials; \ "
             r"the return on everything", HOUSE),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 23, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del d, r
        with self.voiceover(
            "Part twenty-three in twelve lines. <bookmark mark='a'/> The standard model allows a premium of a third "
            "of a point; the record shows six. One point on the discount rate takes a fifth off a long-lived "
            "asset. Firms invest toward a target that q measures, slowly, and wait to build when the future is "
            "volatile. Modigliani and Miller showed when financing cannot matter, and so why it does. The coconut "
            "tree was worth eight, the insurance tree twelve. One formula, price equals the expected discount factor "
            "times the payoff, prices every asset. The Hansen-Jagannathan bound needs risk aversion above eight, "
            "and then the safe rate would be absurd. Habits, long-run risk and disasters each repair it, at a "
            "price. Prices swing more than the dividends that follow. Bubbles appear in the laboratory, and Irving "
            "Fisher's plateau did not hold. And houses, two dials, and the return on everything."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The Gordon formula and its duration; Hayashi's investment rule; the option to wait; "
            "Modigliani and Miller's cost of equity; the discount factor's two consequences; the Hansen-Jagannathan "
            "bound; why a bubble needs no final date; and a starred problem on disasters. Full solutions are in the "
            "part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"John Cochrane, \emph{Asset Pricing} (revised ed., 2005), \ chs.\ 1--2 and 21",
             r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ ch.\ 9",
             r"Avinash Dixit and Robert Pindyck, \emph{Investment under Uncertainty} (1994)",
             r"Robert Shiller, \emph{Irrational Exuberance} (3rd ed., 2015)"],
            [r"Williams (1938); \ Gordon and Shapiro (1956); \ Jorgenson (1963); \ Tobin (1969); \ Hayashi (1982)",
             r"McDonald and Siegel (1986); \ Bloom (2009); \ Modigliani and Miller (1958); \ Myers and Majluf (1984)",
             r"Lucas (1978); \ Breeden (1979); \ Mehra and Prescott (1985); \ Hansen and Jagannathan (1991); \ Weil (1989)",
             r"Campbell and Cochrane (1999); \ Bansal and Yaron (2004); \ Rietz (1988); \ Barro (2006)",
             r"Shiller (1981); \ Campbell and Shiller (1988); \ Tirole (1985); \ Smith, Suchanek and Williams (1988)",
             r"Poterba (1984); \ Chirinko, Fazzari and Meyer (1999); \ Zwick and Mahon (2017); \ Novy-Marx and Rauh "
             r"(2011)",
             r"Jordà et al.\ (2019); \ He and Krishnamurthy (2013); \ Adrian, Etula and Muir (2014)"])
        with self.voiceover(
            "The reading: John Cochrane's Asset Pricing, whose first chapters this part follows; Romer for the "
            "macroeconomics of investment; Dixit and Pindyck for the option to wait; and Shiller's Irrational "
            "Exuberance for the other side. Then the papers, from Williams to the return on everything."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1982, r"Peter Diamond", r"an island where a taboo forbids eating the coconuts you pick: \ "
                          r"climbing pays only if others climb too", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 24 \ $\cdot$ \ Act V, \ The Long Run", font_size=30, color=GREY_B),
                     label(r"Looking for Work", font_size=46),
                     label(r"why are there unemployed workers and unfilled jobs at the same time?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ how the future is priced; \ next: \ why workers and jobs fail to meet",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked how the future is priced. The next asks why people who want work and firms that want "
            "workers fail to find each other. <bookmark mark='a'/> In 1982 Peter Diamond imagined an island where "
            "a taboo forbids eating the coconuts you pick yourself, so climbing a palm is worth it only if you "
            "expect to meet someone else who climbed. <bookmark mark='b'/> Part twenty-four: looking for work. Why "
            "are there unemployed workers and unfilled jobs at the same time?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
