from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403

PROBLEMS = [
    r"Minsky: \ a borrower has cash flow 1 and debt 12 due over 20 years. \ At what interest rates is it hedge, \ "
    r"speculative, \ Ponzi?",
    r"Debt deflation: \ debt is 1 year of income; \ prices fall 10\% a year, \ real income 5\%, \ and 5\% of the debt "
    r"is repaid each year. \ Find the ratio after four years.",
    r"Costly verification: \ show that with $\omega$ lognormal of mean 1, \ $G(\bar\omega) = \Phi(z - \sigma)$ where "
    r"$z = (\ln \bar\omega + \sigma^2/2)/\sigma$.",
    r"Kiyotaki and Moore: \ derive the steady state $u^* = a$, \ $q^* = R a/(R-1)$, \ and the persistence "
    r"$k_t/k^* = (k_{t-1}/k^*)^{\eta/(1+\eta)}$.",
    r"Leverage: \ with beliefs uniform on $[0, 1]$ and payoffs 1 or $d$, \ solve for the price with and without "
    r"borrowing; \ evaluate at $d = 0.2$.",
    r"Households: \ a house worth 100 with a mortgage of 80 loses 20\%. \ Compute the owner's loss as a share of "
    r"equity; \ repeat with a mortgage of 50.",
    r"Prediction: \ a test flags 20\% of years, \ and catches 60\% of crises when the base rate is 4\%. \ What share "
    r"of flagged years are followed by a crisis?",
    r"$\bigstar$ \ Original sin: \ a firm has assets worth 100 baht and owes \$2, \ at 25 baht per dollar. \ At "
    r"what exchange rate is its equity wiped out?",
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
        a = wrapped_label(r"Because finance amplifies: \ debt fixed in money, \ net worth that sets the cost of "
                          r"borrowing, \ collateral whose price depends on who can borrow, \ and leverage that "
                          r"rises in good times and vanishes in bad turn small losses into large ones. \ It is hard "
                          r"to see coming because the warning, \ a credit boom, \ is visible but noisy: \ it raises "
                          r"the odds several times over, \ yet most booms end quietly, \ and the timing is hard to "
                          r"call.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1870, 2020], [0, 120], x_length=4.2, y_length=1.3)
        logo = path(mini, F["years"], F["median"], CREDIT, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why do financial systems blow up, and why is it so hard to see it coming? <bookmark mark='a'/> "
            "Because finance amplifies. Debt fixed in money, net worth that sets the cost of borrowing, collateral "
            "whose price depends on who can borrow against it, and leverage that rises in good times and vanishes "
            "in bad ones turn small losses into large ones. And it is hard to see coming because the warning, a "
            "credit boom, is visible but noisy: it raises the odds of a crisis several times over, yet most booms "
            "end quietly, and the timing is hard to call."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        B, M, F, G, K, L, GF, C, P, R, FI, E_ = (load(x) for x in ("booms", "minsky", "fisher", "bgg", "km",
                                                                    "leverage", "gfc", "counties", "panel",
                                                                    "recessions", "fight", "ccyb"))
        items = [
            (rf"Play it: \ {B['crises']} of the 8 biggest postwar credit booms ended in crises", CRISIS),
            (rf"Minsky: \ the same debts, \ a doubled rate: \ {100 * M['ponzi'][-1]:.0f}\% Ponzi borrowers", HOUSE),
            (rf"Fisher: \ US loans $-{F['loans_fall']:.0f}\%$, \ yet loans to GDP {F['ratio29']:.0f}\% $\to$ "
             rf"{F['ratio32']:.0f}\%", CREDIT),
            (rf"the accelerator: \ net worth $-10\%$, \ investment {G['K_fall']:.1f}\%", RATE),
            (rf"collateral: \ a 1\% shock, \ farmers' land $-{K['dynamic']:.1f}\%$", HOUSE),
            (rf"leverage: \ price {L['cycle']['p0']:.2f} $\to$ {L['cycle']['pD']:.2f}, \ margins "
             rf"{100 * L['cycle']['margin0']:.0f}\% $\to$ {100 * L['cycle']['marginD']:.0f}\%", CRISIS),
            (rf"2008: \ house prices $-{GF['cs_fall']:.0f}\%$; \ the Fed's assets \${GF['wal_before']:.1f} $\to$ "
             rf"\${GF['wal_after']:.1f} trillion", BANK),
            (rf"households: \ {100 * C['by_quintile'][0]['mpc']:.0f} to {100 * C['by_quintile'][-1]['mpc']:.0f} "
             r"cents per dollar, \ rising with leverage", OUTPUT),
            (rf"history: \ crises within three years after the fastest credit growth "
             rf"{100 * P['odds']['by_quintile'][-1]:.0f}\%, \ with house prices too {100 * P['odds']['both']:.0f}\%",
             CREDIT),
            (rf"prediction: \ AUC {P['real_loans']['auc_in']:.2f} in sample, \ {P['real_loans']['auc_oos']:.2f} out "
             r"of sample", HOLD),
            (rf"financial recessions: \ {R['gap5_post']:.1f} points deeper after five years", CRISIS),
            (rf"fighting: \ swap lines \${FI['peak08']:.0f}bn (2008), \ \${FI['peak20']:.0f}bn (2020); \ Spain's "
             rf"buffer full from {E_['ESP']['first_full']}", CB),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 33, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-three in twelve lines. <bookmark mark='a'/> Most of the biggest credit booms ended in "
            "crises. Minsky's borrowers turned speculative and then Ponzi as the boom went on and the rate rose. "
            "Falling prices kept America's debts as heavy in 1932 as in 1929. A loss of net worth raises the cost "
            "of borrowing and cuts investment. Land that is both an input and collateral multiplies a small shock "
            "several times. Leverage changes whose opinion sets prices, so bad news moves them far more than it "
            "should. In 2008 the losses sat in a banking system without deposit insurance, and it ran. Indebted "
            "households cut spending most. Across a hundred and fifty years, credit booms raise the odds of a "
            "crisis several times over, but forecasting the date out of sample is hard. Financial recessions are "
            "deeper and longer. And the playbook for fighting them, written in 2008, was run in weeks in 2020."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Minsky's three borrowers; debt deflation; the algebra of costly verification; the "
            "steady state of the collateral model; the leverage cycle's prices; a levered household's loss; the "
            "arithmetic of predicting rare events; and a starred problem on original sin. Full solutions are in the "
            "part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Charles Kindleberger and Robert Aliber, \emph{Manias, \ Panics, \ and Crashes} (7th ed., 2015)",
             r"Atif Mian and Amir Sufi, \emph{House of Debt} (2014)",
             r"Carmen Reinhart and Kenneth Rogoff, \emph{This Time Is Different} (2009)",
             r"Adam Tooze, \emph{Crashed} (2018); \ Ben Bernanke, \ Timothy Geithner and Henry Paulson, "
             r"\emph{Firefighting} (2019)"],
            [r"Fisher (1933); \ Minsky (1986); \ Bernanke (1983); \ Townsend (1979)",
             r"Kiyotaki and Moore (1997); \ Bernanke, \ Gertler and Gilchrist (1999); \ Geanakoplos (2010)",
             r"Schularick and Taylor (2012); \ Jord\`a, \ Schularick and Taylor (2013, 2017); \ Greenwood et al. "
             r"(2022)",
             r"Gorton and Metrick (2012); \ Brunnermeier and Pedersen (2009); \ Brunnermeier and Sannikov (2014)",
             r"Mian, \ Rao and Sufi (2013); \ Calvo (1998); \ Rajan (2005)"])
        with self.voiceover(
            "The reading: Kindleberger's history of manias and panics; Mian and Sufi on household debt; Reinhart "
            "and Rogoff's eight centuries of crises; and, on 2008 itself, Adam Tooze's history and the account of "
            "the three men who fought it. Then the papers, from Fisher to Brunnermeier and Sannikov."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1992, r"the Bank of England", r"Wednesday 16 September 1992: \ the rate goes from 10\% to "
                          r"12\% in the morning, \ 15\% is announced in the afternoon, \ and by evening the pound has "
                          r"left the Exchange Rate Mechanism", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 34 \ $\cdot$ \ Act VII, \ The World Economy", font_size=30, color=GREY_B),
                     label(r"The Open Economy", font_size=46),
                     label(r"what sets the price of one money in terms of another, \ and what can a country not "
                           r"have at once?", font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"Act VI ends: \ money and the cycle; \ next: \ the world", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "That ends Act six, on money and the cycle. Act seven opens the economy to the world. "
            "<bookmark mark='a'/> On Wednesday the sixteenth of September 1992, the Bank of England raised its rate "
            "from ten percent to twelve in the morning, announced fifteen in the afternoon, spent its reserves by "
            "the billion, and by evening Britain had left the European Exchange Rate Mechanism. The speculators did "
            "not cause the contradiction; they found it. <bookmark mark='b'/> Part thirty-four: the open economy. "
            "What sets the price of one money in terms of another, and what can a country not have at once?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
