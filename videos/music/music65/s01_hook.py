from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"Three pairs of chorale phrases on an organ. \ One is Bach's. \ Two were written by machines \ "
                           r"(and harmonized by another). \ Which is Bach's?", width=10.0)
        with self.voiceover(
            "A question for your ears. Three pairs of phrases in the style of a Bach chorale, on an organ. One is Bach's own. "
            "Two were written by machines, and harmonized by another. Which is Bach's?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.8, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["first", "second", "third"]
        with self.listen(c) as snd:
            window(snd, r"three chorales", kind="synthesized", detail=r"Part 17's organ tones", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = VGroup(label(rf"the second: \ Bach's chorale {bwv(d['bach'])}, \ which no machine here saw while learning", font_size=19, color=TUNE),
                     label(r"the first: \ a Markov chain's tune; \ the third: \ a transformer's; \ both harmonized by Part 17's search", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            f"The second was Bach's, the chorale {bwv_said(d['bach'])}, which the melody generators did not see while learning; the separate Part 17 harmonizer uses a broader chorale corpus. The first "
            "tune came from a chain that counts which note follows which; the third from a small transformer, the kind of "
            "network behind today's language models: for each, the first draw that stayed in the key and could be harmonized, "
            "by Part 17's search. If you hesitated, you are in good company."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"Eugene, \ Oregon, \ 1997: \ Douglas Hofstadter puts three pieces before an audience", WHITE),
            (r"one by Bach; \ one by Steve Larson, \ a professor of music theory there, \ in Bach's style; \ one by David Cope's program EMI", WHITE),
            (r"as reported, \ the audience took EMI's piece for Bach's, \ and Larson's for the computer's", WHITE),
            (r"Hofstadter had expected the program to be found out at once", WHITE),
            (r"what does such a program know, \ and how much of its music is its training's music, \ copied?", TUNE),
        ]
        rows_scene(self, r"Bach, a professor and a program", items,
                   "The question is older than these machines. <bookmark mark='b'/> In 1997, at the University of Oregon in "
                   "Eugene, the cognitive scientist Douglas Hofstadter put three pieces before an audience. <bookmark mark='c'/> "
                   "One was by Bach. One was by Steve Larson, who taught music theory there, written in Bach's style. One was by "
                   "EMI, a program David Cope had been building since 1981. <bookmark mark='d'/> As it was reported, the audience "
                   "took the program's piece for Bach's, and the professor's for the computer's. <bookmark mark='e'/> Hofstadter "
                   "had expected the program to be found out at once, and was troubled. <bookmark mark='f'/> This part "
                   "asks what such a program knows, and how much of its music is simply its training's music, copied.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"dice, \ rules and chance: \ composing machines before computers learnt",
            r"counting what follows what: \ Markov chains on Bach's chorale tunes",
            r"these models: \ copying and prediction, not a universal coherence law",
            r"constraints, \ and Cope's recombination",
            r"music as tokens, \ and a transformer; \ temperature",
            r"four parts, \ judging machines, \ and who owns what they copy",
        ], title=r"The plan", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Dice, rules and chance, the composing machines that came before learning. "
            "<bookmark mark='a'/> Counting which note follows which, on the melodies of Bach's chorales. "
            "<bookmark mark='b'/> An empirical trade in these models between copying and prediction; coherence is not measured directly. "
            "<bookmark mark='c'/> Constraints, and Cope's recombination. <bookmark mark='d'/> Music as tokens, a "
            "transformer, and temperature. <bookmark mark='e'/> And four-part harmony, how to judge a composing machine, and "
            "who owns what it copies."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
