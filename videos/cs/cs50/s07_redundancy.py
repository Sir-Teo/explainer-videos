from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load


def pct_n(up: float) -> str:
    """An availability with as many decimals as it has whole nines (at least one)."""
    d = max(1, math.floor(-math.log10(1 - up)))
    return rf"{100 * up:.{d}f}\%"


def site(text, col, w=2.2, h=0.85, size=20):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(text, font_size=size, color=col).move_to(r))


def cross(m, col=NO):
    return VGroup(Line(m.get_corner(UL), m.get_corner(DR), color=col, stroke_width=4),
                  Line(m.get_corner(UR), m.get_corner(DL), color=col, stroke_width=4))


def load_bar(box, u, col=YES, w=0.32):
    """A vertical bar inside the right end of a box, filled to utilization ``u``."""
    r = box[0]
    hmax = r.height - 0.2
    frame = Rectangle(width=w, height=hmax, stroke_color=GREY_C, stroke_width=1.2)
    frame.move_to(r.get_right() + LEFT * (w / 2 + 0.12))
    fill = Rectangle(width=w, height=max(0.01, hmax * u), stroke_width=0, fill_color=col, fill_opacity=0.85)
    fill.align_to(frame, DOWN).set_x(frame.get_x())
    return VGroup(frame, fill)


