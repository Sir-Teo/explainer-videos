from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


def wl_axes(center, y_length=3.4, x_length=6.4, ylabel=r"relative sensitivity", yr=(0, 1.05), yt=(0, 0.5, 1)):
    return axes([390, 720], list(yr), x_length=x_length, y_length=y_length, xticks=[400, 450, 500, 550, 600, 650, 700],
                yticks=list(yt), xlabel=r"wavelength (nm)", ylabel=ylabel, center=center)


def spectrum_strip(width: float = 6.4, height: float = 0.25) -> VGroup:
    """The visible spectrum as a strip of colours (computed from the CIE functions)."""
    from explainer.psychology.psyche import vision as V
    wl = np.arange(395, 721, 5)
    cols = [V.srgb(V.to_xyz(V.monochromatic(float(w))), None) * min(1.0, 1.2 * float(V.to_xyz(V.monochromatic(float(w)))[1]
                                                                                        / V.XYZ[:, 1].max() * 3 + 0.25))
            for w in wl]
    w = width / len(wl)
    return VGroup(*[Rectangle(width=w, height=height, stroke_width=0, fill_color=ManimColor.from_rgb(np.clip(c, 0, 1)),
                              fill_opacity=1).move_to([i * w, 0, 0]) for i, c in enumerate(cols)])


