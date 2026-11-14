from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.keys()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def keys(self):
        d = load("hook")
        c = clip("hook.keys")
        kb = keyboard(0, 24, width=11.0, height=2.4).move_to(UP * 0.8)
        count = VGroup(label(r"7 white", font_size=40, color=WHITE), label(r"5 black", font_size=40, color=GREY_B), label(r"to every octave", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.6).next_to(kb, DOWN, buff=0.6)
        brace = Brace(VGroup(kb.key[0], kb.key[11]), UP, color=GREY_B, buff=0.1)
        with self.voiceover(
            "Look at a keyboard. Any keyboard: a concert grand, a church organ, a toy. <bookmark mark='a'/> "
            "In every octave there are seven white keys and five black ones, and it has been so for six "
            "hundred years. Listen to the white keys, from C up to the next C. Then to the black keys."
        ) as vo:
            self.play(FadeIn(kb))
            vo.wait_until("a")
            self.play(GrowFromCenter(brace), FadeIn(count))
        with self.listen(c) as snd:
            window(snd, r"the white keys; \ the black keys", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            play_keys(snd, kb, d["white"] + d["black"], d["white_times"] + d["black_times"])
        kb.clear()
        with self.voiceover(
            "You know both of those. The first is the scale that most of the tunes you grew up with are "
            "made from. The second, the five black keys, is a scale too, and an older one: you can pick "
            "out folk songs from Scotland, China and West Africa on those five keys alone."
        ):
            self.play(*[kb.key[n].animate.set_fill(GOLD) for n in (0, 2, 4, 5, 7, 9, 11)], run_time=0.8)
            self.play(*[kb.key[n].animate.set_fill(BLUE) for n in (1, 3, 6, 8, 10)], run_time=0.8)
        self.wait(0.3)
        self.kb, self.count, self.brace = kb, count, brace

    # ------------------------------------------------------------------
    def question(self):
        kb = self.kb
        qs = VGroup(label(r"why seven and five?", font_size=40, color=EAR), label(r"why not six and six, \ or eight and four?", font_size=30, color=GREY_A),
                    label(r"and why are the black keys in a two and a three?", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.3).next_to(kb, DOWN, buff=0.5)
        with self.voiceover(
            "So here is the question for this part. Why seven and five? <bookmark mark='a'/> Twelve keys "
            "could be split six and six, or eight and four. <bookmark mark='b'/> And why are the black "
            "keys bunched as a pair and a triple, and not spaced out evenly? It looks like an accident "
            "of history, a habit of instrument makers. It is not. By the end of this part you will be "
            "able to derive this picture from one interval, the fifth of Part 1, and to prove that among "
            "all the ways of choosing seven notes out of twelve it is unlike any other."
        ) as vo:
            self.play(FadeOut(self.count), FadeOut(self.brace), FadeIn(qs[0]))
            vo.wait_until("a")
            self.play(FadeIn(qs[1]))
            vo.wait_until("b")
            self.play(FadeIn(qs[2]), Indicate(VGroup(kb.key[1], kb.key[3]), color=BLUE), Indicate(VGroup(kb.key[6], kb.key[8], kb.key[10]), color=BLUE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"a scale is a choice:", font_size=32, color=GREY_A), label(r"a few notes, \ out of all there could be.", font_size=32, color=TUNE)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"stack fifths: \ at 5, \ 7 and 12 notes the steps come in two sizes",
            r"seven notes, \ seven modes, \ in order of brightness",
            r"what is special about the white keys: \ even, \ two-sized, \ deep",
            r"minor's three forms; \ scales of five, \ six and eight notes",
            r"other maps of the octave: \ raga, \ maqam, \ slendro",
            r"every scale there is: \ 352 shapes, \ counted",
        ], title=r"Part 12: \ Scales and Modes", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "Rhythm told us when. A scale tells us which: the few notes a piece of music chooses, out of "
            "all the notes there could be. <bookmark mark='a'/> We begin by stacking fifths, and find that "
            "at five, seven and twelve notes something special happens. <bookmark mark='b'/> Seven notes "
            "give seven modes, and we put them in order from bright to dark. <bookmark mark='c'/> We ask "
            "what is special about the white keys, and get three answers. <bookmark mark='d'/> We meet the "
            "minor scale in its three forms, and scales with fewer notes and more. <bookmark mark='e'/> We "
            "look, briefly, at how other traditions divide the octave. <bookmark mark='f'/> And then we "
            "count every scale that could exist on twelve notes, and find where ours sits among them."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
