from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.sampler()
        self.time()

    def card(self):
        card = chapter_card(6, r"Models of context effects", r"What kind of chooser bends with the menu?",
                            lit={1972: r"Tversky", 2001: r"Roe et al."}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter six. Models of context effects."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def sampler(self):
        d = load("decoy")
        head = heading(r"A chooser who compares")
        A = axes([0.3, 5.7], [0, 0.8], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5, 0.75],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share choosing A", center=[-3.3, 0.3, 0], font_size=13)
        vals = [d["pair_40"][0], d["decoy_A_40"][0], d["decoy_B_40"][0], d["extreme_B_40"][0], d["extreme_A_40"][0]]
        cols = [GREY_B, GOOD, AUTH, GOOD, AUTH]
        b = bars(A.ax, [1, 2, 3, 4, 5], vals, cols, width=0.6)
        names = VGroup(*[wrapped_label(t, 1.1, 11, GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, t in
                         enumerate((r"A and B", r"+ decoy for A", r"+ decoy for B", r"+ extreme beyond A",
                                    r"+ extreme beyond B"))])
        half = DashedLine(A.ax.c2p(0.3, 0.5), A.ax.c2p(5.7, 0.5), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (r"Psyche deliberates by comparing: \ at each moment, \ one pair of options on one attribute; \ the "
             r"better gains, \ the worse loses, \ and losses loom larger", WHITE),
            (rf"a decoy for A loses to A on everything: \ A's share rises from 50\% to {100 * d['decoy_A_40'][0]:.0f}\%; "
             rf"\ a decoy for B lowers it to {100 * d['decoy_B_40'][0]:.0f}\%", GOOD),
            (rf"an extreme option beyond A puts A in the middle, \ where it never loses by much: \ "
             rf"{100 * d['extreme_B_40'][0]:.0f}\% against {100 * d['extreme_B_40'][1]:.0f}\%", MODEL),
            (r"one mechanism, \ two effects, \ and no change in what A or B is worth", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.pairwise\_sampler}, \ 60{,}000 simulated choices each")
        with self.voiceover(
            "What kind of chooser bends with the menu? <bookmark mark='a'/> Psyche deliberates by comparing. At each "
            "moment it looks at one pair of options on one attribute. The better one gains, the worse one loses, and "
            "losses loom larger than gains. <bookmark mark='b'/> A decoy for A loses to A on everything, so A gains, "
            "from fifty percent to about three quarters. A decoy for B does the opposite. <bookmark mark='c'/> An "
            "extreme option on the far side of A puts A in the middle, where it never loses by much, and A's share rises. "
            "<bookmark mark='d'/> One mechanism, two effects, and no change in what A or B is worth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(half))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[3]), FadeIn(b[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def time(self):
        d = load("decoy")
        head = heading(r"More thought, \ more context")
        A = axes([0, 85], [0.2, 0.9], x_length=5.6, y_length=3.2, xticks=[0, 20, 40, 60, 80], yticks=[0.3, 0.5, 0.7, 0.9],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"comparisons before choosing",
                 ylabel=r"share choosing A", center=[-3.3, 0.3, 0], font_size=13)
        c1 = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.07, color=GOOD) for x, y in zip(d["steps_grid"], d["decoy_by_steps"])])
        c2 = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.07, color=MODEL) for x, y in zip(d["steps_grid"], d["comp_by_steps"])])
        l1 = curve(A.ax, d["steps_grid"], d["decoy_by_steps"], GOOD, stroke_width=2)
        l2 = curve(A.ax, d["steps_grid"], d["comp_by_steps"], MODEL, stroke_width=2)
        key = VGroup(label(r"with a decoy for A", font_size=13, color=GOOD),
                     label(r"A in the middle", font_size=13, color=MODEL)).arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"in the model, \ both effects grow with deliberation: \ more comparisons, \ more chances for the menu "
             r"to act", WHITE),
            (r"the compromise effect needs many comparisons; \ with few, \ it vanishes", MODEL),
            (r"a testable prediction: \ time pressure should shrink context effects; \ experiments have found it "
             r"for the compromise effect", GOOD),
            (r"sequential-sampling accounts of choice (Part 25's accumulators, \ with several options) make the "
             r"same kind of prediction", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.pairwise\_sampler}")
        with self.voiceover(
            "The model also says when these effects should appear. <bookmark mark='a'/> Both grow with "
            "deliberation. More comparisons give the menu more chances to act. <bookmark mark='b'/> The compromise "
            "effect needs many comparisons. With few, it vanishes. <bookmark mark='c'/> That's a testable prediction: "
            "time pressure should shrink context effects. Experiments have found that for the compromise effect. "
            "<bookmark mark='d'/> The sequential-sampling models of Part 25, extended to several options, make the "
            "same kind of prediction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(c1), Create(l1), FadeIn(c2), Create(l2))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
