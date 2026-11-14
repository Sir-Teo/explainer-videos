from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


def eighths_row(line, chord_pcs, cell=0.62, col=TUNE):
    """Sixteen eighth notes in boxes, beats marked; a beat box is filled when it holds a chord tone."""
    g = VGroup()
    for k, m in enumerate(line):
        on = k % 2 == 0
        ct = m % 12 in chord_pcs
        box = Square(cell, stroke_color=WHITE if on else GREY_D, stroke_width=2 if on else 1,
                     fill_color=(col if ct else RED) if on else BLACK, fill_opacity=0.65 if on else 0.0)
        txt = label(NN[m % 12], font_size=16, color=WHITE).move_to(box)
        g.add(VGroup(box, txt))
    g.arrange(RIGHT, buff=0.04)
    return g


class Scale(SoundScene):
    def construct(self):
        chapter(self, 2, r"The bebop scale", r"Why add an eighth note to a seven-note scale?")
        self.problem()
        self.rows_()
        self.hear()
        self.proof()
        self.everywhere()
        self.teach()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"a line of eighth notes over a chord: \ two notes a beat, \ the beats heard as stronger", WHITE),
            (r"the chord's notes sound right on the beats; \ the others pass between them", WHITE),
            (r"a seven-note scale has four chord tones and three others: \ they cannot alternate for long", WHITE),
            (r"add one chromatic passing tone, \ and they alternate exactly", TUNE),
            (r"the bebop scale, \ as Barry Harris taught it", GREY_A),
        ]
        rows_scene(self, r"the problem", items,
                   "Here is the problem a bebop player faces. A line of eighth notes over a chord has two notes a beat, and the "
                   "beats are heard as stronger. <bookmark mark='b'/> The chord's own notes sound right on the beats; the others "
                   "pass between them. <bookmark mark='c'/> But a seven-note scale has four chord tones and three others, and "
                   "they cannot alternate for long. <bookmark mark='d'/> Add one chromatic passing tone and they alternate "
                   "exactly. <bookmark mark='e'/> That is the bebop scale, as the pianist and teacher Barry Harris taught it.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def rows_(self):
        d = load("bebop")
        pcs = [0, 4, 7, 10]
        a = eighths_row(d["plain"]["line"], pcs, col=TUNE)
        b = eighths_row(d["bebop"]["line"], pcs, col=TUNE)
        la = label(rf"C mixolydian down from B$\flat$: \ {sum(d['plain']['hits'])} of {len(d['plain']['hits'])} beats on chord tones", font_size=20, color=WHITE)
        lb = label(rf"C bebop scale \ (with B$\natural$): \ {sum(d['bebop']['hits'])} of {len(d['bebop']['hits'])}", font_size=20, color=TUNE)
        g = VGroup(VGroup(la, a).arrange(DOWN, buff=0.2), VGroup(lb, b).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.6).move_to(DOWN * 0.1)
        g.scale_to_fit_width(min(g.width, 13.0))
        key = label(r"thick boxes: \ beats; \ gold: \ a chord tone on the beat; \ red: \ not", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"sixteen eighth notes down over C7 \ (C E G B$\flat$)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Run down the C mixolydian scale from B flat in eighth notes, over C seven. <bookmark mark='a'/> The first beats "
            "fall on B flat, G, E, C: all chord tones. Then the scale wraps past the octave, the pattern slips by one, and "
            "the beats start falling on A, F, D. <bookmark mark='b'/> Now add B natural between C and B flat. Eight notes: "
            "the four chord tones and four others, alternating. Every beat lands on a chord tone, for as long as you like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("bebop")
        c = clip("bebop.two")
        pcs = [0, 4, 7, 10]
        a = eighths_row(d["plain"]["line"], pcs)
        b = eighths_row(d["bebop"]["line"], pcs)
        g = VGroup(VGroup(label(r"mixolydian", font_size=20, color=WHITE), a).arrange(DOWN, buff=0.2),
                   VGroup(label(r"bebop scale", font_size=20, color=TUNE), b).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.6).move_to(UP * 0.1)
        g.scale_to_fit_width(min(g.width, 13.0))
        with self.voiceover(
            "Hear both over C seven, with bass and cymbal: the plain scale first, then the bebop scale. Listen for the "
            "moment the first line seems to lose its footing."
        ):
            self.play(FadeIn(g))
        es = list(range(16))
        with self.listen(c) as snd:
            window(snd, r"mixolydian, \ then bebop", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            ta = BL.swing_times(es, d["bpm"]) + d["starts"]["plain"]
            tb = BL.swing_times(es, d["bpm"]) + d["starts"]["bebop"]
            flash(snd, [x[1] for x in a], list(ta), hot=EAR, base=WHITE)
            flash(snd, [x[1] for x in b], list(tb), hot=EAR, base=WHITE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        d = load("bebop")
        rows_ = VGroup(
            label(r"the bebop scale on C: \ C D E F G A B$\flat$ B \ (eight notes)", font_size=21, color=WHITE),
            label(r"in descending order from C: \ C B B$\flat$ A G F E D \ C ...", font_size=21, color=WHITE),
            label(r"chord tones C, \ B$\flat$, \ G, \ E sit at positions 0, \ 2, \ 4, \ 6: \ every other note", font_size=21, color=TUNE),
            label(r"so a run from any chord tone on a beat keeps chord tones on beats, \ and eight is even, \ so it survives every octave", font_size=21, color=TUNE),
            label(rf"checked: \ every chord tone, \ both directions, \ two octaves: \ bebop 100\%, \ mixolydian {round(100 * d['claim']['plain_mean'])}\% on average", font_size=21, color=EAR),
            label(r"the major bebop scale \ (with G$\sharp$) \ does the same for C6: \ C E G A", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows_.scale_to_fit_width(min(rows_.width, 13.0))
        head = label(r"why it works", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Write the bebop scale on C in descending order: C, B, B flat, A, G, F, "
            "E, D, and round again. <bookmark mark='b'/> The chord tones, C, B flat, G and E, sit at positions zero, two, "
            "four and six: every other note. So a run that starts from any chord tone on a beat keeps chord tones on the "
            "beats; and because eight is even, the pattern survives every trip round the octave, in either direction. "
            "<bookmark mark='c'/> Monochord checks the claim: from every chord tone, in both directions, over two octaves, "
            f"the bebop scale lands chord tones on every beat; the mixolydian manages {say(round(100 * d['claim']['plain_mean']))} "
            "per cent on average. The major bebop scale, with a sharp fifth added, does the same for a C sixth chord."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[2]), FadeIn(rows_[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[4]), FadeIn(rows_[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def everywhere(self):
        items = [
            (r"the trick is general: \ interleave a chord's four notes with four others", WHITE),
            (r"a seven-note scale always needs one extra note: \ which one depends on the chord", WHITE),
            (r"Parker's lines often run this way for a bar, \ then change direction or leap", WHITE),
            (r"players do not stay on the grid: \ they shift the pattern deliberately, \ for tension", TUNE),
            (r"a rule to learn, \ and then to break on purpose", GREY_A),
        ]
        rows_scene(self, r"a general trick", items,
                   "The trick is general: interleave a chord's four notes with four others. <bookmark mark='b'/> A seven-note "
                   "scale always needs one extra note, and which one depends on the chord. <bookmark mark='c'/> Charlie Parker's "
                   "lines often run this way for a bar, then change direction or leap. <bookmark mark='d'/> And players do not "
                   "stay on the grid: they shift the pattern on purpose, for tension. <bookmark mark='e'/> A rule to learn, and "
                   "then to break deliberately.", marks="bcde")

    # ------------------------------------------------------------------
    def teach(self):
        items = [
            (r"Barry Harris \ (1929--2021) \ taught the bebop scales in workshops for decades", WHITE),
            (r"David Baker's and Jerry Coker's textbooks put them into jazz education from the 1960s", WHITE),
            (r"the scale is a description of how bebop lines behave, \ written down after the music", WHITE),
            (r"like the rules of Part 16's counterpoint: \ a style, \ distilled", TUNE),
            (r"chapter 3: \ how lines aim at their targets", GREY_A),
        ]
        rows_scene(self, r"teaching it", items,
                   "The pianist Barry Harris taught the bebop scales in workshops for decades, <bookmark mark='b'/> and the "
                   "textbooks of David Baker and Jerry Coker put them into jazz education from the 1960s. "
                   "<bookmark mark='c'/> The scale is a description of how bebop lines behave, written down after the music. "
                   "<bookmark mark='d'/> Like the rules of Part 16's counterpoint, it is a style, distilled. "
                   "<bookmark mark='e'/> Chapter three turns to how lines aim at their targets.", marks="bcde")
