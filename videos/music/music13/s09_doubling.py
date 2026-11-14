from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Doubling(SoundScene):
    def construct(self):
        chapter(self, 8, r"Which notes matter", r"Which notes can a chord do without?")
        self.double()
        self.leave()
        self.shells()
        self.power()

    # ------------------------------------------------------------------
    def double(self):
        d = load("doubling")
        rows = d["rows"]
        order = [1, 0, 3, 2]                               # root doubled, one of each, fifth doubled, third doubled
        g = VGroup()
        for j, k in enumerate(order):
            r = rows[k]
            w = 6.0 * (r["ambiguity"] - 1.5) / 0.6
            bar = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=TUNE if k == 1 else (EAR if k == 2 else WEAK), fill_opacity=0.9)
            bar.move_to([-1.0, 1.3 - 0.95 * j, 0], aligned_edge=LEFT)
            g.add(VGroup(label(r["label"], font_size=28, color=WHITE).next_to(bar, LEFT, buff=0.3), bar, label(f"{r['ambiguity']:.2f}", font_size=26, color=WHITE).next_to(bar, RIGHT, buff=0.15)))
        head = label(r"C, \ E, \ G in four voices: \ how ambiguous is the root?", font_size=30, color=GREY_A).to_edge(UP, buff=0.55)
        rule = label(r"in root position, \ double the root; \ double the third last", font_size=30, color=TUNE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "A triad has three notes. A choir has four voices, an orchestra dozens. Some note must be "
            "doubled. Which? Ask the root model of chapter 5, counting a doubled note twice. "
            "<bookmark mark='a'/> Double the root, and the root's lead grows: the chord is less "
            "ambiguous than with one of each. <bookmark mark='b'/> Double the fifth: slightly more "
            "ambiguous. <bookmark mark='c'/> Double the third: more ambiguous still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]))
            vo.wait_until("c")
            self.play(FadeIn(g[3]))
        with self.voiceover(
            "That is the rule every harmony student is taught. In root position, double the root; the "
            "third is the note you double last. The model gives one reason for it. Chapter 6 gave "
            "another: when the third of a chord is a leading note, two voices singing it would both "
            "want to move to the same place."
        ):
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def leave(self):
        d = load("doubling")
        db = d["partials_db"]
        f0 = 130.81
        rows = partial_rows([f0], [r"C"], n=6, width=10.0, f_lo=110.0, f_hi=900.0, row=0.5, colors=(GREY_B,), tick=0.45, font_size=30).move_to(UP * 1.0)
        ticks = rows.rows[0].ticks
        nums = VGroup(*[label(t, font_size=24, color=GREY_B).next_to(ticks[h], UP, buff=0.12) for h, t in enumerate(("1: C", "2: C", "3: G", "4: C", "5: E", "6: G"))])
        lev = label(rf"in Part 7's piano: \ only {abs(db[2]):.0f} dB below the fundamental", font_size=26, color=MAJOR_C).next_to(ticks[2], DOWN, buff=0.3)
        head = label(r"the harmonics of one C", font_size=28, color=GREY_A).to_edge(UP, buff=0.55)
        facts = VGroup(label(rf"leave out the fifth: \ the root is still {d['no_fifth']['root']}, \ and the chord is still major or minor", font_size=28, color=WHITE),
                       label(r"leave out the third: \ the root is clear, \ but the chord is neither", font_size=28, color=EAR)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "And if you must leave a note out? Leave out the fifth. It is hardly missed, and here is "
            "why. <bookmark mark='a'/> The root's own third harmonic is that same note. In a piano's C, "
            "the G an octave and a fifth above is already sounding, only "
            f"{say(abs(db[2]))} decibels below the fundamental. The fifth is in the chord whether "
            "anyone plays it or not. <bookmark mark='b'/> The third is different. The harmonic that "
            "would supply it is the fifth one, higher and weaker; and the third alone says whether the "
            "chord is major or minor. Leave it out and you have a root with no character."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(nums))
            vo.wait_until("a")
            self.play(ticks[2].animate.set_color(MAJOR_C), nums[2].animate.set_color(MAJOR_C), FadeIn(lev), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(ticks[4].animate.set_color(EAR), nums[4].animate.set_color(EAR), FadeIn(facts[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shells(self):
        d = load("doubling")
        c = clip("doubling.shell")
        t = d["shell_times"]
        kb = keys(48, 72, width=10.0, height=1.8).move_to(UP * 1.0)
        tags = VGroup(*[label(tex(x), font_size=26, color=GREY_A) for x in (r"C$^7$, \ every note", r"C$^7$", r"Cmaj$^7$", r"Cm$^7$")]).arrange(RIGHT, buff=1.0).next_to(kb, DOWN, buff=0.45)
        sub = label(r"root, \ third and seventh only", font_size=24, color=GREY_B).next_to(VGroup(*tags[1:]), DOWN, buff=0.2)
        with self.voiceover(
            "So the essential notes of a seventh chord are three: the root, the third and the seventh. "
            "Jazz pianists call that a shell. Here is a full seventh chord, and then three different "
            "seventh chords as shells. Listen to how much chord is left."
        ):
            self.play(FadeIn(kb), FadeIn(tags), FadeIn(sub))
        with self.listen(c) as snd:
            window(snd, r"a full chord, \ then three shells", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["shells"], t, end=c.duration, colors=[WEAK, GOLD, GOLD, BLUE])
            for k in range(4):
                pulse(snd, tags[k], t[k], t[k + 1] - 0.1 if k < 3 else c.duration, buff=0.12)
        kb.clear()
        cap = label(r"guide tones: \ the third says major or minor; \ the seventh says which seventh", font_size=28, color=TUNE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Three notes each, and every chord is unmistakable. The third and the seventh are called "
            "guide tones: between them they say what kind of chord it is. In a jazz group the bass "
            "player has the root, the pianist plays the guide tones, and everything else is free."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        d = load("doubling")
        c = clip("doubling.power")
        ev = c.events
        pw = d["power"]
        cols = VGroup()
        top = max(v["driven"] for v in pw.values())
        for k, (key, nm) in enumerate((("fifth", r"a fifth: \ E, \ B"), ("third", r"a major third: \ E, \ G$\sharp$"), ("triad", r"a triad: \ E, \ G$\sharp$, \ B"))):
            x = (k - 1) * 3.8
            hc, hd = 2.4 * pw[key]["clean"] / top, 2.4 * pw[key]["driven"] / top
            bc = Rectangle(width=0.7, height=hc, stroke_width=0, fill_color=WEAK, fill_opacity=0.9).move_to([x - 0.45, -1.7 + hc / 2, 0])
            bd = Rectangle(width=0.7, height=hd, stroke_width=0, fill_color=EAR if key != "fifth" else TUNE, fill_opacity=0.9).move_to([x + 0.45, -1.7 + hd / 2, 0])
            cols.add(VGroup(bc, bd, label(f"{pw[key]['clean']:.1f}", font_size=22, color=GREY_A).next_to(bc, UP, buff=0.1), label(f"{pw[key]['driven']:.1f}", font_size=24, color=WHITE).next_to(bd, UP, buff=0.1),
                            label(nm, font_size=26, color=WHITE).move_to([x, -2.1, 0])))
        legend = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=WEAK, fill_opacity=0.9), label(r"clean", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.12),
                        VGroup(Square(0.22, stroke_width=0, fill_color=EAR, fill_opacity=0.9), label(r"through a hard clipper", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.6).move_to(UP * 1.55)
        head = label(r"two guitar strings into a distorting amplifier: \ roughness, \ by Part 5's model", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Rock guitar went the other way, and for a reason you can now compute. A distorting "
            "amplifier is a nonlinear device. Feed it two notes, and it adds new tones at the sums and "
            "differences of all their partials. <bookmark mark='a'/> With a fifth, in the ratio three "
            "to two, those new tones land back on harmonics of a note an octave below: the sound gets "
            "thicker, and stays in tune with itself. With a major third, they land in the cracks. "
            "Here are two of Part 1's plucked strings through a hard clipper: a fifth, then a major "
            "third, then a full triad."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend))
            vo.wait_until("a")
            self.play(*[FadeIn(x[4]) for x in cols], *[FadeIn(VGroup(x[0], x[2])) for x in cols])
        with self.listen(c) as snd:
            window(snd, r"fifth, \ third, \ triad, \ distorted", detail=r"Part 1's strings, \ clipped", corner=DL, tag_corner=DR)
            pulse(snd, cols[0][4], ev["fifth"], ev["third"] - 0.3, buff=0.12)
            pulse(snd, cols[1][4], ev["third"], ev["triad"] - 0.3, buff=0.12)
            pulse(snd, cols[2][4], ev["triad"], c.duration, buff=0.12)
        with self.voiceover(
            "By the model, the distorted third is twice as rough as the distorted fifth, and the full "
            "triad is worse again. <bookmark mark='a'/> So the power chord is a root and a fifth, with "
            "no third: neither major nor minor. It is a voicing chosen by the amplifier. The same "
            "physics that makes a low third muddy on a piano makes a full chord muddy through "
            "distortion, and the musicians' answer was the same: leave notes out."
        ) as vo:
            self.play(*[FadeIn(VGroup(x[1], x[3])) for x in cols])
            vo.wait_until("a")
            self.play(Indicate(cols[0][4], color=TUNE))
        self.wait(0.4)
        self.clear_scene()
