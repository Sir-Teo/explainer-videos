from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403

CODE = [r"\textbf{process } i \textbf{ (the other is } j\textbf{)}:",
        r"\quad 0\ \ \textit{idle}",
        r"\quad 1\ \ \mathit{flag}[i] := \mathrm{true}",
        r"\quad 2\ \ \mathit{turn} := j",
        r"\quad 3\ \ \textbf{wait until } \lnot \mathit{flag}[j] \lor \mathit{turn} = i",
        r"\quad 4\ \ \textit{critical section}",
        r"\quad\ \ \ \ \mathit{flag}[i] := \mathrm{false}; \ \textbf{go to } 0"]


def state_graph(d, center=(0, 0, 0), w=11.0, h=5.2, radius=0.07):
    """The reachable states laid out by breadth-first level; critical states coloured."""
    c = np.asarray(center, float)
    pos = {k: c + np.array([(v[0] - 0.5) * w, (v[1] - 0.5) * h, 0]) for k, v in d["nodes"].items()}
    edges = VGroup(*[Line(pos[a], pos[b], color=GREY_D, stroke_width=1.2) for a, b in d["edges_list"]])
    dots = VGroup()
    dmap = {}
    for k, v in d["nodes"].items():
        col = BAD if (v[2] and v[3]) else (GOAL if (v[2] or v[3]) else WORLD)
        dt = Dot(pos[k], radius=radius, color=col)
        dots.add(dt)
        dmap[k] = dt
    g = VGroup(edges, dots)
    g.dmap, g.pos = dmap, pos
    return g


