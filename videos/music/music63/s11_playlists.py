from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Playlists(SoundScene):
    def construct(self):
        chapter(self, 10, r"Playlists, \ fairness and metadata", r"What makes a good sequence, \ and who gets heard?")
        self.quiz()
        self.order()
        self.path()
        self.fair()
        self.metadata()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("playlist")
        c = clip("playlist.two")
        card = listen_card(r"Six Variations, \ a few seconds each, \ twice. \ Once in a random order; \ once ordered so that each sounds like "
                           r"the one before. \ Which was ordered?", width=10.0)
        with self.voiceover("Your turn. Six Variations, a few seconds each, twice: once in a random order, once ordered so that each sounds like the one before. Which was ordered?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"random or ordered?", kind="physical model", detail=r"six Variations", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(r"the second: \ neighbours share instruments and textures; \ the first jumps", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The second: neighbouring snippets share instruments and textures, while the first jumps about. Smoothness is one thing a playlist can be asked for."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        d = load("playlist")
        lines = VGroup(
            label(r"a smooth playlist is a short path through the songs, \ step by step in the embedding", font_size=20, color=WHITE),
            label(r"the travelling salesman's problem: \ nearest neighbour first, \ then 2-opt swaps that shorten the path", font_size=20, color=WHITE),
            label(rf"every Variation in one sequence: \ path {d['length_smooth']:.0f}, \ against {d['length_random']:.0f} in a random order", font_size=20, color=TUNE),
            label(r"but listeners also want variety, \ a shape, \ a start and an end: \ smoothness is not the only virtue", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.45)
        head = label(r"ordering a playlist", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How was it ordered? <bookmark mark='a'/> A smooth playlist is a short path through the songs, step by step in the "
            "embedding. <bookmark mark='b'/> That is the travelling salesman's problem: start with the nearest neighbour each "
            "time, then swap pairs of steps while the path gets shorter. <bookmark mark='c'/> Ordering every Variation this way "
            "makes a path about half as long as a random order. <bookmark mark='d'/> But listeners also want variety, a shape, a "
            "beginning and an end: smoothness is not the only virtue of a playlist."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fair(self):
        items = [
            (r"fairness to listeners: \ do recommendations serve niche tastes as well as mainstream ones?", WHITE),
            (r"fairness to artists: \ exposure follows popularity, \ and popularity follows exposure \ (Chapter 9)", WHITE),
            (r"studies have found recommenders amplify imbalances already in the plays, \ for example by artists' gender", WHITE),
            (r"remedies: \ constraints on exposure, \ re-ranking, \ and measuring who is shown, \ not only who is played", TUNE),
        ]
        rows_scene(self, r"fairness", items,
                   "Who gets heard is a question of fairness. <bookmark mark='b'/> To listeners: do recommendations serve niche "
                   "tastes as well as mainstream ones? <bookmark mark='c'/> To artists: exposure follows popularity, and popularity "
                   "follows exposure, as Chapter 9 showed. <bookmark mark='d'/> Studies have found recommenders amplifying "
                   "imbalances already present in the plays, for instance by artists' gender. <bookmark mark='e'/> The remedies: "
                   "constraints on exposure, re-ranking, and measuring who is shown, not only who is played.", marks="bcde")

    # ------------------------------------------------------------------
    def metadata(self):
        items = [
            (r"every finder needs to know what it has found: \ titles, \ artists, \ writers, \ dates", WHITE),
            (r"recordings carry ISRCs; \ compositions carry ISWCs; \ linking the two is still often done by hand", WHITE),
            (r"MusicBrainz \ (2000): \ an open, \ crowd-edited encyclopedia of recordings and works", WHITE),
            (r"and Part 60's unmatched royalties are a metadata problem: \ a fingerprint without a name pays nobody", TUNE),
        ]
        rows_scene(self, r"metadata", items,
                   "And finding depends on naming. <bookmark mark='b'/> Every finder needs to know what it has found: titles, "
                   "artists, writers, dates. <bookmark mark='c'/> Recordings carry ISRC codes and compositions ISWC codes, and "
                   "linking the two is still often done by hand. <bookmark mark='d'/> MusicBrainz, begun in 2000, is an open, "
                   "crowd-edited encyclopedia of both. <bookmark mark='e'/> And Part 60's unmatched royalties are a metadata "
                   "problem: a fingerprint without a name pays nobody.", marks="bcde")

    # ------------------------------------------------------------------
    def path(self):
        d = load("map")
        p = load("playlist")
        V = np.array(d["var_xy"])
        cx, cy, sx, sy = 0.0, -0.4, 4.6, 2.7
        pts = [np.array([cx + sx * v[0], cy + sy * v[1], 0]) for v in V]
        dots = VGroup(*[Dot(q, radius=0.06, color=TUNE) for q in pts])
        order = d["order"]
        rng = np.random.default_rng(3)
        rand = [0] + list(rng.permutation(np.arange(1, len(V))))
        def path(seq, col, w):
            return VMobject(stroke_color=col, stroke_width=w, stroke_opacity=0.8).set_points_as_corners([pts[i] for i in seq])
        pr, ps = path(rand, EAR, 1.5), path(order, TUNE, 2.5)
        lab = VGroup(label(rf"random order: \ length {p['length_random']:.0f}", font_size=17, color=EAR), label(rf"the builder's order: \ {p['length_smooth']:.0f}", font_size=17, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_corner(UR, buff=0.4)
        note = label(r"the Variations on the map of the last chapter \ (lengths measured in the full embedding)", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"a playlist is a path", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is what the builder did, on the map of sounds from Chapter 5. Each dot is a Variation. "
            "<bookmark mark='a'/> A random order zig-zags across the map: every step a jump in sound. "
            "<bookmark mark='b'/> The builder's order walks: from each Variation to its nearest unvisited neighbour, then "
            f"untangled where two steps cross. Its path is {say(p['length_smooth'], 0)} long against {say(p['length_random'], 0)}, "
            "which is what you heard as smoothness. A smooth path is not the only good playlist: contrast, surprise and a "
            "shape over the hour matter too, and nearest neighbours know nothing of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(note))
            vo.wait_until("a")
            self.play(Create(pr), FadeIn(lab[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(pr.animate.set_stroke(opacity=0.25), Create(ps), FadeIn(lab[1]), run_time=1.8)
        self.wait(0.6)
        self.clear_scene()
