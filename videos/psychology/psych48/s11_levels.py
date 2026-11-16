from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Levels(VoiceoverScene):
    def construct(self):
        self.card()
        self.rational()
        self.resource()
        self.samples()

    def card(self):
        card = chapter_card(10, r"Rational and resource-rational", r"What would a mind built for this problem do?",
                            lit={1990: r"Anderson", 2020: r"Lieder \& Griffiths"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter ten. Rational and resource-rational."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rational(self):
        head = heading(r"Rational analysis")
        steps = VGroup()
        for k, (txt, c) in enumerate((
                (r"state the goal the mind is trying to achieve", WHITE),
                (r"describe the environment it works in, \ with its statistics", SYMP),
                (r"make minimal assumptions about its limits", MODEL),
                (r"derive the optimal behaviour, \ and compare it with people", GOOD),
                (r"if they differ, \ revise the goal, \ the environment or the limits, \ not the optimality", PERSON))):
            steps.add(VGroup(label(rf"{k + 1}", font_size=26, color=c), wrapped_label(txt, 10.6, 22, WHITE))
                      .arrange(RIGHT, buff=0.4))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, 0.2, 0])
        foot = wrapped_label(r"Anderson and Schooler, \ 1991: \ memory's forgetting curve matches how often information "
                             r"is needed again; \ Marr's computational level, \ made a method (Part 1)", 12.0, 20,
                             YOU).move_to([0, -2.6, 0])
        tag = published_tag(r"Anderson (1990)")
        with self.voiceover(
            "Fitting asks how; another tradition asks why. <bookmark mark='a'/> John Anderson's rational analysis "
            "starts from the goal the mind is trying to achieve, <bookmark mark='b'/> describes the environment it "
            "works in, with its statistics, <bookmark mark='c'/> makes minimal assumptions about its limits, "
            "<bookmark mark='d'/> derives the optimal behaviour, and compares it with people. <bookmark mark='e'/> "
            "If they differ, revise the goal, the environment or the limits, not the optimality. "
            "<bookmark mark='f'/> With Lael Schooler, in 1991, Anderson showed that memory's forgetting curve matches "
            "how often information is needed again in the world. It's Marr's computational level, made a method."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", steps):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def resource(self):
        head = heading(r"Optimal, \ given limited computation")
        rows = rows_of([
            (r"people are not optimal for the problem; \ they may be optimal for the problem plus their limits", WHITE),
            (r"Lieder and Griffiths, \ 2020: \ resource-rational analysis treats thinking itself as costly, \ and "
             r"asks for the best use of a limited budget", MODEL),
            (r"heuristics and biases (Part 24) become sensible strategies for a mind that cannot compute everything",
             GOOD),
            (r"the danger: \ with enough freedom to choose the costs, \ any behaviour can be called rational; \ the "
             r"costs must be measured, \ not chosen to fit", AUTH),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Lieder \& Griffiths (2020)")
        with self.voiceover(
            "Real minds have limits. <bookmark mark='a'/> People aren't optimal for the problem; they may be optimal "
            "for the problem plus their limits. <bookmark mark='b'/> Falk Lieder and Tom Griffiths call this "
            "resource-rational analysis: thinking itself is costly, so ask for the best use of a limited budget. "
            "<bookmark mark='c'/> Heuristics and biases, from Part 24, become sensible strategies for a mind that "
            "can't compute everything. <bookmark mark='d'/> The danger: with enough freedom to choose the costs, any "
            "behaviour can be called rational. The costs must be measured, not chosen to fit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def samples(self):
        d = load("samples")
        head = heading(r"How long should you think?")
        A = axes([0, 41], [0.5, 1.0], x_length=5.6, y_length=3.0, xticks=[1, 10, 20, 30, 40], yticks=[0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"samples considered before "
                 r"choosing", ylabel=r"accuracy", center=[-3.3, 0.3, 0], font_size=12)
        c = curve(A.ax, d["k"], d["acc"], MODEL, stroke_width=4)
        marks = VGroup(*[Dot(A.ax.c2p(int(k), float(d["acc"][int(k) - 1])), radius=0.08, color=col)
                         for k, col in zip(d["best_k"], [GOOD, SYMP, PERSON, AUTH])])
        rows = rows_of([
            (r"choose between two options by sampling evidence about their difference: \ each sample is weak (0.3 SD)",
             WHITE),
            (r"accuracy rises with samples, \ but more and more slowly", MODEL),
            (rf"charge for each sample, \ and the best number falls fast: \ {d['best_k'][0]} samples when thinking is "
             rf"cheap, \ {d['best_k'][-1]} when it costs ten times more", PERSON),
            (r"a mind that decides on few samples may be using its time well: \ the resource-rational reading of "
             r"``one and done''", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"$\Phi(0.3\sqrt{k}) - c\,k$")
        with self.voiceover(
            "Resource-rational analysis can be computed. <bookmark mark='a'/> Choose between two options by "
            "sampling evidence about their difference, each sample weak. <bookmark mark='b'/> Accuracy rises with "
            "samples, but more and more slowly. <bookmark mark='c'/> Now charge for each sample. The best number falls "
            "fast: about thirty-six samples when thinking is cheap, and five when it costs ten times as much. "
            "<bookmark mark='d'/> A mind that decides on a few samples may be using its time well. That's the "
            "resource-rational reading of deciding on one or two samples, which is what people often seem to do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(marks))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
