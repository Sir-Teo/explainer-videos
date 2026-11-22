from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import DATA, FUNC, HEAD, INF, NO, PART, YES, chapter, load


class Structural(WatchScene):
    def construct(self):
        chapter(self, 4, r"Structural hazards", r"What if two instructions need the same part at once?")
        self.hazards()
        self.memory()
        self.divider()

    # ------------------------------------------------------------------
    def hazards(self):
        kinds = VGroup(*[node_box(t, c, font_size=44, pad=0.4, height=1.0) for t, c in (
            (r"structural", INF), (r"data", FUNC), (r"control", NO))]).arrange(RIGHT, buff=0.8).move_to(UP * 1.4)
        what = VGroup(*[label(t, font_size=30, color=GREY_A).next_to(k, DOWN, buff=0.4) for t, k in zip(
            (r"two need the same hardware", r"one needs a value \\ not made yet", r"the next \texttt{pc} \\ isn't "
             r"known yet"), kinds)])
        bubble = Circle(radius=0.32, stroke_color=GREY_B).set_fill(GREY_D, 0.25)
        bt = Text("nop", font="DejaVu Sans Mono", font_size=18, color=GREY_B).move_to(bubble)
        b = VGroup(DashedVMobject(bubble, num_dashes=16), bt).scale(1.4).move_to(DOWN * 2.2 + LEFT * 5.6)
        cure = label(r"the last resort: \ stall, \ and send a bubble down the pipe", font_size=32, color=HEAD).next_to(
            b, RIGHT, buff=0.4)
        with self.voiceover(
            "The ideal pipe breaks whenever an instruction can't move on. These are hazards, and there are three "
            "kinds. <bookmark mark='a'/> Structural: two instructions want the same hardware. Data: one needs a value "
            "that isn't made yet. Control: the machine has to fetch before it knows where the program goes. "
            "<bookmark mark='b'/> The last-resort cure is always the same. Hold the instruction, and let an empty "
            "slot, a bubble, travel down the pipe in its place. The art is stalling as rarely as possible."
        ) as vo:
            self.play(LaggedStart(*[GrowFromCenter(k) for k in kinds], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in what], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(cure))
            self.play(b.animate.shift(RIGHT * 10.0), cure.animate.set_opacity(0.6), run_time=2.5, rate_func=linear)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        hz = load("hazards")["structural"]
        frac = hz["one memory port, the Job"]["memory_fraction"]
        flow = PipelineFlow(load("charts")["ideal"], readouts=False).move_to(UP * 1.3)
        mem = node_box(r"one memory", INF, font_size=28).move_to(DOWN * 1.2)
        a1 = Line(flow.stage["IF"][0].get_bottom(), mem.get_left() + UP * 0.1, color=DATA, stroke_width=4)
        a2 = Line(flow.stage["MEM"][0].get_bottom(), mem.get_right() + UP * 0.1, color=INF, stroke_width=4)
        with self.voiceover(
            "First, the structural kind. <bookmark mark='a'/> Suppose there's one memory. Fetch reads it every cycle. "
            "<bookmark mark='b'/> And whenever a load or store reaches MEM, it wants the same memory, in the same "
            "cycle."
        ) as vo:
            self.play(FadeIn(flow.boxes), FadeIn(flow.regs))
            vo.wait_until("a")
            self.play(GrowFromCenter(mem), Create(a1))
            self.play(ShowPassingFlash(a1.copy().set_stroke(DATA, 10), time_width=0.5), run_time=0.8)
            vo.wait_until("b")
            self.play(Create(a2))
            self.play(ShowPassingFlash(a1.copy().set_stroke(DATA, 10), time_width=0.5),
                      ShowPassingFlash(a2.copy().set_stroke(INF, 10), time_width=0.5), run_time=0.8)
            self.play(Wiggle(mem, scale_value=1.15), mem.box.animate.set_stroke(NO, 4), run_time=0.9)
        card = self.predict(rf"In the Job, {100 * frac:.0f}\% of instructions are loads or stores. \\ With one "
                            r"memory port, \ CPI rises by about...",
                            [r"$0.05$", rf"${frac:.2f}$", r"$1$"],
                            narration=f"In the Job, {100 * frac:.0f} percent of instructions touch data memory. "
                                      "With one port, each of them makes fetch wait a cycle. How much does CPI rise?",
                            room=VGroup(flow.boxes, flow.regs, mem, a1, a2))
        self.reveal(card, 1, narration=(
            f"By about {frac:.2f}: one lost cycle for every memory instruction. The usual fix is two ports: split "
            "instruction and data caches, which Part 9 builds. Our model gives Pebble two ports."))
        self.clear_scene()

    # ------------------------------------------------------------------
    def divider(self):
        d = load("charts")["divide"]
        hz = load("hazards")["structural"]["eight dependent divides"]
        flow = PipelineFlow(d).move_to(DOWN * 0.3)
        src = tag("assumed", r"a divide holds EX for 16 cycles").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Structural hazards also come from slow units. <bookmark mark='a'/> A divide occupies the execute stage "
            "for sixteen cycles, two quotient bits at a time, like Part 4's divider. <bookmark mark='b'/> "
            "Watch the add behind it. It has nowhere to go, so it waits in decode, and bubbles flow out ahead of it."
        ) as vo:
            self.play(FadeIn(flow.boxes), FadeIn(flow.regs), FadeIn(flow.readouts), FadeIn(src))
            vo.wait_until("a")
            flow.run(self, 0, 6, per_cycle=0.6)
            vo.wait_until("b")
            flow.run(self, 6, 16, per_cycle=0.35)
        flow.run(self, 16, len(d["chart"]), per_cycle=0.3)
        res = label(rf"eight dependent divides: \ {hz['cycles']} cycles, \ {hz['divide_stalls']} of them waiting",
                    font_size=28, color=NO).next_to(flow, DOWN, buff=1.0)
        with self.voiceover(
            f"Chain eight divides and the program takes {hz['cycles']} cycles, {hz['divide_stalls']} of them "
            "stalls. Multiplication, in contrast, settles inside one execute cycle, so it costs nothing extra."
        ):
            self.play(Write(res), Indicate(flow.cpi, color=NO))
        self.clear_scene()
