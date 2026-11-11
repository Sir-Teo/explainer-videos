from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES

COIN, TEA = r"\mathit{coin}", r"\mathit{tea}"
NCOIN, NTEA = r"\overline{\mathit{coin}}", r"\overline{\mathit{tea}}"

# The deadlock example (illustrative, enumerated by hand): thread 1 grabs a, grabs b, releases b, releases a; thread 2
# grabs b, grabs a, releases a, releases b.  A state is (steps taken by thread 1, steps taken by thread 2).
REACH = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 3), (1, 4), (2, 0), (2, 4), (3, 0), (3, 1),
         (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
CLASH = [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]  # both threads would hold the same lock


def fit(m, w):
    """Scale a mobject down to width w if it is wider."""
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def keep_in(m, x0=-6.85, x1=6.85):
    """Shift a mobject sideways so that it lies inside [x0, x1]."""
    if m.get_right()[0] > x1:
        m.shift(LEFT * (m.get_right()[0] - x1))
    if m.get_left()[0] < x0:
        m.shift(RIGHT * (x0 - m.get_left()[0]))
    return m


def node(tex, pos, color=GREY_B, r=0.32, fs=24):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.2, fill_color=BG, fill_opacity=1).move_to(pos)
    return VGroup(c, MathTex(tex, font_size=fs, color=color).move_to(c))


def step(a, b, act, color=GREY_B, fs=24):
    """A labelled transition between two nodes, label above."""
    arr = Arrow(a.get_center(), b.get_center(), buff=0.36, color=color, stroke_width=2.6,
                max_tip_length_to_length_ratio=0.15)
    return VGroup(arr, MathTex(act, font_size=fs, color=color).next_to(arr, UP, buff=0.08))


def rule(name, premise, concl, fs=30, color=WHITE):
    """An inference rule: premise over a line over the conclusion, its name on the left."""
    c = MathTex(concl, font_size=fs, color=color)
    p = MathTex(premise, font_size=fs, color=color) if premise else VectorizedPoint()
    ln = Line(LEFT, RIGHT, color=GREY_B, stroke_width=2)
    ln.set_width(max(c.width, p.width) + 0.3)
    g = VGroup(p, ln, c).arrange(DOWN, buff=0.12)
    if not premise:
        p.move_to(ln.get_center() + UP * 0.2)
    n = label(rf"\textsc{{{name}}}", font_size=20, color=HEAD).next_to(ln, LEFT, buff=0.2)
    return VGroup(n, g)


