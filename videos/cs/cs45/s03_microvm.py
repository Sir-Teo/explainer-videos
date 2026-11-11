from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono, tag_box, timeline_bar


def layer(text, color, w, h=0.55, font_size=18, fill=0.18):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=1.8,
                         fill_color=color, fill_opacity=fill)
    t = label(text, font_size=font_size, color=WHITE)
    if t.width > w - 0.15:
        t.width = w - 0.15
    return VGroup(r, t.move_to(r))


class Microvm(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.devices()
        self.boot()
        self.walls()
        self.grades()

    def card(self):
        card = chapter_card(2, r"Virtual machines, \ shrunk", r"How small can a virtual machine be?",
                            lit=(1974, 2020), extra=((1974, r"Popek and Goldberg"), (2007, r"KVM in Linux"),
                                                     (2020, r"Agache et al.: \ Firecracker")), part=PART)
        with self.voiceover("Chapter two. Virtual machines, shrunk."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def split(self):
        head = label(r"A hypervisor in two halves", font_size=36).to_edge(UP, buff=0.3)
        hw = layer(r"processor with a virtualization mode \ (VT-x, \ AMD-V)", GREY_B, 6.6)
        kvm = layer(r"Linux, \ with \textbf{KVM} in the kernel", KERN, 6.6, h=0.6)
        vms = VGroup()
        for _ in range(2):
            app = layer(r"guest's programs", DATA, 2.7)
            gk = layer(r"guest kernel", HEAD, 2.7)
            dev = layer(r"emulated devices", LAM, 2.7)
            inner = VGroup(app, gk, dev).arrange(DOWN, buff=0.4)
            frame = RoundedRectangle(width=3.1, height=inner.height + 0.95, corner_radius=0.12, stroke_color=LAM,
                                     stroke_width=2)
            inner.move_to(frame).shift(UP * 0.2)
            cap = label(r"the monitor process", font_size=16, color=LAM).next_to(dev, DOWN, buff=0.14).align_to(
                frame, LEFT).shift(RIGHT * 0.15)
            vms.add(VGroup(frame, inner, cap))
        vms.arrange(RIGHT, buff=0.4)
        VGroup(vms, kvm, hw).arrange(DOWN, buff=0.25).scale(1.12).move_to([-2.75, -0.35, 0])
        gk, dev = vms[1][1][1], vms[1][1][2]
        a1 = CurvedArrow(gk.get_right() + DOWN * 0.05, kvm[0].get_top() + RIGHT * 3.0, angle=-2.0, color=NO,
                         stroke_width=3)
        a2 = Arrow(kvm[0].get_top() + RIGHT * (dev.get_right()[0] - 0.35 - kvm.get_x()),
                   dev.get_bottom() + RIGHT * (dev.width / 2 - 0.35), buff=0.03, color=KERN, stroke_width=3,
                   max_tip_length_to_length_ratio=0.2)
        a3 = Arrow(dev.get_top() + LEFT * 0.6, gk.get_bottom() + LEFT * 0.6, buff=0.02, color=YES, stroke_width=3,
                   max_tip_length_to_length_ratio=0.45)
        nums = VGroup(label(r"1", font_size=20, color=NO).next_to(a1, RIGHT, buff=0.06),
                      label(r"2", font_size=20, color=KERN).next_to(a2, LEFT, buff=0.06),
                      label(r"3", font_size=20, color=YES).next_to(a3, LEFT, buff=0.06))
        notes = VGroup(
            wrapped_label(r"\textbf{KVM} \ (Linux, \ 2007): \ guest code runs directly on the processor; \ only its "
                          r"\textit{exits} come to the kernel \ (Part 32)", 4.7, font_size=19, color=KERN),
            wrapped_label(r"the \textbf{monitor}, \ an ordinary process, \ pretends to be the rest of a machine: \ "
                          r"disks, \ network cards, \ clock, \ firmware; \ the classic one is QEMU \ (Bellard, \ 2003)",
                          4.7, font_size=19, color=LAM),
            wrapped_label(r"a device access: \ 1 \ the guest touches a device register and exits; \ 2 \ KVM hands "
                          r"it to the monitor; \ 3 \ the monitor emulates it, \ and the guest resumes", 4.7,
                          font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        with self.voiceover(
            "Part 32 built a hypervisor by trap and emulate. On Linux today the work is split in two. "
            "<bookmark mark='a'/> KVM, in the kernel since 2007, uses the processor's virtualization mode: a guest's "
            "code runs directly on the processor, and only its exits come to the kernel. <bookmark mark='b'/> "
            "Everything else a guest expects of a machine, disks, network cards, clock, firmware, is pretended by "
            "an ordinary user process, the virtual machine monitor; the classic one is QEMU, begun by Fabrice "
            "Bellard in 2003. <bookmark mark='c'/> When the guest touches a device, it exits to KVM, KVM hands the "
            "access to the monitor, and the monitor emulates the device and resumes the guest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hw))
            vo.wait_until("a")
            self.play(FadeIn(kvm), FadeIn(notes[0]))
            self.play(*[FadeIn(v[1][0]) for v in vms], *[FadeIn(v[1][1]) for v in vms])
            vo.wait_until("b")
            self.play(*[Create(v[0]) for v in vms], *[FadeIn(v[1][2]) for v in vms], *[FadeIn(v[2]) for v in vms],
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            for a, n in zip((a1, a2, a3), nums):
                self.play(Create(a), FadeIn(n), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    def devices(self):
        head = label(r"Where the weight is", font_size=36).to_edge(UP, buff=0.3)
        full = [r"BIOS or UEFI firmware", r"PCI bus", r"VGA graphics", r"USB controllers", r"sound card",
                r"IDE and SATA disks", r"floppy controller", r"PS/2 keyboard, mouse", r"several network cards",
                r"real-time clock", r"ACPI power"]
        fc = [r"virtio-net", r"virtio-block", r"virtio-vsock", r"serial console", r"keyboard controller"]
        wl = max(mono(t, size=18).width for t in full) + 0.35
        wr = max(mono(t, size=18).width for t in fc) + 0.35
        left = VGroup(*[tag_box(t, color=LAM, size=18, w=wl, h=0.48) for t in full])
        left.arrange_in_grid(rows=6, cols=2, buff=(0.15, 0.13), flow_order="dr")
        right = VGroup(*[tag_box(t, color=YES, size=18, w=wr, h=0.48) for t in fc]).arrange(DOWN, buff=0.13)
        lt = label(r"a general-purpose monitor can emulate \ (a selection)", font_size=19, color=LAM)
        rt = label(r"Firecracker's whole device model", font_size=19, color=YES)
        lg = VGroup(lt, left).arrange(DOWN, buff=0.25)
        rg = VGroup(rt, right).arrange(DOWN, buff=0.25)
        cols = VGroup(lg, rg).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        floppy = left[full.index(r"floppy controller")]
        notes = VGroup(
            wrapped_label(r"every emulated device is code that parses values a hostile guest controls; \ "
                          r"\textbf{VENOM} \ (2015): \ a bug in QEMU's floppy controller let a guest break out to "
                          r"the host", 12.4, font_size=20, color=NO),
            wrapped_label(r"\textbf{Firecracker} \ (Amazon; \ open source 2018; \ Agache et al., \ 2020): \ begun "
                          r"from Google's crosvm, \ written in Rust, \ with paravirtual \textit{virtio} devices "
                          r"\ (Part 32) \ and almost nothing else", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(cols, DOWN, buff=0.6)
        with self.voiceover(
            "That monitor is where the weight is. <bookmark mark='a'/> A general-purpose monitor can pretend to be "
            "almost any PC: firmware, a PCI bus, graphics, USB, sound, many disk controllers and network cards, even "
            "a floppy drive. Each is code that reads values a hostile guest controls. <bookmark mark='b'/> In 2015 "
            "the bug called VENOM, in QEMU's emulated floppy controller, let a guest break out to the host, on "
            "servers that had never seen a floppy. <bookmark mark='c'/> Amazon's Firecracker, open source since "
            "2018 and described by Alexandru Agache and colleagues in 2020, keeps five devices: a virtio network "
            "card and disk, a socket to the host, a serial console, and a scrap of keyboard controller, used only "
            "to stop the machine. It began from Google's crosvm, and is written in Rust."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lt), LaggedStart(*[FadeIn(b) for b in left], lag_ratio=0.12), run_time=2)
            vo.wait_until("b")
            self.play(floppy[0].animate.set_stroke(NO, width=3), floppy[1].animate.set_color(NO), FadeIn(notes[0]))
            self.play(Indicate(floppy, color=NO, scale_factor=1.1))
            vo.wait_until("c")
            self.play(FadeIn(rt), LaggedStart(*[FadeIn(b, shift=LEFT * 0.2) for b in right], lag_ratio=0.2),
                      FadeIn(notes[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def boot(self):
        head = label(r"Booting in milliseconds", font_size=36).to_edge(UP, buff=0.3)
        x0, w = -4.3, 10.8
        full = [(r"firmware", 2.4, GREY_B), (r"boot loader", 1.0, LAM), (r"kernel, \ probing devices", 2.8, HEAD),
                (r"init and services", 3.0, DATA)]
        total = sum(d for _, d, _ in full)
        sec = w / 10.0                               # the top row: ten illustrative seconds across
        y1, y2, y3 = 1.6, 0.45, -1.35
        row1 = VGroup()
        t = 0.0
        for name, d, c in full:
            row1.add(timeline_bar(x0 + t * sec, x0 + (t + d) * sec, y1, c, h=0.45, label_text=name, size=16))
            t += d
        micro_s = 0.125
        sliver = Rectangle(width=micro_s * sec, height=0.45, stroke_width=0, fill_color=YES,
                           fill_opacity=0.9).move_to([x0 + micro_s * sec / 2, y2, 0])
        zoom = [(r"monitor", 0.08, GREY_B), (r"kernel: \ a handful of virtio devices", 0.62, HEAD),
                (r"minimal init", 0.18, DATA), (r"user code", 0.12, YES)]
        row3 = VGroup()
        t = 0.0
        for name, f, c in zoom:
            row3.add(timeline_bar(x0 + t * w, x0 + (t + f) * w, y3, c, h=0.45, label_text=name, size=16))
            t += f
        names = VGroup(label(r"a general-purpose VM", font_size=18, color=WHITE).move_to([-5.6, y1, 0]),
                       label(r"a microVM", font_size=18, color=YES).move_to([-5.6, y2, 0]),
                       label(r"the microVM, \ magnified", font_size=18, color=YES).move_to([-5.6, y3, 0]))
        for n in names:
            if n.width > 2.4:
                n.width = 2.4
        scale1 = label(rf"$\approx$ {total:.0f} s \ (stages illustrative)", font_size=16, color=GREY_B).next_to(
            row1, DOWN, buff=0.1).align_to(row1, RIGHT)
        scale3 = label(r"0 \ to \ 125 ms", font_size=16, color=GREY_B).next_to(row3, DOWN, buff=0.1).align_to(
            row3, RIGHT)
        cone = VGroup(DashedLine(sliver.get_corner(DL), row3.get_corner(UL), color=GREY_C, stroke_width=1.5),
                      DashedLine(sliver.get_corner(DR), row3.get_corner(UR), color=GREY_C, stroke_width=1.5))
        notes = VGroup(
            wrapped_label(r"the Firecracker project reports: \ user code in as little as \textbf{125 ms}; \ under "
                          r"5 MiB of memory overhead per microVM; \ up to 150 microVMs started per second per host",
                          12.4, font_size=20, color=YES),
            wrapped_label(r"faster still, \ do not boot: \ restore a memory snapshot of a machine that already has "
                          r"\ (Lambda SnapStart, \ 2022)", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> A general-purpose virtual machine runs "
            "firmware, a boot loader, a kernel that probes a whole PC's worth of hardware, and an init system, and "
            "takes seconds. <bookmark mark='b'/> On that scale a microVM is a sliver. <bookmark mark='c'/> Magnify "
            "it: the monitor loads the kernel straight into memory, with no firmware; the kernel finds a handful "
            "of virtio devices; and a minimal init starts the user's code. The Firecracker project reports as "
            "little as a hundred and twenty-five milliseconds to user code, under five mebibytes of memory "
            "overhead each, and up to a hundred and fifty new microVMs a second on one host. "
            "<bookmark mark='d'/> Faster still: since 2022, Lambda's SnapStart skips booting, restoring a "
            "snapshot of a machine that booted earlier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in row1], lag_ratio=0.6), FadeIn(scale1),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(names[1]), GrowFromEdge(sliver, LEFT))
            self.play(Indicate(sliver, color=WHITE, scale_factor=1.6))
            vo.wait_until("c")
            self.play(Create(cone), FadeIn(names[2]))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in row3], lag_ratio=0.6), FadeIn(scale3),
                      run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def walls(self):
        head = label(r"One function, \ one virtual machine", font_size=36).to_edge(UP, buff=0.3)
        tenants = [DATA, LAM, YES, HEAD]
        host = Rectangle(width=5.9, height=4.1, stroke_color=GREY_B, stroke_width=2).move_to([-3.6, -0.15, 0])
        host_l = label(r"one host", font_size=18, color=GREY_B).next_to(host, UP, buff=0.1).align_to(host, LEFT)
        before = VGroup()
        for k, c in enumerate(tenants):
            vm = RoundedRectangle(width=2.6, height=1.7, corner_radius=0.1, stroke_color=c, stroke_width=2)
            cs = VGroup(*[Square(0.32, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.35)
                          for _ in range(2 + k % 2)]).arrange(RIGHT, buff=0.15).move_to(vm)
            before.add(VGroup(vm, cs))
        before.arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(host)
        before_l = label(r"before: \ a VM per customer, \ containers inside", font_size=17, color=GREY_A).next_to(
            host, DOWN, buff=0.12)
        rng = random.Random(7)
        after = VGroup()
        for _ in range(48):
            c = rng.choice(tenants)
            m = VGroup(RoundedRectangle(width=0.62, height=0.5, corner_radius=0.05, stroke_color=c, stroke_width=1.5,
                                        fill_color=c, fill_opacity=0.25),
                       Rectangle(width=0.5, height=0.07, stroke_width=0, fill_color=HEAD, fill_opacity=0.9))
            m[1].move_to(m[0]).shift(DOWN * 0.15)
            after.add(m)
        after.arrange_in_grid(rows=6, cols=8, buff=(0.1, 0.12)).move_to(host)
        after_l = label(r"after: \ a microVM per function, \ customers mixed", font_size=17, color=GREY_A).move_to(
            before_l)
        rings = [(r"the jail: \ chroot, \ namespaces, \ cgroups, \ seccomp filter", NO, 5.6, 4.1),
                 (r"the Firecracker process: \ five devices", KERN, 4.8, 3.05),
                 (r"KVM", LAM, 4.0, 2.1), (r"guest kernel", HEAD, 3.2, 1.25), (r"function", DATA, 2.0, 0.42)]
        wall = VGroup()
        for t, c, ww, hh in rings:
            r = RoundedRectangle(width=ww, height=hh, corner_radius=0.12, stroke_color=c, stroke_width=2.2,
                                 fill_color=c, fill_opacity=0.06)
            wall.add(VGroup(r, label(t, font_size=18, color=c)))
        for g in wall:
            g[0].move_to([3.75, -0.15, 0])
        for g in wall[:-1]:
            g[1].next_to(g[0].get_top(), DOWN, buff=0.1)
            if g[1].width > g[0].width - 0.2:
                g[1].width = g[0].width - 0.2
        wall[-1][1].move_to(wall[-1][0])
        foot = wrapped_label(r"to reach the host, \ escaping code must break the guest kernel, \ then KVM or the "
                             r"device model, \ then the jail", 12.4, font_size=20, color=WHITE).to_edge(DOWN,
                                                                                                    buff=0.3)
        with self.voiceover(
            "Why give a function a whole virtual machine? <bookmark mark='a'/> When Lambda launched, it isolated "
            "customers from each other with virtualization, and one customer's functions from each other with "
            "containers, so every customer needed virtual machines of their own. <bookmark mark='b'/> With "
            "Firecracker, every function gets its own microVM, and functions of different customers share a host "
            "safely, densely packed, a bin-packing problem for chapter five. <bookmark mark='c'/> The walls are "
            "layered. Code that escapes a function must still break the guest kernel; then KVM or the small "
            "device model; and then the Firecracker process itself, which a jailer starts in an empty file tree, "
            "in its own namespaces and control groups, behind a filter that allows only the few system calls it "
            "needs."
        ) as vo:
            self.play(FadeIn(head), Create(host), FadeIn(host_l))
            vo.wait_until("a")
            self.play(FadeIn(before), FadeIn(before_l))
            vo.wait_until("b")
            self.play(FadeOut(before), FadeOut(before_l))
            self.play(LaggedStart(*[FadeIn(m) for m in after], lag_ratio=0.03), FadeIn(after_l), run_time=2)
            vo.wait_until("c")
            for g in wall[::-1]:
                self.play(FadeIn(g), run_time=0.6)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def grades(self):
        head = label(r"Isolation comes in grades", font_size=36).to_edge(UP, buff=0.3)
        axis = Arrow([-6.2, 0.2, 0], [6.4, 0.2, 0], buff=0, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.02)
        pts = [(r"process", r"shares everything", GREY_A),
               (r"container", r"shares one kernel: \ about 450 system calls \ (Part 32)", DATA),
               (r"gVisor \ (2018)", r"a second kernel, \ in user space, \ answers the calls", LAM),
               (r"microVM", r"shares KVM and a small device model; \ Kata Containers \ (2017) \ put containers "
                            r"in them", YES),
               (r"full VM", r"a whole PC, \ emulated", HEAD)]
        xs = [-5.4, -2.7, 0.0, 2.7, 5.4]
        marks = VGroup()
        for k, ((t, d, c), x) in enumerate(zip(pts, xs)):
            dot = Dot([x, 0.2, 0], radius=0.11, color=c)
            name = label(t, font_size=23, color=c)
            desc = wrapped_label(d, 2.5, font_size=19, color=GREY_A)
            if k % 2 == 0:
                g = VGroup(name, desc).arrange(DOWN, buff=0.1).next_to(dot, UP, buff=0.3)
            else:
                g = VGroup(name, desc).arrange(DOWN, buff=0.1).next_to(dot, DOWN, buff=0.3)
            marks.add(VGroup(dot, g))
        ends = VGroup(label(r"$\leftarrow$ \ starts faster, \ packs denser", font_size=21, color=GREY_B),
                      label(r"stronger walls \ $\rightarrow$", font_size=21, color=GREY_B))
        ends[0].next_to(axis, DOWN, buff=2.6).to_edge(LEFT, buff=0.5)
        ends[1].next_to(axis, DOWN, buff=2.6).to_edge(RIGHT, buff=0.5)
        foot = label(r"next: \ inside the container", font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Isolation comes in grades. <bookmark mark='a'/> A process shares everything with its neighbours. A "
            "container, as Part 32 showed, shares one kernel and its four hundred and fifty or so system calls. "
            "Google's gVisor, of 2018, answers those calls with a second kernel in user space. A microVM shares "
            "only KVM and a small device model; Kata Containers, from 2017, runs containers inside them. A full "
            "virtual machine pretends to be a whole PC. <bookmark mark='b'/> Each step right buys stronger walls "
            "with start-up time and memory. <bookmark mark='c'/> Next, we open the container."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(ends))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
