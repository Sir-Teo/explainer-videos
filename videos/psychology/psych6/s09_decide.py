from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

A_COL, B_COL = EXC, DATA


def pair(center, r=0.55, gap=2.9, loops=True):
    """Two rival units: mutual inhibition, and (optionally) a loop of self-excitation on each."""
    c = np.asarray(center, float)
    a = unit("A", r, A_COL, 32).move_to(c + LEFT * gap / 2)
    b = unit("B", r, B_COL, 32).move_to(c + RIGHT * gap / 2)
    inh = VGroup(inhibit(a.get_right() + UP * 0.16, b.get_left() + UP * 0.16),
                 inhibit(b.get_left() + DOWN * 0.16, a.get_right() + DOWN * 0.16))
    g = VGroup(a, b, inh)
    g.a, g.b, g.inh = a, b, inh
    if loops:
        g.loops = VGroup(*[CurvedArrow(u.get_top() + LEFT * 0.22 + DOWN * 0.03, u.get_top() + RIGHT * 0.22 + DOWN * 0.03,
                                       angle=-4.6, color=col, stroke_width=4, tip_length=0.18)
                           for u, col in ((a, A_COL), (b, B_COL))])
        g.add(g.loops)
    return g


class Decide(VoiceoverScene):
    def construct(self):
        self.card()
        self.wiring()
        self.race()
        self.holds()
        self.slow()

    def card(self):
        card = chapter_card(8, r"A circuit that decides", r"How can a few cells choose, and remember the choice?",
                            lit=(), part=PART, scale=("circuit",), marr=("how",))
        with self.voiceover(
            "Chapter eight. A circuit that decides."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def wiring(self):
        head = heading(r"Two rivals")
        g = pair([-3.6, 0.6, 0])
        ins = VGroup(*[excite(u.get_bottom() + DOWN * 1.3, u.get_bottom(), color=col, buff=0.06)
                       for u, col in ((g.a, A_COL), (g.b, B_COL))])
        in_l = VGroup(label(r"evidence for A", font_size=24, color=A_COL).next_to(ins[0], DOWN, buff=0.1),
                      label(r"evidence for B", font_size=24, color=B_COL).next_to(ins[1], DOWN, buff=0.1))
        rows = VGroup(
            wrapped_label(r"each unit gets its own input", 5.4, 28, WHITE),
            wrapped_label(r"each inhibits the other", 5.4, 28, INH),
            wrapped_label(r"each excites itself", 5.4, 28, A_COL),
            MathTex(r"\tau\,\frac{dr_A}{dt} = -r_A + f\big(I_A + w_s\, r_A - w_c\, r_B\big)", font_size=36),
            wrapped_label(r"$f$ is an S-shaped curve: \ nothing below a threshold, \ a ceiling at the top", 5.4, 26,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag()
        with self.voiceover(
            "The second circuit makes decisions. Two units. <bookmark mark='a'/> Each receives its own input. "
            "Think of it as the evidence for one of two options. <bookmark mark='b'/> Each one inhibits the "
            "other. That's the lateral inhibition of the last two chapters, now between two rivals. "
            "<bookmark mark='c'/> And each one excites itself: some of its output comes back round as input. "
            "<bookmark mark='d'/> The equation says that each unit's activity relaxes toward a function of "
            "what it receives: its input, plus its own activity, minus its rival's. The function is an "
            "S-shaped curve, with nothing below a threshold and a ceiling at the top. So what does a circuit "
            "like this do?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g.a), FadeIn(g.b))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.3), FadeIn(in_l), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(g.inh), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(g.loops), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def race(self):
        w = load("wta")
        head = heading(r"A small difference in, \ all or nothing out")
        A = axes([0, 300], [0, 1.08], x_length=7.0, y_length=4.2, xticks=[0, 100, 200, 300], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time (ms)", ylabel=r"activity", center=[-3.0, -0.6, 0])
        ax = A.ax
        t = w["t"]
        keep = t <= 300
        ra, rb = trace(ax, t[keep], w["a"][keep, 0], A_COL), trace(ax, t[keep], w["a"][keep, 1], B_COL)
        sa, sb = trace(ax, t[keep], w["b"][keep, 0], A_COL), trace(ax, t[keep], w["b"][keep, 1], B_COL)
        fa, fb = float(w["a"][-1, 0]), float(w["a"][-1, 1])
        t95 = float(t[np.argmax(w["a"][:, 0] > 0.95)])
        x0 = 3.0
        bars = VGroup()
        for i, (v, col, name) in enumerate(((1.2, A_COL, r"A: \ 1.2"), (1.0, B_COL, r"B: \ 1.0"))):
            b = Rectangle(width=0.7, height=1.3 * v, stroke_width=0, fill_color=col, fill_opacity=0.9)
            b.move_to([x0 + 1.1 * i, 0.9 + 1.3 * v / 2, 0])
            bars.add(VGroup(b, label(name, font_size=24, color=col).next_to(b, UP, buff=0.08)))
        bars_l = label(r"the inputs", font_size=24, color=GREY_A).next_to(bars, DOWN, buff=0.12)
        side = VGroup(
            wrapped_label(rf"after {t95:.0f} ms: \ A near {fa:.2f}, \ B near {fb:.2f}", 4.8, 28, WHITE),
            wrapped_label(r"swap the inputs, and B wins", 4.8, 26, GREY_A),
            wrapped_label(r"winner-take-all: \ a graded comparison becomes a choice", 4.8, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.3, -1.6, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "Give A an input of 1.2 and B an input of 1.0. <bookmark mark='a'/> Both start to rise. A rises a "
            "little faster. That pushes B down a little, which frees A to rise more, which pushes B down "
            f"further. <bookmark mark='b'/> Within {t95:.0f} milliseconds A is close to {fa:.2f}, and B is "
            "at nearly zero. A difference of twenty percent going in. All or nothing coming out. "
            "<bookmark mark='c'/> Swap the inputs, and B wins instead. <bookmark mark='d'/> This is called a "
            "winner-take-all circuit. It turns a graded comparison into a choice. And that's something a "
            "brain has to do all the time. You reach for one cup, not for the average of two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(bars), FadeIn(bars_l))
            vo.wait_until("a")
            self.play(Create(ra), Create(rb), run_time=7.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(bars[0].animate.move_to(bars[1].get_center()).align_to(bars[1], DOWN),
                      bars[1].animate.move_to(bars[0].get_center()).align_to(bars[0], DOWN), FadeOut(ra), FadeOut(rb),
                      FadeIn(side[1]), run_time=1.2)
            self.play(Create(sa), Create(sb), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def holds(self):
        w = load("wta")
        head = heading(r"Take the evidence away: \ the choice stays")
        t = w["t"]
        A = axes([0, 600], [0, 1.08], x_length=6.6, y_length=4.0, xticks=[0, 150, 300, 450, 600], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time (ms)", ylabel=r"activity", center=[-3.3, -0.7, 0])
        ax = A.ax
        sw = w["switch"]
        cut = DashedLine(ax.c2p(sw, 0), ax.c2p(sw, 1.08), color=THRESH, stroke_width=2.5)
        cut_l = label(r"the two inputs made equal", font_size=22, color=THRESH).next_to(ax.c2p(sw, 0.55), RIGHT,
                                                                                         buff=0.1)
        ha, hb = trace(ax, t, w["held"][:, 0], A_COL), trace(ax, t, w["held"][:, 1], B_COL)
        la = DashedVMobject(curve(ax, t, w["loose"][:, 0], A_COL, stroke_width=2.5), num_dashes=70)
        lb = DashedVMobject(curve(ax, t, w["loose"][:, 1], B_COL, stroke_width=2.5), num_dashes=70)
        with_l = label(r"with the loops", font_size=22, color=A_COL).next_to(ax.c2p(600, w["held"][-1, 0]), DL, buff=0.1)
        without_l = label(r"without them (dashed)", font_size=22, color=GREY_A).next_to(
            ax.c2p(600, w["loose"][-1, 0]), UL, buff=0.1)
        g = pair([4.1, 1.45, 0], r=0.45, gap=2.3)
        side = VGroup(
            wrapped_label(r"the evidence for A is gone, \ and A stays on", 4.8, 27, WHITE),
            wrapped_label(r"without self-excitation the two drift back together", 4.8, 27, GREY_A),
            wrapped_label(r"a memory held in activity that keeps itself going: \ quick to write, easy to erase",
                          4.8, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.2, -1.5, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "Now the interesting part. Run it again, <bookmark mark='a'/> and at a hundred and fifty "
            "milliseconds make the two inputs equal. The evidence that favoured A is gone. "
            "<bookmark mark='b'/> A stays on. B stays off. The circuit goes on holding its choice, with "
            "nothing in its input to say which it chose. <bookmark mark='c'/> Take away the self-excitation, "
            "and it can't. The two units drift back to the same level, and the choice is lost. "
            "<bookmark mark='d'/> So the loops are doing the remembering. Not a changed synapse this time. "
            "Activity that keeps itself going. That's a second kind of memory, quick to write and easy to "
            "erase. When we get to working memory, in Part 19, this is the mechanism on the table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cut_l))
            self.play(Create(ha), Create(hb), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(with_l), FadeIn(side[0]), Indicate(g.loops, color=WHITE, scale_factor=1.15))
            vo.wait_until("c")
            self.play(FadeOut(g.loops), Create(la), Create(lb), FadeIn(without_l), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(g.loops), FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def slow(self):
        w = load("wta")
        head = heading(r"Harder choices take longer")
        A = axes([0, 6.6], [0, 130], x_length=7.4, y_length=4.2, xticks=[], yticks=[0, 50, 100],
                 xlabel=r"difference between the two inputs", ylabel=r"time to decide (ms)", center=[-2.8, -0.6, 0])
        ax = A.ax
        bars = VGroup()
        for i, (dv, tm) in enumerate(zip(w["diffs"], w["times"])):
            b = Rectangle(width=0.75, height=np.linalg.norm(ax.c2p(0, tm) - ax.c2p(0, 0)), stroke_width=0,
                          fill_color=MODEL, fill_opacity=0.85).move_to(ax.c2p(0.8 + i, tm / 2))
            bars.add(VGroup(b, label(rf"{dv:g}", font_size=24, color=GREY_A).next_to(ax.c2p(0.8 + i, 0), DOWN, buff=0.12),
                            label(rf"{tm:.0f}", font_size=24, color=MODEL).next_to(b, UP, buff=0.06)))
        side = VGroup(
            wrapped_label(rf"a clear difference: \ {w['times'][-1]:.0f} ms", 4.4, 28, WHITE),
            wrapped_label(rf"a difference of {w['diffs'][0]:g}: \ {w['times'][0]:.0f} ms", 4.4, 28, WHITE),
            wrapped_label(r"People do the same: \ harder discriminations take more time (Part 1). \ A model of "
                          r"why, tested against reaction times: \ Part 25.", 4.4, 27, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, -0.4, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "One more property, and it's the one a psychologist cares about. How long does the circuit take "
            f"to decide? <bookmark mark='a'/> When the two inputs differ a lot, {w['times'][-1]:.0f} "
            "milliseconds. As the difference shrinks, the decision takes longer and longer. "
            f"<bookmark mark='b'/> For the smallest difference here, {w['times'][0]:.0f} milliseconds. The "
            "two units start close together, and it takes time for one to pull clear. <bookmark mark='c'/> "
            "People do the same. In Part 1 we measured that harder discriminations take more time, and we "
            "couldn't say why. Here's a candidate reason. Part 25 turns it into a model of deciding, and "
            "tests it against the reaction times of people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in reversed(bars)], lag_ratio=0.5), run_time=5.0)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=WHITE, scale_factor=1.05), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()
