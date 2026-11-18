from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def node(name, color, w=2.2):
    r = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=2,
                         fill_color=BG, fill_opacity=1)
    return VGroup(r, label(name, font_size=20, color=color).move_to(r))


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.choreo()
        self.proofs()

    def card(self):
        self.chapter(14, r"Frontier: \ services you can prove", r"Can a system of services be shown correct?", lit=(1993, 2015), extra=((1993, r"Honda: \ session types"),
                                                     (2015, r"IronFleet, \ Verdi; \ TLA$^+$ at Amazon")), part=PART, said="Chapter fourteen, the frontier. Can a system of services be shown to be correct?")

    def choreo(self):
        self.ask(r"Write the whole conversation once, \\ then generate each service's part. Can they deadlock?",
                 [r"maybe", r"no, by construction"], 1,
                 say="Write the conversation between services once, from above, and generate each service's code from it. Can they deadlock?",
                 reveal="No: that's choreographic programming's guarantee.")
        head = label(r"Protocols as types", font_size=36).to_edge(UP, buff=0.3)
        roles = [(r"client", DATA), (r"orders", HEAD), (r"payments", YES)]
        cols = VGroup(*[node(t, c) for t, c in roles]).arrange(RIGHT, buff=1.8).next_to(head, DOWN, buff=0.35)
        lifelines = VGroup(*[DashedLine(c.get_bottom(), c.get_bottom() + DOWN * 3.0, color=GREY_D) for c in cols])
        msgs = [(0, 1, r"order(items)"), (1, 2, r"charge(amount)"), (2, 1, r"ok $\mid$ declined"),
                (1, 0, r"confirmed $\mid$ rejected")]
        arrows = VGroup()
        for k, (a, b, t) in enumerate(msgs):
            y = cols.get_bottom()[1] - 0.5 - 0.65 * k
            xa, xb = cols[a].get_center()[0], cols[b].get_center()[0]
            ar = Arrow([xa, y, 0], [xb, y, 0], buff=0.05, stroke_width=2, color=GREY_A,
                       max_tip_length_to_length_ratio=0.06)
            arrows.add(VGroup(ar, label(t, font_size=17, color=GREY_A).next_to(ar, UP, buff=0.04)))
        local = label(r"projected to orders: \ $?\,\text{order}.\ !\,\text{charge}.\ "
                      r"?\{\text{ok}: !\text{confirmed},\ \text{declined}: !\text{rejected}\}$", font_size=20,
                      color=HEAD).to_edge(DOWN, buff=1.05)
        lines = wrapped_label(r"session types \ (Honda, \ 1993; \ multiparty: \ Honda, \ Yoshida and Carbone, \ "
                              r"2008) \ and choreographies \ (Montesi): \ write the conversation once, \ check every "
                              r"service against its projection, \ and deadlock is ruled out by construction", 12.4,
                              font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "One line of research treats a protocol between services as a type. <bookmark mark='a'/> Write the "
            "whole conversation once, from above: the client sends an order, the order service asks payments to "
            "charge, payments answers ok or declined, and the order service confirms or rejects. "
            "<bookmark mark='b'/> That global description can be projected onto each participant, giving each "
            "service its own local type: what it receives, what it sends, and in what order. "
            "<bookmark mark='c'/> A compiler can check each service against its projection, and if every one "
            "conforms, the system as a whole cannot deadlock or receive a message it does not expect. These are "
            "session types, introduced by Kohei Honda in 1993 and extended to many parties in 2008, and "
            "choreographic programming, developed by Fabrizio Montesi and others. The open question is how far they "
            "stretch to the failures this part is about: lost messages, retries and crashes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols), Create(lifelines))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a[0]) for a in arrows], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(a[1]) for a in arrows], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(local), Indicate(cols[1], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def proofs(self):
        mc = load("modelcheck")
        g = mc["growth"]
        head = label(r"Checking every execution", font_size=36).to_edge(UP, buff=0.3)
        bars = VGroup()
        lmax = math.log10(g[-1]["states"])
        for k, r in enumerate(g):
            h = 0.3 + 3.0 * math.log10(r["states"]) / lmax
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=KERN, fill_opacity=0.85)
            b.move_to([-5.4 + k * 1.15, -1.9 + h / 2, 0])
            bars.add(VGroup(b, label(f"{r['states']:,}", font_size=16, color=KERN).next_to(b, UP, buff=0.08),
                            label(f"{r['messages']}", font_size=17, color=GREY_B).next_to(b, DOWN, buff=0.1)))
        bl = label(r"messages", font_size=17, color=GREY_B).next_to(bars, DOWN, buff=0.45)
        bt = label(r"states of retry $+$ dedup", font_size=18, color=KERN).next_to(bars, UP, buff=0.45)
        side = VGroup(
            wrapped_label(rf"Chapter 5's check: \ {mc['dedup']['states']:,} states, \ every one safe; \ without "
                          rf"dedup, \ a violation in {len(mc['plain']['trace'])} steps", 6.6, font_size=19,
                          color=YES),
            wrapped_label(r"the state space grows exponentially with the size of the system: \ model checkers "
                          r"\ (Part 33; \ TLA$^+$, \ Part 54) \ check small instances exhaustively", 6.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"Amazon's engineers used TLA$^+$ on DynamoDB, \ S3 and others, \ and found subtle bugs "
                          r"no test had \ (Newcombe et al., \ 2015)", 6.6, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{IronFleet} \ (Dafny) \ and \textbf{Verdi} \ (Coq), \ both 2015: \ distributed "
                          r"systems proved correct for every size, \ down to the running code", 6.6, font_size=19,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In chapter five we checked every execution of a small protocol. <bookmark mark='a'/> With one message "
            f"and one retry there are {g[0]['states']} states; with four messages, {g[-1]['states']:,}. The space "
            "grows exponentially with the system, so a model checker covers small instances completely and large "
            "ones not at all. <bookmark mark='b'/> Even so, small instances find real bugs. Amazon's engineers "
            "wrote TLA-plus models of DynamoDB, S3 and other services, and found subtle errors that no test had "
            "caught. <bookmark mark='c'/> To cover every size, you need proof. In 2015, IronFleet, written in "
            "Dafny, and Verdi, written in Coq, proved distributed systems correct, a replicated state machine and a "
            "key-value store among them, all the way down to the code that runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.3), FadeIn(bl),
                      FadeIn(bt), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()




_ = (DATA, NO, YES)
