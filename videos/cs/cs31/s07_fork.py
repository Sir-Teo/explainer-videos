from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code, fit_right, load, mono)


class Fork(VoiceoverScene):
    def construct(self):
        self.card()
        self.api()
        self.shell()
        self.costs()

    def card(self):
        card = chapter_card(6, r"fork, \ exec and wait", r"How does one process start another?",
                            lit=(1969, 1973, 2019), extra=((1973, r"pipes"), (2019, r"``A fork() in the road''")),
                            part=PART)
        with self.voiceover("Chapter six. Fork, exec, and wait."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def api(self):
        head = label(r"Unix's three calls", font_size=36).to_edge(UP, buff=0.3)
        y0 = 1.6
        sh = Line([-6, y0, 0], [5.8, y0, 0], color=DATA, stroke_width=5)
        shl = label(r"shell", font_size=20, color=DATA).next_to(sh, LEFT, buff=0.15)
        fx = -3.6
        f = Dot([fx, y0, 0], color=WHITE, radius=0.08)
        fl = mono("fork()", 18, WHITE).next_to(f, UP, buff=0.12)
        child = VMobject(color=HEAD, stroke_width=5).set_points_as_corners(
            [[fx, y0, 0], [fx + 0.5, y0 - 1.3, 0], [0.4, y0 - 1.3, 0]])
        cl = label(r"child: \ a copy of the shell", font_size=18, color=HEAD).next_to(child, DOWN, buff=0.12).shift(
            LEFT * 0.6)
        dup = mono("dup2(fd, 1)", 16, HEAD).move_to([-1.6, y0 - 0.95, 0])
        ex = Dot([0.4, y0 - 1.3, 0], color=WHITE, radius=0.08)
        exl = mono('exec("ls")', 18, WHITE).next_to(ex, UP, buff=0.12)
        ls = Line([0.4, y0 - 1.3, 0], [3.2, y0 - 1.3, 0], color=YES, stroke_width=5)
        lsl = label(r"now it is \texttt{ls}: \ same process, \ new program", font_size=18, color=YES).next_to(
            ls, DOWN, buff=0.12)
        xe = Dot([3.2, y0 - 1.3, 0], color=WHITE, radius=0.08)
        xel = mono("exit(0)", 16, WHITE).next_to(xe, RIGHT, buff=0.12)
        w = Dot([3.4, y0, 0], color=WHITE, radius=0.08)
        wl = mono("wait()", 18, WHITE).next_to(w, UP, buff=0.12)
        wa = DashedLine([3.2, y0 - 1.25, 0], [3.4, y0 - 0.05, 0], color=GREY_B)
        lines = VGroup(
            label(r"\texttt{fork}: \ the process becomes two, \ identical but for one return value \ (0 in the child)",
                  font_size=21, color=WHITE),
            label(r"\texttt{exec}: \ replace this process's program with another; \ files stay open",
                  font_size=21, color=YES),
            label(r"\texttt{wait}: \ sleep until a child exits, \ and collect its exit code", font_size=21,
                  color=GREY_A),
            label(r"why two calls, \ not one? \ between them the child can rearrange its own files, \ with "
                  r"ordinary calls: \ redirection and pipes for free", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Unix creates processes with three calls. <bookmark mark='a'/> Fork makes the calling process into two. "
            "Parent and child are identical, with the same memory contents and the same open files, except that fork "
            "returns zero in the child and the child's number in the parent. <bookmark mark='b'/> Exec replaces the "
            "program a process is running with another, keeping the same process and its open files. <bookmark "
            "mark='c'/> And wait puts the parent to sleep until a child exits, then hands back its exit code. "
            "<bookmark mark='d'/> Why separate fork from exec? Because in between, the child is still running the "
            "shell's code, and it can rearrange its own files with ordinary calls before becoming the new program. "
            "That is how output redirection and pipes work, with no special support in the call that starts the "
            "program."
        ) as vo:
            self.play(FadeIn(head), Create(sh), FadeIn(shl))
            vo.wait_until("a")
            self.play(FadeIn(f), FadeIn(fl), Create(child), FadeIn(cl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex), FadeIn(exl), Create(ls), FadeIn(lsl), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(xe), FadeIn(xel), Create(wa), FadeIn(w), FadeIn(wl), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(dup), FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def shell(self):
        d = load("fork")
        head = label(rf"A shell in {d['shell_lines']} lines of C", font_size=34).to_edge(UP, buff=0.25)
        src = code(d["shell_src"], size=13)
        if src.width > 8.6:
            src.scale_to_fit_width(8.6)
        if src.height > 4.7:
            src.scale_to_fit_height(4.7)
        src.next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.4)
        out = VGroup(*[mono(s, 18, YES) for s in d["shell_out"].rstrip().splitlines()]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        box_ = SurroundingRectangle(out, buff=0.2, color=GREY_B, corner_radius=0.08)
        ins = VGroup(mono("echo hello world", 17, GREY_A), mono("echo the cat sat |", 17, GREY_A),
                     mono("    tr a-z A-Z", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        il = label(r"typed:", font_size=20, color=GREY_B)
        right = VGroup(il, ins, label(r"printed:", font_size=20, color=GREY_B), VGroup(box_, out)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).next_to(src, RIGHT, buff=0.45).align_to(src, UP)
        fit_right(right)
        notes = VGroup(
            label(r"read a line; \ \texttt{fork}; \ in the child, \ \texttt{dup2} the pipe onto 0 or 1, "
                  r"\ then \texttt{exec}", font_size=21, color=WHITE),
            label(r"the parent waits for both children; \ then prompts again", font_size=21, color=GREY_A),
            label(r"a pipe is a kernel buffer with two ends: \ \texttt{tr} reads what \texttt{echo} writes, \ "
                  r"neither knowing", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "With those three calls a shell is short. This one is twenty-five lines of C, and it runs on this "
            "machine. <bookmark mark='a'/> It reads a line and splits it at a bar. For each command it forks; the "
            "child connects the pipe to its standard input or output with dup-two, then execs the command. "
            "<bookmark mark='b'/> The parent closes its copies of the pipe and waits for both children. <bookmark "
            "mark='c'/> We typed echo hello world, and then echo the cat sat, piped into tr, which translates lower "
            "case to upper. <bookmark mark='d'/> The pipe is a buffer inside the kernel with two ends. Echo writes "
            "into one; tr reads from the other; neither knows the other exists. Doug McIlroy pushed pipes into Unix "
            "in 1973, and they changed how people wrote programs: small tools, joined together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(right))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def costs(self):
        d = load("fork")
        head = label(r"What a new process costs, \ on this machine", font_size=34).to_edge(UP, buff=0.3)
        items = [(r"\texttt{fork}, \ child exits at once", d["fork_exit_us"], DATA),
                 (r"\texttt{fork} + \texttt{exec} \texttt{/bin/true}", d["fork_exec_us"], HEAD),
                 (r"\texttt{posix\_spawn}", d["spawn_us"], YES)]
        items += [(rf"\texttt{{fork}} with {mb} MiB in use", us, NO) for mb, us in d["mem"] if mb]
        mx = max(v for _, v, _ in items)
        rows = VGroup()
        for i, (nm, v, c) in enumerate(items):
            w = max(7.0 * v / mx, 0.05)
            r = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
            r.move_to([-1.6 + w / 2, 1.7 - i * 0.6, 0])
            t = label(nm, font_size=19, color=c).next_to(r, LEFT, buff=0.15).align_to([-1.75, 0, 0], RIGHT)
            s = f"{v / 1000:.1f} ms" if v >= 1000 else f"{v:.0f} $\\mu$s"
            rows.add(VGroup(r, t, label(s, font_size=19, color=WHITE).next_to(r, RIGHT, buff=0.12)))
        lines = VGroup(
            label(r"fork copies the address space's \textbf{map}, \ not its memory \ (copy-on-write, \ Part 32): "
                  r"\ still, \ more memory, \ slower fork", font_size=21, color=WHITE),
            label(r"Baumann et al. \ (2019), \ ``A fork() in the road'': \ fork no longer fits; \ use "
                  r"\texttt{posix\_spawn}", font_size=21, color=GREY_A),
            label(r"PebbleOS has no fork: \ with bounds and no relocation, \ a copy would need the same addresses "
                  r"\ (Part 32 fixes it)", font_size=21, color=KERN),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What does a new process cost? <bookmark mark='a'/> On this machine, a fork whose child exits at once "
            "takes a hundred and fifty microseconds. Fork followed by exec of a tiny program takes about a "
            "millisecond and a quarter, and posix-spawn, which does both in one call, about the same. <bookmark "
            "mark='b'/> But watch what happens when the parent is using memory. With a gibibyte in use, fork takes "
            "thirty-three milliseconds. <bookmark mark='c'/> Fork does not copy the memory itself: it copies the map "
            "of it, and marks every page to be copied later, only if someone writes. That trick is Part 32's. But "
            "the map grows with the memory. <bookmark mark='d'/> In 2019 researchers from Microsoft, Boston University and ETH "
            "Zurich argued that fork no longer fits modern systems, and that new code should use spawn. "
            "<bookmark mark='e'/> PebbleOS has no fork at all. With bounds but no relocation, a copy of a process "
            "would need the very same addresses. Part 32 gives each process its own addresses, and then fork "
            "becomes possible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:]], lag_ratio=0.3))
            for mk, ln in zip("cde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
