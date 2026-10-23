from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (F, GPU, KEPT, PART, REMOVED, load, spoken_int, take_away)


class Faults(VoiceoverScene):
    def construct(self):
        self.card()
        self.causes()
        self.young()
        self.simulated()

    def card(self):
        card = chapter_card(17, r"When hardware fails", r"Sixteen thousand GPUs never all work at once: \ how often "
                            r"should a run save itself?", part=PART)
        with self.voiceover("Chapter seventeen. When hardware fails."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def causes(self):
        L, P = F.LLAMA3, load("published")
        causes = list(L["causes"])
        other = L["unexpected"] - sum(c for _, c in causes)
        causes.append(("everything else", other))
        mx = causes[0][1]
        bars = VGroup()
        for i, (nm, c) in enumerate(causes):
            w = 5.2 * c / mx
            col = REMOVED if i < 2 else GREY_B
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-1.6 + w / 2, 2.0 - 0.62 * i, 0])
            n_ = label(nm, font_size=21, color=GREY_A).next_to(b, LEFT, buff=0.2).set_x(-1.8, direction=RIGHT)
            v = label(rf"${c}$", font_size=21, color=col).next_to(b, RIGHT, buff=0.12)
            bars.add(VGroup(n_, b, v))
        bh = label(rf"Llama 3: \ the ${L['unexpected']}$ unplanned interruptions of ${L['days']}$ days, \ by cause",
                   font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        nums = VGroup(
            label(rf"one every ${P['llama_mtbf_h']:.1f}$ hours", font_size=26, color=REMOVED),
            label(rf"each GPU: \ about once in ${P['llama_gpu_mtbf_years']:.1f}$ years", font_size=24, color=GPU),
            label(rf"${L['hardware_share']}\%$ hardware; \ only ${L['manual']}$ needed a person; \ over "
                  rf"${L['effective']}\%$ of the time training", font_size=22, color=GREY_A),
            label(rf"and the weather: \ ${L['diurnal'][0]}$--${L['diurnal'][1]}\%$ slower at midday; \ tens of "
                  r"megawatts swinging when all GPUs pause together", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        src = cite(r"Llama Team (2024), Sec.\ 3.3.4, Table 5", corner=DR, font_size=17)
        with self.voiceover(
            f"Back to Llama 3's run. In fifty-four days its job was interrupted {L['interruptions']} times, "
            f"{L['unexpected']} of them unplanned. <bookmark mark='a'/> Here are the causes Meta reported. The "
            "largest by far: a faulty GPU, then a failing memory chip on a GPU, then software bugs, network switches "
            "and cables, and host maintenance. <bookmark mark='b'/> That is one interruption every "
            f"{P['llama_mtbf_h']:.1f} hours. Yet each GPU on its own failed about once in "
            f"{P['llama_gpu_mtbf_years']:.1f} years: the problem is not the parts, it is that there are sixteen "
            "thousand of them, and any one stops the whole job. <bookmark mark='c'/> Thanks to automation, only three "
            "failures needed a person, and the run spent more than ninety percent of its time training. "
            "<bookmark mark='d'/> Even the weather showed, in the throughput and in the power draw."
        ) as vo:
            self.play(FadeIn(bh), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b_[0]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
                                    for b_ in bars], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(nums[0]), FadeIn(nums[1]))
            vo.wait_until("c")
            self.play(FadeIn(nums[2]))
            vo.wait_until("d")
            self.play(FadeIn(nums[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def young(self):
        P = load("published")
        colors = {r"\tau": KEPT, r"\delta": GPU, r"M": REMOVED}
        rows = [
            cmath(r"\text{waste per second}", r"=", r"\frac{\delta}{\tau}", r"+", r"\frac{\tau}{2M}", colors=colors,
                  font_size=32),
            cmath(r"\frac{d}{d\tau}", r":", r"-\frac{\delta}{\tau^2} + \frac{1}{2M} = 0", colors=colors, font_size=32),
            cmath(r"\tau^\ast", r"=", r"\sqrt{2\,\delta\,M}", colors=colors, font_size=38),
            cmath(r"\tau^\ast", r"=", rf"\sqrt{{2 \times {P['llama_ckpt_s']:.0f}\,\text{{s}} \times "
                  rf"{P['llama_mtbf_h']:.1f}\,\text{{h}}}}", r"\approx", rf"{P['llama_young_s'] / 60:.0f}\ \text{{min}}",
                  colors=colors, font_size=32),
        ]
        whys = [why(r"saving every $\tau$ costs $\delta$; \ a failure loses $\tau/2$ on average", font_size=19),
                why(r"minimize", font_size=19), why(r"Young (1974)", font_size=19),
                why(r"Llama 3's numbers", font_size=19)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.0, buff=0.45, edge=6.9)
        delta = label(rf"$\delta$: \ $16{{,}}384$ GPUs $\times$ up to $4$ GB each, \ at $2$ TB/s \ $\approx "
                      rf"{P['llama_ckpt_s']:.0f}$ s", font_size=20, color=GPU).to_edge(DOWN, buff=0.45)
        src = cite(r"Young, CACM (1974); \ Llama Team (2024), Sec.\ 3.3.4", corner=DR, font_size=17)
        with self.voiceover(
            "So a run saves a checkpoint of every GPU's state regularly, and after a failure restarts from the last one. "
            "How often should it save? Saving every tau seconds, at a cost of delta each time, wastes delta over tau of "
            "the run. <bookmark mark='a'/> And a failure, arriving on average every M seconds, throws away the work since "
            "the last save, half an interval on average: tau over two M more. <bookmark mark='b'/> Set the derivative to "
            "zero. <bookmark mark='c'/> The best interval is the square root of two delta M: John Young's rule, from "
            "1974. <bookmark mark='d'/> For Llama 3: checkpoints of up to four gigabytes per GPU, storage that wrote two "
            f"terabytes a second, so a full save took about {P['llama_ckpt_s']:.0f} seconds; with a failure every "
            f"{P['llama_mtbf_h']:.1f} hours, save every {P['llama_young_s'] / 60:.0f} minutes or so."
        ) as vo:
            step(0)
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(rows[0][-1], color=REMOVED))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(delta))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulated(self):
        Fa = load("faults")
        taus = np.asarray(Fa["taus"]) / 60
        gp = np.asarray(Fa["goodput"])
        lo, hi = np.asarray(Fa["lo"]), np.asarray(Fa["hi"])
        fo = np.asarray(Fa["first_order"])
        g = axes([0, math.log10(taus[-1])], [0.4, 1.0], x_length=7.0, y_length=4.0,
                 xlabel=r"minutes between checkpoints", ylabel=r"share of the time spent on useful training",
                 xticks=[0, 1, 2], yticks=[0.4, 0.6, 0.8, 1.0], xfmt=lambda v: f"{10 ** v:g}",
                 center=[-1.8, -0.3, 0], font_size=18)
        x = np.log10(taus)
        bd = band(g.ax, x, np.clip(lo, 0.4, 1), np.clip(hi, 0.4, 1), KEPT)
        cv = curve(g.ax, x, np.clip(gp, 0.4, 1), KEPT, 3)
        fc = DashedVMobject(curve(g.ax, x, np.clip(fo, 0.4, 1), GREY_A, 2), num_dashes=40)
        yx = math.log10(Fa["young"] / 60)
        yl = DashedLine(g.ax.c2p(yx, 0.4), g.ax.c2p(yx, 1.0), color=GPU, dash_length=0.06)
        ylab = label(rf"Young: \ ${Fa['young'] / 60:.0f}$ min", font_size=20, color=GPU).next_to(g.ax.c2p(yx, 1.0), UP,
                                                                                            buff=0.08)
        best = Dot(g.ax.c2p(math.log10(Fa["best_tau"] / 60), Fa["best"]), radius=0.08, color=YELLOW)
        info = VGroup(
            label(rf"simulated: \ ${Fa['H'] / 86400:.0f}$ days, \ ${Fa['runs']}$ runs per interval", font_size=20,
                  color=GREY_A),
            label(rf"failures at random, \ one per ${Fa['M'] / 3600:.1f}$ h", font_size=20, color=REMOVED),
            label(rf"saving: \ ${Fa['delta']:.0f}$ s; \ restarting: \ ${Fa['R'] / 60:.0f}$ min \ (illustrative)",
                  font_size=20, color=GREY_A),
            label(rf"best: \ every ${Fa['best_tau'] / 60:.0f}$ min, \ ${100 * Fa['best']:.1f}\%$ useful", font_size=22,
                  color=YELLOW),
            label(r"dashes: \ Young's first-order formula", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 0.2, 0])
        lost = 1 - Fa["best"]
        restart_share = Fa["R"] / Fa["M"]
        tag = note(r"computed", font_size=18).to_corner(DR, buff=0.2)
        with self.voiceover(
            f"We simulated it: {Fa['H'] / 86400:.0f} days of a run with random failures, one every "
            f"{Fa['M'] / 3600:.1f} hours on average, {Fa['delta']:.0f} seconds to save and, as an illustration, ten "
            "minutes to restart, many times over for each interval between checkpoints. <bookmark mark='a'/> Save too "
            "often, and saving eats the run; too rarely, and every failure throws away hours. <bookmark mark='b'/> The "
            f"best interval in the simulation is {Fa['best_tau'] / 60:.0f} minutes; Young's rule says "
            f"{Fa['young'] / 60:.0f}. <bookmark mark='c'/> Even then, {100 * lost:.0f} percent of the time is lost: "
            f"{100 * restart_share:.0f} percent to the restarts alone, the rest to saving and to work done twice. That "
            "is why frontier labs make restarts fast and checkpoints asynchronous, and why DeepSeek-V4's kernels are "
            "deterministic: a run that replays exactly can be debugged."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(info[:3]))
            vo.wait_until("a")
            self.play(FadeIn(bd), Create(cv), run_time=2.0)
            self.play(Create(fc), FadeIn(info[4]))
            vo.wait_until("b")
            self.play(Create(yl), FadeIn(ylab), FadeIn(best, scale=1.5), FadeIn(info[3]))
            vo.wait_until("c")
            self.play(Indicate(info[2]))
        self.wait(0.3)
        self.clear_scene()
