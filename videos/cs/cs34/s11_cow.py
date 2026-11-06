from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (FILEC, HEAD, KERN, LAM, META, NO, PART, YES, blk, load)


def tnode(text, color, w=0.9, h=0.5, font=16, fill=0.25):
    return blk(text, color, w=w, h=h, font=font, fill=fill)


class Cow(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.checksums()
        self.snapshots()

    def card(self):
        card = chapter_card(10, r"Copy-on-write and checksums", r"What if nothing were ever overwritten?",
                            lit=(1994, 2005), extra=((1994, r"WAFL"), (2005, r"ZFS")), part=PART)
        with self.voiceover("Chapter ten. Copy-on-write and checksums."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _tree(self):
        root = tnode(r"root", KERN, w=1.2).move_to([-2.5, 2.2, 0])
        mids = VGroup(*[tnode("", META) for _ in range(4)]).arrange(RIGHT, buff=0.5).move_to([-2.5, 1.1, 0])
        lows = VGroup(*[tnode("", META, w=0.7) for _ in range(4)]).arrange(RIGHT, buff=0.25).move_to([-3.6, 0.0, 0])
        leaves = VGroup(*[tnode("", FILEC, w=0.55, h=0.45) for _ in range(4)]).arrange(RIGHT, buff=0.12)
        leaves.move_to([-4.3, -1.1, 0])
        e = VGroup(*[Line(root.get_bottom(), m.get_top(), color=GREY_B, stroke_width=1.5) for m in mids],
                   *[Line(mids[1].get_bottom(), x.get_top(), color=GREY_B, stroke_width=1.5) for x in lows],
                   *[Line(lows[1].get_bottom(), x.get_top(), color=GREY_B, stroke_width=1.5) for x in leaves])
        return root, mids, lows, leaves, e

    def tree(self):
        d = load("cow")
        head = label(r"Change one block: \ copy the path to the root", font_size=34).to_edge(UP, buff=0.3)
        root, mids, lows, leaves, e = self._tree()
        uber = blk(r"uberblock", YES, w=1.7, h=0.5, font=15).move_to([-2.5, 3.1, 0]).shift(DOWN * 0.15)
        ue = Arrow(uber.get_bottom(), root.get_top(), buff=0.04, color=YES, stroke_width=2)
        nl = tnode("", YES, w=0.55, h=0.45).move_to(leaves[1].get_center() + RIGHT * 4.6)
        nlow = tnode("", YES, w=0.7).move_to(lows[1].get_center() + RIGHT * 4.6)
        nmid = tnode("", YES).move_to(mids[1].get_center() + RIGHT * 4.6)
        nroot = tnode(r"root", YES, w=1.2).move_to(root.get_center() + RIGHT * 4.6)
        new_e = VGroup(Line(nroot.get_bottom(), nmid.get_top(), color=YES, stroke_width=2),
                       Line(nmid.get_bottom(), nlow.get_top(), color=YES, stroke_width=2),
                       Line(nlow.get_bottom(), nl.get_top(), color=YES, stroke_width=2))
        shared = VGroup(*[DashedLine(nroot.get_bottom(), m.get_top(), color=GREY_D, stroke_width=1.2)
                          for k, m in enumerate(mids) if k != 1],
                        *[DashedLine(nmid.get_bottom(), x.get_top(), color=GREY_D, stroke_width=1.2)
                          for k, x in enumerate(lows) if k != 1],
                        *[DashedLine(nlow.get_bottom(), x.get_top(), color=GREY_D, stroke_width=1.2)
                          for k, x in enumerate(leaves) if k != 1])
        lines = VGroup(
            label(r"write the new data to a \textbf{new} block; \ then a new copy of its parent pointing to it; \ up "
                  r"to a new root", font_size=20, color=YES),
            label(rf"{d['per_write'][0]} blocks for one change in a tree of depth {d['depth']}; \ everything else is "
                  rf"shared", font_size=20, color=WHITE),
            label(r"then \textbf{one} small write switches the uberblock to the new root: \ the atomic moment", font_size=20,
                  color=HEAD),
            label(r"a crash before it: \ the old tree, \ whole; \ after it: \ the new one, \ whole; \ no journal, \ "
                  r"no fsck", font_size=20, color=KERN),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A third answer to crashes: never overwrite anything. NetApp's WAFL file system did this in 1994, and "
            "ZFS and btrfs later. The whole file system is a tree of blocks hanging from one root. <bookmark "
            "mark='a'/> To change one data block, write the new contents to a fresh block. Its parent must now point "
            "somewhere else, so write a fresh copy of the parent too, and so on up to a new root. <bookmark "
            "mark='b'/> In our tree of depth three that is four blocks, and every other block is shared between the "
            "old tree and the new. <bookmark mark='c'/> The last step is one small write: the uberblock, at a fixed "
            "place, switches to the new root. <bookmark mark='d'/> Crash before that write, and the old tree is "
            "untouched. Crash after, and the new one is complete. There is no journal to replay and nothing for fsck "
            "to do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), FadeIn(mids), FadeIn(lows), FadeIn(leaves), Create(e), FadeIn(uber),
                      GrowArrow(ue))
            vo.wait_until("a")
            self.play(FadeIn(nl), Create(new_e[2]), FadeIn(nlow), FadeIn(lines[0]))
            self.play(Create(new_e[1]), FadeIn(nmid))
            self.play(Create(new_e[0]), FadeIn(nroot))
            vo.wait_until("b")
            self.play(Create(shared), FadeIn(lines[1]))
            vo.wait_until("c")
            ue2 = Arrow(uber.get_right(), nroot.get_top(), buff=0.06, color=YES, stroke_width=2.5)
            self.play(Transform(ue, ue2), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def checksums(self):
        d = load("cow")
        head = label(r"Every pointer carries a checksum", font_size=36).to_edge(UP, buff=0.3)
        root = tnode(r"root", KERN, w=1.6).move_to([0, 2.0, 0])
        kids = VGroup(*[tnode(rf"\texttt{{{h}}}", META, w=1.6, font=14) for h in ("a3f1", "7c02", "e9d4")]).arrange(
            RIGHT, buff=0.8).move_to([0, 0.6, 0])
        leaves = VGroup(*[tnode(rf"\texttt{{{h}}}", FILEC, w=1.2, font=13) for h in ("51b8", "0a7e", "c4c9")]).arrange(
            RIGHT, buff=0.4).move_to([2.4, -0.8, 0])
        e = VGroup(*[Line(root.get_bottom(), k.get_top(), color=GREY_B, stroke_width=1.5) for k in kids],
                   *[Line(kids[2].get_bottom(), x.get_top(), color=GREY_B, stroke_width=1.5) for x in leaves])
        bad = leaves[1]
        lines = VGroup(
            label(r"a parent stores, \ beside each pointer, \ a checksum of the child: \ a Merkle tree \ (Part 29)",
                  font_size=20, color=WHITE),
            label(r"so the root vouches for every block below it", font_size=20, color=HEAD),
            label(rf"flip one bit in a leaf: \ reading it, \ the parent's checksum no longer matches: \ caught "
                  rf"\ ({d['found']} bad block found)", font_size=20, color=NO),
            label(rf"with a mirror or parity, \ rewrite it from the good copy: \ {d['after']} bad blocks after "
                  r"the repair", font_size=20, color=YES),
            label(r"ZFS checksums every block, \ and \textbf{scrubs} the whole pool in the background", font_size=20,
                  color=LAM),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Copy-on-write makes a second idea cheap. <bookmark mark='a'/> Since a parent is rewritten whenever a "
            "child changes anyway, let it store, next to each pointer, a checksum of the child. This is Part 29's "
            "Merkle tree. <bookmark mark='b'/> The root's checksum now vouches for every block in the file system. "
            "<bookmark mark='c'/> Suppose a bit rots in a data block, or the disk returns the wrong block. A "
            "traditional file system would hand the bad bytes to the program. Here, the parent's checksum does not "
            "match, and the error is caught. <bookmark mark='d'/> With a mirror, the file system reads the other copy, "
            "checks it, and rewrites the bad one. <bookmark mark='e'/> ZFS does this for every block, and scrubs the "
            "whole pool in the background to find rot before anyone reads it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), FadeIn(kids), FadeIn(leaves), Create(e))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), Indicate(root, color=HEAD))
            vo.wait_until("c")
            self.play(bad[0].animate.set_stroke(NO, width=4).set_fill(NO, opacity=0.4), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(bad[0].animate.set_stroke(YES, width=2).set_fill(YES, opacity=0.3), FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def snapshots(self):
        d = load("cow")
        head = label(r"Snapshots for free, \ and the price", font_size=36).to_edge(UP, buff=0.3)
        W = 9.0
        tot = d["now"] + d["snapshot"]
        bars = VGroup()
        for t, v, c in ((r"two separate copies", tot, GREY_B), (r"now and the snapshot, \ sharing", d["live"], YES)):
            r = Rectangle(width=W * v / tot, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.85)
            bars.add(VGroup(label(t, font_size=20, color=c), r, label(rf"{v} blocks", font_size=20, color=WHITE)))
        for k, b in enumerate(bars):
            b[1].move_to([-5.0, 1.6 - 1.2 * k, 0], aligned_edge=LEFT)
            b[0].next_to(b[1], UP, buff=0.08).align_to(b[1], LEFT)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        lines = VGroup(
            label(r"a \textbf{snapshot} is an old root kept alive: \ taking one costs a single pointer", font_size=21,
                  color=YES),
            label(rf"after {len(d['per_write']) + 10} block writes: \ {d['shared']} of the {d['now']} blocks are "
                  r"still shared", font_size=21, color=WHITE),
            label(r"the price: \ every small write rewrites its path, \ and a file's blocks end up wherever free "
                  r"space was", font_size=21, color=NO),
            label(r"so writes are gathered into \textbf{transaction groups}, \ a few seconds at a time, \ sharing "
                  r"the upper levels", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And a third gift. <bookmark mark='a'/> Keep an old root instead of freeing it, and you have a snapshot: "
            "the whole file system as it was, for the cost of one pointer. <bookmark mark='b'/> After thirteen "
            "writes to our tree, the current version and Monday's snapshot together need 113 blocks, where two copies "
            "would need 170: fifty-seven are still shared. <bookmark mark='c'/> There is a price. Every small write "
            "rewrites the path above it, and since nothing is updated in place, a file that is rewritten piecemeal "
            "ends up scattered. <bookmark mark='d'/> So ZFS gathers seconds of writes into one transaction group, and "
            "writes the shared upper levels once for all of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
