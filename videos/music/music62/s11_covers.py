from __future__ import annotations

from videos.music.music62.common import *  # noqa: F403


class Covers(SoundScene):
    def construct(self):
        chapter(self, 10, r"Covers, \ and how far people agree", r"When are two recordings the same song?")
        self.quiz()
        self.method()
        self.wild()
        self.agreement()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("cover")
        c = clip("cover.three")
        card = listen_card(r"Three recordings. \ Two are versions of one song, \ in different keys, \ tempos and instruments. \ Which is the odd one out?", width=9.5)
        with self.voiceover("Your turn. Three recordings. Two are versions of one song, in different keys, tempos and instruments. Which is the odd one out?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three recordings", kind="physical model", detail=r"Part 56's session, \ Part 38's piano", corner=DL, tag_corner=DR)
            ks = ["first", "second", "third"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = label(r"the third: \ Fr\`ere Jacques; \ the second is the Tune, \ a fourth higher, \ with rubato", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The third, Frère Jacques. The second was the Tune, a fourth higher and with rubato, on the piano. Easy for you; a machine has to be told that a key and a tempo are not the song."):
            self.play(boxes[2][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def method(self):
        d = load("cover")["scores"]
        rows_ = VGroup()
        for k, name, col in (("cover", r"the Tune, \ a fourth up", TUNE), ("other", r"Fr\`ere Jacques", EAR)):
            s = d[k]
            rows_.add(VGroup(label(name, font_size=20, color=col), label(f"{s['cost_no_shift']:.3f}", font_size=20, color=WHITE),
                             label(f"{s['cost']:.3f}", font_size=20, color=WHITE), label(f"{s['shift']}", font_size=20, color=WHITE)))
        rows_.arrange(DOWN, buff=0.5)
        for r in rows_:
            r[0].set_x(-4.0)
            r[1].set_x(-0.4)
            r[2].set_x(2.3)
            r[3].set_x(4.8)
        top = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([x, rows_.get_top()[1] + 0.55, 0]) for t, x in
                       ((r"DTW cost as heard", -0.4), (r"best over 12 keys", 2.3), (r"semitones shifted", 4.8))])
        eq = MathTex(r"\mathrm{sim}(X, Y) = \min_{k \in 0..11}\ \mathrm{DTW}\big(X,\ \mathrm{roll}_k(Y)\big)", font_size=32, color=WHITE).to_edge(UP, buff=1.0)
        note = label(r"lower is closer: \ the cover, \ rotated five semitones, \ is far closer than the other song", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"key-invariant matching", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The machine's version of your judgment: <bookmark mark='a'/> compare chroma sequences by time warping, which "
            "forgives the tempo, and try all twelve rotations of the chroma, which forgives the key. <bookmark mark='b'/> The "
            f"cover's best rotation is {d['cover']['shift']} semitones, the fourth it was transposed by, and its cost falls well "
            "below Frère Jacques's. <bookmark mark='c'/> Systems built this way searched thousands of recordings for covers in "
            "the 2000s; networks trained on cover pairs do it now."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(top), FadeIn(VGroup(*[r[0] for r in rows_])), FadeIn(VGroup(*[r[1] for r in rows_])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[VGroup(r[2], r[3]) for r in rows_])), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wild(self):
        items = [
            (r"a cover can change everything but the song: \\ key, \\ tempo, \\ instruments, \\ genre, \\ even the structure", WHITE),
            (r"2011: \\ the SecondHandSongs collection gives thousands of real cover pairs to test on", WHITE),
            (r"uses: \\ royalty tracking for live performances, \\ finding versions, \\ and Part 60's similarity questions", WHITE),
            (r"where covers end and influence begins is a question for courts, \\ not for DTW", TUNE),
        ]
        rows_scene(self, r"covers in the wild", items,
                   "Real covers are harder. <bookmark mark='b'/> A cover can change everything but the song: key, tempo, instruments, "
                   "genre, even the structure. <bookmark mark='c'/> In 2011 the SecondHandSongs collection gave thousands of real "
                   "cover pairs to test on. <bookmark mark='d'/> The uses are practical: tracking royalties for live performances, "
                   "finding versions, and Part 60's questions of similarity. <bookmark mark='e'/> And where covers end and influence "
                   "begins is a question for courts, not for time warping.", marks="bcde")

    # ------------------------------------------------------------------
    def agreement(self):
        items = [
            (r"every number in this part was scored against an answer key; \ for recordings, \ people make the keys", WHITE),
            (r"beats: \ annotators tap at different levels, \ and disagree by tens of milliseconds", WHITE),
            (r"chords: \ is that a C or a Cmaj7? \ a passing chord or a new harmony?", WHITE),
            (r"structure: \ two experts' boundaries for the same song agree only partly \ (the SALAMI collection, \ 2011, \ has two per song)", WHITE),
            (r"when annotators agree only so far, \ no system can be measured as better than that: \ the ceiling of the task", TUNE),
        ]
        rows_scene(self, r"how far people agree", items,
                   "One more limit, for every chapter of this part. <bookmark mark='b'/> Every number here was scored against an "
                   "answer key, and for real recordings people make the keys. <bookmark mark='c'/> Beats: annotators tap at "
                   "different levels and disagree by tens of milliseconds. <bookmark mark='d'/> Chords: is that a C or a C major "
                   "seventh, a passing chord or a new harmony? <bookmark mark='e'/> Structure: two experts' boundaries for the same "
                   "song agree only in part; the SALAMI collection of 2011 has two annotations per song to show it. "
                   "<bookmark mark='f'/> When people agree only so far, no system can be shown to do better than that: the ceiling "
                   "of the task. Monochord's renders have exact keys; real music never will.", marks="bcdef")
