from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono, module_box

COMPCERT = ["CompCert C", "Clight", r"C\#minor", "Cminor", "CminorSel", "RTL", "LTL", "Linear", "Mach", "Asm"]


def chip(text, color, w=None, font=19):
    t = label(text, font_size=font, color=WHITE)
    r = RoundedRectangle(width=w or t.width + 0.4, height=0.5, corner_radius=0.08, stroke_color=color,
                         stroke_width=1.8, fill_color=BG, fill_opacity=1)
    t.move_to(r)
    return VGroup(r, t)


class Verified(WatchScene):
    def construct(self):
        self.card()
        self.compcert()
        self.csmith()
        self.sel4()
        self.square()

    def card(self):
        self.chapter(11, r"Verified systems", r"Can a whole compiler, \ or a kernel, \ be proved?", lit=(2006, 2009), extra=((2006, r"Leroy: \ CompCert's back end"),
                                                     (2009, r"seL4 proved")), part=PART, said="Chapter eleven. Verified systems.")

    def compcert(self):
        head = label(r"CompCert: \ a compiler with a theorem", font_size=36).to_edge(UP, buff=0.3)
        boxes = VGroup(*[module_box(n, YES if n == "RTL" else DATA, w=1.9, h=0.55, font=18) for n in COMPCERT])
        top, bot = VGroup(*boxes[:5]).arrange(RIGHT, buff=0.55), VGroup(*boxes[5:]).arrange(LEFT, buff=0.55)
        VGroup(top, bot).arrange(DOWN, buff=0.8).next_to(head, DOWN, buff=0.45)
        bot.align_to(top, RIGHT)
        arrows = VGroup()
        for k in range(len(boxes) - 1):
            a, b = boxes[k], boxes[k + 1]
            if k == 4:
                arrows.add(Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.25))
            elif k < 4:
                arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.04, color=GREY_B, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.3))
            else:
                arrows.add(Arrow(a.get_left(), b.get_right(), buff=0.04, color=GREY_B, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.3))
        badges = VGroup(*[MathTex(r"\subseteq", font_size=24, color=YES).next_to(a, UP if k != 4 else RIGHT,
                                                                                 buff=0.04)
                          for k, a in enumerate(arrows)])
        rtl = boxes[5]
        loop = CurvedArrow(rtl.get_corner(DL) + RIGHT * 0.3, rtl.get_corner(DR) + LEFT * 0.3, angle=TAU / 3,
                           color=YES, stroke_width=2, tip_length=0.15)
        loop.next_to(rtl, DOWN, buff=0.02)
        loopl = label(r"optimizations", font_size=17, color=YES).next_to(loop, DOWN, buff=0.05)
        rows = VGroup(
            MathTex(r"\mathit{pass}(p) = \mathsf{OK}(p')", r"\;\Rightarrow\;", r"\mathit{Beh}(p')", r"\subseteq",
                    r"\mathit{Beh}(p)", font_size=30),
            MathTex(r"\mathit{Beh}(p_{10})", r"\subseteq", r"\mathit{Beh}(p_9)", r"\subseteq \cdots \subseteq",
                    r"\mathit{Beh}(p_1)", font_size=30),
            MathTex(r"\mathit{Beh}(\mathit{asm})", r"\subseteq", r"\mathit{Beh}(\mathit{source})", font_size=34,
                    color=YES),
        )
        whys = VGroup(label(r"each pass, \ proved in Coq", font_size=18, color=GREY_A),
                      label(r"chain the passes: \ inclusion is transitive", font_size=18, color=GREY_A),
                      label(r"for a source with no undefined behaviour: \ the assembly does only what the C could",
                            font_size=18, color=YES))
        col = VGroup(*[VGroup(r, w).arrange(DOWN, buff=0.1) for r, w in zip(rows, whys)]).arrange(DOWN, buff=0.28)
        col.next_to(VGroup(bot, loopl), DOWN, buff=0.3)
        with self.voiceover(
            "CompCert, from Xavier Leroy and colleagues at Inria, is a C compiler with a theorem; Leroy described its"
            " verified back end in 2006. <bookmark mark='a'/> It translates C through a chain of intermediate "
            "languages to assembly, optimizing in the middle, on a language called RTL. <bookmark mark='b'/> Each "
            "pass is written in Coq with a proof: if it produces output, every behaviour of the output is a behaviour"
            " of its input. <bookmark mark='c'/> Inclusion is transitive, so the proofs chain. <bookmark mark='d'/> "
            "For a source program with no undefined behaviour, the assembly can only do what the C could do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(boxes[k]), *([GrowArrow(arrows[k - 1])] if k else []))
                                    for k in range(len(boxes))], lag_ratio=0.3), run_time=3)
            self.play(Create(loop), FadeIn(loopl))
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            self.play(LaggedStart(*[FadeIn(b, scale=1.5) for b in badges], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(whys[1]), TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(whys[2]), TransformMatchingTex(rows[1].copy(), rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def csmith(self):
        self.ask(r"Csmith found hundreds of bugs in GCC and LLVM. \\ In CompCert's verified middle end:", [r"many",
                 r"none"], 1,
                 say="Random programs from Csmith found hundreds of bugs in GCC and LLVM. How many in CompCert's verified parts?",
                 reveal="None. The bugs it found were in unverified parts.")
        head = label(r"Csmith against CompCert", font_size=36).to_edge(UP, buff=0.3)
        gen = module_box(r"Csmith", HEAD, w=1.9, h=0.7, font=22).move_to([-5.4, 0.2, 0])
        gl = wrapped_label(r"random C programs \ with no undefined behaviour", 2.4, font_size=18,
                           color=GREY_A).next_to(gen, DOWN, buff=0.2)
        gcc = module_box(r"GCC", DATA, w=2.0, h=0.8, font=22).move_to([-0.6, 2.0, 0])
        llvm = module_box(r"LLVM", DATA, w=2.0, h=0.8, font=22).move_to([-0.6, 0.3, 0])
        outer = Circle(radius=1.15, color=GREY_B, stroke_width=2, fill_color=GREY_E, fill_opacity=0.4).move_to(
            [-0.6, -2.0, 0])
        core = Circle(radius=0.62, color=YES, stroke_width=2.5, fill_color=YES, fill_opacity=0.18).move_to(outer)
        cl = label(r"CompCert", font_size=20, color=WHITE).move_to(core)
        targets = [gcc, llvm, outer]
        feeds = VGroup(*[Arrow(gen.get_right(), t.get_left(), buff=0.1, color=GREY_C, stroke_width=1.8,
                               max_tip_length_to_length_ratio=0.06) for t in targets])

        def hits(target, n, color, ring=None):
            pts = []
            for k in range(n):
                ang = 0.6 + k * 2.1
                if ring is None:
                    p = target.get_center() + np.array([0.75 * np.cos(ang), 0.28 * np.sin(ang), 0])
                else:
                    p = target.get_center() + ring * np.array([np.cos(ang), np.sin(ang), 0])
                pts.append(Star(n=5, outer_radius=0.11, color=color, fill_opacity=1, stroke_width=0).move_to(p))
            return VGroup(*pts)
        h_gcc, h_llvm = hits(gcc, 6, NO), hits(llvm, 6, NO)
        h_cc = hits(outer, 2, NO, ring=0.9)
        notes = VGroup(
            wrapped_label(r"GCC and LLVM: \ hundreds of previously unknown bugs, \ many of them silent wrong code",
                          4.6, font_size=19, color=NO),
            wrapped_label(r"CompCert's verified middle \ (green): \ no wrong-code bugs found", 4.6, font_size=19,
                          color=YES),
            wrapped_label(r"the bugs it did find in CompCert were outside the proof, \ in parts such as the "
                          r"unverified front end \ (grey ring)", 4.6, font_size=19, color=GREY_A),
            wrapped_label(r"testing found the edge of the proof; \ chapter 14 does this to our own compiler", 4.6,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, 0.0, 0])
        cite = note(r"Yang, \ Chen, \ Eide and Regehr, \ PLDI 2011; \ stars schematic", font_size=17).to_edge(
            DOWN, buff=0.25).to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "In 2011 John Regehr's group at the University of Utah published Csmith, which generates random C "
            "programs with no undefined behaviour, and compared what compilers made of them. <bookmark mark='a'/> In "
            "GCC and LLVM it found hundreds of unknown bugs, many of them silent wrong code. <bookmark mark='b'/> In "
            "CompCert's verified middle it found no wrong-code bugs at all. <bookmark mark='c'/> The bugs it did find"
            " in CompCert were outside the proof, in parts such as the unverified front end. <bookmark mark='d'/> The"
            " proof did its job, and testing showed where the proof ended."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gen), FadeIn(gl), FadeIn(gcc), FadeIn(llvm), FadeIn(outer), FadeIn(core),
                      FadeIn(cl), FadeIn(cite))
            self.play(LaggedStart(*[GrowArrow(f) for f in feeds], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in [*h_gcc, *h_llvm]], lag_ratio=0.15),
                      FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(core, color=YES, scale_factor=1.08), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in h_cc], lag_ratio=0.4), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def sel4(self):
        head = label(r"seL4: \ a kernel with a proof", font_size=36).to_edge(UP, buff=0.3)
        layers = VGroup(module_box(r"abstract specification", YES, w=4.0, h=0.65, font=20),
                        module_box(r"executable specification", HEAD, w=4.0, h=0.65, font=20),
                        module_box(r"C implementation", DATA, w=4.0, h=0.65, font=20)).arrange(DOWN, buff=0.75)
        layers.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        refs = VGroup(*[Arrow(layers[k + 1].get_top(), layers[k].get_bottom(), buff=0.06, color=GREY_B,
                              stroke_width=2.4) for k in range(2)])
        rl = VGroup(*[label(r"refines", font_size=18, color=GREY_A).next_to(r, LEFT, buff=0.15) for r in refs])
        side = VGroup(label(r"what each system call does", font_size=17, color=GREY_A),
                      label(r"from a Haskell prototype", font_size=17, color=GREY_A),
                      label(r"what runs", font_size=17, color=GREY_A))
        for s, l in zip(side, layers):
            s.next_to(l, RIGHT, buff=0.2)
        # published sizes (Klein et al., SOSP 2009): about 8,700 lines of C, about 200,000 lines of Isabelle proof
        c_lines, proof_lines = 8_700, 200_000
        scale = 6.2 / proof_lines
        bc = Rectangle(width=c_lines * scale, height=0.45, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
        bp = Rectangle(width=proof_lines * scale, height=0.45, stroke_width=0, fill_color=YES, fill_opacity=0.85)
        VGroup(bc, bp).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.4, 1.3, 0])
        bcl = label(r"C: \ about 8,700 lines", font_size=19, color=DATA).next_to(bc, RIGHT, buff=0.2)
        bpl = label(r"Isabelle/HOL proof: \ about 200,000 lines", font_size=19, color=YES).next_to(bp, UP, buff=0.1)
        bpl.align_to(bp, LEFT)
        cite = note(r"Klein et al., \ SOSP 2009", font_size=17).next_to(bp, DOWN, buff=0.15).align_to(bp, LEFT)
        trust = wrapped_label(r"assumed in 2009: \ the C compiler, \ about 600 lines of assembly, \ the boot code, "
                              r"\ the hardware", 6.2, font_size=19, color=GREY_A).next_to(cite, DOWN, buff=0.5)
        trust.align_to(bp, LEFT)
        later = wrapped_label(r"2013: \ the compiled binary checked against the C \ (Sewell, \ Myreen and Klein): "
                              r"\ the compiler leaves the list", 6.2, font_size=19, color=YES).next_to(
            trust, DOWN, buff=0.3).align_to(trust, LEFT)
        with self.voiceover(
            "In 2009 Gerwin Klein and his colleagues at NICTA in Sydney proved the seL4 microkernel correct. "
            "<bookmark mark='a'/> An abstract specification says what each system call does. <bookmark mark='b'/> An "
            "executable specification, translated from a Haskell prototype, refines it. <bookmark mark='c'/> The C "
            "code, about eight thousand seven hundred lines, refines that, in a proof of about two hundred thousand "
            "lines of Isabelle. <bookmark mark='d'/> The 2009 proof assumed the compiler, about six hundred lines of "
            "assembly, the boot code and the hardware. <bookmark mark='e'/> In 2013 the compiled binary was checked "
            "against the C, taking the compiler off that list, by a technique chapter fourteen returns to."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(layers[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(layers[1]), FadeIn(side[1]), GrowArrow(refs[0]), FadeIn(rl[0]))
            vo.wait_until("c")
            self.play(FadeIn(layers[2]), FadeIn(side[2]), GrowArrow(refs[1]), FadeIn(rl[1]))
            self.play(GrowFromEdge(bc, LEFT), FadeIn(bcl))
            self.play(GrowFromEdge(bp, LEFT), FadeIn(bpl), FadeIn(cite), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(trust))
            vo.wait_until("e")
            self.play(FadeIn(later))
        self.wait(0.4)
        self.clear_scene()

    def square(self):
        head = label(r"Refinement: \ the simulation square", font_size=36).to_edge(UP, buff=0.3)
        s, s2 = MathTex("s", font_size=40, color=YES), MathTex("s'", font_size=40, color=YES)
        c, c2 = MathTex("c", font_size=40, color=DATA), MathTex("c'", font_size=40, color=DATA)
        s.move_to([-4.6, 1.5, 0])
        s2.move_to([-1.8, 1.5, 0])
        c.move_to([-4.6, -0.6, 0])
        c2.move_to([-1.8, -0.6, 0])
        ab = label(r"abstract", font_size=18, color=YES).next_to(s, LEFT, buff=0.3)
        co = label(r"concrete", font_size=18, color=DATA).next_to(c, LEFT, buff=0.3)
        r1 = DashedLine(s.get_bottom(), c.get_top(), buff=0.12, color=HEAD, stroke_width=2.5)
        r1l = MathTex("R", font_size=30, color=HEAD).next_to(r1, LEFT, buff=0.1)
        step_c = Arrow(c.get_right(), c2.get_left(), buff=0.12, color=DATA, stroke_width=3)
        step_s = DashedVMobject(Arrow(s.get_right(), s2.get_left(), buff=0.12, color=YES, stroke_width=3),
                                num_dashes=8)
        r2 = DashedLine(s2.get_bottom(), c2.get_top(), buff=0.12, color=HEAD, stroke_width=2.5)
        r2l = MathTex("R", font_size=30, color=HEAD).next_to(r2, RIGHT, buff=0.1)
        stut = CurvedArrow(s.get_top() + UP * 0.05 + LEFT * 0.15, s.get_top() + UP * 0.05 + RIGHT * 0.15,
                           angle=-PI * 1.3, color=LAM, stroke_width=2, tip_length=0.12)
        rows = VGroup(
            MathTex(r"R(s, c)", r"\;\wedge\;", r"c \to c'", font_size=32),
            MathTex(r"R(s, c)", r"\;\wedge\;", r"c \to c'", r"\;\Rightarrow\;", r"\exists s'.\ ", r"s \to s'",
                    r"\;\wedge\;", r"R(s', c')", font_size=32),
            MathTex(r"R(s, c)", r"\;\wedge\;", r"c \to c'", r"\;\Rightarrow\;", r"\exists s'.\ ",
                    r"(s \to s' \vee s' = s)", r"\;\wedge\;", r"R(s', c')", font_size=32),
        )
        whys = VGroup(label(r"related states; \ the code takes a step", font_size=18, color=GREY_A),
                      label(r"the specification can match it", font_size=18, color=GREY_A),
                      label(r"or stand still: \ a \textbf{stutter}, \ for internal steps", font_size=18, color=LAM))
        col = VGroup(*[VGroup(r, w).arrange(DOWN, buff=0.1, aligned_edge=LEFT) for r, w in zip(rows, whys)])
        col.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.2, 0.9, 0])
        if col.get_right()[0] > 6.85:
            col.shift(LEFT * (col.get_right()[0] - 6.85))
        # tiling: squares along a run
        y_a, y_c, x0, dx = -2.0, -3.1, -5.6, 1.5
        tile = VGroup()
        for k in range(5):
            tile.add(Dot([x0 + k * dx, y_a, 0], radius=0.06, color=YES), Dot([x0 + k * dx, y_c, 0], radius=0.06,
                                                                              color=DATA),
                     DashedLine([x0 + k * dx, y_a, 0], [x0 + k * dx, y_c, 0], color=HEAD, stroke_width=1.6))
            if k < 4:
                tile.add(Line([x0 + k * dx, y_a, 0], [x0 + (k + 1) * dx, y_a, 0], color=YES, stroke_width=2),
                         Line([x0 + k * dx, y_c, 0], [x0 + (k + 1) * dx, y_c, 0], color=DATA, stroke_width=2))
        tl = wrapped_label(r"tile the squares along any run, \ by induction: \ every safety property of the "
                           r"specification holds of the code", 5.6, font_size=19, color=YES).next_to(
            tile, RIGHT, buff=0.5)
        with self.voiceover(
            "Both proofs rest on one picture, the simulation square. <bookmark mark='a'/> Relate each concrete state "
            "to an abstract one. <bookmark mark='b'/> When the concrete machine takes a step, <bookmark mark='c'/> "
            "the abstract machine must be able to match it and keep the relation, <bookmark mark='d'/> or stand "
            "still, a stutter, when the concrete step is internal bookkeeping. <bookmark mark='e'/> Tile the squares "
            "along a run, by induction, and every concrete run is shadowed by an abstract one, so every safety "
            "property of the specification holds of the code. The next chapter checks exactly this for a protocol."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(s), FadeIn(c), FadeIn(ab), FadeIn(co), Create(r1), FadeIn(r1l))
            vo.wait_until("b")
            self.play(GrowArrow(step_c), FadeIn(c2), FadeIn(col[0]))
            vo.wait_until("c")
            self.play(Create(step_s), FadeIn(s2), Create(r2), FadeIn(r2l))
            self.play(FadeIn(whys[1]), TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("d")
            self.play(Create(stut))
            self.play(FadeIn(whys[2]), TransformMatchingTex(rows[1].copy(), rows[2]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(t) for t in tile], lag_ratio=0.05), run_time=2)
            self.play(FadeIn(tl))
        self.wait(0.4)
        self.clear_scene()




_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
