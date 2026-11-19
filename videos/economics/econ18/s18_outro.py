from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403

PROBLEMS = [
    r"Five rules: \ with the island's 38 ballots, \ find the winner under plurality, \ the runoff, \ instant runoff, "
    r"\ Borda's count \ and Condorcet's head-to-head rule.",
    r"The agenda: \ with Condorcet's three voters, \ show that whichever plan is voted on last wins.",
    r"Arrow, \ step one: \ prove that if every voter puts $b$ at the very top or the very bottom, \ so does society.",
    r"Black's theorem: \ with single-peaked preferences on a line, \ prove that the median peak beats every other "
    r"option.",
    r"Strategy: \ find a lie by the 12 fish-first islanders that changes Borda's winner to one they prefer.",
    r"Atkinson: \ for incomes 5, \ 10, \ 20, \ 40, \ 80, \ find the equally distributed equivalent at "
    r"$\varepsilon = 0, 1, 2$, \ and its limit as $\varepsilon \to \infty$.",
    r"The veil: \ find the $\varepsilon$ at which Harsanyi's chooser switches from society B to society A.",
    r"$\bigstar$ \ Scitovsky: \ verify that the compensation test approves the move from state 1 to state 2 \ and the "
    r"move back.",
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
        a = wrapped_label(r"Not without a choice. \ Between two options, \ or along one line, \ majority rule works; "
                          r"\ beyond that, \ every rule breaks a reasonable condition, \ and every rule can be gamed. "
                          r"\ To add people up we must compare them: \ welfare functions, \ cost-benefit analysis and "
                          r"indices do, \ but each carries an ethical number, \ how much we care about equality, \ "
                          r"about the future, \ about a risk to life, \ that economics can make visible and measure "
                          r"the effects of, \ but cannot choose.", 11.6, 28, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = VGroup(*[islander(k, 0.75) for k in ("ana", "bo", "chidi", "dara", "friday")]).arrange(
            RIGHT, buff=0.3).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: can the wants of many people be added up into what society wants? <bookmark mark='a'/> Not without "
            "a choice. Between two options, or along a single line, majority rule works. Beyond that, every rule "
            "breaks some reasonable condition, and every rule can be gamed. To add people up, we have to compare "
            "them. Welfare functions, cost-benefit analysis and indices do, but each carries an ethical number: how "
            "much we care about equality, about the future, about a risk to life. Economics can make that number "
            "visible and measure what follows from it. It cannot choose it for us."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        w, v = load("welfare"), load("vsl")
        items = [
            (r"Condorcet, \ 1785: \ majorities can go in circles", CYCLE),
            (r"Play it: \ 38 ballots, \ five rules, \ five winners", VOTE["A"]),
            (r"Borda against Condorcet; \ independence broken; \ whoever sets the agenda picks the winner", VOTE["B"]),
            (r"Arrow: \ no rule meets four modest conditions; \ the pivotal voter becomes a dictator", RULE),
            (r"single peaks: \ the median voter wins; \ May: \ between two, \ majority rule", WELF),
            (r"Gibbard and Satterthwaite: \ every rule can be gamed; \ Duverger's two parties", VOTE["D"]),
            (r"what we may compare decides which rules survive", E.ACCENT),
            (rf"Bentham to Rawls: \ Atkinson's $\varepsilon$; \ at 1 the island is worth {w['table']['1.0']:.0f}, "
             rf"\ not {w['mean']:.0f}", WELF),
            (r"two veils: \ Harsanyi's average, \ Rawls's minimum, \ one number apart", RAWLS),
            (r"Pareto's limits: \ Scitovsky's reversal; \ the Paretian liberal", CYCLE),
            (rf"cost-benefit: \ weights and discount rates; \ a statistical life, \ \${v['vsl'] / 1e6:.0f} million, "
             rf"\ contested", MONEY),
            (r"capabilities and the HDI; \ behavioural welfare, \ quadratic votes, \ Borda inside machines", LIFE),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 18, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part eighteen in twelve lines. <bookmark mark='a'/> In 1785 Condorcet found that majorities can go in "
            "circles. In Play it, thirty-eight ballots gave five winners under five rules. Borda's count breaks "
            "independence, and whoever sets the agenda picks the winner. Arrow proved that no rule meets four modest "
            "conditions, and the proof finds a pivotal voter who becomes a dictator. With single-peaked preferences "
            "the median voter wins, and between two options May's theorem picks majority rule. Gibbard and "
            "Satterthwaite showed every rule can be gamed, and Duverger saw two parties in it. What we are willing "
            "to compare across people decides which rules survive. From Bentham to Rawls runs Atkinson's family: at "
            "epsilon one, the island's incomes are worth an equal twenty each, not thirty-one. Harsanyi's veil "
            "chooses the average, Rawls's the minimum, and they are one number apart. Pareto's criterion has limits: "
            "Scitovsky's reversal and the Paretian liberal. Cost-benefit analysis needs weights and a discount rate, "
            "and a statistical life is valued at around ten million dollars, a contested number. And capabilities "
            "and the human development index, behavioural welfare, quadratic votes and Borda's count inside "
            "machines are where the field is moving."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The five rules on the island's ballots; the agenda; the first step of Arrow's proof; "
            "Black's median voter theorem; a strategic lie under Borda's count; Atkinson's equivalent incomes; the "
            "switch behind Harsanyi's veil; and a starred problem on Scitovsky's reversal. Full solutions are in the "
            "part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Kenneth J.\ Arrow, \emph{Social Choice and Individual Values} (1951; 3rd ed.\ 2012)",
             r"Amartya Sen, \emph{Collective Choice and Social Welfare} (1970; expanded ed.\ 2017)",
             r"Mas-Colell, Whinston and Green, \emph{Microeconomic Theory} (1995), chs.\ 21--22",
             r"Matthew Adler, \emph{Measuring Social Welfare} (2019)"],
            [r"Condorcet (1785); \ Black (1948); \ May (1952); \ Downs (1957); \ McKelvey (1976)",
             r"Gibbard (1973); \ Satterthwaite (1975); \ Duverger (1951); \ Riker (1982)",
             r"Robbins (1932); \ Hammond (1976); \ d'Aspremont and Gevers (1977); \ Geanakoplos (2005)",
             r"Harsanyi (1953, 1955, 1975); \ Rawls (1971); \ Atkinson (1970); \ Okun (1975)",
             r"Kaldor (1939); \ Hicks (1939); \ Scitovsky (1941); \ Sen (1970); \ Kaplow and Shavell (1994)",
             r"Schelling (1968); \ Thaler and Rosen (1976); \ Ashenfelter and Greenstone (2004); \ Ravallion (2012)",
             r"Bernheim and Rangel (2009); \ Lalley and Weyl (2018); \ Conitzer et al.\ (2024)"])
        with self.voiceover(
            "The reading: Arrow's Social Choice and Individual Values, short and still fresh; Sen's Collective "
            "Choice and Social Welfare, in its expanded edition; the social choice and welfare chapters of "
            "Mas-Colell, Whinston and Green, the graduate text; and Matthew Adler's Measuring Social Welfare. Then "
            "the papers, from Condorcet to choosing for machines."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1798, r"the Reverend Thomas Malthus", r"population, \ unchecked, \ outruns food: \ living "
                          r"standards can never rise for long", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 19 \ $\cdot$ \ Act V, \ The Long Run", font_size=30, color=GREY_B),
                     label(r"The Great Escape", font_size=46),
                     label(r"why was almost everyone poor for almost all of history, \ and what changed?",
                           font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"Act IV asked when markets fail and how to design around them; \ Act V asks how economies grow",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "That ends Act Four, on markets that fail and the designs that can mend them. Act Five asks how "
            "economies grow. <bookmark mark='a'/> In 1798 the Reverend Thomas Malthus explained why living standards "
            "can never rise for long: population, unchecked, outruns food. As a description of every century before "
            "his, the theory was good. <bookmark mark='b'/> Part nineteen: the great escape."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
