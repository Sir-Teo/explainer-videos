from __future__ import annotations

import itertools

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, PART, PATH, SYMBOL, load, logic_tex, node_box


def clause_box(text: str, color=SYMBOL, font_size=30) -> VGroup:
    t = MathTex(logic_tex(text), font_size=font_size, color=WHITE if text != "□" else FAIL)
    box = RoundedRectangle(width=t.width + 0.35, height=t.height + 0.3, corner_radius=0.1, stroke_color=color,
                           stroke_width=2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def proof_layout(info, proof, x0=-5.6, width=11.2, y_top=2.0, dy=1.35, font_size=28):
    """Place the clauses of a refutation: the starting clauses on the top row, each derived clause one row below
    its lower parent, under the middle of its parents."""
    pos, boxes = {}, {}
    start = [i for i in proof if info[i]["parents"] is None]
    for k, i in enumerate(start):
        pos[i] = np.array([x0 + width * (k + 0.5) / len(start), y_top, 0])
    row = {i: 0 for i in start}
    for i in proof:
        if i in pos:
            continue
        parents = info[i]["parents"]
        row[i] = max(row[p] for p in parents) + 1
        x = sum(pos[p][0] for p in parents) / len(parents)
        pos[i] = np.array([x, y_top - dy * row[i], 0])
    for i in proof:
        col = FAIL if info[i]["text"] == "□" else (HEUR if info[i]["goal"] and info[i]["parents"] is None else SYMBOL)
        boxes[i] = clause_box(info[i]["text"], color=col, font_size=font_size).move_to(pos[i])
    # nudge apart boxes that overlap on the same row
    rows = {}
    for i in proof:
        rows.setdefault(row[i], []).append(i)
    for r, ids in rows.items():
        ids.sort(key=lambda i: boxes[i].get_x())
        for a, b in zip(ids, ids[1:]):
            gap = boxes[b].get_left()[0] - boxes[a].get_right()[0]
            if gap < 0.25:
                boxes[b].shift(RIGHT * (0.25 - gap))
    return boxes, row


def proof_edge(boxes, parent, child):
    """Connect clauses without drawing through an unrelated clause's label.

    Long derivations may skip a row. Route those edges through a clear vertical
    lane when a straight segment would cross another box, keeping the arrowhead
    at the actual conclusion rather than an intervening premise.
    """
    start, end = boxes[parent].get_bottom(), boxes[child].get_top()
    obstacles = [box for i, box in boxes.items() if i not in (parent, child)]

    def crosses(a, b, box):
        low, high = 0.0, 1.0
        for axis, bounds in enumerate(((box.get_left()[0] - 0.10, box.get_right()[0] + 0.10),
                                       (box.get_bottom()[1] - 0.10, box.get_top()[1] + 0.10))):
            delta = b[axis] - a[axis]
            if abs(delta) < 1e-10:
                if not bounds[0] <= a[axis] <= bounds[1]:
                    return False
            else:
                enter, leave = sorted((bound - a[axis]) / delta for bound in bounds)
                low, high = max(low, enter), min(high, leave)
                if low > high:
                    return False
        return True

    def clear(points):
        return not any(crosses(a, b, box) for a, b in zip(points, points[1:]) for box in obstacles)

    points = [start, end]
    if not clear(points):
        depart, approach = start + DOWN * 0.20, end + UP * 0.20
        lanes = {start[0], end[0]}
        for box in obstacles:
            lanes.update((box.get_left()[0] - 0.24, box.get_right()[0] + 0.24))
        candidates = []
        for x in sorted(lanes):
            if abs(x) > config.frame_width / 2 - 0.15:
                continue
            route = [start, depart, np.array([x, depart[1], 0]),
                     np.array([x, approach[1], 0]), approach, end]
            route = [p for k, p in enumerate(route) if k == 0 or np.linalg.norm(p - route[k - 1]) > 1e-8]
            if clear(route):
                length = sum(np.linalg.norm(b - a) for a, b in zip(route, route[1:]))
                candidates.append((length, route))
        if not candidates:
            raise ValueError(f"No unobstructed proof edge from {parent} to {child}")
        points = min(candidates, key=lambda item: item[0])[1]
    edge = Line(start, end, color=GREY_C, stroke_width=2).set_points_as_corners(points)
    return edge.add_tip(tip_length=0.10).set_z_index(-1)


def resolution_outcome_label(record, name):
    state = ("proof found" if record["found"] else "cap reached; no proof" if record["status"] == "limit"
             else "no new clauses; no proof")
    return name + r": \ " + state


class Logic(VoiceoverScene):
    def construct(self):
        self.card()
        self.truth()
        self.first_order()
        self.resolution()
        self.unify()
        self.explosion()

    def card(self):
        card = chapter_card(8, r"Logic and resolution", r"Can a machine reason from facts to conclusions?",
                            lit=(1972,), part=PART)
        with self.voiceover("Chapter eight. Logic and resolution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def truth(self):
        kb = VGroup(MathTex(r"\mathrm{Rain} \Rightarrow \mathrm{Wet}", font_size=34),
                    MathTex(r"\mathrm{Sprinkler} \Rightarrow \mathrm{Wet}", font_size=34),
                    MathTex(r"\mathrm{Rain} \lor \mathrm{Sprinkler}", font_size=34)).arrange(DOWN, buff=0.22)
        kb.move_to([-4.6, 1.4, 0])
        kbl = label(r"what we know", font_size=24, color=SYMBOL).next_to(kb, UP, buff=0.25)
        q = MathTex(r"\models\ \mathrm{Wet}\ ?", font_size=40, color=HEUR).next_to(kb, DOWN, buff=0.5)
        tag = note(r"illustrative").to_corner(DL, buff=0.25)
        # the truth table
        hdr = [r"\mathrm{R}", r"\mathrm{S}", r"\mathrm{W}", r"\text{KB}", r"\mathrm{Wet}"]
        rows = []
        for r, s, w in itertools.product([0, 1], repeat=3):
            kbv = ((not r) or w) and ((not s) or w) and (r or s)
            rows.append([r, s, w, int(kbv), w])
        tab = VGroup()
        head = VGroup(*[MathTex(h, font_size=30, color=GREY_A) for h in hdr])
        tab.add(head)
        for row in rows:
            tab.add(VGroup(*[MathTex(r"\mathrm{T}" if v else r"\mathrm{F}", font_size=30,
                                     color=(PATH if v else FAIL) if k >= 3 else WHITE) for k, v in enumerate(row)]))
        for i, rr in enumerate(tab):
            for j, m in enumerate(rr):
                m.move_to([1.0 + 1.1 * j, 2.6 - 0.58 * i, 0])
        hl = VGroup(*[SurroundingRectangle(tab[i + 1], color=PATH, buff=0.06, stroke_width=2.5)
                      for i, row in enumerate(rows) if row[3]])
        concl = label(r"in every row where the facts hold, \ Wet holds: \ entailed", font_size=24, color=PATH)
        concl.to_edge(DOWN, buff=0.35).set_x(2.6)
        flow = VGroup(node_box(r"what you know", SYMBOL, font_size=30), node_box(r"rules of inference", GREY_B,
                                                                                    font_size=30),
                      node_box(r"what follows", HEUR, font_size=30)).arrange(RIGHT, buff=1.0).move_to(UP * 0.2)
        flow.add(*[Arrow(flow[k].get_right(), flow[k + 1].get_left(), buff=0.12, color=GREY_B) for k in range(2)])
        cost = label(r"$n$ symbols: \ $2^n$ rows", font_size=24, color=FAIL).next_to(tab, LEFT, buff=0.6).shift(DOWN * 1.6)
        with self.voiceover(
            "The other great idea of the era was logic: write down what you know, and let the machine work out what follows. "
            "<bookmark mark='a'/> Three facts. If it rains, the grass is wet. If the sprinkler is on, the grass is wet. It is "
            "raining, or the sprinkler is on. <bookmark mark='b'/> Does it follow that the grass is wet? <bookmark mark='c'/> "
            "List every combination of true and false. <bookmark mark='d'/> In every row where all the facts hold, Wet holds "
            "too: the facts entail it. <bookmark mark='e'/> But n symbols make two to the n rows. We need to derive "
            "conclusions, not enumerate worlds."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(m) for m in (flow[0], flow[3], flow[1], flow[4], flow[2])],
                                               lag_ratio=0.4), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(flow), run_time=0.5)
            self.play(FadeIn(kbl), LaggedStart(*[FadeIn(k) for k in kb], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.12))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(h) for h in hl], lag_ratio=0.2), FadeIn(concl))
            vo.wait_until("e")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def first_order(self):
        ex = VGroup(MathTex(r"\forall x\ \forall y\ \forall z\ \ \mathrm{Parent}(x, y) \land \mathrm{Parent}(y, z) "
                            r"\Rightarrow \mathrm{Grandparent}(x, z)", font_size=34),
                    MathTex(r"\mathrm{Parent}(\mathrm{Anne}, \mathrm{Byron}) \qquad \mathrm{Parent}(\mathrm{Byron}, "
                            r"\mathrm{Ada})", font_size=34)).arrange(DOWN, buff=0.3).move_to(UP * 1.9)
        tag = note(r"illustrative").next_to(ex, DOWN, buff=0.15)
        cards = VGroup(
            history_card(1879, r"Gottlob Frege, \textit{Begriffsschrift}", r"quantifiers, \ variables, \ predicates: "
                         r"first-order logic", width=4.2, color=HIST, font_size=19),
            history_card(1930, r"Kurt G\"odel", r"completeness: \ every valid sentence has a proof", width=4.2,
                         color=HIST, font_size=19),
            history_card(1936, r"Church; \ Turing", r"but no program decides validity: \ a prover may search forever "
                         r"when the answer is no", width=4.2, color=FAIL, font_size=19),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.4)
        if cards.width > 13.4:
            cards.width = 13.4
        with self.voiceover(
            "Real knowledge needs more. First-order logic, from Gottlob Frege in 1879, adds objects, relations, and the words "
            "all and some: for all x, y and z, if x is a parent of y and y of z, then x is a grandparent of z. "
            "<bookmark mark='a'/> Kurt Gödel proved in 1930 that every valid first-order sentence has a proof, so a machine "
            "searching through proofs will find one. <bookmark mark='b'/> But no program can decide validity in general: if "
            "the answer is no, the search may never end."
        ) as vo:
            self.play(FadeIn(ex), FadeIn(tag), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def resolution(self):
        d = load("resolution")["prop"]
        info, proof = d["clauses"], d["proof"]
        rule = cmath(r"\frac{A \lor x \qquad B \lor \lnot x}{A \lor B}", font_size=44).move_to([4.8, 2.6, 0])
        rl = label(r"resolution \ (Robinson 1965)", font_size=22, color=SYMBOL).next_to(rule, DOWN, buff=0.15)
        boxes, row = proof_layout(info, proof, x0=-6.4, width=9.6, y_top=1.9, dy=1.3)
        derived = [i for i in proof if info[i]["parents"] is not None]
        lines = {}
        for i in derived:
            parents = info[i]["parents"]
            lines[i] = VGroup(*[proof_edge(boxes, p, i) for p in parents])
        start = [i for i in proof if info[i]["parents"] is None]
        neg = [i for i in start if info[i]["goal"]]
        note1 = label(r"add the negated goal; \\ derive the empty clause $\square$: \\ a contradiction", font_size=22,
                      color=HEUR).move_to([4.8, 0.4, 0])
        sound = label(r"resolution plus factoring: \\ refutation-complete without a resource cap",
                      font_size=22, color=PATH).move_to([4.8, -1.6, 0])
        tag = note(r"computed: \ our resolution prover").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 1965 Alan Robinson gave machines a resolution rule for automated deduction. <bookmark mark='a'/> Write every "
            "fact as a clause, an or of literals. If one clause contains x and another not x, resolve them: at least one of the "
            "rest must hold. <bookmark mark='b'/> To prove a goal, add its negation, here: the grass is not wet, "
            "<bookmark mark='c'/> and resolve until you derive the empty clause, a contradiction. <bookmark mark='d'/> Not wet "
            "and the rain rule give no rain; not wet and the sprinkler rule give no sprinkler; rain or sprinkler, with no "
            "sprinkler, gives rain; rain against no rain leaves nothing. <bookmark mark='e'/> Robinson proved the method sound "
            "and refutation-complete. First-order clauses also need factoring: unify same-sign literals within one clause. "
            "Without a resource cap, resolution and factoring can derive the empty clause whenever the clauses are inconsistent. "
            "Our bounded run can stop without an answer."
        ) as vo:
            self.play(Write(rule), FadeIn(rl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(boxes[i]) for i in start if i not in neg], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(*[FadeIn(boxes[i], shift=DOWN * 0.15) for i in neg])
            vo.wait_until("c")
            self.play(FadeIn(note1))
            vo.wait_until("d")
            for i in derived:
                self.play(Create(lines[i]), FadeIn(boxes[i], shift=DOWN * 0.1), run_time=0.9)
                self.wait(0.6)
            vo.wait_until("e")
            self.play(FadeIn(sound))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unify(self):
        d = load("resolution")["fol"]
        info, proof = d["clauses"], d["proof"]
        boxes, row = proof_layout(info, proof, x0=-6.6, width=13.2, y_top=1.8, dy=1.45, font_size=24)
        allb = VGroup(*boxes.values())
        if allb.width > 13.4:  # the starting clauses are long: shrink the whole proof to fit the frame
            top = allb.get_top()[1]
            allb.scale(13.4 / allb.width).set_x(0)
            allb.shift(UP * (top - allb.get_top()[1]))
        derived = [i for i in proof if info[i]["parents"] is not None]
        lines, subs = {}, {}
        for i in derived:
            parents = info[i]["parents"]
            lines[i] = VGroup(*[proof_edge(boxes, p, i) for p in parents])
            sub = info[i]["sub"]
            if sub:
                pairs = sorted({(k.split("_")[0], v) for k, v in sub.items() if v[:1].isupper()})
                tex = r"\{" + r",\ ".join(rf"{k}/\mathrm{{{v}}}" for k, v in pairs) + r"\}"
                subs[i] = MathTex(tex, font_size=24, color=FCOL).next_to(boxes[i], RIGHT, buff=0.25)
        start = [i for i in proof if info[i]["parents"] is None]
        head = label(r"first order: \ unification finds the substitution that makes two literals match",
                     font_size=26, color=FCOL).to_edge(UP, buff=0.3)
        prolog = history_card(1972, r"Alain Colmerauer \& Philippe Roussel: \ Prolog", r"resolution on Horn clauses, "
                              r"as a programming language \ (with Robert Kowalski)", width=5.4, color=HIST,
                              font_size=19).to_corner(DR, buff=0.25)
        with self.voiceover(
            "With variables, resolution needs one more step. <bookmark mark='a'/> The negated goal can be resolved with the rule "
            "only after the rule's variables are matched to Anne and Ada. Finding the most general such substitution is "
            "unification, the other half of Robinson's paper. <bookmark mark='b'/> Two more steps, and the empty clause. "
            "<bookmark mark='c'/> Restrict clauses to at most one positive literal, and resolution becomes a programming "
            "language: Prolog, created by Alain Colmerauer and Philippe Roussel in Marseille in 1972, with Robert Kowalski's "
            "theory behind it."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(boxes[i]) for i in start], lag_ratio=0.2))
            vo.wait_until("a")
            i0 = derived[0]
            self.play(Create(lines[i0]), FadeIn(boxes[i0], shift=DOWN * 0.1), *([FadeIn(subs[i0])] if i0 in subs else []))
            vo.wait_until("b")
            for i in derived[1:]:
                self.play(Create(lines[i]), FadeIn(boxes[i], shift=DOWN * 0.1), *([FadeIn(subs[i])] if i in subs else []),
                          run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(prolog, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def explosion(self):
        r = load("resolution")
        sat, sos = r["explode_saturate"], r["explode_support"]
        facts = r["facts"]
        g = VGroup(*[label(rf"$\mathrm{{{a}}}$ is a parent of $\mathrm{{{b}}}$", font_size=20, color=GREY_A)
                     for _, a, b in facts]).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([-4.6, 0.6, 0])
        rules = VGroup(label(r"a parent is an ancestor", font_size=20, color=SYMBOL),
                       label(r"a parent of an ancestor is an ancestor", font_size=20, color=SYMBOL),
                       label(r"nobody is their ancestor's ancestor", font_size=20, color=SYMBOL))
        rules.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(g, DOWN, buff=0.3).align_to(g, LEFT)
        goal = label(r"goal: \ Anne is an ancestor of Flora", font_size=22, color=HEUR).next_to(g, UP, buff=0.3)
        goal.align_to(g, LEFT)
        bars = bar_like([(resolution_outcome_label(sat, "all pairs"), sat["made"], FAIL),
                         (resolution_outcome_label(sos, "set of support"), sos["made"], PATH)])
        bars.move_to([2.6, 0.6, 0])
        cap = label(r"clauses recorded at stopping \\ (including input clauses)",
                    font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.3)
        tag = note(r"computed: \ our prover; \ illustrative facts").to_corner(DR, buff=0.2)
        lesson = label(r"complete is not the same as fast: \ the strategy is everything", font_size=26, color=FCOL)
        lesson.next_to(cap, DOWN, buff=0.6)
        lesson.set_x(min(lesson.get_x(), 6.9 - lesson.width / 2))
        if sat["found"]:
            sat_verdict = (f"The level-by-level search found a refutation after {sat['made']:,} recorded clauses; "
                             f"the proof uses {sat['proof_len']} clauses.")
        elif sat["status"] == "limit":
            sat_verdict = (f"The level-by-level search reached its cap of {sat['clause_cap']:,} recorded clauses without finding a refutation. "
                             "That leaves the goal unresolved by this run.")
        else:
            sat_verdict = (f"The level-by-level search stopped with no new clauses after {sat['made']:,} recorded clauses, "
                             "without finding a refutation.")
        if sos["found"]:
            sos_verdict = (f"The set-of-support search found a refutation after {sos['made']:,} recorded clauses; "
                             f"the proof uses {sos['proof_len']} clauses.")
        elif sos["status"] == "limit":
            sos_verdict = (f"The set-of-support search reached its cap of {sos['clause_cap']:,} recorded clauses without finding a refutation. "
                             "That leaves the goal unresolved by this run.")
        else:
            sos_verdict = (f"The set-of-support search stopped with no new clauses after {sos['made']:,} recorded clauses, "
                             "without finding a refutation.")
        with self.voiceover(
            "Completeness is not efficiency. <bookmark mark='a'/> Give the prover eight family facts and three rules, and ask "
            "whether Anne is an ancestor of Flora, four generations away. <bookmark mark='b'/> " + sat_verdict +
            " <bookmark mark='c'/> The set-of-support strategy, from Larry Wos and colleagues in 1965, resolves only pairs "
            "involving the negated goal or its descendants. " + sos_verdict + " <bookmark mark='d'/> Provers live or die by such "
            "strategies. Resolution's descendants, like Vampire and E, still compete every year, and proof assistants call on "
            "them to fill in routine steps."
        ) as vo:
            self.play(FadeIn(goal), FadeIn(g), FadeIn(rules), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()


def bar_like(items, width=5.0, height=0.45, font_size=22) -> VGroup:
    vmax = max(v for _, v, _ in items)
    out = VGroup()
    for txt, v, col in items:
        nm = label(txt, font_size=font_size - 2, color=col)
        bar = Rectangle(width=max(width * v / vmax, 0.05), height=height, stroke_width=0, fill_color=col,
                        fill_opacity=0.85)
        val = MathTex(f"{v:,}".replace(",", "{,}"), font_size=font_size + 4, color=col)
        row = VGroup(nm, VGroup(bar, val.next_to(bar, RIGHT, buff=0.15)))
        row[1].next_to(nm, DOWN, buff=0.12, aligned_edge=LEFT)
        out.add(row)
    return out.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
