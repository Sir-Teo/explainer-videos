from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403

DRAW_C = ["#9B5DE5", "#9B5DE5", WHITE, WHITE, "#2B2D42", WHITE, "#2B2D42", "#2B2D42", WHITE]


def drawbar_set(reg, names, h=2.4, w=0.42, gap=0.75, size=15):
    """Nine drawbars pulled out by their settings (0 to 8), with their footages."""
    g = VGroup()
    for j, (s, nm) in enumerate(zip(reg, names)):
        slot = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.5).move_to([gap * j, 0, 0])
        col = [BLUE, BLUE, WHITE, WHITE, GOLD, WHITE, GOLD, GOLD, WHITE][j]
        bar = Rectangle(width=w * 0.8, height=max(h * s / 8, 0.04), stroke_width=0, fill_color=col, fill_opacity=0.85)
        bar.move_to(slot.get_top() + DOWN * bar.height / 2)
        g.add(VGroup(slot, bar, label(nm, font_size=size, color=GREY_A).next_to(slot, DOWN, buff=0.12), label(str(s), font_size=size + 2, color=WHITE).next_to(slot, UP, buff=0.1)))
    return g


class Additive(SoundScene):
    def construct(self):
        chapter(self, 1, r"Additive synthesis: \ dynamos and drawbars", r"Can any tone be built from sine waves?")
        self.partials()
        self.fourier()
        self.hammond()
        self.organ()
        self.tempered()
        self.cost()

    # ------------------------------------------------------------------
    def partials(self):
        d = load("partials")
        ph = np.array(d["phase"])
        ax = frame_axes(width=10.0, height=3.0, xlo=0, xhi=2, ylo=-1.3, yhi=1.3, center=DOWN * 0.5)
        Ns = ["1", "2", "3", "5", "10", "40"]
        curves = [curve(ph, d[n], ax.to, color=TUNE, width=3) for n in Ns]
        cap = [label(rf"{n} sine{'s' if n != '1' else ''}", font_size=22, color=TUNE).to_corner(UR, buff=0.6).shift(DOWN * 0.5) for n in Ns]
        eq = MathTex(r"y(t) = \frac{2}{\pi}\sum_{k=1}^{N} \frac{(-1)^{k+1}}{k}\,\sin(2\pi k f t)", font_size=34).to_edge(UP, buff=1.0)
        head = label(r"a sawtooth from sines", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Start with the oldest idea. A sine wave at the note's frequency, then one at twice it, at half the strength, "
            "<bookmark mark='a'/> then three times it at a third, <bookmark mark='b'/> five harmonics, <bookmark mark='c'/> "
            "ten, <bookmark mark='d'/> forty. The sum leans and sharpens into a sawtooth: a ramp up and a sudden drop. The "
            "ripples at the drop never quite go away; that is Gibbs's overshoot, nine per cent of the jump however many sines "
            "you add."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(ax), Create(curves[0]), FadeIn(cap[0]))
            self.play(Transform(curves[0], curves[1]), Transform(cap[0], cap[1]))
            vo.wait_until("a")
            self.play(Transform(curves[0], curves[2]), Transform(cap[0], cap[2]))
            vo.wait_until("b")
            self.play(Transform(curves[0], curves[3]), Transform(cap[0], cap[3]))
            vo.wait_until("c")
            self.play(Transform(curves[0], curves[4]), Transform(cap[0], cap[4]))
            vo.wait_until("d")
            self.play(Transform(curves[0], curves[5]), Transform(cap[0], cap[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        items = [
            (r"Fourier: \ any periodic wave is a sum of sines at whole multiples of its frequency \ (Part 3)", WHITE),
            (r"so a steady tone is a list of numbers: \ the level, \ and the phase, \ of each harmonic", WHITE),
            (r"for steady tones the ear mostly ignores the phases: \ the levels are the colour", WHITE),
            (r"additive synthesis turns the list back into sound: \ one sine for each number", TUNE),
            (r"the same list is what the hook's search was matching", GREY_A),
        ]
        rows_scene(self, r"a tone is a list", items,
                   "Fourier's theorem says this always works. <bookmark mark='b'/> Any periodic wave is a sum of sines at whole multiples of its frequency, as Part 3 showed. <bookmark mark='c'/> So a steady tone is a list of numbers: the level, and the phase, of each harmonic. <bookmark mark='d'/> For resolved harmonics in suitable steady tones, phase often has less influence than harmonic levels; phase can matter for unresolved components and waveform envelopes, as the same part found: the levels are the colour. <bookmark mark='e'/> Additive synthesis turns the list back into sound, one sine for each number. <bookmark mark='f'/> And the same list is what the hook's search was matching.", marks="bcdef")

    # ------------------------------------------------------------------
    def hammond(self):
        d = load("organ")
        bars = drawbar_set(d["regs"]["smith"], d["names"]).move_to(DOWN * 0.3 + LEFT * 2.6)
        rat = VGroup(*[label(f"{r:g}" if r != 1.5 else "1.5", font_size=14, color=GREY_A).next_to(bars[j][2], DOWN, buff=0.12) for j, r in enumerate(d["ratios"])])
        rl = label(r"times the note", font_size=14, color=GREY_A).next_to(rat, LEFT, buff=0.25)
        info = VGroup(label(r"1935: \ Laurens Hammond's organ", font_size=20, color=WHITE),
                      label(r"91 tonewheels on geared shafts, \ each beside a magnetic pickup", font_size=17, color=GREY_A),
                      label(r"a wheel's bumps make a near-sine at its pitch", font_size=17, color=GREY_A),
                      label(r"nine drawbars, \ each a harmonic, \ each in nine steps", font_size=17, color=GREY_A),
                      label(r"16' \ is an octave below; \ 8' \ the note; \ 4' \ an octave up", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        head = label(r"the Telharmonium in a cabinet", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In 1935 Laurens Hammond put the Telharmonium in a cabinet. <bookmark mark='a'/> A classic ninety-one-tone generator uses multiple geared shafts carrying steel tonewheels, each beside a magnetic pickup, and a wheel's bumps make a near-sine at its pitch. <bookmark mark='b'/> Nine drawbars mix them, each a harmonic, each in nine steps from silent to full. The names are organ-pipe lengths in feet: sixteen feet sounds an octave below the key, eight feet the key itself, four feet an octave up, and the odd ones, five and a third, two and two thirds, one and three fifths, one and a third, are the fifths and the third between."
        ) as vo:
            self.play(FadeIn(head), FadeIn(info[0]), FadeIn(ghost(bars, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(info[1]), FadeIn(info[2]))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(rat), FadeIn(rl), FadeIn(info[3]), FadeIn(info[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def organ(self):
        d = load("organ")
        c = clip("organ.three")
        regs = [("flute", r"8' alone: \ a flute"), ("smith", r"888000000: \ Jimmy Smith's"), ("full", r"all nine out")]
        sets = VGroup()
        for k, t in regs:
            b = drawbar_set(d["regs"][k], d["names"], h=1.6, w=0.26, gap=0.4, size=11)
            sets.add(VGroup(b, label(t, font_size=17, color=WHITE).next_to(b, UP, buff=0.35)))
        sets.arrange(RIGHT, buff=0.7).move_to(DOWN * 0.2)
        head = label(r"three registrations, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Three registrations on a computed Hammond, each playing the Tune's first phrase. The eight-foot drawbar alone, a "
            "pure flute. Then eight, eight, eight and the rest in: the first three drawbars full, the setting the jazz "
            "organist Jimmy Smith made famous. Then every drawbar out."
        ):
            self.play(FadeIn(head), FadeIn(sets))
        st = d["starts"]
        names = ["flute", "smith", "full"]
        with self.listen(c) as snd:
            window(snd, r"three registrations", kind="synthesized", detail=r"a computed Hammond", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, sets[i], st[k], end, buff=0.12)
        with self.voiceover(
            "The flute is hollow and soft; the three full drawbars add the octave below and the fifth, and the sound turns "
            "round and heavy; all nine out is bright and loud, the organ's full chorus. Nine numbers, nine colours each: "
            "nearly three hundred and ninety million registrations, all additive."
        ):
            self.play(Indicate(sets[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tempered(self):
        d = load("organ")
        rows = VGroup()
        hdr = VGroup(label(r"drawbar", font_size=18, color=GREY_A), label(r"true harmonic", font_size=18, color=GREY_A),
                     label(r"tonewheel used", font_size=18, color=GREY_A), label(r"error", font_size=18, color=GREY_A))
        rows.add(hdr)
        picks = [(1, r"5 1/3'", r"3 \ (of 16')", r"G, \ 7 semitones up"), (4, r"2 2/3'", r"3", r"G, \ 19 semitones up"),
                 (6, r"1 3/5'", r"5", r"E, \ 28 semitones up"), (7, r"1 1/3'", r"6", r"G, \ 31 semitones up")]
        for j, nm, h, wh in picks:
            cv = d["cents"][j]
            rows.add(VGroup(label(nm, font_size=20, color=WHITE), label(h, font_size=20, color=WHITE), label(wh, font_size=20, color=WHITE),
                            label(rf"{cv:+.1f} cents", font_size=20, color=EAR if abs(cv) > 5 else TUNE)))
        for r in rows:
            for i, m in enumerate(r):
                m.move_to([-5.0 + 3.3 * i, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.4)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-5.4 + 3.4 * i + m.width / 2)
        rows.move_to(DOWN * 0.2)
        head = label(r"harmonics borrowed from the scale", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"91 wheels serve every key: \ there is no wheel at the true fifth or third of each note", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"One economy hides in the Hammond's harmonics. <bookmark mark='a'/> Ninety-one wheels must serve every key, so there is no wheel at the true third harmonic of each note. Each drawbar borrows the wheel of the nearest note of the equal-tempered scale. <bookmark mark='b'/> The fifths come out {say(abs(d['cents'][4]), 1)} cents flat, a small offset whose audibility depends on the listening context; <bookmark mark='c'/> but the major third, the fifth harmonic, is {say(d['cents'][6], 1)} cents sharp, Part 6's tempered third. It beats slowly against the true harmonics of anything else in the room, and that slow shimmer is part of the Hammond's sound."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        items = [
            (r"real tones change: \ each harmonic of a piano or trumpet rises and dies on its own schedule \ (Parts 7 and 8)", WHITE),
            (r"Jean-Claude Risset at Bell Labs \ (1960s) \ resynthesized trumpet notes from measured harmonic envelopes", WHITE),
            (r"so additive synthesis needs a sine and an envelope for every harmonic: \ dozens of curves for one note", WHITE),
            (r"instruments that tried it, \ the Synclavier and Kawai's K5, \ asked players to draw them all", WHITE),
            (r"the cheaper road: \ start with every harmonic at once, \ and take away", TUNE),
        ]
        rows_scene(self, r"what additive synthesis costs", items,
                   "Additive synthesis has a price. <bookmark mark='b'/> Real tones change: each harmonic of a piano or a trumpet "
                   "rises and dies on its own schedule, as Parts 7 and 8 measured. <bookmark mark='c'/> In the 1960s Jean-Claude Risset at "
                   "Bell Labs resynthesized trumpet notes from measured envelopes of their harmonics, and they sounded like "
                   "trumpets. <bookmark mark='d'/> So additive synthesis needs a sine and an envelope for every harmonic: dozens of "
                   "curves for one note. <bookmark mark='e'/> Instruments that tried it, the Synclavier and Kawai's K5, asked "
                   "players to draw them all. <bookmark mark='f'/> The cheaper road starts with every harmonic at once, and takes "
                   "away.", marks="bcdef")
