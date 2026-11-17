from __future__ import annotations

from videos.music.music57.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.turn()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"Part 56's mix, \ mastered twice: \ once gently, \ once for maximum loudness. \ Here they are played "
                           r"at exactly the same loudness. \ Which was mastered for loudness?", width=10.0)
        with self.voiceover(
            "In 2008 Metallica fans compared two releases of the same songs, waveform by waveform. Compare by ear first. Part 56's mix, mastered twice: once gently, once for as much loudness as it would "
            "take. Here they are played at exactly the same loudness. Which was mastered for loudness?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two masters, \ one loudness", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        war = load("war")
        g, w = d["gentle"], d["war"]
        e14, e7 = war["env"]["-14.0"], war["env"]["-7.0"]
        a1 = frame_axes(width=10.0, height=1.5, xlo=0, xhi=len(e14), ylo=-1, yhi=1, center=UP * 0.9)
        a2 = frame_axes(width=10.0, height=1.5, xlo=0, xhi=len(e7), ylo=-1, yhi=1, center=DOWN * 1.3)

        def shape(env, ax, col):
            top = [ax.to(i, v) for i, v in enumerate(env)]
            bot = [ax.to(i, -v) for i, v in reversed(list(enumerate(env)))]
            return Polygon(*(top + bot), stroke_width=0, fill_color=col, fill_opacity=0.75)
        s1, s2 = shape(e14, a1, TUNE), shape(e7, a2, EAR)
        l1 = label(rf"gentle: \ {g['lufs']:.0f} LUFS, \ peaks {g['plr']:.0f} dB above the loudness, \ limited by at most {g['gr_max']:.0f} dB", font_size=17, color=TUNE).next_to(a1, UP, buff=0.1)
        l2 = label(rf"for loudness: \ {w['lufs']:.1f} LUFS, \ peaks {w['plr']:.0f} dB above, \ limited by up to {w['gr_max']:.0f} dB", font_size=17, color=EAR).next_to(a2, UP, buff=0.1)
        head = label(r"the second was mastered for loudness", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second. <bookmark mark='a'/> Here are the two waveforms, as delivered. The gentle master reaches minus "
            f"fourteen LUFS, a unit we will build, and its peaks stand {say(g['plr'])} decibels above its loudness. "
            "<bookmark mark='b'/> The loud master is six decibels louder, and to get there its peaks were pushed down by up to "
            f"{say(w['gr_max'])} decibels; they stand only {say(w['plr'])} above. At the same loudness, it is the one whose "
            "drums lost their snap: the sausage, engineers call that waveform."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(ghost(VGroup(s1, s2), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(s2), FadeIn(l2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"September 2008: \ Metallica release \textit{Death Magnetic}", WHITE),
            (r"the CD is mastered so loud that its peaks are shaved flat: \ clipped, \ audibly, \ on track after track", WHITE),
            (r"the same songs, \ released for the game \textit{Guitar Hero III}, \ were mastered with far less limiting", WHITE),
            (r"fans compared the waveforms, \ posted them, \ and petitioned for a remaster; \ the press called it a casualty of the loudness war", WHITE),
            (r"a war fought since the jukebox: \ louder sounds better for a moment, \ so every record tried to be louder than the last", TUNE),
        ]
        rows_scene(self, r"a casualty with waveforms", items,
                   "The question has a history. <bookmark mark='b'/> In September 2008 Metallica released Death Magnetic. <bookmark mark='c'/> The CD was mastered so loud that its peaks were shaved flat, clipped, audibly, on track after track. <bookmark mark='d'/> The same songs, released for the video game Guitar Hero Three, used a less heavily limited version, which many fans preferred. <bookmark mark='e'/> Fans compared the waveforms, posted them, and petitioned for a remaster; the press called the album a casualty of the loudness war. <bookmark mark='f'/> A war fought since the jukebox: louder sounds better for a moment, so every record tried to be louder than the one before.", marks="bcdef")

    # ------------------------------------------------------------------
    def turn(self):
        items = [
            (r"then the playback changed: \ streaming services began turning every track to the same loudness", WHITE),
            (r"a record mastered louder is simply turned down, \ and keeps only the damage", WHITE),
            (r"the playback-level incentive weakened; \ the war's weapons \ (meters, \ limiters) \ became the peace's instruments", WHITE),
            (r"this part builds them: \ a loudness meter, \ a true-peak meter, \ a limiter, \ a mastering chain, \ dither", TUNE),
        ]
        rows_scene(self, r"how normalization changed the incentive", items,
                   "Normalization later changed the incentive, though loud mastering continued. <bookmark mark='b'/> Many streaming services introduced loudness normalization, with settings and policies that vary. <bookmark mark='c'/> A record mastered louder is simply turned down, and keeps only the damage. <bookmark mark='d'/> The automatic playback-level advantage was reduced on normalized playback, and the war's weapons, meters and limiters, became the instruments of the peace. <bookmark mark='e'/> This part builds them: a loudness meter, a true-peak meter, a limiter, a mastering chain, and dither.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"what mastering is for, \ and its chain",
            r"meters: \ peak, \ VU, \ and BS.1770's gated loudness, \ checked against ffmpeg",
            r"true peaks, \ limiters and clippers",
            r"the loudness war in numbers, \ and normalization",
            r"comparing at equal loudness; \ dither",
            r"vinyl, \ delivery, \ and this series' own levels",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. What mastering is for, and its chain. <bookmark mark='b'/> Meters: peak, VU, and the gated "
            "loudness of BS.1770, checked against an independent meter. <bookmark mark='c'/> True peaks, limiters and "
            "clippers. <bookmark mark='d'/> The loudness war in numbers, and normalization. <bookmark mark='e'/> Comparing at "
            "equal loudness, and dither. <bookmark mark='f'/> And vinyl, delivery, and the levels of this series itself."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
