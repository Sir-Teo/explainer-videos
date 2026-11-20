from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403

PROBLEMS = [
    r"Variety: \ with $\sigma = 4$, \ how much do real wages rise when two identical countries trade? \ When ten "
    r"do?",
    r"Grubel-Lloyd: \ America exported \$713bn of capital goods and imported \$1,133bn. \ Compute the index, \ and "
    r"say what aggregation does to it.",
    r"Gravity: \ with trade $\propto Y_o Y_d / D$, \ how does trade with a partner 5,000 km away compare with one "
    r"500 km away of the same size?",
    r"Home market: \ with $\phi = 0.3$, \ show that 55\% of demand gives about 59\% of firms, \ and find the share "
    r"of demand that attracts all of them.",
    r"Melitz: \ with Pareto shape 4.25, \ $\sigma = 4$, \ $\tau = 1.3$ and $f_x/f = 1.5$, \ find the share of firms "
    r"that export.",
    r"Gains: \ America spends 89.4\% of its income on home goods. \ Find the loss from autarky with $\theta = 4$ and "
    r"with $\theta = 2$.",
    r"China shock: \ exposure rose \$1,839 per worker in 2000--07. \ With a coefficient of $-0.596$, \ what fall in "
    r"the manufacturing share follows?",
    r"$\bigstar$ \ Eaton-Kortum: \ derive $\pi_{ni} = T_i (w_i d_{ni})^{-\theta}/\Phi_n$ from Fr\'echet "
    r"productivity draws.",
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
        a = wrapped_label(r"Because people want variety and firms have fixed costs, \ similar countries trade "
                          r"different versions of the same goods; \ and because trade falls with distance and stops "
                          r"at borders, \ most of it is between large neighbours. \ Only the best firms export, \ and "
                          r"trade raises productivity by moving output to them. \ Imports from China raised "
                          r"America's income and devastated the places that made the same things, \ and those places "
                          r"have not recovered.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1985, 2025], [0, 560], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], CHINA, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why is most trade between similar countries, and what did a generation of imports from China do? "
            "<bookmark mark='a'/> Because people want variety and firms have fixed costs, similar countries trade "
            "different versions of the same goods; and because trade falls with distance and stops at borders, "
            "most of it is between large neighbours. Only the best firms export, and trade raises productivity by "
            "moving output to them. Imports from China raised America's income as a whole, and devastated the "
            "places that made the same things, and those places have not recovered."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        I_, K, P, G, F, M, E_, H, C, T, Ch = (load(x) for x in (
            "intra", "krugman", "playit", "gravity", "firms", "melitz", "ek", "hat", "china", "tariffs", "chains"))
        Ix = tables.IDEAL_X.data
        u, c, d = H["regions"].index("USA"), H["regions"].index("CHN"), H["regions"].index("DEU")
        items = [
            (rf"the box: \ loading \${Ix['hand']:.2f} a ton by hand, \ under {100 * Ix['box']:.0f} cents in "
             r"containers", ARCH),
            (rf"two-way trade: \ capital goods {I_['capital goods']['gl2025']:.2f} (2025), \ cars "
             rf"{I_['cars and parts']['gl1967']:.2f} (1967)", FISH),
            (rf"variety: \ two islands, \ real wages +{100 * K['gain2']:.0f}\%; \ 55\% of demand, \ "
             rf"{100 * K['hm_55']:.0f}\% of firms", ARCH),
            (rf"Play it: \ Spain to Portugal \${P['pairs']['PRT']['actual']:.0f}bn, \ Japan "
             rf"\${P['pairs']['JPN']['actual']:.1f}bn", GAIN),
            (rf"gravity: \ distance {G['ols'][2]:.2f} (OLS), \ {G['ppml'][0]:.2f} (PPML); \ borders $\times$"
             rf"{G['mccallum']} (McCallum)", WHITE),
            (rf"firms: \ {100 * F['share_exporters']:.0f}\% export, \ selling {100 * F['sales_share_exporters']:.0f}\% "
             r"of output", FIRM),
            (rf"Melitz: \ {100 * M['exit_share']:.0f}\% exit, \ productivity +{100 * M['welfare_gain']:.1f}\%", TARIFF),
            (rf"Eaton-Kortum: \ formula and simulation within {100 * E_['max_gap']:.1f} points", ARCH),
            (rf"gains: \ autarky costs America {100 * H['acr'][u]:.1f}\%, \ Germany {100 * H['acr'][d]:.1f}\%; \ "
             rf"US-China +25\%: \ {100 * H['welfare'][u]:+.2f}\%, \ {100 * H['welfare'][c]:+.2f}\%", GAIN),
            (rf"China: \ \${C['imp1991']:.0f}bn $\to$ \${C['imp2007']:.0f}bn; \ {C['adh_beta']:.3f} points per "
             r"\$1,000", CHINA),
            (rf"tariffs: \ passed in full; \ buyers $-$\${T['buyers_loss'] / 1e9:.0f}bn, \ net $-$"
             rf"\${T['net_loss'] / 1e9:.1f}bn; \ 2025: \ {T['rate2025']:.1f}\%", TARIFF),
            (rf"chains: \ China's value added \${Ch['china_va']:.2f} an iPhone; \ elasticity 0.76 $\to$ 2", WHITE),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 36, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-six in twelve lines. <bookmark mark='a'/> The container made shipping cheap. Rich countries "
            "trade the same kinds of goods in both directions. Love of variety and economies of scale explain it, "
            "and give the larger market more than its share of an industry. Trade falls with distance, as gravity "
            "says, and borders cut it further. Exporters are few, large and productive, and opening to trade moves "
            "output to them, raising productivity without any firm improving. Comparative advantage, with a "
            "distribution, produces gravity, and three models give one formula for the gains, a few percent for "
            "large economies. The China shock cost particular places a great deal. Tariffs fell on American buyers. "
            "And trade is increasingly in tasks along value chains, with an elasticity that grows with time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The gains from variety; the Grubel-Lloyd index; gravity and distance; the home-market "
            "effect; Melitz's exporters; the gains formula; the China shock's arithmetic; and a starred derivation "
            "of Eaton and Kortum's shares. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Paul Krugman, \ Maurice Obstfeld and Marc Melitz, \emph{International Economics} (12th ed., 2022), "
             r"chs 7--8",
             r"Robert Feenstra, \emph{Advanced International Trade} (2nd ed., 2015), chs 5--6",
             r"Keith Head and Thierry Mayer, ``Gravity Equations'', \emph{Handbook of International Economics} vol.\ 4 "
             r"(2014)",
             r"Marc Levinson, \emph{The Box} (2006)"],
            [r"Tinbergen (1962); \ Grubel and Lloyd (1975); \ Krugman (1979, 1980); \ McCallum (1995)",
             r"Bernard and Jensen (1995); \ Eaton and Kortum (2002); \ Melitz (2003); \ Anderson and van "
             r"Wincoop (2003)",
             r"Santos Silva and Tenreyro (2006); \ Dekle, \ Eaton and Kortum (2008); \ Xing and Detert (2010)",
             r"Arkolakis, \ Costinot and Rodr\'iguez-Clare (2012); \ Autor, \ Dorn and Hanson (2013)",
             r"Amiti, \ Redding and Weinstein (2019); \ Fajgelbaum et al.\ (2020); \ Boehm et al.\ (2023)"])
        with self.voiceover(
            "The reading: Krugman, Obstfeld and Melitz, and Feenstra, for the theory; Head and Mayer's chapter on "
            "gravity equations; and Marc Levinson's history of the box. Then the papers, from Tinbergen to the "
            "tariffs of 2018."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1971, r"Thomas Schelling", r"coins on a checkerboard: \ each moves when too few of its "
                          r"neighbours are like it; \ even when each is content as a minority, \ the board "
                          r"segregates", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 37 \ $\cdot$ \ Act VII, \ The World Economy", font_size=30, color=GREY_B),
                     label(r"Cities and Regions", font_size=46),
                     label(r"why is economic activity piled up in a few places, \ and what does that do to the "
                           r"people in them?", font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from trade between countries \ to the places within them", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part ended in particular places. The next is about places. <bookmark mark='a'/> In 1971 Thomas "
            "Schelling published a model you can play with coins on a checkerboard. Each coin moves to an empty "
            "square when too few of its neighbours are like it. Even when every coin is content to be in the "
            "minority, the board sorts itself into large blocks of one kind: an outcome nobody wanted. "
            "<bookmark mark='b'/> Part thirty-seven: cities and regions. Why is economic activity piled up in a few "
            "places, and what does that do to the people in them?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
