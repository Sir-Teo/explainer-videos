from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load

# opinion colours: A blue, B purple; strong agents filled, weak ones hollow
CA, CB = DATA, LAM
STYLE = {"A": (CA, 0.9), "a": (CA, 0.12), "B": (CB, 0.9), "b": (CB, 0.12)}


def agent(state=None, r=0.17, letter=None, size=24, color=GREY_B, fill=0.0, dashed=False):
    """An agent: a circle styled by its state (A, a, B, b), or plain; optionally with a letter inside."""
    if state in STYLE:
        color, fill = STYLE[state]
    c = Circle(radius=r, stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    if dashed:
        c = DashedVMobject(c, num_dashes=12)
    g = VGroup(c)
    if letter is not None:
        g.add(MathTex(letter, font_size=size, color=WHITE if fill > 0.5 else color).move_to(c))
    return g


def restyle(a, state):
    color, fill = STYLE[state]
    return a[0].animate.set_fill(color, opacity=fill).set_stroke(color)


def scatter(n, x0, x1, y0, y1, dmin, seed):
    rng = random.Random(seed)
    pts = []
    while len(pts) < n:
        p = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        if all(np.linalg.norm(p - q) >= dmin for q in pts):
            pts.append(p)
    return pts


def rule_row(left, right, tag, tag_color=GREY_A, r=0.27, size=24):
    """A rule drawn with agents: [(state, letter, dashed)] + ... -> ..., with a short tag after it."""
    def side(items):
        g = VGroup()
        for k, (st, let, *rest) in enumerate(items):
            if k:
                g.add(MathTex(r"+", font_size=28, color=GREY_B))
            if isinstance(st, str) and st in STYLE:
                g.add(agent(st, r=r, letter=let, size=size))
            else:
                g.add(agent(None, r=r, letter=let, size=size, color=st, fill=rest[0] if rest else 0.0,
                            dashed=bool(rest[1]) if len(rest) > 1 else False))
        return g.arrange(RIGHT, buff=0.12)
    row = VGroup(side(left), MathTex(r"\rightarrow", font_size=30, color=GREY_B), side(right),
                 label(tag, font_size=18, color=tag_color)).arrange(RIGHT, buff=0.22)
    return row


def stacked(rows, whys, buff=0.22):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


class Population(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.rules()
        self.run()
        self.timing()
        self.approx()
        self.power()

    def card(self):
        card = chapter_card(10, r"Population protocols", r"What can a crowd of anonymous, \ forgetful agents "
                            r"compute?", lit=(2004, 2006),
                            extra=((2004, r"Angluin et al.: \ population protocols"),
                                   (2006, r"the semilinear predicates")), part=PART)
        with self.voiceover("Chapter ten. Population protocols."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the model
    def model(self):
        head = label(r"Agents that meet in pairs", font_size=36).to_edge(UP, buff=0.3)
        n = 20
        pts = scatter(n, -6.1, -1.0, -2.6, 2.2, 0.75, seed=4)
        ags = VGroup(*[agent(None, r=0.17, color=GREY_B).move_to(p) for p in pts])
        rng = random.Random(5)
        inf = {0}
        seq = []
        while len(inf) < n:
            i, j = rng.sample(range(n), 2)
            new = (i in inf) != (j in inf)
            if i in inf or j in inf:
                inf |= {i, j}
            seq.append((i, j, new))

        def hit(k):
            return ags[k][0].animate.set_fill(HEAD, opacity=0.9).set_stroke(HEAD)
        ill = note(r"illustrative: \ an epidemic among 20 agents", font_size=16).next_to(
            VGroup(*ags), DOWN, buff=0.2)
        W = 5.6
        notes = VGroup(
            wrapped_label(r"\textbf{anonymous} agents, \ each a \textbf{finite-state} machine: \ no identifiers, \ "
                          r"and the number of states does not grow with $n$", W, font_size=19, color=WHITE),
            wrapped_label(r"a random scheduler picks two agents; \ both update by one fixed rule, \ "
                          r"$(q, r) \mapsto \delta(q, r)$", W, font_size=19, color=DATA),
            wrapped_label(r"\textbf{parallel time}: \ interactions divided by $n$", W, font_size=19, color=GREY_A),
            wrapped_label(r"an epidemic, \ $(1, 0) \mapsto (1, 1)$: \ everyone is told in logarithmic parallel "
                          r"time", W, font_size=19, color=HEAD),
            wrapped_label(r"no agent knows the computation is over: \ the outputs need only \textbf{stabilise} to the "
                          r"right answer", W, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.75, -0.1, 0])
        with self.voiceover(
            "The last model is the most minimal of all. In 2004 Dana Angluin, James Aspnes, Zoë Diamadi, Michael "
            "Fischer and René Peralta imagined tiny sensors carried by a flock of birds. <bookmark mark='a'/> The "
            "agents are anonymous, and each is a finite-state machine whose number of states does not grow with "
            "the population. <bookmark mark='b'/> A random scheduler picks two agents at a time, and both update "
            "by one fixed rule. <bookmark mark='c'/> Time is counted in parallel time: interactions divided by n. "
            "<bookmark mark='d'/> The simplest protocol is an epidemic. One informed agent informs whoever it "
            "meets, and everyone knows in logarithmic parallel time. <bookmark mark='e'/> No agent ever learns "
            "that the computation is over; the answer only has to stabilise."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(a, scale=0.6) for a in ags], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            for i, j, _ in seq[:3]:
                ln = Line(pts[i], pts[j], color=GREY_A, stroke_width=2.5, buff=0.17)
                self.play(Create(ln), run_time=0.3)
                self.play(FadeOut(ln), run_time=0.2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), hit(0), FadeIn(ill))
            shown = 0
            for i, j, new in seq[:14]:
                ln = Line(pts[i], pts[j], color=HEAD if new else GREY_A, stroke_width=2.5, buff=0.17)
                anims = [hit(i), hit(j)] if new else []
                self.play(Create(ln), *anims, run_time=0.35)
                self.play(FadeOut(ln), run_time=0.12)
                shown += 1
            rest = seq[shown:]
            for b in range(0, len(rest), max(1, len(rest) // 5)):
                chunk = rest[b:b + max(1, len(rest) // 5)]
                ks = {k for i, j, new in chunk if new for k in (i, j)}
                if ks:
                    self.play(*[hit(k) for k in ks], run_time=0.4)
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ four-state majority
    def rules(self):
        head = label(r"Exact majority with four states", font_size=36).to_edge(UP, buff=0.3)
        r1 = rule_row([("A", r"A"), ("B", r"B")], [("a", r"a"), ("b", r"b")], r"cancel", NO)
        r2 = rule_row([("A", r"A"), ("b", r"b")], [("A", r"A"), ("a", r"a")], r"convert", CA)
        r3 = rule_row([("B", r"B"), ("a", r"a")], [("B", r"B"), ("b", r"b")], r"convert", CB)
        rules = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([-3.7, 0.55, 0])
        key = wrapped_label(r"filled: \ strong opinions $A$, $B$; \ hollow: \ weak $a$, $b$; \ every agent "
                            r"outputs its letter's side", 5.6, font_size=18, color=GREY_A).next_to(
            rules, DOWN, buff=0.45).align_to(rules, LEFT)
        fs = 28
        rows = [MathTex(r"\Delta(\#A - \#B)", r"=", r"(-1) - (-1)", r"=", r"0", font_size=fs),
                MathTex(r"\Delta(\#A - \#B)", r"=", r"0", font_size=fs),
                MathTex(r"\#A - \#B", r"=", r"m", font_size=fs),
                MathTex(r"m > 0", r"\Rightarrow", r"\#A \ge m > 0", font_size=fs),
                MathTex(r"\#B", r"\to", r"0", r",\ \ ", r"\#b", r"\to", r"0", font_size=fs)]
        rows[4].set_color(YES)
        whys = [label(r"cancelling removes one $A$ and one $B$", font_size=18, color=GREY_B),
                label(r"converting changes only weak agents", font_size=18, color=GREY_B),
                label(r"the initial margin, \ for ever", font_size=18, color=HEAD),
                label(r"strong $A$ never runs out", font_size=18, color=GREY_B),
                label(r"$A$ and $B$ keep meeting until $B$ is gone; \ then $A$ converts every $b$", font_size=18,
                      color=YES)]
        col = stacked(rows, whys, buff=0.2).move_to([3.4, 0.45, 0]).align_to([0.2, 0, 0], LEFT)
        foot = wrapped_label(r"Draief and Vojnovi\'c \ (2012); \ Mertzios et al. \ (2014): \ always right for any "
                             r"margin; \ but on a tie the strong agents all cancel and the population never settles",
                             12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Can such agents decide which of two opinions is in the majority? <bookmark mark='a'/> Four states "
            "suffice: strong opinions A and B, and weak ones, small a and small b. When two strong opposite "
            "opinions meet, both become weak. <bookmark mark='b'/> A strong agent converts a weak agent of the "
            "other side. <bookmark mark='c'/> Watch the difference between the strong counts. Cancelling removes "
            "one strong A and one strong B, <bookmark mark='d'/> and converting touches only weak agents, "
            "<bookmark mark='e'/> so strong A minus strong B is the initial margin, for ever. "
            "<bookmark mark='f'/> If A started ahead, strong As never run out; strong Bs must, since while both "
            "remain they keep meeting; and then every weak b is converted. Everyone outputs A. "
            "<bookmark mark='g'/> It is always right, though a tie never settles."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r1), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(r2), FadeIn(r3))
            vo.wait_until("c")
            self.play(Indicate(r1, color=NO, scale_factor=1.05), FadeIn(col[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(whys[4]))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the run
    def run(self):
        m = load("majority")["run"]
        tr = [{"A": (m["n"] + m["margin"]) // 2, "B": m["n"] - (m["n"] + m["margin"]) // 2, "a": 0, "b": 0}]
        tr += m["trace"]
        n, T = m["n"], len(tr) - 1
        head = label(rf"{n} agents, \ {tr[0]['A']} against {tr[0]['B']}", font_size=36).to_edge(UP, buff=0.3)
        side = int(round(math.sqrt(n)))
        sp = 0.36
        ags = VGroup(*[agent(None, r=0.13).move_to([(k % side) * sp, -(k // side) * sp, 0]) for k in range(n)])
        ags.move_to([-4.3, 0.3, 0])
        rng = random.Random(2)
        states = ["A"] * tr[0]["A"] + ["B"] * tr[0]["B"]
        rng.shuffle(states)

        def step(old, new):
            """Change agents' states so the counts go from old to new (A -> a, B -> b, then weak swaps)."""
            ch = {}
            for strong, weak in (("A", "a"), ("B", "b")):
                idx = [k for k, s in enumerate(states) if s == strong]
                for k in rng.sample(idx, old[strong] - new[strong]):
                    states[k] = weak
                    ch[k] = weak
            a_now = states.count("a")
            src, dst = ("b", "a") if a_now < new["a"] else ("a", "b")
            idx = [k for k, s in enumerate(states) if s == src]
            for k in rng.sample(idx, abs(new["a"] - a_now)):
                states[k] = dst
                ch[k] = dst
            return ch
        tlab = label(r"parallel time 0", font_size=22, color=HEAD).next_to(ags, UP, buff=0.25)
        A = axes([0, 60, 10], [0, n, 25], x_length=5.4, y_length=3.3, x_label=r"parallel time", y_label=r"agents",
                 xticks=[0, 20, 40, 60], yticks=[0, 50, 100])
        A.move_to([3.15, 0.35, 0])
        ax = A.ax
        sty = {"A": (CA, 3.5, 1.0), "a": (CA, 2.4, 0.75), "b": (CB, 2.4, 0.75), "B": (CB, 3.5, 1.0)}
        marks = [0, 1, 2, 3, 4, 5, 7, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, T]
        segs = []
        for u, v in zip(marks, marks[1:]):
            g = VGroup()
            for s, (c, w, o) in sty.items():
                g.add(VMobject(color=c, stroke_width=w, stroke_opacity=o).set_points_as_corners(
                    [ax.c2p(t, tr[t][s]) for t in range(u, v + 1)]))
            segs.append(g)
        legend = VGroup()
        for s, nm in (("A", r"strong $A$"), ("a", r"weak $a$"), ("b", r"weak $b$"), ("B", r"strong $B$")):
            c, w, o = sty[s]
            legend.add(VGroup(agent(s, r=0.11), Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=w, stroke_opacity=o),
                              label(nm, font_size=18, color=c)).arrange(RIGHT, buff=0.12))
        legend.arrange(RIGHT, buff=0.55).move_to([0, -2.05, 0])
        pairs = []
        for t in tr:
            if not pairs or pairs[-1] != (t["A"], t["B"]):
                pairs.append((t["A"], t["B"]))
        inv = MathTex(r"\#A - \#B:\ \ " + r" = ".join(f"{a} - {b}" for a, b in pairs) + rf" = {m['margin']}",
                      font_size=26, color=HEAD)
        if inv.width > 12.6:
            inv.width = 12.6
        inv.move_to([0, -2.7, 0])
        tB = next(t for t in range(len(tr)) if tr[t]["B"] == 0)
        ok = m["correct"] == 1.0 and tr[-1]["b"] == 0 and tr[-1]["B"] == 0
        fin = label(rf"strong $B$ gone by $t = {tB}$; \ " + (rf"every agent outputs $A$ at $t = {T}$" if ok else
                                                           r"the run did not finish"),
                    font_size=19, color=YES if ok else NO).move_to([0, -3.3, 0])
        src = note(r"theory.py: \ one run, \ random pairs; \ agents' positions illustrative", font_size=16).next_to(
            A, UP, buff=0.05).align_to(A, RIGHT)
        with self.voiceover(
            "Here is our instrument's run: a hundred agents, fifty-two for A and forty-eight for B, a margin of "
            "four. <bookmark mark='a'/> Strong agents are filled, weak ones hollow. Within a few units of "
            "parallel time most strong opinions have cancelled. <bookmark mark='b'/> The strong counts fall "
            "together, and their difference never moves: twenty-seven minus twenty-three, down to four minus "
            "zero. <bookmark mark='c'/> The last strong B is gone by time twenty. <bookmark mark='d'/> Then four "
            "strong As must find every remaining weak b, and that slow mop-up takes most of the time. After "
            "fifty-eight units, every agent says A."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(src), FadeIn(legend),
                      LaggedStart(*[FadeIn(a) for a in ags], lag_ratio=0.01))
            self.play(*[restyle(ags[k], s) for k, s in enumerate(states)], FadeIn(tlab))
            vo.wait_until("a")
            for q, (u, v) in enumerate(zip(marks, marks[1:])):
                ch = step(tr[u], tr[v])
                new_t = label(rf"parallel time {v}", font_size=22, color=HEAD).move_to(tlab)
                self.play(Create(segs[q]), Transform(tlab, new_t), *[restyle(ags[k], s) for k, s in ch.items()],
                          run_time=0.9 if v <= 5 else 0.6)
                if v == 5:
                    vo.wait_until("b")
                    self.play(FadeIn(inv))
                if v == tB:
                    vo.wait_until("c")
                    self.play(Indicate(tlab, color=YES))
                    vo.wait_until("d")
            self.play(FadeIn(fin))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ how long
    def timing(self):
        sc = load("majority")["scaling"]
        mg = sc[0]["margin"]
        head = label(r"Why so slow: \ the mop-up", font_size=36).to_edge(UP, buff=0.3)
        fs = 27
        rows = [MathTex(r"\Pr[\text{a given } b \text{ meets an } A]", r"=", r"\frac{2m}{n(n-1)}", font_size=fs),
                MathTex(r"\Pr[\text{some } b \text{ converts}]", r"=", r"\frac{2mk}{n(n-1)}", font_size=fs),
                MathTex(r"\mathbb{E}[\text{interactions}]", r"=", r"\sum_{k=1}^{K} \frac{n(n-1)}{2mk}", font_size=fs),
                MathTex(r"\text{parallel time}", r"\approx", r"\frac{n}{2m}\,\ln n", font_size=fs)]
        rows[3][2].set_color(HEAD)
        whys = [label(r"in one interaction, \ with $m$ strong $A$ left", font_size=18, color=GREY_B),
                label(r"with $k$ weak $b$ left", font_size=18, color=GREY_B),
                label(r"wait for each in turn", font_size=18, color=GREY_B),
                label(r"divide by $n$; \ a harmonic sum is about $\ln n$", font_size=18, color=HEAD)]
        col = stacked(rows, whys, buff=0.25).move_to([-3.3, 0.35, 0]).align_to([-6.5, 0, 0], LEFT)
        meas = [r["parallel_time_mean"] for r in sc]
        est = [r["n"] / (2 * mg) * math.log(r["n"]) for r in sc]
        ch = bar_chart(meas, [rf"$n = {r['n']}$" for r in sc], [KERN] * len(sc), height=2.7, bar_w=0.62, gap=0.45,
                       vmax=max(meas + est), fmt_=lambda v: f"{v:.0f}", font_size=18)
        ch.move_to([4.25, 0.25, 0])
        ticks = VGroup(*[Line(b.get_bottom() + UP * b.height * e / v + LEFT * 0.38,
                              b.get_bottom() + UP * b.height * e / v + RIGHT * 0.38, color=WHITE, stroke_width=3)
                         for b, e, v in zip(ch.bars, est, meas)])
        ct = label(rf"measured parallel time, \ margin {mg}", font_size=19, color=KERN).next_to(ch, UP, buff=0.25)
        tl = wrapped_label(r"white: \ $\frac{n}{2m}\ln n$, \ the mop-up alone", 4.4, font_size=18,
                           color=GREY_A).next_to(ch, DOWN, buff=0.2)
        ok = all(r["correct"] == 1.0 for r in sc)
        src = note(r"theory.py, \ 20 runs each" + (r", \ all correct" if ok else r", \ some wrong"),
                   font_size=16).next_to(tl, DOWN, buff=0.08)
        foot = wrapped_label(r"with more states, \ much faster: \ Doty et al. \ (2021): \ exact majority in "
                             r"$O(\log n)$ parallel time with $O(\log n)$ states", 12.4, font_size=19,
                             color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why so slow? Look at the mop-up. <bookmark mark='a'/> With m strong As left, a particular weak b "
            "meets one of them in a given interaction with probability two m over n times n minus one. "
            "<bookmark mark='b'/> With k weak bs left, some b converts with k times that probability. "
            "<bookmark mark='c'/> Waiting for each in turn gives a harmonic sum, <bookmark mark='d'/> and "
            "dividing by n gives about n over two m, times the natural logarithm of n. <bookmark mark='e'/> Our "
            "instrument ran margin two with fifty, a hundred, two hundred and four hundred agents: sixty-four, a "
            "hundred and thirty-six, two hundred and eighty-four and six hundred and seventy-three units, close "
            "to the estimate. <bookmark mark='f'/> More states make it far faster: in 2021 David Doty and "
            "colleagues reached logarithmic time with logarithmically many states."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(ct), FadeIn(ch[0]), FadeIn(ch.names))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v)) for b, v in
                                    zip(ch.bars, ch.vals)], lag_ratio=0.4), run_time=2.4)
            self.play(Create(ticks), FadeIn(tl), FadeIn(src))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ approximate majority
    def approx(self):
        head = label(r"Approximate majority in three states", font_size=36).to_edge(UP, buff=0.3)
        CX, CY, BL = DATA, LAM, GREY_B
        rows = VGroup(
            rule_row([(CX, r"x", 0.9), (CY, r"y", 0.9)], [(CX, r"x", 0.9), (BL, r"", 0.0, True)], r"", r=0.21,
                     size=22),
            rule_row([(CY, r"y", 0.9), (CX, r"x", 0.9)], [(CY, r"y", 0.9), (BL, r"", 0.0, True)], r"", r=0.21,
                     size=22),
            rule_row([(CX, r"x", 0.9), (BL, r"", 0.0, True)], [(CX, r"x", 0.9), (CX, r"x", 0.9)], r"", r=0.21,
                     size=22),
            rule_row([(CY, r"y", 0.9), (BL, r"", 0.0, True)], [(CY, r"y", 0.9), (CY, r"y", 0.9)], r"", r=0.21,
                     size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tags = VGroup(label(r"the responder of an opposite opinion goes blank", font_size=18, color=NO),
                      label(r"an opinion recruits a blank", font_size=18, color=YES))
        tags[0].next_to(VGroup(rows[0], rows[1]), RIGHT, buff=0.3)
        tags[1].next_to(VGroup(rows[2], rows[3]), RIGHT, buff=0.3)
        rules = VGroup(rows, tags).move_to([3.0, 1.55, 0])
        if rules.get_right()[0] > 6.7:
            rules.shift(LEFT * (rules.get_right()[0] - 6.7))
        # an illustrative run, 16 agents, 10 x against 6 y
        n = 16
        C = np.array([-4.3, -0.55, 0])
        P = [C + 1.75 * np.array([math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0])
             for k in range(n)]
        init = ["x"] * 10 + ["y"] * 6

        def simulate(seed):
            r = random.Random(seed)
            st = init[:]
            r.shuffle(st)
            start = st[:]
            seq = []
            while len(set(st)) > 1 and len(seq) < 400:
                i, j = r.sample(range(n), 2)
                a, b = st[i], st[j]
                if {a, b} == {"x", "y"}:
                    st[j] = "-"
                elif b == "-" and a != "-":
                    st[j] = a
                else:
                    seq.append((i, j, None))
                    continue
                seq.append((i, j, st[j]))
            return start, seq, st
        seed = 0
        while True:
            start, seq, end = simulate(seed)
            if set(end) == {"x"} and len(seq) <= 140:
                break
            seed += 1
        col = {"x": CX, "y": CY, "-": BL}

        def ag(s):
            return Circle(radius=0.2, stroke_color=col[s], stroke_width=2.2, fill_color=col[s],
                          fill_opacity=0.9 if s != "-" else 0.0)
        ags = VGroup(*[ag(s).move_to(P[k]) for k, s in enumerate(start)])

        def to(k, s):
            return ags[k].animate.set_fill(col[s], opacity=0.9 if s != "-" else 0.0).set_stroke(col[s])
        ill = note(r"illustrative: \ 10 $x$ against 6 $y$", font_size=16).next_to(VGroup(*ags), DOWN, buff=0.2)
        W = 6.0
        notes = VGroup(
            wrapped_label(r"Angluin, \ Aspnes and Eisenstat \ (2008): \ with high probability it converges in "
                          r"$O(\log n)$ parallel time, \ to the initial majority when the margin exceeds about "
                          r"$\sqrt{n}\,\log n$", W, font_size=19, color=WHITE),
            wrapped_label(r"fast, \ but it can err on a close vote; \ the four-state protocol is always right, \ "
                          r"but slow", W, font_size=19, color=HEAD),
            wrapped_label(r"Cardelli and Csik\'asz-Nagy \ (2012): \ the switch that drives the cell cycle has the "
                          r"same structure", W, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -1.65, 0])
        with self.voiceover(
            "If a small chance of error is acceptable, three states and logarithmic time are enough. "
            "<bookmark mark='a'/> In Dana Angluin, James Aspnes and David Eisenstat's protocol of 2008, when x "
            "meets y, the responder goes blank; <bookmark mark='b'/> and an opinion that meets a blank recruits "
            "it. <bookmark mark='c'/> Opinions knock each other out and recruit, and the larger side snowballs. "
            "<bookmark mark='d'/> With high probability it converges in logarithmic parallel time, and to the "
            "initial majority whenever the margin is larger than about the square root of n times log n. "
            "<bookmark mark='e'/> Fast, but it can err on a close vote. <bookmark mark='f'/> In 2012 Luca "
            "Cardelli and Attila Csikász-Nagy noticed that the switch controlling the cell cycle has the same "
            "structure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ags), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), FadeIn(tags[1]))
            vo.wait_until("c")
            active = [(i, j, s) for i, j, s in seq if s is not None]
            for i, j, s in active[:10]:
                ln = Line(P[i], P[j], color=GREY_A, stroke_width=2.5, buff=0.2)
                self.play(Create(ln), to(j, s), run_time=0.35)
                self.play(FadeOut(ln), run_time=0.1)
            rest = active[10:]
            k = max(1, len(rest) // 6)
            for b in range(0, len(rest), k):
                last = {}
                for i, j, s in rest[b:b + k]:
                    last[j] = s
                self.play(*[to(j, s) for j, s in last.items()], run_time=0.45)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            vo.wait_until("f")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ what is computable
    def power(self):
        head = label(r"What a population can compute", font_size=36).to_edge(UP, buff=0.3)
        vals = [1, 0, 1, 1, 0, 1, 0, 1]
        xs = [-6.0 + 0.72 * k for k in range(len(vals))]
        y = 1.75

        def tok(v):
            c = YES if v == 5 else (HEAD if v else GREY_B)
            circ = Circle(radius=0.27, stroke_color=c, stroke_width=2.2, fill_color=c,
                          fill_opacity=0.25 if v else 0.0)
            return VGroup(circ, MathTex(str(v), font_size=26, color=WHITE))
        toks = [tok(v).move_to([x, y, 0]) for v, x in zip(vals, xs)]
        tg = VGroup(*toks)
        q = label(r"are at least five birds sick?", font_size=20, color=HEAD).next_to(tg, UP, buff=0.25)
        rl = VGroup(MathTex(r"(i, j)", r"\mapsto", r"(i + j,\ 0)", r"\text{ if } i + j < 5", font_size=26),
                    MathTex(r"(i, j)", r"\mapsto", r"(5,\ 5)", r"\text{ otherwise}", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(tg, DOWN, buff=0.35)
        ill = note(r"illustrative", font_size=16).next_to(rl, DOWN, buff=0.1).align_to(rl, LEFT)
        meets = [(0, 2), (3, 5), (0, 3), (7, 0)]
        fs = 30
        d = [MathTex(r"x_A", r">", r"x_B", font_size=fs),
             MathTex(r"x_A", r"-", r"x_B", r"\ge", r"1", font_size=fs),
             MathTex(r"\textstyle\sum_i a_i x_i", r"\ge", r"c", font_size=fs)]
        for m in d:
            m.move_to([3.6, 1.75, 0])
        dw = label(r"majority is a threshold: \ $a = (1, -1)$, \ $c = 1$", font_size=19, color=GREY_B).move_to(
            [3.6, 1.05, 0])
        thm = wrapped_label(r"\textbf{stably computable = semilinear}: \ Boolean combinations of thresholds "
                            r"$\sum_i a_i x_i \ge c$ and remainders $\sum_i a_i x_i \equiv c \pmod{m}$, \ the "
                            r"predicates of Presburger arithmetic \ (Angluin et al. \ 2004 and 2006; \ Angluin, \ "
                            r"Aspnes and Eisenstat \ 2006)", 12.4, font_size=20, color=WHITE)
        tb = VGroup(SurroundingRectangle(thm, buff=0.18, color=YES, corner_radius=0.1, stroke_width=2), thm)
        tb.move_to([0, -0.55, 0])
        yes = label(r"yes: \ $x \ge 5$, \ \ $x \equiv 0 \pmod{3}$, \ \ $x_A > x_B$", font_size=21, color=YES)
        no = label(r"no: \ $x = y^2$, \ \ $x$ a power of two", font_size=21, color=NO)
        ex = VGroup(yes, no).arrange(RIGHT, buff=1.2).next_to(tb, DOWN, buff=0.3)
        chem = wrapped_label(r"\textbf{chemistry}: \ molecules are agents and reactions are rules; \ error-free "
                             r"reaction networks compute exactly the semilinear functions \ (Chen, \ Doty and "
                             r"Soloveichik, \ 2012), \ and DNA strand displacement can implement any such network \ "
                             r"(Soloveichik, \ Seelig and Winfree, \ 2010)", 12.4, font_size=19,
                             color=KERN).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "What, exactly, can a population compute? <bookmark mark='a'/> A classic example: are at least five "
            "birds sick? Each agent counts up to five. When two meet, one takes the sum and the other drops to "
            "zero; once a sum reaches five, both say yes, and yes spreads like an epidemic. <bookmark mark='b'/> "
            "Majority is the same kind of question: x A greater than x B means x A minus x B is at least one, a "
            "threshold. <bookmark mark='c'/> Thresholds, remainders and their combinations are the semilinear "
            "predicates, those of Presburger arithmetic. Angluin and colleagues showed that all of them can be "
            "computed, and in 2006 Angluin, Aspnes and Eisenstat showed that nothing else can. "
            "<bookmark mark='d'/> Squares and powers of two are not. <bookmark mark='e'/> Chemical reaction "
            "networks are the same model with molecules; without errors they compute exactly the semilinear "
            "functions, and DNA can implement them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tg), FadeIn(q), FadeIn(rl), FadeIn(ill))
            cur = vals[:]
            for i, j in meets:
                s = cur[i] + cur[j]
                ni, nj = (s, 0) if s < 5 else (5, 5)
                cur[i], cur[j] = ni, nj
                arc = ArcBetweenPoints(toks[i].get_top() + UP * 0.05, toks[j].get_top() + UP * 0.05, angle=-PI / 2,
                                       color=HEAD, stroke_width=2.5)
                self.play(Create(arc), run_time=0.4)
                self.play(Transform(toks[i], tok(ni).move_to(toks[i])), Transform(toks[j], tok(nj).move_to(toks[j])),
                          FadeOut(arc), run_time=0.6)
            fives = [k for k in range(len(cur)) if cur[k] != 5]
            self.play(LaggedStart(*[Transform(toks[k], tok(5).move_to(toks[k])) for k in fives], lag_ratio=0.25),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(d[0]))
            self.play(TransformMatchingTex(d[0], d[1]))
            self.play(TransformMatchingTex(d[1], d[2]), FadeIn(dw))
            vo.wait_until("c")
            self.play(FadeIn(tb))
            vo.wait_until("d")
            self.play(FadeIn(ex))
            vo.wait_until("e")
            self.play(FadeIn(chem))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO, load)
