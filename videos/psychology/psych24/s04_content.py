from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Content(VoiceoverScene):
    def construct(self):
        self.card()
        self.schemas()
        self.derive()
        self.compare()

    def card(self):
        card = chapter_card(3, r"Why content helps", r"Are the ``wrong'' cards really wrong?",
                            lit={1985: r"Cheng \& Holyoak", 1989: r"Cosmides", 1994: r"Oaksford \& Chater"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter three. Why content helps."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def schemas(self):
        head = heading(r"Two explanations of the drinking-age effect")
        CARDS = [
            ([(r"takes the action", True), (r"does not", False), (r"meets the condition", False), (r"does not meet it",
                                                                                                   True)],
             r"turn: \ the action, \ and the unmet condition"),
            ([(r"eats cassava root", True), (r"eats molo nuts", False), (r"has a tattoo", False), (r"no tattoo", True)],
             r"turn: \ where a cheater could be"),
        ]
        items = [
            (r"pragmatic schemas", CONTENT, r"Cheng \& Holyoak, \ 1985",
             [r"people know how \emph{permissions} work: \ to do the action, \ meet the condition",
              r"a permission rule with arbitrary content helps, \ even without a story about cheaters"]),
            (r"cheater detection", INSIGHT, r"Cosmides, \ 1989",
             [r"evolution built a specialized ability to catch people who take a benefit without paying the cost",
              r"an unfamiliar rule \ (eat cassava root, \ have a face tattoo) \ is solved when it is a social "
              r"contract, \ not when it is a description"]),
        ]
        cols = VGroup()
        for k, (t, c, who, lines) in enumerate(items):
            body = VGroup(label(t, font_size=32, color=c), label(who, font_size=21, color=GREY_B),
                          rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 5.5, 24, 0.3)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = RoundedRectangle(corner_radius=0.15, width=6.2, height=3.2, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-3.35 + 6.7 * k, 1.05, 0])
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.3)
            faces, cap = CARDS[k]
            row = VGroup()
            for j, (f, turn) in enumerate(faces):
                r = RoundedRectangle(corner_radius=0.06, width=1.3, height=0.78, stroke_color=MODEL if turn else GREY_B,
                                     stroke_width=4 if turn else 2, fill_color="#20262F", fill_opacity=1)
                row.add(VGroup(r, wrapped_label(f, 1.15, 17, WHITE).move_to(r)))
            row.arrange(RIGHT, buff=0.15).next_to(box, DOWN, buff=0.3)
            cl = label(cap, font_size=18, color=MODEL).next_to(row, DOWN, buff=0.15)
            cols.add(VGroup(box, body, row, cl))
        note = rows_of([(r"both say people reason with what the content means, \ not with the form of the rule", MODEL)],
                       12.6, 26, 0.3).to_edge(DOWN, buff=0.85)
        tag = published_tag(r"Cheng \& Holyoak (1985); \ Cosmides (1989)")
        with self.voiceover(
            "Why does the drinking rule help so much? Two explanations led a long debate. <bookmark mark='a'/> "
            "Patricia Cheng and Keith Holyoak proposed pragmatic reasoning schemas. People know how permissions "
            "work: if you take the action, you must meet the condition. A permission rule helps even when its content "
            "is arbitrary. <bookmark mark='b'/> Leda Cosmides proposed something more specific: that evolution built "
            "a mechanism for catching cheaters, people who take a benefit without paying its cost. With an "
            "unfamiliar rule, if a man eats cassava root he must have a tattoo on his face, people chose well when "
            "the rule was framed as a social contract, and poorly when the same rule was a description. "
            "<bookmark mark='c'/> Both say people reason with what the content means, not with the form of the "
            "rule. A third answer asks whether the abstract task was ever being judged by the right standard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("ab", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derivation: \ optimal data selection")
        hyp = VGroup(
            MathTex(r"M_D:\ P(q \mid p) = 1", font_size=32, color=LOGIC),
            MathTex(r"M_I:\ P(q \mid p) = P(q)", font_size=32, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rare = MathTex(r"P(p) = a,\quad P(q) = b,\quad a \le b \ \text{small}", font_size=30, color=CONTENT)
        eig = MathTex(r"\mathbb{E}[I(x)] = H(M) - \sum_{y} P(y \mid x)\, H(M \mid x, y)", font_size=32, color=MODEL)
        left = VGroup(hyp, rare, eig).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-3.2, 0.5, 0])
        rows = rows_of([
            (r"Oaksford \& Chater, \ 1994: \ treat the task as testing a hypothesis about the world, \ not "
             r"checking a rule in logic", WHITE),
            (r"is $q$ dependent on $p$ \ ($M_D$), \ or independent of it \ ($M_I$)? \ start undecided", LOGIC),
            (r"rarity: \ vowels and even numbers, \ like most properties, \ are assumed to apply to few things", CONTENT),
            (r"turn the card that is expected to reduce your uncertainty about the hypotheses the most", MODEL),
        ], 5.8, 23, 0.36).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Oaksford \& Chater (1994), \ \emph{Psychological Review}")
        with self.voiceover(
            "In 1994 Mike Oaksford and Nick Chater argued that people treat the selection task not as a problem in "
            "logic but as a question about the world. <bookmark mark='a'/> Is Q dependent on P, so that every P is a "
            "Q? Or are they independent? A reasoner starts undecided between these two hypotheses. "
            "<bookmark mark='b'/> Add one assumption, rarity: most properties apply to only a few things, so P and Q "
            "are both uncommon. <bookmark mark='c'/> Then ask of each card how much turning it is expected to "
            "reduce uncertainty about the two hypotheses: the entropy before, minus the expected entropy after, "
            "averaged over what might be on the back. <bookmark mark='d'/> That is the expected information gain, "
            "and a rational tester turns the cards that carry the most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Write(hyp), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Write(rare), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Write(eig))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def compare(self):
        d = load("selection")
        head = heading(r"Information, \ and what people turn")
        cards = [r"$p$", r"$q$", r"not-$q$", r"not-$p$"]
        A = axes([0, 4], [0, 0.7], x_length=5.0, y_length=3.0, xticks=[], yticks=[0, 0.35, 0.7],
                 yfmt=lambda v: f"{v:.2f}", ylabel=r"expected gain, \ bits", center=[-3.6, 0.2, 0], font_size=16)
        B = axes([0, 4], [0, 1], x_length=5.0, y_length=3.0, xticks=[], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"people who turn it", center=[2.6, 0.2, 0],
                 font_size=16)
        b1 = VGroup(*[bars(A.ax, [k + 0.5], [v], MODEL, 0.6) for k, v in enumerate(d["eig"])])
        b2 = VGroup(*[bars(B.ax, [k + 0.5], [v], DATA, 0.6) for k, v in enumerate(d["people"])])
        n1 = VGroup(*[label(c, font_size=22).next_to(A.ax.c2p(k + 0.5, 0), DOWN, buff=0.12) for k, c in enumerate(cards)])
        n2 = VGroup(*[label(c, font_size=22).next_to(B.ax.c2p(k + 0.5, 0), DOWN, buff=0.12) for k, c in enumerate(cards)])
        p1 = label(r"Psyche: \ $a = 0.1$, \ $b = 0.2$", font_size=21, color=MODEL).next_to(A, UP, buff=0.15)
        p2 = label(rf"{d['people_studies']} studies, \ {d['people_n']} people \ (Oaksford \& Chater's Table 2)",
                   font_size=21, color=DATA).next_to(B, UP, buff=0.15)
        eig, ppl = d["eig"], d["people"]
        assert list(np.argsort(-eig)) == [0, 1, 2, 3] and list(np.argsort(-ppl)) == [0, 1, 2, 3]
        rows = rows_of([
            (r"the same order: \ $p$, \ then $q$, \ then not-$q$, \ then not-$p$", MODEL),
            (r"under rarity, \ the $q$ card is more informative than not-$q$: \ the ``error'' is good inquiry", CONTENT),
            (r"when $q$ is common, \ the $q$ card loses its value and not-$q$ overtakes it: \ some experiments "
             r"that manipulate this find it, \ others do not", GREY_A),
        ], 12.6, 24, 0.3).to_edge(DOWN, buff=0.6)
        tag = psyche_tag(r"\texttt{reason.selection\_information}")
        with self.voiceover(
            "Here is the calculation. <bookmark mark='a'/> With P and Q both rare, Psyche finds the P card most "
            "informative, then Q, then not-Q, and not-P almost worthless. <bookmark mark='b'/> On the right, how "
            "often people turn each card, from Oaksford and Chater's analysis of thirteen studies and eight hundred "
            "and forty-five people. <bookmark mark='c'/> The same order. On this view, turning the Q card isn't a "
            "failure of logic. If Q is rare, Q is where the information is. <bookmark mark='d'/> The model also "
            "predicts that when Q is common, the Q card loses its value and the not-Q card overtakes it, and some "
            "experiments that make Q common find just that, though not all. The abstract task may have been testing "
            "people against the wrong standard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(n1), FadeIn(p1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in b1], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(n2), FadeIn(p2), LaggedStart(*[FadeIn(b) for b in b2], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
