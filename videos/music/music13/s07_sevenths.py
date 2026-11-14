from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Sevenths(SoundScene):
    def construct(self):
        chapter(self, 6, r"Four notes, \ and more", r"What does a fourth note add?")
        self.kinds()
        self.scale()
        self.resolve()
        self.harmonic()
        self.tall()

    # ------------------------------------------------------------------
    def kinds(self):
        d = load("sevenths")
        c = clip("sevenths.kinds")
        ks = d["kinds"]
        names = [r"major 7th", r"dominant 7th", r"minor 7th", r"half-diminished", r"diminished 7th"]
        row = chord_row([k["names"] for k in ks], width=11.0, space=0.24, above=[k["symbol"] for k in ks], below=names, font_size=24).move_to(UP * 0.8)
        for k, x in enumerate(ks):
            row.notes[k].ink.set_color(KIND_COLOR[x["kind"]])
            row.above[k].set_color(KIND_COLOR[x["kind"]]).scale(1.25)
        with self.voiceover(
            "Add one more third on top of a triad and you have a seventh chord, named for the interval "
            "between its outside notes. There are five that every musician knows. <bookmark mark='a'/> A "
            "major triad with a major seventh. <bookmark mark='b'/> A major triad with a minor seventh: "
            "the dominant seventh. <bookmark mark='c'/> A minor triad with a minor seventh. "
            "<bookmark mark='d'/> A diminished triad with a minor seventh: half-diminished. "
            "<bookmark mark='e'/> And three minor thirds in a row: the diminished seventh."
        ) as vo:
            first = row.notes[0]
            first.heads[3].set_opacity(0.0)
            first.holes[3].set_opacity(0.0)
            lead = label(r"a triad, \ and one more third", font_size=30, color=GREY_A).to_edge(DOWN, buff=1.3)
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.staff.barlines), FadeIn(first), FadeIn(lead))
            self.wait(1.2)
            first.holes[3].set_opacity(1.0)
            self.play(first.heads[3].animate.set_opacity(1.0), Flash(first.heads[3], color=MAJOR_C), run_time=0.8)
            for k, mark in enumerate("abcde"):
                vo.wait_until(mark)
                if k == 0:
                    self.play(FadeOut(lead), FadeIn(row.above[0]), FadeIn(row.below[0]), run_time=0.6)
                    continue
                self.play(FadeIn(row.notes[k]), FadeIn(row.above[k]), FadeIn(row.below[k]), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"five seventh chords", detail=r"on middle C: \ Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(5):
                pulse(snd, row.above[k], d["times"][k], d["times"][k + 1] - 0.15 if k < 4 else c.duration, buff=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scale(self):
        d = load("sevenths")
        sc = d["scale"]
        row = chord_row([[n for n in CH_NAMES(c)] for c in sc], width=11.5, space=0.22, above=[c["symbol"] for c in sc], below=[c["roman"] for c in sc], font_size=26, below_color=WHITE).move_to(UP * 0.9)
        for k, x in enumerate(sc):
            row.notes[k].ink.set_color(KIND_COLOR[x["kind"]])
            row.above[k].set_color(KIND_COLOR[x["kind"]])
        tri = VGroup(label(r"B and F: \ the scale's one tritone", font_size=30, color=EAR),
                     label(r"G$^7$: \ the only major triad that carries it, \ as its third and its seventh", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Build sevenths on the degrees of the major scale, and four kinds appear. Major sevenths on "
            "one and four. Minor sevenths on two, three and six. A half-diminished seventh on seven. "
            "<bookmark mark='a'/> And one chord that occurs once only: the dominant seventh, on the "
            "fifth degree. <bookmark mark='b'/> It is a major triad with the scale's one tritone inside "
            "it: B, its third, and F, its seventh. Part 12 found that a major scale has exactly one "
            "tritone, and that this is what tells you which key you are in. Here it is, packed into a "
            "single chord. Hear a dominant seventh and you know where home is, before you have heard home."
        ) as vo:
            self.play(FadeIn(row), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(VGroup(row.notes[4], row.above[4], row.below[4]), color="#FB923C", scale_factor=1.2))
            vo.wait_until("b")
            self.play(row.notes[4].heads[1].animate.set_color(EAR), row.notes[4].heads[3].animate.set_color(EAR), FadeIn(tri))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def resolve(self):
        d = load("sevenths")
        c = clip("sevenths.resolve")
        t = d["resolve_times"]
        kb = keys(41, 72, width=10.0, height=1.9).move_to(UP * 0.8)
        arrows = VGroup(label(r"B $\rightarrow$ C: \ up a semitone", font_size=30, color=EAR), label(r"F $\rightarrow$ E: \ down a semitone", font_size=30, color=EAR)).arrange(RIGHT, buff=1.2).next_to(kb, DOWN, buff=0.5)
        with self.voiceover(
            "And the tritone moves. B is a semitone below C. F is a semitone above E. Let each go where "
            "it leans, and the tritone closes onto a third. First the two notes alone; then the whole "
            "chord, over its bass."
        ):
            self.play(FadeIn(kb), FadeIn(arrows))
            kb.on(59, RED), kb.on(65, RED)
        with self.listen(c) as snd:
            window(snd, r"a tritone, \ resolving", detail=r"B and F to C and E; \ then G$^7$ to C", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [[59, 65], [60, 64], [43, 59, 62, 65], [48, 60, 64]], t, end=c.duration, colors=[RED, GOLD, RED, GOLD])
            pulse(snd, arrows, t[0], t[2] - 0.2, buff=0.15)
        kb.clear()
        cap = VGroup(label(r"tension and release: \ two voices, \ a semitone each, \ in opposite directions", font_size=28, color=TUNE)).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Tension, and release, from two voices each moving one semitone, in opposite directions. "
            "Nearly every piece of tonal music you know ends with that motion. The five chord has a "
            "leading note and, with its seventh, a note that wants to fall; the one chord is where "
            "they both land."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonic(self):
        d = load("sevenths")
        c = clip("sevenths.just")
        ev = c.events
        card = listen_card(r"The same seventh chord, \ in two tunings. \ Which is smoother: \ A or B?", width=8.8)
        with self.voiceover("An ear question. The same seventh chord, twice, in two different tunings. Which is smoother: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 0.9)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"organ tones on middle C", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], ev["A"], ev["B"] - 0.4)
            pulse(snd, bx[1], ev["B"], c.duration)
        ans = VGroup(label(r"A: \ the piano's tuning: \ a seventh of 1000 cents", font_size=28, color=GREY_A),
                     label(rf"B: \ harmonics $4:5:6:7$: \ a seventh of {d['cents']['harmonic']:.0f} cents", font_size=28, color=TUNE),
                     label(rf"roughness, \ by Part 5's model: \ {d['roughness']['equal']:.2f} \ and \ {d['roughness']['just']:.2f}", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.4)
        with self.voiceover(
            "B. In A the chord was tuned as a piano tunes it. In B its four notes were the fourth, "
            "fifth, sixth and seventh harmonics of one fundamental. <bookmark mark='a'/> That seventh "
            f"harmonic is {say(1000 - d['cents']['harmonic'])} cents flatter than the piano's minor "
            "seventh, and with it the four notes fuse almost into one sound. Barbershop quartets tune "
            "the chord that way, and no keyboard can play it. Rameau's sounding body, one step further "
            "up the series."
        ) as vo:
            self.play(FadeIn(ans[0]), FadeIn(ans[1]))
            vo.wait_until("a")
            self.play(FadeIn(ans[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tall(self):
        d = load("sevenths")["tall"]
        c = clip("sevenths.stack")
        row = chord_row([d["names"]], width=3.4, space=0.26, clef="treble").move_to(LEFT * 4.3 + UP * 0.2)
        n = row.notes[0]
        tags = VGroup(*[label(rf"{m}: \ {tex(l)}", font_size=28, color=GREY_A) for m, l in zip(d["members"], d["labels"])]).arrange(UP, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 1.2 + UP * 0.2)
        with self.voiceover(
            "Why stop at four notes? Keep stacking thirds: above the seventh, the ninth; then the "
            "eleventh; then the thirteenth."
        ):
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.staff.barlines), FadeIn(n.ledgers), FadeIn(tags))
            for h in n.heads:
                h.set_opacity(0.0)
            n.holes.set_opacity(0.0)
            self.add(n)
        with self.listen(c) as snd:
            window(snd, r"thirds, \ stacked", detail=r"from middle C: \ Part 7's piano", corner=DL, tag_corner=DR)
            for j in range(7):
                snd.wait_until(f"n{j}")
                n.heads[j].set_opacity(1.0)
                if j < len(n.holes):
                    n.holes[j].set_opacity(1.0)
                tags[j].set_color(TUNE)
            pulse(snd, tags, d["times"][-1] + 0.4, c.duration, buff=0.15)
        scale = VGroup(*[label(x, font_size=40, color=TUNE) for x in "CDEFGAB"]).arrange(RIGHT, buff=0.4).move_to(RIGHT * 3.3 + UP * 0.6)
        cap = VGroup(label(r"a thirteenth chord is the whole scale,", font_size=28, color=WHITE), label(r"every other note at a time", font_size=28, color=WHITE)).arrange(DOWN, buff=0.12).next_to(scale, DOWN, buff=0.4)
        with self.voiceover(
            "Seven notes; and the next third would be the root again. Look at what they are. "
            "<bookmark mark='a'/> C, E, G, B, D, F, A. A thirteenth chord is the whole scale, taken "
            "every other note. So a chord and a scale are not two different things. They are the same "
            "seven notes, stacked or spread, and jazz harmony lives on that fact: to a jazz player, a "
            "chord symbol is also the name of a scale to improvise on."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in scale], lag_ratio=0.2), FadeIn(cap), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()


def CH_NAMES(c) -> list[str]:
    """The written names of a chord from the scale table (its MIDI keys, spelled in C major)."""
    from explainer.music.monochord.score import Pitch

    return [Pitch.from_midi(m).name for m in c["midis"]]
