from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Sequence(SoundScene):
    def construct(self):
        chapter(self, 4, r"The same step, \ again", r"What is a sequence?")
        self.circle()
        self.fivesix()
        self.chains()

    # ------------------------------------------------------------------
    def circle(self):
        d = load("sequence")
        c = clip("sequence.circle")
        st = block_staff(d["chords"], width=10.4, beats=2).move_to(UP * 0.9)
        names = VGroup(*[label(n, font_size=26, color=TUNE) for n in d["names"]])
        for k, n in enumerate(names):
            n.move_to([st.get_left()[0] + 1.25 + (st.width - 1.5) * (k + 0.5) / len(names), st.get_bottom()[1] - 0.4, 0])
        roots = label(r"roots: \ C \ F \ B \ E \ A \ D \ G \ C \ \ --- \ each a fifth below the last", font_size=24, color=GREY_A).next_to(names, DOWN, buff=0.4)
        with self.voiceover(
            "Take the falling fifth and do it again, and again. From C to F, F to B, B to E, and on round the key "
            "until G falls home to C. Every chord of the key is visited once, and the bass zigzags, down a fifth and "
            "up a fourth, the same step again and again. A pattern repeated at another pitch is a sequence; this "
            "one, the descending-fifths sequence, is the commonest in Baroque music. One step of it is not exact: "
            "F to B is a diminished fifth, because the key has no B flat."
        ):
            self.play(FadeIn(st), FadeIn(names), FadeIn(roots))
        with self.listen(c) as snd:
            window(snd, r"the descending-fifths sequence", detail=r"a plucked string", corner=DL, tag_corner=DR)
            flash(snd, list(names), d["times"], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fivesix(self):
        d = load("more")["fivesix"]
        c = clip("more.fivesix")
        st = block_staff(d["chords"], width=10.4, beats=2).move_to(UP * 0.9)
        names = VGroup(*[label(n, font_size=24, color=TUNE) for n in d["names"]])
        for k, n in enumerate(names):
            n.move_to([st.get_left()[0] + 1.25 + (st.width - 1.5) * (k + 0.5) / len(names), st.get_bottom()[1] - 0.4, 0])
        cap = label(r"the bass climbs by step; \ over each note, \ a fifth, \ then a sixth: \ the same step, \ rising", font_size=24, color=GREY_A).next_to(names, DOWN, buff=0.4)
        with self.voiceover(
            "Sequences can climb too. Here the bass rises by step, and over each bass note an upper voice moves "
            "from a fifth above it to a sixth: C with G, then with A; D with A, then with B; and so on. Each pair of "
            "chords is the same move, a step higher. It is called the rising five-six sequence, and it is how a "
            "piece climbs steadily without leaving the key."
        ):
            self.play(FadeIn(st), FadeIn(names), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the rising 5-6 sequence", detail=r"a plucked string", corner=DL, tag_corner=DR)
            flash(snd, list(names), d["times"], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chains(self):
        ch = load("sequence")["chains"]
        mj = {int(k): v for k, v in ch["major"].items()}
        mn = {int(k): v for k, v in ch["minor"].items()}
        ks = list(range(3, 8))
        c1 = columns([mj.get(k, 0) for k in ks], [str(k) for k in ks], width=4.8, height=2.4, color=WEAK, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(LEFT * 3.3 + DOWN * 0.6)
        c2 = columns([mn.get(k, 0) for k in ks], [str(k) for k in ks], width=4.8, height=2.4, color=WEAK, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(RIGHT * 3.3 + DOWN * 0.6)
        t1 = label(r"major chorales", font_size=24, color=GREY_A).next_to(c1, UP, buff=0.35)
        t2 = label(r"minor chorales", font_size=24, color=GREY_A).next_to(c2, UP, buff=0.35)
        head = label(r"runs of falling fifths in Bach's chorales, \ by number of chords", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        n4 = sum(v for k, v in mj.items() if k >= 4) + sum(v for k, v in mn.items() if k >= 4)
        with self.voiceover(
            "How often does Bach do it? Count runs of chords whose roots keep falling by fifths. "
            f"<bookmark mark='a'/> Runs of three chords, two falling fifths in a row, are everywhere: about "
            f"{say(round(mj.get(3, 0) + mn.get(3, 0), -1))} of them. Runs of four or more are rarer, {say(n4)} in all, "
            "and the longest go round six or seven chords. In a chorale a phrase is short, so the full circle "
            "is rare; in the concertos and suites of the same years it can run for bars on end."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1), FadeIn(c2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()
