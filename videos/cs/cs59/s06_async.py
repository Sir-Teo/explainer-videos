from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, load, tag_box

# valency colours: 0-valent blue, 1-valent purple, bivalent yellow (as in Chapter 4's hexagon)
V0, V1, VB = DATA, LAM, HEAD


def node(color=GREY_B, r=0.17, fill=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill)


def edge(a, b, tex=None, color=GREY_B, dashed=False, side=UP, size=24, buff=0.2):
    """An arrow between two mobjects, optionally labelled (MathTex) beside its middle."""
    if dashed:
        ar = DashedLine(a.get_center(), b.get_center(), buff=buff, color=color, stroke_width=2,
                        dash_length=0.08).add_tip(tip_length=0.16)
    else:
        ar = Arrow(a.get_center(), b.get_center(), buff=buff, color=color, stroke_width=2.5,
                   max_tip_length_to_length_ratio=0.18)
    if tex is None:
        return VGroup(ar)
    t = MathTex(tex, font_size=size, color=color).next_to(ar.get_center(), side, buff=0.1)
    return VGroup(ar, t)


def ladder_rows(rows, whys, x_row, x_why, y_top, dy):
    """Derivation rows (MathTex) left-aligned at x_row, their reasons (labels) at x_why, one line each."""
    for k, (r, w) in enumerate(zip(rows, whys)):
        y = y_top - k * dy
        r.move_to([0, y, 0]).align_to([x_row, 0, 0], LEFT)
        w.move_to([0, y, 0]).align_to([x_why, 0, 0], LEFT)
    return VGroup(*rows), VGroup(*whys)


