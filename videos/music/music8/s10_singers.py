from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Singers(SoundScene):
    def construct(self):
        chapter(self, 9, r"What singers do", r"How does one voice carry over an orchestra, and how does one throat sing two notes?", lit=(1863,), extra=((1974, r"Sundberg's singer's formant"),))
        self.ring()
        self.soprano()
        self.overtone()

    # ------------------------------------------------------------------
    def ring(self):
        d = load("singers")
        c = clip("singers.formant")
        q = listen_card(r"One sung note, \ twice, \ at the same loudness. \\ Which voice would you hear over an orchestra?", width=8.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.4, width=3.0, height=1.3).move_to(DOWN * 0.4)
        with self.voiceover(
            "An opera singer stands in front of eighty instruments, with no microphone, and is heard at the "
            "back of the hall. How? Here is one sung note twice, at the same loudness. Which of these two "
            "voices would you hear over an orchestra?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one note, \ two singers", kind="synthesized", detail=r"a model of a voice", corner=DL, tag_corner=DR)
            for ev, b in zip(("plain", "ring"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.2)
        self.clear_scene()
        g = axes([0, 5000], [-48, 30], x_length=10.4, y_length=3.8, xlabel=r"frequency (Hz)", ylabel=r"dB", xticks=[0, 1000, 2000, 3000, 4000, 5000], yticks=[-40, -20, 0, 20], font_size=20)
        g.move_to(DOWN * 0.9)
        f = np.asarray(d["f"])
        c1 = curve_from(g, f, np.maximum(d["plain_db"], -48), GREY_B, stroke_width=2.5)
        c2 = curve_from(g, f, np.maximum(d["ring_db"], -48), VOICE)
        orch = curve_from(g, f, np.asarray(d["orchestra_db"]) + 12, BRASS, stroke_width=2)
        band = Rectangle(width=g.ax.c2p(3500, 0)[0] - g.ax.c2p(2500, 0)[0], height=3.8, stroke_width=0, fill_color=VOICE, fill_opacity=0.1).move_to(g.ax.c2p(3000, -9))
        key = VGroup(label(r"A: \ a speaking voice's tube", font_size=22, color=GREY_B), label(r"B: \ a trained singer's", font_size=22, color=VOICE),
                     label(r"an orchestra's average spectrum (schematic, \ after Sundberg)", font_size=22, color=BRASS)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).to_corner(UL, buff=0.4)
        bl = label(rf"$+{d['boost_db']:.0f}$ dB", font_size=28, color=VOICE).next_to(band, UP, buff=0.1)
        with self.voiceover(
            "B, the one with the edge on it. Singers call it ring. <bookmark mark='a'/> Here are the two "
            "filters. A is the tube of an ordinary speaking voice. B is the tube of a trained singer on the "
            "same vowel. The first two formants, which make the vowel, are nearly the same. The difference "
            "is higher up: the singer has drawn the third, fourth and fifth resonances together into one "
            f"cluster near three thousand hertz, and the filter is {say(d['boost_db'])} decibels stronger "
            "there. Johan Sundberg traced it in 1974 to the larynx, which trained singers lower, opening a "
            "small extra chamber just above the folds. <bookmark mark='b'/> Now put an orchestra on the same "
            "axes. Its average spectrum is strongest near five hundred hertz and falls away steadily above. "
            "At three thousand it has little left. And three thousand hertz, Part 4 found, is where the ear "
            "is most sensitive. The singer does not sing louder than the orchestra. The singer puts energy "
            "where the orchestra has none and the ear is listening hardest."
        ) as vo:
            self.play(FadeIn(g), Create(c1), Create(c2), FadeIn(key[0]), FadeIn(key[1]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(orch), FadeIn(key[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def soprano(self):
        d = load("singers")
        s = d["soprano"]
        from explainer.music.monochord.instruments import winds as W

        f = np.linspace(100, 4000, 400)
        e1 = W.spectrum_envelope((s["f1_speech"], 2790.0, 3310.0), f)
        e2 = W.spectrum_envelope((s["note"], 2790.0, 3310.0), f)
        g = axes([0, 4000], [-40, 34], x_length=10.0, y_length=3.4, xlabel=r"frequency (Hz)", ylabel=r"dB", xticks=[0, 1000, 2000, 3000, 4000], yticks=[-20, 0, 20], font_size=20)
        g.move_to(DOWN * 1.1)
        c1 = curve_from(g, f, e1, GREY_B, stroke_width=2.5)
        c2 = curve_from(g, f, e2, VOICE)
        harm = VGroup(*[DashedLine(g.ax.c2p(k * s["note"], -40), g.ax.c2p(k * s["note"], 34), color=TUNE, stroke_width=2) for k in (1, 2, 3, 4)])
        hl = label(r"a soprano's high A: \ harmonics 880 Hz apart", font_size=24, color=TUNE).next_to(g, UP, buff=0.15).shift(RIGHT * 2.2)
        rows = VGroup(label(rf"`ee' as spoken: \ first formant near {s['f1_speech']:.0f} Hz, \ far below the note", font_size=24, color=GREY_B),
                      label(r"the jaw drops: \ the first formant is raised onto the note", font_size=24, color=VOICE)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        card = history_card(2004, r"Joliveau, \ Smith and Wolfe", r"measure eight sopranos' mouths while they sing: above about 500 Hz, the first resonance follows the note.", width=5.0, font_size=20).to_corner(UR, buff=0.35)
        with self.voiceover(
            "High voices have a different problem. A soprano singing the A above the staff is at eight "
            "hundred and eighty hertz, so her harmonics are eight hundred and eighty hertz apart. "
            "<bookmark mark='a'/> Suppose she sings ee as she would say it, with its first formant near "
            f"{say(s['f1_speech'])} hertz. There is no harmonic down there for the formant to help. Her "
            "strongest partial, the note itself, sits in the valley beyond it. <bookmark mark='b'/> So she "
            "drops her jaw, which raises the first formant, until it sits on the note. In this simple "
            f"model that gains {say(s['gain_db'])} decibels; real mouths, which are lossier, gain less, but "
            "it is still the difference between filling a hall and not. In 2004 this was measured directly, "
            "in eight sopranos: above about five hundred hertz, the first resonance of the mouth follows "
            "the note as it climbs. <bookmark mark='c'/> The price is the words. Moving the first formant "
            "is changing the vowel. At the top of a soprano's range ee, ah and oo all become the same open "
            "sound, and that is why you cannot make out the text, however good the singer."
        ) as vo:
            self.play(FadeIn(g), FadeIn(harm), FadeIn(hl))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(rows[1]), run_time=2.0)
            self.play(FadeIn(card))
            vo.wait_until("c")
            self.play(Indicate(rows[1], color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overtone(self):
        d = load("singers")
        c = clip("singers.overtone")
        drone = d["drone"]
        n = 16
        sp = np.asarray(d["spectrum_db"])[:n]
        base = DOWN * 2.3 + LEFT * 6.0
        dx = 0.76
        h_of = lambda v: max(2.6 * (1 + v / 50.0), 0.06)   # noqa: E731
        bars = VGroup(*[Rectangle(width=0.44, height=h_of(sp[k]), stroke_width=0, fill_color=GREY_C, fill_opacity=0.8).move_to(base + RIGHT * dx * k, aligned_edge=DOWN) for k in range(n)])
        nums = VGroup(*[label(str(k + 1), font_size=20, color=GREY_B).next_to(base + RIGHT * dx * k, DOWN, buff=0.12) for k in range(n)])
        names = {8: r"C", 9: r"D", 10: r"E", 11: r"F$\uparrow$", 12: r"G", 13: r"A$\downarrow$"}
        nl = VGroup(*[label(t, font_size=22, color=TUNE).next_to(base + RIGHT * dx * (k - 1), DOWN, buff=0.5) for k, t in names.items()])
        head = VGroup(label(r"Two notes from one throat", font_size=36, color=GREY_A),
                      label(rf"a drone at {drone:.0f} Hz; \ the tract's second and third resonances drawn together onto one harmonic", font_size=24, color=VOICE)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        off = d["off_cents"]
        with self.voiceover(
            "And now back to Tuva. A soprano moves one formant onto her note. An overtone singer does "
            "something more extreme with two. <bookmark mark='a'/> The folds hold a low drone, rich in "
            "harmonics. With the tongue the singer makes two narrowings in the mouth, and shapes them until "
            "the second and third resonances of the tube sit almost on top of each other. Together they "
            "make one peak, far sharper than any vowel's, and the singer slides that peak onto a single "
            f"harmonic of the drone. In Monochord's version that harmonic stands {say(d['prominence_db'])} "
            "decibels above its neighbours. A magnetic resonance scanner watched a Tuvan singer do exactly "
            "this in 2020. <bookmark mark='b'/> The ear, which normally fuses harmonics into one sound, "
            "cannot fuse one that sticks out that far, and hears it as a second note. And the notes on "
            "offer are the harmonics themselves: the eighth, ninth and tenth make C, D, E; the twelfth is G. "
            f"The eleventh falls between F and F sharp, {say(off['4'])} cents above the F of Part 1's scale, "
            f"and the thirteenth is an A {say(abs(off['6']))} cents flat. Here is the Tune's first phrase, "
            "sung in the only scale a single throat has."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(bars), FadeIn(nums))
            vo.wait_until("b")
            self.play(FadeIn(nl))
        starts = [c.events[f"n{k}"] for k in range(len(d["harmonics"]))]
        hs = d["harmonics"]

        rest = sp.copy()
        rest[d["target"] - 1] = 0.5 * (sp[d["target"] - 2] + sp[d["target"]]) - 4.0      # the drone's harmonics with no peak on any of them

        def show(m, h):
            for j, b in enumerate(m):
                on = h is not None and j == h - 1
                near = h is not None and abs(j - (h - 1)) == 1
                gain = 0.0 if on else (max(float(rest[j]), -26.0) if near else float(rest[j]))
                b.stretch_to_fit_height(h_of(gain)).move_to(base + RIGHT * dx * j, aligned_edge=DOWN)
                b.set_fill(EAR if on else GREY_C, opacity=1.0 if on else 0.8)
            return m

        def lit(m, t):
            k = int(np.clip(np.searchsorted(starts, t, side="right") - 1, 0, len(hs) - 1))
            return show(m, hs[k] if t < c.duration - 0.05 else None)

        with self.listen(c) as snd:
            window(snd, r"a drone, \ and the Tune in its overtones", kind="synthesized", detail=r"a model of a voice", corner=DL, tag_corner=DR)
            snd.drive(bars, lit)
        show(bars, hs[-1])
        with self.voiceover(
            "Twinkle, twinkle, little star, with a flat last note that no amount of practice will fix, "
            "because it is the thirteenth harmonic and that is where the thirteenth harmonic is. So the two "
            "puzzles this part began with have one answer. A flute and a clarinet differ in which "
            "resonances their column of air has. A singer in Tuva is choosing, with the tongue, where the "
            "resonances of a much shorter column fall. A source, and a resonator that shapes it."
        ):
            self.play(Indicate(nl, color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
