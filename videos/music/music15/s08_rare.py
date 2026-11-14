from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Rare(SoundScene):
    def construct(self):
        chapter(self, 7, r"Which notes tell", r"Which notes give the key away?")
        self.sets()
        self.tritone()
        self.blind()

    # ------------------------------------------------------------------
    def row(self, notes, keys_, y, hot=False):
        left = label(tex(notes), font_size=32, color=WHITE).move_to([-4.6, y, 0], aligned_edge=LEFT)
        ks = VGroup(*[label(tex(k), font_size=30, color=TUNE if hot else GREY_A) for k in keys_]).arrange(RIGHT, buff=0.35).move_to([-0.6, y, 0], aligned_edge=LEFT)
        n = label(str(len(keys_)), font_size=34, color=TUNE if len(keys_) == 1 else WHITE).move_to([5.3, y, 0])
        return VGroup(left, ks, n)

    def sets(self):
        d = load("rare")
        rows = {r["notes"]: r for r in d["rows"]}
        head = VGroup(label(r"notes heard", font_size=22, color=GREY_B).move_to([-4.6, 2.6, 0], aligned_edge=LEFT), label(r"major keys that contain them all", font_size=22, color=GREY_B).move_to([-0.6, 2.6, 0], aligned_edge=LEFT),
                      label(r"how many", font_size=22, color=GREY_B).move_to([5.3, 2.6, 0]))
        a = self.row("C, G", rows["C, G"]["keys"], 1.7)
        b = self.row("C, D, E", rows["C, D, E"]["keys"], 0.7)
        c = self.row("C, D, E, F", rows["C, D, E, F"]["keys"], -0.3)
        with self.voiceover(
            "Which notes carry the news? Forget profiles for a moment, and ask a simpler question: "
            "which major scales contain the notes heard so far? <bookmark mark='a'/> C and G, a perfect "
            f"fifth: {say(len(rows['C, G']['keys']))} of the twelve major scales contain both. A fifth "
            "tells you almost nothing. <bookmark mark='b'/> C, D, E: three keys. <bookmark mark='c'/> "
            "Add F, and it is two: C major or F major. Each new note strikes some keys off the list, "
            "but common intervals strike off very few."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", (a, b, c)):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.rows3 = VGroup(head, a, b, c)

    def tritone(self):
        d = load("rare")
        rows = {r["notes"]: r for r in d["rows"]}
        card = pause_card(r"Two notes: \ B and F. \ How many of the twelve major scales contain both?", width=8.0).move_to(DOWN * 2.2)
        with self.voiceover("Now a prediction. Two notes only: B and F. How many of the twelve major scales contain both?"):
            self.play(FadeIn(card))
        self.wait(2.0)
        t = self.row("B, F", rows["B, F"]["keys"], -1.3, hot=True)
        u = self.row("B, F, C", rows["B, F, C"]["keys"], -2.3, hot=True)
        vec = d["vector"]
        with self.voiceover(
            "Two: C major and F sharp major. <bookmark mark='a'/> And one more note, any note of either "
            "scale that is not in the other, settles it. Three notes, and the key is certain. The "
            "reason is in Part 12. A major scale contains six perfect fifths and only one tritone; so a "
            "fifth could be anywhere, and a tritone can be in only two places. The rarest interval is "
            "the best clue. Richmond Browne pointed this out in 1981, and it is why the dominant "
            "seventh chord of Part 13, which contains the tritone, announces its key so plainly."
        ) as vo:
            self.play(FadeOut(card), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(u))
        self.wait(0.4)
        self.clear_scene()

    def blind(self):
        d = load("rare")
        steps = d["tune_steps"]
        rows = VGroup()
        for k, s in enumerate(steps):
            r = VGroup(label(tex(s["note"]), font_size=32, color=TUNE), VGroup(*[label(tex(x), font_size=26, color=GREY_A) for x in s["keys"]]).arrange(RIGHT, buff=0.3), label(str(len(s["keys"])), font_size=30, color=WHITE))
            r[0].move_to([-5.2, 0, 0])
            r[1].move_to([-4.2, 0, 0], aligned_edge=LEFT)
            r[2].move_to([4.8, 0, 0])
            rows.add(r)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 0.5)
        for r in rows:
            r[2].set_x(4.8)
        head = label(r"the Tune, \ one new note at a time: \ the major keys still possible", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = VGroup(label(r"the Tune never plays B, \ or B$\flat$: \ by its notes alone it is in C or in F", font_size=28, color=EAR),
                     label(r"so a key is not which notes. \ It is which notes matter most.", font_size=30, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Try that on the Tune. Its first note, C, is in seven major scales. <bookmark mark='a'/> G "
            "leaves six; A, four; F, three; E, two. Its last new note is D, and two keys remain: C major "
            "and F major. <bookmark mark='b'/> The Tune never plays a B, and never a B flat. Judged by "
            "its notes alone, it is in two keys at once, which is why the key finder wavered. And yet "
            "no listener hears it in F. <bookmark mark='c'/> So a key cannot be a matter of which notes "
            "are used. It is a matter of which notes matter: which one begins and ends, which are long, "
            "which are leapt to. That is exactly what a profile holds, and a list of notes does not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.6), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(cap[0]))
            vo.wait_until("c")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()
