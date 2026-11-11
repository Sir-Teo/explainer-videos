from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
from videos.quant.quant42.common import (BAD, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C, fit_right,
                                         load)


class Artificial(VoiceoverScene):
    def construct(self):
        f = load("facts")
        self.card(f)
        self.santa_fe()
        self.model()
        self.path(f)
        self.compare_paths(f)
        self.facts(f)
        self.acf(f)
        self.msm(f)
        self.why_it_works()
        self.brock_hommes()
        self.zero_intel()
        self.question()

    def card(self, f):
        c = chapter_card(1, r"Artificial markets", r"Can simple rules produce the market's fat tails and clustered "
                         r"volatility?", part=PART)
        with self.voiceover(
            'Chapter one, and a qualified answer to the pause: this chosen switching-agent model generates clustered volatility and heavier tails than its Gaussian comparator. That shows one possible mechanism. It does not prove that imitation is necessary, that fixed-rule markets must have thin tails, or that a matching simulation identifies the real market. We will compare its misses as well as its successes.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def santa_fe(self):
        cards = VGroup(
            desk_question(r"the Santa Fe market (1997)", r"Arthur, Holland, LeBaron, Palmer and Tayler: agents hold "
                          r"forecasting rules, keep the ones that work, and breed new ones by a genetic algorithm",
                          width=12.4, font_size=19),
            desk_question(r"two regimes", r"learning slowly, they converge to the rational-expectations price; "
                          r"learning fast, technical trading emerges, with bubbles, crashes and volatility clustering",
                          width=12.4, font_size=19),
            desk_question(r"the lesson", 'adaptive interaction is one possible model mechanism; matching stylised facts does not identify a unique cause', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The Santa Fe artificial market. <bookmark mark='a'/> Arthur, Holland, LeBaron, Palmer and Tayler gave agents forecasting rules that were selected and recombined. <bookmark mark='b'/> Their reported slow- and fast-learning regimes differed: prices could resemble a rational-expectations benchmark or show technical trading and clustered volatility. These are model-specific results, not a universal convergence theorem. <bookmark mark='c'/> Adaptive interaction offers a possible explanation, rather than a proof that real investors use these rules."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"\text{fundamentalists}", r":", r"\phi\,(p^* - p_t) + \sigma_f\varepsilon_f", font_size=38,
                      colors={r"\text{fundamentalists}": COMP_C}),
                cmath(r"\text{chartists}", r":", r"\chi\,(p_t - p_{t-1}) + \sigma_c\varepsilon_c", font_size=38,
                      colors={r"\text{chartists}": SHARE_C}),
                cmath(r"p_{t+1} - p_t", r"=", r"\mu\,\bigl[n_f\,(\ldots) + n_c\,(\ldots)\bigr]", font_size=38),
                cmath(r"a_t", r"=", r"a_0 + a_n(n_f - n_c) + a_p(p_t - p^*)^2", font_size=38, colors={r"a_t": HURDLE})]
        whys = [why(r"expect the price to return to its fundamental value"),
                why(r"extrapolate the last move; their orders are noisier, $\sigma_c > \sigma_f$"),
                why(r"a market maker moves the price with the net demand of the two groups, in shares $n_f$ and $n_c$"),
                why(r"the pull toward fundamentalism: herding ($a_n$) and a large mispricing ($a_p$); agents switch with "
                    r"probabilities $\nu e^{\mp a_t}$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A smaller Franke-Westerhoff-type illustration in the House's module. <bookmark mark='a'/> Fundamentalists trade toward a fixed log fundamental value of zero. <bookmark mark='b'/> Chartists extrapolate the last move and have noisier orders. <bookmark mark='c'/> Net demand moves the log price. <bookmark mark='d'/> Switching attractiveness depends on the population imbalance and squared mispricing, with probabilities clipped at one. This implementation has no separate recent-profit state; the performance-based mechanism comes later in Brock and Hommes."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def path(self, f):
        r = np.asarray(f["path"]["r"], float)
        nf = np.asarray(f["path"]["nf"], float)
        t = np.arange(len(r))
        sc = 1 / (np.abs(r).max() * 1.05)
        g1 = axes([0, len(r)], [-1, 1], x_length=11.6, y_length=2.4, xlabel=r"", ylabel=r"returns, simulated",
                  xticks=[], yticks=[], font_size=14).move_to(UP * 1.4)
        g2 = axes([0, len(r)], [0, 1], x_length=11.6, y_length=2.0, xlabel=r"2,000 simulated days",
                  ylabel=r"chartists' share, $n_c$", xticks=[], yticks=[0, 0.5, 1], font_size=14).move_to(DOWN * 1.8)
        bars = VGroup(*[Line(g1.ax.c2p(t[i], 0), g1.ax.c2p(t[i], r[i] * sc), color=SIM_C, stroke_width=1.2)
                        for i in range(0, len(r), 2)])
        sh = curve(g2.ax, t, 1 - nf, SHARE_C, stroke_width=2.5)
        with self.voiceover(
            "Two thousand simulated days. <bookmark mark='a'/> The returns come in bursts: calm stretches, then "
            "violent ones. <bookmark mark='b'/> And underneath, the chartists' share. When herding tips the crowd into "
            "chartism, their noisier, trend-chasing orders dominate, and volatility rises; when a large mispricing "
            "pulls them back to fundamentals, it falls. Volatility here has a cause you can see: who is trading."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.002), run_time=3)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(Create(sh), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def compare_paths(self, f):
        r = np.asarray(f["real_path"], float)
        s_ = np.asarray(f["path"]["r"], float)
        r = (r - r.mean()) / r.std()
        s_ = (s_ - s_.mean()) / s_.std()
        sc = 1 / (max(np.abs(r).max(), np.abs(s_).max()) * 1.05)
        g1 = axes([0, len(r)], [-1, 1], x_length=11.6, y_length=2.2, xlabel=r"", ylabel=r"US market, last 2,000 days to 2020",
                  xticks=[], yticks=[], font_size=14).move_to(UP * 1.5)
        g2 = axes([0, len(s_)], [-1, 1], x_length=11.6, y_length=2.2, xlabel=r"standardised daily returns, same scale",
                  ylabel=r"agent market, 2,000 days", xticks=[], yticks=[], font_size=14).move_to(DOWN * 1.5)
        b1 = VGroup(*[Line(g1.ax.c2p(i, 0), g1.ax.c2p(i, r[i] * sc), color=REAL_C, stroke_width=1.2) for i in range(0, len(r), 2)])
        b2 = VGroup(*[Line(g2.ax.c2p(i, 0), g2.ax.c2p(i, s_[i] * sc), color=SIM_C, stroke_width=1.2) for i in range(0, len(s_), 2)])
        with self.voiceover(
            "Side by side, standardized and displayed on the same scale. <bookmark mark='a'/> The last two thousand research-window US market observations through December twenty twenty; March twenty twenty is near the end. <bookmark mark='b'/> A chosen two-thousand-day segment of the agent simulation also shows bursts. A visual resemblance is descriptive, not a held-out validation or evidence of a unique mechanism."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), LaggedStart(*[Create(b_) for b_ in b1], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b_) for b_ in b2], lag_ratio=0.002), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def facts(self, f):
        rows = [(r"", r"US market, 1926--2020", r"agent market", r"Gaussian")]
        rows.append((r"excess kurtosis", rf"{f['real']['kurt']:.1f}", rf"{f['sim']['kurt']:.1f}", rf"{f['gauss']['kurt']:.1f}"))
        rows.append((r"tail exponent (Hill)", rf"{f['real']['hill']:.1f}", rf"{f['sim']['hill']:.1f}", rf"{f['gauss']['hill']:.1f}"))
        rows.append((r"autocorrelation of returns, lag 1", rf"{f['real']['acf_r'][0]:+.2f}", rf"{f['sim']['acf_r'][0]:+.2f}",
                     rf"{f['gauss']['acf_r'][0]:+.2f}"))
        rows.append((r"autocorrelation of $|r|$, lag 20", rf"{f['real']['acf_abs'][4]:.2f}", rf"{f['sim']['acf_abs'][4]:.2f}",
                     rf"{f['gauss']['acf_abs'][4]:.2f}"))
        cols = [GREY_A, REAL_C, SIM_C, GREY_B]
        xs = [-3.6, 0.9, 3.6, 5.8]
        tab = VGroup()
        for j, row in enumerate(rows):
            cells = VGroup(*[label(c, font_size=20 if j else 19, color=(cols[i] if j else QC.IDEA)) for i, c in enumerate(row)])
            for i, c in enumerate(cells):
                c.move_to([xs[i], 2.0 - 0.8 * j, 0])
            if len(cells[0].get_all_points()):  # an empty header cell has no points to align
                cells[0].align_to(np.array([-6.4, 0, 0]), LEFT)
            tab.add(cells)
        with self.voiceover(
            f"""The descriptive statistics. <bookmark mark='a'/> Sample excess kurtosis is {f['real']['kurt']:.1f} for the research-window US market and {f['sim']['kurt']:.1f} for this agent simulation; a Gaussian has population excess kurtosis zero. <bookmark mark='b'/> Hill estimates summarize a selected upper tail and do not prove an exact power law. <bookmark mark='c'/> Small linear return autocorrelations do not establish full unpredictability or efficiency. <bookmark mark='d'/> At lag twenty the absolute-return autocorrelation is {f['real']['acf_abs'][4]:.2f} in the data and {f['sim']['acf_abs'][4]:.2f} here. These are descriptive comparisons, without a new fit or causal identification."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def acf(self, f):
        lags = np.asarray(f["real"]["lags"], float)
        g = axes([0, 2.05], [-0.05, 0.4], x_length=7.6, y_length=4.2, xlabel=r"lag, days (log scale)",
                 ylabel=r"autocorrelation of $|r|$", xticks=[0, 1, 2], yticks=[0, 0.1, 0.2, 0.3],
                 xfmt=lambda u: {0: "1", 1: "10", 2: "100"}[int(u)], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        lx = np.log10(lags)
        lines = [curve(ax, lx, np.asarray(f[k]["acf_abs"], float), col, stroke_width=3)
                 for k, col in (("real", REAL_C), ("sim", SIM_C), ("gauss", GREY_B))]
        dots = VGroup(*[VGroup(*[Dot(ax.c2p(x_, y_), radius=0.05, color=col) for x_, y_ in zip(lx, f[k]["acf_abs"])])
                        for k, col in (("real", REAL_C), ("sim", SIM_C), ("gauss", GREY_B))])
        leg = legend([(REAL_C, r"US market"), (SIM_C, r"agent market"), (GREY_B, r"Gaussian")], font_size=17)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Absolute-return autocorrelations across horizons. <bookmark mark='a'/> These research-window US estimates show persistent dependence. <bookmark mark='b'/> The chosen agent simulation also shows persistence; the group share is a state variable that can move slowly. Matching this feature does not identify the real market's cause. <bookmark mark='c'/> Independent Gaussian draws have zero population autocorrelation, while finite-sample estimates fluctuate. Part seven used GARCH to describe such persistence."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), Create(lines[0]), FadeIn(dots[0]), run_time=1.5)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(dots[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(dots[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def msm(self, f):
        ms = f["msm"]
        L = np.asarray(ms["L"], float)
        chis, sigs = ms["chis"], ms["sigs"]
        n1, n2 = L.shape
        cell = 0.5
        lo, hi = float(np.log10(L.min() + 1e-3)), float(np.log10(np.quantile(L, 0.9) + 1e-3))
        sq = VGroup()
        for i in range(n1):
            for j in range(n2):
                u = (np.log10(L[i, j] + 1e-3) - lo) / max(hi - lo, 1e-9)
                u = float(np.clip(u, 0, 1))
                col = interpolate_color(ManimColor(SIM_C), ManimColor(GREY_E), u)
                sq.add(Square(cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=col, fill_opacity=0.95)
                       .move_to([(j - n2 / 2 + 0.5) * cell, (i - n1 / 2 + 0.5) * cell, 0]))
        b = ms["best"]
        spread = 100 * float(np.max(L.max(0) - L.min(0)) / L.min())
        ratio = float(L.max() / L.min())
        i_b, j_b = list(chis).index(b["chi"]), list(sigs).index(b["sig_c"])
        mark = Square(cell, stroke_width=3, stroke_color=HURDLE).move_to(sq[i_b * n2 + j_b])
        xl = label(r"chartists' noise $\sigma_c$, 1.6 to 3.6", font_size=17, color=GREY_A).next_to(sq, DOWN, buff=0.25)
        yl = label(r"extrapolation $\chi$, 1.5 to 3.1", font_size=17, color=GREY_A).rotate(PI / 2).next_to(sq, LEFT, buff=0.25)
        grid = VGroup(sq, mark, xl, yl).move_to(LEFT * 2.6 + DOWN * 0.2)
        side = VGroup(label(r"lighter: closer to the US market", font_size=17, color=SIM_C),
                      label(rf"best: $\chi = {b['chi']:.1f}$, $\sigma_c = {b['sig_c']:.2f}$", font_size=18, color=HURDLE),
                      label(rf"kurtosis {b['kurt']:.1f} (target {ms['target'][0]:.1f})", font_size=17, color=GREY_A),
                      label(rf"lag-20 $|r|$ autocorrelation {b['acf20']:.2f} (target {ms['target'][1]:.2f})", font_size=17,
                            color=GREY_A),
                      label(rf"across $\chi$, the loss changes by at most {spread:.0f}\%", font_size=17, color=BAD)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(grid, RIGHT, buff=0.6)
        fit_right(side)
        kurt_b, acf_b, kt, at = b["kurt"], b["acf20"], ms["target"][0], ms["target"][1]
        head = label(r"Fitting the agent market to the real one: simulated moments", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"""The original simulated-moments grid uses eighty-one parameter pairs and a fixed simulation seed. <bookmark mark='a'/> Its loss matches two research-window moments, scaled by their target values. <bookmark mark='b'/> The best tested cell gives kurtosis {kurt_b:.1f} versus {kt:.1f}, and lag-twenty dependence {acf_b:.2f} versus {at:.2f}. This boundary optimum is not a continuous optimum or an unseen forecast. <bookmark mark='c'/> Across this chosen grid the loss changes {ratio:.1f}-fold overall, but by at most {spread:.0f} percent along the extrapolation direction at fixed noise. Weak sensitivity here suggests limited parameter information; it is not a general identification theorem. No new tuning is performed."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(sq), FadeIn(xl), FadeIn(yl), run_time=1.5)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(side[:4]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def why_it_works(self):
        rows = [cmath(r"\text{Var}(r_{t+1}\mid\mathcal F_t)", r"\approx", r"\mu^2\bigl[n_f^2\sigma_f^2 + n_c^2\sigma_c^2\bigr]", font_size=38,
                      colors={r"\text{Var}(r_{t+1}\mid\mathcal F_t)": SIM_C}),
                cmath(r"n_c", r":", r"\text{a slow, herding process}", font_size=40, colors={r"n_c": SHARE_C}),
                cmath(r"\Rightarrow", r"", r"\text{stochastic volatility, with a structural cause}", font_size=38)]
        whys = [why(r"given who is trading, the variance of the next return is set by the groups' shares and noise"),
                why(r"the share moves slowly, because each agent's switch depends on the others'"),
                why(r"Franke and Westerhoff called it structural stochastic volatility, and estimated versions of it on "
                    r"stock indices and exchange rates by the method of simulated moments")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The mechanism within this simulation. <bookmark mark='a'/> Conditional on the full current state and independent order shocks, the next log-return innovation variance is determined by the squared group shares and their noise scales. Conditioning only on the share can leave extra variation from other state variables. <bookmark mark='b'/> Feedback can make the share persistent. <bookmark mark='c'/> This motivates the structural stochastic-volatility interpretation; it does not identify observed market volatility from the plot alone."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def brock_hommes(self):
        rows = [cmath(r"n_h", r"=", r"\frac{e^{\beta U_h}}{\sum_k e^{\beta U_k}}", font_size=42, colors={r"n_h": SHARE_C}),
                cmath(r"U_h", r":", r"\text{each strategy's recent realised profit}", font_size=38),
                cmath(r"\beta \uparrow", r"\Rightarrow", r"\text{a steady state, then cycles, then chaos}", font_size=38,
                      colors={r"\beta \uparrow": BAD})]
        whys = [why(r"Brock and Hommes (1997, 1998): adaptive belief systems; agents pick a forecasting rule with a "
                    r"discrete-choice (logit) probability"),
                why(r"the fitness of a rule is what it earned lately, so fashions follow performance"),
                why(r"as traders switch faster toward what worked, the fundamental steady state loses stability: "
                    r"rational routes to randomness")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The deterministic cousin, from William Brock and Cars Hommes. <bookmark mark='a'/> Traders choose among "
            "forecasting rules with logit probabilities, <bookmark mark='b'/> weighted by each rule's recent profit, so "
            "fashions follow performance. <bookmark mark='c'/> As the intensity of choice rises, the steady state at "
            "the fundamental value loses stability, first to cycles, then to chaos. They called it a rational route to "
            "randomness: no noise needed, only switching toward what worked."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def zero_intel(self):
        cards = VGroup(
            desk_question(r"zero intelligence (1993)", r"Gode and Sunder: traders who bid at random within their budget "
                          r"constraint reach almost full allocative efficiency in a double auction", width=12.4,
                          font_size=19),
            desk_question(r"the order book (2005)", r"Farmer, Patelli and Zovko: random order flow predicts much of how "
                          r"spreads depend on order rates (Part 36)", width=12.4, font_size=19),
            desk_question(r"so what do agents add?", 'institutional efficiency and adaptive price dynamics are model-specific findings, not universal necessities', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "An institutional comparison. <bookmark mark='a'/> Gode and Sunder reported high allocative efficiency for budget-constrained random traders in specified double auctions. It is not guaranteed by arbitrary random trading. <bookmark mark='b'/> Farmer and coauthors studied what selected order-book statistics can follow from a random-flow model. <bookmark mark='c'/> Market rules and adaptive behavior can both matter. These examples do not show that imitation is the only way to produce fat tails or clustering."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a hundred agents each sometimes switch view on their own, and sometimes copy whoever they meet. "
                       r"If copying is far more common, where does the crowd spend its time?")
        with self.voiceover(
            "Pause and predict. A hundred agents each sometimes switch view on their own, and sometimes copy whoever "
            "they happen to meet. If copying is far more common than switching alone, where does the crowd spend its "
            "time: evenly split, or somewhere else?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
