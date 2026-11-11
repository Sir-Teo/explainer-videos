from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load, mono, tag_box

RM_COLOR = {"working": GREY_B, "prepared": HEAD, "committed": YES, "aborted": NO}


def state_node(name, color, r=0.55):
    c = Circle(radius=r, color=color, stroke_width=2.4, fill_color=BG, fill_opacity=1)
    t = label(name, font_size=18, color=color).move_to(c)
    if t.width > 2 * r - 0.1:
        t.scale_to_fit_width(2 * r - 0.1)
    return VGroup(c, t)


def rm_cell(state, w=1.6, h=0.5):
    col = RM_COLOR[state]
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=col, stroke_width=1.8, fill_color=col,
                         fill_opacity=0.18)
    return VGroup(r, label(state, font_size=17, color=WHITE).move_to(r))


class Tla(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.tcommit()
        self.twophase()
        self.bug()
        self.refine()
        self.small()

    def card(self):
        card = chapter_card(12, r"Specifying systems: \ TLA$^+$", r"What exactly should a system do?",
                            lit=(1994, 2006), extra=((1994, r"Lamport: \ TLA"),
                                                     (2006, r"Gray and Lamport: \ TCommit")), part=PART)
        with self.voiceover("Chapter twelve. Specifying systems with TLA plus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def machines(self):
        head = label(r"A system is a state machine", font_size=36).to_edge(UP, buff=0.3)
        vals = [0, 1, 1, 2, 3]
        boxes = VGroup(*[tag_box(f"x = {v}", color=DATA, size=20, w=1.5, h=0.6) for v in vals]).arrange(RIGHT,
                                                                                                         buff=0.7)
        boxes.next_to(head, DOWN, buff=0.6)
        sig = VGroup(*[MathTex(rf"\sigma_{k}", font_size=26, color=GREY_B).next_to(b, UP, buff=0.1)
                       for k, b in enumerate(boxes)])
        arrs = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.06, color=GREY_B,
                              stroke_width=2, max_tip_length_to_length_ratio=0.25) for k in range(len(boxes) - 1)])
        dots = MathTex(r"\cdots", font_size=36, color=GREY_B).next_to(boxes, RIGHT, buff=0.25)
        stl = label(r"stutter", font_size=17, color=LAM).next_to(arrs[1], DOWN, buff=0.15)
        ill = note(r"a counter: \ illustrative", font_size=17).next_to(boxes, DOWN, buff=0.55).align_to(boxes, LEFT)
        rows = VGroup(
            MathTex(r"\mathit{Init}", font_size=36),
            MathTex(r"\mathit{Init}", r"\;\wedge\;", r"\Box", r"\mathit{Next}", font_size=36),
            MathTex(r"\mathit{Init}", r"\;\wedge\;", r"\Box", r"[\mathit{Next}]_{\mathit{vars}}", font_size=36),
            MathTex(r"\mathit{Init}", r"\;\wedge\;", r"\Box", r"[\mathit{Next}]_{\mathit{vars}}", r"\;\wedge\;",
                    r"\mathit{Fairness}", font_size=36, color=YES),
        )
        whys = VGroup(label(r"the first state is an initial one", font_size=19, color=GREY_A),
                      label(r"always: \ each step is a $\mathit{Next}$ step", font_size=19, color=GREY_A),
                      label(r"or a stutter: \ the variables unchanged", font_size=19, color=LAM),
                      label(r"and something good eventually happens", font_size=19, color=YES))
        col = VGroup(*[VGroup(r, w).arrange(RIGHT, buff=0.5) for r, w in zip(rows, whys)])
        col.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(ill, DOWN, buff=0.4).set_x(0)
        for r in rows:
            r.align_to(rows[0], LEFT)
        wx = max(r.get_right()[0] for r in rows) + 0.5
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5).set_x(wx, direction=LEFT)
        with self.voiceover(
            "Leslie Lamport's temporal logic of actions, TLA, from 1994, describes a system as a state machine "
            "written in ordinary mathematics. <bookmark mark='a'/> A state gives a value to every variable; a "
            "behaviour is an infinite sequence of states. <bookmark mark='b'/> A specification is a formula true of "
            "the right behaviours. It starts in an initial state, <bookmark mark='c'/> and always, each step "
            "satisfies the next-state relation, <bookmark mark='d'/> or leaves the variables unchanged: a stutter, "
            "which lets a finer-grained implementation take steps of its own. <bookmark mark='e'/> Fairness adds that"
            " something good eventually happens. TLA plus is the language built around this formula, and TLC is its "
            "model checker."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(boxes[k]), FadeIn(sig[k]),
                                                   *([GrowArrow(arrs[k - 1])] if k else []))
                                    for k in range(len(boxes))], lag_ratio=0.3), FadeIn(dots), FadeIn(ill),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]), Indicate(boxes[0], color=HEAD))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]), FadeIn(stl),
                      Indicate(VGroup(boxes[1], boxes[2]), color=LAM))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def tcommit(self):
        rows_d = load("twophase")["rows"]
        assert all(r["tcommit_states"] == r["tcommit_closed_form"] for r in rows_d)
        head = label(r"TCommit: \ what commit means", font_size=36).to_edge(UP, buff=0.3)
        W = state_node("working", GREY_B).move_to([-5.4, 1.3, 0])
        P = state_node("prepared", HEAD).move_to([-3.0, 1.3, 0])
        C = state_node("committed", YES).move_to([-0.8, 1.3, 0])
        A = state_node("aborted", NO).move_to([-3.0, -0.7, 0])
        e1 = Arrow(W.get_right(), P.get_left(), buff=0.05, color=GREY_B, stroke_width=2.2)
        e2 = Arrow(P.get_right(), C.get_left(), buff=0.05, color=YES, stroke_width=2.2)
        e3 = Arrow(W.get_bottom(), A.get_left(), buff=0.08, color=NO, stroke_width=2.2)
        e4 = Arrow(P.get_bottom(), A.get_top(), buff=0.05, color=NO, stroke_width=2.2)
        g2 = label(r"if every one is prepared or committed", font_size=17, color=YES).next_to(C, UP, buff=0.2)
        g2.shift(LEFT * 1.0)
        g3 = label(r"if nobody has committed", font_size=17, color=NO).next_to(A, RIGHT, buff=0.25)
        one = label(r"one resource manager", font_size=18, color=GREY_A).next_to(VGroup(W, C), UP, buff=0.9)
        inv = MathTex(r"\neg\,(\exists r.\ \mathit{rm}_r = \mathit{committed}", r"\;\wedge\;",
                      r"\exists r.\ \mathit{rm}_r = \mathit{aborted})", font_size=30, color=YES)
        invl = label(r"the invariant, \ \textit{TCConsistent}", font_size=18, color=YES)
        ig = VGroup(inv, invl).arrange(DOWN, buff=0.1).move_to([-3.0, -2.2, 0])
        cnt = VGroup(
            MathTex(r"|S|", r"=", r"|S_{\text{none}}|", r"+", r"|S_{\text{some}}|", font_size=32),
            MathTex(r"|S|", r"=", r"3^n", r"+", r"|S_{\text{some}}|", font_size=32),
            MathTex(r"|S|", r"=", r"3^n", r"+", r"(2^n - 1)", font_size=32, color=YES),
        )
        cw = VGroup(label(r"reachable states: \ nobody has committed, \ or someone has", font_size=17, color=GREY_A),
                    label(r"each: \ working, \ prepared or aborted", font_size=17, color=GREY_A),
                    label(r"all prepared or committed, \ not all prepared", font_size=17, color=GREY_A))
        ccol = VGroup(*[VGroup(c, w).arrange(DOWN, buff=0.08) for c, w in zip(cnt, cw)]).arrange(DOWN, buff=0.28)
        ccol.move_to([3.6, 1.2, 0])
        if ccol.get_right()[0] > 6.85:
            ccol.shift(LEFT * (ccol.get_right()[0] - 6.85))
        tab = grid_table([r"$n$", r"$3^n + 2^n - 1$", r"checker"],
                         [[f"{r['n']}", f"{r['tcommit_closed_form']}", f"{r['tcommit_states']}"] for r in rows_d],
                         widths=[0.8, 2.0, 1.4], row_h=0.4, font_size=19,
                         colors=[[WHITE, YES, YES]] * len(rows_d), mono_cols=())
        tab.next_to(ccol, DOWN, buff=0.4)
        with self.voiceover(
            "Jim Gray and Leslie Lamport's TCommit says what commit means. <bookmark mark='a'/> Each resource manager"
            " starts working, may prepare, then commits or aborts. <bookmark mark='b'/> It may commit only when every"
            " manager is prepared or committed, and abort only when nobody has committed. <bookmark mark='c'/> The "
            "property we want is consistency: never one committed and another aborted. <bookmark mark='d'/> How many "
            "states are reachable? Either nobody has committed, and each manager is working, prepared or aborted: "
            "three to the n. <bookmark mark='e'/> Or someone has, and all are prepared or committed, at least one "
            "committed: two to the n, minus one. <bookmark mark='f'/> Our checker agrees for two to five managers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(one), FadeIn(W), GrowArrow(e1), FadeIn(P))
            self.play(GrowArrow(e2), FadeIn(C), GrowArrow(e3), GrowArrow(e4), FadeIn(A))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(g3))
            vo.wait_until("c")
            self.play(FadeIn(ig))
            vo.wait_until("d")
            self.play(FadeIn(cnt[0]), FadeIn(cw[0]))
            self.play(TransformMatchingTex(cnt[0].copy(), cnt[1]), FadeIn(cw[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(cnt[1].copy(), cnt[2]), FadeIn(cw[2]))
            vo.wait_until("f")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def twophase(self):
        rows_d = load("twophase")["rows"]
        assert all(r["consistent"] for r in rows_d)
        head = label(r"TwoPhase: \ the protocol", font_size=36).to_edge(UP, buff=0.3)
        rms = VGroup(*[rm_cell("working") for _ in range(3)]).arrange(DOWN, buff=0.35).move_to([-5.3, 1.0, 0])
        rml = VGroup(*[label(f"RM{k}", font_size=18, color=GREY_A).next_to(r, LEFT, buff=0.12)
                       for k, r in enumerate(rms)])
        tm = VGroup(RoundedRectangle(width=2.8, height=0.9, corner_radius=0.1, stroke_color=KERN, stroke_width=2.2,
                                     fill_color=KERN, fill_opacity=0.15))
        tm.add(label(r"TM: \ init", font_size=19, color=WHITE).move_to(tm[0])).move_to([-1.9, 1.0, 0])
        bag = RoundedRectangle(width=2.6, height=2.6, corner_radius=0.15, stroke_color=GREY_C, stroke_width=1.6,
                               fill_color=GREY_E, fill_opacity=0.3).move_to([1.4, 1.0, 0])
        bagl = label(r"messages \ (never lost)", font_size=17, color=GREY_A).next_to(bag, UP, buff=0.1)
        msgs = VGroup(*[tag_box(f"Prepared({k})", color=HEAD, size=15, h=0.42) for k in range(3)],
                      tag_box("Commit", color=YES, size=15, h=0.42)).arrange(DOWN, buff=0.15).move_to(bag)

        def set_rm(k, state):
            new = rm_cell(state).move_to(rms[k])
            return Transform(rms[k], new)

        def set_tm(text, col=WHITE):
            return Transform(tm[1], label(text, font_size=19, color=col).move_to(tm[0]))
        tab = grid_table([r"managers", r"TwoPhase states", r"transitions", r"longest path", r"consistent"],
                         [[f"{r['n']}", f"{r['twophase_states']:,}", f"{r['twophase_edges']:,}", f"{r['diameter']}",
                           r"yes" if r["consistent"] else r"no"] for r in rows_d],
                         widths=[1.6, 2.4, 2.0, 2.0, 1.8], row_h=0.4, font_size=19,
                         colors=[[WHITE, DATA, GREY_A, GREY_A, YES]] * len(rows_d), mono_cols=())
        tab.to_edge(DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            "Two-phase commit, the protocol, adds a transaction manager and messages. <bookmark mark='a'/> Each "
            "resource manager that is ready prepares, and sends a Prepared message. <bookmark mark='b'/> The "
            "transaction manager collects them, and when every one has prepared, it decides to commit and sends "
            "Commit. <bookmark mark='c'/> Each resource manager that receives it commits. As in Lamport's "
            "specification, messages are never lost: once sent, a message stays in the bag. <bookmark mark='d'/> "
            "The checker explores every interleaving: two hundred and eighty-eight states for three managers, eight "
            "thousand eight hundred and thirty-two for five, and consistency holds in all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rms), FadeIn(rml), FadeIn(tm), FadeIn(bag), FadeIn(bagl))
            vo.wait_until("a")
            for k in range(3):
                self.play(set_rm(k, "prepared"), FadeIn(msgs[k], shift=RIGHT * 0.3), run_time=0.7)
            vo.wait_until("b")
            self.play(set_tm(r"TM: \ prepared 0, 1, 2", HEAD), run_time=0.8)
            self.play(set_tm(r"TM: \ committed", YES), FadeIn(msgs[3], shift=RIGHT * 0.3))
            vo.wait_until("c")
            self.play(*[set_rm(k, "committed") for k in range(3)])
            vo.wait_until("d")
            self.play(FadeIn(tab))
            self.play(Indicate(VGroup(*tab.cells[2]), color=DATA), Indicate(VGroup(*tab.cells[4]), color=DATA))
        self.wait(0.4)
        self.clear_scene()

    def bug(self):
        bg = load("twophase")["bug"]
        assert not bg["consistent"] and bg["length"] == len(bg["counterexample"]) - 1
        cx = bg["counterexample"]
        n = bg["n"]
        head = label(r"A coordinator that gives up", font_size=36).to_edge(UP, buff=0.3)
        rule = mono("TMTimeoutCommit:  tmState = init, not all prepared  ->  commit, send Commit", size=18, color=NO)
        rule.next_to(head, DOWN, buff=0.35)
        rl = label(r"the planted bug: \ after waiting too long, \ commit without hearing from everyone", font_size=19,
                   color=NO).next_to(rule, DOWN, buff=0.12)
        cols = VGroup()
        for k, st in enumerate(cx):
            s = st["state"]
            act = label(r"start" if st["action"] is None else st["action"].replace("_", r"\_"), font_size=17,
                        color=HEAD)
            cells = VGroup(*[rm_cell(v) for v in s["rmState"]])
            tmc = col_cell(f"TM {s['tmState']}", KERN if s["tmState"] == "init" else YES)
            msg = col_cell(", ".join(s["msgs"]) or "no messages", GREY_B)
            g = VGroup(act, cells, tmc, msg).arrange(DOWN, buff=0.18)
            cells.arrange(DOWN, buff=0.12)
            g.arrange(DOWN, buff=0.18)
            cols.add(g)
        cols.arrange(RIGHT, buff=0.55).next_to(rl, DOWN, buff=0.45)
        for g in cols:
            g[0].move_to([g[1].get_x(), cols.get_top()[1] - 0.12, 0])
        names = VGroup(*[label(f"RM{k}", font_size=17, color=GREY_A).next_to(cols[0][1][k], LEFT, buff=0.15)
                         for k in range(n)])
        arrs = VGroup(*[Arrow(cols[k][1].get_right(), cols[k + 1][1].get_left(), buff=0.06, color=GREY_B,
                              stroke_width=2, max_tip_length_to_length_ratio=0.2) for k in range(len(cols) - 1)])
        last = cols[-1][1]
        bad = SurroundingRectangle(last, color=NO, buff=0.08, stroke_width=3)
        verdict = label(rf"{bg['states']} states explored; \ {bg['length']} steps: \ one committed, \ one aborted",
                        font_size=20, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now plant a bug that looks like good engineering: a timeout. <bookmark mark='a'/> If the coordinator "
            "has waited too long, it commits without hearing from everyone. <bookmark mark='b'/> With three "
            "managers the checker explores six hundred and twenty-three states and returns a counterexample of three "
            "steps. <bookmark mark='c'/> The coordinator times out, and commits before anyone has prepared. "
            "<bookmark mark='d'/> Resource manager zero, still working, chooses to abort, as it is allowed to. "
            "<bookmark mark='e'/> Resource manager one receives Commit, and commits. One committed and one aborted: "
            "the invariant is broken. A coordinator that times out may abort, never commit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(cols[0]), FadeIn(names))
            for k, mk in enumerate("cde"):
                vo.wait_until(mk)
                self.play(GrowArrow(arrs[k]), FadeIn(cols[k + 1], shift=RIGHT * 0.2))
            self.play(Create(bad), FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    def refine(self):
        rows_d = load("twophase")["rows"]
        checked = [r for r in rows_d if r["refines"] is not None]
        assert all(r["refines"] for r in checked)
        head = label(r"TwoPhase implements TCommit", font_size=36).to_edge(UP, buff=0.3)
        trace = [("RMPrepare(0)", "Prepare(0)"), ("TMRcvPrepared(0)", None), ("RMPrepare(1)", "Prepare(1)"),
                 ("TMRcvPrepared(1)", None), ("TMCommit", None), ("RMRcvCommitMsg(0)", "Commit(0)"),
                 ("RMRcvCommitMsg(1)", "Commit(1)")]
        x0, dx, yt, yb = -5.6, 1.75, 1.2, -0.6
        top_l = label(r"TwoPhase", font_size=20, color=DATA).move_to([x0, yt + 1.3, 0]).align_to(
            [x0 - 0.3, 0, 0], LEFT)
        bot_l = label(r"TCommit", font_size=20, color=YES).move_to([x0, yb - 0.8, 0]).align_to(
            [x0 - 0.3, 0, 0], LEFT)
        tdots = VGroup(*[Dot([x0 + k * dx, yt, 0], radius=0.07, color=DATA) for k in range(len(trace) + 1)])
        bdots = VGroup(*[Dot([x0 + k * dx, yb, 0], radius=0.07, color=YES) for k in range(len(trace) + 1)])
        maps = VGroup(*[DashedLine(t.get_center(), b.get_center(), color=GREY_D, stroke_width=1.4)
                        for t, b in zip(tdots, bdots)])
        tsteps, bsteps = VGroup(), VGroup()
        for k, (ca, aa) in enumerate(trace):
            a = Line(tdots[k].get_center(), tdots[k + 1].get_center(), color=DATA, stroke_width=2.4)
            al = label(ca, font_size=16, color=DATA).rotate(PI / 6).next_to(a, UP, buff=0.05)
            tsteps.add(VGroup(a, al))
            if aa:
                b = Line(bdots[k].get_center(), bdots[k + 1].get_center(), color=YES, stroke_width=2.4)
                bl = label(aa, font_size=16, color=YES).next_to(b, DOWN, buff=0.08)
            else:
                b = DashedLine(bdots[k].get_center(), bdots[k + 1].get_center(), color=LAM, stroke_width=2.0)
                bl = label(r"stutter", font_size=16, color=LAM).next_to(b, DOWN, buff=0.08)
            bsteps.add(VGroup(b, bl))
        mapl = label(r"map: \ keep the managers' states, \ forget the coordinator and the messages", font_size=18,
                     color=GREY_A).next_to(VGroup(*maps), RIGHT, buff=0.1)
        mapl.move_to([0, (yt + yb) / 2, 0]).add_background_rectangle(color=BG, opacity=1, buff=0.05)
        ill = note(r"one behaviour for two managers \ (illustrative)", font_size=17).to_corner(UR, buff=0.4).shift(
            DOWN * 0.45)
        rows = VGroup(
            MathTex(r"\mathit{TwoPhase}", r"\;\Rightarrow\;", r"\mathit{TCommit}", font_size=32),
            MathTex(r"\mathit{Next}_{2P}", r"\;\Rightarrow\;", r"\mathit{Next}_{TC}", r"\;\vee\;",
                    r"\mathit{rm}' = \mathit{rm}", font_size=32),
        )
        whys = VGroup(label(r"implementation is implication", font_size=18, color=GREY_A),
                      label(r"every step: \ a TCommit step, \ or a stutter", font_size=18, color=GREY_A))
        VGroup(*[VGroup(r, w).arrange(RIGHT, buff=0.4) for r, w in zip(rows, whys)]).arrange(
            DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=1.0).to_edge(LEFT, buff=0.6)
        res = label(", \\ ".join(f"$n = {r['n']}$" for r in checked) + r": \ every reachable step checked, \ "
                    r"TwoPhase refines TCommit", font_size=19, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Is the protocol a correct implementation of the specification? In TLA, implementation is implication. "
            "<bookmark mark='a'/> Map each protocol state to its resource managers' states, forgetting the "
            "coordinator and the messages. <bookmark mark='b'/> Then every protocol step must be a TCommit step, or "
            "leave the managers unchanged. Preparing and committing map to TCommit's own steps; the coordinator's "
            "bookkeeping maps to stutters, which is exactly why TLA allows them. <bookmark mark='c'/> Our checker "
            "tried every reachable step for two, three and four managers: the protocol refines the specification. "
            "<bookmark mark='d'/> So its consistency follows from TCommit's, by chapter eleven's square, and so "
            "does every other safety property that TCommit has."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(FadeIn(top_l), FadeIn(tdots), FadeIn(ill),
                      LaggedStart(*[Create(s[0]) for s in tsteps], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(s[1]) for s in tsteps], lag_ratio=0.2), run_time=2)
            self.play(Create(maps), FadeIn(bot_l), FadeIn(bdots), FadeIn(mapl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in bsteps], lag_ratio=0.3), run_time=2.5)
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(Indicate(res, color=YES, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    def small(self):
        tp = load("twophase")
        rows_d = tp["rows"]
        bg = tp["bug"]
        head = label(r"Small models, \ real bugs", font_size=36).to_edge(UP, buff=0.3)
        chart = bar_chart([r["twophase_states"] for r in rows_d], [rf"$n = {r['n']}$" for r in rows_d],
                          [DATA] * len(rows_d), height=3.2, bar_w=0.7, gap=0.45, fmt_=lambda v: f"{v:,.0f}",
                          font_size=19, log=True).move_to([-3.6, -0.4, 0])
        cap = label(r"TwoPhase states \ (log scale)", font_size=18, color=GREY_A).next_to(chart, UP, buff=0.3)
        ratios = [rows_d[k + 1]["twophase_states"] / rows_d[k]["twophase_states"] for k in range(len(rows_d) - 1)]
        notes = VGroup(
            wrapped_label(rf"each manager multiplies the states by {min(ratios):.1f} to {max(ratios):.1f}", 5.4,
                          font_size=20, color=DATA),
            wrapped_label(rf"the timeout bug needed only {bg['n']} managers and {bg['length']} steps: \ "
                          r"Jackson's \textbf{small scope hypothesis}, \ most bugs have small counterexamples", 5.4,
                          font_size=20, color=NO),
            wrapped_label(r"for every $n$: \ TLAPS, \ TLA$^+$'s proof system, \ proves invariants by induction, "
                          r"\ like chapter 2's loops", 5.4, font_size=20, color=YES),
            wrapped_label(r"engineers at Amazon and Microsoft have described specifying storage and database "
                          r"designs this way \ (chapter 15)", 5.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "A model checker covers small instances only. <bookmark mark='a'/> The protocol's states grow about five-"
            "fold with each manager, to eight thousand eight hundred and thirty-two at five. <bookmark mark='b'/> But"
            " the timeout bug needed only three managers and three steps. Daniel Jackson's small scope hypothesis "
            "says this is typical: most design bugs have small counterexamples. <bookmark mark='c'/> For every n, TLA"
            " plus has a proof system, TLAPS, in which invariants are proved by induction, like the loops of chapter "
            "two. <bookmark mark='d'/> Engineers at Amazon and Microsoft have described finding design bugs this way "
            "before writing code, as the frontier chapter tells."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(chart[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(nm))
                                    for b, v, nm in zip(chart.bars, chart.vals, chart.names)], lag_ratio=0.3),
                      run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(chart.bars[1], color=NO))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


def col_cell(text, color, w=1.6, h=0.5):
    """A cell in the counterexample's columns: the coordinator's state, or the messages sent so far."""
    t = label(text, font_size=16, color=WHITE)
    if t.width > w - 0.1:
        t.scale_to_fit_width(w - 0.1)
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=1.6, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, t.move_to(r))


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, mono)
