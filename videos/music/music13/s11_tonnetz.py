from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


def net_names(a, b):
    from videos.music.music13.compute import lattice_name

    return {(i, j): lattice_name(i, j) for j in range(b[0], b[1] + 1) for i in range(a[0], a[1] + 1)}


class Net(SoundScene):
    def construct(self):
        chapter(self, 10, r"A map of chords", r"Which chords are neighbours?", extra=((1739, r"Euler's lattice of tones"),))
        self.lattice()
        self.moves()
        self.cycle()
        self.all24()

    # ------------------------------------------------------------------
    def lattice(self):
        a, b = (-3, 3), (-1, 2)
        net = Tonnetz(a, b, dx=1.35, names=net_names(a, b), font_size=26, radius=0.33).move_to(DOWN * 0.5)
        fifth = Arrow(net.at(0, 0), net.at(1, 0), buff=0.36, color=TUNE, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        third = Arrow(net.at(0, 0), net.at(0, 1), buff=0.36, color=BLUE, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        legend = VGroup(label(r"$\rightarrow$ \ a fifth up", font_size=26, color=TUNE), label(r"$\nearrow$ \ a major third up", font_size=26, color=BLUE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
        with self.voiceover(
            "In 1739 Leonhard Euler, the mathematician, drew a map of musical notes. Put fifths along "
            "one direction: F, C, G, D. <bookmark mark='a'/> Put major thirds along another: C, E, G "
            "sharp. <bookmark mark='b'/> Then every note has six neighbours, the six notes most "
            "consonant with it; and every small triangle is a triad."
        ) as vo:
            self.play(FadeIn(net), run_time=1.5)
            self.play(GrowArrow(fifth), FadeIn(legend[0]))
            vo.wait_until("a")
            self.play(GrowArrow(third), FadeIn(legend[1]))
            vo.wait_until("b")
            self.play(*[Indicate(net.node[c], color=WHITE, scale_factor=1.2) for c in ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))])
        up = net.show(net.tri(0, 0, "major", color=MAJOR_C))
        down = net.show(net.tri(0, 0, "minor", color=MINOR_C))
        cap = VGroup(label(r"$\triangle$ \ major: \ C, \ E, \ G", font_size=28, color=MAJOR_C), label(r"$\triangledown$ \ minor: \ C, \ E$\flat$, \ G", font_size=28, color=MINOR_C)).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Triangles that point up are major triads: C, E, G. <bookmark mark='a'/> Triangles that "
            "point down are minor: C, E flat, G. German theorists of the next century named the map the "
            "Tonnetz, the net of tones. Euler drew it to think about tuning. It turned out to be a map "
            "of harmony."
        ) as vo:
            self.play(FadeOut(fifth), FadeOut(third), FadeIn(up), FadeIn(cap[0]))
            vo.wait_until("a")
            self.play(FadeIn(down), FadeIn(cap[1]))
        self.wait(0.4)
        self.play(FadeOut(down), FadeOut(cap), FadeOut(legend))
        self.net, self.up = net, up

    # ------------------------------------------------------------------
    def moves(self):
        d = load("tonnetz")
        c = clip("tonnetz.plr")
        net, up = self.net, self.up
        tris = {"P": net.tri(0, 0, "minor", color=MINOR_C), "L": net.tri(0, 1, "minor", color=MINOR_C), "R": net.tri(-1, 1, "minor", color=MINOR_C)}
        for t in tris.values():
            net.show(t)
            t.set_opacity(0.0)
        rows = VGroup(label(r"P: \ C major $\rightarrow$ C minor \quad E falls a semitone", font_size=26, color=WHITE),
                      label(r"L: \ C major $\rightarrow$ E minor \quad C falls a semitone", font_size=26, color=WHITE),
                      label(r"R: \ C major $\rightarrow$ A minor \quad G rises a tone", font_size=26, color=WHITE)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).to_edge(UP, buff=0.3)

        def reveal(t):
            return t.animate.set_stroke(opacity=1.0).set_fill(opacity=0.4)

        with self.voiceover(
            "On this map, the chords closest to a triad are the three that share an edge with it: two "
            "notes kept, one moved. From C major: <bookmark mark='a'/> flip over the edge C to G, and "
            "the E falls a semitone. C minor, the parallel. <bookmark mark='b'/> Flip over E to G, and "
            "the C falls a semitone to B. E minor. <bookmark mark='c'/> Flip over C to E, and the G "
            "rises a whole tone to A. A minor, the relative minor of Part 12. Each is the smallest "
            "change a triad can make and still be a triad. Listen to the three."
        ) as vo:
            vo.wait_until("a")
            self.play(reveal(tris["P"]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(reveal(tris["L"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(reveal(tris["R"]), FadeIn(rows[2]))
        with self.listen(c) as snd:
            window(snd, r"three smallest moves", detail=r"C major to each neighbour", corner=DL, tag_corner=DR)
            spans = {}
            for k, m in enumerate("PLR"):
                a, b = d["plr_times"][m]
                end = d["plr_times"]["PLR"[k + 1]][0] - 0.2 if k < 2 else c.duration
                pulse(snd, rows[k], a, end, buff=0.08)
                spans[m] = (a, b, end)

            def fn(_, t):
                on_c = any(a <= t < b for a, b, _e in spans.values())
                up.set_fill(opacity=0.85 if on_c else 0.25)
                for m, (a, b, end) in spans.items():
                    tris[m].set_fill(opacity=0.85 if b <= t < end else 0.2)

            snd.drive(up, fn)
        up.set_fill(opacity=0.45)
        for t in tris.values():
            t.set_fill(opacity=0.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cycle(self):
        d = load("tonnetz")
        c = clip("tonnetz.hexa")
        a, b = (-1, 2), (-3, 1)
        net = Tonnetz(a, b, dx=1.25, names=net_names(a, b), font_size=24, radius=0.31).move_to(LEFT * 3.3 + DOWN * 0.1)
        path = Tonnetz.walk(0, 0, "major", "PLPLPL")
        tris = [net.show(net.tri(i, j, k, color=MAJOR_C if k == "major" else MINOR_C)) for i, j, k in path]
        for t in tris[1:]:
            t.set_opacity(0.0)
        names = [x[2] for x in d["cycles"]["PL"]] + ["C"]
        chips = VGroup(*[label(tex(n), font_size=34, color=GREY_B) for n in names]).arrange(DOWN, buff=0.22).move_to(RIGHT * 1.6 + DOWN * 0.1)
        kb = keys(55, 72, width=4.2, height=1.3).move_to(RIGHT * 4.6 + UP * 0.4)
        note = label(r"every step: \ one voice, \ one semitone", font_size=24, color=GREY_A).next_to(kb, DOWN, buff=0.35)
        with self.voiceover(
            "Chain the flips, and you travel. Alternate the first two moves, and you go round a cycle "
            "of six triads: C major, C minor, A flat major, A flat minor, E major, E minor, and back to "
            "C. At every step one voice moves, by one semitone."
        ):
            self.play(FadeIn(net), FadeIn(chips), FadeIn(kb), FadeIn(note), run_time=1.5)
        t = d["hexa_times"]
        with self.listen(c) as snd:
            window(snd, r"six triads and home", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["hexa_voicings"], t, end=c.duration)
            flash(snd, list(chips), t, hot=GOLD, base=GREY_B, fade=0.8, hold=0.9)
            for k in range(1, 7):
                snd.wait_until(t[k])
                tris[k - 1].set_fill(opacity=0.12).set_stroke(opacity=0.5)
                tris[k].set_stroke(opacity=1.0).set_fill(opacity=0.5)
        kb.clear()
        with self.voiceover(
            "That sound, major and minor triads sliding by semitones with no key in charge, is in "
            "Schubert and Wagner and Brahms, and in a great deal of film music since."
        ):
            self.play(Indicate(chips, color=TUNE, scale_factor=1.03))
        top, bot = net.node[(0, 0)], net.node[(0, -3)]
        marks = VGroup(SurroundingRectangle(top, color=EAR, buff=0.06, corner_radius=0.1), SurroundingRectangle(bot, color=EAR, buff=0.06, corner_radius=0.1))
        cm = d["commas"]
        cap = VGroup(label(r"C, \ and D$\flat\flat$ three major thirds below", font_size=28, color=EAR), label(rf"on a piano: \ the same key", font_size=26, color=WHITE),
                     label(rf"in pure tuning: \ {cm['diesis']:.0f} cents apart", font_size=26, color=WHITE), label(r"equal temperament rolls the map up", font_size=28, color=TUNE)).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.3 + DOWN * 0.2)
        with self.voiceover(
            "And notice where we ended. <bookmark mark='a'/> Three major thirds below the C we started "
            "from, on a note whose proper name is D double flat. On a piano that is the same key as C. "
            "In pure tuning it is not: three pure major "
            f"thirds fall short of an octave by {say(cm['diesis'])} cents, the diesis of Part 6. "
            "<bookmark mark='b'/> Equal temperament is what rolls this map up, so that travelling far "
            "enough in any direction brings you home. On Euler's own map, in pure intervals, you would "
            "never come back at all."
        ) as vo:
            self.play(FadeOut(kb), FadeOut(note), FadeOut(chips))
            vo.wait_until("a")
            self.play(Create(marks), FadeIn(cap[0]), FadeIn(cap[1]), FadeIn(cap[2]))
            vo.wait_until("b")
            self.play(FadeIn(cap[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def all24(self):
        d = load("tonnetz")
        c = clip("tonnetz.lr")
        a, b = (0, 13), (0, 1)
        net = Tonnetz(a, b, dx=0.93, names=net_names(a, b), font_size=19, radius=0.26).move_to(UP * 0.9)
        path = Tonnetz.walk(0, 0, "major", "LR" * 12)
        tris = [net.show(net.tri(i, j, k, color=MAJOR_C if k == "major" else MINOR_C)) for i, j, k in path]
        for t in tris[1:]:
            t.set_opacity(0.0)
        names = [x[2] for x in d["cycles"]["LR"]] + ["C"]
        chips = VGroup(*[label(tex(n), font_size=24, color=GREY_B) for n in names]).arrange_in_grid(rows=2, cols=13, buff=(0.32, 0.25)).next_to(net, DOWN, buff=0.6)
        head = label(r"alternate L and R: \ all twenty-four major and minor triads", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Alternate the other two moves instead, and you run along a strip of the map, through all "
            "twenty-four major and minor triads before you return, each one keeping two notes of the "
            "one before. Beethoven runs along nineteen of them in the scherzo of his Ninth Symphony, as "
            "the theorist Richard Cohn pointed out. Here are all twenty-four."
        ):
            self.play(FadeIn(head), FadeIn(net), FadeIn(chips), run_time=1.5)
        t = d["lr_times"]
        with self.listen(c) as snd:
            window(snd, r"twenty-four triads and home", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(chips), t, hot=GOLD, base=GREY_B, fade=0.5, hold=0.45)
            for k in range(1, 25):
                snd.wait_until(t[k])
                tris[k - 1].set_fill(opacity=0.1).set_stroke(opacity=0.35)
                tris[k].set_stroke(opacity=1.0).set_fill(opacity=0.5)
        cap = label(rf"24 chords; \ three voices; \ {d['lr_motion']} semitones of motion in all", font_size=30, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            f"Twenty-four chords, and the three voices moved {say(d['lr_motion'])} semitones in all: a "
            "semitone and a half per chord. Had each chord been played in root position, they would "
            "have leapt hundreds. That economy, getting from chord to chord with the least motion, is "
            "called voice leading, and it is the subject of Part 17."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
