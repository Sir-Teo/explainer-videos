from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403

SPRINK = {"C": [-4.6, 0.4, 0], "S": [-6.0, -0.9, 0], "R": [-3.2, -0.9, 0], "W": [-4.6, -2.2, 0],
          "L": [-2.6, -2.2, 0]}


class Graphs(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Structural models and graphs", r"How do causes pass information?",
                            lit=(1921, 2000), part=PART)
        with self.voiceover("Chapter six. Structural models and graphs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.scm()
        self.three()
        self.berkson()
        self.dsep()

    def scm(self):
        hc = history_card(2000, r"Judea Pearl", r"\textit{Causality}; \ after Sewall Wright's path analysis "
                          r"\ (1921)", width=7.0, color=HIST).to_corner(UL, buff=0.3)
        eqs = VGroup(*[MathTex(t, font_size=28, color=c) for t, c in (
            (r"C := U_C", WHITE), (r"S := f_S(C, U_S)", CAUSE), (r"R := f_R(C, U_R)", CAUSE),
            (r"W := f_W(S, R, U_W)", EFFECT), (r"L := f_L(W, U_L)", EFFECT))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.22)
        eqs.move_to([3.2, -0.6, 0])
        names = {"C": "cloudy", "S": "sprinkler", "R": "rain", "W": "wet", "L": "slippery"}
        el = label(r"$:=$ \ is assignment, \ not equality: \ it says which variable listens to which", font_size=20,
                   color=GREY_A).next_to(eqs, DOWN, buff=0.3)
        g = CausalGraph(SPRINK, [("C", "S"), ("C", "R"), ("S", "W"), ("R", "W"), ("W", "L")],
                        colors={"S": CAUSE, "R": CAUSE, "W": EFFECT, "L": EFFECT}, radius=0.36, font_size=20)
        tags = VGroup(*[label(names[n], font_size=15, color=GREY_B).next_to(g.node[n], LEFT if n in "SW" else RIGHT,
                                                                           buff=0.08) for n in SPRINK])
        with self.voiceover(
            "Judea Pearl, building on Sewall Wright's path analysis of 1921, gave causation a mathematical form: the "
            "structural causal model. <bookmark mark='a'/>Each variable is assigned a value by a function of its "
            "direct causes and an unobserved noise term. Cloudiness; the sprinkler, which depends on cloudiness; "
            "rain, which does too; wet grass, which depends on sprinkler and rain; and a slippery path, which "
            "depends on wet grass. <bookmark mark='b'/>The colon-equals is assignment, not equality: it says which "
            "variable listens to which. <bookmark mark='c'/>Draw an arrow from each variable to those that listen "
            "to it, and you have the model's causal graph."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(el))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*g.node.values())), FadeIn(tags))
            self.play(LaggedStart(*[GrowArrow(a) for a in g.edge.values()], lag_ratio=0.2))
        self.clear_scene()

    def three(self):
        head = label(r"Three junctions", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        specs = [(r"chain", {"A": [-5.6, 0.6, 0], "B": [-4.4, 0.6, 0], "C": [-3.2, 0.6, 0]}, [("A", "B"), ("B", "C")],
                  r"conditioning on $B$ \textit{blocks}", OK),
                 (r"fork", {"A": [-1.2, 0.0, 0], "B": [0.0, 1.2, 0], "C": [1.2, 0.0, 0]}, [("B", "A"), ("B", "C")],
                  r"conditioning on $B$ \textit{blocks}", OK),
                 (r"collider", {"A": [3.2, 1.2, 0], "B": [4.4, 0.0, 0], "C": [5.6, 1.2, 0]}, [("A", "B"), ("C", "B")],
                  r"conditioning on $B$ \textit{opens}", BAD)]
        groups = VGroup()
        for name, pos, edges, rule, col in specs:
            g = CausalGraph(pos, edges, radius=0.3, font_size=18, colors={"B": GOAL})
            t = label(name, font_size=22, color=WHITE).next_to(g, UP, buff=0.25)
            r = label(rule, font_size=19, color=col).next_to(g, DOWN, buff=0.3)
            groups.add(VGroup(g, t, r))
        groups[0].move_to([-4.4, 0.4, 0])
        groups[1].move_to([0.0, 0.4, 0])
        groups[2].move_to([4.4, 0.4, 0])
        rule = stack([(r"a path is \textit{blocked} by $Z$ if it has a chain or fork node in $Z$, \ or a collider "
                       r"with neither it nor any descendant in $Z$", WHITE),
                      (r"$X$ and $Y$ are \textit{d-separated} by $Z$ if every path between them is blocked", GOAL),
                      (r"then $X \perp Y \mid Z$ in every distribution the graph generates", EFFECT)], font_size=21,
                     width=12.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Information flows through a graph along paths, and three kinds of junction govern it. "
            "<bookmark mark='a'/>A chain: A causes B, which causes C. A and C are correlated, but once B is known, "
            "A tells us nothing more about C. Conditioning on B blocks the path. <bookmark mark='b'/>A fork: B causes "
            "both A and C. Again correlated, again blocked by conditioning on B, the common cause. "
            "<bookmark mark='c'/>A collider: A and C both cause B. Now A and C are independent, but conditioning on B, "
            "or on anything B causes, makes them dependent. <bookmark mark='d'/>A path is blocked by a set Z when it "
            "contains a chain or fork node in Z, or a collider with nothing in Z at or below it. "
            "<bookmark mark='e'/>X and Y are d-separated by Z when every path between them is blocked, "
            "<bookmark mark='f'/>and then X and Y are independent given Z in every distribution the model can "
            "generate."
        ) as vo:
            self.play(FadeIn(head))
            for mk, gr in zip("abc", groups):
                vo.wait_until(mk)
                self.play(FadeIn(gr))
            for mk, r in zip("def", rule):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def berkson(self):
        d = load("berkson")
        head = label(r"Berkson's paradox: \ conditioning on a collider", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=5.6, y_length=5.0, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).move_to([-3.0, -0.7, 0])
        xl = label(r"talent", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.15)
        yl = label(r"looks", font_size=19, color=GREY_B).next_to(ax.y_axis, LEFT, buff=0.15).shift(UP * 2)
        dots = VGroup(*[Dot(ax.c2p(max(min(t, 2.9), -2.9), max(min(l_, 2.9), -2.9)), radius=0.035,
                            color=CAUSE if s else GREY_D) for t, l_, s in
                        zip(d["sample_t"], d["sample_l"], d["sample_sel"])])
        line = DashedLine(ax.c2p(-1.4, 2.9), ax.c2p(2.9, -1.4), color=GOAL, stroke_width=2)
        g = CausalGraph({"talent": [2.6, 1.2, 0], "looks": [5.4, 1.2, 0], "actor": [4.0, -0.2, 0]},
                        [("talent", "actor"), ("looks", "actor")], radius=0.55, font_size=16,
                        colors={"actor": GOAL})
        side = stack([(r"everyone: \ correlation " + f"{d['all']:.2f}", GREY_A),
                      (r"actors \ (talent + looks $> 1.5$): \ " + f"{d['selected']:.2f}", CAUSE),
                      (r"selection on a common effect \ manufactures a correlation", GOAL),
                      (r"Berkson \ (1946): \ hospital patients; \ also \ `collider bias' in COVID studies", HIST)],
                     font_size=20, aligned_edge=LEFT, width=5.4).move_to([4.0, -2.0, 0])
        with self.voiceover(
            "Colliders explain a famous illusion. <bookmark mark='a'/>Suppose talent and good looks are independent "
            "in the population: here are six hundred people, with no correlation at all. <bookmark mark='b'/>Suppose "
            "people become film actors when talent and looks together are high enough. Both cause the collider, "
            "being an actor. <bookmark mark='c'/>Among actors, talent and looks are strongly negatively correlated: "
            "minus point six six. The less talented actors had to be better looking to get in. "
            "<bookmark mark='d'/>Selecting on a common effect manufactures a correlation from nothing. Joseph "
            "Berkson found it among hospital patients in 1946, and it resurfaced in studies of patients tested for "
            "COVID-19."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(dots, lag_ratio=0.002), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(line))
            vo.wait_until("c")
            self.play(*[d_.animate.set_opacity(0.15) for d_, s in zip(dots, d["sample_sel"]) if not s],
                      FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def dsep(self):
        d = load("dsep")
        head = label(r"The Reasoner reads independences off the graph", font_size=30, color=CONN).to_edge(UP,
                                                                                                          buff=0.3)
        g = CausalGraph(SPRINK, [("C", "S"), ("C", "R"), ("S", "W"), ("R", "W"), ("W", "L")],
                        colors={"S": CAUSE, "R": CAUSE, "W": EFFECT, "L": EFFECT}, radius=0.36, font_size=20)
        hd = [r"\text{query}", r"\text{d-separated?}"]
        rows = []
        for q in d["queries"]:
            z = r", ".join(q["z"]) if q["z"] else r"\varnothing"
            rows.append([MathTex(q["x"] + r" \perp " + q["y"] + r" \mid " + z, font_size=26), bool(q["dsep"])])
        grid = ValueGrid(hd, rows, col_w=[3.6, 2.4], cell_h=0.52, font_size=24).move_to([2.6, -0.4, 0])
        notes = label(r"sprinkler and rain: \ dependent; \ independent given clouds; \ dependent again given wet "
                      r"grass, \ or even the slippery path", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner implements d-separation and runs it on the sprinkler model. <bookmark mark='a'/>Sprinkler "
            "and rain are dependent, through the clouds. <bookmark mark='b'/>Given the clouds, they are independent: "
            "the fork is blocked. <bookmark mark='c'/>Given the clouds and the wet grass, they are dependent again, "
            "because wet grass is a collider; and conditioning on the slippery path, its descendant, opens it too. "
            "<bookmark mark='d'/>The remaining queries are blocked chains. Every one of these is a testable "
            "prediction about data, made from the graph alone. That is what makes causal graphs empirical."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[2])), FadeIn(VGroup(*grid.cell[3])), FadeIn(notes))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4, len(rows))], lag_ratio=0.3))
        self.clear_scene()
