from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Words(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Communication as policy", r"Why did central banks start talking, \ and what do their words "
             r"do?", "Chapter thirteen. Communication as policy.",
             lit={1994: r"the first statement", 2012: r"the dots"}, scale=("market", "nation"),
             horizon=("a minute", "years"))
        self.timeline()
        self.tantrum()

    def timeline(self):
        items = [
            (1994, r"February 1994: \ the first statement after a meeting", CB),
            (2011, r"April 2011: \ the chair's first press conference after a meeting", RATE),
            (2012.0, r"January 2012: \ a numerical goal, \ 2\% inflation; \ the first ``dots''", PRICE),
            (2012.95, r"December 2012: \ guidance tied to unemployment", OUTPUT),
        ]
        head = label(r"from secrecy to guidance", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        before = label(r"until 1994 the Federal Reserve did not say what it had decided: \ markets inferred it from "
                       r"its trading", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.4)
        rows = VGroup(*[label(t, font_size=23, color=c) for _, t, c in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.35)
        rows.next_to(before, DOWN, buff=0.5)
        why = label(r"if expectations do the work, \ shaping them is the policy", font_size=24, color=WHITE).to_edge(
            DOWN, buff=0.7)
        tag = published_tag(r"Federal Reserve: \ FOMC statements and press conferences; \ Statement on Longer-Run "
                            r"Goals, \ 25 January 2012", corner=DR, font_size=12)
        with self.voiceover(
            "For most of its history the Federal Reserve said as little as possible. <bookmark mark='a'/> Until "
            "1994 it did not even announce its decisions: markets inferred them from its trading. "
            "<bookmark mark='b'/> In February 1994 it issued its first statement after a meeting. "
            "<bookmark mark='c'/> In April 2011 the chair held the first regular press conference. "
            "<bookmark mark='d'/> In January 2012 it adopted a numerical goal of two percent inflation, and began "
            "publishing each policymaker's projection of the rate, the dots. <bookmark mark='e'/> In December "
            "2012 it tied its guidance to unemployment. <bookmark mark='f'/> The reason is the theory of the last "
            "two parts: if expectations do much of the work, then shaping them is the policy, and a central bank "
            "that is understood needs to move its rate less."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(before))
            for mk, r_ in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(why))
        self.clear_scene()

    def tantrum(self):
        T = load("tantrum")
        ax = plane([2012.5, 2014.5], [1, 3.5], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2013, 2014], yticks=[1, 1.5, 2, 2.5, 3, 3.5], ylabel=r"10-year Treasury yield, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=15)
        y = path(ax, T["t"], T["y"], BOND, 2.6, smooth=False)
        day = vline(ax, 2013 + 141 / 365, 1, 3.5, E.ACCENT, 2.5)
        side = VGroup(
            label(r"22 May 2013: \ Bernanke tells Congress \\ the Fed could slow its purchases \\ in the next few "
                  r"meetings", font_size=17, color=E.ACCENT),
            label(rf"the day before: \ {T['before']:.2f}\%", font_size=17, color=BOND),
            label(rf"by the end of 2013: \ {T['peak']:.2f}\%, \\ up {T['rise_bp']:.0f} basis points", font_size=17,
                  color=INFL),
            label(r"the Fed did not decide to slow them \\ until December", font_size=17, color=GREY_A),
            label(r"a sentence about the future \\ moved the price of money now", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Bernanke, \ testimony to the Joint Economic Committee, \ 22 May 2013; \ DGS10 via FRED",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Words move prices, sometimes more than intended. <bookmark mark='a'/> On the twenty-second of May "
            "2013, Ben Bernanke told Congress that the Fed might slow its bond purchases in the next few meetings, "
            "if the economy kept improving. <bookmark mark='b'/> The ten-year yield had been "
            f"{T['before']:.2f} percent the day before. <bookmark mark='c'/> By the end of the year it was "
            f"{T['peak']:.2f} percent, {T['rise_bp']:.0f} basis points higher: the taper tantrum. "
            "<bookmark mark='d'/> The Fed did not decide to slow its purchases until December. "
            "<bookmark mark='e'/> A sentence about the future had tightened financial conditions without any "
            "change in policy at all: the expectations channel, working in a direction the speaker had not "
            "intended."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(y), run_time=2)
            vo.wait_until("a")
            self.play(Create(day), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
