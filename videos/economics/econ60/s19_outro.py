from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403

PROBLEMS = [
    r"Littlewood: \ derive the rule $P(D_H > y) \le p_L/p_H$ for the last protected seat, \ and find $y$ for "
    r"$p_H = 400$, \ $p_L = 150$, \ $D_H \sim$ Poisson(30).",
    r"Markups: \ show that a profit-maximizing price satisfies $(p - c)/p = 1/\varepsilon$; \ with "
    r"$\varepsilon = 2.6$, "
    r"\ what share of the best profit does a 50\% markup earn?",
    r"Overbooking: \ with 100 seats, \ show-up probability 0.9, \ a \$200 fare and a \$600 bump cost, \ write the "
    r"condition for selling the $b$-th ticket and find the best $b$.",
    r"Bundles: \ with $N$ goods valued uniformly on $[0, 1]$, \ explain why the bundle's revenue per good tends to "
    r"$1/2$, \ and what happens to deadweight loss.",
    r"Interference: \ if rooms sell out under both the old price and the discount, \ what does an A/B test "
    r"estimate, \ and what is the true effect of discounting for everyone?",
    r"$\bigstar$ \ One seat left, \ at most one buyer a day with probability $\lambda$, \ values exponential with "
    r"mean $\mu$: \ show that the best fare is $\mu + V_{t+1}$, \ and find the recursion for $V_t$.",
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
        a = wrapped_label(r"Most firms start from cost and a conventional markup, \ which is not as foolish as it "
                          r"looks: \ the profit curve is flat at the top, \ and the elasticity is never known. \ Firms "
                          r"that can learn their demand do better: \ by choices and experiments, \ by fences, \ "
                          r"versions and bundles, \ and where capacity is fixed and time runs out, \ by revenue "
                          r"management. \ The theory is used most where the stakes are highest and the data richest.",
                          11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        D = load("dynamic")
        pol = np.array(D["policy"])
        cells = VGroup()
        for t in range(0, pol.shape[0], 2):
            for j in range(1, pol.shape[1], 2):
                v = float(np.clip((pol[t, j] - 80) / 240, 0, 1))
                cells.add(Square(side_length=0.12, stroke_width=0, fill_opacity=0.9,
                                 fill_color=interpolate_color(ManimColor(LEIS), ManimColor(COST), v)).move_to(
                    [t * 0.07, j * 0.07, 0]))
        cells.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how do firms actually set prices, and how much of the theory do they use? <bookmark mark='a'/> Most "
            "start from cost and a conventional markup, which is less foolish than it looks: the profit curve is "
            "flat at the top, and the elasticity is never known exactly. Firms that can learn their demand do "
            "better, by choices and experiments, by fences, versions and bundles, and, where capacity is fixed and "
            "time runs out, by revenue management. The theory is used most where the stakes are highest and the "
            "data richest."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), run_time=6.0)
        self.clear_scene()

    def recap(self):
        C, J, X, P, L, M, B, H, Ch, Pt, Bd = (load(x) for x in (
            "costplus", "conjoint", "experiment", "playit", "rm", "menu", "bundle", "hilo", "chain", "passthrough",
            "bandit"))
        Rr = P["rules"]
        items = [
            (rf"cost-plus survives: \ a fixed markup earned {100 * C['fixed']:.1f}\% of the best", FIRM),
            (rf"conjoint: \ wifi worth \${J['wtp']['wifi']:.1f}, \ legroom \${J['wtp']['legroom']:.1f}", TEST),
            (rf"interference: \ the A/B test +{100 * X['naive']:.1f} points, \ the truth +{100 * X['global']:.1f}",
             COST),
            (rf"Play it: \ start low and raise, \ \${Rr['start low, raise']['mean']:,.0f} a flight"
             .replace(",", "{,}"), LEIS),
            (rf"Littlewood: \ protect {L['littlewood']['y_star']} seats while P(sell high) $> p_L/p_H$", BUS),
            (rf"overbooking: \ {L['overbooking']['best']} tickets for 100 seats", AIR),
            (r"dynamic programming: \ a fare for every day and every seat left", OPT),
            (rf"versions: \ three earn {M['menu']['profit']:.3f}, \ one {M['menu']['profit_one']:.3f}", AIR),
            (rf"bundles: \ {B['rows'][-1]['revenue_per_good']:.2f} per good in a bundle of 100, \ against 0.25", OPT),
            (r"reference prices: \ high-low beats everyday low when shoppers value a deal", BUS),
            (rf"food pass-through: \ {Pt['cum'][-1]:.2f} in quiet years; \ more in 2021--23", PPI),
            (r"Thompson sampling: \ learn the price while charging it", LEIS),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 60, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del H, Ch, Bd
        with self.voiceover(
            "Part sixty in twelve lines. <bookmark mark='r1'/> Cost-plus survives because the top is flat and the "
            "elasticity unknown. <bookmark mark='r2'/> Conjoint choices reveal what features are worth. <bookmark "
            "mark='r3'/> Experiments in markets with scarce goods double-count. <bookmark mark='r4'/> In the Play it, "
            "start low and raise. <bookmark mark='r5'/> Littlewood protects a seat while it is likely to sell high. "
            "<bookmark mark='r6'/> Overbooking trades fares against bumps. <bookmark mark='r7'/> Dynamic programming "
            "gives a fare for every state. <bookmark mark='r8'/> Versions are damaged on purpose. <bookmark "
            "mark='r9'/> Large bundles capture nearly all the value. <bookmark mark='r10'/> The regular price is "
            "the reference that makes a sale. <bookmark mark='r11'/> Shared cost shocks pass through more. "
            "<bookmark mark='r12'/> And prices can be learned while they are set."
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
            "The problems: Littlewood's rule, derived and applied; the markup rule and the flat top; the overbooking "
            "condition; why big bundles work; what an A/B test measures when everything sells out; and a starred "
            "problem on the last seat. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Kalyan Talluri and Garrett van Ryzin, \emph{The Theory and Practice of Revenue Management} (2004)",
             r"Robert Phillips, \emph{Pricing and Revenue Optimization} (2nd ed., \ 2021)",
             r"Thomas Nagle and Georg M\"uller, \emph{The Strategy and Tactics of Pricing}"],
            [r"Hall and Hitch (1939); \ Becker, \ DeGroot and Marschak (1964); \ Littlewood (1972); \ Mussa and "
             r"Rosen (1978)",
             r"Belobaba (1987); \ Smith, \ Leimkuhler and Darrow (1992); \ Gallego and van Ryzin (1994); \ Deneckere "
             r"and McAfee (1996)",
             r"Blinder et al.\ (1998); \ Bakos and Brynjolfsson (1999); \ Murphy et al.\ (2005); \ Blake and Coey "
             r"(2014)",
             r"DellaVigna and Gentzkow (2019); \ Calvano et al.\ (2020); \ Blake et al.\ (2021); \ Williams (2022)"])
        with self.voiceover(
            "The reading: Talluri and van Ryzin's book on revenue management; Phillips on pricing and revenue "
            "optimization; and Nagle and Müller's practitioner's guide. Then the papers, from Hall and Hitch's "
            "interviews to Williams's airline markets."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2014, r"New Year's Eve, \ New York", r"a software fault switches off a ride-hailing "
                          r"app's surge pricing at the busiest moment of the year; \ requests pile up, \ drivers do "
                          r"not come", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 61 \ $\cdot$ \ Act XI, \ Economics at Work", font_size=30, color=GREY_B),
                     label(r"Economics at the Platforms", font_size=46),
                     label(r"what do the economists inside technology companies do?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from setting one firm's prices to running a marketplace", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"surge pricing", COST), (r"marketplace design", AIR),
                                         (r"experiments at scale", TEST), (r"ranking and search", LEIS))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from one firm's prices to a whole marketplace. <bookmark mark='a'/> On New Year's Eve 2014, a "
            "software fault switched off a ride-hailing app's surge pricing in New York at the busiest moment of the "
            "year. Requests piled up, and drivers did not come. <bookmark mark='b'/> Surge pricing, marketplace "
            "design, experiments at scale, ranking and search. <bookmark mark='c'/> Part sixty-one: economics at the "
            "platforms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
