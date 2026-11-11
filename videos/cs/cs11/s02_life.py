from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble.isa import Instr, encode
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FILE_COLORS, FUNC, HEAD, NO, PART, YES, code, load,
                                   memory_strip, region)


class Life(VoiceoverScene):
    def construct(self):
        self.card()
        self.tower()
        self.journey()

    def card(self):
        card = chapter_card(1, r"A program's life", r"What happens between writing a program and running it?",
                            part=PART)
        with self.voiceover("Chapter one. A program's life."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tower(self):
        head = label(r"Five steps from text to process", font_size=34).to_edge(UP, buff=0.3)
        steps = [(r"source code", r"text a person wrote", YES, r"main.c"),
                 (r"compiler", r"translates it to assembly \ (Part 13)", DATA, r"main.s"),
                 (r"assembler", r"assembly to machine words, \ with holes for unknown addresses \ (Part 6)", CTRL,
                  r"main.o"),
                 (r"linker", r"joins object files, \ fills the holes", FUNC, r"job"),
                 (r"loader", "maps segments, initializes memory and stack, transfers control", HEAD,
                  r"a process")]
        rows = VGroup()
        for name, what, c, art in steps:
            rows.add(VGroup(region(2.4, 0.62, name, c, font_size=22), label(what, font_size=19, color=GREY_A),
                            label(rf"$\to$ \ \texttt{{{art}}}" if art != r"a process" else r"$\to$ \ a process",
                                  font_size=19, color=c)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].next_to(r[1], RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(DOWN * 0.15 + LEFT * 0.3)
        with self.voiceover(
            (
            "Follow the build pipeline from text to a process. <bookmark mark='a'/> Source code describes the "
            "program in a language. <bookmark mark='b'/> A compiler can translate it into assembly; Part 13 "
            "builds that stage. Real toolchains may combine stages or use an intermediate representation. "
            "<bookmark mark='c'/> The assembler encodes instructions and records unresolved symbols as "
            "relocations in an object file. <bookmark mark='d'/> The linker combines objects and libraries, lays "
            "out sections and resolves references that can be fixed at link time. Dynamic references can remain "
            "for later. <bookmark mark='e'/> On Linux, the loader maps the executable's segments, arranges "
            "zero-filled memory and an initial stack, and transfers control to the entry point or dynamic linker. "
            "Runtime startup eventually calls main. Mapping need not read every file page immediately; demand "
            "paging comes in Part 32."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def journey(self):
        pl = load("pebblelink")
        p = next(x for x in pl["patches"] if x["file"] == "main.o" and x["symbol"] == "lookup")
        at, target = p["at"], p["target"]
        before = encode(Instr("jal", rd=1, imm=0))
        after = encode(Instr("jal", rd=1, imm=(target - at) // 4))
        head = label(r"One call's journey", font_size=34).to_edge(UP, buff=0.3)
        stages = VGroup(
            VGroup(label(r"source", font_size=20, color=YES), Text("lookup(word, length);", font="DejaVu Sans Mono",
                                                                   font_size=20, color=CODE)),
            VGroup(label(r"assembly", font_size=20, color=DATA), Text("call lookup", font="DejaVu Sans Mono",
                                                                      font_size=20, color=CODE)),
            VGroup(label(r"main.o: \ a hole", font_size=20, color=CTRL),
                   Text(f"{before:08x}   jal ra, ?", font="DejaVu Sans Mono", font_size=20, color=CODE)),
            VGroup(label(r"its note", font_size=20, color=CTRL),
                   Text(f"at {at}: pc22 lookup", font="DejaVu Sans Mono", font_size=20, color=GREY_A)),
            VGroup(label(r"linked", font_size=20, color=FUNC),
                   Text(f"{after:08x}   jal ra, +{(target - at) // 4}   # lookup is at {target}",
                        font="DejaVu Sans Mono", font_size=20, color=CODE)),
        )
        for s in stages:
            s[0].move_to([-4.6, 0, 0], aligned_edge=RIGHT)
            s[1].next_to(s[0], RIGHT, buff=0.5)
        stages.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        for s in stages:
            s[0].align_to([-4.4, 0, 0], RIGHT)
            s[1].align_to([-4.1, 0, 0], LEFT)
        mem = memory_strip([(r"main.o text", 0.17, FILE_COLORS[0]), (r"table.o text", 0.6, FILE_COLORS[1]),
                            (r"alloc.o, io.o", 0.23, FILE_COLORS[2])], w=2.0, total_h=3.6).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Follow one call through. <bookmark mark='a'/> In the source it is a call to lookup, with the word and "
            "its length. <bookmark mark='b'/> In assembly it becomes call lookup. <bookmark mark='c'/> But lookup "
            "is in another file, so the assembler cannot know how far away it is. It emits a jump-and-link with an "
            "offset of zero, <bookmark mark='d'/> and a note, a relocation: at byte eighty-eight of my code, put the "
            "distance to lookup, in the 22-bit form a jump uses. <bookmark mark='e'/> The linker places main's code "
            f"at address zero and the table's code after it, so lookup lands at {target}. It writes the distance, "
            f"{(target - at) // 4} instructions, into the hole. Nothing else about the word changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mem))
            for mk, s in zip("abcde", stages):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
