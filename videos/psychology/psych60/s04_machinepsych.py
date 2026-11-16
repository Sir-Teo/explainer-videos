from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class MachinePsych(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Machine psychology", r"What happens when a model sits psychology's tests?")
        self.binz()
        self.contamination()
        self.prompts()

    def binz(self):
        rows_section(self, r"The classic problems, \ given to a model", [
            (r"Binz and Schulz, \ 2023: \ a language model given Part 26's vignettes (the Linda problem, \ framing, "
             r"\ the cognitive reflection test) answered much as people do, \ biases included", WHITE),
            (r"later models solved the same classic items: \ the biases shrank or vanished (Hagendorff and "
             r"colleagues, \ 2023)", MODEL),
            (r"was that reasoning, \ or the items, \ famous and much discussed online, \ in the training text?", AUTH),
            (r"three traps follow, \ each one a lesson from earlier in this series", YOU),
        ], "What happens when a model sits psychology's tests? <bookmark mark='a'/> In 2023 Marcel Binz and Eric "
           "Schulz gave a language model Part 26's vignettes: the Linda problem, framing, and the cognitive "
           "reflection test. It answered much as people do, biases included. <bookmark mark='b'/> Later models solved "
           "the same classic items, and the biases shrank or vanished. <bookmark mark='c'/> Was that reasoning, or "
           "were the items, famous and much discussed online, in the training text? <bookmark mark='d'/> Three traps "
           "follow, and each is a lesson from earlier in this series.", tag=published_tag(r"Binz \& Schulz (2023)"))

    def contamination(self):
        d = load("contam")
        head = heading(r"Trap one: \ contamination")
        A = axes([0.3, 2.7], [0, 1.0], x_length=5.2, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"correct", center=[-3.4, 0.3, 0], font_size=12)
        bm = bars(A.ax, [0.82, 1.82], d["memorizer"], AUTH, width=0.32)
        br = bars(A.ax, [1.18, 2.18], d["reasoner"], GOOD, width=0.32)
        names = VGroup(label(r"published items", font_size=13, color=GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.1),
                       label(r"reworded", font_size=13, color=GREY_A).next_to(A.ax.c2p(2, 0), DOWN, buff=0.1))
        chance = DashedLine(A.ax.c2p(0.3, 0.25), A.ax.c2p(2.7, 0.25), color=GREY_B, stroke_width=1.5)
        key = VGroup(label(r"memorizer", font_size=13, color=AUTH), label(r"reasoner", font_size=13, color=GOOD))
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Psyche's two test-takers: \ one saw 80\% of the published items in training; \ one reasons, \ "
             r"right 56\% of the time", WHITE),
            (rf"on the published items the memorizer wins: \ {100 * d['memorizer'][0]:.0f}\% against "
             rf"{100 * d['reasoner'][0]:.0f}\%", AUTH),
            (rf"reworded, \ with the same logic: \ {100 * d['memorizer'][1]:.0f}\%, \ chance; \ the reasoner keeps "
             rf"{100 * d['reasoner'][1]:.0f}\%: \ your first number", GOOD),
            (r"the remedy is Part 2's: \ new items, \ written after training, \ and perturbed versions of old ones",
             YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{machines.contamination}")
        with self.voiceover(
            "Trap one: contamination. <bookmark mark='a'/> Psyche has two test-takers. One saw eighty percent of the "
            "published items during training. The other reasons, and is right fifty-six percent of the time. "
            "<bookmark mark='b'/> On the published items, the memorizer wins: about eighty-five percent against "
            "fifty-six. <bookmark mark='c'/> Reword them, with the same logic, and the memorizer falls to twenty-five "
            "percent, which is chance. The reasoner keeps fifty-four. That's your first number. "
            "<bookmark mark='d'/> The remedy is Part 2's: new items, written after training, and perturbed versions "
            "of old ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key), Create(chance))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowFromEdge(bm[0], DOWN), GrowFromEdge(br[0], DOWN))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), GrowFromEdge(bm[1], DOWN), GrowFromEdge(br[1], DOWN))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def prompts(self):
        d = load("prompts")
        head = heading(r"Traps two and three: \ prompts, \ and one model")
        A = axes([0, 1], [0.4, 2.6], x_length=5.6, y_length=2.6, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"share of human-like answers", center=[-3.3, 0.6, 0], font_size=12)

        def interval(ci, y, col):
            return VGroup(Line(A.ax.c2p(ci[0], y), A.ax.c2p(ci[1], y), color=col, stroke_width=6),
                          Dot(A.ax.c2p((ci[0] + ci[1]) / 2, y), radius=0.06, color=col))
        n1 = interval(d["one_naive"], 2.0, AUTH)
        h1 = interval(d["one_honest"], 1.0, GOOD)
        ln = label(r"phrasings as subjects", font_size=13, color=AUTH).move_to(A.ax.c2p(0.02, 2.35), aligned_edge=LEFT)
        lh = label(r"models as subjects", font_size=13, color=GOOD).move_to(A.ax.c2p(0.02, 1.35), aligned_edge=LEFT)
        rows = rows_of([
            (r"trap two: \ answers move with wording, \ order and examples in the prompt; \ report many phrasings", WHITE),
            (r"trap three: \ 100 phrasings to one model give a narrow interval: \ the red bar, \ your second number",
             AUTH),
            (r"but models differ from one another; \ for a claim about models, \ the model is the subject, \ and one "
             r"model is a sample of one: \ the green bar", GOOD),
            (r"Part 47's pseudo-replication: \ many measurements of one subject are not many subjects", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{machines.prompt\_sample}")
        with self.voiceover(
            "Traps two and three. <bookmark mark='a'/> Trap two: answers move with the wording, the order, and the "
            "examples in a prompt, so report many phrasings. <bookmark mark='b'/> Trap three: a hundred phrasings to "
            "one model give a narrow interval, the red bar. That's your second number. <bookmark mark='c'/> But "
            "models differ from one another. For a claim about models, the model is the subject, and one model is a "
            "sample of one. The honest interval is the green bar. <bookmark mark='d'/> It's Part 47's "
            "pseudo-replication: many measurements of one subject are not many subjects."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ln), FadeIn(lh))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(h1))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
