from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.exposition()
        self.gamelan()
        self.plan()

    # ------------------------------------------------------------------
    def exposition(self):
        card = history_card(1889, r"Paris: \ the Exposition Universelle, \ the Eiffel Tower new", r"a Javanese village on the Esplanade, \ with its gamelan",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"Claude Debussy, \ twenty-six, \ goes back to hear it again and again", WHITE),
            (r"bronze bars and gongs, \ tuned to scales no Western piano had", WHITE),
            (r"years later he wrote that beside it, \ Western percussion sounded like the din of a fairground", TUNE),
            (r"within twenty-five years European composers had rebuilt their scales and their rhythms", EAR),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Paris, 1889. The Exposition Universelle has just opened, under a brand-new Eiffel Tower, and on the Esplanade "
            "there is a Javanese village with its own gamelan orchestra. <bookmark mark='a'/> Claude Debussy, aged twenty-six, "
            "goes back to hear it again and again. <bookmark mark='b'/> Bronze bars and gongs, tuned to scales that no "
            "European piano could play. <bookmark mark='c'/> Years later he wrote that, beside it, Western percussion "
            "sounded like the din of a fairground. <bookmark mark='d'/> Within twenty-five years, European composers had "
            "rebuilt both their scales and their rhythms."
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gamelan(self):
        d = load("hook")
        c = clip("hook.gamelan")
        g = voices_roll([d["elab"], d["balungan"], d["gongs"]], width=11.0, height=3.2, colors=[GREY_A, TUNE, EAR], bar_h=0.1).move_to(DOWN * 0.2)
        x = g.frame.get_left()[0] + g.frame.width * d["gong_beat"] / g.total
        gong = VGroup(Circle(radius=0.32, color=EAR, stroke_width=4).move_to([x + 0.3, g.frame.get_bottom()[1] - 0.15, 0]),
                      label(r"gong", font_size=18, color=EAR).move_to([x + 0.3, g.frame.get_bottom()[1] - 0.65, 0]))
        head = label(r"a gamelan texture of our own, \ in an idealized slendro: \ five near-equal steps", font_size=24, color=GREY_A).to_edge(UP, buff=0.45)
        key = VGroup(*[label(t, font_size=19, color=c_) for t, c_ in (
            (r"gold: \ the core melody, \ one note a beat", TUNE), (r"grey: \ the elaboration, \ twice as fast", GREY_A),
            (r"pink: \ gongs marking the cycle", EAR))]).arrange(RIGHT, buff=0.6).next_to(g, DOWN, buff=0.9)
        with self.voiceover(
            "This is not Javanese music; it is the film's own sketch, built from what Part 9 built. A core melody, one note "
            "to a beat, on metal bars tuned to five nearly equal steps, about two hundred and forty cents apart. An "
            "elaboration above it, twice as fast. Small gongs mark every fourth beat, and the great gong ends the cycle, "
            "where in Javanese music the cycle would begin again."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(gong), FadeIn(key))
        with self.listen(c) as snd:
            window(snd, r"a gamelan texture \ (ours)", detail=r"Part 9's bars and gongs", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [d["elab"], d["balungan"], d["gongs"]], 0.0, d["beat"], colors=[GREY_A, TUNE, EAR])
            cursor(snd, g, 0.0, d["beat"])
            pulse(snd, g, 0.0, c.duration, buff=0.12, color=GREY_B)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the whole-tone scale: \ a scale whose symmetric pitch collection does not uniquely privilege a home note",
            r"every scale with limited transposition, \ enumerated: \ Messiaen's seven among fifteen",
            r"planing, \ the octatonic, \ and two keys at once, \ heard",
            r"rhythm set loose: \ displaced accents and additive metres",
            r"Bartók's proportions tested against a null model",
            r"is a passage octatonic, \ or would any passage fit?",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. First, a scale whose symmetric pitch collection does not uniquely privilege a home note, the whole-tone scale. <bookmark mark='b'/> Then every scale "
            "that shares its symmetry, all of them, enumerated, with Messiaen's famous seven among them. "
            "<bookmark mark='c'/> Chords that slide in parallel, the octatonic scale, and two keys at once. "
            "<bookmark mark='d'/> Rhythm set loose, from displaced accents to additive metres. <bookmark mark='e'/> The "
            "golden section in Bartók, tested against chance. <bookmark mark='f'/> And a question at the frontier: when "
            "analysts call a passage octatonic, how often would any passage of that size fit?"
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
