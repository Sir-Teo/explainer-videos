from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Optics(VoiceoverScene):
    def construct(self):
        self.card()
        self.mtf()
        self.mosaic()

    def card(self):
        card = chapter_card(2, r"Optics and the mosaic", r"What limits the finest detail you can see?",
                            lit=(), part=PART, scale=("molecule",), marr=("how",))
        with self.voiceover("Chapter two. Optics, and the mosaic."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mtf(self):
        d = load("optics")
        head = heading(r"How much contrast survives the lens")
        A = axes([0, 100], [0, 1], x_length=6.4, y_length=3.8, xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 0.5, 1],
                 xlabel=r"grating frequency (cycles per degree)", ylabel=r"contrast passed", center=[-3.0, -0.4, 0])
        ax = A.ax
        f = d["f"]
        cols = {"2.0": GREY_B, "3.0": LIGHT, "6.0": "#F2A65A"}
        diff = VGroup(*[curve(ax, f, d["mtf"][k], c, stroke_width=3.5) for k, c in cols.items()])
        eye = curve(ax, f, d["eye"], MODEL, stroke_width=5)
        lg = legend([(GREY_B, r"2 mm pupil, \ perfect optics"), (LIGHT, r"3 mm, \ perfect"), ("#F2A65A", r"6 mm, \ perfect"),
                     (MODEL, r"3 mm, \ with the eye's blur")], font_size=19).move_to(ax.c2p(78, 0.9))
        rows = rows_of([
            (r"a grating of black and white bars, \ imaged by the eye: \ the finer the bars, \ the more contrast "
             r"the optics wash out", WHITE),
            (rf"diffraction alone stops everything above pupil $\div$ wavelength: \ {d['cutoff']:.0f} cycles per "
             rf"degree for a 3 mm pupil", LIGHT),
            (r"a wider pupil could pass finer detail, \ but a real eye's aberrations grow with it", "#F2A65A"),
            (r"the eye's blur, \ modelled: \ almost nothing left by 60 cycles per degree", MODEL),
        ], 5.2, 25, 0.3).move_to([3.9, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ diffraction, \ plus a Gaussian blur standing in for aberrations")
        with self.voiceover(
            "Before light reaches a single receptor, it passes through the eye's optics, and they set the first "
            "limit. <bookmark mark='a'/> Image a grating of fine bars through a lens and some of its contrast is "
            "lost; the finer the bars, the more is lost. This curve, the modulation transfer function, says how "
            "much survives at each spatial frequency, counted in cycles of the grating per degree of visual angle. "
            "<bookmark mark='b'/> Even perfect optics can't beat diffraction: through a pupil three millimetres "
            "across, nothing finer than about ninety-four cycles per degree gets through. <bookmark mark='c'/> A "
            "wider pupil would pass finer detail in principle, but a real eye's flaws, its aberrations, grow as the "
            "pupil opens. <bookmark mark='d'/> Add a blur standing in for those flaws, and by sixty cycles per "
            "degree almost nothing is left."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(diff[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(diff[0]), Create(diff[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(eye), FadeIn(lg), FadeIn(rows[3]))
        self.clear_scene()

    def mosaic(self):
        d = load("optics")
        head = heading(r"A mosaic that samples the image")
        # a patch of the foveal mosaic: a hexagonal lattice
        cones = VGroup()
        sp = 0.32
        for r in range(-6, 7):
            for c in range(-7, 8):
                x = c * sp + (sp / 2 if r % 2 else 0)
                y = r * sp * np.sqrt(3) / 2
                if x * x + y * y < 2.0 ** 2:
                    cones.add(Circle(radius=sp * 0.45, stroke_width=1.5, color=[LCONE, MCONE, LCONE, MCONE, SCONE][(r * 3 + c) % 5],
                                     fill_opacity=0.35).move_to([x, y, 0]))
        cones.move_to([-4.3, 0.6, 0])
        cap = label(r"cones about half a minute of arc apart", font_size=22, color=GREY_A).next_to(cones, DOWN, buff=0.2)
        A = axes([0, 0.05], [-1.3, 1.3], x_length=6.4, y_length=2.0, xticks=[0, 0.025, 0.05], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v * 60:g}'", xlabel=r"position (minutes of arc)", ylabel=r"light", center=[2.6, 1.55, 0])
        ax = A.ax
        fine = curve(ax, d["xs"], d["fine"], GREY_B, stroke_width=2.5)
        samp = VGroup(*[Dot(ax.c2p(float(x), float(y)), radius=0.06, color=LIGHT) for x, y in zip(d["samples"], d["sampled"])])
        alias = curve(ax, d["xs"], d["alias"], LCONE, stroke_width=4)
        rows = rows_of([
            (rf"two cones per cycle at least: \ the finest grating the mosaic can carry is {d['nyquist']:.0f} cycles "
             rf"per degree", WHITE),
            (r"a finer grating, \ 80 cycles per degree (grey), \ sampled by cones 120 per degree (dots)...", GREY_A),
            (r"...looks exactly like a coarser one, \ 40 cycles per degree (red): \ aliasing, \ the moir\'e of a "
             r"striped shirt on television", LCONE),
            (r"the optics blur away nearly everything above 60: \ lens and mosaic are roughly matched", MODEL),
            (r"20/20 vision resolves detail of one minute of arc: \ about 30 cycles per degree; \ the best eyes "
             r"approach 60", LIGHT),
        ], 7.0, 23, 0.2)
        rows.next_to(A, DOWN, buff=0.3).align_to(A, LEFT)
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ a sampled grating", corner=DL)
        with self.voiceover(
            "Behind the optics, the image falls on a mosaic. <bookmark mark='a'/> At the centre of gaze the cones "
            "are packed about half a minute of arc apart. A mosaic can only carry a grating if it has at least two "
            "receptors per cycle, one for each bar, so the finest grating it can represent is about sixty cycles "
            "per degree. <bookmark mark='b'/> Present a finer one, eighty cycles per degree, to receptors sampling "
            "a hundred and twenty times per degree. <bookmark mark='c'/> The samples are exactly what a coarser "
            "grating, at forty, would give. The fine pattern masquerades as a coarse one. It's called aliasing, and "
            "it's why a striped shirt shimmers on television. <bookmark mark='d'/> But the eye's optics have already "
            "blurred away almost everything above sixty cycles per degree, so very little can alias. The lens and "
            "the mosaic are roughly matched, as in a well-designed camera. <bookmark mark='e'/> For scale: twenty "
            "twenty vision means resolving detail one minute of arc across, about thirty cycles per degree. The "
            "best young eyes come close to sixty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cones), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(fine), FadeIn(rows[1]))
            self.play(LaggedStart(*[FadeIn(s, scale=1.5) for s in samp], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(alias), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
