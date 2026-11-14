from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Thirds(SoundScene):
    def construct(self):
        chapter(self, 1, r"Thirds and sixths become consonant", r"When did the third become a resting place?", extra=((1440, r"the \textit{contenance angloise}"),))
        self.english()
        self.census()
        self.endings()

    # ------------------------------------------------------------------
    def english(self):
        items = [
            (r"about 1440: \ a French poet praises a new `English manner' \ (\textit{contenance angloise})", WHITE),
            (r"John Dunstable and the English: \ full sonorities of thirds and sixths, \ few bare fifths", WHITE),
            (r"Guillaume Du Fay and Gilles Binchois take it up on the continent", WHITE),
            (r"the third is still `imperfect' in theory: \ the practice changes before the name does", TUNE),
            (r"Part 6: \ a just third is 5:4; \ the Pythagorean third, \ 81:64, \ is rough", GREY_A),
        ]
        rows_scene(self, r"the English manner", items,
                   "Part 23 ended with fourteenth-century music that keeps its perfect intervals on the beat and never "
                   "ends on a third. <bookmark mark='b'/> Around 1440 the French poet Martin le Franc praised a new sound "
                   "that composers had learned from the English, a contenance angloise. <bookmark mark='c'/> The English, "
                   "John Dunstable above all, wrote full sonorities of thirds and sixths, and few bare fifths. "
                   "<bookmark mark='d'/> Guillaume Du Fay and Gilles Binchois brought it into continental music. "
                   "<bookmark mark='e'/> In theory the third stayed imperfect for another century: practice moved first. "
                   "<bookmark mark='f'/> And, as Part 6 showed, a third tuned pure, five to four, is smooth, while the "
                   "Pythagorean third of the old theory, eighty-one to sixty-four, is rough; singers tuning by ear could "
                   "make the difference.", marks="bcdef")

    # ------------------------------------------------------------------
    def census(self):
        d = load("thirds")["census"]
        names = ["fourteenth century", "Palestrina", "Monteverdi"]
        tags = [r"14th century", r"Palestrina", r"Monteverdi"]
        groups = VGroup()
        cols = [GREY_B, TUNE, EAR]
        for k, (key, lab_) in enumerate(((r"third", r"sonorities with a third"), (r"triad", r"full triads"), (r"final_third", r"last chords with a third"))):
            vals = [d[n][key] for n in names]
            bars = VGroup()
            for j, v in enumerate(vals):
                h = 2.6 * v
                r = Rectangle(width=0.7, height=max(h, 0.02), stroke_width=0, fill_color=cols[j], fill_opacity=0.9)
                r.move_to([j * 0.9, h / 2, 0])
                t = label(rf"{100 * v:.0f}", font_size=20, color=WHITE).next_to(r, UP, buff=0.08)
                bars.add(VGroup(r, t))
            title = label(lab_, font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.3)
            groups.add(VGroup(bars, title))
        groups.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to(DOWN * 0.2)
        key = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=cols[j], fill_opacity=0.9), label(rf"{tags[j]} \ ({d[names[j]]['pieces']:,} pieces)".replace(",", "{,}"), font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.15)
                       for j in range(3)]).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.6)
        cap = label(r"every quarter note of the edition, \ in 100s", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Measure it. Sample every piece at each quarter note and ask whether the sonority holds a third or a sixth "
            "above its bass. <bookmark mark='a'/> In Part 23's eighty-nine fourteenth-century pieces, "
            f"{say(round(100 * d['fourteenth century']['third']))} in a hundred do; in Palestrina's thirteen hundred Mass "
            f"movements, {say(round(100 * d['Palestrina']['third']))}. <bookmark mark='b'/> Full triads, a third and a "
            f"fifth together, rise from {say(round(100 * d['fourteenth century']['triad']))} in a hundred to "
            f"{say(round(100 * d['Palestrina']['triad']))}. <bookmark mark='c'/> And the last chord, which in the "
            f"fourteenth century had a third once in eighty-nine pieces, has one in {say(round(100 * d['Palestrina']['final_third']))} "
            "in a hundred of Palestrina's movements. A century and a half turned the third from a passing colour into "
            "the sound of the music itself, and finally into a place to end."
        ) as vo:
            self.play(FadeIn(key), FadeIn(cap))
            for mark, gg in zip("abc", groups):
                vo.wait_until(mark)
                self.play(FadeIn(gg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def endings(self):
        d = load("thirds")
        c = clip("thirds.endings")
        gA = voices_roll(d["A"]["voices"], width=5.4, height=2.6, colors=[TUNE, BLUE, GREY_A, GREY_B], bar_h=0.11).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(d["B"]["voices"], width=5.4, height=2.6, colors=[TUNE, BLUE, EAR, GREY_A, GREY_B], bar_h=0.11).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(rf"{d['A']['composer']}, \ \textit{{{d['A']['title'].split('.')[-1].strip()}}}", font_size=20, color=GREY_A).next_to(gA, UP, buff=0.35)
        lb = label(rf"Palestrina, \ \textit{{{d['B']['title'].split(',')[0]}}}", font_size=20, color=GREY_A).next_to(gB, UP, buff=0.35)
        head = label(r"two endings, \ two centuries apart", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the difference in two endings. First the close of de Vitry's motet from Part 23, landing on a bare "
            "octave and fifth. Then the close of a movement of Palestrina's, landing on a full chord with its third. "
            "Listen to the last sound of each."
        ):
            self.play(FadeIn(head), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"de Vitry, \ then Palestrina", detail=r"from the editions, \ synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, d["A"]["voices"], d["starts"]["A"], d["A"]["quarter"], colors=[TUNE, BLUE, GREY_A, GREY_B])
            flash_voices(snd, gB, d["B"]["voices"], d["starts"]["B"], d["B"]["quarter"], colors=[TUNE, BLUE, EAR, GREY_A, GREY_B])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.08)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
