from __future__ import annotations

import math

import numpy as np

from videos.music.music55.common import *  # noqa: F403

LAYOUT = [("C", 0), ("L", 30), ("R", -30), ("Ls", 90), ("Rs", -90), ("Lb", 145), ("Rb", -145)]


def vbap(theta_deg):
    """Pulkki's pairwise vector-base amplitude panning over the ring of LAYOUT (angles positive to the left)."""
    angs = sorted(a for _, a in LAYOUT)
    g = {a: 0.0 for a in angs}
    t = (theta_deg + 180) % 360 - 180
    ring = angs + [angs[0] + 360]
    for a1, a2 in zip(ring[:-1], ring[1:]):
        tt = t if t >= a1 else t + 360
        if a1 <= tt <= a2:
            L = np.array([[math.cos(math.radians(a1)), math.sin(math.radians(a1))], [math.cos(math.radians(a2)), math.sin(math.radians(a2))]])
            p = np.array([math.cos(math.radians(tt)), math.sin(math.radians(tt))])
            gg = p @ np.linalg.inv(L)
            gg = np.maximum(gg, 0)
            gg = gg / np.linalg.norm(gg)
            g[a1] += gg[0]
            g[(a2 + 180) % 360 - 180] += gg[1]
            break
    return g


class Objects(SoundScene):
    def construct(self):
        chapter(self, 10, r"Object audio", r"What if a mix did not know how many loudspeakers it would meet?")
        self.three()
        self.atmos()
        self.vbap()
        self.renderer()
        self.music()

    # ------------------------------------------------------------------
    def three(self):
        items = [
            (r"channel-based: \ a signal for each loudspeaker \ (stereo, \ 5.1 since the 1990s); \ right only for that layout", WHITE),
            (r"scene-based: \ the field itself \ (Ambisonics), \ decoded for any layout", WHITE),
            (r"object-based: \ each sound kept separate, \ with metadata: \ where it is, \ how big, \ moving how", WHITE),
            (r"the renderer, \ at playback, \ knows the loudspeakers \ (or the headphones) \ and places each object", TUNE),
            (r"most mixes now are all three: \ a bed of channels, \ an ambisonic scene, \ and objects", GREY_A),
        ]
        rows_scene(self, r"channels, \ scenes and objects", items,
                   "There are three ways to store space. <bookmark mark='b'/> Channel-based: a signal for each loudspeaker, like "
                   "stereo, or the five point one of cinemas since the 1990s, right only for that layout. <bookmark mark='c'/> "
                   "Scene-based: the field itself, as in Ambisonics, decoded for whatever layout there is. "
                   "<bookmark mark='d'/> Object-based: every sound kept separate, with metadata saying where it is, how big, and how "
                   "it moves. <bookmark mark='e'/> Then a renderer, at playback, which knows the loudspeakers, or the headphones, "
                   "places each object. <bookmark mark='f'/> Most mixes today are all three at once: a bed of channels, perhaps an "
                   "ambisonic scene, and objects.", marks="bcdef")

    # ------------------------------------------------------------------
    def atmos(self):
        items = [
            (r"2012: \ Dolby Atmos opens with Pixar's \textit{Brave}: \ up to 128 tracks, \ objects rendered to as many as 64 loudspeakers, \ some overhead", WHITE),
            (r"the home: \ 7.1.4, \ seven round the listener, \ one subwoofer, \ four in the ceiling", WHITE),
            (r"standards for broadcast: \ MPEG-H 3D Audio and AC-4, \ object audio over the air", WHITE),
            (r"from 2019, \ and widely from 2021: \ streaming services offer music mixed in Atmos, \ heard mostly on headphones, \ rendered binaurally", TUNE),
        ]
        rows_scene(self, r"objects in the cinema and at home", items,
                   "Objects reached the public through the cinema. <bookmark mark='b'/> Dolby Atmos opened in 2012 with Pixar's "
                   "Brave: up to a hundred and twenty-eight tracks, with objects rendered to as many as sixty-four loudspeakers, some "
                   "of them overhead. <bookmark mark='c'/> At home the usual layout is seven point one point four: seven "
                   "loudspeakers round the listener, one subwoofer, four in the ceiling. <bookmark mark='d'/> Broadcasting has "
                   "standards of its own, MPEG-H 3D Audio and AC-4. <bookmark mark='e'/> And from 2019, and widely from 2021, streaming "
                   "services began to offer music mixed in Atmos, heard mostly on headphones, and so rendered binaurally.", marks="bcde")

    # ------------------------------------------------------------------
    def vbap(self):
        cen = DOWN * 0.4 + LEFT * 2.6
        R = 2.3
        theta = ValueTracker(0.0)

        def u(a):
            return np.array([-math.sin(math.radians(a)), math.cos(math.radians(a)), 0])

        sp = VGroup(*[VGroup(Square(side_length=0.32, stroke_color=GREY_B, stroke_width=2.5).move_to(cen + R * u(a)), label(n, font_size=13, color=GREY_A).move_to(cen + (R + 0.42) * u(a)))
                      for n, a in LAYOUT])
        lis = Dot(cen, radius=0.08, color=WHITE)
        obj = always_redraw(lambda: Dot(cen + 1.5 * u(theta.get_value()), radius=0.13, color=EAR))
        names = [n for n, _ in LAYOUT]

        def bars():
            g = vbap(theta.get_value())
            out = VGroup()
            for i, (n, a) in enumerate(LAYOUT):
                v = g.get(a, 0.0)
                b = Rectangle(width=0.42, height=max(2.2 * v, 0.02), stroke_width=0, fill_color=TUNE, fill_opacity=0.85)
                b.move_to([2.0 + 0.7 * i, -1.6 + b.height / 2, 0])
                out.add(b)
            return out

        gb = always_redraw(bars)
        bl = VGroup(*[label(n, font_size=15, color=GREY_A).move_to([2.0 + 0.7 * i, -1.85, 0]) for i, n in enumerate(names)])
        base = Line([1.7, -1.6, 0], [2.0 + 0.7 * 6 + 0.3, -1.6, 0], color=GREY_B, stroke_width=1.5)
        eq = MathTex(r"\mathbf{p} = g_1\mathbf{l}_1 + g_2\mathbf{l}_2 \ \Rightarrow\ \mathbf{g} = \mathbf{p}^{\mathsf T}\mathbf{L}^{-1}, \ \ \|\mathbf{g}\| = 1", font_size=28, color=TUNE).move_to(RIGHT * 4.1 + UP * 1.9)
        note = label(r"Pulkki \ (1997): \ vector-base amplitude panning: \ the two loudspeakers either side, \ at constant power", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"placing an object", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How does a renderer place an object between loudspeakers? <bookmark mark='a'/> The simplest answer is Ville "
            "Pulkki's of 1997, vector-base amplitude panning: write the object's direction as a combination of the two "
            "loudspeakers either side of it, and normalize the gains to constant power. In three dimensions, the three "
            "loudspeakers round it. <bookmark mark='b'/> Watch an object travel once round a seven-loudspeaker ring: at each "
            "moment only the pair that brackets it plays, and the energy hands from pair to pair. Stereo's pan law, wrapped round "
            "the listener."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sp), FadeIn(lis), FadeIn(obj), FadeIn(gb), FadeIn(bl), FadeIn(base))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(note))
            vo.wait_until("b")
            self.play(theta.animate.set_value(360.0), run_time=9.0, rate_func=linear)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def renderer(self):
        items = [
            (r"on headphones, \ the renderer is Chapter 9's: \ each object through the head-related filters for its direction", WHITE),
            (r"on a soundbar, \ crosstalk cancellation and beams bounced off the walls and ceiling", WHITE),
            (r"one mix, \ every playback: \ the renderer's quality is now part of what music sounds like", TUNE),
            (r"and the room the listener sits in is still added on top, \ unless it is headphones", GREY_A),
        ]
        rows_scene(self, r"one mix, \ every playback", items,
                   "The same objects can be rendered anywhere. <bookmark mark='b'/> On headphones, the renderer is the one of "
                   "Chapter 9: each object passes through the head-related filters for its direction. <bookmark mark='c'/> On a "
                   "soundbar, by crosstalk cancellation and by beams bounced off the walls and ceiling. <bookmark mark='d'/> One mix "
                   "serves every playback, so the renderer's quality is now part of what the music sounds like. "
                   "<bookmark mark='e'/> And the listener's own room is still added on top, unless they are wearing headphones.", marks="bcde")

    # ------------------------------------------------------------------
    def music(self):
        items = [
            (r"film sound has a screen to anchor it; \ music has none, \ and listeners face the front by habit", WHITE),
            (r"some mixes put the listener inside the band; \ others keep a stage in front and use the room above and behind", WHITE),
            (r"the binaural rendering of a mix differs from one service and earbud to another; \ the mixer cannot hear every version", WHITE),
            (r"and every spatial mix still needs a stereo version: \ the fold-down is part of the art", TUNE),
        ]
        rows_scene(self, r"space as part of the music", items,
                   "For music the questions are new. <bookmark mark='b'/> Film sound has a screen to anchor it; music has none, and "
                   "listeners face the front from habit. <bookmark mark='c'/> Some mixes put the listener inside the band; others "
                   "keep a stage in front and use the space above and behind for the room. <bookmark mark='d'/> The binaural "
                   "rendering of a mix differs from one service and one earbud to another, so a mixer cannot hear every version "
                   "their listeners will. <bookmark mark='e'/> And every spatial mix still needs a stereo version: the fold-down is "
                   "part of the art.", marks="bcde")
