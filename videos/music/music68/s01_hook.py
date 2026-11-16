from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.aria()
        self.goldberg()
        self.series()
        self.plan()

    # ------------------------------------------------------------------
    def aria(self):
        d = load("hook")
        c = clip("hook.one")
        card = listen_card(r"Variation 1, \ exactly as Part 1 made it: \ the Tune on one simulated string. \ "
                           r"What do you hear in it now \ that you could not hear the first time?", width=9.6)
        with self.voiceover(
            "Sixty-seven parts ago this series began with one string, simulated, and with it played the Tune. Here is that "
            "Variation again, exactly as Part 1 made it. What do you hear in it now that you could not hear the first time?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ev = sorted(((k, v) for k, v in c.events.items() if k.startswith("n")), key=lambda kv: kv[1])
        notes = [(72 + {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}[deg], t, b) for (deg, b), (_, t) in zip(TUNE_NOTES, ev)]
        r = mroll([(m, t, b * 0.55 * 0.9) for m, t, b in notes], width=11.0, height=2.2, lo=70, hi=83, total=c.duration - 1.0)
        r.move_to(UP * 0.4)
        cap = label(r"Variation 1: \ " + d["title"], font_size=20, color=TUNE).next_to(r, DOWN, buff=0.5)
        self.play(FadeOut(card), FadeIn(r), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Variation 1", kind="physical model", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [t for _, t, _ in notes], hot=WHITE, base=TUNE)
            cursor(snd, r, 0.0, 1.0)
        res = VGroup(
            label(r"the same file, \ the same samples", font_size=22, color=WHITE),
            label(r"a fifth is now a ratio, \ a beat-free interval, \ a degree of a key, \ a step in a phrase, \ a line a machine can transcribe", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The same file, the same samples. <bookmark mark='a'/> But the opening leap is now many things at once: a ratio "
            "of three to two, an interval whose aligned harmonic partials do not beat against each other, a tonic-to-dominant move in this key, the first step of a phrase, and a line a "
            "machine could write down. The notes have not changed. The listener has."
        ) as vo:
            self.play(FadeIn(res[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def goldberg(self):
        items = [
            (r"1741: \ Bach publishes an aria with thirty variations for a harpsichord with two keyboards", WHITE),
            (r"every third variation a canon, \ at the unison, \ the second, \ and so on to the ninth; \ the thirtieth a quodlibet of folk songs", WHITE),
            (r"the variations keep the aria's bass and its harmony, \ not its melody", WHITE),
            (r"then the aria again, \ note for note: \ \textit{aria da capo}", TUNE),
            (r"the story of an insomniac count and his harpsichordist Goldberg \ comes from 1802, \ and may be a legend", GREY_A),
        ]
        rows_scene(self, r"the \textit{Goldberg Variations}", items,
                   "In 1741 Johann Sebastian Bach published an aria with thirty variations, for a harpsichord with two keyboards. "
                   "<bookmark mark='b'/> Every third variation through number twenty-seven is a canon, the first at the unison, the next at the second, and so "
                   "on up to the ninth; the thirtieth is a quodlibet, two folk songs sung over the bass. <bookmark mark='c'/> The "
                   "variations keep the aria's bass and harmony, not its melody. <bookmark mark='d'/> And at the end the aria "
                   "comes back, note for note: aria da capo. <bookmark mark='e'/> The story that gives the work its name, an "
                   "insomniac count and his harpsichordist Goldberg, was first told in 1802 and may be a legend. The da capo is "
                   "not: it is in the score.", marks="bcde")

    # ------------------------------------------------------------------
    def series(self):
        m = series_map(current=68, done=67, font_size=15).move_to(DOWN * 0.15)
        head = label(r"sixty-eight parts, \ sixty-seven Variations", font_size=26, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "This series is built the same way. Sixty-seven parts, each of which did something to the Tune with what it had "
            "just taught, from one string to a machine that writes. <bookmark mark='a'/> This is the last part. It does what "
            "the Goldberg does: it plays the Variations, and then the aria again. But first it does one thing no single part "
            "could: it runs the Tune through the whole chain the series built, from a score to a listener, and back to a "
            "score, and measures what survives."
        ) as vo:
            self.play(FadeIn(head), FadeIn(m))
            vo.wait_until("a")
            self.play(Indicate(m.part[68], color=TUNE, scale_factor=1.3), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the chain the series built, \ link by link",
            r"the Tune down the whole chain, \ heard and measured at each stage",
            r"and back up it: \ transcribed, \ quantized, \ identified",
            r"what survives the journey, \ and why notation kept what it kept",
            r"ordering sixty-seven Variations, \ and the suite in three movements",
            r"what was built, \ the ledger, \ what is still unknown; \ and the aria again",
        ], title=r"The plan", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> The chain the series built, link by link. <bookmark mark='b'/> The Tune "
            "down the whole chain, heard and measured at every stage. <bookmark mark='c'/> And back up it: transcribed, "
            "quantized and identified. <bookmark mark='d'/> What survives the journey, and why notation kept what it kept. "
            "<bookmark mark='e'/> How to order sixty-seven Variations, and then the suite itself, in three movements. And "
            "last, what was built, the ledger, what is still unknown, and the aria again."
        ) as vo:
            self.play(FadeIn(card.head))
            for mark, rr in zip("abcde", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
            self.play(FadeIn(card.rows[-1]), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
