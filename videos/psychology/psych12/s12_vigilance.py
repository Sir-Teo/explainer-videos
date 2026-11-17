from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class Vigilance(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_watchers()
        self.what_it_was()

    def card(self):
        card = chapter_card(11, r"The watch, \ revisited", r"Did the radar observers see less, \ or say less?",
                            lit={1948: r"Mackworth", 1995: r"See et al."}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter eleven. The watch, revisited."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _ax(self, center, ylabel, y1):
        return axes([0, 125], [0, y1], x_length=4.8, y_length=3.0, xticks=[0, 30, 60, 90, 120],
                    yticks=[0, y1 / 2, y1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: rf"{100 * v:.0f}\%",
                    xlabel=r"minutes on watch", ylabel=ylabel, center=center)

    def two_watchers(self):
        d = load("watch")
        head = heading(r"Two watchers, \ one hit rate")
        A = self._ax([-3.6, 0.55, 0], r"hits", 0.8)
        B = self._ax([3.0, 0.55, 0], r"false alarms", 0.4)
        t = d["minutes"]

        def line(ax, y, col, dashed=False):
            c = curve(ax, t, y, col, stroke_width=5)
            dots = VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=0.06, color=col) for a, b in zip(t, y)])
            return VGroup(DashedVMobject(c, num_dashes=30) if dashed else c, dots)
        h1, h2 = line(A.ax, d["criterion_hit"], CRIT), line(A.ax, d["sensitivity_hit"], MODEL, dashed=True)
        f1, f2 = line(B.ax, d["criterion_fa"], CRIT), line(B.ax, d["sensitivity_fa"], MODEL)
        lg = legend([(CRIT, r"A: \ grows cautious"), (MODEL, r"B: \ sees less")], font_size=24).next_to(A, DOWN, buff=0.5)
        rows = rows_of([
            (r"A's criterion creeps up; \ B's sensitivity drains away", WHITE),
            (r"their hit rates fall identically: \ Mackworth's measure cannot tell them apart", HIT),
            (r"false alarms can: \ A's fall, \ B's rise", FA),
        ], 6.0, 26, 0.24).move_to([3.0, -2.35, 0])
        tag = psyche_tag(r"computed: \ 25 signals and 225 blanks every 15 minutes")
        with self.voiceover(
            "Back to the radar observer, with the theory in hand. Here are two of Psyche's watchers on a two-hour "
            "watch. <bookmark mark='a'/> Watcher A sees as well at the end as at the start, but grows more cautious: "
            "its criterion creeps up. Watcher B stays just as willing to say yes, but sees less: its sensitivity "
            "drains away. <bookmark mark='b'/> Their hit rates fall identically, block by block. Counting the "
            "double jumps reported, Mackworth's measure, can't tell them apart. <bookmark mark='c'/> The false "
            "alarms can. The cautious watcher's false alarms fall, because it says yes less to everything. The "
            "tiring watcher's rise, because the evidence it's judging is getting worse. The fact Mackworth needed was "
            "in the trials without a signal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(lg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(h1), Create(h2), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(f1), Create(f2), FadeIn(rows[2]), run_time=2.5)
        self.clear_scene()

    def what_it_was(self):
        src = archive.SEE_1995
        head = heading(r"What does fall on a long watch?")
        rows = rows_of([
            (r"applied to real vigilance data, \ detection theory found both: \ criterion shifts and sensitivity losses",
             WHITE),
            (rf"See, \ Howe, \ Warm and Dember (1995), \ {src.data['studies']} studies: \ a real loss of sensitivity, \ "
             r"its size depending on the task and on how fast events come", MODEL),
            (r"later work: \ some decrements that look like lost sensitivity are criterion shifts in disguise", CRIT),
            (r"both happen; \ which dominates depends on the watch. \ What matters: \ you can now ask", THRESH),
            (r"and the fixes differ: \ rest breaks and job rotation for lost sensitivity; \ feedback, \ payoffs and "
             r"fake targets for caution", HIT),
        ], 11.6, 29, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(src.cite)
        with self.voiceover(
            "So which was it on the real watches? <bookmark mark='a'/> When the theory was turned on vigilance, it "
            "found both. <bookmark mark='b'/> A meta-analysis in 1995 by See, Howe, Warm and Dember gathered "
            f"{src.data['studies']} studies and found a real loss of sensitivity, whose size depended on the kind of "
            "discrimination and on how fast events arrived. <bookmark mark='c'/> Later work argued that some "
            "decrements that look like lost sensitivity are criterion shifts in disguise. <bookmark mark='d'/> Both "
            "happen, and which dominates depends on the watch. The advance is that the question can be asked at all. "
            "<bookmark mark='e'/> And it matters, because the remedies differ. Lost sensitivity calls for rest and "
            "shorter watches. Caution calls for feedback, payoffs, and the fake targets of chapter ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i]))
        self.clear_scene()
