from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


def layer(text, color, w, h=0.42, font=16, fill=0.2):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=fill)
    return VGroup(r, label(text, font_size=font, color=WHITE).move_to(r))


def design(title, user, kernel, color, note):
    W = 2.9
    ub = VGroup(*[layer(t, DATA, (W - 0.1 * (len(user) - 1)) / len(user)) for t in user]).arrange(RIGHT, buff=0.1)
    kb = VGroup(*[layer(t, KERN, W) for t in kernel]).arrange(DOWN, buff=0.06)
    line = DashedLine([-W / 2 - 0.1, 0, 0], [W / 2 + 0.1, 0, 0], color=GREY_B, stroke_width=1.5)
    g = VGroup(ub, line, kb).arrange(DOWN, buff=0.14)
    hw = layer(r"hardware", GREY_B, W, fill=0.1).next_to(g, DOWN, buff=0.08)
    t = label(title, font_size=22, color=color).next_to(g, UP, buff=0.2)
    n = label(note, font_size=16, color=GREY_A).next_to(hw, DOWN, buff=0.18)
    if n.width > W + 0.3:
        n.scale_to_fit_width(W + 0.3)
    return VGroup(t, g, hw, n)


class Designs(VoiceoverScene):
    def construct(self):
        self.card()
        self.shapes()
        self.debate()

    def card(self):
        card = chapter_card(13, r"Kernel designs", r"How much belongs inside the kernel?", lit=(1985, 1992, 1995, 2009),
                            extra=((1985, r"Mach"), (1992, r"Tanenbaum--Torvalds"), (1995, r"L4; \ exokernel"),
                                   (2009, r"seL4, \ verified")), part=PART)
        with self.voiceover("Chapter thirteen. Kernel designs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shapes(self):
        head = label(r"Four answers", font_size=36).to_edge(UP, buff=0.3)
        ds = VGroup(
            design(r"monolithic", [r"apps"], [r"file systems", r"drivers", r"network", r"memory, \ scheduling"], KERN,
                   r"Unix, \ Linux, \ the BSDs"),
            design(r"microkernel", [r"apps", r"files", r"drivers"], [r"IPC, \ memory, \ scheduling"], YES,
                   r"Mach, \ L4, \ QNX, \ seL4"),
            design(r"exokernel", [r"apps + library OS"], [r"secure multiplexing only"], LAM,
                   r"Engler, \ Kaashoek, \ O'Toole \ (1995)"),
            design(r"unikernel", [r"one app, \ linked with its OS"], [r"a hypervisor"], HEAD,
                   r"MirageOS \ (2013): \ one image per service"),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        line = label(r"above the dashed line: \ user mode; \ below it: \ kernel mode", font_size=19,
                     color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How much of the operating system should run in kernel mode? There are four main answers. <bookmark "
            "mark='a'/> A monolithic kernel, like Unix and Linux, puts everything inside: the file systems, the "
            "drivers, the network stack, memory and scheduling. Calls between them are ordinary function calls, "
            "which is fast, but a bug in any driver can bring down the machine. <bookmark mark='b'/> A microkernel "
            "keeps only the minimum inside, messages between processes, memory and scheduling, and runs file systems "
            "and drivers as ordinary processes. A crashed driver can be restarted, but every request now costs "
            "messages and switches. <bookmark mark='c'/> An exokernel goes further: the kernel only divides the "
            "hardware safely, and each application links its own operating system as a library. <bookmark "
            "mark='d'/> And a unikernel links one application with just the operating-system code it needs into a "
            "single image, run directly on a hypervisor, the subject of Part 32."
        ) as vo:
            self.play(FadeIn(head), FadeIn(line))
            for mk, d_ in zip("abcd", ds):
                vo.wait_until(mk)
                self.play(FadeIn(d_, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def debate(self):
        p = load("pebbleos")
        head = label(r"``LINUX is obsolete''", font_size=36).to_edge(UP, buff=0.3)
        quotes = VGroup(
            label(r"Tanenbaum, \ January 1992: \ a monolithic kernel is ``a giant step back into the 1970s''",
                  font_size=21, color=YES),
            label(r"Torvalds: \ the microkernel is cleaner in theory; \ Linux works, \ and is fast, \ today",
                  font_size=21, color=KERN),
            label(r"the price of messages: \ Mach's IPC was slow; \ Liedtke's L4 \ (1993--95) \ made it an order of "
                  r"magnitude faster", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.45)
        tab = grid_table([r"kernel", r"size", r"what it does"], [
            [r"PebbleOS", rf"{p['kernel_words']} instructions", r"traps, \ 5 calls, \ a pipe, \ round robin"],
            [r"seL4", r"$\sim$8{,}700 lines of C", r"a microkernel, \ proved correct \ (2009; \ Part 54)"],
            [r"Linux", r"$>$ 30 million lines", r"everything; \ most of it drivers"],
        ], widths=[2.2, 3.6, 6.4], row_h=0.52, font_size=20, mono_cols=())
        tab.next_to(quotes, DOWN, buff=0.45)
        line = label(r"the winners mix: \ macOS is Mach plus BSD; \ Windows NT is a hybrid; \ QNX runs in cars; \ "
                     r"Linux loads drivers as modules", font_size=20, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The choice was argued in public. In January 1992 Andrew Tanenbaum, author of the teaching system MINIX, "
            "posted that Linux was obsolete: <bookmark mark='a'/> a monolithic kernel, he wrote, was a giant step "
            "back into the nineteen-seventies. <bookmark mark='b'/> Linus Torvalds replied that the microkernel might "
            "be cleaner in theory, but Linux worked, and was fast, now. <bookmark mark='c'/> The argument was about "
            "the cost of messages. Mach's were slow, but Jochen Liedtke showed in the L4 kernels that a message "
            "between processes could be an order of magnitude faster, with a kernel designed around it. <bookmark "
            "mark='d'/> Sizes tell the story. PebbleOS is two hundred and eighty-four instructions. seL4, a "
            "microkernel in the L4 family, is about eight thousand seven hundred lines of C, and in 2009 it became "
            "the first general-purpose kernel with a machine-checked proof that it does what its specification "
            "says. Linux has more than thirty million lines, most of them drivers. <bookmark mark='e'/> In practice "
            "the winners mix: macOS is the Mach microkernel fused with BSD Unix, cars run the QNX microkernel, and "
            "Linux loads its drivers as modules."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", quotes):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()
