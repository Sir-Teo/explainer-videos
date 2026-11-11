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
            label('feed an optimal prefix-free machine an infinite fair coin stream; a halting prefix may never appear',
                  font_size=22, color=WHITE),
            label(r"the programs are \textbf{prefix-free} \ (none is the start of another), \ so the "
                  r"probabilities add to at most 1 \ (Kraft)", font_size=22, color=GREY_A),
            label(r"$\Omega$ is the chance the program you get eventually halts: \ a single real number between 0 "
                  r"and 1", font_size=22, color=DATA),
            label(r"it can be approached \textbf{from below}: \ run every program, \ add $2^{-|p|}$ each time one "
                  r"halts", font_size=22, color=YES),
            label('no uniform computable convergence modulus for arbitrary precision; particular finite prefixes may be certified', font_size=22, color=NO),
        ).arrange(DOWN, buff=0.28).next_to(eq, DOWN, buff=0.45)
        with self.voiceover(
            "Fix an optimal prefix-free machine U. <bookmark mark='a'/> Feed it an infinite fair coin stream. A finite halting program prefix may eventually appear; some streams never yield one. <bookmark mark='b'/> Its halting domain is prefix-free, so Kraft's inequality bounds the total cylinder measure by one. <bookmark mark='c'/> Omega is that halting measure, strictly between zero and one for this optimal machine. <bookmark mark='d'/> Dovetail all finite programs and add each halting program's weight once. This gives computable increasing lower approximations. <bookmark mark='e'/> There is no uniform computable convergence modulus providing every requested precision. This does not rule out certifying particular finite prefixes for specially analyzed machines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def ours(self):
        o = load("omega")
        head = label('An exactly classified FINITE SAMPLE, with sampling uncertainty', font_size=32).to_edge(UP, buff=0.3)
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
            label(rf"longest: {o['longest']} steps; iid Wilson 95\%: \\ {{}}[{o['wilson95'][0]:.3f}, {o['wilson95'][1]:.3f}]", font_size=19, color=GREY_A),
            label('S(3)=21 classifies this SAMPLE; \\\\ 2251/5000 is not a population census',
                  font_size=19, color=YES),
            label(r"for a universal machine there is \\ \textbf{no} such bound: \ that would be \\ the busy beaver of "
                  r"every size", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Our finite experiment is a sample fraction, distinct from universal Omega. <bookmark mark='a'/> Draw five thousand independent uniform six-rule, three-state two-symbol machines with replacement, and retain every machine and halt time. <bookmark mark='b'/> Two thousand, two hundred and fifty-one halt: the exact SAMPLE fraction is zero point four five zero two. The population has sixteen to the sixth machines; this sample is not a census. <bookmark mark='c'/> The longest observed halting run takes eleven steps. <bookmark mark='d'/> Independent tape replay through the known bound S of three equals twenty-one classifies every sampled machine, matching the two-thousand-step runs. The displayed Wilson interval describes sampling uncertainty under the iid model. <bookmark mark='e'/> For universal Omega there is no computable all-length halting-time bound. Finite model certainty does not transfer to universal halting measure."
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
            label('given $a=2^{-n}\\lfloor2^n\\Omega\\rfloor$: enumerate until partial sum $q_s\\ge a$', font_size=21, color=WHITE),
            label(r"any program of $\le n$ bits still running then \textbf{never halts}: \ its $2^{-n}$ would push "
                  r"the sum past $\Omega$", font_size=21, color=DATA),
            label('enough bits decide any fixed encoded program; required bit count depends on $U$ and the encoding',
                  font_size=21, color=YES),
            label('optimal PREFIX-FREE complexity: $K(\\Omega\\upharpoonright n)\\ge n-O(1)$; distinct from plain $C$', font_size=21,
                  color=HEAD),
            label('effective sound arithmetic $T$: finitely many bits; Solovay special $U$ requires ZFC soundness hypotheses', font_size=21, color=NO),
        ).arrange(DOWN, buff=0.27).next_to(btl, DOWN, buff=0.45)
        with self.voiceover(
            "Omega depends on the chosen optimal prefix-free machine. <bookmark mark='a'/> Calude, Dinneen and Shu analyzed one particular machine and certified a finite prefix. This is not a uniform algorithm for arbitrary precision or arbitrary machines. <bookmark mark='b'/> Given the first n bits, let a be their dyadic truncation. Dovetail programs until the partial sum is AT LEAST a. Equality is sufficient if reached; insisting on equality alone could miss an overshoot. <bookmark mark='c'/> The remaining mass is then less than two to the minus n. Any still-running program of at most n bits can never halt. <bookmark mark='d'/> With enough bits this settles any particular effectively encoded finite program's halting, including the displayed conjecture-search examples. No machine-independent few-thousand-bit budget is claimed. <bookmark mark='e'/> Its prefixes satisfy optimal PREFIX-FREE complexity K at least n minus a constant, distinct from the preceding chapter's plain C. <bookmark mark='f'/> An effective sound arithmetic theory determines only finitely many bits. Solovay's special-machine result also has soundness conditions on ZFC; it is not an unconditional claim about an arbitrary formal theory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bt), FadeIn(btl))
            for mk, ln in zip("bcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
