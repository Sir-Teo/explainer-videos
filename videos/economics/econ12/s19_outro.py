from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

PROBLEMS = [
    r"Cournot with $N$ firms: \ for $P = a - bQ$ and cost $c$, \ show $P = \frac{a + Nc}{N + 1}$ and each profit "
    r"$\frac{(a - c)^2}{b (N + 1)^2}$; \ check \$40 and \$14.29.",
    r"Bertrand with costs \$10 and \$20: \ show there is no equilibrium in which the low-cost firm prices above \$20, "
    r"\ and find its profit when it prices a cent below.",
    r"Differentiated prices: \ for $q_i = \alpha - \beta p_i + \gamma p_j$, \ derive $p = \frac{\alpha + \beta c}"
    r"{2\beta - \gamma}$ \ and check \$36.67; \ find the joint-profit price.",
    r"Stackelberg: \ derive the leader's 45 and the follower's 22.5, \ and show the leader earns more than in Cournot.",
    r"Grim trigger: \ show the Cournot duopoly needs $\delta \ge \tfrac{9}{17}$, \ and that Bertrand with $N$ firms "
    r"needs $\delta \ge 1 - \tfrac1N$.",
    r"The merger paradox: \ show that two of three Cournot firms lose \$112.50 by merging, \ and that four of five "
    r"exactly break even.",
    r"Cowling and Waterson: \ prove that in Cournot equilibrium the share-weighted Lerner index equals "
    r"$H / \varepsilon$.",
    r"$\bigstar$ \ Dixit: \ with slips at \$30 and use at \$10, \ show credible capacities run from 20 to 40, \ and that "
    r"36 deters an entrant with setup cost \$144.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.0)
        a = wrapped_label(r"Somewhere between monopoly and competition, \ and where depends on what they commit to: \ "
                          r"quantities, \ capacity and difference keep prices above cost, \ while pure price "
                          r"competition drives them down with only two. \ They stop competing when the future is "
                          r"worth more than one season's cheating, \ when they can see each other's prices, \ and "
                          r"when no newcomer or prosecutor arrives.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = yards(0.9).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: how do a handful of firms compete, and when do they stop? <bookmark mark='a'/> Somewhere between "
            "monopoly and perfect competition, and where depends on what they commit to. Quantities, capacity and "
            "being different keep prices above cost; pure price competition drives them to cost with only two "
            "firms. They stop competing when the future is worth more than one season's cheating, when they can see "
            "each other's prices, and when no newcomer, and no prosecutor, arrives."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        b, d, c, m, cm = (load(x) for x in ("boats", "deter", "collusion", "merger", "common"))
        L = load("lysine")
        items = [
            (rf"lysine: \ 64 cents in the price war, \ then a cartel; \ {L['overcharge_pct'][0]} to "
             rf"{L['overcharge_pct'][1]}\% overcharged", CARTEL),
            (rf"Cournot: \ \${b['duo_P']:.0f} with two yards, \ \${b['P20']:.2f} with twenty, \ cost as the limit",
             LEADER),
            (r"Bertrand: \ two firms price at cost; \ the efficient one earns its advantage", CRUSOE),
            (r"the escapes: \ capacity (Kreps--Scheinkman), \ difference, \ repetition", COMPETE),
            (r"Hotelling and Salop: \ together for customers, \ apart for prices; \ too many sellers", PUMP),
            (r"Dixit and Stiglitz: \ a fixed markup, \ and variety that grows with the economy", ENTRANT),
            (rf"commitment: \ Stackelberg's first mover; \ {d['deter_k']:.0f} slips that keep Dara out", LEADER),
            (rf"collusion: \ $\delta \ge$ {c['cournot'][0]:.3f} for two; \ more firms need more patience", CARTEL),
            (r"Green and Porter's wars, \ Stigler partly right, \ leniency's built-in dilemma", E.MISS),
            (r"tacit collusion: \ the law reaches what firms say, \ not what they expect", GREY_A),
            (rf"$L = H/\varepsilon$; \ mergers: \ the paradox, \ \${m['saving_needed']:.2f} of savings, \ Williamson",
             "#F2C14E"),
            (rf"overcharges: \ 16 to 23\% at the median; \ common owners (MHHI {cm['mhhi_one']:,.0f} or "
             rf"{cm['mhhi_many']:,.0f}); \ algorithms".replace(",", "{,}"), ENTRANT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 12, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part twelve in twelve lines. <bookmark mark='a'/> The lysine market went from a price war below cost to "
            "a cartel that overcharged by twelve to twenty-eight percent. Cournot's quantity competition gives forty "
            "dollars with two yards and slides toward cost as yards are added. Bertrand's price competition reaches "
            "cost with two, and the more efficient firm earns only its advantage. Capacity, difference and "
            "repetition explain why most markets of a few price above cost. Hotelling's sellers move together for "
            "customers and apart for prices, and free entry can bring too many. Dixit and Stiglitz give every firm a "
            "fixed markup, and variety that grows with the economy. Commitment rewards the first mover, and "
            "capacity can keep a rival out. A cartel holds when firms are patient enough, and more firms need more "
            "patience. Price wars can happen with nobody cheating; Stigler was partly right; and leniency turns a "
            "cartel into a prisoner's dilemma. The law reaches what firms say to each other, not what they expect. "
            "Concentration predicts markups only under Cournot, and most mergers of close rivals need large savings. "
            "And cartels overcharge by sixteen to twenty-three percent at the median, while common owners and "
            "algorithms raise new questions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Cournot with N firms; Bertrand with unequal costs; price competition with different "
            "products; Stackelberg's leader; the patience a cartel needs; the merger paradox; Cowling and Waterson's "
            "formula; and a starred problem on Dixit's capacity. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jean Tirole, \emph{The Theory of Industrial Organization} (1988), chs.\ 5--9; \ Lu\'is Cabral, "
             r"\emph{Introduction to Industrial Organization} (2nd ed., 2017)",
             r"Dennis Carlton and Jeffrey Perloff, \emph{Modern Industrial Organization}; \ Belleflamme and Peitz, "
             r"\emph{Industrial Organization: Markets and Strategies}",
             r"Massimo Motta, \emph{Competition Policy: Theory and Practice} (2004); \ Whinston, \emph{Lectures on "
             r"Antitrust Economics} (2006)",
             r"John Connor, \emph{Global Price Fixing} (2nd ed., 2008); \ Kurt Eichenwald, \emph{The Informant} (2000)"],
            [r"Cournot (1838); \ Bertrand (1883); \ Edgeworth (1897); \ Hotelling (1929); \ Chamberlin (1933); \ "
             r"Robinson (1933)",
             r"von Stackelberg (1934); \ Stigler (1964); \ Williamson (1968); \ Friedman (1971); \ Dixit and Stiglitz "
             r"(1977); \ Salop (1979)",
             r"d'Aspremont, Gabszewicz and Thisse (1979); \ Dixit (1980); \ Kreps and Scheinkman (1983); \ Porter "
             r"(1983); \ Salant, Switzer and Reynolds (1983)",
             r"Green and Porter (1984); \ Fudenberg and Tirole (1984); \ Farrell and Shapiro (1990); \ Cowling and "
             r"Waterson (1976); \ McGee (1958)",
             r"Baumol, Panzar and Willig (1982); \ Milgrom and Roberts (1982); \ Kreps and Wilson (1982); \ "
             r"Borenstein, Cameron and Gilbert (1997)",
             r"Connor (1998, 2014); \ Levenstein and Suslow (2006); \ Boyer and Kotchoni (2015); \ O'Brien and Salop "
             r"(2000)",
             r"Azar, Schmalz and Tecu (2018); \ Dennis, Gerardi and Schenone (2022); \ Calvano et al.\ (2020); \ "
             r"Assad et al.\ (2024)"])
        with self.voiceover(
            "The reading: chapters five to nine of Tirole's Theory of Industrial Organization, and Cabral's "
            "introduction; Carlton and Perloff, and Belleflamme and Peitz; Motta's Competition Policy and "
            "Whinston's lectures on antitrust; and for the story, Connor's Global Price Fixing and Kurt Eichenwald's "
            "The Informant. Then the papers, from Cournot to the pricing algorithms."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1970, r"George Akerlof, \ ``The Market for `Lemons'\,''", r"thirteen pages on used cars, \ "
                          r"turned down by three journals \\ before the Quarterly Journal of Economics printed them",
                          color=E.ACCENT, width=10.4, font_size=24).move_to(UP * 1.2)
        nxt = VGroup(label(r"Next: \ Part 13 \ $\cdot$ \ Act IV, \ Failure and Design", font_size=30, color=GREY_B),
                     label(r"Lemons and Signals", font_size=46),
                     label(r"what happens to a market when one side knows more than the other?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"the yards knew each other's prices; \ buyers don't always know what they buy", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "In this part, everyone knew what they were buying, and the yards could see each other's prices. "
            "<bookmark mark='a'/> Next time, a market where buyers cannot tell good from bad: George Akerlof's "
            "thirteen pages on used cars, turned down by three journals before the Quarterly Journal of Economics "
            "printed them in 1970. <bookmark mark='b'/> Part thirteen opens Act Four, on failure and design: lemons "
            "and signals."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()
