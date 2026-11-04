from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FIELD_COLOR, FUNC, HEAD, HIST, INF, NO, PART, YES,
                                  Shelves, address_bits, fmt, load, mono)

# a little direct-mapped cache: 8 sets of one 16-byte line, 8-bit addresses: tag 1 bit, index 3, offset 4
SETS, LINE = 8, 16
ACCESSES = [0x14, 0x18, 0x24, 0x94, 0x14, 0x60, 0x64, 0xA4, 0x24]


class Direct(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.walk()
        self.real()

    def card(self):
        card = chapter_card(3, r"A direct-mapped cache", r"Where in the cache does an address go?", lit=(1965,),
                            extra=((1965, r"Wilkes: \ slave memories"),), part=PART)
        with self.voiceover("Chapter three. A direct-mapped cache."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def split(self):
        head = label(r"An address, \ cut into three", font_size=36).to_edge(UP, buff=0.35)
        a = address_bits(0x00010A4C, 18, 8, 6, cell=0.3, font_size=15).move_to(UP * 0.9)
        cap = label(r"a 32-bit address, \ for a 16 KB cache of 256 lines of 64 bytes", font_size=24,
                    color=GREY_A).next_to(a, UP, buff=0.35)
        expl = VGroup(
            label(r"offset: \ which byte inside the line \ ($2^6 = 64$ bytes)", font_size=24, color=FIELD_COLOR["offset"]),
            label(r"index: \ which line of the cache it must go in \ ($2^8 = 256$ lines)", font_size=24,
                  color=FIELD_COLOR["index"]),
            label(r"tag: \ the rest, \ stored with the line, \ to say \textit{which} address is there", font_size=24,
                  color=FIELD_COLOR["tag"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The first caches appeared in the 1960s; Maurice Wilkes described the idea in 1965 as a slave memory, and "
            "IBM's System/360 Model 85 shipped one in 1968. The simplest design is direct-mapped: every address has "
            "exactly one place in the cache it can go. <bookmark mark='a'/> Take a sixteen-kilobyte cache of two "
            "hundred fifty-six lines, each sixty-four bytes. An address is cut into three fields. <bookmark mark='b'/> "
            "The lowest six bits are the offset: which byte within the sixty-four-byte line. <bookmark mark='c'/> The "
            "next eight bits are the index: which of the two hundred fifty-six lines of the cache this address must "
            "live in. <bookmark mark='d'/> The rest is the tag. Many addresses share an index, so the cache stores the "
            "tag beside each line, and on every access compares it: same tag, a hit; different tag or an empty line, "
            "a miss."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(a.cells))
            vo.wait_until("b")
            self.play(FadeIn(a.braces[2]), FadeIn(expl[0]))
            vo.wait_until("c")
            self.play(FadeIn(a.braces[1]), FadeIn(expl[1]))
            vo.wait_until("d")
            self.play(FadeIn(a.braces[0]), FadeIn(expl[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walk(self):
        head = label(r"Eight lines, \ nine accesses", font_size=34).to_edge(UP, buff=0.3)
        sh = Shelves(SETS, 1, w=1.9, h=0.48).move_to(RIGHT * 2.6 + DOWN * 0.3)
        legend = label(r"8-bit addresses: \ tag 1 bit, \ index 3, \ offset 4", font_size=20, color=GREY_B).next_to(
            sh, UP, buff=0.25)
        listing = VGroup()
        results = []
        content: dict[int, int] = {}
        for addr in ACCESSES:
            tag, idx = addr >> 7, (addr >> 4) & 7
            hit = content.get(idx) == tag
            kind = "hit" if hit else ("miss" if idx not in content else "miss, \\ evicts")
            content[idx] = tag
            results.append((addr, tag, idx, hit, kind))
        for addr, tag, idx, hit, kind in results:
            row = VGroup(Text(f"{addr:#04x}", font="DejaVu Sans Mono", font_size=18, color=CODE),
                         Text(format(addr, "08b"), font="DejaVu Sans Mono", font_size=16, color=GREY_B),
                         label(rf"set {idx}: \ " + kind, font_size=18, color=YES if hit else NO)).arrange(RIGHT, buff=0.3)
            listing.add(row)
        listing.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        tally = label(r"", font_size=22)
        shown = {}
        with self.voiceover(
            "Here is a toy cache to watch: eight lines of sixteen bytes, and eight-bit addresses, so one bit of tag, "
            "three of index and four of offset. <bookmark mark='a'/> The first access, hex fourteen, has index one: "
            "the line is empty, a miss, and the line is filled. The second, hex eighteen, falls in the same "
            "sixteen-byte line: a hit, by spatial locality. <bookmark mark='b'/> Watch hex ninety-four. Its index is "
            "also one, but its tag is different, so it throws out the line that hex fourteen brought in, and when hex "
            "fourteen comes back, it misses again. <bookmark mark='c'/> Two busy addresses that share an index fight "
            "over one line even when the rest of the cache is empty. That is the weakness of direct mapping, and the "
            "next chapter's subject."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sh), FadeIn(legend))
            vo.wait_until("a")
            for k, (addr, tag, idx, hit, kind) in enumerate(results):
                if k == 3:
                    vo.wait_until("b")
                self.play(FadeIn(listing[k]), run_time=0.4)
                new = sh.put(idx, 0, f"{addr & 0xF0:#04x}..", YES if hit else NO)
                if idx in shown:
                    self.play(Transform(shown[idx], new), run_time=0.5)
                else:
                    shown[idx] = new
                    self.play(FadeIn(new), run_time=0.5)
                self.play(Indicate(listing[k][2], color=YES if hit else NO), run_time=0.4)
            vo.wait_until("c")
            self.play(*[Indicate(listing[k], color=NO) for k in (0, 3, 4)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real(self):
        d = load("threec")
        rows = {(r["kb"], r["ways"]): r for r in d["rows"]}
        head = label(r"It happens to the Job", font_size=36).to_edge(UP, buff=0.4)
        a = rows[(8, 1)]
        b = rows[(8, 2)]
        lines = VGroup(
            label(r"the word table starts at \texttt{0x10000}, \ the letters at \texttt{0x80000}", font_size=26,
                  color=GREY_A),
            label(r"in a direct-mapped cache of 8 or 16 KB, \ both start in set 0: \ they collide, \ all the way up",
                  font_size=26, color=NO),
            label(rf"8 KB, \ direct-mapped: \ {a['misses']:,} misses", font_size=28, color=NO),
            label(rf"8 KB, \ two lines per set: \ {b['misses']:,} \ (only the first touch of each line)",
                  font_size=28, color=YES),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "This is not a toy problem. <bookmark mark='a'/> The Job keeps its word table at hex ten thousand and the "
            "letters of its words at hex eighty thousand. <bookmark mark='b'/> Both addresses are multiples of the "
            "cache size, so in a direct-mapped cache of eight or sixteen kilobytes, the table and the letters map to "
            "the same sets, line for line, and evict each other constantly. <bookmark mark='c'/> On the first "
            "chapter, an eight-kilobyte direct-mapped cache misses fifteen thousand times. <bookmark mark='d'/> "
            "Allow each set to hold two lines, and the same eight kilobytes miss ninety-two times: once for each "
            "line the chapter ever touches."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
