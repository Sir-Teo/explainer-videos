from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Spike(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.all_or_none()
        self.refractory()

    def card(self):
        card = chapter_card(6, r"The action potential, computed", r"What do the four equations do when they are "
                            r"let go?", lit=(), part=PART, scale=("neuron",), marr=("how",))
        with self.voiceover(
            "Chapter six. The action potential, computed."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def anatomy(self):
        d = load("spike")
        t = np.asarray(d["t"])
        keep = t <= 12
        t = t[keep]
        head = heading(r"One nerve signal, and what each gate is doing")
        A1 = axes([0, 12], [-90, 60], x_length=7.4, y_length=2.5, xticks=[], yticks=[-80, -40, 0, 40],
                  ylabel=r"membrane potential (mV)", center=[-2.5, 1.3, 0], font_size=19)
        A2 = axes([0, 12], [0, 36], x_length=7.4, y_length=1.9, xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 15, 30],
                  xlabel=r"time (ms)", ylabel=r"conductance", center=[-2.5, -1.95, 0], font_size=19)
        ax1, ax2 = A1.ax, A2.ax
        v = curve(ax1, t, d["v"][keep], VOLT, stroke_width=4)
        gna = curve(ax2, t, d["g_na"][keep], NA, stroke_width=4)
        gk = curve(ax2, t, d["g_k"][keep], K, stroke_width=4)
        ena = DashedLine(ax1.c2p(0, d["e_na"]), ax1.c2p(12, d["e_na"]), color=NA, stroke_width=2)
        ek = DashedLine(ax1.c2p(0, d["e_k"]), ax1.c2p(12, d["e_k"]), color=K, stroke_width=2)
        bat = VGroup(label(r"$E_{Na}$", font_size=22, color=NA).next_to(ena, RIGHT, buff=0.08),
                     label(r"$E_K$", font_size=22, color=K).next_to(ek, RIGHT, buff=0.08))
        leg = VGroup(label(r"sodium", font_size=22, color=NA).move_to(ax2.c2p(1.2, 30)),
                     label(r"potassium", font_size=22, color=K).move_to(ax2.c2p(7.2, 14)))
        steps = VGroup(
            wrapped_label(r"1. \ A push lifts the voltage a little.", 4.6, 25, THRESH),
            wrapped_label(r"2. \ Sodium gates open, fast. \ Sodium enters, the voltage rises, more gates open.",
                          4.6, 25, NA),
            wrapped_label(rf"3. \ It heads for $E_{{Na}}$ and peaks at ${d['peak']:+.0f}$ mV.", 4.6, 25, VOLT),
            wrapped_label(r"4. \ Sodium shuts itself off; \ potassium, late, opens and pulls the voltage down.",
                          4.6, 25, K),
            wrapped_label(r"5. \ Potassium is slow to close: \ the voltage dips below rest, toward $E_K$.", 4.6, 25,
                          K),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.75, -0.35, 0])
        keep_in_frame(steps)
        sweep = DashedLine(ax2.c2p(0, 0), ax1.c2p(0, 60), color=GREY_B, stroke_width=1.5)
        times = [1.25, 2.2, d["t_peak"], 3.6, 6.0]
        tag = psyche_tag()
        with self.voiceover(
            "Give the model membrane a brief push of current, and let the equations run. "
            "<bookmark mark='a'/> The top trace is the voltage. Underneath, the two conductances. Nothing was "
            "drawn by hand here; this is the solution. Let's walk through it, because every feature has a "
            "cause you already know. <bookmark mark='b'/> The push lifts the voltage by a few millivolts. "
            "<bookmark mark='c'/> The sodium gate, m, is the fast one, so it responds first. A few sodium "
            "doors open. Sodium flows in, which makes the inside more positive, which opens more sodium doors, "
            "which lets in more sodium. That's a loop that feeds itself, and the voltage takes off. "
            f"<bookmark mark='d'/> It races toward the sodium battery. It doesn't quite get there: it peaks "
            f"at plus {d['peak']:.0f} millivolts, because by now the two slow gates have caught up. "
            "<bookmark mark='e'/> The second sodium door, h, swings shut. And potassium, with its built-in "
            "delay, finally opens. Now the membrane is mostly a potassium membrane, and the voltage falls "
            "toward the potassium battery. <bookmark mark='f'/> It overshoots on the way down, because the "
            "potassium doors are slow to close again, and for a few milliseconds the cell is more negative "
            f"than it was at rest. Then everything relaxes. The whole event took about {d['width']:.0f} "
            "millisecond at half its height, and nothing in it was put in by hand except the three curves "
            "from the clamp."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2), Create(ena), Create(ek), FadeIn(bat))
            vo.wait_until("a")
            self.play(Create(v), Create(gna), Create(gk), FadeIn(leg), run_time=5.0, rate_func=linear)
            self.play(FadeIn(sweep))
            for mark, st, tt in zip("bcdef", steps, times):
                vo.wait_until(mark)
                self.play(sweep.animate.put_start_and_end_on(ax2.c2p(tt, 0), ax1.c2p(tt, 60)), FadeIn(st, shift=UP * 0.1),
                          run_time=1.2)
        self.clear_scene()

    def all_or_none(self):
        d = load("spike")
        th = d["threshold"]
        t = np.asarray(d["family_t"])
        head = heading(r"A threshold, and above it one size only")
        A = axes([0, 10], [-90, 60], x_length=6.4, y_length=3.9, xticks=[0, 2, 4, 6, 8, 10], yticks=[-80, -40, 0, 40],
                 xlabel=r"time (ms)", ylabel=r"membrane potential (mV)", center=[-3.2, -0.5, 0])
        ax = A.ax
        keep = t <= 10
        fam = VGroup(*[curve(ax, t[keep], row[keep], (LEAK if pk < 0 else MODEL), stroke_width=3)
                       for row, pk in zip(d["family"], d["family_peaks"])])
        rel = np.asarray(d["amps"]) / th
        B = axes([0, 3.2], [-80, 60], x_length=4.4, y_length=3.9, xticks=[0, 1, 2, 3], yticks=[-80, -40, 0, 40],
                 xlabel=r"size of the push (1 = threshold)", ylabel=r"peak voltage (mV)", center=[3.9, -0.5, 0],
                 font_size=20)
        dots = VGroup(*[Dot(B.ax.c2p(r_, pk), radius=0.09, color=(LEAK if pk < 0 else MODEL))
                        for r_, pk in zip(rel, d["family_peaks"])])
        thr = DashedLine(B.ax.c2p(1, -80), B.ax.c2p(1, 60), color=THRESH, stroke_width=2)
        thr_l = label(r"threshold", font_size=22, color=THRESH).move_to(B.ax.c2p(1.08, -15), aligned_edge=LEFT)
        below = int((d["family_peaks"] < 0).sum())
        end = label(r"A larger push does not make a larger signal. \ It makes the same one.", font_size=28,
                    color=P.ACCENT).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        tag = psyche_tag()
        with self.voiceover(
            "Now vary the push. <bookmark mark='a'/> Small pushes, and the voltage rises a little and sinks "
            "back. The sodium loop started, but the leak and the potassium current won the race. "
            "<bookmark mark='b'/> Push five per cent harder than a certain value and everything changes: the "
            "loop wins, and you get the full event. There's a threshold, and it's sharp. "
            "<bookmark mark='c'/> And look at what happens above it. A push one and a half times the threshold, "
            "twice, three times: the signals come a little sooner, and they're all the same height. "
            "<bookmark mark='d'/> Plot the peak against the size of the push and it isn't a slope. It's a "
            "step. This is called the all-or-none law, and physiologists had known it for decades as a brute "
            "fact about nerves. Here it's a consequence. Once the sodium loop runs away, the size of the "
            "signal is set by the batteries and the gates, and the stimulus that started it is forgotten. "
            "That has an enormous consequence for the mind. A nerve fibre can't say how strong something is "
            "by sending a bigger signal. It has only one size. We'll come back to how it copes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), Create(thr), FadeIn(thr_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in fam[:below]], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(p_) for p_ in dots[:below]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(fam[below]), FadeIn(dots[below]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c_) for c_ in fam[below + 1:]], lag_ratio=0.5),
                      LaggedStart(*[FadeIn(p_) for p_ in dots[below + 1:]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def refractory(self):
        d = load("spike")
        th = d["threshold"]
        delays, second = np.asarray(d["delays"]), np.asarray(d["second"]) / th
        ok = np.isfinite(second)
        head = heading(r"After a signal, a dead time")
        A = axes([0, 26], [0, 18], x_length=7.2, y_length=3.9, xticks=[0, 5, 10, 15, 20, 25], yticks=[1, 5, 10, 15],
                 xlabel=r"time since the first push (ms)", ylabel=r"push needed for a second signal (1 = threshold)",
                 center=[-2.7, -0.5, 0], font_size=20)
        ax = A.ax
        dead = Rectangle(width=ax.c2p(d["absolute"], 0)[0] - ax.c2p(0, 0)[0], height=3.9, stroke_width=0, fill_color=BAD,
                         fill_opacity=0.22).move_to([(ax.c2p(0, 0)[0] + ax.c2p(d["absolute"], 0)[0]) / 2, ax.c2p(0, 9)[1], 0])
        dead_l = label(r"no push is enough", font_size=22, color=BAD).move_to(dead).rotate(PI / 2)
        line = curve(ax, delays[ok], np.minimum(second[ok], 18), THRESH, stroke_width=4)
        pts = VGroup(*[Dot(ax.c2p(x, min(y, 18)), radius=0.08, color=THRESH) for x, y in zip(delays[ok], second[ok])])
        base = DashedLine(ax.c2p(0, 1), ax.c2p(26, 1), color=GREY_B, stroke_width=2)
        side = VGroup(
            wrapped_label(rf"For about {d['absolute']:.0f} ms: \ nothing. \ The second sodium door, $h$, is still "
                          r"shut, and potassium is still open.", 4.6, 26, BAD),
            wrapped_label(r"Then a second signal is possible, at a price that falls back to normal.", 4.6, 26, THRESH),
            wrapped_label(r"So signals cannot merge, cannot pile up, and cannot turn round.", 4.6, 26, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.75, -0.2, 0])
        keep_in_frame(side)
        tag = note(rf"computed by Psyche at $6.3^\circ$C, the first push twice threshold").to_corner(DR, buff=0.2)
        with self.voiceover(
            "One more property falls out, and it matters as much as the threshold. Fire the membrane once, "
            "and then ask how hard you have to push to fire it again. <bookmark mark='a'/> For the first few "
            "milliseconds the answer is that you can't. No push is big enough. The second sodium door is "
            "still shut, so there's no sodium loop to start, and the potassium doors are still open, holding "
            "the voltage down. This is the absolute refractory period. <bookmark mark='b'/> After that a "
            "second signal can be had, but it costs more: many times the normal push at first, then less and "
            "less, as h recovers and potassium closes. That's the relative refractory period. "
            "<bookmark mark='c'/> Three things follow. A nerve signal is a separate event; two of them can "
            "never merge into one. A fibre has a top speed, a few hundred signals a second. And, as you'll "
            "see in a moment, a signal travelling along an axon can't turn round and go back, because the "
            "stretch it has just left is dead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(base))
            vo.wait_until("a")
            self.play(FadeIn(dead), FadeIn(dead_l), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(pts, lag_ratio=0.1), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()
