from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (DATA, HEAD, KERN, NO, PART, YES, fit_right, grid_table, load)


def layer(text, color, w=5.2, h=0.8):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2, fill_color=color,
                         fill_opacity=0.15)
    return VGroup(r, label(text, font_size=21, color=WHITE).move_to(r))


class Virt(VoiceoverScene):
    def construct(self):
        self.card()
        self.popek()
        self.measured()
        self.x86()
        self.nested()

    def card(self):
        card = chapter_card(12, r"Virtual machines", r"Can one machine pretend to be several?", lit=(1972, 1974, 1999),
                            extra=((1972, r"IBM VM/370"), (1974, r"Popek and Goldberg"), (1999, r"VMware")),
                            part=PART)
        with self.voiceover("Chapter twelve. Virtual machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def popek(self):
        head = label(r"Trap and emulate", font_size=36).to_edge(UP, buff=0.3)
        gu = layer(r"guest processes \ (user mode)", DATA)
        gk = layer(r"guest kernel: \ PebbleOS, \ unmodified \ (\textbf{user} mode)", HEAD)
        hv = layer(r"hypervisor \ (the only code in kernel mode)", KERN)
        stack = VGroup(gu, gk, hv).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.4)
        a1 = CurvedArrow(gk.get_right() + DOWN * 0.1, hv.get_right() + UP * 0.1, angle=-1.6, color=NO,
                         stroke_width=2.5)
        a1l = label(r"\texttt{csrw}: \ trap", font_size=18, color=NO).next_to(a1, RIGHT, buff=0.08)
        a2 = CurvedArrow(hv.get_left() + UP * 0.1, gk.get_left() + DOWN * 0.1, angle=-1.6, color=YES,
                         stroke_width=2.5)
        a2l = label(r"done, \ on the guest's \\ virtual registers", font_size=18, color=YES).next_to(a2, LEFT,
                                                                                                    buff=0.08)
        lines = VGroup(
            label(r"\textbf{sensitive}: \ reads or changes the mode, \ control registers, \ devices", font_size=21,
                  color=WHITE),
            label(r"\textbf{privileged}: \ traps in user mode", font_size=21, color=WHITE),
            label(r"Popek and Goldberg, \ 1974: \ if sensitive $\subseteq$ privileged, \ trap-and-emulate works",
                  font_size=21, color=YES),
            label(r"Pebble passes: \ \texttt{csrr}, \ \texttt{csrw}, \ \texttt{eret}, \ \texttt{halt} and the device "
                  r"page all trap", font_size=21, color=HEAD),
            label(r"a process's \texttt{ecall} or fault is \textit{reflected}: \ the hypervisor does what the "
                  r"hardware would, \ to the virtual registers", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Virtual memory gives each process a private memory. The same trick, applied to the whole machine, gives "
            "each operating system a private computer. IBM's VM three-seventy did it in 1972. <bookmark mark='a'/> "
            "Run the guest kernel, unmodified, in user mode, under a small hypervisor that alone has the real "
            "privilege. <bookmark mark='b'/> Whenever the guest kernel does something privileged, such as writing a "
            "control register, it traps. The hypervisor performs the operation on a copy of the registers it keeps "
            "for that guest, and returns. <bookmark mark='c'/> Popek and Goldberg made the condition precise in 1974. "
            "Call an instruction sensitive if it reads or changes the machine's mode, its control state or its "
            "devices. <bookmark mark='d'/> Call it privileged if it traps in user mode. <bookmark mark='e'/> If every "
            "sensitive instruction is privileged, trap-and-emulate works. <bookmark mark='f'/> Pebble passes: all four "
            "privileged instructions, and every touch of the device page, trap in user mode. <bookmark mark='g'/> "
            "And when a guest's own process makes a system call, the hypervisor reflects it: it saves the program "
            "counter and sets the cause in the guest's virtual registers, as the hardware would, and jumps to the "
            "guest kernel."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stack))
            vo.wait_until("b")
            self.play(Create(a1), FadeIn(a1l))
            self.play(Create(a2), FadeIn(a2l))
            for mk, ln in zip("cdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("virt")
        head = label(r"Part 31's PebbleOS, \ as a guest", font_size=36).to_edge(UP, buff=0.3)
        names = [("csr", r"control register"), ("eret", r"\texttt{eret}"), ("ecall", r"system call, \ reflected"),
                 ("timer", r"timer, \ reflected"), ("device", r"device access"), ("halt", r"\texttt{halt}")]
        cols = VGroup()
        for key, title, color in (("letters", r"two letter-printers", HEAD), ("pipeline", r"the Job's pipeline", DATA)):
            ex = d[key]["exits"]
            tot = sum(ex.values())
            mx = max(ex.values())
            rows = VGroup()
            for k, t in names:
                v = ex[k]
                bar = Rectangle(width=max(0.04, 3.0 * v / mx), height=0.3, stroke_width=0, fill_color=color,
                                fill_opacity=0.8)
                rows.add(VGroup(label(t, font_size=17, color=GREY_A), bar,
                                label(f"{v:,}".replace(",", "{,}"), font_size=17, color=WHITE)))
            for i, r in enumerate(rows):
                r[0].move_to([0, -0.44 * i, 0], aligned_edge=RIGHT)
                r[1].next_to(np.array([0, -0.44 * i, 0]), RIGHT, buff=0.15)
                r[2].next_to(r[1], RIGHT, buff=0.1)
            t = label(rf"{title}: \ {tot:,} exits".replace(",", "{,}"), font_size=21, color=color)
            cols.add(VGroup(t, rows).arrange(DOWN, buff=0.2))
        cols.arrange(RIGHT, buff=0.9).next_to(head, DOWN, buff=0.45)
        fit_right(cols)
        L, P = d["letters"], d["pipeline"]
        lines = VGroup(
            label(rf"output identical; \ guest instructions identical: \ {L['virt_steps']:,} and "
                  rf"{P['virt_steps']:,}".replace(",", "{,}"), font_size=21, color=YES),
            label(rf"the pipeline moves {P['bytes']:,} bytes: \ {P['exits']['device']:,} of its exits are the "
                  rf"device".replace(",", "{,}"), font_size=21, color=NO),
            label(r"so real hypervisors give guests \textbf{paravirtual} devices \ (Xen 2003, \ virtio): \ one "
                  r"exit per buffer, \ not per byte", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "We built that hypervisor for Pebble, and ran Part 31's kernel under it without changing one instruction. "
            "<bookmark mark='a'/> Two processes printing letters: the guest kernel exited to the hypervisor almost six "
            "hundred times, mostly to read and write control registers during its context switches. <bookmark "
            "mark='b'/> The output is identical to the native run, and so is the number of instructions the guest "
            "executed: the guest cannot tell. <bookmark mark='c'/> The Job's pipeline tells a different story. It "
            "moves four thousand six hundred bytes through the console device, and almost every exit is a device "
            "access, one per byte. <bookmark mark='d'/> That is why real hypervisors offer paravirtual devices, as Xen "
            "did in 2003 and virtio does today: the guest knows it is virtual and hands over a whole buffer with a "
            "single exit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0][0]), LaggedStart(*[FadeIn(r) for r in cols[0][1]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(cols[1][0]), LaggedStart(*[FadeIn(r) for r in cols[1][1]], lag_ratio=0.15))
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def x86(self):
        head = label(r"x86 failed the test", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"year", r"approach", r"how"], [
            [r"1974", r"the condition", r"Popek and Goldberg: \ sensitive $\subseteq$ privileged"],
            [r"1985", r"x86 fails it", r"17 sensitive instructions do not trap \ (counted by Robin and Irvine, \ "
                                       r"2000); \ \texttt{popf} ignores the interrupt flag"],
            [r"1999", r"binary translation", r"VMware rewrites guest kernel code on the fly; \ user code runs "
                                             r"directly"],
            [r"2003", r"paravirtualization", r"Xen: \ change the guest kernel to call the hypervisor"],
            [r"2005--06", r"hardware support", r"Intel VT-x, \ AMD-V: \ a new mode below the kernel; \ x86 passes"],
            [r"2006", r"a surprise", r"Adams and Agesen: \ early VT-x was \textit{slower} than VMware's translator"],
        ], widths=[1.6, 3.2, 8.2], row_h=0.6, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The x86, the processor in most computers, failed Popek and Goldberg's test. <bookmark mark='a'/> Robin "
            "and Irvine later counted seventeen sensitive instructions that do not trap. One, pop-flags, run in user "
            "mode, silently ignores the bit that turns interrupts off, so a guest kernel cannot even tell that it "
            "failed. <bookmark mark='b'/> VMware's answer, in 1999, was binary translation: rewrite the guest "
            "kernel's code as it runs, replacing the troublesome instructions, while letting user code run directly. "
            "<bookmark mark='c'/> Xen's answer, in 2003, was to modify the guest kernel to call the hypervisor "
            "openly. <bookmark mark='d'/> Then Intel and AMD added a new mode beneath the kernel, and x86 passed the "
            "test. <bookmark mark='e'/> Surprisingly, Adams and Agesen measured the first hardware version as slower "
            "than VMware's software, because every exit was so expensive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1])))
            for mk, r in zip("abcde", tab.cells[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
        self.wait(0.3)
        self.clear_scene()

    def nested(self):
        d = load("virt")
        head = label(r"Two page tables at once: \ the nested walk", font_size=34).to_edge(UP, buff=0.3)
        n = m = 4
        s = 0.62
        grid = VGroup()
        for i in range(n + 1):
            for j in range(m + 1):
                last = i == n and j == m
                c = YES if last else (HEAD if j == m else KERN)
                grid.add(Circle(radius=0.17, stroke_color=c, stroke_width=2, fill_color=c,
                                fill_opacity=0.15 if last else 0.55).move_to([j * s, -i * s, 0]))
        grid.move_to([-2.4, -0.1, 0])
        rl = VGroup(*[label(t, font_size=16, color=HEAD).next_to(grid[i * (m + 1)], LEFT, buff=0.3) for i, t in
                      enumerate((r"guest L4", r"guest L3", r"guest L2", r"guest L1", r"the data"))])
        cl = VGroup(*[label(t, font_size=16, color=KERN).next_to(grid[j], UP, buff=0.25) for j, t in
                      enumerate((r"h4", r"h3", r"h2", r"h1", r"read"))])
        ctop = label(r"host walk of each guest-physical address", font_size=17, color=KERN).next_to(cl, UP, buff=0.12)
        rows = d["nested"]
        tab = grid_table([r"guest levels $n$", r"host levels $m$", r"references"],
                         [[str(r["n"]), str(r["m"]), str(r["refs"])] for r in rows], widths=[2.0, 2.0, 1.8],
                         row_h=0.42, font_size=18, mono_cols=())
        tab.next_to(grid, RIGHT, buff=1.4).align_to(grid, UP)
        f = MathTex(r"(n+1)(m+1) - 1", font_size=40, color=YES).next_to(tab, DOWN, buff=0.35)
        lines = VGroup(
            label(r"each guest table's address is guest-physical: \ $m$ host references to find it, \ then 1 to "
                  r"read it", font_size=20, color=WHITE),
            label(r"before 2008: \ \textbf{shadow} page tables, \ kept in step by the hypervisor at every guest "
                  r"update", font_size=20, color=GREY_A),
            label(r"nested paging \ (AMD 2007, \ Intel EPT 2008): \ no shadows, \ but a TLB miss costs 24 "
                  r"references, \ not 4", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Memory needs virtualising too. The guest kernel builds page tables from what it thinks are physical "
            "addresses; the hypervisor has its own table from those to the real ones. <bookmark mark='a'/> Modern "
            "hardware walks both. Each guest table entry lives at a guest-physical address, so before the hardware "
            "can read it, it must walk the host's four levels to find it, and only then read it. <bookmark "
            "mark='b'/> Four guest levels times five references, plus four more to translate the final address: "
            "twenty-four memory references for one TLB miss, where a native walk takes four. <bookmark mark='c'/> In "
            "general, n plus one times m plus one, minus one. <bookmark mark='d'/> Before this hardware existed, "
            "hypervisors kept shadow page tables, combining the two, and had to catch every change the guest made to "
            "its own tables. <bookmark mark='e'/> Nested paging, from AMD in 2007 and Intel in 2008, ended that, at "
            "the price of the two-dimensional walk, which is why huge pages matter even more inside virtual machines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), FadeIn(ctop))
            vo.wait_until("a")
            for i in range(n):
                self.play(LaggedStart(*[FadeIn(grid[i * (m + 1) + j], scale=0.5) for j in range(m + 1)],
                                      lag_ratio=0.15), run_time=0.7)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid[n * (m + 1) + j], scale=0.5) for j in range(m + 1)],
                                  lag_ratio=0.15), run_time=0.7)
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("c")
            self.play(FadeIn(f), FadeIn(VGroup(*tab.cells[1], *tab.cells[3], *tab.cells[4])))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
