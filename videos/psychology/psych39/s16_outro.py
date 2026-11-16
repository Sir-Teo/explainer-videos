from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403

PROBLEMS = [
    r"Two clinicians rate 200 patients: \ both yes 30, \ both no 130, \ A yes and B no 25, \ A no and B yes 15. \ "
    r"Compute $p_o$, \ $p_e$ and Cohen's kappa.",
    r"Show that kappa is 0 when the two clinicians' ratings are independent, \ whatever their base rates, \ and find "
    r"the largest kappa possible when one says yes 10\% of the time and the other 30\%.",
    r"Count the symptom combinations that meet ``at least 5 of 9, \ including symptom 1 or symptom 2''.",
    r"A screen has sensitivity 0.9 and specificity 0.91. \ Find the positive predictive value at prevalence 1\%, \ "
    r"10\% and 30\%, \ and say when screening makes sense.",
    r"If a diagnosis has reliability $r_{xx}$ and an outcome has reliability $r_{yy}$, \ show that their correlation "
    r"cannot exceed $\sqrt{r_{xx} r_{yy}}$.",
    r"In a symptom network, \ each of $n$ symptoms is on with probability $\sigma(b + s + c\,k)$, \ where $k$ is the "
    r"number of others on. \ Using a mean-field approximation, \ find the equation for the fraction on, \ and show "
    r"how two stable solutions can coexist.",
    r"$\star$ \ Design a study that could tell a network account of depression from a common-cause account.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, c in (
                (r"1", r"US adults who had ever met the criteria for a disorder", r"46\%", PERSON),
                (r"2", r"kappa for major depression in the DSM-5 field trials", r"about 0.3", SYMP),
                (r"3", r"symptom profiles among 3{,}703 people with depression", r"1{,}030", MODEL),
                (r"4", r"studies where clinicians clearly beat the formula", r"6 to 16\%", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"disorders are common, \ diagnosis is imperfect, \ and categories hide a great deal of "
                             r"variety", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The share of American adults who had ever met the "
            "criteria for a disorder: forty-six percent. The kappa for major depression in the field trials: about "
            "point three. The symptom profiles among three thousand seven hundred people with depression: one "
            "thousand and thirty. And the studies where clinicians clearly beat the formula: six to sixteen percent. "
            "<bookmark mark='b'/> Disorders are common, diagnosis is imperfect, and categories hide a great deal of "
            "variety."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"Rosenhan's study changed diagnosis; \ its data are in serious doubt", AUTH),
            (r"rarity, \ distress, \ dysfunction and harm each fail alone; \ harmful dysfunction combines two", PERSON),
            (r"kappa is agreement beyond chance; \ depression's is about 0.3", SYMP),
            (r"reliability caps validity; \ it does not create it", MODEL),
            (r"227 symptom combinations make one diagnosis", SYMP),
            (r"most disorders are dimensions with conventional cut-offs", GOOD),
            (r"comorbidity is the rule, \ and a p factor summarizes it", PERSON),
            (r"symptom networks can tip suddenly and recover slowly", MODEL),
            (r"nearly half of adults meet criteria at some point; \ most are untreated", WHITE),
            (r"formulas beat clinical judgment, \ and nobody beats the base rate", GOOD),
            (r"suffering speaks in cultural idioms, \ and labels can harm", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 39, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-nine in eleven lines. <bookmark mark='a'/> Rosenhan's study changed diagnosis, and its data "
            "are in serious doubt. Rarity, distress, dysfunction and harm each fail alone, and harmful dysfunction "
            "combines two. Kappa is agreement beyond chance, and depression's is about point three. Reliability caps "
            "validity, but doesn't create it. Two hundred and twenty-seven symptom combinations make one diagnosis. "
            "Most disorders are dimensions with conventional cut-offs. Comorbidity is the rule, and a p factor "
            "summarizes it. Symptom networks can tip suddenly and recover slowly. Nearly half of adults meet "
            "criteria at some point, and most go untreated. Formulas beat clinical judgment, and nobody beats the "
            "base rate. And suffering speaks in cultural idioms, and labels can harm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"kappa, \ base rates, \ taxometrics and a symptom network with hysteresis", STATUS_COLOR["replicated"]),
            (r"field trials with paired clinicians, \ and decades of formula against judgment",
             STATUS_COLOR["replicated"]),
            (r"diagnosis rests on what people report, \ and two clinicians hear it differently",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "kappa, base rates, taxometrics and a symptom network with hysteresis. <bookmark mark='b'/> The second, "
            "that the mind can't be experimented on, met field trials with paired clinicians, and decades of formula "
            "against judgment. <bookmark mark='c'/> And the third, about introspection: diagnosis rests on what "
            "people report, and two clinicians hear it differently. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"anxiety and depression, \ from conditioning to circuits", [40]),
            (r"psychosis, \ addiction and development", [41]),
            (r"does therapy work?", [42]),
            (r"latent variables and networks, \ properly", [44, 47]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Anxiety and depression, from conditioning to circuits, are "
            "next, in Part 40. Psychosis, addiction and development are Part 41. Whether therapy works is Part 42. "
            "And latent variables and networks get their full treatment in Parts 44 and 47."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes a kappa by "
            "hand. One shows when kappa is zero, and how large it can be. One counts the symptom combinations. One "
            "works a screen at three prevalences. One proves that reliability caps validity. One finds the two "
            "stable states of a symptom network. And the last, with the star, asks you to design a study that could "
            "tell a network from a common cause. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Cahalan, \ \emph{The Great Pretender} (2019)",
             r"P. E. Meehl, \ \emph{Clinical versus Statistical Prediction} (1954)",
             r"E. Shorter, \ \emph{A History of Psychiatry} (1997)"],
            [r"D. L. Rosenhan (1973); \ J. C. Wakefield (1992); \ E. Robins \& S. B. Guze (1970)",
             r"J. Cohen (1960); \ D. A. Regier et al.\ (2013)",
             r"E. I. Fried \& R. M. Nesse (2015); \ N. Haslam et al.\ (2012, \ 2020)",
             r"A. Caspi et al.\ (2014); \ R. Kotov et al.\ (2017)",
             r"A. O. J. Cramer et al.\ (2016); \ D. Borsboom (2017); \ J. Kruis \& G. Maris (2016)",
             r"R. C. Kessler et al.\ (2005); \ R. Kohn et al.\ (2004); \ A. F. Jorm et al.\ (2017)",
             r"R. M. Dawes (1979); \ W. M. Grove et al.\ (2000); \ S. Kapur et al.\ (2012)",
             r"M. Nichter (1981); \ B. N. Kaiser et al.\ (2015)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Cahalan's The Great Pretender "
            "is the investigation of Rosenhan; Meehl's book is short and still disturbing; and Shorter's A History "
            "of Psychiatry tells the longer story from the asylums on."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act X: \ when minds suffer", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 40", font_size=32, color=GREY_B), label(r"Fear and Sadness", font_size=40),
                     wrapped_label(r"How do ordinary fear and sadness become anxiety and depression?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Ten has begun. <bookmark mark='a'/> This part asked what a disorder is, and found that the answer is "
            "partly a convention. <bookmark mark='b'/> The next part takes the two commonest: how ordinary fear and "
            "sadness become anxiety and depression, from conditioning to circuits. Part 40: fear and sadness."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
