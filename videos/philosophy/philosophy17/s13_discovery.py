from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


SPRINK = {"C": [-3.6, 1.7, 0], "S": [-5.2, 0.3, 0], "R": [-2.0, 0.3, 0], "W": [-3.6, -1.1, 0], "L": [-1.4, -1.1, 0]}
NAMES = {"C": "cloudy", "S": "sprinkler", "R": "rain", "W": "wet", "L": "slippery"}


def edge_line(pos, a, b, color=GREY_B, radius=0.36, width=3):
    pa, pb = np.array(pos[a], float), np.array(pos[b], float)
    u = (pb - pa) / np.linalg.norm(pb - pa)
    return Line(pa + u * radius, pb - u * radius, color=color, stroke_width=width)


def edge_arrow(pos, a, b, color=GREY_B, radius=0.36, width=3):
    pa, pb = np.array(pos[a], float), np.array(pos[b], float)
    u = (pb - pa) / np.linalg.norm(pb - pa)
    return Arrow(pa + u * radius, pb - u * radius, buff=0.02, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.18)


def nodes(pos, radius=0.36, font_size=20, colors=None):
    colors = colors or {}
    g = {}
    for n, p in pos.items():
        c = colors.get(n, WHITE)
        g[n] = VGroup(Circle(radius=radius, color=c, stroke_width=3).move_to(p),
                      label(n, font_size=font_size, color=c).move_to(p))
    return g


