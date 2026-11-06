from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, words)


class Bounds(VoiceoverScene):
    def construct(self):
        self.card()
        self.plane()
        self.golay()

    def card(self):
        card = chapter_card(4, r"How good can a code be?", r"How much rate must each unit of distance cost?",
                            lit=(1949, 1977), extra=((1949, r"Golay"), (1957, r"Gilbert--Varshamov"),
                                                     (1977, r"MRRW")), part=PART)
        with self.voiceover("Chapter four. How good can a code be?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def plane(self):
        b = load("bounds")
        head = label(r"The rate--distance plane", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 0.52, 0.1], y_range=[0, 1.02, 0.25], x_length=6.2, y_length=4.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(f"{x:g}", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0.1, 0.2, 0.3, 0.4, 0.5)])
        yt = VGroup(*[label(f"{y:g}", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0.25, 0.5, 0.75, 1.0)])
        xl = label(r"relative distance $\delta = d/n$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"rate $R = k/n$", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
        ds = b["delta"]

        def curve(name, color, width=3):
            pts = [ax.c2p(d, v) for d, v in zip(ds, b["curves"][name]) if d <= 0.5]
            return VMobject(color=color, stroke_width=width).set_points_as_corners(pts)
        sing = curve("singleton", GREY_B, 2)
        ham = curve("hamming", HEAD)
        mrrw = curve("mrrw", NO)
        gv = curve("gv", YES)
        best = [min(h, m) for h, m in zip(b["curves"]["hamming"], b["curves"]["mrrw"])]
        band = Polygon(*[ax.c2p(d, u) for d, u in zip(ds, best) if d <= 0.5],
                       *[ax.c2p(d, g) for d, g in reversed(list(zip(ds, b["curves"]["gv"]))) if d <= 0.5],
                       stroke_width=0, fill_color=LAM, fill_opacity=0.25)
        keys = VGroup(label(r"Singleton: \ $R \le 1 - \delta$", font_size=17, color=GREY_B),
                      label(r"Hamming: \ balls must fit", font_size=17, color=HEAD),
                      label(r"linear programming \ (MRRW)", font_size=17, color=NO),
                      label(r"Gilbert--Varshamov: \ achievable", font_size=17, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.c2p(0.36, 0.86))
        pts = VGroup()
        for p in b["points"]:
            if p["delta"] > 0.5:
                continue
            d = Dot(ax.c2p(p["delta"], p["R"]), radius=0.07, color=DATA)
            pts.add(VGroup(d, label(p["name"], font_size=14, color=DATA).next_to(d, RIGHT, buff=0.08)))
        notes = VGroup(
            label(r"long codes: \ correct a fraction $\delta/2$ of errors \\ at rate $R$", font_size=20, color=WHITE),
            label(r"upper bounds: \ no code lies above them", font_size=20, color=NO),
            label(r"Gilbert \ (1952), \ Varshamov \ (1957): \\ \textbf{random} codes reach $1 - H(\delta)$",
                  font_size=20, color=YES),
            label(r"the shaded gap has been open \\ for almost 70 years", font_size=20, color=LAM),
            label(r"binary codes beating GV \\ for long lengths: \ unknown", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Every code trades rate for distance. <bookmark mark='a'/> For long codes, plot the rate against the "
            "relative distance, the minimum distance divided by the length: a code at delta corrects a fraction "
            "delta over two of errors. <bookmark mark='b'/> Some limits are easy. The Singleton bound: rate plus "
            "relative distance is at most one. Hamming's bound: the balls around codewords must fit in the space. "
            "And the linear-programming bound of McEliece, Rodemich, Rumsey and Welch, which is the best known for "
            "large distances. No code lies above the lowest of them. <bookmark mark='c'/> From below, Edgar Gilbert "
            "and Rom Varshamov showed that random codes reach one minus the entropy of delta. <bookmark mark='d'/> "
            "Between the two lies a gap, and it has been open for nearly seventy years. <bookmark mark='e'/> Nobody "
            "knows a family of long binary codes that beats random ones."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(sing), FadeIn(keys[0]))
            self.play(Create(ham), FadeIn(keys[1]))
            self.play(Create(mrrw), FadeIn(keys[2]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(gv), FadeIn(keys[3]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(band), FadeIn(pts), FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def golay(self):
        g = load("golay")
        head = label(r"A perfect code: \ Golay \ (1949)", font_size=34).to_edge(UP, buff=0.3)
        dist = {int(k): v for k, v in g["dist"].items()}
        vals = [dist.get(w, 0) for w in range(24)]
        bars = VGroup()
        top = max(vals)
        for w, v in enumerate(vals):
            h = 3.0 * v / top if v else 0.02
            r = Rectangle(width=0.2, height=max(h, 0.02), stroke_width=0, fill_color=DATA if v else GREY_D,
                          fill_opacity=0.9)
            r.move_to([-6.3 + 0.27 * w, -2.6 + h / 2, 0])
            bars.add(r)
        blabs = VGroup(*[label(words(v), font_size=13, color=WHITE).rotate(PI / 2).next_to(bars[w], UP, buff=0.08)
                         for w, v in enumerate(vals) if v])
        wl = VGroup(*[label(str(w), font_size=13, color=GREY_A).next_to(bars[w], DOWN, buff=0.08)
                      for w, v in enumerate(vals) if v])
        bl = label(r"codewords of each weight", font_size=17, color=GREY_A).next_to(VGroup(bars, wl), DOWN, buff=0.2)
        lines = VGroup(
            label(r"$g(x) = x^{11} + x^{10} + x^6 + x^5 + x^4 + x^2 + 1$: \\ 12 data bits, \ 23 bits sent", font_size=21,
                  color=WHITE),
            label(rf"we enumerated all {words(g['count'])} codewords: \\ minimum weight {g['dmin']}, \ so it corrects 3 "
                  r"errors", font_size=21, color=DATA),
            label(rf"each ball of radius 3 holds {words(g['ball'])} words; \\ $4{{,}}096 \times 2{{,}}048 = 2^{{23}}$: "
                  r"the balls tile the space", font_size=21, color=YES),
            label(r"the only perfect binary codes: \\ repetition, \ Hamming, \ and this one \ (Tiet\"av\"ainen, "
                  r"1973)", font_size=21, color=HEAD),
            label(r"Voyager 1 and 2 sent colour images \\ from Jupiter and Saturn with its extended form", font_size=21,
                  color=LAM),
            label(r"its 24-bit cousin builds the Leech lattice: \\ the densest packing in 24 dimensions \ (2017)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5)
        lines.next_to(bars, RIGHT, buff=0.6).align_to(lines, UP)
        fit_right(lines)
        with self.voiceover(
            "A few codes meet Hamming's bound exactly. <bookmark mark='a'/> In 1949 Marcel Golay published a code "
            "of length twenty-three carrying twelve bits, generated by this polynomial. <bookmark mark='b'/> We "
            "listed all four thousand and ninety-six codewords. The lightest nonzero one has weight seven, so the "
            "code corrects any three errors. <bookmark mark='c'/> A ball of radius three holds two thousand and "
            "forty-eight words, and four thousand and ninety-six such balls fill all two to the twenty-three words "
            "exactly. The code is perfect. <bookmark mark='d'/> Aimo Tietäväinen proved in 1973 that repetition "
            "codes, Hamming codes and this one are the only perfect binary codes. <bookmark mark='e'/> Its extended "
            "version carried Voyager's colour images of Jupiter and Saturn. <bookmark mark='f'/> And it builds the "
            "Leech lattice, which Henry Cohn and coauthors proved in 2017, building on Maryna Viazovska's method, is "
            "the densest way to pack spheres in twenty-four dimensions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.04), FadeIn(wl), FadeIn(bl),
                      run_time=2.0)
            self.play(FadeIn(blabs), FadeIn(lines[1]))
            for mk, ln in zip("cdef", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
