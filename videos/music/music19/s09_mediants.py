from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Mediants(SoundScene):
    def construct(self):
        chapter(self, 8, r"Chromatic mediants", r"Can two chords be close without sharing a key?", extra=((1996, r"Cohn's hexatonic cycles"),))
        self.thirds()
        self.cycle()
        self.hear()

    # ------------------------------------------------------------------
    def thirds(self):
        d = load("mediants")
        st = block_staff(d["mediants"], width=5.2, beats=2, flats=True).move_to(LEFT * 3.4 + DOWN * 0.2)
        nm = VGroup(*[label(tex(n), font_size=24, color=TUNE) for n in d["mediant_names"]])
        for k, n in enumerate(nm):
            n.move_to([st.get_left()[0] + 1.0 + (st.width - 1.2) * (k + 0.5) / len(nm), st.get_bottom()[1] - 0.4, 0])
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"C major to E major: \ roots a major third apart", WHITE),
            (r"one note held \ (E), \ two move by a semitone", WHITE),
            (r"E major has four sharps: \ not a chord of C major at all", WHITE),
            (r"C, \ E, \ A$\flat$, \ C: \ three major thirds, \ round the octave", TUNE),
            (r"Schubert, \ Liszt, \ and every film score that wants wonder", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.8))
        rows_.move_to(RIGHT * 3.0 + DOWN * 0.1)
        with self.voiceover(
            "The trapdoors relied on spelling. Another road to distant keys relies on smooth motion alone. "
            "<bookmark mark='a'/> Move from C major to E major, whose root is a major third above. "
            "<bookmark mark='b'/> E stays where it is; C slips down a semitone to B; G slips up to G sharp. "
            "<bookmark mark='c'/> E major has four sharps; it is not a chord of C major, and yet the move is as "
            "smooth as any in the key. Such pairs are called chromatic mediants. <bookmark mark='d'/> Do it again, E to "
            "A flat, and again, A flat to C: three major thirds go round the octave. <bookmark mark='e'/> Schubert and "
            "Liszt loved these moves, and film composers still use them when they want a sense of wonder."
        ) as vo:
            self.play(FadeIn(st), FadeIn(nm))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cycle(self):
        d = load("mediants")
        names = d["names"][:6]
        centre = LEFT * 3.0 + DOWN * 0.2
        R = 2.1
        pts = [centre + R * np.array([np.sin(2 * np.pi * k / 6), np.cos(2 * np.pi * k / 6), 0]) for k in range(6)]
        nodes = VGroup()
        for k, (p, n) in enumerate(zip(pts, names)):
            maj = d["cycle"][k][1] == "major"
            c_ = Circle(radius=0.42, color=TUNE if maj else BLUE, stroke_width=3, fill_color=TUNE if maj else BLUE, fill_opacity=0.18).move_to(p)
            nodes.add(VGroup(c_, label(tex(n), font_size=24, color=WHITE).move_to(p)))
        edges = VGroup()
        tags = VGroup()
        for k in range(6):
            a, b = pts[k], pts[(k + 1) % 6]
            ln = Line(a, b, buff=0.45, color=GREY_B, stroke_width=3)
            edges.add(ln)
            mid = (a + b) / 2
            out = (mid - centre) / np.linalg.norm(mid - centre)
            tags.add(label("P" if k % 2 == 0 else "L", font_size=22, color=EAR).move_to(mid + 0.32 * out))
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"P \ (parallel): \ C major to C minor, \ the third moves a semitone", WHITE),
            (r"L \ (leading-tone exchange): \ C minor to A$\flat$ major, \ the fifth moves a semitone", WHITE),
            (r"alternate them: \ six triads, \ each one semitone from the last", WHITE),
            (r"and back to C: \ the hexatonic cycle", TUNE),
            (r"Riemann's moves, \ Cohn's cycles: \ neo-Riemannian theory", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.8))
        rows_.move_to(RIGHT * 3.2 + DOWN * 0.1)
        with self.voiceover(
            "There is a theory of these moves that ignores keys altogether. <bookmark mark='a'/> Call P the move from "
            "a major triad to the minor triad on the same root: one note, the third, moves by a semitone. "
            "<bookmark mark='b'/> Call L the leading-tone exchange: keep two notes and move the third by a semitone. "
            "C minor is C, E flat, G; raise G to A flat, and it is A flat major. <bookmark mark='c'/> Alternate "
            "them, P, L, P, L, and every step moves a single voice by a single semitone. <bookmark mark='d'/> After six "
            "steps you are back at C major, having passed through A flat and E major on the way. Richard Cohn called "
            "this the hexatonic cycle in 1996. <bookmark mark='e'/> The moves go back to Hugo Riemann in the 1880s, and "
            "their modern theory is called neo-Riemannian."
        ) as vo:
            self.play(FadeIn(nodes[0]))
            vo.wait_until("a")
            self.play(Create(edges[0]), FadeIn(tags[0]), FadeIn(nodes[1]), FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(Create(edges[1]), FadeIn(tags[1]), FadeIn(nodes[2]), FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(Create(edges[k]), FadeIn(tags[k]), FadeIn(nodes[k + 1])) for k in range(2, 5)], lag_ratio=0.4), FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(Create(edges[5]), FadeIn(tags[5]), FadeIn(rows_[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows_[4]))
        self.cyc = (nodes, edges, tags)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("mediants")
        c = clip("mediants.cycles")
        g1 = chord_roll(d["mediants"], width=3.6, height=2.8, lo=34, hi=84).move_to(LEFT * 4.3 + DOWN * 0.3)
        g2 = chord_roll(d["chords"], width=6.6, height=2.8, lo=34, hi=84).move_to(RIGHT * 2.3 + DOWN * 0.3)
        n1 = VGroup(*[label(tex(n), font_size=22, color=TUNE) for n in d["mediant_names"]])
        n2 = VGroup(*[label(tex(n), font_size=22, color=TUNE) for n in d["names"]])
        for g, names in ((g1, n1), (g2, n2)):
            w = g[0].width / len(names)
            for k, n in enumerate(names):
                n.move_to([g[0].get_left()[0] + w * (k + 0.5), g[0].get_bottom()[1] - 0.35, 0])
        t1 = label(r"major thirds", font_size=26, color=GREY_A).next_to(g1, UP, buff=0.35)
        t2 = label(r"the hexatonic cycle", font_size=26, color=GREY_A).next_to(g2, UP, buff=0.35)
        vl = label(rf"every step: \ {d['voice_leading'][0]} semitone of motion in all", font_size=24, color=EAR).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Hear both. First the cycle of major thirds, C, E, A flat, C. Then the hexatonic cycle, six chords and "
            "home. Watch the three upper bars: in the second, only one of them moves at each step, by a single semitone, "
            "while the bass simply follows the root."
        ):
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(n1), FadeIn(n2), FadeIn(t1), FadeIn(t2))
        with self.listen(c) as snd:
            window(snd, r"thirds, \ then the hexatonic cycle", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing_chords(snd, g1, d["times"]["thirds"])
            flash(snd, list(n1), d["times"]["thirds"], hot=WHITE, base=TUNE)
            sing_chords(snd, g2, d["times"]["hexatonic"])
            flash(snd, list(n2), d["times"]["hexatonic"], hot=WHITE, base=TUNE)
            pulse(snd, t1, 0.0, d["starts"]["hexatonic"] - 0.3, buff=0.08)
            pulse(snd, t2, d["starts"]["hexatonic"], c.duration, buff=0.08)
        with self.voiceover(
            "The ear follows the smallest motion, not the key signature. A minimal step can carry the music into a "
            "chord no key contains, and the listener accepts it, because each voice has barely moved. This is the "
            "second idea of chromatic harmony: closeness measured in semitones of motion, not in shared scales."
        ):
            self.play(FadeIn(vl))
        self.wait(0.4)
        self.clear_scene()
