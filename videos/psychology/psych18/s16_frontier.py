from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.rhythm()
        self.machines()

    def card(self):
        card = chapter_card(15, r"Frontier: \ is attention one thing?", r"Is there such a thing as attention at all?",
                            lit={2012: r"Landau \& Fries", 2017: r"Vaswani et al."}, part=PART,
                            scale=("circuit", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: is attention one thing?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = VGroup(label(r"what is solid", font_size=24, color=GOOD), *[wrapped_label(t, 5.6, 21, WHITE) for t in (
            r"selection by location, \ feature and object",
            r"cueing, \ search slopes, \ the blink, \ Stroop",
            r"inattentional and change blindness",
            r"attention changes neural gain, \ as normalization predicts")]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right = VGroup(label(r"what is argued", font_size=24, color=BAD), *[wrapped_label(t, 5.6, 21, WHITE) for t in (
            r"whether attention is one mechanism or a family sharing a name",
            r"capacity limit, \ or a choice about what to process",
            r"what conflict-driven control really is",
            r"how far training or habits change it")]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.4, 0])
        with self.voiceover(
            "Where does the field stand? <bookmark mark='a'/> Solid: attention selects by location, by feature and "
            "by object. The cueing effects, search slopes, the blink and Stroop are among the most reliable results "
            "in psychology, inattentional and change blindness are robust, and attending changes the gain of "
            "neurons in the way normalization predicts. <bookmark mark='b'/> Argued: whether attention is one "
            "mechanism or a family of them that share a word; whether its limits are limits of capacity or choices "
            "about what to spend effort on; what conflict-driven control really is; and how far training or habits "
            "can change any of it. Some researchers have argued that the word attention has outlived its "
            "usefulness, and that we should name the separate mechanisms instead."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in left], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in right], lag_ratio=0.4), run_time=3.0)
        self.clear_scene()

    def rhythm(self):
        head = heading(r"Does attention flicker?")
        A = axes([0, 1.0], [0, 1], x_length=7.0, y_length=2.4, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[],
                 xlabel=r"time after a cue, \ s", ylabel=r"detection, \ schematic", center=[0, 1.1, 0], font_size=17)
        ax = A.ax
        t = np.linspace(0, 1, 400)
        c1 = curve(ax, t, 0.55 + 0.25 * np.sin(2 * np.pi * 4 * t), ATT, 4)
        c2 = curve(ax, t, 0.55 - 0.25 * np.sin(2 * np.pi * 4 * t), CUE, 3)
        lg = legend([(ATT, r"one location"), (CUE, r"the other")], font_size=18).next_to(A, RIGHT, buff=0.3)
        keep_in_frame(lg)
        rows = rows_of([
            (r"2012: \ after a flash, \ detection at two places rises and falls, \ out of phase, \ about four times "
             r"a second", WHITE),
            (r"as if attention samples locations in turn, \ rhythmically, \ even when it seems to hold still", ATT),
            (r"the evidence is contested: \ the rhythms are small, \ and the statistics of finding them are delicate",
             BAD),
        ], 12.4, 25, 0.32).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "One frontier asks whether attention is steady at all. <bookmark mark='a'/> In 2012 Ayelet Landau and "
            "Pascal Fries flashed a cue and then measured detection at two locations at many moments afterwards. "
            "Detection rose and fell about four times a second, and the two places alternated. "
            "<bookmark mark='b'/> It looked as if attention samples locations in turn, rhythmically, even when we "
            "feel it holding still. The curves here are a schematic of that pattern. <bookmark mark='c'/> It is "
            "contested. The rhythms are small, and later analyses argued that some methods for detecting them find "
            "rhythms in noise. Rhythmic sampling is a hypothesis under test, not a result."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), FadeIn(lg), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def machines(self):
        head = heading(r"Attention in machines")
        eq = MathTex(r"\text{attention}(Q, K, V) = \text{softmax}\!\Big(\frac{Q K^\top}{\sqrt{d}}\Big)\,V",
                     font_size=40, color=CONTROL).move_to([0, 1.9, 0])
        rows = rows_of([
            (r"2017: \ the transformer: \ every word weighs every other by a softmax of their match", CONTROL),
            (r"like biased competition, \ the weights are normalized: \ they share a fixed budget", ATT),
            (r"unlike it, \ nothing is lost: \ every input is processed, \ in parallel, \ at no capacity cost", CUE),
            (r"a shared word, \ a loose analogy: \ \emph{AI, \ Built} derives it; \ Part 60 compares the two", YOU),
        ], 12.4, 26, 0.34).move_to([0, -0.5, 0])
        with self.voiceover(
            "The word attention now has a second home. <bookmark mark='a'/> In 2017 Ashish Vaswani and colleagues "
            "built a language model, the transformer, around an operation they called attention: each word's "
            "representation is updated by a weighted sum of all the others, with weights from a softmax of how well "
            "they match. <bookmark mark='b'/> Like biased competition, the weights are normalized; they share a fixed "
            "budget. <bookmark mark='c'/> Unlike the brain's, nothing is filtered out or lost: every input is "
            "processed in parallel, with no bottleneck and no capacity cost. <bookmark mark='d'/> It is a shared "
            "word and a loose analogy. AI, Built derives the transformer, and Part 60 of this series asks what, if "
            "anything, the two kinds of attention have in common."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
