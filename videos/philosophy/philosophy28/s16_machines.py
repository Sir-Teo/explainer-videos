from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Pragmatics in machines", r"Can a machine read what is meant?", lit=(2023,), part=PART)
        with self.voiceover("Chapter fifteen. Pragmatics in machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tests()
        self.captioner()
        self.assistants()

    def tests(self):
        head = label(r"Testing machines on implicature", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ex = stack([(r"`Are you coming to the party tonight?'", WORD), (r"`I have to work.'", USE),
                    (r"meant: \ no", GOAL)], font_size=24, aligned_edge=LEFT, buff=0.2).move_to([-3.4, 1.2, 0])
        rows = [
            (r"Ruis et al. \ (2023)", r"implicatures like this one: \ many models near chance; \ instruction-tuned "
                                      r"models much better, \ some approaching people", HIST),
            (r"Hu et al. \ (2023)", r"seven pragmatic phenomena, \ models against people: \ the largest models close on "
                                    r"many, \ weakest where social expectations matter", HIST),
            (r"the moral", r"pragmatic competence is not automatic from scale; \ how a model is trained to converse "
                           r"matters", GOAL),
        ]
        g = rows_table(rows, top=-0.1, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Language models now take part in conversations, so they can be tested on implicature. "
            "<bookmark mark='a'/>Are you coming to the party tonight? I have to work. The answer meant is no, though "
            "no one said it. <bookmark mark='b'/>Laura Ruis and colleagues tested models on thousands of exchanges like "
            "this one in 2023. Many models were close to chance; models fine-tuned on instructions and dialogue did "
            "much better, some approaching people. <bookmark mark='c'/>Jennifer Hu and colleagues compared models "
            "with people on seven pragmatic phenomena the same year. The largest models came close to people on "
            "many, and were weakest where social expectations matter. <bookmark mark='d'/>The moral: pragmatic "
            "competence does not come automatically with scale; how a model is trained to converse matters."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            for mk, r in zip("bcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def captioner(self):
        d = load("reference")
        head = label(r"A pragmatic captioner", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        objs = VGroup(VGroup(Square(0.7, color=WORD, fill_opacity=0.8)), VGroup(Circle(0.38, color=WORD, fill_opacity=0.8)),
                      VGroup(Square(0.7, color=OK, fill_opacity=0.8))).arrange(RIGHT, buff=0.8).move_to([-3.4, 1.4, 0])
        target = SurroundingRectangle(objs[2], color=TRUTH, buff=0.15)
        ttag = label(r"describe this one", font_size=18, color=TRUTH).next_to(target, DOWN, buff=0.12)
        S1 = d["S1"]
        words = d["words"]
        lit = [0.5 if d["meaning"][j][2] else 0.0 for j in range(len(words))]
        hd = [r"\text{word}", r"\text{literal speaker}", r"\text{pragmatic speaker}"]
        cells = [[label(f"`{w}'", font_size=21, color=WORD), MathTex(f"{lit[j]:.2f}", font_size=24),
                  MathTex(f"{S1[2][j]:.2f}", font_size=24, color=USE)] for j, w in enumerate(words)]
        grid = ValueGrid(hd, cells, col_w=[1.8, 2.8, 3.0], cell_h=0.48, font_size=20).move_to([2.8, 0.2, 0])
        assert S1[2][1] > S1[2][2] and abs(S1[2][1] - 0.6667) < 1e-3
        rows = stack([(r"a literal speaker: \ any true word will do: \ `green' or `square', \ evenly", WHITE),
                      (r"the pragmatic speaker prefers the word that picks it out: \ `green', \ 2 to 1", USE),
                      (r"Andreas and Klein \ (2016); \ Cohn-Gordon et al. \ (2018): \ RSA reasoning on top of neural "
                       r"captioners makes captions more discriminating", HIST)], font_size=20, aligned_edge=LEFT,
                     width=12.0, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Rational Speech Acts model has also been put to work. <bookmark mark='a'/>Take the three objects of "
            "chapter ten, and ask a system to describe the green square. <bookmark mark='b'/>A literal speaker says "
            "any true word: green or square, evenly. <bookmark mark='c'/>The pragmatic speaker of chapter ten prefers "
            "green, two to one, because square would leave the listener unsure. <bookmark mark='d'/>Jacob Andreas and "
            "Dan Klein in 2016, and Reuben Cohn-Gordon and colleagues in 2018, put this kind of reasoning on top of "
            "neural captioning systems, and their captions became more discriminating: better at picking out one "
            "image among similar ones."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(objs), Create(target), FadeIn(ttag))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[r][0]) for r in range(4)],
                      *[FadeIn(grid.cell[r][1]) for r in range(4)], FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][2]) for r in range(4)], FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def assistants(self):
        head = label(r"Assistants must read intentions", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"indirect requests", r"`can you open the file?' \ wants it opened, \ not a yes", WORD),
            (r"Quantity", r"answers as informative as the user needs, \ and no more", RULE_C),
            (r"Quality", r"say only what there is evidence for: \ the maxim against making things up", OK),
            (r"what is meant", r"a request's purpose, \ not just its words: \ the problem of Part 42, \ "
                               r"\textit{Aligning Reasoners}", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "For an assistant built on a language model, Grice's maxims are design requirements. "
            "<bookmark mark='a'/>Can you open the file wants the file opened, not the answer yes. "
            "<bookmark mark='b'/>Quantity: answers as informative as the user needs, and no more. "
            "<bookmark mark='c'/>Quality: say only what there is evidence for, the maxim a model violates when it "
            "makes things up. <bookmark mark='d'/>And above all, what is meant: a request's purpose, not just its "
            "words. Working out what people want from what they say is the problem of Part 42, aligning reasoners."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
