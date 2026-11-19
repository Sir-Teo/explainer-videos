from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

PROBLEMS = [
    r"The Boston rule: \ with the four children's lists and the lottery, \ show that you get the net loft by "
    r"telling the truth \ and the kiln by listing it first; \ find the blocking pair.",
    r"Deferred acceptance: \ run the apprentices' board with workshops asking, \ and check that every workshop "
    r"prefers the result to the apprentices' version.",
    r"Stability: \ prove that deferred acceptance ends with a stable matching, \ and that it is the asking side's "
    r"best.",
    r"Clarke's rule: \ for the footbridge, \ find who is pivotal and the taxes; \ show Bo cannot gain by reporting "
    r"60 instead of 10.",
    r"Myerson and Satterthwaite: \ with values and costs uniform on $[0, 1]$, \ compute the gains from trade "
    r"under full efficiency, \ a posted price of $\tfrac12$ and the rule $v \ge c + \tfrac14$.",
    r"Top trading cycles: \ run it on the four huts, \ and show that no coalition can do better by trading among "
    r"itself.",
    r"The assignment game: \ find the core of the two boats and two buyers, \ and the competitive prices at each end.",
    r"$\bigstar$ \ What a lottery reveals: \ with offers random within types, \ show that 2SLS with type controls "
    r"recovers a constant effect, \ and why the comparison that ignores types does not.",
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
        a = wrapped_label(r"Yes, \ within limits. \ A clearinghouse can make a market thick, \ uncongested and safe: \ "
                          r"deferred acceptance finds a match no pair wants to break, \ and makes the truth safe for "
                          r"the side that asks; \ swaps and chains find kidneys no price could. \ No rule does "
                          r"everything, \ some trades are always lost to private information, \ and a design works only "
                          r"if people trust it and it fits them.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = VGroup(*[islander(k, 0.75) for k in ("ana", "bo", "chidi", "dara")]).arrange(RIGHT, buff=0.3).next_to(
            a, DOWN, buff=0.45)
        with self.voiceover(
            "So: can a market be engineered, when prices cannot do the work? <bookmark mark='a'/> Yes, within "
            "limits. A clearinghouse can make a market thick, uncongested and safe. Deferred acceptance finds a "
            "match that no pair wants to break, and makes the truth safe for the side that asks; swaps and chains "
            "find kidneys that no price could. But no rule does everything, some good trades are always lost when "
            "values are private, and a design works only if the people in it trust it, and it fits them."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        r, lt, kd, tr = load("roth"), load("lottery"), load("kidneys"), load("trade")
        items = [
            (r"interns hired two years early; \ exploding offers; \ a clearinghouse in 1952", REJECT),
            (r"Play it: \ the Boston rule punished the truth; \ deferred acceptance did not", YOU),
            (r"the revelation principle: \ look only at rules where truth is safe", MECH),
            (r"Clarke's rule: \ pay for the harm you do; \ the budget can't balance", MONEY),
            (rf"no perfect bargain: \ {tr['share']['double'] * 100:.0f}\% of the gains at best", HELD),
            (r"Gale and Shapley: \ a stable matching always exists; \ the asking side gets its best", STABLE),
            (r"Britain's test: \ stable clearinghouses survived; \ couples and the 1998 redesign", STABLE),
            (rf"school choice: \ Boston's switch; \ New York's {r['nyc']['unassigned_before']:,} unplaced fell to "
             rf"{r['nyc']['unassigned_after']:,}".replace(",", "{,}"), SCHOOL),
            (rf"huts and kidneys: \ trading cycles; \ cycles and a chain gave all {kd['with_chains']} patients a kidney",
             KIDNEY),
            (r"thick, \ uncongested, \ safe; \ unravelling; \ repugnance", REJECT),
            (r"the assignment game: \ matching with money, \ a lattice of prices", MONEY),
            (r"lotteries as experiments; \ the elite illusion; \ refugees; \ cutoffs as prices", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 17, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part seventeen in twelve lines. <bookmark mark='a'/> The interns' market unravelled and then "
            "congested, until a clearinghouse in 1952 fixed it. In Play it, the Boston rule punished you for telling "
            "the truth, and deferred acceptance did not. The revelation principle says a designer may look only at "
            "rules where the truth is safe. Clarke's rule makes the truth pay by charging for the harm you do, but "
            "its budget cannot balance. No bargain between a buyer and a seller with private values gets every good "
            "trade done: eighty-four percent of the gains is the best. Gale and Shapley proved a stable matching "
            "always exists, and the asking side gets its best. In Britain, the stable clearinghouses survived, and "
            "couples forced the doctors' redesign of 1998. Boston changed its rule, and in New York the thirty "
            "thousand unplaced pupils fell to three thousand. Trading cycles share out huts, and cycles and a chain "
            "found a kidney for every patient in Agora's pool. A marketplace must be thick, uncongested and safe, and "
            "it can unravel or meet repugnance. With money, matching becomes the assignment game, with a lattice of "
            "prices. And a match's lotteries are experiments, the elite schools are an illusion, refugees can be "
            "placed better, and in large markets cutoffs work like prices."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The Boston rule and its blocking pair; the board with workshops asking; the proof of "
            "stability; Clarke's rule for the footbridge; the gains from trade under three rules; top trading "
            "cycles; the core of the assignment game; and a starred problem on what a lottery reveals. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Alvin E. Roth, \emph{Who Gets What and Why} (2015)",
             r"Alvin E. Roth and Marilda Sotomayor, \emph{Two-Sided Matching} (1990)",
             r"Tilman Börgers, \emph{An Introduction to the Theory of Mechanism Design} (2015)",
             r"Nisan, Roughgarden, Tardos and Vazirani, \emph{Algorithmic Game Theory} (2007), chs.\ 9--10"],
            [r"Gale and Shapley (1962); \ Shapley and Shubik (1971); \ Shapley and Scarf (1974)",
             r"Vickrey (1961); \ Clarke (1971); \ Groves (1973); \ Green and Laffont (1977); \ Myerson (1979)",
             r"Myerson and Satterthwaite (1983); \ Chatterjee and Samuelson (1983); \ Dubins and Freedman (1981)",
             r"Roth (1982, 1984, 1991, 2002, 2007, 2008); \ Roth and Peranson (1999); \ Kagel and Roth (2000)",
             r"Abdulkadiroğlu and Sönmez (2003); \ Abdulkadiroğlu, Pathak and Roth (2005); \ Chen and Kesten (2017)",
             r"Roth, Sönmez and Ünver (2004); \ Rees et al.\ (2009); \ Kojima and Pathak (2009); \ Azevedo and "
             r"Leshno (2016)",
             r"Abdulkadiroğlu, Angrist and Pathak (2014); \ Abdulkadiroğlu, Angrist, Narita and Pathak (2017); \ "
             r"Bansak et al.\ (2018)"])
        with self.voiceover(
            "The reading: Alvin Roth's Who Gets What, and Why, for everyone; Roth and Marilda Sotomayor's Two-Sided "
            "Matching, the graduate text; Tilman Börgers on mechanism design; and the chapters on mechanism design "
            "in Algorithmic Game Theory. Then the papers, from Gale and Shapley to the refugees."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1785, r"the Marquis de Condorcet", r"a majority can prefer A to B, \ B to C, \ and C to A",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 18 \ $\cdot$ \ Act IV, \ Failure and Design", font_size=30, color=GREY_B),
                     label(r"Social Choice and Welfare", font_size=46),
                     label(r"can the wants of many people be added up into what society wants?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ matching people one by one; \ next: \ choosing for everyone at once", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part matched people one by one. The next chooses for everyone at once. "
            "<bookmark mark='a'/> In 1785 the Marquis de Condorcet found that a majority can prefer A to B, B to C, "
            "and C to A. <bookmark mark='b'/> Part eighteen: social choice and welfare."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
