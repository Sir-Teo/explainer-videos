from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


def core(name, color, jobs, pos):
    c = RoundedRectangle(width=1.3, height=0.8, corner_radius=0.1, stroke_color=color, stroke_width=2.5, fill_color=BG,
                         fill_opacity=1).move_to(pos)
    t = label(name, font_size=19, color=color).move_to(c)
    q = VGroup(*[Square(0.3, stroke_width=0, fill_color=jc, fill_opacity=0.85) for jc in jobs]).arrange(
        RIGHT, buff=0.05).next_to(c, DOWN, buff=0.15)
    return VGroup(c, t, q)


class Multi(VoiceoverScene):
    def construct(self):
        self.card()
        self.queues()
        self.stealing()

    def card(self):
        card = chapter_card(10, r"Many processors", r"How do you schedule a machine with many cores?",
                            lit=(1995, 1999), extra=((1995, r"Cilk"), (1999, r"work stealing, \ proved")),
                            part=PART)
        with self.voiceover("Chapter ten. Many processors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def queues(self):
        sw = load("switch")
        head = label(r"One queue, \ or one per core?", font_size=36).to_edge(UP, buff=0.3)
        shared = VGroup(*[Square(0.3, stroke_width=0, fill_color=c, fill_opacity=0.85)
                          for c in (DATA, HEAD, YES, LAM, NO, DATA, HEAD)]).arrange(RIGHT, buff=0.05)
        shared.move_to([-3.6, 1.7, 0])
        sl = label(r"one shared queue", font_size=20, color=WHITE).next_to(shared, UP, buff=0.15)
        cores1 = VGroup(*[core(f"core {i}", GREY_B, [], [-5.1 + i * 1.0, 0.3, 0]).scale(0.7) for i in range(4)])
        arrows = VGroup(*[Arrow(shared.get_bottom(), c.get_top(), buff=0.08, stroke_width=1.6, color=GREY_B)
                          for c in cores1])
        prob1 = label(r"every core locks the same queue; \ jobs hop between caches", font_size=18, color=NO).next_to(
            cores1, DOWN, buff=0.5)
        cores2 = VGroup(*[core(f"core {i}", c, js, [1.6 + i * 1.5, 1.3, 0]) for i, (c, js) in enumerate(
            ((DATA, [DATA, DATA, DATA]), (HEAD, [HEAD]), (YES, [YES, YES]), (LAM, [])))])
        sl2 = label(r"a queue per core \ (Linux, \ since 2.6)", font_size=20, color=WHITE).next_to(cores2, UP,
                                                                                               buff=0.25)
        mig = CurvedArrow(cores2[0][2].get_bottom() + DOWN * 0.05, cores2[3][0].get_bottom() + DOWN * 0.55,
                          angle=0.6, color=HEAD, stroke_width=2.2)
        ml = label(r"balance: \ an idle core pulls work", font_size=18, color=HEAD).next_to(mig, DOWN, buff=0.1)
        lines = VGroup(
            label(r"\textbf{affinity}: \ a job that stays on one core finds its data still in that core's caches",
                  font_size=21, color=YES),
            label(rf"waking a job on another core costs an interrupt between processors: \ "
                  rf"{sw['cross_cpu_ns'] / 1000:.0f} $\mu$s against {sw['same_cpu_ns'] / 1000:.1f} here \ (chapter 5)",
                  font_size=21, color=GREY_A),
            label(r"so: \ per-core queues, \ and occasional balancing, \ nearer cores first", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "With several processors, the first question is where the queue lives. <bookmark mark='a'/> One shared "
            "queue is simple and balances load perfectly, but every core must lock it to take a job, and a job runs "
            "on whichever core happens to be free, far from the data it left in another core's cache. <bookmark "
            "mark='b'/> So Linux, since version 2.6, keeps a queue per core. <bookmark mark='c'/> A job that stays on "
            "one core finds its data still in that core's caches. That is called affinity. <bookmark mark='d'/> "
            "Moving work is expensive. Waking a job on another core took twenty-five microseconds here, against three "
            "on the same one. <bookmark mark='e'/> But queues drift out of balance, so the kernel periodically moves "
            "work, from busy cores to idle ones, trying nearby cores first."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(shared), FadeIn(sl), FadeIn(cores1), LaggedStart(*[GrowArrow(a) for a in arrows]),
                      FadeIn(prob1))
            vo.wait_until("b")
            self.play(FadeIn(cores2), FadeIn(sl2))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(Create(mig), FadeIn(ml), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def stealing(self):
        d = load("smp")
        head = label(r"Work stealing", font_size=36).to_edge(UP, buff=0.3)
        rows = [[str(r["P"]), f"{r['makespan']:,}".replace(",", "{,}"), f"{r['bound']:,.0f}".replace(",", "{,}"),
                 f"{r['speedup']:.1f}", str(r["steals"])] for r in d["rows"]]
        tab = grid_table([r"workers $P$", r"time", r"$T_1/P + T_\infty$", r"speedup", r"steals"], rows,
                         widths=[2.0, 2.0, 2.6, 1.8, 1.6], row_h=0.4, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.3)
        t1 = f"{d['T1']:,}".replace(",", "{,}")
        notes = VGroup(
            label(r"each worker runs its own deque from the bottom; \ an idle one steals from the \textbf{top} of a "
                  r"random victim's", font_size=20, color=WHITE),
            label(rf"a fork-join tree: \ work $T_1$ = {t1}, \ span $T_\infty$ = {d['Tinf']}", font_size=19,
                  color=GREY_A),
            label(r"Blumofe and Leiserson \ (1999): \ expected time $T_1/P + O(T_\infty)$, \ and few steals",
                  font_size=20, color=YES),
            label(r"the top of a deque holds the oldest, \ biggest piece of work: \ one steal buys a lot",
                  font_size=20, color=HEAD),
            label(r"used by Cilk, \ Java's fork/join, \ Go, \ Rust's Rayon and Tokio \ (Part 10's fork-join)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.13).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "For programs that split themselves into many small tasks, there is a better scheme than a balancer. "
            "<bookmark mark='a'/> Each worker keeps its own double-ended queue of tasks, pushing and popping at the "
            "bottom. A worker that runs out picks another at random and steals from the top of its queue. <bookmark "
            "mark='b'/> We simulated a fork-join computation with eighty-three thousand units of work and a critical "
            "path of seventy-one. <bookmark mark='c'/> Blumofe and Leiserson proved in 1999 that work stealing "
            "finishes in expected time the work divided by the workers, plus a multiple of the critical path. "
            "<bookmark mark='d'/> The simulation sits right on that line, up to sixty-four workers, which run "
            "sixty times faster with only four hundred and eighty-seven steals. <bookmark mark='e'/> Steals are rare "
            "because the top of a queue holds the oldest task, which is usually the biggest. <bookmark mark='f'/> "
            "This is the scheduler inside Cilk, Java's fork-join pool, Go's runtime, and Rust's Rayon and Tokio."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
            vo.wait_until("f")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()
