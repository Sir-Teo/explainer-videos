from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Origin(VoiceoverScene):
    def construct(self):
        self.card()
        self.two()
        self.same()
        self.slopes()

    def card(self):
        card = chapter_card(10, r"Where Weber's law comes from", r"Is it the noise, \ or the code?", lit=(), part=PART,
                            scale=("neuron", "mind"), marr=("how",))
        with self.voiceover(
            "Chapter ten. Where Weber's law comes from."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _bells(self, ax, centers, sds, color):
        g = VGroup()
        x = np.linspace(0, 10, 300)
        for c, s in zip(centers, sds):
            y = np.exp(-0.5 * ((x - c) / s) ** 2)
            g.add(curve(ax, x, y, color, stroke_width=3))
        return g

    def two(self):
        head = heading(r"Two ways to get a constant fraction")
        A = axes([0, 10], [0, 1.1], x_length=5.6, y_length=2.0, xticks=[], yticks=[], xlabel=r"the signal in the head",
                 ylabel=r"", center=[-3.4, 1.1, 0])
        B = axes([0, 10], [0, 1.1], x_length=5.6, y_length=2.0, xticks=[], yticks=[], xlabel=r"the signal in the head",
                 ylabel=r"", center=[3.4, 1.1, 0])
        a_b = self._bells(A.ax, [1.0, 3.0, 7.0], [0.15, 0.45, 1.05], WEBERC)
        b_b = self._bells(B.ax, [2.0, 5.2, 8.2], [0.4, 0.4, 0.4], STEVC)
        ta = label(r"1. \ a straight code, \ noise that grows", font_size=30, color=WEBERC).next_to(A, UP, buff=0.2)
        tb = label(r"2. \ a compressed code, \ fixed noise", font_size=30, color=STEVC).next_to(B, UP, buff=0.2)
        rows = rows_of([
            (r"1: \ the signal is proportional to the stimulus, \ and its noise grows in proportion too \ (photons, \ spikes "
             r"that vary more when there are more of them)", WEBERC),
            (r"2: \ the signal grows as the logarithm of the stimulus, \ and its noise stays the same size", STEVC),
            (r"either way, \ a difference is noticed when it is large compared with the noise: \ a constant fraction", THRESH),
        ], 12.4, 29, 0.26).move_to([0, -2.0, 0])
        tag = note(r"a diagram: \ three stimuli, \ each with its spread").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Why should the noticeable difference be a constant fraction? There are two simple ways to "
            "build it, and Psyche's observer used the first. <bookmark mark='a'/> One: the signal in the "
            "head is proportional to the stimulus, and its noise grows in proportion too. Light arrives as "
            "photons, and nerve cells fire spikes, and both get more variable as there are more of them. "
            "<bookmark mark='b'/> Two: the signal grows as the logarithm of the stimulus, compressed, and "
            "its noise stays the same size. <bookmark mark='c'/> Either way, a difference is noticed when "
            "it's large compared with the noise at that level, and either way that makes the noticeable "
            "difference a constant fraction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(ta), Create(a_b), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tb), Create(b_b), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def same(self):
        d = load("origin")
        head = heading(r"The same thresholds, \ to within a few percent")
        A = log_axes((0, 4), (-1, 3), x_length=6.8, y_length=4.2, xlabel=r"the standard", ylabel=r"the just noticeable difference",
                     center=[-2.9, -0.35, 0])
        ax = A.ax
        lx = np.log10(d["standards"])
        la = curve(ax, lx, np.log10(d["jnd_a"]), WEBERC, stroke_width=6)
        lb = DashedVMobject(curve(ax, lx, np.log10(d["jnd_b"]), STEVC, stroke_width=6), num_dashes=40, dashed_ratio=0.45)
        lg = legend([(WEBERC, r"growing noise"), (STEVC, r"compressed code (dashed)")], font_size=26).move_to(ax.c2p(1.2, 2.5))
        rows = rows_of([
            (rf"two machines, \ one curve: \ their thresholds differ by {100 * (1 - d['min_ratio']):.0f}\% at most", WHITE),
            (r"so thresholds alone cannot tell you which is in the head", THRESH),
            (r"what can: \ how confident people are, \ how fast they answer, \ and the cells themselves (Parts 12, \ 13 and 58)",
             MODEL),
            (r"Weber's law is a fact about the output. \ Its cause is an open question", GREY_A),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: two observers built to match")
        with self.voiceover(
            "Now build both, and measure their thresholds at every standard. <bookmark mark='a'/> One "
            "curve. Above the floor, the two machines' thresholds differ by "
            f"{100 * (1 - d['min_ratio']):.0f} percent at most. <bookmark mark='b'/> So thresholds alone "
            "can't tell you which machine is in the head. <bookmark mark='c'/> Other measurements can: "
            "how confident people are, how fast they answer, and the cells themselves. That's Parts 12 and "
            "13, and at the end of the series, Part 58. <bookmark mark='d'/> For now: Weber's law is a "
            "solid fact about what comes out. What produces it is still argued over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lg))
            vo.wait_until("a")
            self.play(Create(la), FadeIn(rows[0]), run_time=2.0)
            self.play(Create(lb), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def slopes(self):
        d = load("tvi")
        src = archive.DEVRIES_ROSE
        head = heading(r"The slope tells you the noise")
        A = log_axes((-4, 7), (-2, 6), x_length=6.8, y_length=4.4, xlabel=r"background intensity",
                     ylabel=r"the just noticeable increment", center=[-3.0, -0.4, 0])
        ax = A.ax
        lx, ly = np.log10(d["intensity"]), np.log10(d["jnd"])
        whole = curve(ax, lx, ly, WHITE, stroke_width=6)
        y0 = float(ly[0])
        guides = VGroup()
        for (x_a, x_b, slope, x_ref, col) in ((-4, -1.6, 0.0, -4, GREY_B), (-3.4, 2.4, 0.5, 0.0, STEVC),
                                               (2.4, 7.0, 1.0, 7.0, WEBERC)):
            y_ref = float(np.interp(x_ref, lx, ly))
            xs = np.array([x_a, x_b])
            ys = y_ref + slope * (xs - x_ref) + (0.0 if slope == 0.0 else -0.45)
            guides.add(DashedLine(ax.c2p(xs[0], ys[0]), ax.c2p(xs[1], ys[1]), color=col, stroke_width=3, dash_length=0.12))
        gl = VGroup(
            label(r"slope 0", font_size=24, color=GREY_B).next_to(ax.c2p(-3.2, y0), UP, buff=0.12),
            label(r"slope $\tfrac12$", font_size=24, color=STEVC).next_to(ax.c2p(0.6, float(np.interp(0.6, lx, ly)) - 0.45),
                                                                       DR, buff=0.05),
            label(r"slope 1", font_size=24, color=WEBERC).next_to(ax.c2p(5.4, float(np.interp(5.4, lx, ly)) - 0.45), DR,
                                                                  buff=0.05),
        )
        rows = rows_of([
            (r"a third source of noise: \ light arrives as photons, \ and a count of photons varies by its square root",
             WHITE),
            (r"very dim: \ the eye's own noise sets a floor, \ ``dark light'' (slope 0)", GREY_A),
            (r"dim: \ photon noise; \ the increment grows as the square root of the background (slope $\tfrac12$): \ "
             r"the de Vries-Rose law, \ 1943 and 1948", STEVC),
            (r"bright: \ noise in proportion, \ Weber's law (slope 1)", WEBERC),
            (r"vision's measured curves bend this way, \ though the middle is only roughly a square root (Part 13)",
             THRESH),
        ], 5.0, 27, 0.24).move_to([4.35, -0.2, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), psyche_tag(r"computed: \ floor, \ photon and Weber noise"))
        with self.voiceover(
            "There's a way to read the noise off the thresholds, and it needs a wider range than one "
            "experiment usually covers. <bookmark mark='a'/> Plot the just noticeable increment against the "
            "background on log-log axes, from almost dark to bright daylight. Psyche's eye here has three "
            "sources of noise. <bookmark mark='b'/> Light comes in photons, and a count of photons varies by "
            "about its square root. <bookmark mark='c'/> Very dim: the eye's own noise, the dark light, "
            "dominates, and the threshold doesn't depend on the background at all. Slope zero. "
            "<bookmark mark='d'/> Dim: photon noise dominates, and the threshold grows as the square root "
            "of the background. Slope one half. Hessel de Vries in 1943 and Albert Rose in 1948 worked "
            "this out from the physics of light. <bookmark mark='e'/> Bright: noise in proportion to the "
            "signal, and Weber's law. Slope one. <bookmark mark='f'/> Measured curves of threshold against "
            "background in vision do bend this way, though the middle stretch is only roughly a square "
            "root, and the eye also turns its own gain down as the light grows. So Weber's law isn't one "
            "law but one regime, and the slope says which noise is in charge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(whole), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(guides[0]), FadeIn(gl[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(guides[1]), FadeIn(gl[1]), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(Create(guides[2]), FadeIn(gl[2]), FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

