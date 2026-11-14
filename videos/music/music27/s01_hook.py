from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.winter()
        self.linden()
        self.plan()

    # ------------------------------------------------------------------
    def winter(self):
        card = history_card(1827, r"Vienna: \ Franz Schubert, \ thirty, \ ill, \ a year from his death", r"\textit{Winterreise}: \ twenty-four songs of a man walking away in winter",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"the fifth song: \ \textit{Der Lindenbaum}, \ the linden tree by the well at the town gate", WHITE),
            (r"a voice and a piano: \ music for a room, \ not a theatre", WHITE),
            (r"the piano is not an accompaniment: \ it is the tree, \ the wind, \ the memory", TUNE),
            (r"by 1900 the same century had built Wagner's theatre and Mahler's orchestra", EAR),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Vienna, 1827. Franz Schubert is thirty, ill, and has a year to live. He is setting twenty-four poems by "
            "Wilhelm Müller about a man who leaves a town in winter: Winterreise, the winter journey. "
            "<bookmark mark='a'/> The fifth song is Der Lindenbaum, the linden tree that stands by the well at the town gate. "
            "<bookmark mark='b'/> It is music for a voice and a piano in a room, not for a theatre. <bookmark mark='c'/> And "
            "the piano is not accompanying. It is the rustling tree, the wind, and the memory. <bookmark mark='d'/> The "
            "century that began with songs like this ended with Wagner's theatre and Mahler's orchestra."
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linden(self):
        d = load("hook")
        c = clip("hook.lindenbaum")
        g = voices_roll([d["voice"], d["piano"]], width=11.4, height=3.4, colors=[TUNE, GREY_A], bar_h=0.08).move_to(DOWN * 0.2)
        head = label(r"Schubert, \ \textit{Der Lindenbaum}, \ bars 1 to 15", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        x0 = g.frame.get_left()[0] + g.frame.width * d["voice_start"] / g.total
        mark = VGroup(DashedLine([x0, g.frame.get_bottom()[1] - 0.15, 0], [x0, g.frame.get_top()[1] + 0.15, 0], color=TUNE, stroke_width=2),
                      label(r"the voice enters", font_size=19, color=TUNE).next_to([x0, g.frame.get_top()[1] + 0.15, 0], UP, buff=0.1))
        cap = label(r"grey: \ the piano's rustling triplets; \ gold: \ the voice", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.4)
        with self.voiceover(
            "Listen to the opening. Eight bars of piano alone: quick triplets that rustle and swell, then horn-like calls "
            "in the left hand. Then the voice enters with a plain tune, almost a folk song, and the piano keeps rustling "
            "underneath. The film plays it from the encoding, on Part 7's piano, with Part 17's synthetic voice singing "
            "the vowel ah."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(mark), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"\textit{Der Lindenbaum}", kind="synthesized", detail=r"piano and a synthetic tenor", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [d["voice"], d["piano"]], 0.0, d["unit"], colors=[TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the piano grows: \ iron, \ felt and seven octaves, \ measured in the scores",
            r"the song and its piano: \ a key-finder hears a stanza turn to minor",
            r"small pieces and stolen time: \ the mazurka's uneven beat, \ rubato modelled",
            r"programme music and Wagner: \ a theme that changes, \ a chord that never resolves",
            r"the stretching, \ measured: \ chromaticism in over 800 pieces from 1370 to 1924",
            r"nations, \ the museum concert, \ the first recordings",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> First the instrument: the piano grows, and the scores grow with it. "
            "<bookmark mark='b'/> Then the song, where a key-finder hears Schubert turn a stanza to minor. "
            "<bookmark mark='c'/> Small pieces, and the stolen time of rubato, modelled and heard. <bookmark mark='d'/> "
            "Programme music and Wagner. <bookmark mark='e'/> Then the claim that harmony was stretched until the key "
            "could barely hold, tested on more than eight hundred pieces from six centuries. <bookmark mark='f'/> And the "
            "century's other inventions: national styles, the concert as a museum, and the first recordings."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
