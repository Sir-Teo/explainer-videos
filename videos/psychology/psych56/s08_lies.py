from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Lies(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Detecting lies", r"Can anyone tell when someone is lying?")
        self.chance()
        self.polygraph()

    def chance(self):
        head = heading(r"Fifty-four percent")
        A = axes([0.3, 3.7], [0, 0.8], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 0.8],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"judgements correct", center=[-3.5, 0.3, 0], font_size=12)
        b = bars(A.ax, [1, 2, 3], [0.54, 0.61, 0.47], [MODEL, GOOD, AUTH], width=0.6)
        h = DashedLine(A.ax.c2p(0.3, 0.5), A.ax.c2p(3.7, 0.5), color=GREY_B)
        names = VGroup(*[label(s, font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"overall", r"truths", r"lies"])])
        rows = rows_of([
            (r"Bond and DePaulo, \ 2006: \ 206 studies, \ about 24,000 judges: \ 54\% correct, \ where 50\% is "
             r"chance", WHITE),
            (r"people judge truths better than lies: \ a truth bias, \ Part 12's criterion set toward ``believe''",
             MODEL),
            (r"police officers and other professionals do little better, \ and are more confident", AUTH),
            (r"the cues people use, \ averted gaze, \ fidgeting, \ are barely related to lying: \ the signal is weak, \ "
             r"so no criterion can do much", PERSON),
        ], 6.2, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = published_tag(r"Bond \& DePaulo (2006)")
        with self.voiceover(
            "Can anyone tell when someone is lying? <bookmark mark='a'/> In 2006 Charles Bond and Bella DePaulo "
            "pooled two hundred and six studies with about twenty-four thousand judges. They were right fifty-four "
            "percent of the time, where fifty is chance. <bookmark mark='b'/> People judge truths better than lies: a "
            "truth bias, Part 12's criterion set toward believing. <bookmark mark='c'/> Police officers and other "
            "professionals do little better, and they're more confident. <bookmark mark='d'/> The cues people use, "
            "averted gaze and fidgeting, are barely related to lying. The signal is weak, so no criterion can do "
            "much."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), Create(h))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]), FadeIn(b[2]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def polygraph(self):
        rows_section(self, r"The polygraph", [
            (r"it records arousal: \ breathing, \ sweating, \ heart rate; \ arousal is not deception", WHITE),
            (r"the US National Research Council's 2003 review: \ better than chance in specific-incident testing, \ "
             r"far from perfect, \ and unsound for screening many people for rare spies", AUTH),
            (r"the screening problem is Part 51's alarm: \ at a low base rate, \ most alarms are false", MODEL),
            (r"brain-scan lie detection (Part 8's row) has not done better outside the laboratory; \ the most "
             r"promising methods ask what a suspect knows, \ not whether they are nervous", PERSON),
        ], "And machines? <bookmark mark='a'/> The polygraph records arousal: breathing, sweating and heart rate. But "
           "arousal isn't deception. <bookmark mark='b'/> In 2003 the US National Research Council's review found it "
           "better than chance in testing about a specific incident, far from perfect, and unsound for screening "
           "many people for a few spies. <bookmark mark='c'/> The screening problem is Part 51's alarm: at a low base "
           "rate, most alarms are false. <bookmark mark='d'/> Brain-scan lie detection, Part 8's row, hasn't done "
           "better outside the laboratory. The most promising methods ask what a suspect knows, not whether they're "
           "nervous.")
