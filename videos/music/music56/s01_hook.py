from __future__ import annotations

from videos.music.music56.common import *  # noqa: F403

NAMES = {"wall": r"a wall of sound", "dub": r"a dub", "dry": r"close and dry"}
COLS = {"wall": EAR, "dub": BLUE, "dry": TUNE}


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.session()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"Headphones on. \ One recording of the Tune by a small band, \ mixed three times: \ close and dry, \ a wall of sound, \ "
                           r"and a dub, \ in some order. \ Which was the dub?", width=10.0)
        with self.voiceover(
            "A question for your ears, with headphones. One recording of the Tune, by a small band, mixed three times: close "
            "and dry, a wall of sound, and a dub, in some order. Which was the dub?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one recording, \ three mixes", kind="physical model", detail=r"our session band", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], st["third"] - 0.4, buff=0.08)
            pulse(snd, boxes[2], st["third"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        me = d["measures"]
        rows = VGroup(VGroup(label(r"mix", font_size=17, color=GREY_A), label(r"what was done", font_size=17, color=GREY_A),
                             label(r"crest factor", font_size=17, color=GREY_A), label(r"L--R correlation", font_size=17, color=GREY_A)))
        what = {"wall": r"every part doubled or tripled, \ an echo chamber, \ the bus crushed, \ all in the centre",
                "dub": r"drums and bass up front, \ the voice in fragments into a tape echo, \ a spring on the snare, \ drops",
                "dry": r"close microphones, \ panned, \ carved, \ a little room"}
        for i, k in enumerate(d["order"]):
            rows.add(VGroup(label([r"first", r"second", r"third"][i] + r": \ " + NAMES[k], font_size=18, color=COLS[k]), label(what[k], font_size=15, color=WHITE),
                            label(f"{me[k]['crest_db']:.0f} dB", font_size=18, color=WHITE), label(f"{me[k]['correlation']:.2f}", font_size=18, color=WHITE)))
        rows.arrange(DOWN, buff=0.4)
        xs = [-4.6, -0.3, 3.6, 5.4]
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(xs[i])
        for r in rows[1:]:
            r[1].scale_to_fit_width(min(r[1].width, 4.6)).set_x(xs[1])
        rows.move_to(DOWN * 0.2)
        note = label(r"the same nine tracks, \ the same notes, \ the same performances", font_size=19, color=TUNE).to_edge(DOWN, buff=0.45)
        head = label(r"the second was the dub", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second. <bookmark mark='a'/> The first was a wall of sound: every part doubled or tripled, an echo chamber, "
            "the whole mix squeezed through a compressor, and everything in the centre; its crest factor, the peaks over the "
            f"average, is only {say(me['wall']['crest_db'])} decibels. <bookmark mark='b'/> The second, the dub: drums and bass "
            "pushed forward, the voice let through only in fragments, into a tape echo, a spring reverb on the snare, and the "
            "drums dropped out near the end. <bookmark mark='c'/> The third, close and dry: each microphone close to its "
            "instrument, panned, carved, with a little of the room. <bookmark mark='d'/> The same tracks, the same notes, the "
            "same performances: three different pieces of music."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            for mark, r in zip("abc", rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"until the 1950s a record was a performance, \ caught as well as possible", WHITE),
            (r"then tape, \ and many tracks: \ Les Paul layering his own guitar; \ Phil Spector's wall of sound \ (1962 on)", WHITE),
            (r"Jamaica, \ 1970s: \ King Tubby and Lee Perry remix songs into dubs on the mixing desk, \ live, \ as performances", WHITE),
            (r"1979: \ Brian Eno lectures on `the recording studio as a compositional tool'", WHITE),
            (r"the studio became an instrument; \ this part learns to play it", TUNE),
        ]
        rows_scene(self, r"the studio as an instrument", items,
                   "This is the story of the last seventy years of popular music. <bookmark mark='b'/> Until the 1950s a record was "
                   "a performance, caught as well as it could be. <bookmark mark='c'/> Then came tape, and many tracks: Les Paul "
                   "layering his own guitar on itself, and from 1962 Phil Spector's wall of sound, a dozen musicians in a small "
                   "room, doubled and drenched in echo. <bookmark mark='d'/> In Jamaica in the 1970s, King Tubby and Lee Perry "
                   "remixed songs into dubs at the mixing desk, live, muting and echoing as a performance in itself. "
                   "<bookmark mark='e'/> In 1979 Brian Eno lectured on the recording studio as a compositional tool. "
                   "<bookmark mark='f'/> The studio had become an instrument, and this part learns to play it.", marks="bcdef")

    # ------------------------------------------------------------------
    def session(self):
        names = [(r"voice", r"Part 8's soprano, \ and a second take", TUNE), (r"piano", r"Part 38's piano, \ a chord every two beats", BLUE),
                 (r"guitar", r"Part 38's guitar, \ arpeggios in eighths", "#A3E635"), (r"bass", r"Part 38's bass, \ root and fifth", EAR),
                 (r"kick, \ snare, \ hi-hat", r"Part 40's drums, \ three close microphones", GREY_A), (r"room", r"an ORTF pair, \ the whole band in a 1.2 s room", GREY_B)]
        rows = VGroup(*[VGroup(label(a, font_size=21, color=c_), label(b, font_size=17, color=WHITE)) for a, b, c_ in names]).arrange(DOWN, buff=0.32)
        for r in rows:
            r[0].set_x(-3.6)
            r[1].next_to([-1.6, r[0].get_y(), 0], RIGHT, buff=0)
        rows.move_to(DOWN * 0.2)
        head = label(r"the session: \ nine tracks, \ the Tune at 100 beats a minute", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The band is ours, built in earlier parts. <bookmark mark='a'/> Part 8's soprano sings the Tune, twice, so that it "
            "can be doubled. Part 38's piano plays a chord every two beats, its guitar arpeggios, its bass the root and the "
            "fifth. Part 40's drums have a close microphone each. <bookmark mark='b'/> And a pair of room microphones hears "
            "the whole band in a room that rings for one point two seconds. Nine tracks, a hundred beats a minute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows, 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:5]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"stereo microphone pairs, \ and where their images fall",
            r"phase between microphones, \ gain staging, \ editing",
            r"the console: \ balance, \ pan laws, \ equalization, \ buses",
            r"masking between tracks, \ mapped and carved",
            r"dynamics, \ depth and width, \ monitoring",
            r"automatic mixing, \ against ours",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Stereo microphone pairs, and where their images fall. <bookmark mark='b'/> Phase between "
            "microphones, gain staging and editing. <bookmark mark='c'/> The console: balance, pan laws, equalization and "
            "buses. <bookmark mark='d'/> Masking between tracks, mapped and carved. <bookmark mark='e'/> Dynamics, depth and "
            "width, and monitoring. <bookmark mark='f'/> And an automatic mixer, against ours."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
