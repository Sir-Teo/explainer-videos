from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, big, load, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.ledger()
        self.dictionary()
        self.preview()
        self.plan()

    def ledger(self):
        d = load("hook")
        led = d["ledger"]
        head = label(r"Row 7: \ sort, \ then count", font_size=36).to_edge(UP, buff=0.35)
        rows = led + [{"part": 17, "label": r"a hash table"}]
        tab = ledger_table(rows, shown=len(led), highlight=(len(led) - 1,), font_size=21, row_h=0.42,
                           label_width=4.8).move_to(DOWN * 0.3)
        cap = label(rf"{human_time(d['v1_seconds'])} \ on one core: \ {big(d['v1_cmp'])} comparisons of words",
                    font_size=23, color=COST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where we left the ledger. <bookmark mark='a'/> Sorting the words, then counting runs of equal ones, "
            "took five seconds on one core: faster than four cores running the old algorithm. <bookmark mark='b'/> "
            "But the sort did a hundred million comparisons of words to answer a simpler question. The Job never "
            "needed the words in order. It needed, for each word, to find its count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows))
            vo.wait_until("a")
            self.play(Indicate(tab.rows[len(led) - 1], color=COST))
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def dictionary(self):
        d = load("hook")
        head = label(r"What the Job really needs", font_size=36).to_edge(UP, buff=0.35)
        ops = VGroup(
            VGroup(mono("insert(word)", 26, CODE), label(r"a new word, \ with count 1", font_size=22, color=GREY_A)),
            VGroup(mono("find(word)", 26, CODE), label(r"is it there? \ where is its count?", font_size=22,
                                                        color=GREY_A)),
            VGroup(mono("count += 1", 26, CODE), label(r"once per word of the text", font_size=22, color=GREY_A)),
        )
        for o in ops:
            o.arrange(RIGHT, buff=0.6)
        ops.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        nums = VGroup(
            label(rf"{words(d['words'])} finds, \ {words(d['distinct'])} inserts", font_size=24, color=DATA),
            label(r"a \textbf{dictionary}: \ the most used abstract data type in computing", font_size=24,
                  color=HEAD),
            label(r"can each operation take constant time, \ whatever the size?", font_size=26, color=YES),
        ).arrange(DOWN, buff=0.3).next_to(ops, DOWN, buff=0.7)
        with self.voiceover(
            "Strip the Job to its operations. <bookmark mark='a'/> Insert a word the first time it appears. Find it "
            "every other time. Add one to its count. <bookmark mark='b'/> Over the thirty novels, that is four "
            "point six million finds and fifty-eight thousand inserts. <bookmark mark='c'/> A structure that "
            "supports insert and find by key is a dictionary, perhaps the most used abstract data type there is. "
            "<bookmark mark='d'/> The question of this part: can each operation take constant time, however many "
            "words there are?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.1) for o in ops], lag_ratio=0.4), run_time=2)
            for mk, n in zip("bcd", nums):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.3)
        self.clear_scene()

    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"hashing: \ expected $O(1)$, \ and how an adversary breaks it", font_size=27, color=DATA),
            label(r"linear probing's $\tfrac12\bigl(1 + 1/(1-\alpha)^2\bigr)$, \ measured", font_size=27,
                  color=CTRL),
            label(r"balanced trees: \ guarantees instead of expectations", font_size=27, color=LAM),
            label(r"amortized structures: \ splay trees, \ Fibonacci heaps, \ union--find", font_size=27,
                  color=YES),
            label(r"the Job with a hash table: \ ledger row 8", font_size=27, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> Hashing, which makes insert and find constant time "
            "on average, and the attack that breaks a careless hash function. <bookmark mark='b'/> Donald Knuth's "
            "first analysis of an algorithm, linear probing, checked against measurement. <bookmark mark='c'/> "
            "Balanced trees, which trade expectations for guarantees. <bookmark mark='d'/> Structures that are "
            "fast only on average over a sequence: splay trees, Fibonacci heaps and union–find. <bookmark "
            "mark='e'/> And the Job with a hash table: ledger row eight."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Data Structures", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the dictionary; \ the birthday bound",
            r"chaining, \ universal hashing, \ open addressing, \ cuckoo and perfect hashing",
            r"binary search trees; \ AVL, \ red--black, \ treaps, \ skip lists, \ splay trees",
            r"B-trees; \ priority queues; \ union--find",
            r"tries and succinct structures; \ persistence; \ cache-friendly layouts",
            r"hash tables in practice; \ the Job, \ hashed",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 17 of Computer Science, Built: Data Structures. <bookmark mark='a'/> In this part: the dictionary "
            "and the birthday bound; chaining, universal hashing, open addressing, cuckoo and perfect hashing; "
            "binary search trees and the ways to keep them balanced; B-trees, priority queues and union–find; "
            "tries, persistence and the memory hierarchy; and hash tables as real systems build them."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
