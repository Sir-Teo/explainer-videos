from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (DATA, FILEC, HEAD, KERN, LAM, META, NO, PART, YES, load)


class Field(VoiceoverScene):
    def construct(self):
        self.card()
        self.rates()
        self.latent()
        self.end_to_end()

    def card(self):
        card = chapter_card(12, r"Disks in the field", r"How do real disks fail?", lit=(1984, 2007),
                            extra=((1984, r"Saltzer, Reed and Clark: \ end to end"),
                                   (2007, r"Schroeder and Gibson")), part=PART)
        with self.voiceover("Chapter twelve. Disks in the field."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rates(self):
        d = load("raid")
        head = label(r"What an MTTF of a million hours means", font_size=36).to_edge(UP, buff=0.3)
        W = 9.0
        vals = [(r"datasheet: \ MTTF 1{,}000{,}000 hours", 0.88, YES), (r"observed: \ typical", 3.0, HEAD),
                (r"observed: \ the worst systems", 13.0, NO)]
        bars = VGroup()
        for k, (t, v, c) in enumerate(vals):
            r = Rectangle(width=W * v / 13.0, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85)
            g = VGroup(label(t, font_size=20, color=c), r, label(rf"{v:g}\% a year", font_size=20, color=WHITE))
            g[1].move_to([-5.2, 1.7 - 1.05 * k, 0], aligned_edge=LEFT)
            g[0].next_to(g[1], UP, buff=0.08).align_to(g[1], LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.2)
            bars.add(g)
        mt = d["mttdl"]
        lines = VGroup(
            label(r"Schroeder and Gibson \ (2007), \ about 100{,}000 disks: \ yearly replacement rates of 2--4\%, \ "
                  r"up to 13\%", font_size=20, color=WHITE),
            label(r"no long flat middle to the bathtub: \ rates climb with age from the second year", font_size=20,
                  color=HEAD),
            label(r"and failures come in clusters: \ one replacement makes another soon more likely", font_size=20,
                  color=NO),
            label(rf"RAID 5's mean time to data loss, \ recomputed at 3\% a year: \ {mt[1]['raid5_years']:,.0f} years, "
                  .replace(",", "{,}") + rf"not {mt[0]['raid5_years']:,.0f}; \ and less with clusters"
                  .replace(",", "{,}"), font_size=20, color=KERN),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every reliability calculation so far took the numbers on the datasheet. A million hours between "
            "failures sounds like a hundred years. <bookmark mark='a'/> It means that a large population should lose "
            "under one percent of its disks a year. <bookmark mark='b'/> In 2007 Schroeder and Gibson looked at the "
            "replacement logs of about a hundred thousand disks in real data centres. Typical yearly replacement "
            "rates were two to four percent, <bookmark mark='c'/> and on some systems thirteen. <bookmark mark='d'/> "
            "The failures did not follow the textbook bathtub, flat for years before wearing out: rates rose steadily "
            "from the second year. <bookmark mark='e'/> And they clustered. A disk being replaced made another "
            "replacement soon more likely, which is exactly what RAID's arithmetic assumes never happens. <bookmark "
            "mark='f'/> Even with independent failures, the mean time to data loss falls more than tenfold when the "
            "real rate is used."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
            vo.wait_until("f")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def latent(self):
        head = label(r"Errors that do not announce themselves", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(a, font_size=22, color=c), label(b, font_size=18, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07) for a, b, c in (
            (r"\textbf{latent sector errors}: \ a sector that can no longer be read",
             r"Bairavasundaram et al. \ (2007): \ 3.45\% of 1.53 million disks developed them within 32 months; \ "
             r"found only when someone reads", HEAD),
            (r"\textbf{silent corruption}: \ the disk returns the wrong bytes, \ and says nothing",
             r"the same group \ (2008): \ more than 400{,}000 checksum mismatches over 41 months", NO),
            (r"\textbf{lost and misdirected writes}: \ acknowledged, \ but never written, \ or written elsewhere",
             r"the disk's own checks pass: \ its error-correcting code is correct for the wrong block", KERN),
            (r"\textbf{firmware}, \ cables, \ controllers, \ memory", r"every layer between the program and the "
                                                                     r"platter can damage data", LAM),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        with self.voiceover(
            "Whole-disk failures at least announce themselves. Worse are the errors that do not. <bookmark mark='a'/> "
            "A latent sector error is a sector that has quietly become unreadable. A study of one and a half million "
            "disks found them in three and a half percent within 32 months, and they are discovered only when someone "
            "reads, which may be during a rebuild. <bookmark mark='b'/> Silent corruption is a disk returning the wrong "
            "bytes without any error at all: the same group counted over four hundred thousand checksum mismatches "
            "in that population. <bookmark mark='c'/> Some writes are acknowledged and then lost, or written to the "
            "wrong place, and the disk's own error-correcting code cannot notice, because it is correct for the block "
            "it is attached to. <bookmark mark='d'/> And every layer in between, from firmware to cables to memory, "
            "can do damage."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def end_to_end(self):
        head = label(r"Check at the ends", font_size=36).to_edge(UP, buff=0.3)
        chain = VGroup(*[label(t, font_size=19, color=c) for t, c in (
            (r"program", DATA), (r"file system", META), (r"page cache", HEAD), (r"driver", KERN), (r"controller", LAM),
            (r"cable", GREY_B), (r"disk firmware", KERN), (r"platter", FILEC))])
        boxes = VGroup()
        for t in chain:
            r = RoundedRectangle(width=1.45, height=0.55, corner_radius=0.08, stroke_color=t.get_color(),
                                 stroke_width=1.6)
            if t.width > 1.35:
                t.width = 1.35
            boxes.add(VGroup(r, t.move_to(r)))
        boxes.arrange(RIGHT, buff=0.12).next_to(head, DOWN, buff=0.7)
        span = DoubleArrow(boxes[1].get_bottom() + DOWN * 0.15, boxes[-1].get_bottom() + DOWN * 0.15, buff=0,
                           color=YES, stroke_width=2.5)
        spl = label(r"a checksum written by the file system, \ verified when it reads", font_size=19,
                    color=YES).next_to(span, DOWN, buff=0.1)
        lines = VGroup(
            label(r"the \textbf{end-to-end argument} \ (Saltzer, Reed and Clark, 1984): \ a check is only complete "
                  r"where the data is used", font_size=20, color=WHITE),
            label(r"so ZFS and btrfs checksum every block \ (chapter 10); \ databases checksum their pages", font_size=20,
                  color=YES),
            label(r"\textbf{scrub}: \ read everything regularly, \ and repair from redundancy while it still exists",
                  font_size=20, color=HEAD),
            label(r"and keep copies on other machines: \ replication \ (Parts 39 and 45)", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "What can be trusted, then? <bookmark mark='a'/> Saltzer, Reed and Clark's end-to-end argument says that "
            "a check made in the middle of a path cannot vouch for the whole of it; only a check at the ends can. A "
            "disk's own error correction protects the platter, but not the cable, the controller, or a write that went "
            "to the wrong place. <bookmark mark='b'/> So the file system itself should checksum what it writes and "
            "verify what it reads, as ZFS and btrfs do, and as databases do for their pages. <bookmark mark='c'/> "
            "Scrubbing reads everything regularly, so latent errors are found and repaired while the redundancy to "
            "repair them still exists. <bookmark mark='d'/> And because whole machines and whole buildings fail too, "
            "the final defence is copies elsewhere, which Parts 39 and 45 take up."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(span), FadeIn(spl), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
