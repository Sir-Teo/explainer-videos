from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.everywhere()
        self.archipelago()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"I believe that there are possible worlds other than the one we happen to inhabit.",
                       r"David Lewis", r"\textit{Counterfactuals} \ (1973)", width=8.8, font_size=26).next_to(
            t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 21 asked what makes a thing the same thing over time. This part asks about all the ways things "
            "could have been. <bookmark mark='a'/>David Lewis opened a chapter of his book on counterfactuals with a "
            "sentence that made his colleagues stare: I believe that there are possible worlds other than the one we "
            "happen to inhabit. <bookmark mark='b'/>He meant it literally. By the end of this part we will see why a "
            "careful philosopher could believe it, what the alternatives cost, and why engineers now compute with "
            "possible worlds every day."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def everywhere(self):
        head = label(r"Modal talk is everywhere", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"could", r"the bridge could have collapsed; \ you could have been born a day later", WORLD),
            (r"must", r"two plus two must be four; \ a bachelor must be unmarried", ABS),
            (r"would", r"if I had left earlier, \ I would have caught the train", CPT),
            (r"-able, -ible", r"this glass is fragile; \ sugar is soluble; \ the code is reachable", NAME),
            (r"in machines", r"a model trained on other data would have decided otherwise", DESC),
        ]
        g = rows_table(rows, top=1.9, gap=0.5, width=8.8, x_text=-2.4, label_size=23, text_size=23)
        note = label(r"each is about what is not actual: \ what are such sentences made true by?", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "We talk about what is not actual all the time. <bookmark mark='a'/>The bridge could have collapsed. You "
            "could have been born a day later. <bookmark mark='b'/>Two plus two must be four; a bachelor must be "
            "unmarried. <bookmark mark='c'/>If I had left earlier, I would have caught the train. "
            "<bookmark mark='d'/>Even the little suffixes are modal: a fragile glass is one that would break if "
            "struck; soluble sugar would dissolve. <bookmark mark='e'/>And machine learning is full of it: a model "
            "trained on other data would have decided otherwise. <bookmark mark='f'/>Every one of these sentences is "
            "about what is not actual. Some of them are plainly true. So what makes them true?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(note))
        self.clear_scene()

    def archipelago(self):
        head = label(r"Worlds: \ the semantics, \ and the metaphysics", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.3)
        spots = [(-4.6, 1.2), (-1.6, 1.9), (1.6, 1.5), (4.6, 1.9), (-3.2, -0.7), (0.0, -0.3), (3.2, -0.6)]
        isl = VGroup(*[island(p, w=2.0, h=1.0, seed=i, color=NAME if i == 5 else WORLD,
                              name=r"actual" if i == 5 else None) for i, p in enumerate(spots)])
        fl = [MathTex(r"\Box p \text{ is true} \iff p \text{ is true at every world}", font_size=32, color=ABS),
              MathTex(r"\Diamond p \text{ is true} \iff p \text{ is true at some world}", font_size=32, color=ABS)]
        fg = VGroup(*fl).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.9)
        q = label(r"but what \textit{is} a world? \ \ a concrete universe, \ a book, \ a state of affairs, "
                  r"\ a useful fiction?", font_size=21, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Part 4 gave the answer that logic needs. <bookmark mark='a'/>Picture a space of worlds, each a complete "
            "way things might have been, with one of them actual. <bookmark mark='b'/>Then necessarily p is true "
            "when p is true at every world, and possibly p when p is true at some world. Leibniz had the picture; "
            "Kripke and others turned it into a semantics in the late nineteen fifties, and it made modal logic "
            "precise. <bookmark mark='c'/>But a semantics is not yet a metaphysics. What is a possible world? A "
            "universe as concrete as ours? A book that describes one? A way things might have been, existing but "
            "never instantiated? Or a useful fiction? This part takes the question seriously."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[DrawBorderThenFill(i) for i in isl], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(fg[0]))
            self.play(Write(fg[1]))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()

    def questions(self):
        head = label(r"Five questions for this part", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([(r"1. \ When I say Humphrey might have won, \ who is it, \ in the other world, \ who wins?",
                       WORLD),
                      (r"2. \ How can it be necessary that water is H$_2$O, \ when we had to find it out?", NAME),
                      (r"3. \ Are worlds real, \ or representations? \ And what does each answer cost?", ABS),
                      (r"4. \ Does being conceivable make something possible?", DESC),
                      (r"5. \ Is necessity the deepest notion, \ or is essence deeper still?", CPT)],
                     font_size=23, aligned_edge=LEFT, width=12.0, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Five questions will run through the part. <bookmark mark='a'/>When I say that Hubert Humphrey, who lost "
            "the 1968 presidential election, might have won, who is it, at the other world, that wins? Humphrey "
            "himself, or someone like him? <bookmark mark='b'/>How can it be necessary that water is H two O, when "
            "chemists had to discover it? <bookmark mark='c'/>Are worlds real things, or representations, and what "
            "does each answer cost? <bookmark mark='d'/>Does being conceivable make something possible? That "
            "question carries the weight of famous arguments about the mind. <bookmark mark='e'/>And is necessity "
            "the deepest notion here, or is there something deeper, essence, which explains it?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"de re and de dicto; \ Quine's mathematical cyclist, \ on a model",
            r"Kripke: \ rigid names, \ and the necessary \textit{a posteriori}",
            r"Lewis's modal realism, \ and counterpart theory, \ translated and checked",
            r"ersatz worlds and alien properties; \ necessitism and the Barcan formula",
            r"conceivability; \ two-dimensional matrices, \ computed \ (the Wall)",
            r"Kripke's puzzle about belief \ (a Price List); \ Fine on essence",
            r"impossible worlds and counterpossibles; \ dispositions, \ finks and masks",
            r"possible worlds at work: \ counterfactual explanations, \ probabilistic programs",
        ], font_size=23)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>The two places a modal word can sit, and Quine's puzzle about them. "
            "<bookmark mark='b'/>Kripke's rigid names, and truths that are necessary but known only by experience. "
            "<bookmark mark='c'/>Lewis's modal realism, and his counterpart theory, which the Reasoner translates and "
            "checks on thousands of models. <bookmark mark='d'/>The alternatives: worlds as representations, and the "
            "view that everything exists necessarily. <bookmark mark='e'/>Conceivability, and the two-dimensional "
            "semantics built to tame it, computed cell by cell: this part's brick in the Wall. <bookmark mark='f'/>"
            "Kripke's puzzle about belief, on a Price List, and essence prised apart from necessity. "
            "<bookmark mark='g'/>Impossible worlds, and dispositions. <bookmark mark='h'/>And the engineering: "
            "explanations that search for the closest world where a decision flips, and programs that put "
            "probabilities on worlds."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
