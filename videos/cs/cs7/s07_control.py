from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import COST, DATA, HEAD, HIST, NO, PART, YES, chapter, load, mono


class Control(WatchScene):
    def construct(self):
        chapter(self, 6, r"Control hazards", r"What do you fetch before you know where the program goes?")
        self.penalty()
        self.cost()
        self.options()

    # ------------------------------------------------------------------
    def penalty(self):
        d = load("charts")["branch"]
        flushed = sum(1 for v in d["seq"].values() if v["flushed"] and v["text"] != "?")
        taken = max(1, sum(1 for r in d["chart"] for ev in r["events"] if ev[0] == "flush"))
        per = flushed / taken
        flow = PipelineFlow(d).move_to(DOWN * 0.3)
        with self.voiceover(
            "Fetch must deliver an instruction every cycle. But after a branch, which one? <bookmark mark='a'/> The "
            "branch is only decided in execute, two stages later. The simplest policy is to keep fetching the next "
            "instructions in memory, and hope the branch isn't taken. Here's a loop whose branch is taken twice."
        ) as vo:
            self.play(FadeIn(flow.boxes), FadeIn(flow.regs), FadeIn(flow.readouts))
            vo.wait_until("a")
            flow.run(self, 0, 3, per_cycle=0.7)
        card = self.predict(r"The branch turns out taken. \\ How many cycles are thrown away?",
                            [r"one", r"two", r"five"],
                            narration="When the branch turns out taken, how many cycles of work are thrown away? "
                                      "One, two, or the whole pipe?", room=flow)
        self.reveal(card, 1 if round(per) == 2 else (0 if round(per) == 1 else 2))
        with self.voiceover(
            "Watch the grey ones fall. <bookmark mark='a'/> By the time the ALU decides, two wrong instructions are "
            "already inside, one in decode and one in fetch. They're flushed before they change anything, and fetch "
            "restarts at the target. Two cycles lost, every taken branch."
        ) as vo:
            vo.wait_until("a")
            flow.run(self, 3, len(d["chart"]), per_cycle=0.55)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        pr = load("predictors")["table"]["the Job, chapter 1"]
        frac = pr["branches"] / pr["instructions"]
        taken = pr["rows"]["always taken"]["accuracy"]  # taken branches: the ones predict-not-taken gets wrong
        eq = MathTex(r"\Delta\text{CPI}", r"=", r"\frac{\text{branches}}{\text{instruction}}", r"\times",
                     r"\frac{\text{wrong}}{\text{branch}}", r"\times", r"\text{penalty}", font_size=44).move_to(UP * 1.0)
        eq[0].set_color(COST)
        num = MathTex(r"\Delta\text{CPI}", r"=", f"{frac:.2f}", r"\times", f"{taken:.2f}", r"\times", r"2",
                      font_size=52).move_to(eq)
        num[0].set_color(COST)
        num[2].set_color(DATA)
        num[4].set_color(NO)
        res = MathTex(rf"\approx {frac * taken * 2:.2f}", font_size=52, color=HEAD).next_to(num, RIGHT, buff=0.3)
        notes = VGroup(
            label(rf"{100 * frac:.0f}\% of the Job's instructions are branches", font_size=30, color=DATA),
            label(rf"{100 * taken:.0f}\% of those are taken: \ wrong, \ if we always guess not taken", font_size=30,
                  color=NO),
        ).arrange(DOWN, buff=0.2).next_to(eq, DOWN, buff=0.9)
        with self.voiceover(
            "How much does that cost? <bookmark mark='a'/> The extra CPI is branches per instruction, times the "
            "fraction we get wrong, times the penalty. <bookmark mark='b'/> In the Job, "
            f"{100 * frac:.0f} percent of instructions are branches, and {100 * taken:.0f} percent of those are "
            f"taken. <bookmark mark='c'/> Two cycles each: about {frac * taken * 2:.2f} cycles added to every "
            "instruction. <bookmark mark='d'/> And a deeper pipeline decides later, so the penalty grows with depth. "
            "This one equation made branch prediction one of the most studied problems in architecture."
        ) as vo:
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0], shift=UP * 0.1))
            self.play(FadeIn(notes[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(TransformMatchingTex(eq, num), run_time=1.4)
            self.play(Write(res))
            vo.wait_until("d")
            self.play(Indicate(num[6], color=HEAD, scale_factor=1.4))
        self.clear_scene()

    # ------------------------------------------------------------------
    def options(self):
        boxes = VGroup(*[node_box(t, c, font_size=38, pad=0.35, height=0.9) for t, c in (
            (r"decide earlier", DATA), (r"delay the branch", HIST), (r"guess", YES))])
        for k, b in enumerate(boxes):
            b.move_to([-4.3 + 4.3 * k, 1.6, 0])
        what = VGroup(
            label(r"compare in ID: \\ a 1-cycle penalty, \\ a longer stage", font_size=28, color=GREY_A),
            VGroup(mono("beq  a0, a1, L", 22), mono("add  a2, a2, 1", 22, HIST),
                   label(r"the slot always runs \\ (MIPS, 1985)", font_size=26, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            label(r"fetch the likely path; \\ check in EX; \\ flush only when wrong", font_size=28, color=GREY_A),
        )
        for w, b in zip(what, boxes):
            w.next_to(b, DOWN, buff=0.45)
        later = label(r"MIPS Release 6 dropped delay slots; \ RISC-V and ARM never had them", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Three ways out. <bookmark mark='a'/> Decide earlier: compare in decode and lose only one cycle, at the "
            "price of a longer stage. <bookmark mark='b'/> Change the rules: in classic MIPS the instruction after a "
            "branch always runs, and the compiler tries to put something useful there. That slot became a burden "
            "later, and newer designs dropped it. <bookmark mark='c'/> Or guess. Fetch the likely path, check in "
            "execute, and pay only when wrong. Every fast processor since the nineties guesses, and guessing well is "
            "the next chapter."
        ) as vo:
            self.play(GrowFromCenter(boxes[0]), FadeIn(what[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(GrowFromCenter(boxes[1]), FadeIn(what[1], shift=UP * 0.1))
            self.play(FadeIn(later))
            vo.wait_until("c")
            self.play(GrowFromCenter(boxes[2]), FadeIn(what[2], shift=UP * 0.1))
            self.play(boxes[2].animate.scale(1.15), boxes[:2].animate.set_opacity(0.4), what[:2].animate.set_opacity(
                0.4), run_time=0.8)
        self.clear_scene()
