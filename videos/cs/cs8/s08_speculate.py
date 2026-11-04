from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, OooChart, bar_chart,
                                  box, fmt, load, mono, phase_legend)


class Speculate(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.recorded()
        self.numbers()
        self.drain()

    def card(self):
        card = chapter_card(7, r"Speculation", r"How does a machine run ahead of what it knows?", lit=(1995,),
                            extra=((1995, r"Pentium Pro: \ 40 in flight"),), part=PART)
        with self.voiceover("Chapter seven. Speculation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        head = label(r"Guess, \ run ahead, \ and keep the receipts", font_size=36).to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"1. \ the predictor guesses each branch; \ fetch follows the guess", font_size=26, color=DATA),
            label(r"2. \ everything after the branch is renamed and executed: \ \textit{speculatively}", font_size=26,
                  color=FUNC),
            label(r"3. \ nothing commits past an unresolved branch", font_size=26, color=YES),
            label(r"4. \ right guess: \ nothing to do. \quad wrong guess: \ drop everything younger, \\ restore the "
                  r"alias table, \ fetch from the right target", font_size=26, color=NO),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Part 7's pipeline guessed branches so that fetch never had to wait. The reorder buffer turns that small "
            "trick into a large one. <bookmark mark='a'/> The predictor guesses every branch, and fetch follows the "
            "guess. <bookmark mark='b'/> Everything after the branch is renamed and executed as usual. It is "
            "speculative: done on the strength of a guess. <bookmark mark='c'/> The reorder buffer makes this safe, "
            "because nothing can commit past a branch that has not been resolved. All speculative work stays in the "
            "buffer, unofficial. <bookmark mark='d'/> When the branch finally executes, either the guess was right, "
            "and there is nothing to do, or it was wrong: then every younger instruction is dropped, the register "
            "alias table is put back as it was at the branch, and fetching restarts at the correct target. Real "
            "cores take a snapshot of the alias table at every branch, so the repair takes a single cycle."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recorded(self):
        tl = load("rob")["scan"][:20]
        head = label(r"A wrong guess, \ recorded", font_size=36).to_edge(UP, buff=0.3)
        ch = OooChart(tl, cw=0.42, ch=0.29, label_width=2.6, label_size=13, show_fetch=True).move_to(DOWN * 0.15)
        leg = phase_legend(font_size=17, show_fetch=True).to_edge(DOWN, buff=0.15)
        bne = ch.rows[2]
        wrong = VGroup(*[ch.rows[i] for i, u in enumerate(tl) if u["squashed"]])
        k_res = tl[2]["t"][3]
        line = ch.column_line(k_res + 1, NO)
        notes = VGroup(
            label(r"predicted: \ same length, \ compare the letters", font_size=21, color=NO),
            label(r"resolved: \ different length; \ 11 wrong-path instructions dropped", font_size=21, color=NO),
            label(r"refetched from \texttt{next}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.3).shift(DOWN * 0.7)
        pen = tl[13]["t"][1] - tl[2]["t"][1] if len(tl) > 13 else 0
        with self.voiceover(
            "Here is one, from the core running the Job. Each bar starts when the instruction was fetched; grey is "
            "fetch and decode. <bookmark mark='a'/> This is the scan loop's branch on the entry's length. The "
            "predictor guessed that the lengths matched, so fetch went on into the letter-comparing code. <bookmark "
            "mark='b'/> Eleven instructions down the wrong path were fetched, renamed, and some even executed. "
            "<bookmark mark='c'/> Then the branch executed and found the lengths were different. Everything after it "
            "was dropped, struck through here; none of it had committed, so none of it counts. <bookmark mark='d'/> "
            "Fetch restarted at the right place, and the next instructions arrived about eight cycles after the "
            "branch itself had. Those eight cycles, the misprediction penalty, are the price of a wrong guess: in "
            "today's deep cores, about fifteen to twenty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.heads), FadeIn(leg), LaggedStart(*[FadeIn(r) for r in ch.rows[:3]]),
                      *[FadeIn(VGroup(ch.bars[i], ch.commits[i])) for i in range(2)])
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.bars[2], ch.commits[2])), Indicate(bne, color=NO), FadeIn(notes[0]))
            vo.wait_until("b")
            idx = [i for i, u in enumerate(tl) if u["squashed"]]
            self.play(LaggedStart(*[FadeIn(VGroup(ch.rows[i], ch.bars[i])) for i in idx], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(notes[1]))
            vo.wait_until("d")
            rest = [i for i in range(len(tl)) if not tl[i]["squashed"] and i > 2]
            self.play(LaggedStart(*[FadeIn(VGroup(ch.rows[i], ch.bars[i], ch.commits[i])) for i in rest],
                                  lag_ratio=0.15), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("speculate")["rows"]
        head = label(r"The Job's first chapter, \ with four predictors", font_size=34).to_edge(UP, buff=0.3)
        keys = ["always taken", "2-bit", "tournament", "perfect"]
        vals = [d[k]["ipc"] for k in keys]
        ch = bar_chart(vals, [r"always taken", r"2-bit", r"tournament", r"perfect"], [NO, CTRL, DATA, YES],
                       height=3.0, bar_w=1.2, gap=1.2, font_size=22).move_to(LEFT * 2.3 + DOWN * 0.1)
        yl = note(r"instructions per cycle", font_size=20).next_to(ch, UP, buff=0.3).align_to(ch, LEFT)
        t = d["tournament"]
        n = t["committed"]
        stats = VGroup(
            label(rf"tournament: \ {t['stats']['mispredicts']:,} wrong guesses", font_size=22, color=DATA),
            label(rf"{t['stats']['squashed']:,} instructions thrown away", font_size=22, color=NO),
            label(rf"= {100 * (t['stats']['squashed'] / n):.0f}\% extra work, \ all of it wasted", font_size=22, color=NO),
            label(rf"{t['stats']['wrong_path_loads']:,} loads on wrong paths", font_size=22, color=INF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        with self.voiceover(
            "How much does the guessing matter? Run the Job's first chapter on the same core with four predictors. "
            "<bookmark mark='a'/> Guess every branch taken, and the core manages zero point six nine instructions per "
            "cycle: worse than the in-order pipeline. <bookmark mark='b'/> A two-bit counter: one point eight seven. "
            "The tournament: one point eight nine. <bookmark mark='c'/> A perfect predictor: three point one six. The "
            "branches cost the core forty percent of its speed. <bookmark mark='d'/> With the tournament predictor, "
            "twenty-two thousand wrong guesses threw away two hundred fifty thousand instructions: thirty percent more "
            "work than the program needed, all of it wasted. Including twenty-nine thousand loads, on paths the "
            "program never took. Hold on to that number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            for mk, ks in (("a", [0]), ("b", [1, 2]), ("c", [3])):
                vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s) for s in stats], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drain(self):
        d = load("speculate")["rows"]
        h = load("hook")
        t = d["tournament"]
        n = t["committed"]
        m = t["stats"]["mispredicts"]
        b = t["stats"]["branches"]
        head = label(r"Why the big window stays empty", font_size=36).to_edge(UP, buff=0.35)
        run = n / m
        eq1 = MathTex(r"\text{instructions between wrong guesses} = \frac{N}{\text{mispredictions}} = "
                      rf"\frac{{{n:,}}}{{{m:,}}} \approx {run:.0f}".replace(",", "{,}"), font_size=36).move_to(UP * 1.6)
        cpi_p = 1 / d["perfect"]["ipc"]
        cpi_t = 1 / t["ipc"]
        pen = (cpi_t - cpi_p) * n / m
        eq2 = MathTex(r"\text{CPI} = \text{CPI}_{\text{perfect}} + \frac{\text{mispredictions}}{N} \times P", font_size=36)
        eq3 = MathTex(rf"{cpi_t:.3f} = {cpi_p:.3f} + \frac{{1}}{{{run:.0f}}} \times P \quad\Rightarrow\quad "
                      rf"P \approx {pen:.1f} \text{{ cycles}}", font_size=34, color=HEAD)
        g = VGroup(eq2, eq3).arrange(DOWN, buff=0.3).move_to(DOWN * 0.2)
        punch = label(rf"a {run:.0f}-instruction stretch, \ then the window drains: \ "
                      rf"on average {h['occupancy']['mean']:.0f} in flight, \ not 128", font_size=26,
                      color=NO).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two lines of arithmetic explain the empty window from the hook. <bookmark mark='a'/> The chapter has "
            "eight hundred twenty-seven thousand instructions and twenty-two thousand wrong guesses: one every "
            "thirty-seven instructions. However large the window, the machine can only ever be about thirty-seven "
            "instructions ahead on the right path before it is thrown back. <bookmark mark='b'/> And the cost of each "
            "throw: the time per instruction is what it would be with perfect prediction, plus the rate of wrong "
            "guesses times a penalty P. <bookmark mark='c'/> Put in the measured numbers, and the penalty comes out "
            "at about eight cycles, just what the recording showed. <bookmark mark='d'/> So the window fills for a "
            "few dozen instructions, then drains, again and again. Better prediction is worth more than a bigger "
            "window, and that is why real cores spend so much on predictors."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq1))
            vo.wait_until("b")
            self.play(Write(eq2))
            vo.wait_until("c")
            self.play(Write(eq3))
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
