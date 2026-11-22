from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.nines()
        self.isolation()

    def card(self):
        self.chapter(13, r"Frontier: \ scheduling, \ isolation and energy", r"How close to optimal can a cloud run?", lit=(2015, 2020), extra=((2015, r"Borg described"), (2020, r"Firecracker")), part=PART, said="Chapter thirteen, the frontier. How close to optimal can a cloud run?")

    def nines(self):
        self.ask(r"Eleven nines, computed from independent failures. \\ Real durability is set by...",
                 [r"the same independent failures", r"correlated failures"], 1,
                 say="Eleven nines of durability, computed from independent disk failures. What really decides durability?",
                 reveal="Correlated failures: a bad batch of disks, a power event, a software bug.")
        d = load("durability")
        c = load("correlated")
        rs = next(r for r in d["schemes"] if r["name"] == "RS(10, 4)")
        head = label(r"Where the nines go", font_size=36).to_edge(UP, buff=0.3)
        vals = [(r"independent fragment failures", rs["nines"], YES),
                (r"whole racks failing, \ fragments spread two per rack", -math.log10(c["p_loss_year_spread"]), HEAD),
                (r"all fragments in one rack", -math.log10(c["p_loss_year_one_rack"]), NO)]
        bars = VGroup()
        for k, (t, v, col) in enumerate(vals):
            w = v / 14 * 8.0
            b = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-3.2 + w / 2, 1.3 - 1.0 * k, 0])
            bars.add(VGroup(b, label(rf"{v:.1f} nines", font_size=20, color=col).next_to(b, RIGHT, buff=0.15),
                            label(t, font_size=18, color=GREY_A).next_to(b, UP, buff=0.08).align_to(b, LEFT)))
        lines = VGroup(
            wrapped_label(r"the same code, \ RS(10, 4), \ under three failure models \ (chapter 8's Markov model, \ "
                          r"and a rack model: \ each rack fails once in twenty years and takes a day to repair)", 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(r"correlated failures \ --- \ a rack, \ a power feed, \ a bad firmware push, \ a software bug "
                          r"in every replica \ --- \ dominate every real durability budget; \ measuring and modelling "
                          r"them is open", 12.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Chapter eight derived durability from independent failures. The frontier is what that assumption hides. "
            f"<bookmark mark='a'/> A ten-plus-four Reed–Solomon code, with fragments failing independently, gives "
            f"about {rs['nines']:.0f} nines a year. <bookmark mark='b'/> Now let whole racks fail instead, each about "
            "once in twenty years, taking a day to repair. With two fragments in each of seven racks, the data is lost only when three racks are "
            f"down at once, and durability falls to about {-math.log10(c['p_loss_year_spread']):.0f} nines. "
            "<bookmark mark='c'/> Put every fragment in one rack, and a single rack failure loses the data: barely "
            "more than one nine. <bookmark mark='d'/> Real durability is decided by correlated failures, a power "
            "feed, a firmware update pushed everywhere, a bug in every replica at once. Measuring and modelling "
            "those is still an open problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, b in zip("abc", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


    def isolation(self):
        head = label(r"Isolation, \ and trusting the machine", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"confidential computing", r"memory encrypted by the processor, \ so that even the cloud's own "
                 r"hypervisor cannot read a tenant's VM \ (AMD SEV-SNP, \ Intel TDX, \ Arm CCA); \ attested remotely",
                 YES),
            tile(r"side channels", r"tenants sharing a core, \ a cache or memory bandwidth can measure each other "
                 r"\ (Part 9, \ Part 8's Spectre); \ the defences cost performance", NO),
            tile(r"disaggregation", r"memory and accelerators pooled across a rack \ (CXL): \ fewer stranded "
                 r"resources, \ new latencies and new failure modes", KERN),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"open: \ isolation that is provable, \ cheap and complete at once \ --- \ verified "
                             r"hypervisors exist \ (seL4, \ Part 54), \ fast ones do too, \ but not yet both at cloud "
                             r"scale", 12.4, font_size=20, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Isolation is the cloud's other frontier. <bookmark mark='a'/> Confidential computing has the processor "
            "encrypt a virtual machine's memory with keys the hypervisor never sees, so that a tenant need not trust "
            "the provider's own software, and can check by remote attestation what it is running on. "
            "<bookmark mark='b'/> Against that stand side channels: tenants sharing a core, a cache or memory "
            "bandwidth can measure each other, as Parts 8 and 9 showed, and every defence costs speed. "
            "<bookmark mark='c'/> And hardware is coming apart: memory and accelerators pooled across a rack, "
            "which wastes less but adds new latencies and new ways to fail. <bookmark mark='d'/> Isolation that is "
            "provable, cheap and complete at the same time remains open. Verified kernels exist, which Part 54 will "
            "meet, and fast hypervisors exist, but not yet both at once at the scale of a cloud."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()



_ = (DATA, KERN, LAM, NO, YES)
