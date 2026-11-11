from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (DATA, HEAD, NO, PART, YES, grid_table, load, mono, num)


class Deadlock(VoiceoverScene):
    def construct(self):
        self.card()
        self.philosophers()
        self.conditions()
        self.banker()

    def card(self):
        card = chapter_card(8, r"Deadlock", r"When does everyone wait forever?", lit=(1965, 1971),
                            extra=((1965, r"Dijkstra: \ philosophers, \ banker"), (1971, r"Coffman et al.")), part=PART)
        with self.voiceover("Chapter eight. Deadlock."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def table_ring(self, n=5, R=1.9, center=(-3.2, -0.2, 0)):
        cx, cy, _ = center
        phil, forks = VGroup(), VGroup()
        for i in range(n):
            a = math.pi / 2 - 2 * math.pi * i / n
            p = VGroup(Circle(radius=0.38, color=DATA, fill_color=DATA, fill_opacity=0.2),
                       label(rf"P{i}", font_size=18, color=WHITE)).move_to([cx + R * math.cos(a), cy + R * math.sin(a), 0])
            phil.add(p)
            b = a - math.pi / n
            f = Line([0, -0.3, 0], [0, 0.3, 0], color=GREY_B, stroke_width=5).rotate(b).move_to(
                [cx + 0.62 * R * math.cos(b), cy + 0.62 * R * math.sin(b), 0])
            forks.add(f)
        return phil, forks

    def philosophers(self):
        d = load("deadlock")
        head = label(r"The dining philosophers", font_size=36).to_edge(UP, buff=0.3)
        phil, forks = self.table_ring()
        holds = VGroup(*[Arrow(forks[i].get_center(), phil[i].get_center(), buff=0.38, color=NO, stroke_width=3,
                               max_tip_length_to_length_ratio=0.3) for i in range(5)])
        wants = VGroup(*[DashedLine(phil[i].get_center(), forks[(i + 1) % 5].get_center(), buff=0.38, color=HEAD)
                         for i in range(5)])
        tr = d["naive"]["trace"]
        steps = VGroup(*[mono(t, 18, NO) for t in tr]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        notes = VGroup(
            label(r"each: \ lock left fork, \ lock right fork, \ eat, \ put both down", font_size=20, color=WHITE),
            label(r"the checker's deadlock, \ 5 steps:", font_size=20, color=NO),
            steps,
            label(rf"every philosopher holds one fork \\ and waits for the next: \ a \textbf{{cycle}}", font_size=20,
                  color=NO),
            label(rf"one philosopher takes the right fork first: \\ no deadlock in {num(d['ordered']['states'])} "
                  rf"states", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.1)
        with self.voiceover(
            "Dijkstra's dining philosophers. <bookmark mark='a'/> Five philosophers sit at a round table with a fork "
            "between each pair. To eat, a philosopher picks up the fork on the left, then the one on the right, eats, "
            "and puts both down. <bookmark mark='b'/> The checker finds the problem in five steps: each philosopher "
            "picks up the left fork. <bookmark mark='c'/> Now each holds one fork and waits for the next, which its "
            "neighbour holds. The waits form a cycle, and nobody ever eats. <bookmark mark='d'/> The fix is to break "
            "the symmetry: let one philosopher pick up the right fork first. Then the forks are always taken in a "
            "fixed global order, a cycle is impossible, and the checker finds no deadlock in any of its three "
            "thousand states."
        ) as vo:
            self.play(FadeIn(head), FadeIn(phil), FadeIn(forks))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(h) for h in holds], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(wants), FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def conditions(self):
        head = label(r"Coffman's four conditions, \ 1971", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"condition", r"what it means", r"break it by"], [
            [r"mutual exclusion", r"a resource is held by one thread at a time", r"sharing it \ (read-only data)"],
            [r"hold and wait", r"threads hold some resources while asking for more", r"taking all at once"],
            [r"no preemption", r"nobody can take a resource away", r"\texttt{trylock}, \ back off, \ retry"],
            [r"circular wait", r"a cycle in the waits-for graph", r"a global \textbf{lock order}"],
        ], widths=[3.0, 5.6, 3.6], row_h=0.6, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"all four hold \ $\Rightarrow$ \ deadlock is possible; \ remove any one and it is not", font_size=21,
                  color=WHITE),
            label(r"in practice: \ a documented lock order \ (Linux's \texttt{lockdep} checks it at run time)",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Coffman and his colleagues named the four conditions for deadlock in 1971. <bookmark mark='a'/> Mutual "
            "exclusion: a resource is held by one thread at a time. <bookmark mark='b'/> Hold and wait: a thread holds "
            "some resources while asking for more. <bookmark mark='c'/> No preemption: nobody can take a resource "
            "away. <bookmark mark='d'/> And circular wait: a cycle in the graph of who waits for whom. <bookmark "
            "mark='e'/> Deadlock needs all four, so preventing it means breaking one. The usual choice is the last: "
            "give every lock a place in a global order and always take them in that order. Linux even checks its own "
            "lock order as it runs, with a tool called lockdep."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("e")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def banker(self):
        d = load("deadlock")["banker"]
        head = label(r"Avoiding it instead: \ the banker's algorithm", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for i, (m, a) in enumerate(zip(d["max"], d["alloc"])):
            need = [x - y for x, y in zip(m, a)]
            rows.append([rf"P{i}", " ".join(map(str, a)), " ".join(map(str, m)), " ".join(map(str, need))])
        tab = grid_table([r"process", r"holds", r"may ask for in all", r"still needs"], rows,
                         widths=[1.8, 2.0, 3.2, 2.4], row_h=0.46, font_size=20, mono_cols=(1, 2, 3))
        tab.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        req = d["requests"]
        safe = " $\\rightarrow$ ".join(f"P{i}" for i in d["safe"])
        notes = VGroup(
            label(rf"three resource types, \ {' '.join(map(str, d['total']))} in all; \\ free now: \ "
                  rf"{' '.join(map(str, d['avail']))}", font_size=20, color=WHITE),
            label(rf"\textbf{{safe}}: \ some order lets everyone finish: \\ {safe}", font_size=20, color=YES),
            label(rf"P{req[0]['p']} asks for {' '.join(map(str, req[0]['req']))}: \ still safe, \ granted",
                  font_size=20, color=YES),
            label(rf"P{req[2]['p']} asks for {' '.join(map(str, req[2]['req']))}: \ available, \\ but no safe order "
                  rf"would remain: \ \textbf{{refused}}", font_size=20, color=NO),
            label(r"needs each thread's maximum in advance: \\ rare outside batch systems", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        if notes.get_right()[0] > 6.9:
            left = notes.get_left()[0]
            notes.scale((6.9 - left) / notes.width).align_to(tab, UP)
            notes.shift(RIGHT * (left - notes.get_left()[0]))
        with self.voiceover(
            "Dijkstra also showed how to avoid deadlock without forbidding any pattern, by refusing dangerous "
            "requests. <bookmark mark='a'/> Each process declares in advance the most it may ask for. The system knows "
            "what each holds and what is free. <bookmark mark='b'/> A state is safe if there is some order in which "
            "every process can get what it still needs, finish, and return its resources. Here one exists. <bookmark "
            "mark='c'/> When P1 asks for one, zero and two, the system pretends to grant it and checks that a safe "
            "order remains. It does, so the request is granted. <bookmark mark='d'/> Later P0 asks for zero, two, "
            "zero. The resources are free, but granting them would leave no safe order, so P0 must wait. <bookmark "
            "mark='e'/> The banker's algorithm needs every maximum declared in advance, which real programs rarely "
            "know, so it lives mostly in textbooks and batch systems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.15))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
