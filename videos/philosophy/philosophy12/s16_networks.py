from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


def net_drawing(kind: str, center, r=1.05, n=10):
    g = Ep.network(kind, n)
    c = np.asarray(center, float)
    if kind == "wheel":
        pos = {i: c + r * np.array([np.cos(PI / 2 - TAU * i / (n - 1)), np.sin(PI / 2 - TAU * i / (n - 1)), 0])
               for i in range(n - 1)}
        pos[n - 1] = c
    else:
        pos = {i: c + r * np.array([np.cos(PI / 2 - TAU * i / n), np.sin(PI / 2 - TAU * i / n), 0]) for i in range(n)}
    edges = VGroup(*[Line(pos[i], pos[j], color=GREY_C, stroke_width=1.5) for i in g for j in g[i] if i < j])
    dots = VGroup(*[Dot(pos[i], radius=0.09, color=AG["A"]) for i in range(n)])
    return VGroup(edges, dots)


class Networks(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Networks of inquiry", r"Can scientists talk too much?", lit=(2007,), part=PART)
        with self.voiceover("Chapter fifteen. Networks of inquiry."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.model()
        self.rivers()
        self.results()
        self.bubbles()

    def model(self):
        hc = history_card(2007, r"Kevin Zollman", r"`The Communication Structure of Epistemic Communities'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"ten scientists; \ an old method that works half the time, \ known", font_size=22),
            label(r"a new method that works 51\% of the time, \ unknown to them", font_size=22, color=OK),
            label(r"each holds a Beta belief about the new method, \ from a random prior", font_size=22,
                  color=GREY_A),
            label(r"each round, \ whoever expects the new method to be better \ tries it 100 times", font_size=22,
                  color=GREY_A),
            label(r"everyone updates on her own results, \ and her neighbours'", font_size=22, color=GOAL),
            label(r"the run ends when nobody tries it, \ or everyone is 99\% sure it is better", font_size=22,
                  color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.0, -0.6, 0])
        nets = VGroup(net_drawing("cycle", [-5.0, 0.9, 0], r=0.85), net_drawing("complete", [-5.0, -1.8, 0], r=0.85))
        nl = VGroup(label(r"a cycle", font_size=20, color=GREY_A).next_to(nets[0], RIGHT, buff=0.2),
                    label(r"complete", font_size=20, color=GREY_A).next_to(nets[1], RIGHT, buff=0.2))
        with self.voiceover(
            "Last, communities of scientists. Kevin Zollman, in 2007, asked whether scientists can share too much "
            "information. <bookmark mark='a'/>Ten scientists choose between an old method, which works half the time, "
            "as everyone knows, <bookmark mark='b'/>and a new one, which in fact works fifty-one percent of the time, "
            "though nobody knows it. <bookmark mark='c'/>Each scientist has a belief about the new method's rate, "
            "starting from a random prior. <bookmark mark='d'/>Each round, every scientist who expects the new method "
            "to be better tries it a hundred times. <bookmark mark='e'/>Everyone updates on her own results and on "
            "those of the colleagues she is connected to: in a cycle, two neighbours; in a complete network, "
            "everyone. <bookmark mark='f'/>The run ends when nobody tries the new method any more, or when everyone "
            "is ninety-nine percent sure that it is better."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), FadeIn(nets), FadeIn(nl))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def rivers(self):
        d = load("rivers")
        head = label(r"One run, \ two networks, \ the same priors", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def plot(traj, center, title, col):
            ax = Axes(x_range=[0, 100, 25], y_range=[0.3, 0.7, 0.1], x_length=5.6, y_length=3.4, tips=False,
                      axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to(center)
            thr = DashedLine(ax.c2p(0, 0.5), ax.c2p(100, 0.5), color=GREY_B)
            lines = VGroup()
            n = len(traj[0])
            for i in range(n):
                ys = [min(max(r[i], 0.3), 0.7) for r in traj]
                lines.add(ax.plot_line_graph(list(range(len(ys))), ys, line_color=col, add_vertex_dots=False,
                                             stroke_width=2))
            t = label(title, font_size=22, color=col).next_to(ax, UP, buff=0.15)
            return VGroup(ax, thr, lines, t), lines
        A, la = plot(d["complete"], [-3.4, -0.2, 0], r"complete network", BAD)
        B, lb = plot(d["cycle"], [3.4, -0.2, 0], r"cycle", OK)
        yl = label(r"each scientist's expected success rate of the new method \ (dashed: the old method's 0.5)",
                   font_size=19, color=GREY_B).next_to(VGroup(A, B), DOWN, buff=0.25)
        foot = label(r"complete: \ one unlucky early batch, \ shared by all, \ and the new method is abandoned",
                     font_size=22, color=BAD).to_edge(DOWN, buff=0.25)
        foot2 = label(r"cycle: \ the same bad news spreads slowly, \ and some keep testing until the truth "
                      r"returns", font_size=22, color=OK).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "To see why, the Reasoner records one run on each network, starting from the very same priors. "
            "<bookmark mark='a'/>Each line is one scientist's expectation for the new method, round by round; below "
            "the dashed line, she stops testing it. <bookmark mark='b'/>In the complete network, an unlucky early "
            "batch of results is shared by everyone at once. Every expectation falls below the line together, nobody "
            "tests the new method again, and the community is stuck with the worse one for good. "
            "<bookmark mark='c'/>In the cycle, the same bad news spreads slowly. Some scientists keep testing, their "
            "good results spread back, and the whole community climbs above the line."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(A[0]), FadeIn(A[1]), FadeIn(A[3]), FadeIn(B[0]), FadeIn(B[1]), FadeIn(B[3]),
                      FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(la), run_time=3)
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeOut(foot), Create(lb), run_time=3)
            self.play(FadeIn(foot2))
        self.clear_scene()

    def results(self):
        d = load("zollman")
        head = label(r"500 runs on each network", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        kinds = [("cycle", r"cycle"), ("wheel", r"wheel"), ("complete", r"complete")]
        nets = VGroup(*[net_drawing(k, [-4.6 + 4.6 * i, 1.3, 0], r=0.8) for i, (k, _) in enumerate(kinds)])
        names = VGroup(*[label(t, font_size=22, color=GREY_A).next_to(nets[i], DOWN, buff=0.15)
                         for i, (_, t) in enumerate(kinds)])
        acc = bar_row([100 * d[k]["right"] for k, _ in kinds], [t for _, t in kinds], [OK, OK, OK], width=5.0,
                      height=0.34, font_size=21, vmax=100, fmt=lambda v: f"{v:.0f}" + r"\%")
        spd = bar_row([d[k]["mean_rounds"] for k, _ in kinds], [t for _, t in kinds], [GOAL, GOAL, GOAL],
                      width=5.0, height=0.34, font_size=21, vmax=140, fmt=lambda v: f"{v:.0f}" + r"\ \text{rounds}")
        al = label(r"reach the truth", font_size=22, color=OK)
        sl = label(r"time to get there", font_size=22, color=GOAL)
        A = VGroup(al, acc).arrange(DOWN, buff=0.2).move_to([-3.4, -1.7, 0])
        B = VGroup(sl, spd).arrange(DOWN, buff=0.2).move_to([3.4, -1.7, 0])
        foot = label(r"less connection: \ more often right, \ but slower \ (the Zollman effect)", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The Reasoner runs the model five hundred times on each of three networks: a cycle, a wheel with a "
            "central hub, and the complete network where everyone hears everything. <bookmark mark='a'/>On the "
            "cycle, the community settles on the better method in nearly nine runs out of ten. On the complete "
            "network, only about half the time. <bookmark mark='b'/>But the complete network decides ten times "
            "faster. <bookmark mark='c'/>Why? When everyone hears everything, a short run of bad luck with the new "
            "method convinces the whole community at once, and since nobody tries it again, the error is never "
            "corrected. In a sparse network, some scientists keep experimenting long enough for the truth to come "
            "back. Less communication buys more truth, at the cost of time: the Zollman effect. Later work has "
            "shown that it depends on the parameters, but it is real in a wide range of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nets), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(A))
            vo.wait_until("b")
            self.play(FadeIn(B))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bubbles(self):
        head = label(r"Bubbles and echo chambers", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        a = VGroup(label(r"an epistemic bubble", font_size=26, color=AG["A"]),
                   label(r"other voices are simply missing", font_size=22),
                   label(r"cure: \ exposure", font_size=22, color=OK)).arrange(DOWN, buff=0.15)
        b = VGroup(label(r"an echo chamber", font_size=26, color=BAD),
                   label(r"other voices are present, \ but discredited in advance", font_size=22),
                   label(r"cure: \ rebuilding trust, \ not more information", font_size=22, color=GOAL)).arrange(
            DOWN, buff=0.15)
        cols = VGroup(a, b).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.6, 0])
        foot = VGroup(label(r"C. Thi Nguyen, \ `Echo Chambers and Epistemic Bubbles' \ (2020)", font_size=21,
                            color=GREY_B),
                      label(r"the structure of who trusts whom \ is part of what a community can know", font_size=25,
                            color=GOAL)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Communication structure matters outside science too. C. Thi Nguyen distinguishes two failures. "
            "<bookmark mark='a'/>In an epistemic bubble, other voices are simply missing; the cure is exposure. "
            "<bookmark mark='b'/>In an echo chamber, other voices are heard, but have been discredited in advance, "
            "so that every contrary report confirms the members' view of outsiders. More information does not help; "
            "what is needed is the slow rebuilding of trust. <bookmark mark='c'/>The lesson of this whole part: what "
            "a community can know depends not only on what each member knows, but on the structure of who hears, "
            "and who trusts, whom."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
