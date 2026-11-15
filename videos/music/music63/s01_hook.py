from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.bar()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def bar(self):
        d = load("hook")
        lib = load("library")
        c = clip("hook.bar")
        phone = VGroup(RoundedRectangle(width=1.6, height=2.8, corner_radius=0.2, stroke_color=GREY_B, stroke_width=3),
                       Circle(radius=0.1, stroke_color=GREY_B).shift(DOWN * 1.15)).move_to(LEFT * 3.8 + UP * 0.2)
        waves = VGroup(*[Arc(radius=0.5 + 0.35 * k, angle=PI / 2, start_angle=-PI / 4, stroke_color=EAR, stroke_width=2).move_arc_center_to(phone.get_right() + RIGHT * 0.1) for k in range(3)])
        head = label(r"five seconds in a noisy bar", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Five seconds of music in a noisy bar, the music no louder than the voices and glasses around it. Can a machine say what it is?"):
            self.play(FadeIn(head), FadeIn(phone), FadeIn(waves))
        with self.listen(c) as snd:
            window(snd, r"a noisy bar", kind="physical model", detail=r"one of the series' sounds, \ simulated noise", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(phone, waves), 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.15)
        r = d["result"][0]
        ans = VGroup(label(rf"{r['track'].split('/')[1]}", font_size=34, color=TUNE),
                     label(rf"from {r['track'].split('/')[0].replace('music', 'Part ')}, \ starting {r['offset_s']:.1f} s in \ (truly {d['offset_s']:.1f} s)", font_size=20, color=WHITE),
                     label(rf"{r['votes']} matching hashes, \ against {lib['clips']:,} clips of Parts 1 to 60", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.3).move_to(RIGHT * 2.2)
        with self.voiceover(
            "It can. <bookmark mark='a'/> Monochord's fingerprinter names the Variation, and the moment in it, out of every "
            f"sound in this series, {say(lib['clips'])} clips, in a fraction of a second."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ans))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"2002, \ London: \ dial 2580, \ hold your phone up to the music, \ and a text message names the song", WHITE),
            (r"Shazam: \ founded in 1999; \ its search described by Avery Wang in 2003; \ bought by Apple in 2018", WHITE),
            (r"ten bad seconds, \ millions of recordings, \ an answer in seconds: \ spectrogram peaks and a hash table", WHITE),
            (r"the same idea polices uploads: \ YouTube's Content ID matches every upload against rights holders' files \ (2007)", WHITE),
            (r"then the harder question: \ not which song is this, \ but which song should come next?", TUNE),
        ]
        rows_scene(self, r"finding music", items,
                   "The idea is old enough to have been a phone call. <bookmark mark='b'/> In 2002 in London you could dial "
                   "two-five-eight-oh, hold your phone up to the music, and get the song's name back in a text message. "
                   "<bookmark mark='c'/> The company, Shazam, was founded in 1999; Avery Wang described its search in 2003, and Apple "
                   "bought it in 2018. <bookmark mark='d'/> Ten bad seconds, millions of recordings, an answer in seconds: from "
                   "spectrogram peaks and a hash table. <bookmark mark='e'/> The same idea polices uploads: YouTube's Content ID has "
                   "matched every upload against rights holders' files since 2007. <bookmark mark='f'/> And then the harder "
                   "question: not which song is this, but which should come next?", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"fingerprints: \ peaks, \ hashes and votes",
            r"noise, \ codecs, \ chance; \ recordings, \ not songs",
            r"tags and embeddings; \ right for the wrong reasons",
            r"learning from listening: \ collaborative filtering",
            r"cold start, \ exploring, \ and popularity feeding on itself",
            r"playlists, \ fairness and metadata",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Fingerprints: peaks, hashes and votes. <bookmark mark='b'/> What noise, codecs and chance do to "
            "them, and why they find recordings, not songs. <bookmark mark='c'/> Tags and embeddings, and a classifier right for "
            "the wrong reasons. <bookmark mark='d'/> Learning from what people play. <bookmark mark='e'/> New songs nobody has "
            "played, exploring, and popularity feeding on itself. <bookmark mark='f'/> And playlists, fairness and metadata."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