class Redundancy(VoiceoverScene):
    def construct(self):
        self.card()
        self.spares()
        self.modes()
        self.evacuate()
        self.majority()

    def card(self):
        card = chapter_card(6, r"Redundancy", r"How many spares, \ and where?", lit=(1985, 2014),
                            extra=((1985, r"Gray: \ \textit{Why Do Computers Stop?}"),
                                   (2014, r"Ongaro and Ousterhout: \ Raft")), part=PART)
        with self.voiceover("Chapter six. Redundancy: how many spares, and where to put them."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def spares(self):
        rows = load("groups")["n_plus_k"]
        need = 10
        head = label(r"N + 1, \ N + 2", font_size=36).to_edge(UP, buff=0.3)
        side = 0.55
        machines = VGroup(*[Square(side, stroke_color=DATA, stroke_width=2, fill_color=DATA, fill_opacity=0.25)
                            for _ in range(need)])
        spares = VGroup(*[Square(side, stroke_color=YES, stroke_width=2, fill_color=YES, fill_opacity=0.25)
                          for _ in range(3)])
        VGroup(*machines, *spares).arrange(RIGHT, buff=0.14).move_to([0, 2.15, 0])
        m_l = label(rf"needed: \ {need} machines' capacity", font_size=18, color=DATA).next_to(machines, DOWN,
                                                                                              buff=0.12)
        s_l = label(r"spares", font_size=18, color=YES).next_to(spares, DOWN, buff=0.12)
        maint = cross(machines[3], GREY_B)
        maint_l = label(r"out for a deploy", font_size=16, color=GREY_B).next_to(machines[3], UP, buff=0.1)
        names = [r"N", r"N + 1", r"N + 2", r"N + 3"]
        cols = [NO, HEAD, YES, YES]
        ch = bar_chart([r["nines"] for r in rows], names, cols, height=2.6, bar_w=0.9, gap=0.65, vmax=6,
                       fmt_=lambda v: rf"{v:.1f}", font_size=20)
        ch.move_to([-3.4, -1.25, 0])
        ups = VGroup(*[label(pct_n(r["up"]), font_size=17, color=c).next_to(ch.names[k], DOWN, buff=0.12)
                       for k, (r, c) in enumerate(zip(rows, cols))])
        ylab = label(r"nines", font_size=18, color=GREY_A).next_to(ch, UP, buff=0.1).align_to(ch, LEFT)
        notes = VGroup(
            wrapped_label(r"each machine up 99\% of the time, \ independently; \ the service is whole while at least "
                          rf"{need} are up", 5.6, font_size=19, color=GREY_A),
            wrapped_label(r"N + 1 survives any one failure; \ N + 2 survives a failure while a machine is out on "
                          r"purpose, \ for a deploy or maintenance", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"Gray \ (1985), \ on Tandem's fault-tolerant computers: \ operations and software, \ not "
                          r"hardware, \ caused most outages", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, -1.0, 0])
        with self.voiceover(
            "Redundancy starts with counting. <bookmark mark='a'/> A service needs the capacity of ten machines, and "
            "each machine is up ninety-nine percent of the time, independently. With exactly ten, the service is "
            "whole only when all ten are up: ninety percent of the time, about one nine. <bookmark mark='b'/> Add one "
            "spare, N plus one, and it survives any single failure: two point three nines. <bookmark mark='c'/> But "
            "machines are also taken out on purpose, for deploys and maintenance, and a failure during that window "
            "finds no spare. So the usual rule is N plus two, three point seven nines here. <bookmark mark='d'/> Jim "
            "Gray's 1985 study of Tandem's fault-tolerant computers found that operations and software, not "
            "hardware, caused most of their outages. Plan for the machine you take out yourself."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in machines], lag_ratio=0.08), FadeIn(m_l), FadeIn(notes[0]))
            self.play(FadeIn(ch[0]), FadeIn(ch.names), FadeIn(ylab), GrowFromEdge(ch.bars[0], DOWN),
                      FadeIn(ch.vals[0]), FadeIn(ups[0]))
            vo.wait_until("b")
            self.play(FadeIn(spares[0], shift=LEFT * 0.2), FadeIn(s_l))
            self.play(GrowFromEdge(ch.bars[1], DOWN), FadeIn(ch.vals[1]), FadeIn(ups[1]))
            vo.wait_until("c")
            self.play(Create(maint), FadeIn(maint_l), machines[3].animate.set_fill(GREY_D, 0.4).set_stroke(GREY_B),
                      FadeIn(notes[1]))
            self.play(FadeIn(spares[1], shift=LEFT * 0.2))
            self.play(GrowFromEdge(ch.bars[2], DOWN), FadeIn(ch.vals[2]), FadeIn(ups[2]))
            vo.wait_until("d")
            self.play(FadeIn(spares[2], shift=LEFT * 0.2), GrowFromEdge(ch.bars[3], DOWN), FadeIn(ch.vals[3]),
                      FadeIn(ups[3]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def modes(self):
        head = label(r"Active--passive, \ active--active", font_size=36).to_edge(UP, buff=0.3)
        xl, xr = -3.5, 3.4
        t_l = label(r"active--passive", font_size=24, color=GREY_A).move_to([xl, 2.55, 0])
        t_r = label(r"active--active", font_size=24, color=GREY_A).move_to([xr, 2.55, 0])
        div = DashedLine([0, 2.7, 0], [0, -1.6, 0], color=GREY_D)
        # active-passive
        users_l = site(r"traffic", DATA, w=1.6, h=0.6, size=18).move_to([xl, 1.75, 0])
        prim = site(r"primary", YES).move_to([xl - 1.45, 0.25, 0])
        stby = site(r"standby", GREY_B).move_to([xl + 1.45, 0.25, 0])
        to_p = Arrow(users_l.get_bottom(), prim.get_top(), buff=0.08, color=DATA, stroke_width=2.5)
        to_s = Arrow(users_l.get_bottom(), stby.get_top(), buff=0.08, color=DATA, stroke_width=2.5)
        repl = DashedLine(prim.get_right(), stby.get_left(), color=GREY_B, stroke_width=2)
        repl_l = label(r"log", font_size=16, color=GREY_B).next_to(repl, DOWN, buff=0.06)
        x_p = cross(prim[0])
        # the failover, on a little timeline (illustrative)
        t0 = xl - 2.6
        tl_d = Rectangle(width=1.6, height=0.3, stroke_width=0, fill_color=NO, fill_opacity=0.8).move_to(
            [t0 + 0.8, -0.85, 0])
        tl_p = Rectangle(width=1.1, height=0.3, stroke_width=0, fill_color=HEAD, fill_opacity=0.8).next_to(
            tl_d, RIGHT, buff=0.05)
        tl_l = VGroup(label(r"detect", font_size=16, color=BG).move_to(tl_d),
                      label(r"promote", font_size=16, color=BG).move_to(tl_p))
        tl_n = label(r"= downtime", font_size=17, color=NO).next_to(tl_p, RIGHT, buff=0.15)
        # active-active
        users_r = site(r"traffic", DATA, w=1.6, h=0.6, size=18).move_to([xr, 1.75, 0])
        s1 = site(r"site 1", YES, w=2.3).move_to([xr - 1.45, 0.25, 0])
        s2 = site(r"site 2", YES, w=2.3).move_to([xr + 1.45, 0.25, 0])
        a1 = Arrow(users_r.get_bottom(), s1.get_top(), buff=0.08, color=DATA, stroke_width=2.5)
        a2 = Arrow(users_r.get_bottom(), s2.get_top(), buff=0.08, color=DATA, stroke_width=2.5)
        b1, b2 = load_bar(s1, 0.45), load_bar(s2, 0.45)
        u_l = VGroup(label(r"45\%", font_size=17, color=YES).next_to(s1, DOWN, buff=0.1),
                     label(r"45\%", font_size=17, color=YES).next_to(s2, DOWN, buff=0.1))
        x_s1 = cross(s1[0])
        b2_hi = load_bar(s2, 0.9, col=HEAD)
        u_hi = label(r"90\%", font_size=17, color=HEAD).next_to(s2, DOWN, buff=0.1)
        ill = note(r"illustrative", font_size=16).next_to(div, DOWN, buff=0.1)
        rule = MathTex(r"\text{to lose 1 of } n \text{ sites, run each below } \tfrac{n-1}{n}:\quad",
                       r"\tfrac{1}{2},\ \tfrac{2}{3},\ \tfrac{3}{4},\ \dots", font_size=32, color=WHITE)
        rule[1].set_color(HEAD)
        rule.move_to([0, -2.45, 0])
        rule_n = label(r"chapter three's cascade, \ $u_0\,n/(n-1) \le 1$, \ run in reverse", font_size=19,
                       color=GREY_A).next_to(rule, DOWN, buff=0.2)
        with self.voiceover(
            "There are two ways to keep a spare. <bookmark mark='a'/> Active-passive: a primary serves, and a standby "
            "follows its log, ready to take over. <bookmark mark='b'/> When the primary dies, something must notice "
            "and promote the standby, and that time is downtime, chapter one's repair time. Worse, the standby has "
            "never served real traffic, so failover is the least tested path in the system. <bookmark mark='c'/> "
            "Active-active: every copy serves all the time, so failover is only routing, exercised every day. "
            "<bookmark mark='d'/> The price is headroom. To lose one of n sites, each must run below n minus one over "
            "n of its capacity: a half for two sites, two thirds for three. It is chapter three's cascade "
            "arithmetic, run in reverse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t_l), FadeIn(t_r), Create(div), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(users_l), FadeIn(prim), FadeIn(stby), GrowArrow(to_p), Create(repl), FadeIn(repl_l))
            vo.wait_until("b")
            self.play(Create(x_p), prim[0].animate.set_stroke(NO), FadeOut(to_p))
            self.play(GrowFromEdge(tl_d, LEFT), FadeIn(tl_l[0]))
            self.play(GrowFromEdge(tl_p, LEFT), FadeIn(tl_l[1]), FadeIn(tl_n))
            self.play(GrowArrow(to_s), stby[0].animate.set_stroke(YES), stby[1].animate.set_color(YES))
            vo.wait_until("c")
            self.play(FadeIn(users_r), FadeIn(s1), FadeIn(s2), GrowArrow(a1), GrowArrow(a2), FadeIn(b1),
                      FadeIn(b2), FadeIn(u_l))
            self.play(Create(x_s1), s1[0].animate.set_stroke(NO), FadeOut(a1), FadeOut(b1), FadeOut(u_l[0]))
            self.play(Transform(b2, b2_hi), Transform(u_l[1], u_hi))
            vo.wait_until("d")
            self.play(Write(rule))
            self.play(FadeIn(rule_n))
        self.wait(0.4)
        self.clear_scene()

    def evacuate(self):
        head = label(r"Evacuating a region", font_size=36).to_edge(UP, buff=0.3)
        glb = site(r"global load balancer", DATA, w=3.6, h=0.7, size=19).move_to([0, 2.05, 0])
        regs = VGroup(*[site(rf"region {k + 1}", YES, w=3.0, h=1.6, size=22) for k in range(3)]).arrange(
            RIGHT, buff=1.0).move_to([0, -0.35, 0])
        for r in regs:
            r[1].shift(LEFT * 0.3)
        arrows = VGroup(*[Arrow(glb.get_bottom(), r.get_top(), buff=0.1, color=DATA, stroke_width=2.5)
                          for r in regs])
        bars = [load_bar(r, 0.6) for r in regs]
        ul = [label(r"60\%", font_size=18, color=YES).next_to(r, DOWN, buff=0.1) for r in regs]
        sick = label(r"errors rising, \ cause unknown", font_size=17, color=HEAD).next_to(regs[1], UP, buff=0.1)
        sick.shift(RIGHT * 0.95)
        hi = [load_bar(regs[k], 0.9, col=HEAD) for k in (0, 2)]
        uh = [label(r"90\% \ $= 60\% \times 3/2$", font_size=18, color=HEAD).next_to(regs[k], DOWN, buff=0.1)
              for k in (0, 2)]
        ill = note(r"illustrative", font_size=16).next_to(glb, RIGHT, buff=0.3)
        notes = VGroup(
            wrapped_label(r"\textbf{headroom}: \ the survivors must absorb the load \ (the last section's rule)", 4.0,
                          font_size=18, color=WHITE),
            wrapped_label(r"\textbf{data}: \ replicated there already \ (Part 39); \ what was not is the "
                          r"\textit{recovery point}, \ the time taken the \textit{recovery time}", 4.0, font_size=18,
                          color=WHITE),
            wrapped_label(r"\textbf{practice}: \ an evacuation never rehearsed is a hope, \ not a plan", 4.0,
                          font_size=18, color=WHITE),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The largest unit of redundancy is a whole region, a separate set of buildings, power and network, "
            "because, as chapter one showed, replicas that share a cause fail together. <bookmark mark='a'/> Three "
            "regions share the traffic, each sixty percent busy. <bookmark mark='b'/> Region two starts to misbehave: "
            "errors are rising, and nobody yet knows why. <bookmark mark='c'/> The first move is not to debug but to "
            "evacuate: steer its traffic to the other two, which rise to ninety percent. Debug afterwards, with no "
            "users waiting. <bookmark mark='d'/> Evacuation needs three things ready in advance: headroom in the "
            "other regions; the data, already there through Part 39's replication, since whatever had not been "
            "copied is lost or stranded; and practice, because an evacuation that has never been rehearsed is a "
            "hope, not a plan."
        ) as vo:
            self.play(FadeIn(head), FadeIn(glb), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(regs), *[GrowArrow(a) for a in arrows], *[FadeIn(b) for b in bars],
                      *[FadeIn(u) for u in ul])
            vo.wait_until("b")
            self.play(regs[1][0].animate.set_stroke(HEAD), regs[1][1].animate.set_color(HEAD), FadeIn(sick))
            self.play(Wiggle(regs[1]))
            vo.wait_until("c")
            self.play(arrows[1].animate.set_opacity(0.15), regs[1][0].animate.set_stroke(GREY_D),
                      regs[1][1].animate.set_color(GREY_C), FadeOut(bars[1]), FadeOut(ul[1]), FadeOut(sick))
            self.play(Transform(bars[0], hi[0]), Transform(bars[2], hi[1]), Transform(ul[0], uh[0]),
                      Transform(ul[2], uh[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.5), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def majority(self):
        rows = load("groups")["raft"]
        by = {(r["a"], r["n"]): r for r in rows}
        head = label(r"A Raft group's availability", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-4.3, 0.55, 0])
        R = 1.25
        nodes = VGroup()
        for k in range(5):
            ang = PI / 2 + k * TAU / 5
            c = Circle(radius=0.36, stroke_color=YES, stroke_width=2.5, fill_color=YES, fill_opacity=0.2)
            c.move_to(C + R * np.array([math.cos(ang), math.sin(ang), 0]))
            nodes.add(VGroup(c, label(rf"{k + 1}", font_size=20, color=WHITE).move_to(c)))
        crown = label(r"leader", font_size=16, color=HEAD).next_to(nodes[0], UP, buff=0.08)
        status = label(r"5 of 5 up: \ serving", font_size=20, color=YES).move_to(C + DOWN * 2.0)
        s2 = label(r"3 of 5 up: \ still a majority", font_size=20, color=YES).move_to(status)
        s3 = label(r"2 of 5 up: \ no majority, \ no service", font_size=20, color=NO).move_to(status)
        safe = label(r"but nothing committed is lost", font_size=17, color=GREY_A).next_to(s3, DOWN, buff=0.12)

        def down(k):
            return [nodes[k][0].animate.set_stroke(NO).set_fill(NO, 0.15), nodes[k][1].animate.set_color(NO)]
        eq = MathTex(r"A = \sum_{k=\lfloor n/2 \rfloor + 1}^{n} \binom{n}{k}\, a^k (1-a)^{n-k}", font_size=34,
                     color=HEAD).move_to([2.6, 2.1, 0])
        eq_l = label(r"the chance that a majority is up, \ for independent nodes each up a fraction $a$",
                     font_size=18, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        body = [[rf"{n}", rf"{(n - 1) // 2}", rf"{by[(0.99, n)]['nines']:.1f}", rf"{by[(0.999, n)]['nines']:.1f}"]
                for n in (1, 3, 5, 7)]
        tab = grid_table([r"nodes", r"failures survived", r"nines, \ $a = 99\%$", r"nines, \ $a = 99.9\%$"], body,
                         widths=[1.2, 2.2, 2.0, 2.1], row_h=0.5, font_size=21, mono_cols=())
        tab.next_to(eq_l, DOWN, buff=0.35).set_x(2.6)
        hl = SurroundingRectangle(VGroup(*tab.cells[3]), color=HEAD, buff=0.06, stroke_width=2)
        notes = VGroup(
            wrapped_label(r"even sizes buy nothing: \ four nodes survive one failure, \ like three, \ and need more "
                          r"votes", 6.3, font_size=19, color=WHITE),
            wrapped_label(r"the nines assume independence; \ chapter one's shared causes cap them, \ so the five go in "
                          r"different zones", 6.3, font_size=19, color=NO),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Finally, a group that agrees. <bookmark mark='a'/> Part 38's Raft serves while a majority of its nodes "
            "is up, because every decision needs a majority of votes. Five nodes survive two failures; "
            "<bookmark mark='b'/> a third failure takes the majority, and with it the service, though nothing "
            "committed is lost. <bookmark mark='c'/> If nodes fail independently, the group's availability is the "
            "chance that more than half are up, a sum over the binomial distribution. <bookmark mark='d'/> At "
            "ninety-nine percent a node, three nodes give three and a half nines, five give five, and seven give six "
            "and a half. At ninety-nine point nine, five nodes give eight. <bookmark mark='e'/> Two caveats. Even "
            "sizes buy nothing: four nodes survive one failure, like three. And the nines assume independence; "
            "chapter one showed how a shared cause caps them, which is why the five nodes go in different zones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(crown), FadeIn(status))
            vo.wait_until("a")
            self.play(*down(1), *down(3))
            self.play(Transform(status, s2))
            vo.wait_until("b")
            self.play(*down(0), FadeOut(crown))
            self.play(Transform(status, s3), FadeIn(safe))
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(eq_l))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, 5)], lag_ratio=0.3),
                      run_time=2.0)
            self.play(Create(hl))
            vo.wait_until("e")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
