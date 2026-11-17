from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Cortex(VoiceoverScene):
    def construct(self):
        self.card()
        self.bar()
        self.gabor()
        self.phase()
        self.hierarchy()

    def card(self):
        card = chapter_card(5, r"Edges in the cortex", r"What does the first stage of visual cortex look for?",
                            lit={1959: r"Hubel and Wiesel"}, part=PART, scale=("neuron", "circuit"), marr=("how", "what"))
        with self.voiceover("Chapter five. Edges in the cortex."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bar(self):
        d = load("cortex")
        head = heading(r"A cell that wants a line")
        A = axes([-5, 185], [0, 62], x_length=6.2, y_length=3.4, xticks=[0, 45, 90, 135, 180], yticks=[0, 25, 50],
                 xfmt=lambda v: f"{v:g}^\\circ", xlabel=r"orientation of the bar", ylabel=r"spikes per sweep",
                 center=[-3.0, -0.3, 0])
        ax = A.ax
        pts = scatter(ax, d["bar_th"], d["bar_mean"], CELL, radius=0.08)
        bars = VGroup()
        for t in d["bar_th"][::2]:
            r = Rectangle(width=0.08, height=0.55, stroke_width=0, fill_color=LIGHT, fill_opacity=0.9).rotate(-np.deg2rad(t))
            bars.add(r.move_to(ax.c2p(float(t) + 8, 56)))
        rows = rows_of([
            (r"1958: \ spots of light did little; \ the edge of a glass slide sliding into the projector made a cell "
             r"fire furiously", WHITE),
            (r"the cell wanted a line, \ at one orientation, \ in one place", CELL),
            (r"turn the bar away from that angle and the firing falls off", GREY_A),
            (r"neighbouring cells prefer neighbouring angles: \ every orientation is covered, \ at every point", LIGHT),
        ], 5.2, 26, 0.32).move_to([3.9, -0.2, 0])
        keep_in_frame(rows)
        tags = VGroup(historical_tag(archive.HUBEL_WIESEL_1959.cite), psyche_tag(r"simulated: \ one cell, \ ten sweeps "
                                                                                    r"per angle"))
        with self.voiceover(
            "In 1958, at Johns Hopkins, David Hubel and Torsten Wiesel were recording from single cells in the "
            "visual cortex of a cat, and getting nowhere with spots of light. <bookmark mark='a'/> The story, as they "
            "told it later, is that the cell burst into life as they slid a glass slide into the projector: not the "
            "spot on the slide, but the faint straight edge of the glass, sweeping across the screen. "
            "<bookmark mark='b'/> The cell wanted a line, at one particular orientation, in one particular place. "
            "<bookmark mark='c'/> Here's a simulated cell like theirs: sweep a bar across its field at each angle, "
            "and count spikes. Turn the bar away from the preferred angle, and the firing falls off. "
            "<bookmark mark='d'/> Neighbouring cells prefer neighbouring angles, so that at every point of the visual "
            "field, every orientation is covered. The work won them a share of the Nobel Prize in 1981."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.12), FadeIn(bars), FadeIn(rows[2]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def gabor(self):
        d = load("cortex")
        head = heading(r"A receptive field you can write down: \ the Gabor")
        ev = picture(d["rf_even"], 2.6, smooth=True, lo=-0.06, hi=0.06).move_to([-5.0, 1.0, 0])
        od = picture(d["rf_odd"], 2.6, smooth=True, lo=-0.06, hi=0.06).move_to([-2.2, 1.0, 0])
        le = label(r"even-symmetric", font_size=22, color=GREY_A).next_to(ev, DOWN, buff=0.12)
        lo_ = label(r"odd-symmetric", font_size=22, color=GREY_A).next_to(od, DOWN, buff=0.12)
        eq = MathTex(r"g(x, y) = e^{-(x^2 + y^2)/2\sigma^2}\,\cos\!\left(\tfrac{2\pi}{\lambda}\,x' + \phi\right)",
                     font_size=32).move_to([-3.6, -1.1, 0])
        A = axes([-90, 90], [0, 1.05], x_length=4.8, y_length=3.0, xticks=[-90, -45, 0, 45, 90], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}^\\circ", xlabel=r"grating orientation", ylabel=r"response", center=[3.4, 0.7, 0])
        ax = A.ax
        tc = curve(ax, d["th"], d["tune"], CELL, stroke_width=5)
        rows = rows_of([
            (r"light bars where the field is excited, \ dark where it is inhibited: \ a grating under a Gaussian", WHITE),
            (rf"its tuning: \ half the response {d['hw']:.0f}$^\circ$ from the preferred angle, \ in the range "
             rf"recorded in cats and monkeys", CELL),
        ], 6.0, 25, 0.28).move_to([3.4, -2.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ a Gabor filter, \ full-field gratings")
        with self.voiceover(
            "Like the retina's Mexican hat, these fields can be written down. <bookmark mark='a'/> The usual model "
            "is a Gabor function, named for the physicist Dennis Gabor: a striped grating seen through a Gaussian "
            "window. Light stripes where light excites the cell, dark where it inhibits. The even version has a "
            "bright bar down its middle; the odd one has an edge. <bookmark mark='b'/> Show it gratings at every "
            "orientation, and its response falls to half about twenty degrees either side of the preferred angle, "
            "which is about what's recorded in real cells."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ev), FadeIn(od), FadeIn(le), FadeIn(lo_), FadeIn(eq), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(tc), FadeIn(rows[1]))
        self.clear_scene()

    def phase(self):
        d = load("cortex")
        head = heading(r"Simple cells and complex cells")
        A = axes([0, 360], [0, 1.1], x_length=6.4, y_length=3.4, xticks=[0, 90, 180, 270, 360], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}^\\circ", xlabel=r"where the grating's bars fall (phase)", ylabel=r"response",
                 center=[-3.0, -0.3, 0])
        ax = A.ax
        s = curve(ax, d["phase"], d["simple"], CENTRE, stroke_width=4)
        c = curve(ax, d["phase"], d["complex"], CELL, stroke_width=5)
        lg = legend([(CENTRE, r"simple: \ one Gabor, \ rectified"), (CELL, r"complex: \ even$^2$ + odd$^2$")],
                    font_size=21).move_to(ax.c2p(180, 0.5))
        rows = rows_of([
            (r"Hubel and Wiesel, \ 1962: \ simple cells care exactly where the bars fall", CENTRE),
            (r"complex cells respond to the right orientation anywhere in their field", CELL),
            (r"the energy model: \ square and add an even and an odd filter; \ $\cos^2 + \sin^2 = 1$, \ so position "
             r"drops out", WHITE),
            (r"a small step toward recognizing a shape wherever it is", GREY_A),
        ], 5.2, 26, 0.32).move_to([3.9, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the energy model (Adelson and Bergen 1985)")
        with self.voiceover(
            "In 1962 Hubel and Wiesel sorted these cells into two kinds. <bookmark mark='a'/> Simple cells care "
            "exactly where the bars fall. Slide the same grating sideways and the response swings from full to "
            "nothing, as a single Gabor followed by a threshold would. <bookmark mark='b'/> Complex cells respond to "
            "the right orientation anywhere in their field. <bookmark mark='c'/> A model that does this is called "
            "the energy model: take an even and an odd filter, square each response and add them. Because cosine "
            "squared plus sine squared is one, the position of the bars drops out, and only orientation and "
            "contrast remain. <bookmark mark='d'/> It's a small first step toward recognizing a shape wherever it "
            "appears, which is the problem of Part 14."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(s), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(lg), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def hierarchy(self):
        head = heading(r"A first hierarchy")
        boxes = chain_boxes([(r"receptors: \ light at a point", LIGHT), (r"ganglion cells: \ centre minus surround", CENTRE),
                             (r"simple cells: \ aligned centres make a bar", CENTRE), (r"complex cells: \ simple cells "
                                                                                     r"pooled over position", CELL)])
        boxes.move_to([0, 1.2, 0])
        rows = rows_of([
            (r"Hubel and Wiesel's proposal: \ a simple cell's field is a row of centre-surround fields, \ lined up", WHITE),
            (r"1995: \ paired recordings found thalamic cells connected to the simple cells whose subregions they "
             r"overlapped, \ of the same sign (Reid and Alonso)", CENTRE),
            (r"as a first approximation it holds; \ it is also the first two layers of every convolutional network "
             r"(\emph{AI, Built})", LIGHT),
        ], 12.4, 27, 0.32).move_to([0, -1.6, 0])
        with self.voiceover(
            "Put the pieces together and you get a hierarchy, the first in the study of the brain. "
            "<bookmark mark='a'/> Hubel and Wiesel proposed that a simple cell's elongated field is built from a row "
            "of centre-surround fields, lined up along a line. <bookmark mark='b'/> It took until 1995 to check it "
            "directly. Clay Reid and Jose-Manuel Alonso recorded from pairs of cells, one in the thalamus and one in "
            "the cortex, and found connections where the thalamic cell's centre overlapped a matching part of the "
            "simple cell's field. <bookmark mark='c'/> As a first approximation, the hierarchy holds. It's also, "
            "near enough, the first two layers of every convolutional neural network, as the series AI, Built "
            "shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()


def chain_boxes(items, width: float = 12.6, font_size: int = 24, height: float = 1.1) -> VGroup:
    n = len(items)
    w = (width - 0.45 * (n - 1)) / n
    boxes = VGroup()
    for name, col in items:
        box = RoundedRectangle(width=w, height=height, corner_radius=0.12, color=col, stroke_width=2.5, fill_color=col,
                               fill_opacity=0.1)
        boxes.add(VGroup(box, wrapped_label(name, w - 0.2, font_size, col).move_to(box)))
    boxes.arrange(RIGHT, buff=0.45)
    arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, color=GREY_B, stroke_width=3,
                            max_tip_length_to_length_ratio=0.45) for i in range(n - 1)])
    return VGroup(boxes, arrows)
