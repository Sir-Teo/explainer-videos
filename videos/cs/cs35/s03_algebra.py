from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, rel_table)


def T(d, color=DATA, font=17):
    return rel_table(d["cols"], d["rows"], font=font, color=color)


class Algebra(VoiceoverScene):
    def construct(self):
        self.card()
        self.operators()
        self.compose()

    def card(self):
        card = chapter_card(2, r"Relational algebra", r"What can you compute with tables alone?", lit=(1970, 1974),
                            extra=((1974, r"Chamberlin and Boyce: \ SEQUEL"),), part=PART)
        with self.voiceover("Chapter two. Relational algebra."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def operators(self):
        a = load("algebra")
        head = label(r"Six operators, \ each a table in and a table out", font_size=34).to_edge(UP, buff=0.3)
        books = T(a["books"]).move_to([-3.6, 1.2, 0])
        bl = label(r"\texttt{books}", font_size=18, color=DATA).next_to(books, UP, buff=0.1)
        authors = T(a["authors"], color=HEAD).move_to([3.2, 1.5, 0])
        al = label(r"\texttt{authors}", font_size=18, color=HEAD).next_to(authors, UP, buff=0.1)
        ops = [
            ("select", r"$\sigma_{\text{year} < 1900}(\text{books})$: \ the rows that qualify", YES),
            ("project", r"$\pi_{\text{author}}(\text{books})$: \ some columns, \ duplicates gone", LAM),
            ("join", r"$\text{books} \bowtie \text{authors}$: \ pairs that agree on \texttt{author}", HEAD),
            ("union", r"$\cup$, \ $-$: \ set union and difference of like tables; \ $\rho$ renames", KERN),
        ]
        res = {}
        res["select"] = T(a["select"], color=YES)
        res["project"] = T(a["project"], color=LAM)
        res["join"] = T(a["join"], color=HEAD, font=15)
        res["union"] = T(a["minus"], color=KERN)
        caps = VGroup(*[label(t, font_size=20, color=c) for _, t, c in ops])
        for k, (name, _, _) in enumerate(ops):
            res[name].move_to([0, -1.6, 0])
            caps[k].next_to(res[name], UP, buff=0.18)
        with self.voiceover(
            "Codd gave his model an algebra: operators that each take tables and return a table, so they can be "
            "combined freely. Here are two small tables, books and authors. <bookmark mark='a'/> Selection keeps the "
            "rows that satisfy a condition: the books published before 1900. <bookmark mark='b'/> Projection keeps "
            "some columns, and drops the duplicate rows that may result: the authors. <bookmark mark='c'/> Join pairs "
            "every book with every author it agrees with on the shared column: now each book carries its author's year "
            "of birth. <bookmark mark='d'/> And the set operations, union and difference, work on tables of the same "
            "shape, here the books not in a second list, with renaming to make shapes match. That is all. Every "
            "question of the kind SQL asks is a composition of these."
        ) as vo:
            self.play(FadeIn(head), FadeIn(books), FadeIn(bl), FadeIn(authors), FadeIn(al))
            prev = None
            for mk, (name, _, _), cap in zip("abcd", ops, caps):
                vo.wait_until(mk)
                anims = [FadeIn(res[name]), FadeIn(cap)]
                if prev:
                    anims += [FadeOut(res[prev[0]]), FadeOut(prev[1])]
                self.play(*anims)
                prev = (name, cap)
        self.wait(0.3)
        self.clear_scene()

    def compose(self):
        a = load("algebra")
        head = label(r"Composing them: \ a query is a tree", font_size=36).to_edge(UP, buff=0.3)
        expr = MathTex(r"\pi_{\text{book}}\big(\sigma_{\text{year} - \text{born} < 45}(\text{books} \bowtie "
                       r"\text{authors})\big)", font_size=34, color=WHITE).next_to(head, DOWN, buff=0.4)
        leafb = label(r"books", font_size=28, color=DATA)
        leafa = label(r"authors", font_size=28, color=HEAD)
        jn = MathTex(r"\bowtie", font_size=52, color=HEAD)
        sg = MathTex(r"\sigma_{\text{year} - \text{born} < 45}", font_size=44, color=YES)
        pj = MathTex(r"\pi_{\text{book}}", font_size=44, color=LAM)
        pj.move_to([-3.5, 0.9, 0])
        sg.move_to([-3.5, 0.0, 0])
        jn.move_to([-3.5, -0.9, 0])
        leafb.move_to([-4.6, -1.9, 0])
        leafa.move_to([-2.4, -1.9, 0])
        edges = VGroup(Line(pj.get_bottom(), sg.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5),
                       Line(sg.get_bottom(), jn.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5),
                       Line(jn.get_bottom(), leafb.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5),
                       Line(jn.get_bottom(), leafa.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5))
        tree = VGroup(pj, sg, jn, leafb, leafa, edges)
        sql = VGroup(*[mono(t, 18, YES) for t in ("SELECT book", "FROM books JOIN authors", "  ON books.author = authors.author",
                                                  "WHERE year - born < 45")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.06)
        sql.move_to([2.6, 0.6, 0])
        ans = T(a["young"], color=LAM).next_to(sql, DOWN, buff=0.5)
        lines = VGroup(
            label(r"SQL is a friendlier way to write such a tree; \ the database turns one into the other",
                  font_size=20, color=WHITE),
            label(r"Codd's theorem \ (1972): \ the algebra and the relational calculus, \ a logic of tuples, \ can "
                  r"express the same queries", font_size=20, color=HEAD),
            label(r"trees can be rewritten: \ push $\sigma$ below $\bowtie$, \ reorder joins: \ the same answer, \ "
                  r"different costs \ (chapter 6)", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Combining operators gives a tree. <bookmark mark='a'/> Which books did their authors publish before the "
            "age of forty-five? Join books to authors, select the rows where the year minus the birth year is under "
            "forty-five, "
            "and project the titles. <bookmark mark='b'/> In SQL it reads almost like English, and the database "
            "translates it back into a tree like this one. <bookmark mark='c'/> Emma, Persuasion and Ulysses qualify; "
            "Dracula does not: Stoker was fifty. <bookmark mark='d'/> Codd also showed that the algebra is exactly as expressive as a "
            "logic of tuples, the relational calculus, which is closer to how SQL states things. <bookmark mark='e'/> "
            "And because operators obey laws, the tree can be rewritten, selections pushed down, joins reordered, "
            "without changing the answer. Choosing among those rewritings is the optimizer's job."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(expr), FadeIn(tree))
            vo.wait_until("b")
            self.play(FadeIn(sql), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(ans))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()


_ = (NO,)
