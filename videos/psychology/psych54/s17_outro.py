from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403

PROBLEMS = [
    r"A test is 60 days away. \ Using the ridgeline, \ roughly when should a single restudy happen?",
    r"Three reviews per item, \ a 28-day window: \ write equal and expanding (doubling) schedules.",
    r"Reading comprehension = decoding $\times$ language comprehension. \ Decoding 0.4, \ comprehension 0.9: \ "
    r"predict, \ and say which teaching helps more.",
    r"A mindset effect of 0.08 SD: \ how many students per arm for 80\% power (two-sided, \ 5\%)?",
    r"Knowledge tracing with $L$ = 0.5, \ guess 0.2, \ slip 0.1: \ the student answers wrong. \ Find P(known) after.",
    r"Design the crossover test that would support learning styles. \ What result is needed?",
    r"$\star$ \ Redesign a course you know: \ retrieval, \ spacing, \ interleaving, \ load, \ and how you will "
    r"evaluate it.",
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
        d = load("policies")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"human tutoring in later reviews", r"about 0.8 SD; \ school trials about 0.4", PERSON),
                (r"2", r"recall on day 60: \ crammed, \ spaced", rf"{100 * d['recall'][0]:.0f}\%, \ "
                                                               rf"{100 * d['recall'][2]:.0f}\%", MODEL),
                (r"3", r"feedback studies where performance got worse", r"over a third", AUTH),
                (r"4", r"a national mindset lesson", r"about 0.1 grade points, \ for some", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"what feels like learning and what produces it point in opposite directions", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Later reviews put human tutoring at about zero point eight "
            "standard deviations, and school trials at about zero point four. Psyche's crammed reviews left seventeen "
            "percent on day sixty, and spaced ones seventy-one. Over a third of feedback studies found performance got "
            "worse. And the national mindset lesson raised grades by about a tenth of a point, for some students. "
            "<bookmark mark='b'/> What feels like learning and what produces it point in opposite directions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"two sigma became about half a sigma, \ still large", WHITE),
            (r"a test is a learning event", SYMP),
            (r"space reviews against the date you need them", SYMP),
            (r"interleave confusable problems", MODEL),
            (r"performance during practice misleads", MODEL),
            (r"testing and spacing top the ten techniques", MODEL),
            (r"cut extraneous load; \ fade worked examples", PERSON),
            (r"styles fail the crossover test", AUTH),
            (r"tutors model the learner, \ inner and outer loops", PERSON),
            (r"where a review goes beats how many", GOOD),
            (r"reading needs decoding and comprehension", GOOD),
            (r"mindset and feedback: \ small, \ for some, \ sometimes negative", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 54, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-four in twelve lines. <bookmark mark='a'/> Two sigma became about half a sigma, and that's "
            "still large. A test is a learning event. Space reviews against the date you'll need them. Interleave "
            "confusable problems. Performance during practice misleads. Testing and spacing top the ten techniques. "
            "Cut extraneous load, and fade worked examples. Learning styles fail the crossover test. Tutors model the "
            "learner, in inner and outer loops. Where a review goes beats how many reviews there are. Reading needs "
            "decoding and comprehension. And mindset and feedback effects are small, for some, and sometimes "
            "negative."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"behaviour change, \ scaled and shrinking", [55]),
            (r"memory in court", [56]),
            (r"learning machines and learning minds", [60]),
            (r"a dissertation on a learning intervention", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Interventions that shrink at scale are Part 55's subject. "
            "Memory goes to court in Part 56. Learning machines and learning minds meet in Part 60. And Part 62's "
            "dissertation can test a learning intervention properly."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One reads the ridgeline. "
            "One writes schedules. One applies the simple view of reading. One computes the sample a small effect "
            "needs. One updates knowledge tracing after a wrong answer. One designs the learning-styles test. And the "
            "last, with the star, asks you to redesign a course you know. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"P. C. Brown, \ H. L. Roediger \& M. A. McDaniel, \ \emph{Make It Stick} (2014)",
             r"J. Dunlosky et al.\ (2013)",
             r"E. L. Bjork \& R. A. Bjork (2011)"],
            [r"B. S. Bloom (1984); \ K. VanLehn (2011); \ A. Nickow et al.\ (2020)",
             r"H. L. Roediger \& J. D. Karpicke (2006); \ N. J. Cepeda et al.\ (2008); \ D. Rohrer \& K. Taylor (2007)",
             r"S. Freeman et al.\ (2014); \ L. Deslauriers et al.\ (2019)",
             r"J. Sweller (1988); \ H. Pashler et al.\ (2008)",
             r"B. Settles \& B. Meeder (2016); \ A. Castles, \ K. Rastle \& K. Nation (2018)",
             r"D. S. Yeager et al.\ (2019); \ A. N. Kluger \& A. DeNisi (1996)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Make It Stick is the best short "
            "book for learners; Dunlosky and colleagues' review is the evidence in one place; and the Bjorks' chapter "
            "explains desirable difficulties."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ 4 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 55", font_size=32, color=GREY_B),
                     label(r"Behaviour Change at Scale", font_size=36),
                     wrapped_label(r"why do nudges shrink when they leave the laboratory?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Four parts of Act Twelve are done. <bookmark mark='a'/> This one turned memory research into engineering, "
            "and found learners pulling the other way. <bookmark mark='b'/> The next scales up from a classroom to a "
            "country. Why do nudges shrink when they leave the laboratory? Part 55: behaviour change at scale."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
