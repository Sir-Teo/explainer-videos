from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, load, tag_box

V0, V1 = DATA, LAM


def proc(name, color=GREY_B, r=0.3, size=24):
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    return VGroup(c, MathTex(name, font_size=size, color=WHITE).move_to(c))


def polygon_pos(n, center, radius, start=90):
    return [np.array(center) + radius * np.array([math.cos(math.radians(start + 360 * k / n)),
                                                  math.sin(math.radians(start + 360 * k / n)), 0])
            for k in range(n)]


def msg(a, b, color=DATA, buff=0.36, sw=2.2):
    return Arrow(a, b, buff=buff, stroke_width=sw, color=color, max_tip_length_to_length_ratio=0.14)


def cross(at, color=NO, s=0.16):
    return VGroup(Line(at + np.array([-s, -s, 0]), at + np.array([s, s, 0]), color=color, stroke_width=4),
                  Line(at + np.array([-s, s, 0]), at + np.array([s, -s, 0]), color=color, stroke_width=4))


def ladder(rows, whys, x_row, x_why, y_top, dy):
    """Derivation rows (MathTex) left-aligned at x_row, their reasons at x_why, one line each."""
    for k, (r, w) in enumerate(zip(rows, whys)):
        y = y_top - k * dy
        r.move_to([0, y, 0]).align_to([x_row, 0, 0], LEFT)
        w.move_to([0, y, 0]).align_to([x_why, 0, 0], LEFT)
    return VGroup(*rows), VGroup(*whys)


def stacked(rows, whys, buff=0.22):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


