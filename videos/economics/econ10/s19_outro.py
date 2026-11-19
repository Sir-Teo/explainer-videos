from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

PROBLEMS = [
    r"One price: \ with demand $q = a - b\,p$ and marginal cost $c$, \ show that $p^* = \tfrac{1}{2}(a/b + c)$, \ "
    r"that $(p^* - c)/p^* = 1/\varepsilon$ there, \ and that the deadweight loss is a quarter of the competitive "
    r"surplus.",
    r"Third degree: \ students $q = 60 - 10p$, \ townsfolk $q = 100 - 5p$, \ $c = 1$. \ Show that one price serves "
    r"only the townsfolk, \ and that two prices raise welfare.",
    r"Screening: \ types $\theta_L < \theta_H$, \ a share $s$ high. \ Show $q_L = \theta_L - \tfrac{s}{1-s}"
    r"(\theta_H - \theta_L)$ \ and that the high type's rent is $(\theta_H - \theta_L)\,q_L$.",
    r"Oi: \ two buyers with $q = 10 - p$ and one with $q = 16 - p$, \ cost 2. \ Show that the best tariff that keeps "
    r"all three is a price of 4 and a fee of 18, \ and that it beats shutting the two out.",
    r"Coase in two periods: \ values uniform on $[0, 1]$, \ discount $\delta$. \ Show that the first price is "
    r"$\frac{(2-\delta)^2}{2(4 - 3\delta)}$, \ below $\tfrac{1}{2}$.",
    r"Ramsey: \ minimize the deadweight loss of two prices subject to covering a fixed cost, \ and derive "
    r"$\frac{p_i - c_i}{p_i} = \frac{k}{\varepsilon_i}$.",
    r"Littlewood: \ derive the rule from the last seat kept back, \ and find it for \$4 and \$10 fares and late "
    r"demand $N(12, 5^2)$.",
    r"$\bigstar$ \ Personal prices: \ if $\log v = a + s\,e$ with $e$ logistic, \ show that at its best personal "
    r"price every buyer buys with probability $1 - s$, \ and compare with Agora's 65\%.",
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
        a = wrapped_label(r"She raises it above cost until the revenue from one more sale is just its cost, \ and "
                          r"the buyers she turns away are the economy's loss. \ Then, \ wherever she can tell "
                          r"buyers apart or make them sort themselves, \ she charges them differently, \ and each "
                          r"step takes more of their surplus and wastes less of it. \ What limits her is how much she "
                          r"knows, \ what she can promise, \ and the regulator.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = ferry_glyph(1.8).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: what does a seller do when the price is hers to set? <bookmark mark='a'/> She raises it above cost, "
            "until the revenue from one more sale is just what it costs her, and the buyers she turns away are the "
            "economy's loss. Then, wherever she can tell buyers apart, or make them sort themselves, she charges "
            "them differently, and each step takes more of their surplus and wastes less of it. What limits her is "
            "how much she knows about her buyers, what she can credibly promise, and the regulator."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=RIGHT * 0.3))
        self.clear_scene()

    def recap(self):
        f, m, t, s, r, d, lw, pt = (load(x) for x in ("ferry", "monopoly", "third", "screen", "rides", "durable",
                                                      "littlewood", "passthrough"))
        items = [
            (r"Dupuit's roofless carriage: \ a price made worse on purpose", E.ACCENT),
            (rf"the ferry: \ the best fare \${f['best_fare']:.2f}, \ and the crossings it turns away", BO),
            (r"marginal revenue = marginal cost; \ the Lerner index is one over the elasticity", MR),
            (rf"what it costs: \ Harberger's triangle \ (\${m['dwl']:.0f} of \${m['cs_competitive']:.0f}), \ "
             r"Posner's rectangle", DWL),
            (r"first degree: \ all the surplus, \ none wasted", PROFIT),
            (rf"third degree: \ students at \${t['discriminate']['p'][0]:.2f}, \ a market opened", STUD),
            (rf"second degree: \ a menu that sorts, \ the low type's quality cut to {s['qL']:.2f}", TOWN),
            (rf"two-part tariffs and bundles: \ Oi's \${r['two']['fee']:.0f} fee, \ Adams and Yellen", CS),
            (rf"durable goods: \ Coase, \ a first price of \${1000 * d['rows'][-1]['first_price']:.0f} with daily cuts",
             HOLD),
            (r"natural monopoly, \ Ramsey prices, \ gold plating, \ price caps, \ monopsony", GREY_A),
            (rf"pass-through: \ coffee's {pt['elasticity']:.2f} after six quarters; \ markups, \ contested", BEAN),
            (rf"Littlewood's {lw['protect_best']} seats; \ prices learned by machine", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 10, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part ten in twelve lines. <bookmark mark='a'/> Dupuit's roofless carriage made a product worse on "
            "purpose. Bo's best fare was about five dollars sixty, and it turned crossings away that were worth "
            "more than they cost. The monopolist sets marginal revenue equal to marginal cost, and the Lerner index "
            "is one over the elasticity. Harberger's triangles say the waste is small; Posner's rectangles add the "
            "cost of fighting for the monopoly. A price for every buyer takes all the surplus and wastes none. Two "
            "prices opened a market for the students. A menu sorts buyers, at the cost of quality cut for the "
            "low type. Two-part tariffs and bundles take more again. A durable good competes with its own future, as "
            "Coase saw. Natural monopolies need someone to pay for the pipes; regulators cap profits, and get gold "
            "plating, or cap prices; and one employer pays less and hires fewer. Coffee's shelf price takes up "
            "fifty-five hundredths of a change in the bean price in a year and a half, and how large markups are is "
            "contested. And Littlewood's thirteen seats led to the prices that machines set today."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The monopoly price, the Lerner rule and the deadweight loss for straight-line demand; "
            "the students and the townsfolk; the screening menu and its information rent; Oi's two-part tariff for "
            "three visitors; the Coase problem in two periods; Ramsey's rule; Littlewood's rule; and a starred problem "
            "on why, at its best personal price, every one of Agora's buyers buys with the same probability. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jean Tirole, \emph{The Theory of Industrial Organization} (1988), chs.\ 1--4",
             r"Paul Belleflamme and Martin Peitz, \emph{Industrial Organization: Markets and Strategies} (2015)",
             r"Hal Varian, \emph{Intermediate Microeconomics}: \ monopoly, \ monopoly behaviour, \ factor markets",
             r"Kalyan Talluri and Garrett van Ryzin, \emph{The Theory and Practice of Revenue Management} (2004)"],
            [r"Dupuit (1844, 1849); \ Pigou (1920); \ Robinson (1933); \ Lerner (1934)",
             r"Harberger (1954); \ Posner (1975); \ Schmalensee (1981); \ Varian (1985)",
             r"Mussa and Rosen (1978); \ Maskin and Riley (1984); \ Deneckere and McAfee (1996); \ Oi (1971)",
             r"Stigler (1963); \ Adams and Yellen (1976); \ McAfee, McMillan and Whinston (1989)",
             r"Coase (1972); \ Stokey (1981); \ Bulow (1982, 1986); \ Gul, Sonnenschein and Wilson (1986)",
             r"Ramsey (1927); \ Boiteux (1956); \ Averch and Johnson (1962); \ Littlechild (1983); \ Littlewood "
             r"(1972)",
             r"Nakamura and Zerom (2010); \ Weyl and Fabinger (2013); \ Hall (1988); \ De Loecker and Warzynski "
             r"(2012)",
             r"De Loecker, Eeckhout and Unger (2020); \ Traina (2018); \ Dub\'e and Misra (2023); \ Calvano et al.\ "
             r"(2020); \ Assad et al.\ (2024)"])
        with self.voiceover(
            "The reading: the first four chapters of Tirole's Theory of Industrial Organization; Belleflamme and "
            "Peitz; Varian's chapters on monopoly; and Talluri and van Ryzin on revenue management. Then the papers, "
            "from Dupuit's bridges to the pricing algorithms."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1950, r"Merrill Flood and Melvin Dresher, \ at RAND", r"a new game, \ played a hundred "
                          r"times by two colleagues, \ to test a young mathematician's idea: \ they cooperated far "
                          r"more often than the idea said they should", color=E.ACCENT, width=10.4,
                          font_size=24).move_to(UP * 1.2)
        nxt = VGroup(label(r"Next: \ Part 11 \ $\cdot$ \ Act III, Markets", font_size=30, color=GREY_B),
                     label(r"Games", font_size=46),
                     label(r"what happens when my best choice depends on yours, \ and yours on mine?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"Bo had no rivals: \ his choices depended only on his buyers", font_size=30, color=GREY_A
                     ).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "Bo had no rivals, so his best price depended only on his buyers. <bookmark mark='a'/> Next time, choices "
            "that depend on each other. In January 1950, at the RAND Corporation, Merrill Flood and Melvin Dresher "
            "had two colleagues play a new game a hundred times, to test an idea of a young Princeton mathematician "
            "named John Nash. The players cooperated far more often than the idea said they should. "
            "<bookmark mark='b'/> Part eleven: games."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()
