from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403

PROBLEMS = [
    r"Opt-in enrolment 40\%, \ opt-out 90\%: \ solve the two-type model for $q$ and $p$.",
    r"A megastudy arm estimated at +5 points with SE 1.5; \ arms' true effects have mean +1 and SD 1. \ Shrink it.",
    r"A trial: \ base rate 30\%, \ effect 2 points, \ 80\% power, \ 5\% two-sided: \ people per arm?",
    r"Academic trials with SE 4 points are published only if significant. \ True effect 1.5. \ Roughly what is the "
    r"average published estimate?",
    r"Energy use falls 2\% per home at a cost of \$1 a letter. \ A home uses 10,000 kWh a year. \ Cost per kWh "
    r"saved, \ if one letter a month for a year?",
    r"Give one test that separates a nudge from manipulation, \ and apply it to a pre-ticked box.",
    r"$\star$ \ Design a trial of a new reminder for a public service: \ outcome, \ arms, \ power, \ "
    r"preregistration, \ persistence and cost.",
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
        m = load("mega")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"automatic enrolment, \ from 37\%", r"86\%", PERSON),
                (r"2", r"the megastudy winner at +7 points", rf"truly about {100 * m['winner_true']:+.1f}", MODEL),
                (r"3", r"nudge-unit trials, \ on average", r"about 1.4 points", AUTH),
                (r"4", r"campaign contact in general elections", r"about zero", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"structure moves millions; \ messages move a few, \ a little, \ and less than the "
                             r"journals said", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Automatic enrolment took participation from thirty-seven "
            "percent to eighty-six. The megastudy's winner at plus seven was truly about one and a half. Nudge-unit "
            "trials averaged about one and a half points. And campaign contact in general elections persuaded about "
            "nobody, on average. <bookmark mark='b'/> Structure moves millions. Messages move a few, a little, and "
            "less than the journals said."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"a default is a decision someone already made", WHITE),
            (r"inertia, \ endorsement and loss aversion", SYMP),
            (r"framing, \ reminders, \ commitment and norms", SYMP),
            (r"a megastudy's winner is inflated; \ shrink it", MODEL),
            (r"journals 8.7 points, \ nudge units 1.4", MODEL),
            (r"for whom and where is the finding", MODEL),
            (r"money works while it is paid", PERSON),
            (r"messages cost attention and can backfire", AUTH),
            (r"campaigns and ads barely measurable", AUTH),
            (r"accuracy prompts and inoculation: \ small", PERSON),
            (r"a celebrated nudge was fabricated", AUTH),
            (r"steer transparently, \ and fix the system too", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 55, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-five in twelve lines. <bookmark mark='a'/> A default is a decision someone already made. It "
            "works through inertia, endorsement and loss aversion. The toolbox adds framing, reminders, commitment and "
            "norms. A megastudy's winner is inflated, so shrink it. Journals say eight point seven points, and nudge "
            "units one point four. For whom and where is the finding. Money works while it's paid. Messages cost "
            "attention and can backfire. Campaigns and ads are barely measurable. Accuracy prompts and inoculation "
            "help a little. A celebrated nudge was fabricated. And steer transparently, and fix the system too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"behaviour and the law", [56]),
            (r"health behaviour and stepped care", [57]),
            (r"incentives and the science of science", [61]),
            (r"a dissertation with a preregistered trial", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Behaviour and the law are Part 56. Health behaviour and "
            "stepped care are Part 57. The incentives of science itself are Part 61. And Part 62's dissertation can "
            "be a preregistered trial."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One solves the default "
            "algebra. One shrinks a megastudy arm. One sizes a trial. One estimates a filtered average. One prices "
            "energy savings. One separates a nudge from manipulation. And the last, with the star, asks you to design "
            "a trial of a reminder for a public service. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. H. Thaler \& C. R. Sunstein, \ \emph{Nudge} (2008; \ final edition 2021)",
             r"S. DellaVigna \& E. Linos (2022)",
             r"N. Chater \& G. Loewenstein (2023)"],
            [r"E. J. Johnson \& D. Goldstein (2003); \ B. C. Madrian \& D. F. Shea (2001)",
             r"R. H. Thaler \& S. Benartzi (2004); \ H. Allcott (2011); \ P. W. Schultz et al.\ (2007)",
             r"K. L. Milkman et al.\ (2021); \ C. J. Bryan, \ E. Tipton \& D. S. Yeager (2021)",
             r"S. Mertens et al.\ (2022); \ M. Maier et al.\ (2022)",
             r"J. Kalla \& D. Broockman (2018); \ R. A. Lewis \& J. M. Rao (2015); \ J. D. Hall \& J. M. Madsen (2022)",
             r"G. Pennycook et al.\ (2021); \ S. S. Iyengar \& M. R. Lepper (2000)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Nudge is the book that started "
            "it; DellaVigna and Linos are the accounting; and Chater and Loewenstein are the argument about what nudges "
            "leave out."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ 5 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 56", font_size=32, color=GREY_B),
                     label(r"Psychology and Law", font_size=36),
                     wrapped_label(r"how can a confident witness be wrong?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Five parts of Act Twelve are done. <bookmark mark='a'/> This one asked how far a choice's presentation "
            "moves millions, and found the honest answer smaller and more interesting. <bookmark mark='b'/> The next "
            "goes to court. How can a confident witness be wrong, and when is confidence worth trusting? Part 56: "
            "psychology and law."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
