from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, edge_arrow, fit_right, grid_table, load,
                                   state_node)


class Process(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.states()

    def card(self):
        card = chapter_card(4, r"The process", r"What exactly is a running program?",
                            lit=(1965, 1969), extra=((1965, r"Multics: \ processes"), (1969, r"Unix")), part=PART)
        with self.voiceover("Chapter four. The process."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def anatomy(self):
        d = load("process")
        head = label(r"A process: \ a program, \ running, \ with its own state", font_size=34).to_edge(UP, buff=0.3)
        H = 4.3
        cols = {"library": CODE, "buffers": DATA, "compiled code": CODE, "globals": HEAD, "free": GREY_D,
                "stack": YES}
        span = d["hi"] - d["lo"]
        strip = VGroup()
        y = 2.25
        tags = VGroup()
        for name, a, b in d["parts"]:
            hh = max(H * (b - a) / span, 0.3)
            r = Rectangle(width=1.6, height=hh, stroke_color=BG, stroke_width=1, fill_color=cols[name],
                          fill_opacity=0.8 if name != "free" else 0.25)
            r.move_to([-4.6, y - hh / 2, 0])
            y -= hh
            strip.add(r)
            size = b - a
            sz = f"{size // 1024} KiB" if size >= 4096 else f"{size} B"
            tags.add(label(rf"{name}: \ {sz}", font_size=17, color=cols[name] if name != "free" else GREY_B)
                     .next_to(r, RIGHT, buff=0.2))
        lo = label(r"\texttt{lo} = 1 MiB", font_size=17, color=GREY_B).next_to(strip, UP, buff=0.08)
        hi = label(r"\texttt{hi} = 2 MiB", font_size=17, color=GREY_B).next_to(strip, DOWN, buff=0.08)
        tab = grid_table([r"PCB field", r"holds"], [[f, h] for f, h in d["fields"]], widths=[2.4, 4.6], row_h=0.46,
                         font_size=19, mono_cols=(0,))
        tab.move_to([3.1, 0.55, 0])
        tl = label(rf"the \textbf{{process control block}}: \ {d['pcb_bytes']} bytes in the kernel's memory",
                   font_size=20, color=KERN).next_to(tab, UP, buff=0.2)
        lines = VGroup(
            label(r"the job's memory: \ its code, \ its 512 KiB hash table, \ a stack at the top", font_size=21,
                  color=WHITE),
            label(rf"PebbleOS keeps {d['nproc']} PCBs in a table; \ Linux's \texttt{{task\_struct}} has hundreds of "
                  r"fields", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        fit_right(lines)
        with self.voiceover(
            "A process is a program while it runs: the code, plus everything that changes as it runs. <bookmark "
            "mark='a'/> Here is the job's process under PebbleOS: one mebibyte of memory, from its lower bound to its "
            "upper bound. At the bottom, the small library that every process links, and its two buffers. Then the "
            "compiled code of the Job itself, under two kibibytes. Then its globals, mostly the hash table from Part "
            "17. And at the top, the stack, growing down. <bookmark mark='b'/> The rest of the process lives in the "
            "kernel, in its process control block. <bookmark mark='c'/> Its state; its fifteen registers and its "
            "program counter, saved at every trap; its bounds; its number; where its input comes from and its output "
            "goes; and a few counters. <bookmark mark='d'/> That is everything the kernel needs to stop a program at "
            "any instruction, and later resume it as if nothing had happened. <bookmark mark='e'/> PebbleOS keeps "
            "four of these blocks in a table. The Linux equivalent has hundreds of fields, but the same idea."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.2), FadeIn(lo), FadeIn(hi),
                      LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def states(self):
        d = load("pebbleos")["short"]
        head = label(r"The life of a process", font_size=36).to_edge(UP, buff=0.3)
        new = state_node(r"new", GREY_B, [-5.6, 1.2, 0], font=24)
        ready = state_node(r"ready", HEAD, [-2.3, 1.2, 0], font=24)
        run = state_node(r"running", YES, [2.3, 1.2, 0], font=24)
        done = state_node(r"exited", GREY_B, [5.6, 1.2, 0], font=24)
        blk = state_node(r"blocked", NO, [0.0, -1.0, 0], font=24)
        r = d["report"]
        disp = sum(p["dispatched"] for p in d["procs"])
        a1 = edge_arrow(new, ready, r"loaded", font=19)
        a2 = edge_arrow(ready, run, rf"dispatched \ ({disp})", bend=-0.6, font=19, side=UP)
        a3 = edge_arrow(run, ready, rf"timer \ ({r['ticks']})", bend=-0.6, font=19, side=DOWN)
        a4 = edge_arrow(run, blk, rf"waits for the pipe \ ({r['blocks']})", font=19, side=RIGHT)
        a5 = edge_arrow(blk, ready, r"woken", font=19, side=LEFT)
        a6 = edge_arrow(run, done, r"\texttt{exit} \ (2)", font=19)
        nb = f"{d['bytes']:,}".replace(",", "{,}")
        lines = VGroup(
            label(rf"counted in PebbleOS, \ running the Job on {nb} bytes as two processes", font_size=21,
                  color=WHITE),
            label(r"one process \textbf{running} per processor; \ any number \textbf{ready}; \ \textbf{blocked} ones "
                  r"cost nothing until woken", font_size=21, color=GREY_A),
            label(r"the scheduler's whole job: \ which ready process runs next \ (chapters 7--11)", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every process moves through a few states. <bookmark mark='a'/> It is created and loaded, and becomes "
            "ready: able to run, waiting for a processor. <bookmark mark='b'/> The kernel dispatches it, and it runs. "
            "<bookmark mark='c'/> When the timer fires, it goes back to ready, and another process gets the "
            "processor. <bookmark mark='d'/> When it asks for something that is not there yet, like bytes from an "
            "empty pipe, it is blocked, and costs nothing until the bytes arrive and it is woken. <bookmark "
            "mark='e'/> When it calls exit, it is finished. <bookmark mark='f'/> The numbers are counted in PebbleOS, "
            "while our two processes ran the Job on a short passage: forty-one dispatches, thirty-eight timer "
            "interrupts, one wait for the pipe. <bookmark mark='g'/> At any moment one process per processor is "
            "running, and any number may be ready. <bookmark mark='h'/> Choosing which ready process runs next is "
            "the scheduler's whole job, and the subject of chapters seven to eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(new))
            vo.wait_until("a")
            self.play(FadeIn(ready), FadeIn(a1))
            vo.wait_until("b")
            self.play(FadeIn(run), FadeIn(a2))
            vo.wait_until("c")
            self.play(FadeIn(a3))
            vo.wait_until("d")
            self.play(FadeIn(blk), FadeIn(a4), FadeIn(a5))
            vo.wait_until("e")
            self.play(FadeIn(done), FadeIn(a6))
            vo.wait_until("f")
            self.play(FadeIn(lines[0]))
            vo.wait_until("g")
            self.play(FadeIn(lines[1]))
            vo.wait_until("h")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
