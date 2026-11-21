from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class KrusellSmith(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Aggregate shocks: \ Krusell and Smith", r"What if the state is a whole distribution?",
             "Chapter seven. Aggregate shocks: Krusell and Smith.", lit={1998: r"Krusell and Smith",
                                                                      2010: r"Den Haan"},
             scale=("household", "nation"), horizon=("a decade",))
        self.problem()
        self.algorithm()
        self.fit()
        self.why()

    def problem(self):
        eq = MathTex(r"V(a, e;\ z, \lambda)", r"\qquad \lambda' = \Gamma(z, \lambda, z')", font_size=46,
                     color=THEORY).move_to(UP * 2.0)
        rows = VGroup(
            label(r"to choose, \ a household must forecast prices", font_size=23, color=WHITE),
            label(r"prices depend on capital, \ capital on the whole distribution $\lambda$", font_size=23,
                  color=WHITE),
            label(r"so the state includes a distribution: \ infinitely many numbers", font_size=23, color=ERR),
            label(r"Krusell and Smith's bet: \ forecast with the mean alone, \ and check", font_size=24,
                  color=RULE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.7)
        with self.voiceover(
            "So far the economy has been in a steady state. Now let it have booms and recessions: aggregate "
            "productivity switches between good and bad times, and unemployment rises in the bad ones. <bookmark "
            "mark='a'/> To decide how much to save, a household must forecast next year's wages and interest "
            "rates. <bookmark mark='b'/> Those depend on next year's capital, which depends on how much every "
            "household saves, which depends on the whole distribution of wealth today, and on how that "
            "distribution will move. <bookmark mark='c'/> The state of the economy includes a distribution: in "
            "principle, infinitely many numbers. <bookmark mark='d'/> Krusell and Smith made a bet: let households "
            "forecast using only the average, and then check whether anything better was available."
        ) as vo:
            self.play(Write(eq), run_time=1.8)
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def algorithm(self):
        K = load("ks")
        steps = flow_chain([(r"guess a rule: \ $\log K' = b_0 + b_1 \log K$", RULE),
                            (r"solve every household's problem, \ given the rule", MANY),
                            (r"simulate the whole distribution", DIST),
                            (r"regress $\log K'$ on $\log K$: \ a new rule", RULE)], box_w=2.9, box_h=1.35,
                           font_size=19, buff=0.45).move_to(UP * 1.6)
        back = CurvedArrow(steps.boxes[-1].get_bottom() + DOWN * 0.1, steps.boxes[0].get_bottom() + DOWN * 0.1,
                           angle=-TAU / 6, color=GREY_B, stroke_width=3)
        hist = K["history"]
        slopes = [h["b"][1][1] for h in hist[1:]]
        lo = float(np.floor(min(slopes) * 100) / 100)
        ax = plane([1, len(hist)], [lo, 1.0], center=DOWN * 2.1 + LEFT * 1.6, x_length=7.0, y_length=2.3,
                   xticks=[1, 10, 20, 30], yticks=[lo, 1.0], xlabel=r"round",
                   ylabel=r"the estimated slope, \ good times", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=13)
        conv = path(ax, np.arange(2, len(hist) + 1), slopes, RULE, 2.6, smooth=False)
        side = VGroup(
            label(rf"{K['rounds']} rounds \\ {K['seconds']:.0f} seconds", font_size=20, color=WHITE),
            label(rf"final rule, \ good times: \\ $\log K' = {K['b'][1][0]:.3f} + {K['b'][1][1]:.3f}\log K$",
                  font_size=19, color=RULE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.6)
        tag = published_tag(r"calibration: \ Den Haan, \ Judd and Juillard, \ JEDC (2010)", corner=DR, font_size=12)
        with self.voiceover(
            "The algorithm is a loop. <bookmark mark='a'/> Guess a rule that forecasts next quarter's capital from "
            "this quarter's, one for good times and one for bad. <bookmark mark='b'/> Solve every household's "
            "problem as if the rule were true, by the endogenous grid method. <bookmark mark='c'/> Simulate the "
            "economy for a thousand quarters, moving the whole distribution forward. <bookmark mark='d'/> Regress "
            "the simulated capital on its own past to get a new rule, and go round again until the rule stops "
            f"changing. <bookmark mark='e'/> Here it took {K['rounds']} rounds and {K['seconds']:.0f} seconds, in "
            "the calibration that a comparison of methods made standard in 2010."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            self.play(Create(back))
            vo.wait_until("e")
            self.play(FadeIn(ax), Create(conv), FadeIn(side), run_time=2.0)
        self.clear_scene()

    def fit(self):
        K = load("ks")
        b = K["burn"]
        k = np.array(K["K"])[b:b + 300]
        kr = np.array(K["K_rule"])[b:b + 300]
        z = np.array(K["z"])[b:b + 300]
        lo, hi = float(min(k.min(), kr.min())) - 0.3, float(max(k.max(), kr.max())) + 0.3
        ax = plane([0, 300], [lo, hi], center=LEFT * 1.4 + DOWN * 0.2, x_length=8.6, y_length=4.6,
                   xticks=[0, 100, 200, 300], yticks=[round(lo + 0.3), round(hi - 0.3)], xlabel=r"quarters",
                   ylabel=r"capital", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        spans, start = [], None
        for t, zz in enumerate(z):
            if zz == 0 and start is None:
                start = t
            if zz == 1 and start is not None:
                spans.append((start, t))
                start = None
        if start is not None:
            spans.append((start, len(z)))
        sh = shade(ax, spans, lo, hi)
        act = path(ax, np.arange(len(k)), k, WHITE, 2.6, smooth=False)
        rule = path(ax, np.arange(len(kr)), kr, RULE, 2.2, smooth=False)
        side = VGroup(
            label(r"grey bands: \ bad times", font_size=18, color=GREY_A),
            label(r"white: \ the economy, \\ every household simulated", font_size=18, color=WHITE),
            label(r"gold: \ the rule alone, \\ run on the same shocks", font_size=18, color=RULE),
            label(rf"$R^2$: \ {K['r2'][1]:.6f} and {K['r2'][0]:.6f}", font_size=18, color=WHITE),
            label(rf"the rule's drift over \\ 1,000 quarters: \ at most {K['dh_max']:.2f}\%".replace(
                "1,000", "1{,}000"), font_size=18, color=RULE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "How good is a forecast that uses only the mean? <bookmark mark='a'/> The white line is capital in the "
            "simulated economy, with every household's choices in it; the grey bands are bad times. <bookmark "
            "mark='b'/> The usual measure of fit is the regression's R-squared, and it is "
            f"{K['r2'][1]:.6f} in good times and {K['r2'][0]:.6f} in bad: almost perfect. <bookmark mark='c'/> "
            "Wouter den Haan pointed out that R-squared flatters a rule that is only ever asked one quarter "
            "ahead. A stricter test feeds the rule nothing but the shocks and lets it run for a thousand quarters "
            "on its own. That is the gold line. <bookmark mark='d'/> It never drifts more than "
            f"{K['dh_max']:.2f} percent from the real thing. Approximate aggregation: the mean is nearly enough."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(sh), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(act), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(rule), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def why(self):
        K = load("ks")
        a = np.array(K["a"])
        ap = np.array(K["ap_mid"])
        dist = np.array(K["dist"])
        ax = plane([0, 150], [0, 150], center=LEFT * 2.0 + DOWN * 0.3, x_length=5.6, y_length=4.8,
                   xticks=[0, 50, 100, 150], yticks=[0, 50, 100, 150], xlabel=r"wealth this quarter",
                   ylabel=r"wealth next quarter", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        rule = path(ax, a, np.minimum(ap, 150), MANY, 3.0, xr=(0, 150))
        cdf = np.cumsum(dist * a) / np.sum(dist * a)
        mass = VGroup()
        for i in range(0, len(a) - 1):
            if a[i] > 150:
                break
            h = dist[i] / (a[i + 1] - a[i]) * 400
            p0, p1 = ax.ax.c2p(a[i], 0), ax.ax.c2p(a[i + 1], min(h, 40))
            mass.add(Rectangle(width=max(p1[0] - p0[0], 0.01), height=max(p1[1] - p0[1], 0.0), stroke_width=0,
                               fill_color=DIST, fill_opacity=0.5).move_to((p0 + p1) / 2))
        del cdf
        side = VGroup(
            label(r"green: \ an employed household's \\ saving rule, \ in normal times", font_size=18, color=MANY),
            label(r"purple: \ where the households are", font_size=18, color=DIST),
            label(r"above the poorest, \ the rule is \\ almost a straight line", font_size=19, color=WHITE),
            label(rf"the richer half own {100 * K['rich_half_share']:.0f}\% \\ of the capital", font_size=19,
                  color=RICH),
            label(r"so moving wealth among them \\ barely changes total saving:\\ Gorman, \ almost", font_size=19,
                  color=E.ACCENT),
            label(r"it fails where spending, \ not capital, \\ is what matters, \ and the poor \\ do the spending",
                  font_size=18, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Here is the saving rule of an employed household, next "
            "quarter's wealth against this quarter's, <bookmark mark='b'/> with the population drawn beneath it. "
            "<bookmark mark='c'/> Except near the bottom, the rule is almost a straight line. <bookmark mark='d'/> "
            f"And the richer half of households own {100 * K['rich_half_share']:.0f} percent of the capital. "
            "<bookmark mark='e'/> Where the rules are straight lines with a common slope, shifting wealth between "
            "households does not change their total saving: Gorman's condition from chapter one, holding almost "
            "exactly for the households who matter for capital. The poor have curved rules, but they own too "
            "little to move the total. <bookmark mark='f'/> That is also when it fails: when the question is about "
            "spending rather than capital, the poor and their curved rules are exactly the households who matter."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(rule), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(mass), FadeIn(side[1]))
            for mk, s_ in zip("cdef", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=UP * 0.1))
        self.clear_scene()
