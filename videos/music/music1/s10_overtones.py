from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (EAR, FREQ, GOOD, HIST, PART, RATIO, STR, TIME, TUNE, clip, flat_name, load,
                                        ring, say, window)


class Overtones(SoundScene):
    def construct(self):
        self.card()
        self.heard()
        self.each()
        self.find()
        self.timbre()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"One string is a chord", r"Do we actually hear the modes?", lit=(1636, 1701), part=PART)
        with self.voiceover("Chapter nine. One string is a chord."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def spectrogram(self, c, width=7.0, height=4.4):
        d = load("overtones")
        marks = [(row["hz"], str(row["n"])) for row in d["table"][:8]]
        return Spectrogram(c, width=width, height=height, fmax=1150.0, marks=marks, db_range=(-60.0, -4.0))

    # ------------------------------------------------------------------
    def heard(self):
        c = clip("overtones.whole")
        sp = self.spectrogram(c, width=7.2, height=4.2).move_to(RIGHT * 2.6 + DOWN * 0.5)
        mono = MonochordView(width=6.6, ruler=False).move_to(RIGHT * 2.6 + UP * 0.2)
        hum = mono.lens(1.0, amp=0.22)
        ax = VGroup(label(r"time $\rightarrow$", font_size=22, color=GREY_B).next_to(sp.frame, DOWN, buff=0.45),
                    label(r"frequency $\rightarrow$", font_size=22, color=GREY_B).rotate(PI / 2).next_to(sp.frame, LEFT, buff=0.75),
                    label(r"brighter $=$ louder", font_size=22, color=GREY_B).next_to(sp.frame, UP, buff=0.15))
        card = history_card(1636, r"Mersenne", r"hears, \ in one string, \ at least four higher notes sounding with "
                            r"the main one. \ He cannot explain it.", width=4.0).to_corner(UL, buff=0.35)
        card2 = history_card(1701, r"Joseph Sauveur", r"the string swings in all its modes at once. \ He names the "
                             r"\emph{harmonics}, \ the \emph{nodes}, \ and the science: \ \emph{acoustics}.",
                             width=4.0).next_to(card, DOWN, buff=0.3)
        with self.voiceover(
            "In 1636 Mersenne wrote down something odd. When he listened closely to one string he heard, besides "
            "its own note, at least four higher notes sounding with it. He could not explain them. "
            "<bookmark mark='a'/> Sixty-five years later Joseph Sauveur could: the string is swinging in all its "
            "modes at once, and each mode sings its own note. <bookmark mark='b'/> We can look at that directly. "
            "This picture is called a spectrogram. Time runs to the right, frequency runs upward, and brightness "
            "is loudness. Every horizontal line is one mode of the string. Here is a single pluck."
        ) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.2), FadeIn(mono), FadeIn(hum))
            vo.wait_until("a")
            self.play(FadeIn(card2, shift=RIGHT * 0.2))
            vo.wait_until("b")
            sp.playhead.set_opacity(0)
            self.play(FadeOut(mono), FadeOut(hum), FadeIn(sp), FadeIn(ax))
        with self.listen(c) as snd:
            window(snd, r"one pluck", corner=DL)
            sp.playhead.set_opacity(1)
            snd.drive(sp.playhead, sp.follow())
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def each(self):
        d = load("overtones")
        c = clip("overtones.each")
        whole = clip("overtones.whole")
        sp = self.spectrogram(whole, width=6.2, height=4.6).move_to(LEFT * 3.2 + DOWN * 0.3)
        sp.playhead.set_opacity(0)
        head = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"partial", r"hertz", r"nearest note")])
        xs = [1.2, 2.8, 4.9]
        rows = VGroup()
        for i, row in enumerate(d["table"][:8]):
            off = rf"\ ({row['cents']:+.0f} cents)" if abs(row["cents"]) >= 5 else ""
            r = VGroup(MathTex(str(row["n"]), font_size=36, color=harmonic_color(row["n"])),
                       label(say(row["hz"], 1), font_size=28, color=FREQ),
                       label(flat_name(row["note"]) + off, font_size=28, color=harmonic_color(row["n"])))
            for cell, x in zip(r, xs):
                cell.move_to([x, 2.0 - 0.56 * (7 - i), 0])
            r[2].align_to([xs[2] - 0.7, 0, 0], LEFT)
            rows.add(r)
        for h, x in zip(head, xs):
            h.move_to([x, 2.6, 0])
        with self.voiceover(
            "Now take the pluck apart. Each line of the spectrogram is one partial, and we can play them one at a "
            "time, each at the same loudness, from the bottom up. The table says what note each one is nearest to."
        ):
            self.play(FadeIn(sp), FadeIn(head))
        with self.listen(c) as snd:
            window(snd, r"partials 1 to 8, \ one at a time", detail=r"each raised to the same loudness")
            for row, r in zip(d["table"][:8], rows):
                snd.wait_until(f"p{row['n']}")
                band = Rectangle(width=sp.frame.width, height=0.2, stroke_color=harmonic_color(row["n"]), stroke_width=2,
                                 fill_color=harmonic_color(row["n"]), fill_opacity=0.15)
                band.move_to([sp.frame.get_x(), sp.y_of(row["hz"]), 0])
                snd.show(band)
                self.play(FadeIn(r), run_time=0.25)
                self.wait(0.5)
                self.remove(band)
        chord = SurroundingRectangle(VGroup(rows[3], rows[4], rows[5]), color=TUNE, buff=0.12, corner_radius=0.1,
                                     stroke_width=2)
        ctag = label(r"C, \ E, \ G: \ a major chord", font_size=30, color=TUNE).move_to([3.2, -2.75, 0])
        e5, b5 = d["table"][4], d["table"][6]
        with self.voiceover(
            f"Read the names. {d['open_note'][0]}, an octave above it, then a G, then another C. "
            "<bookmark mark='a'/> Partials four, five and six are C, E and G: a major chord, the most familiar chord "
            "in Western music, and it is sitting inside every string that has ever been plucked. "
            f"<bookmark mark='b'/> The fit to the piano's notes is close but not exact. The E is "
            f"{say(abs(e5['cents']))} cents flat of the piano's E, and the seventh partial falls "
            f"{say(abs(b5['cents']))} cents below B flat, in a crack between the keys. Part 6 is about that crack."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(chord), FadeIn(ctag))
            vo.wait_until("b")
            self.play(Indicate(rows[4][2], color=TUNE), Indicate(rows[6][2], color=TUNE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def find(self):
        d = load("overtones")
        c = clip("overtones.find")
        whole = clip("overtones.whole")
        q = listen_card(r"First the third partial, \ alone and quiet. \ Hold it in your head. \\ "
                        r"Then the pluck. \ Can you still hear that note inside it?", width=9.6).to_edge(UP, buff=0.45)
        sp = self.spectrogram(whole, width=7.4, height=3.6).move_to(DOWN * 1.2)
        sp.playhead.set_opacity(0)
        hz3 = d["table"][2]["hz"]
        band = Rectangle(width=sp.frame.width, height=0.2, stroke_color=harmonic_color(3), stroke_width=2.5,
                         fill_color=harmonic_color(3), fill_opacity=0.12).move_to([sp.frame.get_x(), sp.y_of(hz3), 0])
        with self.voiceover(
            "So why do you not hear a chord when someone plucks a string? Try this. I will play the third partial "
            "on its own, quietly. Hold on to it. Then the whole pluck."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(sp))
        with self.listen(c) as snd:
            window(snd, r"partial 3, \ then the pluck")
            snd.show(band)
            snd.wait_until("pluck")
            sp.playhead.set_opacity(1)
            t0 = snd.time_of("pluck")
            snd.drive(sp.playhead, lambda m, t: m.set_x(sp.x_of(t - t0)))
        sp.playhead.set_opacity(0)
        with self.voiceover(
            "Most people find that the note is there once they know where to listen, and that it is hard to stop "
            "hearing it afterwards. Organ builders and piano tuners train themselves to do this all day. "
            "<bookmark mark='a'/> But left alone, your hearing does something remarkable: it takes a dozen "
            "frequencies and reports one note. How and why it does that is the subject of Part 4."
        ) as vo:
            self.play(Indicate(band, color=TUNE, scale_factor=1.02))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timbre(self):
        d = load("overtones")
        t = d["table"]
        terms = VGroup(
            VGroup(label(r"\textbf{partial}", font_size=30, color=FREQ),
                   label(r"any one frequency in a sound", font_size=26, color=GREY_A)),
            VGroup(label(r"\textbf{fundamental}", font_size=30, color=harmonic_color(1)),
                   label(r"the lowest partial: \ the note we name", font_size=26, color=GREY_A)),
            VGroup(label(r"\textbf{harmonic}", font_size=30, color=GOOD),
                   label(r"a partial at a whole multiple of the fundamental", font_size=26, color=GREY_A)),
            VGroup(label(r"\textbf{overtone}", font_size=30, color=HIST),
                   label(r"a partial above the fundamental: \ the first overtone is the second harmonic", font_size=26,
                         color=GREY_A)),
            VGroup(label(r"\textbf{timbre}", font_size=30, color=TUNE),
                   label(r"what tells two sounds of the same pitch and loudness apart", font_size=26, color=GREY_A)),
        )
        for r in terms:
            r[0].move_to([-5.9, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.2, 0, 0], aligned_edge=LEFT)
        terms.arrange(DOWN, buff=0.34, aligned_edge=LEFT).to_edge(UP, buff=0.5)
        for r in terms:
            r[1].set_x(-3.2 + r[1].width / 2)
        bars = partial_bars([row["db"] for row in t[:10]], width=5.6, height=1.6, floor_db=-42.0).move_to(LEFT * 3.4 + DOWN * 2.35)
        life = partial_bars([row["t60"] for row in t[:10]], width=5.6, height=1.6, db=False).move_to(RIGHT * 3.4 + DOWN * 2.35)
        cap1 = label(r"how loud each partial starts", font_size=24, color=GREY_B).next_to(bars, UP, buff=0.15)
        cap2 = label(rf"how long each one lasts \ (from {t[0]['t60']:.0f} s down to {t[9]['t60']:.1f} s)", font_size=24,
                     color=GREY_B).next_to(life, UP, buff=0.15)
        with self.voiceover(
            "Some words. Any single frequency in a sound is a partial. <bookmark mark='a'/> The lowest is the "
            "fundamental. <bookmark mark='b'/> Partials at whole multiples of it are harmonics. "
            "<bookmark mark='c'/> An overtone is a partial above the fundamental, so the first overtone is the "
            "second harmonic. <bookmark mark='d'/> And timbre is what tells two sounds apart when their pitch and "
            "loudness are the same."
        ) as vo:
            self.play(FadeIn(terms[0]))
            for mark, r in zip("abcd", terms[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        with self.voiceover(
            "For our string, the timbre is two lists. How strongly each partial starts, which the plucking point "
            f"sets. <bookmark mark='a'/> And how long each one lasts. The fundamental rings for {say(t[0]['t60'])} "
            f"seconds; the tenth partial is gone in {say(t[9]['t60'], 1)}. That is why a plucked note starts bright "
            "and ends mellow. A note is not a frequency. It is a family of them, with a life in time. Now we can go "
            "back to Pythagoras with something he did not have."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(cap1))
            vo.wait_until("a")
            self.play(FadeIn(life), FadeIn(cap2))
        self.wait(0.3)
        self.clear_scene()
