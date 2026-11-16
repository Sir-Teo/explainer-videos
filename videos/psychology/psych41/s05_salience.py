from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Salience(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.model()

    def card(self):
        card = chapter_card(4, r"Aberrant salience", r"Why does the irrelevant start to matter?",
                            lit={2003: r"Kapur"}, part=PART, scale=("circuit", "person"), marr=("what", "how"))
        with self.voiceover("Chapter four. Aberrant salience."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"When everything seems to mean something")
        rows = rows_of([
            (r"Part 17: \ dopamine carries a prediction error, \ and marks what deserves attention and learning", SYMP),
            (r"Kapur, \ 2003: \ in psychosis, \ dopamine fires out of step with events, \ and lends significance to "
             r"things that have none", AUTH),
            (r"a number plate, \ a song on the radio, \ a stranger's glance begin to feel meant", PERSON),
            (r"a delusion is then the explanation a person builds for a world that has started to feel strange: \ "
             r"a reasonable inference from unreasonable inputs", MODEL),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Kapur (2003)")
        with self.voiceover(
            "How could too much dopamine produce a delusion? <bookmark mark='a'/> In Part 17, dopamine carried a "
            "prediction error, and marked what deserves attention and learning. <bookmark mark='b'/> In 2003 Shitij "
            "Kapur proposed that in psychosis, dopamine fires out of step with events, and lends significance to "
            "things that have none. <bookmark mark='c'/> A number plate, a song on the radio, a stranger's glance, "
            "begin to feel meant. <bookmark mark='d'/> A delusion is then the explanation a person builds for a world "
            "that has started to feel strange. A reasonable inference, from unreasonable inputs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        d = load("salience")
        head = heading(r"Salience, \ computed")
        panels = VGroup()
        for q, c in ((0, GOOD), (20, AUTH)):
            V = d[f"V{q}"]
            A = axes([0, 21], [-0.2, 1.3], x_length=5.2, y_length=2.2, xticks=None, yticks=[0, 0.5, 1.0],
                     yfmt=lambda v: f"{v:.1f}", xlabel=r"cue (1 is rewarded)", ylabel=r"learned value",
                     font_size=12)
            cols = [PERSON] + [c] * (len(V) - 1)
            b = bars(A.ax, np.arange(1, len(V) + 1), V, cols, width=0.7)
            thr = DashedLine(A.ax.c2p(0, 0.25), A.ax.c2p(21, 0.25), color=GREY_B, stroke_width=1.5)
            t = label(rf"bursts on {q}\% of trials: \ {d[f'n{q}']} irrelevant cues above the line", font_size=15,
                      color=c).next_to(A, UP, buff=0.1)
            panels.add(VGroup(A, b, thr, t))
        panels.arrange(DOWN, buff=0.55).move_to([-3.3, -0.4, 0])
        rows = rows_of([
            (r"Psyche: \ twenty cues, \ one followed by reward; \ a Rescorla-Wagner learner over 2{,}000 trials", WHITE),
            (r"normal dopamine: \ only the rewarded cue gains value", GOOD),
            (rf"add random bursts on 20\% of trials: \ every cue gains a little value, \ and {d['n20']} of the "
             rf"nineteen irrelevant ones cross the line", AUTH),
            (r"a model of the idea, \ not a test of it: \ it shows what Kapur's account predicts", YOU),
        ], 5.6, 19, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.aberrant\_salience}, \ median of 21 runs")
        with self.voiceover(
            "Here's the idea in Psyche. <bookmark mark='a'/> Twenty cues, only one of them followed by reward, and a "
            "Rescorla-Wagner learner over two thousand trials. <bookmark mark='b'/> With normal dopamine, only the "
            "rewarded cue gains value. <bookmark mark='c'/> Now add random dopamine bursts on one trial in five. "
            "Every cue gains a little value, and a few of the irrelevant ones cross the line where they'd draw "
            "attention. <bookmark mark='d'/> It's a model of the idea, not a test of it. It shows what Kapur's "
            "account predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels[0][0]), FadeIn(panels[0][2]), FadeIn(panels[1][0]),
                      FadeIn(panels[1][2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(panels[0][1]), FadeIn(panels[0][3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(panels[1][1]), FadeIn(panels[1][3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
