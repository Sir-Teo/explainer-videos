from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Probe(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"What a model represents", r"What can a probe find?", lit=(2023,), part=PART)
        with self.voiceover("Chapter fourteen. What a model represents."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.probes()
        self.result()
        self.lessons()

    def probes(self):
        head = label(r"Probing", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the method", r"train a simple classifier to read a property off a model's internal vectors", RULE_C),
            (r"if it succeeds", r"the information is there, \ in a usable form", OK),
            (r"what it does not show", r"that the model \textit{uses} it, \ or that it is about the world rather than "
                                       r"the text", BAD),
            (r"examples", r"Othello-GPT \ (Li et al., \ 2023): \ a board state recoverable from a model trained only on "
                          r"move sequences \ (\textit{AI, Built})", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "How could we tell what a model represents? <bookmark mark='a'/>One method is probing: train a simple "
            "classifier to read some property off the model's internal vectors. <bookmark mark='b'/>If the probe "
            "succeeds on words or inputs it was not trained on, the information is there, in a usable form. "
            "<bookmark mark='c'/>It does not show that the model uses it, or that it is about the world rather than "
            "about the text. <bookmark mark='d'/>The most striking example is Othello-GPT, from Kenneth Li and "
            "colleagues in 2023: a model trained only on sequences of legal moves, from whose activations a probe can "
            "recover the state of the board, as the AI series showed."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def result(self):
        d = load("probe")
        head = label(r"Two probes on the Reasoner's word vectors", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["category_right"] == 15 and d["category_n"] == 17 and d["fiction_right"] == 0 and d["fiction_n"] == 6
        hd = [r"\text{probe}", r"\text{held-out words right}", r"\text{chance}"]
        cells = [[label(r"kind: \ animal, \ royal, \ city, \ food", font_size=20, color=WORD),
                  MathTex(f"{d['category_right']} / {d['category_n']}", font_size=26, color=OK),
                  MathTex(r"\approx \tfrac14", font_size=24)],
                 [label(r"fictional or real: \ Holmes, \ Watson, \ Frodo \ / \ Darwin, \ Newton, \ Dickens", font_size=20,
                        color=TRUTH), MathTex(f"{d['fiction_right']} / {d['fiction_n']}", font_size=26, color=BAD),
                  MathTex(r"\tfrac12", font_size=24)]]
        grid = ValueGrid(hd, cells, col_w=[6.4, 3.2, 1.6], cell_h=0.6, font_size=21).move_to([0, 0.8, 0])
        rows = stack([(r"each word held out in turn; \ nearest class average of the others", GREY_A),
                      (r"kind is recoverable from distribution", OK),
                      (r"fictionality is not: \ in this text, \ fictional and real people appear in the same kinds of "
                       r"sentences", BAD),
                      (r"the probe is wrong every time: \ each name sits next to the people it shares sentences with", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.24).move_to([0, -1.7, 0])
        with self.voiceover(
            "The Reasoner probes its own small word vectors from chapter twelve. <bookmark mark='a'/>The first probe "
            "asks each word's kind: animal, royalty, city, or food. Each word is held out in turn and assigned to the "
            "nearest average of the others. Fifteen of seventeen come out right, against about one in four by chance. "
            "<bookmark mark='b'/>The second asks whether a person is fictional: Holmes, Watson and Frodo against "
            "Darwin, Newton and Dickens. It gets none of the six right. <bookmark mark='c'/>In this corpus fictional "
            "and real people appear in the same kinds of sentences: they live in London, write books, meet kings. "
            "Nothing in the distribution marks the difference, and each name sits next to the real or fictional "
            "people it shares sentences with. <bookmark mark='d'/>So a model can represent a great deal from text, and "
            "still be blind to facts about reference that the text does not encode."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]], FadeIn(rows[0]),
                      FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lessons(self):
        head = label(r"What the probes teach", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"a lot from form", r"kinds, \ relations, \ even a game board: \ text encodes much of the world's "
                                 r"structure", OK),
            (r"what is missing", r"whatever the text does not mark: \ here, \ fiction against fact", BAD),
            (r"real corpora", r"do mark it, \ often: \ `in the novel', \ `the detective', \ `born in 1809'", WORD),
            (r"the open question", r"whether a big enough model of text has everything meaning requires, \ or only "
                                   r"everything form can carry", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "What do the probes teach? <bookmark mark='a'/>That a great deal can be learned from form alone: kinds, "
            "relations, even, in Othello-GPT, the state of a board. Text encodes much of the world's structure. "
            "<bookmark mark='b'/>And that whatever the text does not mark is missing: here, fiction against fact. "
            "<bookmark mark='c'/>Real corpora do often mark it, with in the novel, the detective, born in 1809, which "
            "is why large models usually know that Holmes is fictional. <bookmark mark='d'/>The open question is "
            "whether a big enough model of text has everything meaning requires, or only everything that form can "
            "carry."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
