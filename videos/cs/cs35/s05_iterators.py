from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, box, code, load, mono, num)


class Iterators(VoiceoverScene):
    def construct(self):
        self.card()
        self.volcano()
        self.job_plan()
        self.access()

    def card(self):
        card = chapter_card(4, r"How a query runs", r"What does the database actually do?", lit=(1994,),
                            extra=((1994, r"Graefe: \ Volcano"),), part=PART)
        with self.voiceover("Chapter four. How a query runs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def volcano(self):
        head = label(r"Operators as iterators", font_size=36).to_edge(UP, buff=0.3)
        ops = VGroup(*[box(3.4, 0.7, rf"\text{{{t}}}", c, font_size=21) for t, c in (
            ("Top 20 (a heap)", KERN), ("Hash aggregate by word", LAM), ("Scan words", DATA))]).arrange(DOWN, buff=0.6)
        ops.move_to([-3.6, 0.7, 0])
        arrows = VGroup(*[Arrow(ops[i + 1].get_top(), ops[i].get_bottom(), buff=0.06, color=GREY_B, stroke_width=2)
                          for i in range(2)])
        pulls = VGroup(*[label(r"\texttt{next()}", font_size=16, color=HEAD).next_to(a, RIGHT, buff=0.1)
                         for a in arrows])
        api = code([
            "class Operator:",
            "    def open(self): ...",
            "    def next(self): ...   # one tuple, or None",
            "    def close(self): ...",
        ], size=20).move_to([2.6, 1.2, 0])
        lines = VGroup(
            label(r"every operator has the same three calls; \ each pulls tuples from its children", font_size=20,
                  color=WHITE),
            label(r"a \textbf{pipeline}: \ a tuple flows up as soon as it exists; \ nothing is materialized but the "
                  r"hash table", font_size=20, color=YES),
            label(r"\textbf{blocking} operators \ (sort, \ the aggregate's output, \ a hash join's build side) "
                  r"must see all their input first", font_size=20, color=NO),
            label(r"Graefe's Volcano \ (1994): \ new operators plug in without changing the others", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        lines.set_x(0)
        with self.voiceover(
            "A plan is a tree of operators, and almost every database runs it the same way. <bookmark mark='a'/> "
            "Each operator is an iterator, with three calls: open, next, close. Next returns one tuple, or says there "
            "are no more. <bookmark mark='b'/> The root asks its child for the next tuple, which asks its child, down "
            "to the scan, which reads a row from a page and passes it up. <bookmark mark='c'/> Tuples flow up one at a "
            "time, so the scan never stores the table. <bookmark mark='d'/> Some operators must see all their input "
            "before producing anything: a sort, a hash join building its table, an aggregate. <bookmark mark='e'/> "
            "Goetz Graefe's Volcano made this the standard model, because any operator can sit under any other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ops))
            vo.wait_until("a")
            self.play(FadeIn(api), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(*[GrowArrow(a) for a in arrows], FadeIn(pulls))
            vo.wait_until("c")
            dot = Dot(ops[2].get_top(), radius=0.09, color=YES)
            self.play(FadeIn(dot), FadeIn(lines[1]))
            self.play(dot.animate.move_to(ops[1].get_bottom()), run_time=0.8)
            self.play(FadeOut(dot))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def job_plan(self):
        j = load("job")
        head = label(r"The Job's plan, \ run", font_size=36).to_edge(UP, buff=0.3)
        ex = VGroup(*[mono(ln, 20, CODE) for ln in j["explain"].splitlines()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        ex.next_to(head, DOWN, buff=0.45)
        if ex.width > 12.8:
            ex.width = 12.8
        st = j["stats"]
        flow = VGroup(
            label(rf"the scan produced {num(st['Scan words'])} tuples", font_size=23, color=DATA),
            label(rf"the hash aggregate turned them into {num(st['Hash aggregate by words.word'])} groups", font_size=23,
                  color=LAM),
            label(r"the heap kept 20", font_size=23, color=KERN),
            label(rf"{num(st['pages'])} pages of 100 rows read, \ once; \ the alternative, \ sorting first, \ was "
                  rf"estimated at {num(j['plans']['sort aggregate']['cost'])} page reads", font_size=23, color=HEAD),
            label(rf"our engine, \ in Python: \ {j['ours_seconds']:.1f} s; \ sqlite3, \ in C: \ "
                  rf"{j['sqlite_seconds']:.2f} s; \ same answer", font_size=23, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(ex, DOWN, buff=0.7)
        for f in flow:
            if f.width > 12.8:
                f.width = 12.8
        flow.set_x(0)
        with self.voiceover(
            "Here is the Job's plan from our database, with what happened when it ran. <bookmark mark='a'/> The scan "
            "produced four point six million tuples. <bookmark mark='b'/> The hash aggregate folded them into "
            "fifty-eight thousand groups, one per distinct word. <bookmark mark='c'/> And the top-twenty operator kept "
            "a heap of twenty. <bookmark mark='d'/> The table was read once, forty-six thousand pages; the other "
            "plan, sorting the words to group them, was estimated at five times as many page reads, and rejected. "
            "<bookmark mark='e'/> Our engine, in Python, took seven seconds; sqlite, in C, two. The answers agree to "
            "the last count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ex))
            for mk, f in zip("abcde", flow):
                vo.wait_until(mk)
                self.play(FadeIn(f))
        self.wait(0.3)
        self.clear_scene()

    def access(self):
        it = load("iterators")
        head = label(r"Choosing an access path", font_size=36).to_edge(UP, buff=0.3)
        cols = VGroup()
        for name, title, c in (("nested loops", r"scan, \ then nested loops", NO),
                               ("hash join, full scan", r"scan, \ then a hash join", HEAD),
                               ("chosen", r"the optimizer's choice: \ the index", YES)):
            p = it["plans"][name]
            body = [ln.split("   (")[0] for ln in p["explain"].splitlines()[3:]]
            ex = VGroup(*[mono(ln[6:], 16, CODE) for ln in body]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            g = VGroup(label(title, font_size=21, color=c), ex,
                       label(rf"estimated {num(p['cost'])} pages; \ read {num(p['stats']['pages'])}", font_size=19,
                             color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            cols.add(g)
        cols.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.4).set_x(0)
        note = label(r"a \textbf{selection} on an indexed column: \ probe the B+ tree \ (chapter 8) \ instead of "
                     r"reading every page", font_size=20, color=LAM).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first choice is how to reach each table: read it all, or use an index. Here is the whale query on a "
            "sample of the corpus, three ways. <bookmark mark='a'/> Scan the words and join with nested loops. "
            "<bookmark mark='b'/> Scan and hash join: the same pages, a cheaper join. <bookmark mark='c'/> Or, as the "
            "optimizer chose, look up whale in an index, fetch only those rows, and join the books to them: "
            "eighty-five pages instead of twelve hundred. Its guess was off, ten whale rows where there are eighty-one, "
            "but the choice was still right. Chapter 7 shows what happens when a guess is far worse."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c))
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()


_ = (PART,)
