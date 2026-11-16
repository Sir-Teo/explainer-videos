from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ what pitch, \ what tempo?", r"How do we know how this music sounded?")
        self.pitch()
        self.heard()
        self.instruments()
        self.tempo()
        self.problem()

    # ------------------------------------------------------------------
    def pitch(self):
        items = [
            (r"no standard pitch: \ the A above middle C ranged from about 390 to about 465 Hz", WHITE),
            (r"the evidence: \ surviving organs, \ woodwinds, \ tuning forks; \ Bruce Haynes's survey \ (2002)", WHITE),
            (r"`chamber pitch', \ `choir pitch', \ `French pitch': \ a whole tone apart and more", WHITE),
            (r"today's convention: \ A = 415 Hz for Baroque music, \ a semitone below 440", TUNE),
            (r"a compromise, \ not a fact: \ Bach's Leipzig organs were higher, \ Versailles lower", GREY_A),
        ]
        rows_scene(self, r"what pitch?", items,
                   "Every modern performance of this music must decide what the scores do not say. <bookmark mark='b'/> "
                   "There was no standard pitch: the A above middle C ranged from about three hundred and ninety hertz to "
                   "about four hundred and sixty-five, from place to place and from organ to orchestra. "
                   "<bookmark mark='c'/> The evidence is in surviving organs, woodwind instruments and, later, tuning forks, "
                   "gathered in Bruce Haynes's history of performing pitch. <bookmark mark='d'/> Musicians spoke of chamber "
                   "pitch, choir pitch and French pitch, a whole tone and more apart. <bookmark mark='e'/> Today's players "
                   "of Baroque music mostly use four hundred and fifteen, a semitone below the modern four hundred and "
                   "forty, <bookmark mark='f'/> which is a convenient modern standard that also lies near some historical pitch levels.", marks="cdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pitch")
        c = clip("frontier.pitch")
        rows_ = VGroup()
        for name, a4 in d["standards"]:
            rows_.add(VGroup(label(rf"A = {a4:.0f} Hz", font_size=26, color=TUNE if a4 == 415 else WHITE), label(name, font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.6))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.2)
        cap = label(r"from the lowest to the highest: \ about three semitones, a minor third", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is the range: one chord, A major, with its A tuned to three hundred and ninety-two, four hundred and "
            "fifteen, four hundred and forty, and four hundred and sixty-five hertz. From the lowest to the highest is "
            "about three semitones, a minor third. A singer whose part is comfortable at one is straining at the other."
        ):
            self.play(FadeIn(rows_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"four standards of pitch", detail=r"organ tones", kind="synthesized", corner=DL, tag_corner=DR)
            names = [n for n, _ in d["standards"]]
            for i, n in enumerate(names):
                end = d["starts"][names[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, rows_[i], d["starts"][n], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tempo(self):
        items = [
            (r"no metronome until 1815: \ tempo words, \ dance types, \ time signatures", WHITE),
            (r"Quantz \ (1752): \ measure tempo by the pulse, \ about 80 beats a minute", WHITE),
            (r"dance treatises give steps: \ a dance's tempo is a body's", WHITE),
            (r"the evidence disagrees: \ performances of the same Bach movement differ by half", TUNE),
            (r"historically informed performance: \ evidence plus taste, \ argued in public", GREY_A),
        ]
        rows_scene(self, r"what tempo?", items,
                   "Tempo is harder still. <bookmark mark='b'/> There was no metronome before 1815: composers wrote tempo "
                   "words, dance names and time signatures, and players knew the rest. <bookmark mark='c'/> Johann Joachim "
                   "Quantz, flautist to Frederick the Great, proposed in 1752 measuring tempo against the human pulse, "
                   "about eighty beats a minute. <bookmark mark='d'/> Dance treatises describe steps, and a dance's tempo is "
                   "the speed at which a body can do them. <bookmark mark='e'/> Yet recorded performances of the same Bach "
                   "movement differ in speed by half or more. <bookmark mark='f'/> Historically informed performance is the "
                   "art of combining this evidence with taste, and of arguing about it in public.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"instruments as data: \ every surviving Baroque organ and woodwind, \ its pitch measured", WHITE),
            (r"a statistical history of pitch: \ by place, \ by decade, \ by instrument type", WHITE),
            (r"tempo from documents: \ the durations recorded for services and operas", WHITE),
            (r"$\bigstar$ \ research problem: \ estimate the tempo range of a dance type from its treatises and timings", EAR),
            (r"and state the uncertainty, \ as a historian of the evidence would", TUNE),
        ])
        head = label(r"evidence, \ counted", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "These are questions that numbers can sharpen. <bookmark mark='a'/> Treat every surviving instrument as a data "
            "point, with its pitch measured, <bookmark mark='b'/> and a history of pitch becomes a statistical model, by "
            "place, by decade and by kind of instrument. <bookmark mark='c'/> Some documents record how long services, "
            "operas or ballets took, which bounds their tempos. <bookmark mark='d'/> Here is this part's research "
            "problem: estimate the range of tempos for one dance type, the sarabande, say, from its treatises and from "
            "documented timings, <bookmark mark='e'/> and say how uncertain the answer is, as any honest history of "
            "evidence must."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def instruments(self):
        items = [
            (r"gut strings, \ lighter bows, \ less tension: \ a softer, \ quicker sound", WHITE),
            (r"natural trumpets and horns: \ only the notes of the harmonic series \ (Part 8)", WHITE),
            (r"recorders and one-keyed flutes; \ oboes with few keys", WHITE),
            (r"surviving instruments, \ often altered later: \ evidence to read with care", TUNE),
            (r"copies made today test the treatises against what the instruments can do", GREY_A),
        ]
        rows_scene(self, r"the instruments themselves", items,
                   "The instruments are evidence too. <bookmark mark='b'/> Historical violins and bows varied; gut strings, setup and bow design affect response, and blanket claims of uniformly lower tension or softer sound are unreliable. <bookmark mark='c'/> Trumpets and horns had no valves and played only the notes of the harmonic series, as in Part 8. <bookmark mark='d'/> Flutes had one key, oboes few. <bookmark mark='e'/> Most surviving instruments were altered later to suit later music, so they must be read with care. <bookmark mark='f'/> Copies made today let players test what the treatises say against what the instruments can actually do.", marks="cdef")
