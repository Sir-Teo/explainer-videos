from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, OooChart, RobRing,
                                  box, fmt, load, mono, phase_legend)


def squash_times(tl):
    """A squashed instruction disappears when the branch before it resolves (the last surviving instruction's
    completion)."""
    out = {}
    last = None
    for u in tl:
        if not u["squashed"]:
            last = u
        elif last is not None:
            out[u["seq"]] = last["t"][3]
    return out


class Rob(WatchScene):
    def construct(self):
        self.card()
        self.idea()
        self.ring()
        self.precise()

    def card(self):
        self.chapter(5, r"The reorder buffer", r"How can a machine run out of order, \ yet stop in order?", lit=(1985, 1995), extra=((1985, r"Smith and Pleszkun"), (1995, r"Pentium Pro")), part=PART, said="Chapter five. The reorder buffer.")

    # ------------------------------------------------------------------
    def idea(self):
        self.wrong_idea(r"An out-of-order processor \\ changes the order of your program",
                        r"It executes out of order, \\ but commits in order: the program can't tell",
                        narration="Out of order sounds alarming. Does the processor change the order of your program?",
                        right_narration="No. It executes out of order, but it commits results in program order, so the program "
                                        "can never tell.")
        self.clear_scene()
        head = label(r"In order, \ out of order, \ in order", font_size=38).to_edge(UP, buff=0.4)
        a = box(3.2, 1.0, r"\text{fetch, \ rename}", DATA, 26)
        b = box(3.2, 1.0, r"\text{execute}", FUNC, 26)
        c = box(3.2, 1.0, r"\text{commit}", YES, 26)
        row = VGroup(a, b, c).arrange(RIGHT, buff=0.9).move_to(UP * 0.7)
        arr = VGroup(Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_C),
                     Arrow(b.get_right(), c.get_left(), buff=0.08, color=GREY_C))
        tags = VGroup(label(r"in program order", font_size=22, color=DATA).next_to(a, DOWN, buff=0.25),
                      label("when operands, \\ resources and ordering permit", font_size=22, color=FUNC).next_to(b, DOWN, buff=0.25),
                      label(r"in program order", font_size=22, color=YES).next_to(c, DOWN, buff=0.25))
        rule = VGroup(
            label(r"an instruction's result is \textit{speculative} \ until it commits:", font_size=26, color=GREY_A),
            label("architectural effects retire oldest first; \\ cache effects are separate", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Smith and Pleszkun's 1985 work studied several ways to provide precise interrupts in pipelined "
            "processors. The reorder buffer is one important approach. <bookmark mark='a'/> Dispatch instructions "
            "in order, execute them when their operands, resources and ordering constraints permit, and retire "
            "architectural effects in program order. <bookmark mark='b'/> Execution results may already be in "
            "temporary storage or a physical register file, and dependent instructions may use them before "
            "retirement. <bookmark mark='c'/> A precise exception exposes a valid architectural prefix of the "
            "program, with the faulting instruction handled according to its specified policy. Cache and predictor "
            "effects require separate reasoning."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(a), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(b), FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[1]), FadeIn(c), FadeIn(tags[2]))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring(self):
        tl = load("rob")["scan"]
        sq = squash_times(tl)
        head = label(r"The reorder buffer: \ a ring, \ filled at the tail, \ emptied at the head", font_size=32).to_edge(
            UP, buff=0.25)
        n = 32
        ring = RobRing(n, inner=1.45, outer=2.35).move_to(LEFT * 2.6 + DOWN * 0.35)
        leg = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                              label(t, font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.12)
                       for t, c in ((r"waiting for operands", CTRL), (r"executing", FUNC),
                                    (r"done, \ waiting to commit", DATA), (r"on a wrong path", GREY_D))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18)
        leg.to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        clock = label(r"cycle 0", font_size=26, color=HEAD).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        counter = label(r"committed: \ 0", font_size=24, color=YES).next_to(clock, DOWN, buff=0.2).align_to(leg, LEFT)
        c0 = min(u["t"][1] for u in tl)
        c1 = max(max(u["t"]) for u in tl) + 1
        slot_of = {}
        head_i, tail_i = 0, 0
        committed = 0
        fills = VGroup(*[VectorizedPoint(ring.slots[i].get_center()) for i in range(n)])
        tags = VGroup(*[VectorizedPoint(ring.slots[i].get_center()) for i in range(n)])
        hp = ring.pointer(0, r"head", YES)
        tp = ring.pointer(0, r"tail", DATA)
        live: dict[int, dict] = {}

        def state_color(u, c):
            if u["squashed"]:
                return GREY_D
            t = u["t"]
            if t[2] < 0 or c < t[2]:
                return CTRL
            if t[3] < 0 or c < t[3]:
                return FUNC
            return DATA

        with self.voiceover(
            "We draw this reorder buffer as a ring of slots. <bookmark mark='a'/> The animation follows a short "
            "recorded scan-loop window. Up to four instructions are renamed into tail slots each cycle. Orange "
            "means waiting, green executing, and blue complete but waiting to retire. <bookmark mark='b'/> Up to "
            "four completed instructions retire from the head in order. A completed younger instruction cannot "
            "retire around an unfinished older one. <bookmark mark='c'/> A branch redirect discards its younger "
            "entries and restarts fetch. Their architectural destinations were never committed, but their execution "
            "was real within the model: loads may already have changed the simulated cache. The ring records "
            "retirement order; it does not erase every microarchitectural trace of squashed work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ring), FadeIn(leg), FadeIn(clock), FadeIn(counter), FadeIn(hp), FadeIn(tp))
            self.add(fills, tags)  # above the ring's opaque slots
            vo.wait_until("a")
            for c in range(c0, c1):
                if c == c0 + 4:
                    vo.wait_until("c")  # the squash happens in this cycle
                anims = []
                # commits, then squashes, then renames
                for u in tl:
                    if u["t"][4] == c and u["seq"] in live:
                        i = slot_of[u["seq"]]
                        anims.append(Transform(fills[i], VectorizedPoint(ring.slots[i].get_center())))
                        anims.append(Transform(tags[i], VectorizedPoint(ring.slots[i].get_center())))
                        del live[u["seq"]]
                        committed += 1
                        head_i = (i + 1) % n
                for u in tl:
                    if sq.get(u["seq"]) == c and u["seq"] in live:
                        i = slot_of[u["seq"]]
                        anims.append(Transform(fills[i], VectorizedPoint(ring.slots[i].get_center())))
                        anims.append(Transform(tags[i], VectorizedPoint(ring.slots[i].get_center())))
                        del live[u["seq"]]
                if any(sq.get(u["seq"]) == c for u in tl):
                    alive = [slot_of[s] for s in live]
                    order = sorted(live, key=lambda s: s)
                    tail_i = (slot_of[order[-1]] + 1) % n if order else head_i
                for u in tl:
                    if u["t"][1] == c:
                        i = tail_i
                        slot_of[u["seq"]] = i
                        live[u["seq"]] = u
                        tail_i = (tail_i + 1) % n
                if not live:
                    head_i = tail_i
                else:
                    head_i = slot_of[min(live)]
                for s, u in live.items():
                    i = slot_of[s]
                    col = state_color(u, c)
                    f = ring.slots[i].copy().set_fill(col, opacity=0.85).set_stroke(width=0)
                    t = ring.tag(i, u["text"].split()[0], color=WHITE)
                    anims.append(Transform(fills[i], f))
                    anims.append(Transform(tags[i], t))
                anims.append(Transform(hp, ring.pointer(head_i, r"head", YES)))
                anims.append(Transform(tp, ring.pointer(tail_i, r"tail", DATA)))
                anims.append(Transform(clock, label(rf"cycle {c - c0}", font_size=26, color=HEAD).move_to(clock,
                                                                                                    aligned_edge=LEFT)))
                anims.append(Transform(counter, label(rf"committed: \ {committed}", font_size=24, color=YES).move_to(
                    counter, aligned_edge=LEFT)))
                self.play(*anims, run_time=0.55)
                if c == c0 + 3:
                    vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def precise(self):
        self.ask(r"A divide faults after younger instructions have already finished. \\ What must the machine do?",
                 [r"keep their results", r"discard them, and report the divide", r"retry the divide"], 1,
                 say="A divide faults, but younger instructions have already finished. What must the machine do?",
                 reveal="Throw their results away, and report the divide, as if they never ran.")
        d = load("rob")["divzero"]
        head = label(r"A precise exception", font_size=36).to_edge(UP, buff=0.3)
        ch = OooChart(d["timeline"], cw=0.34, ch=0.4, label_width=2.6, label_size=16, c0=3).move_to(DOWN * 0.1 +
                                                                                                    LEFT * 0.5)
        leg = phase_legend(font_size=17).to_edge(DOWN, buff=0.2)
        div = ch.rows[7]
        later = VGroup(*ch.rows[8:12])
        mark = label(r"the divide reaches the head: \ divide by zero", font_size=22, color=NO).next_to(ch, RIGHT,
                                                                                                   buff=0.2)
        mark.shift(UP * 0.6)
        res = VGroup(
            label(rf"memory at \texttt{{0x800}}: \ {d['mem'][0]} \ (committed before)", font_size=22, color=YES),
            label(rf"memory at \texttt{{0x804}}: \ {d['mem'][1]} \ (younger write uncommitted)", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(mark, DOWN, buff=0.35).align_to(mark, LEFT)
        if res.get_right()[0] > 7:
            res.shift(LEFT * (res.get_right()[0] - 6.9))
            mark.shift(LEFT * (mark.get_right()[0] - 6.9) if mark.get_right()[0] > 6.9 else 0)
        with self.voiceover(
            "Here is Pebble's deliberate divide-zero fault policy. <bookmark mark='a'/> Division has a modeled "
            "sixteen-cycle latency. The fault is recorded with its instruction instead of being reported "
            "immediately. <bookmark mark='b'/> Younger operations can compute results, including a store's address "
            "and data. They wait behind the divide and cannot commit architectural effects. <bookmark mark='c'/> "
            "When the fault reaches the head, older instructions have retired, the faulting divide does not write a "
            "result, and younger instructions are discarded. Pebble stops and reports the fault; it does not "
            "implement an operating-system resume path. <bookmark mark='d'/> The older store has written eleven to "
            "memory. The younger store has not committed its write. That is precise architectural state under this "
            "policy. Remaining cache or predictor effects are a separate question, and RISC-V M defines a different "
            "result for integer division by zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.heads), LaggedStart(*[FadeIn(r) for r in ch.rows], lag_ratio=0.05),
                      FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(VGroup(ch.bars[i], ch.commits[i])) for i in range(7)], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(ch.bars[7]), Indicate(div, color=NO))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(ch.bars[i]) for i in range(8, ch.n)], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(mark), *[r.animate.set_opacity(0.3) for r in later])
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()


