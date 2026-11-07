from __future__ import annotations

import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono


def tx(s: str) -> str:
    """One of the instrument's assertions (unicode or ASCII) as LaTeX."""
    s = s.replace("&&", "∧").replace("||", "∨").replace("==>", "⇒").replace("<=", "≤").replace(">=", "≥")
    s = s.replace("==", "=")
    s = re.sub(r"\b([A-Za-z]+)'(\d+)", r"\1'_{\2}", s)
    s = re.sub(r"\b([A-Za-z]{2,})\b", r"\\mathit{\1}", s)
    for a, b in ((">>>", r" \mathbin{>\!\!>\!\!>} "), (">>", r" \mathbin{>\!\!>} "), ("≥", r" \ge "),
                 ("≤", r" \le "), ("∧", r" \,\wedge\, "), ("∨", r" \,\vee\, "), ("¬", r" \neg "),
                 ("⇒", r" \Rightarrow "), ("≠", r" \ne "), ("*", r" \cdot ")):
        s = s.replace(a, b)
    return s


def num(v: int) -> str:
    return f"{v:,}".replace(",", "{,}")


def wrap(v: int, w: int = 16) -> int:
    v &= (1 << w) - 1
    return v - (1 << w) if v >= 1 << (w - 1) else v


def listing_lines(rows) -> list[str]:
    return ["    " * r["depth"] + r["code"] for r in rows]


SHORT = (("established", r"invariant established"), ("preserved", r"invariant preserved"),
         ("exit", r"exit gives the postcondition"), ("non-negative", r"variant $\ge 0$"),
         ("decreases", r"variant decreases"))


def short_name(name: str) -> str:
    return next(s for k, s in SHORT if k in name)


