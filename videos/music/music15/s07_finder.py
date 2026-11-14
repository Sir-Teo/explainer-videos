from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Finder(SoundScene):
    def construct(self):
        chapter(self, 6, r"How well, \ and how fast", r"How good is a key finder?")
        self.scores()
        self.mistakes()
        self.speed()

    # ------------------------------------------------------------------
    def scores(self):
        d = load("finder")
        f = d["full"]
        vals = [100 * f[k]["accuracy"] for k in ("first", "ratings", "last", "bayes", "counts")]
        names = [r"the first note", r"listeners' ratings", r"the last note", r"probabilities", r"corpus counts"]
        ch = columns(vals, names, width=11.0, height=2.6, color=WEAK, hot=(1, 4), hot_color=TUNE, fmt="{:.0f}", font_size=22, top=100).move_to(DOWN * 1.0)
        yl = label(rf"keys found, \ in a hundred: \ {len(names)} methods on 54 tunes in each of 12 keys", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(rf"{d['cases']} tests", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How good is it? Give it each of our fifty-four tunes in each of the twelve keys: "
            f"{say(d['cases'])} tests. <bookmark mark='a'/> With Krumhansl's profile, the listeners' "
            f"ratings, it finds the key {say(100 * f['ratings']['accuracy'])} times in a hundred. Most of "
            "its mistakes are one mistake: it names the key a fifth above, because the ratings give the "
            "fifth degree too much weight. <bookmark mark='b'/> Replace the ratings with profiles "
            "counted from music, as David Temperley did in 2007 from a harmony textbook's examples, and "
            f"it is right {say(100 * f['counts']['accuracy'])} times in a hundred. Counting beats asking."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.bars[1], ch.labels[1], ch.values[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(ch.bars[4], ch.labels[4], ch.values[4])), FadeIn(VGroup(ch.bars[3], ch.labels[3], ch.values[3])))
        with self.voiceover(
            "Now two methods that need no profile at all. <bookmark mark='a'/> Guess that the key is the "
            f"tune's first note: right {say(100 * f['first']['accuracy'])} times in a hundred; more of "
            "these tunes begin on the fifth degree than on the tonic. <bookmark mark='b'/> Guess that "
            f"it is the last note: {say(100 * f['last']['accuracy'])}. One note, and it beats the "
            "listeners' ratings. That is Part 14's finding, turned into a key finder: tunes go home to "
            "end. The catch is that you have to wait for the end."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.bars[0], ch.labels[0], ch.values[0])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(ch.bars[2], ch.labels[2], ch.values[2])))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speed(self):
        d = load("finder")
        ns = d["ns"]
        g = axes([0, 21], [0, 100], x_length=8.5, y_length=3.6, xlabel=r"notes heard", ylabel=r"keys found, \ in a hundred", xticks=[2, 5, 10, 15, 20], yticks=[25, 50, 75, 100], font_size=22).move_to(LEFT * 1.4 + DOWN * 0.4)
        cb = curve_from(g, ns, [100 * v for v in d["curve"]["bayes"]], TUNE, stroke_width=4)
        ck = curve_from(g, ns, [100 * v for v in d["curve"]["ratings"]], WEAK, stroke_width=3)
        lb = label(r"probabilities", font_size=24, color=TUNE).next_to(g.ax.c2p(20, 100 * d["curve"]["bayes"][-1]), RIGHT, buff=0.2)
        lk = label(r"ratings", font_size=24, color=WEAK).next_to(g.ax.c2p(20, 100 * d["curve"]["ratings"][-1]), RIGHT, buff=0.2)
        five = Dot(g.ax.c2p(5, 100 * d["five"]), radius=0.09, color=WHITE)
        fl = label(rf"5 notes: \ {100 * d['five']:.0f}", font_size=26, color=WHITE).next_to(five, UL, buff=0.15)
        head = label(r"how many notes does it take?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So how soon can the key be known? Give the key finder only the first few notes of each "
            "tune. <bookmark mark='a'/> With two notes it is guessing. With four it is right three "
            f"times in four. <bookmark mark='b'/> With five notes, {say(100 * d['five'])} times in a "
            "hundred. After that it improves slowly: a tune tells you its key in its first breath and "
            "then spends the rest of its time confirming it. Human listeners are at least as quick. In "
            "experiments, a few notes or a single chord are enough for most people to hear which note "
            "would be home."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cb), Create(ck), FadeIn(lb), FadeIn(lk), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(five), FadeIn(fl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mistakes(self):
        d = load("more")["mistakes"]
        clock = fifths_clock(radius=1.8, font_size=28, signatures=False, minors=True).move_to(LEFT * 3.6 + DOWN * 0.3)
        rows = VGroup(label(rf"{d['total']} mistakes with the listeners' ratings", font_size=28, color=WHITE),
                      label(rf"{d['dominant']}: \ the key a fifth above", font_size=28, color=EAR),
                      label(rf"{d['mediant']}: \ the minor key on the third degree", font_size=28, color=EAR),
                      label(r"never a key from the far side of the circle", font_size=28, color=TUNE),
                      label(rf"profiles counted from the other 53 tunes: \ right {100 * d['own']:.0f} in a hundred", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 0.2)
        with self.voiceover(
            "Look at how it goes wrong, because the mistakes are informative. <bookmark mark='a'/> Of "
            f"{say(d['total'])} wrong answers, {say(d['dominant'])} name the key a fifth above the true "
            f"one, and {say(d['mediant'])} name the minor key on its third degree. <bookmark mark='b'/> "
            "Those are the next-door neighbours: keys that share six of the seven notes. The key finder "
            "is never wrong by half the circle. Its confusions are a map of which keys are alike, and "
            "chapter eight will draw that map. <bookmark mark='c'/> One more check: throw away the "
            "published profiles, and count new ones from fifty-three of our tunes to test on the "
            f"fifty-fourth. Right {say(100 * d['own'])} times in a hundred. A few dozen nursery tunes "
            "hold enough of the statistics of a key to find it."
        ) as vo:
            self.play(FadeIn(clock), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), Indicate(clock.cell[7], color=EAR, scale_factor=1.5))
            self.play(FadeIn(rows[2]), Indicate(clock.minor[7], color=EAR, scale_factor=1.5))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), Indicate(clock.cell[6], color=GREY_B))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
