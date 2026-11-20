from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403

PROBLEMS = [
    r"The corridor: \ with reserve demand $i = f + (c - f)\,\bar\Phi((R - n)/s)$, \ find the reserves that put the "
    r"rate mid-corridor, \ and the rate's slope there.",
    r"The floor: \ show that in a floor system the rate does not change when reserves fall by a small amount, \ and "
    r"that raising the rate on reserves raises it one for one.",
    r"QE in T-accounts: \ the central bank buys 100 of bonds from a household; \ write every balance sheet that "
    r"changes.",
    r"Recursive identification: \ in a two-variable VAR with the rate ordered last, \ show that the shock is the "
    r"residual of the rate on the other variable's innovation.",
    r"The price puzzle: \ if the bank raises $i_t$ on news $n_t$ that raises $\pi_{t+1}$, \ and $n_t$ is left out, "
    r"\ sign the bias in the estimated response of $\pi$.",
    r"Real time: \ fit a log-linear trend to output that grew 4\% a year for 20 years and 2.5\% for the next 6; \ "
    r"find the end-point gap.",
    r"Self-fulfilling yields: \ with default when $r\,b > F$, \ $F \sim N(\mu, \sigma^2)$, \ derive "
    r"$R(r) = (1 + r_f)/(1 - p(r)) - 1$ and count its fixed points.",
    r"$\bigstar$ \ The information effect: \ if a surprise is $s = v + \lambda n$, \ find the bias of the "
    r"instrumented response of output when $n$ raises it.",
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
        a = wrapped_label(r"It sets the price of overnight money, \ by the reserves it supplies or the rate it pays on "
                          r"them, \ and it moves borrowing costs further out by what it promises and what it buys. \ "
                          r"We know what it achieves only where we can find the part of its decisions that is its own: "
                          r"\ the evidence says a tightening lowers output after a year or more and prices later, \ by "
                          r"amounts still argued; \ and a central bank that is believed can sometimes do the most by "
                          r"never having to act.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1954, 2027], [0, 20], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["ff"], RATE, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what does a central bank actually do, and how do we know what it achieves? "
            "<bookmark mark='a'/> It sets the price of overnight money, either by the reserves it supplies or by "
            "the rate it pays on them, and it moves borrowing costs further out by what it promises and what it "
            "buys. We can know what it achieves only where we can find the part of its decisions that is its own. "
            "Where we can, a tightening lowers output after a year or more and prices later, by amounts still "
            "argued. And a central bank that is believed can sometimes do the most by never having to act."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        S, R, P, M, U, Z, Q, RS, D, C = (load(x) for x in ("spreads", "reserves", "playit", "mc", "usvar", "zlb",
                                                           "qe", "rstar", "debt", "called"))
        items = [
            (rf"Draghi's sentence: \ Spain {S['jul12']['ES']:.1f}\% in July 2012, \ {S['jul14']['ES']:.1f}\% two "
             r"years later", E.ACCENT),
            (rf"reserves: \ \${R['reserves_pre']:.0f} billion in 2008, \ a corridor; \ trillions since, \ a floor",
             RES),
            (rf"Play it: \ the gap of 1978, \ {P['gap_rt']:+.1f}\% then, \ {P['gap_today']:+.1f}\% now", OUTPUT),
            (r"transmission: \ five channels, \ long and variable lags; \ markets move first", RATE),
            (r"the problem: \ the bank acts on what it sees; \ the price puzzle", HOLD),
            (rf"four answers on {M['reps']} Islands: \ narrative and clean surprises find the truth", PRICE),
            (rf"the consensus: \ output {U['commod']['ip_trough']['value']:+.1f}\% after "
             rf"{U['commod']['ip_trough']['h']} months; \ prices later", INFL),
            (r"real time: \ the trend of the 1960s saw slack that was not there", OUTPUT),
            (rf"zero: \ Japan from 1999, \ the Fed for {Z['us_zero_months']} months, \ the ECB below zero", RATE),
            (rf"QE: \ {Q['total_bp']:+.0f} basis points on eight days; \ guidance, \ negative rates, \ yield caps",
             BOND),
            (rf"r$^*$: \ {RS['us_2000']:.1f}\% in 2000, \ {RS['last']['rstar_us']:.1f}\% now; \ uncertain by a "
             r"point", CB),
            (rf"the euro: \ equilibria at {100 * D['free']['equilibria'][0]:.1f}\% and "
             rf"{100 * D['free']['equilibria'][1]:.0f}\%; \ a backstop leaves one", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 31, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del C
        with self.voiceover(
            "Part thirty-one in twelve lines. <bookmark mark='a'/> A sentence in London brought Spain's borrowing "
            "costs down by more than half. A central bank sets an overnight rate in the market for reserves: by "
            "quantity in a corridor, by announcement on a floor. In your seat in 1979, the data of the day showed "
            "slack that was not there. The rate reaches the economy through loans, credit, assets, the currency "
            "and expectations, slowly. Its effects are hard to measure because the bank acts on what it sees, "
            "which produced the price puzzle. On the Island, narrative shocks and clean surprises recovered the "
            "truth, and an information effect hid half of it. In America, output falls after a year or more, "
            "prices later. Rules need the gap and the neutral rate, and neither can be seen. At zero, central "
            "banks bought bonds, made promises and went below zero, with real but limited effects. The neutral "
            "rate has fallen. And the euro's crisis was partly self-fulfilling, which a believed backstop ended."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The corridor and the floor; quantitative easing in T-accounts; recursive identification "
            "and the price puzzle; a gap measured in real time; self-fulfilling yields; and a starred problem on "
            "the information effect. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Frederic Mishkin, \emph{The Economics of Money, Banking and Financial Markets}, \ chs.\ 14--16 and "
             r"23--25",
             r"Carl Walsh, \emph{Monetary Theory and Policy} (4th ed., 2017), \ chs.\ 1, 11 and 12",
             r"Alan Blinder, \emph{Central Banking in Theory and Practice} (1998)",
             r"Valerie Ramey, ``Macroeconomic Shocks and Their Propagation'', \ \emph{Handbook of Macroeconomics} "
             r"2A (2016)"],
            [r"Sims (1992); \ Christiano, \ Eichenbaum and Evans (1999); \ Romer and Romer (1989, 2000, 2004)",
             r"Kuttner (2001); \ Gertler and Karadi (2015); \ Nakamura and Steinsson (2018); \ Coibion (2012)",
             r"Orphanides (2001, 2004); \ Laubach and Williams (2003); \ Holston, \ Laubach and Williams (2023)",
             r"Wallace (1981); \ Gagnon, \ Raskin, \ Remache and Sack (2011); \ Swanson (2021); \ Bernanke (2020)",
             r"Calvo (1988); \ De Grauwe (2011)"])
        with self.voiceover(
            "The reading: Mishkin's textbook for the institutions; Carl Walsh for the theory; Alan Blinder's short "
            "book on central banking from the inside; and Valerie Ramey's survey of how shocks are identified. "
            "Then the papers, from Sims's price puzzle to the information effect, and Ben Bernanke's 2020 lecture "
            "on the new tools of monetary policy."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2013, r"Thomas Herndon", r"a graduate student asked to replicate a famous result for a "
                          r"class: \ growth falls sharply once public debt passes 90\% of GDP. \ A spreadsheet formula "
                          r"had left out five countries", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 32 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"The Treasury", font_size=46),
                     label(r"what can a government's budget do for the economy, \ and how much debt is too much?",
                           font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ the central bank; \ next: \ the finance ministry", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about the central bank. The next is about the other half of macroeconomic policy, the "
            "finance ministry. <bookmark mark='a'/> In 2010 Carmen Reinhart and Kenneth Rogoff reported that "
            "economic growth falls sharply once public debt passes ninety percent of GDP, and finance ministers "
            "cited the threshold for austerity. In 2013 a graduate student, Thomas Herndon, asked to replicate it "
            "for a class, found that a spreadsheet formula had left out five countries. <bookmark mark='b'/> Part "
            "thirty-two: the treasury. What can a government's budget do for the economy, and how much debt is "
            "too much?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
