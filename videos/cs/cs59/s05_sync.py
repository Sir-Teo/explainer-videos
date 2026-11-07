from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, tag_box


def proc(name, color=GREY_B, r=0.32, size=19):
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    return VGroup(c, label(name, font_size=size, color=WHITE).move_to(c))


def cross(at, color=NO, s=0.15):
    return VGroup(Line(at + np.array([-s, -s, 0]), at + np.array([s, s, 0]), color=color, stroke_width=4),
                  Line(at + np.array([-s, s, 0]), at + np.array([s, -s, 0]), color=color, stroke_width=4))


def stacked(rows, whys, buff=0.22):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def setlab(vals):
    return MathTex(r"\{" + ", ".join(str(v) for v in sorted(vals)) + r"\}", font_size=26, color=DATA)


class Sync(VoiceoverScene):
    def construct(self):
        self.card()
        self.floodset()
        self.hidden()
        self.chain()
        self.hexagon()
        self.signatures()

    def card(self):
        card = chapter_card(4, r"Synchronous agreement and its bounds", r"How many rounds, \ and how many honest "
                            r"processes?", lit=(1982, 1983, 1986),
                            extra=((1982, r"Lamport, \ Shostak and Pease: \ $n > 3f$"),
                                   (1983, r"Dolev and Strong: \ signatures"),
                                   (1986, r"Fischer, \ Lynch and Merritt: \ the hexagon")), part=PART)
        with self.voiceover("Chapter four. Synchronous agreement and its bounds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def floodset(self):
        head = label(r"FloodSet: \ tell everyone everything", font_size=36).to_edge(UP, buff=0.3)
        P = [np.array(p) for p in ((-5.0, 1.15, 0), (-2.2, 1.15, 0), (-2.2, -1.35, 0), (-5.0, -1.35, 0))]
        ps = VGroup(*[proc(rf"$p_{k + 1}$").move_to(P[k]) for k in range(4)])
        ins = [1, 0, 1, 1]
        W = [{v} for v in ins]
        sets = VGroup(*[setlab(W[k]).next_to(ps[k], UP if k < 2 else DOWN, buff=0.15) for k in range(4)])
        ill = note(r"illustrative: \ $n = 4$, \ $f = 1$", font_size=16).move_to([-3.6, -2.5, 0])
        rl = label(r"round 0", font_size=22, color=HEAD).move_to([-3.6, -0.1, 0])
        prog = code_block(["W := {my input}", "repeat f + 1 rounds:", "    send W to everyone",
                           "    W := W + all received", "decide min(W)"], size=17).move_to([3.4, 2.0, 0])
        fs = 28
        rows = [MathTex(r"f \text{ crashes}", r",\ ", r"f + 1 \text{ rounds}", r"\;\Longrightarrow\;",
                        r"\text{a clean round}", font_size=fs),
                MathTex(r"\text{a clean round}", r"\;\Longrightarrow\;", r"W_p = W_q", r"\ \text{for all live } p, q",
                        font_size=fs),
                MathTex(r"W_p = W_q", r"\;\Longrightarrow\;", r"\min W_p = \min W_q", font_size=fs)]
        rows[2][2].set_color(YES)
        whys = [label(r"pigeonhole: \ some round has no new crash", font_size=18, color=GREY_B),
                label(r"in it every live process hears every other", font_size=18, color=GREY_B),
                label(r"equal sets stay equal, \ so all decide alike", font_size=18, color=GREY_B)]
        col = stacked(rows, whys, buff=0.22).next_to(prog, DOWN, buff=0.45)
        col.set_x(3.3)

        def send(pairs):
            ds = VGroup(*[Dot(P[a], radius=0.08, color=DATA).set_z_index(3) for a, b in pairs])
            self.play(FadeIn(ds, run_time=0.15))
            self.play(*[d.animate.move_to(P[b]) for d, (a, b) in zip(ds, pairs)], run_time=0.9)
            self.play(FadeOut(ds, run_time=0.15))
        with self.voiceover(
            "With synchronous rounds and crashes, agreement has a simple algorithm. <bookmark mark='a'/> In "
            "FloodSet each process keeps the set of values it has seen. Every round it sends the set to everyone "
            "and adds what it receives; after f plus one rounds it decides the smallest value in its set. "
            "<bookmark mark='b'/> Four processes, one crash. In round one, process two, the only one holding a "
            "zero, crashes after sending to process three alone. <bookmark mark='c'/> In round two process three "
            "passes the zero on, and everyone decides zero. <bookmark mark='d'/> Why does it work? With f crashes "
            "in f plus one rounds, some round has no crash. In that clean round every live process hears every "
            "other, so afterwards their sets are equal, and stay equal. Equal sets, equal minima."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ps), FadeIn(sets), FadeIn(ill), FadeIn(rl))
            vo.wait_until("a")
            self.play(FadeIn(prog))
            vo.wait_until("b")
            self.play(Transform(rl, label(r"round 1", font_size=22, color=HEAD).move_to(rl)))
            alive = [0, 2, 3]
            send([(a, b) for a in alive for b in range(4) if b != a] + [(1, 2)])
            self.play(FadeIn(cross(P[1])), ps[1][0].animate.set_stroke(NO))
            W[2] |= W[1]
            self.play(Transform(sets[2], setlab(W[2]).move_to(sets[2])))
            vo.wait_until("c")
            self.play(Transform(rl, label(r"round 2", font_size=22, color=HEAD).move_to(rl)))
            send([(a, b) for a in alive for b in alive if b != a])
            U = set().union(*[W[k] for k in alive])
            self.play(*[Transform(sets[k], setlab(U).move_to(sets[k])) for k in alive])
            dec = VGroup(*[label(r"decide 0", font_size=18, color=YES).next_to(sets[k], LEFT if k in (0, 3) else RIGHT,
                                                                               buff=0.15) for k in alive])
            self.play(FadeIn(dec))
            vo.wait_until("d")
            self.play(FadeIn(col[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def hidden(self):
        fl = load("floodset")["rows"]
        head = label(r"Why $f$ rounds are not enough", font_size=36).to_edge(UP, buff=0.3)
        ys = [1.7, 0.8, -0.1, -1.0]
        xs = [-5.5, -3.7, -1.9, -0.6]          # round boundaries; the last column is the decision
        lanes = VGroup()
        for k, y in enumerate(ys):
            lanes.add(Line([xs[0], y, 0], [xs[2] + 0.35, y, 0], color=GREY_C, stroke_width=1.5))
            lanes.add(label(rf"$p_{k + 1}$", font_size=19, color=GREY_A).next_to([xs[0], y, 0], LEFT, buff=0.12))
        ins = VGroup(*[label(str(v), font_size=19, color=DATA).move_to([xs[0] + 0.2, y + 0.2, 0])
                       for v, y in zip((0, 1, 1, 1), ys)])
        bounds = VGroup(*[DashedLine([x, 2.1, 0], [x, -1.35, 0], color=GREY_D, stroke_width=1.2, dash_length=0.07)
                          for x in xs[:3]])
        rlab = VGroup(*[label(rf"round {k + 1}", font_size=16, color=GREY_B).move_to([(xs[k] + xs[k + 1]) / 2, 2.3, 0])
                        for k in range(2)])
        m1 = Arrow([xs[0] + 0.1, ys[0], 0], [xs[1] - 0.1, ys[1], 0], buff=0, stroke_width=2.5, color=DATA,
                   max_tip_length_to_length_ratio=0.15)
        m2 = Arrow([xs[1] + 0.1, ys[1], 0], [xs[2] - 0.1, ys[2], 0], buff=0, stroke_width=2.5, color=DATA,
                   max_tip_length_to_length_ratio=0.15)
        x1 = cross(np.array([xs[0] + 1.1, ys[0], 0]), s=0.12)
        x2 = cross(np.array([xs[1] + 1.1, ys[1], 0]), s=0.12)
        d3 = label(r"sees 0: \ decides 0", font_size=17, color=YES).next_to([xs[2] + 0.35, ys[2], 0], RIGHT, buff=0.1)
        d4 = label(r"sees 1: \ decides 1", font_size=17, color=NO).next_to([xs[2] + 0.35, ys[3], 0], RIGHT, buff=0.1)
        cap = wrapped_label(r"$f = 2$ crashes, \ 2 rounds: \ each crash passes the 0 to just one process and dies",
                            6.4, font_size=18, color=GREY_A).move_to([-3.2, -1.85, 0])
        ill = note(r"illustrative run", font_size=16).next_to(cap, DOWN, buff=0.1)
        rows = [[f"{r['n']}", f"{r['f']}", f"{r['rounds']}", f"{r['summary']['checked']:,}".replace(",", "{,}"),
                 r"always" if r["agreement"] else r"can fail"] for r in fl]
        tab = grid_table([r"$n$", r"$f$", r"rounds", r"runs checked", r"agreement"], rows,
                         widths=[0.6, 0.6, 1.1, 1.8, 1.4], row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([3.6, 0.55, 0])
        for row, r in zip(tab.cells[1:], fl):
            row[4].set_color(YES if r["agreement"] else NO)
            if r["rounds"] == r["f"] + 1:
                row[2].set_color(YES)
        tl = note(r"FloodSet, \ every input and every crash pattern: \ who, \ when, \ and to whom it still sent",
                  font_size=16).next_to(tab, DOWN, buff=0.15)
        if tl.width > 6.3:
            tl.width = 6.3
        foot = wrapped_label(r"agreement holds exactly from $f + 1$ rounds", 6.3, font_size=20,
                             color=YES).next_to(tl, DOWN, buff=0.3)
        with self.voiceover(
            "Is the extra round really needed? <bookmark mark='a'/> Here is how an adversary defeats FloodSet with "
            "only f rounds, for f equal to two. Process one alone holds a zero. In round one it sends it only to "
            "process two, and crashes. <bookmark mark='b'/> In round two, process two passes it only to process "
            "three, and crashes too. <bookmark mark='c'/> Process three decides zero; process four never heard of "
            "it and decides one. <bookmark mark='d'/> Our instrument checked FloodSet exhaustively: every input, "
            "and every pattern of who crashes, when, and who still hears from it. With f rounds or fewer it always "
            "finds a run that breaks agreement. With f plus one rounds every run agrees, all fifty-six thousand "
            "eight hundred and forty-eight of them for four processes and two crashes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), FadeIn(bounds), FadeIn(rlab), FadeIn(ins))
            vo.wait_until("a")
            self.play(GrowArrow(m1))
            self.play(FadeIn(x1))
            vo.wait_until("b")
            self.play(GrowArrow(m2))
            self.play(FadeIn(x2))
            vo.wait_until("c")
            self.play(FadeIn(d3), FadeIn(d4))
            self.play(FadeIn(cap), FadeIn(ill))
            vo.wait_until("d")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(tl),
                      run_time=2.5)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def chain(self):
        head = label(r"Every algorithm needs $f + 1$ rounds", font_size=36).to_edge(UP, buff=0.3)
        names = [r"\alpha_0", r"\alpha_1", r"\alpha_2", r"\cdots", r"\alpha_{m-1}", r"\alpha_m"]
        boxes = VGroup()
        for k, nm in enumerate(names):
            fr = RoundedRectangle(width=1.35, height=0.85, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.6,
                                  fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(fr, MathTex(nm, font_size=30, color=WHITE).move_to(fr)))
        boxes.arrange(RIGHT, buff=0.65).next_to(head, DOWN, buff=0.75)
        links = VGroup(*[MathTex(r"\overset{q}{\sim}", font_size=30, color=HEAD).move_to(
            (boxes[k].get_right() + boxes[k + 1].get_left()) / 2) for k in range(len(boxes) - 1)])
        d0 = label(r"all inputs 0: \ decides 0", font_size=17, color=YES).next_to(boxes[0], UP, buff=0.12)
        dm = label(r"all inputs 1: \ decides 1", font_size=17, color=NO).next_to(boxes[-1], UP, buff=0.12)
        fs = 30
        rows = [MathTex(r"\alpha_j", r"\overset{q}{\sim}", r"\alpha_{j+1}", font_size=fs),
                MathTex(r"d(\alpha_j)", r"=", r"d_q(\alpha_j)", r"=", r"d_q(\alpha_{j+1})", r"=", r"d(\alpha_{j+1})",
                        font_size=fs),
                MathTex(r"0", r"=", r"d(\alpha_0)", r"=", r"d(\alpha_1)", r"=", r"\cdots", r"=", r"d(\alpha_m)", r"=",
                        r"1", font_size=fs)]
        rows[2][0].set_color(YES)
        rows[2][10].set_color(NO)
        whys = [label(r"neighbouring runs: \ some correct process $q$ sees exactly the same in both", font_size=18,
                      color=GREY_B),
                label(r"$q$ decides the same in both, \ and agreement makes everyone decide as $q$", font_size=18,
                      color=GREY_B),
                label(r"along the whole chain: \ a contradiction, \ so no such algorithm exists", font_size=18,
                      color=GREY_B)]
        col = stacked(rows, whys, buff=0.25).move_to([-2.7, -0.3, 0])
        how = VGroup(
            wrapped_label(r"\textbf{building the chain}: \ change one input at a time, \ first crashing that "
                          r"process before it says anything", 5.0, font_size=18, color=WHITE),
            wrapped_label(r"remove a message of the \textit{last} round: \ only its receiver notices", 5.0,
                          font_size=18, color=YES),
            wrapped_label(r"remove one of round $r$: \ first silence its receiver in round $r + 1$ \ (a shorter "
                          r"chain, \ one more crash), \ then remove it unseen, \ then restore", 5.0, font_size=18,
                          color=HEAD),
            wrapped_label(r"one crash per round: \ $f$ crashes cover $f$ rounds, \ never $f + 1$ \ (needs "
                          r"$n \ge f + 2$)", 5.0, font_size=18, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.15, -0.5, 0])
        src = note(r"Fischer and Lynch \ (1982); \ Dolev and Strong \ (1983)", font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "FloodSet needs f plus one rounds; could a cleverer algorithm need fewer? No, and the proof is a "
            "chain. <bookmark mark='a'/> Suppose an algorithm always decides within f rounds. Line up runs from "
            "one where every input is zero, which must decide zero, to one where every input is one. <bookmark "
            "mark='b'/> Each run differs from the next so little that some correct process sees exactly the same "
            "in both. <bookmark mark='c'/> That process decides the same in both, and agreement drags everyone "
            "along, <bookmark mark='d'/> so the decision never changes along the chain: zero equals one. <bookmark "
            "mark='e'/> The chain changes one input at a time, crashing that process first, and removes messages "
            "one at a time. A last-round message changes only its receiver's view; an earlier one is removed by "
            "first silencing its receiver in the next round, at the cost of another crash. One crash per round: f "
            "crashes cover f rounds, never f plus one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(d0), FadeIn(boxes[-1]), FadeIn(dm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[1:-1]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(lk) for lk in links], lag_ratio=0.3), run_time=1.8)
            self.play(FadeIn(col[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(*[b[0].animate.set_stroke(HEAD, width=2.4) for b in boxes], run_time=0.8)
            vo.wait_until("e")
            for h in how:
                self.play(FadeIn(h), run_time=0.8)
            self.play(FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def hexagon(self):
        hx = load("hexagon")
        names, ins, dec = hx["names"], hx["inputs"], hx["decisions"]
        head = label(r"Three processes cannot survive one liar", font_size=36).to_edge(UP, buff=0.3)
        # the triangle the protocol was written for
        tc = np.array([-4.6, 0.85, 0])
        tp = [tc + 1.25 * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3)]
        tri = VGroup(*[proc(n, color=NO if n == "C" else GREY_B).move_to(p) for n, p in zip("ABC", tp)])
        tl = VGroup(*[Line(tp[a], tp[b], color=GREY_D, stroke_width=2) for a, b in ((0, 1), (1, 2), (2, 0))])
        tl.set_z_index(-1)
        tcap = wrapped_label(r"the protocol is written for three processes; \ $C$ may lie", 4.6, font_size=18,
                             color=GREY_A).next_to(tri, DOWN, buff=0.3)
        # the hexagon: six honest copies wired in a ring
        hc = np.array([2.7, 0.3, 0])
        R = 1.9
        hp = [hc + R * np.array([np.cos(PI / 2 - k * TAU / 6), np.sin(PI / 2 - k * TAU / 6), 0]) for k in range(6)]
        hn = VGroup(*[proc(rf"${n[0]}_{n[1]}$", color=DATA if v == 0 else LAM, r=0.36).move_to(p)
                      for n, v, p in zip(names, ins, hp)])
        hl = VGroup(*[Line(hp[k], hp[(k + 1) % 6], color=GREY_D, stroke_width=2) for k in range(6)]).set_z_index(-1)
        il = VGroup(*[label(rf"in {v}", font_size=16, color=DATA if v == 0 else LAM).move_to(
            hc + (R + 0.62) * (hp[k] - hc) / R) for k, v in enumerate(ins)])
        verdict = VGroup()
        for k, p in enumerate(hx["pairs"]):
            ok = p["agreement"] and p["validity"]
            mid = (hp[k] + hp[(k + 1) % 6]) / 2
            out = hc + (mid - hc) * 0.62
            verdict.add(label(rf"{p['byzantine']} lies" if ok else rf"{p['byzantine']} lies: \ {p['decisions'][0]} vs "
                              rf"{p['decisions'][1]}", font_size=16, color=YES if ok else NO).move_to(out))
        leg = label(r"fill: \ the copy's decision \ (blue 0, \ purple 1)", font_size=16, color=GREY_A).next_to(
            tcap, DOWN, buff=0.25)
        fs = 30
        eq = MathTex(r"0", r"=", r"d(A_0)", r"=", r"d(B_0)", r"=", r"d(C_0)", r"=", r"d(A_1)", r"=", r"d(B_1)", r"=",
                     r"1", font_size=fs)
        eq[0].set_color(YES)
        eq[12].set_color(NO)
        eqw = label(r"validity at both ends \ (equal inputs), \ agreement at every step: \ impossible", font_size=18,
                    color=GREY_B)
        eg = VGroup(eq, eqw).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.75)
        src = note(r"$n \le 3f$: \ split the processes into three groups of at most $f$ and argue the same way \ "
                   r"(Lamport, \ Shostak and Pease 1982; \ this proof Fischer, \ Lynch and Merritt 1986)",
                   font_size=16).to_edge(DOWN, buff=0.25)
        if src.width > 12.6:
            src.width = 12.6
        with self.voiceover(
            "Now let processes lie. Lamport, Shostak and Pease proved in 1982 that Byzantine agreement needs more "
            "than three f processes; the cleanest proof, by Fischer, Lynch and Merritt in 1986, is a hexagon. "
            "<bookmark mark='a'/> Take any protocol for three processes, A, B and C, meant to survive one liar. "
            "<bookmark mark='b'/> Wire six honest copies into a ring, the zero copies with input zero and the one "
            "copies with input one, each treating its two ring neighbours as the other two. <bookmark mark='c'/> "
            "Any two neighbours see exactly what they would in a three-process run where the third lies, playing a "
            "different copy to each. So validity makes A zero and B zero decide zero and B one decide one, and "
            "agreement makes every neighbouring pair match. <bookmark mark='d'/> Around the ring, zero equals one. "
            "<bookmark mark='e'/> Our instrument ran a natural two-round majority protocol on the hexagon, and it "
            "breaks where it must: C zero disagrees with A one, and C one with A zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tri), Create(tl), FadeIn(tcap))
            vo.wait_until("b")
            self.play(FadeIn(hn), Create(hl), FadeIn(il))
            for _ in range(2):
                ds = VGroup(*[Dot(hp[k], radius=0.08, color=HEAD).set_z_index(3) for k in range(6) for _d in (1, -1)])
                tg = [hp[(k + d) % 6] for k in range(6) for d in (1, -1)]
                self.play(FadeIn(ds, run_time=0.15))
                self.play(*[d.animate.move_to(t) for d, t in zip(ds, tg)], run_time=0.9)
                self.play(FadeOut(ds, run_time=0.15))
            vo.wait_until("c")
            self.play(*[hn[k][0].animate.set_fill(DATA if dec[n] == 0 else LAM, opacity=0.45)
                        for k, n in enumerate(names)], FadeIn(leg))
            vo.wait_until("d")
            self.play(FadeIn(eg))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(v) for v in verdict], lag_ratio=0.3), run_time=2.0)
            bad = [k for k, p in enumerate(hx["pairs"]) if not (p["agreement"] and p["validity"])]
            self.play(*[hl[k].animate.set_stroke(NO, width=5) for k in bad])
            self.play(FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def signatures(self):
        head = label(r"With signatures: \ Dolev and Strong", font_size=36).to_edge(UP, buff=0.3)
        rounds = [("v : s", DATA), ("v : s : p1", LAM), ("v : s : p1 : p2", HEAD)]
        msgs = VGroup(*[tag_box(t, color=c, size=19) for t, c in rounds]).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        msgs.move_to([-3.9, 1.0, 0])
        rl = VGroup(*[label(rf"round {k + 1}", font_size=17, color=GREY_B).next_to(m, LEFT, buff=0.3)
                      for k, m in enumerate(msgs)])
        arr = VGroup(*[Arrow(msgs[k].get_bottom(), msgs[k + 1].get_top(), buff=0.06, stroke_width=2, color=GREY_B,
                             max_tip_length_to_length_ratio=0.3) for k in range(2)])
        al = VGroup(label(r"$p_1$ signs and relays", font_size=16, color=GREY_A).next_to(arr[0], RIGHT, buff=0.15),
                    label(r"$p_2$ signs and relays", font_size=16, color=GREY_A).next_to(arr[1], RIGHT, buff=0.15))
        ill = note(r"illustrative chain", font_size=16).next_to(msgs, DOWN, buff=0.25)
        rules = VGroup(
            wrapped_label(r"the sender signs its value; \ in round $r$ a process accepts $v$ if it carries $r$ "
                          r"distinct signatures, \ the sender's first, \ then adds its own and relays it", 6.3,
                          font_size=19, color=WHITE),
            wrapped_label(r"after $f + 1$ rounds: \ decide $v$ if it is the only value accepted, \ otherwise a "
                          r"fixed default", 6.3, font_size=19, color=DATA),
            wrapped_label(r"why it agrees: \ a correct process that accepts in round $r \le f$ relays, \ so all "
                          r"accept by round $r + 1$; \ a value first accepted in round $f + 1$ carries $f + 1$ "
                          r"signatures, \ one of them correct, \ and that process relayed it earlier", 6.3,
                          font_size=19, color=YES),
            wrapped_label(r"a sender who signs both 0 and 1 is caught together: \ everyone accepts both, \ everyone "
                          r"takes the default", 6.3, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.3, 0.25, 0])
        foot = wrapped_label(r"Dolev and Strong \ (1983): \ broadcast for \textit{any} number of faulty processes, \ "
                             r"in $f + 1$ rounds, \ and no algorithm does it in fewer; \ unforgeable signatures \ "
                             r"(Part 30) \ beat $n > 3f$", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "That bound assumes a liar can claim anything about what others said. Part 30's signatures take that "
            "power away. "
            "<bookmark mark='a'/> In Danny Dolev and Ray Strong's protocol of 1983 the sender signs its value. A "
            "process that in round r receives a value carrying r distinct signatures, the sender's first, accepts "
            "it, adds its signature and relays it. <bookmark mark='b'/> After f plus one rounds it decides the "
            "value if it accepted exactly one, and a default otherwise. <bookmark mark='c'/> Why do correct "
            "processes agree? A value a correct process accepts by round f is relayed, so everyone accepts it a "
            "round later. A value first accepted in the last round carries f plus one signatures, so one signer "
            "was correct and relayed it earlier. <bookmark mark='d'/> A sender who signs two values is exposed to "
            "all. <bookmark mark='e'/> It works for any number of faulty processes, in f plus one rounds, the "
            "minimum."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(msgs[0]), FadeIn(rl[0]), FadeIn(rules[0]))
            for k in range(2):
                self.play(GrowArrow(arr[k]), FadeIn(al[k]))
                self.play(FadeIn(msgs[k + 1], shift=DOWN * 0.1), FadeIn(rl[k + 1]))
            self.play(FadeIn(ill))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]))
            vo.wait_until("d")
            self.play(FadeIn(rules[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
