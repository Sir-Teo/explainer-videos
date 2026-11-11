from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, NO, PART, T0C, T1C, YES, grid_table, load, mono, num)


class Race(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.checker()
        self.counts()

    def card(self):
        card = chapter_card(2, r"The race", r"How many ways can two threads interleave?", lit=(1981,),
                            extra=((1981, r"Clarke, \ Emerson; \ Queille, \ Sifakis: \ model checking"),), part=PART)
        with self.voiceover("Chapter two. The race."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        d = load("tree")
        sch = d["schedules"]
        head = label(r"Every schedule of two increments", font_size=34).to_edge(UP, buff=0.3)
        n = len(sch)
        W = 12.4
        xs = {s["order"]: -W / 2 + W * (i + 0.5) / n for i, s in enumerate(sch)}
        y0, dy = 2.4, 0.66
        pos = {}
        for depth in range(6, -1, -1):
            prefixes = sorted({s["order"][:depth] for s in sch})
            for p in prefixes:
                kids = [xs[s["order"]] for s in sch if s["order"].startswith(p)]
                pos[p] = (sum(kids) / len(kids), y0 - dy * depth)
        edges = VGroup()
        for p, (x, y) in pos.items():
            if not p:
                continue
            px, py = pos[p[:-1]]
            c = T0C if p[-1] == "0" else T1C
            edges.add(Line([px, py, 0], [x, y, 0], color=c, stroke_width=2).set_z_index(-1))
        dots = VGroup(*[Dot([x, y, 0], radius=0.05, color=GREY_B) for p, (x, y) in pos.items() if len(p) < 6])
        leaves = VGroup()
        for s in sch:
            x, y = pos[s["order"]]
            c = YES if s["c"] == 2 else NO
            leaves.add(VGroup(Circle(radius=0.2, color=c, fill_color=c, fill_opacity=0.35).move_to([x, y - 0.3, 0]),
                              MathTex(str(s["c"]), font_size=22, color=WHITE).move_to([x, y - 0.3, 0])))
        key = VGroup(label(r"left: \ thread A takes a step", font_size=18, color=T0C),
                     label(r"right: \ thread B", font_size=18, color=T1C)).arrange(RIGHT, buff=0.6).next_to(
            head, DOWN, buff=0.12)
        f = MathTex(r"\binom{6}{3} = 20 \text{ schedules}", font_size=34, color=WHITE)
        lines = VGroup(
            label(rf"{n - d['lost']} of {n} give 2: \ only those where one thread finishes before the other starts",
                  font_size=21, color=YES),
            label(rf"the other {d['lost']} give 1: \ a lost update", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        f.next_to(lines, UP, buff=0.25)
        with self.voiceover(
            "How many ways can two threads interleave three instructions each? <bookmark mark='a'/> Draw it as a tree. "
            "At each step, either thread A or thread B takes its next instruction: left for A, right for B. "
            "<bookmark mark='b'/> Every path from the top to a leaf is one schedule, and each leaf shows the final "
            "count. <bookmark mark='c'/> There are six choose three, twenty schedules, one for each way to place A's "
            "three steps among the six. <bookmark mark='d'/> Only two of them give the right answer: the ones where one "
            "thread finishes before the other begins. <bookmark mark='e'/> The other eighteen lose an update. A test "
            "that runs the program a few times sees whichever schedules the hardware happens to pick."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(key), Create(edges, lag_ratio=0.02), FadeIn(dots), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(lf) for lf in leaves], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(f))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]), *[Indicate(lf, color=YES) for lf, s in zip(leaves, sch) if s["c"] == 2])
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def checker(self):
        head = label(r"A model checker: \ try every interleaving", font_size=34).to_edge(UP, buff=0.3)
        prog = VGroup(
            label(r"a program:", font_size=20, color=GREY_A),
            mono("A:  ld r, c;  addi r, r, 1;  st c, r", 19, T0C),
            mono("B:  ld r, c;  addi r, r, 1;  st c, r", 19, T1C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        state = VGroup(
            label(r"a \textbf{state}: \ each thread's next instruction and registers, \ and memory", font_size=20,
                  color=WHITE),
            label(r"a \textbf{step}: \ one thread executes one instruction", font_size=20, color=WHITE),
            label(r"breadth-first from the start: \ every reachable state, \ once", font_size=20, color=YES),
            label(r"check a property in each \ (``at most one thread in the critical section'')", font_size=20,
                  color=HEAD),
            label(r"a violation comes with the shortest schedule that reaches it", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(prog, state).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.5)
        note = label(r"\texttt{explainer/cs/conc/mc.py}: \ about 400 lines of Python", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Instead of hoping a test finds the bad schedule, we can try all of them. <bookmark mark='a'/> We wrote a "
            "small model checker. It takes a program written in a tiny assembly language, one list of instructions per "
            "thread. <bookmark mark='b'/> A state is where each thread is, what its registers hold, and what memory "
            "holds. A step lets one thread execute one instruction. <bookmark mark='c'/> Starting from the initial "
            "state, it explores every reachable state, breadth first, visiting each only once, so loops are fine. "
            "<bookmark mark='d'/> In each state it checks a property, such as: at most one thread is in its critical "
            "section. <bookmark mark='e'/> And because the search is breadth first, a violation comes with the "
            "shortest schedule that produces it. This is model checking, invented independently by Clarke and "
            "Emerson and by Queille and Sifakis around 1981, in its simplest form."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(prog))
            for mk, ln in zip("bcde", (VGroup(state[0], state[1]), state[2], state[3], state[4])):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def counts(self):
        d = load("race")
        head = label(r"What the checker finds", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for r in d["rows"]:
            rows.append([str(r["k"]), num(r["schedules"]), rf"$\binom{{{6 * r['k']}}}{{{3 * r['k']}}}$",
                         num(r["states"]), rf"{r['outcomes'][0]} to {r['outcomes'][-1]}"])
        tab = grid_table([r"increments each, \ $k$", r"schedules", r"formula", r"distinct states",
                          r"final count"], rows, widths=[2.6, 2.4, 1.8, 2.4, 2.4], row_h=0.55, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        fx = d["fixed"]
        lines = VGroup(
            label(r"schedules grow exponentially, \ but \textbf{states} only polynomially: \ many schedules meet in "
                  r"the same state", font_size=21, color=WHITE),
            label(r"the count can end as low as \textbf{2}, \ whatever $k$ is: \ one thread's first load can be "
                  r"overwritten at the very end", font_size=21, color=NO),
            label(rf"with an atomic fetch-and-add, \ or a lock around the three instructions: \ only "
                  rf"{fx['fai']['outcomes'][0]}, \ for $k = 3$", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Here is what the checker finds as each thread does more increments. <bookmark mark='a'/> The number of "
            "schedules is a binomial coefficient, and grows exponentially: two point seven million for four increments "
            "each. <bookmark mark='b'/> But the number of distinct states grows only polynomially, under two "
            "thousand, because many schedules arrive at the same state, and the checker visits each state once. That "
            "is what makes model checking feasible. <bookmark mark='c'/> And it finds a surprise. With k increments "
            "each, the final count can be as low as two, whatever k is. Thread A loads zero and stalls; B does all but "
            "its last increment; A stores one, so B's last load reads one; then A finishes; and finally B stores two. "
            "<bookmark mark='d'/> Make the increment atomic, with a fetch-and-add instruction or a lock around the "
            "three steps, and the checker proves that only the right answer remains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            for mk, ln in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
