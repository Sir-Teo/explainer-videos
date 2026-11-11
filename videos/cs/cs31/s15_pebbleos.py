from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, COST, DATA, HEAD, KERN, LAM, NO, PART, YES, code, fit_right, flow_box, gantt,
                                   load, time_axis)
from videos.cs.cs31.compute import TOK


class PebbleOS(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.timeline()
        self.breakdown()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"PebbleOS runs the Job", r"What does a kernel cost the Job?", lit=(1973,),
                            extra=((1973, r"pipes"),), part=PART)
        with self.voiceover("Chapter fourteen. PebbleOS runs the Job."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pipeline(self):
        head = label(r"The Job as two processes: \ \texttt{tok | job}", font_size=34).to_edge(UP, buff=0.3)
        y = 1.7
        tape = flow_box(r"the tape", GREY_B, 1.5, 0.7, 19).move_to([-5.6, y, 0])
        tok = flow_box(r"\texttt{tok}", DATA, 1.4, 0.7, 21).move_to([-2.8, y, 0])
        pipe = flow_box(r"pipe \ (4 KiB)", KERN, 1.9, 0.7, 19).move_to([0.0, y, 0])
        job = flow_box(r"\texttt{job}", HEAD, 1.4, 0.7, 21).move_to([2.8, y, 0])
        con = flow_box(r"console", GREY_B, 1.5, 0.7, 19).move_to([5.6, y, 0])
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.2) for a, b in
                        ((tape, tok), (tok, pipe), (pipe, job), (job, con))])
        tags = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(a, UP, buff=0.08) for t, a in zip(
            (r"\texttt{read}", r"\texttt{write}", r"\texttt{read}", r"\texttt{write}"), arrs)])
        src = code(TOK.strip().splitlines(), size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 1.2)
        notes = VGroup(
            label(r"\texttt{tok}: \ the text in, \ one lower-case word \\ per line out \ (Pebble language, \ 18 lines)",
                  font_size=21, color=DATA),
            label(r"\texttt{job}: \ Part 17's hash table, \ unchanged: \\ it reads the words as if they were the "
                  r"novels", font_size=21, color=HEAD),
            label(r"both compiled by Part 13's compiler for PebbleOS: \\ \texttt{getc} and \texttt{putc} become calls "
                  r"into \\ the 4 KiB-buffered library", font_size=21, color=WHITE),
            label(r"the kernel: \ moves bytes, \ blocks whichever end \\ must wait, \ preempts every 20{,}000 "
                  r"instructions", font_size=21, color=KERN),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(src, RIGHT, buff=0.5).align_to(src, UP)
        fit_right(notes)
        with self.voiceover(
            "Now PebbleOS runs the Job, and the Job becomes two processes, joined by a pipe, as a Unix user would "
            "write it. <bookmark mark='a'/> The first process, tok, reads the text from the tape and writes one "
            "lower-case word per line. It is eighteen lines of our own language. <bookmark mark='b'/> The second, "
            "job, is Part 17's hash-table program, unchanged. It reads words from the pipe as if they were the "
            "novels, and prints the same twenty lines. <bookmark mark='c'/> Both are compiled by Part 13's compiler "
            "with one change: get-c and put-c become calls into the small library, which talks to the kernel four "
            "kibibytes at a time. <bookmark mark='d'/> The kernel moves the bytes, blocks whichever end has to wait, "
            "and preempts each process after twenty thousand instructions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tape), FadeIn(tok), FadeIn(pipe), FadeIn(job), FadeIn(con),
                      LaggedStart(*[GrowArrow(a) for a in arrs]), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def timeline(self):
        p = load("pebbleos")
        s = p["short"]
        head = label(rf"{s['bytes']:,} bytes through the pipeline".replace(",", "{,}"), font_size=34).to_edge(UP,
                                                                                                         buff=0.3)
        T = s["steps"]
        g = gantt(s["timeline"], 0, T, width=11.4, h=0.45, lanes=["tok", "job", "kernel"], font=19)
        g.move_to([0.4, 1.6, 0])
        fill = s["fill"]
        ax = Axes(x_range=[0, len(fill), len(fill)], y_range=[0, 4096, 4096], x_length=11.4, y_length=1.5,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([0.4, -0.6, 0])
        pts = [ax.c2p(i, v) for i, v in enumerate(fill)]
        fl = VMobject(color=KERN, stroke_width=2).set_points_as_corners(pts)
        fln = label(r"bytes in \\ the pipe", font_size=17, color=KERN).next_to(ax, LEFT, buff=0.1).shift(DOWN * 0.2)
        fln.scale_to_fit_width(min(fln.width, 1.5))
        full = label(r"4096: \ full", font_size=15, color=GREY_B).next_to(ax.c2p(0, 4096), LEFT, buff=0.05)
        xa = time_axis(g, [0, 200000, 400000, 600000, 800000], y=ax.get_bottom()[1], font=13)
        xl = label(r"instructions", font_size=15, color=GREY_B).next_to(xa, DOWN, buff=0.05)
        r = s["report"]
        notes = VGroup(
            label(rf"{r['switches']} switches, \ {r['ticks']} timer interrupts, \ {r['blocks']} wait for the pipe, "
                  rf"\ {r['syscalls']} system calls", font_size=20, color=WHITE),
            label(r"tok fills the pipe in bursts; \ job drains it, \ and both share the processor in 20{,}000-"
                  r"instruction slices", font_size=20, color=GREY_A),
            label(rf"output: \ byte for byte the Job's twenty lines \ (checked on all {len(p['samples'])} "
                  rf"passages)", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is a short passage of seven thousand bytes going through. <bookmark mark='a'/> The top chart shows "
            "who has the processor: tok in blue, job in yellow, the kernel in orange between them. <bookmark "
            "mark='b'/> Below, the number of bytes waiting in the pipe. Tok writes in four-kibibyte bursts, and the "
            "pipe fills; job reads, and it drains. <bookmark mark='c'/> Fifteen context switches, thirty-eight timer "
            "interrupts, a dozen system calls, and once, the job had to wait for an empty pipe. <bookmark "
            "mark='d'/> Neither program knows the other exists, or that it is being interrupted. <bookmark "
            "mark='e'/> And the output is byte for byte the Job's twenty lines, on every one of the thirty-two test "
            "passages."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.lane_labels), LaggedStart(*[FadeIn(b) for b in g.bars], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(fln), FadeIn(full), FadeIn(xa), FadeIn(xl), Create(fl), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def breakdown(self):
        p = load("pebbleos")
        head = label(r"Where the instructions go, \ per byte of the novels", font_size=34).to_edge(UP, buff=0.3)
        pb = p["per_byte"]
        sc = 0.083
        parts = [("tok", pb["tok"], DATA), ("job", pb["job"], HEAD), ("kernel", pb["kernel"], KERN)]
        bar = VGroup()
        x = -5.9
        for name, v, c in parts:
            r = Rectangle(width=v * sc, height=0.7, stroke_width=0, fill_color=c, fill_opacity=0.85)
            r.move_to([x + v * sc / 2, 1.4, 0])
            x += v * sc
            bar.add(VGroup(r, label(rf"{name} \ {v:.1f}", font_size=18, color=BG).move_to(r)))
        tot = sum(v for _, v, _ in parts)
        bt = label(rf"{tot:.0f} instructions a byte", font_size=21, color=WHITE).next_to(bar, RIGHT, buff=0.25)
        r8 = Rectangle(width=p["row8_per_byte"] * sc, height=0.7, stroke_width=0, fill_color=GREY_B,
                       fill_opacity=0.7).move_to([-5.9 + p["row8_per_byte"] * sc / 2, 0.3, 0])
        r8l = label(rf"row 8, \ bare metal: \ {p['row8_per_byte']:.1f}", font_size=18, color=BG).move_to(r8)
        e = p["errors"]
        notes = VGroup(
            label(r"the kernel's 23 a byte: \ copying bytes one at a time, \ tape to tok, \ tok to pipe, \ pipe to "
                  r"job", font_size=20, color=KERN),
            label(r"tok is new work; \ job pays 11 more a byte for calling \texttt{getc} through the library",
                  font_size=20, color=WHITE),
            label(rf"the job alone under PebbleOS, \ reading the tape: \ {p['alone_ratio']:.2f}$\times$ its bare "
                  r"instructions", font_size=20, color=GREY_A),
            label(rf"the full 25 MB from a model fitted on 24 passages: \ held-out errors {e['tok'] * 100:.2f}\%, \ "
                  rf"{e['job'] * 100:.2f}\%, \ {e['kernel'] * 100:.1f}\%", font_size=20, color=GREY_A),
            label(r"the cure for copying: \ share pages \ (Part 32), \ and move data without the processor "
                  r"\ (Part 34)", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(r8, DOWN, buff=0.55).to_edge(LEFT, buff=0.9)
        fit_right(notes)
        with self.voiceover(
            "What does all this cost? We ran the pipeline on thirty-two passages and counted every instruction, in "
            "each process and in the kernel, then fitted the counts and projected them to all thirty novels. "
            "<bookmark mark='a'/> Per byte of text: thirty-four instructions in tok, fifty in job, and twenty-three "
            "in the kernel. A hundred and seven in all. <bookmark mark='b'/> The bare program of Part 17 needed "
            "thirty-nine. <bookmark mark='c'/> The kernel's share is almost all copying, one byte at a time: from the "
            "tape into tok, from tok into the pipe, from the pipe into job. <bookmark mark='d'/> Tok is extra work the "
            "single program never did, and job pays eleven more instructions a byte because every get-c is now a "
            "function call. <bookmark mark='e'/> Run alone under PebbleOS, the job needs one point four four times "
            "its bare instructions. <bookmark mark='f'/> The fitted counts match passages held out of the fit to "
            "within about two percent. <bookmark mark='g'/> Copying is the price here, and later parts remove it: Part 32 "
            "lets processes share pages, and Part 34 moves data without the processor touching each byte."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.3), FadeIn(bt))
            vo.wait_until("b")
            self.play(FadeIn(r8), FadeIn(r8l))
            for mk, n_ in zip("cdefg", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        p = load("pebbleos")
        led = p["ledger"]
        row = led[-1]
        head = label(r"Ledger row 11", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.33,
                           label_width=4.8).scale(0.92).move_to(UP * 0.9)
        r8 = p["row8"]
        notes = VGroup(
            label(rf"{row['instructions'] / 1e9:.2f} billion instructions on Part 8's core, \ at row 8's IPC and "
                  rf"memory stalls, \ plus {p['trap_cycles']} cycles for each trap and \texttt{{eret}}",
                  font_size=20, color=WHITE),
            label(rf"{row['seconds']:.2f} s, \ against {r8['seconds']:.2f} s for the bare program: \ "
                  rf"{row['seconds'] / r8['seconds']:.1f}$\times$ slower", font_size=21, color=NO),
            label(r"and worth it: \ the two programs are protected from each other, \ interruptible, \ and joined "
                  r"by a pipe neither had to know about", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the ledger gets row eleven. <bookmark mark='a'/> Two point six seven billion instructions, priced on "
            "Part 8's out-of-order core at the same rate as row eight, with the same memory stalls, and thirty-five "
            "cycles of pipeline drain for every trap and every return. <bookmark mark='b'/> Two point one seven "
            "seconds, against point eight one for the bare program: two point seven times slower. Like the "
            "garbage-collected row of Part 15, it goes backwards, and that is the honest result. <bookmark mark='c'/> "
            "An operating system does not make one program faster. It makes many programs safe from one another, "
            "lets them share the machine, and lets two programs that know nothing about each other work as one. "
            "Making that cheap is the work of the next three parts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
