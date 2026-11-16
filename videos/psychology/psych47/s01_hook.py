from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.clark()
        self.deeper()
        self.question()
        self.objectives()

    def clark(self):
        d = load("fpr")
        head = heading(r"Twenty words, \ one conclusion")
        A = axes([0.3, 3.7], [0, 0.6], x_length=4.6, y_length=3.2, xticks=None, yticks=[0, 0.05, 0.25, 0.5],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"false positives", center=[-3.6, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [d["F1"], d["F2"], d["minF"]], [AUTH, SYMP, GOOD], width=0.6)
        five = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(3.7, 0.05), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[wrapped_label(t, 1.4, 12, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"by participants", AUTH), (r"by items", SYMP), (r"both random", GOOD)))])
        rows = rows_of([
            (r"1973: \ Herbert Clark notices that psycholinguists test whether an effect generalizes to new people, "
             r"\ but not to new words", WHITE),
            (rf"Psyche runs {d['reps']} priming studies with no effect at all: \ 30 people, \ 20 words, \ and words "
             rf"that differ", MODEL),
            (rf"analysed by participants only, \ {100 * d['F1']:.0f}\% come out significant; \ the promise was 5\%",
             AUTH),
            (r"treat words as a sample too, \ and the rate returns to 5\% or below: \ the fix took thirty years to "
             r"become routine", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.false\_positive\_rates}")
        with self.voiceover(
            "In 1973 the psychologist Herbert Clark looked at a generation of studies of language. "
            "<bookmark mark='a'/> They tested whether an effect would generalize to new people. They never tested "
            "whether it would generalize to new words. <bookmark mark='b'/> Psyche runs two hundred priming studies "
            "in which nothing works at all: thirty people, twenty words, and words that differ from one another. "
            "<bookmark mark='c'/> Analysed by participants only, about half come out significant. The promise was "
            "five percent. <bookmark mark='d'/> Treat the words as a sample too, and the rate returns to five "
            "percent or below. The fix took thirty years to become routine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[1]), FadeIn(b[2]))
        self.clear_scene()

    def deeper(self):
        head = heading(r"The deeper point")
        rows = rows_of([
            (r"Clark's point is about generalizing across stimuli; \ the deeper version is about generalizing across "
             r"people", WHITE),
            (r"a relation that holds across people need not hold within any one of them", AUTH),
            (r"most psychological theories are about the second: \ what happens in a mind when something changes", MODEL),
            (r"and most studies measure the first: \ many people, \ once each", PERSON),
            (r"this part is about telling them apart", YOU),
        ], 12.4, 24, 0.48).move_to([0, -0.3, 0])
        with self.voiceover(
            "Clark's point is about generalizing across stimuli. <bookmark mark='a'/> There's a deeper version, the "
            "hardest in the series. <bookmark mark='b'/> A relation that holds across people need not hold within "
            "any one of them. <bookmark mark='c'/> Most psychological theories are about the second: what happens "
            "inside a mind when something changes. <bookmark mark='d'/> And most studies measure the first: many "
            "people, each measured once. <bookmark mark='e'/> This part is about telling them apart."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ when is a finding about people a finding about a person?")
        rows = rows_of([
            (r"repeated measures and multilevel models", SYMP),
            (r"participants and stimuli, \ both as samples", MODEL),
            (r"within against between, \ and ergodicity", PERSON),
            (r"lives in time: \ diaries, \ inertia, \ and tipping points", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks when a finding about people is a finding about a person. <bookmark mark='a'/> "
            "Repeated measures and multilevel models. <bookmark mark='b'/> Participants and stimuli, both as samples. "
            "<bookmark mark='c'/> Within against between, and ergodicity. <bookmark mark='d'/> And lives in time: "
            "diaries, inertia, and tipping points."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 47", font_size=34, color=GREY_B), label(r"People over Time", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the language-as-fixed-effect fallacy, \ simulated",
            r"multilevel models, \ shrinkage and crossed random effects",
            r"how many stimuli a claim needs",
            r"within against between, \ and person-mean centring",
            r"ergodicity, \ and a population that describes no one",
            r"experience sampling, \ inertia and critical slowing down",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 47 of Psychology, Built: people over time. <bookmark mark='a'/> We'll simulate the "
            "language-as-fixed-effect fallacy. We'll build multilevel models, watch them shrink, and cross "
            "participants with items. We'll ask how many stimuli a claim needs. We'll separate within-person from "
            "between-person relations. We'll build a population whose averages describe no one. And we'll follow "
            "lives in time: diaries, emotional inertia, and the warning signs before a tipping point."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
