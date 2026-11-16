from __future__ import annotations

import numpy as np

from videos.music.music60.common import *  # noqa: F403


class Superstars(SoundScene):
    def construct(self):
        chapter(self, 6, r"Superstars and cumulative advantage", r"Are hits better songs, \ or luckier ones?")
        self.rosen()
        self.experiment()
        self.shares()
        self.heard()
        self.lessons()

    # ------------------------------------------------------------------
    def rosen(self):
        items = [
            (r"Rosen \ (1981): \ when one performance can reach everyone, \ a little more talent earns far more money", WHITE),
            (r"recording, \ radio and streaming let the best-liked singer be heard in every home at once", WHITE),
            (r"Krueger \ (2005): \ the top 1\% of acts took about a quarter of US concert revenue in 1982, \ more than half by 2003", WHITE),
            (r"on the services, \ most tracks are played rarely, \ and a small share of artists collects most of the money", WHITE),
            (r"but is the top of the market there because it is better?", TUNE),
        ]
        rows_scene(self, r"the economics of superstars", items,
                   "Music's markets are famously unequal. <bookmark mark='b'/> The economist Sherwin Rosen explained why in 1981: "
                   "when one performance can reach everyone, a little more talent earns far more money. <bookmark mark='c'/> "
                   "Recording, radio and streaming let the best-liked singer be heard in every home at once. "
                   "<bookmark mark='d'/> Alan Krueger found that the top one percent of acts took about a quarter of American "
                   "concert revenue in 1982, and more than half by 2003. <bookmark mark='e'/> On the services, most tracks are "
                   "played rarely, and a small share of artists collects most of the money. <bookmark mark='f'/> But is the top of "
                   "the market there because it is better?", marks="bcdef")

    # ------------------------------------------------------------------
    def experiment(self):
        items = [
            (r"Salganik, \ Dodds and Watts \ (Science, \ 2006): \ 14,341 people, \ 48 songs by unknown bands", WHITE),
            (r"each person listened, \ rated, \ and could download; \ one group saw nothing of what others did", WHITE),
            (r"eight other groups, \ eight separate `worlds', \ saw how often each song had been downloaded in their own world", WHITE),
            (r"same songs, \ same kinds of people: \ random assignment helps identify social-influence effects across comparable groups, alongside ordinary sampling variation", WHITE),
            (r"they found: \ influence made hits bigger, \ and which songs became hits less predictable", TUNE),
        ]
        rows_scene(self, r"MusicLab", items,
                   "A famous experiment asked. <bookmark mark='b'/> In 2006 Matthew Salganik, Peter Dodds and Duncan Watts put forty-eight songs by unknown bands online, and 14,341 people came. <bookmark mark='c'/> Each could listen, rate, and download. One group saw nothing of what anyone else did. <bookmark mark='d'/> Eight other groups, eight separate worlds, saw how often each song had been downloaded in their own world. <bookmark mark='e'/> Same songs, same kinds of people: random assignment helps identify social-influence effects across comparable groups, alongside ordinary sampling variation. <bookmark mark='f'/> They found that influence made the hits bigger, and which songs became hits less predictable.", marks="bcdef")

    # ------------------------------------------------------------------
    def shares(self):
        d = load("market")
        soc = [np.sort(s)[::-1] for s in d["social"][:4]]
        ind = np.sort(d["independent"][0])[::-1]
        W, H = 2.6, 2.2
        panels = VGroup()

        def panel(sh, title, col, x, y):
            ax = frame_axes(width=W, height=H, xlo=0, xhi=48, ylo=0, yhi=0.2, center=[x, y, 0])
            bars = VGroup(*[Rectangle(width=W / 48 * 0.8, height=max(0.001, H * min(v, 0.2) / 0.2), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to(ax.to(i + 0.5, 0), aligned_edge=DOWN) for i, v in enumerate(sh)])
            t = label(title, font_size=15, color=col).next_to(ax, UP, buff=0.1)
            return VGroup(ax, bars, t)
        panels.add(panel(ind, r"independent", TUNE, -4.6, 0.3))
        for k in range(4):
            panels.add(panel(soc[k], rf"social world {k + 1}", BLUE, 0.2 + 3.4 * (k % 2), 1.35 - 2.5 * (k // 2)))
        g1 = label(rf"Gini: \ independent {d['gini_independent']:.2f}, \ social {d['gini_social']:.2f}", font_size=17, color=WHITE).move_to([-4.6, -1.6, 0])
        g2 = label(rf"unpredictability: \ {d['U_independent']:.4f} \ against {d['U_social']:.4f}", font_size=17, color=WHITE).move_to([-4.6, -2.15, 0])
        g3 = label(rf"winners' quality ranks in the 8 worlds: \ {', '.join(str(r) for r in d['winner_quality_rank'])}", font_size=17, color=EAR).to_edge(DOWN, buff=0.25)
        head = label(r"the experiment, \ simulated: \ market shares, \ largest first", font_size=24, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Monochord simulates the experiment. Forty-eight songs, each with a hidden quality, the chance that a listener "
            "downloads it; seven hundred listeners in each world. <bookmark mark='a'/> In the independent world, listeners choose "
            "by each song's appeal alone; the market shares fall off gently. <bookmark mark='b'/> In the social worlds, they "
            "choose partly by what others downloaded, and the leaders run away. The Gini coefficient, nought for equality and "
            f"one for a single winner, rises from {say(d['gini_independent'], 2)} to {say(d['gini_social'], 2)}. "
            "<bookmark mark='c'/> And the worlds disagree: a song's share differs between social worlds almost twice as much as "
            "between independent ones. <bookmark mark='d'/> Quality matters, but not alone: the eight worlds' winners were the "
            "first, second, fourth and even the eleventh best song."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in panels[1:]], lag_ratio=0.25), FadeIn(g1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(g2))
            vo.wait_until("d")
            self.play(FadeIn(g3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("market")
        c = clip("market.two")
        boxes = choice_boxes([r"world 1's hit", r"world 2's hit"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.5)
        note = label(rf"two of the same 48 melodies \ (by Part 14's model); \ quality ranks {d['pair_rank'][0]} and {d['pair_rank'][1]}", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"two worlds' hits", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here are two worlds' hits: the most downloaded song in world one, and in world two. Same forty-eight songs, two different winners."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two hits", kind="physical model", detail=r"Part 14's model, \ Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["one"], st["two"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["two"], c.duration, buff=0.08)
        with self.voiceover("Both are good songs in our model, among its best two; which of them won depended on who happened to arrive first."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lessons(self):
        items = [
            (r"cumulative advantage: \ success makes success, \ through charts, \ playlists, \ radio, \ and friends", WHITE),
            (r"the best songs rarely fail completely, \ the worst rarely succeed; \ in between, \ almost anything can happen", WHITE),
            (r"so a hit tells you less about a song than it seems to, \ and history is a sample of one world", WHITE),
            (r"recommendation systems are a social-influence world, \ built by engineers \ (Part 63)", TUNE),
        ]
        rows_scene(self, r"what it means", items,
                   "What does it mean? <bookmark mark='b'/> Cumulative advantage: success makes success, through charts, "
                   "playlists, radio and friends. <bookmark mark='c'/> In the experiment the best songs rarely failed completely, "
                   "and the worst rarely succeeded; in between, almost anything could happen. <bookmark mark='d'/> So a hit tells "
                   "you less about a song than it seems to, and the history we have is a sample of one world. "
                   "<bookmark mark='e'/> And a recommendation system is a social-influence world built by engineers, which Part 63 "
                   "takes apart.", marks="bcde")
