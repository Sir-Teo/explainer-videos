from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

PROBLEMS = [
    r"The guessing game: \ with $n \ge 2$ players choosing from $[0, 100]$ and $p < 1$, \ show that everyone choosing 0 "
    r"is the only Nash equilibrium.",
    r"The penalty: \ for scoring chances $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$, \ find both mixtures by "
    r"indifference, \ and check 0.383, \ 0.417 and 0.796 for chapter 5's numbers.",
    r"The battle of the sexes: \ find all three equilibria, \ and show the mixed one gives each player less than "
    r"either pure one.",
    r"Entry: \ find every Nash equilibrium of chapter 6's game in strategic form, \ and show that only one is "
    r"subgame perfect.",
    r"Tit for tat: \ with Axelrod's payoffs, \ show that tit for tat against itself is an equilibrium only if "
    r"$\delta \ge \tfrac{T-R}{R-S} = \tfrac{2}{3}$.",
    r"The traffic light: \ check that the distribution $(0, \tfrac14, \tfrac14, \tfrac12)$ on chicken satisfies "
    r"every obedience constraint, \ and gives each driver 5.25.",
    r"Rubinstein: \ with patience $\delta$ for both, \ derive the first proposer's share $\frac{1}{1+\delta}$.",
    r"$\bigstar$ \ The cognitive hierarchy: \ find level 2's choice for $\tau = 1.5$, \ and show that the "
    r"population's mean falls as $\tau$ rises.",
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
        a = wrapped_label(r"Each predicts the others, \ and an equilibrium is where those predictions come true: \ "
                          r"nobody can do better alone. \ Selfishness can trap everyone, \ as in the prisoner's "
                          r"dilemma, \ but a future worth protecting, \ the ability to see each other's moves, \ and "
                          r"forgiveness can sustain cooperation. \ Real people reason only a step or two ahead the "
                          r"first time, \ and learn their way toward equilibrium.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = VGroup(islander("ana", 0.9), islander("bo", 0.9)).arrange(RIGHT, buff=0.9).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: what happens when my best choice depends on yours, and yours on mine? <bookmark mark='a'/> Each of "
            "us predicts the other, and an equilibrium is where those predictions come true, so that nobody can do "
            "better alone. Selfishness can trap everyone, as in the prisoner's dilemma. But a future worth "
            "protecting, the ability to see what the other does, and a little forgiveness can sustain cooperation. "
            "And real people reason only a step or two ahead the first time, and learn their way toward equilibrium."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        g, p, c, lk = (load(x) for x in ("guess", "penalty", "correlated", "levelk"))
        items = [
            (r"Flood and Dresher's hundred rounds: \ 60 cooperative, \ 14 as Nash predicted", COOP),
            (rf"the guessing game: \ 0 in theory; \ {g['nagel']['mean']:.1f} and {g['ft']['mean']:.1f} on average in "
             r"practice", ANA),
            (r"dominance, \ and its iteration: \ one more layer of knowledge each round", LEVEL),
            (r"Nash equilibrium: \ best responses that cross; \ it always exists", EQ),
            (r"coordination, \ battle, \ chicken, \ stag hunt: \ several equilibria, \ and trust", COOP),
            (rf"mixing: \ the penalty kick scores {100 * p['value']:.1f}\% whichever way; \ professionals mix", BO),
            (r"backward induction, \ subgame perfection, \ empty threats", DEFECT),
            (r"the centipede and the ultimatum game: \ people pass, \ and offer near half", "#F2A65A"),
            (r"repetition: \ $\delta \ge \tfrac12$ sustains cooperation; \ the folk theorem allows almost anything",
             COOP),
            (r"Axelrod: \ nice, \ retaliatory, \ forgiving; \ with mistakes, \ win-stay, lose-shift wins", EQ),
            (rf"focal points, \ the traffic light's {c['ce']:.2f}, \ evolution, \ learning", "#F2C14E"),
            (rf"levels of thinking: \ $\tau \approx$ {lk['tau_nagel']:.1f} to {lk['tau_ft']:.1f}; \ machines "
             r"that solve poker", LEVEL),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 11, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part eleven in twelve lines. <bookmark mark='a'/> Flood and Dresher's players cooperated in sixty of a "
            "hundred rounds, against the theory. The guessing game's equilibrium is nought, but people average "
            "between about twenty and forty. Dominance rules out bad choices, one layer of knowledge at a time. A "
            "Nash equilibrium is where best responses cross, and one always exists. Coordination, the battle of the "
            "sexes, chicken and the stag hunt have several equilibria each, and the best may need trust. Mixed "
            "strategies leave the other side indifferent, and professional footballers play them. Backward induction "
            "rules out empty threats. In the centipede and the ultimatum game, people pass, and offer close to half. "
            "Repetition sustains cooperation when the future matters enough, and the folk theorem allows almost "
            "anything. Axelrod's winners were nice, retaliatory and forgiving, and with mistakes, win-stay, "
            "lose-shift did best. Focal points and traffic lights pick among equilibria; evolution and learning can "
            "find them, or circle them. And people think one to four steps ahead, while machines now solve poker."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Why nought is the guessing game's only equilibrium; the penalty kick's mixtures; the "
            "battle of the sexes; the entry game's two equilibria; when tit for tat is an equilibrium; the traffic "
            "light's obedience constraints; Rubinstein's split; and a starred problem on the cognitive hierarchy. "
            "Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Martin Osborne, \emph{An Introduction to Game Theory} (2004); \ Osborne and Rubinstein, \emph{A Course "
             r"in Game Theory} (1994)",
             r"Drew Fudenberg and Jean Tirole, \emph{Game Theory} (1991), chs.\ 1--5; \ Robert Gibbons, \emph{A "
             r"Primer in Game Theory} (1992)",
             r"Thomas Schelling, \emph{The Strategy of Conflict} (1960); \ Robert Axelrod, \emph{The Evolution of "
             r"Cooperation} (1984)",
             r"Colin Camerer, \emph{Behavioral Game Theory} (2003); \ Martin Nowak, \emph{Evolutionary Dynamics} "
             r"(2006)"],
            [r"von Neumann (1928); \ Nash (1950, 1951); \ Flood (1952); \ Selten (1965, 1978); \ Harsanyi (1967--68)",
             r"Aumann (1974); \ Maynard Smith and Price (1973); \ Brown (1951); \ Robinson (1951); \ Shapley (1964)",
             r"Friedman (1971); \ Rubinstein (1982); \ Kreps, Milgrom, Roberts and Wilson (1982); \ Fudenberg and "
             r"Maskin (1986)",
             r"Axelrod (1980); \ Nowak and Sigmund (1993); \ Rosenthal (1981); \ McKelvey and Palfrey (1992)",
             r"G\"uth, Schmittberger and Schwarze (1982); \ Henrich et al.\ (2001); \ Nagel (1995); \ Stahl and Wilson "
             r"(1994)",
             r"Camerer, Ho and Chong (2004); \ Chiappori, Levitt and Groseclose (2002); \ Palacios-Huerta (2003); \ "
             r"Walker and Wooders (2001)",
             r"Hart and Mas-Colell (2000); \ Erev and Roth (1998); \ Bowling et al.\ (2015); \ Brown and Sandholm "
             r"(2018, 2019)"])
        with self.voiceover(
            "The reading: Osborne's introduction, and Osborne and Rubinstein's course; the first five chapters of "
            "Fudenberg and Tirole, and Gibbons's primer; Schelling's Strategy of Conflict and Axelrod's Evolution of "
            "Cooperation; and Camerer's Behavioral Game Theory. Then the papers, from von Neumann to the poker "
            "programs."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1992, r"Archer Daniels Midland, \ and an informant", r"for three years the FBI secretly "
                          r"films executives from America, \ Japan and Korea \\ agreeing on the world price of lysine, \ "
                          r"an animal-feed additive", color=E.ACCENT, width=10.4, font_size=24).move_to(UP * 1.2)
        nxt = VGroup(label(r"Next: \ Part 12 \ $\cdot$ \ Act III, Markets", font_size=30, color=GREY_B),
                     label(r"Competition among the Few", font_size=46),
                     label(r"how do a handful of firms compete, \ and when do they stop?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"Ana and Bo played for fish; \ firms play for markets", font_size=30, color=GREY_A
                     ).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "Ana and Bo played for fish. Firms play for markets. <bookmark mark='a'/> Next time, a repeated game "
            "caught on tape: from 1992, with the help of an informant inside the company, the FBI secretly filmed "
            "executives of Archer Daniels Midland and their rivals from Japan and Korea agreeing on the world price "
            "of lysine, an additive for animal feed. <bookmark mark='b'/> Part twelve: competition among the few."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()
