from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Phrase(SoundScene):
    def construct(self):
        chapter(self, 8, r"Question and answer", r"How does a tune breathe?")
        self.lengths()
        self.ode()

    # ------------------------------------------------------------------
    def lengths(self):
        d = load("phrase")
        ks = list(range(4, 13))
        vals = [d["lengths"].get(str(k), 0) for k in ks]
        ch = columns(vals, [str(k) for k in ks], width=7.0, height=2.4, color=WEAK, hot=(4,), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(LEFT * 3.0 + DOWN * 0.9)
        xl = label(r"beats in a phrase", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        long_ = VGroup(label(r"the last note of a phrase", font_size=26, color=GREY_A), label(rf"{d['lengthening']:.1f} times as long", font_size=40, color=TUNE), label(r"as the others, \ on average", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.0 + DOWN * 0.3)
        head = label(r"the size of a phrase", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        total = sum(d["lengths"].values())
        with self.voiceover(
            "Phrases have a typical size. <bookmark mark='a'/> "
            f"{say(100 * d['lengths']['8'] / total)} in a hundred of ours last eight beats, and most of "
            "the rest six, four or twelve: a few seconds, the length of a comfortable breath. "
            "<bookmark mark='b'/> And the last note of a phrase is long: on average "
            f"{say(d['lengthening'], 1)} times as long as the others. A singer needs the time to "
            "breathe, and a listener uses the long note to hear that a phrase has ended. Speech does the "
            "same, and linguists call it final lengthening."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(xl))
            vo.wait_until("b")
            self.play(FadeIn(long_))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ode(self):
        d = load("phrase")
        c = clip("phrase.ode")
        o = d["ode"]
        ends = [0] + o["phrase_ends"][1::2]                 # the tune's two long phrases (each is two of the corpus's half phrases)
        rows = VGroup()
        rolls = []
        for k in range(2):
            a, b = ends[k], ends[k + 1]
            r = roll(o["pitches"][a:b], o["beats"][a:b], width=9.6, height=1.5, lo=-1, hi=8, lines=(0,), color=TUNE, thick=0.13)
            rolls.append(r)
            rows.add(r)
        rows.arrange(DOWN, buff=0.6).move_to(LEFT * 1.2 + UP * 0.6)
        deg = {0: "1", 2: "2", 4: "3", 7: "5"}
        tags = VGroup(*[label(rf"ends on {deg[o['pitches'][ends[k + 1] - 1]]}", font_size=26, color=EAR if o["pitches"][ends[k + 1] - 1] else TUNE).next_to(rolls[k], RIGHT, buff=0.4) for k in range(2)])
        head = label(r"\textit{Ode to Joy}: \ two phrases", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "And phrases come in pairs. Here is the whole of Beethoven's tune: two long phrases. Listen "
            "to the last note of each."
        ):
            self.play(FadeIn(head), FadeIn(rows))
        with self.listen(c) as snd:
            window(snd, r"two phrases", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(2):
                sing(snd, rolls[k], d["times"][ends[k]:ends[k + 1]], hot=WHITE, base=TUNE)
            for k in range(2):
                snd.wait_until(d["times"][ends[k + 1] - 1])
                self.add(tags[k])
        mid, fin = d["mid_end"], d["final_end"]
        order = sorted(mid, key=lambda k: -mid[k])[:4]
        cap = VGroup(label(r"a phrase in the middle of a tune ends on " + r", \ ".join(order[:3]) + rf" or {order[3]}", font_size=26, color=WHITE),
                     label(rf"the last phrase ends on 1: \ {100 * fin['1']:.0f} in a hundred", font_size=28, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The first phrase ends on the second degree: open, a question. The second is the same music, "
            "and ends on the first: an answer. Musicians call such a pair an antecedent and a "
            "consequent. <bookmark mark='a'/> In our tunes, a phrase in the middle may end on the "
            "fifth degree, the first, the third or the second. The final phrase ends on the first "
            f"{say(100 * fin['1'])} times in a hundred. A tune is a series of questions, and one last "
            "answer."
        ) as vo:
            self.play(Indicate(tags[0], color=EAR), Indicate(tags[1], color=TUNE))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
