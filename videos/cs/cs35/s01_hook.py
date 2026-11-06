from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, LAM, NO, PART, YES, box, code, grid_table, load, mono, num)


class Hook(VoiceoverScene):
    def construct(self):
        self.two_ways()
        self.how()
        self.plan()

    def two_ways(self):
        j = load("job")
        head = label(r"The Job, \ twice", font_size=36).to_edge(UP, buff=0.3)
        left = code([
            "words = tokenize(text)              # Part 12",
            "table = HashTable(65536)            # Part 17",
            "for w in words:",
            "    table[w] = table.get(w, 0) + 1",
            "pairs = list(table.items())",
            "pairs.sort(key=count, reverse=True) # Part 16",
            "print(pairs[:20])",
        ], size=17)
        lt = label(r"how: \ every step chosen by hand", font_size=20, color=NO).next_to(left, UP, buff=0.15)
        lg = VGroup(lt, left).move_to([-3.4, 1.0, 0])
        sql = mono("SELECT word, COUNT(*) FROM words", 19, YES)
        sql2 = mono("GROUP BY word ORDER BY 2 DESC LIMIT 20", 19, YES)
        rt = label(r"what: \ one line of SQL", font_size=20, color=YES)
        rg = VGroup(rt, VGroup(sql, sql2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, buff=0.2)
        rg.move_to([3.3, 1.5, 0])
        top = j["top"][:6]
        tab = grid_table([r"word", r"count"], [[w, num(c)] for w, c in top], widths=[1.6, 1.8], row_h=0.36,
                         font_size=18, mono_cols=(0,))
        tab.next_to(rg, DOWN, buff=0.4)
        lines = VGroup(
            label(rf"over the thirty novels: \ {num(j['rows'])} rows, \ the same twenty answers as Part 17's "
                  r"program", font_size=21, color=WHITE),
            label(rf"sqlite3 on this machine: \ {j['sqlite_seconds']:.2f} s, \ with no instructions about how",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "For thirty parts the Job has been a program: tokenize the novels, count the words in a hash table, "
            "sort, print the top twenty. <bookmark mark='a'/> Every step of it chosen by hand, with the data "
            "structure, the hashing and the sort each a part of this course. <bookmark mark='b'/> Here is the same "
            "job as one line of SQL. It says what we want: for each word, how many times it occurs, the twenty most "
            "common. It says nothing about how. <bookmark mark='c'/> Loaded into a database as four point six "
            "million rows, one per word, it gives exactly the same twenty answers, <bookmark mark='d'/> and sqlite, "
            "on this machine, answers in about two seconds, with no instructions at all about hash tables or sorts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lg))
            vo.wait_until("b")
            self.play(FadeIn(rg))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def how(self):
        j = load("job")
        head = label(r"So who decides how?", font_size=36).to_edge(UP, buff=0.3)
        stages = VGroup(*[box(2.3, 0.8, t, c, font_size=22) for t, c in (
            (r"\text{SQL}", YES), (r"\text{parser}", GREY_B), (r"\text{optimizer}", HEAD), (r"\text{executor}", DATA),
            (r"\text{answer}", YES))]).arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.06, color=GREY_B,
                                stroke_width=2) for i in range(4)])
        ex = VGroup(*[mono(ln, 16, CODE) for ln in j["explain"].splitlines()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08)
        el = label(r"our database's plan for the Job \ (EXPLAIN)", font_size=19, color=HEAD)
        eg = VGroup(el, ex).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(stages, DOWN, buff=0.6)
        if eg.width > 12.5:
            eg.width = 12.5
        lines = VGroup(
            label(r"the \textbf{optimizer} chooses among many correct plans by estimating what each costs",
                  font_size=21, color=HEAD),
            label(r"and the \textbf{transaction manager} lets thousands of users share the data as if each were "
                  r"alone, \ through crashes", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So who decides how? <bookmark mark='a'/> A database turns the query into a plan in stages. The parser "
            "reads the SQL; the optimizer considers many plans that would all give the right answer, and estimates "
            "what each would cost; the executor runs the cheapest. <bookmark mark='b'/> Here is the plan our own "
            "database, built for this part, chose for the Job: scan the words, aggregate them in a hash table, and "
            "keep the top twenty in a heap. It found Part 17's program by itself. <bookmark mark='c'/> And underneath "
            "is a second machine, the transaction manager, which lets thousands of users read and write at once, "
            "each as if alone, even through crashes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in stages], lag_ratio=0.2), *[GrowArrow(a) for a in arrows])
            vo.wait_until("b")
            self.play(FadeIn(eg), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Databases", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Codd's relational model, \ its algebra, \ and normal forms",
            r"how a query runs: \ iterators, \ joins, \ and their costs, \ measured",
            r"Selinger's optimizer, \ and why size estimates go wrong",
            r"B+ trees, \ and indexes in general",
            r"transactions: \ serializability, \ two-phase locking, \ snapshots, \ isolation levels",
            r"recovery with ARIES, \ column stores, \ and our database running the Job",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 35 of Computer Science, Built: Databases. <bookmark mark='a'/> We start with Codd's idea "
            "and the algebra it created, and the theory of good table design. We follow a query through iterators "
            "and joins, measuring their costs, and watch an optimizer search for the cheapest plan, and see why its "
            "estimates go wrong. We build a B-plus tree. Then transactions: what it means for concurrent work to be "
            "correct, how locking and snapshots achieve it, and what the weaker isolation levels give up. Then "
            "recovery with ARIES, column stores for analytics, and our own database running the Job."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (DATA, LAM)