class Bsearch(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariant()
        self.skeleton()
        self.overflow()
        self.midpoints()
        self.variant()
        self.wellfounded()

    def card(self):
        card = chapter_card(3, r"Binary search, \ proved", r"Can a proof catch what years of use missed?",
                            lit=(1967, 2006), extra=((1967, r"Floyd: \ well-founded sets"),
                                                     (2006, r"Bloch: \ the midpoint overflow")), part=PART)
        with self.voiceover("Chapter three. Binary search, proved."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def invariant(self):
        head = label(r"The invariant of binary search", font_size=36).to_edge(UP, buff=0.3)
        arr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]           # illustrative
        x = 20
        n, cw, y0 = len(arr), 0.95, 0.45
        x0 = -cw * (n - 1) / 2
        cells = VGroup(*[Square(side_length=cw * 0.92, stroke_color=GREY_C, stroke_width=1.5, fill_color=GREY_E,
                                fill_opacity=0.6).move_to([x0 + j * cw, y0, 0]) for j in range(n)])
        vals = VGroup(*[label(f"{v}", font_size=22, color=WHITE).move_to(c) for v, c in zip(arr, cells)])
        idx = VGroup(*[label(f"{j}", font_size=15, color=GREY_B).next_to(c, UP, buff=0.08)
                       for j, c in enumerate(cells)])
        target = label(rf"looking for the first element $\ge {x}$", font_size=22, color=HEAD).next_to(
            head, DOWN, buff=0.3)
        # the run: lo, hi, mid at each step (the lower-bound search)
        lo, hi, steps = 0, n, []
        while lo < hi:
            mid = lo + (hi - lo) // 2
            steps.append((lo, hi, mid))
            if arr[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        steps.append((lo, hi, None))

        def ptr(name, j, col, up=False):
            xx = x0 + j * cw - (cw / 2 if not up else 0)
            if up:
                a = Arrow([xx, y0 + 1.25, 0], [xx, y0 + cw / 2 + 0.05, 0], buff=0, color=col, stroke_width=3,
                          max_tip_length_to_length_ratio=0.3)
                t = mono(name, size=18, color=col).next_to(a, UP, buff=0.05)
            else:
                a = Arrow([xx, y0 - 1.25, 0], [xx, y0 - cw / 2 - 0.05, 0], buff=0, color=col, stroke_width=3,
                          max_tip_length_to_length_ratio=0.3)
                t = mono(name, size=18, color=col).next_to(a, DOWN, buff=0.05).shift(
                    (LEFT if name == "lo" else RIGHT) * 0.25)
            return VGroup(a, t)

        def paint(lo_, hi_):
            return [c.animate.set_fill(NO if j < lo_ else (YES if j >= hi_ else GREY_E), opacity=0.45 if
                                       (j < lo_ or j >= hi_) else 0.6) for j, c in enumerate(cells)]
        p_lo, p_hi = ptr("lo", 0, DATA), ptr("hi", n, LAM)
        inv = MathTex(r"\forall j < \mathit{lo}:\ a[j] < x", r"\qquad", r"\forall j \ge \mathit{hi}:\ a[j] \ge x",
                      r"\qquad", r"0 \le \mathit{lo} \le \mathit{hi} \le n", font_size=34)
        inv[0].set_color(NO)
        inv[2].set_color(YES)
        inv[4].set_color(DATA)
        inv.move_to([0, -1.85, 0])
        inv_l = label(r"the invariant", font_size=19, color=GREY_A).next_to(inv, UP, buff=0.15)
        lo_f, hi_f, _ = steps[-1]
        done = label(rf"$\mathit{{lo}} = \mathit{{hi}} = {lo_f}$: \ nothing unknown is left, \ and the invariant "
                     rf"alone says $a[{lo_f}] = {arr[lo_f]}$ is the answer", font_size=21, color=HEAD).next_to(
            inv, DOWN, buff=0.45)
        ill = note(r"illustrative array", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Binary search is the classic test of reasoning about a loop. <bookmark mark='a'/> We look in a "
            "sorted array for the first element at least x. Two indices, low and high, bracket the answer. "
            "<bookmark mark='b'/> The invariant: everything left of low is less than x, everything from high on "
            "is at least x, and low never passes high. <bookmark mark='c'/> Each step looks at the middle and "
            "moves one end, keeping the invariant true. <bookmark mark='d'/> When low meets high nothing unknown "
            "is left, and the invariant alone says that low is the answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(vals), FadeIn(idx), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(target), FadeIn(p_lo), FadeIn(p_hi))
            vo.wait_until("b")
            self.play(FadeIn(inv_l), Write(inv))
            vo.wait_until("c")
            p_mid = None
            for lo_, hi_, mid in steps[:-1]:
                new_mid = ptr("mid", mid, HEAD, up=True)
                if p_mid is None:
                    self.play(FadeIn(new_mid), run_time=0.5)
                else:
                    self.play(Transform(p_mid, new_mid), run_time=0.5)
                p_mid = p_mid or new_mid
                nlo, nhi = (mid + 1, hi_) if arr[mid] < x else (lo_, mid)
                self.play(*paint(nlo, nhi), p_lo.animate.become(ptr("lo", nlo, DATA)),
                          p_hi.animate.become(ptr("hi", nhi, LAM)), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeOut(p_mid), FadeIn(done))
        self.wait(0.4)
        self.clear_scene()

    def skeleton(self):
        bs = load("hoare")["programs"]["binsearch"]
        head = label(r"What our checker proves", font_size=36).to_edge(UP, buff=0.3)
        loop = bs["listing"][0]
        code = code_block(listing_lines(bs["listing"]), size=20).move_to([-4.0, 0.75, 0])
        ann = MathTex(r"I:\ " + tx(loop["invariant"]), r"\qquad V:\ " + tx(loop["variant"]), font_size=28)
        ann[0].set_color(YES)
        ann[1].set_color(LAM)
        ann.next_to(code, DOWN, buff=0.35).align_to(code, LEFT)
        havoc_i = next(i for i, r in enumerate(bs["listing"]) if r["kind"] == "havoc")
        assert_i = next(i for i, r in enumerate(bs["listing"]) if r["kind"] == "assert")
        def text_of(line):          # an indented line is (anchor point, text): box the text only
            return line[-1] if isinstance(line, VGroup) and isinstance(line[0], VectorizedPoint) else line
        hb = SurroundingRectangle(text_of(code[havoc_i]), color=HEAD, buff=0.06, stroke_width=2)
        ab = SurroundingRectangle(text_of(code[assert_i]), color=NO, buff=0.06, stroke_width=2)
        notes = VGroup(
            wrapped_label(r"\texttt{c} stands for the comparison $a[\mathit{mid}] < x$: \ an unknown, \ chosen afresh "
                          r"each pass, \ so the proof covers every array and every target", 5.6, font_size=19,
                          color=HEAD),
            wrapped_label(r"the assertion is the array access: \ $a[\mathit{mid}]$ must be in range", 5.6,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ann, DOWN, buff=0.35).align_to(code, LEFT)
        rows, colors = [], []
        for v in bs["vcs"]:
            ok = v["status"] == "valid"
            rows.append([short_name(v["name"]), f"{v['clauses']:,}", f"{v['seconds']:.2f} s",
                         r"valid" if ok else r"refuted"])
            colors.append([WHITE, GREY_A, GREY_A, YES if ok else NO])
        tab = grid_table([r"verification condition", r"clauses", r"SAT time", r"result"], rows,
                         widths=[3.5, 1.2, 1.3, 1.1], row_h=0.48, font_size=19, colors=colors, mono_cols=())
        tab.move_to([3.0, 0.9, 0])
        tl = label(rf"{bs['w']}-bit integers, \ our CDCL solver \ (Part 26)", font_size=18, color=GREY_A).next_to(
            tab, UP, buff=0.25)
        caveat = wrapped_label(r"what this checks: \ every access in bounds, \ and termination; \ the search "
                               r"property itself needs reasoning about arrays, \ which this small checker does not do",
                               6.3, font_size=18, color=GREY_B).next_to(tab, DOWN, buff=0.45)
        slowest = max(bs["vcs"], key=lambda v: v["seconds"])
        with self.voiceover(
            "Our checker sees the loop's skeleton. <bookmark mark='a'/> The comparison with the array becomes an "
            "unknown c, chosen afresh on every pass, so whatever is proved holds for every array and every "
            "target. <bookmark mark='b'/> The assertion inside is the array access: the middle index must be in "
            "range. <bookmark mark='c'/> We supply the invariant, low between zero and high, and a variant, high "
            "minus low. <bookmark mark='d'/> Out come five verification conditions. Bit-blasted over sixteen-bit "
            "integers and given to our SAT solver from Part 26, all five are valid; the hardest took about one "
            "and a half seconds. The search property itself needs reasoning about arrays, which this small "
            "checker leaves out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(Create(hb), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(ab), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(ann))
            vo.wait_until("d")
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0], tab.rule)))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(caveat))
        assert abs(slowest["seconds"] - 1.5) < 0.2       # the narration says "about one and a half seconds"
        self.wait(0.4)
        self.clear_scene()

    def overflow(self):
        bad = load("hoare")["programs"]["binsearch_buggy"]
        pres = next(v for v in bad["vcs"] if "preserved" in v["name"])
        ce = pres["counterexample"]
        lo, hi = ce["lo"], ce["hi"]
        s = lo + hi
        ws = wrap(s)
        mid = ws >> 1
        head = label(r"Bloch's bug, \ found by the solver", font_size=36).to_edge(UP, buff=0.3)
        line = mono(bad["listing"][1]["code"], size=26, color=NO).next_to(head, DOWN, buff=0.4)
        lmin, lmax = -(1 << 15), (1 << 15) - 1
        W, yl = 12.0, 0.9

        def X(v):
            return -W / 2 + W * (v - lmin) / (lmax - lmin)
        nl = Line([X(lmin), yl, 0], [X(lmax), yl, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for v in (lmin, 0, lmax):
            ticks.add(Line([X(v), yl - 0.1, 0], [X(v), yl + 0.1, 0], color=GREY_C, stroke_width=2))
            ticks.add(label(f"${num(v)}$", font_size=17, color=GREY_B).next_to([X(v), yl - 0.1, 0], DOWN,
                                                                              buff=0.1))
        rng = Line([X(lo), yl, 0], [X(hi), yl, 0], color=YES, stroke_width=8)
        d_lo = VGroup(Dot([X(lo), yl, 0], color=DATA), label(rf"$\mathit{{lo}} = {num(lo)}$", font_size=19,
                                                              color=DATA).next_to([X(lo), yl, 0], UP, buff=0.18))
        d_hi = VGroup(Dot([X(hi), yl, 0], color=LAM), label(rf"$\mathit{{hi}} = {num(hi)}$", font_size=19,
                                                             color=LAM).next_to([X(hi), yl, 0], UP, buff=0.18))
        d_hi[1].shift(RIGHT * 0.35)
        d_lo[1].shift(LEFT * 0.35)
        rng_l = label(r"the range: \ $\mathit{mid}$ must land here", font_size=17, color=YES).next_to(
            rng, DOWN, buff=0.45)
        walker = Dot([X(lo), yl, 0], color=HEAD, radius=0.1)
        d_mid = VGroup(Dot([X(mid), yl, 0], color=NO, radius=0.1),
                       label(rf"$\mathit{{mid}} = {num(mid)}$", font_size=19, color=NO).next_to(
                           [X(mid), yl, 0], UP, buff=0.18))
        steps = VGroup(
            label(rf"$\mathit{{lo}} + \mathit{{hi}} = {num(s)}$, \ more than ${num(lmax)}$", font_size=22,
                  color=HEAD),
            label(rf"16 bits wrap it to ${num(s)} - {num(1 << 16)} = {num(ws)}$", font_size=22, color=HEAD),
            label(rf"${num(ws)} \gg 1 = {num(mid)} < \mathit{{lo}}$: \ the conjunct $" + tx(pres["failing"][0]) +
                  r"$ is false", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -1.35, 0])
        foot = wrapped_label(r"Joshua Bloch \ (2006): \ the same line was in Java's \texttt{Arrays.binarySearch}, "
                             r"\ and in the binary search Jon Bentley proved correct in \textit{Programming Pearls}; "
                             r"\ that proof was about mathematical integers", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now restore the textbook midpoint: add low and high, and halve. <bookmark mark='a'/> The solver no "
            "longer proves the invariant preserved. It returns a counterexample: low fifteen thousand and "
            "seventy-two, high twenty-five thousand five hundred and fifty-eight. <bookmark mark='b'/> Their sum,"
            " forty thousand six hundred and thirty, is beyond the largest sixteen-bit integer, and wraps round "
            "to minus twenty-four thousand nine hundred and six. <bookmark mark='c'/> Halved, that is minus "
            "twelve thousand four hundred and fifty-three, far below low: the array access fails. <bookmark "
            "mark='d'/> Joshua Bloch reported in 2006 that this line was in Java's library, and in the binary "
            "search Jon Bentley had proved correct in Programming Pearls. That proof was right about mathematical"
            " integers, and wrong about the machine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(line), Create(nl), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(d_lo), FadeIn(d_hi), Create(rng), FadeIn(rng_l))
            vo.wait_until("b")
            self.play(FadeIn(walker), FadeIn(steps[0]))
            self.play(walker.animate.move_to([X(lmax), yl, 0]), run_time=1.2, rate_func=linear)
            walker.move_to([X(lmin), yl, 0])
            self.play(walker.animate.move_to([X(ws), yl, 0]), FadeIn(steps[1]), run_time=1.2, rate_func=linear)
            vo.wait_until("c")
            self.play(walker.animate.move_to([X(mid), yl, 0]), run_time=0.8)
            self.play(FadeIn(d_mid), FadeOut(walker), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def midpoints(self):
        ms = load("hoare")["midpoints"]
        head = label(r"Five midpoints, \ every input", font_size=36).to_edge(UP, buff=0.3)
        rows, colors = [], []
        for m in ms:
            if m["status"] == "valid":
                res = rf"proved \ ({m['clauses']:,} clauses)"
                col = YES
            else:
                c = m["counterexample"]
                res = rf"fails at $\mathit{{lo}} = {num(c['lo'])}$, \ $\mathit{{hi}} = {num(c['hi'])}$"
                col = NO
            rows.append([m["mid"], "$" + tx(m["pre"]) + "$", res, f"{m['seconds']:.3f} s"])
            colors.append([WHITE, DATA, col, GREY_A])
        tab = grid_table([r"midpoint", r"assuming", r"over all 16-bit inputs", r"SAT time"], rows,
                         widths=[4.3, 2.6, 4.6, 1.3], row_h=0.58, font_size=20, colors=colors, mono_cols=(0,))
        tab.next_to(head, DOWN, buff=0.45)
        notes = VGroup(
            wrapped_label(r"Bloch's two fixes: \ add half the difference; \ or shift the sum without a sign, \ which "
                          r"reads the lost carry back as the top bit", 12.4, font_size=20, color=YES),
            wrapped_label(r"without $\mathit{lo} \ge 0$ the first fix fails too: \ $\mathit{hi} - \mathit{lo}$ "
                          r"itself overflows", 12.4, font_size=20, color=NO),
            wrapped_label(r"the difference shifted without a sign is right for every $\mathit{lo} < \mathit{hi}$",
                          12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The solver can judge every proposed repair. <bookmark mark='a'/> The textbook midpoint fails. "
            "Bloch's first fix, low plus half the difference, is proved for non-negative indices; his second, an "
            "unsigned shift of the sum, is proved too, because the shift reads the lost carry back as the top "
            "bit. <bookmark mark='b'/> Drop the assumption that low is non-negative, and the first fix fails as "
            "well: the difference itself overflows. <bookmark mark='c'/> Shifting the difference without a sign "
            "is right for every low below high. Each verdict took a fraction of a second."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0], tab.rule)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:4]], lag_ratio=0.4), run_time=2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[5])), FadeIn(notes[2]))
        assert max(m["seconds"] for m in ms) < 1.0        # "a fraction of a second"
        self.wait(0.4)
        self.clear_scene()

    def variant(self):
        good = load("hoare")["programs"]["binsearch"]
        bad = load("hoare")["programs"]["binsearch_buggy"]
        dec_g = next(v for v in good["vcs"] if "decreases" in v["name"])
        dec_b = next(v for v in bad["vcs"] if "decreases" in v["name"])
        head = label(r"Total correctness: \ the variant", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"\dfrac{\{I \wedge b \wedge V = v_0\}\ c\ \{I \wedge V < v_0\} \qquad I \wedge b \Rightarrow "
                       r"V \ge 0}{[\,I\,]\ \mathbf{while}\ b\ \mathbf{do}\ c\ [\,I \wedge \neg b\,]}", font_size=34)
        rule.next_to(head, DOWN, buff=0.35)
        rl = label(r"square brackets: \ the loop also terminates", font_size=18, color=GREY_A).next_to(
            rule, DOWN, buff=0.12)
        case1 = MathTex(r"\mathit{hi} - (\mathit{mid} + 1)", r"<", r"\mathit{hi} - \mathit{lo}", font_size=34)
        case2 = MathTex(r"\mathit{mid} - \mathit{lo}", r"<", r"\mathit{hi} - \mathit{lo}", font_size=34)
        w1 = label(r"$\mathit{lo} := \mathit{mid} + 1$: \ since $\mathit{mid} \ge \mathit{lo}$", font_size=19,
                   color=DATA)
        w2 = label(r"$\mathit{hi} := \mathit{mid}$: \ since $\mathit{mid} < \mathit{hi}$", font_size=19, color=LAM)
        g1 = VGroup(w1, case1).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g2 = VGroup(w2, case2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cases = VGroup(g1, g2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, -0.4, 0])
        verdict = VGroup(
            label(rf"with $\mathit{{lo}} + ((\mathit{{hi}} - \mathit{{lo}}) \gg 1)$: \ {dec_g['status']}",
                  font_size=19, color=YES),
            label(rf"with $(\mathit{{lo}} + \mathit{{hi}}) \gg 1$: \ refuted at $\mathit{{lo}} = "
                  rf"{num(dec_b['counterexample']['lo'])}$, \ $\mathit{{hi}} = {num(dec_b['counterexample']['hi'])}$",
                  font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(cases, DOWN, buff=0.4).align_to(cases, LEFT)
        # an illustrative run of the repaired loop from [0, 1000), the unknown comparison alternating
        lo, hi, gaps, k = 0, 1000, [], 0
        while lo < hi:
            gaps.append(hi - lo)
            mid = lo + ((hi - lo) >> 1)
            if k % 2 == 0:
                lo = mid + 1
            else:
                hi = mid
            k += 1
        gaps.append(hi - lo)
        bw, H = 0.42, 2.6
        bars = VGroup(*[Rectangle(width=bw * 0.8, height=max(0.03, H * g / gaps[0]), stroke_width=0,
                                  fill_color=HEAD, fill_opacity=0.85) for g in gaps])
        for i, b in enumerate(bars):
            b.move_to([1.6 + i * bw, -2.75, 0], aligned_edge=DOWN)
        bvals = VGroup(*[label(f"{g}", font_size=14, color=GREY_A).next_to(b, UP, buff=0.05)
                         for g, b in zip(gaps, bars)])
        base = Line([1.6 - bw / 2, -2.75, 0], [1.6 + (len(gaps) - 0.5) * bw, -2.75, 0], color=GREY_C)
        bcap = label(r"$\mathit{hi} - \mathit{lo}$ in a run \ (illustrative)", font_size=18, color=GREY_A).next_to(
            base, DOWN, buff=0.12)
        with self.voiceover(
            "Partial correctness says nothing if the loop runs for ever; total correctness adds termination, and "
            "the tool is a variant. <bookmark mark='a'/> Find a quantity that stays non-negative and that every "
            "pass makes strictly smaller. Here it is high minus low. <bookmark mark='b'/> Moving low to mid plus "
            "one shrinks the gap, because mid is at least low; moving high to mid shrinks it, because mid is "
            "below high. <bookmark mark='c'/> Both lean on the midpoint lying in range, and with the textbook "
            "midpoint the solver refutes this condition too. <bookmark mark='d'/> In a run the gap falls at every"
            " pass, and a natural number cannot fall for ever."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(g1))
            self.play(FadeIn(g2))
            vo.wait_until("c")
            self.play(FadeIn(verdict))
            vo.wait_until("d")
            self.play(Create(base), FadeIn(bcap))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(t)) for b, t in zip(bars, bvals)],
                                  lag_ratio=0.25), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def wellfounded(self):
        head = label(r"Well-founded orders", font_size=36).to_edge(UP, buff=0.3)
        M, N, sp = 3, 6, 0.62
        ox, oy = -6.0, -2.6

        def P(m, n):
            return np.array([ox + n * sp, oy + m * 1.2, 0])
        grid = VGroup(*[Dot(P(m, n), radius=0.05, color=GREY_D) for m in range(M + 1) for n in range(N + 1)])
        ax_m = VGroup(*[label(rf"$m = {m}$", font_size=17, color=GREY_B).next_to(P(m, 0), LEFT, buff=0.25)
                        for m in range(M + 1)])
        ax_n = label(r"$n \to$", font_size=17, color=GREY_B).next_to(P(0, N), DOWN, buff=0.3)
        # an illustrative descent in the lexicographic order: n falls; when it cannot, m falls and n jumps up
        chain = [(3, 2), (3, 1), (3, 0), (2, 5), (2, 4), (2, 3), (2, 2), (1, 6), (1, 5), (1, 4), (0, 3), (0, 2),
                 (0, 1), (0, 0)]
        assert all(a > b for a, b in zip(chain, chain[1:]))      # Python compares tuples lexicographically
        path = VGroup(*[Arrow(P(*a), P(*b), buff=0.08, stroke_width=2.5,
                              color=HEAD if a[0] == b[0] else KERN, max_tip_length_to_length_ratio=0.25)
                        for a, b in zip(chain, chain[1:])])
        pts = VGroup(*[Dot(P(*c), radius=0.08, color=WHITE) for c in chain])
        notes = VGroup(
            wrapped_label(r"\textbf{well-founded}: \ no infinite descending chain; \ the natural numbers under $<$ "
                          r"are the first example", 5.4, font_size=20, color=WHITE),
            wrapped_label(r"pairs in dictionary order: \ $(m, n) > (m', n')$ if $m > m'$, \ or $m = m'$ and "
                          r"$n > n'$; \ $n$ may jump up \ (orange) \ whenever $m$ falls", 5.4, font_size=20,
                          color=KERN),
            wrapped_label(r"Ackermann's function terminates so: \ every recursive call makes $(m, n)$ smaller in "
                          r"this order, \ though its values explode", 5.4, font_size=20, color=YES),
            wrapped_label(r"Floyd \ (1967) \ proved termination with well-founded sets", 5.4, font_size=20,
                          color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        ill = note(r"illustrative chain", font_size=16).next_to(ax_n, DOWN, buff=0.15).align_to(ax_m, LEFT)
        with self.voiceover(
            "Variants need not be numbers. <bookmark mark='a'/> A termination proof needs only an order with no "
            "infinite descending chain: a well-founded order. <bookmark mark='b'/> Pairs compared like words in a"
            " dictionary are one. The second number may jump up whenever the first goes down, so a descent can be"
            " long, but never endless. <bookmark mark='c'/> That is how one proves that Ackermann's function "
            "terminates, though its values explode: every recursive call makes its pair of arguments smaller in "
            "this order. <bookmark mark='d'/> Floyd proved termination with such sets in 1967."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(ax_m), FadeIn(ax_n), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            for a, d in zip(path, pts[1:]):
                self.play(GrowArrow(a), FadeIn(d), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, mono)
