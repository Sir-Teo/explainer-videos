from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Motet(SoundScene):
    def construct(self):
        chapter(self, 7, r"The motet", r"What happens when a clausula is given words?", extra=((1280, r"Franco of Cologne"),))
        self.words()
        self.three()
        self.franco()
        self.petrus()

    # ------------------------------------------------------------------
    def words(self):
        items = [
            (r"a clausula's upper voice is a long melisma: \ many notes, \ one syllable", WHITE),
            (r"give each of its notes a syllable of a new poem, \ and it becomes a `motet', \ from French \textit{mot}, \ word", WHITE),
            (r"then a third voice, \ with a third poem: \ two texts at once, \ often in two languages", WHITE),
            (r"Latin chant below, \ French love songs above: \ sacred and secular in one piece", TUNE),
            (r"the Montpellier Codex, \ copied about 1300, \ holds more than three hundred", GREY_A),
        ]
        rows_scene(self, r"a clausula with words", items,
                   "The clausulae of Notre Dame had a second life. <bookmark mark='b'/> The upper voice of a clausula is "
                   "a long melisma, many notes on one syllable. Someone put a new poem under it, one syllable to each "
                   "note, and the result was called a motet, probably from the French mot, a word. <bookmark mark='c'/> "
                   "Then a third voice was added with a third poem, so that two different texts are sung at once, often "
                   "in two different languages. <bookmark mark='d'/> Below, a fragment of Latin chant; above, French "
                   "poems about love, or politics, or the street cries of Paris. Sacred and secular in one piece, and "
                   "nobody could follow all the words. <bookmark mark='e'/> The Montpellier Codex, copied around 1300, "
                   "holds more than three hundred of them.")

    # ------------------------------------------------------------------
    def three(self):
        d = load("motet")
        c = clip("motet.three")
        vs = [d["triplum"], d["motetus"], d["tenor"]]
        g = voices_roll(vs, width=11.2, height=3.2, colors=[EAR, TUNE, GREY_A], bar_h=0.11).move_to(DOWN * 0.15)
        labs_ = VGroup(label(r"triplum: \ sixth mode, \ quick", font_size=18, color=EAR),
                       label(r"motetus: \ first mode", font_size=18, color=TUNE),
                       label(r"tenor: \ the chant, \ fifth mode, \ three longs and a rest", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.6).next_to(g, UP, buff=0.25)
        head = label(r"a three-voice motet \ (ours)", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the texture, computed for the film and sung on vowels instead of poems. Three layers at three "
            "speeds: the chant at the bottom in slow longs, grouped three at a time with a rest, a pattern called an "
            "ordo; the motetus in the first mode; and the triplum on top, quicker still. Each voice keeps its own "
            "rhythm, and they coincide on perfect consonances at the start of each perfection."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(labs_))
        with self.listen(c) as snd:
            window(snd, r"three voices, \ three speeds", detail=r"three synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[EAR, TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def franco(self):
        shapes = VGroup()
        for name, w, h, tail in ((r"long", 0.42, 0.42, True), (r"breve", 0.42, 0.42, False), (r"semibreve", 0.36, 0.36, False)):
            if name == "semibreve":
                sh = Square(side_length=0.36, stroke_width=0, fill_color=WHITE, fill_opacity=1).rotate(PI / 4)
            else:
                sh = Rectangle(width=w, height=h, stroke_width=0, fill_color=WHITE, fill_opacity=1)
            grp = VGroup(sh)
            if tail:
                grp.add(Line(sh.get_right(), sh.get_right() + DOWN * 0.7, color=WHITE, stroke_width=3))
            shapes.add(VGroup(grp, label(name, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.3))
        shapes.arrange(RIGHT, buff=1.2).move_to(UP * 1.2)
        rows_ = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"Franco of Cologne, \ \textit{Ars cantus mensurabilis}, \ about 1280: \ the shape of a note gives its length", WHITE),
            (r"long, \ breve, \ semibreve: \ each worth three \ (perfect) \ or two \ (imperfect) \ of the next", WHITE),
            (r"rules decide which, \ from the neighbours: \ chapter 8 programs them", WHITE),
            (r"rhythm freed from the six patterns: \ any sequence of lengths can now be written", TUNE))]).arrange(DOWN, buff=0.28, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        rows_.scale_to_fit_width(min(rows_.width, 12.4))
        with self.voiceover(
            "Motets needed a new notation, because a poem with one syllable per note cannot be written in ligatures. "
            "<bookmark mark='a'/> Around 1280 a theorist called Franco of Cologne set out the answer in his Art of "
            "Measurable Song: the shape of each single note gives its length. <bookmark mark='b'/> A long, a breve and "
            "a semibreve, with context-sensitive long and breve relationships; Franco’s semibreve subdivision should not simply be equated with later minim-based prolation. <bookmark mark='c'/> Which of the two depends on "
            "the neighbouring notes, by rules that the next chapter turns into a program. <bookmark mark='d'/> With "
            "Franco, rhythm is no longer a choice among six patterns. A much wider range of durations can be represented within the system’s rules, note by "
            "note, which is the principle of every Western notation since."
        ) as vo:
            self.play(FadeIn(shapes))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def petrus(self):
        items = [
            (r"Petrus de Cruce, \ about 1290: \ a breve divided into four, \ five, \ even seven semibreves", WHITE),
            (r"the triplum turns into rapid declamation over a slow motetus and tenor", WHITE),
            (r"the hocket: \ two voices sharing one line, \ note and rest in turn, \ like a hiccup \ (\textit{hoquetus})", WHITE),
            (r"the shortest note keeps getting shorter: \ the Ars nova will need a new name for it", TUNE),
        ]
        rows_scene(self, r"the quickening top voice", items,
                   "Freed from the patterns, the top voice began to speed up. <bookmark mark='b'/> In the motets of "
                   "Petrus de Cruce, around 1290, a single breve of the slow voices can hold four, five or even seven "
                   "semibreves in the triplum, which turns into rapid declamation of its poem above a slow motetus and "
                   "tenor. <bookmark mark='c'/> Another device of the time is the hocket, from a word for a hiccup: two "
                   "voices share one line, one singing while the other rests, note by note. <bookmark mark='d'/> The "
                   "shortest written note kept getting shorter, and the next generation would have to give the smaller "
                   "values names of their own.")
