from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Music(VoiceoverScene):
    def construct(self):
        self.card()
        self.roughness()
        self.listen()
        self.culture()

    def card(self):
        card = chapter_card(8, r"Music", r"Why do some chords sound rough?",
                            lit={1965: r"Plomp \& Levelt", 2016: r"McDermott"}, part=PART, scale=("mind", "culture"),
                            marr=("what",))
        with self.voiceover("Chapter eight. Music."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def roughness(self):
        d = load("music")
        head = heading(r"Roughness, \ and the simple ratios")
        A = axes([1.0, 2.05], [0, 1.05], x_length=8.4, y_length=3.5, xticks=[1.0, 1.25, 1.5, 1.75, 2.0], yticks=[0, 0.5, 1],
                 xlabel=r"frequency ratio of the two notes", ylabel=r"sensory roughness", center=[-1.6, 0.8, 0])
        ax = A.ax
        c = curve(ax, d["ratio"], d["diss"], SOUND, stroke_width=4)
        marks = VGroup()
        for name, r in zip(d["names"], d["ratios_named"]):
            if name in ("unison",):
                continue
            y = float(np.interp(r, d["ratio"], d["diss"]))
            col = BAD if name == "tritone" else TIMING
            dot = Dot(ax.c2p(r, y), color=col, radius=0.06)
            lab = label(name, font_size=18, color=col).next_to(dot, UP if name in ("tritone", "octave") else DOWN, buff=0.12)
            marks.add(VGroup(dot, lab))
        rows = rows_of([
            (r"two tones within one auditory filter beat against each other: \ heard as roughness", WHITE),
            (r"Plomp and Levelt, \ 1965: \ roughest at about a quarter of a critical band apart", PLACE),
            (r"for notes with harmonics, \ add up every pair: \ dips at the simple ratios, \ 5:4, \ 4:3, \ 3:2, \ 2:1", TIMING),
        ], 12.4, 26, 0.26).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: \ six harmonics each, \ Plomp and Levelt's curve in Sethares's form")
        with self.voiceover(
            "Why do some combinations of notes sound smooth and others rough? <bookmark mark='a'/> Part of the answer "
            "is in the cochlea. Two pure tones close enough to fall into the same auditory filter beat against each "
            "other, and fast beating is heard as roughness. <bookmark mark='b'/> Reinier Plomp and Willem Levelt "
            "measured it in 1965: two pure tones sound roughest when they're about a quarter of a critical band "
            "apart, and smooth once they're a full band apart. <bookmark mark='c'/> Real notes have harmonics. Add up "
            "the roughness of every pair of harmonics from two such notes, and plot it against the ratio of their "
            "fundamentals. The curve dips at exactly the ratios Western music calls consonant: the major third, five to "
            "four; the fourth, four to three; the fifth, three to two; the octave, two to one. At those ratios, the "
            "harmonics of the two notes coincide instead of rubbing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3), FadeIn(rows[2]), run_time=4.0)
        self.clear_scene()

    def listen(self):
        head = heading(r"On you: \ a fifth, \ then a tritone")
        rows = rows_of([
            (r"a fifth: \ 220 and 330 Hz, \ a ratio of 3:2", TIMING),
            (r"a tritone: \ 220 and 311 Hz, \ a ratio of $\sqrt{2}$", BAD),
            (r"to most listeners raised on Western music, \ the second sounds rougher and tenser", YOU),
        ], 11.8, 32, 0.5).move_to([0, -0.2, 0])
        tag = psyche_tag(r"computed: \ two harmonic tones, \ six harmonics each")
        with self.voiceover("Here are two of them. First a fifth, three to two. Listen.") as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
        play(self, "fifth")
        with self.voiceover("Now a tritone, an irrational ratio, the square root of two."):
            self.play(FadeIn(rows[1]))
        play(self, "tritone")
        with self.voiceover(
            "To most listeners raised on Western music, the second sounds rougher and less settled. The question is "
            "whether that's the cochlea talking, or the culture."
        ):
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def culture(self):
        head = heading(r"Roughness is universal; \ the preference is not")
        rows = rows_of([
            (r"2016: \ McDermott and colleagues play chords to the Tsimane', \ in the Bolivian Amazon", WHITE),
            (r"their own music is mostly sung one voice at a time, \ with little harmony", GREY_A),
            (r"they rated consonant and dissonant chords as equally pleasant", TIMING),
            (r"but they disliked roughness, \ like everyone tested: \ the cochlea's part is shared", PLACE),
            (r"the preference for consonance seems to be learned from a musical culture", PRIOR),
        ], 12.6, 29, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.MCDERMOTT_2016.cite)
        with self.voiceover(
            "In 2016, Josh McDermott and colleagues took the question to the Tsimane', who live in the Bolivian "
            "Amazon. <bookmark mark='a'/> They played them chords and asked how pleasant each one was. "
            "<bookmark mark='b'/> Tsimane' music is mostly sung by one voice at a time, with little harmony. "
            "<bookmark mark='c'/> They rated consonant and dissonant chords as equally pleasant, while Bolivians in "
            "towns and cities, and Americans, preferred consonance, in that order. <bookmark mark='d'/> But the "
            "Tsimane' did dislike acoustic roughness, as everyone tested does. The cochlea's part is shared. "
            "<bookmark mark='e'/> The preference for consonant chords seems to be learned from a musical culture. "
            "It's one study, in one society, and it's been argued over; Philosophy, Built returns to roughness and "
            "taste in its Part 40."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
