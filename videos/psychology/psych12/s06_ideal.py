from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class Ideal(VoiceoverScene):
    def construct(self):
        self.card()
        self.ratio()
        self.where()
        self.accuracy()

    def card(self):
        card = chapter_card(5, r"The ideal observer", r"Where should the line go?",
                            lit={1933: r"Neyman and Pearson"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter five. The ideal observer."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ratio(self):
        d = load("ideal")
        head = heading(r"The best decision variable: \ the likelihood ratio")
        A = axes([-3, 5], [-3, 3], x_length=6.2, y_length=4.0, xticks=[-2, 0, 2, 4], yticks=[-2, 0, 2],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=r"the evidence, $x$",
                 ylabel=r"likelihood ratio (log scale)", center=[-3.0, -0.1, 0])
        ax = A.ax
        lr = curve(ax, d["x"], np.clip(np.log10(d["lr"]), -3, 3), MODEL, stroke_width=5)
        one = DashedLine(ax.c2p(-3, 0), ax.c2p(5, 0), color=GREY_C, stroke_width=2)
        eq = MathTex(r"\ell(x) = \frac{p(x \mid \text{signal})}{p(x \mid \text{noise})}", font_size=40, color=MODEL)
        rows = rows_of([
            (r"how much more likely this evidence is under signal than under noise", WHITE),
            (r"with equal spreads it rises steadily with $x$: \ a line on $x$ is a line on $\ell$", MODEL),
            (r"Neyman and Pearson (1933): \ for any false-alarm rate, \ the ratio gives the most hits", THRESH),
            (r"no rule does better: \ the ROC of the ratio is the highest possible \ (Statistics, \ Built, \ Part 10)",
             GREY_A),
        ], 5.0, 27, 0.28)
        side = VGroup(eq, rows).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.9, 0.0, 0])
        keep_in_frame(side)
        tag = psyche_tag(r"computed: \ $d' = 1.5$")
        with self.voiceover(
            "So far the criterion was a line on the evidence. What's the best place for it, and is a line on the "
            "evidence even the best kind of rule? <bookmark mark='a'/> The answer runs through one quantity: the "
            "likelihood ratio, how much more probable this evidence is if a signal was there than if it wasn't. "
            "<bookmark mark='b'/> When the two distributions have the same spread, the ratio rises steadily with "
            "the evidence, so a line on the evidence is the same as a line on the ratio. <bookmark mark='c'/> And "
            "a line on the ratio is the best rule there is. That's the Neyman-Pearson lemma, from 1933: for any "
            "false-alarm rate you're willing to accept, the likelihood ratio gives the most hits. "
            "<bookmark mark='d'/> Its ROC sits above every other rule's. Statistics, Built proves it in its "
            "tenth part. Here, it means the radar observer's question has a best answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(one), FadeIn(eq))
            vo.wait_until("a")
            self.play(Create(lr), FadeIn(rows[0]), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()

    def where(self):
        d = load("ideal")
        head = heading(r"Where the line goes: \ base rates and payoffs")
        eq = MathTex(r"\text{say yes when}\quad \ell(x) \;>\; \frac{P(\text{noise})}{P(\text{signal})}"
                     r"\cdot\frac{V_{\text{cr}} + C_{\text{fa}}}{V_{\text{hit}} + C_{\text{miss}}}",
                     font_size=40, color=THRESH).move_to([0, 2.2, 0])
        A = axes([-3.5, 5.0], [0, 0.45], x_length=7.0, y_length=2.8, xticks=[-2, 0, 2, 4], yticks=[],
                 xfmt=lambda v: f"{v:g}", xlabel=r"evidence", ylabel=r"", center=[-2.7, -0.95, 0])
        ax = A.ax
        g = gauss_pair(ax, d["d"])
        cols = [WHITE, CRIT, MISS]
        lines = VGroup()
        for k, col in zip(d["criteria"], cols):
            lines.add(DashedLine(ax.c2p(float(k), 0), ax.c2p(float(k), 0.44), color=col, stroke_width=4))
        labs = VGroup(*[label(rf"{100 * p:.0f}\%", font_size=22, color=c).next_to(ln, UP, buff=0.05)
                        for p, ln, c in zip(d["prev"], lines, cols)])
        rows = rows_of([
            (r"signals half the time: \ $\ell > 1$, \ the line at the midpoint", WHITE),
            (rf"signals 20\% of the time: \ $\ell > 4$; \ hits fall to {pct(d['hit'][1])}", CRIT),
            (rf"signals 5\% of the time: \ $\ell > 19$; \ hits {pct(d['hit'][2])}", MISS),
            (r"payoffs enter the same way: \ if misses are costly, \ the bar comes down", HIT),
        ], 4.6, 26, 0.28).move_to([4.5, -0.9, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $d' = 1.5$, \ all trials worth the same")
        with self.voiceover(
            "The lemma doesn't say which false-alarm rate to accept. That depends on two things the eye knows "
            "nothing about. <bookmark mark='a'/> The rule: say yes when the likelihood ratio beats the odds against "
            "a signal, times the ratio of what's at stake. <bookmark mark='b'/> If signals come half the time and "
            "every outcome is worth the same, the bar is one, and the line sits at the midpoint. "
            "<bookmark mark='c'/> If signals come one time in five, the evidence must be four times as likely "
            "under signal before yes pays. The line moves right, and the hit rate falls to "
            f"{100 * d['hit'][1]:.0f} percent. <bookmark mark='d'/> One time in twenty, the bar is nineteen, and the "
            f"ideal observer catches only {100 * d['hit'][2]:.0f} percent of the signals. <bookmark mark='e'/> "
            "Payoffs enter the same formula. If a miss costs much more than a false alarm, the bar comes down. "
            "So a good observer's criterion is supposed to move. The question is whether it moves the right "
            "amount."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(g))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            for i, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(Create(lines[i]), FadeIn(labs[i]), FadeIn(rows[i]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def accuracy(self):
        d = load("ideal")
        head = heading(r"The trap in ``be as accurate as possible''")
        A = axes([-2, 5], [0, 1.0], x_length=6.6, y_length=4.0, xticks=[-2, 0, 2, 4], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"where the line is drawn",
                 ylabel=r"share of all trials answered correctly", center=[-2.9, -0.2, 0])
        ax = A.ax
        cols = [WHITE, CRIT, MISS]
        cs = VGroup(*[curve(ax, d["grid"], d["ev"][i], cols[i], stroke_width=4) for i in range(3)])
        lg = legend([(cols[i], rf"signals {100 * p:.0f}\% of the time") for i, p in enumerate(d["prev"])],
                    font_size=22).move_to(ax.c2p(3.3, 0.22))
        top = Dot(ax.c2p(float(d["criteria"][2]), float(d["acc_opt_05"])), radius=0.08, color=MISS)
        rows = rows_of([
            (rf"at 5\%: \ the best line gets {pct(d['acc_opt_05'], 1)} right", MISS),
            (rf"saying ``no'' to everything gets {pct(d['acc_always_no_05'])} right", GREY_A),
            (rf"the midpoint line, \ which catches most signals, \ gets {pct(d['acc_neutral_05'])}", WHITE),
            (r"when signals are rare, \ accuracy rewards silence. \ What matters is the cost of a miss", THRESH),
        ], 4.8, 27, 0.28).move_to([4.4, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $d' = 1.5$")
        with self.voiceover(
            "And here's a trap that catches people who build screening tests. Plot the share of all trials "
            "answered correctly against where the line is drawn, for the three base rates. "
            "<bookmark mark='a'/> When signals come five percent of the time, the best line gets "
            f"{100 * d['acc_opt_05']:.1f} percent right. <bookmark mark='b'/> Saying no to every single trial "
            "gets ninety-five percent right. <bookmark mark='c'/> And the midpoint line, which catches most of the "
            f"signals, gets only {100 * d['acc_neutral_05']:.0f} percent. <bookmark mark='d'/> When signals are rare, "
            "accuracy rewards silence. If the signal is a tumour or a bomb, accuracy is the wrong goal. The cost of a "
            "miss has to enter the formula, and someone has to decide what it is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), FadeIn(lg),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()
