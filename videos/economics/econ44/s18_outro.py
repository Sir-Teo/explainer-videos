from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403

PROBLEMS = [
    r"Zurcher's game: \ a rebuild costs \$4,000, \ upkeep is \$6 a month per 5,000 miles, \ and a bus covers 3,300 "
    r"miles a month. \ Using the rule that the best mileage is about $\sqrt{2 \cdot RC \cdot v / c}$, \ find it.",
    r"Rust: \ with $RC$ = 9.79 and $\theta$ = 2.65 (per 1,000 steps), \ how many months of upkeep at 150,000 miles is "
    r"a rebuild worth? \ At 250,000?",
    r"Myopia: \ the log likelihood is $-299.2$ at $\beta$ = 0.9999 and $-305.7$ at $\beta$ = 0. \ Compute the "
    r"likelihood-ratio statistic and test at 5\%.",
    r"Double marginalization: \ demand $P$ = 10 $-$ $Q$, \ cost 2. \ Find the integrated price, \ the wholesale and "
    r"retail prices of separate firms, \ and the fixed fee a two-part tariff could charge.",
    r"Platforms: \ with $n_1 = 1 + 0.2 n_2 - p_1$ and $n_2 = 1 + \alpha_2 n_1 - p_2$ at zero cost, \ show that "
    r"$p_1$ = 0.5 and $p_2$ = 0.5 when $\alpha_2$ = 0.2.",
    r"Arrow: \ demand $P$ = 10 $-$ $Q$; \ a new process cuts cost from 4 to 2. \ Find the gain to a monopolist and "
    r"to an innovator in a competitive industry. \ Is the innovation drastic?",
    r"Killer acquisitions: \ with the chapter's numbers, \ for which development costs does the start-up develop the "
    r"drug but the incumbent shelve it?",
    r"$\bigstar$ \ Baron and Myerson with two types: \ derive the virtual cost $c_H + \frac{\nu}{1-\nu}(1-w)(c_H - "
    r"c_L)$ and show the high-cost output is $a$ minus it.",
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
        a = wrapped_label(r"Over time, \ by investing and racing, \ with choices that look ahead and can be estimated "
                          r"from what firms do. \ With networks, \ the price structure matters, \ markets can tip, \ "
                          r"and antitrust must weigh effects that do not show in today's prices.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1974.9, 1985.4], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, BUS, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: how do firms compete over time, and what is different when the product is a network? "
            "<bookmark mark='a'/> Over time, firms invest and race, and their choices look ahead, as Zurcher's did; "
            "those choices can be estimated from what firms actually do. With networks, the structure of prices "
            "matters as much as their level, markets can tip and stay tipped, and antitrust must weigh effects that "
            "do not show up in today's prices."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        R, C, Dq, V, Pl, L, I, K, Q, G, P = (load(x) for x in ("rust", "ccp", "duopoly", "vertical", "platform",
                                                               "lockin", "innovation", "killer", "qlearn",
                                                               "regulation", "playit"))
        items = [
            (rf"the game: \ rebuild at {P['best'] // 1000}k miles; \ \${P['best_cost']:,.0f} a month", BUS),
            (rf"Rust: \ $RC$ = {R['nfxp']['RC']:.2f}, \ $\theta$ = {R['nfxp']['theta1']:.2f}; \ myopia rejected "
             rf"(LR {R['lr']:.1f})", BUS),
            (rf"CCP: \ no fixed point; \ fine with 1,000 buses, \ fragile with {R['n_repl']} rebuilds", CCP_C),
            (rf"dynamic duopoly: \ a race, \ {Dq['lead_changes']} changes of leader", PATIENT),
            (rf"vertical: \ two markups, \ price {V['p_sep']:.0f} instead of {V['p_int']:.0f}", LOSS),
            (r"platforms: \ the side worth most to the other pays least, \ even below cost", FIRM2),
            (rf"lock-in: \ a worse first mover wins {100 * L['at02']:.0f}\% of runs; \ QWERTY disputed", MYOPIC),
            (rf"innovation: \ Arrow's replacement effect; \ an inverted U, \ peak at $\Delta$ = {I['peak']:.1f}",
             GAIN),
            (rf"killer acquisitions: \ a project worth {K['entrant_gain']:.0f} to its maker is shelved", LOSS),
            (rf"algorithms: \ profit gain {Q['mean_gain']:.2f}; \ punishments in every session", FIRM1),
            (r"antitrust: \ consumer welfare against power; \ Microsoft, \ Google", E.ACCENT),
            (rf"regulation: \ cut high-cost output {G['q_hi_full']:.0f} $\to$ {G['q_hi']:.1f} to shrink the rent",
             PATIENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 44, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del C, Pl
        with self.voiceover(
            "Part forty-four in twelve lines. <bookmark mark='a'/> Rebuilding an engine trades rebuild bills "
            "against upkeep, and the best rule balances them. Rust recovered from Zurcher's choices what a rebuild "
            "and an ageing engine must have cost, and the data reject a superintendent who ignored the future. "
            "Conditional choice probabilities skip the fixed point, at a price in precision. Firms that invest "
            "against each other race, hardest when close. Two markups are worse than one, for everyone. A platform "
            "charges least to the side the other side values most, sometimes less than nothing. Network effects "
            "can lock a market into a worse technology, though whether QWERTY is one is disputed. Competition can "
            "spur or starve innovation, and the evidence traces an inverted U. Incumbents can buy rivals' projects "
            "to shelve them. Pricing algorithms can learn to collude without being told. Antitrust law weighs "
            "consumer welfare against concentrated power. And a regulator who knows less than the firm trades "
            "efficiency against the rents it must leave."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The best rebuild rule; Rust's costs in months of upkeep; a test of myopia; double "
            "marginalization and its fix; a platform's prices; Arrow's replacement effect; killer acquisitions; and "
            "a starred derivation of Baron and Myerson's virtual cost. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jean Tirole, \emph{The Theory of Industrial Organization} (1988)",
             r"Aguirregabiria, \emph{Empirical Industrial Organization: \ Models, \ Methods, \ and Applications} "
             r"(2021)",
             r"Michael Whinston, \emph{Lectures on Antitrust Economics} (2006)",
             r"Jean Tirole, \emph{Economics for the Common Good} (2017)"],
            [r"Spengler (1950); \ Arrow (1962); \ Baron and Myerson (1982); \ David (1985); \ Rust (1987)",
             r"Arthur (1989); \ Liebowitz and Margolis (1990); \ Hotz and Miller (1993); \ Pakes and McGuire (1994)",
             r"Ericson and Pakes (1995); \ Rochet and Tirole (2003); \ Rysman (2004); \ Aghion et al.\ (2005)",
             r"Armstrong (2006); \ Bajari, \ Benkard and Levin (2007); \ Ryan (2012); \ Kwoka (2013, \ 2015)",
             r"Khan (2017); \ Calvano et al.\ (2020); \ Cunningham, \ Ederer and Ma (2021); \ Assad et al.\ (2024)"])
        with self.voiceover(
            "The reading: Tirole's text again; Victor Aguirregabiria's book on empirical industrial organization, "
            "which covers the dynamic methods; Michael Whinston's lectures on antitrust economics; and Tirole's "
            "Economics for the Common Good, on regulating platforms. Then the papers, from Spengler to the "
            "algorithms."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2006, r"DellaVigna and Malmendier", r"show gym members on monthly contracts paying more than "
                          r"\$17 a visit when a ten-visit pass cost \$10 a visit: \ paying not to go to the gym",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 45 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"Behavioural Economics", font_size=46),
                     label(r"what changes in economics when people are not the agents of Part 5?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from firms that look ahead \ to people who do not always", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part assumed that people and firms look ahead well: Zurcher was patient, firms race rationally. "
            "<bookmark mark='a'/> In 2006 Stefano DellaVigna and Ulrike Malmendier studied gym members who chose a "
            "monthly contract and paid, on average, more than seventeen dollars a visit, when a ten-visit pass "
            "would have cost them ten. They were paying not to go to the gym. <bookmark mark='b'/> Part "
            "forty-five: behavioural economics. What changes in economics when people are not the agents of Part "
            "five?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
