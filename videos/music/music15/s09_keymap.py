from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class KeyMap(SoundScene):
    def construct(self):
        chapter(self, 8, r"A map of keys", r"Which keys are neighbours?", extra=((1728, r"Heinichen's circle of keys"),))
        self.circle()
        self.signatures()
        self.jumps()
        self.torus()

    # ------------------------------------------------------------------
    def circle(self):
        d = load("keymap")
        clock = fifths_clock(radius=2.0, font_size=30, signatures=True).move_to(LEFT * 3.3 + DOWN * 0.2)
        sh = d["shared"]
        rows = VGroup(label(r"a fifth away: \ 6 of 7 notes shared", font_size=28, color=WHITE), label(r"two fifths: \ 5 \quad three: \ 4 \quad four: \ 3", font_size=28, color=WHITE),
                      label(rf"the far side, \ F$\sharp$: \ {sh['F♯ major']} shared", font_size=28, color=EAR), label(r"sharps or flats in the signature = steps round the circle", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.3 + UP * 0.2)
        with self.voiceover(
            "There are twelve major keys. Are some closer to each other than others? The oldest answer "
            "is the circle of fifths, printed by Johann David Heinichen in 1728. <bookmark mark='a'/> "
            "Put the keys round a circle, each a fifth above the last. Part 12 showed why this is the "
            "right order: move a major scale up a fifth, and exactly one note changes. So neighbours on "
            "the circle share six of their seven notes; <bookmark mark='b'/> two steps away, five; and "
            "the key on the far side shares only two. <bookmark mark='c'/> The number of sharps or flats "
            "in a key signature is simply how many steps round the circle that key is from C."
        ) as vo:
            self.play(FadeIn(clock), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(clock.cell[7], color=TUNE), Indicate(clock.cell[5], color=TUNE), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), Indicate(clock.cell[6], color=EAR))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), *[Indicate(clock.sig[pc], color=WHITE) for pc in (7, 2, 9, 5, 10)])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jumps(self):
        d = load("keymap")
        c = clip("keymap.jumps")
        tags = VGroup(*[VGroup(label(t, font_size=32, color=WHITE), label(rf"$r = {d['pairs'][k]['r']:+.2f}$", font_size=26, color=GREY_A), label(rf"{d['pairs'][k]['shared']} notes shared", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.15)
                        for k, t in (("G", r"C major $\rightarrow$ G major"), ("a", r"C major $\rightarrow$ A minor"), ("Fs", r"C major $\rightarrow$ F$\sharp$ major"))]).arrange(RIGHT, buff=0.9).move_to(UP * 0.6)
        head = label(r"how alike are two keys' profiles?", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Krumhansl and Kessler measured closeness another way: by how alike two keys' profiles are. "
            "If the notes that fit one key also fit the other, the keys are close. For C major, the "
            f"closest key of all is A minor, with a correlation of {say(d['pairs']['a']['r'], 2)}; then "
            f"G major and F major, {say(d['pairs']['G']['r'], 2)}; and the furthest is F sharp major, at "
            f"minus {say(abs(d['pairs']['Fs']['r']), 2)}: what fits one is what does not fit the other. "
            "Hear the distances. A cadence in C, and then the same cadence in each of three keys."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.5), run_time=3.0)
        order = ("G", "a", "Fs")
        with self.listen(c) as snd:
            window(snd, r"near, \ nearest, \ far", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(order):
                pulse(snd, tags[i], d["starts"][k], d["starts"][order[i + 1]] - 0.4 if i < 2 else c.duration, buff=0.15)
        with self.voiceover(
            "The first two are steps into the next room. The third is a different building: for a "
            "moment after the change, nothing fits, and your sense of home has to be rebuilt from "
            "nothing. A film composer who wants the floor to drop away moves by that interval."
        ):
            self.play(Indicate(tags[2], color=EAR, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def torus(self):
        d = load("keymap")
        tm = torus_map(d["angles"], width=10.5, height=4.4, font_size=26).move_to(DOWN * 0.5)
        cap = label(r"capitals: \ major keys \quad small letters: \ minor keys \quad the left edge joins the right, \ the top joins the bottom", font_size=20, color=GREY_B).next_to(tm, DOWN, buff=0.2)
        head = label(rf"the 24 keys, \ placed by how alike their profiles are", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        c_, a_, g_, f_, cm = tm.cell[(0, "major")], tm.cell[(9, "minor")], tm.cell[(7, "major")], tm.cell[(5, "major")], tm.cell[(0, "minor")]
        with self.voiceover(
            "Now put all twenty-four keys on one map, so that keys with similar profiles are close "
            "together. A flat sheet cannot do it, and neither can a circle. Krumhansl and Kessler found "
            "that it takes a torus, the surface of a ring: here it is cut open and laid flat, so the "
            "left edge joins the right and the top joins the bottom. <bookmark mark='a'/> Find C major. "
            "Beside it are its relative minor, A minor, and its parallel minor, C minor; and along one "
            "line run the fifths: F, C, G. <bookmark mark='b'/> Nobody told the computation about "
            "circles of fifths, or relative keys. It was given ratings from listeners, and it drew the "
            "chart that Gottfried Weber drew by hand in 1817 from his experience of music."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tm), FadeIn(cap), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(c_, color=WHITE, scale_factor=1.8))
            self.play(Indicate(a_, color=WHITE, scale_factor=1.6), Indicate(cm, color=WHITE, scale_factor=1.6))
            self.play(Indicate(f_, color=WHITE, scale_factor=1.6), Indicate(g_, color=WHITE, scale_factor=1.6))
            vo.wait_until("b")
            self.play(FadeIn(label(rf"two circles hold {100 * d['explained']:.0f}\% of the differences between profiles", font_size=22, color=TUNE).next_to(head, DOWN, buff=0.15)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def signatures(self):
        d = load("more")["signatures"]
        sh = VGroup(*[label(rf"{x}$\sharp$", font_size=34, color=TUNE) for x in d["sharps"]]).arrange(RIGHT, buff=0.4)
        fl = VGroup(*[label(rf"{x}$\flat$", font_size=34, color=BLUE) for x in d["flats"]]).arrange(RIGHT, buff=0.4)
        ks = VGroup(*[label(tex(x), font_size=24, color=GREY_A) for x in d["keys_sharp"]])
        kf = VGroup(*[label(tex(x), font_size=24, color=GREY_A) for x in d["keys_flat"]])
        rows = VGroup(VGroup(label(r"sharps, \ in the order they are added", font_size=24, color=GREY_B), sh).arrange(DOWN, buff=0.25),
                      VGroup(label(r"flats, \ in the order they are added", font_size=24, color=GREY_B), fl).arrange(DOWN, buff=0.25)).arrange(DOWN, buff=1.1).move_to(UP * 0.5)
        for k, x in enumerate(ks):
            x.next_to(sh[k], DOWN, buff=0.2)
        for k, x in enumerate(kf):
            x.next_to(fl[k], DOWN, buff=0.2)
        cap = label(r"both rows are the line of fifths of Part 13, \ read in opposite directions", font_size=28, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "This is all a key signature is. Go one step clockwise from C, to G, and one note must be "
            "raised: F becomes F sharp. Another step, to D: C sharp as well. <bookmark mark='a'/> The "
            "sharps arrive in a fixed order: F, C, G, D, A, E, B. Under each is the key that it "
            "completes. <bookmark mark='b'/> Going the other way, the flats arrive in exactly the "
            "reverse order: B, E, A, D, G, C, F. <bookmark mark='c'/> Both rows are the line of fifths "
            "from Part 13. A signature is not a list to be memorised. It is an address: so many steps, "
            "in one direction or the other, from C. And at the bottom of the circle, six sharps and six "
            "flats name the same twelve keys of the piano: the circle closes, thanks to the equal "
            "temperament of Part 6."
        ) as vo:
            self.play(FadeIn(rows[0][0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in sh], lag_ratio=0.25), LaggedStart(*[FadeIn(x) for x in ks], lag_ratio=0.3), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]), LaggedStart(*[FadeIn(x) for x in fl], lag_ratio=0.25), LaggedStart(*[FadeIn(x) for x in kf], lag_ratio=0.3), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
