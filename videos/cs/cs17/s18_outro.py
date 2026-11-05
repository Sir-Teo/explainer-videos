from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono, slots)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        tiles = Group(
            tile(MathTex(r"1 - e^{-n^2/2m}", font_size=44, color=CTRL), r"the birthday bound", CTRL),
            tile(MathTex(r"\tfrac12\Bigl(1 + \tfrac{1}{(1-\alpha)^2}\Bigr)", font_size=40, color=DATA),
                 r"linear probing", DATA),
            tile(MathTex(r"h \le 1.44 \lg n", font_size=44, color=LAM), r"balanced trees", LAM),
            tile(MathTex(r"3\bigl(r(t) - r(x)\bigr) + 1", font_size=38, color=YES), r"the access lemma", YES),
            tile(MathTex(r"O\bigl(m\,\alpha(n)\bigr)", font_size=44, color=HEAD), r"union--find", HEAD),
            tile(MathTex(rf"\text{{row 8: }} {load('job')['seconds']:.2f}\text{{ s}}", font_size=40, color=COST),
                 r"the Job, \ hashed", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Data Structures", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. The dictionary, and the birthday bound that makes collisions certain. "
            "Chaining with universal hashing, which no adversary can defeat, and the attack that defeats a fixed "
            "hash. Linear probing and Knuth's formula, measured; cuckoo hashing's threshold at one half; perfect "
            "hashing in linear space. Search trees, balanced by heights, by colours or by coin flips; splay trees "
            "and their access lemma; B-trees for disks; Fibonacci heaps; union–find and the inverse Ackermann "
            "function; tries and succinct trees; persistence. And the Job with a hash table, six times faster "
            "than the sort."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"heaps in Dijkstra and Prim, \ union--find in Kruskal", [18]),
            (r"universal families, \ Bloom filters, \ sketches", [20]),
            (r"tries, \ suffix trees, \ FM-indexes", [21]),
            (r"concurrent hash maps and lock-free skip lists", [33]),
            (r"log-structured merge trees", [34]),
            (r"B+-trees and hash joins", [35]),
            (r"persistent trees: \ Git's object store", [41]),
            (r"inverted indexes", [47]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 18's graph algorithms run on heaps and union–find. Part 20 builds Bloom "
            "filters and sketches from universal hash families. Part 21 turns tries into suffix trees and "
            "compressed indexes. Part 33 makes hash maps and skip lists safe for many threads. Parts 34 and 35 "
            "build storage engines on log-structured merge trees and B-plus trees. Part 41's Git is a persistent "
            "tree, and Part 47's search engine is an inverted index."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"choosing", r"hash map for lookups; \ ordered map for ranges and neighbours"),
            (r"security", r"untrusted keys need a keyed hash \ (SipHash): \ hash flooding is real"),
            (r"performance", r"count cache lines, \ not just operations: \ open addressing beats chaining"),
            (r"databases", r"every index is a B+-tree or a hash: \ know which your query uses"),
            (r"interviews", r"heaps, \ tries and union--find solve half the classic problems"),
        ])
        with self.voiceover(
            "In practice. Choose a hash map for lookups and an ordered map when you need ranges or neighbours. Never "
            "hash untrusted keys with a fixed function; hash flooding is a real attack. Count cache lines as well "
            "as operations: an open-addressing table can be several times faster than a chained one. Every database "
            "index is a B-plus tree or a hash, and a query plan tells you which. And in interviews, heaps, tries "
            "and union–find solve half the classic problems."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that $h_{a,b}(x) = ((ax + b) \bmod p) \bmod m$, \ with $a, b$ random, \ is universal: \ "
            r"$\Pr[h(x) = h(y)] \le 1/m$ for $x \ne y$.",
            r"From linear probing's insertion cost $\tfrac12\bigl(1 + 1/(1-\alpha)^2\bigr)$, \ derive the "
            r"successful-search cost $\tfrac12\bigl(1 + 1/(1-\alpha)\bigr)$.",
            r"Show that union by rank keeps every tree's height at most $\lg n$, \ and that a chain of unions "
            r"without it can reach $n - 1$.",
            r"Prove that an AVL tree with $n$ nodes has height below $1.4405 \lg(n + 2)$.",
            r"\textit{Build.} \ Rewrite the Job v2 so that it needs no division per letter, \ in the Pebble "
            r"language, \ and measure its instructions per cycle on Part 8's core.",
            r"$\bigstar$ \textit{Research.} \ Prove that splay trees are dynamically optimal, \ or find any binary "
            r"search tree algorithm that is $o(\log \log n)$-competitive.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: remove the division from the Job's hash and see what it does to the instructions per cycle. "
            "The last, marked with a star, is a research problem: its answer is not known, and the notes say where "
            "to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 18, \ Graphs", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Euler's bridges, \ breadth and depth", DATA), (r"Dijkstra, \ and why it is universally optimal", LAM),
            (r"spanning trees with union--find", YES), (r"flows and cuts: \ one theorem, \ two faces", COST))]
                      ).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"the shape of road maps, \ the internet and compilers", font_size=26, color=GREY_A).to_edge(
            DOWN, buff=0.8)
        with self.voiceover(
            "Next time. Euler invented the graph to walk the bridges of Königsberg, and graphs are now the shape of "
            "road maps, the internet and compilers. Breadth-first and depth-first search; Dijkstra's algorithm on "
            "this part's heaps, and the recent proof that it is universally optimal; spanning trees with "
            "union–find; and flows and cuts, two faces of one theorem. Part 18, Graphs."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Cormen, Leiserson, Rivest and Stein, \textit{Introduction to Algorithms}, \ chapters 10--13, 18--19, 21",
             r"Knuth, \textit{The Art of Computer Programming}, \ volume 3, \ chapter 6",
             r"Tarjan, \textit{Data Structures and Network Algorithms}; \ Okasaki, \textit{Purely Functional Data "
             r"Structures}",
             r"Mehlhorn and Sanders, \textit{Algorithms and Data Structures}; \ Navarro, \textit{Compact Data "
             r"Structures}"],
            [r"Carter and Wegman (1979); \ Knuth, ``Notes on open addressing'' (1963); \ Celis (1986)",
             r"Fredman, Koml\'os and Szemer\'edi (1984); \ Pagh and Rodler (2001)",
             r"Adelson-Velsky and Landis (1962); \ Guibas and Sedgewick (1978); \ Seidel and Aragon (1989); \ Pugh "
             r"(1990)",
             r"Sleator and Tarjan (1985); \ Fredman and Tarjan (1987); \ Tarjan (1975); \ Bayer and McCreight (1970)",
             r"Jacobson (1989); \ Driscoll, Sarnak, Sleator and Tarjan (1989); \ Klink and W\"alde (2011)",
             r"Farach-Colton, Krapivin and Kuszmaul (2025); \ Demaine et al. (2004); \ Kraska et al. (2018)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
