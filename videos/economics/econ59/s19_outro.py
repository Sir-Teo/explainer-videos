from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403

PROBLEMS = [
    r"Critical diversion: \ for two symmetric firms with linear demand, \ each pricing to maximize profit, \ show "
    r"that a joint rise of $X$ pays iff $D > X/(X + M)$. \ Evaluate it for $M = 0.4$ and $X = 5\%$.",
    r"A firm with 30\% of a market buys one with 4\%. \ Find $\Delta$HHI, \ and say which of the 1982, \ 2010 and "
    r"2023 presumptions it triggers when the post-merger HHI is 1,600.".replace(",", "{,}"),
    r"Pricing pressure: \ from the merged firm's first-order condition, \ show that the merger acts like a rise of "
    r"$D_{AB}(p_B - c_B)$ in $A$'s marginal cost; \ find the GUPPI when $D_{AB} = 0.3$, \ $p_B - c_B = \$20$, \ "
    r"$p_A = \$100$.",
    r"Pass-through: \ show that a monopolist with linear demand passes on half of a cost change, \ and one with "
    r"constant elasticity $\varepsilon > 1$ passes on $\varepsilon/(\varepsilon - 1)$ of it.",
    r"A cartel's price is \$120 for 24 months against a but-for price of \$100, \ on sales of 50,000 units a month. "
    r"\ Find the overcharge, \ the damages and the American treble damages.".replace(",", "{,}"),
    r"$\bigstar$ \ The bargaining model: \ with weight $w$, \ show that the fee rises by $w \times$ departure "
    r"$\times$ share to the integrated rival $\times$ its margin, \ and find the departure rate at which the "
    r"rivals' extra costs equal the integrated distributor's saving.",
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
        a = wrapped_label(r"As a prediction, \ argued before someone who is not an economist. \ The law asks whether "
                          r"competition may be substantially lessened; \ economics answers with a market, \ "
                          r"diversion, \ margins, \ pass-through and a model. \ What survives cross-examination is "
                          r"evidence that does not depend on one specification, \ one curve or one input, \ and "
                          r"predictions that retrospectives later confirm.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        T = load("towns")
        logo = island_map(T, width=4.4, height=2.2, radius=0.045).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how is economics used to decide a merger, and what survives cross-examination? <bookmark mark='a'/> "
            "It is used as a prediction, argued before someone who is not an economist. The law asks whether "
            "competition may be substantially lessened, and economics answers with a market, diversion ratios, "
            "margins, pass-through and a model. What survives cross-examination is evidence that does not hang on "
            "one specification, one demand curve or one input, and predictions that retrospectives later confirm."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo.coast), LaggedStart(*[FadeIn(d) for d in logo.dots], lag_ratio=0.05),
                      run_time=6.0)
        self.clear_scene()

    def recap(self):
        T, P, Mk, U, F, A, Ef, V, C, R, W, L = (load(x) for x in (
            "towns", "playit", "market", "upp", "forms", "agency", "efficiency", "vertical", "cartel", "retro",
            "witness", "labour"))
        pairs = P["pairs"]
        G = load("regression")
        items = [
            (r"`may be substantially to lessen competition': \ a prediction, \ argued in court", GOV),
            (rf"the map: \ Alder alone charges {T['lone_premium']:.0f}\% more, \ but rents differ too", ALDER),
            (rf"Play it: \ one market when diversion beats $X/(X + M)$: \ {100 * pairs[0]['D']:.0f}\% $>$ "
             rf"{100 * pairs[0]['critical']:.0f}\%", BIRCH),
            (r"the market: \ the smallest set a monopolist could raise prices in; \ beware cellophane", CEDAR),
            (r"the HHI's lines moved in 2010 and back in 2023; \ the economics did not", GOV),
            (rf"pricing pressure: \ Alder's GUPPI {100 * U['products']['Alder']['guppi']:.1f}\%, \ simulated "
             rf"+{100 * U['simulation']['dp'][0]:.1f}\%", SIM),
            (rf"the curve decides: \ one data set, \ +{F['rise'][0]:.1f}\% to +{F['rise'][3]:.1f}\%", CARTEL),
            (rf"pass-through: \ {100 * Ef['pass_through']['merged'][0]:.0f}\% merged, \ Staples 15--17\%, \ not "
             r"two-thirds", SAVE),
            (rf"vertical: \ the fee rises \${V['fee_rise']:.2f}; \ the departure rate decides", BIRCH),
            (rf"the cartel: \ {100 * C['estimate']:.1f}\% overcharge, \ damages trebled", CARTEL),
            (rf"in court: \ every specification {G['mv_min']:.0f}--{G['mv_max']:.0f}\%; \ the harm sits where Cedar is "
             r"absent", DEF),
            (rf"retrospective: \ +{R['estimate']:.1f}\%; \ the plain logit said +{A['mean_predicted']:.1f}\%", WORK),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 59, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del Mk, W, L
        with self.voiceover(
            "Part fifty-nine in twelve lines. <bookmark mark='r1'/> The law asks for a prediction. <bookmark "
            "mark='r2'/> Raw price maps mix competition with costs. <bookmark mark='r3'/> A pair is one market when "
            "diversion beats X over X plus M, and high margins make markets narrow. <bookmark mark='r4'/> The "
            "market is the smallest set a monopolist could raise prices in, tested at prices not already raised. "
            "<bookmark mark='r5'/> The guidelines' lines moved; the economics did not. <bookmark mark='r6'/> "
            "Pricing pressure is diversion times the partner's margin. <bookmark mark='r7'/> The shape of demand "
            "can triple a simulated price rise. <bookmark mark='r8'/> Merged firms pass on less of a saving than "
            "independent ones. <bookmark mark='r9'/> In a vertical merger, the bargaining model's most sensitive "
            "input decides. <bookmark mark='r10'/> Overcharges come from before-during-after regressions. "
            "<bookmark mark='r11'/> A regression in court must survive every reasonable alternative. <bookmark "
            "mark='r12'/> And retrospectives score the tools."
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
            "The problems: the critical diversion, derived; a merger against three sets of guidelines; pricing "
            "pressure from the first-order condition; pass-through under two demand curves; a cartel's damages; "
            "and a starred problem on the vertical bargaining model. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Peter Davis and Eliana Garc\'es, \emph{Quantitative Techniques for Competition and Antitrust "
             r"Analysis} (2010)",
             r"John Kwoka, \emph{Mergers, Merger Control, and Remedies} (2015)",
             r"The U.S. Merger Guidelines (2010, \ 2023); \ the European Commission's horizontal merger guidelines "
             r"(2004)"],
            [r"Harris and Simons (1989); \ Werden (1996); \ Crooke, \ Froeb, \ Tschantz and Werden (1999)",
             r"Katz and Shapiro (2003); \ Ashenfelter et al.\ (2006); \ Abrantes-Metz et al.\ (2006); \ Whinston "
             r"(2007)",
             r"Farrell and Shapiro (2010); \ Ashenfelter and Hosken (2010); \ Cooper et al.\ (2019)",
             r"Prager and Schmitt (2021); \ Shapiro (2021) on AT\&T; \ Krueger and Ashenfelter (2022); \ "
             r"Brot-Goldberg et al.\ (2024)"])
        with self.voiceover(
            "The reading: Davis and Garcés's book of quantitative techniques, the working manual of the trade; "
            "Kwoka on mergers and remedies; and the guidelines themselves, American and European. Then the papers, "
            "from Harris and Simons's critical loss to the hospital studies."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1985, r"American Airlines against People Express", r"a no-frills airline undercuts "
                          r"everyone; \ American answers with software: \ sell the seats that would fly empty at the "
                          r"low fare, \ and protect the rest for late bookers", color=E.ACCENT, width=10.4,
                          font_size=23)
        nxt = VGroup(label(r"Next: \ Part 60 \ $\cdot$ \ Act XI, \ Economics at Work", font_size=30, color=GREY_B),
                     label(r"The Price", font_size=46),
                     label(r"how do firms really set prices?", font_size=24, color=E.ACCENT)).arrange(DOWN,
                                                                                                    buff=0.22)
        head = label(r"from judging prices in court to setting them", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"willingness to pay", ALDER), (r"price experiments", SIM),
                                         (r"revenue management", BIRCH), (r"dynamic pricing", CEDAR))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from judging prices in court to setting them. <bookmark mark='a'/> In 1985 People Express, "
            "a no-frills airline, was undercutting everyone, and American Airlines could not match its fares on "
            "every seat. American's answer was software: sell the seats that would have flown empty at the low "
            "fare, and protect the rest for travellers who book late. <bookmark mark='b'/> Measuring willingness to "
            "pay, price experiments, revenue management and dynamic pricing. <bookmark mark='c'/> Part sixty: the "
            "price."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
