from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Process(VoiceoverScene):
    def construct(self):
        self.card()
        self.review()
        self.methods()
        self.integration()
        self.wip()
        self.dora()

    def card(self):
        card = chapter_card(8, r"Review and process", r"How does a team turn work into shipped software?",
                            lit=(1970, 2018), extra=((1970, r"Royce: \ the waterfall, \ criticized"),
                                                     (2001, r"the Agile Manifesto"),
                                                     (2013, r"Bacchelli and Bird: \ code review"),
                                                     (2018, r"Forsgren, Humble and Kim: \ Accelerate")), part=PART)
        with self.voiceover("Chapter eight. Review and process."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def review(self):
        head = label(r"Code review", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"Fagan's inspections at IBM \ (1976): \ formal meetings that read code line by line, \ "
                          r"and found many defects before testing", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"modern review \ (Bacchelli and Bird, \ Microsoft, 2013): \ developers \textit{expect} to "
                          r"find defects, \ but most comments are about understanding, \ alternatives and style; \ "
                          r"the main gains are shared knowledge and awareness", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"size matters: \ reviewers find defects well in a few hundred lines \ at a few hundred "
                          r"lines an hour, \ and poorly beyond \ (the Cisco study, \ 2006)", 12.4, font_size=23,
                          color=YES),
            wrapped_label(r"machines take the mechanical part: \ formatters, \ linters, \ type checkers and static "
                          r"analysis in continuous integration \ (Part 54)", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Before a change is merged, someone else reads it. <bookmark mark='a'/> Michael Fagan's inspections at "
            "IBM in the nineteen seventies were formal meetings that walked through code line by line, and they "
            "caught many defects before testing. <bookmark mark='b'/> Modern review is lighter: a diff and a "
            "conversation. When Alberto Bacchelli and Christian Bird studied it at Microsoft, developers said they "
            "reviewed to find defects, but most comments were about understanding the change, alternatives and "
            "style. The largest benefit was knowledge spreading through the team. <bookmark mark='c'/> Size "
            "matters: reviewers do well on a few hundred lines at a time, read at a few hundred lines an hour, and "
            "poorly beyond that. <bookmark mark='d'/> The mechanical part belongs to machines: formatters, linters, "
            "type checkers and the static analyses of Part 54, run on every change."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def methods(self):
        head = label(r"From waterfall to iterations", font_size=36).to_edge(UP, buff=0.3)
        phases = [r"requirements", r"design", r"code", r"test", r"operate"]
        wf = VGroup()
        for i, p in enumerate(phases):
            b = RoundedRectangle(width=2.2, height=0.5, corner_radius=0.08, stroke_color=DATA, fill_color=DATA,
                                 fill_opacity=0.12).move_to([-5.2 + i * 1.4, 2.0 - i * 0.6, 0])
            wf.add(VGroup(b, label(p, font_size=16, color=WHITE).move_to(b)))
        loop = VGroup()
        cx, cy, R = 3.6, 1.0, 1.3
        for i, p in enumerate([r"plan", r"build", r"review", r"ship", r"learn"]):
            a = PI / 2 - i * TAU / 5
            pos = [cx + (R + 0.45) * math.cos(a), cy + (R + 0.35) * math.sin(a), 0]
            loop.add(label(p, font_size=21, color=YES).move_to(pos))
        ring = Circle(radius=R, color=YES, stroke_width=1.5, fill_opacity=0).move_to([cx, cy, 0]).set_stroke(opacity=0.5)
        lines = VGroup(
            wrapped_label(r"Royce's 1970 paper drew the waterfall \ --- \ and called it ``risky and invites "
                          r"failure'': \ testing comes last, \ when changes cost most", 12.4, font_size=21,
                          color=NO),
            wrapped_label(r"iterative development: \ short cycles that end in working software; \ Scrum's "
                          r"sprints, \ Kanban's flow, \ the Agile Manifesto \ (2001)", 12.4, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How should the work itself be organized? <bookmark mark='a'/> The waterfall, one phase after another "
            "from requirements to operation, is usually traced to Winston Royce's paper of 1970. But Royce drew it "
            "in order to criticize it: he called it risky and an invitation to failure, because testing comes last, "
            "when mistakes are most expensive to fix. <bookmark mark='b'/> The alternative that won is iterative: "
            "short cycles, each ending in working software that people can use and react to. Scrum organizes the "
            "cycles as sprints of a few weeks, each planned, demonstrated and reviewed; Kanban as a continuous flow "
            "of items across a board; and the Agile Manifesto of 2001, written by seventeen practitioners at a ski "
            "resort in Utah, gave the movement its name and its values: working software over documentation, and "
            "responding to change over following a plan."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in wf], lag_ratio=0.25), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(loop), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def wip(self):
        k = load("kanban")
        head = label(r"Work in progress is a queue", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for r in k["rows"]:
            lim = r"none" if r["wip_limit"] is None else f"{r['wip_limit']}"
            rows.append([lim, f"{r['wip']:,.1f}", f"{r['throughput']:.2f}", f"{r['cycle_time']:,.1f} days",
                         f"{r['lead_time']:,.1f} days"])
        tab = grid_table([r"WIP limit", r"items in progress", r"done per day", r"start to done",
                          r"request to done"], rows, widths=[1.9, 2.5, 2.2, 2.6, 2.8], row_h=0.48, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        tab.cells[1][1].set_color(NO)
        tab.cells[1][3].set_color(NO)
        for i in range(2, len(rows) + 1):
            tab.cells[i][3].set_color(YES)
        lines = VGroup(
            MathTex(r"L = \lambda W", font_size=36, color=HEAD),
            wrapped_label(r"four people, \ 0.8 new items a day, \ 4 days of work each; \ juggling items costs "
                          r"5\% per extra item: \ with no limit everything is started, \ nothing finishes", 11.0,
                          font_size=20, color=WHITE),
            wrapped_label(r"Little's law \ (Part 31): \ at a steady throughput, \ fewer items in progress means "
                          r"each finishes sooner; \ limit what you start, \ finish what you started", 11.0,
                          font_size=20, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Kanban's central rule is a limit on work in progress, and Part 31's queueing explains why. "
            "<bookmark mark='a'/> We simulated four people receiving new items at random, eight every ten days on "
            "average, each needing four days of work, where juggling several items costs a little focus for each extra "
            "one. With no limit, everyone starts everything: over a thousand items end up in progress, output "
            "collapses, and an item takes years. <bookmark mark='b'/> With a limit of eight, throughput matches the "
            "arrivals and an item started is done in about six days. Tighter limits shorten that further, while the "
            "wait in the backlog grows: from request to done stays about ten days. <bookmark mark='c'/> It is "
            "Little's law, L equals lambda W: at a given throughput, the time each item spends in progress is "
            "proportional to the number in progress. Stop starting; start finishing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[i])) for i in range(2, len(rows) + 1)],
                                  lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def dora(self):
        head = label(r"Measuring delivery", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"deployment frequency", r"on demand, \ many times a day", r"between once a month and once every "
                 r"six months"],
                [r"lead time for changes", r"less than a day", r"one to six months"],
                [r"change failure rate", r"0--15\%", r"46--60\%"],
                [r"time to restore service", r"less than an hour", r"one week to one month"]]
        tab = grid_table([r"metric", r"elite teams", r"low performers"], rows, widths=[3.6, 3.6, 5.4], row_h=0.6,
                         font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        for i in range(1, 5):
            tab.cells[i][1].set_color(YES)
            tab.cells[i][2].set_color(NO)
        lines = VGroup(
            wrapped_label(r"the DORA research programme \ (Forsgren, Humble and Kim, \ \textit{Accelerate}, \ 2018; "
                          r"\ State of DevOps reports, \ figures from 2019): \ survey data from tens of thousands of "
                          r"professionals", 12.4, font_size=20, color=GREY_A),
            wrapped_label(r"the striking finding: \ speed and stability go together; \ the teams that deploy most "
                          r"often also fail least and recover fastest", 12.4, font_size=21, color=HEAD),
            wrapped_label(r"Goodhart's caution: \ a measure that becomes a target stops measuring", 12.4,
                          font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Can delivery be measured at all? Nicole Forsgren, Jez Humble and Gene Kim proposed four numbers, from "
            "years of surveys of tens of thousands of professionals. <bookmark mark='a'/> How often a team deploys; "
            "how long a change takes from commit to production; what fraction of changes cause a failure; and how "
            "long it takes to restore service. In their 2019 report the elite teams deployed many times a day, "
            "shipped changes within a day, failed on at most fifteen percent of them and recovered within an hour. "
            "<bookmark mark='b'/> The striking finding is that speed and stability were not a trade-off: the teams "
            "that deployed most often also failed least. Small, frequent changes are easier to review, test and "
            "undo. <bookmark mark='c'/> And a caution from the economist Charles Goodhart: once a measure becomes a "
            "target, it stops being a good measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def integration(self):
        m = load("merges")
        head = label(r"Integrate often", font_size=36).to_edge(UP, buff=0.3)

        def iv(h):
            return {1: r"every hour", 4: r"every 4 hours", 24: r"daily", 72: r"every 3 days", 168: r"weekly",
                    336: r"every 2 weeks"}[h]
        rows = [[iv(r["interval_h"]), f"{r['conflict_share'] * 100:.0f}\\%", f"{r['hunks_per_merge']:.2f}",
                 f"{r['hunks_per_week']:.1f}"] for r in m["rows"]]
        tab = grid_table([r"each branch merged", r"merges that conflict", r"conflicts per merge",
                          r"conflicts per week of work"], rows, widths=[3.0, 3.0, 2.8, 3.6], row_h=0.46,
                         font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][3].set_color(YES if m["rows"][k - 1]["hunks_per_week"] < 2 else NO)
        lines = VGroup(
            wrapped_label(rf"{m['devs']} people, \ {m['files']} files \ (a few hot ones), \ "
                          rf"{m['edits_per_day']:.0f} edits a day each; \ a conflict is two branches changing the "
                          r"same region of a file", 12.4, font_size=20, color=GREY_A),
            wrapped_label(r"long branches pay more than in proportion: \ conflicts per week of work grow with the "
                          r"branch's life; \ hence \textbf{continuous integration} \ (Beck, Fowler) \ and "
                          r"trunk-based development", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "How often should a developer's work be merged into everyone else's? <bookmark mark='a'/> We simulated "
            "ten people editing four hundred files, a few of them hot, six edits a day each, each on a branch merged "
            "back at a fixed interval. A conflict is two branches changing the same region of a file. "
            "<bookmark mark='b'/> Merging every hour, almost nothing conflicts. Daily, a third of merges conflict, "
            "lightly. Weekly, nearly every merge conflicts, with eleven clashes to resolve. And per week of work, "
            "the conflicts keep growing as branches live longer: three a week for daily merges, fifteen for "
            "two-week branches. <bookmark mark='c'/> That is the argument for continuous integration, Kent Beck's and "
            "Martin Fowler's practice of merging to the main line at least daily, with tests run on every merge: "
            "small, frequent merges are cheaper in total, not just individually."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(1, len(rows) + 1)],
                                  lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
