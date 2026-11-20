from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403

PROBLEMS = [
    r"The gym: \ a monthly fee of \$70 and 4.3 visits a month. \ What does a visit cost? \ How many visits a month "
    r"would make the fee cheaper than a pass at \$10 a visit?",
    r"Present bias: \ with $\beta$ = 0.7 and $\delta$ = 1, \ compare \$100 today with \$110 tomorrow, \ and the same "
    r"pair a year away. \ Below what $\beta$ does today's \$100 win?",
    r"O'Donoghue and Rabin: \ costs 3, \ 5, \ 8, \ 13 over four weeks. \ Find when the naif and the sophisticate act "
    r"with $\beta$ = 1/2, \ then with $\beta$ = 0.7.",
    r"The mug: \ owner and buyer both value a mug at \$4; \ losses over goods count 2$\times$, \ over money "
    r"1$\times$. \ Find the ask and the bid. \ Can they trade?",
    r"Left digits: \ within a band, \ price falls \$40 per 1,000 miles; \ at each 10,000 it drops a further \$170. "
    r"\ Estimate $\theta$.",
    r"Commitment: \ 30\% of those offered take the account, \ and the offer raises average savings by 11. \ What is "
    r"the effect on a taker, \ and what does it assume?",
    r"Fehr and Schmidt: \ a responder with $\alpha$ = 1 \ and a proposer with $\beta$ = 0.6. \ Find the smallest "
    r"acceptable share and the proposer's offer.",
    r"$\bigstar$ \ Selection: \ estimates are published with probability 1 if $z \ge 1.96$, \ $\gamma$ otherwise. "
    r"\ Write the density of a published estimate, \ and show the published mean exceeds $\mu$ when $\gamma < 1$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Choices become predictable in new ways: \ people overweight now, \ code outcomes as gains "
                          r"and losses, \ attend to little, \ and care about others. \ Markets cure some of this and "
                          r"feed on the rest, \ and welfare must be read where choices agree.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1959, 2026.5], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, GYM, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what changes in economics when people are not the agents of Part five? <bookmark mark='a'/> "
            "Choices become predictable in new ways. People overweight the present, judge outcomes as gains and "
            "losses from a reference point, attend to a few things, and care about others. Markets cure some of "
            "this, where people learn fast, and feed on the rest. And welfare can no longer be read from any single "
            "choice, only from where choices agree."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        G, M, Mr, Gf, Co, S, N, Ca, U, Nu, Fc, K = (load(x) for x in (
            "gym", "mugs", "marathon", "golf", "condos", "seed", "enrol", "cars", "social", "nudges", "forecast",
            "contract"))
        T = tables.NUDGES_2022.data
        items = [
            (rf"the gym: \ forecast {G['forecast']:.1f} visits, \ made {G['visits']:.1f}: \ "
             rf"\${G['price_per_visit']:.2f} a visit", GYM),
            (rf"the mug: \ asks {M['loss']['ratio']:.1f}$\times$ bids; \ {100 * M['loss']['share_traded']:.0f}\% "
             r"traded, \ not 50\%", SELL),
            (rf"runners bunch under round times; \ golfers try {100 * Gf['within']:.1f} points harder for par", PLAN),
            (rf"sellers' losses: \ bounds {Co['lower']:.2f} and {Co['upper']:.2f} bracket {Co['m']:.1f}", SELL),
            (r"present bias: \ plans reverse; \ naifs procrastinate, \ sophisticates bind themselves", NAIF),
            (rf"the gym's contract: \ visits priced below cost, \ \${K['naif_monopoly']['p']:.2f}", FIRM),
            (rf"commitment: \ {100 * S['take_up']:.0f}\% take a lock; \ effect on takers {S['tot']:.0f}", SOPH),
            (rf"defaults: \ {100 * N['opt_in_naif']['participation'][11]:.0f}\% against "
             rf"{100 * N['auto_naif']['participation'][11]:.0f}\% for naifs after a year", NUDGE),
            (rf"inattention: \ shrouded add-ons; \ left digits, \ $\hat\theta$ = {Ca['theta_hat']:.2f}", BUY),
            (rf"fairness: \ {100 * U['reject_20']:.0f}\% would reject a fifth; \ offers average "
             rf"{100 * U['mean_offer']:.0f}\%", GAIN),
            (rf"nudges at scale: \ {T['academic_effect']} points published, \ {T['unit_effect']} in full; \ "
             rf"corrected {Nu['mle']['mu']:.2f}", HOLD),
            (rf"forecasters: \ each over-reacts ({Fc['diagnostic']['individual']:+.2f}), \ the average under-reacts",
             LOSS),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 45, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del Mr
        with self.voiceover(
            "Part forty-five in twelve lines. <bookmark mark='a'/> Gym members forecast their visits as if they "
            "were Part five's agents, and pay for the difference. Owners ask about twice what buyers bid, and too "
            "few mugs change hands. Runners bunch under round times and golfers try harder for par. Sellers facing "
            "a loss ask more, and two regressions bracket by how much. Present bias makes plans reverse; naifs "
            "put things off, and sophisticates bind themselves. A gym prices visits below cost for present-biased "
            "members. Commitment is demanded, mostly by those who know their bias. Defaults decide for people who "
            "put off deciding. Shrouded fees survive competition, and left digits leave steps in prices. Fairness "
            "rejects low offers and makes proposers generous. Published nudges look six times bigger than nudges in "
            "full, and a model of the filter undoes most of it. And forecasters over-react one by one while their "
            "average under-reacts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The price of a gym visit; a preference reversal; naifs and sophisticates; the mug; "
            "left-digit bias from a step and a slope; the effect on takers of a commitment account; fairness in the "
            "ultimatum game; and a starred derivation of why a filtered literature overstates. Full solutions are in "
            "the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Richard Thaler, \emph{Misbehaving: \ The Making of Behavioral Economics} (2015)",
             r"Daniel Kahneman, \emph{Thinking, \ Fast and Slow} (2011)",
             r"Sanjit Dhami, \emph{The Foundations of Behavioral Economic Analysis} (2016)",
             r"Bernheim, \ DellaVigna and Laibson (eds.), \emph{Handbook of Behavioral Economics} (2018--19)"],
            [r"Kahneman and Tversky (1979); \ Thaler (1980); \ Kahneman, \ Knetsch and Thaler (1990)",
             r"Laibson (1997); \ O'Donoghue and Rabin (1999); \ Fehr and Schmidt (1999); \ Madrian and Shea (2001)",
             r"Genesove and Mayer (2001); \ List (2003); \ Thaler and Benartzi (2004); \ Sims (2003)",
             r"DellaVigna and Malmendier (2004, \ 2006); \ Ashraf, \ Karlan and Yin (2006); \ Gabaix and Laibson "
             r"(2006)",
             r"DellaVigna (2009); \ Bernheim and Rangel (2009); \ Pope and Schweitzer (2011); \ DellaVigna and Linos "
             r"(2022)"])
        with self.voiceover(
            "The reading: Richard Thaler's Misbehaving, a history of the field by one of its founders; Daniel "
            "Kahneman's Thinking, Fast and Slow; Sanjit Dhami's graduate text; and the Handbook of Behavioral "
            "Economics, edited by Douglas Bernheim, Stefano DellaVigna and David Laibson. Then the papers, from "
            "prospect theory to nudges at scale."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2007, r"Cohen and Dupas", r"randomize the price of insecticide-treated bed nets at Kenyan "
                          r"clinics: \ small prices cut take-up sharply, \ and those who paid were no more likely to "
                          r"use "
                          r"a net", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 46 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"Development", font_size=46),
                     label(r"why do the poor stay poor, \ and what actually helps?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from biased choices \ to choices made in poverty", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Next time, the economics of development. <bookmark mark='a'/> A bed net treated with insecticide costs "
            "a few dollars and prevents malaria. Should it be given away, or sold cheaply so that only people who "
            "value it take one? Jessica Cohen and Pascaline Dupas randomized the price at clinics in Kenya. Even "
            "small prices cut take-up sharply, and those who paid were no more likely to use their nets. "
            "<bookmark mark='b'/> Part forty-six asks why the poor stay poor, and what actually helps."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
