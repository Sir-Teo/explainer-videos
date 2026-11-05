from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.memory()
        self.realtime()
        self.futamura()
        self.warmup()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the limits of runtimes", r"What can a runtime not yet promise?",
                            lit=(2005,), extra=((2005, r"Hertz and Berger: \ the price of collection"),), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: the limits of runtimes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def memory(self):
        d = load("cost")
        head = label(r"How much memory does collection need?", font_size=34).to_edge(UP, buff=0.3)
        rows = [r for r in d["rows"] if not r.get("oom") and r["collections"]]
        L = d["peak_live"]
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 2.2, 0.5], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(LEFT * 3.3 + DOWN * 0.3)
        pts_ = [ax.c2p(2 * r["semispace"] / L, r["per_word"]) for r in rows]
        line = VMobject(color=YES, stroke_width=3).set_points_as_corners(pts_)
        dots = VGroup(*[Dot(p, radius=0.06, color=YES) for p in pts_])
        xt = VGroup(*[label(f"{v}" + r"$\times$", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (5, 10, 15, 20)])
        xl = label(r"memory, \ as a multiple of the live data", font_size=17, color=GREY_B).next_to(xt, DOWN,
                                                                                                 buff=0.12)
        yl = label(r"words copied per word allocated", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        side = VGroup(
            label(r"ours: \ the Job under Cheney's collector", font_size=20, color=YES),
            label(r"Hertz and Berger \ (2005), \ against ideal explicit freeing:", font_size=20, color=GREY_A),
            label(r"with 5$\times$ the memory: \ as fast", font_size=20, color=GREY_A),
            label(r"with 3$\times$: \ 17\% slower", font_size=20, color=GREY_A),
            label(r"with 2$\times$: \ nearly 70\% slower", font_size=20, color=NO),
            label(r"open: \ how close can a collector come to the live data, \ at what cost in time?",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4)
        if side.width > 5.8:
            side.scale_to_fit_width(5.8)
        with self.voiceover(
            "Chapter eight showed that a collector trades memory for time. How much memory? <bookmark mark='a'/> "
            "Here is our measurement again, now against the total memory as a multiple of the live data. Below "
            "about three times, the copying collector does more copying than the program does allocating. "
            "<bookmark mark='b'/> Matthew Hertz and Emery Berger measured the same trade for Java in 2005, against "
            "an oracle that frees every object at the last moment it is used. With five times the memory, a good "
            "collector was as fast as the oracle. With three times, seventeen percent slower. With twice, nearly "
            "seventy percent slower. <bookmark mark='c'/> How close a collector can get to the live data, and "
            "what it must pay in time to get there, is still an open question; partial lower bounds, such as "
            "Bendersky and Petrank's on collectors that may compact only part of the heap, are recent."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in side[1:5]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def realtime(self):
        head = label(r"Pauses you can promise", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"a short \textit{longest} pause is not enough: \ many short pauses close together are a long one",
                  font_size=21, color=GREY_A),
            label(r"\textbf{minimum mutator utilization}: \ in every window of $w$ ms, \ the program gets at least "
                  r"$u$ of the time", font_size=21, color=GREY_A),
            label(r"Metronome \ (Bacon, Cheng and Rajan, \ 2003): \ a collector \textit{scheduled} like a real-time "
                  r"task, \ with a proved bound", font_size=21, color=YES),
            label(r"it has run real-time Java in industrial and military systems; \ the bound needs the allocation rate "
                  r"to be known",
                  font_size=20, color=GREY_B),
            label(r"open: \ bounded pauses, \ bounded memory and high throughput, \ all at once, \ for any program",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Chapter ten measured pauses in microseconds. But a short longest pause is not the whole story. "
            "<bookmark mark='a'/> A thousand short pauses close together are, to the program, one long one. "
            "<bookmark mark='b'/> The right measure is minimum mutator utilization: in every window of, say, ten "
            "milliseconds, what fraction of the time does the program get? <bookmark mark='c'/> IBM's Metronome "
            "collector, by Bacon, Cheng and Rajan in 2003, schedules the collector like a real-time task and "
            "proves a bound on that fraction, <bookmark mark='d'/> provided the program's allocation rate and live "
            "data are known in advance; it has run real-time Java in industrial and military systems. <bookmark mark='e'/> A collector with bounded "
            "pauses, bounded memory and high throughput together, for every program, does not yet exist, and it "
            "is not known whether one can."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def futamura(self):
        head = label(r"Compilers from interpreters", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"\mathit{spec}(\mathit{interp},\ \mathit{prog}) \;=\; \text{a compiled } \mathit{prog}",
                    font_size=32, color=WHITE),
            MathTex(r"\mathit{spec}(\mathit{spec},\ \mathit{interp}) \;=\; \text{a compiler}", font_size=32,
                    color=WHITE),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"the \textbf{Futamura projections} \ (1971): \ specialize an interpreter to a program, \ and the "
                  r"interpretation disappears", font_size=21, color=GREY_A),
            label(r"PyPy \ (Bolz et al., \ 2009): \ write an interpreter; \ a \textbf{meta-tracing} JIT traces the "
                  r"interpreter running your loop", font_size=21, color=YES),
            label(r"Truffle and Graal \ (W\"urthinger et al., \ 2017): \ partial evaluation of interpreters, \ for "
                  r"JavaScript, \ Ruby, \ Python, \ R", font_size=21, color=YES),
            label(r"ours would qualify: \ the Pebble VM is an interpreter, \ and row 6 is the price of not "
                  r"specializing it", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(eqs, DOWN, buff=0.5)
        with self.voiceover(
            "Row six's factor of a hundred and fifty is the price of an interpreter. There is a beautiful way to "
            "remove it without writing a compiler. <bookmark mark='a'/> In 1971 Yoshihiko Futamura observed that "
            "if you specialize an interpreter to one fixed program, partially evaluating everything that depends "
            "only on the program, what remains is that program, compiled. Specialize the specializer to the "
            "interpreter, and you get a compiler. <bookmark mark='b'/> For decades this was theory. PyPy made it "
            "practical: you write an interpreter for your language, and a meta-tracing JIT traces the interpreter "
            "as it runs your hot loops. <bookmark mark='c'/> Oracle's Truffle and Graal do it by partial "
            "evaluation, and run JavaScript, Ruby, Python and R from interpreters alone. <bookmark mark='d'/> Our "
            "Pebble VM is exactly such an interpreter. How much of row six's factor such methods can recover, "
            "automatically and with guarantees, is active research."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def warmup(self):
        head = label(r"Do JITs even warm up?", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"the textbook story: \ slow at first, \ then compiled, \ then a steady peak", font_size=22,
                  color=GREY_A),
            label(r"Barrett et al. \ (2017): \ benchmarks on seven VMs, \ thousands of iterations each, \ with "
                  r"statistics",
                  font_size=21, color=GREY_A),
            label(r"many never reached a steady state; \ some got \textit{slower} as they ran", font_size=22,
                  color=NO),
            label(r"and correctness: \ WebAssembly's semantics, \ machine-checked \ (Watt, \ 2018); \ "
                  r"verified collectors \ (CakeML)", font_size=21, color=YES),
            label(r"open: \ JITs whose performance can be predicted, \ and runtimes proved correct end to end",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "One more surprise, and a warning about measurement. <bookmark mark='a'/> The textbook story of a JIT "
            "is that a program starts slow, gets compiled, and then runs at a steady peak. <bookmark mark='b'/> In "
            "2017 Edd Barrett and colleagues tested that story carefully, running benchmarks on seven virtual "
            "machines for thousands of iterations each, with proper statistics. <bookmark mark='c'/> Many benchmarks never "
            "reached a steady state at all, and some got slower the longer they ran. <bookmark mark='d'/> "
            "Correctness is a frontier too. WebAssembly's semantics has been checked by machine, and CakeML, an ML "
            "compiler verified in a proof assistant, includes a verified garbage collector. <bookmark mark='e'/> "
            "Runtimes whose speed can be predicted, and runtimes proved correct from bytecode to collector, remain "
            "open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def open(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"a collector with bounded pauses, \ constant memory overhead \ and constant work per word, \ or a "
                  r"proof that none exists", font_size=21, color=GREY_A),
            label(r"compilers derived from interpreters, \ with guaranteed speed", font_size=21, color=GREY_A),
            label(r"JIT performance that can be predicted, \ not just measured", font_size=21, color=GREY_A),
            label(r"a production runtime, \ JIT and concurrent collector included, \ proved correct", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is where the field stands. <bookmark mark='a'/> Is there a collector with bounded pauses, a "
            "constant factor of extra memory, and constant work per word allocated, all at once, or can one prove "
            "that no collector has all three? <bookmark mark='b'/> Can compilers derived from interpreters come "
            "with guarantees about their speed? <bookmark mark='c'/> Can a JIT's performance be predicted rather "
            "than measured? <bookmark mark='d'/> And can a whole production runtime, JIT and concurrent collector "
            "included, be proved correct? <bookmark mark='e'/> This part's research problem takes up the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