class Discovery(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Discovering causes", r"Can the graph itself be learned from data?",
                            lit=(1990, 2006), part=PART)
        with self.voiceover("Chapter twelve. Discovering causes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.skeleton()
        self.orient()
        self.equivalence()
        self.brick()
        self.beyond()

    def skeleton(self):
        d = load("pc")
        head = label(r"The PC algorithm \ (Spirtes and Glymour, \ 1991): \ the skeleton", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        nd = nodes(SPRINK)
        keys = sorted(SPRINK)
        pairs = [(a, b) for i, a in enumerate(keys) for b in keys[i + 1:]]
        lines = {p: edge_line(SPRINK, *p) for p in pairs}
        sep = {tuple(k.split("-")): v for k, v in d["data"]["sepsets"].items()}
        r1 = [p for p in pairs if p in sep and len(sep[p]) == 1]
        r2 = [p for p in pairs if p in sep and len(sep[p]) == 2]
        key = label(r", \ ".join(f"{k}: {v}" for k, v in NAMES.items()), font_size=17, color=GREY_A).next_to(
            nd["W"], DOWN, buff=0.45).set_x(-3.3)
        side = stack([(r"start: \ every pair connected", WHITE),
                      (r"round 0: \ test $X \perp Y$: \ every pair is dependent, \ nothing removed", GREY_A),
                      (r"round 1: \ test $X \perp Y \mid Z$: \ remove " + r", \ ".join(f"{a}--{b}" for a, b in r1), CAUSE),
                      (r"\ \ \ \ e.g. \ $S \perp R \mid C$: \ sprinkler and rain are linked only through clouds", GREY_A),
                      (r"round 2: \ remove " + r", \ ".join(f"{a}--{b}" for a, b in r2) + r" \ \ ($C \perp W \mid S, R$)",
                       CAUSE),
                      (r"from " + f"{d['n']:,}".replace(",", "{,}") + r" samples: \ " + f"{d['data']['tests']}" +
                       r" G-tests; \ the true skeleton", OK)], font_size=20, aligned_edge=LEFT, width=7.2).move_to(
            [2.8, -0.2, 0])
        assert sorted(map(tuple, d["data"]["skeleton"])) == sorted(map(tuple, d["oracle"]["skeleton"]))
        with self.voiceover(
            "Can the graph itself be learned from data? Peter Spirtes and Clark Glymour's PC algorithm says yes, "
            "up to a limit. <bookmark mark='a'/>Start with every pair of variables connected. "
            "<bookmark mark='b'/>Round zero: test each pair for independence. In the sprinkler data every pair is "
            "dependent, so nothing goes. <bookmark mark='c'/>Round one: test each remaining pair for independence "
            "given one neighbour. Four edges go. <bookmark mark='d'/>For instance, sprinkler and rain are "
            "independent given the clouds: they are linked only through them. <bookmark mark='e'/>Round two, "
            "conditioning on two: clouds and wet grass are independent given sprinkler and rain. "
            "<bookmark mark='f'/>The Reasoner ran this on twenty thousand samples from the sprinkler model, with "
            "fifty-six statistical tests, and recovered the true skeleton."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(v) for v in nd.values()], FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines.values()], lag_ratio=0.05), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), *[lines[p].animate.set_opacity(0.08) for p in r1])
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(nd["C"], color=CAUSE))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), *[lines[p].animate.set_opacity(0.08) for p in r2])
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def orient(self):
        d = load("pc")["data"]
        head = label(r"Orienting the edges", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        nd = nodes(SPRINK)
        und = {tuple(e): edge_line(SPRINK, *e) for e in d["undirected"]}
        dirs = {tuple(e): edge_arrow(SPRINK, *e, color=EFFECT) for e in d["directed"]}
        plain = {tuple(e): edge_line(SPRINK, *e) for e in d["directed"]}
        side = stack([(r"v-structure: \ $S - W - R$ with $W$ \textit{not} in $S$ and $R$'s separating set", CAUSE),
                      (r"so orient $S \to W \leftarrow R$: \ a collider", CAUSE),
                      (r"Meek's rules \ (1995): \ $W - L$ must be $W \to L$, \ or a new collider would appear", EFFECT),
                      (r"$C - S$ and $C - R$: \ no rule applies: \ left undirected", BAD),
                      (r"the output: \ a CPDAG, \ standing for every graph the data cannot tell apart", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=7.2).move_to([2.8, -0.2, 0])
        with self.voiceover(
            "Next, the algorithm orients what it can. <bookmark mark='a'/>Sprinkler and rain are both adjacent "
            "to wet grass, but not to each other, and wet grass was not among the variables that separated them. "
            "<bookmark mark='b'/>That pattern is only possible if both point into wet grass: a collider, which "
            "has a distinctive statistical signature. <bookmark mark='c'/>Christopher Meek's rules then propagate: "
            "the edge from wet grass to slippery must point away, or it would create a collider the data did not "
            "show. <bookmark mark='d'/>The edges from the clouds cannot be oriented. <bookmark mark='e'/>The "
            "output is a partially directed graph that stands for every causal graph the data cannot tell apart."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(v) for v in nd.values()], *[Create(l) for l in und.values()],
                      *[Create(l) for l in plain.values()])
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(nd["W"], color=CAUSE))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), ReplacementTransform(plain[("S", "W")], dirs[("S", "W")]),
                      ReplacementTransform(plain[("R", "W")], dirs[("R", "W")]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), ReplacementTransform(plain[("W", "L")], dirs[("W", "L")]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), *[l.animate.set_color(BAD) for l in und.values()])
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def equivalence(self):
        d = load("pc")
        head = label(r"The Markov equivalence class", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        small = {k: [v[0] * 0.55, v[1] * 0.55 - 0.3, 0] for k, v in SPRINK.items()}
        groups = VGroup()
        for i, edges in enumerate(d["class"]):
            off = np.array([-4.4 + 4.4 * i, 0, 0]) - np.array([-3.6 * 0.55, 0, 0])
            pos = {k: list(np.array(v) + off) for k, v in small.items()}
            nd = nodes(pos, radius=0.26, font_size=15)
            arrs = [edge_arrow(pos, a, b, radius=0.26, width=2.5,
                               color=CAUSE if {a, b} & {"C"} else GREY_B) for a, b in edges]
            groups.add(VGroup(*nd.values(), *arrs))
        cnt = label(r"the Reasoner enumerates every orientation of the skeleton: \ " + f"{d['class_size']}" +
                    r" acyclic graphs share its independences", font_size=20, color=WHITE).next_to(groups, DOWN,
                                                                                              buff=0.45)
        thm = stack([(r"Verma and Pearl \ (1990): \ two DAGs are Markov equivalent iff they have the same skeleton "
                      r"and the same v-structures", OK),
                     (r"the clouds may cause rain, \ or rain the clouds: \ no observational data can decide", BAD)],
                    font_size=20, width=12.6).next_to(cnt, DOWN, buff=0.35)
        with self.voiceover(
            "How many graphs does the output stand for? <bookmark mark='a'/>The Reasoner enumerates every way of "
            "orienting the skeleton without cycles, and keeps those with the same independences. Three remain. "
            "<bookmark mark='b'/>Thomas Verma and Pearl proved the general rule: two causal graphs are "
            "observationally equivalent exactly when they have the same skeleton and the same colliders. "
            "<bookmark mark='c'/>In one of these graphs the clouds cause the rain; in another the rain causes the "
            "clouds. No quantity of passive observation can decide which."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.3), FadeIn(cnt))
            vo.wait_until("b")
            self.play(FadeIn(thm[0]))
            vo.wait_until("c")
            self.play(FadeIn(thm[1]))
        self.clear_scene()

    def brick(self):
        w = wall(upto=17, current=17).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(17, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the seventeenth brick in the Wall. <bookmark mark='a'/>The dream: read causes off "
            "correlations, given enough data. <bookmark mark='b'/>The wall: Markov equivalence. Graphs with the "
            "same skeleton and the same colliders entail exactly the same independences, so even infinite "
            "observational data leave the direction of many arrows open. <bookmark mark='c'/>What it forces: "
            "intervene, or assume. An experiment breaks the symmetry; so do assumptions about time order, about "
            "the form of the equations, or about the noise, which is where the field went next."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[17], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def beyond(self):
        d = load("pc")["lingam"]["uniform"]
        head = label(r"Breaking the symmetry: \ non-Gaussian noise", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        axs = VGroup()
        clouds = VGroup()
        for i, (pts, name, dep, col) in enumerate(((d["forward_pts"], r"$X \to Y$: \ residual of $Y$ on $X$",
                                                    d["forward_dep"], OK),
                                                   (d["backward_pts"], r"$Y \to X$: \ residual of $X$ on $Y$",
                                                    d["backward_dep"], BAD))):
            xm = max(abs(p[0]) for p in pts) * 1.05
            ym = max(abs(p[1]) for p in pts) * 1.05
            ax = Axes(x_range=[-xm, xm, xm], y_range=[-ym, ym, ym], x_length=4.2, y_length=2.8,
                      axis_config={"color": GREY_B, "include_ticks": False}).move_to([-3.4 + 6.8 * i, 0.4, 0])
            dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.025, color=col, fill_opacity=0.7) for x, y in pts])
            t = label(name, font_size=19, color=col).next_to(ax, UP, buff=0.15)
            s = label(r"dependence of residual on regressor: \ " + f"{dep:.2f}", font_size=19, color=col).next_to(
                ax, DOWN, buff=0.15)
            axs.add(VGroup(ax, t, s))
            clouds.add(dots)
        g = load("pc")["lingam"]["gaussian"]
        rows = stack([(r"both residuals are \textit{uncorrelated} with the regressor; \ only the true direction "
                       r"leaves them \textit{independent} \ (LiNGAM: \ Shimizu et al., \ 2006)", WHITE),
                      (r"with Gaussian noise: \ " + f"{g['forward_dep']:.3f}" + r" and " + f"{g['backward_dep']:.3f}" +
                       r": \ no direction can be told", BAD),
                      (r"latent variables: \ FCI \ (Spirtes et al.; \ Zhang, \ 2008); \ scores: \ GES \ (Chickering, "
                       r"\ 2002); \ NOTEARS \ (Zheng et al., \ 2018)", GREY_A)], font_size=19, width=12.8).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Assumptions about the noise can break the symmetry. <bookmark mark='a'/>Let X cause Y linearly, with "
            "noise that is uniform, not bell-shaped. Regress Y on X: the residual is independent of X. "
            "<bookmark mark='b'/>Regress the wrong way, X on Y: the residual is still uncorrelated with Y, as least "
            "squares guarantees, but no longer independent of it; the cloud has a slanted, parallelogram shape. "
            "<bookmark mark='c'/>Shohei Shimizu and colleagues turned this into the LiNGAM algorithm. "
            "<bookmark mark='d'/>With Gaussian noise the trick fails, and both directions look the same: Markov "
            "equivalence is the Gaussian case. <bookmark mark='e'/>Other methods handle hidden variables, like "
            "Jiji Zhang's complete version of FCI; search over scores, like David Maxwell Chickering's GES; or "
            "turn acyclicity into a smooth constraint, as NOTEARS did in 2018, bringing discovery into deep learning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(axs[0]), FadeIn(clouds[0]))
            vo.wait_until("b")
            self.play(FadeIn(axs[1]), FadeIn(clouds[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
