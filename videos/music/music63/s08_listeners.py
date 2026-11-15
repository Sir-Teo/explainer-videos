from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Listeners(SoundScene):
    def construct(self):
        chapter(self, 7, r"Learning from listening", r"Can what other people play tell you what you will like?")
        self.idea()
        self.als()
        self.compare()
        self.heard()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"collaborative filtering: \ people who played what you played also played this", WHITE),
            (r"no audio at all: \ only who played what, \ and how often", WHITE),
            (r"2006 to 2009: \ the Netflix Prize, \ a million dollars for 10\% better predictions of film ratings", WHITE),
            (r"music services have plays, \ not ratings: \ implicit feedback, \ where silence is not dislike", WHITE),
            (r"2015: \ Spotify's Discover Weekly, \ thirty songs a week for every listener, \ largely from these methods", TUNE),
        ]
        rows_scene(self, r"collaborative filtering", items,
                   "The other way to find music ignores the sound altogether. <bookmark mark='b'/> Collaborative filtering: people "
                   "who played what you played also played this. <bookmark mark='c'/> It uses no audio, only who played what, and how "
                   "often. <bookmark mark='d'/> From 2006 to 2009 the Netflix Prize offered a million dollars for ten percent better "
                   "predictions of film ratings, and made these methods famous. <bookmark mark='e'/> Music services have plays, not "
                   "ratings: implicit feedback, in which not playing a song is not the same as disliking it. "
                   "<bookmark mark='f'/> In 2015 Spotify's Discover Weekly began giving every listener thirty songs a week, largely "
                   "from these methods.", marks="bcdef")

    # ------------------------------------------------------------------
    def als(self):
        lines = VGroup(
            MathTex(r"p_{ui} = [r_{ui} > 0], \qquad c_{ui} = 1 + \alpha\, r_{ui}", font_size=34, color=WHITE),
            MathTex(r"\min_{x, y}\ \sum_{u,i} c_{ui}\,\big(p_{ui} - x_u^\top y_i\big)^2 + \lambda\Big(\sum_u \|x_u\|^2 + \sum_i \|y_i\|^2\Big)", font_size=32, color=TUNE),
            label(r"$x_u$: \ a listener's taste; \ $y_i$: \ a song's profile; \ both learnt, \ 8 numbers each", font_size=19, color=WHITE),
            label(r"alternating least squares: \ fix the songs, \ solve for every listener; \ fix the listeners, \ solve for every song", font_size=19, color=WHITE),
            label(r"Hu, \ Koren and Volinsky \ (2008)", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"implicit matrix factorization", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The standard method for plays is from Yifan Hu, Yehuda Koren and Chris Volinsky, in 2008. <bookmark mark='a'/> "
            "Whether a listener played a song is the preference; how often sets the confidence in it. <bookmark mark='b'/> Find "
            "a short vector for every listener and every song so that their dot product predicts the preference, weighted by "
            "the confidence. <bookmark mark='c'/> The listener's vector is their taste, the song's its profile, both learnt from "
            "the plays alone. <bookmark mark='d'/> Solve by alternating least squares: fix the songs and solve for every "
            "listener, then fix the listeners and solve for every song."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[4]))
            for mark, ln in zip("abcd", lines[:4]):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("recs")
        r = d["recall"]
        rows_ = VGroup()
        top = max(r.values())
        for k, name, col in (("random", r"random songs", GREY_B), ("popular", r"the most played songs", BLUE), ("als", r"implicit ALS", TUNE)):
            rows_.add(VGroup(label(name, font_size=19, color=col), Rectangle(width=6.0 * r[k] / top, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.8),
                             label(f"{100 * r[k]:.0f}\\%", font_size=18, color=WHITE)))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.2 + LEFT * 2.5)
        for row in rows_:
            row[1].next_to(row[0], RIGHT, buff=0.3).align_to(rows_, LEFT).shift(RIGHT * 3.6)
            row[2].next_to(row[1], RIGHT, buff=0.2)
        setup = label(rf"{d['users']} simulated listeners with known tastes, \ {d['items']} songs from the series' library, \ {d['plays']:,} plays; \ a fifth of each listener's songs hidden",
                      font_size=16, color=GREY_A).to_edge(UP, buff=1.0)
        note = label(r"recall at 10: \ the share of each listener's hidden songs in their top ten", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"does it work?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Monochord simulates {say(d['users'])} listeners whose tastes it knows, {say(d['items'])} songs from the series' "
            "library, and their plays; a fifth of each listener's songs are hidden, and each method must find them. "
            f"<bookmark mark='a'/> Random songs find {say(100 * r['random'])} percent in the top ten. <bookmark mark='b'/> "
            f"Recommending the most played songs to everyone finds {say(100 * r['popular'])} percent: popularity is a strong "
            f"baseline. <bookmark mark='c'/> The factorization finds {say(100 * r['als'])} percent, by learning each listener's "
            "taste."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup), FadeIn(note))
            for mark, row in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(row))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("recs")
        c = clip("recs.three")
        names = [n.split("/")[1] for n in d["top3"]]
        boxes = choice_boxes(names, width=3.4, height=0.9, buff=0.4, size=16).move_to(UP * 0.5)
        note = label(r"the three songs the factorization suggests to its most active listener, \ none of which they had played", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"three suggestions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here are the three songs it suggests to its most active listener, none of which that listener had played."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three suggestions", kind="physical model", detail=r"clips from the series' library", corner=DL, tag_corner=DR)
            ks = ["one", "two", "three"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        self.wait(0.4)
        self.clear_scene()
