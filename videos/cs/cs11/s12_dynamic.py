from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, code, load, region)


class Dynamic(VoiceoverScene):
    def construct(self):
        self.card()
        self.compare()
        self.plt()
        self.interpose()

    def card(self):
        card = chapter_card(11, r"Dynamic linking", r"Why isn't every program a copy of the C library?",
                            lit=(1987,), extra=((1987, r"SunOS 4: \ shared libraries"),), part=PART)
        with self.voiceover("Chapter eleven. Dynamic linking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def compare(self):
        d = load("dynamic")
        dy, st = d["dynamic"], d["static"]
        head = label(r"\texttt{hello.c}, \ linked two ways on this machine", font_size=32).to_edge(UP, buff=0.3)
        ch = bar_chart([st["bytes"] / 1024, dy["bytes"] / 1024], [r"static", r"dynamic"], [NO, YES], height=3.0,
                       bar_w=1.3, gap=1.2, fmt_=lambda v: f"{v:,.0f} KB", font_size=20).to_edge(LEFT, buff=1.2).shift(
            DOWN * 0.3)
        side = VGroup(
            label(r"static: \ the C library's code copied into the file", font_size=21, color=NO),
            label(rf"dynamic: \ a note saying \texttt{{{dy['needed'][0]}}} is needed, \\ and one import: "
                  rf"\texttt{{{dy['plt'][0].replace('_', chr(92) + '_')}}}", font_size=21, color=YES),
            label(rf"start-up: \ {st['start_ms']:.2f} ms static, \ {dy['start_ms']:.2f} ms dynamic \\ (finding and "
                  r"mapping the library costs a little)", font_size=21, color=GREY_A),
            label(r"one copy of libc in memory, \ shared by every process; \\ fix a bug once, \ every program has "
                  r"the fix", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        ldd = code(d["ldd"], size=14, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A two-line program that prints hello, linked two ways on this computer. <bookmark mark='a'/> Linked "
            f"statically, the parts of the C library it uses are copied into the file: {st['bytes'] / 1024:.0f} "
            f"kilobytes. Linked dynamically, the file is {dy['bytes'] / 1024:.0f} kilobytes, <bookmark mark='b'/> "
            "because it holds only a note that it needs the C library, and a list of the functions it will take "
            "from it: here, just puts, with a version tag saying which interface of glibc it expects. <bookmark mark='c'/> The price is "
            "a little start-up work, finding and mapping the library, about a tenth of a millisecond here. "
            "<bookmark mark='d'/> The gains are large: one copy of the library in memory, shared by every process "
            "that uses it, and a security fix to the library fixes every program at once. ldd lists what a program "
            "will load."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch[0]), FadeIn(ch.names), GrowFromEdge(ch.bars[0], DOWN), FadeIn(ch.vals[0]),
                      FadeIn(side[0]))
            self.play(GrowFromEdge(ch.bars[1], DOWN), FadeIn(ch.vals[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(ldd))
        self.wait(0.3)
        self.clear_scene()

    def plt(self):
        head = label(r"Position-independent code, \ the GOT and the PLT", font_size=32).to_edge(UP, buff=0.3)
        call = region(3.0, 0.7, r"\texttt{call puts@plt}", DATA, font_size=20).move_to(LEFT * 4.6 + UP * 1.2)
        plt = region(3.2, 0.7, r"PLT: \ \texttt{jmp *GOT[puts]}", CTRL, font_size=20).move_to(LEFT * 0.6 + UP * 1.2)
        got = region(3.0, 0.7, r"GOT: \ \texttt{puts} $\to$ ?", FUNC, font_size=20).move_to(RIGHT * 3.6 + UP * 1.2)
        lib = region(3.0, 0.7, r"libc: \ \texttt{puts}", YES, font_size=20).move_to(RIGHT * 3.6 + DOWN * 0.5)
        ld = region(3.2, 0.7, r"the dynamic linker", HEAD, font_size=20).move_to(LEFT * 0.6 + DOWN * 0.5)
        a1 = Arrow(call.get_right(), plt.get_left(), color=GREY_B, buff=0.1)
        a2 = Arrow(plt.get_right(), got.get_left(), color=GREY_B, buff=0.1)
        a3 = Arrow(got.get_bottom(), ld.get_right(), color=HEAD, buff=0.1)
        a4 = Arrow(ld.get_right() + DOWN * 0.15, lib.get_left() + DOWN * 0.15, color=YES, buff=0.1)
        got2 = region(3.0, 0.7, r"GOT: \ \texttt{puts} $\to$ libc", FUNC, font_size=20).move_to(got)
        a5 = CurvedArrow(got.get_bottom() + RIGHT * 0.5, lib.get_top() + RIGHT * 0.5, angle=-0.6, color=YES)
        pts = VGroup(
            label(r"a shared library loads at a different address in every process: \ its code cannot contain "
                  r"addresses", font_size=20, color=GREY_A),
            label(r"so every address it needs lives in a table of data, \ the \textit{GOT}, \ filled in at load "
                  r"time", font_size=20, color=FUNC),
            label(r"calls go through little stubs, \ the \textit{PLT}; \ the first call asks the dynamic linker, \ "
                  r"later ones jump straight there", font_size=20, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How does a call reach a library whose address is not known until the program runs? <bookmark "
            "mark='a'/> A shared library is loaded at a different address in different processes, so its code "
            "cannot contain absolute addresses. It is compiled as position-independent code: every address it needs "
            "is kept in a table of data, the global offset table, which the loader fills in. <bookmark mark='b'/> "
            "Calls into another library go through a small stub in the procedure linkage table, which jumps to "
            "whatever the table holds. <bookmark mark='c'/> On the first call the table points back into the dynamic "
            "linker, which looks the function up, writes its real address into the table, <bookmark mark='d'/> and "
            "jumps there. Every later call goes through the stub straight to the function. This is lazy binding, and "
            "it is the reason for the PLT32 relocation we saw on count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(FadeIn(got), FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(call), FadeIn(plt), GrowArrow(a1), GrowArrow(a2), FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(ld), GrowArrow(a3), FadeIn(lib), GrowArrow(a4))
            vo.wait_until("d")
            self.play(Transform(got, got2), Create(a5), FadeOut(a3), FadeOut(a4))
        self.wait(0.3)
        self.clear_scene()

    def interpose(self):
        h = load("heap")
        head = label(r"Interposition: \ replacing a library function", font_size=32).to_edge(UP, buff=0.3)
        cmd = code(["LD_PRELOAD=./mtrace.so  perl -ne '...'  1342.txt"], size=18).next_to(head, DOWN, buff=0.4)
        boxes = VGroup(region(2.6, 0.7, r"perl: \ \texttt{malloc(24)}", DATA, font_size=19),
                       region(3.0, 0.7, r"mtrace.so: \ log it, \ then", YES, font_size=19),
                       region(2.6, 0.7, r"libc's \texttt{malloc}", GREY_B, font_size=19)).arrange(RIGHT, buff=0.8)
        boxes.next_to(cmd, DOWN, buff=0.7)
        arr = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.08, color=GREY_B),
                     Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.08, color=GREY_B))
        pts = VGroup(
            label(r"the dynamic linker searches preloaded libraries first: \ our \texttt{malloc} wins", font_size=21,
                  color=GREY_A),
            label(r'ours finds the real one with \texttt{dlsym(RTLD\_NEXT, "malloc")}', font_size=21, color=FUNC),
            label(rf"that is how chapter 6 recorded {h['records']:,} events \ without touching Perl", font_size=21,
                  color=HEAD),
            label(r"also used for: \ profilers, \ leak checkers, \ sandboxes \ --- \ and malware", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Dynamic linking has a remarkable side effect: you can replace a library function without touching the "
            "program. <bookmark mark='a'/> Set LD_PRELOAD to a library of your own, and the dynamic linker searches "
            "it before the C library. <bookmark mark='b'/> So when Perl calls malloc, it reaches our malloc, which "
            "writes a record of the request and then calls the real one, found by asking for the next definition of "
            "the same name. <bookmark mark='c'/> That is how chapter six recorded almost two hundred and seventy-seven "
            "thousand events from an unmodified Perl. <bookmark mark='d'/> Profilers and memory-leak checkers use "
            "the same trick, and so, sometimes, does malware."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cmd))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), FadeIn(boxes[1]), GrowArrow(arr[1]), FadeIn(boxes[2]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
