from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Tendency(SoundScene):
    def construct(self):
        chapter(self, 6, r"Where notes want to go", r"Does each note have a direction?", extra=((1956, r"Meyer's \textit{Emotion and Meaning}"),))
        self.gap()
        self.inertia()
        self.degrees()
        self.quiz()

    # ------------------------------------------------------------------
    def gap(self):
        g = load("tendency")["gap_fill"]
        demo = roll([0, 9, 7, 5, 4, 2], [1, 1, 1, 1, 1, 2], width=5.2, height=2.4, lines=(), color=TUNE).move_to(LEFT * 3.6 + UP * 0.3)
        brace = Brace(Line([demo.notes[0].get_right()[0], demo.notes[0].get_center()[1], 0], [demo.notes[0].get_right()[0], demo.notes[1].get_center()[1], 0]), LEFT, color=EAR, buff=0.4)
        bl = label(r"the gap", font_size=24, color=EAR).next_to(brace, LEFT, buff=0.1)
        fl = label(r"the fill", font_size=24, color=TUNE).next_to(demo.notes[3], DOWN, buff=0.4)
        pb = pair_bars([(r"leaps that are filled, \ in a hundred", 100 * g["real"], 100 * g["walks"])], width=4.4, height=2.6, names=(r"the tunes", r"by chance: \ the same moves, \ the same range"), top=60).move_to(RIGHT * 3.4 + DOWN * 0.6)
        pb.legend.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(pb, UP, buff=0.3)
        head = label(r"Leonard Meyer, \ 1956: \ a leap opens a gap, \ and the melody fills it", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Does any rule of melody survive that test? Here is a candidate. In 1956 Leonard Meyer "
            "proposed that a leap opens a gap, <bookmark mark='a'/> and that the melody then fills the "
            "gap, by steps, in the other direction. Count how often a leap of a fourth or more is "
            "followed by steps back into the gap. <bookmark mark='b'/> In our tunes: "
            f"{say(100 * g['real'])} leaps in a hundred. In melodies made by chance from the same moves, "
            f"confined to the same range: {say(100 * g['walks'])}. So gap-fill is partly arithmetic. "
            "But only partly. Something is left over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(demo))
            vo.wait_until("a")
            self.play(GrowFromCenter(brace), FadeIn(bl), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(pb), FadeIn(pb.legend))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def degrees(self):
        d = load("tendency")
        T = np.array(d["transitions"])
        hm = heat(T, size=4.2, color=TUNE, rows=list("1234567"), cols=list("1234567"), top=0.52).move_to(LEFT * 3.6 + DOWN * 0.4)
        rl = label(r"from", font_size=22, color=GREY_B).next_to(hm, LEFT, buff=0.15)
        cl = label(r"to", font_size=22, color=GREY_B).next_to(hm, UP, buff=0.1)
        goes = d["goes"]
        lines = VGroup(*[label(rf"{a} $\rightarrow$ {goes[a]['to']}: \quad {100 * goes[a]['p']:.0f} in a hundred", font_size=30, color=WHITE) for a in ("7", "4", "6", "2")]).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 0.5)
        home = label(rf"degrees 1, \ 3 and 5: \ {100 * d['triad']:.0f}\% of all the time", font_size=28, color=TUNE).next_to(lines, DOWN, buff=0.6)
        head = label(r"where each degree of the scale goes next", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        cells = {"7": (6, 0), "4": (3, 2), "6": (5, 4), "2": (1, 0)}
        with self.voiceover(
            "The clearest leftover is that the notes of a scale are not equal. Count where each degree "
            f"goes next. <bookmark mark='a'/> The seventh rises to the first {say(100 * goes['7']['p'])} "
            f"times in a hundred. <bookmark mark='b'/> The fourth falls to the third "
            f"{say(100 * goes['4']['p'])} times. <bookmark mark='c'/> The sixth falls to the fifth "
            f"{say(100 * goes['6']['p'])} times. <bookmark mark='d'/> The second falls to the first "
            f"{say(100 * goes['2']['p'])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hm), FadeIn(rl), FadeIn(cl))
            for mark, a, ln in zip("abcd", ("7", "4", "6", "2"), lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), Create(SurroundingRectangle(hm.cell[cells[a]], color=EAR, buff=0.02, stroke_width=3)), run_time=0.7)
        with self.voiceover(
            "These are the tendency tones. Degrees two, four, six and seven lean toward their "
            "neighbours one, three and five: the notes of the home chord of Part 13, where our tunes "
            f"spend {say(100 * d['triad'])} percent of their time. Shuffled notes do not lean. This is "
            "the scale itself at work: the pull of the tritone in Part 13, heard one note at a time."
        ):
            self.play(FadeIn(home))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("tendency")
        p = load("phrase")
        c = clip("tendency.endings")
        ev = c.events
        card = listen_card(r"One phrase, \ three last notes. \ Which one sounds finished: \ A, \ B or C?", width=8.8)
        with self.voiceover("Try your ear. One phrase, with three different last notes. Which one sounds finished: A, B or C?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        rolls = VGroup(*[roll(d["stem"] + [v], [1] * 6 + [2], width=3.6, height=2.0, lo=-2, hi=6, lines=(0,), color=WEAK) for v in d["endings"].values()]).arrange(RIGHT, buff=0.5).move_to(UP * 0.5)
        tags = VGroup(*[label(t, font_size=40, color=GREY_A).next_to(r, UP, buff=0.2) for t, r in zip("ABC", rolls)])
        self.play(FadeOut(card), FadeIn(rolls), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, key in enumerate("ABC"):
                sing(snd, rolls[k], d["times"][key], hot=WHITE, base=WEAK)
                pulse(snd, tags[k], ev[key], ev["ABC"[k + 1]] - 0.5 if k < 2 else c.duration, buff=0.12)
        ans = VGroup(*[label(t, font_size=24, color=col).next_to(r, DOWN, buff=0.25) for t, col, r in
                       zip((r"stays on the second", r"falls to the seventh", r"comes home to the first"), (GREY_A, GREY_A, TUNE), rolls)])
        fin = label(rf"last phrases that end on the first degree: \ {100 * p['final_end']['1']:.0f} in a hundred", font_size=28, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "C. In A the phrase stayed on the second degree; in B it fell to the seventh; in C it came "
            f"home to the first. <bookmark mark='a'/> In our tunes, {say(100 * p['final_end']['1'])} "
            "last phrases in a hundred end on the first degree. The others sound like a question "
            "waiting for an answer, and in the next chapter but one we will hear that used."
        ) as vo:
            self.play(FadeIn(ans), rolls[2].notes[-1].animate.set_fill(TUNE))
            vo.wait_until("a")
            self.play(FadeIn(fin))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inertia(self):
        d = load("more")["inertia"]
        rows = [(r"after a step down, \ another move down", 100 * d["real"]["down"], 100 * d["chance"]["down"]), (r"after a step up, \ another move up", 100 * d["real"]["up"], 100 * d["chance"]["up"])]
        pb = pair_bars(rows, width=8.5, height=2.4, names=(r"the tunes", r"by chance: \ the same moves, \ reshuffled")).move_to(LEFT * 1.6 + DOWN * 0.9)
        pb.legend.next_to(pb, UP, buff=0.3)
        land = VGroup(label(r"a leap lands on 1, \ 3 or 5", font_size=24, color=GREY_A), label(rf"{100 * d['leaps_on_triad']:.0f} in a hundred", font_size=34, color=TUNE),
                      label(rf"a step: \ {100 * d['steps_on_triad']:.0f}", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.6 + DOWN * 0.4)
        head = label(r"two more habits, \ put to the same test", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Two more habits pass the test. The first is momentum. <bookmark mark='a'/> After a step "
            f"down, the next move is down again {say(100 * d['real']['down'])} times in a hundred; "
            f"chance would give {say(100 * d['chance']['down'])}. After a step up, the tune keeps "
            f"climbing {say(100 * d['real']['up'])} times, against {say(100 * d['chance']['up'])}. A line "
            "that is walking tends to keep walking, especially downhill. <bookmark mark='b'/> The second "
            "is where leaps land. A leap arrives on the first, third or fifth degree of the scale "
            f"{say(100 * d['leaps_on_triad'])} times in a hundred; a step, only "
            f"{say(100 * d['steps_on_triad'])}. Tunes walk through the scale, and jump along the chord. "
            "Part 13's triad is inside the melody."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pb), FadeIn(pb.legend))
            vo.wait_until("b")
            self.play(FadeIn(land))
        self.wait(0.4)
        self.clear_scene()
