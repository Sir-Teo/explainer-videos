from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Mri(VoiceoverScene):
    def construct(self):
        self.card()
        self.spins()
        self.relax()
        self.kspace()

    def card(self):
        card = chapter_card(4, r"MRI in five minutes", r"How does a magnet take a picture?", lit=(), part=PART,
                            scale=("molecule", "brain"), marr=("tissue",))
        with self.voiceover(
            "Chapter four. MRI in five minutes."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def spins(self):
        head = heading(r"Step 1: \ line up the protons, \ then knock them over")
        g = np.random.default_rng(4)

        def protons(center, aligned):
            c = np.asarray(center, float)
            out = VGroup()
            for i in range(5):
                for j in range(3):
                    a = PI / 2 + (g.normal(0, 0.25) if aligned else g.uniform(0, TAU))
                    p = c + np.array([(i - 2) * 0.62, (j - 1) * 0.62, 0])
                    d = 0.2 * np.array([np.cos(a), np.sin(a), 0])
                    out.add(VGroup(Circle(radius=0.2, color=GREY_D, stroke_width=1.5).move_to(p),
                                   Arrow(p - d, p + d, buff=0, color=BLOOD, stroke_width=3,
                                         max_tip_length_to_length_ratio=0.45)))
            return out

        a = protons([-3.9, 1.15, 0], False)
        b = protons([-3.9, -1.85, 0], True)
        al = keep_in_frame(label(r"protons in water: \ pointing anywhere", font_size=27, color=GREY_A).next_to(a, UP, buff=0.12))
        bl = keep_in_frame(label(r"in the field: \ a slight majority line up", font_size=27, color=BLOOD).next_to(b, UP, buff=0.12))
        field = Arrow([-6.2, -2.75, 0], [-6.2, -0.95, 0], buff=0, color=THRESH, stroke_width=5)
        field_l = label(r"$B_0$", font_size=30, color=THRESH).next_to(field, LEFT, buff=0.08)
        rows = rows_of([
            (r"your body is mostly water; \ each hydrogen nucleus is a small magnet", WHITE),
            (r"the scanner's field: \ 3 tesla, \ about 60{,}000 times the Earth's", THRESH),
            (r"in it the protons wobble at a set rate: \ 128 million times a second at 3 tesla", WHITE),
            (r"a radio pulse at exactly that rate tips them over; \ as they recover, \ they give a radio "
             r"signal back", BLOOD),
        ], 5.9, 29, 0.3).move_to([3.7, -0.3, 0])
        keep_in_frame(rows)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        steps = VGroup(*[
            VGroup(label(str(i + 1), font_size=44, color=c), wrapped_label(t, 9.0, 32, c)).arrange(RIGHT, buff=0.45)
            for i, (t, c) in enumerate(((r"line up the protons, \ then knock them over", BLOOD),
                                        (r"how fast they recover depends on the tissue", VOLT),
                                        (r"the scanner measures the picture's Fourier transform", THRESH)))
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, -0.2, 0])
        with self.voiceover(
            "The other instrument uses a magnet, and you need to know just enough of how it works to know "
            "what its pictures are pictures of. Three steps. <bookmark mark='a'/> One. Your body is mostly "
            "water, and the nucleus of every hydrogen atom in it, a single proton, is a tiny magnet. "
            "Normally they point in all directions and cancel. <bookmark mark='b'/> Put a person in a "
            "strong field, sixty thousand times the Earth's, and a slight majority of the protons line up "
            "with it. <bookmark mark='c'/> They don't sit still. Each one wobbles around the field, like a "
            "spinning top, at a rate set by the field's strength. At three tesla, that's about a hundred "
            "and twenty-eight million times a second, a radio frequency. <bookmark mark='d'/> So send in a "
            "radio pulse at exactly that frequency. It tips the protons over. Switch it off, and as they "
            "swing back into line they broadcast a faint radio signal of their own. That signal is all the "
            "scanner ever hears."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(steps, lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(steps))
            self.play(FadeIn(a, lag_ratio=0.03), FadeIn(al), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b, lag_ratio=0.03), FadeIn(bl), GrowArrow(field), FadeIn(field_l), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[Rotate(p[1], angle=-PI / 2, about_point=p[0].get_center()) for p in b], FadeIn(rows[3]),
                      run_time=1.5)
        self.clear_scene()

    def relax(self):
        m = load("mri")
        head = heading(r"Step 2: \ how fast they recover depends on the tissue")
        A = axes([0, 3000], [0, 1.05], x_length=5.4, y_length=3.2, xticks=[0, 1000, 2000, 3000], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time after the pulse (ms)", ylabel=r"lined up again",
                 center=[-3.9, -0.5, 0])
        B = axes([0, 300], [0, 1.05], x_length=5.4, y_length=3.2, xticks=[0, 100, 200, 300], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time after the pulse (ms)", ylabel=r"signal still in step",
                 center=[3.4, -0.5, 0])
        ga = curve(A.ax, m["t"], m["grey_recovery"], NOISE, stroke_width=4)
        wa = curve(A.ax, m["t"], m["white_recovery"], VOLT, stroke_width=4)
        gb = curve(B.ax, m["t2"], m["grey_decay"], NOISE, stroke_width=4)
        wb = curve(B.ax, m["t2"], m["white_decay"], VOLT, stroke_width=4)
        lg = legend([(VOLT, r"white matter"), (NOISE, r"grey matter")], font_size=28).next_to(head, DOWN, buff=0.3)
        end = wrapped_label(r"Read the signal at a chosen moment and the tissues differ in brightness: \ that "
                            r"difference is the picture's contrast.", 12.6, 30, P.ACCENT).to_edge(DOWN, buff=0.4)
        tag = note(r"computed, with round values for the two tissues").to_corner(DR, buff=0.15)
        with self.voiceover(
            "Two. The signal fades, and how fast it fades depends on what the water is sitting in. "
            "<bookmark mark='a'/> The protons take a second or so to line up with the field again, and "
            "it's quicker in white matter, the brain's fatty cables, than in grey. <bookmark mark='b'/> "
            "And their signals drift out of step with one another within a tenth of a second, again at a "
            "rate that depends on the tissue. <bookmark mark='c'/> So if you read the signal at a "
            "well-chosen moment after the pulse, grey matter, white matter and fluid give different "
            "strengths. That difference is the contrast in the picture. An MRI scan is a map of how the "
            "water in each spot behaves, and nothing in it is a photograph. Remember the second kind of "
            "fading. The functional scan is built on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lg), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(wa), Create(ga), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(wb), Create(gb), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def kspace(self):
        m = load("mri")
        head = heading(r"Step 3: \ the scanner measures the picture's Fourier transform")
        y = -0.85
        k = heat(m["k_log"], 3.0, 0.0, float(m["k_log"].max()), center=[-5.2, y, 0], grey=True)
        kl = keep_in_frame(label(r"measured: \ strengths of stripe patterns", font_size=26, color=GREY_A).next_to(k, DOWN, buff=0.12))
        # place becomes pitch: three protons along a gradient, each wobbling at its own rate
        waves = VGroup()
        for i, (x0, f, name) in enumerate(((-4.2, 3, r"left: \ slower"), (0.0, 5, r"middle"), (4.2, 7, r"right: \ faster"))):
            xs = np.linspace(-1.5, 1.5, 200)
            w = VMobject(color=BLOOD, stroke_width=3).set_points_as_corners(
                [np.array([x0 + u, -0.6 + 0.45 * np.sin(2 * np.pi * f * (u + 1.5) / 3.0), 0]) for u in xs])
            waves.add(VGroup(w, label(name, font_size=26, color=BLOOD).next_to(w, DOWN, buff=0.2)))
        grad = VGroup(Arrow([-5.6, 0.75, 0], [5.6, 0.75, 0], buff=0, color=THRESH, stroke_width=5),
                      label(r"the field, made a little stronger from left to right", font_size=26, color=THRESH))
        grad[1].next_to(grad[0], UP, buff=0.1)
        pitch = VGroup(waves, grad)
        arrow = Arrow([-3.6, y, 0], [-2.8, y, 0], buff=0, color=GREY_B, stroke_width=4)
        recon = [heat(m["recon"][i], 2.1, 0.0, 1.0, center=[-1.6 + 2.3 * i, y + 0.3, 0], grey=True) for i in range(4)]
        caps = [label(t, font_size=27, color=VOLT).next_to(recon[i], DOWN, buff=0.1) for i, t in enumerate(
            (r"all of it", r"the middle half", r"a quarter", r"an eighth"))]
        # order shown: from little to all, as the scan fills in
        end = rows_of([
            (r"a gradient makes the field, and so the wobble's rate, depend on position: \ place becomes pitch",
             WHITE),
            (r"each reading is the strength of one stripe pattern across the head; \ the image is their sum",
             THRESH),
        ], 12.6, 29, 0.2).next_to(head, DOWN, buff=0.35)
        tag = psyche_tag(r"computed on a test image")
        with self.voiceover(
            "Three. How does a radio signal from the whole head turn into a picture? "
            "<bookmark mark='a'/> By making the field slightly stronger on one side of the head than the "
            "other. Then protons on one side wobble a little faster than those on the other, and where a "
            "proton is has been turned into the pitch of its signal. <bookmark mark='b'/> Work through "
            "the consequences and you find that each reading the scanner takes is the strength of one "
            "striped pattern across the head: so many stripes, at such an angle. The full set of readings "
            "is the picture's Fourier transform, which you can meet properly in Analysis, Built. "
            "<bookmark mark='c'/> Run the transform backwards and the picture appears. With only the "
            "coarsest eighth of the stripes, it's a blur. Each further batch adds finer detail. "
            "<bookmark mark='d'/> So a scan takes time, because the patterns are collected one after "
            "another. A whole brain at a resolution of a few millimetres takes a second or two. Hold on to "
            "that number as well."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(end[0]), FadeIn(grad), LaggedStart(*[Create(w_[0]) for w_ in waves], lag_ratio=0.3),
                      *[FadeIn(w_[1]) for w_ in waves], run_time=3.0)
            vo.wait_until("b")
            self.play(FadeOut(pitch), run_time=0.5)
            self.play(FadeIn(k), FadeIn(kl), FadeIn(end[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow))
            for i in (3, 2, 1, 0):
                self.play(FadeIn(recon[i]), FadeIn(caps[i]), run_time=1.0)
            vo.wait_until("d")
        self.clear_scene()
