from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, SECTION_COLOR, YES, code, grid_table,
                                   load, region)


class Loading(VoiceoverScene):
    def construct(self):
        self.card()
        self.maps()
        self.aslr()
        self.argv()

    def card(self):
        card = chapter_card(12, r"Loading \ and the address space", r"What does a running process look like?",
                            lit=(2001,), extra=((2001, r"PaX: \ address-space randomization"),), part=PART)
        with self.voiceover("Chapter twelve. Loading and the address space."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def maps(self):
        mp = load("maps")["rows"]

        def kind(r):
            n = r["name"]
            if n == "[stack]":
                return "stack"
            if n == "[heap]":
                return "heap"
            if "libc" in n or "ld-linux" in n:
                return "libs"
            if n.startswith("["):
                return None
            if n and "x" in r["perms"]:
                return ".text"
            if n and "w" in r["perms"]:
                return ".data"
            if n:
                return "ro"
            return None

        groups = []
        for r in mp:
            k = kind(r)
            if k is None:
                continue
            if groups and groups[-1][0] == k:
                groups[-1][2] = r["hi"]
            else:
                groups.append([k, r["lo"], r["hi"]])
        names = {".text": r"the program's code \ (r-x)", ".data": r"its data \ (rw-)", "ro": r"its constants \ (r--)",
                 "heap": r"the heap \ (grows up)", "libs": r"libc and the dynamic linker", "stack": r"the stack \ "
                                                                                               r"(grows down)"}
        colors = {".text": DATA, ".data": CTRL, "ro": GREY_B, "heap": YES, "libs": FUNC, "stack": NO}
        head = label(r"A process's address space, \ read from \texttt{/proc/self/maps}", font_size=30).to_edge(UP,
                                                                                                         buff=0.3)
        strip = VGroup()
        for k, lo, hi in groups:
            strip.add(VGroup(region(4.6, 0.42, names[k], colors[k], font_size=16),
                             Text(f"{lo:#014x}", font="DejaVu Sans Mono", font_size=13, color=GREY_B)))
        for g in strip:
            g[1].next_to(g[0], LEFT, buff=0.2)
        strip = VGroup(*reversed(list(strip)))
        strip.arrange(DOWN, buff=0.12).move_to(LEFT * 1.3 + DOWN * 0.2)
        gaps = note(r"not to scale: \ the gaps are terabytes of unmapped addresses", font_size=17).next_to(
            strip, DOWN, buff=0.2)
        side = VGroup(
            label(r"each region has its own permissions:", font_size=19, color=GREY_A),
            label(r"code can run but not be written", font_size=19, color=DATA),
            label(r"data and stack can be written \\ but not run \ (chapter 14)", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover("This is a schematic built from one Linux process's proc self maps snapshot. <bookmark mark='a'/> It orders selected mappings by virtual address: executable segments, a brk heap region, libraries and stack. Large allocations can use other mappings, and the layout is neither universal nor drawn to scale. Mapping virtual space does not mean every byte occupies physical RAM. <bookmark mark='b'/> The actual snapshot records permissions per mapping. In this build the code is executable and not writable; ordinary data and stack are writable and not executable. The schematic groups library mappings for readability, although those mappings have different permissions. Part 32 connects virtual mappings to physical pages.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in reversed(list(strip))], lag_ratio=0.3), FadeIn(gaps), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    def aslr(self):
        a = load("aslr")
        head = label(r"Run it three times", font_size=34).to_edge(UP, buff=0.3)
        rows = [[n] + [r[k] for r in a["runs"]] for k, n in enumerate(a["names"])]
        t = grid_table([r"address of", r"run 1", r"run 2", r"run 3"], rows, [1.8, 3.0, 3.0, 3.0], row_h=0.5,
                       font_size=19, colors=[[GREY_A, CODE, CODE, CODE]] * len(rows), mono_cols=(1, 2, 3)).move_to(
            UP * 0.6)
        pts = VGroup(
            label("ASLR randomizes selected regions; PIE, platform and configuration determine coverage",
                  font_size=21, color=HEAD),
            label("less predictable addresses; leaks and repeated guesses can weaken protection", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.15).next_to(t, DOWN, buff=0.4)
        fixed = None
        if a["fixed"]:
            fixed = note(rf"with randomization switched off \ (\texttt{{setarch -R}}): \ the stack at "
                         rf"\texttt{{{a['fixed'][0][3]}}} every time", font_size=18).to_edge(DOWN, buff=0.35)
        else:
            fixed = note(r"setarch -R was rejected here; fixed-address comparison unavailable", font_size=18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "The compiled probe prints five kinds of address across three runs. <bookmark mark='a'/> Here the PIE "
            "program, global, heap, stack and printf addresses vary. The executable's PIE configuration matters: "
            "non-PIE text can remain fixed while other regions move. <bookmark mark='b'/> Address-space layout "
            "randomization makes useful addresses less predictable; the PaX project introduced an influential "
            "implementation in 2001. Coverage and entropy depend on platform and configuration. Leaks, limited "
            "entropy and repeated guesses can weaken it. <bookmark mark='c'/> The final panel records whether "
            "disabling randomization with setarch was permitted. This environment may reject that request. A "
            "rejected request is not evidence of a successful fixed-address comparison, and ASLR does not itself "
            "prevent an out-of-bounds write."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.3),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts))
            vo.wait_until("c")
            if fixed is not None:
                self.play(FadeIn(fixed))
        self.wait(0.3)
        self.clear_scene()

    def argv(self):
        head = label(r"How \texttt{main} gets its arguments", font_size=34).to_edge(UP, buff=0.3)
        cmd = code(["$ job pride.txt"], size=20).next_to(head, DOWN, buff=0.3)
        cells = [(r'\texttt{"pride.txt"}', YES), (r'\texttt{"job"}', YES), (r"\texttt{NULL}", GREY_B),
                 (r"\texttt{argv[1]} \ $\to$", DATA), (r"\texttt{argv[0]} \ $\to$", DATA), (r"\texttt{argc} = 2", CTRL)]
        stack = VGroup(*[region(3.2, 0.5, t, c, font_size=18) for t, c in cells]).arrange(DOWN, buff=0.04)
        stack.move_to(LEFT * 2.8 + DOWN * 0.5)
        sp = VGroup(Arrow(LEFT * 0.7, ORIGIN, color=HEAD, buff=0, stroke_width=3),
                    label(r"sp", font_size=19, color=HEAD)).arrange(LEFT, buff=0.1).next_to(stack[-1], LEFT, buff=0.1)
        top = label(r"the top of memory", font_size=16, color=GREY_B).next_to(stack, UP, buff=0.1)
        arrows = VGroup(CurvedArrow(stack[3].get_right(), stack[0].get_right(), angle=0.8, color=DATA),
                        CurvedArrow(stack[4].get_right(), stack[1].get_right(), angle=0.8, color=DATA))
        pts = VGroup(
            label("simplified argument-only initial stack; \\\\ Linux also has environment pointers and an auxiliary vector", font_size=20, color=GREY_A),
            label(r"\texttt{\_start} \ (not \texttt{main}) \ runs first: \\ it finds them and calls "
                  r"\texttt{main(argc, argv)}", font_size=20, color=FUNC),
            label("Pebble implements this argument-only layout: \\\\ \\texttt{a0} = argc, \\texttt{a1} = argv", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The initial stack is an interface between the operating system and runtime startup. <bookmark mark='a'/> Our diagram simplifies a Unix-style arrangement to argument strings, an array of pointers ending in null, and an argument count. A real Linux initial stack also includes environment pointers and an auxiliary vector, with architecture-specific alignment. <bookmark mark='b'/> The entry routine runs before main and passes the arguments according to the platform's conventions. It is runtime startup, not a universal direct loader call to main. <bookmark mark='c'/> Pebble's small loader implements the argument-only teaching layout and supplies argc and argv in a0 and a1. Its tests check the strings and pointer array; it is not a complete implementation of Linux process startup."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cmd))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in stack], lag_ratio=0.3), FadeIn(top),
                      run_time=3)
            self.play(Create(arrows), FadeIn(sp), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
