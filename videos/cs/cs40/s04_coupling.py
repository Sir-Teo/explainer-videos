from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box)


class Coupling(VoiceoverScene):
    def construct(self):
        self.card()
        self.layers()
        self.stability()
        self.cycles()
        self.history()

    def card(self):
        card = chapter_card(3, r"Coupling, \ measured", r"How tangled is this repository?", lit=(1974, 1994),
                            extra=((1974, r"Stevens, Myers and Constantine: \ coupling and cohesion"),
                                   (1994, r"Martin: \ stability metrics")), part=PART)
        with self.voiceover("Chapter three. Coupling, measured."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def layers(self):
        r = load("repo")
        cr = r["cross"]
        head = label(r"Layers, \ and what crosses them", font_size=36).to_edge(UP, buff=0.3)
        lib = module_box(r"\texttt{explainer}: \ the library", YES, w=4.2, h=0.8, font=21).move_to([0, -1.6, 0])
        vid = module_box(r"\texttt{videos}: \ the scenes", DATA, w=4.2, h=0.8, font=21).move_to([0, 1.3, 0])
        tools = module_box(r"\texttt{tools}", HEAD, w=2.2, h=0.7, font=20).move_to([-4.6, -0.15, 0])
        tests = module_box(r"\texttt{tests}", LAM, w=2.2, h=0.7, font=20).move_to([4.6, -0.15, 0])

        def n(a, b):
            return cr.get(f"{a} -> {b}", 0)
        V, E = "videos (scenes)", "explainer (library)"
        down = Arrow(vid.get_bottom() + LEFT * 0.6, lib.get_top() + LEFT * 0.6, buff=0.08, color=GREY_B,
                     stroke_width=5)
        dl = label(f"{n(V, E):,} imports", font_size=20, color=GREY_A).next_to(down, LEFT, buff=0.15)
        up = Arrow(lib.get_top() + RIGHT * 0.6, vid.get_bottom() + RIGHT * 0.6, buff=0.08, color=NO, stroke_width=3)
        ul = label(rf"{n(E, V)} imports the wrong way", font_size=20, color=NO).next_to(up, RIGHT, buff=0.15)
        self_v = label(rf"{n(V, V):,} imports among the scenes", font_size=18, color=GREY_A).next_to(vid, UP,
                                                                                                buff=0.15)
        self_l = label(rf"{n(E, E):,} within the library", font_size=18, color=GREY_A).next_to(lib, DOWN,
                                                                                            buff=0.15)
        t1 = Arrow(tools.get_bottom(), lib.get_left() + UP * 0.1, buff=0.08, color=HEAD, stroke_width=2)
        t2 = Arrow(tests.get_bottom(), lib.get_right() + UP * 0.1, buff=0.08, color=LAM, stroke_width=2)
        bad = r["upward_edges"]
        note = wrapped_label(rf"\texttt{{{bad[0][0].replace('_', chr(92) + '_')}}} imports \texttt{{{bad[0][1]}}}: \ "
                             r"the library reaches into one video to reuse how it loads the novels", 12.0,
                             font_size=19, color=NO).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "This repository has a layered design, a rule that no file states but every file is supposed to obey. "
            "<bookmark mark='a'/> The library, explainer, holds the shared instruments: the Pebble machine, the "
            "simulators, the drawing helpers. The scenes, in videos, use the library. <bookmark mark='b'/> Over two "
            "thousand imports go downward, from scenes to library, as they should. <bookmark mark='c'/> And two go "
            "up. One library module, which loads the thirty novels, reaches into the first AI video to reuse its "
            "code. It works today; it means the library cannot be used without that video, and a change to the "
            "video can break every part that loads the novels. <bookmark mark='d'/> Tools and tests sit beside the "
            "library and depend on it too."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lib), FadeIn(vid), FadeIn(self_v), FadeIn(self_l))
            vo.wait_until("b")
            self.play(GrowArrow(down), FadeIn(dl))
            vo.wait_until("c")
            self.play(GrowArrow(up), FadeIn(ul), FadeIn(note))
            vo.wait_until("d")
            self.play(FadeIn(tools), FadeIn(tests), GrowArrow(t1), GrowArrow(t2))
        self.wait(0.4)
        self.clear_scene()

    def stability(self):
        r = load("repo")
        h = r["instability_hist"]
        head = label(r"Instability", font_size=36).to_edge(UP, buff=0.3)
        formula = MathTex(r"I = \frac{C_e}{C_a + C_e}", font_size=40, color=HEAD).move_to([3.8, 2.0, 0])
        fl = VGroup(label(r"$C_a$: \ modules that import this one \ (afferent)", font_size=19, color=GREY_A),
                    label(r"$C_e$: \ modules this one imports \ (efferent)", font_size=19, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(formula, DOWN, buff=0.25)
        top = max(h)
        bars = VGroup()
        x0, w, hmax, y0 = -6.0, 0.62, 3.6, -2.4
        for i, v in enumerate(h):
            hh = max(0.03, hmax * v / top)
            col = YES if i < 2 else (NO if i == 9 else GREY_B)
            b = Rectangle(width=w * 0.85, height=hh, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [x0 + i * w, y0 + hh / 2, 0])
            t = label(f"{v:,}", font_size=15, color=GREY_A).next_to(b, UP, buff=0.05)
            bars.add(VGroup(b, t))
        ticks = VGroup(*[label(f"{i / 10:.1f}", font_size=14, color=GREY_B).move_to([x0 + i * w, y0 - 0.22, 0])
                         for i in range(0, 10, 3)])
        xl = label(r"instability $I$ \ (modules)", font_size=17, color=GREY_A).move_to([x0 + 2.8, y0 - 0.6, 0])
        rows = [[rf"\texttt{{{t['module'].replace('_', chr(92) + '_')}}}", f"{t['ca']}", f"{t['ce']}",
                 f"{t['I']:.2f}"] for t in r["top"][:6]]
        tab = grid_table([r"most depended on", r"$C_a$", r"$C_e$", r"$I$"], rows, widths=[3.6, 0.9, 0.9, 0.9],
                         row_h=0.36, font_size=17, mono_cols=())
        tab.move_to([3.7, -1.2, 0])
        note = wrapped_label(r"\textbf{stable dependencies}: \ depend in the direction of stability; \ the "
                             r"library's core is imported by hundreds of modules and imports almost nothing", 6.4,
                             font_size=18, color=YES).next_to(tab, DOWN, buff=0.25)
        with self.voiceover(
            "Robert Martin turned coupling into numbers. <bookmark mark='a'/> For each module count the modules "
            "that depend on it, the afferent couplings, and the modules it depends on, the efferent ones. Its "
            "instability is the second count over the total. A module that everything uses and that uses nothing is "
            "stable: changing it is expensive, so it should rarely need to change. <bookmark mark='b'/> Here is the "
            "distribution over this repository. Most modules, the scenes themselves, have instability one: they use "
            "the library and nothing uses them, so they are free to change. A few hundred sit near zero. "
            "<bookmark mark='c'/> These are the most depended upon: the library's packages, imported by hundreds "
            "of modules each, and importing almost nothing. <bookmark mark='d'/> That is Martin's stable "
            "dependencies principle in practice: depend in the direction of stability, never on something likely "
            "to change more often than you."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(formula), FadeIn(fl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.1), FadeIn(ticks),
                      FadeIn(xl))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def cycles(self):
        r = load("repo")
        head = label(r"Cycles, \ and inverting a dependency", font_size=36).to_edge(UP, buff=0.3)
        cyc = VGroup(*[label(r" $\to$ ".join(rf"\texttt{{{m.split('.')[-1].replace('_', chr(92) + '_')}}}"
                                              for m in c) + r" $\to \circlearrowleft$", font_size=18,
                             color=NO if i == 0 else GREY_A) for i, c in enumerate(r["cycles"])]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14)
        ch = label(rf"{len(r['cycles'])} strongly connected components \ (Tarjan, \ Part 18)", font_size=21,
                   color=WHITE)
        left = VGroup(ch, cyc).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.2, 0.9, 0])
        hi = module_box(r"policy", DATA, w=1.8)
        lo = module_box(r"detail", NO, w=1.8)
        ab = module_box(r"interface", YES, w=2.0)
        before = VGroup(hi, lo).arrange(DOWN, buff=0.8)
        a0 = Arrow(hi.get_bottom(), lo.get_top(), buff=0.06, color=GREY_B, stroke_width=2)
        bl = label(r"before", font_size=18, color=GREY_A).next_to(before, UP, buff=0.15)
        hi2, lo2 = module_box(r"policy", DATA, w=1.8), module_box(r"detail", NO, w=1.8)
        after = VGroup(hi2, ab, lo2).arrange(DOWN, buff=0.5)
        a1 = Arrow(hi2.get_bottom(), ab.get_top(), buff=0.06, color=GREY_B, stroke_width=2)
        a2 = Arrow(lo2.get_top(), ab.get_bottom(), buff=0.06, color=YES, stroke_width=2)
        al = label(r"after", font_size=18, color=GREY_A).next_to(after, UP, buff=0.15)
        dip = VGroup(VGroup(bl, before, a0), VGroup(al, after, a1, a2)).arrange(RIGHT, buff=1.0).move_to(
            [3.9, 0.6, 0])
        foot = VGroup(
            wrapped_label(r"a cycle makes its modules one module: \ none can be tested, \ reused or understood "
                          r"alone; \ the first here ties the library's root to its own narration engine", 12.4,
                          font_size=20, color=NO),
            wrapped_label(r"\textbf{dependency inversion}: \ both sides depend on an interface the policy owns; \ "
                          r"the arrow from the detail now points up, \ and the cycle is gone", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Strongly connected components, Part 18's algorithm, find the cycles. <bookmark mark='a'/> This "
            "repository has five. Four are inside single AI videos, where a compute script and its helpers import "
            "each other. The first is in the library itself: its root package, the narration engine and the "
            "voice-over scene import each other in a ring. <bookmark mark='b'/> A cycle fuses its modules into one: "
            "none can be tested, reused or understood alone, and the order in which they load starts to matter. "
            "<bookmark mark='c'/> The standard cure is dependency inversion. When high-level policy calls a low-level "
            "detail that also needs the policy, give the policy an interface and make the detail depend on that. "
            "Both arrows now point at the abstraction, and the cycle is broken."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(dip), FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        c = load("cochange")
        h = load("history")
        head = label(r"Coupling in time", font_size=36).to_edge(UP, buff=0.3)

        def tt(p):
            return rf"\texttt{{{p.replace('_', chr(92) + '_')}}}"
        rows = [[tt(r["a"]), tt(r["b"]), f"{r['support']}", f"{max(r['conf_ab'], r['conf_ba']) * 100:.0f}\\%"]
                for r in c["pairs"][:5]]
        tab = grid_table([r"file", r"changes together with", r"commits", r"confidence"], rows,
                         widths=[4.6, 4.6, 1.5, 1.8], row_h=0.46, font_size=18, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k in range(1, 4):
            tab.cells[k][3].set_color(NO)
        lines = VGroup(
            label(rf"this repository's history: \ {h['commits']} commits, \ {c['used']} of them small enough to "
                  r"read as one change", font_size=20, color=GREY_A),
            wrapped_label(r"\textbf{logical coupling} \ (Gall, Hajek and Jazayeri, 1998): \ files that always "
                          r"change together depend on each other, \ whatever the imports say", 12.4, font_size=21,
                          color=HEAD),
            wrapped_label(r"the top three are one fact, \ the parts built so far, \ written in three files: \ every "
                          r"part must edit all three \ --- \ \textit{shotgun surgery}; \ the fix is one source of "
                          r"truth that the others are generated from", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Imports show only one kind of coupling. Version control shows another. <bookmark mark='a'/> Harald "
            "Gall and colleagues proposed in 1998 to look for files that change in the same commits. We mined this "
            "repository's history. <bookmark mark='b'/> Every commit that changed the project's instructions file "
            "also changed the series syllabus, and almost all of them the series plan. The reason is mundane: each "
            "of the three records how many parts are built. <bookmark mark='c'/> One fact stored in three places, so "
            "every new part edits all three, and forgetting one leaves them disagreeing. Refactoring books call "
            "it shotgun surgery. The cure is one source of truth from which the others are generated. Our own "
            "process has the smell this chapter teaches you to find."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0].next_to(head, DOWN, buff=0.15)))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(*[Indicate(VGroup(*tab.cells[k]), color=NO) for k in (1, 2, 3)])
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
