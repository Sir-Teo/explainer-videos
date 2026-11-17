from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Usability(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"How many users?", r"Are five users enough?")
        self.curve_()
        self.tools()

    def curve_(self):
        d = load("discovery")
        head = heading(r"The problem-discovery curve")
        A = axes([0, 21], [0, 1.0], x_length=5.6, y_length=3.2, xticks=[1, 5, 10, 15, 20], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"users tested",
                 ylabel=r"problems found", center=[-3.3, 0.3, 0], font_size=12)
        ch = curve(A.ax, d["n"], d["homog"], GOOD, stroke_width=4)
        ce = curve(A.ax, d["n"], d["hetero"], AUTH, stroke_width=4)
        v5 = DashedLine(A.ax.c2p(5, 0), A.ax.c2p(5, 1.0), color=GREY_B)
        key = VGroup(label(r"every problem equally findable", font_size=13, color=GOOD),
                     label(r"problems that differ", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Nielsen and Landauer, \ 1993: \ if each user finds each problem with probability $p$, \ $n$ users find "
             r"$1 - (1 - p)^n$ of them", WHITE),
            (rf"with their average $p$ of about 0.31, \ five users find {100 * d['homog'][4]:.0f}\%: \ ``test with five "
             rf"users''", GOOD),
            (rf"but problems differ: \ some almost everyone hits, \ some one user in twenty; \ with the same average "
             rf"$p$, \ five users find {100 * d['hetero'][4]:.0f}\%, \ twenty find {100 * d['hetero'][-1]:.0f}\%", AUTH),
            (r"Spool and Schroeder, \ and Faulkner, \ found five users missing many problems in real tests: \ "
             r"iterate with small tests, \ but do not claim coverage", YOU),
        ], 6.0, 19, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.discovery}, \ problems' $p \sim$ Beta(0.6, 1.34)")
        with self.voiceover(
            "How many users does a usability test need? <bookmark mark='a'/> In 1993 Jakob Nielsen and Thomas Landauer "
            "wrote the curve. If each user finds each problem with probability p, n users find one minus one minus p "
            "to the n of them. <bookmark mark='b'/> With their average p of about a third, five users find eighty-four "
            "percent. Hence the advice: test with five users. <bookmark mark='c'/> But problems differ. Some almost "
            "everyone hits, and some only one user in twenty. With the same average p, five users find about sixty "
            "percent, and twenty users still miss almost a fifth. <bookmark mark='d'/> Later studies, by Jared Spool "
            "and Will Schroeder and by Laura Faulkner, found five users missing many problems in real tests. The "
            "useful advice survives: iterate with small tests. But don't claim coverage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(v5))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ch))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ce))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def tools(self):
        chips_section(self, r"Tests, \ questionnaires and experiments", [
            (r"think-aloud", r"a user does real tasks and says what they are thinking: \ finds problems, \ not rates",
             MODEL),
            (r"SUS", r"the System Usability Scale: \ ten items, \ a score from 0 to 100; \ about 68 is average across "
                     r"many studies", PERSON),
            (r"task metrics", r"success, \ time and errors on set tasks, \ with intervals, \ not just averages (Part 4)",
             SYMP),
            (r"an experiment", r"when the question is ``is B better than A?'': \ randomize users and measure "
                               r"(\emph{Computer Science, Built} Part 44)", GOOD),
        ], "So what does a usability team actually use? <bookmark mark='a'/> Think-aloud tests: a user does real tasks "
           "and says what they're thinking. They find problems, not rates. <bookmark mark='b'/> Questionnaires like "
           "the System Usability Scale: ten items and a score from zero to a hundred, where about sixty-eight is "
           "average across many studies. <bookmark mark='c'/> Task metrics: success, time and errors on set tasks, "
           "reported with intervals, not just averages. <bookmark mark='d'/> And when the question is whether design "
           "B is better than A, an experiment: randomize users and measure.", chip_w=3.2, text_w=9.0)
