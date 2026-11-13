from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Rough(SoundScene):
    def construct(self):
        chapter(self, 4, r"Roughness, \ measured", r"How far apart must two tones be to sound smooth?", lit=(1965,),
                extra=((1965, r"Plomp and Levelt"),), spoken="Roughness, measured")
        self.experiment()
        self.glide()
        self.pure()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("plomp")
        card = history_card(1965, r"Reinier Plomp and Willem Levelt, \ Soesterberg",
                            r"play pairs of pure tones to listeners who are not musicians, and ask one question: how pleasant is this sound?",
                            width=5.6).to_corner(UL, buff=0.4)
        g = axes([0, 6], [0, 1.1], x_length=6.4, y_length=3.4, xlabel="", ylabel=r"roughness", xticks=None, yticks=[], font_size=20)
        g.move_to(RIGHT * 3.0 + DOWN * 0.1)
        xl = label(r"how far apart the two tones are $\rightarrow$", font_size=20, color=GREY_B).next_to(g.ax.c2p(6, 0), DOWN, buff=1.05).align_to(g.ax.c2p(6, 0), RIGHT)
        g.add(xl)
        cu = curve(g.ax, d["x"], d["curve"], ROUGH)
        peak = DashedLine(g.ax.c2p(1, 0), g.ax.c2p(1, 1.0), color=GREY_B, stroke_width=1.5)
        band = DashedLine(g.ax.c2p(4, 0), g.ax.c2p(4, 0.5), color=GOOD, stroke_width=1.5)
        pl = label(r"worst: \\ a quarter \\ of a band", font_size=22, color=ROUGH).next_to(g.ax.c2p(1, 0), DOWN, buff=0.15)
        bl = label(r"smooth again: \\ one whole band", font_size=22, color=GOOD).next_to(g.ax.c2p(4, 0), DOWN, buff=0.15)
        zero = label(r"unison: \\ smooth", font_size=22, color=GREY_A).next_to(g.ax.c2p(0, 0), DOWN, buff=0.15).shift(LEFT * 0.3)
        notes = VGroup(label(r"the same curve at every pitch, \ if the separation is", font_size=24, color=GREY_A),
                       label(r"measured in the bands of the ear \ (Part 4)", font_size=24, color=EAR),
                       label(rf"near {d['lo']:.0f} Hz: \ worst about {d['worst_hz']:.0f} Hz apart", font_size=24, color=ROUGH)
                       ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(card, DOWN, buff=0.5).align_to(card, LEFT)
        with self.voiceover(
            "For a hundred years Helmholtz's theory was argued about, mostly by musicians judging chords on "
            "pianos and organs. In 1965 two Dutch psychologists, Reinier Plomp and Willem Levelt, did the simple "
            "thing. They took listeners with no musical training, played them pairs of pure tones, and "
            "asked only: how pleasant is this? <bookmark mark='a'/> This is the shape they found, in the form "
            "that later workers fitted to it. In unison, smooth. Pull the tones apart, and the sound roughens "
            "quickly to a worst point. <bookmark mark='b'/> Then it recovers, and beyond a certain separation the "
            "two tones are entirely smooth again. <bookmark mark='c'/> Now the important part. The worst "
            "separation is not a fixed number of hertz, and it is not a fixed musical interval. It is a quarter "
            "of a critical band, the width of the ear's filter that we measured in Part 4. And the roughness is "
            "gone at about one whole band. Roughness is what you hear when two tones land on the same stretch of "
            f"the membrane. Near {say(d['lo'])} hertz, the worst gap is about {say(d['worst_hz'])} hertz."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(zero), run_time=2.5)
            self.play(Create(peak), FadeIn(pl))
            vo.wait_until("b")
            self.play(Create(band), FadeIn(bl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.8), run_time=6.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def glide(self):
        d = load("plomp")
        c = clip("plomp.glide")
        secs = d["seconds"]
        q = listen_card(r"Two pure tones. \ One stays put. \ The other climbs a whole octave in twelve seconds. \\ When is the sound roughest: \ "
                        r"near the start, \ in the middle, \ or at the end?", width=10.2, font_size=26).to_edge(UP, buff=0.35)
        g = axes([0, 12], [0, 1.15], x_length=10.0, y_length=2.5, xlabel=r"the upper tone, \ in semitones above the lower", ylabel="", xticks=[0, 2, 4, 6, 7, 8, 10, 12], yticks=[], font_size=20)
        g.move_to(DOWN * 1.25)
        dot = Dot(g.ax.c2p(0, 0), radius=0.12, color=TUNE)
        with self.voiceover(
            "You can run their experiment in twelve seconds. Two pure tones. One stays where it is, at five "
            "hundred hertz. The other starts in unison with it and climbs steadily through a whole octave. The "
            "question: when is the sound roughest? Near the start, in the middle, or at the end?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(dot))
        trail = VMobject(stroke_color=ROUGH, stroke_width=3)
        semis, rough = d["semis"], d["rough"]

        def draw(m, t):
            k = int(np.clip(t / secs, 0, 1) * (len(semis) - 1))
            if k >= 1:
                m.set_points_as_corners([g.ax.c2p(s, v) for s, v in zip(semis[:k + 1:6], rough[:k + 1:6])])

        with self.listen(c) as snd:
            window(snd, r"one tone still, \ one climbing an octave", kind="synthesized", detail=r"two pure tones", corner=DL, tag_corner=DR)
            snd.show(trail)
            snd.drive(trail, draw)
            snd.drive(dot, lambda m, t: m.move_to(g.ax.c2p(12 * min(t / secs, 1.0), float(np.interp(12 * min(t / secs, 1.0), semis, rough)))))
        full = curve(g.ax, semis, rough, ROUGH)
        marks = VGroup(label(r"the tritone", font_size=22, color=GREY_A).next_to(g.ax.c2p(6, 0.02), UP, buff=0.3),
                       label(r"the fifth", font_size=22, color=GREY_A).next_to(g.ax.c2p(7, 0.02), UP, buff=0.75),
                       label(r"the octave", font_size=22, color=GREY_A).next_to(g.ax.c2p(12, 0.02), UP, buff=0.3))
        peak = label(rf"roughest: \ {d['worst_semitones']:.1f} semitones apart, \ in the first second", font_size=26, color=ROUGH).move_to(g.ax.c2p(5.4, 0.95))
        with self.voiceover(
            f"Near the start. The roughness peaked in the first second, when the tones were about "
            f"{say(d['worst_semitones'], 1)} semitones apart, and it was gone before they were a minor third "
            "apart. <bookmark mark='a'/> But notice what did not happen. The climbing tone passed through the "
            "tritone, the most notorious dissonance in music, and nothing happened. It passed through the fifth, "
            "and nothing happened. It arrived at the octave, and there was no moment of arrival. For nine seconds "
            "the sound was simply smooth."
        ) as vo:
            self.add(full)
            self.remove(trail)
            self.play(FadeOut(q), FadeIn(peak))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.6), run_time=5.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pure(self):
        d = load("plomp")
        c = clip("plomp.pure")
        bx = boxes((r"500 Hz + 750 Hz", r"500 Hz + 703 Hz"), buff=1.2, width=4.0, height=1.5, font_size=30).move_to(UP * 1.4)
        names = VGroup(label(r"a fifth, \ 3 : 2", font_size=28, color=GREY_A).next_to(bx[0], DOWN, buff=0.2), label(r"a tritone, \ 45 : 32", font_size=28, color=GREY_A).next_to(bx[1], DOWN, buff=0.2))
        with self.voiceover(
            "To be sure, here they are standing still. A fifth, and then a tritone, each made of two pure tones."
        ):
            self.play(FadeIn(bx), FadeIn(names))
        with self.listen(c) as snd:
            window(snd, r"a fifth, \ then a tritone, \ in pure tones", kind="synthesized", detail=r"pairs of pure tones", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.2)
        vals = VGroup(label(rf"roughness: \ {100 * d['pure_fifth'] / d['peak']:.1f}\% of the worst", font_size=26, color=GOOD).next_to(names[0], DOWN, buff=0.2),
                      label(rf"roughness: \ {100 * d['pure_tritone'] / d['peak']:.1f}\% of the worst", font_size=26, color=GOOD).next_to(names[1], DOWN, buff=0.2))
        moral = VGroup(label(r"for pure tones, \ every interval wider than a minor third is smooth", font_size=30, color=EAR),
                       label(r"so where do the ratios come from?", font_size=34, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 2.0)
        with self.voiceover(
            "Both are smooth. A little strange, perhaps, the second one, but there is no grinding in it. "
            "<bookmark mark='a'/> Monochord's roughness for the two is a fraction of one percent of the worst case, "
            "and two percent. <bookmark mark='b'/> So here is where a careful measurement leaves Helmholtz. "
            "Roughness is real, and it depends on the ear's bands. But for pure tones it knows nothing about "
            "ratios. Every interval wider than a minor third is as smooth as every other. The fifth is not "
            "special. The octave is not special. <bookmark mark='c'/> So where do the ratios come from? The answer "
            "is that no musical instrument makes a pure tone."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(vals))
            vo.wait_until("b")
            self.play(FadeIn(moral[0]))
            vo.wait_until("c")
            self.play(FadeIn(moral[1]))
        self.wait(0.3)
        self.clear_scene()
