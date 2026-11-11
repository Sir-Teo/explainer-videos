from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, box, fmt, load, mono)

DEP_COLOR = {"RAW": YES, "WAR": CTRL, "WAW": NO}


class Rename(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.counts()
        self.renaming()
        self.limit()

    def card(self):
        card = chapter_card(2, r"False dependences, \ and renaming", r"Which orderings are real?", lit=(1967, 1975),
                            extra=((1967, r"Tomasulo renames registers"), (1975, r"Keller's look-ahead processors")),
                            part=PART)
        with self.voiceover("Chapter two. False dependences, and renaming."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def listing(self, lines, y=1.0):
        code = VGroup(*[mono(s, 24) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        code.move_to([-2.2, y, 0])
        nums = VGroup(*[label(str(i + 1), font_size=20, color=GREY_C).next_to(c, LEFT, buff=0.35)
                        for i, c in enumerate(code)])
        return code, nums

    def arc(self, code, i, j, kind, side):
        a = code[i].get_right() if side > 0 else code[i].get_left()
        b = code[j].get_right() if side > 0 else code[j].get_left()
        x = max(c.get_right()[0] for c in code) + 0.25 if side > 0 else min(c.get_left()[0] for c in code) - 0.75
        p0, p1 = np.array([x, a[1], 0]), np.array([x, b[1], 0])
        ang = -PI * 0.55 * side * (1 + 0.25 * (j - i - 1))
        return CurvedArrow(p0, p1, angle=ang, color=DEP_COLOR[kind], stroke_width=3, tip_length=0.15)

    def kinds(self):
        d = load("rename")
        head = label(r"Three kinds of dependence", font_size=36).to_edge(UP, buff=0.3)
        code, nums = self.listing(d["example"])
        arcs = {}
        side = {"RAW": 1, "WAR": -1, "WAW": -1}
        for i, j, k, r in d["deps"]:
            arcs.setdefault(k, VGroup()).add(self.arc(code, i, j, k, side[k]))
        keys = VGroup(
            label(r"read after write: \ a value flows \ \textit{(true)}", font_size=24, color=YES),
            label(r"write after read: \ a name is reused \ \textit{(anti)}", font_size=24, color=CTRL),
            label(r"write after write: \ a name is reused \ \textit{(output)}", font_size=24, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(DR, buff=0.4)
        punch = label(r"only the green arrows carry data", font_size=28, color=HEAD).to_edge(DOWN, buff=0.35)
        punch.align_to(keys, RIGHT).shift(UP * 1.9)
        with self.voiceover(
            "These five instructions illustrate register dependencies and name hazards. <bookmark mark='a'/> The "
            "first load produces the value used by the following add. Without value prediction, that add must wait "
            "for its actual input: a read-after-write dependence. <bookmark mark='b'/> The second load reuses a0. "
            "If all versions shared one storage location, it must not overwrite the old value before the earlier "
            "add reads it: a write-after-read hazard. <bookmark mark='c'/> The two loads also reuse the destination "
            "name, creating a write-after-write hazard in such an organization. <bookmark mark='d'/> Those last "
            "hazards arise from storage-name reuse, not a value passing between the operations. Separate live "
            "versions remove them. The genuine producer-consumer chains, and any memory, control or resource "
            "constraints, still have to be respected."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(VGroup(n, c)) for n, c in zip(nums, code)], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(Create(arcs["RAW"]), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(Create(arcs["WAR"]), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(Create(arcs["WAW"]), FadeIn(keys[2]))
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("rename")["counts"]
        head = label(r"On the Job's first chapter", font_size=36).to_edge(UP, buff=0.35)
        n = d["instructions"]
        vals = [(r"read after write", d["raw"], YES), (r"write after read", d["war"], CTRL),
                (r"write after write", d["waw"], NO)]
        rows = VGroup()
        mx = max(v for _, v, _ in vals)
        for name, v, c in vals:
            bar = Rectangle(width=7.0 * v / mx, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.8)
            rows.add(VGroup(label(name, font_size=24, color=c), bar,
                            label(rf"{v:,}", font_size=22, color=GREY_A)))
        for r in rows:
            r[1].next_to(ORIGIN, RIGHT, buff=0)
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        for r in rows:
            r[0].next_to(r[1], LEFT, buff=0.3)
        rows.move_to(DOWN * 0.2 + RIGHT * 0.8)
        cap = note(rf"operand-use and name-reuse events, \ over {n:,} retired instructions", font_size=22).next_to(
            rows, UP, buff=0.5)
        why = label("15 writable registers, \\ plus constant zero; \\ names are reused", font_size=26,
                    color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Count register uses over the Job's eight hundred twenty-seven thousand instructions. The counting "
            "convention matters. <bookmark mark='a'/> About nine hundred eighty-one thousand source-operand uses "
            "refer to an earlier writer; repeated operands count separately. <bookmark mark='b'/> The other bars "
            "count roughly four hundred fifty-seven thousand read-since-write reuse events, and about as many "
            "successive-writer events. They are not all possible pairs of dependent instructions. <bookmark "
            "mark='c'/> Pebble has fifteen writable architectural registers plus a constant zero register. Reusing "
            "those writable names creates anti and output hazards. Renaming separates live register versions, while "
            "genuine value dependencies and memory or control constraints remain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(*[FadeIn(r[0]) for r in rows[1:]], *[GrowFromEdge(r[1], LEFT) for r in rows[1:]],
                      *[FadeIn(r[2]) for r in rows[1:]])
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def renaming(self):
        d = load("rename")
        head = label(r"Renaming: \ a new register for every new value", font_size=34).to_edge(UP, buff=0.3)
        code, nums = self.listing(d["example"], y=0.9)
        code.shift(LEFT * 1.6)
        nums.shift(LEFT * 1.6)
        renamed = VGroup()
        for i, r in enumerate(d["renamed"]):
            srcs = ", ".join(r["srcs"]) if r["op"] != "lw" else f"0({r['srcs'][0]})"
            txt = f"{r['op']:<4} {r['dst']}, {srcs}"
            renamed.add(mono(txt, 24, color=HEAD).move_to([2.2, code[i].get_y(), 0], aligned_edge=LEFT))
        renamed.align_to(np.array([1.0, 0, 0]), LEFT)
        arrows = VGroup(*[Arrow(code[i].get_right() + RIGHT * 0.1, renamed[i].get_left() + LEFT * 0.1, buff=0.05,
                                stroke_width=2, color=GREY_C, max_tip_length_to_length_ratio=0.15)
                          for i in range(len(code))])
        # the register alias table
        names = ["a0", "a1", "a2"]
        rat_title = label(r"register alias table", font_size=22, color=GREY_B)
        cells = VGroup()
        for nm in names:
            cells.add(VGroup(Text(nm, font="DejaVu Sans Mono", font_size=20, color=CODE),
                             Rectangle(width=1.0, height=0.42, stroke_color=GREY_C, stroke_width=1.5)).arrange(
                RIGHT, buff=0.2))
        cells.arrange(DOWN, buff=0.08)
        rat = VGroup(rat_title, cells).arrange(DOWN, buff=0.15).to_corner(DR, buff=0.35)
        vals = {nm: VectorizedPoint(cells[k][1].get_center()) for k, nm in enumerate(names)}
        self.add(*vals.values())
        after = label("distinct live versions; \\ physical names are safely recycled later", font_size=26,
                      color=YES).to_edge(DOWN, buff=0.35)
        chains = VGroup(SurroundingRectangle(VGroup(renamed[0], renamed[1]), color=FUNC, buff=0.08),
                        SurroundingRectangle(VGroup(renamed[2], renamed[3]), color=INF, buff=0.08))
        with self.voiceover(
            "Give each live destination version a separate physical name. <bookmark mark='a'/> A register alias "
            "table maps architectural names to their current physical versions. Source operands capture either an "
            "existing value or its producing version. <bookmark mark='b'/> Process instructions in order: look up "
            "sources first, allocate a fresh destination version, then update the mapping. Here the first load "
            "writes p twenty, and its add reads that version while writing p twenty-one. <bookmark mark='c'/> The "
            "later load writes p twenty-two. It cannot overwrite the earlier load's value, though its own address, "
            "memory and execution-resource constraints still apply. <bookmark mark='d'/> The displayed live "
            "versions have distinct names, removing register anti and output hazards. Physical registers are safely "
            "reclaimed and reused later; they are not unique forever. The two value chains can overlap when their "
            "remaining constraints permit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(nums, code)))
            vo.wait_until("a")
            self.play(FadeIn(rat))
            for i, r in enumerate(d["renamed"]):
                if i == 0:
                    vo.wait_until("b")
                if i == 2:
                    vo.wait_until("c")
                d_arch = d["example"][i].split()[1].rstrip(",")
                k = names.index(d_arch)
                new = Text(r["dst"], font="DejaVu Sans Mono", font_size=20, color=HEAD).move_to(cells[k][1])
                self.play(GrowArrow(arrows[i]), FadeIn(renamed[i]), Transform(vals[d_arch], new), run_time=0.9)
            vo.wait_until("d")
            self.play(Create(chains), FadeIn(after))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self):
        d = load("rename")["limit"]
        head = label(r"What renaming is worth, \ in the limit", font_size=36).to_edge(UP, buff=0.35)
        a = label(rf"an oracle machine, \ every name its own register: \ IPC {d['renamed']:,.0f}", font_size=28,
                  color=YES)
        b = label(rf"the same oracle, \ held to the false dependences: \ IPC {d['not renamed']:.2f}", font_size=28,
                  color=NO)
        g = VGroup(a, b).arrange(DOWN, buff=0.5).move_to(UP * 0.4)
        ratio = label(rf"a factor of {d['renamed'] / d['not renamed']:,.0f}", font_size=40, color=HEAD).next_to(
            g, DOWN, buff=0.6)
        cav = note("whole trace, future paths/word addresses, unlimited starts; \\\\ realistic device/I/O ordering omitted", font_size=22).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "This comparison uses an offline scheduler of the complete recorded execution, not a functional "
            "processor. It knows future paths and memory word addresses, assumes the listed operation latencies, "
            "and has unlimited start width and lookahead. It also omits realistic device and I/O ordering. "
            "<bookmark mark='a'/> With separate register versions, that particular oracle schedule averages about "
            "two thousand four hundred instructions per modeled cycle. It can overlap work whose future inputs were "
            "supplied by the recorded trace. <bookmark mark='b'/> Adding the scheduler's register-name constraints "
            "reduces this to about three point seven. <bookmark mark='c'/> The ratio shows how strongly these "
            "artificial name constraints affect this oracle. It is not a feasible hardware speedup, a bound across "
            "algorithms, or a claim that real cores approach either number. Register renaming is widely used in "
            "high-performance out-of-order designs because it removes name hazards within finite resources."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(a))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(ratio), FadeIn(cav))
        self.wait(0.3)
        self.clear_scene()
