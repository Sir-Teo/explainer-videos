from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403

DISC_COLORS = [CONTENT, INSIGHT, SEARCH, LOGIC]


def tower(state, center=(0, 0, 0), peg_gap: float = 1.25, scale: float = 1.0) -> VGroup:
    """Three pegs with discs: ``state`` gives each disc's peg, smallest first."""
    c = np.array(center, float)
    n = len(state)
    g = VGroup(Line(c + np.array([-1.7, -0.6, 0]) * scale, c + np.array([1.7, -0.6, 0]) * scale, color=GREY_B))
    for p in range(3):
        x = (p - 1) * peg_gap * scale
        g.add(Line(c + np.array([x, -0.6, 0]) * 1 + np.array([0, 0, 0]),
                   c + np.array([x, -0.6 + 1.25 * scale, 0]), color=GREY_B, stroke_width=3))
    for p in range(3):
        on = [d for d in range(n) if state[d] == p][::-1]  # largest at the bottom
        for h, d in enumerate(on):
            w = (0.35 + 0.22 * d) * scale
            r = RoundedRectangle(corner_radius=0.05, width=w * 2, height=0.2 * scale, stroke_width=0,
                                 fill_color=DISC_COLORS[d % 4], fill_opacity=0.95)
            r.move_to(c + np.array([(p - 1) * peg_gap * scale, -0.6 * 1 + (0.11 + 0.21 * h) * scale, 0]))
            g.add(r)
    return g


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.space()
        self.graph()

    def card(self):
        card = chapter_card(4, r"Problem solving as search", r"What is a problem, \ to a machine or a mind?",
                            lit={1957: r"Newell, \ Shaw \& Simon", 1972: r"Newell \& Simon"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter four. Problem solving as search."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def space(self):
        head = heading(r"States, \ operators, \ a goal")
        start = tower((0, 0, 0), center=(-3.6, 1.0, 0))
        goal = tower((2, 2, 2), center=(3.6, 1.0, 0))
        ls = label(r"start", font_size=26, color=GREY_A).next_to(start, UP, buff=0.2)
        lg = label(r"goal", font_size=26, color=MODEL).next_to(goal, UP, buff=0.2)
        arr = Arrow([-1.4, 1.0, 0], [1.4, 1.0, 0], color=GREY_B, buff=0.1)
        rows = rows_of([
            (r"Newell, \ Shaw \& Simon, \ 1957 to 1972: \ a problem is a space of \emph{states}, \ "
             r"\emph{operators} that move between them, \ and a \emph{goal}", WHITE),
            (r"move one disc at a time, \ never a larger disc on a smaller one", SEARCH),
            (r"solving is searching the space; \ the General Problem Solver searched by \emph{means-ends analysis}: "
             r"\ find the biggest difference from the goal, \ and set up a subgoal to remove it", MODEL),
            (r"their evidence: \ people thinking aloud while they solved, \ compared with the program's steps", GREY_A),
        ], 12.6, 25, 0.34).move_to([0, -1.8, 0])
        tag = historical_tag(r"Newell, \ Shaw \& Simon (1958); \ Newell \& Simon (1972)")
        with self.voiceover(
            "Reasoning starts from what you know. Problem solving starts from where you are. "
            "<bookmark mark='a'/> In the late 1950s Allen Newell, Cliff Shaw and Herbert Simon described any problem "
            "the same way: a set of states, operators that move between them, and a goal. <bookmark mark='b'/> Here "
            "is the Tower of Hanoi: move the stack to the right-hand peg, one disc at a time, never putting a larger "
            "disc on a smaller one. <bookmark mark='c'/> Solving is searching through the states. Their General "
            "Problem Solver used means-ends analysis: find the biggest difference between where you are and the goal, "
            "and set up a subgoal to remove it. <bookmark mark='d'/> And their evidence came from people thinking "
            "aloud while they solved, compared step by step with what the program did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(start), FadeIn(ls))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(goal), FadeIn(lg), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def graph(self):
        d = load("hanoi")
        head = heading(r"The whole space, \ drawn")
        xy = d["xy"] * 1.85 + np.array([2.7, -0.25])
        pts = [np.array([x, y, 0]) for x, y in xy]
        edges = VGroup(*[Line(pts[a], pts[b], color=GREY_D, stroke_width=2) for a, b in d["edges"]])
        nodes = VGroup(*[Dot(p, radius=0.07, color=GREY_B) for p in pts])
        S = [tuple(s) for s in d["states"]]
        si, gi = S.index((0, 0, 0)), S.index((2, 2, 2))
        st = label(r"start", font_size=20, color=GREY_A).next_to(pts[si], UP, buff=0.12)
        gl = label(r"goal", font_size=20, color=MODEL).next_to(pts[gi], RIGHT, buff=0.12)
        opt = VMobject(color=MODEL, stroke_width=6).set_points_as_corners([pts[k] for k in d["opt"]])
        hill = VMobject(color=LOST, stroke_width=3.5).set_points_as_corners([pts[k] for k in d["hill"]])
        hill.shift(RIGHT * 0.04 + DOWN * 0.04)
        rows = rows_of([
            (rf"three discs: \ ${d['n_states']} = 3^3$ states, \ each a dot; \ each line a legal move", WHITE),
            (r"the shortest path: \ 7 moves, \ straight down one side", MODEL),
            (rf"a hill-climber that always moves more discs toward the goal: \ the median of 101 runs takes "
             rf"{d['hill_median']} moves; \ {pct(d['hill_optimal_share'])} find the shortest", LOST),
            (rf"with four discs, \ 81 states: \ the hill-climber's median is {d['hill4_median']:.0f} moves, \ "
             r"against 15", LOST),
            (r"the right move sometimes leads away from the goal: \ that is why people pause there", SEARCH),
        ], 5.6, 23, 0.34).move_to([-3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{reason.hanoi\_graph}, \ \texttt{hill\_climb}")
        hm = int(d["hill_median"])
        with self.voiceover(
            "Psyche can draw the whole space. <bookmark mark='a'/> With three discs there are twenty-seven states, "
            "each a dot, and every line is a legal move. The space is a triangle of triangles. "
            "<bookmark mark='b'/> The shortest solution is seven moves, straight along one side. "
            f"<bookmark mark='c'/> A hill-climber, which always prefers moves that put more of the stack on the goal "
            f"peg, wanders. The median of a hundred and one runs takes {hm} moves, and only "
            f"{spct(d['hill_optimal_share'])} find the shortest path. <bookmark mark='d'/> With four discs and "
            f"eighty-one states, its median is {d['hill4_median']:.0f} moves, against fifteen. "
            "<bookmark mark='e'/> The trouble is that the right move sometimes takes you away from the goal: to get "
            "the big disc across, the small ones must first go the wrong way. That is where people tend to slow down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(nodes), FadeIn(st), FadeIn(gl), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(opt), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(hill), FadeIn(rows[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
