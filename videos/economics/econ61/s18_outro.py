from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403

PROBLEMS = [
    r"Surge: \ with requests $340\,e^{-0.9(m-1)}$ and drivers $70 + 45(m-1)$ at multiplier $m$, \ find the "
    r"clearing multiplier, \ and show that rides rise when the fare does.",
    r"Surplus: \ if a rider books with probability $e^{-p/\mu}$, \ show that consumer surplus per trip is $\mu$, \ "
    r"and find surplus per dollar at $\mu = 25$, \ $p = 15$.",
    r"Quality scores: \ bids 4, \ 3, \ 2.5, \ 1 and qualities 0.5, \ 1, \ 0.7, \ 0.9 for three slots: \ rank by "
    r"bid $\times$ quality and find each winner's price per click.",
    r"Interference: \ 300 riders, \ 170 drivers; \ riders want a ride with probability 0.5, \ 0.7 with a discount. "
    r"\ Half get it: \ what does the A/B test estimate, \ and what is the true effect?",
    r"CUPED: \ show that subtracting $\theta(\bar X_B - \bar X_A)$ with $\theta = \mathrm{Cov}(X, Y)/\mathrm{Var}(X)$ "
    r"cuts the variance of the difference by the factor $1 - \rho^2$.",
    r"$\bigstar$ \ The commission: \ the platform maximizes $c\,F\,T(c)$ for fare $F$ and trips $T(c)$. \ Show "
    r"that at its best commission $d\ln T/d\ln c = -1$, \ and explain why drivers' waits enter $T'(c)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"They design markets that a company owns: \ the commission, \ the surge, \ the ranking, \ "
                          r"the ratings, \ the ad auction. \ They measure what those choices do, \ mostly by "
                          r"experiment, \ and they catch the ways experiments mislead: \ peeking, \ interference, \ "
                          r"effects that change with time. \ And they ask the questions engineers do not: \ is it "
                          r"caused, \ what does the other side do, \ and whose welfare is it?", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        riders = VGroup(*[Dot(radius=0.08, color=RIDER) for _ in range(5)]).arrange(DOWN, buff=0.15)
        drivers = VGroup(*[Dot(radius=0.08, color=DRIVER) for _ in range(5)]).arrange(DOWN, buff=0.15)
        hub = Circle(radius=0.35, color=PLAT, stroke_width=3).set_fill(PLAT, opacity=0.25)
        net = VGroup(riders, hub, drivers).arrange(RIGHT, buff=1.2).next_to(a, DOWN, buff=0.45)
        lines = VGroup(*[Line(d.get_center(), hub.get_center(), stroke_width=1.2, color=GREY_B)
                         for d in list(riders) + list(drivers)])
        with self.voiceover(
            "So: what do the economists inside technology companies do? <bookmark mark='a'/> They design markets "
            "that a company owns: the commission, the surge, the ranking, the ratings, the ad auction. They "
            "measure what those choices do, mostly by experiment, and they catch the ways experiments mislead: "
            "peeking, interference, effects that change with time. And they ask the questions engineers do not: "
            "is it caused, what does the other side do, and whose welfare is it?"
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(net), Create(lines), run_time=2.0)
        self.clear_scene()

    def recap(self):
        N, C, S, Rk, R, G, A, P, X, U, L, F = (load(x) for x in (
            "night", "commission", "surplus", "ranking", "reputation", "gsp", "ads", "peeking", "switchback",
            "uplift", "longterm", "flex"))
        items = [
            (rf"surge off: \ about {100 * N['off']['rate_peak']:.0f}\% of requests filled at the peak; \ on: \ all",
             SURGE),
            (rf"Play it: \ the platform's best commission, \ {100 * C['best_c']:.0f}\%; \ riders and drivers lose "
             r"more than it gains", PLAT),
            (rf"surge's surplus: \ \${S['cs_per_dollar']:.2f} per dollar on the Island, \ about \$1.60 for UberX",
             RIDER),
            (rf"ranking: \ position alone gives the top slot {Rk['top_vs_fifth']:.1f} times the fifth's attention",
             SELL),
            (rf"reputation: \ percent positive, \ median {100 * R['pp_median']:.0f}\%; \ count the silence", DRIVER),
            (rf"quality scores: \ more clicks and more revenue, \ \${G['plain']['quality']['revenue']:.3f} against "
             rf"\${G['plain']['bid only']['revenue']:.3f}", AD),
            (rf"advertising: \ the dashboard +{100 * A['attributed_roi']:,.0f}\%, \ the truth "
             rf"{100 * A['true_roi']:.0f}\%".replace(",", "{,}").replace("-", "{-}"), AD),
            (rf"peeking: \ {100 * P['ever']:.0f}\% of A/A tests `win' at some daily look", TEST),
            (rf"interference: \ the user test +{100 * X['user']:.1f}, \ the truth +{100 * X['truth']:.1f}", TEST),
            (r"uplift: \ coupons to the likeliest buyers do worse than at random", RIDER),
            (rf"surrogates: \ +{100 * L['short']:.0f}\% in a month, \ {100 * L['truth']:.1f}\% over a year"
             .replace("-", "{-}"), GAIN),
            (rf"flexibility: \ worth {F['ratio']:.1f} times a fixed shift's surplus", DRIVER),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 61, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del U
        with self.voiceover(
            "Part sixty-one in twelve lines. <bookmark mark='r1'/> A price that moves clears the market on the "
            "busiest night. <bookmark mark='r2'/> The platform's best commission is not the market's. <bookmark "
            "mark='r3'/> Surge's random prices reveal riders' surplus. <bookmark mark='r4'/> Position has value of "
            "its own, apart from relevance. <bookmark mark='r5'/> Ratings inflate; count the silence. <bookmark "
            "mark='r6'/> Quality scores align revenue with relevance. <bookmark mark='r7'/> The sales that come "
            "through an ad are not the sales it causes. <bookmark mark='r8'/> Peeking manufactures winners. "
            "<bookmark mark='r9'/> Shared drivers inflate an A/B test. <bookmark mark='r10'/> Target the effect, "
            "not the outcome. <bookmark mark='r11'/> The short run can point the wrong way. <bookmark mark='r12'/> "
            "And flexibility has a value that a job's protections must be weighed against."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems: the surge that clears the market; consumer surplus under an exponential demand curve; "
            "a quality-scored auction; an A/B test with shared drivers; the variance that CUPED removes; and a "
            "starred problem on the platform's commission. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Ron Kohavi, \ Diane Tang and Ya Xu, \emph{Trustworthy Online Controlled Experiments} (2020)",
             r"David Evans and Richard Schmalensee, \emph{Matchmakers: \ The New Economics of Multisided Platforms} "
             r"(2016)"],
            [r"Rochet and Tirole (2003); \ Edelman, \ Ostrovsky and Schwarz (2007); \ Varian (2007); \ Ostrovsky and "
             r"Schwarz (2009)",
             r"Blake, \ Nosko and Tadelis (2015); \ Lewis and Rao (2015); \ Hall, \ Kendrick and Nosko (2015); \ "
             r"Tadelis (2016)",
             r"Cohen et al.\ (2016); \ Einav, \ Farronato and Levin (2016); \ Chen et al.\ (2019); \ Athey and Luca "
             r"(2019)",
             r"Athey, \ Chetty, \ Imbens and Kang (2019); \ Brynjolfsson, \ Collis and Eggers (2019); \ Fradkin, \ "
             r"Grewal and Holtz (2021); \ Bajari et al.\ (2023)"])
        with self.voiceover(
            "The reading: Kohavi, Tang and Xu on online experiments; Evans and Schmalensee on multisided "
            "platforms. Then the papers, from Rochet and Tirole's two-sided markets to Bajari and his colleagues "
            "on experiments in marketplaces."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2008, r"Mumbai's textile mills", r"free management consulting, \ offered to a randomly "
                          r"chosen group of plants: \ clean floors, \ recorded defects, \ counted stock",
                          color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 62 \ $\cdot$ \ Act XI, \ Economics at Work", font_size=30, color=GREY_B),
                     label(r"Inside the Firm", font_size=46),
                     label(r"why are some firms so much better run than others, \ and can it be taught?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the platform's market to the firm's own workings", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"management practices", GAIN), (r"personnel economics", DRIVER),
                                         (r"executive pay", AD), (r"governance", PLAT))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from the platform's market to the firm's own workings. <bookmark mark='a'/> Near Mumbai, "
            "economists offered free management consulting to a randomly chosen group of large textile plants: "
            "clean floors, recorded defects, stock that is counted. Practices that had been free to adopt all "
            "along. <bookmark mark='b'/> Management, personnel economics, executive pay, governance. <bookmark "
            "mark='c'/> Part sixty-two: inside the firm."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
