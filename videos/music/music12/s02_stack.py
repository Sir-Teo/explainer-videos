from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403

NAMES = ["F", "C", "G", "D", "A", "E", "B", r"F$\sharp$", r"C$\sharp$", r"G$\sharp$", r"D$\sharp$", r"A$\sharp$"]


def picture(d, n: int, shift=ORIGIN) -> VGroup:
    """The first ``n`` notes of the stack on the circle, and the steps they leave as a bar."""
    order = d["order"][:n]
    circ = octave_circle(order, radius=1.7, names=NAMES[:n], color=TUNE).move_to(LEFT * 3.6 + UP * 0.3)
    row = d["rows"][n - 1]
    bar = step_bar(row["gaps"], width=6.2, height=0.6, colors=(LONG, SHORT, BAD)).move_to(RIGHT * 2.9 + UP * 0.9)
    sizes = row["sizes"]
    txt = label(rf"{n} notes: \ " + (r"steps of " + r", \ ".join(f"{s:.0f}" for s in sizes) + r" cents"), font_size=28, color=GOOD if len(sizes) == 2 else GREY_A).next_to(bar, DOWN, buff=0.4)
    kinds = label({1: r"one size", 2: r"two sizes", 3: r"three sizes"}[len(sizes)], font_size=34, color=GOOD if len(sizes) == 2 else BAD).next_to(txt, DOWN, buff=0.3)
    g = VGroup(circ, bar, txt, kinds).shift(shift)
    g.circ, g.bar = circ, bar
    return g


