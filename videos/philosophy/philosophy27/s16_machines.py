from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


def mark(v, size=24):
    return MathTex(r"\checkmark" if v else r"\times", font_size=size, color=OK if v else BAD)


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Meaning in machines", r"Do language models know what words mean?",
                            lit=(2018, 2019, 2023), part=PART)
        with self.voiceover("Chapter fifteen. Meaning in machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sql()
        self.benchmarks()
        self.nli()
        self.reversal()

    def sql(self):
        d = load("sql")
        head = label(r"Logical forms, \ compiled to SQL", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["all_agree"] and len(d["rows"]) == 7
        r = next(x for x in d["rows"] if x["sentence"] == "every student smokes")
        lf = MathTex(r"\forall x\,[\textsc{student}(x) \rightarrow \textsc{smoke}(x)]", font_size=32,
                     color=SENSE).move_to([-3.0, 2.0, 0])
        code = Paragraph(*[ln for ln in self.wrap(r["query"], 46)], font="Monospace", font_size=15,
                         color=REF, line_spacing=0.6).move_to([-3.0, 0.2, 0])
        arrow = Arrow(lf.get_bottom(), code.get_top(), buff=0.15, color=GREY_B)
        hd = [r"\text{sentence}", r"\text{model checker}", r"\text{sqlite}"]
        cells = [[label(x["sentence"].replace(" (QR)", "").replace(" (surface)", ": surface").replace(
            " (inverse)", ": inverse"), font_size=17, color=NAME), tv(x["model"], 20), tv(x["sql"], 20)]
            for x in d["rows"]]
        grid = ValueGrid(hd, cells, col_w=[3.6, 1.5, 1.1], cell_h=0.38, font_size=17).move_to([3.8, -0.3, 0])
        foot = label(r"semantic parsing: \ from sentences to executable meanings", font_size=21, color=GOAL).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Formal semantics is not only philosophy. It is the theory behind every system that turns language into "
            "something a computer can execute. <bookmark mark='a'/>The Reasoner takes the logical forms its parser "
            "produced in chapter ten and compiles them into the database language SQL. Every student smokes "
            "becomes a query: there is no row in the entity table that is a student and not a smoker. "
            "<bookmark mark='b'/>It loads the model into a sqlite database, runs all seven queries, and compares "
            "the answers with its own model checker. They agree on every sentence, including both readings of the "
            "scope ambiguity. <bookmark mark='c'/>Turning sentences into executable meanings like this is called "
            "semantic parsing, and it is what a question-answering system over a database has to do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lf), GrowArrow(arrow), FadeIn(code))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for i in range(len(cells)):
                self.play(*[FadeIn(x) for x in grid.cell[i]], run_time=0.3)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    @staticmethod
    def wrap(s, width):
        words, lines, cur = s.split(" "), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > width and cur:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            lines.append(cur)
        return lines

    def benchmarks(self):
        head = label(r"How machines are tested on meaning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"FraCaS \ (1996)", r"a suite of inference problems built by semanticists: \ quantifiers, \ plurals, \ "
                                 r"anaphora, \ attitudes", HIST),
            (r"Spider \ (2018)", r"Yu et al.: \ questions paired with SQL over two hundred databases", REF),
            (r"SCAN; \ COGS", r"Lake and Baroni \ (2018); \ Kim and Linzen \ (2020): \ can a network compose meanings "
                              r"it was never shown together?", SENSE),
            (r"MED \ (2019)", r"Yanaka et al.: \ monotonicity inferences, \ upward and downward, \ the patterns of "
                              r"chapter 11", NAME),
            (r"the pattern", r"large models do well on common cases, \ and less well on systematic ones: \ scope, \ "
                             r"negation, \ downward contexts", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "How do we test whether a machine handles meaning? <bookmark mark='a'/>FraCaS, a suite of inference "
            "problems written by semanticists in 1996, covers quantifiers, plurals, anaphora and attitude reports. "
            "<bookmark mark='b'/>Spider, from Tao Yu and colleagues in 2018, pairs questions with SQL queries over "
            "two hundred databases. <bookmark mark='c'/>SCAN, from Brenden Lake and Marco Baroni, and COGS, from "
            "Najoung Kim and Tal Linzen, test compositional generalization: can a network interpret a combination of "
            "parts it never saw combined? <bookmark mark='d'/>And MED, from Hitomi Yanaka and colleagues in 2019, "
            "tests exactly the monotonicity inferences of chapter eleven. <bookmark mark='e'/>Across these "
            "benchmarks the broad pattern has been that neural models do well on common cases and less well on "
            "systematic ones: scope, negation, and downward-entailing contexts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def nli(self):
        d = load("nli")
        head = label(r"A test suite whose answers are proved", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        edits = ["narrow the noun", "widen the noun", "narrow the verb", "widen the verb"]
        ex = {"narrow the noun": r"dogs $\to$ small dogs", "widen the noun": r"small dogs $\to$ dogs",
              "narrow the verb": r"makes noise $\to$ barks", "widen the verb": r"barks $\to$ makes noise"}
        hd = [r"\text{premise}"] + [r"\text{" + e + "}" for e in edits]
        rows_d = d["rows"]
        cells = [[label(rf"`{q} \dots'", font_size=20, color=SENSE)] + [mark(rows_d[q][e]) for e in edits]
                 for q in ("every", "some", "no", "most")]
        grid = ValueGrid(hd, cells, col_w=[2.2, 2.6, 2.6, 2.6, 2.6], cell_h=0.48, font_size=19).move_to([0, 0.6, 0])
        exl = VGroup(*[label(ex[e], font_size=16, color=GREY_A) for e in edits])
        for e, lab in zip(range(len(edits)), exl):
            lab.next_to(grid.head[e + 1], UP, buff=0.12)
        assert rows_d["every"] == {"narrow the noun": True, "widen the noun": False, "narrow the verb": False,
                                   "widen the verb": True}
        assert rows_d["most"]["widen the verb"] and not rows_d["most"]["narrow the noun"]
        rows = stack([(r"each label: \ does the edited sentence follow? \ checked on every choice of sets over 4 "
                       r"elements", OK),
                      (r"no annotator disagreement, \ no label noise: \ the gold standard is a theorem", GOAL),
                      (r"a model's answers can be scored against the logic, \ case by case", NAME)], font_size=21,
                     aligned_edge=LEFT, width=12.0, buff=0.24).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner can build such a test itself. <bookmark mark='a'/>Take a premise like every dog barks, and "
            "edit it: narrow the noun to small dogs, widen it, narrow the verb to something stronger, or widen it to "
            "makes noise. <bookmark mark='b'/>For each of four determiners and each edit, it decides whether the "
            "edited sentence follows, by checking every choice of sets over a four-element universe. "
            "<bookmark mark='c'/>The answers are the monotonicity profiles: every licenses narrowing the noun and "
            "widening the verb; some, widening both; no, narrowing both; most, only widening the verb. "
            "<bookmark mark='d'/>Every label in this suite is a theorem. There is no annotator disagreement and no "
            "label noise. <bookmark mark='e'/>A language model's answers can be scored against the logic, case by "
            "case."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(exl))
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[i][0]) for i in range(len(cells))], FadeIn(rows[0]))
            vo.wait_until("c")
            for i in range(len(cells)):
                self.play(*[FadeIn(x) for x in grid.cell[i][1:]], run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reversal(self):
        head = label(r"Identity, \ in silicon", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the reversal curse", r"Berglund et al. \ (2023): \ models trained on `A is B' often fail to infer "
                                    r"`B is A'", BAD),
            (r"an example", r"`Who is Tom Cruise's mother?' \ answered correctly far more often than \ `Who is Mary "
                            r"Lee Pfeiffer's son?'", SPEAK),
            (r"Frege's point", r"`$a = b$' carries information that `$a = a$' does not; \ the direction of learning "
                               r"shows it", SENSE),
            (r"do their words refer?", r"Mandelkern and Linzen: \ perhaps, \ by the externalist route of chapters 5 "
                                       r"and 6: \ through a history of use by people", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "One recent finding goes back to the first page of this part. <bookmark mark='a'/>In 2023 Lukas Berglund "
            "and colleagues reported what they called the reversal curse: language models trained on statements of "
            "the form A is B often fail to answer questions that need B is A. <bookmark mark='b'/>In one test, a "
            "leading model answered who is Tom Cruise's mother correctly about four times in five, and who is Mary "
            "Lee Pfeiffer's son only about a third of the time. <bookmark mark='c'/>Frege's identity statements are "
            "symmetric in logic. But a equals b carries information that a equals a does not, and a learner that "
            "stores it in one direction shows it. <bookmark mark='d'/>Do such models refer to anything at all? "
            "Matthew Mandelkern and Tal Linzen have argued that they may, by the externalist route of chapters five "
            "and six: their words come to them through a long history of use by people who did."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
