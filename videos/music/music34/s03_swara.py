from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Swara(SoundScene):
    def construct(self):
        chapter(self, 2, r"Swara and shruti", r"How many notes are in an octave?")
        self.swaras()
        self.shrutis()
        self.comma()
        self.quiz()
        self.measured()
        self.fixed()

    # ------------------------------------------------------------------
    def swaras(self):
        names = [("Sa", "S", 0), ("Re", "R", 2), ("Ga", "G", 4), ("Ma", "m", 5), ("Pa", "P", 7), ("Dha", "D", 9), ("Ni", "N", 11)]
        cells = VGroup(*[VGroup(label(n, font_size=30, color=TUNE if n in ("Sa", "Pa") else WHITE), label(s, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.15) for n, s, _ in names]).arrange(RIGHT, buff=0.8).move_to(UP * 1.0)
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"seven swaras: \ Sa Re Ga Ma Pa Dha Ni \ ---\ sung as \textit{sargam}", WHITE),
            (r"Sa and Pa are fixed; \ Re, \ Ga, \ Dha, \ Ni can be lowered \ (\textit{komal}), \ Ma raised \ (\textit{tivra})", WHITE),
            (r"twelve positions in all, \ as on the piano", TUNE),
            (r"written here: \ lower case for komal \ (r g d n), \ M' for tivra Ma, \ a dot for the lower octave", GREY_A))]).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        head = label(r"the seven swaras", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The notes are called swaras. <bookmark mark='a'/> There are seven, Sa, Re, Ga, Ma, Pa, Dha and Ni, sung as "
            "sargam, the way Western singers use do, re, mi. <bookmark mark='b'/> In this Hindustani naming scheme Sa and Pa have no komal or tivra variants; their sounding intonation and ornament still depend on practice. Re, Ga, Dha and Ni "
            "can be lowered, komal, and Ma can be raised, tivra. <bookmark mark='c'/> That gives twelve positions, like the "
            "piano's. <bookmark mark='d'/> In this film komal notes are written in lower case, tivra Ma with a mark, and a "
            "dot after a note means the octave below."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shrutis(self):
        d = load("shruti")
        L = 11.6
        line = Line(LEFT * L / 2, RIGHT * L / 2, color=GREY_B).move_to(UP * 0.4)
        ticks = VGroup()
        for r in d["rows"]:
            x = -L / 2 + L * r["cents"] / 1200
            ticks.add(VGroup(Line([x, 0.25, 0], [x, 0.85, 0], color=TUNE, stroke_width=3)))
        et = VGroup(*[Line([-L / 2 + L * k / 12, -0.35, 0], [-L / 2 + L * k / 12, 0.1, 0], color=BLUE, stroke_width=2) for k in range(13)])
        lab = VGroup(label(r"22 shrutis \ (one modern list of just ratios)", font_size=19, color=TUNE).next_to(line, UP, buff=0.7),
                     label(r"12 equal semitones", font_size=19, color=BLUE).next_to(line, DOWN, buff=0.6))
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"the \textit{N\=a\d{t}ya\'s\=astra} \ (about 2,000 years old) \ divides the octave into 22 shrutis", WHITE),
            (r"later writers read them as just ratios: \ two versions of Re, \ Ga, \ Dha, \ Ni, \ a comma apart", WHITE),
            (r"whether musicians ever sang 22 fixed pitches is disputed", TUNE))]).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"shruti: \ the finer divisions", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Between the twelve positions lies an old question. <bookmark mark='a'/> The Natyashastra, a treatise about two "
            "thousand years old, divides the octave into twenty-two shrutis. <bookmark mark='b'/> Later writers read them as "
            "just ratios, giving two versions of most notes, a comma apart, about twenty cents: here, one modern list, "
            "against twelve equal steps. <bookmark mark='c'/> Whether musicians ever sang twenty-two fixed pitches, or the "
            "shrutis described something else, is disputed among scholars."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks), FadeIn(et), FadeIn(lab))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("ga")
        c = clip("ga.quiz")
        card = listen_card(r"Ga held over the drone, \ twice: \ once at the equal-tempered major third, \ once at the pure 5:4. \ "
                           r"Which one beats against the drone, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Ga, the major third above Sa, held over the drone, twice: once at the piano's "
            "equal-tempered third, once at the pure ratio five to four. Which one beats, a shimmer against the drone, "
            "A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup(label(r"A", font_size=44, color=GREY_A), label(r"B", font_size=44, color=GREY_A)).arrange(RIGHT, buff=4.0).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["A"], d["starts"]["B"] - 0.6, buff=0.12)
            pulse(snd, cells[1], d["starts"]["B"], c.duration, buff=0.12)
        ans = VGroup(label(r"A: \ 400 cents, \ equal temperament: \ beats", font_size=21, color=EAR).next_to(cells[0], DOWN, buff=0.5),
                     label(r"B: \ 386 cents, \ 5:4: \ still", font_size=21, color=TUNE).next_to(cells[1], DOWN, buff=0.5))
        with self.voiceover(
            f"A beats. At four hundred cents, the tempered Ga's fourth partial and the drone's tenth miss each other by about {say(round(d['beat_hz']))} hertz, a fast shimmer. In this synthesis the five-to-four third aligns those particular partials and reduces their beating; this is not a single prescribed Ga for every raga. Against a drone, singers and string players can hear exactly where a note sits; the piano cannot adjust."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        items = [
            (r"Jairazbhoy and Stone \ (1963): \ measured the intonation of Hindustani musicians", WHITE),
            (r"they found no fixed system: \ the same note varied between performers and between ragas", WHITE),
            (r"later studies with pitch tracking \ (CompMusic, \ 2010s) \ found notes as regions, \ not points", WHITE),
            (r"a note's position depends on the raga and on the phrase: \ the same swara can sit higher in one raga than another", TUNE),
            (r"the real answer to `how many notes?' \ is in the ornaments \ (chapter 4)", GREY_A),
        ]
        rows_scene(self, r"intonation, \ measured", items,
                   "What do musicians actually do? <bookmark mark='b'/> In 1963 Nazir Jairazbhoy and A. W. Stone measured the "
                   "intonation of Hindustani musicians. <bookmark mark='c'/> They found no fixed system: the same note varied "
                   "between performers and between ragas. <bookmark mark='d'/> Later studies, with computer pitch tracking of many "
                   "recordings, found that notes are better described as regions than as points. <bookmark mark='e'/> Where a "
                   "note sits depends on the raga and on the phrase around it: the same swara can sit higher in one raga than in another. <bookmark mark='f'/> The real answer to how many "
                   "notes there are lies in the ornaments, chapter four.", marks="cdef")

    # ------------------------------------------------------------------
    def comma(self):
        d = load("comma")
        c = clip("comma.three")
        cells = VGroup(VGroup(label(r"Re \ = \ 9/8", font_size=30, color=TUNE), label(r"204 cents: \ two fifths up, \ an octave down", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"Re \ = \ 10/9", font_size=30, color=BLUE), label(r"182 cents: \ a pure third below a pure fourth... \ less", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"both, \ alternating", font_size=30, color=EAR), label(r"a comma apart: \ 21.5 cents", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        cells[1][1].become(label(r"182 cents: \ a pure major third \ less a whole tone of 9/8", font_size=18, color=GREY_A).move_to(cells[1][1]))
        head = label(r"two shrutis for Re, \ heard", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear two of the shrutis. Re as nine eighths, two hundred and four cents, reached by stacking fifths. Re as ten "
            "ninths, one hundred and eighty-two cents, the step left when a pure third is split into two unequal tones. Each "
            "over the drone, then the two alternating alone. They differ by the syntonic comma of Part 6, twenty-one and a "
            "half cents: small; audibility depends on the listener, duration, timbre and context."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"9/8, \ 10/9, \ both", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            ks = ["9/8", "10/9", "both"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixed(self):
        items = [
            (r"Sa and Pa: no komal/tivra variants\\intonation and ornament remain contextual", WHITE),
            (r"Pa is conventionally the fifth above Sa, often approached near the pure ratio: \ the drone's own second note", WHITE),
            (r"every other note is \textit{cala}: \ it has more than one form, \ and moves in gamaka", WHITE),
            (r"so the fixed frame is Sa--Pa--Sa, \ and everything else is placed against it", TUNE),
            (r"Part 5: \ the fifth is the most consonant interval after the octave", GREY_A),
        ]
        rows_scene(self, r"Sa and Pa as reference categories", items,
                   "Why are Sa and Pa never altered? <bookmark mark='b'/> They are called achala, immovable. <bookmark mark='c'/> Pa is conventionally the fifth above Sa, often approached near the pure ratio, the drone's own other note. <bookmark mark='d'/> Every other note is chala: it has more than one form, and can move in ornament. <bookmark mark='e'/> So the fixed frame is Sa, Pa and the upper Sa, and everything else is placed against it, <bookmark mark='f'/> resting on the consonance of the fifth from Part 5.", marks="cdef")
