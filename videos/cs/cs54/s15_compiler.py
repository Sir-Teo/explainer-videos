from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, grid_table, load,
                                   mono, module_box, tag_box)


def kept_lines(src: str, shrunk: str) -> list[int]:
    """Indices of the original program's lines that survive in the shrunk one (it is a subsequence of them)."""
    out, j = [], 0
    sh = shrunk.splitlines()
    for i, ln in enumerate(src.splitlines()):
        if j < len(sh) and ln == sh[j]:
            out.append(i)
            j += 1
    assert j == len(sh)
    return out


def hex_row(h: str, n: int, ref: str | None = None, size=18):
    """The first n bytes of a hex string as boxes; bytes that differ from ``ref`` in red."""
    bs = [h[2 * k:2 * k + 2] for k in range(n)]
    rs = [ref[2 * k:2 * k + 2] for k in range(n)] if ref else bs
    return VGroup(*[tag_box(b, color=NO if b != r else GREY_B, size=size, w=0.62, h=0.48)
                    for b, r in zip(bs, rs)]).arrange(RIGHT, buff=0.06)


class Compiler(VoiceoverScene):
    def construct(self):
        self.card()
        self.differential()
        self.hunt()
        self.shrink()
        self.job()
        self.validation()
        self.pcc()

    def card(self):
        card = chapter_card(14, r"Fuzzing and validating our compiler",
                            r"Does our compiler mean what our programs say?", lit=(1997, 2011),
                            extra=((1997, r"Necula: \ proof-carrying code"), (2011, r"Csmith")), part=PART)
        with self.voiceover("Chapter fourteen. Fuzzing and validating our compiler."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def differential(self):
        fz = load("fuzz")["hunt"]
        head = label(r"Differential testing, \ and a planted bug", font_size=36).to_edge(UP, buff=0.3)
        gen = module_box(r"random program", HEAD, w=2.5, h=0.6, font=19).move_to([-5.3, 1.5, 0])
        gl = wrapped_label(r"always well defined: \ bounded loops, \ indices in range, \ valid pointers", 2.6,
                           font_size=17, color=GREY_A).next_to(gen, DOWN, buff=0.15)
        ref = module_box(r"IR interpreter", YES, w=2.3, h=0.5, font=18)
        lv = VGroup(*[module_box(rf"level {k}", DATA, w=2.3, h=0.5, font=18) for k in range(4)])
        runs = VGroup(ref, *lv).arrange(DOWN, buff=0.16).move_to([-1.6, 1.0, 0])
        arr = VGroup(*[Arrow(gen.get_right(), r.get_left(), buff=0.08, color=GREY_C, stroke_width=1.6,
                             max_tip_length_to_length_ratio=0.08) for r in runs])
        what = VGroup(label(r"what the program means", font_size=17, color=YES),
                      *[label(t, font_size=17, color=GREY_A) for t in (
                          r"no optimization", r"+ register allocation", r"+ SSA passes, \ including SCCP",
                          r"+ inlining first")]).arrange(DOWN, buff=0.16)
        for w, r in zip(what, runs):
            w.next_to(r, RIGHT, buff=0.25)
        bug = wrapped_label(r"\textbf{planted}: \ SCCP's constant folder divides with Python's floor \ "
                            r"(\texttt{//}, \texttt{\%}) \ instead of Pebble's truncation toward zero", 5.6,
                            font_size=19, color=NO).to_corner(DL, buff=0.5).shift(UP * 0.2)
        rows = VGroup(
            MathTex(r"a", r"=", r"q \cdot b + r", font_size=32),
            MathTex(r"-7", r"=", r"0 \cdot 256 + (-7)", font_size=32, color=YES),
            MathTex(r"-7", r"=", r"(-1) \cdot 256 + 249", font_size=32, color=NO),
        )
        whys = VGroup(label(r"both rules satisfy this", font_size=18, color=GREY_A),
                      label(r"Pebble: \ truncate, \ $q = 0$, \ $r = -7$", font_size=18, color=YES),
                      label(r"floor: \ $q = -1$, \ $r = 249$", font_size=18, color=NO))
        col = VGroup(*[VGroup(r, w).arrange(RIGHT, buff=0.4) for r, w in zip(rows, whys)])
        col.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.1, -2.1, 0])
        for r in rows:
            r.shift(RIGHT * (rows[0][1].get_x() - r[1].get_x()))
        wx = max(r.get_right()[0] for r in rows) + 0.35
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.35).set_x(wx, direction=LEFT)
        diff = label(r"they differ only when exactly one operand is negative", font_size=18, color=GREY_A).next_to(
            bug, DOWN, buff=0.2).align_to(bug, LEFT)
        assert "floor" in fz["description"]
        with self.voiceover(
            "<bookmark mark='a'/> Part 13's generator writes random Pebble programs that are always well defined, so "
            "every correct implementation prints the same bytes. <bookmark mark='b'/> Each runs on the IR "
            "interpreter, which says what it means, and compiled at all four levels on the emulator. <bookmark "
            "mark='c'/> Now plant a bug: the SCCP pass's constant folder divides by Python's rule, rounding down, not"
            " Pebble's, which truncates toward zero. <bookmark mark='d'/> Both rules satisfy a equals q b plus r. "
            "<bookmark mark='e'/> For minus seven over two hundred and fifty-six, truncation gives zero, remainder "
            "minus seven; <bookmark mark='f'/> rounding down gives minus one, remainder two hundred and forty-nine."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(gen), FadeIn(gl))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(r), FadeIn(w))
                                    for a, r, w in zip(arr, runs, what)], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(bug), Indicate(what[3], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]), FadeIn(diff))
        self.wait(0.4)
        self.clear_scene()

    def hunt(self):
        h = load("fuzz")["hunt"]
        f = h["found"]
        assert h["clean_agree"] and f["levels_disagree"] == [3]
        head = label(r"The hunt", font_size=36).to_edge(UP, buff=0.3)
        n_ok = h["programs"] - h["skipped_stuck"] - 1
        tiles = VGroup()
        kinds = [("agree", YES)] * n_ok + [("skipped", GREY_C)] * h["skipped_stuck"] + [(f"seed {f['seed']}", NO)]
        for t, c in kinds:
            tiles.add(module_box(t, c, w=1.7, h=0.6, font=18))
        tiles.arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.45)
        tl = label(rf"{h['programs']} programs, \ {h['hunt_seconds']:.1f} s: \ {n_ok} agree, \ "
                   rf"{h['skipped_stuck']} did not finish in the step limit, \ one disagrees", font_size=19,
                   color=GREY_A).next_to(tiles, DOWN, buff=0.2)
        stats = label(rf"seed {f['seed']}: \ {f['lines']} lines, \ {f['functions']} functions, \ "
                      rf"{f['output_bytes']} bytes of output", font_size=20, color=WHITE).next_to(tl, DOWN, buff=0.4)
        nb = 12
        r_ref = hex_row(f["ref"], nb)
        r_got = hex_row(f["got"], nb, f["ref"])
        rl = VGroup(label(r"interpreter, \ levels 0--2", font_size=18, color=YES),
                    label(r"level 3", font_size=18, color=NO))
        grid = VGroup(VGroup(rl[0], r_ref).arrange(RIGHT, buff=0.3), VGroup(rl[1], r_got).arrange(RIGHT, buff=0.3))
        grid.arrange(DOWN, buff=0.2, aligned_edge=RIGHT).next_to(stats, DOWN, buff=0.4)
        first = r_got[f["first_difference"]]
        fl = label(rf"first difference: \ byte {f['first_difference']} \ (counting from 0)", font_size=18,
                   color=NO).next_to(grid, DOWN, buff=0.2)
        why = wrapped_label(r"only level 3 inlines: \ inside \texttt{main}, \ a call's argument becomes a constant, "
                            r"\ and the broken folder divides it. \ With the bug removed, \ every program tried agrees "
                            r"at every level", 12.0, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Then we hunt. <bookmark mark='a'/> Program by program, the fuzzer generates and compares; one program "
            "did not finish within the step limit and was skipped. <bookmark mark='b'/> The fifth, seed four, "
            "disagrees: seventy-five lines, six functions, ninety-two bytes of output. <bookmark mark='c'/> Levels "
            "zero, one and two print what the interpreter prints; level three differs from byte one on. <bookmark "
            "mark='d'/> Level three inlines, so a call's argument becomes a constant, and the broken folder divides "
            "it. <bookmark mark='e'/> With the bug removed, every program tried agrees at every level: the fuzzer "
            "found the bug, not noise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles[:-1]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tiles[-1]), FadeIn(tl))
            self.play(FadeIn(stats))
            vo.wait_until("c")
            self.play(FadeIn(grid[0]))
            self.play(FadeIn(grid[1]))
            self.play(Indicate(first, color=NO), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(why))
            vo.wait_until("e")
            self.play(Indicate(VGroup(*tiles[:n_ok]), color=YES))
        self.wait(0.4)
        self.clear_scene()

    def shrink(self):
        fz = load("fuzz")
        f, s = fz["hunt"]["found"], fz["shrunk"]
        src = f["src"].splitlines()
        keep = set(kept_lines(f["src"], s["src"]))
        hist = s["history"]
        head = label(r"Delta debugging: \ shrink while it still fails", font_size=36).to_edge(UP, buff=0.3)
        lh = 0.066
        bars = VGroup()
        for i, ln in enumerate(src):
            w = max(0.03, 0.028 * len(ln))
            ind = 0.028 * (len(ln) - len(ln.lstrip()))
            b = Rectangle(width=w, height=lh * 0.7, stroke_width=0, fill_color=YES if i in keep else GREY_B,
                          fill_opacity=0.9 if ln.strip() else 0.0)
            b.move_to([-6.3 + ind + w / 2, 2.55 - i * lh, 0])
            bars.add(b)
        bl = label(r"the failing program, \ one bar per line", font_size=17, color=GREY_A).next_to(bars, DOWN,
                                                                                                 buff=0.15)
        bl.align_to(bars, LEFT)
        # removal order: the sweep goes bottom-up; blank lines are dropped at the very end
        order = [i for i in range(len(src) - 1, -1, -1) if i not in keep and src[i].strip()]
        order += [i for i in range(len(src)) if i not in keep and not src[i].strip()]

        def counter(k):
            return label(rf"lines: \ {hist[k]} \ \ (accepted removals: {k})", font_size=21, color=HEAD).move_to(
                [-3.0, -2.95, 0])
        cnt = counter(0)
        checkpoints = [0, 8, 16, 24, 32, 40, 48, len(hist) - 1]
        shown = []                       # one statement per line on screen: the putc line is split at its semicolons
        for ln in s["src"].splitlines():
            ind = ln[:len(ln) - len(ln.lstrip())]
            parts = [p.strip() for p in ln.strip().split(";") if p.strip()]
            shown += [ind + p + ";" for p in parts] if len(parts) > 1 else [ln]
        code = code_block(shown, size=19).move_to([2.9, 1.0, 0])
        if code.get_right()[0] > 6.85:
            code.shift(LEFT * (code.get_right()[0] - 6.85))
        hi = SurroundingRectangle(code[next(k for k, ln in enumerate(shown) if "(v / 256)" in ln)], color=NO,
                                  buff=0.06, stroke_width=2)
        stat = label(rf"{s['tests']} tests, \ {s['accepted']} accepted removals, \ {s['seconds']:.1f} s: \ "
                     rf"{s['lines_before']} lines $\to$ {s['lines']}", font_size=20, color=YES).next_to(
            code, DOWN, buff=0.4)
        expl = VGroup(
            MathTex(r"\mathit{f1}(-7, -78) = -7 + 17 / 50 = -7", font_size=28),
            MathTex(r"(-7) / 256:", r"\quad 0 \ \text{(Pebble)}", r"\quad -1 \ \text{(the broken folder)}",
                    font_size=28),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(stat, DOWN, buff=0.35)
        expl[1][1].set_color(YES)
        expl[1][2].set_color(NO)
        outs = label(rf"output: \ \texttt{{{s['ref']}}} \ against \ \texttt{{{s['got']['3']}}} \ at level 3",
                     font_size=20, color=NO).next_to(expl, DOWN, buff=0.25)
        for m in (stat, expl, outs):
            if m.get_left()[0] < -1.6:
                m.shift(RIGHT * (-1.6 - m.get_left()[0]))
        cite = note(r"Zeller and Hildebrandt \ (2002); \ hierarchical, \ after Misherghi and Su \ (2006); \ "
                    r"order of the bars schematic", font_size=17).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Delta debugging, from Andreas Zeller and Ralf Hildebrandt in 2002, shrinks a failing input while the "
            "failure persists. <bookmark mark='a'/> Ours tries removing each statement or block, from the bottom up, "
            "and keeps a removal if the program still shows the disagreement. <bookmark mark='b'/> Seventy-five "
            "tests, fifty-four accepted removals, under five seconds. <bookmark mark='c'/> Nine lines are left. "
            "<bookmark mark='d'/> f1 of minus seven returns minus seven. The second byte printed is minus seven over "
            "two hundred and fifty-six: zero for Pebble, minus one for the broken folder, so the byte is F F instead "
            "of zero zero. The bug, in one line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(bl), FadeIn(cnt), FadeIn(cite))
            vo.wait_until("a")
            removed = 0
            for a, b in zip(checkpoints, checkpoints[1:]):
                target = len(src) - hist[b]
                grp = VGroup(*[bars[i] for i in order[removed:target]])
                removed = target
                self.play(FadeOut(grp), Transform(cnt, counter(b)), run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(stat))
            vo.wait_until("c")
            rest = VGroup(*[bars[i] for i in order[removed:]])
            self.play(FadeOut(rest))
            self.play(FadeIn(code, shift=RIGHT * 0.3), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(expl[0]))
            self.play(Create(hi), FadeIn(expl[1]))
            self.play(FadeIn(outs))
        self.wait(0.4)
        self.clear_scene()

    def job(self):
        jb = load("job")
        assert jb["all_agree"]
        rows = jb["rows"]
        head = label(r"The Job, \ at every level", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"text", r"words", r"level 0", r"level 1", r"level 2", r"level 3", r"all agree"],
                         [[f"{r['bytes']} bytes", f"{r['words']}", *[f"{r['levels'][str(k)]['steps']:,}"
                                                                     for k in range(4)],
                           r"yes" if r["interp_matches_python"] and all(v["agree"] for v in r["levels"].values())
                           else r"no"] for r in rows],
                         widths=[1.6, 1.1, 1.5, 1.5, 1.5, 1.5, 1.6], row_h=0.42, font_size=19,
                         colors=[[WHITE, GREY_A, GREY_A, DATA, DATA, DATA, YES]] * len(rows), mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        tl = label(r"steps on the emulator; \ output compared with the IR interpreter and an independent Python "
                   r"version", font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.15)
        big = max(rows, key=lambda r: r["bytes"])
        steps = [big["levels"][str(k)]["steps"] for k in range(4)]
        chart = bar_chart(steps, [rf"level {k}" for k in range(4)], [GREY_B, DATA, DATA, YES], height=2.0,
                          bar_w=0.6, gap=0.45, fmt_=lambda v: f"{v:,.0f}", font_size=18).to_edge(DOWN, buff=0.45)
        chart.to_edge(LEFT, buff=1.2)
        cl = label(rf"the longest text, \ {big['bytes']} bytes", font_size=18, color=GREY_A).next_to(chart, UP,
                                                                                                  buff=0.15)
        warn = wrapped_label(rf"{jb['tapes']} inputs agreeing is \textbf{{evidence}}, \ not proof: \ another input "
                             r"might find a bug none of these did", 5.4, font_size=20, color=HEAD).next_to(
            chart, RIGHT, buff=1.0)
        with self.voiceover(
            "The real test is the Job, Part 13's word-counting program. <bookmark mark='a'/> We compile it at every "
            "level and run it on five texts, up to two hundred and twenty-six bytes. <bookmark mark='b'/> Every level"
            " prints exactly what the interpreter prints, and the interpreter agrees with an independent Python "
            "version. <bookmark mark='c'/> The optimizations pay: on the longest text, level three takes twelve "
            "thousand eight hundred and fifty-four steps, against thirty-eight thousand six hundred and thirty-three "
            "unoptimized. <bookmark mark='d'/> But five agreeing inputs are evidence, not proof."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0], tab.rule)))
            self.play(LaggedStart(*[FadeIn(VGroup(*row[:-1])) for row in tab.cells[1:]], lag_ratio=0.25),
                      FadeIn(tl), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(row[-1]) for row in tab.cells[1:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(cl), FadeIn(chart[0]),
                      LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n))
                                    for b, v, n in zip(chart.bars, chart.vals, chart.names)], lag_ratio=0.3),
                      run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    def validation(self):
        head = label(r"Translation validation", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\forall p.\ ", r"[\![ C(p) ]\!] = [\![ p ]\!]", font_size=34),
            MathTex(r"\mathit{Validate}(p, C(p)) = \mathit{yes}", r"\;\Rightarrow\;", r"[\![ C(p) ]\!] = [\![ p ]\!]",
                    font_size=34, color=YES),
        )
        whys = VGroup(label(r"prove the compiler once, \ for every program: \ CompCert's road", font_size=18,
                            color=GREY_A),
                      label(r"or check each compilation: \ only the validator need be trusted", font_size=18,
                            color=YES))
        col = VGroup(*[VGroup(r, w).arrange(DOWN, buff=0.1) for r, w in zip(rows, whys)]).arrange(DOWN, buff=0.3)
        col.next_to(head, DOWN, buff=0.35)
        passes = [r"lower", r"SSA", r"SCCP", r"GVN, \ LICM", r"registers"]
        boxes = VGroup(*[module_box(p, DATA, w=1.7, h=0.55, font=18) for p in passes]).arrange(RIGHT, buff=0.75)
        boxes.next_to(col, DOWN, buff=0.6)
        checks = VGroup(*[Circle(radius=0.17, color=GREY_B, stroke_width=2).next_to(b, RIGHT, buff=0.2)
                          for b in boxes[:-1]])
        chk = VGroup(*[MathTex(r"\checkmark", font_size=24, color=YES).move_to(c) for c in checks])
        arrs = VGroup(*[Line(boxes[k].get_right(), boxes[k + 1].get_left(), color=GREY_C, stroke_width=1.6)
                        for k in range(len(boxes) - 1)])
        claim = VGroup(MathTex(r"\text{folded: } (-7) / 256 \mapsto -1", font_size=28, color=NO),
                       MathTex(r"\text{Pebble: } \mathrm{trunc}(-7 / 256) = 0 \neq -1", font_size=28, color=NO),
                       label(r"refused", font_size=22, color=NO)).arrange(DOWN, buff=0.12)
        claim.next_to(boxes[2], DOWN, buff=0.45)
        ill = note(r"illustrative: \ a validator for constant folding \ (not run)", font_size=17).next_to(
            claim, DOWN, buff=0.15)
        stop = Cross(stroke_color=NO, stroke_width=4).scale(0.17).move_to(checks[2])
        notes = wrapped_label(r"equivalence is undecidable in general \ (Rice), \ so validators target particular "
                              r"passes and may say ``don't know''. \ CompCert's register allocation is checked this "
                              r"way, \ by a validator proved in Coq \ (Rideau and Leroy, \ 2010)", 12.6,
                              font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Translation validation, from Amir Pnueli, Michael Siegel and Eli Singerman in 1998, checks every "
            "compilation instead of sampling inputs. <bookmark mark='a'/> Proving a compiler correct for every "
            "program is CompCert's hard road. <bookmark mark='b'/> Instead, after each run, a validator checks that "
            "this output means the same as this input; only the validator must be trusted. <bookmark mark='c'/> For "
            "our bug, a validator for constant folding would recompute each folded constant by Pebble's rules: minus "
            "seven over two hundred and fifty-six is zero, not minus one, so the compilation is refused. <bookmark "
            "mark='d'/> Equivalence is undecidable in general, so validators target particular passes and may answer "
            "don't know. CompCert's register allocation is checked this way, by a validator proved in Coq."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15), Create(arrs), FadeIn(checks))
            self.play(LaggedStart(*[FadeIn(chk[k]) for k in (0, 1)], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(claim[0]), FadeIn(ill))
            self.play(FadeIn(claim[1]))
            self.play(Create(stop), FadeIn(claim[2]), checks[2].animate.set_color(NO))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def pcc(self):
        head = label(r"Proof-carrying code", font_size=36).to_edge(UP, buff=0.3)
        prod = RoundedRectangle(width=3.4, height=3.6, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2,
                                fill_color=GREY_E, fill_opacity=0.3).move_to([-4.9, 0.2, 0])
        pl = label(r"producer \ (untrusted)", font_size=20, color=GREY_A).next_to(prod.get_top(), DOWN, buff=0.2)
        comp = module_box(r"compiler", DATA, w=2.4, h=0.55, font=18)
        prover = module_box(r"prover", LAM, w=2.4, h=0.55, font=18)
        VGroup(comp, prover).arrange(DOWN, buff=0.5).move_to(prod).shift(DOWN * 0.2)
        cons = RoundedRectangle(width=4.6, height=3.6, corner_radius=0.15, stroke_color=KERN, stroke_width=2,
                                fill_color=KERN, fill_opacity=0.08).move_to([4.2, 0.2, 0])
        cl = label(r"consumer \ (the kernel)", font_size=20, color=KERN).next_to(cons.get_top(), DOWN, buff=0.2)
        vcg = module_box(r"VC generator \ (wp, \ ch. 4)", HEAD, w=3.6, h=0.55, font=18)
        chk = module_box(r"proof checker \ (ch. 10)", KERN, w=3.6, h=0.55, font=18)
        run = module_box(r"run, \ no run-time checks", YES, w=3.6, h=0.55, font=18)
        VGroup(vcg, chk, run).arrange(DOWN, buff=0.35).move_to(cons).shift(DOWN * 0.25)
        pkg_code = tag_box("code", color=DATA, size=18, w=1.2, h=0.5)
        pkg_proof = tag_box("proof", color=LAM, size=18, w=1.2, h=0.5)
        pkg = VGroup(pkg_code, pkg_proof).arrange(DOWN, buff=0.08).move_to([-0.5, 0.2, 0])
        a1 = Arrow(prod.get_right(), pkg.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        a2 = Arrow(pkg.get_right(), cons.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        i1 = Arrow(vcg.get_bottom(), chk.get_top(), buff=0.04, color=GREY_B, stroke_width=2,
                   max_tip_length_to_length_ratio=0.3)
        i2 = Arrow(chk.get_bottom(), run.get_top(), buff=0.04, color=GREY_B, stroke_width=2,
                   max_tip_length_to_length_ratio=0.3)
        tam = wrapped_label(r"tamper with the code, \ and its condition changes: \ the old proof no longer fits", 9.0,
                            font_size=19, color=NO).move_to([0, -2.3, 0])
        heirs = wrapped_label(r"descendants: \ typed assembly language \ (Morrisett et al., \ 1998); \ WebAssembly's "
                              r"validator \ (Part 15); \ the eBPF verifier \ (Part 31), \ which checks the code itself "
                              r"instead of a shipped proof", 12.6, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now let the code carry its own proof. <bookmark mark='a'/> In George Necula's proof-carrying code, from "
            "1997, an untrusted producer ships machine code with a proof that it obeys a safety policy. <bookmark "
            "mark='b'/> The consumer computes the verification condition from the code, by weakest preconditions as "
            "in chapter four, <bookmark mark='c'/> and checks the proof with a small checker, as in chapter ten; then"
            " the code runs with no run-time checks. <bookmark mark='d'/> Tamper with the code and its condition "
            "changes, so the proof no longer fits. <bookmark mark='e'/> Descendants include typed assembly language, "
            "WebAssembly's validator from Part 15, and Part 31's eBPF verifier, which checks the code itself instead "
            "of a shipped proof."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(prod), FadeIn(pl), FadeIn(comp), FadeIn(prover))
            self.play(GrowArrow(a1), FadeIn(pkg))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(cons), FadeIn(cl), FadeIn(vcg))
            vo.wait_until("c")
            self.play(GrowArrow(i1), FadeIn(chk))
            self.play(GrowArrow(i2), FadeIn(run))
            vo.wait_until("d")
            self.play(pkg_code[0].animate.set_stroke(NO), pkg_code[1].animate.set_color(NO), FadeIn(tam))
            self.play(Indicate(chk, color=NO))
            vo.wait_until("e")
            self.play(FadeIn(heirs))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, mono)
