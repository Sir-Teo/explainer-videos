from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

PROBLEMS = [
    r"The box: \ Ana spends a share $a$ of her wealth on fish, \ Bo a share $b$. \ Show that the contract curve is "
    r"$y = \frac{k_B x Y}{k_A (X - x) + k_B x}$ \ with $k = \tfrac{a}{1-a}$, \ and find it for Ana and Bo.",
    r"Equilibrium: \ derive the competitive price $p = \frac{a\,e_{A2} + b\,e_{B2}}{(1-a)\,e_{A1} + (1-b)\,e_{B1}}$ "
    r"\ and check it for Ana and Bo.",
    r"Walras's law: \ show that $p \cdot z(p) = 0$ for any prices, \ and that only relative prices matter.",
    r"The first welfare theorem: \ where does the proof use local nonsatiation? \ Give an economy where the "
    r"theorem fails without it.",
    r"The second theorem: \ find the transfer that makes the efficient point with 5 fish for Ana an equilibrium.",
    r"Scarf's economy: \ show that $\sum_k p_k^2$ and $p_1 p_2 p_3$ are constant along the auctioneer's path.",
    r"Arrow securities: \ with no aggregate risk and equal patience, \ show that complete markets give full "
    r"insurance, \ and find the securities' prices.",
    r"$\bigstar$ \ Kantorovich: \ write the dual of the boatyard's programme, \ and show that a machine works on a "
    r"part only if its day's value there equals the machine's price.",
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
        a = wrapped_label(r"It can, \ and it need not. \ An equilibrium in which every market clears exists for any "
                          r"economy of the kind Arrow and Debreu described, \ and it is efficient if every good has a "
                          r"price, \ nobody sets prices, \ and everyone knows what they are buying; \ in a large "
                          r"economy it is the only outcome no group can undo. \ But nothing guarantees there is one "
                          r"equilibrium, \ or that a market will find it, \ and efficient is not fair.", 11.6, 29,
                          WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = VGroup(cigarette(1.1), cigarette(1.1), cigarette(1.1)).arrange(DOWN, buff=0.08).next_to(a, DOWN,
                                                                                                   buff=0.45)
        with self.voiceover(
            "So: can a whole economy of selfish traders reach a state that nobody could improve on, and will it? "
            "<bookmark mark='a'/> It can, and it need not. An equilibrium where every market clears exists for "
            "any economy of the kind Arrow and Debreu described. It is efficient if every good has a price, nobody "
            "sets prices, and everyone knows what they're buying, and in a large economy it's the only outcome no "
            "group can undo. But nothing guarantees there is only one, or that a market will find it; and "
            "efficient is not the same as fair."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in logo], lag_ratio=0.3))
        self.clear_scene()

    def recap(self):
        b, c, f, s, i, k, r, d = (load(x) for x in ("box", "core", "fact", "simplex", "island", "plan", "risk",
                                                    "dial"))
        items = [
            (r"Radford's camp: \ one price where traders could read the boards", E.ACCENT),
            (r"the box: \ the lens of gains, \ and the contract curve where trade stops", CC),
            (rf"prices: \ offer curves cross at {b['p']:.3f} baskets a fish; \ Walras's law", PRICE),
            (rf"the core shrinks to the price outcome: \ Ana's fish {c['intervals']['20'][0]:.2f} to "
             rf"{c['intervals']['20'][1]:.2f} with 20 copies", CORE),
            (r"the first welfare theorem in five lines; \ its assumptions are Act IV", E.ACCENT),
            (r"the second: \ any efficient point, \ by a lump-sum transfer", ANA),
            (rf"existence: \ Brouwer, \ Sperner's colouring, \ Scarf's walk ({s['grids']['48']['walk']['rooms']} "
             rf"rooms)", CC),
            (r"stability: \ gross substitutes yes; \ Scarf's economy circles for ever", HOLD),
            (rf"the island cleared: \ Newton in {i['newton_iterations']} steps, \ the auctioneer in "
             rf"{i['auctioneer_steps']}", "#7BD88F"),
            (r"anything goes: \ three equilibria, \ and the Sonnenschein--Mantel--Debreu theorem", "#C9A0FF"),
            (rf"Arrow securities share risk; \ a bond alone does not; \ Kantorovich's {k['sets']:.0f} sets and "
             r"their prices", PLAN),
            (r"misallocation, \ contested; \ the NAFTA forecasts, \ wrong; \ equilibria on purpose", HOLD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 9, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del f, r, d
        with self.voiceover(
            "Part nine in twelve lines. <bookmark mark='a'/> Radford's camp found one price wherever traders could "
            "read the boards. In the box, the lens shows the gains from trade, and the contract curve where trade "
            "stops. Prices clear both markets where the offer curves cross, and Walras's law ties the markets "
            "together. As traders multiply, the core shrinks to the price outcome. The first welfare theorem takes "
            "five lines, and its assumptions are the next act; the second reaches any efficient point by a lump-sum "
            "transfer. Existence comes from Brouwer's theorem, or from Sperner's colouring and Scarf's walk. "
            "Stability holds for gross substitutes and fails in Scarf's economy. Newton's method cleared the island "
            "in six steps. Anything goes: several equilibria are possible, and the theory can't rule them out. "
            "Arrow's securities share risk that a bond alone cannot. Kantorovich found prices inside a plan. And "
            "misallocation is contested, the NAFTA forecasts were wrong, and equilibria are now computed on "
            "purpose to share courses fairly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The contract curve and the equilibrium price of the box, in general; Walras's law; where "
            "the first theorem's proof needs people to want more; the second theorem's transfer; the two conserved "
            "quantities of Scarf's cycle; Arrow securities with no aggregate risk; and a research problem, marked "
            "with a star, on the dual of Kantorovich's programme. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Andreu Mas-Colell, Michael Whinston and Jerry Green, \emph{Microeconomic Theory}, chs.\ 15--19",
             r"Gerard Debreu, \emph{Theory of Value} (1959)",
             r"David Kreps, \emph{Microeconomic Foundations I} (2013); \ Jehle and Reny, \emph{Advanced "
             r"Microeconomic Theory}, ch.\ 5",
             r"Herbert Scarf, \emph{The Computation of Economic Equilibria} (1973)"],
            [r"Radford (1945), \emph{Economica}; \ Edgeworth, \emph{Mathematical Psychics} (1881); \ Walras (1874)",
             r"Arrow and Debreu (1954); \ McKenzie (1954); \ Debreu and Scarf (1963); \ Aumann (1964)",
             r"Arrow, Block and Hurwicz (1959); \ Scarf (1960, 1967); \ Anderson, Plott, Shimomura and Granat (2004)",
             r"Sonnenschein (1973); \ Mantel (1974); \ Debreu (1974); \ Kirman (1992); \ Brown and Matzkin (1996)",
             r"Arrow (1953); \ Mises (1920); \ Lange (1936--37); \ Hayek (1945); \ Kantorovich (1939)",
             r"Hsieh and Klenow (2009); \ Bils, Klenow and Ruane (2021); \ Kehoe (2005, 2014)",
             r"Papadimitriou (1994); \ Daskalakis, Goldberg and Papadimitriou (2009); \ Shapley and Scarf (1974); "
             r"\ Budish (2011)"])
        with self.voiceover(
            "The reading: chapters fifteen to nineteen of Mas-Colell, Whinston and Green; Debreu's short Theory of "
            "Value; Kreps, and Jehle and Reny; and Scarf's Computation of Economic Equilibria. Then the papers, from Radford's camp to Budish's course market."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1849, r"Jules Dupuit, \ a French engineer", r"why railway companies left third-class "
                          r"carriages without roofs: \ not to save money, \ but to keep richer passengers paying "
                          r"for second class", color=E.ACCENT, width=10.4, font_size=24).move_to(UP * 1.2)
        nxt = VGroup(label(r"Next: \ Part 10 \ $\cdot$ \ Act III, Markets", font_size=30, color=GREY_B),
                     label(r"The Price Maker", font_size=46),
                     label(r"what does a seller do when the price is hers to set?", font_size=26, color=E.ACCENT)
                     ).arrange(DOWN, buff=0.22).next_to(hc, DOWN, buff=0.6)
        head = label(r"every theorem in this part: \ nobody sets the prices", font_size=30, color=GREY_A
                     ).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "Every theorem in this part assumed that nobody sets prices. <bookmark mark='a'/> Next time, a seller "
            "who does. A French engineer, Jules Dupuit, noticed that railway companies left their third-class "
            "carriages without roofs, not to save money but to keep the passengers who could afford second class "
            "from travelling third. <bookmark mark='b'/> Part ten: the price maker."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()
