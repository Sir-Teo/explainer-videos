from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


class Attention(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.history()
        self.verdict()

    def card(self):
        card = chapter_card(9, r"Attention to cues", r"Which cues are worth learning about?",
                            lit={1975: r"Mackintosh", 1980: r"Pearce \& Hall"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter nine. Attention to cues."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rules(self):
        head = heading(r"Let $\alpha$ learn")
        left = VGroup(
            label(r"Mackintosh, \ 1975", font_size=30, color=CUE_A),
            wrapped_label(r"attend to the cues that predict best", 5.4, 26, WHITE),
            MathTex(r"\Delta\alpha_X \propto -\big(|\lambda - V_X| - |\lambda - V_{\text{others}}|\big)", font_size=32),
            wrapped_label(r"a cue that beats the others gains attention; \ a worse one loses it", 5.4, 23, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(
            label(r"Pearce and Hall, \ 1980", font_size=30, color=CS),
            wrapped_label(r"attend to the cues whose consequences are uncertain", 5.4, 26, WHITE),
            MathTex(r"\alpha_X \leftarrow \gamma\,|\lambda - \textstyle\sum V| + (1-\gamma)\,\alpha_X", font_size=32),
            wrapped_label(r"a cue followed by surprises stays interesting; \ a well-understood one is ignored",
                          5.4, 23, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.2, 0])
        tag = historical_tag(archive.MACKINTOSH_PEARCE_HALL.cite)
        with self.voiceover(
            "Latent inhibition says that animals learn not only what cues predict but which cues to pay attention to. "
            "In Rescorla-Wagner, a cue's learning rate, alpha, is fixed. Two theories let it learn, and they "
            "disagree about how. <bookmark mark='a'/> Nicholas Mackintosh, in 1975: attend to the cues that predict "
            "best. A cue whose own prediction is better than the others' gains attention; a cue that does worse loses "
            "it. That explains blocking a second way: the light is a worse predictor than the noise, so the rat stops "
            "attending to it. <bookmark mark='b'/> John Pearce and Geoffrey Hall, in 1980, said nearly the opposite: "
            "attend to the cues whose consequences are still uncertain. A cue followed by surprises keeps its "
            "attention; once you know what a cue means, you can stop watching it. That explains latent inhibition: "
            "a tone followed, reliably, by nothing becomes boring, and is learned about slowly afterwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[1:]))
            vo.wait_until("b")
            self.play(FadeIn(right[1:]))
        self.clear_scene()

    def history(self):
        d = load("attention")
        head = heading(r"The same history, \ opposite attention")
        x = np.arange(len(d["mack_A"]))
        mk = axes([0, 160], [0, 1.05], x_length=5.4, y_length=3.0, xticks=[0, 80, 160], yticks=[0, 0.5, 1],
                  xlabel=r"trial", ylabel=r"attention, \ $\alpha$", center=[-3.5, -0.1, 0], font_size=18)
        ph = axes([0, 160], [0, 1.05], x_length=5.4, y_length=3.0, xticks=[0, 80, 160], yticks=[0, 0.5, 1],
                  xlabel=r"trial", ylabel=r"attention, \ $\alpha$", center=[3.3, -0.1, 0], font_size=18)
        t1 = label(r"Mackintosh", font_size=26, color=CUE_A).next_to(mk.ax, UP, buff=0.15)
        t2 = label(r"Pearce-Hall", font_size=26, color=CS).next_to(ph.ax, UP, buff=0.15)
        curves = VGroup(curve(mk.ax, x, d["mack_A"], CR, 4), curve(mk.ax, x, d["mack_B"], US, 4),
                        curve(ph.ax, x, d["ph_A"], CR, 4), curve(ph.ax, x, d["ph_B"], US, 4))
        lg = legend([(CR, r"A: \ always followed by food"), (US, r"B: \ followed by food half the time")], font_size=21)
        lg.arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.3)
        rows = rows_of([
            (r"Mackintosh: \ attention to A, \ the reliable predictor", CUE_A),
            (r"Pearce-Hall: \ attention to B, \ the one that keeps surprising", CS),
        ], 12.4, 25, 0.2).to_edge(DOWN, buff=0.6)
        tag = psyche_tag(r"computed: \ \texttt{conditioning.mackintosh} and \texttt{pearce\_hall}")
        with self.voiceover(
            "Give both models one history. <bookmark mark='a'/> Cue A is always followed by food. Cue B is followed "
            "by food half the time, at random. <bookmark mark='b'/> Mackintosh's animal learns to attend to A, the "
            "cue that predicts reliably, and to tune B out. <bookmark mark='c'/> Pearce and Hall's animal does the "
            "reverse: A has been figured out and loses attention, while B, which keeps producing surprises, holds it. "
            "Same experience, opposite attention."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lg), FadeIn(mk), FadeIn(ph), FadeIn(t1), FadeIn(t2))
            vo.wait_until("b")
            self.play(Create(curves[0]), Create(curves[1]), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(curves[2]), Create(curves[3]), FadeIn(rows[1]), run_time=2.0)
        self.clear_scene()

    def verdict(self):
        head = heading(r"Which is right? \ Both, \ it seems")
        rows = rows_of([
            (r"people learn new things faster about cues that were predictive before: \ Mackintosh's signature",
             CUE_A),
            (r"and attend more to cues whose outcomes were uncertain: \ Pearce and Hall's", CS),
            (r"hybrid models combine the two; \ reviews of human learning find evidence for both processes", YOU),
            (r"attention, \ learned from prediction errors, \ is where conditioning meets Part 18", GREY_A),
        ], 12.4, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Which one describes real animals? <bookmark mark='a'/> In people, cues that were good predictors in one "
            "task are learned about faster in the next, which is Mackintosh's signature, and it shows in where people "
            "look. <bookmark mark='b'/> But people also attend more to cues whose outcomes were uncertain, which is "
            "Pearce and Hall's. <bookmark mark='c'/> So the current answer is both, perhaps for different purposes: "
            "exploiting what predicts, and exploring what doesn't yet. Hybrid models combine the two, and reviews of "
            "human learning find evidence for each. <bookmark mark='d'/> Attention that is itself learned from "
            "prediction errors is where conditioning meets the study of attention, in Part 18."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
