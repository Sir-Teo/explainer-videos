from __future__ import annotations

import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, grid_table, load,
                                   mono, tag_box)

# An illustrative Kripke structure: five states, their atomic propositions, and their successors (every state has
# one, so every path is infinite).
K_LABELS = {0: "p", 1: "p", 2: "p", 3: "q", 4: ""}
K_SUCC = {0: [1, 4], 1: [2], 2: [3, 0], 3: [3], 4: [4]}
K_POS = {0: (-5.4, 0.0), 1: (-3.8, 1.3), 2: (-2.2, 0.0), 3: (-0.6, 1.3), 4: (-5.4, -1.9)}


def ctl_tex(s: str) -> str:
    """One of the checker's formulas (unicode) as LaTeX: try0 becomes try with subscript 0."""
    s = re.sub(r"\b([a-z]+)(\d)\b", r"\\mathit{\1}_{\2}", s)
    s = re.sub(r"\bdeadlock\b", r"\\mathit{deadlock}", s)
    for a, b in (("¬", r"\neg "), ("∧", r" \wedge "), ("→", r" \rightarrow "), ("AG", r"\mathbf{AG}\,"),
                 ("AF", r"\mathbf{AF}\,"), ("EF", r"\mathbf{EF}\,"), ("EG", r"\mathbf{EG}\,")):
        s = s.replace(a, b)
    return s


def state_circle(props: str, name: str, r=0.36, color=GREY_B):
    c = Circle(radius=r, color=color, stroke_width=2.2, fill_color=BG, fill_opacity=1)
    t = MathTex(props.replace(",", r",\,") if props else r"\cdot", font_size=26, color=WHITE).move_to(c)
    n = MathTex(name, font_size=22, color=GREY_B)
    g = VGroup(c, t, n)
    g.circle, g.text, g.name = c, t, n
    return g


def self_loop(circle, direction, color=GREY_B):
    """A small arc leaving and re-entering a state on the side ``direction``."""
    r = circle.width / 2
    d = np.array(direction, dtype=float)
    d /= np.linalg.norm(d)
    centre = circle.get_center() + d * (r + 0.08)
    back = np.arctan2(-d[1], -d[0])
    arc = Arc(radius=0.22, start_angle=back + 1.0, angle=TAU - 2.0, arc_center=centre, color=color, stroke_width=2)
    arc.add_tip(tip_length=0.12)
    return arc


