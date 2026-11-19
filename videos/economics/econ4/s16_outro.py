from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

PROBLEMS = [
    r"Demand is $q = 100 - 2p + u$ and supply $q = 20 + 3p + v$, \ with $\operatorname{var}(u) = 4$, \ "
    r"$\operatorname{var}(v) = 1$, \ independent. \ To what does the least-squares slope of $q$ on $p$ converge? \ "
    r"Which curve would it find if $u$ never moved?",
    r"Storms cut the Island's supply by 80 fish at every price, \ and also keep 10 fish' worth of buyers at home. \ "
    r"With demand $dq/dp = -66.7$ and supply $dq/dp = 88.9$, \ what does the storm's Wald ratio estimate? \ Which "
    r"assumption failed?",
    r"$\log w = \alpha + 0.08\,S + 0.10\,A + e$, \ $\operatorname{cov}(S, A) = 1.5$, \ $\operatorname{var}(S) = 5.5$. "
    r"\ Find the probability limit of least squares. \ Now years of school are reported with an error of variance 1. "
    r"\ What does least squares find now?",
    r"NSW trainees earned \$2{,}096 in 1974, \$1{,}532 in 1975 and \$6{,}349 in 1978; \ the survey men \$5{,}619, "
    r"\$2{,}466 and \$6{,}984. \ Compute the raw comparison, \ and two differences in differences, \ from 1974 and "
    r"from 1975. \ The experiment said \$1{,}794. \ What went wrong?",
    r"A low lottery number raises the chance of serving from 0.20 to 0.36, \ and lowers average earnings by \$400. "
    r"\ Estimate the effect of service. \ For whom is it the effect?",
    r"$y = 100 + 0.8\,(\pi - E\pi)$, \ $E_t = E_{t-1} + 0.5\,(\pi_{t-1} - E_{t-1})$, \ $E = 2$ in the calm years. \ "
    r"The council holds $\pi = 8$ from now on. \ Find output in each of the first four years, \ and compare the "
    r"menu's promise.",
    r"Earnings have $\sigma = 0.4$; \ half the sample is offered a place. \ How many people do you need to detect an "
    r"effect of 0.05 with 80\% power at the 5\% level? \ And if only 30\% of those offered take it up?",
    r"$\bigstar$ \ Design the Island's next village trial: \ how many villages, \ at what shares, \ to detect a "
    r"spillover of $-0.04$ per unit share with 80\% power?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = label(ASK, font_size=54, color=E.ACCENT).move_to(UP * 1.8)
        a = wrapped_label(r"When something moved one thing and nothing else: \ a storm, \ a lottery, \ a birthday, \ "
                          r"a border. \ Find it, \ or make it; \ say what it moved, \ and for whom; \ and ask whether "
                          r"the answer will survive the policy it informs.", 11.5, 33, WHITE)
        a.next_to(q, DOWN, buff=0.6)
        logo = magnifier(0.7).next_to(a, DOWN, buff=0.6)
        with self.voiceover(
            "So: when can data answer an economic question? <bookmark mark='a'/> When something moved one thing and "
            "nothing else: a storm, a lottery, a birthday, a border. Find such a thing, or make one. Say exactly "
            "what it moved, and for whom. And ask whether the answer will survive the policy it informs."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo.ring), Create(logo.handle), LaggedStart(*[FadeIn(d, scale=0.3) for d in logo.dots],
                                                                         lag_ratio=0.1))
        self.clear_scene()

    def recap(self):
        s, ins, sc, la, dr, ck, L, dl = (load(x) for x in ("season", "instrument", "schooling", "lalonde", "draft",
                                                            "credibility", "lucas", "dial"))
        ex, v = load("experiment"), load("villages")
        items = [
            (rf"the fish market's cloud: \ least squares $+{s['ols_slope']:.1f}$, \ the planted demand "
             rf"${-s['b']:.1f}$", OLSC),
            (rf"the storm as instrument: \ ${ins['storm']['estimate']:.1f}$; \ the feast traces supply: "
             rf"$+{ins['feast']['estimate']:.1f}$", IVC),
            (r"Haavelmo: \ ask first what the data could reveal; \ exclusions are assumptions", E.ACCENT),
            (rf"school and ability: \ least squares {sc['ols']:.3f}, \ the new school {sc['iv']:.3f}, \ planted "
             rf"{sc['truth']:.2f}", "#F2B84B"),
            (r"LaLonde: \ the experiment $+\$886$; \ the survey comparisons from $-\$15{,}578$ to $+\$1{,}714$",
             NONEXP),
            (rf"the lottery of 1969 was not fair: \ correlation ${dr['rho']:.2f}$; \ Angrist used it anyway", E.MISS),
            (rf"New Jersey against Pennsylvania: \ $+{ck['did']:.2f}$ workers per restaurant", "#F26D6D"),
            (rf"by choice the apprenticeship looked harmful (${100 * ex['chose']['diff']:+.0f}\%$); \ by lottery "
             rf"${100 * ex['lottery']['diff']:+.0f}\%$", EXP),
            (rf"the council's menu promised {L['predicted_y_at_push']:.1f}; \ output went back to "
             rf"{L['y_push_last']:.1f}", "#C9A0FF"),
            (rf"a year of school: \ about 6 to 15\%; \ in {dl['iv_above']} of {dl['n']} studies the instrument says "
             r"more", IVC),
            (rf"spillovers: \ within villages ${v['within']:+.3f}$, \ everyone against no one ${v['total']:+.3f}$",
             E.TRUTH),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {txt}", font_size=30, color=col) for i, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 4, \ in eleven lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part four in eleven lines. <bookmark mark='a'/> A cloud of prices and quantities traces whichever curve "
            "moved less; on the Island the best line even sloped up. A storm, which moves only supply, traced "
            "demand, and a feast traced supply. Haavelmo taught us to ask first what the data could reveal, and to "
            "see that every exclusion is an assumption. Ability that raises both schooling and pay inflates the "
            "regression, and a new school undid the bias. LaLonde showed the methods of the day missing an "
            "experiment's answer, sometimes in sign. The lottery of 1969 wasn't even fair, yet it still made a "
            "usable instrument. A border found more fast-food jobs, not fewer, after a minimum wage rise. Chosen "
            "freely, the apprenticeship looked harmful; by lottery, it paid. A pattern the council leaned on "
            "vanished. A year of school is worth something like six to fifteen percent. And when treatments spill "
            "over, a trial can overstate what a policy delivers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=34.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The probability limit of a regression through a cloud; a storm that also keeps buyers at "
            "home; ability bias meeting measurement error; LaLonde's data with two before-and-after comparisons that "
            "disagree; the Wald estimate of a lottery; the council's four years; how many people a trial needs; and "
            "a research problem, marked with a star, on designing a trial that can see spillovers. Full solutions "
            "are in the part's notes."
        ):
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Joshua Angrist and J\"orn-Steffen Pischke, \emph{Mostly Harmless Econometrics} (2009) and "
             r"\emph{Mastering 'Metrics} (2014)",
             r"James Stock and Mark Watson, \emph{Introduction to Econometrics}, chs.\ 1--3, 12--13",
             r"Scott Cunningham, \emph{Causal Inference: The Mixtape} (2021)",
             r"Daron Acemoglu, David Laibson and John List, \emph{Economics}, ch.\ 2"],
            [r"Working (1927), \emph{QJE} 41; \ Wright (1928), Appendix B; \ Stock and Trebbi (2003), \emph{JEP} 17",
             r"Haavelmo (1944); \ Leamer (1983), \emph{AER} 73; \ LaLonde (1986), \emph{AER} 76; \ Lucas (1976)",
             r"Angrist (1990); \ Angrist and Krueger (1991); \ Card and Krueger (1994); \ Imbens and Angrist (1994)",
             r"Bound, Jaeger and Baker (1995); \ Staiger and Stock (1997); \ Card (2001), \emph{Econometrica} 69",
             r"Deaton, Imbens and Heckman (2010), \emph{JEL} 48; \ Angrist and Pischke (2010), \emph{JEP} 24",
             r"Crépon et al.\ (2013), \emph{QJE} 128; \ Egger et al.\ (2022) and Muralidharan et al.\ (2023), "
             r"\emph{Econometrica}"])
        with self.voiceover(
            "The reading for this part: Angrist and Pischke's two books, Mostly Harmless Econometrics and Mastering "
            "Metrics; the instrumental-variables chapters of Stock and Watson; Scott Cunningham's Mixtape, free "
            "online; and the evidence chapter of Acemoglu, Laibson and List. Then the papers, from Working's cloud "
            "and Wright's appendix to the trials that randomize whole villages."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1938, r"Paul Samuelson, \ ``A Note on the Pure Theory of Consumer's Behaviour''",
                          r"keep only what can be observed, \ the choices people make, \ and see how much of the "
                          r"theory of wants survives", color=E.ACCENT, width=9.0, font_size=26).move_to(UP * 0.6)
        nxt = VGroup(label(r"Next: \ Part 5", font_size=30, color=GREY_B),
                     label(r"What People Want", font_size=56, color=WHITE),
                     label(r"can you tell what someone wants from what they buy?", font_size=26, color=GREY_A)
                     ).arrange(DOWN, buff=0.15).next_to(hc, DOWN, buff=0.6)
        acts = VGroup(label(r"Act I \ $\cdot$ \ The Question: \ complete", font_size=34, color=GREY_A),
                      label(r"Act II \ $\cdot$ \ Choosing", font_size=40, color=E.ACCENT)).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "Act One ends here: what an economy is, what a market does, how it's measured, and what the evidence "
            "can say. Act Two turns to the people inside it. <bookmark mark='a'/> In 1938 Paul Samuelson, still in "
            "his early twenties, tried to rebuild the theory of demand from nothing but what can be observed: the "
            "choices people make. <bookmark mark='b'/> Part five: what people want. Can you tell what someone "
            "wants from what they buy?"
        ) as vo:
            self.play(FadeIn(acts[0]))
            self.play(FadeIn(acts[1], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(acts), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