class Cones(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.fundamentals()
        self.univariance()
        self.three()

    def card(self):
        card = chapter_card(8, r"Three numbers for a spectrum", r"What is colour, \ to an eye?",
                            lit={1802: r"Young", 1931: r"CIE"}, part=PART, scale=("molecule", "mind"), marr=("what",))
        with self.voiceover("Chapter eight. Three numbers for a spectrum."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def history(self):
        head = heading(r"From a prism to three receptors")
        rows = rows_of([
            (r"Newton, \ 1672: \ white light is a mixture; \ a prism spreads it into a spectrum, \ and the rays "
             r"themselves are not coloured", WHITE),
            (r"Young, \ 1802: \ the eye cannot have a receptor for every wavelength at every point; \ perhaps it has "
             r"three", LIGHT),
            (r"Maxwell and Helmholtz, \ 1850s: \ any colour can be matched by mixing three lights", CENTRE),
            (r"1983: \ the three cone pigments measured, \ cell by cell, \ in human retinas", MCONE),
        ], 12.2, 29, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Colour has a long history, and its central idea came from pure reasoning. <bookmark mark='a'/> Isaac "
            "Newton showed in 1672 that white light is a mixture, which a prism spreads into a spectrum. Later he "
            "insisted that the rays themselves are not coloured: colour is something the seeing does. "
            "<bookmark mark='b'/> In 1802 Thomas Young argued that the eye can't possibly have a separate receptor "
            "for every wavelength at every point of the retina. Perhaps, he guessed, it has three. "
            "<bookmark mark='c'/> In the eighteen-fifties James Clerk Maxwell and Hermann von Helmholtz turned the "
            "guess into an experiment: any colour can be matched by a mix of three lights. "
            "<bookmark mark='d'/> The receptors themselves weren't measured until the nineteen-sixties, and the "
            "three cone pigments of human retinas, one cell at a time, in 1983."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def fundamentals(self):
        d = load("cones")
        head = heading(r"Three cones, \ and the rods")
        A = wl_axes([-2.6, -0.2, 0], y_length=3.8, x_length=7.0)
        ax = A.ax
        wl = d["wl"]
        cols = (LCONE, MCONE, SCONE)
        cs = VGroup(*[curve_in(ax, wl, d["lms"][:, j], c, stroke_width=5) for j, c in enumerate(cols)])
        rod = DashedVMobject(curve_in(ax, wl, d["rod"], ROD, stroke_width=3), num_dashes=60)
        strip = spectrum_strip(7.0).next_to(ax, DOWN, buff=0.08).align_to(ax, LEFT)
        lg = legend([(LCONE, rf"L cones, \ peak {d['peaks'][0]:.0f} nm"), (MCONE, rf"M cones, \ peak {d['peaks'][1]:.0f} nm"),
                     (SCONE, rf"S cones, \ peak {d['peaks'][2]:.0f} nm"), (ROD, rf"rods, \ peak {d['rod_peak']:.0f} nm")],
                    font_size=22).move_to([4.4, 1.3, 0])
        rows = rows_of([
            (r"long, \ middle and short: \ the names are about wavelength, \ not colour; \ L and M overlap heavily", WHITE),
            (r"the rods have one pigment, \ which is why night vision has no colour", ROD),
        ], 4.8, 25, 0.3).move_to([4.4, -1.5, 0])
        tag = published_tag(archive.COLOUR_TABLES.cite)
        with self.voiceover(
            "Here are the three cone types, as measured by Andrew Stockman and Lindsay Sharpe in 2000, from people's "
            "colour matches and from the eyes of people missing one type. <bookmark mark='a'/> The long-wavelength "
            "cones peak near five hundred and seventy nanometres, the middle ones near five forty-five, and the short "
            "ones near four forty-five. The names are about wavelength, not colour: the long cones peak in what "
            "looks yellow-green, and the long and middle curves overlap heavily. <bookmark mark='b'/> The "
            "rods, dashed, have a single pigment, peaking near five hundred and five. With only one kind of rod, "
            "night vision has no colour at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(strip), FadeIn(tag))
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.4), FadeIn(lg[:3]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(rod), FadeIn(lg[3]), FadeIn(rows[1]))
        self.clear_scene()

    def univariance(self):
        d = load("cones")
        head = heading(r"One cone cannot see colour")
        A = wl_axes([-3.0, -0.2, 0], y_length=3.6, x_length=6.4)
        ax = A.ax
        wl = d["wl"]
        L = d["lms"][:, 0]
        cl = curve_in(ax, wl, L, LCONE, stroke_width=5)
        i540 = int(np.where(wl == 540)[0][0])
        i620 = int(np.where(wl == 620)[0][0])
        p1 = Line(ax.c2p(540, 0), ax.c2p(540, L[i540]), color=MCONE, stroke_width=6)
        p2 = Line(ax.c2p(620, 0), ax.c2p(620, L[i620]), color=LCONE, stroke_width=6)
        rows = rows_of([
            (r"a cone's pigment either catches a quantum or does not: \ its response says how many it caught, \ "
             r"nothing about their wavelength", WHITE),
            (rf"a 540 nm light and a 620 nm light {L[i540] / L[i620]:.1f} times brighter give an L cone the same "
             rf"catch", LCONE),
            (r"the principle of univariance: \ colour needs a comparison between cone types", LIGHT),
        ], 5.2, 26, 0.32).move_to([3.8, -0.2, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.COLOUR_TABLES.cite)
        with self.voiceover(
            "A single cone cannot see colour. <bookmark mark='a'/> Its pigment either catches a quantum or doesn't, "
            "and once it's caught, every quantum has the same effect. The cone's output says how many quanta it "
            "caught, and nothing about their wavelength. <bookmark mark='b'/> So a light at five forty, where the "
            "long cone is sensitive, and a light at six twenty, where it's less sensitive but made brighter by the "
            "right amount, give it exactly the same response. <bookmark mark='c'/> This is called the principle of "
            "univariance. Colour exists only in the comparison between cone types."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(p1), Create(p2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def three(self):
        d = load("cones")
        head = heading(r"A light is a spectrum; \ a colour is three numbers")
        A = wl_axes([-3.4, 0.4, 0], y_length=2.8, x_length=5.8, ylabel=r"light reaching the eye")
        ax = A.ax
        wl = d["wl"]
        light = d["light"] / d["light"].max()
        lc = curve_in(ax, wl, light, LIGHT, stroke_width=4)
        samples = VGroup(*[Line(ax.c2p(float(w), 0), ax.c2p(float(w), float(v)), color=LIGHT, stroke_width=1.5)
                           for w, v in zip(wl[::2], light[::2]) if w <= 720])
        n = d["n_samples"]
        eq = MathTex(r"\begin{pmatrix} L \\ M \\ S \end{pmatrix} = \sum_\lambda \begin{pmatrix} l(\lambda) \\ m(\lambda)"
                     r" \\ s(\lambda) \end{pmatrix} E(\lambda)", font_size=36).move_to([3.6, 1.0, 0])
        lms = d["light_lms"] / d["light_lms"].max()
        vals = MathTex(rf"= \begin{{pmatrix}} {lms[0]:.2f} \\ {lms[1]:.2f} \\ {lms[2]:.2f} \end{{pmatrix}}", font_size=36)
        vals.next_to(eq, RIGHT, buff=0.15)
        keep_in_frame(VGroup(eq, vals))
        rows = rows_of([
            (rf"a leaf in daylight, \ sampled every 5 nm: \ {n} numbers", LIGHT),
            (r"the eye keeps three: \ a 3-by-$N$ matrix times a vector", WHITE),
            (r"a projection from a space of many dimensions onto three: \ most of the information in the light is "
             r"thrown away, \ and lights that differ can land on the same three numbers", CENTRE),
        ], 12.2, 26, 0.26).to_edge(DOWN, buff=0.85)
        tag = psyche_tag(r"computed: \ daylight times a leaf's reflectance, \ through the cones")
        with self.voiceover(
            "So here's what colour is, to an eye. <bookmark mark='a'/> The light from a leaf in daylight is a "
            "spectrum: the power at every wavelength. Sampled every five nanometres across the visible range, that's "
            "seventy-nine numbers. <bookmark mark='b'/> The eye keeps three. Each cone type weights the spectrum by "
            "its sensitivity and adds it up, which is a three-by-seventy-nine matrix times a vector. "
            "<bookmark mark='c'/> In the language of linear algebra, it's a projection from a space of seventy-nine "
            "dimensions down to three. Almost all the information in the light is thrown away. And different lights "
            "can land on exactly the same three numbers. That's the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lc), FadeIn(samples), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(vals), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
