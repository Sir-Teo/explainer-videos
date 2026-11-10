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
            "Hash tables and search trees treat a key as an opaque value to hash or compare. A trie, "
            "Edward Fredkin's name from 1960, uses the key's letters as directions. <bookmark mark='a'/> "
            "The root has one edge per possible first letter, each child one edge per second letter, and "
            "a word is a path; nodes where a word ends are marked. Finding a word of L letters takes L "
            "steps, however many words are stored. <bookmark mark='b'/> Words that share a prefix share a"
            " path, so a trie answers prefix queries directly: autocomplete, and the longest-prefix match"
            " that routes every internet packet. <bookmark mark='c'/> Chains of nodes with a single child"
            " waste space, and a radix tree merges each chain into one edge labelled with a string."
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
            "mark='a'/> The words have about four hundred and fifty thousand letters, but the trie needs "
            "far fewer nodes, because so many words share beginnings. <bookmark mark='b'/> The radix tree"
            " needs fewer still, under two nodes per word. <bookmark mark='c'/> Yet each node, stored the"
            " obvious way, costs a pointer per child, eight bytes each. The last idea of this chapter is "
            "to store the tree's shape itself in a couple of bits per node."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def succinct(self):
        d = load("tries")
        head = label(r"LOUDS: \ one checked tree, \ two kinds of position", font_size=32).to_edge(UP, buff=0.3)
        children = [[1, 2], [3, 4], [], [5], [], []]
        bits = "".join("1" * len(kids) + "0" for kids in children)
        assert bits == "11011001000" and len(bits) == 2 * len(children) - 1
        positions = {0: [-4.6, 2.1], 1: [-5.4, 1.2], 2: [-3.7, 1.2],
                     3: [-6.0, 0.3], 4: [-4.8, 0.3], 5: [-6.0, -0.6]}
        nodes = {v: VGroup(Circle(radius=0.23, stroke_color=HEAD if v == 1 else DATA,
                                  stroke_width=2, fill_color=BG, fill_opacity=1),
                           mono(str(v), 18, WHITE)).move_to([*xy, 0]) for v, xy in positions.items()}
        edges = VGroup(*[Line(nodes[v].get_center(), nodes[w].get_center(), buff=0.23,
                              color=GREY_B, stroke_width=1.5)
                         for v, kids in enumerate(children) for w in kids])
        tree = VGroup(edges, *nodes.values())
        tree_note = label(r"BFS node IDs: \ 0 through 5", font_size=18, color=GREY_B).next_to(tree, DOWN, buff=0.18)
        groups = VGroup()
        cursor = 0
        for v, kids in enumerate(children):
            cells = VGroup()
            for b in "1" * len(kids) + "0":
                cell = VGroup(Square(side_length=0.43, stroke_color=HEAD if v == 1 else GREY_B,
                                     fill_color=DATA if b == "1" else BG, fill_opacity=0.5 if b == "1" else 1),
                              mono(b, 18, WHITE))
                cell[1].move_to(cell[0]); cells.add(cell)
            cells.arrange(RIGHT, buff=0.02)
            tag = mono(str(v), 16, HEAD if v == 1 else GREY_B).next_to(cells, UP, buff=0.09)
            groups.add(VGroup(cells, tag))
            cursor += len(kids) + 1
        groups.arrange(RIGHT, buff=0.14).move_to([2.1, 1.65, 0])
        encoding = label(r"each node: \ one 1 per child, \ then 0; \ $2n-1 = 11$ bits", font_size=19,
                         color=DATA).next_to(groups, DOWN, buff=0.2)
        definitions = VGroup(
            MathTex(r"\operatorname{rank}_1(i)=\#1\text{s in }b[0:i]", font_size=26, color=DATA),
            label(r"$\operatorname{select}_b(j)$: \ position of zero-based $j$th bit $b$", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.16).next_to(encoding, DOWN, buff=0.32)
        witness = VGroup(
            MathTex(r"s_1=\operatorname{select}_0(0)+1=3", font_size=27, color=HEAD),
            MathTex(r"\text{first child of node 1}=\operatorname{rank}_1(3)+1=3", font_size=27, color=YES),
            MathTex(r"\text{parent}(5)=\operatorname{rank}_0(\operatorname{select}_1(4))=3", font_size=26, color=LAM),
        ).arrange(DOWN, buff=0.17).move_to([0, -1.25, 0])
        notes = VGroup(
            label(r"built here: \ rank only; \ fixed 512/64-bit directory + bounded popcount", font_size=20, color=YES),
            label(rf"{words(d['rank_queries_checked'])} rank queries checked, including both ends; \ "
                  rf"{words(d['rank_overhead'])} logical directory bits for {words(d['rank_bits'])} input bits", font_size=19, color=HEAD),
            label(r"packed-bit estimate excludes Python objects; \ fixed overhead is not $o(n)$; \ "
                  r"succinct theory uses a different growing directory", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Succinct tree theory stores topology in about two bits per node, plus a lower-order "
            "navigation index. <bookmark mark='a'/> Here is a concrete six-node tree. In breadth-first "
            "order, write one for each child, then zero. Its eleven bits are exactly two n minus one. "
            "<bookmark mark='b'/> Node IDs and bit positions are different. Rank counts ones before a bit"
            " position; select gives the position of a numbered occurrence. Every index here starts at "
            "zero. <bookmark mark='c'/> Node one's block starts at bit three. Two ones precede it, so its"
            " first child has node ID three. The rank of zeroes before the one for node five gives its "
            "parent, node three. <bookmark mark='d'/> Our code implements rank with counts every five "
            "hundred and twelve bits, finer counts every sixty-four, and a bounded population count. It "
            "does not implement select. <bookmark mark='e'/> All sixty-five thousand five hundred and "
            "thirty-seven rank positions pass an independent prefix-sum check, including zero and the "
            "full length. <bookmark mark='f'/> The displayed overhead is a logical packed-bit estimate, "
            "excluding Python objects. This fixed directory is not Jacobson's lower-order construction. "
            "Compressed indexes later exploit entropy or repetition; they need not shrink every input."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tree), FadeIn(tree_note))
            vo.wait_until("a"); self.play(FadeIn(groups), FadeIn(encoding))
            vo.wait_until("b"); self.play(FadeIn(definitions))
            vo.wait_until("c"); self.play(FadeOut(definitions), FadeIn(witness))
            vo.wait_until("d"); self.play(FadeIn(notes[0]))
            vo.wait_until("e"); self.play(FadeIn(notes[1]))
            vo.wait_until("f"); self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
