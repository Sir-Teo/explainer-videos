from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load, log_axes)


class Cdn(VoiceoverScene):
    def construct(self):
        self.card()
        self.edge()
        self.zipf()
        self.caches()

    def card(self):
        card = chapter_card(14, r"Caches at the edge", r"Why serve the world from a thousand places?",
                            lit=(1998, 2002), extra=((1998, r"Akamai"), (1999, r"Breslau et al.: \ Zipf-like "
                                                                               r"requests"),
                                                     (2002, r"Che, Tung and Wang")), part=PART)
        with self.voiceover("Chapter fourteen. Caches at the edge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def edge(self):
        head = label(r"Move the bytes closer", font_size=36).to_edge(UP, buff=0.3)
        origin = box(2.0, 0.7, r"origin: \ Frankfurt", HEAD, font_size=18).move_to([4.6, 1.6, 0])
        edges = VGroup(*[box(1.6, 0.6, t, YES, font_size=17) for t in (r"edge: \ San Jose", r"edge: \ Chicago",
                                                                       r"edge: \ Tokyo")])
        edges.arrange(DOWN, buff=0.45).move_to([0, 0.4, 0])
        users = VGroup(*[Dot(radius=0.08, color=DATA) for _ in range(9)])
        for k, u in enumerate(users):
            u.move_to(edges[k // 3].get_center() + LEFT * (2.5 + 0.35 * (k % 3)) + UP * (0.18 * (k % 3 - 1)))
        links = VGroup(*[Line(u.get_center(), edges[k // 3].get_left(), color=GREY_D, stroke_width=1.5)
                         for k, u in enumerate(users)])
        back = VGroup(*[DashedLine(e.get_right(), origin.get_left(), color=GREY_D, dash_length=0.08) for e in edges])
        lines = VGroup(
            wrapped_label(r"throughput $\propto 1/\text{RTT}$ \ (Mathis), \ and each handshake costs round trips: "
                          r"\ the cheapest optimization is a shorter path", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"a CDN keeps copies in thousands of sites; \ DNS answers each user with a nearby one \ "
                          r"(short TTLs), \ or \textbf{anycast} announces one address from every site and lets BGP "
                          r"(Part 36) pick the closest", 12.4, font_size=21, color=YES),
            wrapped_label(r"a miss goes back to the origin; \ so: \ how often can a small cache answer?", 12.4,
                          font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Everything in this part says that distance is expensive. Throughput falls as one over the round trip, "
            "and every handshake costs round trips. <bookmark mark='a'/> So the cheapest optimization of all is to "
            "make the path shorter. A content delivery network, starting with Akamai in 1998, keeps copies of "
            "popular content in thousands of places near users. <bookmark mark='b'/> Users are steered to a nearby "
            "copy in two ways: by DNS, answering each resolver with the address of a nearby site, with short times "
            "to live; or by anycast, announcing the same address from every site and letting BGP route each user "
            "to the closest. <bookmark mark='c'/> A request the nearby cache cannot answer goes back to the origin. "
            "So the question is how much a small cache can answer, and that depends on what people ask for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(origin), FadeIn(edges), FadeIn(users), Create(links), Create(back))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def zipf(self):
        c = load("cdn")
        head = label(r"Zipf's law, \ in the novels", font_size=36).to_edge(UP, buff=0.3)
        g = log_axes([0, 5, 1], [0, 6, 1], x_length=6.4, y_length=4.0, x_label=r"rank of the word",
                     y_label=r"occurrences").move_to([-3.0, -0.5, 0])
        ax = g.ax
        pts = [(math.log10(r), math.log10(n)) for r, n in c["rank_counts"] if n > 0]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=DATA) for x, y in pts])
        s = c["s"]
        # line through the fitted region, anchored at rank 100
        r100 = next(n for r, n in c["rank_counts"] if r >= 100)
        y100 = math.log10(r100)
        fit = Line(ax.c2p(1, y100 + s), ax.c2p(4.6, y100 - 2.6 * s), color=YES, stroke_width=2.5)
        top = ", \\ ".join(rf"\texttt{{{w}}} {n:,}" for w, n in c["top"][:5])
        notes = VGroup(
            wrapped_label(rf"{c['words']:,} words, \ {c['distinct']:,} distinct", 5.6, font_size=20, color=WHITE),
            wrapped_label(rf"most common: \ {top}", 5.6, font_size=18, color=GREY_A),
            wrapped_label(rf"the $k$th most common word occurs $\propto k^{{-s}}$ times: \ fitted on ranks 10 to "
                          rf"10{{,}}000, \ $s = {s:.2f}$", 5.6, font_size=20, color=YES),
            wrapped_label(r"web requests follow the same law \ (Breslau et al., 1999, \ $s$ between 0.6 and 1): \ a "
                          r"few objects are wanted constantly, \ most almost never", 5.6, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "In 1935 George Kingsley Zipf noticed that in any long text, the k-th most common word appears roughly "
            "in proportion to one over k. We can check it on the novels we have been counting all series. "
            "<bookmark mark='a'/> Four point six million words, fifty-eight thousand distinct ones; the commonest "
            "are the, and, to, of, a. Plot each word's count against its rank, both on logarithmic scales. "
            "<bookmark mark='b'/> The points fall on a line. Fitted between ranks ten and ten thousand, its slope "
            "is minus one point two two. <bookmark mark='c'/> Requests for web objects follow the same kind of "
            "law, as Lee Breslau and colleagues measured in 1999, with exponents a little below one: a few objects "
            "are requested constantly, and a long tail almost never. That shape is what makes caching work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def caches(self):
        c = load("cdn")
        head = label(r"An LRU cache on the novels", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['size']:,}", f"{r['size'] / c['distinct'] * 100:.2g}\\%", f"{r['ideal'] * 100:.1f}\\%",
                 f"{r['che'] * 100:.1f}\\%", f"{r['lru'] * 100:.1f}\\%"] for r in c["rows"]]
        tab = grid_table([r"cache size, \ words", r"of the vocabulary", r"best static", r"Che's formula",
                          r"LRU, \ measured"], rows, widths=[2.6, 2.4, 1.9, 2.2, 2.2], row_h=0.44, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][3].set_color(KERN)
            tab.cells[k][4].set_color(YES)
        lines = VGroup(
            wrapped_label(r"requests: \ the first two million words of the novels, \ in order; \ the cache keeps "
                          r"the most recently used words", 12.4, font_size=20, color=GREY_A),
            MathTex(r"\text{Che: } \sum_i \big(1 - e^{-p_i T}\big) = \text{size}, \qquad \text{hit rate} = \sum_i "
                    r"p_i\big(1 - e^{-p_i T}\big)", font_size=30, color=KERN),
            wrapped_label(r"a cache holding 1.7\% of the vocabulary answers 79\% of requests: \ that is Zipf's law "
                          r"at work", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"LRU beats Che's prediction because text is not independent draws: \ \texttt{whale} "
                          r"comes in bursts, \ as real web traffic does, \ and recency captures it", 12.4,
                          font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.35)
        lines[1].set_x(0)
        with self.voiceover(
            "Treat each word of the novels, in order, as a request, and put a cache in front of it that keeps the "
            "most recently used words: least-recently-used replacement, as in Part 9. <bookmark mark='a'/> A cache "
            "of a thousand words, under two percent of the vocabulary, answers seventy-nine percent of the "
            "requests. That is Zipf's law at work. <bookmark mark='b'/> In 2002 Hao Che and his colleagues found a "
            "simple, accurate way to predict an LRU cache's hit rate when requests are independent: each object "
            "stays in the cache for about the same characteristic time T, set so that the expected number of "
            "objects in it equals its size. <bookmark mark='c'/> Here the formula underestimates, by up to ten "
            "points. The reason is in the text: words are not independent draws. Whale comes in bursts, in the "
            "chapters about whales, and recency captures that, just as it captures the bursts of real web traffic "
            "when something becomes popular. At ten thousand words, LRU matches the best static choice of the most "
            "common words."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(lines[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k][:3])) for k in range(1, 5)], lag_ratio=0.2))
            self.play(LaggedStart(*[FadeIn(tab.cells[k][4]) for k in range(1, 5)], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(lines[2]))
            vo.wait_until("b")
            self.play(Write(lines[1]), LaggedStart(*[FadeIn(tab.cells[k][3]) for k in range(1, 5)], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, NO)
