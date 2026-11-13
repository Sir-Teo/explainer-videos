from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Bands(SoundScene):
    def construct(self):
        chapter(self, 3, r"How fine is the ruler?", r"How close can two tones be, and still be heard as two?", lit=(1863,),
                extra=((1940, r"Fletcher's critical band"),))
        self.overlap()
        self.fletcher()
        self.widths()
        self.pairs()
        self.cochleagram()

    # ------------------------------------------------------------------
    def overlap(self):
        d = load("wave")
        co = Cochlea(width=10.4, scale=1.3).move_to(UP * 0.7)
        x = d["x_mm"]
        e1 = d["env_1000"]
        shift = d["mm_per_octave"] * np.log2(1.1)
        e11 = np.interp(x + shift, x, e1)
        a = co.lens(d["env_2000"], color=AIR, opacity=0.35)
        b = co.lens(e1, color=TUNE, opacity=0.35)
        c_ = co.lens(e11, color=BAD, opacity=0.35)
        la = co.pin(14.1, r"2000 Hz", color=AIR, up=1.55)
        lb = co.pin(18.7, r"1000 Hz", color=TUNE, up=1.55)
        lc = co.pin(18.7 - shift, r"1100 Hz", color=BAD, up=2.05)
        t1 = label(r"an octave apart: \ two separate stretches of membrane", font_size=28, color=GREY_A).move_to(DOWN * 2.3)
        t2 = label(r"a tenth apart: \ the same stretch, \ the same hair cells", font_size=28, color=BAD).move_to(DOWN * 2.3)
        with self.voiceover(
            "The cochlea sorts frequencies by place. But look again at the wave from the last chapter. A single "
            "pure tone does not move a point on the membrane. It moves a stretch of it, several millimetres long. "
            "<bookmark mark='a'/> Two tones an octave apart move two separate stretches, and different hair cells "
            "report each one. <bookmark mark='b'/> But bring the second tone down to within a tenth of the "
            "first, and the two stretches lie on top of each other. The same hair cells feel both. So there must "
            "be a limit to how finely the ear can separate, and Part 3 told us that it matters: it is the limit "
            "below which the ear starts to hear phase. How wide is it?"
        ) as vo:
            self.play(FadeIn(co), FadeIn(b), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeOut(a), FadeOut(la), FadeOut(t1), FadeIn(c_), FadeIn(lc), FadeIn(t2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fletcher(self):
        d = load("bands")
        card = history_card(1940, r"Harvey Fletcher, \ Bell Laboratories",
                            r"hides a pure tone in a band of noise centred on it, and widens the band, keeping the "
                            r"noise's power in each hertz the same", width=5.4).to_corner(UL, buff=0.4)
        g = axes([1, np.log10(2000)], [-12, 2], x_length=6.2, y_length=3.6, xlabel=r"width of the band of noise (Hz)",
                 ylabel=r"how strong the tone must be to be heard (dB)", xticks=[1, 2, 3], yticks=[-10, -5, 0],
                 xfmt=lambda v: f"{10 ** v:g}", font_size=20)
        g.move_to(RIGHT * 3.2 + DOWN * 0.2)
        cu = curve(g.ax, np.log10(d["fletcher_bw"]), d["fletcher_db"], EAR)
        knee = DashedLine(g.ax.c2p(np.log10(d["erb_1k"]), -12), g.ax.c2p(np.log10(d["erb_1k"]), 1.5), color=GOOD, stroke_width=2)
        kl = label(rf"{d['erb_1k']:.0f} Hz", font_size=24, color=GOOD).next_to(knee, UP, buff=0.05)
        # the picture of the experiment: a tone, and noise around it
        base = Line(LEFT * 2.4, RIGHT * 2.4, color=GREY_C, stroke_width=2).move_to(LEFT * 3.9 + DOWN * 2.3)
        tone = Line(base.get_center(), base.get_center() + UP * 1.3, color=TUNE, stroke_width=6)
        w = ValueTracker(0.25)
        noise = always_redraw(lambda: Rectangle(width=w.get_value(), height=0.55, stroke_width=0, fill_color=GREY_B, fill_opacity=0.45)
                              .move_to(base.get_center() + UP * 0.275))
        filt = ArcBetweenPoints(base.get_center() + LEFT * 0.7, base.get_center() + RIGHT * 0.7, angle=-PI * 0.85, color=GOOD, stroke_width=3)
        fl = label(r"the ear's filter", font_size=22, color=GOOD).next_to(filt, UP, buff=0.5).shift(RIGHT * 1.5)
        with self.voiceover(
            "The measurement was made in 1940 by Harvey Fletcher, at Bell Laboratories, and it is clever. Hide a "
            "pure tone in a narrow band of noise centred on it, and find how strong the tone must be to be heard. "
            "<bookmark mark='a'/> Now widen the band, keeping the noise's power in every hertz the same, so that "
            "the total noise grows. At first the tone gets harder to hear: more noise, more masking. "
            "<bookmark mark='b'/> But past a certain width, adding noise makes no difference at all. The tone is "
            "exactly as easy to hear as before. <bookmark mark='c'/> Fletcher's reading: the ear listens for the "
            "tone through a filter, and noise that falls outside the filter does not count. He called its width "
            f"the critical band. This curve is Monochord's ear doing his experiment at a thousand hertz, and the "
            f"band comes out about {say(d['erb_1k'])} hertz wide."
        ) as vo:
            self.play(FadeIn(card), FadeIn(base), FadeIn(tone), FadeIn(noise), FadeIn(g))
            vo.wait_until("a")
            n = int(np.argmax(d["fletcher_bw"] > d["erb_1k"]))
            first = curve(g.ax, np.log10(d["fletcher_bw"][:n + 1]), d["fletcher_db"][:n + 1], EAR)
            self.play(w.animate.set_value(1.4), Create(first), run_time=max(vo.until("b") - 0.2, 1.0))
            rest = curve(g.ax, np.log10(d["fletcher_bw"][n:]), d["fletcher_db"][n:], EAR)
            self.play(w.animate.set_value(4.6), Create(rest), run_time=max(vo.until("c") - 0.2, 1.0))
            self.add(cu)
            self.remove(first, rest)
            self.play(Create(filt), FadeIn(fl), Create(knee), FadeIn(kl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def widths(self):
        d = load("bands")
        w = load("wave")
        g = faxes(100, 10000, [0, 1.1], x_length=7.4, y_length=2.7, ylabel=r"three of the ear's filters", yticks=[], font_size=20)
        g.move_to(LEFT * 2.6 + UP * 1.45)
        cols = (AIR, TUNE, BAD)
        shapes = VGroup(*[fcurve(g, d["f"], 10 ** (d[f"shape_{int(r['hz'])}"] / 20), col) for r, col in zip(d["widths"], cols)])
        form = MathTex(r"\text{width} \;=\; 24.7\,\bigl(4.37\,f_{\text{kHz}} + 1\bigr)\ \text{Hz}", font_size=32).move_to(RIGHT * 4.0 + UP * 2.3)
        src = label(r"Glasberg and Moore (1990)", font_size=20, color=GREY_B).next_to(form, DOWN, buff=0.15)
        table = VGroup(*[VGroup(label(rf"at ${hz_name(r['hz'])}$ Hz:", font_size=26, color=col), label(rf"{r['erb']:.0f} Hz wide", font_size=26),
                                label(rf"= \ {r['semitones']:.1f} semitones", font_size=26, color=RATIO)).arrange(RIGHT, buff=0.3)
                         for r, col in zip(d["widths"], cols)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 2.6 + DOWN * 1.35)
        for row in table:
            row[2].set_opacity(0)
        ask = pause_card(r"At 1000 Hz the band is 133 Hz wide: \ from 934 to 1066 Hz. \\ How big is that as a musical interval?", width=6.2).move_to(RIGHT * 3.6 + DOWN * 1.3)
        r1 = d["widths"][1]
        ans = VGroup(MathTex(r"\tfrac{1066}{934} = 1.14", font_size=32), MathTex(rf"12\log_2 1.14 = {r1['semitones']:.1f}\ \text{{semitones}}", font_size=32, color=GOOD)
                     ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.9 + DOWN * 0.9)
        per = w["inner"] * d["mm_per_band"] / w["length_mm"]
        foot = label(rf"about {d['bands_to_16k']:.0f} bands side by side cover all of hearing; \ each is {d['mm_per_band']:.1f} mm of membrane, \ "
                     rf"about {round(per, -1):.0f} hair cells", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Fifty years of such experiments give a formula for the width at any frequency. "
            "<bookmark mark='a'/> At two hundred and fifty hertz the band is "
            f"{say(d['widths'][0]['erb'])} hertz wide. At a thousand, {say(r1['erb'])}. At four thousand, "
            f"{say(d['widths'][2]['erb'])}. In hertz they grow steadily. But music does not count in hertz. "
            "<bookmark mark='b'/> Take the band at a thousand hertz, from nine hundred and thirty-four to a "
            "thousand and sixty-six. Pause, and work out how big that is as a musical interval."
        ) as vo:
            self.play(FadeIn(form), FadeIn(src), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in shapes], lag_ratio=0.4), LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.4), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "The ratio of the two edges is one point one four, and twelve times its logarithm to base two is "
            f"{say(r1['semitones'], 1)} semitones: a little more than a whole tone. <bookmark mark='a'/> Do the "
            f"same for the others. At four thousand hertz, {say(d['widths'][2]['semitones'], 1)} semitones, nearly "
            "the same. Through the middle and the top of its range the ear's filter is a fixed musical interval "
            "wide: the constant-Q ruler of Part 3 was the right guess. <bookmark mark='b'/> But at two hundred and "
            f"fifty hertz the band is {say(d['widths'][0]['semitones'], 1)} semitones, more than a minor third, "
            "and lower down it is wider still. That is the bend in the map of the last chapter, and it is why "
            "two notes close together in the bass sound thick and muddy, while the same two notes sound clean "
            "three octaves up. <bookmark mark='c'/> Lay these bands side by side and about "
            f"{say(d['bands_to_16k'])} of them cover the whole of hearing. Each is a little under a millimetre "
            f"of membrane, and holds about {say(round(per, -1))} hair cells."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans), table[1][2].animate.set_opacity(1))
            vo.wait_until("a")
            self.play(table[2][2].animate.set_opacity(1))
            vo.wait_until("b")
            self.play(table[0][2].animate.set_opacity(1), Indicate(shapes[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("bands")
        c = clip("bands.pairs")
        gaps = d["gaps"]
        q = listen_card(r"Three pairs of pure tones. \ Each pair sounds together. \\ In which pairs do you hear two separate tones?",
                        width=9.6).to_edge(UP, buff=0.45)
        bx = boxes((r"1", r"2", r"3"), buff=0.9, width=3.3, height=2.2, font_size=30).move_to(DOWN * 0.7)
        for b, gap in zip(bx, gaps):
            b[1].become(label(rf"1000 Hz \ + \ {1000 + gap:.0f} Hz", font_size=24, color=GREY_A).next_to(b[0], DOWN, buff=0.15))
        with self.voiceover(
            "You can hear a critical band for yourself. Three pairs of pure tones follow. In each, the lower tone "
            "is a thousand hertz, and the two sound together. The question is simple: in which pairs do you hear "
            "two separate tones?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"three pairs of tones", kind="synthesized", detail=r"1000 Hz and a second tone above it", corner=DL, tag_corner=DR)
            for ev, b, gap in zip(("beats", "rough", "two"), bx, gaps):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                box = b[0]
                shape = VMobject(stroke_color=TUNE, stroke_width=2, fill_color=TUNE, fill_opacity=0.45)
                snd.show(shape)

                def draw(m, t, box=box, gap=gap, t0=t0):
                    xs = np.linspace(-0.5, 0.5, 240)
                    span = 0.5 if gap < 20 else 0.12
                    tt = t + xs * span
                    e = np.abs(np.cos(np.pi * gap * tt)) if gap < 100 else 0.64 + 0.03 * np.sin(60 * tt)
                    on = 1.0 if t0 <= t < t0 + 1.8 else 0.0
                    w, h = box.width * 0.9, box.height * 0.36
                    top = [box.get_center() + RIGHT * w * x + UP * h * v * on for x, v in zip(xs, e)]
                    bot = [box.get_center() + RIGHT * w * x + DOWN * h * v * on for x, v in zip(xs[::-1], e[::-1])]
                    m.set_points_as_corners(top + bot + top[:1])

                snd.drive(shape, draw)
                snd.wait_until(t0 + 1.85)
        g = axes([700, 1600], [0, 1.15], x_length=8.4, y_length=2.3, xlabel=r"frequency (Hz)", ylabel=r"", xticks=[800, 1000, 1200, 1400, 1600], yticks=[], font_size=20)
        g.move_to(DOWN * 1.0)
        fsel = (d["f"] > 700) & (d["f"] < 1600)
        bell = curve(g.ax, d["f"][fsel], 10 ** (d["shape_1000"][fsel] / 20), GOOD)
        lines = VGroup(Line(g.ax.c2p(1000, 0), g.ax.c2p(1000, 1.0), color=TUNE, stroke_width=5),
                       *[Line(g.ax.c2p(1000 + gp, 0), g.ax.c2p(1000 + gp, 1.0), color=col, stroke_width=5) for gp, col in zip(gaps, (AIR, BAD, GREY_A))])
        tags = VGroup(label(r"8 Hz apart: \ one tone, \ swelling 8 times a second: \ \textbf{beats}", font_size=26, color=AIR),
                      label(r"60 Hz apart: \ one harsh, \ buzzing tone: \ \textbf{roughness}", font_size=26, color=BAD),
                      label(r"400 Hz apart: \ two clean tones", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(UP * 1.6)
        bl = label(r"one band of the ear", font_size=22, color=GOOD).move_to(g.ax.c2p(1000, 1.0) + UP * 0.25 + LEFT * 1.6)
        with self.voiceover(
            "Only in the last. <bookmark mark='a'/> In the first pair the tones are eight hertz apart, and you hear "
            "one tone, swelling and fading eight times a second. Those are beats. <bookmark mark='b'/> In the "
            "second they are sixty hertz apart. It is still not two tones. It is one tone with a harsh buzz in it, "
            "and the name for that is roughness. <bookmark mark='c'/> In the third pair, four hundred hertz apart, "
            "the two tones separate and each sounds smooth. <bookmark mark='d'/> Here is why. The first two pairs "
            "sit inside a single band of the ear. The same hair cells receive both tones, and what they feel is "
            "the sum, rising and falling. The third pair lands in two different places. Keep the second sound in "
            "mind. Two partials inside one band, too far apart to beat slowly, too close to separate: that "
            "roughness is the physical root of dissonance, and it is the whole subject of Part 5."
        ) as vo:
            self.play(FadeOut(q), FadeOut(bx), FadeIn(g), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(tags[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[3]), FadeIn(tags[2]))
            vo.wait_until("d")
            self.play(Create(bell), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cochleagram(self):
        d = load("bands")
        c = clip("bands.phrase")
        pic = picture(d["cochleagram"], -50, 0, 7.0, 4.3).move_to(LEFT * 2.2 + DOWN * 0.1)
        head = label(r"the Tune's first phrase, \ as the cochlea delivers it", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        ylab = VGroup(label(r"apex: \ 80 Hz", font_size=20, color=GREY_B).next_to(pic.frame.get_corner(DL), LEFT, buff=0.12),
                      label(r"base: \ 6 kHz", font_size=20, color=GREY_B).next_to(pic.frame.get_corner(UL), LEFT, buff=0.12),
                      label(r"64 places", font_size=20, color=GREY_B).rotate(PI / 2).next_to(pic.frame, LEFT, buff=0.2))
        xlab = label(r"time", font_size=20, color=GREY_B).next_to(pic.frame, DOWN, buff=0.12)
        with self.voiceover(
            "Put sixty-four of these filters in a row, spaced as the ear spaces them, and feed them the first "
            "phrase of the Tune. This picture is the ear's own version of a spectrogram: time runs across, place "
            "along the membrane runs up."
        ):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(ylab), FadeIn(xlab))
        with self.listen(c) as snd:
            window(snd, r"the Tune's first phrase", detail=r"Part 1's string", corner=DR, tag_corner=UR)
            pic.playhead.set_opacity(1)
            snd.drive(pic.playhead, sweep(pic, d["cg_seconds"]))
        pic.playhead.set_opacity(0)
        res = d["resolved"]["130.8"]
        notes = VGroup(label(r"low partials: \\ one line each. \\ \textbf{Resolved.}", font_size=26, color=GOOD),
                       label(r"high partials: \\ several to a band. \\ \textbf{Unresolved.}", font_size=26, color=BAD),
                       MathTex(r"\text{partials are } f_0 \text{ apart;}", font_size=26), MathTex(r"\text{the band at partial } n", font_size=26),
                       MathTex(r"\text{is about } 0.11\,n f_0 \text{ wide}", font_size=26),
                       MathTex(r"\Rightarrow\ \text{resolved up to } n \approx 8", font_size=30, color=GOOD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        notes.move_to(RIGHT * 4.3 + DOWN * 0.1)
        notes[1].shift(UP * 0.0)
        with self.voiceover(
            "Look at one note. <bookmark mark='a'/> At the bottom its partials stand apart, one line each. The ear "
            "has resolved them, as Helmholtz's globes did. <bookmark mark='b'/> Higher up the lines run together "
            "into a smear. There the partials are packed several to a band, and the ear cannot pull them apart. "
            "<bookmark mark='c'/> Where is the border? The partials of a note are spaced by its fundamental. The "
            "band around the n-th partial is about eleven percent of that partial's frequency. So the band becomes "
            "wider than the spacing at about the eighth or ninth partial. <bookmark mark='d'/> For the low C of "
            f"our string, Monochord's count is {say(res)} resolved partials. Remember this number. The first eight "
            "partials of a note are heard one by one; the rest are heard as a crowd. That one fact will explain "
            "how you hear pitch, in chapter seven."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]), FadeIn(notes[4]))
            vo.wait_until("d")
            self.play(FadeIn(notes[5]))
        self.wait(0.3)
        self.clear_scene()
