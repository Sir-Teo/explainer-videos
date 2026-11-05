from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Tries(VoiceoverScene):
    def construct(self):
        self.card()
        self.trie()
        self.corpus()
        self.succinct()

    def card(self):
        card = chapter_card(12, r"Tries and succinct structures", r"Can the key's letters be the path?", lit=(1960,),
                            extra=((1960, r"Fredkin: \ trie memory"), (1989, r"Jacobson: \ succinct trees")),
                            part=PART)
        with self.voiceover("Chapter twelve. Tries, and succinct structures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def trie(self):
        head = label(r"A trie: \ one edge per letter", font_size=34).to_edge(UP, buff=0.3)
        words_ = ["tea", "ten", "the", "then", "they", "to"]
        # positions by hand: root t; children e, h, o
        P = {"": [0, 2.0], "t": [0, 1.1], "te": [-2.6, 0.2], "th": [0.6, 0.2], "to": [3.0, 0.2],
             "tea": [-3.4, -0.7], "ten": [-1.8, -0.7], "the": [0.6, -0.7], "then": [-0.2, -1.6],
             "they": [1.4, -1.6]}
        ends = set(words_)
        nodes = {k: VGroup(Circle(radius=0.2, stroke_color=YES if k in ends else DATA, stroke_width=2,
                                  fill_color=YES if k in ends else BG, fill_opacity=0.35 if k in ends else 1)
                           ).move_to([x, y - 0.3, 0]) for k, (x, y) in P.items()}
        edges = VGroup()
        letters = VGroup()
        for k in P:
            if k:
                p = k[:-1]
                ln = Line(nodes[p].get_center(), nodes[k].get_center(), buff=0.2, color=GREY_B, stroke_width=1.6)
                edges.add(ln)
                letters.add(mono(k[-1], 18, CODE).move_to(ln.get_center() + LEFT * 0.18))
        pts = VGroup(
            label(r"find a word of $L$ letters in $O(L)$ steps, \ however many words are stored", font_size=22,
                  color=YES),
            label(r"words with a common prefix share a path: \ prefix search, \ autocomplete, \ IP routing",
                  font_size=22, color=GREY_A),
            label(r"a \textbf{radix tree} merges each chain of single children into one edge", font_size=22,
                  color=LAM),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Hash tables and search trees treat a key as an opaque value to hash or compare. A trie, Edward "
            "Fredkin's name from 1960, uses the key's letters as directions. <bookmark mark='a'/> The root has one "
            "edge per possible first letter, each child one edge per second letter, and a word is a path; nodes "
            "where a word ends are marked. Finding a word of L letters takes L steps, however many words are "
            "stored. <bookmark mark='b'/> Words that share a prefix share a path, so a trie answers prefix queries "
            "directly: autocomplete, and the longest-prefix match that routes every internet packet. <bookmark "
            "mark='c'/> Chains of nodes with a single child waste space, and a radix tree merges each chain into "
            "one edge labelled with a string."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], Create(edges), FadeIn(letters))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def corpus(self):
        d = load("tries")
        head = label(r"The Job's vocabulary as a trie", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"", r"count"], [
            [r"distinct words", words(d["distinct"])],
            [r"letters in them", words(d["letters"])],
            [r"trie nodes", words(d["trie_nodes"])],
            [r"radix-tree nodes", words(d["radix_nodes"])],
        ], widths=[4.4, 2.6], row_h=0.55, font_size=22, mono_cols=(),
            colors=[[WHITE, GREY_A], [WHITE, GREY_A], [WHITE, DATA], [WHITE, LAM]]).next_to(head, DOWN, buff=0.6)
        share = 1 - d["trie_nodes"] / d["letters"]
        pts = VGroup(
            label(rf"shared prefixes save {100 * share:.0f}\% of the letters", font_size=23, color=YES),
            label(rf"merging chains leaves {words(d['radix_nodes'])} nodes: \ under two per word", font_size=23,
                  color=LAM),
            label(r"but a pointer per child is expensive: \ store the shape itself in as few bits as possible",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Here is the Job's vocabulary, all fifty-eight thousand distinct words, in a trie. <bookmark "
            "mark='a'/> The words have about four hundred and fifty thousand letters, but the trie needs far fewer "
            "nodes, because so many words share beginnings. <bookmark mark='b'/> The radix tree needs fewer still, "
            "under two nodes per word. <bookmark mark='c'/> Yet each node, stored the obvious way, costs a pointer "
            "per child, eight bytes each. The last idea of this chapter is to store the tree's shape itself in a "
            "couple of bits per node."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def succinct(self):
        d = load("tries")
        head = label(r"Succinct structures \ (Jacobson, \ 1989)", font_size=34).to_edge(UP, buff=0.3)
        bits = "1101101001100100"
        row = VGroup(*[VGroup(Square(side_length=0.48, stroke_color=GREY_B, stroke_width=1.4,
                                     fill_color=DATA if b == "1" else BG, fill_opacity=0.6 if b == "1" else 1),
                              mono(b, 18, WHITE)) for b in bits]).arrange(RIGHT, buff=0.04)
        for c in row:
            c[1].move_to(c[0])
        row.next_to(head, DOWN, buff=0.6)
        steps = VGroup(
            label(r"a tree of $n$ nodes in $2n$ bits: \ write each node's children in unary, \ level by level "
                  r"\ (LOUDS)", font_size=21, color=GREY_A),
            MathTex(r"\mathrm{rank}(i) = \#\text{ones in } b[0..i), \qquad \mathrm{select}(j) = \text{position of "
                    r"the } j\text{-th one}", font_size=30, color=DATA),
            label(r"navigation is rank and select: \ the first child of node $i$ sits at $\mathrm{select}(i) + 1$",
                  font_size=21, color=GREY_A),
            label(r"rank in $O(1)$ time: \ a count every 512 bits, \ a smaller one every 64, \ a popcount for the "
                  r"rest", font_size=21, color=YES),
            label(rf"measured: \ {words(d['rank_bits'])} bits need {words(d['rank_overhead'])} extra "
                  rf"({100 * d['rank_overhead'] / d['rank_bits']:.0f}\%), \ every rank checked", font_size=21,
                  color=HEAD),
            label(r"within $o(n)$ bits of the information-theoretic minimum: \ FM-indexes for genomes \ (Part 21)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(row, DOWN, buff=0.45)
        with self.voiceover(
            "Guy Jacobson showed in his 1989 thesis that a tree can be stored in about two bits per node and still "
            "be navigated quickly. <bookmark mark='a'/> Write, for each node in level order, a one for each child "
            "and then a zero. That string of two n bits determines the tree. <bookmark mark='b'/> Navigation then "
            "reduces to two questions about the bit string. Rank of i: how many ones come before position i. "
            "Select of j: where is the j-th one. <bookmark mark='c'/> A node's children are found by a select, and "
            "its parent by a rank. <bookmark mark='d'/> Rank takes constant time with a small directory: a count "
            "every five hundred and twelve bits, a finer count every sixty-four, and the processor's popcount "
            "instruction for the remainder. <bookmark mark='e'/> We built one: the directory adds about a fifth to "
            "the bits, and every rank we checked was right. <bookmark mark='f'/> Structures within a lower-order "
            "term of the information-theoretic minimum are called succinct, and in Part 21 they index whole "
            "genomes in less space than the genome itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()
