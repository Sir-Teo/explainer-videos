from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403
from videos.psychology.psych13.s09_cones import spectrum_strip, wl_axes


class Matching(VoiceoverScene):
    def construct(self):
        self.card()
        self.experiment()
        self.functions()
        self.metamers()
        self.diagram()

    def card(self):
        card = chapter_card(9, r"Colour matching as linear algebra", r"Why do three primaries suffice, \ and when do they "
                            r"not?", lit={1931: r"the standard observer", 1955: r"Stiles and Burch"}, part=PART,
                            scale=("mind",), marr=("what",))
        with self.voiceover("Chapter nine. Colour matching as linear algebra."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def experiment(self):
        d = load("matching")
        head = heading(r"The matching experiment")
        disc = VGroup(AnnularSector(inner_radius=0, outer_radius=1.5, angle=PI, start_angle=PI / 2, stroke_width=0,
                                    fill_color="#E8D44D", fill_opacity=1),
                      AnnularSector(inner_radius=0, outer_radius=1.5, angle=PI, start_angle=-PI / 2, stroke_width=0,
                                    fill_color="#E3D24F", fill_opacity=1),
                      Line(UP * 1.5, DOWN * 1.5, color=GREY_D, stroke_width=2)).move_to([-3.9, 0.4, 0])
        lt = label(r"test light", font_size=22, color=GREY_A).next_to(disc, LEFT, buff=0.15)
        lm = label(r"mixture", font_size=22, color=GREY_A).next_to(disc, RIGHT, buff=0.15)
        knobs = VGroup(*[VGroup(Circle(radius=0.22, color=c, stroke_width=3), label(n, font_size=20, color=c))
                         .arrange(DOWN, buff=0.08) for n, c in (("645 nm", LCONE), ("526 nm", MCONE), ("444 nm", SCONE))])
        knobs.arrange(RIGHT, buff=0.35).next_to(disc, DOWN, buff=0.45)
        w = d["w580"]
        w5 = d["w500"]
        eq1 = MathTex(r"P\,\mathbf{w} = \mathbf{c}_{\text{test}}", font_size=40).move_to([2.6, 2.0, 0])
        eq2 = MathTex(r"\mathbf{w} = P^{-1}\,\mathbf{c}_{\text{test}}", font_size=40).next_to(eq1, DOWN, buff=0.25)
        rows = rows_of([
            (r"turn three knobs until the two halves look identical", WHITE),
            (r"the columns of $P$: \ the cone excitations of the three primaries; \ $\mathbf{c}$: \ those of the test", GREY_A),
            (rf"580 nm (yellow): \ red {w[0]:.2f}, \ green {w[1]:.2f}, \ blue {w[2]:.2f}", LIGHT),
            (rf"500 nm (blue-green): \ red {w5[0]:.2f}: \ \emph{{negative}}. \ No mix matches it; \ add the red to the "
             rf"test side instead", LCONE),
        ], 5.6, 25, 0.3).move_to([3.0, -1.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the cones' 3-by-3 system, \ Stiles and Burch's primaries")
        with self.voiceover(
            "The matching experiment is simple. <bookmark mark='a'/> An observer looks at a disc split in two. One "
            "half shows a test light. The other shows a mixture of three fixed lights, primaries, here a red, a "
            "green and a blue at the wavelengths Stiles and Burch used. The observer turns three knobs until the "
            "halves look identical. <bookmark mark='b'/> In the cones' terms, the match happens when the mixture "
            "gives the same three numbers as the test. That's a system of three linear equations in three unknowns: "
            "the primaries' cone excitations times the amounts equals the test's. Invert the matrix, and you have "
            "the amounts. <bookmark mark='c'/> A yellow at five eighty: mostly red, some green, no blue. "
            "<bookmark mark='d'/> A blue-green at five hundred needs a negative amount of red. No mixture of the "
            "three matches it. What the observer can do is add red to the test side instead, and match that. "
            "Negative weights are real, and every set of three primaries needs them somewhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(disc), FadeIn(lt), FadeIn(lm), FadeIn(knobs), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq1), FadeIn(eq2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def functions(self):
        d = load("matching")
        head = heading(r"Predicted from the cones, \ measured in 1955")
        A = wl_axes([-2.6, -0.3, 0], y_length=4.0, x_length=7.0, ylabel=r"amount of each primary",
                    yr=(-0.6, 3.6), yt=(0, 1, 2, 3))
        ax = A.ax
        zero = DashedLine(ax.c2p(390, 0), ax.c2p(720, 0), color=GREY_D, stroke_width=1.5)
        cols = (LCONE, MCONE, SCONE)
        pred = VGroup(*[curve_in(ax, d["sb_wl"], d["derived"][:, j], c, stroke_width=4) for j, c in enumerate(cols)])
        data = VGroup(*[scatter(ax, d["sb_wl"][::2], d["sb"][::2, j], c, radius=0.05, opacity=1.0) for j, c in enumerate(cols)])
        r = d["r"]
        rows = rows_of([
            (r"solve the 3-by-3 system at every wavelength: \ three colour-matching functions", WHITE),
            (r"lines: \ predicted from today's cone curves; \ dots: \ ten observers' matches, \ Stiles and Burch, \ "
             r"1955", GREY_A),
            (rf"agreement: \ $r$ = {min(r):.4f} or better", MODEL),
            (r"(a consistency check, \ not an independent test: \ the cone curves were themselves derived partly from "
             r"matching data)", GREY_B),
        ], 4.6, 24, 0.27).move_to([4.3, -0.2, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(archive.COLOUR_TABLES.cite),
                      psyche_tag(r"computed: \ $P^{-1}$ times the cone curves"))
        with self.voiceover(
            "Do this at every wavelength, and you get three curves, called colour-matching functions: how much of "
            "each primary it takes to match each pure wavelength. <bookmark mark='a'/> The lines are computed from "
            "the cone curves of the last chapter, with one three-by-three inverse. <bookmark mark='b'/> The dots are "
            "real matches: ten observers in W. S. Stiles and J. M. Burch's laboratory in 1955, with exactly these "
            "primaries. Notice the red curve dipping below zero between the blue and green primaries. "
            "<bookmark mark='c'/> The agreement is a correlation of point nine nine nine or better for every curve. "
            "<bookmark mark='d'/> It's a consistency check, not an independent test, because today's cone curves were "
            "themselves partly derived from matches like these. But it shows the whole of colour matching follows "
            "from three curves and one matrix inverse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tags), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in pred], lag_ratio=0.3), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in data], lag_ratio=0.3), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def metamers(self):
        d = load("matching")
        head = heading(r"Metamers: \ the null space, \ made visible")
        A = wl_axes([-3.0, 0.3, 0], y_length=3.4, x_length=6.4, ylabel=r"spectral power", yr=(0, 1.0), yt=(0, 0.5, 1))
        ax = A.ax
        wl = d["wl"]
        m = max(float(d["base"].max()), float(d["twin"].max()))
        a = curve_in(ax, wl, d["base"] / m, LIGHT, stroke_width=4)
        b = curve_in(ax, wl, d["twin"] / m, CELL, stroke_width=4)
        sa = swatch(d["rgb_base"], 1.5).move_to([3.0, 1.4, 0])
        sb = swatch(d["rgb_twin"], 1.5).next_to(sa, RIGHT, buff=0.0)
        la = label(r"spectrum A", font_size=22, color=LIGHT).next_to(sa, UP, buff=0.12)
        lb = label(r"spectrum B", font_size=22, color=CELL).next_to(sb, UP, buff=0.12)
        ua = d["under_a"]
        rows = rows_of([
            (r"B is A plus a wiggle that every cone sums to zero: \ a vector in the null space of the 3-by-79 matrix", WHITE),
            (r"different spectra, \ identical cone excitations, \ identical colour: \ metamers", CELL),
            (r"the null space has 76 dimensions: \ every colour you see stands for a vast family of different lights", GREY_A),
            (rf"change the light to a warm lamp and the match breaks: \ S differs by {abs(1 - ua[2]) * 100:.0f}\%, \ "
             rf"M by {abs(1 - ua[1]) * 100:.0f}\%", LCONE),
        ], 5.6, 24, 0.28).move_to([3.6, -1.6, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ a null-space metamer")
        with self.voiceover(
            "Now the linear algebra pays off. <bookmark mark='a'/> Take a spectrum, A. Add to it a wiggle chosen so "
            "that every cone type sums it to exactly zero: in the jargon, a vector in the null space of the cone "
            "matrix. The result, B, is a genuinely different light. <bookmark mark='b'/> But all three cone "
            "excitations are identical, so the two look identical. They're called metamers. <bookmark mark='c'/> The "
            "cone matrix has seventy-nine columns and only three rows, so its null space has seventy-six "
            "dimensions. Every colour you see stands for an enormous family of physically different lights. "
            "<bookmark mark='d'/> Metamers only match under the light they were matched in. Multiply both by the "
            "spectrum of a warm incandescent lamp, and the match breaks. This is why a jacket and trousers can match "
            "in the shop and differ in the street."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(a), FadeIn(sa), FadeIn(la))
            vo.wait_until("a")
            self.play(Create(b), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sb), FadeIn(lb), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def diagram(self):
        d = load("matching")
        head = heading(r"Every colour on one page: \ the 1931 chromaticity diagram")
        A = axes([0, 0.8], [0, 0.9], x_length=5.0, y_length=5.6, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 xlabel=r"$x$", ylabel=r"$y$", center=[-3.6, -0.4, 0])
        ax = A.ax
        loc = d["locus"]
        pts = [ax.c2p(float(x), float(y)) for x, y in loc]
        locus = Polygon(*pts, color=WHITE, stroke_width=3, fill_opacity=0.0)
        from explainer.psychology.psyche import vision as V
        fills = VGroup()
        for (x, y), w in zip(loc[::3], d["locus_nm"][::3]):
            c = V.srgb(V.to_xyz(V.monochromatic(float(w))), None)
            fills.add(Dot(ax.c2p(float(x), float(y)), radius=0.07, color=ManimColor.from_rgb(np.clip(c, 0, 1))))
        tri = Polygon(*[ax.c2p(float(x), float(y)) for x, y in d["srgb_xy"]], color=LIGHT, stroke_width=3,
                      fill_color=LIGHT, fill_opacity=0.12)
        wp = Dot(ax.c2p(*map(float, d["white"])), radius=0.06, color=WHITE)
        nm = VGroup(*[label(rf"{int(w)}", font_size=18, color=GREY_B).next_to(ax.c2p(float(x), float(y)), LEFT if x < 0.3 else RIGHT, buff=0.08)
                      for (x, y), w in zip(loc, d["locus_nm"]) if int(w) in (460, 500, 520, 560, 600)])
        rows = rows_of([
            (r"1931: \ the CIE fixed a standard observer from Wright's and Guild's matches, \ seventeen observers in "
             r"all; \ every display, \ camera and paint standard is built on it", WHITE),
            (r"divide out brightness, \ and every colour is a point; \ pure wavelengths trace the horseshoe", GREY_A),
            (r"mixtures of two lights lie on the line between them; \ of three, \ inside their triangle", LIGHT),
            (r"a screen's three primaries make a triangle: \ it cannot show the colours outside it, \ \ which is why no "
             r"screen shows a true spectral blue-green", CENTRE),
        ], 6.4, 24, 0.3).move_to([3.3, -0.3, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.COLOUR_TABLES.cite, corner=DR)
        with self.voiceover(
            "In 1931 the International Commission on Illumination turned this into a standard. <bookmark mark='a'/> "
            "From matches made by William Wright and John Guild, seventeen observers in all, it fixed a standard "
            "observer: three colour-matching functions that every display, camera, printer and paint chart is still "
            "built on. <bookmark mark='b'/> Divide out overall brightness, and every colour becomes a point on a "
            "page. The pure wavelengths trace this horseshoe. <bookmark mark='c'/> Because matching is linear, a "
            "mixture of two lights lies on the straight line between them, and a mixture of three lies inside their "
            "triangle. <bookmark mark='d'/> A screen has three primaries, so it can only show the colours inside its "
            "triangle. Everything outside, including the vivid blue-greens of pure spectral light, it simply cannot "
            "show. Three primaries suffice to match any colour, but only if some amounts are allowed to be negative, "
            "which a screen cannot do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(locus), FadeIn(fills), FadeIn(nm), FadeIn(wp), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(tri), FadeIn(rows[3]))
        self.clear_scene()
