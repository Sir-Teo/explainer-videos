from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, OooChart, bar_chart,
                                  box, fmt, load, mono, phase_legend)


class Speculate(WatchScene):
    def construct(self):
        self.card()
        self.idea()
        self.recorded()
        self.numbers()

    def card(self):
        self.chapter(7, r"Speculation", r"How does a machine run ahead of what it knows?", lit=(1995,), extra=((1995, r"Pentium Pro: \ 40 in flight"),), part=PART, said="Chapter seven. Speculation.")

    # ------------------------------------------------------------------
    def idea(self):
        head = label(r"Guess, \ run ahead, \ and keep the receipts", font_size=36).to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"1. \ the predictor guesses each branch; \ fetch follows the guess", font_size=26, color=DATA),
            label("2. \\ younger work may execute speculatively, \\ subject to constraints", font_size=26,
                  color=FUNC),
            label(r"3. \ nothing commits past an unresolved branch", font_size=26, color=YES),
            label(r"4. \ right guess: \ nothing to do. \quad wrong guess: \ drop everything younger, \\ restore the "
                  r"alias table, \ fetch from the right target", font_size=26, color=NO),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Prediction lets fetch proceed before a branch resolves. <bookmark mark='a'/> Fetch follows a predicted "
            "direction and target, within its bandwidth limits. <bookmark mark='b'/> Younger operations may be "
            "renamed and execute when their operands, resources and ordering rules allow. <bookmark mark='c'/> "
            "Ordered retirement prevents younger architectural effects from committing past an unresolved older "
            "branch. It does not keep every physical result or cache effect inside the reorder buffer. <bookmark "
            "mark='d'/> A wrong direction or target discards younger work, repairs register mappings and recovery "
            "state, and redirects fetch. Our simulator rebuilds its alias table from surviving entries. Physical "
            "processors use different mixtures of checkpoints and rollback; checkpoint availability and front-end "
            "refill affect recovery time. A single-cycle universal repair rule would be misleading."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
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
            label("resolved: \\ different length; \\ 11 displayed entries squashed", font_size=21, color=NO),
            label(r"refetched from \texttt{next}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.3).shift(DOWN * 0.7)
        pen = tl[13]["t"][1] - tl[2]["t"][1] if len(tl) > 13 else 0
        with self.voiceover(
            "This is a recorded branch redirect in the functional core. Grey covers fetch and decode; the other "
            "colors distinguish waiting, execution, completion and retirement. <bookmark mark='a'/> The prediction "
            "follows a same-length entry into the letter-comparison path. <bookmark mark='b'/> Eleven displayed "
            "younger entries are later squashed. They reached different stages; some executed and some only waited. "
            "<bookmark mark='c'/> The resolved branch selects the different-length path. No younger entry has "
            "retired, but its resource use and any modeled cache effects still matter. <bookmark mark='d'/> The "
            "chart measures about eight cycles from the branch's rename to the first refetched instruction's "
            "rename. That interval includes branch execution and front-end progress. Recovery penalty depends on "
            "the timestamps and configuration; it is not a universal constant for all branches or processors."
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
        self.ask(r"Branch prediction improves from 90\% to 99\%. \\ The cycles lost to mispredictions fall by about...",
                 [r"10\%", r"90\%"], 1,
                 say="Prediction improves from ninety to ninety-nine percent right. How much do mispredictions cost now?",
                 reveal="Ninety percent less: one miss in a hundred instead of ten. That's why the last few percent matter.")
        d = load("speculate")["rows"]
        head = label(r"The Job's first chapter, \ with four predictors", font_size=34).to_edge(UP, buff=0.3)
        keys = ["always taken", "2-bit", "tournament", "perfect"]
        vals = [d[k]["ipc"] for k in keys]
        ch = bar_chart(vals, [r"always taken", r"2-bit", r"tournament", r"oracle-assisted"], [NO, CTRL, DATA, YES],
                       height=3.0, bar_w=1.05, gap=0.9, font_size=22).move_to(LEFT * 2.1 + DOWN * 0.1)
        yl = note(r"instructions per cycle", font_size=20).next_to(ch, UP, buff=0.3).align_to(ch, LEFT)
        t = d["tournament"]
        n = t["committed"]
        stats = VGroup(
            label(rf"tournament: \ {t['stats']['mispredicts']:,} branch redirects", font_size=22, color=DATA),
            label(rf"{t['stats']['squashed']:,} renamed entries squashed", font_size=22, color=NO),
            label(rf"= {100 * (t['stats']['squashed'] / n):.0f}\% of retired count; \ not executed work", font_size=22, color=NO),
            label(rf"{t['stats']['wrong_path_loads']:,} loads on wrong paths", font_size=22, color=INF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        with self.voiceover(
            "These four functional-core runs differ in prediction policy. <bookmark mark='a'/> Always-taken "
            "prediction gives about zero point six nine retired instructions per cycle. <bookmark mark='b'/> "
            "Two-bit and tournament prediction give about one point eight seven and one point eight nine. <bookmark "
            "mark='c'/> The oracle-assisted setting gives about three point one six. It knows correct-path "
            "outcomes, yet this implementation still records two redirects and one memory-order violation, so its label must not imply zero recovery events. <bookmark mark='d'/> In the tournament "
            "run, the model counts twenty-two thousand two hundred ninety-six branch redirects and two hundred "
            "fifty-three thousand seven hundred sixty-four squashed renamed entries. That is about thirty-one "
            "percent of the retired count, not thirty-one percent extra executed instructions. Some entries never "
            "issued. Separately, twenty-eight thousand nine hundred five loads execute on wrong paths in the "
            "modeled memory system."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            for mk, ks in (("a", [0]), ("b", [1, 2]), ("c", [3])):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
                if mk == "a":
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s) for s in stats], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

