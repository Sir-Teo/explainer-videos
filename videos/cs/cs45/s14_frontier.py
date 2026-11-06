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


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.nines()
        self.predictions()
        self.isolation()
        self.open()

    def card(self):
        card = chapter_card(13, r"Frontier: \ scheduling, \ isolation and energy",
                            r"How close to optimal can a cloud run?", lit=(2015, 2020),
                            extra=((2015, r"Borg described"), (2020, r"Firecracker")), part=PART)
        with self.voiceover("Chapter thirteen, the frontier. How close to optimal can a cloud run?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def nines(self):
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

    def predictions(self):
        p = load("packing")["uniform"]["mean_ratio"]
        head = label(r"Scheduling with predictions", font_size=36).to_edge(UP, buff=0.3)
        names = [(r"next fit", "next fit", NO), (r"first fit", "first fit", HEAD), (r"best fit", "best fit", LAM),
                 (r"first fit decreasing", "first fit decreasing", YES)]
        bars = VGroup()
        for k, (t, key, col) in enumerate(names):
            v = p[key]
            w = (v - 1) / 0.3 * 5.0 + 0.05
            b = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-3.0 + w / 2, 1.7 - 0.65 * k, 0])
            bars.add(VGroup(b, label(rf"{100 * (v - 1):.0f}\% above optimal", font_size=17, color=col).next_to(
                b, RIGHT, buff=0.15), label(t, font_size=18, color=GREY_A).move_to([-4.6, b.get_y(), 0])))
        cap = label(r"chapter 5: \ mean bins above the exact optimum, \ random instances", font_size=17,
                    color=GREY_B).next_to(bars, UP, buff=0.25)
        lines = VGroup(
            wrapped_label(r"first fit decreasing is close to optimal because it knows the sizes in advance; \ an "
                          r"online scheduler does not, \ and a VM's lifetime is unknown too", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{learning-augmented algorithms} \ (Lykouris and Vassilvitskii, \ 2018, \ and "
                          r"after): \ use a model's predictions of size and lifetime, \ and prove the result is near "
                          r"optimal when they are right and never much worse than the classical bound when wrong",
                          12.4, font_size=20, color=YES),
            wrapped_label(r"in production: \ schedulers that predict how long each VM will live, \ to pack machines "
                          r"that empty together", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Chapter five's heuristics show how much knowing the future is worth. <bookmark mark='a'/> First fit "
            f"decreasing, which sorts every item before packing, came within {100 * (p['first fit decreasing'] - 1):.0f} "
            f"percent of the optimum on our instances; next fit, which never looks back, {100 * (p['next fit'] - 1):.0f} "
            "percent. But a real scheduler is online: requests arrive one at a time, and nobody says how long a "
            "virtual machine will live. <bookmark mark='b'/> A new line of theory, learning-augmented algorithms, "
            "starting with Thodoris Lykouris and Sergei Vassilvitskii in 2018, gives an algorithm a model's "
            "predictions and proves two things: that it is near optimal when the predictions are right, and never "
            "much worse than the classical guarantee when they are wrong. <bookmark mark='c'/> In practice, "
            "schedulers now predict how long each virtual machine will run, so that machines can be packed with "
            "work that finishes together, and be emptied, repaired or switched off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.3), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
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

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Correlated failure}: \ durability models calibrated on real correlated "
                          r"failures, \ and placements that provably bound them.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Online packing with lifetimes}: \ competitive ratios for vector bin packing "
                          r"when items leave, \ with and without predictions.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Stable autoscaling}: \ controllers for delayed, \ noisy, \ coupled services "
                          r"with guarantees.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Carbon-optimal scheduling}: \ placing work in time and space to minimize "
                          r"emissions under deadlines.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ an online algorithm for vector bin packing "
                             r"of jobs with unknown lifetimes, \ given predictions, \ that is near optimal when they "
                             r"are accurate and robust when they are not", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Durability models calibrated on real correlated failures, and data "
            "placements that provably limit them. <bookmark mark='b'/> Online packing in several dimensions when "
            "jobs also leave, with and without predictions. <bookmark mark='c'/> Autoscaling controllers for "
            "services that are delayed, noisy and coupled to one another, with guarantees of stability. "
            "<bookmark mark='d'/> And carbon-optimal scheduling: placing work in time and space to minimize "
            "emissions while meeting deadlines. <bookmark mark='e'/> This part's research problem asks for an "
            "online algorithm that packs jobs of unknown lifetime into machines with several resources, using "
            "predictions, near optimal when they are accurate and robust when they are not."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
