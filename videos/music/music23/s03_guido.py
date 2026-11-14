from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403

SYL_C = {"ut": TUNE, "re": TUNE, "mi": EAR, "fa": EAR, "sol": TUNE, "la": TUNE}


class Guido(SoundScene):
    def construct(self):
        chapter(self, 2, r"Guido's hexachords", r"How do you learn a melody you have never heard?", extra=((1030, r"Guido's letter to Brother Michael"),))
        self.letter()
        self.gamut()
        self.mutation()
        self.staff()

    # ------------------------------------------------------------------
    def letter(self):
        d = load("chant")
        g_ = load("guido")
        notes = d["ut"]
        starts = d["ut_lines"][:6]
        g = mroll(notes, width=11.6, height=1.7, lo=58, hi=71, total=max(n[1] + n[2] for n in notes), color=GREY_B).move_to(UP * 0.3)
        marks = VGroup()
        for k, i in enumerate(starts):
            g.notes[i].set_fill(TUNE)
            marks.add(label(g_["ut_syllables"][i], font_size=24, color=TUNE).next_to(g.notes[i], UP, buff=0.18))
        lines = label(r"Ut \ queant laxis \ / \ Re-sonare fibris \ / \ Mi-ra gestorum \ / \ Fa-muli tuorum \ / \ Sol-ve polluti \ / \ La-bii reatum", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.45)
        card = history_card(1030, r"Arezzo: \ Guido writes to Brother Michael", r"a way for boys to sing a chant they have never heard \ ``in a few days''", width=11.2, font_size=24).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In the 1030s a monk and teacher called Guido, working at Arezzo in Tuscany, wrote a letter to a fellow monk, "
            "Brother Michael, describing a way to teach boys to sing a chant they had never heard, in a matter of days "
            "instead of years. <bookmark mark='a'/> His tool was the hymn you just heard. Each of its first six lines "
            "begins one step higher than the last, C, D, E, F, G, A, <bookmark mark='b'/> and the syllables that begin "
            "them, ut, re, mi, fa, sol, la, became the names of the six notes. Learn how the hymn sounds at each line's "
            "start, and you know how each step of the scale sounds in its place. Six centuries later, ut became do."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(g.notes[i], color=WHITE) for i in starts], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(marks), FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gamut(self):
        d = load("guido")
        gam = d["gamut"]
        x0, W = -4.3, 10.6
        lo, hi = gam[0], gam[-1]
        xs = {p: x0 + W * (p - lo) / (hi - lo) for p in gam}
        names = VGroup(*[label(LETTER[p % 12], font_size=19, color=GREY_A if p % 12 != 10 else EAR).move_to([xs[p], 2.25 - (0.32 if p % 12 == 10 else 0.0), 0]) for p in gam])
        bars = VGroup()
        for k, h in enumerate(d["hexachords"]):
            y = 1.35 - 0.5 * k
            col = {"hard": BLUE, "natural": TUNE, "soft": EAR}[h["kind"]]
            pts = VGroup()
            for s, p in zip(("ut", "re", "mi", "fa", "sol", "la"), h["notes"]):
                if p in xs:
                    pts.add(label(s, font_size=18, color=col).move_to([xs[p], y, 0]))
            tag = label(rf"{h['kind']} \ on {LETTER[h['start'] % 12]}", font_size=18, color=col).move_to([-5.4, y, 0])
            bars.add(VGroup(tag, pts))
        cap = label(r"mi--fa is always the semitone: \ E--F, \ B--C, \ or A--B$\flat$", font_size=22, color=WHITE).to_edge(DOWN, buff=0.45)
        head = label(rf"the gamut: \ {len(gam)} notes, \ from Gamma-ut to E-la", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"The whole range of notes the singers used, the gamut, ran {say(len(gam))} notes, from a low G called "
            "gamma-ut, the Greek letter gamma, which gave us the word gamut, up to a high E. <bookmark mark='a'/> Six "
            "syllables cannot name twenty-two notes, so the six-note pattern, tone, tone, semitone, tone, tone, was laid "
            "over the gamut seven times: <bookmark mark='b'/> starting on G, the hard hexachord, with B natural; "
            "starting on C, the natural hexachord; and starting on F, the soft hexachord, which needs a B flat. "
            "<bookmark mark='c'/> In every one of them the semitone is mi to fa. Wherever you are, mi to fa is the "
            "half step, and a singer who knows which syllable a note is knows where the half steps lie."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mutation(self):
        d = load("guido")
        c = clip("guido.mutation")
        line = d["line"]
        notes = [[p, k, 1.0] for k, p in enumerate(line)]
        notes[-1][2] = 2.0
        g = mroll(notes, width=11.0, height=2.0, lo=63, hi=74, total=len(line) + 1).move_to(UP * 0.4)
        syl = VGroup(*[label(s, font_size=20, color=SYL_C[s]).next_to(g.notes[k], DOWN, buff=0.25) for k, s in enumerate(d["line_syllables"])])
        names = VGroup(*[label(LETTER[p % 12], font_size=16, color=GREY_B).next_to(g.notes[k], UP, buff=0.15) for k, p in enumerate(line)])
        mut = d["line_mutations"]
        mk = VGroup(*[DashedLine(g.notes[i].get_left() + LEFT * 0.08 + UP * 0.9, g.notes[i].get_left() + LEFT * 0.08 + DOWN * 1.3, color=EAR, stroke_width=2) for i in mut])
        cap = VGroup(label(r"F G A B$\flat$: \ the soft hexachord, \ ut re mi fa", font_size=22, color=WHITE),
                     label(r"then up through B natural: \ change to the hard hexachord on G \ (a mutation)", font_size=22, color=EAR),
                     label(r"solmization as a shortest path: \ the fewest mutations, \ found by dynamic programming", font_size=22, color=TUNE)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A melody that wanders out of one hexachord must change to another, a mutation. This line starts on F and "
            "uses B flat, so it begins in the soft hexachord: ut, re, mi, fa. Later it climbs through B natural to C, "
            "which the soft hexachord cannot name, so the singer re-names a note on the way, G becomes ut of the hard "
            "hexachord, and carries on. Listen for the B flat early on and the B natural near the end."
        ):
            self.play(FadeIn(g), FadeIn(names), FadeIn(syl[:7]), FadeIn(cap[0]))
        with self.listen(c) as snd:
            window(snd, r"B$\flat$, \ then B$\natural$", detail=r"one synthetic voice", kind="synthesized", corner=UL, tag_corner=UR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in notes], hot=WHITE, base=TUNE)
            flash(snd, list(syl), [n[1] * d["unit"] for n in notes], hot=WHITE, base=GREY_B, fade=0.5)
        with self.voiceover(
            f"The mutation falls at note {say(mut[0] + 1)}, the G. <bookmark mark='a'/> Choosing the syllables is "
            "a small optimization problem: among all the ways to name the notes, pick the one with the fewest changes of "
            "hexachord. <bookmark mark='b'/> It is a shortest path through a graph of hexachords, solved here by dynamic "
            "programming and checked against brute force; medieval singers solved it in their heads, with rules of thumb "
            "for where to mutate."
        ) as vo:
            self.play(FadeIn(syl[7:]), Create(mk), FadeIn(cap[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cap[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def staff(self):
        lines = VGroup()
        cols = [GREY_B, "#E05A5A", GREY_B, "#F5C542"]
        for k in range(4):
            lines.add(Line([-6.0, -0.6 + 0.5 * k, 0], [-1.6, -0.6 + 0.5 * k, 0], color=cols[k], stroke_width=3 if k in (1, 3) else 1.5))
        lets = VGroup(label("F", font_size=24, color="#E05A5A").next_to(lines[1], LEFT, buff=0.2), label("C", font_size=24, color="#F5C542").next_to(lines[3], LEFT, buff=0.2))
        pts = [(-5.4, 0), (-4.9, 1), (-4.4, 3), (-3.9, 2), (-3.4, 1), (-2.9, 0), (-2.4, 1), (-1.9, 2)]
        neumes = VGroup(*[Square(side_length=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=0.9).move_to([x, -0.6 + 0.25 * s, 0]) for x, s in pts])
        rows_ = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"Guido's other gift: \ lines a third apart, \ every note on a line or a space", WHITE),
            (r"the F line red, \ the C line yellow: \ the letters became our clefs", WHITE),
            (r"the `Guidonian hand': \ the gamut on the joints of the fingers, \ for teaching", WHITE),
            (r"named after him, \ though it appears nowhere in his writings", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 7.6))
        rows_.move_to(RIGHT * 2.75 + DOWN * 0.1)
        with self.voiceover(
            "Guido's other gift is in front of every musician today. <bookmark mark='a'/> Earlier neumes showed the shape "
            "of a melody but not its exact steps. Guido drew lines a third apart, so that every note sits on a line or in "
            "a space, and its pitch can be read without having heard it. <bookmark mark='b'/> He coloured the F line red "
            "and the C line yellow, and wrote the letters at the start; those letters, worn by centuries of copying, are "
            "our F and C clefs. <bookmark mark='c'/> Teachers later mapped the whole gamut onto the joints of the left "
            "hand, pointing at a joint to call for a note, <bookmark mark='d'/> and named it after Guido, though it "
            "appears nowhere in what he wrote."
        ) as vo:
            self.play(Create(lines), FadeIn(lets), FadeIn(rows_[0]))
            self.play(LaggedStart(*[FadeIn(n) for n in neumes], lag_ratio=0.1), run_time=1.2)
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
