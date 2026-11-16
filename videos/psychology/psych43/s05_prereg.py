from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403

PLAN = r"""plan = Plan(
    target="ego depletion",
    outcome="Hedges's g, RT variability, depleted - control",
    sign=+1, original=0.68, original_se=0.30,
    sesoi=0.10, alpha=0.05,          # one-sided
    min_n=0,                         # keep every lab that ran the protocol
    estimator="random effects (DerSimonian-Laird)")

result = analyse(lab_data, plan)     # run once, after the plan is frozen
verdict(result, plan, d33=0.46)"""


class Prereg(VoiceoverScene):
    def construct(self):
        self.card()
        self.code()
        self.dry()
        self.forks()

    def card(self):
        card = chapter_card(4, r"The plan, \ written as code", r"What will each result mean?",
                            lit={2022: r"Chambers \& Tzavella"}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter four. The plan, written as code."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def code(self):
        head = heading(r"Preregistration")
        box = RoundedRectangle(width=7.4, height=4.6, corner_radius=0.12, stroke_color=MODEL, stroke_width=1.5,
                               fill_color=BLACK, fill_opacity=0.5).move_to([-2.9, -0.1, 0])
        src = [l for l in PLAN.split("\n") if l.strip()]
        lines = VGroup(*[Text(l, font="DejaVu Sans Mono", font_size=13, color=GREY_A)
                         for l in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for l, t in zip(src, lines):
            t.shift(RIGHT * 0.09 * (len(l) - len(l.lstrip())))  # Text drops leading spaces: indent by hand
        lines[-2:].shift(DOWN * 0.25)  # a blank line before the two calls
        if lines.width > box.width - 0.4:
            lines.scale_to_fit_width(box.width - 0.4)
        lines.move_to(box)
        rows = rows_of([
            (r"hypothesis, \ outcome, \ direction, \ smallest effect of interest, \ exclusion rule and estimator, \ "
             r"written before the data are read", WHITE),
            (r"the three criteria for calling it a replication are fixed in advance too, \ so the verdict cannot be "
             r"chosen after the fact", MODEL),
            (r"a registered report goes further: \ the journal accepts the plan, \ and publishes whatever it finds", GOOD),
        ], 5.2, 19, 0.38).move_to([3.9, -0.1, 0])
        with self.voiceover(
            "Next, the plan. <bookmark mark='a'/> Here it is, as code: the hypothesis, the outcome, its direction, "
            "the smallest effect of interest, the exclusion rule and the estimator, written down before the data are "
            "read. <bookmark mark='b'/> The three criteria for calling the result a replication are fixed in advance "
            "too, so the verdict can't be chosen afterwards. <bookmark mark='c'/> A registered report goes further. "
            "The journal accepts the plan, and publishes whatever it finds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.15), run_time=3.0)
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def dry(self):
        d = load("dryrun")
        head = heading(r"A dry run, \ before any real data")
        A = axes([0.3, 3.7], [0, 1], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share significant", center=[-3.4, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], d["share"], [GREY_B, PERSON, GOOD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.6, 13, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.15) for i, (t, c) in
                         enumerate(((r"no effect", GREY_B), (rf"$d = {d['effects'][1]:g}$", PERSON),
                                    (rf"$d = {d['effects'][2]:g}$, \ the original", GOOD)))])
        rows = rows_of([
            (rf"Psyche simulates {d['k']} labs of {d['n']} per group, \ 200 times for each true effect, \ and runs the "
             rf"frozen analysis on each", WHITE),
            (rf"with no effect, \ {pct(d['share'][0])} come out significant: \ the planned false-positive rate", GREY_A),
            (rf"at the smallest effect of interest, \ {pct(d['share'][1])}; \ at the original effect, \ "
             rf"{pct(d['share'][2])}", PERSON),
            (r"the code runs, \ the error rates are what was promised, \ and any bug is found before it can be "
             r"tempted to help", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{capstone.dry\_run}, \ 200 runs each")
        with self.voiceover(
            "Before any real data, the plan is run on simulated data. <bookmark mark='a'/> Psyche simulates "
            "twenty-three labs, of forty-six people per group, two hundred times for each true effect, and runs the "
            "frozen analysis on each. <bookmark mark='b'/> With no effect, about one run in twenty comes out "
            "significant: the planned false-positive rate. <bookmark mark='c'/> At the smallest effect of interest, "
            "about seven runs in ten. At the original effect, every run. <bookmark mark='d'/> So the code runs, the "
            "error rates are what was promised, and any bug is found before it could be tempted to help."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def forks(self):
        head = heading(r"Every fork, \ closed in advance")
        data = (
            (r"outcome", r"one: \ the primary measure, \ named; \ the others listed as secondary", SYMP),
            (r"direction", r"the sign predicted, \ so the test is one-sided by plan, \ not by convenience", PERSON),
            (r"exclusions", r"which people and which labs are dropped, \ by rules written before the data", AUTH),
            (r"estimator", r"random effects across labs, \ with the software and its settings", MODEL),
            (r"verdict", r"three criteria and a Bayes factor, \ with what each result would mean", GOOD),
            (r"deviations", r"anything that had to change, \ reported as a change, \ with its reason", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=2.6), wrapped_label(how, 9.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.3, 0])
        with self.voiceover(
            "Each line of the plan closes a fork in the garden of Part 4. <bookmark mark='a'/> The outcome: one primary "
            "measure, named, and the others listed as secondary. <bookmark mark='b'/> The direction, so the test is "
            "one-sided by plan, not by convenience. <bookmark mark='c'/> The exclusions: which people and which labs "
            "are dropped, by rules written before the data. <bookmark mark='d'/> The estimator, with its software and "
            "settings. <bookmark mark='e'/> The verdict: three criteria and a Bayes factor, with what each result "
            "would mean. <bookmark mark='f'/> And deviations: anything that had to change is reported as a change, with "
            "its reason."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
