from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

F_COL, E_COL = EXC, DATA


def half_centres(center, r=0.5, gap=2.6):
    c = np.asarray(center, float)
    f = unit("F", r, F_COL, 30).move_to(c + LEFT * gap / 2)
    e = unit("E", r, E_COL, 30).move_to(c + RIGHT * gap / 2)
    inh = VGroup(inhibit(f.get_right() + UP * 0.15, e.get_left() + UP * 0.15),
                 inhibit(e.get_left() + DOWN * 0.15, f.get_right() + DOWN * 0.15))
    g = VGroup(f, e, inh)
    g.f, g.e, g.inh = f, e, inh
    return g


class Rhythm(VoiceoverScene):
    def construct(self):
        self.card()
        self.brown()
        self.model()
        self.tuning()

    def card(self):
        card = chapter_card(9, r"A circuit that keeps time", r"Where does the rhythm of walking come from?",
                            lit={1911: r"Graham Brown's half-centres"}, part=PART, scale=("circuit",),
                            marr=("how",))
        with self.voiceover(
            "Chapter nine. A circuit that keeps time."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def brown(self):
        head = heading(r"1911: \ a spinal cord that steps by itself")
        cord = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.5, color=GREY_B, stroke_width=3,
                                fill_color="#111722", fill_opacity=1).move_to([-2.9, 0.2, 0])
        cord_l = label(r"spinal cord", font_size=24, color=GREY_B).next_to(cord, UP, buff=0.1).shift(LEFT * 1.4)
        brain = Line(cord.get_top() + RIGHT * 0.9, cord.get_top() + RIGHT * 0.9 + UP * 1.2, color=VOLT, stroke_width=5)
        brain_l = label(r"from the brain", font_size=24, color=VOLT).next_to(brain.get_end(), RIGHT, buff=0.15)
        sense = Line(cord.get_left() + LEFT * 1.5 + DOWN * 0.4, cord.get_left() + DOWN * 0.4, color=VOLT,
                     stroke_width=5)
        sense_l = wrapped_label(r"sensation from the legs", 1.7, 24, VOLT).next_to(sense, UP, buff=0.12)
        keep_in_frame(sense_l)

        def cross(at):
            return VGroup(Line(at + UL * 0.2, at + DR * 0.2, color=BAD, stroke_width=6),
                          Line(at + UR * 0.2, at + DL * 0.2, color=BAD, stroke_width=6))

        cut1, cut2 = cross(brain.get_center()), cross(sense.get_center())
        g = half_centres(cord.get_center())
        outs = VGroup(*[Line(u.get_bottom(), u.get_bottom() + DOWN * 1.35, color=col, stroke_width=4)
                        for u, col in ((g.f, F_COL), (g.e, E_COL))])
        muscles = VGroup(*[RoundedRectangle(width=1.7, height=0.55, corner_radius=0.2, color=col, stroke_width=3,
                                            fill_color=col, fill_opacity=0.15).next_to(o, DOWN, buff=0)
                           for o, col in zip(outs, (F_COL, E_COL))])
        m_l = VGroup(label(r"flexor", font_size=24, color=F_COL).next_to(muscles[0], DOWN, buff=0.1),
                     label(r"extensor", font_size=24, color=E_COL).next_to(muscles[1], DOWN, buff=0.1))
        phase = ValueTracker(0.0)
        for k, m in enumerate(muscles):
            m.add_updater(lambda mob, k=k: mob.set_fill(opacity=0.12 + 0.75 * max(
                0.0, np.sin(TAU * phase.get_value() + PI * k))))
        side = VGroup(
            wrapped_label(r"Sherrington: \ walking is a chain of reflexes; \ the feel of each step triggers the "
                          r"next", 5.2, 27, GREY_A),
            wrapped_label(r"Graham Brown cuts the cord off from the brain, \ and cuts the sensory nerves from "
                          r"the legs", 5.2, 27, WHITE),
            wrapped_label(r"the muscles still take turns: \ the rhythm is made inside the cord", 5.2, 27, THRESH),
            wrapped_label(r"his proposal: \ two half-centres, each inhibiting the other", 5.2, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, -0.2, 0])
        keep_in_frame(side)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The third circuit keeps time. When you walk, the muscles that bend each leg and the muscles that "
            "straighten it take turns, about once a second, and you give it no thought. Where does the rhythm "
            "come from? <bookmark mark='a'/> Around 1900 the leading view, Charles Sherrington's, was that "
            "walking is a chain of reflexes. The feel of each step triggers the next. <bookmark mark='b'/> In "
            "1911 Thomas Graham Brown tested that, in cats. He cut the spinal cord off from the brain. And he "
            "cut the sensory nerves coming in from the legs, so that no feeling of a step could arrive. "
            "<bookmark mark='c'/> The leg muscles still contracted in alternation. Flexor, extensor, flexor, "
            "extensor. The rhythm was being made inside the spinal cord itself. <bookmark mark='d'/> And "
            "Graham Brown proposed how. Two groups of neurons, one driving the flexors and one the extensors, "
            "each inhibiting the other. He called them half-centres. The idea was ignored for half a "
            "century. It's now the starting point for how every rhythmic movement is understood."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(cord, cord_l, brain, brain_l, sense, sense_l)),
                      FadeIn(VGroup(outs, muscles, m_l)))
            self.play(phase.animate.set_value(3.0), run_time=6.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), phase.animate.set_value(5.0), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(cut1, scale=1.6), phase.animate.set_value(6.0), run_time=2.0,
                      rate_func=linear)
            self.play(FadeIn(cut2, scale=1.6), phase.animate.set_value(8.0), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), phase.animate.set_value(12.0), run_time=8.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(g), FadeIn(side[3]), phase.animate.set_value(22.0), run_time=20.0, rate_func=linear)
        self.clear_scene()

    def model(self):
        r = load("rhythm")
        head = heading(r"Mutual inhibition, plus fatigue")
        g = half_centres([-4.4, 1.9, 0], r=0.42, gap=2.1)
        drive = VGroup(*[excite(u.get_top() + UP * 0.75, u.get_top(), color=GREY_A, buff=0.05) for u in (g.f, g.e)])
        drive_l = label(r"the same steady drive to both", font_size=22, color=GREY_A).next_to(drive, RIGHT, buff=0.3)
        A = axes([0, 4], [0, 0.85], x_length=8.4, y_length=3.3, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time (s)", ylabel=r"output", center=[-2.4, -1.35, 0])
        ax = A.ax
        t = r["t"] / 1000
        y1, y2 = trace(ax, t, r["y"][:, 0], F_COL), trace(ax, t, r["y"][:, 1], E_COL)
        fat = DashedVMobject(curve(ax, t, r["fatigue"][:, 0], F_COL, stroke_width=2), num_dashes=90)
        lg = legend([(F_COL, r"unit F"), (E_COL, r"unit E"), (F_COL, r"F's fatigue (dashed)")], font_size=22)
        lg.arrange(RIGHT, buff=0.5).next_to(ax.c2p(4, 0.85), UL, buff=0.1)
        side = VGroup(
            wrapped_label(r"one gets ahead and silences the other", 4.2, 26, WHITE),
            wrapped_label(r"it tires; \ its grip loosens; \ the rested one escapes and takes over", 4.2, 26, WHITE),
            wrapped_label(rf"period: \ {r['period']:.0f} ms", 4.2, 30, THRESH),
            wrapped_label(rf"correlation between the two: \ ${r['correlation']:.2f}$", 4.2, 26, GREY_A),
            wrapped_label(r"nothing rhythmic goes in", 4.2, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([4.7, -0.6, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "Here's the circuit in Psyche. Mutual inhibition, as in the last chapter. No self-excitation this "
            "time. Instead, each unit tires: the longer it has been active, the weaker it gets. "
            "<bookmark mark='a'/> Both units receive the same steady drive. Nothing rhythmic goes in. "
            "<bookmark mark='b'/> Watch. One unit gets ahead, and silences the other. <bookmark mark='c'/> "
            "But it's tiring. Its output sags, its grip on the other loosens, and the other, which has been "
            "resting, escapes and takes over. Now it's the first one's turn to rest. <bookmark mark='d'/> And "
            f"round it goes, with a period of {r['period']:.0f} milliseconds. When one is up, the other is "
            f"down: the correlation between the two outputs is {r['correlation']:.2f}. A steady input has "
            "been turned into a rhythm, by two units and two ingredients."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in drive], lag_ratio=0.2), FadeIn(drive_l), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(y1), Create(y2), Create(fat), FadeIn(lg), FadeIn(side[0]), run_time=12.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()

    def tuning(self):
        r = load("rhythm")
        head = heading(r"What sets the tempo, \ and what kills the rhythm")
        A = axes([0, 1000], [0, 2200], x_length=4.6, y_length=3.0, xticks=[0, 300, 600, 900], yticks=[0, 1000, 2000],
                 xlabel=r"time constant of fatigue (ms)", ylabel=r"period (ms)", center=[-4.2, 0.45, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(f, p_), radius=0.08, color=THRESH) for f, p_ in zip(r["fatigues"], r["periods"])])
        ln = trace(ax, r["fatigues"], r["periods"], THRESH, 2.5)
        B = axes([0, 4], [0, 0.85], x_length=4.6, y_length=3.0, xticks=[0, 2, 4], yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"time (s)", ylabel=r"output, with weak inhibition",
                 center=[1.3, 0.45, 0])
        bx = B.ax
        t = r["t"] / 1000
        q1, q2 = trace(bx, t, r["quiet"][:, 0], F_COL), trace(bx, t, r["quiet"][:, 1] + 0.006, E_COL)
        cond = MathTex(rf"{r['lo']:.2f} \;<\; a \;<\; {r['hi']:.1f}", font_size=34, color=INH)
        cond_g = VGroup(label(r"it alternates only if the inhibition $a$ is strong enough, and not too strong:",
                              font_size=24, color=GREY_A), cond).arrange(RIGHT, buff=0.3)
        cond_g.next_to(VGroup(A, B), DOWN, buff=0.25)
        keep_in_frame(cond_g)
        side = VGroup(
            label(r"central pattern generators", font_size=28, color=P.ACCENT),
            label(r"walking, \ swimming", font_size=26, color=WHITE),
            label(r"breathing, \ chewing", font_size=26, color=WHITE),
            wrapped_label(r"the brain says go, and how fast; \ the cord makes the rhythm", 3.0, 25, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([5.5, 0.7, 0])
        keep_in_frame(side)
        motif = wrapped_label(r"one motif, three behaviours: \ inhibit your neighbours (edges), \ add "
                              r"self-excitation (a choice held), \ add fatigue (a rhythm)", 10.2, 27, P.ACCENT)
        motif.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        tag = psyche_tag()
        with self.voiceover(
            "Two questions about this circuit. First, what sets the tempo? <bookmark mark='a'/> The fatigue "
            f"does. Make the units tire quickly, and a full cycle takes {r['periods'][0]:.0f} milliseconds. Make "
            f"them tire slowly, and the period stretches to {r['periods'][-1] / 1000:.0f} seconds. "
            "<bookmark mark='b'/> Second, what kills the rhythm? Weaken the inhibition, and there's nothing "
            "to make them take turns. Both units settle at the same steady level. The alternation needs the "
            "inhibition to be strong enough, though not so strong that one unit wins for good. "
            "<bookmark mark='c'/> Circuits of this kind are called central pattern generators, and they run "
            "walking, swimming, breathing and chewing. The brain tells them to go, and how fast. It doesn't "
            "have to send the rhythm. <bookmark mark='d'/> Now look back over three chapters. Inhibit your "
            "neighbours, and you sharpen edges. Add self-excitation, and you hold a choice. Add fatigue "
            "instead, and you keep time. One motif, three behaviours. That's what a circuit is: the same "
            "cells, doing different things because of how they're wired."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(d, scale=1.5) for d in pts], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(B))
            self.play(Create(q1), Create(q2), run_time=3.0, rate_func=linear)
            self.play(FadeIn(cond_g))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in side], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("d")
            self.play(FadeIn(motif, shift=UP * 0.1))
        self.clear_scene()
