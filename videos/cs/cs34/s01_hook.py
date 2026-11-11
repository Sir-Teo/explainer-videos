from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BITS, FILEC, HEAD, META, NO, PART, YES, blk, load, num)

ROLE = {"data bitmap": ("bitmap", BITS), "data": ("data", FILEC), "inode table": ("inode", META)}


class Hook(VoiceoverScene):
    def construct(self):
        self.append()
        self.eight()
        self.plan()

    def append(self):
        h = load("hook")
        head = label(r"Append one block, \ and the power fails", font_size=36).to_edge(UP, buff=0.3)
        ram = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.6)
        ram.move_to([-3.6, 0.9, 0])
        rl = label(r"memory: \ the file system's view", font_size=20, color=GREY_A).next_to(ram, UP, buff=0.1)
        dsk = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.6)
        dsk.move_to([3.6, 0.9, 0])
        dl = label(r"the disk", font_size=20, color=GREY_A).next_to(dsk, UP, buff=0.1)
        names = [ROLE[r] for r in h["writes"]]
        mem = VGroup(*[blk(n, c, w=1.2, h=0.8, font=18, fill=0.35) for n, c in names]).arrange(RIGHT, buff=0.25)
        mem.move_to(ram)
        disk = VGroup(*[blk(n, c, w=1.2, h=0.8, font=18, fill=0.05) for n, c in names]).arrange(RIGHT, buff=0.25)
        disk.move_to(dsk)
        for b in disk:
            b[0].set_stroke(opacity=0.35)
            b[1].set_opacity(0.35)
        lines = VGroup(
            label(r"three blocks must change: \ the \textbf{bitmap} marks a block used, \ the \textbf{data} goes in "
                  r"it, \ the \textbf{inode} points at it", font_size=21, color=WHITE),
            label(r"the disk writes them one at a time, \ in an order of its own choosing", font_size=21,
                  color=HEAD),
            label(r"a crash can leave \textbf{any subset} of the three on the disk: \ $2^3 = 8$ possible disks",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        bolt = VMobject(color=YELLOW, stroke_width=5).set_points_as_corners(
            [[0.25, 2.1, 0], [-0.15, 1.2, 0], [0.2, 1.2, 0], [-0.25, 0.1, 0]])
        with self.voiceover(
            "You add a line to a file, and the power fails. <bookmark mark='a'/> What is on the disk? To append a "
            "block, the file system must change three blocks: a bitmap, to mark a free block as used; the block "
            "itself, with the new data; and the file's inode, to point at it and record the new length. <bookmark "
            "mark='b'/> In memory all three change at once. But the disk writes one block at a time, and it is free "
            "to reorder them for speed. <bookmark mark='c'/> So a crash can leave any subset of the three on the "
            "disk. Eight possible disks."
        ) as vo:
            self.play(FadeIn(head), Create(ram), Create(dsk), FadeIn(rl), FadeIn(dl), FadeIn(disk))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, scale=0.9) for m in mem], lag_ratio=0.3), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            fly = mem[0].copy()
            self.play(fly.animate.move_to(disk[0]), run_time=1.2)
            self.add(fly)
            vo.wait_until("c")
            self.play(Create(bolt), FadeIn(lines[2]))
            self.play(FadeOut(bolt), run_time=0.4)
        self.wait(0.3)
        self.clear_scene()

    def eight(self):
        h = load("hook")
        head = label(r"Every disk a crash can leave", font_size=36).to_edge(UP, buff=0.3)
        roles = h["writes"]
        cells = VGroup()
        verdicts = []
        for s in h["states"]:
            boxes = VGroup()
            for r in roles:
                nm, c = ROLE[r]
                on = r in s["durable"]
                b = blk(nm, c, w=1.0, h=0.62, font=17, fill=0.45 if on else 0.0)
                if not on:
                    b[0].set_stroke(opacity=0.3)
                    b[1].set_opacity(0.3)
                boxes.add(b)
            boxes.arrange(RIGHT, buff=0.08)
            probs = s["problems"]
            if s["content"] == "another file's bytes":
                txt, col = r"the file shows \\ \texttt{PASSWORD=hunter2}", NO
            elif any(p != "leaked block" for p in probs):
                txt, col = r"corrupt: \ a used block \\ marked free", NO
            elif probs:
                txt, col = r"a block lost \\ (harmless)", HEAD
            else:
                txt, col = (r"old file, \ intact" if s["content"] == "old" else r"new file, \ intact"), YES
            verdicts.append((txt, col, s))
            fsck_txt = r"fsck: \ clean" if not probs else r"fsck: \ " + ", ".join(p for p in probs)
            v = label(txt, font_size=21, color=col)
            f = label(fsck_txt, font_size=17, color=GREY_B)
            frame = RoundedRectangle(width=3.3, height=2.45, corner_radius=0.1, stroke_color=GREY_D, stroke_width=1.2)
            inner = VGroup(boxes, v, f).arrange(DOWN, buff=0.2)
            if inner.width > 3.15:
                inner.width = 3.15
            inner.move_to(frame)
            cells.add(VGroup(frame, inner))
        cells.arrange_in_grid(rows=2, cols=4, buff=(0.16, 0.25)).next_to(head, DOWN, buff=0.35)
        bad = [i for i, (_, _, s) in enumerate(verdicts) if s["content"] == "another file's bytes"]
        sneaky = [i for i in bad if not verdicts[i][2]["problems"]]
        c = load("crash")
        none = next(r for r in c["rows"] if r["mode"] == "none")
        ordered = next(r for r in c["rows"] if r["mode"] == "ordered" and "barriers" not in r)
        foot = VGroup(
            label(rf"across four operations, \ {num(none['states'])} crash points: \ {none['corrupt']} corrupt, \ "
                  rf"{none['bad_data']} show the wrong bytes", font_size=21, color=NO),
            label(rf"with a journal, \ in ordered mode: \ all {num(ordered['states'])} come back intact \ "
                  rf"(chapter 8)", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here they are, all eight, each mounted and checked. <bookmark mark='a'/> Nothing written: the old file, "
            "intact. Only the data written: also fine, the new block sits unused. <bookmark mark='b'/> Bitmap without "
            "inode: a block is marked used that nobody owns. A leak, harmless but wasteful. <bookmark mark='c'/> The "
            "inode without the bitmap: the file points at a block the bitmap calls free, and the next file to be "
            "written will be handed it too. Corrupt. <bookmark mark='d'/> And the worst: bitmap and inode, but not "
            "the data. The checker finds nothing wrong at all. Yet the file now ends with whatever that block held "
            "before: here, a password from a file someone deleted. <bookmark mark='e'/> Across four common operations "
            "our checker finds 34 crash points that corrupt the file system and 22 that show the wrong bytes. With a "
            "journal, every one comes back intact. This part is about why."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]), FadeIn(cells[2]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1]), FadeIn(cells[4]))
            vo.wait_until("c")
            self.play(FadeIn(cells[3]), FadeIn(cells[6]))
            vo.wait_until("d")
            for i in range(8):
                if i not in (0, 1, 2, 3, 4, 6):
                    self.play(FadeIn(cells[i]), run_time=0.6)
            for i in sneaky:
                self.play(cells[i][0].animate.set_stroke(NO, width=3.5), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.wait(0.5)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Storage", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"disks and flash: \ seeks, \ erase blocks, \ write amplification, \ modelled and simulated",
            r"a Unix file system: \ inodes, \ directories, \ and where the blocks go",
            r"every crash point, \ checked: \ fsck, \ ordered writes, \ journaling",
            r"logs, \ copy-on-write trees and checksums; \ RAID and real failure rates",
            r"fsync, \ and what applications must do; \ LSM trees",
            r"PebbleOS reads the novels from its own file system",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 34 of Computer Science, Built: Storage, the last part of the operating systems act. <bookmark "
            "mark='a'/> We begin at the bottom, with disks and flash, and model the time each takes. We build a Unix file system "
            "and put its blocks where reading them is fast. Then we crash it, at every point, and check it each time, "
            "and build the defences one by one: careful ordering, journaling, logs, copy-on-write trees with "
            "checksums, and RAID, with the failure rates disks really have. We ask what fsync promises and what "
            "applications must do, meet the LSM trees behind most modern databases, and end with PebbleOS reading "
            "the thirty novels from a file system of its own."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
