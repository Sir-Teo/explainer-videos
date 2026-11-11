from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono


def box(text, color, w, h=0.42, size=17, fill=0.0, dashed=False, use_mono=False):
    """A labelled rectangle; ``fill`` > 0 tints it with its colour."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=1.6,
                         fill_color=color if fill else BG, fill_opacity=fill if fill else 1)
    if dashed:
        r = VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_width=0, fill_color=BG,
                                    fill_opacity=1),
                   DashedVMobject(r.copy().set_fill(opacity=0), num_dashes=int(6 * (w + h))))
    t = mono(text, size=size, color=WHITE) if use_mono else label(text, font_size=size, color=WHITE)
    if t.width > w - 0.12:
        t.width = w - 0.12
    t.move_to(r)
    return VGroup(r, t)


def side_notes(items, width=3.3, size=19, buff=0.3):
    return VGroup(*[wrapped_label(t, width, font_size=size, color=c) for t, c in items]).arrange(
        DOWN, aligned_edge=LEFT, buff=buff)


class Isolation(VoiceoverScene):
    def construct(self):
        self.card()
        self.pages()
        self.ladder()
        self.sandbox()
        self.browser()
        self.enclaves()

    def card(self):
        card = chapter_card(7, r"Isolation", r"Can two programs share a machine, \ and nothing else?",
                            lit=(1962, 2017, 2018), extra=((1962, r"Atlas: \ paging"), (2017, r"WebAssembly"),
                                                           (2018, r"site isolation")), part=PART)
        with self.voiceover("Chapter seven. Isolation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pages(self):
        head = label(r"The first wall: \ address spaces \ (Parts 31 and 32)", font_size=36).to_edge(UP, buff=0.3)
        maps = {"A": {0: 5, 1: 2, 2: None, 3: "K"}, "B": {0: 1, 1: 6, 2: None, 3: "K"}}
        cols = {"A": DATA, "B": LAM}
        frames = VGroup()
        owner = {}
        for p, mp in maps.items():
            for v in mp.values():
                if isinstance(v, int):
                    owner[v] = p
        for f in range(8):
            c = cols[owner[f]] if f in owner else (KERN if f in (0, 7) else GREY_D)
            frames.add(box(rf"frame {f}" + (r" \ (kernel)" if f in (0, 7) else ""), c, 2.4, h=0.42, size=17,
                           fill=0.15 if (f in owner or f in (0, 7)) else 0.0))
        frames.arrange(DOWN, buff=0.08).move_to([1.6, -0.1, 0])
        fl = label(r"physical memory", font_size=18, color=GREY_A).next_to(frames, UP, buff=0.12)
        tables, rowmap = VGroup(), {}
        for p, y in (("A", 1.25), ("B", -1.55)):
            t = label(rf"process {p}: \ its page table", font_size=19, color=cols[p])
            rows = VGroup()
            for v, f in maps[p].items():
                ftxt = r"---" if f is None else (r"kernel only" if f == "K" else rf"frame {f}")
                r = VGroup(box(rf"page {v}", cols[p], 1.2, h=0.36, size=16),
                           box(ftxt, GREY_B if f is not None else GREY_D, 1.6, h=0.36, size=16)).arrange(RIGHT,
                                                                                                         buff=0.05)
                rows.add(r)
                rowmap[(p, v)] = r
            rows.arrange(DOWN, buff=0.05)
            g = VGroup(t, rows).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-4.6, y, 0])
            tables.add(g)
        a1 = Arrow(rowmap[("A", 1)][1].get_right(), frames[2].get_left(), buff=0.06, stroke_width=2.5, color=DATA,
                   max_tip_length_to_length_ratio=0.06)
        a2 = Arrow(rowmap[("B", 1)][1].get_right(), frames[6].get_left(), buff=0.06, stroke_width=2.5, color=LAM,
                   max_tip_length_to_length_ratio=0.06)
        same = label(r"the same address, \ page 1, \ in both: \ different frames", font_size=18,
                     color=HEAD).next_to(frames, DOWN, buff=0.25)
        bad = Arrow(rowmap[("B", 3)][1].get_right(), rowmap[("B", 3)][1].get_right() + RIGHT * 0.9, buff=0.04,
                    stroke_width=3, color=NO, max_tip_length_to_length_ratio=0.25)
        trap = label(r"fault: \ trap to the kernel", font_size=17, color=NO).next_to(bad, DOWN, buff=0.08)
        notes = side_notes([
            (r"a process can name only what its page table maps, \ and only the kernel may change a page table "
             r"\ (the mode bit, \ Part 31)", WHITE),
            (r"so the wall is the kernel itself: \ every line of it is trusted \ --- \ Linux has tens of millions",
             NO),
            (r"seL4, \ about ten thousand lines, \ is proved to enforce it \ (Klein et al., \ 2009; \ Part 54)", YES),
        ], width=3.4).move_to([5.05, -0.1, 0])
        with self.voiceover(
            "The first wall between programs is one we built in Parts 31 and 32. <bookmark mark='a'/> Every process "
            "has a page table, and can name only the memory its table maps. <bookmark mark='b'/> Two processes use "
            "the same address, page one, and reach different frames, each unaware of the other. <bookmark mark='c'/> "
            "Touch a page that is unmapped, or kept for the kernel, and the hardware traps to the kernel. Only the "
            "kernel may change a page table, because only it runs with the mode bit set. <bookmark mark='d'/> So the "
            "wall is exactly as strong as the kernel, and every one of its tens of millions of lines is trusted. "
            "<bookmark mark='e'/> The seL4 kernel, about ten thousand lines, is proved to enforce its isolation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frames), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(tables))
            vo.wait_until("b")
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(same))
            vo.wait_until("c")
            self.play(GrowArrow(bad), FadeIn(trap), Indicate(rowmap[("B", 3)], color=NO))
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def ladder(self):
        head = label(r"A ladder of walls", font_size=36).to_edge(UP, buff=0.3)
        spec = [
            (r"language sandbox", r"WebAssembly", [("pair", "A", "B"), ("shared", r"one process"),
                                                    ("shared", r"kernel"), ("shared", r"hardware")]),
            (r"process", r"Unix", [("pair", "A", "B"), ("shared", r"kernel"), ("shared", r"hardware")]),
            (r"container", r"namespaces, \ cgroups", [("pair", "A", "B"), ("pair", r"own view", r"own view"),
                                                     ("shared", r"kernel"), ("shared", r"hardware")]),
            (r"virtual machine", r"KVM, \ Xen", [("pair", "A", "B"), ("pair", r"kernel", r"kernel"),
                                                ("shared", r"hypervisor"), ("shared", r"hardware")]),
            (r"separate machines", r"", [("pair", "A", "B"), ("pair", r"kernel", r"kernel"),
                                        ("pair", r"hardware", r"hardware"), ("shared", r"network")]),
        ]
        cols = VGroup()
        shared_bars = []
        for k, (title, ex, rows) in enumerate(spec):
            stack = VGroup()
            for row in rows:
                if row[0] == "pair":
                    c = DATA if row[1] == "A" else GREY_B
                    pr = VGroup(box(row[1], c, 1.08, h=0.44, size=16),
                                box(row[2], LAM if row[2] == "B" else GREY_B, 1.08, h=0.44, size=16))
                    pr.arrange(RIGHT, buff=0.08)
                    stack.add(pr)
                else:
                    b = box(row[1], KERN, 2.24, h=0.44, size=16, fill=0.25)
                    stack.add(b)
                    shared_bars.append(b)
            stack.arrange(DOWN, buff=0.08)
            t = label(title, font_size=20, color=WHITE)
            e = label(ex, font_size=16, color=GREY_B) if ex else VectorizedPoint()
            col = VGroup(t, stack, e).arrange(DOWN, buff=0.22)
            stack.align_to(t, UP).shift(DOWN * 0.5)
            e.next_to(stack, DOWN, buff=0.18)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.26, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        arrow = DoubleArrow([-6.2, -0.95, 0], [6.2, -0.95, 0], stroke_width=2.5, color=GREY_B, buff=0,
                            max_tip_length_to_length_ratio=0.02)
        al = label(r"cheaper, \ faster to start", font_size=18, color=GREY_A).next_to(arrow, DOWN, buff=0.1).align_to(
            arrow, LEFT)
        ar = label(r"less shared, \ stronger wall", font_size=18, color=GREY_A).next_to(arrow, DOWN, buff=0.1).align_to(
            arrow, RIGHT)
        notes = VGroup(
            wrapped_label(r"\textbf{an escape goes through whatever is shared} \ (orange): \ any kernel bug is a "
                          r"possible container escape \ --- \ such as Dirty COW, \ a copy-on-write race in Linux found "
                          r"in 2016", 12.4, font_size=20, color=NO),
            wrapped_label(r"VENOM \ (2015): \ a bug in an emulated floppy-disk controller let a virtual machine's "
                          r"guest attack the host", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Processes are one rung on a ladder of walls. <bookmark mark='a'/> A language sandbox runs several "
            "programs inside one process. Processes share a kernel. Containers are processes given their own view of "
            "files and names, still on one kernel. Virtual machines each bring a kernel and share a hypervisor. "
            "Separate machines share only the network. <bookmark mark='b'/> Moving right, less is shared and the wall "
            "is stronger, but each rung costs more to run and to start. <bookmark mark='c'/> And an escape goes "
            "through whatever is shared: any kernel bug, such as the copy-on-write race called Dirty COW in 2016, is "
            "a possible container escape. <bookmark mark='d'/> In 2015 a bug called VENOM, in an emulated floppy-disk "
            "controller, let a virtual machine attack its host."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cols], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(GrowFromCenter(arrow), FadeIn(al), FadeIn(ar))
            vo.wait_until("c")
            self.play(*[Indicate(b, color=KERN, scale_factor=1.06) for b in shared_bars], FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def sandbox(self):
        head = label(r"Dropping privilege: \ system-call filters", font_size=36).to_edge(UP, buff=0.3)
        proc = box(r"a renderer, \ after start-up", DATA, 5.6, h=0.6, size=20, fill=0.12).move_to([-3.2, 2.15, 0])
        filt = box(r"the filter: \ an allow-list of system calls", HEAD, 6.2, h=0.55, size=19, fill=0.12)
        filt.move_to([-3.2, -0.35, 0])
        kern = box(r"kernel", KERN, 6.2, h=0.6, size=20, fill=0.2).move_to([-3.2, -2.55, 0])
        calls = [("read", True), ("write", True), ("exit", True), ("open", False), ("execve", False),
                 ("socket", False)]
        toks = VGroup()
        for k, (nm, ok) in enumerate(calls):
            t = box(nm, GREY_A, 0.92, h=0.42, size=16, use_mono=True).move_to([-5.7 + k * 1.0, 1.2, 0])
            toks.add(t)
        crosses = VGroup()
        moves_ok, moves_no = [], []
        for t, (nm, ok) in zip(toks, calls):
            target = t.copy().move_to([t.get_x(), -1.65 if ok else 0.35, 0])
            target[0].set_stroke(YES if ok else NO)
            target[1].set_color(YES if ok else NO)
            (moves_ok if ok else moves_no).append(Transform(t, target))
            if not ok:
                crosses.add(label(r"refused", font_size=16, color=NO).move_to([t.get_x(), 0.78, 0]))
        notes = side_notes([
            (r"least privilege \ (Chapter 1): \ initialise, \ then give up every call you will not need", WHITE),
            (r"seccomp \ (Linux, \ 2005); \ since 2012 its filters are small programs in classic BPF, \ the "
             r"language Part 31's eBPF grew from", HEAD),
            (r"Capsicum \ (FreeBSD, \ 2010): \ after \texttt{cap\_enter} a process loses all global names and keeps "
             r"only the descriptors it holds \ --- \ Chapter 6's capabilities", DATA),
        ], width=5.0, size=19, buff=0.35).move_to([4.0, -0.1, 0])
        with self.voiceover(
            "A process can also shrink its own power. <bookmark mark='a'/> A browser's renderer parses hostile pages, "
            "so once started it installs a filter on its own system calls. <bookmark mark='b'/> Calls on the "
            "allow-list, like read, write and exit, pass. Opening files, starting programs and making sockets are "
            "refused, so even a renderer the attacker fully controls can do little but compute. <bookmark mark='c'/> "
            "It is least privilege made mechanical: Linux has offered it since 2005 as seccomp, with filters written "
            "as small BPF programs since 2012. <bookmark mark='d'/> FreeBSD's Capsicum, from 2010, goes further: "
            "after one call a process loses every global name and keeps only the descriptors it holds, the "
            "capabilities of the last chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(proc), FadeIn(kern))
            vo.wait_until("a")
            self.play(FadeIn(filt), FadeIn(toks))
            vo.wait_until("b")
            self.play(*moves_ok, run_time=1.5)
            self.play(*moves_no, run_time=1.2)
            self.play(FadeIn(crosses))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def browser(self):
        head = label(r"The browser \ (Parts 15 and 42)", font_size=36).to_edge(UP, buff=0.3)
        bp = box(r"browser process \ (privileged)", KERN, 4.6, h=0.55, size=19, fill=0.15).move_to([-3.6, 2.2, 0])
        sites = [r"bank.example", r"news.example", r"evil.example"]
        rs = VGroup(*[box(s, [YES, DATA, NO][k], 1.85, h=0.75, size=16, dashed=True, use_mono=True)
                      for k, s in enumerate(sites)]).arrange(RIGHT, buff=0.2).move_to([-3.6, 0.75, 0])
        links = VGroup(*[Line(bp.get_bottom(), r.get_top(), color=GREY_C, stroke_width=1.5) for r in rs])
        rl = label(r"one sandboxed renderer process per site", font_size=18, color=GREY_A).next_to(rs, DOWN, buff=0.15)
        sl = wrapped_label(r"after Spectre \ (Chapter 4), \ anything in the same address space can be read: \ so "
                           r"the wall between sites must be a process \ --- \ \textbf{site isolation}, \ on by "
                           r"default in desktop Chrome since 2018", 6.2, font_size=19, color=WHITE)
        sl.next_to(rl, DOWN, buff=0.35).set_x(-3.6)
        n = 8
        cells = VGroup(*[Rectangle(width=0.42, height=0.55, stroke_color=DATA, stroke_width=1.2, fill_color=DATA,
                                   fill_opacity=0.15) for _ in range(n)]).arrange(RIGHT, buff=0)
        guard = Rectangle(width=1.6, height=0.55, stroke_color=GREY_C, stroke_width=1.2, fill_color=GREY_D,
                          fill_opacity=0.5)
        mem = VGroup(cells, guard).arrange(RIGHT, buff=0).move_to([3.6, 2.0, 0])
        ml = label(r"linear memory: \ $[0, n)$", font_size=17, color=DATA).next_to(cells, UP, buff=0.1)
        gl = label(r"guard pages", font_size=17, color=GREY_A).next_to(guard, UP, buff=0.1)
        ptr = Arrow([cells[3].get_x(), 1.15, 0], cells[3].get_bottom(), buff=0.03, stroke_width=3, color=YES,
                    max_tip_length_to_length_ratio=0.3)
        ptr2 = Arrow([guard.get_x(), 1.15, 0], guard.get_bottom(), buff=0.03, stroke_width=3, color=NO,
                     max_tip_length_to_length_ratio=0.3)
        il = label(r"$i < n$: \ load", font_size=17, color=YES).next_to(ptr, DOWN, buff=0.05)
        tl = label(r"$i \ge n$: \ trap", font_size=17, color=NO).next_to(ptr2, DOWN, buff=0.05)
        rule = MathTex(r"\text{load}(i)", r"=", r"\begin{cases} M[\,\text{base} + i\,] & i < n \\ "
                       r"\text{trap} & \text{otherwise} \end{cases}", font_size=30).move_to([3.6, -0.35, 0])
        wn = side_notes([
            (r"WebAssembly \ (in every major browser since 2017): \ a sandbox \textit{inside} a process; \ jumps only "
             r"to validated code, \ calls through a typed table", WHITE),
            (r"64-bit engines reserve the 4 GiB a 32-bit index can reach, \ plus guard pages: \ the bounds check "
             r"is Part 32's paging, \ done by the hardware", YES),
        ], width=5.6, size=18, buff=0.25).next_to(rule, DOWN, buff=0.35).set_x(3.6)
        with self.voiceover(
            "The browser is where these walls meet strangers' code every day. <bookmark mark='a'/> A privileged "
            "browser process talks to the network and the disk, and each site runs in its own sandboxed renderer. "
            "<bookmark mark='b'/> After Spectre, anything in the same address space could be read by speculation, so "
            "the wall between sites had to be a process, and in 2018 Chrome turned site isolation on by default on "
            "the desktop. <bookmark mark='c'/> Inside a page, WebAssembly, in every major browser since 2017, is a "
            "sandbox within a process: every load is checked against its linear memory, and control reaches only "
            "validated code. <bookmark mark='d'/> Sixty-four-bit engines reserve the whole range a thirty-two-bit "
            "index can reach, plus guard pages, so the bounds check is Part 32's paging, done in hardware."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bp), Create(links), FadeIn(rs), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(mem), FadeIn(ml), FadeIn(gl))
            self.play(GrowArrow(ptr), FadeIn(il), Write(rule), FadeIn(wn[0]))
            vo.wait_until("d")
            self.play(GrowArrow(ptr2), FadeIn(tl), FadeIn(wn[1]))
        self.wait(0.4)
        self.clear_scene()

    def enclaves(self):
        head = label(r"Enclaves, \ and their breaks", font_size=36).to_edge(UP, buff=0.3)
        layers = VGroup(*[box(t, c, 4.6, h=0.6, size=19, fill=0.12) for t, c in
                          ((r"application", DATA), (r"operating system \ --- \ locked out", NO),
                           (r"hypervisor \ --- \ locked out", NO),
                           (r"processor \ (the only thing trusted)", YES))]).arrange(DOWN, buff=0.12)
        layers.move_to([-3.9, 0.8, 0])
        layers[0][1].shift(LEFT * 1.0)
        enc = box(r"enclave", YES, 1.5, h=0.42, size=17, fill=0.3).move_to(layers[0]).shift(RIGHT * 1.35)
        lock = label(r"encrypted, \ attested", font_size=16, color=YES).next_to(layers[0], UP, buff=0.08)
        lock.align_to(enc, RIGHT)
        bits = [1, 0, 1, 1, 0, 0, 1, 0]
        ax = Line([0.6, -1.0, 0], [6.4, -1.0, 0], color=GREY_C, stroke_width=1.5)
        dots = VGroup()
        for k, bt in enumerate(bits):
            dots.add(Dot([0.95 + k * 0.72, 0.6 if bt else -0.4, 0], radius=0.11, color=HEAD))
        pl = VGroup(label(r"page 7", font_size=17, color=GREY_A).move_to([0.0, 0.6, 0]),
                    label(r"page 3", font_size=17, color=GREY_A).move_to([0.0, -0.4, 0]))
        bl = VGroup(*[label(str(bt), font_size=19, color=NO).move_to([0.95 + k * 0.72, -1.3, 0])
                      for k, bt in enumerate(bits)])
        tlab = label(r"pages the enclave faults on, \ in order \ (illustrative)", font_size=17,
                     color=GREY_A).move_to([3.5, 1.25, 0])
        blab = label(r"the secret's bits, \ read off", font_size=17, color=NO).next_to(bl, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"\textbf{controlled channel} \ (Xu, \ Cui \& Peinado, \ 2015): \ the OS still runs the "
                          r"enclave's page tables, \ so it sees which pages a secret-dependent branch touches", 6.4,
                          font_size=19, color=NO),
            wrapped_label(r"\textbf{Foreshadow} \ (2018): \ speculative execution \ (Chapter 4) \ read enclave memory "
                          r"through the L1 cache", 6.4, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.2, -2.55, 0])
        lesson = wrapped_label(r"an enclave shares the core, \ the caches and the page tables with the adversary it "
                               r"excludes", 5.6, font_size=19, color=HEAD).move_to([3.6, -2.75, 0])
        with self.voiceover(
            "Every wall so far trusts the kernel. An enclave turns that around. <bookmark mark='a'/> Intel's SGX, "
            "from 2015, lets an application seal a region of memory that the processor encrypts and keeps even from "
            "the operating system and the hypervisor, and it can attest to a remote party what code is inside. "
            "<bookmark mark='b'/> But the operating system still manages the enclave's page tables. In 2015 Xu, Cui "
            "and Peinado showed that it can unmap pages and watch which ones the enclave faults on; when a branch "
            "depends on a secret, that sequence spells it out. <bookmark mark='c'/> In 2018 Foreshadow used "
            "speculative execution to read enclave memory outright. <bookmark mark='d'/> An enclave still shares the "
            "core, the caches and the page tables with the adversary it excludes. Isolation is only as good as what "
            "is not shared."
        ) as vo:
            self.play(FadeIn(head), FadeIn(layers))
            vo.wait_until("a")
            self.play(FadeIn(enc), FadeIn(lock))
            self.play(Indicate(layers[1], color=NO, scale_factor=1.04), Indicate(layers[2], color=NO,
                                                                                 scale_factor=1.04))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(pl), FadeIn(tlab), FadeIn(notes[0]))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.25), run_time=2)
            self.play(LaggedStart(*[FadeIn(b) for b in bl], lag_ratio=0.15), FadeIn(blab))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono)
