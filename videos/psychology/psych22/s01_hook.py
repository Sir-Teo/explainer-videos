from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

STATEMENTS = ("A robin is a bird.", "A penguin is a bird.", "A bat is a bird.", "An apple is a fruit.",
              "A tomato is a fruit.", "An olive is a fruit.", "A chair is furniture.", "A telephone is furniture.")


class Hook(VoiceoverScene):
    def construct(self):
        self.on_you()
        self.typicality()
        self.question()
        self.objectives()

    def on_you(self):
        stage = demo_stage(8.8, 4.0, center=[0, 0.7, 0])
        note = label(r"say ``true'' or ``false'' out loud, \ as fast as you can", font_size=26,
                     color=GREY_A).next_to(stage, DOWN, buff=0.3)
        with self.voiceover(
            "Let's start with an experiment on you. <bookmark mark='a'/> Some sentences will appear, one at a time. "
            "For each, say true or false out loud, as fast as you can, and notice which ones made you hesitate. "
            "Ready?"
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(note))
        spot = stage.box.get_center() + UP * 0.1
        for s_ in STATEMENTS:
            t_ = label(s_, font_size=56, color=WHITE).move_to(spot)
            self.add(t_)
            self.wait(1.6)
            self.remove(t_)
            self.wait(0.4)
        self.clear_scene()

    def typicality(self):
        head = heading(r"Some members are better than others")
        rows = rows_of([
            (r"a robin is a bird: \ instant; \ a penguin is a bird: \ true, \ but slower; \ a bat: \ false, \ but "
             r"you had to think", CAT_A),
            (r"Rosch, \ 1975: \ hundreds of students rated how good an example each member is: \ they agreed, \ and "
             r"robins beat penguins", WHITE),
            (r"typical members are verified faster, \ named first, \ learnt earlier, \ and used as reference points",
             MODEL),
            (r"McCloskey and Glucksberg, \ 1978: \ for borderline items, \ is a tomato a fruit, \ people disagree "
             r"with each other, \ and change their own minds when asked again", LOST),
        ], 7.0, 22, 0.36).move_to([2.6, -0.1, 0])
        ladder_words = ("robin", "sparrow", "canary", "eagle", "owl", "duck", "chicken", "ostrich", "penguin")
        ladder = VGroup(*[word_chip(w, CAT_A if k < 3 else (PROTO if k < 6 else LOST), 18, width=1.9)
                          for k, w in enumerate(ladder_words)]).arrange(DOWN, buff=0.08).move_to([-4.3, 0.45, 0])
        line = DashedLine([-5.5, ladder.get_bottom()[1] - 0.15, 0], [-3.1, ladder.get_bottom()[1] - 0.15, 0],
                          color=GREY_C)
        bat = word_chip("bat", GREY_B, 18, width=1.9).next_to(line, DOWN, buff=0.15)
        arrow = Arrow([-5.75, ladder.get_bottom()[1], 0], [-5.75, ladder.get_top()[1], 0], buff=0, color=GREY_B,
                      stroke_width=3)
        alab = label(r"better example", font_size=16, color=GREY_B).rotate(PI / 2).next_to(arrow, LEFT, buff=0.08)
        lnote = label(r"order after Rosch (1975), \ schematic", font_size=14, color=GREY_A).next_to(bat, DOWN,
                                                                                                    buff=0.12)
        tag = historical_tag(r"Rosch (1975); \ McCloskey \& Glucksberg (1978)")
        with self.voiceover(
            "Did you notice? <bookmark mark='a'/> A robin is a bird came at once. A penguin is a bird is just as true, "
            "but most people are a beat slower. And a bat is a bird is false, but it makes you think. "
            "<bookmark mark='b'/> In 1975 Eleanor Rosch asked students to rate how good an example of its category "
            "each member was. They agreed with each other closely: robins and sparrows are very good birds; "
            "penguins and ostriches are poor ones. <bookmark mark='c'/> And that rating predicts almost everything: "
            "typical members are verified faster, named first when you list a category, learnt earlier by "
            "children, and used as reference points. <bookmark mark='d'/> At the edges it gets stranger. Michael "
            "McCloskey and Sam Glucksberg asked people whether borderline things belonged, is a tomato a fruit, is "
            "a telephone furniture. People disagreed with each other, and when asked again some weeks later, a fair "
            "number changed their own minds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(alab), LaggedStart(*[FadeIn(c) for c in ladder], lag_ratio=0.15),
                      FadeIn(rows[1], shift=RIGHT * 0.15), run_time=2.5)
            self.play(Create(line), FadeIn(bat), FadeIn(lnote))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what do you know when you know what a bird is?")
        rows = rows_of([
            (r"a definition, \ as Aristotle thought? \ Why it fails", LOST),
            (r"an average, \ the prototype; \ or every bird you have met, \ the exemplars: \ two equations", PROTO),
            (r"six problems that tell the theories apart, \ and attention that learns", EXEMPLAR),
            (r"similarity as a space, \ and a law of generalization proposed for any mind", SPACE),
            (r"knowledge as a network, \ concepts as theories, \ learning from a few examples, \ and meaning from "
             r"the company words keep", MODEL),
        ], 11.8, 30, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "This part asks a question that sounds simple: what do you know when you know what a bird is? "
            "<bookmark mark='a'/> For two thousand years the answer was a definition. We'll see why it fails. "
            "<bookmark mark='b'/> Then the two great answers of the last fifty years: a concept is an average, a "
            "prototype, or a concept is the collection of every example you have met. Each becomes an equation. "
            "<bookmark mark='c'/> Six classic problems, with open data, will tell them apart, and show that attention "
            "itself has to be learnt. <bookmark mark='d'/> Then similarity as a space, and a law that Roger Shepard "
            "argued should hold for any mind anywhere, tested on open data from the 1950s. <bookmark mark='e'/> And "
            "finally knowledge as a network, concepts as theories, how a child learns a word from three examples, "
            "and what a computer learns about meaning from Jane Austen's novels."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 22", font_size=34, color=GREY_B), label(r"Concepts and Categories", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why concepts are not definitions: \ typicality, \ family resemblance, \ fuzzy boundaries",
            r"the prototype model and the generalized context model, \ derived; \ the 5-4 test between them",
            r"the six problems of Shepard, \ Hovland and Jenkins, \ and ALCOVE fitted to open data",
            r"multidimensional scaling of colours and Morse code, \ and Shepard's universal law, \ tested",
            r"Tversky's features, \ semantic networks and priming, \ concepts as theories",
            r"the number game by Bayes' rule; \ word vectors from Jane Austen",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 22 of Psychology, Built, the fifth part of Act Five, on thinking: concepts and categories. "
            "<bookmark mark='a'/> We'll see why concepts are not definitions. We'll derive the prototype model and "
            "the generalized context model, and the structure built to tell them apart. We'll fit a learning model "
            "to the six problems of Shepard, Hovland and Jenkins, from data that are open. We'll scale colours and "
            "Morse code into maps, and test Shepard's universal law on them. Then Tversky's features, semantic "
            "networks and priming, and concepts as theories. And we'll learn concepts from a few examples by Bayes' "
            "rule, and learn the meanings of words from their company."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=24.0)
        self.clear_scene()
