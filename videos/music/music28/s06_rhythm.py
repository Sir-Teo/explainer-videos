from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


class Rhythm(SoundScene):
    def construct(self):
        chapter(self, 5, r"Rhythm set loose", r"Where is the downbeat?", extra=((1913, r"\textit{The Rite of Spring}"),))
        self.rite()
        self.quiz()
        self.measure()
        self.metres()
        self.blocks()

    # ------------------------------------------------------------------
    def rite(self):
        items = [
            (r"\textit{The Rite of Spring}: \ a ballet of pagan Russia, \ Paris, \ 29 May 1913", WHITE),
            (r"one dissonant chord, \ repeated in even pulses, \ with accents in unpredictable places", WHITE),
            (r"in its last dance the metre changes almost every bar: \ 3/16, \ 2/16, \ 5/16 ...", WHITE),
            (r"the ostinato: \ a short figure repeated, \ the music built from blocks set side by side", TUNE),
            (r"the film describes the work and plays an original sketch", GREY_A),
        ]
        rows_scene(self, r"the Rite", items,
                   "The most famous rhythmic shock of the century came in 1913. <bookmark mark='b'/> Stravinsky's ballet The Rite of Spring, a vision of pagan Russia, was first danced in Paris on the twenty-ninth of May. <bookmark mark='c'/> In one of its dances a single dissonant chord is repeated in even pulses by the strings, while eight horns punch accents in places the ear cannot predict. <bookmark mark='d'/> In its last dance the metre changes almost every bar. <bookmark mark='e'/> And the music is built from ostinatos, short figures repeated and set side by side in blocks. <bookmark mark='f'/> The film describes the work and plays its own sketch so the construction remains explicit.", marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("accents")
        c = clip("accents.quiz")
        n = d["pulses"]
        card = listen_card(r"One chord, \ repeated in even pulses, \ twice. \ Once the accents fall every fourth pulse; \ "
                           r"once they fall where chance put them. \ In which can you not find the downbeat, \ A or B?", width=10.6)
        with self.voiceover(
            "The film's sketch. One chord on the strings, repeated in even pulses, twice. Once the accents fall on every "
            "fourth pulse; once they fall wherever chance put them. In which one can you not find the downbeat, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)

        def row(accs):
            g = VGroup(*[Rectangle(width=0.28, height=0.9 if i in accs else 0.35, stroke_width=0, fill_color=GREY_A, fill_opacity=0.9) for i in range(n)])
            g.arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
            return g
        rA = row(d["displaced"]).move_to(UP * 0.8)
        rB = row(d["regular"]).move_to(DOWN * 1.2)
        la = label(r"A", font_size=36, color=GREY_A).next_to(rA, LEFT, buff=0.4)
        lb = label(r"B", font_size=36, color=GREY_A).next_to(rB, LEFT, buff=0.4)
        self.play(FadeOut(card), FadeIn(rA), FadeIn(rB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            flash(snd, list(rA), [d["starts"]["A"] + i * d["unit"] for i in range(n)], hot=WHITE, base=GREY_A)
            flash(snd, list(rB), [d["starts"]["B"] + i * d["unit"] for i in range(n)], hot=WHITE, base=GREY_A)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(rf"A: \ accents at random: \ {round(100 * d['off']['displaced'])} in 100 off the beat", font_size=21, color=EAR).next_to(rA, DOWN, buff=0.25),
                     label(r"B: \ every fourth pulse: \ the metre is obvious", font_size=21, color=BLUE).next_to(rB, DOWN, buff=0.25))
        with self.voiceover(
            'In A the accents fall at random, and seven of the eight land off the beat of a four-four bar: these accents conflict with the chosen four-four grid; listeners may still infer metre from other cues. In B the metre announces itself after two accents. The pulse never changed; only the accents moved.'
        ):
            self.play(FadeIn(ans), *[r.animate.set_color(EAR) for r in rA], *[r.animate.set_color(BLUE) for r in rB])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        rows_ = text_rows([
            (r"Part 11's syncopation index: \ an accent on a weak pulse followed by silence on a strong one", WHITE),
            (r"random accents can conflict with a chosen metre; \ other cues and metric models matter", WHITE),
            (r"pulse can remain while accents give less consistent metric evidence", WHITE),
            (r"a new kind of rhythmic energy: \ surprise in place of swing", TUNE),
            (r"Part 46 measures what listeners predict, \ and what surprises them", GREY_A),
        ], font_size=24)
        head = label(r"when metric cues conflict", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why does the ear give up? <bookmark mark='a'/> Part 11 measured syncopation as accents on weak pulses followed by silence on strong ones. <bookmark mark='b'/> Random accents can conflict with a specified metre, but syncopation depends on the pattern, the metric model and other cues. <bookmark mark='c'/> This can make metric prediction harder, without implying that every listener stops predicting: the pulse is still there, but the accents provide less consistent evidence for this hierarchy. <bookmark mark='d'/> It is a new kind of rhythmic energy, surprise in place of swing. <bookmark mark='e'/> Part 46 measures what listeners predict and what surprises them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def metres(self):
        items = [
            (r"changing metres: \ the bar line follows the music, \ not the other way round", WHITE),
            (r"the ostinato as a building block: \ figures of different lengths repeating against each other", WHITE),
            (r"polyrhythm \ (Part 11): \ 3 against 2, \ 4 against 3, \ layered", WHITE),
            (r"from Stravinsky to minimalism \ (Reich, \ Glass), \ and to electronic dance music's loops", TUNE),
            (r"the drum machine and the sequencer make the ostinato a tool \ (Part 53)", GREY_A),
        ]
        rows_scene(self, r"metres that change", items,
                   "Other devices followed. <bookmark mark='b'/> Changing metres, where the bar line follows the music rather "
                   "than the music the bar line. <bookmark mark='c'/> Ostinatos as building blocks, figures of different "
                   "lengths repeating against each other. <bookmark mark='d'/> Polyrhythms, three against two or four against "
                   "three, which Part 11 drew. <bookmark mark='e'/> The ostinato runs from Stravinsky to the minimalism of "
                   "Steve Reich and Philip Glass, and to the loops of electronic dance music. <bookmark mark='f'/> In Part 53 "
                   "the sequencer makes it a tool.", marks="cdef")

    # ------------------------------------------------------------------
    def blocks(self):
        d = load("blocks")
        c = clip("blocks.layers")
        cols = [TUNE, BLUE, EAR]
        g = voices_roll(d["lines"], width=11.4, height=3.2, colors=cols, bar_h=0.09).move_to(DOWN * 0.1)
        x0, W = g.frame.get_left()[0], g.frame.width
        marks = VGroup(*[DashedLine([x0 + W * t / g.total, g.frame.get_bottom()[1] - 0.15, 0], [x0 + W * t / g.total, g.frame.get_top()[1] + 0.15, 0],
                                    color=GREY_B, stroke_width=2) for t in (0, 60)])
        head = label(r"three ostinatos: \ 3, \ 4 and 5 pulses long \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(rf"they start together and next coincide after {d['lcm']} pulses: \ the least common multiple", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Layered ostinatos make a texture that keeps changing although nothing in it changes. Three figures, three, four "
            "and five pulses long, start together. Each repeats exactly; but their combination does not repeat until all "
            "three come round together, after sixty pulses, the least common multiple of three, four and five. Listen for "
            "the shifting pattern of coincidences."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(marks), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"3 \ against 4 \ against 5", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, g, d["lines"], 0.0, d["unit"], colors=cols)
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()
