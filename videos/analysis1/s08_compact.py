from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import endpoint, load
from videos.analysis1.s07_open_closed import blob_pts, nbhd


def cover_bar(a, b, y, X, color=C.OPEN_SET, sw=5, opacity=0.9):
    return VGroup(Line([X(a), y, 0], [X(b), y, 0], color=color, stroke_width=sw, stroke_opacity=opacity),
                  endpoint([X(a), y, 0], False, color, radius=0.05), endpoint([X(b), y, 0], False, color, radius=0.05))


class Compact(VoiceoverScene):
    def construct(self):
        self.card()
        self.finite()
        self.game()
        self.losers()
        self.closed()
        self.consequences()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Compactness", r"What is the next best thing to being finite?", part=1)
        with self.voiceover(
            "Chapter seven: compactness, the single most useful idea in this video, and the hardest to see the point "
            "of at first."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def finite(self):
        vals = [0.6, 1.4, 0.9, 2.1, 1.2, 0.4]
        xs = np.linspace(-5.6, -1.4, len(vals))
        bars = VGroup(*[Rectangle(width=0.45, height=v, stroke_width=0, fill_color=C.SEQ, fill_opacity=0.7)
                        .move_to([x, -1.5 + v / 2, 0]) for x, v in zip(xs, vals)])
        top = bars[3].copy().set_fill(C.EPS, 0.9)
        l1 = label(r"a function on a finite set\\has a largest value", font_size=28).next_to(bars, UP, buff=0.5)
        seq_vals = [0, 2, 1, 2, 0, 2, 2, 1, 2, 0, 2, 2]
        pts = VGroup(*[Dot([1.0 + 0.45 * i, -1.5 + 0.8 * v, 0], radius=0.08, color=C.EPS if v == 2 else C.SEQ)
                       for i, v in enumerate(seq_vals)])
        l2 = label(r"a sequence in a finite set\\repeats some value forever", font_size=28).next_to(pts, UP, buff=0.5)
        dots = MathTex(r"\cdots", font_size=36).next_to(pts, RIGHT, buff=0.2)
        quote = label(r"Compactness: the next best thing to being finite", font_size=32, color=C.COMPACT_SET)
        quote.to_edge(UP, buff=0.5)
        with self.voiceover(
            "Finite sets are pleasant. <bookmark mark='a'/> A function on a finite set always has a largest value: just "
            "check them all. <bookmark mark='b'/> And a sequence that stays inside a finite set has to repeat some value "
            "infinitely often. <bookmark mark='c'/> Infinite sets lose both properties, in general. Compactness is the "
            "property that brings them back; it's often called the next best thing to being finite."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(l1))
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=2) for p in pts], lag_ratio=0.1), FadeIn(dots), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def game(self):
        d = load("cover")
        a, b, chosen = d["a"], d["b"], [int(i) for i in d["chosen"]]
        X = lambda v: -5.6 + v * 11.2  # noqa: E731
        base_y = -2.6
        seg = VGroup(Line([X(0), base_y, 0], [X(1), base_y, 0], color=C.COMPACT_SET, stroke_width=7),
                     Dot([X(0), base_y, 0], radius=0.08, color=C.COMPACT_SET), Dot([X(1), base_y, 0], radius=0.08,
                                                                                     color=C.COMPACT_SET))
        ticks = VGroup(Text("0", font_size=24, color=GREY_B).move_to([X(0), base_y - 0.35, 0]),
                       Text("1", font_size=24, color=GREY_B).move_to([X(1), base_y - 0.35, 0]))
        defs = VGroup(
            label(r"An \textbf{open cover} of $K$: open sets $G_\alpha$ whose union contains $K$.", font_size=28),
            label(r"$K$ is \textbf{compact} if every open cover has a \emph{finite} subcover. \ (Rudin 2.31--2.32)",
                  font_size=28, color=C.COMPACT_SET),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        # stack the 70 intervals in rows without overlap
        order = np.argsort(a)
        rows_end = []
        ypos = {}
        for i in order:
            for r, e in enumerate(rows_end):
                if a[i] > e + 0.01:
                    rows_end[r] = b[i]
                    ypos[i] = r
                    break
            else:
                rows_end.append(b[i])
                ypos[i] = len(rows_end) - 1
        dy = 0.32
        bars = {i: cover_bar(max(a[i], -0.03), min(b[i], 1.03), base_y + 0.45 + dy * ypos[i], X) for i in range(len(a))}
        all_bars = VGroup(*[bars[i] for i in range(len(a))])
        with self.voiceover(
            "Here's the definition. <bookmark mark='c'/> An open cover of a set K is any collection of open sets whose "
            "union contains K. <bookmark mark='k'/> K is compact if every open cover has a finite subcover: finitely "
            "many of the sets already cover K. <bookmark mark='g'/> Think of it as a game. You cover K any way you like, "
            "with as many open sets as you like. <bookmark mark='m'/> Here's a random cover of the interval from zero to "
            "one by seventy little open intervals."
        ) as vo:
            self.play(FadeIn(seg), FadeIn(ticks))
            vo.wait_until("c")
            self.play(FadeIn(defs[0]))
            vo.wait_until("k")
            self.play(FadeIn(defs[1]))
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(bars[i], shift=DOWN * 0.3) for i in np.random.default_rng(1).permutation(len(a))],
                                  lag_ratio=0.03), run_time=3)
        walker = Dot([X(0), base_y, 0], radius=0.11, color=C.EPS)
        picked = VGroup()
        with self.voiceover(
            "My move is to throw away all but finitely many and still cover K. <bookmark mark='w'/> On this interval, "
            "here's a strategy: start at the left end, and take the interval containing that point that reaches "
            "furthest right. Jump to where it ends, and repeat. <bookmark mark='n'/> Nine intervals, out of seventy, and "
            "the whole interval is covered."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(walker, scale=2))
            for j in chosen:
                bar = bars[j]
                self.play(bar.animate.set_color(C.COMPACT_SET), run_time=0.35)
                picked.add(bar)
                self.play(walker.animate.move_to([X(min(b[j], 1.0)), base_y, 0]), run_time=0.45)
            vo.wait_until("n")
            rest = VGroup(*[bars[i] for i in range(len(a)) if i not in chosen])
            self.play(rest.animate.set_opacity(0.12))
        assert len(chosen) == 9
        claim = label(r"For $[0, 1]$ this always works. \ Why it can't get stuck is chapter 8.", font_size=28,
                      color=GREY_A).to_edge(UP, buff=1.45)
        self.play(FadeIn(claim))
        self.wait(1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def losers(self):
        X = lambda v: -5.6 + v * 11.2  # noqa: E731
        base_y = -2.4
        seg = VGroup(Line([X(0), base_y, 0], [X(1), base_y, 0], color=GREY_A, stroke_width=7),
                     endpoint([X(0), base_y, 0], False, GREY_A), endpoint([X(1), base_y, 0], False, GREY_A))
        lab = MathTex(r"(0, 1)", font_size=36).next_to(seg, DOWN, buff=0.3)
        cov = MathTex(r"G_n = \Big(\frac1n,\ 1\Big), \quad n = 2, 3, 4, \ldots", font_size=38, color=C.OPEN_SET)
        cov.to_edge(UP, buff=0.5)
        bars = VGroup(*[cover_bar(1 / n, 1.0, base_y + 0.4 + 0.3 * (n - 2), X) for n in range(2, 16)])
        with self.voiceover(
            "Not every set lets me win. <bookmark mark='a'/> Cover the open interval from zero to one by the intervals "
            "from one over n up to one. <bookmark mark='b'/> Together they cover everything, since every point x is bigger "
            "than one over n for large n. <bookmark mark='c'/> But any finitely many of them have a largest n, and they "
            "leave the gap from zero to one over that n uncovered."
        ) as vo:
            self.play(FadeIn(seg), FadeIn(lab))
            vo.wait_until("a")
            self.play(Write(cov))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.2) for b_ in bars], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("c")
            keep = VGroup(*bars[:5])
            self.play(VGroup(*bars[5:]).animate.set_opacity(0.1), keep.animate.set_color(C.COMPACT_SET))
            gap = Line([X(0), base_y, 0], [X(1 / 6), base_y, 0], color=C.PATHOLOGY, stroke_width=11)
            gap_l = label(r"uncovered: $(0, \tfrac16]$", font_size=28, color=C.PATHOLOGY).next_to(gap, DOWN, buff=0.55)
            self.play(Create(gap), FadeIn(gap_l))
        verdict = label(r"So $(0,1)$ is not compact. \ Neither is $\R$: \ cover it by $(-n, n)$.", font_size=30)
        verdict.next_to(cov, DOWN, buff=0.3)
        intr = label(r"Unlike openness, compactness belongs to the set itself, not the space around it \ (Rudin 2.33).",
                     font_size=26, color=GREY_A).next_to(verdict, DOWN, buff=0.25)
        with self.voiceover(
            "So the open interval is not compact. <bookmark mark='r'/> Neither is the whole real line: the intervals from "
            "minus n to n cover it, and finitely many of them are bounded. Notice the trouble in both cases: something "
            "escapes, either to a missing endpoint or off to infinity. <bookmark mark='i'/> And unlike openness, "
            "compactness doesn't depend on the surrounding space: Rudin proves it's a property of the set itself."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(verdict))
            vo.wait_until("i")
            self.play(FadeIn(intr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closed(self):
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.34)", font_size=28, color=GREY_A),
                      label(r"Compact subsets of a metric space are closed.", font_size=32)).arrange(DOWN, buff=0.12)
        stmt.to_edge(UP, buff=0.4)
        c0 = np.array([-4.3, -0.5, 0])
        pts = blob_pts(c0, scale=0.78)
        K = Polygon(*pts, stroke_color=C.COMPACT_SET, stroke_width=3, fill_color=C.COMPACT_SET, fill_opacity=0.25)
        Kl = MathTex(r"K", font_size=38, color=C.COMPACT_SET).move_to(c0 + np.array([-0.35, 0.3, 0]))
        p = np.array([-1.2, 0.35, 0])
        pd = Dot(p, radius=0.08, color=WHITE)
        pl = MathTex(r"p", font_size=36).next_to(pd, UR, buff=0.08)
        qs = [c0 + np.array(v) for v in ((0.9, 0.35, 0), (0.55, -0.6, 0), (-0.1, 0.75, 0), (-0.7, -0.35, 0), (0.15, -0.05, 0),
                                         (-0.95, 0.55, 0))]
        colors = [C.OPEN_SET, C.CONNECTED_SET, C.APPROX, C.SEQ, C.DELTA, C.EPS]
        W, V, Qd = VGroup(), VGroup(), VGroup()
        for q, col in zip(qs, colors):
            r = np.linalg.norm(p - q) / 2
            W.add(nbhd(q, r, color=col, fill=0.06, width=2, dashes=40))
            V.add(DashedVMobject(Circle(radius=r, color=col, stroke_width=2).move_to(p), num_dashes=40))
            Qd.add(Dot(q, radius=0.06, color=col))
        rmin = min(np.linalg.norm(p - q) for q in qs) / 2
        Vmin = nbhd(p, rmin, color=WHITE, fill=0.3, width=3)
        for q in qs:  # each pair of disks is disjoint
            r = np.linalg.norm(p - q) / 2
            assert np.linalg.norm(p - q) >= 2 * r - 1e-9
        txt = VGroup(
            label(r"1. for each $q \in K$: disks around $q$ and $p$", font_size=24),
            label(r"\quad of radius $\tfrac12 d(p,q)$: they cannot meet", font_size=24),
            label(r"2. the disks around the $q$'s cover $K$:", font_size=24),
            label(r"\quad keep finitely many", font_size=24),
            label(r"3. intersect the matching disks around $p$:", font_size=24),
            label(r"\quad still a disk, and it misses $K$", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.2, -0.6, 0])
        with self.voiceover(
            "Now three theorems that make compact sets useful. <bookmark mark='s'/> First, compact sets are closed. "
            "<bookmark mark='p'/> Take a point p outside a compact set K. <bookmark mark='q'/> For each point q of K, "
            "draw a disk around q and a disk around p, each with radius half the distance between them, so they can't "
            "overlap. <bookmark mark='c'/> The disks around the points of K cover K, so finitely many of them already do. "
            "<bookmark mark='i'/> Now intersect the matching finitely many disks around p. That intersection is still a "
            "disk around p, because there are only finitely many, and it misses all of K. So p is not a limit point of "
            "K, and K contains all of its limit points: it's closed."
        ) as vo:
            self.play(FadeIn(K), FadeIn(Kl))
            vo.wait_until("s")
            self.play(FadeIn(stmt))
            vo.wait_until("p")
            self.play(FadeIn(pd, scale=2), FadeIn(pl))
            vo.wait_until("q")
            self.play(FadeIn(Qd[0]), FadeIn(W[0]), Create(V[0]), FadeIn(txt[0:2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(Qd[i]), FadeIn(W[i]), Create(V[i])) for i in range(1, len(qs))],
                                  lag_ratio=0.3), FadeIn(txt[2:4]), run_time=2.4)
            vo.wait_until("i")
            self.play(FadeIn(Vmin), V.animate.set_stroke(opacity=0.3), FadeIn(txt[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consequences(self):
        t1 = VGroup(label(r"\textbf{Rudin 2.35} \ Closed subsets of compact sets are compact.", font_size=30),
                    label(r"(cover $F$; add the open set $F^c$; that covers all of $K$; keep finitely many)", font_size=24,
                          color=GREY_B)).arrange(DOWN, buff=0.12)
        t2 = VGroup(label(r"\textbf{Rudin 2.36} \ If $K_1 \supset K_2 \supset \cdots$ are nonempty and compact,", font_size=30),
                    label(r"then $\bigcap K_n \neq \emptyset$. \quad (Compare $\bigcap (0, \tfrac1n) = \emptyset$.)", font_size=30)
                    ).arrange(DOWN, buff=0.12)
        t3 = VGroup(label(r"\textbf{Rudin 2.37} \ Every infinite subset of a compact set $K$ has a limit point in $K$.",
                          font_size=30),
                    label(r"(otherwise each point of $K$ has a disk with at most one point of the subset;", font_size=24,
                          color=GREY_B),
                    label(r"finitely many disks cover $K$, so the subset is finite)", font_size=24, color=GREY_B)
                    ).arrange(DOWN, buff=0.12)
        grp = VGroup(t1, t2, t3).arrange(DOWN, buff=0.55).move_to(UP * 0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Second, a closed subset of a compact set is compact: given a cover of the subset, throw "
            "in the complement of the subset, an open set, to cover everything; keep finitely many; then drop the "
            "complement again. <bookmark mark='b'/> Third, nested compact sets can't shrink to nothing: if each one is "
            "nonempty and inside the last, something lies in all of them. Compare the open intervals from zero to one "
            "over n, which do shrink to nothing. <bookmark mark='c'/> And the one we'll use most: every infinite subset "
            "of a compact set has a limit point in the set. Otherwise every point would have a little disk containing "
            "at most one point of the subset, finitely many disks would cover everything, and the subset would be "
            "finite."
        ) as vo:
            for mk, t in zip("abc", grp):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
        moral = label(r"An infinite set inside a compact set cannot spread out without piling up somewhere.",
                      font_size=30, color=C.COMPACT_SET).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That last one is the finiteness we were after: <bookmark mark='m'/> inside a compact set, infinitely many "
            "points can't spread out without piling up somewhere. Which sets are compact? For subsets of the real line, "
            "and of k-dimensional space, there's a beautifully simple answer."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(moral))
        self.wait(0.5)
        self.clear_scene()
