from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.hdx()
        self.results()
        self.ramanujan()
        self.open()

    def card(self):
        card = chapter_card(11, r"Frontier: \ high-dimensional expanders",
                            r"What happens when triangles, \ not just edges, \ must expand?", lit=(2015, 2022),
                            extra=((2015, r"Marcus, \ Spielman and Srivastava"),
                                   (2022, r"good quantum codes; \ c$^3$ testable codes")), part=PART)
        with self.voiceover("Chapter eleven, the frontier. What happens when triangles, and not just edges, have to "
                            "expand?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hdx(self):
        head = label(r"Expansion in every dimension", font_size=36).to_edge(UP, buff=0.3)
        # a small triangulated disc, and the link of its centre vertex
        c = LEFT * 3.2 + DOWN * 0.3
        ring = [c + 2.0 * np.array([math.cos(2 * math.pi * k / 7), math.sin(2 * math.pi * k / 7), 0])
                for k in range(7)]
        tris = VGroup(*[Polygon(c, ring[k], ring[(k + 1) % 7], stroke_color=GREY_B, stroke_width=1.5,
                                fill_color=DATA, fill_opacity=0.18) for k in range(7)])
        centre = Dot(c, radius=0.1, color=HEAD)
        link = VGroup(*[Line(ring[k], ring[(k + 1) % 7], color=HEAD, stroke_width=4) for k in range(7)])
        cap1 = label(r"a complex: \ vertices, \ edges, \ triangles", font_size=19, color=GREY_A).next_to(
            tris, DOWN, buff=0.3)
        cap2 = label(r"the link of the yellow vertex: \ a graph", font_size=19, color=HEAD).next_to(cap1, DOWN,
                                                                                               buff=0.15)
        side = VGroup(
            wrapped_label(r"\textbf{high-dimensional expander}: \ the whole complex is connected and every vertex's "
                          r"link is itself an expander graph", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"local-to-global \ (Garland 1973, \ sharpened since 2016): \ if every link expands "
                          r"enough, \ random walks on the triangles mix fast", 5.6, font_size=19, color=YES),
            wrapped_label(r"bounded-degree examples are not found at random: \ they are built from algebra \ "
                          r"(Ramanujan complexes, \ Lubotzky, \ Samuels and Vishne 2005)", 5.6, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.3 + DOWN * 0.2)
        with self.voiceover(
            "An expander is a graph in which every set of vertices has many edges leaving it. "
            "<bookmark mark='a'/> A high-dimensional expander asks the same of a complex: vertices, edges and "
            "triangles, glued together. <bookmark mark='b'/> Around each vertex, the triangles that touch it form a "
            "small graph called its link. <bookmark mark='c'/> A complex is a high-dimensional expander when it is "
            "connected and every link is itself an expander. <bookmark mark='d'/> The surprise is a local-to-global "
            "principle, going back to Howard Garland in 1973 and sharpened in the last decade: if every link "
            "expands enough, then random walks that move from triangle to triangle mix fast across the whole complex. "
            "<bookmark mark='e'/> Unlike ordinary expanders, bounded-degree examples are not found by drawing at "
            "random; the known constructions come from deep algebra."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tris], lag_ratio=0.15), FadeIn(cap1))
            vo.wait_until("b")
            self.play(FadeIn(centre), Create(link), FadeIn(cap2))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def results(self):
        head = label(r"What they have already done", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"counting by sampling", r"Anari, \ Liu, \ Oveis Gharan and Vinzant \ (2019): \ the bases of any "
                 r"matroid can be sampled by a fast-mixing walk; \ spectral independence \ (2020) \ extends it to "
                 r"spin systems", YES),
            tile(r"codes", r"2022: \ locally testable codes with constant rate, \ distance and locality \ (Dinur et "
                 r"al.; \ Panteleev and Kalachev), \ and good quantum LDPC codes \ (Part 53)", DATA),
            tile(r"proofs", r"Dinur's combinatorial proof of the PCP theorem \ (2006, \ Part 27) \ amplifies gaps with "
                 r"expanders; \ HDX are a route to stronger PCPs", LAM),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"in each, \ expansion turns a local check into a global guarantee", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In a few years high-dimensional expanders have settled old questions. <bookmark mark='a'/> In 2019 Nima "
            "Anari, Kuikui Liu, Shayan Oveis Gharan and Cynthia Vinzant proved that a simple random walk samples the "
            "bases of any matroid quickly, settling a conjecture of Mihail and Vazirani, and spectral independence "
            "then carried the method to models from statistical physics. <bookmark mark='b'/> In 2022 two groups "
            "built locally testable codes with constant rate, distance and locality, and good quantum low-density "
            "codes of the kind Part 53 needed. <bookmark mark='c'/> And Irit Dinur's proof of the PCP theorem, from "
            "Part 27, already amplified gaps with expanders; higher-dimensional ones are a route to stronger "
            "versions. <bookmark mark='d'/> In each case, expansion turns a local check into a global guarantee."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ramanujan(self):
        rows = load("regular")["rows"]
        head = label(r"How good can an expander be?", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[2, 13, 1], y_range=[0, 7.5, 1], x_length=7.5, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5).shift(
            LEFT * 2.2)
        xt = VGroup(*[label(rf"{d}", font_size=16, color=GREY_B).next_to(ax.c2p(d, 0), DOWN, buff=0.1)
                      for d in (3, 4, 6, 8, 12)])
        yt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(2, v), LEFT, buff=0.1)
                      for v in (0, 2, 4, 6)])
        xl = label(r"degree $d$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        curve = ax.plot(lambda d: 2 * math.sqrt(d - 1), x_range=[2.2, 13], color=YES, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(r["d"], r["lambda"]), radius=0.08, color=HEAD) for r in rows])
        key = VGroup(label(r"$2\sqrt{d-1}$: \ the Alon--Boppana bound", font_size=19, color=YES),
                     label(r"random $d$-regular graphs, \ 400 vertices", font_size=19, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.4).shift(UP * 1.0)
        side = wrapped_label(r"no infinite family can beat the bound; \ graphs that meet it are Ramanujan; \ "
                             r"Friedman \ (2008): \ random regular graphs come within any $\epsilon$; \ Marcus, \ "
                             r"Spielman and Srivastava \ (2015): \ bipartite Ramanujan graphs of every degree exist",
                             5.0, font_size=18, color=GREY_A).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        with self.voiceover(
            "How small can a regular graph's second eigenvalue be? <bookmark mark='a'/> Alon and Boppana showed it "
            "cannot go below two times the square root of d minus one, in the limit. Graphs that reach the bound are "
            "called Ramanujan graphs. <bookmark mark='b'/> Our random regular graphs from chapter five sit just "
            "under the curve, and Joel Friedman proved in 2008 that random regular graphs come within any margin of "
            "it. <bookmark mark='c'/> In 2015 Adam Marcus, Daniel Spielman and Nikhil Srivastava proved that "
            "bipartite Ramanujan graphs exist for every degree, with a new method, interlacing families of "
            "polynomials, that also solved the Kadison–Singer problem."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Explicit Ramanujan graphs}: \ simple constructions for every degree, \ not "
                          r"just bipartite or prime-power ones.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Lossless expanders}: \ explicit graphs whose small sets expand by almost the "
                          r"full degree.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Faster flows in practice}: \ almost-linear max-flow is a theorem; \ "
                          r"practical solvers still use older methods.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Sparsest cut}: \ the best approximation ratio in polynomial time \ "
                          r"(Arora, \ Rao and Vazirani: \ $O(\sqrt{\log n})$).", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ prove or refute the small-set expansion "
                             r"hypothesis \ (Raghavendra and Steurer, \ 2010): \ that telling whether small sets "
                             r"expand is hard, \ which would imply the unique games conjecture", 12.4,
                             font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Simple explicit Ramanujan graphs for every degree. "
            "<bookmark mark='b'/> Explicit expanders in which small sets grow by almost the full degree. "
            "<bookmark mark='c'/> Turning almost-linear maximum flow from a theorem into practical software. "
            "<bookmark mark='d'/> And the best approximation for the sparsest cut, where the square-root-log bound of "
            "Arora, Rao and Vazirani still stands. <bookmark mark='e'/> This part's research problem is the "
            "small-set expansion hypothesis of Raghavendra and Steurer: that telling whether small sets in a graph "
            "expand is computationally hard. It would imply the unique games conjecture of Part 23, and nobody knows "
            "whether it is true."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
