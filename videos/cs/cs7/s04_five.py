from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import CLOCK, CTRL, HEAD, PART, STAGE_COLOR, STAGES, YES, chapter, load

JOBS = {"IF": r"fetch the word at \texttt{pc}", "ID": r"decode; \ read registers", "EX": r"the ALU",
        "MEM": r"data memory", "WB": r"write a register"}
CARRY = [r"\texttt{pc}, \ the word", r"$a$, $b$, \ $rd$, \ control", r"result, \ $rd$", r"value, \ $rd$"]


class Five(WatchScene):
    def construct(self):
        chapter(self, 3, r"Pebble's five stages", r"Where do you cut a single-cycle machine?", lit=(1985,),
                extra=((1985, r"the MIPS R2000"),))
        self.stages()
        self.run()

    # ------------------------------------------------------------------
    def stages(self):
        d = load("charts")["ideal"]
        flow = PipelineFlow(d, readouts=True).move_to(DOWN * 0.1)
        jobs = VGroup(*[label(JOBS[s], font_size=20, color=STAGE_COLOR[s]).next_to(flow.stage[s], DOWN, buff=0.55)
                        for s in STAGES])
        carry = VGroup(*[label(c, font_size=21, color=CLOCK).next_to(r, UP, buff=0.18) for c, r in
                         zip(CARRY, flow.reg)])
        self.flow = flow
        with self.voiceover(
            "Cut Pebble's datapath where the work naturally changes hands. <bookmark mark='a'/> Fetch the instruction. "
            "Decode it and read its registers. Execute it in the ALU. Touch data memory. Write the result back. "
            "<bookmark mark='b'/> Between the stages go pipeline registers. At every clock edge each one captures what "
            "its instruction still needs: operands, the destination register, even the control signals, decoded once "
            "and carried along. <bookmark mark='c'/> That's how five instructions, each at a different point in its "
            "life, share one datapath."
        ) as vo:
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(flow.stage[s][0]), FadeIn(flow.stage[s][1:]),
                                                   FadeIn(j, shift=UP * 0.1))
                                    for s, j in zip(STAGES, jobs)], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(r) for r in flow.reg], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in carry], lag_ratio=0.2), run_time=1.6)
            for _ in range(3):
                self.play(flow.tick.animate.set_opacity(0.9), run_time=0.15)
                self.play(flow.tick.animate.set_opacity(0), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeOut(jobs), FadeOut(carry), FadeIn(flow.readouts))

    # ------------------------------------------------------------------
    def run(self):
        flow = self.flow
        d = flow.data
        n, cycles = d["retired"], d["cycles"]
        card = self.predict(rf"{n} independent instructions, \ five stages. \\ How many cycles?",
                            [rf"{n}", rf"{n + 4}", rf"{5 * n}"],
                            narration=f"Now feed it {n} instructions that don't depend on each other. How many "
                                      f"cycles until the last one is done: {n}, {n + 4}, or {5 * n}?", room=flow)
        self.park(card)
        with self.voiceover(
            "Watch the clock. <bookmark mark='a'/> The first instruction enters fetch. Every cycle, everything moves "
            "one stage right, and a new one enters behind it. <bookmark mark='b'/> By cycle five the pipeline is full: "
            "five instructions in flight, and one finishing every cycle."
        ) as vo:
            vo.wait_until("a")
            flow.run(self, 0, 4, per_cycle=0.9, flash=False)
            vo.wait_until("b")
            self.play(Indicate(flow.boxes, color=HEAD, scale_factor=1.03), run_time=0.8)
        flow.run(self, 4, cycles, per_cycle=0.6, flash=False)
        self.reveal(card, 1)
        law = MathTex(r"\text{cycles}", r"=", r"n + 4", r"\quad\Rightarrow\quad", r"\text{CPI} = 1 + \tfrac{4}{n}",
                      r"\ \to 1", font_size=40).to_edge(DOWN, buff=0.7)
        law[2].set_color(HEAD)
        law[4].set_color(YES)
        ok = tag("simulated", r"cycle by cycle; final state checked against Part 6's emulator").to_corner(DR,
                                                                                                         buff=0.3)
        with self.voiceover(
            f"{n} instructions, {cycles} cycles: four to fill the pipe, then one per cycle. <bookmark mark='a'/> So "
            "cycles equal n plus four, and CPI is one plus four over n, which heads to one for a long program. "
            "<bookmark mark='b'/> That's the ideal. The rest of this film is about what stops us reaching it."
        ) as vo:
            self.play(Indicate(flow.clock, color=CLOCK), Indicate(flow.retired, color=YES))
            vo.wait_until("a")
            self.play(Write(law), FadeIn(ok))
            vo.wait_until("b")
            self.play(Indicate(law[4], color=CTRL))
        self.clear_scene()
