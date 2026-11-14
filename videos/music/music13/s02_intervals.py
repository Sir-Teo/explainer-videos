from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Intervals(SoundScene):
    def construct(self):
        chapter(self, 1, r"Naming a distance", r"How far apart are two notes?")
        self.count()
        self.all()
        self.line()
        self.inversion()
        self.two_names()
        self.quiz()

    # ------------------------------------------------------------------
    def count(self):
        row = chord_row([["C4", "E4"], ["C4", "G4"], ["C4", "Eb4"]], width=6.4, space=0.24, below=[r"a third", r"a fifth", r"a third, \ too"], font_size=26).move_to(UP * 1.5)
        kb = keys(60, 72, width=6.0, height=1.5).move_to(DOWN * 1.6 + LEFT * 3.0)
        letters = VGroup(*[label(x, font_size=40, color=TUNE) for x in ("C", "D", "E")]).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.2 + RIGHT * 3.2)
        nums = VGroup(*[label(str(k + 1), font_size=26, color=GREY_A).next_to(letters[k], DOWN, buff=0.15) for k in range(3)])
        qual = VGroup(label(r"C to E: \ 4 semitones: \ a \textbf{major} third", font_size=28, color=MAJOR_C), label(r"C to E$\flat$: \ 3 semitones: \ a \textbf{minor} third", font_size=28, color=MINOR_C)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 1.5 + RIGHT * 3.0)
        with self.voiceover(
            "An interval is the distance between two notes, and its name has two parts. The first part "
            "is a number, and you get it by counting letters, including both ends. <bookmark mark='a'/> C "
            "to E: C, D, E. Three letters, so a third. <bookmark mark='b'/> C to G: five letters, a "
            "fifth. Notice that this counts both ends, the way people once counted days. That is why two "
            "thirds stacked make a fifth and not a sixth, and why the octave, the eighth note, is only "
            "seven steps away."
        ) as vo:
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(letters[k], nums[k])) for k in range(3)], lag_ratio=0.5), run_time=1.6)
            self.play(FadeIn(row.below[0]))
            vo.wait_until("b")
            self.play(FadeIn(row.notes[1]), FadeIn(row.below[1]))
        with self.voiceover(
            "The number tells you how the interval looks on the staff. It does not tell you how it "
            "sounds, because <bookmark mark='a'/> C to E and C to E flat are both thirds: both span "
            "three letters. So there is a second part to the name, the quality. <bookmark mark='b'/> The "
            "larger third, four semitones, is major. The smaller, three semitones, is minor."
        ) as vo:
            self.play(FadeOut(letters), FadeOut(nums), FadeIn(kb))
            vo.wait_until("a")
            self.play(FadeIn(row.notes[2]), FadeIn(row.below[2]), FadeIn(row.staff.barlines))
            vo.wait_until("b")
            kb.on(60), kb.on(64)
            self.play(FadeIn(qual[0]), row.notes[0].ink.animate.set_color(MAJOR_C))
            kb.on(63, BLUE)
            self.play(FadeIn(qual[1]), row.notes[2].ink.animate.set_color(MINOR_C))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def all(self):
        d = load("intervals")
        c = clip("intervals.all")
        rows = d["rows"]
        kb = keys(60, 72, width=7.0, height=1.7).move_to(DOWN * 1.3)
        chips = VGroup(*[label(r["short"], font_size=24, color=GREY_B) for r in rows]).arrange(RIGHT, buff=0.34).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Here is every interval from C up to the octave. Each one twice: the two notes in turn, "
            "then together. Watch the names go by."
        ):
            self.play(FadeIn(kb), LaggedStart(*[FadeIn(x) for x in chips], lag_ratio=0.08), run_time=2.0)
        shown = None
        with self.listen(c) as snd:
            window(snd, r"thirteen intervals", detail=r"from C: \ each note, \ then both", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [[60, 60 + k] for k in range(13)], d["both"], end=c.duration)
            flash(snd, list(chips), d["times"], hot=GOLD, base=GREY_B, fade=0.5, hold=1.5)
            for k, r in enumerate(rows):
                snd.wait_until(f"i{k}")
                if shown is not None:
                    self.remove(*shown)
                name = label(r["name"], font_size=44, color=TUNE).move_to(UP * 1.3)
                semi = label(rf"{r['semitones']} semitone{'s' if r['semitones'] != 1 else ''}: \ C to {tex(r['label'])}", font_size=28, color=GREY_A).next_to(name, DOWN, buff=0.25)
                shown = [name, semi]
                self.add(name, semi)
        kb.clear()
        self.remove(*shown)
        groups = VGroup(
            VGroup(label(r"seconds, \ thirds, \ sixths, \ sevenths", font_size=30, color=WHITE), label(r"two sizes: \ major and minor", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(label(r"unisons, \ fourths, \ fifths, \ octaves", font_size=30, color=WHITE), label(r"one size: \ perfect; \ $+1$ augmented, \ $-1$ diminished", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(label(r"six semitones", font_size=30, color=EAR), label(r"C to F$\sharp$: \ augmented fourth \quad C to G$\flat$: \ diminished fifth", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.4)
        with self.voiceover(
            "Seconds, thirds, sixths and sevenths come in two sizes, major and minor. <bookmark mark='a'/> "
            "Unisons, fourths, fifths and octaves come in one, called perfect. Make a perfect interval a "
            "semitone larger and it is augmented; a semitone smaller, diminished. <bookmark mark='b'/> And "
            "in the middle sits one distance with two names. Six semitones is an augmented fourth if you "
            "write it C to F sharp, and a diminished fifth if you write it C to G flat."
        ) as vo:
            self.play(FadeOut(kb), FadeIn(groups[0]))
            for k in (2, 3, 4, 8, 9, 10, 11, 1):
                chips[k].set_color(MAJOR_C if rows[k]["quality"] == "major" else MINOR_C)
            vo.wait_until("a")
            for k in (0, 5, 7, 12):
                chips[k].set_color(WHITE)
            self.play(FadeIn(groups[1]))
            vo.wait_until("b")
            self.play(FadeIn(groups[2]), Indicate(chips[6], color=EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def line(self):
        d = load("intervals")
        ln = d["line"]
        gap = 0.98
        cells = VGroup()
        for k, e in enumerate(ln):
            col = TUNE if e["line"] == 0 else WHITE
            cells.add(VGroup(label(tex(e["label"]), font_size=32, color=col), label(e["short"], font_size=22, color=GREY_B)).arrange(DOWN, buff=0.3).move_to([(k - 6) * gap, 0, 0]))
        links = VGroup(*[Line([(k - 6) * gap + 0.3, 0.32, 0], [(k - 5) * gap - 0.3, 0.32, 0], color=GREY_D, stroke_width=2) for k in range(12)])
        row = VGroup(cells, links).move_to(UP * 0.6)
        head = label(r"the line of fifths: \ each note a fifth above the one to its left", font_size=28, color=GREY_A).to_edge(UP, buff=0.6)

        def span(a, b, text, color, y):
            br = Line([cells[a + 6].get_left()[0], y, 0], [cells[b + 6].get_right()[0], y, 0], color=color, stroke_width=5)
            return VGroup(br, label(text, font_size=24, color=color).next_to(br, DOWN, buff=0.12))

        y = row.get_bottom()[1] - 0.35
        perfect, major, minor = span(-1, 1, r"perfect", WHITE, y), span(2, 5, r"major", MAJOR_C, y), span(-5, -2, r"minor", MINOR_C, y)
        aug, dim = span(6, 6, r"augmented", RED, y), span(-6, -6, r"diminished", RED, y)
        with self.voiceover(
            "Why these names? One picture explains all of them at once. Lay the notes out in fifths: "
            "the chain from Part 12, with C in the middle. Under each note is its interval above C. "
            "<bookmark mark='a'/> Now the quality of an interval is simply how far apart its two notes "
            "are on this line. One step: perfect. <bookmark mark='b'/> Two to five steps to the right: "
            "major. <bookmark mark='c'/> Two to five steps to the left: minor. <bookmark mark='d'/> Six "
            "or more: augmented on the right, diminished on the left."
        ) as vo:
            self.play(FadeIn(head), FadeIn(links), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.06), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(perfect))
            vo.wait_until("b")
            self.play(FadeIn(major))
            vo.wait_until("c")
            self.play(FadeIn(minor))
            vo.wait_until("d")
            self.play(FadeIn(aug), FadeIn(dim))
        moral = VGroup(label(r"sharpward is major; \ flatward is minor.", font_size=34, color=TUNE),
                       label(r"an interval's quality is a direction on the line of fifths.", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So major and minor are not moods that happen to be attached to intervals. They are "
            "directions. Sharpward along the line of fifths is major; flatward is minor. It is the same "
            "line that ordered the modes from bright to dark in Part 12, and it is the same reason: a "
            "major interval is one whose upper note lies on the bright side of the lower."
        ):
            self.play(FadeIn(moral))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inversion(self):
        d = load("intervals")
        row = chord_row([["C4", "E4"], ["E4", "C5"], ["C4", "G4"], ["G4", "C5"]], width=7.5, space=0.22, below=[r"major third", r"minor sixth", r"perfect fifth", r"perfect fourth"], font_size=24).move_to(UP * 1.7)
        sums = VGroup(label(r"$3 + 6 = 9$", font_size=30, color=TUNE), label(r"$5 + 4 = 9$", font_size=30, color=TUNE)).arrange(RIGHT, buff=2.4).next_to(row, DOWN, buff=0.3)
        rule = VGroup(label(r"major $\leftrightarrow$ minor", font_size=28, color=WHITE), label(r"augmented $\leftrightarrow$ diminished", font_size=28, color=WHITE),
                      label(r"perfect stays perfect", font_size=28, color=WHITE)).arrange(RIGHT, buff=0.7).next_to(sums, DOWN, buff=0.4)
        names = [r"semitone", r"tone", r"minor third", r"major third", r"fourth", r"tritone"]
        classes = VGroup(*[VGroup(label(str(k + 1), font_size=30, color=TUNE), label(nm, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.12) for k, nm in enumerate(names)]).arrange(RIGHT, buff=0.55)
        chead = label(r"six interval classes", font_size=26, color=GREY_A)
        cls = VGroup(chead, classes).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Turn an interval upside down, by lifting its lower note an octave, and you have its "
            "inversion. C up to E is a major third. <bookmark mark='a'/> E up to C is a minor sixth. A "
            "fifth becomes a fourth. <bookmark mark='b'/> The numbers always add up to nine, and the "
            "qualities swap: major with minor, augmented with diminished; perfect stays perfect. On the "
            "line of fifths, inversion is the same distance walked the other way."
        ) as vo:
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.notes[0]), FadeIn(row.below[0]))
            vo.wait_until("a")
            self.play(FadeIn(row.notes[1]), FadeIn(row.below[1]))
            self.play(FadeIn(row.notes[2]), FadeIn(row.below[2]), FadeIn(row.notes[3]), FadeIn(row.below[3]), FadeIn(row.staff.barlines))
            vo.wait_until("b")
            self.play(FadeIn(sums), FadeIn(rule))
        with self.voiceover(
            "And if you do not care which way up an interval is, only six kinds are left: the interval "
            "classes. Semitone, tone, minor third, major third, fourth, tritone. The interval vector of "
            "Part 12 counted exactly these six, and they are the six ways two notes can sound together."
        ):
            self.play(FadeIn(chead), LaggedStart(*[FadeIn(x) for x in classes], lag_ratio=0.2), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_names(self):
        d = load("intervals")
        c = clip("intervals.tritones")
        ev = c.events
        bx = boxes((r"C -- F$\sharp$", r"C -- G$\flat$", r"the piano"), buff=0.6, width=3.2, height=1.3, font_size=34).move_to(UP * 0.8)
        cents = VGroup(*[label(t, font_size=26, color=GREY_A).next_to(bx[k], DOWN, buff=0.2) for k, t in
                         enumerate((rf"{d['aug4']:.0f} cents", rf"{d['dim5']:.0f} cents", r"600 cents"))])
        head = label(r"quarter-comma meantone \ (Part 6): \ two names, \ two pitches", font_size=28, color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "One key of the piano with two names: is that only pedantry? Not in the tunings of Part 6. "
            "In quarter-comma meantone, where the fifths are narrowed to make the thirds pure, F sharp "
            f"and G flat are different pitches, {say(d['dim5'] - d['aug4'])} cents apart. Listen to C "
            "with F sharp, then C with G flat, and then the single compromise a piano offers."
        ):
            self.play(FadeIn(head), FadeIn(bx), FadeIn(cents))
        with self.listen(c) as snd:
            window(snd, r"two tritones, \ then one", kind="synthesized", detail=r"organ tones on middle C", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], ev["aug4"], ev["dim5"] - 0.3)
            pulse(snd, bx[1], ev["dim5"], ev["equal"] - 0.3)
            pulse(snd, bx[2], ev["equal"], c.duration)
        moral = VGroup(label(r"the first is close to $7:5$, \ the second to $10:7$.", font_size=28, color=GREY_A),
                       label(r"the spelling remembers what the keyboard forgot.", font_size=32, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The augmented fourth was close to the ratio seven to five, the diminished fifth to ten to "
            "seven: two different intervals, which equal temperament folds into one key. The spelling "
            "remembers what the keyboard forgot: where a note comes from, and, as we will see, where it "
            "wants to go."
        ):
            self.play(FadeIn(moral))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        c = clip("intervals.quiz")
        ev = c.events
        card = listen_card(r"Three intervals above middle C. \ One of them is the tritone. \ Which: \ A, \ B or C?", width=9.0)
        with self.voiceover("Try your ear. Three intervals above middle C. One of them is the tritone. Which: A, B or C?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B", "C"), buff=0.9, width=2.2, height=1.2, font_size=48).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], ev["A"], ev["B"] - 0.4)
            pulse(snd, bx[1], ev["B"], ev["C"] - 0.4)
            pulse(snd, bx[2], ev["C"], c.duration)
        ans = VGroup(label(r"A: \ perfect fourth", font_size=28, color=GREY_A), label(r"B: \ the tritone", font_size=30, color=TUNE), label(r"C: \ perfect fifth", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.9).move_to(DOWN * 1.4)
        with self.voiceover(
            "B. A was a perfect fourth and C a perfect fifth: open, steady sounds. The tritone sits "
            "between them, a semitone from each, and it is the restless one. Remember that restlessness. "
            "In chapter 6 it becomes the engine of harmony."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
