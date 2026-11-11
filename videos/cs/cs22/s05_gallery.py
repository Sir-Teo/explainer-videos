from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, load, mono, words)

THREE = [DATA, YES, HEAD]


class Gallery(VoiceoverScene):
    def construct(self):
        self.card()
        self.comb()
        self.fisk()
        self.cost()

    def card(self):
        card = chapter_card(4, r"Guarding an art gallery", r"How many guards does a polygon need?",
                            lit=(1975, 1978), extra=((1975, r"Chv\'atal"), (1978, r"Fisk's proof")), part=PART)
        with self.voiceover("Chapter four. Guarding an art gallery."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def comb(self):
        d = load("gallery")
        P = [tuple(p) for p in d["comb"]]
        f, _ = fit(P, center=LEFT * 2.4 + DOWN * 0.5, w=8.4, h=4.6)
        head = label(r"Chv\'atal's comb", font_size=34).to_edge(UP, buff=0.35)
        poly = Polygon(*[f(p) for p in P], color=DATA, stroke_width=3).set_fill(DATA, 0.12)
        tips = [p for p in P if p[1] == max(q[1] for q in P)]
        guards = VGroup(*[Star(n=5, outer_radius=0.16, inner_radius=0.07, color=HEAD, fill_opacity=1).move_to(
            f((t[0], 3.5))) for t in tips])
        views = VGroup()
        for t in tips:
            g = (t[0], 3.5)
            tri = Polygon(f(g), f((t[0] - 2, 2)), f(t), f((t[0] + 2, 2)), stroke_width=0).set_fill(HEAD, 0.25)
            views.add(tri)
        side = VGroup(
            label('Klee (1973): \\ a simple polygon without holes; \\\\ point guards see in every direction', font_size=23, color=WHITE),
            label(r"Chv\'atal (1975): \ $\lfloor n/3 \rfloor$ always suffice, \\ and sometimes are needed", font_size=23,
                  color=YES),
            label(rf"this comb has {len(P)} walls and {len(tips)} teeth: \\ no guard sees into two tips, \\ so it needs "
                  rf"{len(tips)} $= \lfloor {len(P)}/3 \rfloor$", font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        if side.width > 5.4:
            side.width = 5.4
            side.to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Klee's gallery is a simple polygon without holes. A point guard sees along every segment that stays inside it. <bookmark mark='a'/> Chvátal proved in 1975 that floor n over three guards always suffice, and some polygons require that many. <bookmark mark='b'/> This comb has seventeen walls and five separated teeth. No guard can see all the way into two tips, so it needs five guards, exactly the bound. The theorem concerns continuous point guards; camera direction, range and obstacles inside a room would define other problems."
        ) as vo:
            self.play(FadeIn(head), Create(poly), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), LaggedStart(*[FadeIn(v) for v in views], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(g, scale=1.5) for g in guards], lag_ratio=0.2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    def fisk(self):
        d = load("gallery")
        P = [tuple(p) for p in d["poly"]]
        tris = [tuple(t) for t in d["tris"]]
        col = d["col"]
        f, _ = fit(P, center=LEFT * 2.8 + DOWN * 0.35, w=6.6, h=5.8)
        head = label(r"Fisk's proof, \ in three colours", font_size=34).to_edge(UP, buff=0.3)
        poly = Polygon(*[f(p) for p in P], color=WHITE, stroke_width=3)
        diags = VGroup()
        seen = set()
        n = len(P)
        for t in tris:
            for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                e = (min(a, b), max(a, b))
                if e in seen or (e[1] - e[0]) % n in (1, n - 1):
                    continue
                seen.add(e)
                diags.add(Line(f(P[a]), f(P[b]), color=GREY_B, stroke_width=1.6))
        vdots = VGroup(*[Dot(f(p), radius=0.1, color=GREY_D) for p in P])
        coloured = [vdots[i].copy().set_color(THREE[col[i]]) for i in range(n)]
        counts = d["counts"]
        best = min(range(3), key=lambda c: counts[c])
        stars = VGroup(*[Star(n=5, outer_radius=0.2, inner_radius=0.09, color=THREE[best], fill_opacity=1).move_to(
            f(P[i])) for i in range(n) if col[i] == best])
        side = VGroup(
            label(r"1. \ triangulate the polygon \\ (every polygon has an \textbf{ear}: \ Meisters, \ 1975)",
                  font_size=21, color=WHITE),
            label(r"2. \ the triangles form a tree, \ so walking it \\ colours the corners with three colours, \\ every "
                  r"triangle getting all three", font_size=21, color=LAM),
            label(rf"3. \ the colours split the {n} corners {counts[0]} + {counts[1]} + {counts[2]}: \\ the smallest "
                  rf"class has at most $\lfloor n/3 \rfloor = {n // 3}$", font_size=21, color=YES),
            label(rf"4. \ put a guard on each of its {counts[best]} corners: \\ every triangle has one, \ and a triangle \\ "
                  r"is seen entirely from any corner", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Steve Fisk found a proof in 1978 that fits on a postcard. <bookmark mark='a'/> First triangulate the "
            "gallery with diagonals. That is always possible: Gary Meisters showed every polygon has an ear, three "
            "consecutive corners whose triangle lies inside, and cutting ears one by one triangulates it. <bookmark "
            "mark='b'/> The triangles, joined across diagonals, form a tree. Colour the corners of one triangle "
            "blue, green and yellow; each neighbouring triangle shares two coloured corners, so its third has only "
            "one colour left. Walking the tree colours every corner, and every triangle gets all three colours. "
            "<bookmark mark='c'/> Some colour is used at most n over three times. <bookmark mark='d'/> Put a guard "
            "on every corner of that colour. Each triangle has one, and a triangle is seen entirely from any of its "
            "corners, so the whole gallery is watched."
        ) as vo:
            self.play(FadeIn(head), Create(poly), FadeIn(vdots))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[Create(x) for x in diags], lag_ratio=0.08), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            order = []
            for t in tris:
                for i in t:
                    if i not in order:
                        order.append(i)
            self.play(LaggedStart(*[Transform(vdots[i], coloured[i]) for i in order], lag_ratio=0.12), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), LaggedStart(*[FadeIn(s, scale=1.6) for s in stars], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        d = load("gallery")
        rg = d["random_guards"]
        head = label(r"Triangulating, \ and finding the fewest guards", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(rf"rescanning ears: \ up to $O(n^3)$; \ 22-gon: {words(d['tests'])} candidate/containment tests", font_size=22,
                  color=WHITE),
            label(r"split into monotone pieces, \ then triangulate each by a stack: \ $O(n \log n)$ \ (Garey, \ "
                  r"Johnson, \ Preparata and Tarjan, \ 1978)", font_size=22, color=DATA),
            label('Chazelle (1991): \\ a theoretical $O(n)$ algorithm for simple polygons', font_size=22, color=LAM),
            label(rf"on 200 random {rg['n']}-gons, \ Fisk's smallest colour averaged {rg['mean']:.1f} guards, \ "
                  rf"against the bound of {rg['bound']}", font_size=22, color=YES),
            label(r"but the true minimum is \textbf{NP-hard} to find \ (Lee and Lin, 1986), \ and even "
                  r"$\exists\mathbb{R}$-complete \ (Abrahamsen, \ Adamaszek and Miltzow, \ 2018)", font_size=22,
                  color=NO),
            label('applications: \\ coverage with cameras and sensors, \\ polygon triangulation for graphics',
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "How fast can we triangulate a simple polygon without holes? <bookmark mark='a'/> Maintaining a set of valid ears gives a quadratic algorithm. Our short implementation repeatedly rescans candidates and containment points, and can take cubic time. The displayed count records candidate and containment tests, not every arithmetic operation. <bookmark mark='b'/> Splitting into monotone pieces, then using stacks, gives n log n time. <bookmark mark='c'/> Chazelle proved a linear-time bound in 1991; we have not implemented that algorithm. <bookmark mark='d'/> Our two hundred polygons, each with sixty vertices, all pass independent triangle, area and colouring checks. The smallest colour gives a valid guard set, usually smaller than the worst-case bound, without certifying a minimum. <bookmark mark='e'/> Finding a minimum continuous point-guard set is existential-real complete, hence NP-hard. This is a different task from Fisk's constructive guarantee. <bookmark mark='f'/> Coverage and triangulation motivate practical variants, whose geometric and visibility assumptions must be stated separately."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                if ln is not lines[0]:
                    self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
