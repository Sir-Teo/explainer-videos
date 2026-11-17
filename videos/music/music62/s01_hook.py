from __future__ import annotations

from videos.music.music62.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.hearing()
        self.uses()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The session, \ twice, \ with a click track. \ In one the clicks are on the beat; \ in the other they are "
                           rf"{d['offset_ms']} ms late. \ Which is on the beat?", width=9.5)
        with self.voiceover(
            f"A child can clap along to a song; for decades a program could not. First, your own sense of the beat. The session, twice, with a click track. In one the clicks are on the beat; in the other "
            f"they are {say(d['offset_ms'])} milliseconds late, less than a tenth of a second. Which is on the beat?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"on the beat?", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(rf"the second: \ the first's clicks trail the drums by {d['offset_ms']} ms, \ and most listeners hear it at once", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The second. In the first the clicks trail the drums by eighty milliseconds, and most listeners hear it at once: we are precise judges of the beat."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"a child can clap along to a song; \ for decades a program could not", WHITE),
            (r"and today's still taps at half or double speed, \ and loses its place in a rubato", WHITE),
            (r"the listeners of this part run DJ software, \ practice apps, \ playlists and accompaniment systems", WHITE),
            (r"they all ask three questions: \ where is the beat, \ what is the chord, \ where does the section change?", TUNE),
        ]
        rows_scene(self, r"clapping along", items,
                   "That precision is easy for people. <bookmark mark='b'/> A child can clap along to a song; for decades a "
                   "program could not. <bookmark mark='c'/> And today's programs still tap at half or double speed, and lose "
                   "their place in a rubato. <bookmark mark='d'/> These listeners run DJ software, practice apps, playlists and "
                   "accompaniment systems. <bookmark mark='e'/> They all ask three questions: where is the beat, what is the "
                   "chord, and where does the section change?", marks="bcde")

    # ------------------------------------------------------------------
    def hearing(self):
        items = [
            (r"we do not wait for each beat: \\ attention is entrained, \\ an oscillator locked to the pulse \\ (Large and Jones, \\ 1999)", WHITE),
            (r"tapping along, \\ people tap a few tens of milliseconds early: \\ they predict \\ (Repp's reviews of synchronization)", WHITE),
            (r"left to themselves, \\ people walk and tap near 120 a minute \\ (Moelants, \\ 2002, \\ for preferred tempo)", WHITE),
            (r"an 80 ms slip is obvious; \\ a 20 ms one is not: \\ the scale on which machines are judged", TUNE),
        ]
        rows_scene(self, r"how people hear the beat", items,
                   "How do people do it? <bookmark mark='b'/> We do not wait for each beat: attention is entrained, like an oscillator "
                   "locked to the pulse, as Edward Large and Mari Riess Jones described in 1999. <bookmark mark='c'/> Tapping along, "
                   "people tap a few tens of milliseconds early: they predict the beat rather than react to it. "
                   "<bookmark mark='d'/> Some studies report preferred tapping or movement rates near a hundred and twenty a minute, with substantial individual and contextual variation, Dirk Moelants "
                   "found in 2002. <bookmark mark='e'/> Timing sensitivity depends on tempo, timbre, task and listener; eighty milliseconds is conspicuous in this example, while twenty can also be detectable. That "
                   "is the scale on which the machines of this part are judged.", marks="bcde")

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"DJ software: \ match two songs' tempos and line up their beats and bars, \ automatically", WHITE),
            (r"practice apps: \ slow a song down without changing its pitch, \ loop four bars, \ show the chords as they pass", WHITE),
            (r"playlists by tempo: \ running, \ dancing, \ sleeping", WHITE),
            (r"musicology at scale: \ tempos, \ harmonies and forms of thousands of recordings, \ measured", WHITE),
            (r"each depends on the three answers being right, \ or right enough", TUNE),
        ]
        rows_scene(self, r"what these listeners run", items,
                   "These listeners run things you may use. <bookmark mark='b'/> DJ software matches two songs' tempos and lines up "
                   "their beats and bars automatically. <bookmark mark='c'/> Practice apps slow a song without changing its pitch, "
                   "loop four bars and show the chords as they pass. <bookmark mark='d'/> Playlists are built by tempo, for running, "
                   "dancing or sleep. <bookmark mark='e'/> And musicology measures the tempos, harmonies and forms of thousands of "
                   "recordings at once. <bookmark mark='f'/> Each depends on the three answers being right, or right enough.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"novelty and tempo, \ and the tempo's octave",
            r"tracking beats by dynamic programming; \ downbeats",
            r"chroma, \ and chords in context",
            r"time warping, \ and an accompanist that follows",
            r"structure from self-similarity and repetition",
            r"covers, \ and how far people agree",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Where the beats might be, and how fast they come. <bookmark mark='b'/> Tracking them, and finding "
            "the bar. <bookmark mark='c'/> Chroma, and chords in context. <bookmark mark='d'/> Time warping, and an accompanist "
            "that follows a singer. <bookmark mark='e'/> The form of a song, from its repetitions. <bookmark mark='f'/> And covers, "
            "and how far people agree."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
