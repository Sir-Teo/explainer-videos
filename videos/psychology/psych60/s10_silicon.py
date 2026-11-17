from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Silicon(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Silicon samples", r"Can a model stand in for participants?", scale=("society",))
        self.argyle()
        self.chart()

    def argyle(self):
        rows_section(self, r"Out of one, \ many", [
            (r"Argyle and colleagues, \ 2023: \ a model prompted with thousands of real respondents' backgrounds "
             r"reproduced the patterns of their vote choices and attitudes in American surveys", GOOD),
            (r"the promise: \ cheap pilots, \ survey design, \ hard-to-reach groups", MODEL),
            (r"later studies: \ responses too uniform, \ minority views pulled toward the majority's, \ results that "
             r"change with the model and its version", AUTH),
            (r"Part 46's survey science asks: \ the same means, \ but the same spread, \ the same subgroups?", YOU),
        ], "Can a model stand in for participants? <bookmark mark='a'/> In 2023 Lisa Argyle and colleagues prompted "
           "a model with thousands of real respondents' backgrounds, and it reproduced the patterns of their vote "
           "choices and attitudes in American surveys. <bookmark mark='b'/> The promise is cheap pilots, help with "
           "survey design, and hard-to-reach groups. <bookmark mark='c'/> Later studies found responses too "
           "uniform, minority views pulled toward the majority's, and results that change with the model and its "
           "version. <bookmark mark='d'/> Part 46's survey science asks: the same means, but the same spread, and the "
           "same subgroups?", tag=published_tag(r"Argyle et al.\ (2023)"))

    def chart(self):
        d = load("silicon")
        head = heading(r"Five groups, \ human and silicon")
        A = axes([0.3, 5.7], [1, 7], x_length=5.6, y_length=3.0, xticks=None, yticks=[2, 4, 6],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"group mean (1 to 9)", center=[-3.3, 0.3, 0], font_size=12)
        x = np.arange(1, 6)
        bh = bars(A.ax, x - 0.18, d["human_group"], PERSON, width=0.34)
        bs = bars(A.ax, x + 0.18, d["silicon_group"], MODEL, width=0.34)
        names = VGroup(*[label(rf"{100 * s:.0f}\%", font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 1), DOWN,
                                                                                       buff=0.1)
                         for i, s in enumerate(d["shares"])])
        nl = label(r"share of the population", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        key = VGroup(label(r"people", font_size=13, color=PERSON), label(r"silicon", font_size=13, color=MODEL))
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (rf"overall means match: \ {d['human_mean']:.2f} against {d['silicon_mean']:.2f}", GOOD),
            (rf"spread does not: \ SD {d['human_sd']:.1f} for people, \ {d['silicon_sd']:.1f} for silicon: \ your "
             rf"third number", AUTH),
            (rf"the smallest group is off by {d['group_error'][-1]:+.1f} points: \ pulled toward the majority", AUTH),
            (r"use silicon samples for pilots and wording; \ test claims about people on people", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{machines.silicon}, \ 5,000 respondents")
        with self.voiceover(
            "Here's that test in Psyche. Five groups answer a survey question, and silicon respondents answer from "
            "what a model has absorbed. <bookmark mark='a'/> The overall means match. <bookmark mark='b'/> The spread "
            "doesn't: a standard deviation of one point seven for people, and zero point seven for silicon. That's "
            "your third number. <bookmark mark='c'/> And the smallest group is off by almost a point, pulled toward "
            "the majority. <bookmark mark='d'/> So use silicon samples for pilots and wording, and test claims about "
            "people on people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(nl), FadeIn(key), FadeIn(bh), FadeIn(bs))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
