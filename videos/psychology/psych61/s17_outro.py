from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403

PROBLEMS = [
    r"An outcome's reliability is 0.6 and it is a sum of many small causes. \ What is the most any model can "
    r"predict?",
    r"40 labs, \ 100 people each, \ $d$ = 0.3, \ no true variation. \ The expected SD of the labs' estimates?",
    r"A million volunteers, \ mean 0.22, \ SD 1. \ The 95\% interval? \ What would you need to know about the "
    r"bias?",
    r"A design space of 10 binary choices. \ How many cells, \ and how many parameters with all pairwise "
    r"interactions?",
    r"In Smaldino's model, \ $\alpha = W/(1 + (1 - W)e)$ with $W = 0.8$. \ The false-positive rate at efforts 1 "
    r"and 75?",
    r"One hypothesis in ten is true, \ power 0.8, \ $\alpha$ 0.05. \ The share of positives that are false?",
    r"$\star$ \ Write a commissioning brief for a study your organization will act on.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        c = load("challenge")
        l_ = load("labs")
        s = load("selection")
        sc = load("science")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"the best held-out $R^2$", rf"about 0.2 at best in the real challenge; \ {c['best']:.2f} in "
                                                  rf"Psyche", PERSON),
                (r"2", r"40 labs, \ no true variation", rf"{l_['none_est'].min():.1f} to {l_['none_est'].max():.1f}",
                 MODEL),
                (r"3", r"a million self-selected volunteers", rf"interval $\pm${s['half'][-1]:.3f}, \ bias "
                                                              rf"{s['mean'][-1]:.2f}", AUTH),
                (r"4", r"false share after selection on publications",
                 rf"{100 * np.mean(sc['pos_fdr'][-20:]):.0f}\%", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            wrapped_label(ans, 5.4, 22, col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"ceilings, \ noise, \ bias and incentives: \ four facts a redesigned field must "
                             r"build around", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> In the real challenge the best held-out R squared was "
            "about zero point two, for two of the six outcomes, and much lower for the rest; in Psyche, zero point "
            "one three. Forty labs with no true variation gave estimates from about minus zero point one to zero "
            "point seven. A million self-selected volunteers gave an interval of plus or minus zero point zero zero "
            "two around a bias of zero point two two. And selection on publications left eighty-eight percent of "
            "positives false. <bookmark mark='b'/> Ceilings, noise, bias and incentives: four facts a redesigned "
            "field must build around."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=12.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"life outcomes have low predictability ceilings", WHITE),
            (r"explain and predict: \ score causal models out of sample", MODEL),
            (r"many labs: \ most heterogeneity is small", GOOD),
            (r"size fixes noise, \ not selection or validity", AUTH),
            (r"most participants and authors are still WEIRD, \ and English", AUTH),
            (r"experiments as spaces, \ with surrogate models", MODEL),
            (r"machines can search theory space; \ people judge", PERSON),
            (r"theories as code make risky predictions", PERSON),
            (r"selection on publications breeds bad methods", AUTH),
            (r"digital traces need validation at the right level", SYMP),
            (r"automate tasks, \ not responsibility", SYMP),
            (r"rank reforms by evidence: \ power and registered reports first", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 61, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part sixty-one in twelve lines. <bookmark mark='a'/> Life outcomes have low ceilings of predictability. "
            "To explain and predict, score causal models out of sample. Across many labs, most heterogeneity is "
            "small. Size fixes noise, not selection or validity. Most participants and authors are still WEIRD, and "
            "English-speaking. Experiments can be spaces, with surrogate models. Machines can search the space of "
            "theories, and people judge. Theories written as code make risky predictions. Selection on publications "
            "breeds bad methods. Digital traces need validation at the right level. Automate tasks, not "
            "responsibility. And rank reforms by evidence, with power and registered reports first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"a registered report, \ executed end to end", [62]),
            (r"Psyche's whole Battery, \ and the complete Ledger", [62]),
            (r"the open problems of all sixty-two parts", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Everything does, in Part 62: a registered report executed end "
            "to end, Psyche's whole Battery and the complete Ledger, and the open problems of all sixty-two parts."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One finds a ceiling. One "
            "computes the spread of many labs. One reads a huge biased sample. One counts a design space. Two work "
            "through Smaldino and McElreath's arithmetic. And the last, with the star, asks you to write a "
            "commissioning brief. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. J. Salganik, \ \emph{Bit by Bit: Social Research in the Digital Age}",
             r"T. Yarkoni \& J. Westfall (2017)",
             r"P. E. Smaldino \& R. McElreath (2016)"],
            [r"M. J. Salganik et al.\ (2020); \ J. M. Hofman et al.\ (2021)",
             r"R. A. Klein et al.\ (2014, \ 2018); \ H. Moshontz et al.\ (2018)",
             r"A. Coutrot et al.\ (2018); \ E. Awad et al.\ (2018); \ J. K. Hartshorne et al.\ (2018)",
             r"A. G. Thalmayer et al.\ (2021); \ D. E. Blasi et al.\ (2022)",
             r"A. Almaatouq et al.\ (2024); \ J. C. Peterson et al.\ (2021); \ D. Borsboom et al.\ (2021)",
             r"J. C. Eichstaedt et al.\ (2015); \ N. J. L. Brown \& J. C. Coyne (2018)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Salganik's book is the best "
            "introduction to research with digital data; Yarkoni and Westfall's paper sets out prediction's case; "
            "and Smaldino and McElreath's model shows how incentives shape methods."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XIII: \ the frontier, \ four of five", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 62", font_size=32, color=GREY_B),
                     label(r"The Dissertation", font_size=34),
                     wrapped_label(r"was Kant right?", 6.0, 24, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Four parts of the frontier are done. <bookmark mark='a'/> This one designed the next psychology. "
            "<bookmark mark='b'/> The last part does it: one question, taken through a registered report, reviewed "
            "before the data exist, run, and reported whatever it shows. Then the accounts are closed, and Kant's "
            "objections are answered. Part 62: the dissertation."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