def kripke(scale=1.0, shift=ORIGIN, names=True):
    """The illustrative structure drawn: ``.nodes[i]``, ``.edges`` and the initial-state arrow."""
    nodes = {}
    for i, (x, y) in K_POS.items():
        g = state_circle(K_LABELS[i], f"s_{i}")
        g.move_to([x, y, 0])
        g.name.next_to(g.circle, LEFT if i in (0, 4) else (RIGHT if i in (2, 3) else UP), buff=0.1)
        if not names:
            g.name.set_opacity(0)
        nodes[i] = g
    edges = VGroup()
    for a, bs in K_SUCC.items():
        for b in bs:
            ca, cb = nodes[a].circle, nodes[b].circle
            if a == b:
                edges.add(self_loop(ca, UP if a == 3 else RIGHT))
            elif (a, b) == (2, 0):
                edges.add(CurvedArrow(ca.get_bottom() + LEFT * 0.1, cb.get_bottom() + RIGHT * 0.1, angle=-0.9,
                                      color=GREY_B, stroke_width=2, tip_length=0.14))
            else:
                edges.add(Arrow(ca.get_center(), cb.get_center(), buff=0.38, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.12))
    start = Arrow(nodes[0].circle.get_center() + UP * 1.0 + LEFT * 0.5, nodes[0].circle.get_center(), buff=0.38,
                  color=HEAD, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
    g = VGroup(*nodes.values(), edges, start)
    g.nodes, g.edges, g.start = nodes, edges, start
    g.scale(scale, about_point=ORIGIN).shift(shift)
    return g


def unroll(depth: int):
    """The computation tree from state 0: a list of (state, parent index, level)."""
    out = [(0, None, 0)]
    frontier = [0]
    for lev in range(1, depth + 1):
        nxt = []
        for k in frontier:
            for b in K_SUCC[out[k][0]]:
                out.append((b, k, lev))
                nxt.append(len(out) - 1)
        frontier = nxt
    return out


class Modelcheck(VoiceoverScene):
    def construct(self):
        self.card()
        self.kripke_()
        self.trees()
        self.fixpoints()
        self.peterson()
        self.fairness()
        self.counterexamples()
        self.explosion()

    def card(self):
        card = chapter_card(6, r"Model checking", r"Can a machine explore every behaviour?", lit=(1977, 1981, 2007),
                            extra=((1977, r"Pnueli: \ temporal logic"),
                                   (1981, r"Clarke and Emerson; \ Queille and Sifakis"),
                                   (2007, r"Turing Award: \ Clarke, \ Emerson, \ Sifakis")), part=PART)
        with self.voiceover("Chapter six. Model checking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kripke_(self):
        pt = load("peterson")
        head = label(r"Kripke structures", font_size=36).to_edge(UP, buff=0.3)
        K = kripke()
        ill = note(r"illustrative", font_size=16).next_to(K, DOWN, buff=0.3).align_to(K, LEFT)
        notes = VGroup(
            wrapped_label(r"\textbf{states}, \ one or more of them initial \ (the yellow arrow)", 5.6, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{transitions}: \ every state has a successor, \ so every run is an infinite path; "
                          r"\ a stuck state gets a loop to itself", 5.6, font_size=20, color=GREY_A),
            wrapped_label(r"\textbf{labels}: \ the atomic propositions true in each state, \ here $p$ and $q$", 5.6,
                          font_size=20, color=DATA),
            wrapped_label(rf"Peterson's lock for two processes, \ explored breadth first by our checker: \ "
                          rf"{pt['states']} states, \ {pt['edges']} transitions", 5.6, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 0.0, 0])
        with self.voiceover(
            "A model checker explores behaviour rather than text. <bookmark mark='a'/> Behaviour is a Kripke "
            "structure, after Saul Kripke's semantics for modal logic: a set of states, some of them initial. "
            "<bookmark mark='b'/> Transitions say which state can follow which; every state has a successor, so every"
            " run is an infinite path. <bookmark mark='c'/> Each state is labelled with the simple facts true in it. "
            "<bookmark mark='d'/> Peterson's lock from Part 33, explored breadth first by our checker, has twenty "
            "states and forty-six transitions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(n.circle) for n in K.nodes.values()], *[FadeIn(n.name) for n in K.nodes.values()],
                      GrowArrow(K.start), FadeIn(notes[0]), FadeIn(ill))
            vo.wait_until("b")
            self.play(Create(K.edges), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(*[FadeIn(n.text) for n in K.nodes.values()], FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def trees(self):
        head = label(r"Paths and computation trees", font_size=36).to_edge(UP, buff=0.3)
        T = unroll(4)
        levels = {}
        for k, (_, _, lev) in enumerate(T):
            levels.setdefault(lev, []).append(k)
        x0, x1, ytop, dy = -6.4, -0.6, 1.9, 1.05
        pos = {}
        for lev, ks in levels.items():                     # spread each level evenly under the root
            n = len(ks)
            for q, k in enumerate(ks):
                pos[k] = [x0 + (x1 - x0) * (q + 0.5) / n, ytop - lev * dy, 0]
        circ = {k: VGroup(Circle(radius=0.22, color=GREY_B, stroke_width=2, fill_color=BG, fill_opacity=1),
                          MathTex(K_LABELS[s] or r"\cdot", font_size=22)).move_to(pos[k])
                for k, (s, _, _) in enumerate(T)}
        edges = {k: Line(pos[p], pos[k], color=GREY_C, stroke_width=1.8, buff=0.22)
                 for k, (_, p, _) in enumerate(T) if p is not None}
        dots = VGroup(*[label(r"$\vdots$", font_size=20, color=GREY_C).next_to(circ[k], DOWN, buff=0.08)
                        for k in levels[4]])
        tree = VGroup(*circ.values(), *edges.values(), dots)

        def path_to(k):
            out = []
            while k is not None:
                out.append(k)
                k = T[k][1]
            return out[::-1]

        def light(ks, color):
            anims = [circ[k][0].animate.set_stroke(color=color, width=4) for k in ks]
            anims += [edges[k].animate.set_stroke(color=color, width=4) for k in ks if k in edges]
            return anims

        def reset():
            return ([c[0].animate.set_stroke(color=GREY_B, width=2) for c in circ.values()] +
                    [e.animate.set_stroke(color=GREY_C, width=1.8) for e in edges.values()])
        first_q = min((k for k, (s, _, _) in enumerate(T) if "q" in K_LABELS[s]), key=lambda k: T[k][2])
        all_p = [k for k in path_to(next(k for k in levels[4] if T[k][0] == 1))]   # s0 s1 s2 s0 s1: p all along
        never_q = path_to(next(k for k in levels[4] if T[k][0] == 4 and T[T[k][1]][0] == 4))
        not_p = [k for k, (s, _, _) in enumerate(T) if "p" not in K_LABELS[s]]
        ltl = VGroup(
            label(r"\textbf{LTL} \ (Pnueli, \ 1977): \ a property of each path", font_size=20, color=WHITE),
            MathTex(r"\mathbf{G}\,p \quad \mathbf{F}\,q \quad \mathbf{X}\,p \quad p\ \mathbf{U}\ q", font_size=30),
            label(r"always, \ eventually, \ next, \ until", font_size=17, color=GREY_B),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ctl = VGroup(label(r"\textbf{CTL} \ (Clarke and Emerson, \ 1981): \ $\mathbf{A}$ all paths, \ $\mathbf{E}$ "
                           r"some path", font_size=20, color=WHITE))
        forms = [(r"\mathbf{EF}\,q", r"some path reaches $q$", True, YES),
                 (r"\mathbf{AG}\,p", r"$p$ everywhere on every path", False, NO),
                 (r"\mathbf{AF}\,q", r"every path reaches $q$", False, NO),
                 (r"\mathbf{EG}\,p", r"some path keeps $p$ for ever", True, YES)]
        rows = VGroup(*[VGroup(MathTex(f, font_size=30, color=c), label(t, font_size=18, color=GREY_A),
                               label(r"holds" if ok else r"fails", font_size=18, color=c)).arrange(RIGHT, buff=0.3)
                        for f, t, ok, c in forms])
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        for r in rows:
            r[2].move_to([6.3, r.get_y(), 0])
        VGroup(ltl, ctl, rows).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, 0.0, 0])
        for r in rows:
            r[2].set_x(6.3)
        with self.voiceover(
            "Unroll the structure from its initial state, and you get a tree of every possible future. <bookmark "
            "mark='a'/> Amir Pnueli's linear temporal logic, of 1977, speaks of one path at a time: always, "
            "eventually, until. <bookmark mark='b'/> Clarke and Emerson's CTL, of 1981, adds path quantifiers: A for "
            "all paths, E for some. <bookmark mark='c'/> E F q: some path reaches q. True. <bookmark mark='d'/> A G "
            "p: p everywhere, on every path. False. <bookmark mark='e'/> A F q: every path reaches q. False: this one"
            " stays in the dead end. <bookmark mark='f'/> E G p: some path keeps p for ever. True, round the loop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tree))
            vo.wait_until("a")
            self.play(FadeIn(ltl))
            self.play(*light(all_p, HEAD), run_time=1.0)
            vo.wait_until("b")
            self.play(*reset(), FadeIn(ctl), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), *light(path_to(first_q), YES))
            vo.wait_until("d")
            self.play(*reset(), run_time=0.4)
            self.play(FadeIn(rows[1]), *light(not_p, NO))
            vo.wait_until("e")
            self.play(*reset(), run_time=0.4)
            self.play(FadeIn(rows[2]), *light(never_q, NO))
            vo.wait_until("f")
            self.play(*reset(), run_time=0.4)
            self.play(FadeIn(rows[3]), *light(all_p, YES))
        self.wait(0.4)
        self.clear_scene()

    def fixpoints(self):
        head = label(r"Checking CTL by fixpoints", font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"\mathbf{EF}\,q", r"\;\equiv\;", r"q \,\vee\, \mathbf{EX}\,\mathbf{EF}\,q", font_size=34),
            MathTex(r"Z", r"\;=\;", r"q \,\vee\, \mathbf{EX}\,Z", font_size=34),
            MathTex(r"\mathbf{EF}\,q", r"\;=\;", r"\mu Z.\ q \,\vee\, \mathbf{EX}\,Z", font_size=34, color=YES),
        ).arrange(DOWN, buff=0.28)
        for e in eqs:
            e.shift(RIGHT * (eqs[0][1].get_x() - e[1].get_x()))
        whys = VGroup(label(r"now, \ or after one step", font_size=17, color=GREY_A),
                      label(r"an equation in a set of states $Z$", font_size=17, color=GREY_A),
                      label(r"its least solution", font_size=17, color=YES))
        for w, e in zip(whys, eqs):
            w.next_to(e, DOWN, buff=0.05)
        VGroup(*[VGroup(e, w) for e, w in zip(eqs, whys)]).arrange(DOWN, buff=0.2).move_to([3.6, 1.85, 0])
        K = kripke(scale=0.95, shift=RIGHT * 0.3 + DOWN * 0.1)
        # Kleene iteration Z_0 = {} , Z_{k+1} = q-states ∪ predecessors of Z_k
        pred = {b: [a for a, bs in K_SUCC.items() if b in bs] for b in K_SUCC}
        Z, rounds = set(), []
        while True:
            nz = {s for s in K_SUCC if "q" in K_LABELS[s]} | {a for b in Z for a in pred[b]}
            if nz == Z:
                break
            rounds.append(sorted(nz - Z))
            Z = nz
        ztxt = VGroup(*[MathTex(rf"Z_{k + 1} = \{{" + r",\,".join(f"s_{s}" for s in sorted(
            set().union(*rounds[:k + 1]))) + r"\}", font_size=28, color=YES) for k in range(len(rounds))])
        ztxt.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.15), col_alignments="ll").move_to([3.6, -0.4, 0])
        stable = label(rf"after {len(rounds)} rounds nothing new: \ $s_4$, \ the dead end, \ never joins", font_size=19,
                       color=GREY_A).next_to(ztxt, DOWN, buff=0.2)
        foot = wrapped_label(r"$\mathbf{EG}$ is a greatest fixpoint; \ the rest follow by duality; \ each "
                             r"subformula costs one pass over states and transitions \ (Clarke, \ Emerson and Sistla, \ "
                             r"1986): \ linear time", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "CTL is checked backwards, over sets of states. <bookmark mark='a'/> E F q holds now, or one step later. "
            "<bookmark mark='b'/> That is an equation in an unknown set, and E F q is its least solution. <bookmark "
            "mark='c'/> Iterate: start with the q states, add every state with a successor in the set, and repeat. "
            "The set grows backwards along the transitions. <bookmark mark='d'/> After four rounds nothing changes, "
            "and the dead end never joins. <bookmark mark='e'/> E G is a greatest fixpoint, the rest follow by "
            "duality, and the whole check takes time linear in the structure, as Clarke, Emerson and Sistla showed in"
            " 1986."
        ) as vo:
            self.play(FadeIn(head), FadeIn(K))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(eqs[0].copy(), eqs[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(eqs[1].copy(), eqs[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            for k, new in enumerate(rounds):
                self.play(*[K.nodes[s].circle.animate.set_fill(YES, opacity=0.45) for s in new],
                          FadeIn(ztxt[k]), run_time=0.9)
                self.wait(0.6)
            vo.wait_until("d")
            self.play(FadeIn(stable), Indicate(K.nodes[4], color=NO))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        assert len(rounds) == 4
        self.wait(0.4)
        self.clear_scene()

    def peterson(self):
        pt = load("peterson")
        head = label(r"Peterson's lock, \ checked", font_size=36).to_edge(UP, buff=0.3)
        lines = ["process i (j is the other):", "  ncs:   idle, or",
                 "  flag[i] = 1", "  turn = j", "  await flag[j] == 0 or turn == i",
                 "  cs:    critical section", "  flag[i] = 0"]
        code = code_block(lines, size=18).move_to([-3.9, 0.6, 0])
        cap = label(r"each line one atomic step: \ the guarded commands our checker explores", font_size=18,
                    color=GREY_A).next_to(code, DOWN, buff=0.3).align_to(code, LEFT)
        meaning = {"AG ¬(cs0 ∧ cs1)": r"never both in the critical section",
                   "AG (try0 → AF cs0)": r"a waiting process always gets in",
                   "AG (try0 → EF cs0)": r"a waiting process can always get in",
                   "AG EF (ncs0 ∧ ncs1)": r"both can always return to idle",
                   "EF cs0": r"process 0 can get in at all",
                   "AG ¬deadlock": r"it never gets stuck"}
        rows = VGroup()
        for c in pt["ctl"]:
            f = MathTex(ctl_tex(c["formula"]), font_size=26, color=YES if c["holds"] else NO)
            m = label(meaning[c["formula"]], font_size=17, color=GREY_A)
            v = label(r"holds" if c["holds"] else r"fails", font_size=18, color=YES if c["holds"] else NO)
            rows.add(VGroup(f, m, v))
        for r in rows:
            r[1].next_to(r[0], DOWN, buff=0.06).align_to(r[0], LEFT)
        rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([2.9, -0.15, 0])
        for r in rows:
            r[2].move_to([6.4, r[0].get_y(), 0])
        bad = next(r for r, c in zip(rows, pt["ctl"]) if not c["holds"])
        ring = SurroundingRectangle(VGroup(bad[0], bad[1]), color=NO, buff=0.08, stroke_width=2)
        agree = pt["part33"]
        with self.voiceover(
            "Now a real algorithm. <bookmark mark='a'/> Peterson's lock: raise your flag, give the other process the "
            "turn, and wait until its flag is down or the turn is yours. <bookmark mark='b'/> Our checker answers six"
            " questions over all twenty states. Mutual exclusion holds; the lock never gets stuck; a waiting process "
            "can always get in. <bookmark mark='c'/> But a waiting process does not always get in. <bookmark "
            "mark='d'/> Part 33's checker, working with single loads and stores, agrees on mutual exclusion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(cap))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*code[2:5]), color=HEAD, scale_factor=1.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(Create(ring))
            vo.wait_until("d")
            p33 = label(rf"Part 33's checker, \ {agree['part33_states']} states of loads and stores: \ mutual "
                        rf"exclusion {'holds' if agree['part33_mutex'] else 'fails'} there too", font_size=18,
                        color=HEAD).to_edge(DOWN, buff=0.35)
            assert agree["agree"]
            self.play(FadeIn(p33))
        self.wait(0.4)
        self.clear_scene()

    def fairness(self):
        pt = load("peterson")
        ru = pt["response_unfair"]
        head = label(r"Liveness needs fairness", font_size=36).to_edge(UP, buff=0.3)
        prop = MathTex(r"\mathbf{G}\,(\mathit{try}_0 \rightarrow \mathbf{F}\,\mathit{cs}_0)", font_size=40).next_to(
            head, DOWN, buff=0.35)
        propl = label(r"LTL: \ whenever process 0 tries, \ it eventually gets in", font_size=19,
                      color=GREY_A).next_to(prop, DOWN, buff=0.12)
        steps = ru["prefix"]
        cards = VGroup()
        for st in steps:
            s = st["state"]
            box = RoundedRectangle(width=2.5, height=1.1, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.8,
                                   fill_color=BG, fill_opacity=1)
            txt = VGroup(mono(f"P0 {s['pc0']}  P1 {s['pc1']}", size=15, color=WHITE),
                         mono(f"flags {s['flag0']}{s['flag1']}  turn {s['turn']}", size=15, color=GREY_A)
                         ).arrange(DOWN, buff=0.12).move_to(box)
            cards.add(VGroup(box, txt))
        cards.arrange(RIGHT, buff=1.15).move_to([-0.6, -0.2, 0])
        arrows = VGroup()
        for k in range(1, len(steps)):
            a = Arrow(cards[k - 1].get_right(), cards[k].get_left(), buff=0.05, color=GREY_B, stroke_width=2,
                      max_tip_length_to_length_ratio=0.2)
            t = mono(steps[k]["action"], size=15, color=HEAD).next_to(a, UP, buff=0.06)
            arrows.add(VGroup(a, t))
        cyc = ru["cycle"]
        loop = self_loop(cards[-1][0], RIGHT, color=NO)
        loop_t = mono(cyc[0]["action"], size=15, color=NO).next_to(loop, RIGHT, buff=0.1)
        cards[-1][0].set_stroke(color=NO)
        cap = wrapped_label(r"a \textbf{lasso}: \ process 0 waits, \ the door is open, \ but the scheduler only ever runs "
                            r"process 1, \ which idles for ever", 12.0, font_size=19, color=NO).next_to(cards, DOWN,
                                                                                                    buff=0.45)
        weak = pt["response_weak"]
        assert all(w["holds"] for w in weak) and not ru["holds"]
        fix = wrapped_label(r"\textbf{weak fairness}: \ a step that stays enabled is eventually taken; \ assume it for "
                            r"each process, \ and the property holds for both", 12.0, font_size=19,
                            color=YES).next_to(cap, DOWN, buff=0.3)
        with self.voiceover(
            "That failure is about liveness: something good must eventually happen. <bookmark mark='a'/> Whenever "
            "process zero tries, it eventually gets in. <bookmark mark='b'/> The counterexample is a lasso, a stem "
            "followed by a cycle repeated for ever. Process zero raises its flag and gives away the turn. <bookmark "
            "mark='c'/> The door is open, but the scheduler only ever runs process one, which idles. <bookmark "
            "mark='d'/> No real scheduler is that unfair. Assume weak fairness, that a step which stays enabled is "
            "eventually taken, and the property holds for both processes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(prop), FadeIn(propl))
            vo.wait_until("b")
            self.play(FadeIn(cards[0]))
            for k in range(1, len(cards)):
                self.play(GrowArrow(arrows[k - 1][0]), FadeIn(arrows[k - 1][1]), FadeIn(cards[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(loop), FadeIn(loop_t), FadeIn(cap))
            self.play(Rotate(loop, angle=TAU, about_point=loop.get_center()), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(fix))
        self.wait(0.4)
        self.clear_scene()

    def counterexamples(self):
        pt = load("peterson")
        rf = load("raft")
        br = pt["broken"]
        head = label(r"Counterexamples", font_size=36).to_edge(UP, buff=0.3)
        t1 = label(rf"Peterson with the flag raised after the turn: \ {br['states']} states, \ mutual exclusion "
                   rf"fails", font_size=20, color=NO).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        cards = VGroup()
        for st in br["counterexample"]:
            s = st["state"]
            both = s["pc0"] == "cs" and s["pc1"] == "cs"
            box = RoundedRectangle(width=1.62, height=1.15, corner_radius=0.08, stroke_color=NO if both else GREY_C,
                                   stroke_width=2.2 if both else 1.5, fill_color=BG, fill_opacity=1)
            txt = VGroup(mono(st["action"] or "init", size=13, color=HEAD),
                         mono(f"{s['pc0']} {s['pc1']}", size=14, color=WHITE),
                         mono(f"f{s['flag0']}{s['flag1']} t{s['turn']}", size=13, color=GREY_A)
                         ).arrange(DOWN, buff=0.08).move_to(box)
            cards.add(VGroup(box, txt))
        cards.arrange(RIGHT, buff=0.18).next_to(t1, DOWN, buff=0.25).set_x(0)
        legend = label(r"each box: \ the step taken, \ where P0 and P1 are, \ flags and turn", font_size=17,
                       color=GREY_B).next_to(cards, DOWN, buff=0.15)
        t2 = label(rf"Raft-lite election \ (Part 38), \ 3 nodes, \ terms up to {rf['max_term']}: \ "
                   rf"{rf['states']:,} states, \ at most one leader per term", font_size=20,
                   color=YES).next_to(legend, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        t3 = label(rf"a voter that forgets its vote: \ {rf['bug']['states']:,} states, \ and two leaders in one "
                   rf"term after {rf['bug']['length']} steps", font_size=20, color=NO).next_to(t2, DOWN, buff=0.2)
        t3.align_to(t2, LEFT)
        acts = [s["action"] for s in rf["bug"]["counterexample"][1:]]
        chips = VGroup(*[tag_box(a, color=NO if a.startswith("Win") else KERN, size=16) for a in acts])
        chips.arrange(RIGHT, buff=0.32).next_to(t3, DOWN, buff=0.3).set_x(0)
        carr = VGroup(*[Arrow(chips[k].get_right(), chips[k + 1].get_left(), buff=0.03, color=GREY_B,
                              stroke_width=1.8, max_tip_length_to_length_ratio=0.35) for k in range(len(chips) - 1)])
        last = rf["bug"]["counterexample"][-1]["state"]
        leaders = [i for i, nd in enumerate(last["nodes"]) if nd["role"] == "leader"]
        term = last["nodes"][leaders[0]]["term"]
        fin = label(rf"nodes {leaders[0]} and {leaders[1]} are both leader of term {term}: \ node 0 voted twice in "
                    rf"one term", font_size=19, color=NO).next_to(chips, DOWN, buff=0.25)
        assert not br["mutex"] and rf["election_safety"] and not rf["bug"]["election_safety"]
        with self.voiceover(
            "A failed check comes with a counterexample. <bookmark mark='a'/> Give away the turn before raising the "
            "flag, and the checker finds a six-step path to both processes in the critical section. <bookmark "
            "mark='b'/> The search is breadth first, so no shorter path exists. <bookmark mark='c'/> The same tool "
            "checks a small Raft election from Part 38: with three nodes and two terms, never two leaders in one "
            "term. <bookmark mark='d'/> Plant a voter that forgets its vote, and two leaders appear in the same term "
            "after six steps."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in cards], lag_ratio=0.35), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(legend), Indicate(cards[-1], color=NO))
            vo.wait_until("c")
            self.play(FadeIn(t2))
            vo.wait_until("d")
            self.play(FadeIn(t3))
            self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.3), Create(carr), run_time=2.5)
            self.play(FadeIn(fin))
        self.wait(0.4)
        self.clear_scene()

    def explosion(self):
        ph = load("philosophers")
        naive = [r for r in ph["rows"] if not r["ordered"]]
        ordered = [r for r in ph["rows"] if r["ordered"]]
        head = label(r"State explosion", font_size=36).to_edge(UP, buff=0.3)
        chart = bar_chart([r["states"] for r in naive], [rf"$n = {r['n']}$" for r in naive], [HEAD] * len(naive),
                          height=3.4, bar_w=0.55, gap=0.3, fmt_=lambda v: f"{v:,.0f}", font_size=19, log=True)
        chart.move_to([-3.4, -0.3, 0])
        cap = label(r"reachable states of $n$ dining philosophers \ (log scale)", font_size=18,
                    color=GREY_A).next_to(chart, UP, buff=0.3)
        ratio = naive[-1]["states"] / naive[-2]["states"]
        assert all(r["EF_deadlock"] and r["counterexample_length"] == r["n"] for r in naive)
        assert not any(r["EF_deadlock"] for r in ordered)
        st = ph["starvation"]
        notes = VGroup(
            wrapped_label(rf"each philosopher multiplies the states by about {ratio:.1f}: \ exponential in the "
                          r"number of components", 5.4, font_size=20, color=HEAD),
            wrapped_label(r"$\mathbf{EF}\,\mathit{deadlock}$ holds for every $n$: \ the shortest path is $n$ steps, "
                          r"\ everyone picks up the left fork", 5.4, font_size=20, color=NO),
            wrapped_label(rf"take forks in a global order \ (Part 33) \ and no deadlock is reachable: \ "
                          rf"{ordered[-1]['states']:,} states for $n = {ordered[-1]['n']}$", 5.4, font_size=20,
                          color=YES),
            wrapped_label(rf"but philosopher 0 can still starve under weak fairness \ (n = {st['n']}); \ strong "
                          r"fairness rules it out", 5.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        assert not st["weak"]["holds"] and st["strong"]["holds"]
        with self.voiceover(
            "The catch is size. <bookmark mark='a'/> Dijkstra's dining philosophers: two have six states; eight have "
            "one thousand one hundred and fifty-four. Each philosopher multiplies the count by about two point four: "
            "the state explosion. <bookmark mark='b'/> For every size the checker finds the deadlock, everyone "
            "holding a left fork, in n steps. <bookmark mark='c'/> Take forks in a global order, Part 33's cure, and "
            "no deadlock is reachable. <bookmark mark='d'/> Yet a philosopher can still starve under weak fairness, "
            "though not under strong. To go further, we must stop listing states one by one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n))
                                    for b, v, n in zip(chart.bars, chart.vals, chart.names)], lag_ratio=0.35),
                      FadeIn(chart[0]), run_time=3)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, grid_table, KERN)
