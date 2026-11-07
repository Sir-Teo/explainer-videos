from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono


def sub(name: str) -> str:
    """A state name as TeX: P1 -> P_1."""
    return name[0] + (("_" + name[1:]) if len(name) > 1 else "")


def node(name: str, pos, color=GREY_B, r=0.3, fs=24):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.2, fill_color=BG, fill_opacity=1).move_to(pos)
    t = MathTex(sub(name), font_size=fs, color=color).move_to(c)
    g = VGroup(c, t)
    g.circle, g.text = c, t
    return g


def edge(a, b, act, color=GREY_B, angle=0.0, side=1, fs=24, r=0.3, lab_buff=0.18, shift=0.0):
    """A labelled transition from node a to node b; curved when angle is not zero (positive bends to the right of
    the direction of travel).  The label sits beside the middle of the arrow, on the outside of a curve."""
    pa, pb = a.get_center(), b.get_center()
    d = (pb - pa) / np.linalg.norm(pb - pa)
    if angle:
        s = pa + r * rotate_vector(d, -angle / 2)
        e = pb - r * rotate_vector(d, angle / 2)
        arr = CurvedArrow(s, e, angle=angle, color=color, stroke_width=2.4, tip_length=0.16)
        mid = arr.point_from_proportion(0.5)
        out = mid - (s + e) / 2
        out = out / np.linalg.norm(out)
    else:
        o = rotate_vector(d, PI / 2) * shift
        pa, pb = pa + o, pb + o
        arr = Arrow(pa, pb, buff=r + 0.02, color=color, stroke_width=2.4, max_tip_length_to_length_ratio=0.15,
                    tip_length=0.16)
        mid = (pa + pb) / 2
        out = rotate_vector(d, PI / 2) * side
    t = MathTex(act, font_size=fs, color=color) if "\\" in act or len(act) == 1 else label(act, font_size=fs - 4,
                                                                                            color=color)
    t.move_to(mid + out * (lab_buff + max(t.width, t.height) / 2))
    g = VGroup(arr, t)
    g.arrow, g.text = arr, t
    return g


def paint(n, c):
    """Animations that recolour a state: its outline and its name, not its fill."""
    return [n.circle.animate.set_stroke(color=c), n.text.animate.set_color(c)]


def machine(lts, pos, color=GREY_B, fs=24):
    """Nodes and edges of a labelled transition system, with node positions given; parallel edges between the same
    two states are drawn as one arrow with both labels."""
    nodes = {s: node(s, p, color, fs=fs) for s, p in pos.items()}
    edges = {}
    for s, outs in lts.items():
        if s not in pos:
            continue
        for a, t in outs:
            edges.setdefault((s, t), []).append(a)
    return nodes, edges


def traces(lts, s, depth=3):
    out = {()}
    if depth == 0:
        return out
    for a, t in lts[s]:
        out |= {(a,) + tr for tr in traces(lts, t, depth - 1)}
    return out


def trace_tex(ts) -> str:
    items = sorted(ts, key=lambda tr: (len(tr), tr))
    return r"\{\," + r",\ ".join(r"\varepsilon" if not tr else "".join(tr) for tr in items) + r"\,\}"


