from __future__ import annotations

from videos.psychology.psych9.common import *  # noqa: F403

PROBLEMS = [
    r"In a study of 250 identical and 250 fraternal pairs the correlations are .62 and .40. \ Give Falconer's three "
    r"shares. \ The standard error of each correlation is about $(1 - r^2)/\sqrt{n}$: \ can this study tell the shared "
    r"home's share from zero?",
    r"A trait has $a^2 = 0.6$ and no shared home, \ but spouses resemble each other, \ so fraternal twins share 0.6 of "
    r"A, not 0.5. \ What do the two twin correlations become, \ and what does Falconer's formula report?",
    r"In each of two fields the heritability of plant height is 0.9 and the variance is 1; \ the fields' means differ "
    r"by 3. \ What is the heritability in the two fields pooled, half from each? \ What does that say about pooling "
    r"populations?",
    r"A variant explains 0.02\% of the variance of a trait. \ How many people give an 80\% chance of detecting it at "
    r"$p < .05$? \ At $p < 5 \times 10^{-8}$? \ What is the chance with 300 people?",
    r"A genome-wide study makes $10^{6}$ independent tests of variants that do nothing. \ How many pass at $p < .05$? "
    r"\ At $p < 5 \times 10^{-8}$? \ A score predicts 14\% of a trait: \ what is the chance that someone in its top "
    r"tenth is above the median?",
    r"With \texttt{explainer.psychology.psyche.genes}: run \texttt{twin\_study} with \texttt{mz\_extra} from 0 to 0.6 "
    r"and plot Falconer's $h^2$. \ Then use \texttt{sibling\_design} to find the \texttt{nurture} that makes the "
    r"within-family effect 40\% smaller than the population effect.",
    r"$\star$ \ Design the study that would tell a direct effect of a child's genes from an effect of the home their "
    r"parents' genes made, \ and say what result would count against genetic nurture.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        tw, v, c, g = (load(k) for k in ("twins", "violate", "candidate", "gwas"))
        lee = archive.LEE_2018.data
        items = [
            (r"two Jims: \ a list chosen after looking proves nothing; \ a design fixed in advance can", MZC),
            (r"a family passes on genes and a home together; \ twins and adoption pull them apart", HOME),
            (r"many small genes make a bell curve; \ heritability is the genes' share of the variance", GENE),
            (rf"the twin formula, $h^2 = 2\,(r_{{\!I}} - r_{{\!F}})$: \ on the Pool, ${tw['est_h2']:.2f}$ for a planted "
             rf"${tw['a2']:.1f}$", GENE),
            (rf"its assumptions fail both ways: \ genes read as ${v['est_h2'][1]:.2f}$, \ or the home as "
             rf"${v['est_c2'][4]:.2f}$", BAD),
            (r"heritability is not fixedness, \ not about groups, \ not about you, \ not a constant", THRESH),
            (r"three laws: \ everything is heritable, \ the shared home counts for less, \ much is neither", DATA),
            (rf"candidate genes: \ 1{{,}}000 people had a {pct(c['power_1000'])} chance; \ the decade's findings failed", BAD),
            (rf"a million tests need $5 \times 10^{{-8}}$ and huge samples: \ 3 positions became "
             rf"{lee['okbay_snps']:,}".replace(",", "{,}"), GENE),
            (rf"a score predicts groups, not persons; \ between siblings its effect is {pct(lee['within_family_smaller'])} "
             r"smaller", GREY_A),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=32, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 9, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part nine in ten lines. <bookmark mark='a'/> A list of coincidences chosen after looking "
            "proves nothing, and a design fixed in advance can. A family passes on genes and a home "
            "together, and twins and adoption pull them apart. Many small genes add up to a bell curve, "
            "and heritability is the genes' share of the variance. The twin formula doubles the "
            "difference between two correlations, and on the Pool it gives back what we planted. Its "
            "assumptions fail in both directions: too much for the genes if identical twins are treated "
            "alike, too much for the home if parents' genes shape it. Heritability isn't fixedness, isn't "
            "about groups, isn't about you, and isn't a constant. Three laws: everything is heritable, "
            "the shared home counts for less, and much is neither. Candidate genes were tested in samples "
            "that couldn't have seen them, and the decade's findings failed. A million tests need a "
            "threshold of five in a hundred million and enormous samples, and then three positions became "
            "thousands. And a polygenic score predicts groups, not persons, and part of it is the home."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a variance shared out, a formula, a diagram fitted to data. \ And Fisher's prediction of 1918, many tiny "
             r"effects, confirmed position by position", STATUS_COLOR["replicated"]),
            (r"nature runs the experiments we cannot: \ two kinds of twins, \ adoption, \ and Mendel's lottery between "
             r"brothers and sisters", STATUS_COLOR["replicated"]),
            (r"an instrument that records without asking. \ But the analyst still chooses: \ a hundred thousand "
             r"tests are a hundred thousand forking paths", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today touches the second objection: that the mind can't be "
            "experimented on. You can't assign a child different genes, or a different family. But nature "
            "does. Twins come in two kinds. Adoption moves children between homes. And Mendel's lottery "
            "deals each brother and sister a random hand. They're experiments nobody designed, and each "
            "rests on assumptions that have to be checked, which is what chapter four was for. "
            "<bookmark mark='b'/> And on the first objection, that the mind admits no mathematics: here "
            "was a variance shared out, a formula in four lines, a diagram fitted to data. And a "
            "prediction. In 1918 Fisher's model said that traits like these must rest on very many genes "
            "of tiny effect. A century later, a million tests at a time, that's what was found."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"reasoning about cheats: \ an evolutionary claim, tested", [24]),
            (r"how people understand a risk", [26]),
            (r"temperament, and what parents do", [30]),
            (r"intelligence, its heritability, and the history of eugenics", [32]),
            (r"personality: \ what twins say and what families say", [33]),
            (r"attraction and mate preferences across cultures", [37]),
            (r"the genetics of depression, psychosis and addiction", [40, 41]),
            (r"path diagrams, fitted in earnest", [44]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Reasoning about cheats, an evolutionary claim put "
            "to the test, is Part 24. How people understand a risk is Part 26. Temperament, and what "
            "parents do, is Part 30. Intelligence, its heritability and the history of eugenics are Part "
            "32. Personality, and the gap between what twins say and what families say, is Part 33. "
            "Attraction across cultures is Part 37. The genetics of depression, psychosis and addiction "
            "are Parts 40 and 41. And path diagrams, fitted in earnest, begin in Part 44."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One applies "
            "the twin formula and asks what a study of that size can tell apart. One works out what "
            "assortative mating does to it. One pools Lewontin's two fields. One computes the samples that "
            "the candidate-gene studies needed. One counts the false alarms in a million tests, and asks "
            "what a score says about one person. One uses Psyche's genes module to break the twin design "
            "and to reproduce the gap inside families. And the last, with the star, is the frontier's "
            "problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"V. S. Knopik, J. M. Neiderhiser, J. C. DeFries \& R. Plomin, \emph{Behavioral Genetics} (7th ed., 2017)",
             r"K. P. Harden, \emph{The Genetic Lottery} (2021)",
             r"D. S. Falconer \& T. F. C. Mackay, \emph{Introduction to Quantitative Genetics} (4th ed., 1996)",
             r"D. J. Kevles, \emph{In the Name of Eugenics} (1985)"],
            [r"F. Galton (1875); \ R. A. Fisher (1918); \ T. J. Bouchard et al.\ (1990)",
             r"T. J. Bouchard \& M. McGue (1981); \ T. J. C. Polderman et al.\ (2015)",
             r"E. Turkheimer (2000); \ E. Turkheimer et al.\ (2003); \ C. M. A. Haworth et al.\ (2010)",
             r"A. Caspi et al.\ (2003); \ C. F. Chabris et al.\ (2012); \ R. Border et al.\ (2019)",
             r"C. A. Rietveld et al.\ (2013); \ J. J. Lee et al.\ (2018); \ A. Okbay et al.\ (2022)",
             r"A. Kong et al.\ (2018); \ L. J. Howe et al.\ (2022); \ A. R. Martin et al.\ (2019)",
             r"E. Karavani et al.\ (2019); \ D. M. Buss (1989); \ A. A. S. Weir et al.\ (2002)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Turkheimer's three "
            "laws take five pages, and they're the best five pages to start with."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"so far: \ the parts, a map, instruments, \ and where differences come from", font_size=26,
                      color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 10", font_size=32, color=GREY_B), label(r"Chemistry and Clocks", font_size=50),
                     wrapped_label(r"In 1938 two men live for a month in a cave, \ on a day of twenty-eight hours, \ to "
                                   r"see whether the body will follow. \ One of them adapts.", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So that's where the differences between people come from, as far as anyone can say: some "
            "from genes, less than you'd think from the home people share, and a good deal from neither. "
            "<bookmark mark='a'/> But a person also differs from themselves. The same mind isn't the same "
            "at four in the afternoon and at four in the morning, after a coffee, or after a week of bad "
            "sleep. The brain sits in a body with rhythms, hormones and drugs. <bookmark mark='b'/> In "
            "1938 a physiologist and his student went down into a cave in Kentucky and lived there for a "
            "month, on a day of twenty-eight hours, to see whether the body would follow the clock on the "
            "wall. One of them adapted. The other couldn't. Why, and what it tells us about the clock "
            "inside, is Part 10: chemistry and clocks."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
