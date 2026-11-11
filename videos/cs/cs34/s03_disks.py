from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (HEAD, LAM, NO, PART, YES, grid_table, load, platter)


class Disks(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanics()
        self.sequential()
        self.schedule()
        self.load_()

    def card(self):
        card = chapter_card(2, r"Disks", r"Why is reading in order hundreds of times faster?", lit=(1956, 1973),
                            extra=((1956, r"IBM 350"), (1973, r"IBM 3340, \ ``Winchester''")), part=PART)
        with self.voiceover("Chapter two. Disks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def mechanics(self):
        d = load("disk")
        head = label(r"Seek, \ rotate, \ transfer", font_size=36).to_edge(UP, buff=0.3)
        pl = platter(r=2.1, tracks=7).move_to([-3.6, -0.4, 0])
        sector = AnnularSector(inner_radius=1.45, outer_radius=1.72, angle=0.35, start_angle=2.6, color=NO,
                               fill_opacity=0.8).shift(pl.get_center())
        spin = VGroup(pl, sector)
        pivot = pl.get_center() + RIGHT * 2.9 + DOWN * 1.6
        arm_tip = pl.get_center() + RIGHT * 0.7 + DOWN * 1.9
        arm = VGroup(Line(pivot, arm_tip, color=GREY_A, stroke_width=6), Dot(pivot, radius=0.12, color=GREY_B),
                     Dot(arm_tip, radius=0.07, color=HEAD))
        parts = VGroup(
            VGroup(label(r"\textbf{seek}: \ move the arm to the track", font_size=22, color=HEAD),
                   label(rf"0.5 ms to the next track, \ {d['t_max']:.0f} ms across the disk; \ "
                         rf"{d['avg_seek']:.1f} ms on average", font_size=19, color=GREY_A)),
            VGroup(label(r"\textbf{rotation}: \ wait for the sector to come round", font_size=22, color=NO),
                   label(rf"7200 rpm: \ a turn in {d['rev']:.2f} ms, \ half a turn, \ {d['half_turn']:.2f} ms, \ on "
                         rf"average", font_size=19, color=GREY_A)),
            VGroup(label(r"\textbf{transfer}: \ read it as it passes under the head", font_size=22, color=YES),
                   label(rf"{d['mb_s']:.0f} MB/s: \ 4 KiB in {d['transfer_4k_ms'] * 1000:.0f} $\mu$s", font_size=19,
                         color=GREY_A)),
        )
        for p in parts:
            p.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.9, 0.4, 0])
        tot = label(rf"a random 4 KiB read: \ {d['random_4k_ms']:.1f} ms, \ almost all of it waiting", font_size=23,
                    color=WHITE).to_edge(DOWN, buff=0.45)
        xs = [c["d"] / 1000 for c in d["curve"]]
        ys = [c["ms"] for c in d["curve"]]
        ax = Axes(x_range=[0, 100, 25], y_range=[0, 16, 4], x_length=3.0, y_length=1.4,
                  axis_config={"color": GREY_D, "include_numbers": False})
        sc = VGroup(ax, VMobject(color=HEAD, stroke_width=2.5).set_points_smoothly([ax.c2p(x, y) for x, y in
                                                                                     zip(xs, ys)]),
                    label(r"seek time against distance: \ $\sqrt{d}$", font_size=15, color=GREY_B).next_to(ax, DOWN,
                                                                                                         buff=0.08))
        sc.next_to(parts, DOWN, buff=0.3).align_to(parts, LEFT)
        with self.voiceover(
            "A hard disk is a stack of platters spinning on one spindle, with an arm that carries a head over each "
            "surface. Reading a block takes three steps. <bookmark mark='a'/> First the seek: the arm swings to the "
            "right track. It accelerates and then brakes, so the time grows like the square root of the distance: "
            "half a millisecond to the next track, sixteen across the whole disk, almost nine on average. "
            "<bookmark mark='b'/> Then the rotation: the head waits for the sector to come round. At 7200 turns a "
            "minute, a turn is 8.3 milliseconds, so the average wait is half that. <bookmark mark='c'/> Then the "
            "transfer, as the sector passes under the head: 150 megabytes a second, so four kilobytes take 27 "
            "microseconds. <bookmark mark='d'/> A random read: thirteen milliseconds, and nearly all of it is spent "
            "waiting for things to move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(spin), FadeIn(arm))
            vo.wait_until("a")
            self.play(FadeIn(parts[0]), FadeIn(sc))
            self.play(Rotate(arm, angle=-0.28, about_point=pivot), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(parts[1]))
            self.play(Rotate(spin, angle=-2.2, about_point=pl.get_center()), run_time=2.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(parts[2]))
            self.play(Rotate(spin, angle=-0.4, about_point=pl.get_center()), sector.animate.set_color(YES),
                      run_time=0.8, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

    def sequential(self):
        d = load("disk")
        head = label(r"Random against sequential", font_size=36).to_edge(UP, buff=0.3)
        W = 10.0
        bars = VGroup()
        for t, v, c in ((r"sequential: \ one seek, \ then every block as it passes", d["mb_s"], YES),
                        (r"random 4 KiB reads", d["random_mb_s"], NO)):
            w = max(0.04, W * v / d["mb_s"])
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.85)
            bars.add(VGroup(label(t, font_size=21, color=c), r, label(rf"{v:.2f} MB/s" if v < 10 else
                                                                    rf"{v:.0f} MB/s", font_size=22, color=WHITE)))
        for k, b in enumerate(bars):
            b[1].move_to([-5.0, 1.0 - 1.5 * k, 0], aligned_edge=LEFT)
            b[0].next_to(b[1], UP, buff=0.1).align_to(b[1], LEFT)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        lines = VGroup(
            label(rf"${d['ratio']:.0f}\times$: \ {d['random_iops']:.0f} random reads a second, \ against a whole "
                  rf"track every turn", font_size=22, color=WHITE),
            label(r"the rule for the rest of the part: \ \textbf{put together what is read together}, \ and write "
                  r"in long runs", font_size=22, color=HEAD),
            label(r"(the model has no cache; \ a real drive also reads ahead and buffers whole tracks)", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That waiting is the whole story of disk performance. <bookmark mark='a'/> Read the disk in order, and "
            "after one seek every block arrives as it passes the head: 150 megabytes a second. <bookmark mark='b'/> "
            "Read four-kilobyte blocks at random places, and each one costs a seek and half a turn: 77 reads a "
            "second, a third of a megabyte a second. <bookmark mark='c'/> Nearly five hundred times slower, for the "
            "same disk. <bookmark mark='d'/> So the rule for everything that follows: keep together what will be read "
            "together, and write in long runs. File systems, logs and databases are designed around it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def schedule(self):
        d = load("disk")
        head = label(r"Which request next?", font_size=36).to_edge(UP, buff=0.3)
        q, h0 = d["queue"], d["head"]
        x0, x1 = -5.6, 3.4

        def X(c):
            return x0 + (x1 - x0) * c / 199
        axis = Line([x0, 2.2, 0], [x1, 2.2, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup(*[label(str(c), font_size=15, color=GREY_B).move_to([X(c), 2.5, 0]) for c in (0, 50, 100,
                                                                                                    150, 199)])
        reqs = VGroup(*[Dot([X(c), 2.2, 0], radius=0.07, color=HEAD) for c in q])
        cyl = label(r"cylinder", font_size=16, color=GREY_B).next_to(axis, LEFT, buff=0.15)
        hd = Triangle(color=YES, fill_opacity=1).scale(0.12).rotate(PI).move_to([X(h0), 2.0, 0])
        names = {"fcfs": (r"first come, first served", GREY_A), "sstf": (r"shortest seek first", NO),
                 "scan": (r"SCAN, \ the elevator", YES), "cscan": (r"C-SCAN: \ one way only", LAM)}
        paths = VGroup()
        tags = VGroup()
        ys = {"fcfs": 1.4, "sstf": 0.2, "scan": -1.0, "cscan": -2.2}
        for p in ("fcfs", "sstf", "scan", "cscan"):
            seq = [h0] + d["static"][p]["order"]
            y = ys[p]
            pts = [[X(c), y + 0.55 - 0.9 * k / (len(seq) - 1), 0] for k, c in enumerate(seq)]
            col = names[p][1]
            paths.add(VMobject(color=col, stroke_width=2.5).set_points_as_corners(pts))
            tags.add(VGroup(label(names[p][0], font_size=19, color=col),
                            label(rf"{d['static'][p]['distance']} cylinders", font_size=19, color=WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05).move_to([5.3, y + 0.1, 0]))
        with self.voiceover(
            "A busy disk has a queue of requests, and the order it serves them in matters. Here is the textbook "
            "example: the head at cylinder 53, eight requests waiting. <bookmark mark='a'/> First come, first served "
            "zigzags across the disk: 640 cylinders of travel. <bookmark mark='b'/> Shortest seek first always goes "
            "to the nearest request: 236. <bookmark mark='c'/> SCAN, the elevator, sweeps one way serving everything "
            "on its path, then the other way: 299 here. <bookmark mark='d'/> C-SCAN sweeps one way only and jumps "
            "back, so every cylinder waits about the same: 322, not counting the jump."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(reqs), FadeIn(hd), FadeIn(cyl))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(Create(paths[i]), FadeIn(tags[i]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def load_(self):
        d = load("disk")
        row = d["load"][-1]
        head = label(rf"Under load: \ {row['rate']} requests a second, \ simulated", font_size=34).to_edge(UP,
                                                                                                        buff=0.3)
        nm = {"fcfs": r"first come, first served", "sstf": r"shortest seek first", "scan": r"SCAN",
              "cscan": r"C-SCAN"}
        rows = [[nm[p], rf"{row[p]['mean']:.0f} ms", rf"{row[p]['p99']:.0f} ms", rf"{row[p]['max']:.0f} ms"]
                for p in ("fcfs", "sstf", "scan", "cscan")]
        tab = grid_table([r"policy", r"mean response", r"99th percentile", r"worst"], rows, widths=[3.6, 2.4, 2.4,
                                                                                                  2.0],
                         row_h=0.5, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        tab.cells[1][1].set_color(NO)
        tab.cells[2][3].set_color(NO)
        tab.cells[3][3].set_color(YES)
        lines = VGroup(
            label(r"first come, first served falls behind: \ the arm spends its time travelling", font_size=21,
                  color=WHITE),
            label(r"shortest seek first has the best mean, \ but a request far from the crowd can wait and wait",
                  font_size=21, color=NO),
            label(r"SCAN gets nearly the same mean with a much shorter worst case", font_size=21, color=YES),
            label(r"in practice the drive reorders its own queue \ (NCQ, \ 32 commands): \ only it knows where the "
                  r"platter is; \ Linux uses deadline-style schedulers, \ or none at all for flash", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.7)
        with self.voiceover(
            "Static queues hide the real problem, so here is a simulated disk with 72 random requests "
            "arriving every second, close to the most it can serve. <bookmark mark='a'/> First come, first served "
            "keeps up only just: the mean response is near a tenth of a second. <bookmark mark='b'/> Shortest seek "
            "first cuts the mean by a factor of three, but its worst case is long: a request at the far edge keeps "
            "losing to nearer ones. That is starvation. <bookmark mark='c'/> SCAN matches its mean and bounds the "
            "wait, because the sweep always comes back. <bookmark mark='d'/> Today the drive does much of this itself: "
            "it accepts a queue of commands and orders them, because only it knows where the platter is. For flash, "
            "with no arm at all, Linux often schedules nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i]))
        self.wait(0.3)
        self.clear_scene()
