from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono)


def regfile(color, title, vals=None, cw=0.66, ch=0.46):
    cells = VGroup()
    names = ["ra", "sp", "a0", "a1", "a2", "a3", "a4", "a5", "t0", "t1", "t2", "t3", "s0", "s1", "s2", "pc"]
    for i, n in enumerate(names):
        r = Rectangle(width=cw, height=ch, stroke_color=color, stroke_width=1.2, fill_color=color,
                      fill_opacity=0.18)
        t = mono(n, 16, WHITE).move_to(r)
        cells.add(VGroup(r, t))
    cells.arrange_in_grid(rows=2, cols=8, buff=0.03)
    t = label(title, font_size=22, color=color).next_to(cells, UP, buff=0.12)
    return VGroup(t, cells)


class Switch(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanics()
        self.measured()

    def card(self):
        card = chapter_card(5, r"The context switch", r"What does it cost to change programs?",
                            lit=(1961,), extra=((1961, r"CTSS: \ swap to the drum"),), part=PART)
        with self.voiceover("Chapter five. The context switch."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def mechanics(self):
        d = load("switch")
        head = label(r"Switching from A to B", font_size=36).to_edge(UP, buff=0.3)
        cpu = regfile(YES, r"the processor's registers").move_to([0, 1.5, 0])
        pa = regfile(DATA, r"A's PCB").move_to([-3.55, -0.8, 0])
        pb = regfile(HEAD, r"B's PCB").move_to([3.55, -0.8, 0])
        down = Arrow(cpu.get_bottom() + LEFT * 0.8, pa.get_top() + RIGHT * 0.5, buff=0.1, color=DATA, stroke_width=3)
        up = Arrow(pb.get_top() + LEFT * 0.5, cpu.get_bottom() + RIGHT * 0.8, buff=0.1, color=HEAD, stroke_width=3)
        dl = label(r"1. \ trap: \ save A", font_size=22, color=DATA).next_to(down, LEFT, buff=0.1)
        ul = label(r"3. \ restore B, \ \texttt{eret}", font_size=22, color=HEAD).next_to(up, RIGHT, buff=0.1)
        mid = label(r"2. \ the scheduler \\ picks B", font_size=22, color=KERN).move_to([0, -1.75, 0])
        lines = VGroup(
            label(rf"PebbleOS: \ {d['saved_words']} words per process \ (15 registers, \ pc, \ bounds); \ a switch "
                  rf"through \texttt{{yield}} takes {d['kernel_per_switch']:.0f} kernel instructions", font_size=21,
                  color=WHITE),
            label(r"a real kernel also saves floating-point and vector registers \ (2 KiB with AVX-512), \ and "
                  r"switches the address space \ (Part 32)", font_size=21, color=GREY_A),
            label(r"the process never notices: \ it resumes at the same instruction, \ with the same registers",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "To switch from process A to process B, the kernel does three things. <bookmark mark='a'/> A trap "
            "brings it in, from the timer or a system call, and it saves A's registers and program counter in A's "
            "process control block. <bookmark mark='b'/> The scheduler chooses B. <bookmark mark='c'/> Then the "
            "kernel loads B's saved registers, sets B's bounds, and returns with e-ret, into B, at exactly the "
            "instruction where B was stopped last time. <bookmark mark='d'/> In PebbleOS that is eighteen words per "
            "process, and a switch through yield costs a hundred and eighteen kernel instructions. <bookmark "
            "mark='e'/> A real kernel saves more: the floating-point and vector registers, two kibibytes of them on "
            "a processor with AVX-512, and it changes the address space, which is Part 32's subject. <bookmark "
            "mark='f'/> And neither process can tell. Each resumes with its registers exactly as it left them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cpu), FadeIn(pa), FadeIn(pb))
            vo.wait_until("a")
            self.play(GrowArrow(down), FadeIn(dl), Indicate(cpu[1], color=DATA))
            vo.wait_until("b")
            self.play(FadeIn(mid))
            vo.wait_until("c")
            self.play(GrowArrow(up), FadeIn(ul), Indicate(pb[1], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
            vo.wait_until("f")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("switch")
        head = label(r"Measured: \ a byte bounced between two processes", font_size=34).to_edge(UP, buff=0.3)
        A = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.12, stroke_color=DATA, fill_color=BG,
                             fill_opacity=1).move_to([-3.2, 1.4, 0])
        B = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.12, stroke_color=HEAD, fill_color=BG,
                             fill_opacity=1).move_to([3.2, 1.4, 0])
        la = label(r"parent", font_size=26, color=DATA).move_to(A)
        lb = label(r"child", font_size=26, color=HEAD).move_to(B)
        p1 = Arrow(A.get_right() + UP * 0.18, B.get_left() + UP * 0.18, buff=0.1, color=GREY_B, stroke_width=2.5)
        p2 = Arrow(B.get_left() + DOWN * 0.18, A.get_right() + DOWN * 0.18, buff=0.1, color=GREY_B, stroke_width=2.5)
        pl = label(r"two pipes: \ write a byte, \ wait for it back", font_size=21, color=GREY_B).next_to(p1, UP, buff=0.14)
        ball = Dot(A.get_right() + UP * 0.18, color=YES, radius=0.08)
        same, cross = d["same_cpu_ns"] / 1000, d["cross_cpu_ns"] / 1000
        rows = VGroup(
            label(rf"both on one processor: \ {same:.1f} $\mu$s a round trip \ (two switches, \ four system calls)",
                  font_size=22, color=YES),
            label(rf"on two processors: \ {cross:.1f} $\mu$s: \ the other core must be woken \ (an interrupt "
                  r"between processors)", font_size=22, color=NO),
            label(r"the hidden cost comes after: \ B finds the caches full of A's data \ (Part 9), \ and refills them",
                  font_size=22, color=WHITE),
            label(r"so schedulers try not to switch too often: \ the quantum \ (chapter 8)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(VGroup(A, B), DOWN, buff=0.8)
        with self.voiceover(
            "How long does a switch take on a real machine? The standard experiment: two processes joined by two "
            "pipes, bouncing one byte back and forth. <bookmark mark='a'/> Each must block until the other answers, "
            "so every round trip forces two context switches and four system calls. <bookmark mark='b'/> With both "
            "processes on one processor, a round trip takes two point nine microseconds. <bookmark mark='c'/> With "
            "the processes on different processors it is much slower, twenty-five microseconds here, because the "
            "other core has gone to sleep and must be woken by an interrupt between processors, and on a virtual "
            "machine that is expensive. <bookmark mark='d'/> And the largest cost is often invisible in this "
            "measurement: the incoming process finds the caches full of the other one's data, and runs slowly until "
            "it has refilled them. <bookmark mark='e'/> So a scheduler should not switch more often than it must. "
            "How often it must is the question of the quantum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb), GrowArrow(p1), GrowArrow(p2),
                      FadeIn(pl))
            vo.wait_until("a")
            for _ in range(2):
                self.play(ball.animate.move_to(B.get_left() + UP * 0.18), run_time=0.5)
                ball.move_to(B.get_left() + DOWN * 0.18)
                self.play(ball.animate.move_to(A.get_right() + DOWN * 0.18), run_time=0.5)
                ball.move_to(A.get_right() + UP * 0.18)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()
