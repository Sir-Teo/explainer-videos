from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403

CELL = 0.52
GOAL_COLORS = (PERSON, GOOD, CROWD)
GOAL_NAMES = ("A", "B", "C")


def grid(shape, walls, goals, origin=(-6.2, 2.0)) -> tuple[VGroup, callable]:
    """The gridworld: cells, walls and lettered goals; returns (group, a function from (row, col) to a point)."""
    H, W = shape
    ox, oy = origin

    def at(rc):
        return np.array([ox + rc[1] * CELL, oy - rc[0] * CELL, 0])

    cells = VGroup(*[Square(side_length=CELL, stroke_color=GREY_D, stroke_width=1, fill_color="#14181F",
                            fill_opacity=1).move_to(at((r, c))) for r in range(H) for c in range(W)])
    wall = VGroup(*[Square(side_length=CELL, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9).move_to(at(tuple(w)))
                    for w in walls])
    gs = VGroup(*[VGroup(Square(side_length=CELL * 0.86, stroke_width=0, fill_color=c, fill_opacity=0.35)
                         .move_to(at(tuple(g))), label(n, font_size=20, color=c).move_to(at(tuple(g))))
                  for g, c, n in zip(goals, GOAL_COLORS, GOAL_NAMES)])
    return VGroup(cells, wall, gs), at


def post_bars(ax, p) -> VGroup:
    return bars(ax, [0, 1, 2], [float(v) for v in p], list(GOAL_COLORS), width=0.6)