class Peterson(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Checking a mutual-exclusion protocol", r"Can two processes share a resource "
                            r"safely?", lit=(1981,), part=PART)
        with self.voiceover("Chapter thirteen. Checking a mutual-exclusion protocol."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.algorithm()
        self.graph_()
        self.broken()
        self.fairness()

    def algorithm(self):
        hc = history_card(1981, r"Gary Peterson", r"two processes, one critical section, three shared variables",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        code = VGroup(*[MathTex(l, font_size=30) for l in CODE]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        box = SurroundingRectangle(code, color=GREY_C, buff=0.25, corner_radius=0.1)
        cg = VGroup(box, code).move_to([0, -0.6, 0])
        note_ = label(r"the flag says `I want in'; \ the turn says `after you'", font_size=24, color=GOAL).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Here is a classic problem. Two processes share a resource, say a printer, and must never use it at "
            "the same time. Each has a critical section where it uses the resource. <bookmark mark='a'/>In 1981 Gary "
            "Peterson published a famous short solution using three shared variables. <bookmark mark='b'/>To enter, "
            "process i raises its flag, then gives the turn to the other process, then waits until either the other "
            "process's flag is down, or the turn has come back to i. <bookmark mark='c'/>On leaving, it lowers its "
            "flag. The flag says 'I want in'; the turn says 'after you'. Is it correct? With two processes "
            "interleaving their steps, intuition is unreliable. So check every possible interleaving."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cg))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def graph_(self):
        d = load("peterson")["peterson"]
        g = state_graph(d, center=(0, -0.2, 0))
        head = label(rf"every interleaving: \ {d['states']} reachable states, \ {d['edges']} transitions",
                     font_size=28, color=CONN).to_edge(UP, buff=0.4)
        key = VGroup(VGroup(Dot(color=WORLD), label(r"neither critical", font_size=20)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(color=GOAL), label(r"one critical", font_size=20)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(color=BAD), label(r"both critical", font_size=20)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.6).next_to(head, DOWN, buff=0.2)
        res = VGroup(MathTex(r"\mathsf{AG}\,\lnot(\mathit{crit}_0 \land \mathit{crit}_1)", font_size=34, color=OK),
                     label(r"no red state is reachable: \ mutual exclusion holds \ $\checkmark$", font_size=24,
                           color=OK)).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.35)
        assert d["mutex"]
        with self.voiceover(
            "The Reasoner's model checker starts from the state where both processes are idle and explores every "
            "possible next step of either process, breadth first. <bookmark mark='a'/>It finds "
            f"{d['states']} reachable states, joined by {d['edges']} transitions. <bookmark mark='b'/>Colour each "
            "state by how many processes are in their critical sections. <bookmark mark='c'/>A violation of mutual "
            "exclusion would be a red state, with both inside. There is none. Necessarily, on every path, always, "
            "at most one process is critical. Peterson's algorithm is safe, and this is not a test of a few runs: it "
            "is every run."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(g[0]), run_time=2)
            self.play(LaggedStart(*[FadeIn(x, scale=2) for x in g[1]], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.clear_scene()

    def broken(self):
        d = load("peterson")["broken"]
        g = state_graph(d, center=(0, 0.1, 0), h=4.2)
        tr = d["trace"]
        keys = ["".join(str(x) for x in s) for s in tr]
        head = label(r"a broken variant: \ give the turn \textit{before} raising the flag", font_size=28,
                     color=CONN).to_edge(UP, buff=0.4)
        path_ = VGroup(*[Line(g.pos[a], g.pos[b], color=BAD, stroke_width=5) for a, b in zip(keys, keys[1:])])
        steps = []
        for a, b in zip(tr, tr[1:]):
            who = 0 if a[0] != b[0] else 1
            act = {0: r"\text{start}", 1: rf"\mathit{{turn}} := {1 - who}", 2: rf"\mathit{{flag}}_{who} := 1",
                   3: r"\text{enter}", 4: r"\text{leave}"}[a[who]]
            steps.append(rf"P_{who}\!:\ {act}")
        tl = MathTex(r",\ ".join(steps), font_size=24, color=BAD).to_edge(DOWN, buff=0.4)
        if tl.width > 13.4:
            tl.width = 13.4
        cap = label(rf"{d['states']} states; \ the checker returns the shortest path to a red state: \ "
                    rf"{len(tr) - 1} steps", font_size=24, color=BAD).next_to(tl, UP, buff=0.25)
        assert not d["mutex"] and tr[-1][0] == 4 and tr[-1][1] == 4
        with self.voiceover(
            "Now change one detail: give the turn away before raising the flag, the two middle lines swapped. "
            "<bookmark mark='a'/>The state graph grows to fifty states, and this time some are red. "
            "<bookmark mark='b'/>Because the checker explores breadth first, it hands back the shortest path to a "
            f"violation: {len(tr) - 1} steps. <bookmark mark='c'/>Process zero gives the turn away. Process one gives "
            "it back, raises its flag, and, since process zero's flag is still down, enters. Then process zero raises "
            "its flag, finds that the turn is its own, and enters too. Both are inside. A bug that a test might never hit, found and "
            "explained by exhaustive search."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p) for p in path_], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(cap), FadeIn(tl))
        self.clear_scene()

    def fairness(self):
        d = load("peterson")["peterson"]
        head = label(r"Liveness: \ can process 0 wait forever?", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"with any scheduler", font_size=28, color=BAD),
                   MathTex(r"\mathsf{EG}\,(\mathit{try}_0 \land \lnot \mathit{crit}_0)", font_size=32),
                   label(rf"holds in {d['starve_unfair']} states: \ the scheduler can simply never run process 0",
                         font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(label(r"with a strongly fair scheduler", font_size=28, color=OK),
                   label(r"a process that is enabled infinitely often runs infinitely often", font_size=24,
                         color=GREY_A),
                   label(rf"fair paths of endless waiting: \ {d['starve_fair']} \ $\checkmark$", font_size=26,
                         color=OK)).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        how = label(r"computed by strongly connected components (Emerson and Lei 1986): \ every fair cycle must let both "
                    r"processes move", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        assert d["starve_fair"] == 0 and d["starve_unfair"] > 0
        with self.voiceover(
            "Safety is half the story. Can a process that wants to enter wait forever? <bookmark mark='a'/>With an "
            "arbitrary scheduler, yes: the Reasoner finds paths on which process zero waits forever, because the "
            "scheduler simply never lets it move. That is not the algorithm's fault. <bookmark mark='b'/>So add an "
            "assumption about the scheduler, strong fairness: a process that is able to move infinitely often does "
            "move infinitely often. <bookmark mark='c'/>Under fairness, the checker finds no path of endless waiting. "
            "Peterson's algorithm is starvation-free. <bookmark mark='d'/>The computation looks for cycles in the "
            "state graph on which waiting could last forever, and discards those that are unfair to either process."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1][2]))
            vo.wait_until("d")
            self.play(FadeIn(how))
        self.clear_scene()