class Stack(SoundScene):
    def construct(self):
        chapter(self, 1, r"Stacking fifths", r"What do you get from one interval, \ repeated?", lit=(-530,))
        self.build()
        self.closing()
        self.listen_three()

    # ------------------------------------------------------------------
    def build(self):
        d = load("stack")
        head = label(r"go up a pure fifth (3 : 2), \ again and again; \ fold every note back into one octave", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        pics = {n: picture(d, n, DOWN * 0.4) for n in (1, 2, 3, 4, 5, 6, 7, 12)}
        with self.voiceover(
            "Part 1 found the most consonant interval after the octave: the fifth, three to two. Part 6 "
            "tuned whole instruments with it. Here we use it to choose notes. Start anywhere, say on F, "
            "and go up a fifth, and another, and another. Whenever a note leaves the octave, bring it "
            "back down. <bookmark mark='a'/> Draw the octave as a circle: once round is twice the "
            "frequency. F. Then C. <bookmark mark='b'/> Then G, D, A. <bookmark mark='c'/> Stop at "
            "five notes and look at the steps between neighbours. There are only two sizes: a whole tone "
            "of two hundred and four cents, and a wider step of two hundred and ninety-four. "
            "<bookmark mark='d'/> Add a sixth note, E, and that tidiness goes: three sizes. "
            "<bookmark mark='e'/> Add a seventh, B, and it comes back. Five whole tones, and two small "
            "steps of ninety cents. These seven notes are the white keys. <bookmark mark='f'/> Go on. "
            "Eight, nine, ten, eleven notes all leave three sizes of step. At twelve there are two "
            "again, and now they are nearly equal: ninety cents and a hundred and fourteen."
        ) as vo:
            cur = pics[1]
            turn = label(r"once round the circle \ is one octave", font_size=26, color=GREY_B).move_to(RIGHT * 2.9 + UP * 0.2)
            self.play(FadeIn(head), FadeIn(cur.circ), FadeIn(turn))
            self.wait(6.0)
            arc = Arc(radius=1.35, start_angle=np.pi / 2, angle=-2 * np.pi * 0.585, color=TUNE, stroke_width=4).move_arc_center_to(cur.circ.ring.get_center())
            fifth = label(r"a fifth: \ 702 of an octave's 1200 cents", font_size=24, color=TUNE).next_to(turn, DOWN, buff=0.4)
            self.play(Create(arc), FadeIn(fifth), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(arc), FadeOut(fifth))
            self.play(Indicate(cur.circ.dots[0], color=WHITE, scale_factor=2.0))
            self.wait(1.5)
            self.remove(*cur.circ)
            cur = pics[2]
            self.add(*cur.circ)
            vo.wait_until("b")
            for n in (3, 4, 5):
                self.remove(*cur.circ)
                cur = pics[n]
                self.add(*cur.circ)
                self.wait(0.7)
            vo.wait_until("c")
            self.remove(turn)
            self.add(cur[1], cur[2], cur[3])
            self.play(Indicate(cur[3], scale_factor=1.1), run_time=0.8)
            for mark, n in zip("def", (6, 7, 12)):
                vo.wait_until(mark)
                if n == 12:
                    self.wait(4.5)
                self.remove(*cur.circ, cur[1], cur[2], cur[3])
                cur = pics[n]
                self.add(*cur.circ, cur[1], cur[2], cur[3])
                self.play(Indicate(cur[3], scale_factor=1.1), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closing(self):
        d = load("stack")
        circ = octave_circle(d["order"], radius=2.0, names=NAMES, color=TUNE).move_to(LEFT * 3.2 + DOWN * 0.2)
        extra = Dot(circ.at(d["comma"] / 1200.0), radius=0.1, color=BAD)
        zoom = VGroup(Dot(radius=0.16, color=TUNE), Dot(radius=0.16, color=BAD)).arrange(RIGHT, buff=1.4).move_to(RIGHT * 3.2 + UP * 0.9)
        br = Brace(zoom, DOWN, color=GREY_B, buff=0.15)
        text = VGroup(label(rf"{d['comma']:.1f} cents", font_size=36, color=BAD), label(r"the first note, \ and the thirteenth", font_size=26, color=GREY_A),
                      label(r"twelve fifths overshoot seven octaves \\ by the comma of Part 6", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.3).next_to(br, DOWN, buff=0.2)
        with self.voiceover(
            "Why stop at twelve? Because at twelve the stack very nearly closes. Go up one more fifth, "
            "the thirteenth note, and it lands almost exactly on the note we started from. "
            f"<bookmark mark='a'/> Almost: it is {say(d['comma'], 1)} cents too high. That small gap is the "
            "comma we met in Part 6, twelve fifths against seven octaves, and it is the difference "
            "between the two sizes of step in the twelve-note stack. Shave a fiftieth of a semitone off "
            "every fifth and the gap vanishes, the two sizes become one, and you have the keyboard's "
            "equal temperament. The twelve notes on a piano are a stack of fifths, bent slightly so that "
            "it closes."
        ) as vo:
            self.play(FadeIn(circ))
            vo.wait_until("a")
            self.play(FadeIn(extra, scale=2.0), FadeIn(zoom), GrowFromCenter(br), FadeIn(text))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_three(self):
        d = load("stack")
        c = clip("stack.three")
        names = {5: r"five: \ the pentatonic scale", 7: r"seven: \ the diatonic scale", 12: r"twelve: \ the chromatic scale"}
        note = listen_note(r"the stacks of five, \ seven and twelve notes, \ each played as a scale", width=9.0, font_size=26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Five, seven and twelve. Those are the three stacks whose steps come in just two sizes, and "
            "each of them is a scale with a name. Here they are, in the tuning the stack gives them."
        ):
            self.play(FadeIn(note))
        self.play(FadeOut(note))
        shown = None
        with self.listen(c) as snd:
            window(snd, r"five, \ seven, \ twelve", detail=r"Part 7's piano, \ in pure fifths", corner=DL, tag_corner=DR)
            for n in (5, 7, 12):
                snd.wait_until(d["starts"][str(n)])
                if shown is not None:
                    self.remove(shown)
                pic = picture(d, n, DOWN * 0.3)
                title = label(names[n], font_size=36, color=TUNE).to_edge(UP, buff=0.5)
                shown = VGroup(pic, title)
                self.add(shown)
                ts = d["note_times"][str(n)]
                cells = pic.bar.cells
                for k, t in enumerate(ts[:-1]):                    # each step of the bar lights as the scale climbs through it
                    snd.wait_until(t)
                    self.play(cells[k % len(cells)].animate(rate_func=there_and_back).shift(UP * 0.15), run_time=min(0.22, 0.2))
        self.remove(shown)
        facts = VGroup(label(r"5 \ \ pentatonic: \ the black keys", font_size=34, color=SHORT), label(r"7 \ \ diatonic: \ the white keys", font_size=34, color=TUNE),
                       label(r"12 \ \ chromatic: \ all of them", font_size=34, color=GREY_A)).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        with self.voiceover(
            "The pentatonic scale, five notes. The diatonic scale, seven. The chromatic, twelve. One "
            "interval, repeated, has produced the black keys, the white keys, and the whole keyboard. "
            "Is that luck? There is a theorem that says it is not."
        ):
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.5), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
