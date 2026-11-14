from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Tone(SoundScene):
    def construct(self):
        chapter(self, 11, r"Words and tune", r"What does speech do to a melody?")
        self.tones()
        self.speech()

    # ------------------------------------------------------------------
    def tones(self):
        d = load("tone")
        c = clip("tone.four")
        names = [(r"m\=a", r"mother"), (r"m\'a", r"hemp"), (r"m\v{a}", r"horse"), (r"m\`a", r"to scold")]
        cells = VGroup()
        curves = []
        for k, (syl, meaning) in enumerate(names):
            f = np.array(d["curves"][str(k + 1)])
            box = Rectangle(width=2.3, height=1.8, stroke_color="#3A4250", stroke_width=1.5)
            xs = np.linspace(-0.9, 0.9, len(f))
            ys = -0.7 + 1.4 * (np.log(f) - np.log(d["lo"])) / (np.log(d["hi"]) - np.log(d["lo"]))
            cv = VMobject(color=TUNE, stroke_width=5).set_points_smoothly([np.array([x, y, 0.0]) for x, y in zip(xs, ys)])
            curves.append(cv)
            cells.add(VGroup(VGroup(box, cv), label(syl, font_size=40, color=WHITE), label(meaning, font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.5).move_to(UP * 0.5)
        head = label(r"Mandarin: \ one syllable, \ four pitch shapes, \ four words", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A melody usually carries words, and words have melodies of their own. In Mandarin Chinese "
            "the syllable ma means mother, hemp, horse or to scold, depending on the shape of its pitch: "
            "level, rising, dipping or falling. Here are those four shapes on a single vowel, from Part "
            "8's voice."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.3), run_time=2.5)
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"four tones", detail=r"Part 8's voice, \ the vowel ah", corner=DL, tag_corner=DR)
            for k in range(4):
                pulse(snd, cells[k][0], st[k], st[k] + d["seconds"] + 0.25, buff=0.08)
        facts = VGroup(label(rf"Cantonese songs: \ tune and speech tones move the same way about {100 * d['cantonese_match']:.0f} times in a hundred", font_size=26, color=WHITE),
                       label(r"English songs: \ strong syllables on strong beats", font_size=26, color=WHITE),
                       label(r"every song is a negotiation between two melodies", font_size=30, color=TUNE)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So what happens when such a language is sung? The tune and the tones can collide, and a "
            "word can turn into another word. <bookmark mark='a'/> In Cantonese, which has six tones, "
            "songwriters avoid the collision: in a study of Cantonese songs by Patrick Wong and Randy "
            "Diehl, the melody moved in the same direction as the speech tones about nine times in "
            "ten. <bookmark mark='b'/> In English it is stress that a tune must respect: strong "
            "syllables on strong beats, as in Part 11. <bookmark mark='c'/> Every song is a negotiation "
            "between two melodies: the one in the music, and the one already in the words."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speech(self):
        xs = np.linspace(-4.5, 4.5, 80)
        ys = 0.9 * np.exp(-((xs + 2.2) / 1.6) ** 2) + 0.5 * np.exp(-((xs - 0.8) / 1.2) ** 2) - 0.14 * xs
        spoken = VMobject(color=WEAK, stroke_width=4).set_points_smoothly([np.array([x, y + 1.3, 0.0]) for x, y in zip(xs, ys)])
        steps = np.round(ys * 3) / 3
        sung = VGroup(*[Line([xs[i], steps[i] - 0.9, 0], [xs[i + 8], steps[i] - 0.9, 0], color=TUNE, stroke_width=6) for i in range(0, 72, 8)])
        ls = label(r"speech: \ pitch glides, \ and sinks through the sentence", font_size=26, color=GREY_A).next_to(spoken, UP, buff=0.25)
        lg = label(r"song: \ pitch holds still on each syllable, \ on the steps of a scale", font_size=26, color=TUNE).next_to(sung, DOWN, buff=0.3)
        with self.voiceover(
            "Even without tones, speech has a melody. Its pitch glides continuously, rises on the "
            "words that matter, and sinks through the sentence as the breath runs out: the same arch "
            "that we found in phrases. <bookmark mark='a'/> Song differs in two ways. The pitch holds "
            "still on each syllable, and the places where it holds are the steps of a scale. The line "
            "between the two is thin. Diana Deutsch found in 2011 that a spoken phrase, simply repeated "
            "a few times in a loop, begins to sound sung: the listener's own ear pulls the glides onto "
            "steps. Repetition, the mark of music in chapter 7, is enough to turn speech into melody."
        ) as vo:
            self.play(Create(spoken), FadeIn(ls), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in sung], lag_ratio=0.3), FadeIn(lg), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
