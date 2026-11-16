from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


class Modal(SoundScene):
    def construct(self):
        chapter(self, 9, r"Modal synthesis", r"What if an instrument is just its modes?")
        self.modes()
        self.string()
        self.dispersion()
        self.quiz()
        self.uses()

    # ------------------------------------------------------------------
    def modes(self):
        items = [
            (r"any linear vibrating object moves as a sum of modes: \ shapes that each vibrate at one frequency \ (Parts 1 and 9)", WHITE),
            (r"strike it, \ and each mode rings as a damped sine: \ its frequency, \ its decay, \ and how hard the strike excites it", WHITE),
            (r"so the sound is a bank of resonators: \ Part 51's struck drum, \ many times over", WHITE),
            (r"the modes can come from theory, \ from finite elements \ (Part 9's bars), \ or from a measured recording", WHITE),
            (r"IRCAM's Mosaic and Modalys \ (1990s) \ built instruments this way, \ joined by their contact points", TUNE),
        ]
        rows_scene(self, r"an instrument as its modes", items,
                   "The third physical route uses modes. <bookmark mark='b'/> Any linear vibrating object moves as a sum of modes, "
                   "shapes that each vibrate at one frequency, as Parts 1 and 9 showed. <bookmark mark='c'/> Strike it, and each "
                   "mode rings as a damped sine, with its own frequency, its own decay, and its own share of the strike. "
                   "<bookmark mark='d'/> So the sound is a bank of resonators, Part 51's struck drum many times over. "
                   "<bookmark mark='e'/> The modes can come from theory, from finite elements like Part 9's bars, or from a measured "
                   "recording. <bookmark mark='f'/> IRCAM's Mosaic and Modalys built instruments this way in the 1990s, joining "
                   "objects at their points of contact.", marks="bcdef")

    # ------------------------------------------------------------------
    def string(self):
        d = load("modal")
        lines = VGroup(
            MathTex(r"u(x_p, t) = \sum_{n} a_n \sin\frac{n\pi x_p}{L}\, \cos(2\pi f_n t)\, e^{-\sigma_n t}", font_size=34),
            MathTex(r"f_n = n f_1 \sqrt{1 + B n^2}, \qquad \sigma_n = \sigma_0 + \sigma_1 \Big(\frac{n\pi}{L}\Big)^2", font_size=34),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.7)
        notes = VGroup(label(r"$a_n$: \ the pluck's shape, \ mode by mode; \ $x_p$: \ the pickup", font_size=18, color=WHITE),
                       label(rf"a stiff, \ damped G3 string: \ $B = {d['B'] * 1e4:.2f} \times 10^{{-4}}$; \ {d['modes']} modes", font_size=18, color=GREY_A),
                       label(r"exact for this equation: \ no grid, \ no time step, \ no dispersion", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"the stiff string, \ as modes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Take the stiff, damped string of Part 7. <bookmark mark='a'/> As modes, its pickup signal is a sum over n of the pluck's share of mode n, the mode's shape at the pickup, a cosine at the mode's frequency, and a decay. <bookmark mark='b'/> The frequencies follow the stiff string's law, each a little sharper than n times the first, and higher modes die faster. <bookmark mark='c'/> For the retained modes of this linear equation, frequencies are evaluated directly, avoiding grid dispersion; truncation, sampling and floating-point errors remain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dispersion(self):
        d = load("modal")
        ks = np.array([k for k, _ in d["cents"]])
        cs = np.array([c for _, c in d["cents"]])
        lo = min(cs.min(), -5) * 1.15
        ax = frame_axes(width=8.4, height=3.4, xlo=0, xhi=26, ylo=lo, yhi=3, center=LEFT * 1.0 + DOWN * 0.2)
        st = stems(ks, cs, ax.to, color=EAR, r=0.05)
        yt = VGroup(*[label(f"{v:d}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, -10, -20) if v >= lo])
        xl = label(r"partial number \ (every fifth missing: \ the pluck is at a fifth)", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.3)
        yl = label(r"finite differences against the modes, \ cents", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(rf"grid: \ {d['N']} intervals, \ Courant number {d['courant']:.2f}", font_size=17, color=WHITE),
                      label(rf"partial {int(ks[-1])}: \ {cs[-1]:.0f} cents flat", font_size=17, color=EAR),
                      label(rf"the two signals differ by {d['err_db']:.0f} dB overall", font_size=17, color=GREY_A),
                      label(r"the scheme's error: \ numerical dispersion, \ which grows with frequency", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.3)
        head = label(r"where the bead simulation errs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now compare with Part 7's bead-by-bead simulation of the same string, which steps a grid of "
            f"{say(d['N'])} intervals forward at forty-eight kilohertz. <bookmark mark='a'/> Below the Courant limit the scheme "
            "is no longer exact: its waves travel slightly too slowly at high frequencies, so each partial comes out a little "
            f"flat, by under a cent at the bottom and {say(-cs[-1])} cents by partial {say(int(ks[-1]))}. <bookmark mark='b'/> The "
            f"two signals differ by {say(-d['err_db'])} decibels overall. A finer grid would shrink it; the modal sum has no grid "
            "to refine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]), FadeIn(ghost(st, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(st), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("modal")
        c = clip("modal.two")
        card = listen_card(r"One plucked string, \ twice: \ once as a sum of modes, \ once bead by bead on a grid. \ "
                           r"Which was computed on the grid?", width=9.6)
        with self.voiceover(
            "Your turn. One plucked string, twice: once as a sum of modes, once bead by bead on a grid. Which was computed on "
            "the grid? Listen to the top of the sound."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one string, \ twice", kind="physical model", detail=r"modes, \ and beads", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        with self.voiceover(
            "The second. If you could not tell, that is the point: the grid's errors sit in the highest partials, which die "
            "first, and differ from the exact sum by a few cents to a few tens. The difference may be subtle in this example; we have not measured listener discrimination. "
            "The bead simulation's virtue is elsewhere: it handles what modes cannot, like a string that hits a fret or "
            "stretches as it swings, where the equation is no longer linear."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"modes are exact and cheap to control: \ move one mode's frequency or decay and nothing else changes", WHITE),
            (r"they need the object to be linear and its modes known: \ nonlinear joints and collisions require additional coupling or contact models", WHITE),
            (r"games and films strike thousands of virtual objects this way: \ contact sounds from modes \ (van den Doel and Pai, \ 1998)", WHITE),
            (r"the costs differ: \ a mode per partial; \ a grid point per bead; \ a delay line per wave", WHITE),
            (r"which to choose depends on what you need to control", TUNE),
        ]
        rows_scene(self, r"modes at work", items,
                   "Modes have a clear profile. <bookmark mark='b'/> They are exact and easy to control: move one mode's frequency "
                   "or decay, and nothing else changes. <bookmark mark='c'/> But they need the object to be linear and its modes "
                   "known; nonlinear joints and collisions require additional coupling or contact models. <bookmark mark='d'/> Games and films strike thousands of "
                   "virtual objects this way; Kees van den Doel and Dinesh Pai made contact sounds from modes in 1998. "
                   "<bookmark mark='e'/> And the costs differ: a mode per partial, a grid point per bead, a delay line per wave. "
                   "<bookmark mark='f'/> Which to choose depends on what you need to control.", marks="bcdef")
