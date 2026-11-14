from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Piano(SoundScene):
    def construct(self):
        chapter(self, 8, r"The fortepiano and the metronome", r"What did the new instruments change?", extra=((1815, r"Maelzel's metronome"),))
        self.fortepiano()
        self.crescendo()
        self.mannheim()
        self.metronome()
        self.builders()
        self.period()
        self.debate()

    # ------------------------------------------------------------------
    def fortepiano(self):
        items = [
            (r"Cristofori's hammer harpsichord \ (Florence, \ about 1700) \ becomes the Viennese fortepiano", WHITE),
            (r"leather-covered hammers, \ a light action, \ five octaves: \ soft and loud by touch \ (Part 7)", WHITE),
            (r"the harpsichord could not make a crescendo; \ the fortepiano could", WHITE),
            (r"dynamics become part of the composition: \ \textit{p}, \ \textit{f}, \ \textit{sf}, \ crescendo", TUNE),
            (r"by Beethoven's late sonatas: \ six octaves and more, \ iron bracing coming", GREY_A),
        ]
        rows_scene(self, r"an instrument that can be soft and loud", items,
                   "The keyboard changed under the composers' hands. <bookmark mark='b'/> Bartolomeo Cristofori's harpsichord "
                   "with hammers, built in Florence around 1700, had become by the 1780s the Viennese fortepiano: "
                   "<bookmark mark='c'/> leather-covered hammers, a light action, five octaves, soft or loud by the touch "
                   "of the finger, as Part 7 simulated. <bookmark mark='d'/> A harpsichord cannot make a crescendo; the "
                   "fortepiano can, <bookmark mark='e'/> and dynamics became part of the composition, written into the score "
                   "as piano, forte, sudden accents and crescendos. <bookmark mark='f'/> By Beethoven's last sonatas the "
                   "instrument had six octaves and more, and iron bracing was on its way.", marks="cdef")

    # ------------------------------------------------------------------
    def crescendo(self):
        d = load("dynamics")
        c = clip("piano.crescendo")
        notes = d["notes"]
        g = mroll(notes, width=11.0, height=2.0, lo=70, hi=84, total=max(n[1] + n[2] for n in notes)).move_to(DOWN * 0.1)
        for b, v in zip(g.notes, d["velocity"]):
            b.set_opacity(0.3 + 0.7 * (v - 0.5) / 1.4)
        head = label(r"one phrase, \ three times, \ a long crescendo", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        cap = label(r"the hammer strikes faster: \ louder, \ and brighter \ (Part 7: \ more high partials)", font_size=22, color=GREY_A).next_to(g, DOWN, buff=0.45)
        with self.voiceover(
            "This is what the harpsichord could not do. The Tune's first phrase three times on Part 7's piano, the hammer "
            "striking a little faster on every note: a long crescendo. Listen for the tone brightening as it grows louder, "
            "because a faster hammer excites more of the string's high partials."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a crescendo", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in notes], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def metronome(self):
        items = [
            (r"1815: \ Johann Nepomuk Maelzel patents the metronome \ (after Winkel's design)", WHITE),
            (r"1817: \ Beethoven publishes metronome marks for his first eight symphonies", WHITE),
            (r"for the first time a composer's tempo is a number", TUNE),
            (r"many of the marks are very fast: \ faster than most performers have played them", WHITE),
            (r"was his metronome broken? \ did he misread it? \ did he mean them?", EAR),
        ]
        rows_scene(self, r"tempo as a number", items,
                   "A machine changed tempo too. <bookmark mark='b'/> In 1815 Johann Nepomuk Maelzel patented the "
                   "metronome, borrowing the design of the Dutch inventor Dietrich Winkel. <bookmark mark='c'/> In 1817 "
                   "Beethoven published metronome marks for his first eight symphonies, <bookmark mark='d'/> and for the "
                   "first time a composer's tempo was a number rather than a word. <bookmark mark='e'/> Many of the marks "
                   "are very fast, faster than most performers have dared, <bookmark mark='f'/> and the argument about them "
                   "has run for two centuries.")

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"hypothesis 1: \ the metronome was faulty", WHITE),
            (r"hypothesis 2: \ he read the wrong edge of the weight, \ or misjudged in his deafness", WHITE),
            (r"hypothesis 3: \ he meant them, \ and later performers slowed down", WHITE),
            (r"the evidence: \ marks in many works, \ the machine's mechanics, \ others' marks of the time", TUNE),
            (r"a statistical study of all his marks \ (Martín-Castro and Ucar, \ 2020) \ found a consistent slowing of about 12 beats a minute", GREY_A),
        ]
        rows_scene(self, r"Beethoven's puzzling marks", items,
                   "There are three kinds of explanation. <bookmark mark='b'/> The machine was faulty; "
                   "<bookmark mark='c'/> or Beethoven misread it, perhaps reading the scale at the wrong edge of the "
                   "sliding weight, or misjudged because of his deafness; <bookmark mark='d'/> or he meant the marks, and "
                   "later performers slowed down. <bookmark mark='e'/> The evidence is the marks themselves, across many "
                   "works, the mechanics of the machine, and other composers' marks of the time. <bookmark mark='f'/> A "
                   "statistical study published in 2020 compared his marks with tempos in recordings and argued for a "
                   "systematic misreading worth about twelve beats a minute. The film could not obtain that study's data "
                   "to recompute it; it stays here as a claim to check, which is what the problems at the end ask.", marks="cdef")

    # ------------------------------------------------------------------
    def builders(self):
        items = [
            (r"Viennese pianos \ (Stein, \ Walter): \ light action, \ clear, \ quick decay", WHITE),
            (r"English pianos \ (Broadwood): \ heavier action, \ fuller, \ longer tone", WHITE),
            (r"Haydn in London writes for the English sound; \ Beethoven owns a Broadwood from 1818", WHITE),
            (r"the instrument shapes the writing: \ held pedal, \ long lines, \ big chords", TUNE),
            (r"Part 7's piano model is closer to the modern grand: \ an anachronism the film admits", GREY_A),
        ]
        rows_scene(self, r"two kinds of piano", items,
                   "There were two kinds of piano. <bookmark mark='b'/> Viennese makers like Johann Andreas Stein and Anton Walter built a light action and a clear, quickly fading tone. <bookmark mark='c'/> English makers like John Broadwood built a heavier action and a fuller, longer tone. <bookmark mark='d'/> Haydn wrote for the English sound in London, and Beethoven owned a Broadwood from 1818. <bookmark mark='e'/> The instrument shapes the writing: a longer tone allows held pedal, long lines, bigger chords. <bookmark mark='f'/> The piano model of Part 7 used in this film is closer to a modern grand, an anachronism worth admitting.", marks="cdef")

    # ------------------------------------------------------------------
    def mannheim(self):
        items = [
            (r"Mannheim, \ 1750s--1770s: \ the most disciplined orchestra in Europe", WHITE),
            (r"the `Mannheim crescendo': \ a long rise from soft to loud over a repeated figure", WHITE),
            (r"the symphony: \ strings, \ pairs of oboes and horns, \ then flutes, \ clarinets, \ trumpets, \ drums", WHITE),
            (r"Mozart heard them in 1777 and wrote home about the clarinets", TUNE),
            (r"dynamics as an effect of the whole orchestra, \ not one instrument", GREY_A),
        ]
        rows_scene(self, r"the orchestra grows", items,
                   "The orchestra changed too. <bookmark mark='b'/> At Mannheim, the court of the Elector Palatine kept an orchestra famous across Europe for its discipline. <bookmark mark='c'/> Its signature was the crescendo: a long rise from soft to loud over a repeated figure, which visitors described as overwhelming. <bookmark mark='d'/> The symphony orchestra grew from strings with pairs of oboes and horns to include flutes, clarinets, trumpets and drums. <bookmark mark='e'/> Mozart heard the Mannheim players in 1777, and wrote to his father wishing that Salzburg had clarinets. <bookmark mark='f'/> Loud and soft became an effect of the whole orchestra, not of one instrument.", marks="cdef")

    # ------------------------------------------------------------------
    def period(self):
        items = [
            (r"from the 1960s and 70s: \ period instruments and the old treatises \ (Part 25)", WHITE),
            (r"Mozart on a Viennese fortepiano: \ lighter, \ clearer, \ faster to fade", WHITE),
            (r"gut strings, \ lighter bows, \ vibrato as an ornament: \ a leaner quartet", WHITE),
            (r"some things cannot be recovered: \ the rooms, \ the audiences, \ their ears", TUNE),
            (r"Part 7 can model an instrument; \ nothing here models a listener of 1790", GREY_A),
        ]
        rows_scene(self, r"hearing it as it sounded", items,
                   "Can we hear this music as it sounded? <bookmark mark='b'/> From the 1960s and 70s, performers took up period instruments and the old treatises, as Part 25 described for the Baroque. <bookmark mark='c'/> Mozart's concertos on a Viennese fortepiano sound lighter and clearer than on a modern grand, each note fading sooner. <bookmark mark='d'/> Quartets on gut strings, with lighter bows and vibrato used as an ornament rather than all the time, sound leaner. <bookmark mark='e'/> But some things cannot be recovered: the rooms, the audiences, and the ears of people for whom this was the newest music. <bookmark mark='f'/> Part 7 can model an instrument. Nothing in this series models a listener of 1790.", marks="cdef")
