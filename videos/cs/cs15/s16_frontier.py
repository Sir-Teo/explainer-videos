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
        ax = Axes(x_range=[0, max(20, 1.1*max(2*r["semispace"]/L for r in rows)), 5],
                  y_range=[0, max(2.2, 1.15*max(r["per_word"] for r in rows)), .5], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(LEFT * 3.3 + DOWN * 0.3)
        pts_ = [ax.c2p(2 * r["semispace"] / L, r["per_word"]) for r in rows]
        line = VMobject(color=YES, stroke_width=3).set_points_as_corners(pts_)
        dots = VGroup(*[Dot(p, radius=0.06, color=YES) for p in pts_])
        xt = VGroup(*[label(f"{v}" + r"$\times$", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (5, 10, 15, 20)])
        yt = VGroup(*[label(str(v), font_size=15, color=GREY_B).next_to(ax.c2p(0,v), LEFT, buff=.12)
                      for v in (0,1,2)])
        xl = label('reserved memory / collection-sampled live peak', font_size=17, color=GREY_B).next_to(xt, DOWN,
                                                                                                 buff=0.12)
        yl = label(r"words copied per word allocated", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        side = VGroup(
            label(r"ours: \ the Job under Cheney's collector", font_size=20, color=YES),
            label('Hertz and Berger (2005): selected workloads, reachability oracle', font_size=20, color=GREY_A),
            label(r"with 5$\times$ the memory: \ as fast", font_size=20, color=GREY_A),
            label(r"with 3$\times$: \ 17\% slower", font_size=20, color=GREY_A),
            label(r"with 2$\times$: \ nearly 70\% slower", font_size=20, color=NO),
            label('state machine, root, object and movement assumptions before a bound',
                  font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4)
        if side.width > 5.8:
            side.scale_to_fit_width(5.8)
        with self.voiceover(
            (
            "Memory can buy less collection work, but state the cost model. <bookmark mark='a'/> Our curve shows "
            "copied words per allocated word against reserved memory divided by a collection-sampled live-set "
            "estimate. It does not plot measured wall time. <bookmark mark='b'/> Hertz and Berger's 2005 study "
            "compared selected Java workloads with an oracle that freed objects just before they became "
            "unreachable, not at their semantic last access. For their historical Appel collector, five times the "
            "memory matched explicit management, three times was seventeen percent slower, and twice was about "
            "seventy percent slower. <bookmark mark='c'/> Those are scoped empirical results. A modern "
            "collector's memory-time bounds depend on its machine, root and object model, movement policy, and "
            "workload. Define those assumptions before comparing measurements or claiming a lower bound."
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
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
            label('start from known real-time bounds; specify a precise extension',
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            (
            "A measured maximum pause is not a real-time guarantee. <bookmark mark='a'/> Many short pauses close "
            "together can still prevent useful progress. <bookmark mark='b'/> Minimum mutator utilization asks "
            "how much program time is guaranteed in every window of a specified length. <bookmark mark='c'/> "
            "Metronome schedules collection to obtain utilization guarantees under its allocation and live-data "
            "assumptions. <bookmark mark='d'/> Earlier work by Blelloch and Cheng already gives explicit "
            "real-time copying bounds, including terms for reachable space, object count, processors and object "
            "depth. A vague three-way goal is therefore not one unsolved theorem. <bookmark mark='e'/> Meaningful "
            "research starts from an established bound and specifies what should improve: constants, root "
            "handling, object-size limits, scheduling, or a different machine model. Then prove or measure that "
            "particular extension."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def futamura(self):
        head = label(r"Compilers from interpreters", font_size=34).to_edge(UP, buff=0.3)
        def block(text,width,color):
            r=RoundedRectangle(width=width,height=.9,corner_radius=.1,color=color,fill_color=color,fill_opacity=.1)
            t=label(text,font_size=21,color=color)
            if t.width>width-.25:t.scale_to_fit_width(width-.25)
            return VGroup(r,t.move_to(r))
        inputs=block('interpreter + fixed program',3.5,DATA)
        specializer=block('specialize',2.0,HEAD)
        residual=block('residual program(input)',3.6,YES)
        row=VGroup(inputs,specializer,residual).arrange(RIGHT,buff=.9)
        arrows=VGroup(*[Arrow(x.get_right(),y.get_left(),buff=.08,color=GREY_B,tip_length=.13)
                         for x,y in zip(row,row[1:])])
        eqs=VGroup(VGroup(row,arrows),
                  MathTex(r"\mathit{spec}(\mathit{spec},\ \mathit{interp})=\text{a compiler}",font_size=28)
                 ).arrange(DOWN,buff=.35).next_to(head,DOWN,buff=.5)
        pts = VGroup(
            label('Futamura (1971): specialize an interpreter with respect to a fixed program', font_size=21, color=GREY_A),
            label(r"PyPy \ (Bolz et al., \ 2009): \ write an interpreter; \ a \textbf{meta-tracing} JIT traces the "
                  r"interpreter running your loop", font_size=21, color=YES),
            label(r"Truffle and Graal \ (W\"urthinger et al., \ 2017): \ partial evaluation of interpreters, \ for "
                  r"JavaScript, \ Ruby, \ Python, \ R", font_size=21, color=YES),
            label('specialization may remove dispatch; the ledger also includes other costs', font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(eqs, DOWN, buff=0.5)
        with self.voiceover("Can we derive compiled code from an interpreter? <bookmark mark='a'/> Fix the source program and specialize an interpreter with respect to it. A suitable partial evaluator leaves a residual program that still accepts the runtime input. The diagram separates that fixed program from the input that remains unknown. Specializing the specializer with respect to the interpreter yields a compiler: the second Futamura projection. <bookmark mark='b'/> PyPy's meta-tracing takes a different route, tracing interpreter execution along hot paths. <bookmark mark='c'/> Truffle and Graal use interpreter partial evaluation with supporting annotations and runtime machinery. <bookmark mark='d'/> These methods can remove dispatch and expose optimization opportunities. They do not guarantee removal of all interpretation cost or recovery of our ledger's entire gap; representation and algorithms still matter.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(eqs), FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[1]))
            vo.wait_until('c')
            self.play(FadeIn(pts[2]))
            vo.wait_until('d')
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
            label('integrate verified components with production JITs and native interfaces',
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            (
            "Measurement needs more than one appealing run. <bookmark mark='a'/> The usual JIT story predicts a "
            "slow start followed by a stable compiled peak. <bookmark mark='b'/> Barrett and colleagues tested "
            "that story in 2017 with many iterations across seven virtual machines. <bookmark mark='c'/> Their "
            "benchmarks did not all reach a stable peak; some slowed down. Our best-of-three tables are small "
            "illustrations, not that kind of steady-state study. <bookmark mark='d'/> Correctness has strong "
            "starting points too: mechanized WebAssembly semantics and verified compiler and collector components "
            "in projects such as CakeML. <bookmark mark='e'/> Integrating those guarantees with a specified "
            "production JIT, concurrency model and native interface is a more precise research goal than claiming "
            "that no runtime has ever been verified."
        )
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
            label('improve a specified known collector bound under explicit assumptions', font_size=21, color=GREY_A),
            label(r"compilers derived from interpreters, \ with guaranteed speed", font_size=21, color=GREY_A),
            label(r"JIT performance that can be predicted, \ not just measured", font_size=21, color=GREY_A),
            label(r"a production runtime, \ JIT and concurrent collector included, \ proved correct", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover("Here are useful research directions with explicit scope. <bookmark mark='a'/> Start from a known real-time collector bound. State the machine, allocation rate, roots, object sizes and liveness limits, then seek a precise improvement or matching lower bound. <bookmark mark='b'/> Can interpreter-derived compilers provide useful performance guarantees for a defined class of programs? <bookmark mark='c'/> Can JIT performance be predicted across changing phases rather than summarized by a best run? <bookmark mark='d'/> How far can verified compilation and collection be integrated with production concurrency, native interfaces and optimizing JITs? Existing verified components provide starting points. <bookmark mark='e'/> This part's research exercise chooses the first direction and asks for a model, a baseline theorem and a testable extension.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, q in zip('abcd', qs):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