class Concurrency(VoiceoverScene):
    def construct(self):
        self.card()
        self.syntax()
        self.rules()
        self.derivation()
        self.pi()
        self.deadlock()

    def card(self):
        card = chapter_card(10, r"Processes and channels", r"What does a program mean when it talks to others?",
                            lit=(1978, 1980, 1992),
                            extra=((1978, r"Hoare: \ CSP"), (1980, r"Milner: \ CCS"),
                                   (1992, r"Milner, \ Parrow, \ Walker: \ the $\pi$-calculus")), part=PART)
        with self.voiceover("Chapter ten. Processes and channels. What does a program mean when it talks to "
                            "others?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ CCS: the grammar, and two parts
    def syntax(self):
        head = label(r"CCS: \ a calculus of communicating systems", font_size=36).to_edge(UP, buff=0.3)
        fs = 30
        act = VGroup(MathTex(r"\alpha", r"::=", r"a", r"\ \big|\ ", r"\bar{a}", r"\ \big|\ ", r"\tau", font_size=fs,
                             color=HEAD),
                     label(r"receive on $a$, \ send on $a$, \ a silent internal step", font_size=18, color=GREY_B))
        act.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        prods = [(r"0", r"does nothing"), (r"\alpha.P", r"does $\alpha$, \ then behaves as $P$"),
                 (r"P + Q", r"a choice"), (r"P \mid Q", r"in parallel"), (r"(\nu a)\,P", r"$a$ is private to $P$"),
                 (r"A", r"a named process, \ perhaps recursive")]
        prow = VGroup()
        for k, (t, g) in enumerate(prods):
            y = 1.15 - 0.55 * k
            lead = MathTex(r"P ::=" if k == 0 else r"\big|", font_size=fs, color=WHITE)
            lead.move_to([0, y, 0]).align_to(np.array([-5.3, 0, 0]), RIGHT)
            m = MathTex(t, font_size=fs, color=WHITE).move_to([0, y, 0]).align_to(np.array([-5.05, 0, 0]), LEFT)
            gg = label(g, font_size=18, color=GREY_B).move_to([0, y, 0]).align_to(np.array([-3.3, 0, 0]), LEFT)
            prow.add(VGroup(lead, m, gg))
        act.next_to(prow, UP, buff=0.4).align_to(np.array([-6.2, 0, 0]), LEFT)
        dc = MathTex(r"C \stackrel{\mathrm{def}}{=} " + NCOIN + r".\," + TEA + r".\,0", font_size=28, color=DATA)
        dv = MathTex(r"V \stackrel{\mathrm{def}}{=} " + COIN + r".\," + NTEA + r".\,V", font_size=28, color=LAM)
        defs = VGroup(dc, dv).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 2.2, 0])
        keep_in(defs)
        bc = Circle(radius=0.6, stroke_color=DATA, stroke_width=2.4, fill_color=BG, fill_opacity=1).move_to(
            [2.6, 0.0, 0])
        bv = Circle(radius=0.6, stroke_color=LAM, stroke_width=2.4, fill_color=BG, fill_opacity=1).move_to(
            [5.6, 0.0, 0])
        lc = MathTex("C", font_size=32, color=DATA).move_to(bc)
        lv = MathTex("V", font_size=32, color=LAM).move_to(bv)
        pc = [bc.point_at_angle(PI / 5), bc.point_at_angle(-PI / 5)]
        pv = [bv.point_at_angle(PI - PI / 5), bv.point_at_angle(PI + PI / 5)]
        ports = VGroup(*[Dot(p, radius=0.07, color=WHITE) for p in pc + pv])
        plab = VGroup(MathTex(NCOIN, font_size=20).next_to(pc[0], UP, buff=0.1),
                      MathTex(TEA, font_size=20).next_to(pc[1], DOWN, buff=0.1),
                      MathTex(COIN, font_size=20).next_to(pv[0], UP, buff=0.1),
                      MathTex(NTEA, font_size=20).next_to(pv[1], DOWN, buff=0.1))
        wires = VGroup(Line(pc[0], pv[0], color=HEAD, stroke_width=3), Line(pc[1], pv[1], color=HEAD, stroke_width=3))
        res = DashedVMobject(RoundedRectangle(width=4.9, height=2.1, corner_radius=0.3, color=KERN, stroke_width=2),
                             num_dashes=40).move_to([4.1, 0.0, 0])
        resl = MathTex(r"(\nu\," + COIN + r", " + TEA + r")", font_size=24, color=KERN).next_to(res, DOWN, buff=0.1)
        csp = wrapped_label(r"Hoare's CSP \ (1978): \ synchronous messages between processes; \ Go's channels "
                            r"descend from it", 6.3, font_size=19, color=GREY_A)
        csp.next_to(resl, DOWN, buff=0.4).set_x(4.0)
        keep_in(csp)
        with self.voiceover(
            "Chapter five compared machines; now we build them from parts. Robin Milner's Calculus of Communicating "
            "Systems, of nineteen eighty, has a tiny grammar. <bookmark mark='a'/> An action is a name a, its "
            "complement a bar, or tau, a silent internal step. <bookmark mark='b'/> A process is zero, which does "
            "nothing; an action followed by a process; a choice; two processes in parallel; a restriction, which "
            "makes a name private; or a named process, which may call itself. <bookmark mark='c'/> A customer offers "
            "a coin, then waits for tea. <bookmark mark='d'/> A machine accepts a coin, offers tea, and starts "
            "again. <bookmark mark='e'/> Side by side, complementary ports join, and restriction hides both names "
            "from everyone else. <bookmark mark='f'/> Tony Hoare's CSP, of nineteen seventy-eight, also built "
            "programs from processes that exchange synchronous messages; Go's channels descend from it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(act[0]), FadeIn(act[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in prow], lag_ratio=0.35), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(dc), Create(bc), FadeIn(lc), FadeIn(ports[:2]), FadeIn(plab[:2]))
            vo.wait_until("d")
            self.play(FadeIn(dv), Create(bv), FadeIn(lv), FadeIn(ports[2:]), FadeIn(plab[2:]))
            vo.wait_until("e")
            self.play(Create(wires[0]), Create(wires[1]))
            self.play(Create(res), FadeIn(resl))
            vo.wait_until("f")
            self.play(FadeIn(csp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the transition rules
    def rules(self):
        head = label(r"The rules of motion", font_size=36).to_edge(UP, buff=0.3)
        ar = r"\xrightarrow{\alpha}"
        rs = [
            rule("Act", "", r"\alpha.P " + ar + r" P"),
            rule("Sum", r"P " + ar + r" P'", r"P + Q " + ar + r" P'"),
            rule("Par", r"P " + ar + r" P'", r"P \mid Q " + ar + r" P' \mid Q"),
            rule("Com", r"P \xrightarrow{a} P' \qquad Q \xrightarrow{\bar{a}} Q'",
                 r"P \mid Q \xrightarrow{\tau} P' \mid Q'", color=HEAD),
            rule("Res", r"P " + ar + r" P' \qquad \alpha \notin \{a, \bar{a}\}",
                 r"(\nu a)\,P " + ar + r" (\nu a)\,P'"),
        ]
        top = VGroup(*rs[:3]).arrange(RIGHT, buff=0.7, aligned_edge=DOWN)
        bot = VGroup(*rs[3:]).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
        VGroup(top, bot).arrange(DOWN, buff=0.75).next_to(head, DOWN, buff=0.6)
        fit(top, 13.2)
        fit(bot, 13.2)
        glosses = [r"do the action, \ become the rest", r"either side; \ the other is dropped",
                   r"one side moves alone", r"complementary actions meet: \ one silent step",
                   r"a private name is invisible outside; \ $\tau$ passes"]
        gl = VGroup(*[label(g, font_size=18, color=GREY_B).next_to(r[1], DOWN, buff=0.18) for g, r in zip(glosses, rs)])
        foot = wrapped_label(r"with mirror images of \textsc{Sum}, \ \textsc{Par} and \textsc{Com}, \ and a rule that "
                             r"unfolds named processes: \ chapter one's style \ (Plotkin's structural operational "
                             r"semantics, \ 1981), \ now with labels", 12.4, font_size=20, color=WHITE)
        foot.next_to(bot, DOWN, buff=1.0)
        with self.voiceover(
            "The meaning of a process is a labelled transition system, given by rules in the style of chapter one. "
            "<bookmark mark='a'/> An action prefix can do its action and become the rest. <bookmark mark='b'/> A "
            "choice can do whatever either side can, and the other side is dropped. <bookmark mark='c'/> In "
            "parallel, either side may move alone, the other unchanged. <bookmark mark='d'/> The heart is "
            "communication: if one side can do a and the other a bar, together they take a silent tau step, both "
            "moving at once. <bookmark mark='e'/> And a restricted name cannot be used from outside: a move on a or "
            "a bar is blocked, but tau passes through. <bookmark mark='f'/> These five rules, with their mirror "
            "images and one for unfolding named processes, are all of CCS."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(rs[k], shift=UP * 0.1), FadeIn(gl[k]))
                if k == 3:
                    self.play(Circumscribe(rs[3][1], color=HEAD))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ deriving one communication
    def derivation(self):
        head = label(r"Deriving a communication", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        lc = MathTex(NCOIN + r".\," + TEA + r".\,0", r"\xrightarrow{" + NCOIN + r"}", TEA + r".\,0", font_size=fs,
                     color=DATA)
        lv = MathTex(COIN + r".\," + NTEA + r".\,V", r"\xrightarrow{" + COIN + r"}", NTEA + r".\,V", font_size=fs,
                     color=LAM)
        leaves = VGroup(lc, lv).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.55)
        l1 = Line(LEFT, RIGHT, color=GREY_B, stroke_width=2).set_width(leaves.width + 0.3).next_to(leaves, DOWN,
                                                                                                  buff=0.14)
        mid = MathTex(r"C", r"\mid", r"V", r"\xrightarrow{\tau}", TEA + r".\,0", r"\mid", NTEA + r".\,V",
                      font_size=fs, color=HEAD).next_to(l1, DOWN, buff=0.14)
        R = r"(\nu\," + COIN + r", " + TEA + r")"
        root = MathTex(R, r"(", r"C", r"\mid", r"V", r")", r"\xrightarrow{\tau}", R, r"(", TEA + r".\,0", r"\mid",
                       NTEA + r".\,V", r")", font_size=fs, color=YES)
        l2 = Line(LEFT, RIGHT, color=GREY_B, stroke_width=2).set_width(root.width + 0.3).next_to(mid, DOWN,
                                                                                                buff=0.14)
        root.next_to(l2, DOWN, buff=0.14)
        n_act = VGroup(label(r"\textsc{Act}", font_size=19, color=HEAD).next_to(lc, LEFT, buff=0.25),
                       label(r"\textsc{Act}", font_size=19, color=HEAD).next_to(lv, RIGHT, buff=0.25))
        n_com = label(r"\textsc{Com}", font_size=19, color=HEAD).next_to(l1, RIGHT, buff=0.2)
        n_res = label(r"\textsc{Res}", font_size=19, color=HEAD).next_to(l2, RIGHT, buff=0.2)
        unf = note(r"($C$ and $V$ unfolded)", font_size=16).next_to(leaves, UP, buff=0.1)
        y = -1.55
        s0 = node(r"S_0", [-5.4, y, 0], YES)
        s1 = node(r"S_1", [-3.3, y, 0], GREY_A)
        s2 = node(r"S_2", [-1.2, y, 0], GREY_A)
        t1 = step(s0, s1, r"\tau", HEAD)
        t2 = step(s1, s2, r"\tau", HEAD)
        stl = label(r"$S_2 = $ the customer gone, \ the machine waiting: \ no move", font_size=18,
                    color=GREY_B).next_to(VGroup(s0, s2), DOWN, buff=0.25)
        wk = VGroup(MathTex(r"S_0", r"\approx", r"0", font_size=36, color=YES),
                    wrapped_label(r"weak bisimulation \ (Milner): \ chapter five's game, \ with $\tau$ steps unseen",
                                  5.3, font_size=19, color=GREY_A)).arrange(DOWN, buff=0.15)
        wk.move_to([3.6, y + 0.05, 0])
        cong = wrapped_label(r"strong bisimilarity is preserved by every CCS operator: \ equal parts can be swapped "
                             r"inside any system", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Let us derive the customer's first step. <bookmark mark='a'/> By the action rule, the customer, "
            "unfolded, can do coin bar and become tea, then zero. <bookmark mark='b'/> The machine can do coin and "
            "become tea bar, then V. <bookmark mark='c'/> The communication rule joins them: together they take a "
            "tau step to the two remainders. <bookmark mark='d'/> Restriction lets tau through, so the closed system "
            "moves. Every step of a system is a small proof like this one. <bookmark mark='e'/> The closed system "
            "has just two tau steps, coin and then tea, after which nothing more can happen. <bookmark mark='f'/> "
            "Chapter five's bisimulation applies, with tau steps treated as unobservable: Milner's weak "
            "bisimulation. Seen from outside, this system is equivalent to zero. <bookmark mark='g'/> And strong "
            "bisimilarity is preserved by every operator of CCS, so equal parts can be swapped inside any system."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(lc), FadeIn(n_act[0]), FadeIn(unf))
            vo.wait_until("b")
            self.play(Write(lv), FadeIn(n_act[1]))
            vo.wait_until("c")
            self.play(Create(l1), FadeIn(n_com))
            self.play(TransformMatchingTex(VGroup(lc, lv).copy(), mid), run_time=1.3)
            vo.wait_until("d")
            self.play(Create(l2), FadeIn(n_res))
            self.play(TransformMatchingTex(mid.copy(), root), run_time=1.3)
            vo.wait_until("e")
            self.play(FadeIn(s0))
            self.play(GrowArrow(t1[0]), FadeIn(t1[1]), FadeIn(s1))
            self.play(GrowArrow(t2[0]), FadeIn(t2[1]), FadeIn(s2))
            self.play(FadeIn(stl))
            vo.wait_until("f")
            self.play(FadeIn(wk))
            vo.wait_until("g")
            self.play(FadeIn(cong))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the pi-calculus: names travel
    def pi(self):
        head = label(r"The $\pi$-calculus: \ names travel", font_size=36).to_edge(UP, buff=0.3)
        rule_ = MathTex(r"\bar{x}\langle y\rangle.P", r"\ \mid\ ", r"x(z).Q", r"\ \longrightarrow\ ", r"P",
                        r"\ \mid\ ", r"Q\{y/z\}", font_size=34).next_to(head, DOWN, buff=0.4)
        rule_[0].set_color(DATA)
        rule_[2].set_color(LAM)
        rgl = label(r"send $y$ on $x$; \ receive a name on $x$ as $z$; \ the receiver continues with $y$ for $z$",
                    font_size=19, color=GREY_B).next_to(rule_, DOWN, buff=0.15)
        # the picture: a server with a private channel, a client, a public channel s
        y = -0.85
        sv = Circle(radius=0.55, stroke_color=DATA, stroke_width=2.4, fill_color=BG, fill_opacity=1).move_to(
            [-5.3, y, 0])
        cl = Circle(radius=0.55, stroke_color=LAM, stroke_width=2.4, fill_color=BG, fill_opacity=1).move_to(
            [-2.0, y, 0])
        svl = label(r"server", font_size=18, color=DATA).next_to(sv, DOWN, buff=0.12)
        cll = label(r"client", font_size=18, color=LAM).next_to(cl, DOWN, buff=0.12)
        pub = Line(sv.get_right(), cl.get_left(), color=GREY_B, stroke_width=3).shift(UP * 0.2)
        publ = MathTex("s", font_size=24, color=GREY_B).next_to(pub, UP, buff=0.08)
        rdot = Dot(sv.get_center() + DOWN * 0.15, radius=0.09, color=HEAD)
        rlab = MathTex("r", font_size=24, color=HEAD).next_to(rdot, UP, buff=0.06)
        scope0 = DashedVMobject(Ellipse(width=1.7, height=2.0, color=KERN, stroke_width=2), num_dashes=28).move_to(sv)
        scope1 = DashedVMobject(Ellipse(width=5.4, height=2.3, color=KERN, stroke_width=2),
                                num_dashes=56).move_to(VGroup(sv, cl))
        nul = MathTex(r"(\nu r)", font_size=24, color=KERN).next_to(scope0, UP, buff=0.08)
        nul1 = MathTex(r"(\nu r)", font_size=24, color=KERN).next_to(scope1, UP, buff=0.08)
        priv = Line(sv.get_right() + DOWN * 0.25, cl.get_left() + DOWN * 0.25, color=HEAD, stroke_width=4)
        privl = MathTex("r", font_size=24, color=HEAD).next_to(priv, DOWN, buff=0.08)
        msg = Dot(pub.get_start(), radius=0.1, color=HEAD).set_z_index(5)
        fs = 28
        e0 = MathTex(r"(\nu r)", r"(", r"\bar{s}\langle r\rangle.P", r")", r"\mid", r"s(z).Q", font_size=fs)
        e1 = MathTex(r"\equiv", r"(\nu r)", r"(", r"\bar{s}\langle r\rangle.P", r"\mid", r"s(z).Q", r")",
                     font_size=fs)
        e2 = MathTex(r"\longrightarrow", r"(\nu r)", r"(", r"P", r"\mid", r"Q\{r/z\}", r")", font_size=fs, color=YES)
        eqs = VGroup(e0, e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([2.9, -0.3, 0])
        e1.shift(RIGHT * 0.3)
        e2.shift(RIGHT * 0.3)
        ew = VGroup(label(r"$r$ is private to the server", font_size=18, color=GREY_B),
                    label(r"widen the scope: \ allowed, \ $r$ is not free in $s(z).Q$", font_size=18, color=KERN),
                    label(r"the message passes: \ the client now holds $r$", font_size=18, color=YES))
        for w, e in zip(ew, eqs):
            w.next_to(e, DOWN, buff=0.08).align_to(e, LEFT)
        for k in (1, 2):
            eqs[k].shift(DOWN * 0.3 * k)
            ew[k].shift(DOWN * 0.3 * k)
        keep_in(VGroup(eqs, ew))
        foot = wrapped_label(r"\textbf{scope extrusion}: \ links between processes are data; \ a request carrying its "
                             r"own reply channel, \ as in Go, \ is exactly this", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In CCS the wiring is fixed: who can talk to whom never changes. <bookmark mark='a'/> The pi-calculus of "
            "Milner, Joachim Parrow and David Walker, from nineteen ninety-two, sends names over names. Send y on "
            "channel x; receive a name on x and call it z. When they meet, the receiver continues with y in place of "
            "z. <bookmark mark='b'/> Now a server makes a private channel r, <bookmark mark='c'/> and wants to send "
            "it to a client over the public channel s. <bookmark mark='d'/> First, the scope of r is widened to "
            "include the client, which is allowed because the client does not mention r. <bookmark mark='e'/> Then "
            "the message passes, and the client holds r. The scope has extruded: the two now share a private link "
            "that no one else can reach. <bookmark mark='f'/> Links between processes are data. A request that "
            "carries its own reply channel, as in Go, is exactly this."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rule_), FadeIn(rgl))
            vo.wait_until("b")
            self.play(Create(sv), FadeIn(svl), FadeIn(rdot), FadeIn(rlab), Create(scope0), FadeIn(nul))
            self.play(Write(e0), FadeIn(ew[0]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(cll), Create(pub), FadeIn(publ))
            vo.wait_until("d")
            self.play(ReplacementTransform(scope0, scope1), ReplacementTransform(nul, nul1), run_time=1.3)
            self.play(TransformMatchingTex(e0.copy(), e1), FadeIn(ew[1]), run_time=1.3)
            vo.wait_until("e")
            self.add(msg)
            self.play(msg.animate.move_to(pub.get_end()), run_time=0.9)
            self.play(FadeOut(msg), Create(priv), FadeIn(privl))
            self.play(TransformMatchingTex(e1.copy(), e2), FadeIn(ew[2]), run_time=1.3)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ deadlock: a reachable stuck state
    def deadlock(self):
        head = label(r"Deadlock: \ a reachable stuck state", font_size=36).to_edge(UP, buff=0.3)
        fs = 26
        g = [r"\overline{g_a}", r"\overline{g_b}", r"\overline{r_b}", r"\overline{r_a}"]
        h = [r"\overline{g_b}", r"\overline{g_a}", r"\overline{r_a}", r"\overline{r_b}"]
        defs = VGroup(
            MathTex(r"K_x \stackrel{\mathrm{def}}{=} g_x.\,r_x.\,K_x", font_size=fs, color=KERN),
            MathTex(r"T_1 \stackrel{\mathrm{def}}{=} " + r".\,".join(g) + r".\,0", font_size=fs, color=DATA),
            MathTex(r"T_2 \stackrel{\mathrm{def}}{=} " + r".\,".join(h) + r".\,0", font_size=fs, color=LAM),
            MathTex(r"(\nu\, g, r)\,(T_1 \mid T_2 \mid K_a \mid K_b)", font_size=fs, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.45)
        dgl = VGroup(label(r"a lock: \ grab, \ then release \ (Part 33)", font_size=17, color=GREY_B),
                     label(r"grabs $a$, \ then $b$", font_size=17, color=GREY_B),
                     label(r"grabs $b$, \ then $a$", font_size=17, color=GREY_B))
        for d, r in zip(dgl, defs):
            d.next_to(r, RIGHT, buff=0.25)
        # the state grid
        step_ = 0.7
        O = np.array([0.45, -2.55, 0])

        def P(i, j):
            return O + RIGHT * step_ * i + UP * step_ * j

        frame = VGroup(Line(P(0, 0), P(4, 0) + RIGHT * 0.35, color=GREY_D, stroke_width=1.5),
                       Line(P(0, 0), P(0, 4) + UP * 0.35, color=GREY_D, stroke_width=1.5))
        xl = VGroup(*[MathTex(g[i], font_size=18, color=DATA).move_to((P(i, 0) + P(i + 1, 0)) / 2 + DOWN * 0.3)
                      for i in range(4)])
        yl = VGroup(*[MathTex(h[j], font_size=18, color=LAM).move_to((P(0, j) + P(0, j + 1)) / 2 + LEFT * 0.35)
                      for j in range(4)])
        ax1 = MathTex(r"T_1", font_size=22, color=DATA).next_to(P(4, 0), RIGHT, buff=0.45)
        ax2 = MathTex(r"T_2", font_size=22, color=LAM).next_to(P(0, 4), UP, buff=0.4)
        clash = VGroup(*[Square(side_length=0.5, stroke_width=0, fill_color=NO, fill_opacity=0.3).move_to(P(i, j))
                         for i, j in CLASH])
        reach = set(REACH)
        unreach = [(i, j) for i in range(5) for j in range(5) if (i, j) not in reach and (i, j) not in CLASH]
        ghost = VGroup(*[Dot(P(i, j), radius=0.05, color=GREY_D) for i, j in unreach])
        dots = {s: Dot(P(*s), radius=0.09, color=GREY_A) for s in REACH}
        edges = {}
        for (i, j) in REACH:
            for t in ((i + 1, j), (i, j + 1)):
                if t in reach:
                    edges[((i, j), t)] = Line(P(i, j), P(*t), color=GREY_B, stroke_width=2)
        stuck = [s for s in REACH if not any(e[0] == s for e in edges)]
        layers = {}
        for s in REACH:
            layers.setdefault(s[0] + s[1], []).append(s)
        legend = VGroup(
            VGroup(Dot(radius=0.09, color=NO), wrapped_label(r"deadlock: \ each holds one lock \ and waits for the "
                                                             r"other", 2.7, font_size=17, color=NO)),
            VGroup(Dot(radius=0.09, color=YES), label(r"finished", font_size=17, color=YES)),
            VGroup(Square(side_length=0.22, stroke_width=0, fill_color=NO, fill_opacity=0.3),
                   label(r"both would hold one lock", font_size=17, color=GREY_B)),
        )
        for it in legend:
            it.arrange(RIGHT, buff=0.15, aligned_edge=UP)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -0.9, 0]).align_to(np.array([3.75, 0, 0]),
                                                                                         LEFT)
        count = VGroup(label(rf"{len(REACH)} reachable states", font_size=19, color=WHITE),
                       label(rf"{len(edges)} $\tau$ steps", font_size=19, color=WHITE),
                       label(rf"{len(stuck)} with no move", font_size=19, color=WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.1)
        count.next_to(legend, UP, buff=0.4).align_to(legend, LEFT)
        dfn = VGroup(
            label(r"deadlock \ $=$ \ reachable, \ no move, \ not finished", font_size=21, color=NO),
            label(r"finding one is a search: \ Part 54's model checker", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(defs, DOWN, buff=0.45).align_to(defs, LEFT)
        sess = wrapped_label(r"session types: \ a channel's type is its protocol \ (Part 43's request and reply); \ "
                             r"some type systems built on them rule out such deadlocks", 5.6, font_size=19,
                             color=YES).next_to(dfn, DOWN, buff=0.3).align_to(defs, LEFT)
        ill = note(r"illustrative; \ states enumerated by hand", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Concurrency's classic failure is now a precise question. <bookmark mark='a'/> A lock, as in Part 33, is "
            "a process that can be grabbed, then released, forever. <bookmark mark='b'/> Thread one grabs lock a, "
            "then b, then releases both; thread two grabs b, then a. <bookmark mark='c'/> Draw each state of the "
            "closed system as a point: how far thread one has got, across, and thread two, up. Every grab and "
            "release is a tau step. <bookmark mark='d'/> Where both threads would hold one lock, there is no state. "
            "<bookmark mark='e'/> Explore from the start: nineteen states are reachable. <bookmark mark='f'/> Two "
            "have no move. One is the finish. The other is deadlock: each thread holds one lock and waits for the "
            "other's. A deadlock is a reachable stuck state that is not finished, and finding one is a search, which "
            "is what Part 54's model checker does. <bookmark mark='g'/> Session types go further: a channel's type "
            "is its protocol, like Part 43's request and reply, and some type systems built on them rule out such "
            "deadlocks before the program runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(dgl[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]), FadeIn(dgl[1]))
            self.play(FadeIn(defs[2]), FadeIn(dgl[2]), FadeIn(defs[3]))
            vo.wait_until("c")
            self.play(Create(frame), FadeIn(xl), FadeIn(yl), FadeIn(ax1), FadeIn(ax2))
            vo.wait_until("d")
            self.play(FadeIn(clash), FadeIn(legend[2]))
            vo.wait_until("e")
            self.play(GrowFromCenter(dots[(0, 0)]), run_time=0.4)
            for d in range(1, 9):
                new = layers.get(d, [])
                es = [e for (a, b), e in edges.items() if b in new]
                self.play(*[Create(e) for e in es], *[GrowFromCenter(dots[s]) for s in new], run_time=0.45)
            self.play(FadeIn(ghost), FadeIn(count))
            vo.wait_until("f")
            self.play(dots[(1, 1)].animate.set_color(NO).scale(1.5), dots[(4, 4)].animate.set_color(YES).scale(1.5),
                      FadeIn(legend[:2]))
            self.play(Flash(dots[(1, 1)], color=NO, flash_radius=0.3))
            self.play(FadeIn(dfn))
            vo.wait_until("g")
            self.play(FadeIn(sess))
        self.wait(0.6)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