class Equivalence(VoiceoverScene):
    def construct(self):
        self.card()
        self.contexts()
        self.game()
        self.coinduction()
        self.vending()
        self.applicative()
        self.logical()
        self.tait()

    def card(self):
        card = chapter_card(5, r"When are two programs the same?", r"Can we prove it without trying every context?",
                            lit=(1981, 1990), extra=((1981, r"Park: \ bisimulation"),
                                                     (1990, r"Abramsky: \ applicative bisimulation")), part=PART)
        with self.voiceover("Chapter five. When are two programs the same? Can we prove it without trying every "
                            "context?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ every context is too many
    def contexts(self):
        head = label(r"Every context is too many", font_size=36).to_edge(UP, buff=0.3)
        ce = MathTex(r"e_1 \cong e_2", r"\iff", r"\text{for every context } C:\ \ C[e_1] \Downarrow n \iff "
                     r"C[e_2] \Downarrow n", font_size=30, color=WHITE).next_to(head, DOWN, buff=0.35)
        ce[2].set_color(NO)
        progs = VGroup(*[VGroup(SurroundingRectangle(m, buff=0.18, corner_radius=0.1, color=c), m) for m, c in (
            (mono("fun x -> x + x", size=22, color=WHITE), DATA), (mono("fun x -> 2 * x", size=22, color=WHITE),
                                                                   LAM))]).arrange(RIGHT, buff=2.4)
        progs.next_to(ce, DOWN, buff=0.5)
        names = VGroup(MathTex("e_1", font_size=28, color=DATA).next_to(progs[0], UP, buff=0.1),
                       MathTex("e_2", font_size=28, color=LAM).next_to(progs[1], UP, buff=0.1))
        ctx = [("([ ] 5)", "10"), ("(([ ] 3) + 1)", "7"), ("((fun g -> g (g 1)) [ ])", "4")]
        rows = VGroup()
        for c, v in ctx:
            r = VGroup(mono(c, size=19, color=GREY_A), MathTex(r"\Downarrow " + v, font_size=26, color=DATA),
                       MathTex(r"\Downarrow " + v, font_size=26, color=LAM),
                       MathTex(r"\checkmark", font_size=26, color=YES))
            rows.add(r)
        for r in rows:
            r[0].move_to([-2.6, 0, 0])
            r[1].move_to([progs[0].get_x() + 1.6, 0, 0])
            r[2].move_to([progs[1].get_x() + 1.6, 0, 0])
            r[3].move_to([5.6, 0, 0])
        rows.arrange(DOWN, buff=0.28)
        for r in rows:
            r[0].set_x(-2.4)
            r[1].set_x(1.0)
            r[2].set_x(3.4)
            r[3].set_x(4.9)
        rows.next_to(progs, DOWN, buff=0.45)
        ch = label(r"context $C$", font_size=20, color=GREY_B).next_to(rows[0][0], UP, buff=0.25)
        dots = MathTex(r"\vdots \quad \text{infinitely many}", font_size=26, color=NO).next_to(rows, DOWN, buff=0.2)
        tools = VGroup(
            label(r"bisimulation: \ check one step, \ forever \ \ (coinduction)", font_size=22, color=HEAD),
            label(r"logical relations: \ build the relation type by type \ \ (induction)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        ill = note(r"illustrative programs", font_size=16).to_corner(DR, buff=0.2).shift(UP * 0.95)
        with self.voiceover(
            "Chapter four defined sameness: two programs are contextually equivalent when no context can tell "
            "them apart. <bookmark mark='a'/> Are x plus x and two times x the same function? <bookmark "
            "mark='b'/> Apply each to five, add one to its value at three, apply it twice: every test agrees. "
            "<bookmark mark='c'/> But there are infinitely many contexts, and testing is not proof. <bookmark "
            "mark='d'/> This chapter gives two methods that never quantify over contexts: bisimulation, which "
            "checks one step and then the same again, forever; and logical relations, which build sameness type "
            "by type."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ce))
            vo.wait_until("a")
            self.play(FadeIn(progs), FadeIn(names), FadeIn(ill))
            vo.wait_until("b")
            self.play(FadeIn(ch))
            for r in rows:
                self.play(FadeIn(r[0], shift=RIGHT * 0.2), run_time=0.5)
                self.play(FadeIn(r[1]), FadeIn(r[2]), FadeIn(r[3]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(dots), Circumscribe(ce[2], color=NO))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tools], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the bisimulation game
    def _choice(self):
        L = load("bisim")["choice"]["lts"]
        pos = {"P": [-5.3, 1.75, 0], "P1": [-5.3, 0.15, 0], "P2": [-6.1, -1.45, 0], "P3": [-4.5, -1.45, 0],
               "Q": [-2.3, 1.75, 0], "Q1": [-3.1, 0.15, 0], "Q2": [-1.5, 0.15, 0], "Q3": [-3.1, -1.45, 0],
               "Q4": [-1.5, -1.45, 0]}
        nodes, eds = machine(L, pos)
        sides = {("P", "P1"): 1, ("P1", "P2"): -1, ("P1", "P3"): 1, ("Q", "Q1"): -1, ("Q", "Q2"): 1,
                 ("Q1", "Q3"): -1, ("Q2", "Q4"): 1}
        edges = {(s, t): edge(nodes[s], nodes[t], ", ".join(acts), side=sides[(s, t)]) for (s, t), acts in
                 eds.items()}
        tp = mono("a.(b + c)", size=22, color=WHITE).move_to([-5.3, 2.6, 0])
        tq = mono("a.b + a.c", size=22, color=WHITE).move_to([-2.3, 2.6, 0])
        return L, nodes, edges, tp, tq

    def game(self):
        b = load("bisim")["choice"]
        head = label(r"Same traces, \ different machines", font_size=36).to_edge(UP, buff=0.3)
        L, nodes, edges, tp, tq = self._choice()
        mP = VGroup(tp, *[nodes[s] for s in ("P", "P1", "P2", "P3")],
                    *[e for (s, _), e in edges.items() if s.startswith("P")])
        mQ = VGroup(tq, *[nodes[s] for s in ("Q", "Q1", "Q2", "Q3", "Q4")],
                    *[e for (s, _), e in edges.items() if s.startswith("Q")])
        tr = VGroup(
            MathTex(r"\mathrm{traces}(P) = " + trace_tex(traces(L, "P")), font_size=30, color=WHITE),
            MathTex(r"\mathrm{traces}(Q) = " + trace_tex(traces(L, "Q")), font_size=30, color=WHITE),
            label(r"the same \ (our checker)" if b["same_traces"] else r"different", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.2, 2.1, 0])
        story = wrapped_label(r"read $a$ as \textit{coin}, \ $b$ as \textit{tea}, \ $c$ as \textit{coffee}: \ "
                              r"$Q$ chooses your drink when it takes the coin", 5.6, font_size=20, color=GREY_A)
        story.next_to(tr, DOWN, buff=0.25).align_to(tr, LEFT)
        moves = VGroup(
            label(r"1. \ attacker: \ $P \xrightarrow{a} P_1$", font_size=21, color=HEAD),
            label(r"\phantom{1. }\ defender must match: \ $Q \xrightarrow{a} Q_1$ \ or \ $Q \xrightarrow{a} Q_2$",
                  font_size=21, color=DATA),
            label(r"2. \ against $Q_1$: \ $P_1 \xrightarrow{c} P_3$; \ \ $Q_1$ has no $c$", font_size=21, color=NO),
            label(r"\phantom{2. }\ against $Q_2$: \ $P_1 \xrightarrow{b} P_2$; \ \ $Q_2$ has no $b$", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -0.75, 0])
        res = label(r"the attacker always wins: \ $P \not\sim Q$ \ \ (our checker agrees)" if not b["bisimilar"]
                    else r"bisimilar", font_size=21, color=NO)
        f = b["formula"].replace("<", r"\langle ").replace(">", r"\rangle ").replace(" and ", r" \wedge ")
        f = f.replace("true", r"\mathsf{true}")
        form = MathTex(r"P \models " + f, r"\qquad", r"Q \not\models " + f, font_size=28, color=YES)
        form[2].set_color(NO)
        hm = label(r"a formula of Hennessy--Milner logic \ (1985) \ tells them apart", font_size=19, color=GREY_B)
        bottom = VGroup(res, form, hm).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3).set_x(1.6)
        moves.next_to(bottom, UP, buff=0.3).align_to(tr, LEFT)
        for g in (tr, story, moves, bottom):
            if g.get_right()[0] > 6.85:
                g.shift(LEFT * (g.get_right()[0] - 6.85))
        with self.voiceover(
            "Programs that run forever are better compared by what they can do next. Here are two "
            "tiny machines in Milner's notation. <bookmark mark='a'/> Both can do a then b, or a then c: the same "
            "traces. <bookmark mark='b'/> But read a as a coin, and b and c as tea and coffee. The first takes "
            "your coin and lets you choose; the second chooses for you as it takes the coin."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mP), FadeIn(mQ))
            vo.wait_until("a")
            self.play(FadeIn(tr))
            vo.wait_until("b")
            self.play(FadeIn(story))
        with self.voiceover(
            "Bisimulation makes this a game. <bookmark mark='c'/> An attacker moves in either machine: a coin, in "
            "the first. <bookmark mark='d'/> The defender must answer with the same action in the other, and so "
            "commits to a branch. <bookmark mark='e'/> Whichever it picks, the attacker asks for the drink that "
            "branch cannot give. <bookmark mark='f'/> The attacker always wins, so the machines are not "
            "bisimilar, and one formula says why: the first can take a coin and then offer both drinks."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeOut(story), FadeIn(moves[0]), edges[("P", "P1")].animate.set_color(HEAD),
                      *paint(nodes["P1"], HEAD))
            vo.wait_until("d")
            self.play(FadeIn(moves[1]), edges[("Q", "Q1")].animate.set_color(DATA),
                      edges[("Q", "Q2")].animate.set_color(DATA), *paint(nodes["Q1"], DATA),
                      *paint(nodes["Q2"], DATA))
            vo.wait_until("e")
            self.play(FadeIn(moves[2]), edges[("P1", "P3")].animate.set_color(NO), Wiggle(nodes["Q1"]))
            self.play(FadeIn(moves[3]), edges[("P1", "P2")].animate.set_color(NO), Wiggle(nodes["Q2"]))
            vo.wait_until("f")
            self.play(FadeIn(res))
            self.play(Write(form), FadeIn(hm))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ coinduction
    def coinduction(self):
        head = label(r"Bisimulation, \ and coinduction", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        df = VGroup(
            label(r"$R$ is a \textbf{bisimulation} if, \ whenever $p \mathrel{R} q$:", font_size=22, color=WHITE),
            MathTex(r"p \xrightarrow{a} p'", r"\implies", r"q \xrightarrow{a} q' \text{ for some } q' \text{ with } "
                    r"p' \mathrel{R} q'", font_size=fs, color=HEAD),
            MathTex(r"q \xrightarrow{a} q'", r"\implies", r"p \xrightarrow{a} p' \text{ for some } p' \text{ with } "
                    r"p' \mathrel{R} q'", font_size=fs, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        df[1:].shift(RIGHT * 0.4)
        rows = VGroup(
            MathTex(r"R \text{ is a bisimulation}", r"\iff", r"R \subseteq F(R)", font_size=32),
            MathTex(r"{\sim}", r"=", r"\bigcup\, \{\, R \mid R \subseteq F(R) \,\}", font_size=32),
            MathTex(r"{\sim}", r"=", r"\nu F", font_size=32, color=YES),
            MathTex(r"R \subseteq F(R)", r"\implies", r"R \subseteq {\sim}", font_size=32, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(df, DOWN, buff=0.4).align_to(df, LEFT)
        rows[2].align_to(rows[1], LEFT)
        whys = VGroup(
            label(r"$F$: \ the pairs whose moves match into $R$", font_size=19, color=GREY_B),
            label(r"bisimilarity: \ the union of them all", font_size=19, color=GREY_B),
            label(r"Knaster--Tarski: \ the \textit{greatest} fixed point", font_size=19, color=YES),
            label(r"coinduction: \ exhibit one $R$, \ check one step", font_size=19, color=YES),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        # the lattice of relations: least fixed points climb from below, greatest descend from above
        x = 4.9
        top = MathTex(r"\text{all pairs}", font_size=22, color=GREY_B).move_to([x, 2.0, 0])
        botm = MathTex(r"\emptyset", font_size=26, color=GREY_B).move_to([x, -3.0, 0])
        spine = Line(botm.get_top() + UP * 0.1, top.get_bottom() + DOWN * 0.1, color=GREY_D, stroke_width=2)
        mu = Dot([x, -1.7, 0], color=DATA)
        nu = Dot([x, 0.8, 0], color=YES)
        mul = MathTex(r"\mu F", font_size=26, color=DATA).next_to(mu, LEFT, buff=0.15)
        nul = MathTex(r"\nu F = {\sim}", font_size=26, color=YES).next_to(nu, LEFT, buff=0.15)
        up = Arrow(botm.get_top() + RIGHT * 0.35, mu.get_center() + RIGHT * 0.35, buff=0.05, color=DATA,
                   stroke_width=3)
        dn = Arrow(top.get_bottom() + RIGHT * 0.35, nu.get_center() + RIGHT * 0.35, buff=0.05, color=YES,
                   stroke_width=3)
        upl = label(r"Kleene: \ climb \ (ch.\ 3)", font_size=18, color=DATA).next_to(up, RIGHT, buff=0.1)
        dnl = label(r"refine \ down", font_size=18, color=YES).next_to(dn, RIGHT, buff=0.1)
        lat = VGroup(top, botm, spine, mu, nu, mul, nul, up, dn, upl, dnl)
        if lat.get_right()[0] > 6.85:
            lat.shift(LEFT * (lat.get_right()[0] - 6.85))
        with self.voiceover(
            "The definition is David Park's, from nineteen eighty-one, refining Robin Milner's work on CCS. "
            "<bookmark mark='a'/> A relation is a bisimulation if, whenever p is related to q, every move of p is "
            "matched by a move of q with the same action, into related states, and the other way round. <bookmark "
            "mark='b'/> Write F of R for the pairs whose moves match into R. <bookmark mark='c'/> Bisimilarity is "
            "the union of all bisimulations, <bookmark mark='d'/> the greatest fixed point of F, by Knaster and "
            "Tarski. <bookmark mark='e'/> Chapter three climbed to least fixed points from below; this one is "
            "reached from above. <bookmark mark='f'/> Its proof principle is coinduction: exhibit one relation, "
            "and check one step."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(df))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]), run_time=1.4)
            vo.wait_until("e")
            self.play(FadeIn(top), FadeIn(botm), Create(spine))
            self.play(GrowArrow(up), FadeIn(mu), FadeIn(mul), FadeIn(upl))
            self.play(GrowArrow(dn), FadeIn(nu), FadeIn(nul), FadeIn(dnl))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(Circumscribe(rows[3], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the vending machines, related
    def vending(self):
        v = load("bisim")["vending"]
        c = load("bisim")["choice"]
        L = v["lts"]
        head = label(r"A bisimulation, \ exhibited", font_size=36).to_edge(UP, buff=0.3)
        pos = {"V1": [-1.8, 1.3, 0], "V2": [-1.8, -1.3, 0], "W1": [-5.2, 2.0, 0], "W2": [-5.2, 0.0, 0],
               "W3": [-5.2, -2.0, 0]}
        nodes, eds = machine(L, pos)
        ang = {("V2", "V1"): 2.2}
        shf = {("W2", "W3"): -0.12, ("W3", "W2"): -0.12}
        sides = {("W3", "W2"): -1}
        edges = VGroup(*[edge(nodes[s], nodes[t], ", ".join(a), angle=ang.get((s, t), 0.0),
                              side=sides.get((s, t), -1), fs=22, shift=shf.get((s, t), 0.0))
                         for (s, t), a in eds.items()])
        tv = label(r"$V$: \ two states", font_size=20, color=GREY_A).next_to(nodes["V1"], UP, buff=0.5)
        tw = label(r"$W$: \ three states", font_size=20, color=GREY_A).next_to(nodes["W1"], UP, buff=0.15)
        pairs = sorted([(p, q) for p in ("V1", "V2") for q in ("W1", "W2", "W3")
                        if v["partition"][p] == v["partition"][q]], key=lambda pq: (pq[1], pq[0]))
        rel = VGroup(*[DashedLine(nodes[p].get_center(), nodes[q].get_center(), buff=0.32, color=KERN,
                                  stroke_width=2, dash_length=0.1) for p, q in pairs])
        rtex = MathTex(r"R = \{" + r",\ ".join(rf"({sub(p)}, {sub(q)})" for p, q in pairs) + r"\}", font_size=28,
                       color=KERN)

        def moves(s):
            return {a: t for a, t in L[s]}
        checks = VGroup()
        for p, q in pairs:
            mp, mq = moves(p), moves(q)
            acts = sorted(mp)
            ok = sorted(mp) == sorted(mq) and all((mp[a], mq[a]) in pairs for a in acts)
            tgt = sorted({(mp[a], mq[a]) for a in acts})
            txt = (rf"$({sub(p)}, {sub(q)})$: \ " + r", ".join(rf"\textit{{{a}}}" for a in acts) + r" $\mapsto$ "
                   + r", ".join(rf"$({sub(x)}, {sub(y)})$" for x, y in tgt) + (r" \ $\checkmark$" if ok else ""))
            checks.add(label(txt, font_size=20, color=YES if ok else NO))
        right = VGroup(rtex, checks.arrange(DOWN, aligned_edge=LEFT, buff=0.14)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.25)
        right.move_to([3.3, 1.4, 0])
        concl = label(r"$R \subseteq F(R)$, \ so $V_1 \sim W_1$", font_size=24, color=YES).next_to(right, DOWN,
                                                                                                   buff=0.3)
        concl.align_to(right, LEFT)
        pr = VGroup(
            label(r"our checker: \ partition refinement, \ from ``all related'' downwards", font_size=19,
                  color=GREY_B),
            label(rf"$V, W$: \ {v['blocks']} blocks after {v['rounds']} rounds: \ $V_1 \sim W_1$", font_size=20,
                  color=YES if v["bisimilar"] else NO),
            label(rf"$a.(b+c), \ a.b + a.c$: \ {c['blocks']} blocks after {c['rounds']} rounds: \ $P \not\sim Q$"
                  if not c["bisimilar"] else r"bisimilar", font_size=20, color=NO),
            label(r"(Kanellakis and Smolka, \ 1983; \ Paige and Tarjan, \ 1987)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(concl, DOWN, buff=0.45).align_to(right, LEFT)
        for g in (right, concl, pr):
            if g.get_right()[0] > 6.85:
                g.shift(LEFT * (g.get_right()[0] - 6.85))
        blockcol = [HEAD, DATA]
        recolor = [a for s in nodes for a in paint(nodes[s], blockcol[v["partition"][s] % 2])]
        with self.voiceover(
            "Here coinduction proves two machines the same. <bookmark mark='a'/> V takes a coin and serves tea or "
            "coffee, then starts again. W does the same, but returns to a copy of its start. <bookmark mark='b'/> "
            "Exhibit a relation: the starts together, the waiting states together, and V's start with W's copy. "
            "<bookmark mark='c'/> Check one step for each pair: every move lands in a related pair. <bookmark "
            "mark='d'/> So the machines are bisimilar, forever, from a finite check. <bookmark mark='e'/> Our "
            "checker finds such relations itself, starting with everything related and splitting blocks until "
            "nothing changes."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], FadeIn(tv), FadeIn(tw))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e[0]) for e in edges], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(e[1]) for e in edges], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rel], lag_ratio=0.3), FadeIn(rtex))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(ch, shift=RIGHT * 0.15) for ch in checks], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(concl))
            vo.wait_until("e")
            self.play(FadeIn(pr[0]), *recolor)
            self.play(LaggedStart(*[FadeIn(t) for t in pr[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ applicative bisimulation
    def applicative(self):
        head = label(r"Applicative bisimulation \ (Abramsky, \ 1990)", font_size=36).to_edge(UP, buff=0.3)
        df = VGroup(
            label(r"$e \lesssim e'$ \ when:", font_size=24, color=WHITE),
            MathTex(r"e \Downarrow n", r"\implies", r"e' \Downarrow n", font_size=30, color=DATA),
            MathTex(r"e \Downarrow \mathsf{fun}\ x \to b", r"\implies",
                    r"e' \Downarrow \mathsf{fun}\ x \to b' \ \text{ and }\ b[v/x] \lesssim b'[v/x]"
                    r"\ \text{ for every value } v", font_size=30, color=HEAD),
            label(r"the largest such relation, \ both ways: \ applicative bisimilarity \ \ (coinductive again)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.4)
        df[1:3].shift(RIGHT * 0.4)
        if df.width > 13.2:
            df.scale_to_fit_width(13.2)
        fs = 34
        L = [
            MathTex(r"\mathsf{fun}\ x \to x + x", r"\quad\text{vs}\quad", r"\mathsf{fun}\ x \to 2 \times x",
                    font_size=fs),
            MathTex(r"(x + x)[n/x]", r"\quad\text{vs}\quad", r"(2 \times x)[n/x]", font_size=fs),
            MathTex(r"n + n", r"\quad\text{vs}\quad", r"2 \times n", font_size=fs),
            MathTex(r"\Downarrow 2n", r"\quad\text{and}\quad", r"\Downarrow 2n", font_size=fs, color=YES),
        ]
        slot = np.array([-1.0, -0.6, 0])
        for m in L:
            m.move_to(slot)
        why = [label(r"both are values: \ functions", font_size=20, color=GREY_B),
               label(r"apply both to the same argument $n$", font_size=20, color=GREY_B),
               label(r"substitute", font_size=20, color=GREY_B),
               label(r"the integer clause: \ the same number", font_size=20, color=YES)]
        for w in why:
            w.next_to(slot, DOWN, buff=0.55)
        concl = MathTex(r"\mathsf{fun}\ x \to x + x \;\simeq\; \mathsf{fun}\ x \to 2 \times x", font_size=30,
                        color=YES).next_to(slot, DOWN, buff=1.2)
        thm = VGroup(
            label(r"one argument at a time, \ instead of every context", font_size=22, color=HEAD),
            label(r"a congruence \ (Howe's method), \ so in a pure language like ours it coincides with "
                  r"$\cong$", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "For functions, Samson Abramsky's applicative bisimulation, from nineteen ninety, plays the same "
            "game. <bookmark mark='a'/> If one program evaluates to a number, the other must give the same "
            "number; if to a function, so must the other, and the two bodies, given any one argument, must be "
            "related again. <bookmark mark='b'/> Our two functions are already values. <bookmark "
            "mark='c'/> Apply both to the same n. <bookmark mark='d'/> Substitute. <bookmark mark='e'/> Both give "
            "two n. <bookmark mark='f'/> One argument at a time, never a context. By Howe's method this relation "
            "is a congruence, so in a pure language like ours it coincides with contextual equivalence."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in df], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(Write(L[0]), FadeIn(why[0]))
            cur, cw = L[0], why[0]
            for k, mk in zip(range(1, 4), "cde"):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(cur, L[k]), ReplacementTransform(cw, why[k]), run_time=1.3)
                cur, cw = L[k], why[k]
            self.play(FadeIn(concl))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(t) for t in thm], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ logical relations for equivalence
    def logical(self):
        head = label(r"Logical relations: \ sameness, \ type by type", font_size=36).to_edge(UP, buff=0.3)
        ys = [-2.3, -0.4, 1.5]
        xl, xr = -6.1, -3.4
        cols = [DATA, HEAD, GREY_B]
        rungs = VGroup(*[DashedLine([xl + 0.75, y, 0], [xr - 0.75, y, 0], color=c, stroke_width=3,
                                    dash_length=0.12) for y, c in zip(ys[:2], cols)])
        rails = VGroup(Line([xl, -2.9, 0], [xl, 2.3, 0], color=GREY_D, stroke_width=2),
                       Line([xr, -2.9, 0], [xr, 2.3, 0], color=GREY_D, stroke_width=2))
        ex = [("1 + 2", "3"), (r"\lambda x.\, x + x", r"\lambda x.\, 2 \times x")]
        terms = VGroup()
        for (a, b), y, c in zip(ex, ys, cols):
            ta = MathTex(a, font_size=26, color=WHITE)
            tb = MathTex(b, font_size=26, color=WHITE)
            ta.next_to([xl, y, 0], UP, buff=0.12)
            tb.next_to([xr, y, 0], UP, buff=0.12)
            terms.add(VGroup(ta, tb))
        for t in terms:
            for m in t:
                if m.get_left()[0] < -6.85:
                    m.shift(RIGHT * (-6.85 - m.get_left()[0]))
        tl = VGroup(*[MathTex(s, font_size=24, color=c).next_to([(xl + xr) / 2, y, 0], DOWN, buff=0.15)
                      for s, y, c in zip((r"\sim_{\mathsf{int}}", r"\sim_{\mathsf{int} \to \mathsf{int}}"), ys, cols)])
        top = MathTex(r"\vdots", font_size=30, color=GREY_B).move_to([(xl + xr) / 2, ys[2], 0])
        ill = note(r"illustrative terms", font_size=16).next_to([(xl + xr) / 2, -2.95, 0], DOWN, buff=0.05)
        dx = -2.4
        d_int = MathTex(r"e \sim_{\mathsf{int}} e'", r"\iff", r"e \Downarrow n,\ e' \Downarrow n \text{ (same } n),"
                        r"\text{ or both diverge}", font_size=27, color=DATA)
        d_fun = VGroup(
            MathTex(r"e \sim_{\sigma \to \tau} e'", r"\iff", r"a \sim_\sigma a' \implies e\ a \sim_\tau e'\ a'",
                    font_size=27, color=HEAD),
            label(r"related arguments, \ related results", font_size=19, color=GREY_A))
        d_fun.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fund = VGroup(
            label(r"fundamental property \ (induction on the typing):", font_size=20, color=YES),
            MathTex(r"\vdash e : \tau", r"\implies", r"e \sim_\tau e", font_size=28, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        defs = VGroup(d_int, d_fun, fund).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 1.25, 0])
        defs.align_to(np.array([dx, 0, 0]), LEFT)
        if defs.get_right()[0] > 6.85:
            defs.scale_to_fit_width(6.85 - dx).align_to(np.array([dx, 0, 0]), LEFT)
        fs = 30
        chain = [MathTex(r"e \sim_\tau e'", font_size=fs),
                 MathTex(r"C[e] \sim_{\mathsf{int}} C[e']", font_size=fs),
                 MathTex(r"C[e] \Downarrow n \iff C[e'] \Downarrow n", font_size=fs),
                 MathTex(r"e \cong e'", font_size=fs + 4, color=YES)]
        cy = -1.85
        for m in chain:
            m.move_to([dx + 2.4, cy, 0])
        cwhy = [label(r"for one pair", font_size=19, color=GREY_B),
                label(r"the fundamental property, \ applied to $C$", font_size=19, color=GREY_B),
                label(r"the bottom rung", font_size=19, color=GREY_B),
                label(r"for every $C$: \ contextual equivalence", font_size=19, color=YES)]
        for w in cwhy:
            w.move_to([dx + 2.4, cy - 0.65, 0])
        fixn = note(r"with \textsf{fix}: \ relations closed under limits \ (ch.\ 4), \ or indexed by steps \ "
                    r"(Appel and McAllester, \ 2001)", font_size=18).to_edge(DOWN, buff=0.12).set_x(2.2)
        if fixn.get_right()[0] > 6.85:
            fixn.shift(LEFT * (fixn.get_right()[0] - 6.85))
        with self.voiceover(
            "The second method builds sameness by induction on types: chapter four's ladder, now between two "
            "programs. <bookmark mark='a'/> Integer programs are related if they give the same number, or both "
            "diverge. <bookmark mark='b'/> Functions are related if they send related arguments to related "
            "results. <bookmark mark='c'/> The fundamental property, by induction on typing: every well-typed "
            "program is related to itself. <bookmark mark='d'/> Now take two related programs. <bookmark "
            "mark='e'/> Put both in a context: applied to the context, the fundamental property keeps them "
            "related. <bookmark mark='f'/> On the bottom rung, that means the same result. <bookmark mark='g'/> "
            "For every context: contextual equivalence, with no context examined."
        ) as vo:
            self.play(FadeIn(head), Create(rails))
            vo.wait_until("a")
            self.play(FadeIn(terms[0]), Create(rungs[0]), FadeIn(tl[0]), FadeIn(d_int), FadeIn(ill))
            vo.wait_until("b")
            self.play(FadeIn(terms[1]), Create(rungs[1]), FadeIn(tl[1]), FadeIn(d_fun), FadeIn(top))
            vo.wait_until("c")
            self.play(FadeIn(fund))
            vo.wait_until("d")
            self.play(Write(chain[0]), FadeIn(cwhy[0]))
            cur, cw = chain[0], cwhy[0]
            for k, mk in zip(range(1, 4), "efg"):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(cur, chain[k]), ReplacementTransform(cw, cwhy[k]), run_time=1.3)
                cur, cw = chain[k], cwhy[k]
            self.play(FadeIn(fixn))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Tait's normalization, and NbE
    def tait(self):
        rows = load("nbe")["rows"]
        head = label(r"Tait: \ every typed term normalizes", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        d = VGroup(
            MathTex(r"\mathrm{Red}_\iota", r"=", r"\{\, t \mid t \text{ reaches a normal form} \,\}", font_size=fs,
                    color=DATA),
            MathTex(r"\mathrm{Red}_{\sigma \to \tau}", r"=", r"\{\, t \mid s \in \mathrm{Red}_\sigma \implies "
                    r"t\ s \in \mathrm{Red}_\tau \,\}", font_size=fs, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lem = VGroup(
            label(r"1. \ $\mathrm{Red}_\tau$ contains only normalizing terms \ (induction on $\tau$)", font_size=20,
                  color=GREY_A),
            label(r"2. \ $\vdash t : \tau$ \ implies \ $t \in \mathrm{Red}_\tau$ \ (induction on $t$): \ the "
                  r"application case \textit{is} the definition", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        top = VGroup(d, lem).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.35)
        if top.width > 13.2:
            top.scale_to_fit_width(13.2)
        top.set_x(0)
        body = [[r["term"], str(r["nbe"]), str(r["beta"]), str(r["beta_steps"]),
                 r"yes" if r["same_normal_form"] else r"no"] for r in rows]
        cols = [[WHITE, YES, WHITE, GREY_A, YES if r["same_normal_form"] else NO] for r in rows]
        tab = grid_table([r"Church term", r"NbE", r"normal order", r"its $\beta$-steps", r"same normal form"], body,
                         widths=[2.2, 1.2, 2.0, 1.9, 2.6], row_h=0.42, font_size=20, colors=cols, mono_cols=(0,))
        tab.next_to(top, DOWN, buff=0.45).set_x(0)
        cap = label(r"our NbE: \ evaluate into Python functions, \ then read the normal form back", font_size=19,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        with self.voiceover(
            "Logical relations first proved that typed programs stop. <bookmark "
            "mark='a'/> At the base type, the reducible terms are those with a normal form; at a function type, "
            "those that send reducible arguments to reducible results. <bookmark mark='b'/> Reducible terms "
            "normalize, by induction on the type. Every typed term is reducible, by induction on the term, and "
            "the application case that defeated the naive proof is now the definition. That is Tait's method, "
            "from nineteen sixty-seven. <bookmark mark='c'/> Read as a program, such a proof normalizes: evaluate "
            "into functions, then read a normal form back. Berger and Schwichtenberg made this precise in "
            "nineteen ninety-one. <bookmark mark='d'/> Ours agrees with step-by-step reduction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(d[0]))
            self.play(FadeIn(d[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in lem], lag_ratio=0.6), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(Circumscribe(VGroup(*[r[4] for r in tab.cells[1:]]), color=YES))
        self.wait(0.6)
        self.clear_scene()


_ = (KERN, LAM)
