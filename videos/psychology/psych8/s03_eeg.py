from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Eeg(VoiceoverScene):
    def construct(self):
        self.card()
        self.berger()
        self.together()
        self.inverse()

    def card(self):
        card = chapter_card(2, r"Voltages on the scalp", r"What can an electrode outside the skull hear?",
                            lit={1929: r"Berger's EEG"}, part=PART, scale=("circuit", "brain"), marr=("tissue",))
        with self.voiceover(
            "Chapter two. Voltages on the scalp."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _rhythm(self, center, width, alpha, seed):
        g = np.random.default_rng(seed)
        x = np.linspace(0, 1, 500)
        y = 0.35 * g.standard_normal(500).cumsum() / 12
        y = y - np.linspace(y[0], y[-1], 500)
        y += alpha * np.sin(2 * np.pi * 10 * x * 2.0) * (0.75 + 0.25 * np.sin(2 * np.pi * 1.3 * x))
        y += 0.06 * g.standard_normal(500)
        c = np.asarray(center, float)
        pts = [c + np.array([(xi - 0.5) * width, yi * 0.9, 0]) for xi, yi in zip(x, y)]
        return VMobject(color=EEGC, stroke_width=2.5).set_points_as_corners(pts)

    def berger(self):
        b = archive.BERGER_1929.data
        head = heading(r"Jena, the 1920s: \ a rhythm through the skull")
        hd = head_outline(3.4).move_to([-5.2, 0.4, 0])
        el = VGroup(Dot(hd.get_center() + np.array([-0.55, 1.25, 0]), radius=0.09, color=EEGC),
                    Dot(hd.get_center() + np.array([-1.3, 0.55, 0]), radius=0.09, color=EEGC))
        closed = self._rhythm([-1.2, 1.3, 0], 5.0, 0.42, 5)
        opened = self._rhythm([-1.2, -1.7, 0], 5.0, 0.05, 6)
        cl = label(r"eyes closed: \ about ten waves a second", font_size=27, color=EEGC).next_to(closed, UP, buff=0.12)
        ol = label(r"eyes open: \ the rhythm goes", font_size=27, color=GREY_A).next_to(opened, UP, buff=0.22)
        rows = rows_of([
            (rf"first recorded in {b['first_recording']}, \ published in {b['published']}", WHITE),
            (r"millionths of a volt, \ through skin and bone", WHITE),
            (rf"doubted for five years, \ until Cambridge confirmed it in 1934", GREY_A),
        ], 4.6, 30).move_to([4.6, 0.0, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.BERGER_1929.cite)
        tag = note(r"the traces are drawings").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now go outside the skull. In the nineteen-twenties, in Jena, a psychiatrist called Hans Berger "
            "pressed electrodes to the heads of his patients and of his own son, and connected them to the "
            "most sensitive instrument he could get. <bookmark mark='a'/> He found a voltage that rose and "
            "fell about ten times a second, when the person sat quietly with eyes closed. "
            "<bookmark mark='b'/> When they opened their eyes, or did a sum, it faded. <bookmark mark='c'/> "
            f"He made his first recording in {b['first_recording']}, and didn't publish until "
            f"{b['published']}. The signal is millionths of a volt, a thousand times smaller than the "
            "impulse inside a neuron in Part 5. <bookmark mark='d'/> Hardly anyone believed him. It took "
            "until 1934, when Edgar Adrian's laboratory in Cambridge repeated it, for the brain wave to be "
            "accepted. Berger named his record the electroencephalogram. Everyone else calls it the EEG. "
            "You met its rhythm in Part 6, as two populations of cells swinging against each other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(hd), FadeIn(el))
            vo.wait_until("a")
            self.play(Create(closed), FadeIn(cl), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(opened), FadeIn(ol), run_time=2.5, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def together(self):
        e = load("eeg")
        head = heading(r"Why the scalp hears only cells that act together")
        g = np.random.default_rng(9)

        def arrows(center, aligned):
            c = np.asarray(center, float)
            out = VGroup()
            for i in range(6):
                for j in range(4):
                    a = PI / 2 if aligned else g.uniform(0, TAU)
                    p = c + np.array([(i - 2.5) * 0.48, (j - 1.5) * 0.5, 0])
                    d = 0.19 * np.array([np.cos(a), np.sin(a), 0])
                    out.add(Arrow(p - d, p + d, buff=0, color=EEGC if aligned else NOISE, stroke_width=3,
                                  max_tip_length_to_length_ratio=0.4))
            return out

        # the opening picture: brief impulses miss one another, slow synaptic currents overlap and add
        def bumps(y0, width, col):
            x = np.linspace(-3.4, 3.4, 400)
            out, total = VGroup(), np.zeros_like(x)
            for c in (-0.9, 0.0, 0.9):
                y = np.exp(-0.5 * ((x - c) / width) ** 2)
                total += y
                out.add(VMobject(color=col, stroke_width=2.5, stroke_opacity=0.75).set_points_as_corners(
                    [np.array([xi, y0 + 0.7 * yi, 0]) for xi, yi in zip(x, y)]))
            out.add(VMobject(color=WHITE, stroke_width=4).set_points_as_corners(
                [np.array([xi, y0 + 0.7 * yi, 0]) for xi, yi in zip(x, total)]))
            return out

        sp = bumps(0.7, 0.05, SPIKE).shift(LEFT * 1.6)
        sy = bumps(-2.3, 0.9, EEGC).shift(LEFT * 1.6)
        spl = wrapped_label(r"three impulses, \ a millisecond each: \ they miss one another", 4.2, 29, SPIKE)
        spl.next_to(sp, RIGHT, buff=0.4)
        syl = wrapped_label(r"three synaptic currents, \ tens of milliseconds each: \ they overlap, \ and the sum "
                            r"(white) is large", 4.2, 29, EEGC).next_to(sy, RIGHT, buff=0.4)
        intro = VGroup(sp, spl, sy, syl)
        keep_in_frame(intro)

        left = arrows([-4.85, 1.0, 0], True)
        right = arrows([-4.85, -1.9, 0], False)
        ll = label(r"lined up: \ they add", font_size=27, color=EEGC).next_to(left, UP, buff=0.14)
        rl = keep_in_frame(label(r"every which way: \ they cancel", font_size=27, color=NOISE).next_to(right, UP, buff=0.14))
        A = axes([1, 6], [0, 6], x_length=4.3, y_length=3.8, xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}",
                 xlabel=r"number of sources", ylabel=r"size of their sum", center=[0.1, -0.5, 0])
        ax = A.ax
        ca = curve(ax, np.log10(e["n"]), np.log10(e["aligned"]), EEGC, stroke_width=4)
        cr = curve(ax, np.log10(e["n"]), np.log10(e["random"]), NOISE, stroke_width=4)
        la = label(r"aligned: \ $N$", font_size=27, color=EEGC).next_to(ax.c2p(4.6, 4.7), UL, buff=0.1)
        lr = label(r"random: \ $\sqrt{N}$", font_size=27, color=NOISE).next_to(ax.c2p(5.0, 2.5), DOWN, buff=0.5)
        rows = rows_of([
            (rf"a million sources: \ aligned ones sum {fmt_int(round(e['ratio_million'], -2))} times larger", THRESH),
            (r"so the EEG is the synaptic currents of cortical cells that stand side by side and are driven "
             r"together", WHITE),
            (r"impulses are too brief and too scattered to add", GREY_A),
        ], 3.7, 29, 0.3).move_to([5.05, -0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed")
        with self.voiceover(
            "What is that voltage? Not impulses. An impulse lasts a millisecond, and a neighbour's impulse "
            "a moment later doesn't line up with it. What adds up at a distance is the slower current that "
            "flows when a synapse is active, which makes each cell, for a few hundredths of a second, a "
            "tiny battery with a plus end and a minus end. <bookmark mark='a'/> Now it's a matter of "
            "arithmetic. If the batteries all point the same way and switch on together, their fields add. "
            "<bookmark mark='b'/> If they point every which way, they mostly cancel. "
            "<bookmark mark='c'/> A hundred aligned sources sum to a hundred. A hundred random ones sum to "
            "about ten, the square root. <bookmark mark='d'/> With a million sources, the aligned sum is "
            f"about {round(e['ratio_million'], -2):,.0f} times larger. <bookmark mark='e'/> And the "
            "cortex is built to be aligned. Its large cells stand side by side like trees in a plantation, "
            "pointing at the surface. So the EEG is the synaptic input of large sheets of those cells, when "
            "it arrives in step. Everything else in the brain is electrically invisible from outside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(Create(sp), FadeIn(spl), run_time=2.0)
            self.wait(3.0)
            self.play(Create(sy), FadeIn(syl), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(intro))
            self.play(FadeIn(left, lag_ratio=0.03), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(right, lag_ratio=0.03), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(A))
            self.play(Create(ca), Create(cr), FadeIn(la), FadeIn(lr), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.clear_scene()

    def inverse(self):
        e = load("eeg")
        head = heading(r"Which sources made this pattern? \ There is no single answer")
        elec, src = e["electrodes"], e["sources"]
        scale = 1.75

        def headmap(center, strengths, title, col):
            c = np.asarray(center, float)
            dip = 0.31
            g = VGroup(Arc(radius=scale, start_angle=-dip, angle=PI + 2 * dip, color=GREY_B,
                           stroke_width=3).move_arc_center_to(c),
                       Line(c + scale * np.array([-np.cos(dip), -np.sin(dip), 0]),
                            c + scale * np.array([np.cos(dip), -np.sin(dip), 0]), color=GREY_D, stroke_width=2))
            top = max(float(np.abs(strengths).max()), 1e-9)
            for (x, y), s in zip(src, strengths):
                if abs(s) < 0.04 * top:
                    g.add(Dot(c + np.array([x, y, 0]) * scale, radius=0.04, color=GREY_D))
                else:
                    g.add(Dot(c + np.array([x, y, 0]) * scale, radius=0.07 + 0.16 * abs(s) / top,
                              color=col if s > 0 else BAD, fill_opacity=0.9))
            for x, y in elec:
                g.add(Square(side_length=0.14, stroke_width=0, fill_color=EEGC, fill_opacity=1).move_to(
                    c + np.array([x, y, 0]) * scale))
            g.add(label(title, font_size=27, color=col).next_to(g, UP, buff=0.12))
            return g

        a0 = headmap([-4.7, 0.7, 0], np.zeros(len(src)), r"a toy head, \ nine electrodes", EEGC)
        a = headmap([-4.7, 0.7, 0], e["focal"], r"one small source", THRESH)
        b = headmap([-0.5, 0.7, 0], e["other"], r"a quite different set", MODEL)
        top = float(np.abs(e["scalp_focal"]).max())

        def bars(center, v, col):
            c = np.asarray(center, float)
            g = VGroup(Line(c + LEFT * 1.7, c + RIGHT * 1.7, color=GREY_D, stroke_width=2))
            for k, val in enumerate(v):
                h = 0.9 * val / top
                r = Rectangle(width=0.26, height=max(abs(h), 0.01), stroke_width=0, fill_color=col, fill_opacity=0.9)
                r.move_to(c + np.array([(k - 4) * 0.38, h / 2, 0]))
                g.add(r)
            return g

        ba = bars([-4.7, -1.7, 0], e["scalp_focal"], THRESH)
        bb = bars([-0.5, -1.7, 0], e["scalp_other"], MODEL)
        bl = label(r"the voltage at each of the nine electrodes", font_size=27, color=EEGC).move_to([-2.6, -2.9, 0])
        eq = label(r"$=$", font_size=60).move_to([-2.6, -1.3, 0])
        rows = rows_of([
            (rf"{e['n_sources']} possible sources, \ {e['n_electrodes']} electrodes: \ more unknowns than "
             r"measurements", WHITE),
            (r"some patterns of sources cancel at every electrode; \ add one, \ and nothing outside changes", THRESH),
            (r"So an EEG tells you \emph{when}, to the millisecond. \ \emph{Where} needs an assumption.", P.ACCENT),
        ], 4.5, 28, 0.32).move_to([4.75, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: a toy head (Psyche)")
        with self.voiceover(
            "There's a second cost, and it's permanent. Here's a toy head, seen from the front, with nine "
            "electrodes on the scalp. <bookmark mark='a'/> Put one small source inside, and each electrode "
            "reads a voltage. That's the forward problem, from source to scalp, and it has one answer. "
            "<bookmark mark='b'/> Now the question a researcher faces: given the nine voltages, where was "
            "the source? <bookmark mark='c'/> Here's a quite different arrangement, several sources, some "
            "positive and some negative, spread across the head. Its nine voltages are identical, to the "
            "last decimal. <bookmark mark='d'/> That isn't an accident of the toy. There are more possible "
            "sources than electrodes, so there are whole patterns of sources that cancel at every "
            "electrode. Add any of them to a solution and you have another solution. Helmholtz proved this "
            "in the eighteen-fifties. <bookmark mark='e'/> So the EEG tells you when something happened, to "
            "the millisecond. Where it happened can't be read off. It can only be estimated, by adding "
            "assumptions about what sources are plausible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(a0))
            vo.wait_until("a")
            self.play(FadeOut(a0), FadeIn(a))
            self.play(FadeIn(ba), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(bb), FadeIn(eq, scale=1.4))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()
