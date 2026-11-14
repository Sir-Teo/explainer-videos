from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


class Predictions(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.contingency()
        self.rescorla()

    def card(self):
        card = chapter_card(7, r"What the rule predicts", r"How much follows from one line?",
                            lit={1972: r"Rescorla \& Wagner", 1978: r"Kremer"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter seven. What the rule predicts."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def panel(self, center, title, n, series, ylo=-1.05, yhi=1.05, note=""):
        A = axes([0, n], [ylo, yhi], x_length=3.7, y_length=2.2, xticks=[0, n // 2, n], yticks=[-1, 0, 1] if ylo < 0 else
                 [0, 0.5, 1], xlabel=r"trial", ylabel="", center=center, font_size=17)
        ax = A.ax
        cs = VGroup(*[curve(ax, np.arange(len(y)), y, col, stroke_width=3) for y, col, _ in series])
        lg = legend([(col, name) for _, col, name in series], font_size=18, buff=0.08)
        lg.next_to(A, DOWN, buff=0.2).align_to(ax, LEFT)
        t = wrapped_label(title, 3.9, 22, YOU).next_to(ax, UP, buff=0.25).align_to(ax, LEFT)
        nt = label(note, font_size=17, color=GREY_A).next_to(lg, DOWN, buff=0.1).align_to(ax, LEFT) if note else VGroup()
        return VGroup(A, cs, lg, t, nt)

    def four(self):
        d = load("rw")
        head = heading(r"Three more designs, \ one rule")
        p1 = self.panel([-4.6, 0.9, 0], r"overshadowing: \ a loud cue and a faint one, \ together", 40,
                        [(d["over_A"], CUE_A, r"loud A"), (d["over_X"], CS, r"faint X"),
                         (d["solo_X"], GREY_B, r"X trained alone")], 0, 1.05)
        p2 = self.panel([0.0, 0.9, 0], r"conditioned inhibition: \ A$+$ and AX$-$, \ mixed", 120,
                        [(d["inh_A"], CUE_A, r"A"), (d["inh_X"], INHIB, r"X, \ below zero")])
        p3 = self.panel([4.6, 0.9, 0], r"overexpectation: \ A$+$ and B$+$, \ then AB$+$", 120,
                        [(d["oe_A"], CS, r"A and B \ (the same curve)")], 0, 1.05, r"the compound starts at trial 80")
        for p in (p1, p2, p3):
            keep_in_frame(p)
        rows = rows_of([
            (r"overshadowing: \ the salient cue takes most of the prediction", CUE_A),
            (r"inhibition: \ a cue that signals the outcome's absence goes negative, \ a safety signal", INHIB),
            (r"overexpectation: \ two predictors together predict the outcome twice; \ both lose strength though "
             r"still reinforced", YOU),
        ], 12.6, 23, 0.16).to_edge(DOWN, buff=0.6)
        tag = psyche_tag(r"computed: \ \texttt{conditioning.rescorla\_wagner}")
        with self.voiceover(            "Blocking was the rule's first success. Here are three more. <bookmark mark='a'/> Overshadowing. Train a "
            "loud cue and a faint one together. Both are paired with the outcome every time, but the salient one, "
            "learning faster, takes most of the prediction, and the faint one ends far below where it would be "
            "trained alone. Pavlov saw this. <bookmark mark='b'/> Conditioned inhibition. Cue A is followed by food, "
            "but whenever X accompanies A, no food comes. X can't become negative by being paired with nothing, on "
            "its own. But A's prediction creates an error when A and X appear together, and X goes below zero: it "
            "becomes a safety signal, a cue that the outcome won't happen. <bookmark mark='c'/> And overexpectation, "
            "the prediction nobody expected. Train A and B separately, each until it fully predicts the food. Then "
            "present them together, with the same food. Together they predict two helpings, the error is negative, "
            "and both lose strength, even though both are still being reinforced on every trial. The rule predicts "
            "that reward can weaken learning. In 1978 Edward Kremer tested it with rats, and found exactly that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, p, r in zip("abc", (p1, p2, p3), rows):
                vo.wait_until(m)
                self.play(FadeIn(p[0]), FadeIn(p[3]), FadeIn(p[4]), Create(p[1]), FadeIn(p[2]), FadeIn(r), run_time=2.0)
        self.clear_scene()

    def contingency(self):
        head = heading(r"Why the rule computes $\Delta P$")
        lines = VGroup(
            label(r"the context, \ C, \ is a cue present on every trial", font_size=27, color=CONTEXT),
            MathTex(r"\text{trials with the cue: } \; \mathbb{E}[\Delta V_X] \propto P(\text{US}\mid X) - V_C - V_X = 0",
                    font_size=34),
            MathTex(r"\text{trials without it: } \; \mathbb{E}[\Delta V_C] \propto P(\text{US}\mid \text{no }X) - V_C = 0",
                    font_size=34),
            MathTex(r"\Rightarrow \; V_C = P(\text{US}\mid \text{no } X), \qquad V_X = P(\text{US}\mid X) - "
                    r"P(\text{US}\mid \text{no } X) = \Delta P", font_size=36, color=YOU),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0, 1.2, 0])
        keep_in_frame(lines)
        rows = rows_of([
            (r"at equilibrium the expected change is zero; \ solve the two equations", WHITE),
            (r"so Rescorla's random group learns nothing about the tone: \ the box itself predicts the shock", CONTEXT),
            (r"with equal learning rates for outcomes and their absence, \ the asymptote is exactly the contingency \ "
             r"(Chapman and Robbins, \ 1990)", CR),
        ], 12.4, 26, 0.28).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Now the puzzle of the two dogs. How can a rule built from pairings compute a contingency? "
            "<bookmark mark='a'/> The trick is the context: the box, the room, is a cue too, and it's present on every "
            "trial. <bookmark mark='b'/> On trials with the cue, the cue and the context share the prediction. At "
            "equilibrium the expected change is zero, so the two strengths add up to the probability of the outcome "
            "with the cue. <bookmark mark='c'/> On trials without the cue, the context alone predicts, so its strength "
            "settles at the probability of the outcome without the cue. <bookmark mark='d'/> Subtract, and the cue's "
            "strength is the difference: delta P. In the random group, the context predicts the shocks perfectly "
            "well by itself, and the tone, adding nothing, ends at zero. Gretchen Chapman and Steven Robbins pointed "
            "out in 1990 that, with equal learning rates for outcomes and their absence, the rule's asymptote is "
            "exactly the contingency, which ties the rat's learning to the gardener's judgment."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Write(lines[2]))
            vo.wait_until("d")
            self.play(Write(lines[3]), FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def rescorla(self):
        d = load("rescorla68")
        head = heading(r"Rescorla's ten groups, \ run on Psyche")
        groups = d["groups"]
        A = axes([-0.5, 9.5], [0, 0.55], x_length=8.8, y_length=3.6, xticks=[], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 ylabel=r"suppression ratio \ (0.5 = no fear)", center=[-1.6, 0.6, 0])
        ax = A.ax
        bars = VGroup()
        labs = VGroup()
        for k, ((p1, p0), sr) in enumerate(zip(groups, d["SR"])):
            col = INHIB if p1 == p0 else CR
            b = Rectangle(width=0.55, height=max(ax.c2p(0, sr)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                          fill_color=col, fill_opacity=0.85)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            bars.add(b)
            labs.add(label(rf"{p1:g}\\{p0:g}", font_size=17, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.12))
        cap = label(r"chance of shock: \ with the tone (top), \ without it (bottom)", font_size=19, color=GREY_A)
        cap.next_to(labs, DOWN, buff=0.15)
        rows = rows_of([
            (r"equal chances: \ ratios close to 0.5, \ little or no fear, \ as Rescorla found", INHIB),
            (r"fear grows with the contingency, \ within each chance with the tone", CR),
            (r"the rule reproduces the paper's three statements; \ the exact ratios are Psyche's", GREY_A),
        ], 3.8, 23, 0.34).move_to([4.9, 0.6, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ 8 rats a group, \ the paper's schedule; \ $\alpha = 0.12$, \ "
                         r"$\beta = 1$ and 0.4; \ the median shown")
        with self.voiceover(
            "And here is Rescorla's 1968 experiment, run on Psyche with the paper's schedule: eight simulated rats "
            "in each of the ten groups, the median shown, and a low bar meaning more fear. <bookmark mark='a'/> The "
            "four groups with equal chances, in red, stay close to point five: little or no fear, however many pairings "
            "they had. "
            "<bookmark mark='b'/> In the others, fear grows as the chance of shock without the tone falls, just as "
            "the paper reported. <bookmark mark='c'/> The exact numbers depend on choices Psyche makes, the learning "
            "rates and how fear turns into suppression. The pattern doesn't: it's the contingency, and the rule "
            "computes it from nothing but pairings and a context."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(labs), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(rows[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