class Inverse(VoiceoverScene):
    def construct(self):
        self.card()
        self.planner()
        self.walk("up")
        self.walk("turn")
        self.people()

    def card(self):
        card = chapter_card(10, r"Mind reading as inverse planning", r"How do you know where someone is going?",
                            lit={2009: r"Baker, \ Saxe \& Tenenbaum", 2017: r"Baker et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter ten. Mind reading as inverse planning."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def planner(self):
        d = load("goals")
        head = heading(r"Run the planner backwards")
        g, at = grid((7, 9), d["walls"], d["goals"])
        rows = rows_of([
            (r"forward: \ Part 17's planner picks moves that bring an agent closer to its goal, \ mostly; \ a "
             r"softmax over the moves' values", WHITE),
            (r"backward: \ watch the moves and ask which goal makes them likely", MODEL),
            (r"$P(\text{goal} \mid \text{path}) \propto P(\text{path} \mid \text{goal})\, P(\text{goal})$", MODEL),
            (r"Baker, \ Saxe and Tenenbaum, \ 2009: \ this is how people read goals from movement", YOU),
        ], 6.0, 21, 0.4).move_to([3.3, -0.2, 0])
        tag = psyche_tag(r"computed: \ Psyche's inverse planner")
        with self.voiceover(
            "Now the computational idea. How do you know where someone is going, before they get there? "
            "<bookmark mark='a'/> Part 17 built a planner: an agent that picks moves bringing it closer to its "
            "goal, mostly, with a little noise, a softmax over the values of its moves. <bookmark mark='b'/> Run "
            "it backwards. Watch the moves, and ask which goal would make them likely. <bookmark mark='c'/> That's "
            "Bayes' rule, with the planner as the likelihood. <bookmark mark='d'/> In 2009 Baker, Rebecca "
            "Saxe and Joshua Tenenbaum proposed that this is how people read goals from movement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def walk(self, which):
        d = load("goals")
        path = [tuple(int(v) for v in c) for c in d[f"path_{which}"]]
        post = np.asarray(d[f"post_{which}"], float)
        head = heading(r"Which goal?" if which == "up" else r"A change of mind, \ or a long way round?")
        g, at = grid((7, 9), d["walls"], d["goals"])
        A = axes([-0.6, 2.6], [0, 1.0], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"posterior", center=[3.6, 0.4, 0], font_size=15)
        names = VGroup(*[label(n, font_size=20, color=c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15)
                         for k, (n, c) in enumerate(zip(GOAL_NAMES, GOAL_COLORS))])
        b = post_bars(A.ax, post[0])
        agent = Dot(at(path[0]), radius=0.15, color=WHITE)
        trail = VGroup()
        if which == "up":
            text = (r"starting left of the wall, \ the agent steps up: \ that is the way to A, \ and away from B and C; "
                    r"\ three steps and the model is nearly sure")
            vo_text = (
                "Here's Psyche's version, with three goals, A, B and C, and a wall. <bookmark mark='a'/> The agent "
                "starts left of the wall and steps up. That's the way to A, and away from B and C. "
                f"<bookmark mark='b'/> After one step the model gives A {spct(post[1, 0])}. After three, it's "
                "nearly sure. <bookmark mark='c'/> Nothing here knows about minds. It only knows that agents "
                "mostly take efficient paths to what they want.")
        else:
            text = (r"starting right of the wall, \ going up suits A, \ and suits C too, \ by the long way round "
                    r"the wall; \ the turn at the top settles it")
            vo_text = (
                "Now a harder walk. <bookmark mark='a'/> The agent starts right of the wall and goes up. That "
                "suits A, but it also suits C, by the long way round the top of the wall. "
                f"<bookmark mark='b'/> For three steps the model holds both, A at {spct(post[3, 0])} and C at "
                f"{spct(post[3, 2])}. <bookmark mark='c'/> Then the agent turns left along the top, and C takes "
                "over. The model changes its mind because the evidence did.")
        row = wrapped_label(text, 5.6, 20, WHITE).move_to([3.4, -2.4, 0])
        tag = psyche_tag(r"computed: \ Psyche's inverse planner, \ $\beta = 0.7$")
        with self.voiceover(vo_text) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g), FadeIn(A), FadeIn(names), FadeIn(b), FadeIn(agent))
            vo.wait_until("a")
            self.play(FadeIn(row))
            stop = 1 if which == "up" else 3
            for k in range(1, len(path)):
                seg = Line(at(path[k - 1]), at(path[k]), color=WHITE, stroke_width=3)
                trail.add(seg)
                nb = post_bars(A.ax, post[k])
                self.play(agent.animate.move_to(at(path[k])), Create(seg), Transform(b, nb), run_time=0.5)
                if k == stop:
                    vo.wait_until("b")
            vo.wait_until("c")
        self.clear_scene()

    def people(self):
        head = heading(r"The model against people")
        rows = rows_of([
            (r"Baker, \ Saxe and Tenenbaum: \ people watched agents move through mazes and rated, \ step by step, "
             r"\ which goal each was heading for", WHITE),
            (r"the inverse-planning model's goal inferences tracked people's closely: \ in the 2007 conference "
             r"version, \ a correlation of .96 across 100 stimuli", MODEL),
            (r"the fit held across three experiments", CROWD),
            (r"Baker, \ Jara-Ettinger, \ Saxe and Tenenbaum, \ 2017: \ an agent looking for its favourite food "
             r"truck: \ people infer what it wants, \ what it believes and what it can see, \ all at once, \ from "
             r"its movement", PERSON),
            (r"a computational account of mind reading: \ assume others are roughly rational, \ and invert", YOU),
        ], 12.4, 21, 0.34).move_to([0, -0.3, 0])
        tag = published_tag(r"Baker, \ Saxe \& Tenenbaum (2009); \ Baker et al.\ (2017)")
        with self.voiceover(
            "Is it how people do it? <bookmark mark='a'/> Baker and colleagues had people watch agents move "
            "through mazes and rate, step by step, which goal each was heading for. <bookmark mark='b'/> The "
            "inverse-planning model's inferences tracked people's closely. In the 2007 conference version, the "
            "correlation was point nine six, across a hundred stimuli. <bookmark mark='c'/> The fit held across three "
            "experiments. <bookmark mark='d'/> In 2017 the same group, with "
            "Jara-Ettinger, had an agent looking for its favourite food truck. People inferred what it wanted, "
            "what it believed and what it could see, all at once, from its movement. <bookmark mark='e'/> It's a "
            "computational account of mind reading: assume others are roughly rational, and invert."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
