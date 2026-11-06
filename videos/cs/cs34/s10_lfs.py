from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (FILEC, HEAD, JRN, KERN, LAM, META, NO, PART, YES, blk, curve, load)


class Lfs(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.cost()
        self.bimodal()

    def card(self):
        card = chapter_card(9, r"The log-structured file system", r"What if the disk were only ever written in order?",
                            lit=(1992,), extra=((1992, r"Rosenblum and Ousterhout: \ Sprite LFS"),), part=PART)
        with self.voiceover("Chapter nine. The log-structured file system."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"Make every write sequential", font_size=36).to_edge(UP, buff=0.3)
        seq = [("D", FILEC), ("D", FILEC), ("I", META), ("D", FILEC), ("I", META), ("map", JRN), ("D", FILEC),
               ("D", FILEC), ("I", META), ("map", JRN)]
        log = VGroup(*[blk(t, c, w=0.75, h=0.75, font=17, fill=0.3) for t, c in seq]).arrange(RIGHT, buff=0.05)
        log.next_to(head, DOWN, buff=1.0)
        segs = VGroup(Brace(log[:6], UP, color=GREY_B), Brace(log[6:], UP, color=GREY_B))
        segl = VGroup(label(r"segment 1", font_size=17, color=GREY_B).next_to(segs[0], UP, buff=0.05),
                      label(r"segment 2", font_size=17, color=GREY_B).next_to(segs[1], UP, buff=0.05))
        cp = blk(r"checkpoint", KERN, w=1.8, h=0.6, font=16, fill=0.25).next_to(log, DOWN, buff=1.0).to_edge(LEFT,
                                                                                                         buff=1.0)
        cpa = CurvedArrow(cp.get_right(), log[9].get_bottom() + DOWN * 0.05, angle=0.5, color=KERN, stroke_width=2)
        dead = VGroup(*[Cross(log[i], stroke_color=NO, stroke_width=3, scale_factor=0.6) for i in (0, 2, 5)])
        lines = VGroup(
            label(r"memory is large, \ so most reads hit the cache: \ the disk's work is mostly \textbf{writes}",
                  font_size=20, color=WHITE),
            label(r"buffer every change, \ data \textbf{and} inodes, \ and write them out as one long segment",
                  font_size=20, color=YES),
            label(r"inodes now move: \ an \textbf{inode map} \ (itself in the log) \ says where each is; \ a "
                  r"checkpoint says where the map is", font_size=20, color=JRN),
            label(r"an overwritten block leaves a dead copy behind: \ something must reclaim the space", font_size=20,
                  color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1992 Rosenblum and Ousterhout asked a radical question. <bookmark mark='a'/> Memories had grown large "
            "enough that most reads were served from the cache, so what a disk mostly did was write. And small writes "
            "scattered over the disk are the slowest thing it can do. <bookmark mark='b'/> So buffer every change, "
            "file data and inodes alike, and write them all out together, in order, as one long segment, at the "
            "disk's full speed. Never write anything in place. <bookmark mark='c'/> But then an inode moves every "
            "time it changes. A map of where each inode now is is written into the log too, and a checkpoint region "
            "at a fixed place says where the newest map is. Crash recovery starts from the last checkpoint and reads "
            "forward. <bookmark mark='d'/> The catch: every overwrite leaves a dead copy behind, and the free space "
            "fills with holes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in log], lag_ratio=0.12), FadeIn(segs),
                      FadeIn(segl), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(cp), Create(cpa), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(Create(dead), FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        d = load("lfs")
        head = label(r"The cleaner, \ and its cost", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0.2, 0.9, 0.1], y_range=[1, 14, 2], x_length=6.6, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.0, -0.5, 0])
        xt = VGroup(*[label(rf"{x:.1f}", font_size=16, color=GREY_B).next_to(ax.c2p(x, 1), DOWN, buff=0.1)
                      for x in (0.3, 0.5, 0.7, 0.9)])
        yt = VGroup(*[label(str(y), font_size=16, color=GREY_B).next_to(ax.c2p(0.2, y), LEFT, buff=0.1)
                      for y in (1, 3, 5, 7, 9, 11, 13)])
        xl = label(r"disk utilization", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"write cost: \ disk traffic per byte of new data", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        us = d["u"]
        f = VMobject(color=GREY_B, stroke_width=2.5).set_points_smoothly(
            [ax.c2p(u, 2 / (1 - u)) for u in [0.2 + 0.01 * i for i in range(67)]])
        cols = {"greedy, uniform": HEAD, "greedy, hot and cold": NO, "cost-benefit, hot and cold": YES}
        cs = VGroup(*[curve(ax, us, d["curves"][k], c, width=2.5) for k, c in cols.items()])
        keys = VGroup(
            label(r"$2/(1-u)$: \ cleaning segments \\ as full as the disk", font_size=18, color=GREY_B),
            *[label(k, font_size=18, color=c) for k, c in cols.items()],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 1.0, 0])
        exp = VGroup(
            label(r"to free a segment at utilization $u$: \\ read it (1), \ write back its live $u$, \\ to gain "
                  r"$1 - u$ of space", font_size=18, color=WHITE),
        ).next_to(keys, DOWN, buff=0.5).align_to(keys, LEFT)
        foot = label(r"simulated: \ 200 segments of 64 blocks; \ one-block files overwritten 20 times over; \ "
                     r"hot and cold: \ 90\% of writes to 10\% of the files", font_size=16, color=GREY_B).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "The cleaner reclaims the holes. It reads some segments, writes their live blocks back out compactly, and "
            "the old segments are free again. <bookmark mark='a'/> To free a segment whose live fraction is u, it "
            "reads the whole segment and writes back u of it, to gain 1 minus u of space for new data. So each byte "
            "of new data costs two over one minus u bytes of disk traffic. If the cleaner had to clean segments as "
            "full as the disk is on average, the cost would explode as the disk fills. <bookmark mark='b'/> Our "
            "simulation, after Rosenblum's, does better than that line, because the cleaner picks the emptiest "
            "segments, which are emptier than average. <bookmark mark='c'/> With hot and cold data, ninety percent "
            "of the writes going to a tenth of the files, the greedy cleaner gains only a little. <bookmark "
            "mark='d'/> Rosenblum's cost-benefit policy does much better, as the next picture explains."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(f), FadeIn(keys[0]), FadeIn(exp))
            vo.wait_until("b")
            self.play(Create(cs[0]), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(Create(cs[1]), FadeIn(keys[2]))
            vo.wait_until("d")
            self.play(Create(cs[2]), FadeIn(keys[3]))
        self.wait(0.3)
        self.clear_scene()

    def bimodal(self):
        d = load("lfs")
        head = label(r"Which segments to clean", font_size=36).to_edge(UP, buff=0.3)
        W, H = 5.2, 2.2

        def hist(bins, color):
            mx = max(bins)
            g = VGroup()
            w = W / len(bins)
            for k, v in enumerate(bins):
                h = max(0.005, H * v / mx)
                g.add(Rectangle(width=w * 0.9, height=h, stroke_width=0, fill_color=color,
                                fill_opacity=0.85).move_to([k * w, h / 2, 0]))
            base = Line([-w / 2, 0, 0], [W - w / 2, 0, 0], color=GREY_D)
            ticks = VGroup(*[label(t, font_size=15, color=GREY_B).move_to([W * x - w / 2, -0.25, 0]) for x, t in
                             ((0, "0"), (0.5, "0.5"), (1, "1"))])
            return VGroup(g, base, ticks)
        hg = hist(d["hist"]["greedy"]["bins"], NO)
        hc = hist(d["hist"]["cost-benefit"]["bins"], YES)
        tg = label(rf"greedy: \ the emptiest; \ mean {d['hist']['greedy']['mean']:.2f}", font_size=19,
                   color=NO).next_to(hg, UP, buff=0.15)
        tc = label(rf"cost-benefit; \ mean {d['hist']['cost-benefit']['mean']:.2f}", font_size=19,
                   color=YES).next_to(hc, UP, buff=0.15)
        VGroup(VGroup(hg, tg), VGroup(hc, tc)).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.6)
        cap = label(r"utilization of each segment when it was cleaned \ (disk 75\% full, \ hot and cold)",
                    font_size=17, color=GREY_B).next_to(VGroup(hg, hc), DOWN, buff=0.2)
        lines = VGroup(
            label(r"greedy waits for cold segments to become the emptiest, \ which takes a long time: \ cold "
                  r"data hoards free space", font_size=20, color=NO),
            label(r"cost-benefit: \ clean when $\dfrac{(1 - u) \times \text{age}}{1 + u}$ is largest: \ old, \ "
                  r"stable free space is worth more", font_size=20, color=YES),
            label(r"so cold segments are cleaned while still quite full, \ hot ones once nearly empty: \ "
                  r"\textbf{two peaks}, \ as the paper found", font_size=20, color=HEAD),
            label(r"the same cleaner lives on: \ in every flash drive \ (chapter 3), \ in F2FS, \ and in LSM trees "
                  r"\ (chapter 14)", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is when each segment was cleaned, and how full it was. <bookmark mark='a'/> The greedy cleaner "
            "always takes the emptiest segment. Hot segments empty quickly and are cleaned again and again. Cold "
            "segments, full of data that rarely changes, empty only slowly, are seldom the emptiest, and hold on to "
            "their scraps of free space for a long time. <bookmark mark='b'/> Rosenblum's cost-benefit rule weighs the free space "
            "gained by how long it is likely to stay free: one minus u, times the age of the data, over the cost, one "
            "plus u. <bookmark mark='c'/> Now cold segments are worth cleaning while still quite full, because once "
            "compacted they stay compact, and hot segments are left alone until they are nearly empty. Two peaks, "
            "exactly the shape the paper reported. <bookmark mark='d'/> The idea outlived its file system: every flash "
            "drive runs a cleaner like this one, and so does every LSM tree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(hg), FadeIn(tg), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(hc), FadeIn(tc), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
