from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, words)


class Omega(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.ours()
        self.oracle()

    def card(self):
        card = chapter_card(11, r"Chaitin's $\Omega$", r"What is the probability that a program halts?", lit=(1975,),
                            extra=((1975, r"Chaitin"),), part=PART)
        with self.voiceover("Chapter eleven. Chaitin's Omega."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def definition(self):
        head = label(r"The halting probability", font_size=34).to_edge(UP, buff=0.35)
        eq = MathTex(r"\Omega \;=\; \sum_{p \text{ halts}} 2^{-|p|}", font_size=48, color=HEAD).next_to(head, DOWN,
                                                                                                    buff=0.4)
        lines = VGroup(
            label(r"choose a program by \textbf{tossing a coin} for each bit, \ until the bits spell a whole program",
                  font_size=22, color=WHITE),
            label(r"the programs are \textbf{prefix-free} \ (none is the start of another), \ so the "
                  r"probabilities add to at most 1 \ (Kraft)", font_size=22, color=GREY_A),
            label(r"$\Omega$ is the chance the program you get eventually halts: \ a single real number between 0 "
                  r"and 1", font_size=22, color=DATA),
            label(r"it can be approached \textbf{from below}: \ run every program, \ add $2^{-|p|}$ each time one "
                  r"halts", font_size=22, color=YES),
            label(r"but you can never know how close you are", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.28).next_to(eq, DOWN, buff=0.45)
        with self.voiceover(
            "In 1975 Chaitin packed the halting problem into a single number. <bookmark mark='a'/> Pick a program "
            "at random by tossing a coin for each bit, until the bits spell out a complete program. <bookmark "
            "mark='b'/> If no program is the beginning of another, these probabilities add up to at most one. "
            "<bookmark mark='c'/> Omega is the probability that the program you get eventually halts: one real "
            "number between zero and one. <bookmark mark='d'/> You can approach it from below. Run every program "
            "side by side, and each time one halts, add its probability. <bookmark mark='e'/> The sums climb "
            "toward Omega, but nothing ever tells you how close you are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def ours(self):
        o = load("omega")
        head = label(r"A halting probability we can compute", font_size=32).to_edge(UP, buff=0.3)
        rows = o["rows"]
        ax = Axes(x_range=[0, 11.5, 1], y_range=[0, 0.5, 0.1], x_length=5.4, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5).to_edge(
            LEFT, buff=1.2)
        xs = [np.log2(r["t"]) for r in rows]
        ys = [r["fraction"] for r in rows]
        pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
        path = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.05, color=HEAD) for p in pts])
        xt = VGroup(*[label(str(r["t"]), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for x, r in zip(xs, rows) if r["t"] in (1, 4, 16, 64, 512, 2000)])
        yt = VGroup(*[label(f"{v:.1f}", font_size=15, color=GREY_A).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.1, 0.2, 0.3, 0.4, 0.5)])
        xl = label(r"step budget $t$ \ (log scale)", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yl = label(r"fraction halted", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.55)
        final = rows[-1]["fraction"]
        asym = DashedLine(ax.c2p(0, final), ax.c2p(11.5, final), color=YES, stroke_width=1.5)
        al = label(rf"{final:.4f}", font_size=18, color=YES).next_to(asym, UP, buff=0.05).align_to(asym, RIGHT)
        r16 = next(r for r in rows if r["t"] == 16)["fraction"]
        notes = VGroup(
            label(rf"{words(o['N'])} random 3-state machines \\ (each rule: \ a random write, \ move, \\ and next "
                  r"state or halt)", font_size=19, color=WHITE),
            label(rf"by 16 steps: \ {r16:.4f}; \ by 2,000: \ the same", font_size=19, color=HEAD),
            label(rf"longest halting run seen: \ {o['longest']} steps", font_size=19, color=GREY_A),
            label(r"why is this \textbf{exact}? \ BB(3): \\ every halting 3-state machine \\ stops within 21 steps",
                  font_size=19, color=YES),
            label(r"for a universal machine there is \\ \textbf{no} such bound: \ that would be \\ the busy beaver of "
                  r"every size", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "We cannot compute Omega, but we can compute a small cousin. <bookmark mark='a'/> Draw five thousand "
            "random Turing machines with three states, each rule choosing at random what to write, which way to "
            "move, and whether to go to another state or halt. Run each with a growing budget of steps, and count "
            "the fraction that has halted. <bookmark mark='b'/> It climbs, quickly at first. By sixteen steps it "
            "reaches forty-five percent, and after two thousand steps it has not moved. <bookmark mark='c'/> The "
            "longest halting run we saw was eleven steps. <bookmark mark='d'/> Here we know the curve is finished, "
            "because of Part 1: the three-state busy beaver runs twenty-one steps, so any three-state machine "
            "still running after twenty-one never stops. <bookmark mark='e'/> For a universal machine no such "
            "bound exists. Knowing when the curve was finished would mean knowing the busy beaver at every size."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(path), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15), run_time=2.5)
            self.play(Create(asym), FadeIn(al), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def oracle(self):
        head = label(r"The first $n$ bits of $\Omega$ decide every $n$-bit program", font_size=32).to_edge(UP,
                                                                                                   buff=0.35)
        bits = "0." + "0000001000000100000110001000011010001111110010111011101000010000"  # arXiv nlin/0112022
        bt = mono(r"Omega_U = " + bits + "...", 20, HEAD).next_to(head, DOWN, buff=0.4)
        btl = label(r"the first 64 bits of one universal machine's $\Omega$, \ as computed by Calude, \ Dinneen and "
                    r"Shu \ (2002)", font_size=18, color=GREY_A).next_to(bt, DOWN, buff=0.12)
        lines = VGroup(
            label(r"given $\Omega_n$, \ its first $n$ bits: \ run all programs side by side \ until the halted ones "
                  r"add up to $\Omega_n$", font_size=21, color=WHITE),
            label(r"any program of $\le n$ bits still running then \textbf{never halts}: \ its $2^{-n}$ would push "
                  r"the sum past $\Omega$", font_size=21, color=DATA),
            label(r"so $\Omega$'s bits answer Goldbach, \ Riemann, \ Con(ZFC): \ each is one short program's halting",
                  font_size=21, color=YES),
            label(r"$\Omega$ is \textbf{random}: \ its first $n$ bits have complexity $\ge n - c$", font_size=21,
                  color=HEAD),
            label(r"a sound theory determines only finitely many bits \ (Chaitin); \ for some $U$, \ ZFC can't "
                  r"determine \textbf{any} \ (Solovay, 2000)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.27).next_to(btl, DOWN, buff=0.45)
        with self.voiceover(
            "Omega is a strange number. <bookmark mark='a'/> Cristian Calude, Michael Dinneen and Chi-Kou Shu "
            "computed the first sixty-four bits for one particular universal machine in 2002. For larger machines, "
            "nobody can. Here is why. <bookmark mark='b'/> Suppose you knew the first n bits. Run every program "
            "side by side, adding up the probabilities of those that halt, until the sum reaches those n bits. "
            "<bookmark mark='c'/> Any program of n bits or fewer that is still running then can never halt: if it "
            "did, its contribution would push the total past Omega. <bookmark mark='d'/> So a few thousand bits of "
            "Omega would settle Goldbach's conjecture, the Riemann hypothesis and the consistency of set theory, "
            "each the halting of one short program. <bookmark mark='e'/> It follows that Omega is random: its first "
            "n bits cannot be compressed by more than a constant. <bookmark mark='f'/> And by chapter ten, a sound "
            "theory can determine only finitely many of its bits. Robert Solovay found a universal machine for "
            "which set theory cannot determine even one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bt), FadeIn(btl))
            for mk, ln in zip("bcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
