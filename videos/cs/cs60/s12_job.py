from __future__ import annotations

import math
import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, LogPlot, grid_table, load,
                                   module_box, mono)

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()

STAGES = [("classify", DATA), ("hash", LAM), ("emit", HEAD), ("count", YES)]
SLOW, FAST = 16, 48            # trace cycles shown slowly, then quickly


def say_int(n: int) -> str:
    """An integer below a million as a speaker says it (British: 'one hundred and five')."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return _ONES[n // 100] + " hundred" + ("" if rest == 0 else " and " + say_int(rest))
    rest = n % 1000
    return say_int(n // 1000) + " thousand" + ("" if rest == 0 else (" and " if rest < 100 else " ") + say_int(rest))


def cm(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def lines(texts, color, size=17):
    return VGroup(*[mono(t, size=size, color=color) for t in texts]).arrange(DOWN, buff=0.1)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.clock()
        self.trace()
        self.verify()
        self.tablesize()
        self.lanes()
        self.ledger()

    def card(self):
        card = chapter_card(11, r"The Job in hardware", r"What if the Job were a circuit?", lit=(1978, 2014),
                            extra=((1978, r"Kung and Leiserson: \ systolic arrays"),
                                   (2014, r"Putnam et al.: \ search ranking on FPGAs")), part=PART)
        with self.voiceover("Chapter eleven. The Job in hardware."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _stages(self, w=2.45, h=1.25, gap=0.6, y=1.0):
        boxes = VGroup(*[RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=c, stroke_width=2.4,
                                          fill_color=c, fill_opacity=0.08) for _, c in STAGES]).arrange(RIGHT, buff=gap)
        boxes.move_to([0.45, y, 0])
        regs = VGroup(*[Rectangle(width=0.14, height=h * 0.8, stroke_color=KERN, stroke_width=1.5, fill_color=KERN,
                                  fill_opacity=0.5).move_to((a.get_right() + b.get_left()) / 2)
                        for a, b in zip(boxes, boxes[1:])])
        wires = VGroup(*[Line(a.get_right(), b.get_left(), color=GREY_B, stroke_width=2)
                         for a, b in zip(boxes, boxes[1:])])
        inp = Arrow(boxes[0].get_left() + LEFT * 1.0, boxes[0].get_left(), buff=0, color=DATA, stroke_width=3,
                    max_tip_length_to_length_ratio=0.2)
        il = label(r"one byte \\ per cycle", font_size=17, color=DATA).next_to(inp, UP, buff=0.1)
        names = VGroup(*[label(rf"{k + 1}.\ {n}", font_size=21, color=c).next_to(boxes[k], UP, buff=0.12)
                         for k, (n, c) in enumerate(STAGES)])
        return boxes, regs, wires, inp, il, names

    def pipeline(self):
        tm = load("accel")["timing"]
        st = tm["stages"]
        head = label(r"The word-counting unit: \ four stages", font_size=36).to_edge(UP, buff=0.3)
        boxes, regs, wires, inp, il, names = self._stages(h=1.45, y=1.25)
        does = [r"a letter? \\ its 5-bit code", r"$h \leftarrow 33h + c$ \\ two adders",
                r"word ended: \\ index $+$ tag", r"read, \ compare, \\ add one, \ write"]
        body = VGroup(*[label(d, font_size=18, color=WHITE) for d in does])
        stats = VGroup(*[label(rf"{cm(st[n]['gates'])} gates, \ depth {st[n]['depth']}", font_size=17, color=c)
                         for n, c in STAGES])
        for b_, s_, bx in zip(body, stats, boxes):
            VGroup(b_, s_).arrange(DOWN, buff=0.14).move_to(bx)
        entries, bits = tm["table_entries"], tm["table_bits"]
        table = module_box(rf"table: \ {cm(entries)} entries \ $\times$ {bits // entries} bits", KERN, w=3.4, h=0.6,
                           font=18).next_to(boxes[3], DOWN, buff=0.55).align_to(boxes[3], RIGHT)
        tl = VectorizedPoint(table.get_top())
        tl2 = DoubleArrow(table.get_top(), [table.get_x(), boxes[3].get_bottom()[1], 0], buff=0,
                          color=KERN, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        regl = label(r"registers between stages: \ each stage holds a different byte", font_size=18, color=KERN)
        regl.next_to(boxes, DOWN, buff=0.45).align_to(boxes[0], LEFT)
        totals = VGroup(
            label(rf"{cm(tm['gates'])} gates \ $+$ {tm['flip_flops']} flip-flops", font_size=24, color=HEAD),
            label(r"the same four stages, \ a $2^{20}$-entry table, \ for the thirty novels", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(regl, DOWN, buff=0.45).align_to(boxes[0], LEFT)
        src = note(r"built from Part 3's gates, \ Part 4's adders and Part 5's registers; \ simulated gate by gate",
                   font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here is the Job as a circuit, taking one byte on every clock tick. <bookmark mark='a'/> Stage one "
            "asks whether the byte is a letter, and gives its five-bit code. <bookmark mark='b'/> Stage two keeps"
            " a rolling hash of the word: thirty-three times the hash, plus the code, in two of Part 4's adders. "
            "<bookmark mark='c'/> When a word ends, stage three folds the hash into a twelve-bit index and keeps "
            "all of it as a tag. <bookmark mark='d'/> Stage four reads that entry of a table, compares the tags, "
            "adds one and writes it back. <bookmark mark='e'/> Registers between the stages let all four work at "
            "once, each on a different byte, like Part 7's pipeline. <bookmark mark='f'/> In all, "
            f"{say_int(tm['gates'])} gates and {say_int(tm['flip_flops'])} flip-flops, beside the table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), GrowArrow(inp), FadeIn(il))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                anims = [FadeIn(boxes[k]), FadeIn(names[k]), FadeIn(body[k]), FadeIn(stats[k])]
                if k:
                    anims.append(Create(wires[k - 1]))
                if k == 3:
                    anims += [FadeIn(table), Create(tl), GrowFromCenter(tl2)]
                self.play(*anims)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r, scale=1.3) for r in regs], lag_ratio=0.3), FadeIn(regl))
            vo.wait_until("f")
            self.play(FadeIn(totals))
        self.wait(0.4)
        self.clear_scene()

    def clock(self):
        tm = load("accel")["timing"]
        st = tm["stages"]
        gps, ffps, mem = tm["gate_ps"], tm["ff_ps"], tm["mem_ps"]
        head = label(r"The clock: \ the slowest stage", font_size=36).to_edge(UP, buff=0.3)
        sc = 5.6 / 1300.0
        x0 = -3.6
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (n, c) in enumerate(STAGES):
            y = 2.2 - 0.7 * k
            logic = st[n]["depth"] * gps
            b = VGroup(Rectangle(width=max(logic * sc, 0.03), height=0.45, stroke_width=0, fill_color=c,
                                 fill_opacity=0.85).move_to([x0 + logic * sc / 2, y, 0]))
            if st[n]["mem_ps"]:
                m = st[n]["mem_ps"]
                b.add(Rectangle(width=m * sc, height=0.45, stroke_width=0, fill_color=NO, fill_opacity=0.85)
                      .move_to([x0 + logic * sc + m * sc / 2, y, 0]))
                b.add(label(r"table read", font_size=18, color=BLACK).move_to(b[1]))
            bars.add(b)
            names.add(label(rf"{n}: \ {st[n]['depth']} gate{'' if st[n]['depth'] == 1 else 's'} deep", font_size=19, color=c).next_to([x0, y, 0], LEFT,
                                                                                                 buff=0.2))
            vals.add(label(rf"{st[n]['ps']:.0f} ps", font_size=19, color=c).next_to(b, RIGHT, buff=0.12))
        per = tm["period_ps"]
        line = DashedLine([x0 + per * sc, 2.6, 0], [x0 + per * sc, -0.3, 0], color=HEAD, stroke_width=2.5)
        vals[3].next_to(line, RIGHT, buff=0.15).set_y(bars[3].get_y())
        ll = label(rf"period {per:.0f} ps", font_size=19, color=HEAD).next_to(line, DOWN, buff=0.1)
        cr = tm["critical_stage"]
        rows = VGroup(
            MathTex(r"T", r"=", r"t_{\text{table}}", r"+", r"d_{\text{%s}} \cdot t_{\text{gate}}" % cr, r"+",
                    r"t_{\text{reg}}", font_size=34),
            MathTex(r"T", r"=", rf"{mem:.0f}", r"+", rf"{st[cr]['depth']} \cdot {gps:.0f}", r"+", rf"{ffps:.0f}",
                    r"=", rf"{per:.0f}\ \text{{ps}}", font_size=34),
            MathTex(r"f", r"=", r"\frac{1}{T}", r"\approx", rf"{tm['clock_mhz']:.0f}\ \text{{MHz}}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.6).set_y(-2.15)
        rows[2][-1].set_color(HEAD)
        logic = wrapped_label(rf"logic alone: \ {tm['max_logic_depth']} gates $\cdot$ {gps:.0f} $+$ {ffps:.0f} "
                              rf"$=$ {tm['logic_only_period_ps']:.0f} ps, \ or {tm['logic_only_mhz'] / 1000:.1f} GHz",
                              4.6, font_size=19, color=GREY_A)
        crit = label(r"the critical path is the table read", font_size=22, color=NO)
        VGroup(crit, logic).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rows, RIGHT, buff=0.6)
        src = note(r"the series' timing model: \ 10 ps a gate, \ 70 ps a register, \ 1 ns a memory read",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            f"How fast can it tick? <bookmark mark='a'/> Classifying takes {say_int(st['classify']['depth'])} gate"
            f" delays, hashing {say_int(st['hash']['depth'])}, emitting {say_int(st['emit']['depth'])}, and "
            f"counting {say_int(st['count']['depth'])}. <bookmark mark='b'/> But counting must also read the "
            "table, and a memory read takes a nanosecond, more than all the logic together. <bookmark mark='c'/> "
            "So the period is the table read, plus nineteen gate delays, plus the register: twelve hundred and "
            f"sixty picoseconds, about {say_int(round(tm['clock_mhz']))} megahertz. <bookmark mark='d'/> The "
            "critical path is the table read. The logic alone could run at three gigahertz: the bill, again, is "
            "for memory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(names))
            vo.wait_until("a")
            for k in range(4):
                self.play(GrowFromEdge(bars[k][0], LEFT), FadeIn(vals[k]) if k < 3 else Wait(0.01), run_time=0.6)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[3][1], LEFT), FadeIn(bars[3][2]), FadeIn(vals[3]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(line), FadeIn(ll))
            self.play(Write(rows[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(crit), Indicate(bars[3][1], color=NO))
            self.play(FadeIn(logic))
        self.wait(0.4)
        self.clear_scene()

    def trace(self):
        a = load("accel")
        tr = a["run"]["trace"][:FAST]
        text = a["text"][:FAST + 1]
        words = re.findall(r"[a-z]+", a["text"].lower())
        head = label(r"Bytes through the pipeline, \ cycle by cycle", font_size=36).to_edge(UP, buff=0.3)
        chars = mono(text[:FAST].replace(" ", "\u00b7"), size=22, color=WHITE).move_to([0.2, 2.45, 0])
        for k, ch in enumerate(text[:FAST]):
            if ch == " ":
                chars[k].set_color(GREY_D)
        y_ptr = chars.get_top()[1] + 0.12

        def ptr_at(k):
            return [chars[k].get_x(), y_ptr, 0]
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.07).rotate(PI).move_to(ptr_at(0))
        boxes, regs, wires, inp, il, names = self._stages(w=2.55, h=1.3, gap=0.55, y=0.55)
        il.become(label(r"byte in", font_size=17, color=DATA).next_to(inp, UP, buff=0.1))
        clock = label(r"cycle 0", font_size=26, color=HEAD).move_to([-5.6, -0.4, 0])
        ill = note(r"lane 0 of the run on chapter 1 of \emph{Pride and Prejudice}; \ the netlist's registers, "
                   r"recorded", font_size=16).to_edge(DOWN, buff=0.15)

        def show(t):
            r = tr[t]
            prev = text[t - 1] if t > 0 else " "
            s1 = [f"'{prev}' -> {r['s1_code']}" if r["s1_letter"] else (f"'{prev}': separator" if t else "-")]
            s2 = [f"h = {r['h']}"] + (["word ended"] if r["s2_end"] else [""])
            s3 = [f"index {r['s3_index']}", f"tag {r['s3_tag']}"] if r["s3_emit"] else ["-", ""]
            s4 = [f"slot {r['s3_index']}", f"<- count {r['wd_count']}"] if r["we"] else (
                ["lost"] if r["miss"] else ["-"])
            out = VGroup()
            for b, ls, (_, c) in zip(boxes, (s1, s2, s3, s4), STAGES):
                out.add(lines([x if x else " " for x in ls], c if any(x not in ("-", "") for x in ls) else GREY_D)
                        .move_to(b))
            return out
        state = show(0)
        hdr = ["slot", "tag (the word's hash)", "word", "count"]
        tab_rows = []
        emits = [t for t in range(FAST) if tr[t]["we"]]
        for k, t in enumerate(emits):
            tab_rows.append([f"{tr[t]['s3_index']}", f"{tr[t]['s3_tag']}", words[k], f"{tr[t]['wd_count']}"])
        tab = grid_table(hdr, tab_rows, widths=[1.2, 3.0, 2.4, 1.1], row_h=0.36, font_size=19, mono_cols=(0, 1, 2, 3))
        tab.move_to([1.9, -2.1, 0])
        tt = label(r"the table, \ as written", font_size=19, color=KERN).to_edge(LEFT, buff=0.7).align_to(tab, UP)
        tt.shift(DOWN * 0.15)
        wn = label(r"(names attached afterwards: \\ the hardware holds \\ only hashes)", font_size=16,
                   color=GREY_B)
        wn.next_to(tt, DOWN, buff=0.15).align_to(tt, LEFT)
        with self.voiceover(
            "Now feed it the opening of Pride and Prejudice. <bookmark mark='a'/> The I of It enters, and a cycle"
            " later stage one holds its code, nine. <bookmark mark='b'/> The hash grows by a letter every cycle. "
            "<bookmark mark='c'/> The space ends the word; its hash moves to stage three and becomes an index and"
            " a tag, <bookmark mark='d'/> and at cycle five stage four writes a count of one into that slot. "
            "<bookmark mark='e'/> Meanwhile the next word is already being hashed. <bookmark mark='f'/> Faster "
            "now: truth, universally, acknowledged, each counted four cycles after its last letter, a byte every "
            "cycle, never stalling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chars), FadeIn(ptr), FadeIn(boxes), FadeIn(names), FadeIn(regs),
                      Create(wires), GrowArrow(inp), FadeIn(il), FadeIn(clock), FadeIn(state), FadeIn(ill),
                      FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(tt), FadeIn(wn))
            vo.wait_until("a")
            shown = 0
            marks = {1: "b", 3: "c", 5: "d", 7: "e", SLOW: "f"}
            for t in range(1, FAST):
                if t in marks:
                    vo.wait_until(marks[t])
                rt = 0.75 if t < SLOW else 0.32
                new = show(t)
                anims = [Transform(state, new), ptr.animate.move_to(ptr_at(t)),
                         chars[t - 1].animate.set_opacity(0.35),
                         Transform(clock, label(rf"cycle {t}", font_size=26, color=HEAD).move_to(clock))]
                if tr[t]["we"]:
                    anims.append(FadeIn(VGroup(*tab.cells[shown + 1]), shift=UP * 0.1))
                    anims.append(Indicate(boxes[3], color=YES, scale_factor=1.03))
                    shown += 1
                self.play(*anims, run_time=rt)
        self.wait(0.4)
        self.clear_scene()

    def verify(self):
        r = load("accel")["run"]
        head = label(r"Checked against the software Job", font_size=36).to_edge(UP, buff=0.3)
        top = [x.split() for x in r["top"].strip().splitlines()][:10]
        tl = VGroup(*[mono(f"{w:<6}{n:>3}", size=19, color=WHITE) for w, n in top]).arrange(DOWN, buff=0.1,
                                                                                         aligned_edge=LEFT)
        tl.to_edge(LEFT, buff=1.1).shift(DOWN * 0.35)
        tt = label(r"the unit's top ten \ (of twenty)", font_size=19, color=GREY_A).next_to(tl, UP, buff=0.25)
        tl_f = SurroundingRectangle(tl, color=GREY_C, buff=0.2, corner_radius=0.1)

        def check(ok, text, col=WHITE):
            mark = label(r"\checkmark" if ok else r"$\times$", font_size=26, color=YES if ok else NO)
            return VGroup(mark, label(text, font_size=21, color=col)).arrange(RIGHT, buff=0.2)
        checks = VGroup(
            label(rf"chapter 1, \ {cm(r['bytes'])} bytes, \ {r['lanes']} lanes of the unit, \ {r['cycles']} cycles, "
                  r"\ at gate level", font_size=21, color=GREY_A),
            check(r["hashes_match"], r"every hash leaving stage 3 equals the software's"),
            check(r["tables_match_model"], r"every lane's table equals the model's"),
            check(r["top_exact"], r"the top twenty is the software Job's, \ exactly"),
            check(r["accounted"], rf"{cm(r['counted_occurrences'])} counted $+$ {r['lost_occurrences']} lost "
                                  rf"$=$ {cm(r['words'])} words"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(tl_f, RIGHT, buff=0.8).shift(UP * 0.4)
        lost = wrapped_label(rf"but {r['inexact_words']} of {r['distinct']} distinct words were short: \ a word "
                             r"whose index another word already owns is not stored", 6.6, font_size=20, color=NO)
        lost.next_to(checks, DOWN, buff=0.45).align_to(checks, LEFT)
        lanes = label(r"lost per lane: \ " + r", \ ".join(str(x) for x in r["overflow_per_lane"]), font_size=19,
                      color=GREY_A).next_to(lost, DOWN, buff=0.2).align_to(checks, LEFT)
        with self.voiceover(
            "Is it right? <bookmark mark='a'/> We ran all of chapter one through eight copies of the unit, gate "
            "by gate, and compared everything with the software. <bookmark mark='b'/> Every hash leaving stage "
            "three was the software's. <bookmark mark='c'/> Every table held exactly what a model of the table "
            "says it should. <bookmark mark='d'/> The top twenty is the software Job's, word for word. "
            f"<bookmark mark='e'/> And every word is counted or lost. {say_int(r['inexact_words']).capitalize()} "
            "words came up short: each table has one slot per index and never looks elsewhere, so a word whose "
            "slot is taken is not stored, and the overflow register says so."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(checks[0]), Create(tl_f), FadeIn(tt), LaggedStart(*[FadeIn(x) for x in tl],
                                                                                 lag_ratio=0.1), run_time=1.5)
            for k, m in zip(range(1, 5), "bcde"):
                vo.wait_until(m)
                self.play(FadeIn(checks[k], shift=RIGHT * 0.2))
            self.play(FadeIn(lost))
            self.play(FadeIn(lanes))
        self.wait(0.4)
        self.clear_scene()

    def tablesize(self):
        rows = load("sweep")["rows"]
        head = label(r"How big a table?", font_size=36).to_edge(UP, buff=0.3)
        plot = LogPlot(1, 5, 2, 7, r"table size \ (KB, \ log scale)", r"words \ (log scale)", x_length=5.6,
                       y_length=4.0)
        plot.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        n = rows[0]["distinct"]

        def pred(m):
            return n - m * (1 - math.exp(-n / m))
        lost = VGroup(*[Dot(plot.c2p(math.log10(r["kbytes"]), math.log10(r["lost_occurrences"])), radius=0.08,
                            color=NO) for r in rows])
        inex = VGroup(*[Dot(plot.c2p(math.log10(r["kbytes"]), math.log10(r["inexact_words"])), radius=0.08,
                            color=LAM) for r in rows])
        lost_l = VMobject(color=NO, stroke_width=2.5).set_points_as_corners([d.get_center() for d in lost])
        inex_l = VMobject(color=LAM, stroke_width=2.5).set_points_as_corners([d.get_center() for d in inex])
        kpb = rows[0]["kbytes"] / rows[0]["entries"]
        ks = [rows[0]["index_bits"] + 0.25 * i for i in range(4 * (rows[-1]["index_bits"] - rows[0]["index_bits"]) + 1)]
        curve = DashedVMobject(VMobject(color=GREY_A, stroke_width=2.5).set_points_smoothly(
            [plot.c2p(math.log10((2 ** k) * kpb), math.log10(pred(2 ** k))) for k in ks]), num_dashes=40)
        keys = VGroup(label(r"occurrences lost", font_size=18, color=NO),
                      label(r"distinct words not counted exactly", font_size=18, color=LAM),
                      label(r"predicted, \ from $n$ and $m$ alone", font_size=18, color=GREY_A),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(plot.ax, UP, buff=0.05).align_to(
            plot.ax, RIGHT).shift(DOWN * 0.15)
        eqs = VGroup(
            MathTex(r"P(\text{slot empty})", r"=", r"\left(1 - \tfrac1m\right)^n", r"\approx", r"e^{-n/m}",
                    font_size=30),
            MathTex(r"\text{occupied}", r"\approx", r"m\,\bigl(1 - e^{-n/m}\bigr)", font_size=30),
            MathTex(r"\text{not exact}", r"=", r"n", r"-", r"\text{occupied}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 1.45)
        nm = label(rf"$n = {cm(n)}$ distinct words, \ $m$ slots", font_size=18, color=GREY_B).next_to(eqs, UP,
                                                                                                    buff=0.2).align_to(
            eqs, LEFT)
        pick = [r for r in rows if r["index_bits"] in (16, 20, 22)]
        tab = grid_table([r"$m$", r"measured", r"predicted"],
                         [[rf"$2^{{{r['index_bits']}}}$", cm(r["inexact_words"]), cm(round(pred(r["entries"])))]
                          for r in pick], widths=[1.1, 1.6, 1.6], row_h=0.4, font_size=19, mono_cols=())
        tab.next_to(eqs, DOWN, buff=0.35).align_to(eqs, LEFT)
        r20 = next(r for r in rows if r["index_bits"] == 20)
        top_from = min(r["entries"] for r in rows if r["top_exact"])
        verdict = wrapped_label(rf"at $2^{{20}}$ entries \ ({r20['kbytes'] / 1024:.1f} MiB): \ "
                                rf"{cm(r20['lost_occurrences'])} of {cm(r20['words'])} occurrences lost "
                                rf"\ ({100 * r20['lost_occurrences'] / r20['words']:.1f}\%); \ the top twenty is "
                                rf"exact from {cm(top_from)} entries up", 5.0, font_size=18, color=HEAD)
        verdict.next_to(tab, DOWN, buff=0.3).align_to(eqs, LEFT)
        src = note(r"one lane, \ the thirty novels, \ the unit's functional model \ (checked against its netlist)",
                   font_size=16).to_edge(DOWN, buff=0.15)
        pct = 100 * r20["lost_occurrences"] / r20["words"]
        with self.voiceover(
            "How big must the table be? For the thirty novels we swept it from four thousand entries to four "
            "million. <bookmark mark='a'/> Lost occurrences fall from over a million to under three thousand, "
            "<bookmark mark='b'/> and the words not counted exactly fall with them. <bookmark mark='c'/> Part "
            "17's birthday argument predicts that curve from two numbers: with n words in m slots, a slot stays "
            "empty with probability about e to the minus n over m, <bookmark mark='d'/> and every word beyond the"
            " occupied slots is short. <bookmark mark='e'/> The prediction lands within a few percent. At a "
            f"million entries, seven megabytes, the unit loses {say_dec(pct)} percent of occurrences, and the top "
            "twenty is exact. A direct-mapped table loses words; Part 17's probing would not, at the cost of "
            "cycles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in lost], lag_ratio=0.15), Create(lost_l),
                      FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in inex], lag_ratio=0.15), Create(inex_l),
                      FadeIn(keys[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(nm), Write(eqs[0]))
            self.play(FadeIn(eqs[1], shift=DOWN * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(eqs[2], shift=DOWN * 0.2))
            self.play(Create(curve), FadeIn(keys[2]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*[c for row in tab.cells for c in row])), FadeIn(tab.rule))
            self.play(FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    def lanes(self):
        j = load("job")["job"]
        m = load("roofline")["machine"]
        L = j["lanes"]
        head = label(r"More lanes", font_size=36).to_edge(UP, buff=0.3)
        f = j["clock_mhz"] * 1e6
        sc = 7.0 / (1000 * L[0]["seconds"])
        x0 = -3.2
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, r in enumerate(L):
            y = 1.9 - 0.85 * k
            ws = 1000 * r["stream_cycles"] / f * sc
            wm = 1000 * r["merge_cycles"] / f * sc
            b = VGroup(Rectangle(width=max(ws, 0.03), height=0.5, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
                       .move_to([x0 + ws / 2, y, 0]))
            if wm:
                b.add(Rectangle(width=wm, height=0.5, stroke_width=0, fill_color=KERN, fill_opacity=0.85)
                      .move_to([x0 + ws + wm / 2, y, 0]))
            bars.add(b)
            names.add(label(rf"{r['lanes']} lane" + ("s" if r["lanes"] > 1 else ""), font_size=21, color=WHITE)
                      .next_to([x0, y, 0], LEFT, buff=0.2))
            vals.add(label(rf"{1000 * r['seconds']:.2f} ms, \ {r['gbytes_per_second']:.1f} GB/s", font_size=19,
                           color=HEAD).next_to(b, RIGHT, buff=0.15))
        keys = VGroup(label(r"streaming the bytes", font_size=18, color=DATA),
                      label(r"merging the lanes' tables", font_size=18, color=KERN)).arrange(RIGHT, buff=0.5)
        keys.next_to(bars, DOWN, buff=0.4).align_to([x0, 0, 0], LEFT)
        last = L[-1]
        notes = VGroup(
            label(rf"at {last['lanes']} lanes, \ merging ({cm(last['merge_cycles'])} cycles) costs more than "
                  rf"streaming ({cm(last['stream_cycles'])})", font_size=19, color=KERN),
            label(rf"and {last['gbytes_per_second']:.1f} GB/s must come from memory: \ this machine measured "
                  rf"{m['bandwidth_gbs']:.0f} GB/s \ (chapter 2)", font_size=19, color=NO),
            label(rf"lost occurrences fall too, \ {cm(L[0]['lost_occurrences'])} to {cm(last['lost_occurrences'])}: "
                  r"\ more tables, \ more slots", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(keys, DOWN, buff=0.4).align_to(names, LEFT)
        with self.voiceover(
            "For more speed, use more units. <bookmark mark='a'/> Cut the text at word boundaries into lanes, "
            "each with its own unit and table, and merge the tables at the end. <bookmark mark='b'/> One lane "
            "takes thirty-one milliseconds for the thirty novels; four take eight; sixteen, a little over two. "
            "<bookmark mark='c'/> Sixty-four take about one, but merging now costs more than reading: Amdahl's "
            "law, from chapter one. <bookmark mark='d'/> And sixty-four lanes want twenty-three gigabytes a "
            "second of text, nearly all that this machine's memory delivers: the slope of the roofline again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys))
            vo.wait_until("a")
            self.play(FadeIn(names[0]), GrowFromEdge(bars[0], LEFT), FadeIn(vals[0]))
            vo.wait_until("b")
            for k in (1, 2):
                self.play(FadeIn(names[k]), GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(names[3]), GrowFromEdge(bars[3], LEFT), FadeIn(vals[3]))
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        hashrow = next(r for r in led if r["part"] == 17)
        nbytes = j["job"]["bytes"]
        head = label(rf"Ledger row {len(led) - 1}", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.24,
                           label_width=4.8).scale(0.8).move_to(UP * 0.55)
        cpb = hashrow["cycles"] / nbytes
        notes = VGroup(
            label(rf"row {len(led) - 1}: \ the thirty novels through one unit at {row['clock_mhz']:.0f} MHz: \ "
                  rf"{1000 * row['seconds']:.0f} ms; \ with 64 lanes, \ about "
                  rf"{1000 * row['lanes']['64']:.0f} ms", font_size=19, color=HEAD),
            label(rf"Part 17's hash table on Pebble: \ about {cpb:.0f} cycles a byte; \ the unit: \ one", font_size=19,
                  color=WHITE),
            label(r"assumes the bytes arrive one a cycle, \ and a 7 MB table read in 1 ns, \ which is optimistic",
                  font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        for n_ in notes:
            if n_.width > 12.8:
                n_.width = 12.8
        with self.voiceover(
            "The ledger gets row twenty-one. <bookmark mark='a'/> A word-counting unit, one byte per cycle at "
            f"{say_int(round(row['clock_mhz']))} megahertz, counts the thirty novels in about thirty-one "
            "milliseconds, the fastest row yet. <bookmark mark='b'/> Part 17's hash table on Pebble spent about "
            "twenty-nine cycles on every byte; the circuit spends one, because it fetches no instructions at all."
            " <bookmark mark='c'/> Two honest caveats: the text must arrive a byte a cycle, and a seven-megabyte "
            "table answering in a nanosecond is optimistic. The arithmetic is now nearly free; what remains, "
            "again, is moving the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


def say_dec(x: float, digits: int = 1) -> str:
    whole, frac = f"{x:.{digits}f}".split(".")
    return say_int(int(whole)) + " point " + " ".join(_ONES[int(c)] for c in frac)


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, module_box)