class Detectors(VoiceoverScene):
    def construct(self):
        self.card()
        self.oracle()
        self.timeouts()
        self.classes()
        self.rotating()
        self.partition()
        self.omega()
        self.accrual()

    def card(self):
        card = chapter_card(8, r"Failure detectors", r"How much must a process know about crashes to agree?",
                            lit=(1996, 2004),
                            extra=((1996, r"Chandra and Toueg; \ Chandra, \ Hadzilacos and Toueg"),
                                   (2004, r"Hayashibara et al.: \ $\varphi$ accrual")), part=PART)
        with self.voiceover("Chapter eight. Failure detectors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the idea
    def oracle(self):
        head = label(r"An oracle beside every process", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-3.7, -0.5, 0])
        P = polygon_pos(5, C, 1.75)
        ps = VGroup(*[proc(rf"p_{k + 1}").move_to(P[k]) for k in range(5)])
        links = VGroup(*[Line(P[i], P[j], color=GREY_D, stroke_width=1.2, buff=0.32)
                         for i in range(5) for j in range(i + 1, 5)])

        def fd(k, tex, color=KERN):
            t = MathTex(tex, font_size=22, color=color)
            box = RoundedRectangle(width=max(0.8, t.width + 0.3), height=0.46, corner_radius=0.08,
                                   stroke_color=KERN, stroke_width=1.5, fill_color=BG, fill_opacity=1)
            t.move_to(box)
            d = (P[k] - C) / np.linalg.norm(P[k] - C)
            g = VGroup(box, t)
            g.move_to(P[k] + d * (0.62 + 0.25 * abs(d[0]) + g.width / 2 * abs(d[0])))
            return g
        empty = r"\{\,\}"
        boxes = [fd(k, empty) for k in range(5)]
        sus = [fd(k, r"\{p_3\}") for k in range(5)]
        wrong = fd(0, r"\{p_3,\, p_5\}", color=NO)
        x3 = cross(P[2])
        late = msg(P[4], P[0], color=DATA)
        W = 5.4
        notes = VGroup(
            wrapped_label(r"a \textbf{failure detector}: \ a local module that outputs the processes it currently "
                          r"\textbf{suspects} of having crashed", W, font_size=20, color=WHITE),
            wrapped_label(r"$p_3$ crashes: \ the others come to suspect it", W, font_size=20, color=NO),
            wrapped_label(r"it may be wrong: \ $p_1$ suspects $p_5$, \ which is only slow, \ and trusts it again "
                          r"when $p_5$'s message arrives", W, font_size=20, color=HEAD),
            wrapped_label(r"Chandra and Toueg \ (1996): \ describe a detector by the \textbf{mistakes it may make}, "
                          r"\ not by how it is built", W, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.75, -0.1, 0])
        ill = note(r"illustrative", font_size=16).next_to(VGroup(ps, *boxes), DOWN, buff=0.2)
        with self.voiceover(
            "Chapter five showed that one possible crash makes asynchronous consensus impossible. In 1996 Tushar "
            "Chandra and Sam Toueg asked how much knowledge about crashes would be enough. <bookmark mark='a'/> "
            "Give every process a local oracle, a failure detector, which outputs the processes it currently "
            "suspects of having crashed. <bookmark mark='b'/> When process three crashes, the others' detectors "
            "come to suspect it. <bookmark mark='c'/> But a detector may be wrong. Process one suspects process "
            "five, which is merely slow, and trusts it again when its message arrives. <bookmark mark='d'/> The "
            "insight was to describe detectors by the mistakes they may make, not by how they are built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(links), FadeIn(ps))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in boxes], lag_ratio=0.2), FadeIn(notes[0]),
                      FadeIn(ill))
            vo.wait_until("b")
            self.play(Create(x3), ps[2][0].animate.set_stroke(NO), boxes[2].animate.set_opacity(0.25))
            self.play(LaggedStart(*[Transform(boxes[k], sus[k]) for k in (0, 1, 3, 4)], lag_ratio=0.3),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Transform(boxes[0], wrong), FadeIn(notes[2]))
            self.play(GrowArrow(late))
            self.play(Transform(boxes[0], fd(0, r"\{p_3\}")), FadeOut(late))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ heartbeats
    def timeouts(self):
        head = label(r"Building one from heartbeats", font_size=36).to_edge(UP, buff=0.3)

        def X(t):
            return -5.3 + 0.97 * t
        yq, yp = 2.0, 0.85
        lq = Line([X(0) - 0.15, yq, 0], [X(12), yq, 0], color=GREY_C, stroke_width=2)
        lp = Line([X(0) - 0.15, yp, 0], [X(12), yp, 0], color=GREY_C, stroke_width=2)
        nq = MathTex(r"q", font_size=30).next_to(lq, LEFT, buff=0.2)
        np_ = MathTex(r"p", font_size=30).next_to(lp, LEFT, buff=0.2)
        tl = label(r"time", font_size=17, color=GREY_B).next_to(lp.get_end(), UP, buff=0.12)
        sends = list(range(8))
        delay = {k: 0.35 for k in sends}
        delay[3] = 2.25
        beats = [Arrow([X(s), yq, 0], [X(s + delay[s]), yp, 0], buff=0, stroke_width=2,
                       color=HEAD if s == 3 else DATA, tip_length=0.16, max_tip_length_to_length_ratio=0.16)
                 for s in sends]
        crash = cross(np.array([X(7.6), yq, 0]))
        sus1 = Rectangle(width=X(4.35) - X(3.55), height=0.22, stroke_width=0, fill_color=NO,
                         fill_opacity=0.85).move_to([(X(3.55) + X(4.35)) / 2, yp - 0.24, 0])
        sus2 = Rectangle(width=X(12) - X(9.75), height=0.22, stroke_width=0, fill_color=NO,
                         fill_opacity=0.85).move_to([(X(9.75) + X(12)) / 2, yp - 0.24, 0])
        l1 = label(r"false suspicion", font_size=17, color=NO).next_to(sus1, DOWN, buff=0.1)
        l1b = label(r"timeout doubled", font_size=17, color=HEAD).next_to(l1, DOWN, buff=0.06)
        l2 = label(r"suspected for ever", font_size=17, color=NO).next_to(sus2, DOWN, buff=0.1)
        ill = note(r"illustrative", font_size=16).next_to(lq.get_end(), UP, buff=0.15).shift(LEFT * 0.4)
        fs = 30
        rows = [MathTex(r"T_k", r"=", r"2^{k}\,T_0", font_size=fs),
                MathTex(r"2^{k}\,T_0", r"\ge", r"\Delta + \pi", font_size=fs),
                MathTex(r"k", r"\ge", r"\log_2 \frac{\Delta + \pi}{T_0}", font_size=fs)]
        whys = [label(r"the timeout after $k$ false suspicions", font_size=19, color=GREY_B),
                label(r"once the network settles, \ heartbeats are at most $\Delta + \pi$ apart", font_size=19,
                      color=GREY_B),
                label(r"after that many mistakes, \ no more: \ finitely many in all", font_size=19, color=YES)]
        rg, wg = ladder(rows, whys, -6.3, -2.2, -0.75, 0.75)
        concl = wrapped_label(r"every crashed process is eventually suspected for ever, \ every correct one "
                              r"eventually trusted for ever: \ an \textbf{eventually perfect} detector, \ "
                              r"$\Diamond\mathcal{P}$", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How is such a detector built? With heartbeats. <bookmark mark='a'/> Process q sends one every "
            "period, and p suspects q when none arrives within a timeout. <bookmark mark='b'/> One heartbeat is "
            "delayed, the timer expires, and p suspects a healthy q. When it arrives, p trusts q again and "
            "doubles the timeout. <bookmark mark='c'/> When q really crashes, the heartbeats stop and p suspects "
            "it for ever. <bookmark mark='d'/> Under partial synchrony, once the network settles, heartbeats are "
            "at most the delay bound plus the period apart. Each mistake doubles the timeout, "
            "<bookmark mark='e'/> so after logarithmically many mistakes there are no more. <bookmark mark='f'/> "
            "The result is an eventually perfect detector."
        ) as vo:
            self.play(FadeIn(head), Create(lq), Create(lp), FadeIn(nq), FadeIn(np_), FadeIn(tl), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(b) for b in beats[:3]], lag_ratio=0.5), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowArrow(beats[3]), run_time=1.2)
            self.play(GrowFromEdge(sus1, LEFT), FadeIn(l1))
            self.play(LaggedStart(*[GrowArrow(b) for b in beats[4:]], lag_ratio=0.4), FadeIn(l1b), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(crash))
            self.play(GrowFromEdge(sus2, LEFT), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(concl, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the classes
    def classes(self):
        head = label(r"Completeness and accuracy", font_size=36).to_edge(UP, buff=0.3)
        W = 6.9
        defs = VGroup(
            wrapped_label(r"\textbf{strong completeness}: \ every crashed process is eventually suspected, \ for "
                          r"ever, \ by \textit{every} correct process", W, font_size=19, color=WHITE),
            wrapped_label(r"\textbf{weak completeness}: \ the same, \ by \textit{some} correct process", W,
                          font_size=19, color=GREY_A),
            wrapped_label(r"\textbf{strong accuracy}: \ no process is suspected before it crashes", W, font_size=19,
                          color=WHITE),
            wrapped_label(r"\textbf{weak accuracy}: \ \textit{some} correct process is never suspected", W,
                          font_size=19, color=GREY_A),
            wrapped_label(r"\textbf{eventual} accuracy: \ the same, \ but only after some unknown time", W,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.1, 0.35, 0])
        cw, ch, gx, gy = 1.35, 0.7, 0.14, 0.14
        x0, y0 = 3.75, 1.35
        names = [[r"\mathcal{P}", r"\mathcal{Q}"], [r"\mathcal{S}", r"\mathcal{W}"],
                 [r"\Diamond\mathcal{P}", r"\Diamond\mathcal{Q}"], [r"\Diamond\mathcal{S}", r"\Diamond\mathcal{W}"]]
        cells = []
        for r in range(4):
            line = []
            for c in range(2):
                fr = RoundedRectangle(width=cw, height=ch, corner_radius=0.08, stroke_color=YES if c == 0 else GREY_B,
                                      stroke_width=1.8, fill_color=BG, fill_opacity=1)
                fr.move_to([x0 + c * (cw + gx), y0 - r * (ch + gy), 0])
                t = MathTex(names[r][c], font_size=34, color=WHITE if c == 0 else GREY_A).move_to(fr)
                line.append(VGroup(fr, t))
            cells.append(line)
        grid = VGroup(*[VGroup(*l) for l in cells])
        rh = [r"strong accuracy", r"weak accuracy", r"eventually strong", r"eventually weak"]
        rheads = VGroup(*[label(t, font_size=17, color=HEAD if k > 1 else GREY_A).next_to(cells[k][0], LEFT,
                                                                                       buff=0.2)
                          for k, t in enumerate(rh)])
        ch_ = [VGroup(label(r"strong", font_size=17, color=YES), label(r"completeness", font_size=16,
                                                                        color=YES)).arrange(DOWN, buff=0.04),
               VGroup(label(r"weak", font_size=17, color=GREY_A), label(r"completeness", font_size=16,
                                                                        color=GREY_A)).arrange(DOWN, buff=0.04)]
        cheads = VGroup(*[h.next_to(cells[0][c], UP, buff=0.15) for c, h in enumerate(ch_)])
        eqs = VGroup(*[MathTex(r"\equiv", font_size=30, color=YES).move_to(
            (cells[r][0].get_right() + cells[r][1].get_left()) / 2) for r in range(4)])
        gossip = wrapped_label(r"forward your suspicions to everyone: \ weak completeness becomes strong", 5.0,
                               font_size=18, color=YES).next_to(grid, DOWN, buff=0.3).align_to(rheads, LEFT)
        hi = SurroundingRectangle(cells[3][0], buff=0.07, color=HEAD, stroke_width=3)
        foot = wrapped_label(r"perfect $\mathcal{P}$ is stronger than strong $\mathcal{S}$ and eventually perfect "
                             r"$\Diamond\mathcal{P}$; \ both are stronger than \textbf{eventually strong} "
                             r"$\Diamond\mathcal{S}$, \ the weakest of the four", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Chandra and Toueg sorted detectors by two properties. <bookmark mark='a'/> Completeness: every "
            "crashed process is eventually suspected for ever, by every correct process, or in the weak version "
            "by some correct process. <bookmark mark='b'/> Accuracy: strongly, no process is suspected before it "
            "crashes; weakly, some correct process is never suspected. <bookmark mark='c'/> And eventual "
            "versions, which hold only after some unknown time. <bookmark mark='d'/> That makes eight classes. "
            "<bookmark mark='e'/> But weak completeness becomes strong if every process forwards its suspicions "
            "to everyone, so four remain. <bookmark mark='f'/> Our heartbeat detector is eventually perfect, and "
            "the weakest, eventually strong, will turn out to be enough."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(defs[1]), FadeIn(cheads))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]), FadeIn(defs[3]), FadeIn(rheads[:2]))
            vo.wait_until("c")
            self.play(FadeIn(defs[4]), FadeIn(rheads[2:]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c, scale=0.85) for line in cells for c in line], lag_ratio=0.12),
                      run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(eqs), FadeIn(gossip), *[cells[r][1].animate.set_opacity(0.35) for r in range(4)])
            vo.wait_until("f")
            self.play(Create(hi), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ consensus with <>S
    def rotating(self):
        head = label(r"Consensus with $\Diamond\mathcal{S}$ and a majority", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-4.0, -0.75, 0])
        P = polygon_pos(5, C, 1.7)
        ps = VGroup(*[proc(rf"p_{k + 1}").move_to(P[k]) for k in range(5)])
        est0 = [1, 0, 1, 0, 1]

        def est(k, v, ts, color=None):
            d = (P[k] - C) / np.linalg.norm(P[k] - C)
            t = MathTex(rf"{v}_{{{ts}}}", font_size=30, color=color or (V0 if v == 0 else V1))
            return t.move_to(P[k] + d * 0.68)
        ests = [est(k, est0[k], 0) for k in range(5)]
        estg = VGroup(*ests)
        x5 = cross(P[4])
        rl = label(r"round 1: \ coordinator $p_1$", font_size=22, color=HEAD).move_to([-4.0, 2.35, 0])
        rl2 = label(r"round 2: \ coordinator $p_2$", font_size=22, color=HEAD).move_to(rl)
        prog = code_block(["round r, coordinator c:", "1 send (est, ts) to c", "2 c: wait for a majority,",
                           "    take est with largest ts,", "    send it to all", "3 wait for it, or suspect c:",
                           "    got v: est, ts := v, r; ack", "    suspected c: nack",
                           "4 c: majority of acks:", "    decide v, tell everyone"], size=17).move_to([3.3, 1.05, 0])
        phase = [VGroup(prog[1]), VGroup(*prog[2:5]), VGroup(*prog[5:8]), VGroup(*prog[8:10])]

        pb = [SurroundingRectangle(ph, buff=0.06, color=HEAD, stroke_width=1.8) for ph in phase]
        hl = pb[0].copy()
        ring1 = Circle(radius=0.38, color=HEAD, stroke_width=3).move_to(P[0])
        ring2 = Circle(radius=0.38, color=HEAD, stroke_width=3).move_to(P[1])
        to1 = VGroup(*[msg(P[k], P[0], DATA) for k in (1, 2, 3)])
        nack = VGroup(*[msg(P[k], P[0], NO) for k in (1, 2, 3)])
        susp = VGroup(*[label(r"suspects $p_1$", font_size=16, color=NO).next_to(ests[k], DOWN if k > 1 else UP,
                                                                                buff=0.08) for k in (1, 2, 3)])
        to2 = VGroup(*[msg(P[k], P[1], DATA) for k in (0, 2, 3)])
        out2 = VGroup(*[msg(P[1], P[k], HEAD) for k in (0, 2, 3)])
        acks = VGroup(*[msg(P[k], P[1], YES) for k in (0, 2, 3)])
        new = [est(k, 0, 2) if k != 4 else ests[4].copy() for k in range(5)]
        decided = [ps[k][0].animate.set_fill(YES, opacity=0.35).set_stroke(YES) for k in range(4)]
        fs = 30
        sf = [MathTex(r"|M_1| > \tfrac{n}{2}", r",\ ", r"|M_2| > \tfrac{n}{2}", font_size=fs),
              MathTex(r"|M_1 \cap M_2|", r"\ge", r"|M_1| + |M_2| - n", font_size=fs),
              MathTex(r"|M_1 \cap M_2|", r">", r"0", font_size=fs)]
        for r in sf:
            r.move_to([3.3, -1.75, 0])
        sfl = wrapped_label(r"two majorities share a process: \ a value a majority adopted is seen by every later "
                            r"coordinator, \ with the largest timestamp", 6.4, font_size=18,
                            color=YES).next_to(sf[0], DOWN, buff=0.25).set_x(3.3)
        ill = note(r"illustrative: \ $n = 5$, \ $p_5$ crashed; \ subscripts are timestamps",
                   font_size=16).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Here is Chandra and Toueg's algorithm for an eventually strong detector and a correct majority. "
            "<bookmark mark='a'/> A coordinator rotates from round to round, and everyone sends it an estimate, "
            "stamped with the round in which it was adopted. <bookmark mark='b'/> In round one the coordinator is "
            "slow, the detectors suspect it, and the others refuse and move on. Mistakes cost time, never safety. "
            "<bookmark mark='c'/> In round two, process two gathers a majority of estimates, takes the latest, "
            "and proposes it; the others adopt it and acknowledge. <bookmark mark='d'/> With a majority of "
            "acknowledgements it decides. <bookmark mark='e'/> Safety is counting: two majorities always share a "
            "process, so every later coordinator sees the adopted value."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ps), FadeIn(estg), FadeIn(prog), Create(x5), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(rl), Create(ring1), Create(hl))
            self.play(LaggedStart(*[GrowArrow(a) for a in to1], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(susp), Transform(hl, pb[2].copy()))
            self.play(ReplacementTransform(to1, nack))
            vo.wait_until("c")
            self.play(FadeOut(nack), FadeOut(susp), ReplacementTransform(ring1, ring2), Transform(rl, rl2),
                      Transform(hl, pb[0].copy()))
            self.play(LaggedStart(*[GrowArrow(a) for a in to2], lag_ratio=0.2))
            self.play(Transform(hl, pb[1].copy()),
                      Indicate(ests[1], color=HEAD))
            self.play(FadeOut(to2), LaggedStart(*[GrowArrow(a) for a in out2], lag_ratio=0.2))
            self.play(Transform(hl, pb[2].copy()), *[Transform(ests[k], new[k]) for k in range(4)])
            self.play(ReplacementTransform(out2, acks))
            vo.wait_until("d")
            self.play(Transform(hl, pb[3].copy()),
                      FadeOut(acks), *decided)
            vo.wait_until("e")
            self.play(FadeIn(sf[0]), FadeIn(sfl))
            self.play(TransformMatchingTex(sf[0], sf[1]))
            self.play(TransformMatchingTex(sf[1], sf[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ why a majority
    def partition(self):
        head = label(r"Why a majority must be correct", font_size=36).to_edge(UP, buff=0.3)
        xs = [-4.0, -2.4, 2.4, 4.0]
        y = 1.45
        ps = VGroup(*[proc(rf"p_{k + 1}").move_to([x, y, 0]) for k, x in enumerate(xs)])
        boxA = RoundedRectangle(width=3.0, height=1.05, corner_radius=0.12, stroke_color=V0, stroke_width=2).move_to(
            [-3.2, y, 0])
        boxB = RoundedRectangle(width=3.0, height=1.05, corner_radius=0.12, stroke_color=V1, stroke_width=2).move_to(
            [3.2, y, 0])
        la = label(r"$A$: \ inputs 0", font_size=20, color=V0).next_to(boxA, UP, buff=0.12)
        lb = label(r"$B$: \ inputs 1", font_size=20, color=V1).next_to(boxB, UP, buff=0.12)
        wall = DashedLine([0, 2.4, 0], [0, 0.55, 0], color=GREY_C, stroke_width=1.6, dash_length=0.1)
        xB = VGroup(*[cross(ps[k].get_center()) for k in (2, 3)])
        xA = VGroup(*[cross(ps[k].get_center()) for k in (0, 1)])

        def dec(box, v, t):
            return label(rf"decides {v} at ${t}$", font_size=19, color=V0 if v == 0 else V1).next_to(box, DOWN,
                                                                                                    buff=0.15)
        dA, dB = dec(boxA, 0, r"t_A"), dec(boxB, 1, r"t_B")
        runs = [label(r"run 1: \ $B$ crashed at the start", font_size=21, color=WHITE),
                label(r"run 2: \ $A$ crashed at the start", font_size=21, color=WHITE),
                label(r"run 3: \ no crash; \ messages across are slow", font_size=21, color=HEAD)]
        for r in runs:
            r.move_to([0, -0.05, 0])
        slow = VGroup(Arrow([-1.6, 1.15, 0], [-0.08, 1.15, 0], buff=0, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.2),
                      Arrow([1.6, 1.75, 0], [0.08, 1.75, 0], buff=0, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.2))
        fs = 30
        rows = [MathTex(r"\text{run 3}", r"\overset{A}{\sim}", r"\text{run 1}", r"\text{ until } t_A", font_size=fs),
                MathTex(r"\text{run 3}", r"\overset{B}{\sim}", r"\text{run 2}", r"\text{ until } t_B", font_size=fs),
                MathTex(r"0", r"\ne", r"1", font_size=fs)]
        whys = [label(r"same messages, \ same suspicions: \ $A$ decides 0", font_size=19, color=GREY_B),
                label(r"and $B$ decides 1", font_size=19, color=GREY_B),
                label(r"two correct halves disagree", font_size=19, color=NO)]
        rg, wg = ladder(rows, whys, -5.8, -0.9, -0.85, 0.7)
        foot = wrapped_label(r"Chandra and Toueg \ (1996): \ with $\Diamond\mathcal{P}$, \ and so with "
                             r"$\Diamond\mathcal{S}$, \ consensus needs $f < n/2$; \ with $\mathcal{S}$ it survives "
                             r"any number of crashes", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why must a majority be correct? <bookmark mark='a'/> Split the processes into two halves, inputs "
            "zero and inputs one, and allow half of them to crash. <bookmark mark='b'/> In run one the right half "
            "crashes at the start. The left half must decide alone; it has seen only zeros, so it decides zero, "
            "at some time t A. <bookmark mark='c'/> In run two the left half crashes, and the right half decides "
            "one, at time t B. <bookmark mark='d'/> In run three nobody crashes, but messages across are slow, "
            "and each half suspects the other until both have decided, which eventual accuracy allows. "
            "<bookmark mark='e'/> Each half sees what it saw before: one decides zero, the other one. "
            "<bookmark mark='f'/> A strong detector needs no majority at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ps), Create(boxA), Create(boxB), FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(runs[0]), Create(xB), VGroup(ps[2], ps[3]).animate.set_opacity(0.4))
            self.play(FadeIn(dA))
            vo.wait_until("c")
            self.play(ReplacementTransform(runs[0], runs[1]), FadeOut(xB), FadeOut(dA),
                      VGroup(ps[2], ps[3]).animate.set_opacity(1), Create(xA),
                      VGroup(ps[0], ps[1]).animate.set_opacity(0.4))
            self.play(FadeIn(dB))
            vo.wait_until("d")
            self.play(ReplacementTransform(runs[1], runs[2]), FadeOut(xA), FadeOut(dB),
                      VGroup(ps[0], ps[1]).animate.set_opacity(1), Create(wall))
            self.play(GrowArrow(slow[0]), GrowArrow(slow[1]))
            self.play(FadeIn(dA), FadeIn(dB))
            vo.wait_until("e")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Omega
    def omega(self):
        head = label(r"$\Omega$: \ the weakest detector for consensus", font_size=36).to_edge(UP, buff=0.3)
        out = [[1, 1, 3, 3, 2, 2, 2], [2, 2, 2, 1, 2, 2, 2], [3, 1, 1, 3, 2, 2, 2], [4, 4, 2, None, None, None, None]]
        ys = [2.0, 1.25, 0.5, -0.25]
        x0, dx = -5.0, 0.8
        lanes = VGroup(*[Line([x0 - 0.45, y, 0], [x0 + 6.4 * dx, y, 0], color=GREY_D, stroke_width=1.4)
                         for y in ys])
        lnames = VGroup(*[MathTex(rf"p_{k + 1}", font_size=26).next_to(lanes[k], LEFT, buff=0.15)
                          for k in range(4)])
        cells = []
        for k, row in enumerate(out):
            line = VGroup()
            for s, v in enumerate(row):
                if v is None:
                    continue
                c = YES if (s >= 4 and v == 2) else GREY_B
                line.add(tag_box(f"p{v}", color=c, size=16, w=0.62, h=0.46).move_to([x0 + s * dx, ys[k], 0]))
            cells.append(line)
        x4 = cross(np.array([x0 + 3 * dx, ys[3], 0]))
        cut = DashedLine([x0 + 3.5 * dx, 2.45, 0], [x0 + 3.5 * dx, -0.6, 0], color=YES, stroke_width=1.6,
                         dash_length=0.08)
        cl = label(r"from here on: \ $p_2$, \ for ever", font_size=17, color=YES).next_to(cut, DOWN, buff=0.1)
        tl = label(r"time $\rightarrow$", font_size=17, color=GREY_B).next_to(lanes[3], DOWN, buff=0.2).align_to(
            lanes[3], LEFT)
        ill = note(r"illustrative", font_size=16).next_to(tl, DOWN, buff=0.1).align_to(tl, LEFT)
        W = 5.2
        notes = VGroup(
            wrapped_label(r"$\Omega$ outputs one trusted process, \ the \textbf{leader}; \ outputs may disagree "
                          r"and change", W, font_size=19, color=WHITE),
            wrapped_label(r"eventually every correct process trusts the same correct process, \ for ever", W,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.95, 1.4, 0])
        fs = 30
        thm = [MathTex(r"\mathcal{D}", r"\text{ solves consensus}", font_size=fs),
               MathTex(r"\mathcal{D}", r"\text{ can simulate }", r"\Omega", font_size=fs)]
        for t in thm:
            t.move_to([3.95, -0.2, 0])
        imp = MathTex(r"\Downarrow", font_size=30, color=HEAD).next_to(thm[0], DOWN, buff=0.12)
        thm[1].next_to(imp, DOWN, buff=0.12)
        src = label(r"Chandra, \ Hadzilacos and Toueg \ (1996)", font_size=17, color=HEAD).next_to(thm[1], DOWN,
                                                                                                 buff=0.15)
        foot = VGroup(
            wrapped_label(r"the proof reuses Chapter 5's valency argument: \ simulate runs with sampled detector "
                          r"outputs, \ find the step where the outcome becomes decided; \ the process taking it must "
                          r"be correct", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"$\Omega$ is equivalent to $\Diamond\mathcal{S}$, \ and it is the leader election of "
                          r"Paxos and Raft \ (Part 38): \ timing is needed for progress, \ never for safety", 12.4,
                          font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Is eventually strong the least a detector can offer? <bookmark mark='a'/> Omega outputs just one "
            "process, a leader. Outputs may disagree and change, and a trusted process may crash, "
            "<bookmark mark='b'/> but eventually every correct process trusts the same correct one for ever. "
            "<bookmark mark='c'/> In 1996 Chandra, Vassos Hadzilacos and Toueg proved that any detector with "
            "which consensus can be solved can simulate omega: it is the weakest. <bookmark mark='d'/> The proof "
            "reuses chapter five's valency argument: simulate runs with sampled detector outputs and find the "
            "step that decides the outcome; whoever takes it must be correct. <bookmark mark='e'/> Omega is "
            "equivalent to eventually strong, and it is the leader election of Paxos and Raft."
        ) as vo:
            self.play(FadeIn(head), Create(lanes), FadeIn(lnames), FadeIn(tl), FadeIn(ill))
            vo.wait_until("a")
            for s in range(4):
                self.play(*[FadeIn(c) for c in [cells[k][s] for k in range(4) if s < len(cells[k])]],
                          *([Create(x4)] if s == 3 else []), run_time=0.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*cells[k][4:])) for k in range(3)], lag_ratio=0.2),
                      Create(cut), FadeIn(cl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(thm[0]))
            self.play(FadeIn(imp), TransformMatchingTex(thm[0].copy(), thm[1]), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ phi accrual
    def accrual(self):
        head = label(r"Suspicion as a number", font_size=36).to_edge(UP, buff=0.3)
        mu, sd = 1.0, 0.25

        def pdf(x):
            return math.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))

        def phi(t):
            return -math.log10(max(0.5 * math.erfc((t - mu) / (sd * math.sqrt(2))), 1e-12))
        A = axes([0, 3, 0.5], [0, 1.8, 0.5], x_length=5.0, y_length=2.6, x_label=r"time since the last heartbeat",
                 y_label=r"how often each gap occurs", xticks=None, yticks=None)
        A.move_to([-3.7, 0.55, 0])
        ax = A.ax
        curve = ax.plot(pdf, x_range=[0, 3, 0.02], color=DATA, stroke_width=3)
        tk = ValueTracker(0.6)
        line = always_redraw(lambda: DashedLine(ax.c2p(tk.get_value(), 0), ax.c2p(tk.get_value(), 1.75),
                                                color=HEAD, stroke_width=2, dash_length=0.08))
        area = always_redraw(lambda: ax.get_area(curve, x_range=[tk.get_value(), 3], color=NO, opacity=0.45))
        pl = label(r"$P_{\mathrm{later}}(t)$", font_size=20, color=NO).move_to(ax.c2p(2.2, 0.75))
        unit = 0.27
        base = np.array([0.15, -0.95, 0])
        frame = Rectangle(width=0.4, height=8.6 * unit, stroke_color=GREY_C, stroke_width=1.4).move_to(
            base + UP * 8.6 * unit / 2)
        bar = always_redraw(lambda: Rectangle(width=0.36, height=max(0.01, min(8.5, phi(tk.get_value())) * unit),
                                              stroke_width=0, fill_color=HEAD if phi(tk.get_value()) < 8 else NO,
                                              fill_opacity=0.9).move_to(
            base + UP * max(0.01, min(8.5, phi(tk.get_value())) * unit) / 2))
        thr = DashedLine(base + UP * 8 * unit + LEFT * 0.35, base + UP * 8 * unit + RIGHT * 0.35, color=NO,
                         stroke_width=2, dash_length=0.06)
        thl = MathTex(r"\Phi", font_size=26, color=NO).next_to(thr, LEFT, buff=0.08)
        ml = MathTex(r"\varphi", font_size=30, color=HEAD).next_to(frame, DOWN, buff=0.12)
        fs = 28
        rows = [MathTex(r"P_{\mathrm{later}}(t)", r"=", r"1 - F(t)", font_size=fs),
                MathTex(r"\varphi(t)", r"=", r"-\log_{10}", r"P_{\mathrm{later}}(t)", font_size=fs),
                MathTex(r"\varphi(t) \ge \Phi", r"\iff", r"P_{\mathrm{later}}(t) \le 10^{-\Phi}", font_size=fs)]
        whys = [label(r"$F$ fitted to the recent gaps", font_size=18, color=GREY_B),
                label(r"Hayashibara, \ D\'efago, \ Yared and Katayama \ (2004)", font_size=18, color=GREY_B),
                label(r"suspect once a mistake would be that unlikely", font_size=18, color=YES)]
        col = stacked(rows, whys, buff=0.3).move_to([4.15, 0.75, 0])
        ill = note(r"illustrative gaps", font_size=16).next_to(A, DOWN, buff=0.15)
        foot = wrapped_label(r"SWIM \ (Das, \ Gupta and Motivala, \ 2002): \ ping a random member; \ if it is "
                             r"silent, \ ask a few others to ping it; \ spread the verdicts by gossip", 12.4,
                             font_size=19, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real systems turn suspicion into a number. <bookmark mark='a'/> The phi accrual detector of Naohiro "
            "Hayashibara and colleagues, from 2004, fits a distribution to the recent gaps between heartbeats. "
            "<bookmark mark='b'/> As time passes without a heartbeat, the chance that one is still on its way "
            "shrinks, <bookmark mark='c'/> and phi is minus its logarithm to base ten. <bookmark mark='d'/> "
            "Suspect when phi passes a threshold: a threshold of eight means a mistake would have probability one "
            "in a hundred million. <bookmark mark='e'/> And SWIM, from 2002, probes random members and spreads "
            "its verdicts by gossip, so detection costs each process the same however large the group."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(curve), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            self.add(area, line)
            self.play(FadeIn(pl), FadeIn(frame), FadeIn(ml), FadeIn(thr), FadeIn(thl))
            self.add(bar)
            vo.wait_until("b")
            self.play(tk.animate.set_value(1.5), run_time=2.5)
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(tk.animate.set_value(2.55), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, YES, load)
