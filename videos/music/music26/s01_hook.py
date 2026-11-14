from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.mozart()
        self.theme()
        self.plan()

    # ------------------------------------------------------------------
    def mozart(self):
        card = history_card(1781, r"Vienna: \ Mozart, \ twenty-five, \ newly free of his archbishop", r"twelve variations on a French song: \ `Ah, \ vous dirai-je, \ maman'",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"the song's tune is our Tune: \ the melody this series has varied twenty-five times", TUNE),
            (r"Mozart's variations, \ K. 265, \ printed in 1785: \ a piece for teaching, \ and a catalogue of a style", WHITE),
            (r"the style rests on expectations so firm that breaking them is a joke", WHITE),
            (r"Haydn's quartet `The Joke' \ (1781) \ ends with silences: \ is it over yet?", EAR),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Vienna, the early 1780s. Mozart, in his mid-twenties and newly free of his employer, the Archbishop of "
            "Salzburg, is making a living in the capital by teaching, publishing and playing. Among the pieces he writes "
            "is a set of twelve variations on a French song, Ah, vous dirai-je, maman. <bookmark mark='a'/> The song's "
            "tune is ours: the Tune this series has varied twenty-five times so far. <bookmark mark='b'/> Mozart's set, "
            "printed in 1785, is a teaching piece and, without meaning to be, a catalogue of a style. "
            "<bookmark mark='c'/> It is a style built on expectations so firm that breaking them could be a joke, "
            "<bookmark mark='d'/> and Haydn made exactly that joke in a quartet of 1781, whose finale stops, starts, and "
            "stops again, until the audience cannot tell whether it is over."
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theme(self):
        d = load("hook")
        c = clip("hook.theme")
        g = voices_roll([d["melody"], d["acc"]], width=11.0, height=3.2, colors=[TUNE, GREY_A], bar_h=0.12).move_to(DOWN * 0.3)
        head = label(r"the Tune with a plain Classical accompaniment \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"tonic, \ subdominant, \ dominant: \ two bars each, \ a cadence every four", font_size=22, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Here is the theme, as the film harmonizes it: the Tune over plain chords on the fortepiano of Part 7. "
            "Notice how little it needs: the tonic, the subdominant, the dominant, a chord every bar or two, and a cadence "
            "every four bars. A Viennese listener of 1781 would know, after two bars, almost exactly what was coming."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the theme", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [d["melody"], d["acc"]], 0.0, d["unit"], colors=[TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 26: \ The Classical Style", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"a style of shared expectations; \ periodic phrasing", WHITE),
            (r"sonata form, \ traced by a key-finder through a Haydn movement", WHITE),
            (r"the quartet as a conversation; \ the accompaniment", EAR),
            (r"Haydn, \ Mozart, \ Beethoven: \ 33 quartet movements measured", WHITE),
            (r"a fair test of who wrote what, \ and why it is hard", WHITE),
            (r"the fortepiano, \ the metronome, \ and style as statistics", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Mozart's set is not in this series' library of scores, so this part reads the style through another body of "
            "music, thirty-three string quartet movements by Haydn, Mozart and Beethoven. <bookmark mark='a'/> First the "
            "expectations, and the phrasing that makes them. <bookmark mark='b'/> Then sonata form, traced through a "
            "Haydn movement by Part 15's key-finder. <bookmark mark='c'/> The quartet as a conversation, and the "
            "accompaniment patterns that hold it up. <bookmark mark='d'/> The three composers, measured. "
            "<bookmark mark='e'/> The fair test of authorship that Part 24 asked for, and why it is hard. "
            "<bookmark mark='f'/> And the new instruments and the new metronome, before the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
