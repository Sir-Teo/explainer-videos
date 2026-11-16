from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Section(SoundScene):
    def construct(self):
        chapter(self, 4, r"Sections and the chorus effect", r"Why do eight violins not sound like one loud violin?")
        self.arithmetic()
        self.hear()
        self.solo()
        self.chorus()
        self.sizes_()
        self.seating()
        self.sizes()

    # ------------------------------------------------------------------
    def arithmetic(self):
        d = load("section")
        x0 = -5.0
        def bar(v, col, y, txt):
            w = 0.35 * v
            return VGroup(Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                          label(txt, font_size=19, color=col).move_to([x0 + w + 0.3, y, 0], aligned_edge=LEFT))
        bars = VGroup(bar(d["coherent_gain_db"], EAR, 1.2, rf"eight players in perfect lockstep: \ +{d['coherent_gain_db']:.0f} dB \ (amplitudes add)"),
                      bar(d["incoherent_gain_db"], TUNE, 0.2, rf"eight independent players, \ in theory: \ +{d['incoherent_gain_db']:.0f} dB \ (powers add)"),
                      bar(d["gain_db"], BLUE, -0.8, rf"our section, \ measured: \ +{d['gain_db']:.1f} dB"))
        bars.scale_to_fit_width(min(bars.width, 12.6)).move_to(DOWN * 0.1)
        cap = label(r"twice the players: \ +3 dB, \ not +6; \ a section grows louder slowly", font_size=20, color=WHITE).to_edge(DOWN, buff=1.0)
        head = label(r"eight violins against one", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Eight violins are louder than one, but by how much? <bookmark mark='a'/> If eight players moved in perfect lockstep, their waves would add, eight times the amplitude, eighteen decibels. <bookmark mark='b'/> But real players are never exactly together: their pitches differ by a few cents and their vibratos drift, so their phases tend to decorrelate, so an incoherent-power approximation is useful: eight times the power, nine decibels. <bookmark mark='c'/> Our section of eight, each with its own small detuning, vibrato and timing, measures {d['gain_db']:.1f} decibels louder than one player. Under that approximation and equal individual levels, doubling the players adds about three decibels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*bars).copy().set_opacity(0.15)))
            for mark, b in zip("abc", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b))
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("section")
        c = clip("section.two")
        one = VGroup(Circle(radius=0.3, color=TUNE, fill_opacity=0.3), label(r"one violin", font_size=20, color=TUNE)).arrange(DOWN, buff=0.2)
        eight = VGroup(VGroup(*[Circle(radius=0.22, color=BLUE, fill_opacity=0.3) for _ in range(8)]).arrange_in_grid(rows=2, cols=4, buff=0.12),
                       label(r"eight violins", font_size=20, color=BLUE)).arrange(DOWN, buff=0.2)
        g = VGroup(one, eight).arrange(RIGHT, buff=2.0).move_to(UP * 0.3)
        cap = label(r"played at the same level, \ so only the difference in sound remains", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "So a section is not one loud player; it is a different sound. Here is a phrase on one violin, and then on eight, "
            "turned to the same level so that only the difference in sound remains. Listen for the shimmer in the second."
        ):
            self.play(FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"one, \ then eight", kind="synthesized", detail=r"additive, \ from the bowed-string spectrum", corner=DL, tag_corner=DR)
            pulse(snd, one, d["starts"]["one"], d["starts"]["eight"] - 0.3, buff=0.1)
            pulse(snd, eight, d["starts"]["eight"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chorus(self):
        items = [
            (r"the chorus effect: \ slightly different pitches beat against each other, \ many beats at once", WHITE),
            (r"the result: \ a smoother, \ wider sound; \ the vibrato of one player is hidden in the crowd", WHITE),
            (r"the same physics as Part 36's paired gamelan, \ and the piano's three strings of Part 7", WHITE),
            (r"studios fake it with a delay line whose delay wobbles: \ the chorus pedal \ (Part 49)", TUNE),
            (r"a section's sound, \ not its loudness, \ is why orchestras have sections", GREY_A),
        ]
        rows_scene(self, r"the chorus effect", items,
                   "That shimmer is the chorus effect. <bookmark mark='b'/> Slightly different pitches beat against each other, "
                   "many beats at once. <bookmark mark='c'/> The result is a smoother, wider sound, and one player's vibrato is "
                   "hidden in the crowd. <bookmark mark='d'/> It is the physics of Part 36's paired gamelan instruments and of the "
                   "piano's three strings in Part 7. <bookmark mark='e'/> Studios fake it with a delay line whose delay wobbles: "
                   "the chorus effect of Part 49. <bookmark mark='f'/> A section's sound, more than its loudness, is why "
                   "orchestras have sections.", marks="cdef")

    # ------------------------------------------------------------------
    def sizes(self):
        items = [
            (r"a modern string section: \ about 16 first violins, \ 14 second, \ 12 violas, \ 10 cellos, \ 8 basses", WHITE),
            (r"with wind complements varying by score, often two to four of each in a large modern orchestra: \ the strings are many because each is quiet", WHITE),
            (r"a solo violin against the section: \ the concerto's contrast is one against many", WHITE),
            (r"dividing a section \ (\textit{divisi}) \ thins it: \ half the players, \ 3 dB less, \ less shimmer", TUNE),
            (r"chapter 5: \ what happens when different instruments share a line", GREY_A),
        ]
        rows_scene(self, r"section sizes", items,
                   "This sets the orchestra's proportions. <bookmark mark='b'/> A modern string section has about sixteen first violins, fourteen seconds, twelve violas, ten cellos and eight basses, <bookmark mark='c'/> with wind complements varying by score, often two to four of each in a large modern orchestra: the strings are many because each is quiet. <bookmark mark='d'/> A solo violin against the section is the concerto's contrast, one against many. <bookmark mark='e'/> Dividing a section, divisi, thins it: half the players, three decibels less, and less shimmer. <bookmark mark='f'/> Chapter five turns to different instruments sharing one line.", marks="cdef")

    # ------------------------------------------------------------------
    def sizes_(self):
        d = load("sizes")
        c = clip("sizes.five")
        cells = VGroup()
        for n, lv in zip(d["players"], d["level_db"]):
            g = VGroup(*[Dot(radius=0.06, color=BLUE) for _ in range(n)]).arrange_in_grid(rows=2 if n > 2 else 1, buff=0.08)
            cells.add(VGroup(g, label(rf"{n}", font_size=20, color=WHITE), label(rf"+{lv:.1f} dB", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15))
        cells.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to(UP * 0.3)
        cap = label(r"each version played at the same level, \ so only the texture changes; \ the numbers are what the level would have risen", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Hear the chorus grow: one held note on one violin, then two, four, eight and sixteen, each version turned to "
            "the same level, so that only the texture changes. The numbers show how much louder each would have been: about "
            "three decibels for every doubling, not six."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"1, \ 2, \ 4, \ 8, \ 16 violins", kind="synthesized", detail=r"additive, \ from the bowed-string spectrum", corner=DL, tag_corner=DR)
            for k, t0 in enumerate(d["starts"]):
                pulse(snd, cells[k], t0, t0 + 2.0, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def seating(self):
        items = [
            (r"the usual modern plan: \ violins to the conductor's left, \ cellos and violas to the right, \ basses behind them", WHITE),
            (r"woodwinds in the centre behind the strings; \ brass and percussion at the back", WHITE),
            (r"older plans split first and second violins left and right, \ so their dialogues cross the stage", WHITE),
            (r"seating changes balance and blend: \ the hall mixes what the score separates", TUNE),
            (r"Part 55's rooms, \ and Part 43's ensembles, \ return to this", GREY_A),
        ]
        rows_scene(self, r"where the sections sit", items,
                   "Where the sections sit matters too. <bookmark mark='b'/> The usual modern plan puts the violins to the conductor's left, the cellos and violas to the right, and the basses behind them. <bookmark mark='c'/> The woodwinds sit in the centre behind the strings, with brass and percussion at the back. <bookmark mark='d'/> Older plans split the first and second violins left and right, so that their dialogues cross the stage. <bookmark mark='e'/> Seating changes balance and blend: the hall mixes what the score separates. <bookmark mark='f'/> Part 55's rooms and Part 43's ensembles return to this.", marks="cdef")

    # ------------------------------------------------------------------
    def solo(self):
        d = load("solo")
        c = clip("solo.two")
        one = VGroup(Circle(radius=0.32, color=TUNE, fill_color=TUNE, fill_opacity=0.5), label(r"one violin", font_size=20, color=TUNE)).arrange(DOWN, buff=0.2)
        vls = VGroup(*[Circle(radius=0.2, color=BLUE, fill_color=BLUE, fill_opacity=0.5) for _ in range(12)]).arrange_in_grid(rows=2, cols=6, buff=0.12)
        vcs = VGroup(*[Circle(radius=0.26, color="#A3E635", fill_color="#A3E635", fill_opacity=0.5) for _ in range(6)]).arrange(RIGHT, buff=0.12)
        tutti = VGroup(VGroup(vls, vcs).arrange(DOWN, buff=0.25), label(r"twelve violins and six cellos, \ an octave lower", font_size=20, color=BLUE)).arrange(DOWN, buff=0.2)
        cells = VGroup(one, tutti).arrange(RIGHT, buff=2.0).move_to(UP * 0.3)
        with self.voiceover(
            "The contrast of one against many is a resource in itself, the basis of the concerto. Hear a phrase on one "
            "violin, answered an octave lower by twelve violins and six cellos: the soloist's line is clear and personal, "
            "the section's broad and anonymous."
        ):
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"solo, \ then tutti", kind="synthesized", detail=r"additive, \ from the bowed-string spectrum", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["solo"], d["starts"]["tutti"] - 0.2, buff=0.1)
            pulse(snd, cells[1], d["starts"]["tutti"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()
