from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403
from videos.economics.econ5.s01_hook import receipt_glyph

PROBLEMS = [
    r"Bo's receipts: \ prices $(4, 3)$, $(2, 4)$, $(6, 2)$; \ bundles $(3, 8)$, $(6, 6)$, $(4, 6)$; \ \$36 each "
    r"week. \ Find every direct revealed preference, \ the WARP violation, \ and Afriat's index.",
    r"$u = x^{0.6} y^{0.4}$, \ $p_x = 4$, \ $p_y = 3$, \ $m = 60$. \ Find the best bundle, \ the MRS there, \ and "
    r"$\lambda$. \ Show that doubling every price and income changes nothing.",
    r"CES with weights $\tfrac12$ and $\sigma = 2$; \ $p_x = 1$, \ $p_y = 4$, \ $m = 10$. \ Find the bundle. \ By "
    r"how much does $x/y$ change if $p_y$ doubles?",
    r"Ana: \ $u = \min(x, y)$; \ Chidi: \ $u = x + 1.2\,y$. \ Fish \$6, coconuts \$10, \ \$60. \ What does each "
    r"buy? \ Below what coconut price does Chidi switch?",
    r"Coconuts: \ \$2 each for the first 6, \ then \$1; \ fish \$2; \ Bo spends half on each. \ At what income does "
    r"he jump past the sixth coconut, \ and from how many to how many?",
    r"The EITC subsidizes earnings at 34\% up to \$8{,}580. \ Earners have $z = n\,r^{e}$ for a net reward $r$. "
    r"\ With potential earnings $n$ uniform on \$4{,}000--\$14{,}000, \ what share bunch at the kink when "
    r"$e = 0.25$, \ and when $e = 1$?",
    r"Becker: \ each household spends a uniform random share of $m$ on $x$. \ Show that market demand is "
    r"$m/(2p)$ per household, \ with price elasticity $-1$, \ although no household obeys WARP.",
    r"$\bigstar$ \ Design eleven budgets that catch as many random choosers as possible, \ and also catch "
    r"Cobb--Douglas choosers with a 5\% tremble. \ Are the two goals in conflict?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = label(ASK, font_size=50, color=E.ACCENT).move_to(UP * 1.8)
        a = wrapped_label(r"Yes, \ as far as the choices are consistent: \ if they satisfy GARP, \ a utility function "
                          r"explains them all, \ and the data bound how someone trades one thing for another. \ Not "
                          r"why they want it, \ and only where the budgets crossed.", 11.5, 32, WHITE)
        a.next_to(q, DOWN, buff=0.6)
        logo = receipt_glyph(0.7).next_to(a, DOWN, buff=0.5)
        with self.voiceover(
            "So: can you tell what someone wants from what they buy? <bookmark mark='a'/> Yes, as far as their "
            "choices are consistent. If they satisfy GARP, some utility function explains every one of them, and the "
            "choices themselves bound how the person trades one thing for another. They won't tell you why the "
            "person wants it, and they only speak where the budgets crossed."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo.paper), LaggedStart(*[Create(x) for x in logo.lines], lag_ratio=0.2))
        self.clear_scene()

    def recap(self):
        r, t, bu, cr, ch, b, st, am, f = (load(x) for x in ("receipts", "tangency", "bulk", "credit", "choosers",
                                                             "bronars", "studies", "america", "ferry"))
        items = [
            (rf"Bo's receipts: \ weeks 1 and 3 contradict each other; \ index {r['ccei']:.3f}", VIOL),
            (r"tastes are a ranking: \ complete, transitive, continuous; \ cycles get pumped", IC),
            (r"utility is a label: \ only the order counts, \ and the MRS survives relabelling", E.ACCENT),
            (r"shapes: \ substitutes, complements, Cobb--Douglas, \ and CES between them", "#C9A0FF"),
            (rf"the tangency: \ MRS = price ratio; \ $\lambda = {t['lam']:.3f}$, \ the value of a dollar", BUDGET),
            (rf"a bulk price makes demand jump \ (at \${bu['tie']:.2f}); \ a tax credit's kink makes people bunch",
             COCO),
            (rf"random choosers fail GARP {100 * b['power']:.1f}\% of the time on our eleven lines", RANDOM),
            (rf"children: \ 4.3 contradictions at 7, \ 2.1 at 11; \ Dutch adults: \ index "
             rf"{st['ckms2014']['mean_ccei']:.2f}", IC),
            (rf"America, 1929--2025: \ no GARP violations, \ but no power within decades", E.ACCENT),
            (r"rationality assumes neither selfishness nor calculation; \ Becker's random demand slopes down", PASS),
            (rf"from 2{{,}}000 ferry choices, \ the value of time: \ \${f['vot']:.2f} an hour", E.TRUTH),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {txt}", font_size=30, color=col) for i, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 5, \ in eleven lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part five in eleven lines. <bookmark mark='a'/> Bo's receipts contradicted each other, by about six "
            "percent of a week's money. Tastes are a ranking, and rankings that go round in circles get pumped. "
            "Utility is a label: only its order counts, and the rate of trade survives any relabelling. Four shapes, "
            "and the CES family between them, cover most tastes. The best bundle sets the rate of trade equal to the "
            "price ratio, and the multiplier is the value of a dollar. Bulk prices make demand jump, and tax "
            "credits make people bunch. On our eleven lines random choosers almost always fail; children and adults "
            "mostly pass. America's spending passes too, but the test can't see inside a decade. Rationality "
            "assumes neither selfishness nor calculation, and budgets alone make demand slope down. And a logit "
            "read the value of time from two thousand ferry choices."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=34.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Bo's receipts, scored by hand; a Cobb–Douglas consumer and her multiplier; a CES "
            "consumer when a price doubles; Ana and Chidi at a corner; the income at which a bulk price makes Bo "
            "jump; how many earners bunch at a credit's kink; why Becker's random households have a demand curve; "
            "and a research problem, marked with a star, on designing the most powerful eleven budgets. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Hal Varian, \emph{Intermediate Microeconomics}, chs.\ 2--7",
             r"Andreu Mas-Colell, Michael Whinston and Jerry Green, \emph{Microeconomic Theory}, chs.\ 1--3",
             r"David Kreps, \emph{Microeconomic Foundations I}, chs.\ 1--4; \ Jehle and Reny, \emph{Advanced "
             r"Microeconomic Theory}, ch.\ 1",
             r"Christopher Chambers and Federico Echenique, \emph{Revealed Preference Theory} (2016)"],
            [r"Samuelson (1938), \emph{Economica} 5; \ Houthakker (1950), \emph{Economica} 17; \ Debreu (1954)",
             r"Afriat (1967), \emph{IER} 8; \ Varian (1982), \emph{Econometrica} 50; \ Bronars (1987)",
             r"Becker (1962), \emph{JPE} 70; \ Harbaugh, Krause and Berry (2001); \ Andreoni and Miller (2002)",
             r"Choi et al.\ (2007, 2014), \emph{AER}; \ Saez (2010); \ Blundell, Browning and Crawford (2008)",
             r"McFadden (1974); \ Kitamura and Stoye (2018); \ Chen, Liu, Shan and Zhong (2023), \emph{PNAS}"])
        with self.voiceover(
            "The reading for this part: the consumer chapters of Hal Varian's intermediate textbook; the first three "
            "chapters of Mas-Colell, Whinston and Green for the graduate version; Kreps, and Jehle and Reny; and "
            "Chambers and Echenique's monograph on revealed preference. Then the papers, from Samuelson's note to "
            "the experiments, the kinks and the machines."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2006, r"Robert Jensen and Nolan Miller, \ Hunan province, China",
                          r"they subsidize rice for poor households, \ and many buy less rice, \ not more: \ a "
                          r"Giffen good, \ explained by an equation Slutsky wrote in 1915", color=E.ACCENT, width=9.0,
                          font_size=26).move_to(UP * 0.6)
        lead = label(r"from one choice \ to a change of price", font_size=40, color=GREY_A)
        nxt = VGroup(label(r"Next: \ Part 6", font_size=30, color=GREY_B),
                     label(r"Demand", font_size=56, color=WHITE),
                     label(r"when a price changes, \ what happens to what people buy, \ and to how well off they "
                           r"are?", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "This part asked what a single choice reveals. The next asks what happens when a price changes. "
            "<bookmark mark='a'/> In 2006 Robert Jensen and Nolan Miller subsidized rice for poor households in "
            "Hunan, in China, and many of them bought less rice, not more. A good whose demand rises with its "
            "price, long thought a textbook curiosity, was there in the data, and the equation that explains it was "
            "written by Eugen Slutsky in 1915. <bookmark mark='b'/> Part six: demand."
        ) as vo:
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeOut(lead), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
