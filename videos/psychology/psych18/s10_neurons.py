from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Neurons(VoiceoverScene):
    def construct(self):
        self.card()
        self.v4()
        self.derive()
        self.gains()

    def card(self):
        card = chapter_card(9, r"What attention does to a neuron", r"Is attention a filter, \ a gain, \ or a competition?",
                            lit={1985: r"Moran \& Desimone", 1995: r"Desimone \& Duncan", 2009: r"Reynolds \& Heeger"},
                            part=PART, scale=("neuron", "circuit"), marr=("how", "tissue"))
        with self.voiceover("Chapter nine. What attention does to a neuron."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def v4(self):
        head = heading(r"Two stimuli in one receptive field")
        rf = Circle(1.25, color=GREY_B, stroke_width=3).move_to([-3.8, 1.0, 0])
        good = Rectangle(width=0.18, height=0.8, stroke_width=0, fill_color=TARGET, fill_opacity=1).move_to(
            rf.get_center() + LEFT * 0.55)
        poor = Rectangle(width=0.18, height=0.8, stroke_width=0, fill_color=DIST, fill_opacity=1).move_to(
            rf.get_center() + RIGHT * 0.55)
        rl = label(r"a V4 neuron's receptive field", font_size=19, color=GREY_B).next_to(rf, DOWN, buff=0.15)
        legend_ = VGroup(label(r"red: \ the stimulus it prefers", font_size=18, color=TARGET),
                         label(r"green: \ one it barely responds to", font_size=18, color=DIST))
        legend_.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(rl, DOWN, buff=0.15)
        A = axes([0, 4], [0, 1.1], x_length=5.4, y_length=2.6, xticks=[], yticks=[0, 0.5, 1],
                 ylabel=r"response, \ schematic", center=[2.9, 1.2, 0], font_size=16)
        ax = A.ax
        vals = [(1.0, TARGET, r"preferred alone"), (0.15, DIST, r"poor alone"), (0.9, ATT, r"both; \ attend red"),
                (0.25, CUE, r"both; \ attend green")]
        bars = VGroup()
        for k, (v, col, name) in enumerate(vals):
            lo, hi = ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, v)
            bars.add(VGroup(Rectangle(width=0.8, height=hi[1] - lo[1], stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]),
                            wrapped_label(name, 1.2, 15, col).next_to(lo, DOWN, buff=0.1)))
        rows = rows_of([
            (r"1985: \ Moran and Desimone record from monkeys' V4 with two stimuli inside one receptive field", WHITE),
            (r"the response follows the attended stimulus, \ as if the other were not there", ATT),
            (r"in V1, \ with smaller fields, \ the effect is much weaker", GREY_A),
            (r"biased competition: \ stimuli compete for a neuron, \ and attention biases the contest", CONTROL),
        ], 12.4, 25, 0.28).to_edge(DOWN, buff=0.75)
        tag = published_tag(archive.MORAN_DESIMONE_1985.cite)
        with self.voiceover(
            "What does attending do inside the brain? <bookmark mark='a'/> In 1985 Jeffrey Moran and Robert Desimone "
            "recorded from neurons in area V4 of monkeys trained to attend to one of two stimuli, both placed inside "
            "one neuron's receptive field. One stimulus was the kind the neuron liked; the other drove it weakly. "
            "<bookmark mark='b'/> With attention on the preferred stimulus, the neuron responded as if it were alone. "
            "With attention on the poor one, the response collapsed, as if the preferred stimulus had vanished from "
            "the field. The bars here are a schematic of that pattern, not their data. <bookmark mark='c'/> In V1, "
            "where receptive fields are small and rarely hold two objects, the effect was much weaker. "
            "<bookmark mark='d'/> Desimone and John Duncan, in 1995, generalized it as biased competition: stimuli "
            "compete for a neuron's response, and attention, along with salience and expectation, biases the contest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rf), FadeIn(rl), FadeIn(good), FadeIn(poor), FadeIn(legend_))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(bars[0]), FadeIn(bars[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]), FadeIn(bars[3]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derived: \ the normalization model of attention")
        lines = VGroup(
            MathTex(r"R = \frac{E}{S + \sigma}", font_size=44),
            MathTex(r"S = \text{pool}\big(E\big)", font_size=40),
            MathTex(r"R = \frac{A\,E}{\text{pool}\big(A\,E\big) + \sigma}", font_size=44, color=ATT),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-3.6, 0.9, 0])
        notes = VGroup(
            wrapped_label(r"a neuron's drive $E$, \ divided by the activity of its neighbours: \ normalization, \ "
                          r"found all over cortex", 5.2, 21, GREY_A),
            wrapped_label(r"the suppressive drive $S$ pools $E$ over nearby places and features", 5.2, 21, CONTROL),
            wrapped_label(r"attention multiplies the drive by an attention field $A$ before normalization, \ "
                          r"inside the pool too", 5.2, 21, ATT),
        )
        for n, l in zip(notes, lines):
            n.next_to(l, RIGHT, buff=0.5)
            keep_in_frame(n)
        rows = rows_of([
            (r"Heeger, \ 1992: \ normalization explains contrast saturation and cross-orientation suppression", WHITE),
            (r"Reynolds and Heeger, \ 2009: \ add one multiplication, \ and the attention data fall into place", ATT),
            (r"two objects in a field: \ the attended one's drive dominates the pool, \ so it dominates the response",
             CONTROL),
        ], 12.4, 24, 0.24).to_edge(DOWN, buff=0.75)
        tag = published_tag(archive.REYNOLDS_HEEGER_2009.cite)
        with self.voiceover(
            "The recordings that followed seemed to disagree, until one model reconciled them. "
            "<bookmark mark='a'/> Start with normalization: a neuron's excitatory drive, E, divided by the pooled "
            "activity of its neighbours, plus a constant. David Heeger proposed it in 1992 for primary visual "
            "cortex, where it explains why responses saturate as contrast rises and why one orientation suppresses "
            "another; it has since been found almost everywhere in cortex. <bookmark mark='b'/> The pool, S, sums the "
            "drive over nearby places and features. <bookmark mark='c'/> In 2009 John Reynolds and Heeger added one "
            "step. Attention is a field, A, that multiplies the drive before normalization: in the numerator, and "
            "inside the pool. That is the whole model. <bookmark mark='d'/> Moran and Desimone's result falls out: "
            "with two stimuli in the field, the attended one's multiplied drive dominates the pool, so it dominates "
            "the response."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(lines[0]), FadeIn(notes[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def gains(self):
        d = load("normalize")
        head = heading(r"Contrast gain or response gain: \ it depends on size")
        c = d["c"]
        panels = VGroup()
        for k, (name, title, sub) in enumerate([("small", r"a small stimulus, \ a broad attention field",
                                                 r"contrast gain: \ the curve shifts left"),
                                                ("large", r"a large stimulus, \ a narrow attention field",
                                                 r"response gain: \ the curve scales up")]):
            top = max(d[f"{name}_a"].max(), d[f"{name}_u"].max()) * 1.1
            A = axes([-2, 0], [0, top], x_length=4.8, y_length=2.3, xticks=[-2, -1, 0], yticks=[],
                     xfmt=lambda v: {-2: "1\\%", -1: "10\\%", 0: "100\\%"}[int(v)], xlabel=r"contrast",
                     center=[-3.4 + 6.8 * k, 0.7, 0], font_size=16)
            ax = A.ax
            lc = np.log10(c)
            cu = curve(ax, lc, d[f"{name}_u"], GREY_B, 3)
            ca = curve(ax, lc, d[f"{name}_a"], ATT, 4)
            t = label(title, font_size=19, color=WHITE).next_to(ax, UP, buff=0.2)
            s = label(sub, font_size=19, color=ATT).next_to(A, DOWN, buff=0.1)
            ratio = (rf"$c_{{50}}$ $\times$ {d[f'{name}_c50']:.2f}, \ $R_{{max}}$ $\times$ {d[f'{name}_rmax']:.2f}")
            r_ = label(ratio, font_size=17, color=MODEL).next_to(s, DOWN, buff=0.08)
            panels.add(VGroup(A, t, cu, ca, s, r_))
        key = legend([(GREY_B, r"attending elsewhere"), (ATT, r"attending here")], font_size=18)
        key.arrange(RIGHT, buff=0.6).move_to([0, 2.9, 0])
        rows = rows_of([
            (r"some studies found attention acts like more contrast; \ others, \ like a bigger response", WHITE),
            (r"the model: \ a broad attention field around a small stimulus boosts the drive and the pool alike", ATT),
            (r"a narrow field inside a large stimulus boosts the drive but little of the pool", CONTROL),
            (r"Herrmann and colleagues, \ 2010: \ change the sizes in people, \ and the effect switches as predicted",
             DATA),
        ], 12.4, 23, 0.16).to_edge(DOWN, buff=0.7)
        ptag = psyche_tag(r"\texttt{attention.normalization\_crf}: \ one dimension of space, \ attention gain 2")
        tag = published_tag(archive.REYNOLDS_HEEGER_2009.cite)
        with self.voiceover(
            "The model's best trick concerns a long-running dispute. <bookmark mark='a'/> Some experiments found that "
            "attention acts like turning up a stimulus's contrast: the whole contrast-response curve shifts to the "
            "left. Others found it scales the response: the curve stretches upward. <bookmark mark='b'/> In the "
            "normalization model, the answer depends on the sizes. With a small stimulus and a broad attention field, "
            "attention multiplies the drive and the pool alike, so at high contrast they cancel and only the "
            "midpoint moves: contrast gain. <bookmark mark='c'/> With a large stimulus and a narrow attention field, "
            "attention multiplies the neuron's own drive but only a small part of the pool, so the whole curve "
            "scales: response gain. Psyche's one-dimensional version shows both. <bookmark mark='d'/> In 2010 "
            "Katrin Herrmann, Marisa Carrasco, Heeger and colleagues tested the prediction in people, changing the "
            "stimulus size and the spread of attention, and found the switch from one kind of gain to the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag), FadeIn(key), *[FadeIn(p[0]) for p in panels],
                      *[FadeIn(p[1]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(panels[0][2]), Create(panels[1][2]))
            vo.wait_until("b")
            self.play(Create(panels[0][3]), FadeIn(panels[0][4]), FadeIn(panels[0][5]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(panels[1][3]), FadeIn(panels[1][4]), FadeIn(panels[1][5]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
