from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, trace)


class People(VoiceoverScene):
    def construct(self):
        self.card()
        self.conway()
        self.channels()
        self.brooks()
        self.truck()

    def card(self):
        card = chapter_card(9, r"Teams", r"Why does the shape of a team become the shape of its software?",
                            lit=(1968, 1975), extra=((1968, r"Conway: \ How Do Committees Invent?"),
                                                     (1975, r"Brooks: \ The Mythical Man-Month")), part=PART)
        with self.voiceover("Chapter nine. Teams."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def conway(self):
        head = label(r"Conway's law", font_size=36).to_edge(UP, buff=0.3)
        quote = wrapped_label(r"``Organizations which design systems are constrained to produce designs which are "
                              r"copies of the communication structures of these organizations.'' \ --- \ Melvin "
                              r"Conway, 1968", 12.0, font_size=24, color=HEAD).next_to(head, DOWN, buff=0.55)
        teams = VGroup(*[Circle(radius=0.45, color=c, fill_opacity=0.2).set_fill(c) for c in (DATA, YES, LAM)]
                       ).arrange(RIGHT, buff=1.1).move_to([-3.9, -0.6, 0])
        tl = VGroup(*[label(t, font_size=17, color=WHITE).move_to(c) for t, c in zip((r"web", r"payments", r"data"),
                                                                                   teams)])
        mods = VGroup(*[RoundedRectangle(width=1.4, height=0.7, corner_radius=0.1, stroke_color=c, fill_color=c,
                                         fill_opacity=0.15) for c in (DATA, YES, LAM)]).arrange(RIGHT, buff=0.6)
        mods.move_to([3.9, -0.6, 0])
        ml = VGroup(*[label(t, font_size=16, color=WHITE).move_to(m) for t, m in zip((r"front end", r"billing API",
                                                                                     r"warehouse"), mods)])
        e1 = VGroup(Line(teams[0].get_right(), teams[1].get_left(), color=GREY_B),
                    Line(teams[1].get_right(), teams[2].get_left(), color=GREY_B))
        e2 = VGroup(Line(mods[0].get_right(), mods[1].get_left(), color=GREY_B),
                    Line(mods[1].get_right(), mods[2].get_left(), color=GREY_B))
        arrow = Arrow([-1.2, -0.6, 0], [0.95, -0.6, 0], color=HEAD, buff=0)
        lines = VGroup(
            wrapped_label(r"teams that never talk produce modules that do not fit; \ a module owned by three teams "
                          r"changes slowly", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"the \textbf{inverse Conway manoeuvre}: \ design the teams around the architecture you "
                          r"want \ (one team per service, \ Part 43)", 12.4, font_size=21, color=YES),
            wrapped_label(r"evidence: \ in Microsoft's Windows Vista, \ organizational metrics predicted failure-prone "
                          r"components better than code metrics did \ (Nagappan, Murphy and Basili, 2008)", 12.4,
                          font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1968 Melvin Conway observed that organizations produce systems shaped like themselves. "
            "<bookmark mark='a'/> Three teams, connected the way their people talk, build three modules connected "
            "the same way. <bookmark mark='b'/> Teams that never talk produce modules that do not fit, and a module "
            "owned by three teams changes slowly. <bookmark mark='c'/> Companies now use the law on purpose, the "
            "inverse Conway manoeuvre: decide the architecture first, then draw the teams to match it, one team "
            "for each service. <bookmark mark='d'/> There is evidence: a study of Windows Vista found that measures of "
            "the organization, how many people and teams touched a component, predicted which components would "
            "fail better than measures of the code did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(quote))
            vo.wait_until("a")
            self.play(FadeIn(teams), FadeIn(tl), Create(e1), GrowArrow(arrow), FadeIn(mods), FadeIn(ml), Create(e2))
            for mk, l in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def channels(self):
        head = label(r"$n(n-1)/2$", font_size=40).to_edge(UP, buff=0.3)
        groups = VGroup()
        for k, n in enumerate((3, 5, 8, 12)):
            R = 0.9
            c = [-4.8 + k * 3.2, 0.6, 0]
            pts = [[c[0] + R * math.cos(TAU * i / n + PI / 2), c[1] + R * math.sin(TAU * i / n + PI / 2), 0]
                   for i in range(n)]
            edges = VGroup(*[Line(pts[i], pts[j], stroke_width=1, color=NO).set_opacity(0.6)
                             for i in range(n) for j in range(i + 1, n)])
            dots = VGroup(*[Dot(p, radius=0.07, color=WHITE) for p in pts])
            lb = label(rf"{n} people: \ {n * (n - 1) // 2} channels", font_size=19, color=GREY_A).move_to(
                [c[0], -0.75, 0])
            groups.add(VGroup(edges, dots, lb))
        lines = VGroup(
            wrapped_label(r"work splits $n$ ways; \ coordination grows like $n^2$", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"hence small teams, \ narrow interfaces between them \ (Parnas again), \ and Amazon's "
                          r"``two-pizza'' rule", 12.4, font_size=23, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Brooks gave the arithmetic behind his law. <bookmark mark='a'/> Work can be split among n people, but "
            "if every pair must coordinate, there are n times n minus one over two channels: three for three people, "
            "ten for five, twenty-eight for eight, sixty-six for twelve. <bookmark mark='b'/> The work shrinks like "
            "one over n; the talking grows like n squared. <bookmark mark='c'/> Hence small teams with narrow "
            "interfaces between them, which is Parnas' principle applied to people, and Amazon's rule that a team "
            "should be small enough to feed with two pizzas."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def brooks(self):
        b = load("brooks")
        head = label(r"Brooks' law, \ simulated", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 22, 4], [16, 24, 2], x_length=6.4, y_length=3.6, x_label=rf"month when {b['add']} people join",
                 y_label=r"month the project finishes", xticks=(0, 4, 8, 12, 16, 20), yticks=(16, 18, 20, 22, 24)
                 ).move_to([-2.9, -0.5, 0])
        ax = g.ax
        base = DashedLine(ax.c2p(0, b["base"]), ax.c2p(22, b["base"]), color=GREY_B)
        bl = label(rf"no one added: \ month {b['base']:.1f}", font_size=17, color=GREY_B).next_to(
            ax.c2p(4, b["base"]), UP, buff=0.1)
        pts = [(r["add_at"], r["finish"]) for r in b["late"]]
        cur = VGroup(trace(ax, pts, HEAD, width=3), *[Dot(ax.c2p(x, y), radius=0.06,
                                                          color=YES if y < b["base"] else NO) for x, y in pts])
        notes = VGroup(
            wrapped_label(rf"{b['team']} people, \ {b['work']:.0f} person-months of work; \ newcomers take "
                          rf"{b['ramp']:.0f} months to reach full speed \ and cost a mentor half their time "
                          r"meanwhile; \ every pair pays a small coordination tax", 5.2, font_size=18, color=GREY_A),
            wrapped_label(r"join early: \ the project finishes sooner", 5.2, font_size=20, color=YES),
            wrapped_label(r"join when less time is left than the ramp-up: \ the project finishes \textit{later} "
                          r"--- \ Brooks' law, \ with its condition attached", 5.2, font_size=20, color=NO),
            wrapped_label(r"from the start, \ more people help until coordination dominates: \ our model is fastest "
                          r"near 24 people, \ slower at 40", 5.2, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.7, -0.4, 0])
        with self.voiceover(
            "Is Brooks' law true? We built a model with his mechanisms and nothing else. <bookmark mark='a'/> Six "
            "people and a hundred and twenty person-months of work. Newcomers need six months to reach full speed, "
            "and while they learn they take half the time of an experienced colleague; every pair pays a small tax "
            "for coordination. Without changes the project ends in month twenty-two. <bookmark mark='b'/> Add four "
            "people in month two, and it ends in month eighteen. <bookmark mark='c'/> Add the same four in month "
            "sixteen, with less time left than their ramp-up, and it ends later than if nobody had come. So the law "
            "holds, with a condition Brooks implied: it applies when the project is already late, and the newcomers "
            "cannot become productive before the end. <bookmark mark='d'/> And from the start, more people help "
            "until coordination dominates: in this model a team of twenty-four is fastest, and forty is slower."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            self.play(Create(base), FadeIn(bl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(cur), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def truck(self):
        head = label(r"The truck factor", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{truck factor}: \ the smallest number of people whose loss would stall a "
                          r"project, \ because nobody else knows their code", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"Avelino, Passos, Hora and Valente \ (2016): \ in 133 popular GitHub projects, \ 65\% had "
                          r"a truck factor of 1 or 2", 12.4, font_size=23, color=NO),
            wrapped_label(r"the remedies are the ones this part keeps meeting: \ review \ (knowledge spreads), \ "
                          r"documented interfaces, \ tests that explain intent, \ and rotating who changes what",
                          12.4, font_size=23, color=YES),
            wrapped_label(r"the xz backdoor \ (2024): \ a lone, \ tired maintainer of a widely used compression "
                          r"library was befriended for years by an attacker who became co-maintainer \ (Part 61)",
                          12.4, font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Conway's law has a darker corollary: knowledge lives in people. <bookmark mark='a'/> A project's "
            "truck factor is the smallest number of people whose loss would stall it, because nobody else "
            "understands their code. <bookmark mark='b'/> Guilherme Avelino and colleagues estimated it for a "
            "hundred and thirty-three popular open-source projects: almost two thirds had a truck factor of one or "
            "two. <bookmark mark='c'/> The remedies are the ones this part keeps meeting: review spreads knowledge, "
            "documented interfaces and explanatory tests preserve it, and rotating who changes what keeps it "
            "shared. <bookmark mark='d'/> And a lone maintainer is also a security risk. In 2024 a backdoor was "
            "found in xz, a compression library present on most Linux systems; its author, overworked and alone, "
            "had been befriended over years by an attacker who became co-maintainer. Part 61 returns to it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