class Async(VoiceoverScene):
    def construct(self):
        self.card()
        self.start()
        self.critical()
        self.commute()
        self.endless()
        self.benor()
        self.rounds()

    def card(self):
        card = chapter_card(5, r"Asynchrony: \ FLP and randomness", r"What exactly does one crash break, \ and how "
                            r"do coins repair it?", lit=(1983, 1985),
                            extra=((1983, r"Ben-Or: \ coins"), (1985, r"Fischer, \ Lynch and Paterson")), part=PART)
        with self.voiceover("Chapter five. Asynchrony: FLP and randomness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def start(self):
        head = label(r"Lemma 1: \ a bivalent place to start", font_size=36).to_edge(UP, buff=0.3)
        inputs = ["000", "100", "110", "111"]
        boxes = VGroup()
        for k, bits in enumerate(inputs):
            fr = RoundedRectangle(width=1.75, height=0.8, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.6,
                                  fill_color=BG, fill_opacity=1)
            bs = VGroup(*[MathTex(b, font_size=32, color=V0 if b == "0" else V1) for b in bits]).arrange(RIGHT,
                                                                                                       buff=0.38)
            bs.move_to(fr)
            nm = MathTex(rf"C_{k}", font_size=28, color=WHITE).next_to(fr, DOWN, buff=0.12)
            boxes.add(VGroup(fr, bs, nm))
        boxes.arrange(RIGHT, buff=1.1).next_to(head, DOWN, buff=1.0)
        pn = VGroup(*[MathTex(rf"p_{j + 1}", font_size=20, color=GREY_B).next_to(boxes[0][0], UP, buff=0.06).set_x(
            boxes[0][1][j].get_x()) for j in range(3)])
        links = VGroup(*[MathTex(rf"\overset{{p_{k + 1}}}{{\sim}}", font_size=30, color=GREY_B).move_to(
            (boxes[k][0].get_right() + boxes[k + 1][0].get_left()) / 2) for k in range(3)])

        def tag(k, txt, col):
            return label(txt, font_size=19, color=col).next_to(boxes[k][0], UP, buff=0.42)
        tags = [tag(0, r"0-valent", V0), tag(1, r"?", GREY_B), tag(2, r"?", GREY_B), tag(3, r"1-valent", V1)]
        sup = [tag(1, r"0-valent", V0), tag(2, r"1-valent", V1)]
        vnote = label(r"validity fixes the ends", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.25)
        fs = 30
        rows = [MathTex(r"C_1", r"\overset{p_2}{\sim}", r"C_2", font_size=fs),
                MathTex(r"\sigma(C_1)", r"\overset{p_2}{\sim}", r"\sigma(C_2)", font_size=fs),
                MathTex(r"d(\sigma(C_1))", r"=", r"d(\sigma(C_2))", font_size=fs),
                MathTex(r"0", r"=", r"1", font_size=fs)]
        rows[3][0].set_color(V0)
        rows[3][2].set_color(V1)
        whys = [label(r"they differ only in $p_2$'s input", font_size=19, color=GREY_B),
                label(r"run $\sigma$: \ $p_2$ crashed at the start; \ the others see the same", font_size=19,
                      color=GREY_B),
                label(r"same views, \ same decisions", font_size=19, color=GREY_B),
                label(r"but $C_1$ is 0-valent and $C_2$ 1-valent", font_size=19, color=NO)]
        rg, wg = ladder_rows(rows, whys, -5.6, -1.4, -0.75, 0.62)
        concl = label(r"so some starting configuration is bivalent", font_size=24, color=VB).next_to(wg, DOWN,
                                                                                                  buff=0.35)
        concl.set_x(0)
        bit2 = VGroup(boxes[1][1][1], boxes[2][1][1])
        crossed = VGroup(*[Line(b.get_corner(DL) + [-0.05, -0.05, 0], b.get_corner(UR) + [0.05, 0.05, 0], color=NO,
                                stroke_width=4) for b in bit2])
        with self.voiceover(
            "Part 38 told this theorem's story; here is the machinery of its proof. "
            "<bookmark mark='a'/> Three processes, any one of which may crash. Line up the starting configurations, "
            "changing one input at a time. All zeros must decide zero, and all ones must decide one. "
            "<bookmark mark='b'/> Suppose no start is bivalent. Then somewhere two neighbours have opposite "
            "valencies, here C one and C two. <bookmark mark='c'/> They differ only in process two's input. "
            "<bookmark mark='d'/> Run both with process two crashed from the very start. The others see exactly the "
            "same in both runs, so they decide the same. <bookmark mark='e'/> But one start was zero-valent and the "
            "other one-valent. So some start is bivalent: the inputs alone do not fix the outcome."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes), FadeIn(links), FadeIn(pn))
            self.play(FadeIn(tags[0]), FadeIn(tags[3]), FadeIn(tags[1]), FadeIn(tags[2]), FadeIn(vnote))
            vo.wait_until("b")
            self.play(ReplacementTransform(tags[1], sup[0]), ReplacementTransform(tags[2], sup[1]))
            vo.wait_until("c")
            self.play(boxes[1][0].animate.set_stroke(HEAD, width=2.6), boxes[2][0].animate.set_stroke(HEAD, width=2.6),
                      links[1].animate.set_color(HEAD), Indicate(bit2, color=HEAD))
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(Create(crossed), bit2.animate.set_opacity(0.35))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            self.play(FadeIn(concl, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def critical(self):
        head = label(r"Lemma 2: \ the step that would decide", font_size=36).to_edge(UP, buff=0.3)
        xs = [-6.0 + 1.45 * k for k in range(5)]
        E = VGroup(*[node(VB if k == 0 else GREY_B).move_to([x, 1.0, 0]) for k, x in enumerate(xs)])
        D = VGroup(*[node(GREY_D, fill=0.6).move_to([x, -1.0, 0]) for x in xs])
        ech = VGroup(*[edge(E[k], E[k + 1]) for k in range(4)])
        down = VGroup(*[edge(E[k], D[k], r"e", color=HEAD, side=RIGHT, size=22) for k in range(5)])
        cl = MathTex(r"C", font_size=26, color=VB).next_to(E[0], UP, buff=0.12)
        calC = label(r"$\mathcal{C}$: \ reached from $C$ without $e$", font_size=19, color=GREY_A).next_to(
            VGroup(E), UP, buff=0.75)
        calD = label(r"$\mathcal{D} = e(\mathcal{C})$", font_size=19, color=GREY_A).next_to(VGroup(D), DOWN,
                                                                                            buff=0.45)
        ill = note(r"illustrative", font_size=16).next_to(calD, DOWN, buff=0.12)
        dcol = [V0, V0, V1, V1, V1]
        c0 = MathTex(r"C_0", font_size=24, color=WHITE).next_to(E[1], UP, buff=0.12)
        c1 = MathTex(r"C_1", font_size=24, color=WHITE).next_to(E[2], UP, buff=0.12)
        ep = MathTex(r"e'", font_size=24, color=HEAD).next_to(ech[1], DOWN, buff=0.08)
        d0 = MathTex(r"D_0", font_size=24, color=V0).next_to(D[1], DOWN, buff=0.12)
        d1 = MathTex(r"D_1", font_size=24, color=V1).next_to(D[2], DOWN, buff=0.12)
        W = 5.5
        notes = VGroup(
            wrapped_label(r"$C$ bivalent; \ $e = (p, m)$ a pending step: \ $p$ receives $m$", W, font_size=19),
            wrapped_label(r"\textbf{claim}: \ some configuration in $\mathcal{D}$ is still bivalent, \ so the "
                          r"adversary can deliver $e$ and not decide", W, font_size=19, color=VB),
            wrapped_label(r"if not, \ $\mathcal{D}$ holds both valencies \ (from $C$ both decisions are reachable, "
                          r"\ before or after $e$)", W, font_size=19, color=GREY_A),
            wrapped_label(r"so two neighbours $C_0$ and $C_1 = e'(C_0)$ have $D_0 = e(C_0)$ 0-valent and "
                          r"$D_1 = e(C_1)$ 1-valent: \ a \textbf{decisive step}", W, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 0.0, 0])
        with self.voiceover(
            "The second step is the heart. <bookmark mark='a'/> Take a bivalent configuration C and any "
            "pending step e: process p receiving message m. Let the adversary take any other steps first, and only "
            "then apply e. <bookmark mark='b'/> The claim is that some of the results are still bivalent, so the "
            "adversary can deliver e without letting a decision happen. <bookmark mark='c'/> Suppose not, so every "
            "result is univalent. Both valencies must appear, because from C either decision can still be reached. "
            "<bookmark mark='d'/> So somewhere there are two neighbours, C zero and C one, one step e prime apart, "
            "where applying e to the first gives zero-valent and to the second one-valent. Call that a decisive "
            "step."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(E[0]), FadeIn(cl), FadeIn(notes[0]))
            self.play(LaggedStart(*[AnimationGroup(Create(ech[k]), FadeIn(E[k + 1])) for k in range(4)],
                                  lag_ratio=0.5), FadeIn(calC), run_time=2.0)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(down[k][0]), FadeIn(down[k][1]), FadeIn(D[k]))
                                    for k in range(5)], lag_ratio=0.3), FadeIn(calD), FadeIn(ill), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(*[D[k].animate.set_fill(dcol[k], opacity=0.9).set_stroke(dcol[k]) for k in range(5)],
                      FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(c0), FadeIn(c1), FadeIn(ep), ech[1][0].animate.set_color(HEAD), FadeIn(d0), FadeIn(d1))
            self.play(FadeIn(notes[3]))
            self.play(Indicate(VGroup(E[1], E[2], D[1], D[2]), color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def commute(self):
        head = label(r"Why there is no decisive step", font_size=36).to_edge(UP, buff=0.3)
        # case 1: e' is a step of another process
        c0 = node(GREY_B).move_to([-3.6, 1.65, 0])
        c1 = node(GREY_B).move_to([-5.1, 0.35, 0])
        dd0 = node(V0).move_to([-2.1, 0.35, 0])
        dd1 = node(V1).move_to([-3.6, -0.95, 0])
        lab1 = VGroup(MathTex(r"C_0", font_size=24).next_to(c0, UP, buff=0.1),
                      MathTex(r"C_1", font_size=24).next_to(c1, LEFT, buff=0.12),
                      MathTex(r"D_0", font_size=24, color=V0).next_to(dd0, RIGHT, buff=0.12),
                      MathTex(r"D_1", font_size=24, color=V1).next_to(dd1, DOWN, buff=0.1))
        a1 = VGroup(edge(c0, c1, r"e'", side=LEFT), edge(c0, dd0, r"e", color=HEAD, side=RIGHT),
                    edge(c1, dd1, r"e", color=HEAD, side=LEFT))
        a1x = edge(dd0, dd1, r"e'", color=NO, side=RIGHT)
        cap1 = label(r"case 1: \ $e'$ is a step of $p' \ne p$", font_size=21, color=WHITE).move_to([-3.6, 2.45, 0])
        fs = 28
        r1 = [MathTex(r"e'(e(C_0))", r"=", r"e(e'(C_0))", font_size=fs),
              MathTex(r"e'(D_0)", r"=", r"D_1", font_size=fs)]
        for r in r1:
            r.move_to([-3.6, -1.85, 0])
        w1 = label(r"different processes: \ the steps commute", font_size=18, color=GREY_B).next_to(r1[0], DOWN,
                                                                                                     buff=0.15)
        x1 = label(r"a 1-valent configuration below a 0-valent one", font_size=18, color=NO).next_to(w1, DOWN,
                                                                                                    buff=0.15)
        # case 2: e' is a step of p itself; run sigma without p
        C0 = node(GREY_B).move_to([3.3, 1.65, 0])
        D0 = node(V0).move_to([1.7, 0.6, 0])
        D1 = node(V1).move_to([4.9, 0.6, 0])
        A = node(VB).move_to([3.3, -0.6, 0])
        S0 = node(V0).move_to([1.7, -1.65, 0])
        S1 = node(V1).move_to([4.9, -1.65, 0])
        lab2 = VGroup(MathTex(r"C_0", font_size=24).next_to(C0, UP, buff=0.1),
                      MathTex(r"D_0", font_size=24, color=V0).next_to(D0, LEFT, buff=0.12),
                      MathTex(r"D_1", font_size=24, color=V1).next_to(D1, RIGHT, buff=0.12),
                      MathTex(r"A", font_size=26, color=VB).next_to(A, DOWN, buff=0.12),
                      MathTex(r"\sigma(D_0)", font_size=24, color=V0).next_to(S0, LEFT, buff=0.12),
                      MathTex(r"\sigma(D_1)", font_size=24, color=V1).next_to(S1, RIGHT, buff=0.12))
        a2 = VGroup(edge(C0, D0, r"e", color=HEAD, side=LEFT), edge(C0, D1, r"e',\,e", color=HEAD, side=RIGHT))
        sg = edge(C0, A, r"\sigma", color=YES, dashed=True, side=RIGHT)
        a2b = VGroup(edge(A, S0, r"e", color=HEAD, side=LEFT, size=22),
                     edge(A, S1, r"e',\,e", color=HEAD, side=RIGHT, size=22),
                     edge(D0, S0, r"\sigma", color=YES, dashed=True, side=LEFT, size=22),
                     edge(D1, S1, r"\sigma", color=YES, dashed=True, side=RIGHT, size=22))
        cap2 = label(r"case 2: \ $e'$ is a step of $p$: \ let $p$ sleep", font_size=21, color=WHITE).move_to(
            [3.3, 2.45, 0])
        w2 = wrapped_label(r"$\sigma$: \ a finite run from $C_0$ where $p$ takes no step and someone decides \ "
                           r"(one crash must be survived)", 5.4, font_size=18, color=GREY_B).move_to([3.3, -2.45, 0])
        x2 = label(r"$A$ reaches both valencies, \ yet $\sigma$ decided at $A$", font_size=18, color=NO).next_to(
            w2, DOWN, buff=0.15)
        sep = DashedLine([0.15, 2.6, 0], [0.15, -3.3, 0], color=GREY_D, stroke_width=1.2, dash_length=0.08)
        with self.voiceover(
            "Two cases destroy it. <bookmark mark='a'/> If e prime is a step of some process other than p, the two "
            "steps commute: applying them in either order gives the same configuration. <bookmark mark='b'/> "
            "Then D one is reachable from D zero, a one-valent configuration below a zero-valent one. Impossible. "
            "<bookmark mark='c'/> If e prime is a step of p itself, let p fall silent. "
            "A protocol that survives one crash must have a finite run from C zero, call it sigma, "
            "in which p never moves and someone decides. <bookmark mark='d'/> Sigma involves no step of p, so it "
            "commutes with both of p's steps. From its end A, one path reaches zero-valent, another one-valent. "
            "<bookmark mark='e'/> So A is bivalent, yet a decision was made there. Contradiction either way."
        ) as vo:
            self.play(FadeIn(head), Create(sep))
            vo.wait_until("a")
            self.play(FadeIn(cap1), FadeIn(c0), FadeIn(c1), FadeIn(dd0), FadeIn(dd1), FadeIn(lab1))
            self.play(LaggedStart(*[GrowArrow(a[0]) for a in a1], lag_ratio=0.3), FadeIn(VGroup(*[a[1] for a in a1])))
            self.play(FadeIn(r1[0]), FadeIn(w1))
            vo.wait_until("b")
            self.play(GrowArrow(a1x[0]), FadeIn(a1x[1]))
            self.play(TransformMatchingTex(r1[0], r1[1]))
            self.play(FadeIn(x1))
            vo.wait_until("c")
            self.play(FadeIn(cap2), FadeIn(C0), FadeIn(D0), FadeIn(D1), FadeIn(lab2[:3]),
                      *[GrowArrow(a[0]) for a in a2], *[FadeIn(a[1]) for a in a2])
            self.play(Create(sg[0]), FadeIn(sg[1]), FadeIn(A), FadeIn(lab2[3]), FadeIn(w2))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(Create(a[0]), FadeIn(a[1])) for a in a2b], lag_ratio=0.25),
                      FadeIn(S0), FadeIn(S1), FadeIn(lab2[4:]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(x2), Indicate(A, color=NO, scale_factor=1.6))
        self.wait(0.4)
        self.clear_scene()

    def endless(self):
        head = label(r"Lemma 3: \ a run that never decides", font_size=36).to_edge(UP, buff=0.3)
        n = 8
        xs = [-6.0 + 1.5 * k for k in range(n)]
        cs = VGroup(*[node(VB, r=0.2).move_to([x, 1.4, 0]) for x in xs])
        who = [r"p_1", r"p_2", r"p_3"] * 3
        arr = VGroup(*[edge(cs[k], cs[k + 1], who[k], color=GREY_B, side=UP, size=24) for k in range(n - 1)])
        dots = MathTex(r"\cdots", font_size=36, color=VB).next_to(cs[-1], RIGHT, buff=0.3)
        cap = wrapped_label(r"each stage: \ the next process in the queue receives its \textbf{oldest} message; \ "
                            r"Lemma 2 lets the adversary do it and land bivalent again", 12.0, font_size=20,
                            color=GREY_A).next_to(cs, DOWN, buff=0.45)
        ill = note(r"every configuration shown is bivalent", font_size=16).next_to(cap, DOWN, buff=0.12)
        checks = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"every process steps for ever", YES), (r"every message is delivered", YES),
            (r"no one crashes", YES), (r"no one decides", NO))]).arrange(RIGHT, buff=0.5).next_to(ill, DOWN, buff=0.45)
        if checks.width > 12.8:
            checks.width = 12.8
        thm = wrapped_label(r"\textbf{Fischer, \ Lynch and Paterson \ (1985)}: \ no deterministic protocol solves "
                            r"consensus in an asynchronous system if even one process may crash", 11.0, font_size=22,
                            color=WHITE)
        box = SurroundingRectangle(thm, buff=0.25, color=HEAD, corner_radius=0.1, stroke_width=2)
        tg = VGroup(box, thm).next_to(checks, DOWN, buff=0.5)
        with self.voiceover(
            "The third step builds the bad run. <bookmark mark='a'/> Keep the processes in a queue. At each stage, "
            "take the next process and the oldest message waiting for it; the second lemma lets the adversary "
            "deliver exactly that message and land in a bivalent configuration again. <bookmark mark='b'/> Repeat "
            "for ever. Every process takes infinitely many steps, every message arrives, nobody crashes, and nobody "
            "ever decides. <bookmark mark='c'/> That is the theorem of 1985. Notice that the crash never happens. "
            "Its mere possibility forces the protocol to wait, and waiting is what the adversary exploits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cs[0]))
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(ill))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arr[k][0]), FadeIn(arr[k][1]), FadeIn(cs[k + 1]))
                                    for k in range(n - 1)], lag_ratio=0.45), run_time=4.0)
            self.play(FadeIn(dots))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in checks], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tg))
        self.wait(0.4)
        self.clear_scene()

    def benor(self):
        head = label(r"Ben-Or: \ two votes and a coin", font_size=36).to_edge(UP, buff=0.3)
        prog = code_block(["phase r:", "  send x to all", "  wait for n - f values",
                           "  if > n/2 of all n say v:", "    propose v", "  else: propose ?",
                           "  wait for n - f proposals", "  if > f propose v: decide v", "  if any says v: x := v",
                           "  else: x := coin()"], size=19).move_to([-4.0, -0.2, 0])
        pbox = SurroundingRectangle(prog, buff=0.3, color=GREY_D, corner_radius=0.08, stroke_width=1.4)
        vote1 = SurroundingRectangle(VGroup(*prog[1:6]), buff=0.06, color=DATA, stroke_width=1.6)
        vote2 = SurroundingRectangle(VGroup(*prog[6:]), buff=0.06, color=KERN, stroke_width=1.6)
        v1l = label(r"vote 1", font_size=18, color=DATA).next_to(pbox, UP, buff=0.12).align_to(pbox, LEFT)
        v2l = label(r"vote 2", font_size=18, color=KERN).next_to(pbox, DOWN, buff=0.12).align_to(pbox, LEFT)
        props = ["1", "1", "1", "?", "?"]
        tags = VGroup(*[tag_box(t, color=V1 if t == "1" else GREY_B, size=22, w=0.6, h=0.6) for t in props])
        tags.arrange(RIGHT, buff=0.3).move_to([3.3, 1.75, 0])
        tl = label(r"the five proposals of one phase", font_size=17, color=GREY_A).next_to(tags, UP, buff=0.15)
        ill = note(r"illustrative: \ $n = 5$, \ $f = 2$", font_size=16).next_to(tags, DOWN, buff=0.12)
        hear = label(r"a process hears any $n - f = 3$", font_size=17, color=HEAD).next_to(ill, DOWN, buff=0.12)
        subsets = [(2, 3, 4), (0, 3, 4), (1, 2, 4)]

        def marks(s):
            return VGroup(*[SurroundingRectangle(tags[i], buff=0.07, color=HEAD, stroke_width=2.4) for i in s])
        fs = 27
        rows = [MathTex(r"\#\,v\text{-proposals}", r"\ge", r"f + 1", font_size=fs),
                MathTex(r"\#\,v\text{-proposals seen}", r"\ge", r"f + 1", r"-", r"f", font_size=fs),
                MathTex(r"\#\,v\text{-proposals seen}", r"\ge", r"1", font_size=fs)]
        rows[2][2].set_color(YES)
        whys = [label(r"someone decided $v$", font_size=18, color=GREY_B),
                label(r"each process misses at most $f$", font_size=18, color=GREY_B),
                label(r"so everyone adopts $v$, \ and next phase decides it", font_size=18, color=YES)]
        col = VGroup()
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
            col.add(VGroup(r, w))
        maj = wrapped_label(r"two values are never both proposed: \ each needs more than $n/2$ reports, \ and two "
                            r"majorities share a process", 6.0, font_size=18, color=DATA).next_to(hear, DOWN, buff=0.3)
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(maj, DOWN, buff=0.35).set_x(3.3)
        with self.voiceover(
            "Michael Ben-Or's protocol of 1983 escapes by flipping coins, and survives any minority of crashes. "
            "<bookmark mark='a'/> Each phase has two votes. First every process sends its value and waits for n "
            "minus f of them. If more than half of all n processes reported the same value, it proposes that value, "
            "otherwise a question mark. <bookmark mark='b'/> Then it waits for n minus f proposals. More than f "
            "proposals of v: decide v. At least one: adopt v. None: flip a coin. <bookmark mark='c'/> Why is it "
            "safe? Two different values are never proposed in one phase, since each would need a majority of "
            "reports. <bookmark mark='d'/> And if anyone decides v, more than f processes proposed it. Every "
            "process misses at most f proposals, so each sees a v and adopts it, <bookmark mark='e'/> and the next "
            "phase decides v everywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pbox), FadeIn(prog))
            vo.wait_until("a")
            self.play(Create(vote1), FadeIn(v1l))
            vo.wait_until("b")
            self.play(Create(vote2), FadeIn(v2l))
            vo.wait_until("c")
            self.play(FadeIn(maj))
            vo.wait_until("d")
            self.play(FadeIn(tags), FadeIn(tl), FadeIn(ill), FadeIn(hear))
            m = marks(subsets[0])
            self.play(Create(m), run_time=0.6)
            for s in subsets[1:]:
                self.play(Transform(m, marks(s)), run_time=0.6)
            self.play(FadeIn(col[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def rounds(self):
        bo = load("benor")["rows"]
        head = label(r"How long the coins take", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        rows = [MathTex(r"\Pr[\text{all coins agree}]", r"\ge", r"2^{-n}", font_size=fs),
                MathTex(r"\Pr[T > t]", r"\le", r"(1 - 2^{-n})^{t}", font_size=fs),
                MathTex(r"\mathbb{E}[T]", r"=", r"\sum_{t \ge 0} \Pr[T > t]", r"\le", r"\sum_{t \ge 0}",
                        r"(1 - 2^{-n})^{t}", font_size=fs),
                MathTex(r"\mathbb{E}[T]", r"\le", r"2^{n}", font_size=fs)]
        rows[3][2].set_color(HEAD)
        whys = [label(r"every flipper lands on the value the others hold", font_size=18, color=GREY_B),
                label(r"each phase is a fresh try", font_size=18, color=GREY_B),
                label(r"a geometric series", font_size=18, color=GREY_B),
                label(r"then one more phase to decide", font_size=18, color=GREY_B)]
        col = VGroup()
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
            col.add(VGroup(r, w))
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.5, 0.15, 0]).align_to([-6.6, 0, 0], LEFT)
        tdef = label(r"$T$: \ phases until every live process holds the same value", font_size=18,
                     color=GREY_A).next_to(col, UP, buff=0.3).align_to(col, LEFT)
        ch = bar_chart([r["mean_rounds"] for r in bo], [rf"$n = {r['n']}$" for r in bo], [KERN] * len(bo),
                       height=2.6, bar_w=0.75, gap=0.5, fmt_=lambda v: f"{v:.1f}", font_size=19)
        ch.move_to([3.7, 0.1, 0])
        ct = label(r"mean phases to decide", font_size=20, color=KERN).next_to(ch, UP, buff=0.3)
        fl = label(r"$f = " + r",\ ".join(str(r["f"]) for r in bo) + r"$ crashed; \ inputs split half and half",
                   font_size=17, color=GREY_A).next_to(ch, DOWN, buff=0.2)
        mx = label(r"longest run: \ " + r",\ ".join(str(r["max_rounds"]) for r in bo) + r" phases", font_size=17,
                   color=GREY_A).next_to(fl, DOWN, buff=0.1)
        ok = all(r["agreement"] == 1.0 and r["terminated"] == 1.0 for r in bo)
        agr = label(r"every run agreed and ended" if ok else r"some runs failed", font_size=17,
                    color=YES if ok else NO).next_to(mx, DOWN, buff=0.1)
        src = note(r"theory.py, \ 200 runs each: \ crashes at the start, \ then only the coins differ", font_size=16).next_to(agr, DOWN, buff=0.1)
        foot = wrapped_label(r"private coins: \ the wait can grow exponentially with $n$; \ a common coin, \ seen "
                             r"alike by all, \ makes it constant", 12.4, font_size=19, color=HEAD).to_edge(DOWN,
                                                                                                    buff=0.25)
        with self.voiceover(
            "Safety never depends on the coins; termination does. <bookmark mark='a'/> In any phase, the processes "
            "that flip may all land on the value the others hold, with probability at least one over two to the n. "
            "<bookmark mark='b'/> Each phase is a fresh try, so failing t phases in a row has probability at most "
            "one minus two to the minus n, to the power t, <bookmark mark='c'/> and the expected wait is at most "
            "two to the n phases, plus one to decide. <bookmark mark='d'/> Our instrument ran it with split inputs "
            "and just under half the processes crashed. Four processes took four point eight phases on average; "
            "six, nine point three; eight, eighteen point two; ten, thirty-three point nine. <bookmark mark='e'/> "
            "Every run agreed and ended, but the mean roughly doubles with every two processes. A common coin, "
            "seen alike by everyone, makes it constant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tdef))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("d")
            self.play(FadeIn(ct), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(fl))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v)) for b, v in
                                    zip(ch.bars, ch.vals)], lag_ratio=0.5), run_time=3.0)
            self.play(FadeIn(mx), FadeIn(agr), FadeIn(src))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, NO, YES)
