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


class Rob(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.ring()
        self.precise()
        self.pipeline()
        self.checked()

    def card(self):
        card = chapter_card(5, r"The reorder buffer", r"How can a machine run out of order, \ yet stop in order?",
                            lit=(1985, 1995), extra=((1985, r"Smith and Pleszkun"), (1995, r"Pentium Pro")),
                            part=PART)
        with self.voiceover("Chapter five. The reorder buffer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        head = label(r"In order, \ out of order, \ in order", font_size=38).to_edge(UP, buff=0.4)
        a = box(3.2, 1.0, r"\text{fetch, \ rename}", DATA, 26)
        b = box(3.2, 1.0, r"\text{execute}", FUNC, 26)
        c = box(3.2, 1.0, r"\text{commit}", YES, 26)
        row = VGroup(a, b, c).arrange(RIGHT, buff=0.9).move_to(UP * 0.7)
        arr = VGroup(Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_C),
                     Arrow(b.get_right(), c.get_left(), buff=0.08, color=GREY_C))
        tags = VGroup(label(r"in program order", font_size=22, color=DATA).next_to(a, DOWN, buff=0.25),
                      label(r"in any order: \ as operands arrive", font_size=22, color=FUNC).next_to(b, DOWN, buff=0.25),
                      label(r"in program order", font_size=22, color=YES).next_to(c, DOWN, buff=0.25))
        rule = VGroup(
            label(r"an instruction's result is \textit{speculative} \ until it commits:", font_size=26, color=GREY_A),
            label(r"registers, \ memory and devices change only at commit, \ oldest first", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In 1985 James Smith and Andrew Pleszkun proposed the fix, and every out-of-order core since has used it. "
            "<bookmark mark='a'/> Bring instructions in, in program order. Let them execute in whatever order their "
            "operands allow. But then put them back in order before anything they did becomes official. <bookmark "
            "mark='b'/> The last step is called commit, or retirement. Until an instruction commits, its result is "
            "held aside, visible to the instructions that need it but not yet written into the architectural "
            "registers or memory. <bookmark mark='c'/> Commit happens strictly oldest first. So at any moment, the "
            "official state of the machine is exactly what it would be if the instructions had run one at a time, in "
            "order, up to the oldest one still in flight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(tags[0]))
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
            "Here is the structure that does this, the reorder buffer, drawn as what it is: a ring of slots. "
            "<bookmark mark='a'/> These are about thirty cycles of the core running the Job's scan loop. Each cycle, "
            "up to four instructions are renamed and take slots at the tail, in program order. They wait, in orange, "
            "for their operands; execute, in green; and when finished, turn blue and wait. <bookmark mark='b'/> "
            "Each cycle, up to four finished instructions leave from the head, but only from the head: a finished "
            "instruction behind an unfinished one must wait for it. <bookmark mark='c'/> Watch the grey ones. The "
            "machine guessed wrong about a branch and fetched down a wrong path. When the branch executes and the "
            "mistake is found, everything younger than it is simply dropped from the ring: none of it had committed, "
            "so none of it ever happened. The tail jumps back to just after the branch, and fetching resumes on the "
            "right path."
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
            label(rf"memory at \texttt{{0x804}}: \ {d['mem'][1]} \ (the later store never happened)", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(mark, DOWN, buff=0.35).align_to(mark, LEFT)
        if res.get_right()[0] > 7:
            res.shift(LEFT * (res.get_right()[0] - 6.9))
            mark.shift(LEFT * (mark.get_right()[0] - 6.9) if mark.get_right()[0] > 6.9 else 0)
        with self.voiceover(
            "Now the problem that defeated the Model 91. Here a divide by zero sits in the middle of some code, "
            "followed by instructions that use other values. <bookmark mark='a'/> The divide is slow: sixteen cycles. "
            "<bookmark mark='b'/> Meanwhile the four instructions after it execute and finish, including a store. "
            "They are done, in blue, but they are behind the divide in the reorder buffer, so they wait. <bookmark "
            "mark='c'/> When the divide reaches the head, the machine finds that it faulted. And at that moment "
            "everything older has committed and nothing younger has: so it discards the younger instructions, and "
            "reports the exception with the state exactly as it was just before the divide. <bookmark mark='d'/> "
            "The store before the divide reached memory. The store after it, which had already computed its address "
            "and data, never did. The exception is precise, though execution was not in order."
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

    # ------------------------------------------------------------------
    def pipeline(self):
        head = label(r"The modern out-of-order pipeline", font_size=36).to_edge(UP, buff=0.3)
        stages = [(r"fetch", DATA, r"predict \\ the path"), (r"decode", DATA, r""),
                  (r"rename", CTRL, r"RAT, \\ free list"), (r"dispatch", CTRL, r"ROB, \ IQ, \\ LSQ entries"),
                  (r"issue", FUNC, r"oldest \\ ready first"), (r"execute", FUNC, r"ALUs, \\ memory ports"),
                  (r"write back", INF, r"broadcast \\ the tag"), (r"commit", YES, r"in order, \\ from the head")]
        boxes = VGroup(*[box(1.45, 0.75, rf"\text{{{s}}}", c, 19) for s, c, _ in stages]).arrange(RIGHT, buff=0.12)
        boxes.move_to(UP * 1.4)
        subs = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.18) for (_, _, t), b in
                        zip(stages, boxes)])
        brace_in = BraceBetweenPoints(boxes[0].get_left() + DOWN * 1.3, boxes[3].get_right() + DOWN * 1.3,
                                      direction=DOWN, color=DATA)
        t_in = label(r"in order", font_size=20, color=DATA).next_to(brace_in, DOWN, buff=0.1)
        brace_out = BraceBetweenPoints(boxes[4].get_left() + DOWN * 1.3, boxes[6].get_right() + DOWN * 1.3,
                                       direction=DOWN, color=FUNC)
        t_out = label(r"out of order", font_size=20, color=FUNC).next_to(brace_out, DOWN, buff=0.1)
        t_c = label(r"in order", font_size=20, color=YES).next_to(boxes[7], DOWN, buff=1.45)
        two = VGroup(
            label(r"our core, \ like the Pentium Pro (1995): \ results wait in the reorder buffer, \ copied to the "
                  r"registers at commit", font_size=21, color=GREY_A),
            label(r"MIPS R10000, \ Alpha 21264, \ most cores today: \ one big physical register file; \ the ROB "
                  r"holds only pointers", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Put together, the pieces make the pipeline that nearly every fast processor has used since the "
            "mid-1990s. <bookmark mark='a'/> Fetch, following the branch predictor's guesses. Decode. Rename, through "
            "the register alias table and a list of free physical registers. Dispatch, which gives each instruction "
            "its slot in the reorder buffer, the issue queue, and, for loads and stores, the load-store queue. "
            "<bookmark mark='b'/> Then, out of order: issue, oldest ready instruction first, to an execution unit; "
            "execute; and write back, broadcasting the result's tag to everyone waiting for it. <bookmark mark='c'/> "
            "And commit, in order, from the head of the reorder buffer. <bookmark mark='d'/> There are two ways to "
            "keep the values. Our core, like Intel's Pentium Pro of 1995, keeps each result in its reorder-buffer "
            "entry and copies it to the architectural registers at commit. The MIPS R10000 and the Alpha 21264, and "
            "most designs since, keep every value in one large physical register file and let the table of names do "
            "all the work: commit just declares a mapping final, and frees the register that held the old value."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(boxes[k], subs[k])) for k in range(4)], lag_ratio=0.25),
                      FadeIn(brace_in), FadeIn(t_in))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(boxes[k], subs[k])) for k in range(4, 7)], lag_ratio=0.25),
                      FadeIn(brace_out), FadeIn(t_out))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(boxes[7], subs[7])), FadeIn(t_c))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t) for t in two], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checked(self):
        head = label(r"Our core, \ checked", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(
            label(r"\texttt{explainer/cs/pebble/ooo.py}: \ about 700 lines, \ cycle by cycle", font_size=24,
                  color=GREY_A),
            label(r"120 random programs \ $\times$ \ 6 configurations, \ and the Job: \ the same registers, \ memory, "
                  r"\ output \ and instruction count as the emulator", font_size=24, color=YES),
            label(r"a divide by zero, \ a store that must not happen, \ a load that must wait: \ all precise",
                  font_size=24, color=YES),
            label(r"every value is computed for real, \ on the right path \textit{and} the wrong one", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "This core is not a diagram; it is a program, about seven hundred lines, that simulates the machine "
            "cycle by cycle. <bookmark mark='a'/> It is checked the way every part of Pebble is checked: on a hundred "
            "twenty random programs, in six different configurations, and on the Job, it must finish with exactly the "
            "registers, memory, output and instruction count that the emulator gives. <bookmark mark='b'/> And the "
            "awkward cases have their own tests: the divide by zero, the store that must never reach memory, the "
            "load that must wait. <bookmark mark='c'/> One more property will matter later. The core computes every "
            "value for real, including on wrong paths that are later thrown away. Those wrong paths really load from "
            "memory. Remember that when we reach chapter nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, l in zip("abc", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
