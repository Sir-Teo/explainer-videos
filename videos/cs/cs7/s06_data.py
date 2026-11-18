from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import HEAD, NO, PART, YES, chapter, load


def stalls(d) -> int:
    return sum(1 for r in d["chart"] for ev in r["events"] if ev[0] == "stall")


class Data(WatchScene):
    def construct(self):
        chapter(self, 5, r"Data hazards and forwarding", r"What if an instruction needs a result still on its way?")
        self.raw()
        self.forwarding()
        self.loaduse()
        self.measured()
        self.check()

    # ------------------------------------------------------------------
    def raw(self):
        d = load("charts")["noforward"]
        f = load("charts")["forward"]
        flow = PipelineFlow(d).move_to(DOWN * 0.3)
        n = d["retired"]
        prog = VGroup(*[Text(f["seq"][str(s)]["text"], font="DejaVu Sans Mono", font_size=30, color=GREY_A)
                        for s in range(6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(UP * 0.2)
        arrows = VGroup(*[CurvedArrow(prog[k].get_right() + RIGHT * 0.15, prog[k + 1].get_right() + RIGHT * 0.15,
                                      angle=-1.6, color=HEAD, stroke_width=3, tip_length=0.14) for k in range(1, 5)])
        with self.voiceover(
            "Here's a chain where every instruction uses the one before it. <bookmark mark='a'/> The add reads a "
            "zero, which the instruction just ahead of it is still computing. The subtract needs the add's answer, "
            "and so on down."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in prog], lag_ratio=0.15), run_time=1.4)
            vo.wait_until("a")
            for k in range(4):
                self.play(Create(arrows[k]), Indicate(prog[k + 2], color=HEAD), run_time=0.45)
        self.play(VGroup(prog, arrows).animate.scale(0.6).to_corner(UL, buff=0.35), FadeIn(flow.boxes),
                  FadeIn(flow.regs), FadeIn(flow.readouts), run_time=1.0)
        card = self.predict(rf"No tricks: \ an instruction waits in decode \ until its operand is written back. "
                            rf"\ How many cycles for these {n}?",
                            [rf"{n + 4}", rf"{d['cycles']}", rf"{5 * n}"],
                            narration="Suppose the only rule is: wait in decode until your operand has been written "
                                      f"back. How many cycles for these {n}? {n + 4}, as if nothing happened? "
                                      f"{d['cycles']}? Or {5 * n}?", room=flow)
        self.park(card)
        with self.voiceover(
            "Watch the subtract. It reaches decode, finds its operand missing, and stays. Bubbles leak out ahead of it."
        ):
            flow.run(self, 0, 9, per_cycle=0.55)
        flow.run(self, 9, len(d["chart"]), per_cycle=0.35)
        self.reveal(card, 1, narration=(
            f"{d['cycles']} cycles, nearly double. Each dependent pair costs two bubbles."))
        self.clear_scene()

    # ------------------------------------------------------------------
    def forwarding(self):
        nf, f = load("charts")["noforward"], load("charts")["forward"]
        flow = PipelineFlow(f).move_to(UP * 0.5)
        with self.voiceover(
            "But the value exists long before it is written back. <bookmark mark='a'/> It's sitting at the end of "
            "execute, in the next pipeline register. <bookmark mark='b'/> So send it straight back, to the next "
            "instruction's ALU input. That's forwarding, and the yellow arcs are values taking the shortcut."
        ) as vo:
            self.play(FadeIn(flow.boxes), FadeIn(flow.regs), FadeIn(flow.readouts))
            vo.wait_until("a")
            flow.run(self, 0, 4, per_cycle=0.8)
            vo.wait_until("b")
            flow.run(self, 4, 8, per_cycle=0.8)
        flow.run(self, 8, len(f["chart"]), per_cycle=0.5)
        race = Race([(r"forwarding", f["cycles"], YES), (r"no forwarding", nf["cycles"], NO)], unit="cycles",
                    fmt="{:.0f}", width=7.0, lane_h=0.42, gap=0.35, font_size=24).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(race.lanes), *[FadeIn(c) for c in race.clocks])
        self.add(*race.bars)
        race.go(self, seconds=3.0)
        race.freeze()
        with self.voiceover(
            f"{f['cycles']} cycles instead of {nf['cycles']}: every bubble gone. The hardware is a few comparators "
            "and multiplexers. Does a source register match the destination of an instruction ahead? Then take the "
            "newest match."
        ):
            self.play(Indicate(race.clocks[0], color=YES))
        self.clear_scene()

    # ------------------------------------------------------------------
    def loaduse(self):
        d = load("charts")["loaduse"]
        k = stalls(d)
        flow = PipelineFlow(d).move_to(DOWN * 0.2)
        self.play(FadeIn(flow.boxes), FadeIn(flow.regs), FadeIn(flow.readouts))
        card = self.predict(r"A load, \ then an add that uses the loaded word. \\ With forwarding, how many bubbles?",
                            [r"none", r"one", r"two"],
                            narration="Now a load, and right behind it an add that uses the loaded word. Forwarding "
                                      "is on. How many bubbles: none, one, or two?", room=flow)
        self.park(card)
        flow.run(self, 0, 4, per_cycle=0.7)
        flow.run(self, 4, len(d["chart"]), per_cycle=0.5)
        names = ["none", "one", "two"]
        self.reveal(card, min(k, 2), narration=(
            f"{names[min(k, 2)].capitalize()}. A loaded word only exists at the end of the memory stage, but the add "
            "needs it at the start of execute. Forwarding can move a value sideways, not back in time."))
        fix = label(r"the cure: \ the compiler slips an independent instruction into the gap \ (Part 13)",
                    font_size=24, color=YES).to_edge(DOWN, buff=0.5)
        with self.voiceover("So the hardware stalls once, and compilers learn to fill that slot with useful work."):
            self.play(FadeIn(fix, shift=UP * 0.1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        hz = load("hazards")["benchmarks"]
        names = list(hz)
        a, b = "no forwarding, no prediction", "forwarding"
        maxc = max(max(hz[n][a]["cpi"], hz[n][b]["cpi"]) for n in names)
        scale = 5.0 / maxc
        rows = VGroup()
        for k, n in enumerate(names):
            y = 2.3 - 0.66 * k
            nl = label(n, font_size=20, color=GREY_A).move_to([-2.6, y, 0], aligned_edge=RIGHT)
            r1 = Rectangle(width=hz[n][a]["cpi"] * scale, height=0.4, stroke_width=0, fill_color=NO,
                           fill_opacity=0.65).move_to([-2.4 + hz[n][a]["cpi"] * scale / 2, y, 0])
            r2 = Rectangle(width=hz[n][b]["cpi"] * scale, height=0.4, stroke_width=0, fill_color=YES,
                           fill_opacity=0.8).move_to([-2.4 + hz[n][b]["cpi"] * scale / 2, y, 0])
            v = Text(f"{hz[n][a]['cpi']:.2f}", font="DejaVu Sans Mono", font_size=18, color=NO).next_to(r1, RIGHT,
                                                                                                    buff=0.15)
            v2 = Text(f"{hz[n][b]['cpi']:.2f}", font="DejaVu Sans Mono", font_size=18, color=YES).move_to(v)
            rows.add(VGroup(nl, r1, r2, v, v2))
        one = DashedLine([-2.4 + scale, 2.7, 0], [-2.4 + scale, -2.5, 0], color=GREY_C, stroke_width=1.5)
        ol = label(r"CPI 1", font_size=18, color=GREY_C).next_to(one, DOWN, buff=0.05)
        src = tag("simulated", r"seven programs on Pebble's pipeline").to_corner(DR, buff=0.3)
        lo = min(hz[n][a]["cpi"] for n in names)
        hi = max(hz[n][a]["cpi"] for n in names)
        best = max(names, key=lambda n: hz[n][a]["cpi"] - hz[n][b]["cpi"])
        with self.voiceover(
            "On real programs: <bookmark mark='a'/> without forwarding, CPI runs from "
            f"{lo:.1f} to {hi:.1f}. <bookmark mark='b'/> Switch it on, and every bar shrinks. The {best} drops from "
            f"{hz[best][a]['cpi']:.2f} to {hz[best][b]['cpi']:.2f}. What's left is load-use stalls, and branches."
        ) as vo:
            self.play(Create(one), FadeIn(ol), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[3]))
                                    for r in rows], lag_ratio=0.12), run_time=2.2)
            vo.wait_until("b")
            self.play(*[Transform(r[1], r[2]) for r in rows], *[Transform(r[3], r[4].next_to(r[2], RIGHT, buff=0.15))
                                                                  for r in rows], run_time=1.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        self.checkpoint(
            [(r"Pipelining makes each instruction finish sooner. \ True?",
              r"No: latency grows a little; throughput is what rises"),
             (r"Why can't forwarding remove the load-use bubble?",
              r"The loaded word appears a cycle after the add needs it")],
            narration="Checkpoint. Two questions. Pause if you want to think. First: does pipelining make each "
                      "instruction finish sooner? Second: why can't forwarding remove the load-use bubble?",
            answers_narration="No: each instruction takes slightly longer. Throughput is what rises. And the loaded "
                              "word appears one cycle after the add needs it.")
