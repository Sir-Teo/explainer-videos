from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, COST, CTRL, DATA, FILE_COLORS, FUNC, HEAD, NO, PART, YES, code,
                                   grid_table, load, region)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.compare()

    def card(self):
        card = chapter_card(15, r"The Job, \ linked", r"What does writing it properly cost?", part=PART)
        with self.voiceover("Chapter fifteen. The Job, linked."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def design(self):
        j = load("job")
        head = label(r"The Job, \ version 1", font_size=34).to_edge(UP, buff=0.3)
        desc = [("main.s", r"reads letters into a 256-byte buffer \\ in its own stack frame", FILE_COLORS[0]),
                ("table.s", r"\texttt{lookup}: \ a linked list of 16-byte nodes \\ on the heap, \ kept in first-seen "
                            r"order", FILE_COLORS[1]),
                ("alloc.s", r"\texttt{alloc}: \ a bump allocator \\ over 384 KB of \texttt{.bss}", FILE_COLORS[2]),
                ("io.s", r"\texttt{getc}, \ \texttt{putc}, \ \texttt{printnum} \\ (digits in a stack buffer)",
                 FILE_COLORS[3])]
        tiles = VGroup()
        for (name, d, c), o in zip(desc, j["objects"]):
            tiles.add(VGroup(region(2.9, 0.6, rf"{name} \ ({o['text']} B)", c, font_size=20),
                             label(d, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.15))
        tiles.arrange_in_grid(2, 2, buff=(0.8, 0.5)).next_to(head, DOWN, buff=0.4)
        node = VGroup(*[region(1.3, 0.5, t, c, font_size=16) for t, c in (("next", FUNC), ("letters", DATA),
                                                                         ("length", CTRL), ("count", YES))]).arrange(
            RIGHT, buff=0).to_edge(DOWN, buff=0.9)
        nl = label(r"a node", font_size=17, color=GREY_B).next_to(node, LEFT, buff=0.2)
        conv = note(r"every function follows chapter 4's convention: \ frames, \ saved registers, \ aligned "
                    r"\texttt{sp}", font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the Job written the way a compiler would write it. <bookmark mark='a'/> main reads letters into "
            "a buffer in its own stack frame. The table is a linked list of sixteen-byte nodes on the heap, kept in "
            "the order words were first seen, so ties break exactly as before. The allocator just bumps a pointer "
            "through three hundred and eighty-four kilobytes of bss, never freeing anything, which is all the Job "
            "needs. And the input and output routines include printnum, which keeps its digits in a small buffer in "
            "its frame. <bookmark mark='b'/> Each node holds a pointer to the next, a pointer to the word's letters, "
            "its length and its count. <bookmark mark='c'/> And every function obeys the calling convention of "
            "chapter four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(node), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(conv))
        self.wait(0.3)
        self.clear_scene()

    def compare(self):
        j = load("job")
        rows = j["rows"]
        head = label(r"Against Part 6's single file", font_size=34).to_edge(UP, buff=0.3)
        body = [[r["name"], f"{r['bytes']:,}", r"yes" if r["same"] else r"no", f"{r['v0']:,}", f"{r['v1']:,}",
                 rf"{100 * (r['v1'] / r['v0'] - 1):+.0f}\%"] for r in rows]
        t = grid_table([r"input", r"bytes", r"same output", r"version 0", r"version 1", r"change"], body,
                       [2.4, 1.6, 2.2, 2.2, 2.2, 1.6], row_h=0.55, font_size=20,
                       colors=[[GREY_A, GREY_B, YES, CTRL, DATA, HEAD]] * len(body), mono_cols=()).move_to(UP * 0.5)
        pts = VGroup(
            label(r"slower on a paragraph: \ every byte now costs a call to \texttt{getc}", font_size=21, color=NO),
            label(r"faster on long texts: \ walking a list is one instruction per entry cheaper than counting "
                  r"through an array", font_size=21, color=YES),
            label(rf"the deepest the stack ever went: \ {rows[0]['stack']} bytes", font_size=21, color=GREY_A),
            label(r"the algorithm is unchanged: \ still a scan of the whole vocabulary per word", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "How does it compare with Part 6's single hand-written file? <bookmark mark='a'/> On a paragraph, the "
            "first chapter of Pride and Prejudice, and twenty thousand bytes, the output is identical every time. "
            "<bookmark mark='b'/> On the paragraph, version one is a few percent slower: every byte of input now "
            "costs a function call and return. <bookmark mark='c'/> On longer texts it is faster, by eleven percent "
            "at twenty thousand bytes, because following a next pointer takes one instruction fewer per entry than "
            "counting through an array. <bookmark mark='d'/> The stack never went deeper than three hundred and "
            "twenty bytes. <bookmark mark='e'/> Structure, it turns out, costs almost nothing here. But the "
            "algorithm has not changed: each word still pays for a scan of the vocabulary. Part 13's compiler will "
            "write this program automatically, and Act Four will change the algorithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.4))
            for mk, p in zip("bcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
