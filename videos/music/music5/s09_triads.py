from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Triads(SoundScene):
    def construct(self):
        chapter(self, 8, r"Major and minor", r"Why do two chords made of the same intervals sound so different?", lit=(1722,),
                extra=((1722, r"Rameau's fundamental bass"),))
        self.same()
        self.bass()
        self.map()

    # ------------------------------------------------------------------
    def same(self):
        d = load("triads")
        c = clip("triads.pair")
        q = listen_card(r"Two chords, \ A and B. \ Each is built from the same three intervals: \\ a major third, \ a minor third, \ and a fifth. \ Do they sound alike?",
                        width=9.8, font_size=26).to_edge(UP, buff=0.35)
        stacks = VGroup()
        for name, order in ((r"A", (r"major third", r"minor third")), (r"B", (r"minor third", r"major third"))):
            notes = VGroup(*[Dot(radius=0.14, color=TUNE) for _ in range(3)])
            gaps = (1.0, 0.75) if order[0] == "major third" else (0.75, 1.0)
            notes[0].move_to(ORIGIN)
            notes[1].move_to(UP * gaps[0])
            notes[2].move_to(UP * (gaps[0] + gaps[1]))
            lab = VGroup(label(order[0], font_size=22, color=GREY_A).next_to((notes[0].get_center() + notes[1].get_center()) / 2, RIGHT, buff=0.3),
                         label(order[1], font_size=22, color=GREY_A).next_to((notes[1].get_center() + notes[2].get_center()) / 2, RIGHT, buff=0.3),
                         label(r"fifth", font_size=22, color=GREY_B).next_to(notes[1], LEFT, buff=0.35))
            brace = Line(notes[0].get_center() + LEFT * 0.2, notes[2].get_center() + LEFT * 0.2, color=GREY_C, stroke_width=1.5)
            stacks.add(VGroup(notes, lab, brace, label(name, font_size=44, color=GREY_A).next_to(notes, DOWN, buff=0.3)))
        stacks.arrange(RIGHT, buff=3.0).move_to(DOWN * 0.9)
        with self.voiceover(
            "Now a test that separates the two causes inside music itself. Take three notes. From the bottom "
            "note to the middle one, a major third; from the middle to the top, a minor third; so that the outer "
            "two are a fifth apart. That is chord A. For chord B, swap the two thirds: minor below, major above. "
            "The same three intervals, in a different order. Do the two chords sound alike?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(stacks))
        with self.listen(c) as snd:
            window(snd, r"chord A, \ then chord B", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, s in zip("AB", stacks):
                t0 = snd.time_of(ev)
                pulse(snd, s, t0, t0 + 2.2, buff=0.2)
        r = {x["name"]: x for x in d["rows"]}
        names = VGroup(label(r"major", font_size=36, color=SMOOTH).next_to(stacks[0], UP, buff=0.2), label(r"minor", font_size=36, color=AIR).next_to(stacks[1], UP, buff=0.2))
        vals = VGroup(label(rf"roughness \ {r['major']['rough']:.2f}", font_size=28).next_to(stacks[0], RIGHT, buff=0.5).shift(DOWN * 1.0),
                      label(rf"roughness \ {r['minor']['rough']:.2f}", font_size=28).next_to(stacks[1], RIGHT, buff=0.5).shift(DOWN * 1.0))
        with self.voiceover(
            "Nobody mistakes one for the other. A is a major chord, B is a minor chord, and the difference "
            "between them is the most famous difference in Western music. <bookmark mark='a'/> But ask "
            f"Monochord for their roughness, and it answers {say(r['major']['rough'], 2)} and "
            f"{say(r['minor']['rough'], 2)}: the same to within "
            f"{say(100 * d['same_roughness'], 1)} percent. It has to. The same pairs of notes are present in "
            "both, so nearly the same pairs of partials are beating. Roughness cannot tell major from minor."
        ) as vo:
            self.play(FadeOut(q), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(vals))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bass(self):
        d = load("triads")
        c = clip("triads.four")
        cols = {"major": SMOOTH, "minor": AIR, "diminished": ROUGH, "augmented": LIMIT}
        head = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"chord", r"as whole numbers", r"repeats after", r"its fundamental bass lies", r"roughness")])
        xs = (-6.3, -4.2, -1.3, 1.4, 5.4)
        for h, x in zip(head, xs):
            h.move_to(RIGHT * x + UP * 2.3, aligned_edge=LEFT)
        rows = VGroup()
        for k, r in enumerate(d["rows"]):
            a, b, c_ = r["as_integers"]
            row = VGroup(label(r["name"], font_size=30, color=cols[r["name"]]), MathTex(rf"{a} : {b} : {c_}", font_size=32),
                         label(rf"{r['repeat']} cycles", font_size=26, color=GREY_A),
                         label(rf"{r['octaves_below']:.1f} octaves below its lowest note", font_size=24, color=EAR), label(rf"{r['rough']:.2f}", font_size=26))
            for cell, x in zip(row, xs):
                cell.move_to(RIGHT * x + UP * (1.45 - 0.95 * k), aligned_edge=LEFT)
            rows.add(row)
        with self.voiceover(
            "Harmonicity can. Write each chord as whole numbers. <bookmark mark='a'/> The major triad is four to "
            "five to six. Its three notes are neighbouring partials of one series, whose fundamental lies "
            "exactly two octaves below the chord's lowest note. That is the note you heard inside it in the last "
            "chapter. The whole chord repeats every four cycles of its lowest note. <bookmark mark='b'/> The "
            "minor triad is ten to twelve to fifteen. It fits a harmonic series too, but only as its tenth, "
            "twelfth and fifteenth partials, of a fundamental more than three octaves down. It takes ten cycles "
            "to repeat. The ear's search for a single source succeeds at once on the major chord, and only "
            "weakly on the minor. <bookmark mark='c'/> Two more chords complete the family. Listen to all four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        with self.listen(c) as snd:
            window(snd, r"major, \ minor, \ diminished, \ augmented", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for r, row in zip(d["rows"], rows):
                t0 = snd.time_of(r["name"])
                pulse(snd, row, t0, t0 + 1.8, buff=0.12)
        with self.voiceover(
            "The diminished triad, two minor thirds, and the augmented, two major thirds. Both are rougher than "
            "the first two, and both fit a harmonic series only very high up: twenty-five to thirty to "
            "thirty-six, and sixteen to twenty to twenty-five. Rough, and hard to fuse. Composers have always "
            "used them as chords that must move on. But here is a warning. Both of our measures put the "
            "diminished chord last. In listening experiments it is usually the augmented chord that people like "
            "least. Two causes explain a great deal, and not everything."
        ):
            self.play(Indicate(VGroup(rows[2][1], rows[3][1]), color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def map(self):
        d = load("triads")
        grid = np.asarray(d["grid"])
        steps = np.asarray(d["steps"])
        lo, hi = float(grid.min()), float(np.percentile(grid, 97))
        img = heat_image(-grid[::-1], -hi, -lo, 5.2, 5.2)
        frame = Square(side_length=5.2, stroke_color=GREY_D, stroke_width=1.2)
        pic = Group(img, frame).move_to(LEFT * 2.9 + DOWN * 0.2)

        def at(a, b):
            fx = (a - steps[0]) / (steps[-1] - steps[0])
            fy = (b - steps[0]) / (steps[-1] - steps[0])
            return frame.get_corner(DL) + RIGHT * 5.2 * fx + UP * 5.2 * fy

        ticks = VGroup(*[label(str(k), font_size=18, color=GREY_B).next_to(at(k, steps[0]), DOWN, buff=0.1) for k in range(1, 7)],
                       *[label(str(k), font_size=18, color=GREY_B).next_to(at(steps[0], k), LEFT, buff=0.1) for k in range(1, 7)])
        xl = label(r"lower interval (semitones)", font_size=20, color=GREY_B).next_to(frame, DOWN, buff=0.4)
        yl = label(r"upper interval (semitones)", font_size=20, color=GREY_B).rotate(PI / 2).next_to(frame, LEFT, buff=0.45)
        head = label(r"every chord of three notes: \ bright is smooth", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        named = [v for v in d["valleys"] if v["name"]]
        marks = VGroup(*[Circle(radius=0.14, color=WHITE, stroke_width=2.5).move_to(at(v["lower"], v["upper"])) for v in named])
        lst = VGroup(*[label(rf"({v['lower']:.0f}, {v['upper']:.0f}) \quad {v['name']}", font_size=24, color=GREY_A) for v in sorted(named, key=lambda v: (v["name"]))]
                     ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 0.9)
        quartal = next((v for v in d["valleys"] if not v["name"] and abs(v["lower"] - 5) < 0.2 and abs(v["upper"] - 5) < 0.2), None)
        qm = Circle(radius=0.16, color=LIMIT, stroke_width=3).move_to(at(5, 5))
        ql = VGroup(label(r"(5, 5): \ two fourths stacked", font_size=24, color=LIMIT), label(r"as smooth as a major triad, \\ and it fuses poorly: \ 9 : 12 : 16", font_size=22, color=GREY_A)
                    ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(lst, DOWN, buff=0.45).align_to(lst, LEFT)
        with self.voiceover(
            "With a formula for roughness we can do something no theorist before the computer could: lay out "
            "every possible chord of three notes at once. <bookmark mark='a'/> Across, the interval from the "
            "bottom note to the middle one. Up, the interval from the middle to the top. Bright is smooth, dark "
            "is rough. The dark bands along the edges are chords containing a semitone or a tone. "
            "<bookmark mark='b'/> And the bright spots, the valleys of this landscape, are chords with names. "
            "Four and three semitones: the major triad. Three and four: the minor. And around them the same two "
            "chords with their notes in another order, which musicians call inversions. <bookmark mark='c'/> One "
            "valley has no place in classical harmony: two fourths stacked. Roughness rates it as smooth as a "
            "major triad. But as whole numbers it is nine to twelve to sixteen, and it fuses poorly. Classical "
            "composers treated it as a dissonance. Jazz pianists, four centuries later, made it a signature "
            "sound. The map shows what the ear's hardware allows. What a culture does with it is another matter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), LaggedStart(*[FadeIn(x) for x in lst], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("c")
            if quartal is not None:
                self.play(Create(qm), FadeIn(ql))
        self.wait(0.3)
        self.clear_scene()
