from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Cold(SoundScene):
    def construct(self):
        chapter(self, 8, r"Cold start and exploring", r"How does a song nobody has played ever get recommended?")
        self.problem()
        self.content()
        self.heard()
        self.explore()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"tens of thousands of new tracks are uploaded to the services every day", WHITE),
            (r"collaborative filtering knows nothing about a song until people play it", WHITE),
            (r"and people play what is recommended: \ a new song can wait for ever", WHITE),
            (r"the same for a new listener: \ no plays, \ no taste", WHITE),
            (r"the fixes: \ use the sound, \ and spend some recommendations on finding out", TUNE),
        ]
        rows_scene(self, r"the cold start", items,
                   "Plays have a weakness. <bookmark mark='b'/> Tens of thousands of new tracks reach the services every day. "
                   "<bookmark mark='c'/> Collaborative filtering knows nothing about a song until people play it, "
                   "<bookmark mark='d'/> and people mostly play what is recommended, so a new song can wait for ever. "
                   "<bookmark mark='e'/> A new listener has the same problem: no plays, no taste. <bookmark mark='f'/> Two fixes: "
                   "use the sound, and spend some recommendations on finding out.", marks="bcdef")

    # ------------------------------------------------------------------
    def content(self):
        d = load("recs")["cold"]
        lines = VGroup(
            label(rf"hide every play of {d['n']} songs: \ to the factorization they are new", font_size=20, color=WHITE),
            label(r"learn, \ on the songs people did play, \ a map from the sound's embedding to the song's learnt profile", font_size=20, color=WHITE),
            label(r"apply it to the new songs, \ and recommend them by their sound alone", font_size=20, color=WHITE),
            label(rf"recall at 5 among the new songs: \ from their sound {100 * d['content']:.0f}\%, \ at random {100 * d['random']:.0f}\%", font_size=22, color=TUNE),
        ).arrange(DOWN, buff=0.45)
        head = label(r"recommending from the sound", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Monochord tries the first fix. <bookmark mark='a'/> It hides every play of {say(d['n'])} songs, so that to the "
            "factorization they are new. <bookmark mark='b'/> On the songs people did play, it learns a map from the sound's "
            "embedding to the profile the factorization found. <bookmark mark='c'/> Then it applies the map to the new songs and "
            f"recommends them by their sound alone. <bookmark mark='d'/> It finds {say(100 * d['content'])} percent of listeners' "
            f"new songs in their top five, against {say(100 * d['random'])} at random: in our simulation, taste follows the sound "
            "partly, and the map recovers that part."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("recs")
        c = clip("cold.two")
        names = [n.split("/")[1] for n in d["cold_pair"]]
        boxes = choice_boxes([rf"new: \ {names[0]}", rf"nearest played: \ {names[1]}"], width=4.4, height=0.9, buff=0.8, size=17).move_to(UP * 0.5)
        head = label(r"a new song, \ and its nearest neighbour", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear one of the new songs, and the played song whose sound is nearest to it in the embedding: the song it will be recommended alongside."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["cold_starts"]
        with self.listen(c) as snd:
            window(snd, r"new, \ then nearest", kind="physical model", detail=r"clips from the series' library", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["cold"], st["near"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["near"], c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def explore(self):
        items = [
            (r"the second fix: \ explore: \ show some listeners a song the system is unsure of, \ and learn from what they do", WHITE),
            (r"a bandit problem, \ as in clinical trials and advertising: \ exploit what works, \ or explore what might", WHITE),
            (r"Thompson sampling: \ recommend with probability that it is best, \ given everything seen so far", WHITE),
            (r"the cost is real: \ an exploration is a recommendation that may be worse", WHITE),
            (r"without it, \ the system never learns about what it never shows: \ the next chapter", TUNE),
        ]
        rows_scene(self, r"exploring", items,
                   "The second fix is to explore. <bookmark mark='b'/> Show some listeners a song the system is unsure about, and "
                   "learn from what they do. <bookmark mark='c'/> This is a bandit problem: trade off exploiting what works against "
                   "exploring what might. <bookmark mark='d'/> Thompson sampling recommends each song with the probability that it "
                   "is the best, given everything seen so far. <bookmark mark='e'/> The cost is real: an exploration is a "
                   "recommendation that may be worse. <bookmark mark='f'/> But without it, the system never learns about what it "
                   "never shows, which the next chapter measures.", marks="bcdef")
