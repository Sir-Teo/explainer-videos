from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Symbols(SoundScene):
    def construct(self):
        chapter(self, 9, r"Writing a chord down", r"How do you name a chord in one line?")
        self.four_ways()
        self.read()
        self.two_names()

    # ------------------------------------------------------------------
    def table(self, key: str):
        d = load("symbols")
        k = d["keys"][key]
        fig = [tex(b) + (rf"$\,^{{{f}}}$" if f else "") for b, f in zip(k["bass"], d["figured"])]
        rows = [(r"figured bass", r"about 1600", fig), (r"Roman numerals", r"about 1800", [r.replace("6", "$^6$").replace("7", "$^7$") for r in d["roman"]]),
                (r"lead sheet", r"1920s on", [tex(s).replace("7", "$^7$") for s in k["symbols"]]), (r"Nashville numbers", r"1950s", [n.replace("⁷", "$^7$") for n in d["nashville"]])]
        g = VGroup()
        g.cells = []
        for j, (nm, when, cells) in enumerate(rows):
            y = 2.0 - 0.95 * j
            head = VGroup(label(nm, font_size=28, color=WHITE), label(when, font_size=20, color=GREY_B)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([-5.0, y, 0], aligned_edge=LEFT)
            cs = VGroup(*[label(c, font_size=34, color=TUNE if j in (1, 3) else GREY_A).move_to([-1.2 + 1.5 * i, y, 0]) for i, c in enumerate(cells)])
            g.add(VGroup(head, cs))
            g.cells.append(cs)
        return g

    def four_ways(self):
        d = load("symbols")
        c = clip("symbols.prog")
        t = self.table("C")
        head = label(r"one progression, \ four ways to write it", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        keylab = label(r"in C", font_size=34, color=WHITE).move_to(RIGHT * 5.6 + UP * 2.9)
        with self.voiceover(
            "Chords are written down in at least four ways, and each tells you something different. "
            "<bookmark mark='a'/> Figured bass, from around sixteen hundred: a bass note, and numbers "
            "for the intervals above it. It tells a player what to play, and says nothing about roots. "
            "<bookmark mark='b'/> Roman numerals, from around eighteen hundred: the degree of the scale "
            "that the root stands on. They tell you the chord's job in the key. <bookmark mark='c'/> "
            "Lead-sheet symbols, from the dance bands of the nineteen twenties and thirties: the root "
            "by letter, then the kind of chord. They give you the notes and leave the voicing to you. "
            "<bookmark mark='d'/> And the Nashville number system, from the recording studios of the "
            "nineteen fifties: scale degrees in plain digits, so that a band can change key without "
            "rewriting anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keylab))
            for mark, r in zip("abcd", t):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.7)
        with self.voiceover(
            "Here is that progression in C, and then in E flat. Watch which of the four lines have to be rewritten."
        ):
            self.play(*[Indicate(cs, color=WHITE, scale_factor=1.05) for cs in t.cells], run_time=1.5)
        t2 = self.table("Eb")
        kb = keys(36, 72, width=9.0, height=1.0).to_edge(DOWN, buff=1.05)
        self.play(FadeIn(kb))
        with self.listen(c) as snd:
            window(snd, r"in C; \ then in E flat", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["voiced"]["C"] + d["voiced"]["Eb"], d["times"]["C"] + d["times"]["Eb"], end=c.duration)
            cols = [VGroup(*[cs[i] for cs in t.cells]) for i in range(5)]
            for i in range(5):
                pulse(snd, cols[i], d["times"]["C"][i], d["times"]["C"][i + 1] if i < 4 else d["times"]["C"][4] + 1.6, buff=0.1)
            snd.wait_until(d["start"]["Eb"] - 0.45)
            new_key = label(r"in E$\flat$", font_size=34, color=WHITE).move_to(keylab)
            self.remove(keylab, *t.cells[0], *t.cells[2])
            self.add(new_key, *t2.cells[0], *t2.cells[2])
            for cs in (t2.cells[0], t2.cells[2]):
                cs.set_color(EAR)
            cols2 = [VGroup(t2.cells[0][i], t.cells[1][i], t2.cells[2][i], t.cells[3][i]) for i in range(5)]
            for i in range(5):
                pulse(snd, cols2[i], d["times"]["Eb"][i], d["times"]["Eb"][i + 1] if i < 4 else c.duration, buff=0.1)
        kb.clear()
        cap = label(r"the letters all changed; \ the numbers did not.", font_size=32, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The letters all changed. The numbers did not. Roman numerals and Nashville numbers describe "
            "what each chord does; the letters describe which keys are under your fingers. A studio "
            "player handed a chart in numbers can play the song in any key the singer asks for."
        ):
            self.play(FadeOut(kb), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def read(self):
        d = load("symbols")
        rows = d["read"]
        pick = [1, 2, 3, 4, 5, 7]
        g = VGroup()
        for j, k in enumerate(pick):
            r = rows[k]
            y = 1.9 - 0.82 * j
            notes = r", \ ".join(tex(x) for x in r["labels"]) + (rf" \quad over {tex(r['bass'])}" if r["bass"] else "")
            g.add(VGroup(label(tex(r["text"]), font_size=36, color=TUNE).move_to([-5.2, y, 0], aligned_edge=LEFT), label(r["kind"], font_size=24, color=GREY_B).move_to([-2.4, y, 0], aligned_edge=LEFT),
                         label(notes, font_size=30, color=WHITE).move_to([1.6, y, 0], aligned_edge=LEFT)))
        head = label(r"a small language: \ root, \ triad, \ seventh, \ changes, \ / bass", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Lead-sheet symbols are a small formal language, and Monochord reads it. First the root. "
            "Then the triad: major, unless a small m says minor. Then the seventh: minor, unless it "
            "says m a j. Then any changes. Then, after a slash, the bass note. <bookmark mark='a'/> A "
            "minor seven: A, C, E, G. <bookmark mark='b'/> G seven over B: a dominant seventh on G with "
            "its third in the bass, which Rameau would call the first inversion. <bookmark mark='c'/> F "
            "sharp minor seven flat five is the half-diminished chord; D sus four replaces the third "
            "with a fourth; and a diminished seventh on B stacks three minor thirds."
        ) as vo:
            parts = VGroup(*[VGroup(label(a, font_size=64, color=c), label(b, font_size=24, color=c)).arrange(DOWN, buff=0.3) for a, b, c in
                             ((r"F$\sharp$", r"root", TUNE), (r"m", r"triad", MINOR_C), (r"7", r"seventh", WHITE), (r"$\flat$5", r"change", EAR), (r"/A", r"bass", BLUE))]).arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to(DOWN * 0.3)
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(x) for x in parts], lag_ratio=0.9), run_time=11.0)
            vo.wait_until("a")
            self.play(FadeOut(parts), FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
            self.wait(1.5)
            self.play(FadeIn(g[2]))
            vo.wait_until("c")
            self.play(LaggedStart(FadeIn(g[3]), FadeIn(g[4]), FadeIn(g[5]), lag_ratio=0.8), run_time=6.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_names(self):
        d = load("symbols")
        row = chord_row([["C4", "E4", "G4", "A4"]], width=3.2, space=0.26).move_to(LEFT * 4.4 + UP * 0.6)
        names = VGroup(VGroup(label(r"Am$^7$/C", font_size=44, color=MINOR_C), label(r"stack thirds from A: \ A, \ C, \ E, \ G", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15),
                       VGroup(label(r"C$^6$", font_size=44, color=MAJOR_C), label(r"a C triad with a sixth added", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.7).move_to(RIGHT * 1.6 + UP * 0.6)
        cap = label(r"a chord symbol is already an analysis.", font_size=32, color=TUNE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "But the symbols inherit Rameau's problem. Take C, E, G, A. <bookmark mark='a'/> Stack it in "
            "thirds from A, and it is an A minor seventh chord with C in the bass. <bookmark mark='b'/> "
            "Call C the root, and it is a C chord with an added sixth. The notes cannot tell you which, "
            "and in chapter 5 the root model was split almost evenly. What decides is context: what "
            "the bass does next, and which chord came before. <bookmark mark='c'/> So a chord symbol is "
            "never just a description of the notes. It is already a small act of analysis."
        ) as vo:
            self.play(FadeIn(row))
            vo.wait_until("a")
            self.play(FadeIn(names[0]), row.notes[0].heads[3].animate.set_color(MINOR_C))
            vo.wait_until("b")
            self.play(FadeIn(names[1]), row.notes[0].heads[0].animate.set_color(MAJOR_C))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
