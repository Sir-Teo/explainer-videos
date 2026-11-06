from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, grid_table, load, mono, words)


class PointLocation(VoiceoverScene):
    def construct(self):
        self.card()
        self.slabs()
        self.trapezoids()

    def card(self):
        card = chapter_card(11, r"Point location", r"Which region of the map am I in?", lit=(1976, 1991),
                            extra=((1976, r"Dobkin--Lipton slabs"), (1991, r"Seidel's trapezoids")), part=PART)
        with self.voiceover("Chapter eleven. Point location."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _base(self, d):
        segs = [tuple(map(tuple, s)) for s in d["segs"]]
        box = [(-0.5, -1.5), (11.5, -1.5), (11.5, 7.5), (-0.5, 7.5)]
        f, s = fit(box, center=LEFT * 2.5 + DOWN * 0.4, w=8.0, h=5.6)
        frame = Polygon(*[f(p) for p in box], color=GREY_D, stroke_width=1.5)
        S = VGroup(*[Line(f(a), f(b), color=DATA, stroke_width=3.2) for a, b in segs])
        ends = VGroup(*[Dot(f(p), radius=0.06, color=HEAD) for s_ in segs for p in s_])
        return segs, f, frame, S, ends

    def slabs(self):
        d = load("pointloc")
        segs, f, frame, S, ends = self._base(d)
        head = label(r"Slabs: \ fast, \ but too big", font_size=34).to_edge(UP, buff=0.3)
        xs = sorted({p[0] for s in segs for p in s})
        sl = VGroup(*[DashedLine(f((x, -1.5)), f((x, 7.5)), color=GREY_B, stroke_width=1.2, dash_length=0.07)
                      for x in xs])
        q = (6.2, 3.3)
        qd = Dot(f(q), radius=0.09, color=NO)
        side = VGroup(
            label(r"a map is a subdivision by $n$ segments; \\ a query asks which face holds a point", font_size=21,
                  color=WHITE),
            label(r"draw a vertical line through every endpoint: \\ within a slab the segments don't cross, \\ so they "
                  r"are sorted", font_size=21, color=GREY_A),
            label(r"two binary searches: \ the slab, \ then the segment \\ below: \ $O(\log n)$", font_size=21,
                  color=YES),
            label(r"but each slab may store every segment: \\ $O(n^2)$ space \ (Dobkin and Lipton, 1976)", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 5.2:
            side.width = 5.2
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Your phone knows its coordinates; which country, which county, which time zone is it in? <bookmark "
            "mark='a'/> A map is a subdivision of the plane by n segments, and point location asks which face holds a "
            "query point. <bookmark mark='b'/> The first fast answer, by David Dobkin and Richard Lipton in 1976, "
            "draws a vertical line through every endpoint. Inside one slab no two segments cross, so they are "
            "sorted from bottom to top. <bookmark mark='c'/> A query is two binary searches: one for the slab, one "
            "for the segment just below the point. That is log n time. <bookmark mark='d'/> The trouble is space: "
            "a long segment crosses many slabs, and can be stored in every one, n squared in the worst case."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), LaggedStart(*[Create(x) for x in S], lag_ratio=0.15), FadeIn(ends))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(qd))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[Create(x) for x in sl], lag_ratio=0.05))
            vo.wait_until("c")
            k = sum(1 for x in xs if x < q[0])
            band = Rectangle(width=f((xs[k], 0))[0] - f((xs[k - 1], 0))[0], height=f((0, 7.5))[1] - f((0, -1.5))[1],
                             stroke_width=0).set_fill(YES, 0.15).move_to(
                [(f((xs[k], 0))[0] + f((xs[k - 1], 0))[0]) / 2, f((0, 3.0))[1], 0])
            self.play(FadeIn(side[2]), FadeIn(band), Indicate(qd, color=NO))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def trapezoids(self):
        d = load("pointloc")
        segs, f, frame, S, ends = self._base(d)
        head = label(r"The trapezoidal map", font_size=34).to_edge(UP, buff=0.3)
        W = VGroup(*[Line(f(a), f(b), color=LAM, stroke_width=1.6) for a, b in d["walls"]])
        n = len(segs)
        side = VGroup(
            label(r"from each endpoint, \ a wall up and down \\ only to the \textbf{nearest} segment", font_size=21,
                  color=LAM),
            label(rf"{n} segments: \ {d['trapezoids']} trapezoids $= 3n + 1$", font_size=21, color=YES),
            label(r"each trapezoid's left side comes from one endpoint: \\ a left end gives two, \ a right end one: \\ "
                  r"at most $2n + n + 1$", font_size=21, color=WHITE),
            label(r"random maps of 5, \ 20 and 80 segments: \\ " + ", \\ ".join(words(r["max"]) for r in d["rows"])
                  + r" \ trapezoids, \ every time", font_size=21, color=GREY_A),
            label(r"insert the segments in \textbf{random} order, \\ keeping a search structure of the splits:", font_size=21,
                  color=HEAD),
            label(r"expected $O(n)$ space, \ $O(\log n)$ query, \\ $O(n \log n)$ build \ (Mulmuley 1990; \ Seidel "
                  r"1991)", font_size=21, color=YES),
            label(r"backwards analysis, \ a third time; \\ Kirkpatrick (1983): \ the same bounds, \ deterministically",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        if side.width > 5.4:
            side.width = 5.4
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The fix is to stop the walls early. <bookmark mark='a'/> From each endpoint, draw a wall up and a wall "
            "down, but only as far as the nearest segment. The plane falls into trapezoids. <bookmark mark='b'/> "
            "These seven segments make twenty-two trapezoids, <bookmark mark='c'/> and that is no accident: every "
            "trapezoid's left side is fixed by one endpoint; a left endpoint can play that part for at most two "
            "trapezoids, and a right endpoint for one, so there are never more than three n plus one. On twenty random maps of five, twenty and eighty "
            "segments, every one hit the bound exactly. <bookmark mark='d'/> To query it fast, insert the segments "
            "in random order and keep a record of how each trapezoid was split, a search structure shaped like a "
            "directed acyclic graph. <bookmark mark='e'/> Ketan Mulmuley and Raimund Seidel showed that it has "
            "expected linear size and answers in logarithmic time. <bookmark mark='f'/> The proof is backwards "
            "analysis, a third time. David Kirkpatrick had reached the same bounds deterministically in 1983, with a "
            "hierarchy of ever coarser triangulations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(S), FadeIn(ends))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(w) for w in W], lag_ratio=0.08), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
            vo.wait_until("f")
            self.play(FadeIn(side[6]))
        self.wait(0.3)
        self.clear_scene()
