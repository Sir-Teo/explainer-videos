from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403

PROBLEMS = [
    r"Ricardo: \ Home needs 1 hour for a fish and 2 for a bolt; \ Foreign 3 and 4. \ Who has the comparative "
    r"advantage in cloth, \ and between which prices can they trade?",
    r"The same, \ with 1,200 hours each and half of spending on each good: \ find the world price, \ and show that "
    r"Home gains nothing.",
    r"Wages: \ with Ricardo's numbers, \ show that Portugal's wage relative to England's lies between $10/9$ and "
    r"$3/2$.",
    r"Continuum: \ with equal spending shares, \ show that $\omega = \frac{\bar z}{1-\bar z}\frac{L^*}{L}$, \ and "
    r"that a larger $L^*$ raises $\omega$ and lowers $\bar z$.",
    r"Stolper-Samuelson: \ with labour shares 0.7 and 0.3, \ show that a 10\% rise in cloth's price raises the wage "
    r"17.5\% and lowers the rent 7.5\%, \ to first order.",
    r"Tariff: \ $D = 100 - 10p$, \ $S = 10p - 20$, \ world price 4, \ tariff 1. \ Find the consumers' loss, \ the "
    r"producers' gain, \ the revenue and the deadweight loss.",
    r"Optimal tariff: \ import demand $M = 120 - 20p$, \ foreign supply $X^* = 40p^* - 120$. \ Find the best "
    r"tariff, \ and check that $t/p^* = 1/\varepsilon^*$.",
    r"$\bigstar$ \ Show that identical technologies, \ equal factor prices and identical homothetic tastes imply "
    r"$F_c = V_c - s_c V_w$.",
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
        a = wrapped_label(r"Because relative costs differ, \ through technology and through what countries have, \ "
                          r"trade lets each buy what is dear to make at home, \ and the country gains. \ But not "
                          r"everyone in it: \ the factors used intensively in imports, \ and those stuck in "
                          r"import-competing industries, \ lose. \ Because they are few and concentrated, \ they "
                          r"often win the politics. \ The winners could compensate them, \ and rarely do.", 11.6, 25,
                          WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1929, 2025], [0, 20], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], TARIFF, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why do countries trade, and who wins and loses when they do? <bookmark mark='a'/> Because "
            "relative costs differ, through technology and through what countries have, trade lets each buy what "
            "is dear to make at home, and the country as a whole gains. But not everyone in it. The owners of the "
            "factors that imports use intensively, and of those stuck in industries that compete with imports, "
            "lose. Because they are few and concentrated, they often win the politics. The winners could "
            "compensate them, and rarely do."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        O, P, R, M, J, H, S, L, Sp, T, W, D, F = (load(x) for x in (
            "openness", "playit", "ricardo", "many", "japan", "ho", "stolper", "leontief", "specific", "tariff", "war",
            "dials", "film"))
        items = [
            (rf"trade in rich economies: \ {O['m1870']:.0f}\% of GDP (1870), \ {O['m1932']:.0f}\% (1932), \ "
             rf"{O['m2019']:.0f}\% (2019)", WHITE),
            (rf"Play it: \ the weaker island gains {100 * P['island']['gain']:.0f}\%, \ the stronger "
             rf"{100 * P['arch']['gain']:.0f}\%", ISLAND),
            (rf"Ricardo: \ wine for cloth at {R['p']:.0f}; \ Portugal's wage {1 / R['wage_ratio']:.2f} times England's",
             WINE),
            (rf"the continuum: \ the Archipelago grows; \ the Island's wage {M['free']['omega']:.2f} $\to$ "
             rf"{M['grow']['omega']:.2f}", ARCH),
            (rf"Japan: \ the test passes in {J['negative']} of 8 years; \ gains at most {J['gain_lo']:.0f}--"
             rf"{J['gain_hi']:.0f}\%", CLOTH),
            (rf"factor proportions: \ the Island sells {H['island']['X'][0]:.0f} bolts for {-H['island']['X'][1]:.0f} "
             r"machines; \ factor prices equalize", CAPITAL),
            (rf"Stolper-Samuelson: \ cloth +10\%, \ wage {100 * S['dw']:+.0f}\%, \ rent {100 * S['dr']:+.0f}\%",
             LABOUR),
            (rf"Leontief: \ \${L['k_exports']:,.0f} against \${L['k_imports']:,.0f}; \ Trefler: \ right sign "
             rf"{100 * L['sign_test']:.0f}\%", TARIFF),
            (rf"specific factors: \ food +10\%, \ land {100 * Sp['drT']:+.0f}\%, \ wage {100 * Sp['dw']:+.0f}\%, \ "
             rf"capital {100 * Sp['drK']:+.0f}\%", LAND),
            (rf"a tariff: \ shoppers $-{T['small']['cs_loss']:.0f}$, \ weavers $+{T['small']['ps_gain']:.0f}$, \ "
             rf"treasury $+{T['small']['revenue']:.0f}$; \ best large tariff {100 * T['opt_av']:.0f}\%", FISH),
            (rf"a trade war: \ each side {100 * W['pay']['tariff|tariff'][0]:+.0f} \ (in hundredths) \ against free "
             r"trade", TARIFF),
            (rf"the gains from trade, \ America: \ {100 * D['gain10']:.1f}--{100 * D['gain5']:.1f}\%; \ its tariff "
             rf"{F['v2024']:.1f}\% $\to$ {F['v2025']:.1f}\%", GAIN),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 35, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-five in twelve lines. <bookmark mark='a'/> Trade in rich economies is twice the share of "
            "output it was in the 1930s. A country worse at everything still gains from trade, and so does its "
            "partner. Ricardo's four numbers say why: relative costs, not absolute ones, decide who sells what, and "
            "wages follow productivity. With many goods, growth abroad raises wages at home while moving industries "
            "away. Japan's opening passes the theory's test. With equal technologies, endowments decide trade, and "
            "trade in goods equalizes the prices of factors. Stolper and Samuelson show that a country's scarce "
            "factor loses. Leontief's paradox and Trefler's missing trade show that technology differences are "
            "needed too. In the short run, the factors stuck in an industry gain or lose most. A small country's "
            "tariff makes it poorer; a large one's makes its neighbour poorer. So countries fall into trade wars, "
            "and sign agreements to escape them. And the gains from trade are real, a few percent of income."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Comparative advantage with four numbers, and a large country that gains nothing; "
            "Ricardo's wage band; the continuum model; the magnification effect; the triangles of a tariff; the "
            "optimal tariff; and a starred proof of the factor-content prediction that Trefler tested. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Paul Krugman, \ Maurice Obstfeld and Marc Melitz, \emph{International Economics} (12th ed., 2022), "
             r"chs 3--6, 9--10",
             r"Robert Feenstra, \emph{Advanced International Trade} (2nd ed., 2015), chs 1--3",
             r"Douglas Irwin, \emph{Clashing over Commerce: A History of US Trade Policy} (2017)",
             r"Arnaud Costinot and Andr\'es Rodr\'iguez-Clare, ``Trade Theory with Numbers'', \emph{Handbook of "
             r"International Economics} vol.\ 4 (2014)"],
            [r"Ricardo (1817); \ Heckscher (1919); \ Ohlin (1933); \ Stolper and Samuelson (1941); \ Lerner (1952)",
             r"Leontief (1953); \ Jones (1971); \ Dornbusch, \ Fischer and Samuelson (1977); \ Leamer (1980)",
             r"Grossman and Helpman (1994); \ Trefler (1995); \ Bagwell and Staiger (1999); \ Goldberg and "
             r"Maggi (1999)",
             r"Eaton and Kortum (2002); \ Bernhofen and Brown (2004, 2005); \ Irwin (2005)",
             r"Arkolakis, \ Costinot and Rodr\'iguez-Clare (2012); \ Costinot and Donaldson (2012)"])
        with self.voiceover(
            "The reading: Krugman, Obstfeld and Melitz for the undergraduate course; Feenstra's Advanced "
            "International Trade for the graduate one; Douglas Irwin's history of American trade policy; and "
            "Costinot and Rodriguez-Clare's chapter, which puts numbers on the theories. Then the papers, from "
            "Ricardo to Costinot and Donaldson."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1956, r"Malcom McLean", r"26 April 1956: \ a converted tanker, \ the \emph{Ideal X}, \ "
                          r"leaves Newark for Houston \ with fifty-eight truck trailers on its deck", color=E.ACCENT,
                          width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 36 \ $\cdot$ \ Act VII, \ The World Economy", font_size=30, color=GREY_B),
                     label(r"Trade II: \ Scale, \ Firms and Gravity", font_size=46),
                     label(r"why is most trade between similar countries, \ and what did a generation of imports "
                           r"from China do?", font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from why countries trade \ to what they trade, \ and with whom", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked why countries trade. The next asks what they trade, and with whom. "
            "<bookmark mark='a'/> On the twenty-sixth of April 1956 a converted tanker, the Ideal X, left Newark "
            "for Houston with fifty-eight truck trailers on its deck. Its owner, Malcom McLean, a trucker, had seen "
            "how slow and costly it was to load a ship by hand. The box he put to sea changed what it costs to "
            "move a thing across the world. <bookmark mark='b'/> Part thirty-six: scale, firms and gravity. Why is "
            "most trade between similar countries, and what did a generation of imports from China do?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
