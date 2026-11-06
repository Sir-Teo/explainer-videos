from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, module_box, trace)


class Delivery(VoiceoverScene):
    def construct(self):
        self.card()
        self.strategies()
        self.canary()
        self.dark()
        self.migrations()
        self.knight()
        self.rollback()
        self.pipeline()

    def card(self):
        card = chapter_card(7, r"Continuous delivery", r"How do you change a running system safely?",
                            lit=(2010, 2016), extra=((2010, r"Humble and Farley: \ Continuous Delivery"),
                                                     (2016, r"Google: \ the SRE book")), part=PART)
        with self.voiceover("Chapter seven. Continuous delivery."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def strategies(self):
        head = label(r"Releasing a little at a time", font_size=36).to_edge(UP, buff=0.3)
        W, y = 10.0, 1.6
        frame = Rectangle(width=W, height=0.55, stroke_color=GREY_B, stroke_width=1.5).move_to([0, y, 0])
        share = ValueTracker(0.0)

        def new_bar():
            w = max(0.001, W * share.get_value())
            return Rectangle(width=w, height=0.55, stroke_width=0, fill_color=YES, fill_opacity=0.85).move_to(
                [-W / 2 + w / 2, y, 0])
        old_bar = Rectangle(width=W, height=0.55, stroke_width=0, fill_color=DATA, fill_opacity=0.55).move_to(
            [0, y, 0])
        nb = always_redraw(new_bar)
        pct = always_redraw(lambda: label(rf"{100 * share.get_value():.0f}\% \ of requests on the new version",
                                          font_size=20, color=YES).next_to(frame, DOWN, buff=0.2))
        users = label(r"all requests", font_size=18, color=GREY_B).next_to(frame, UP, buff=0.15)
        stages = VGroup(*[label(t, font_size=18, color=HEAD).move_to([-W / 2 + W * f, y + 0.6, 0])
                          for t, f in ((r"1\%", 0.01), (r"5\%", 0.05), (r"25\%", 0.25), (r"100\%", 1.0))])
        flag = VGroup(RoundedRectangle(width=0.9, height=0.45, corner_radius=0.22, stroke_color=LAM, fill_color=BG,
                                       fill_opacity=1), Dot(radius=0.15, color=LAM))
        flag[1].move_to(flag[0].get_left() + RIGHT * 0.23)
        flag_l = label(r"a feature flag: \ off", font_size=18, color=LAM).next_to(flag, RIGHT, buff=0.2)
        flag_g = VGroup(flag, flag_l).move_to([0, -0.35, 0])
        lines = VGroup(
            wrapped_label(r"\textbf{blue/green}: \ run the new version beside the old, \ switch the traffic at once, "
                          r"\ switch back if it fails", 12.4, font_size=20, color=DATA),
            wrapped_label(r"\textbf{canary}: \ send a small share of traffic to the new version and compare it with "
                          r"the old \ (the miners' bird, \ which showed the gas first)", 12.4, font_size=20,
                          color=YES),
            wrapped_label(r"\textbf{progressive rollout}: \ 1\%, \ 5\%, \ 25\%, \ 100\%, \ with automatic rollback "
                          r"at any stage", 12.4, font_size=20, color=HEAD),
            wrapped_label(r"\textbf{feature flags}: \ ship code switched off, \ turn it on for some users later: \ "
                          r"deploying and releasing become separate decisions", 12.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A merged change is not yet running for anyone. Delivering it safely means never betting everything on "
            "one moment. <bookmark mark='a'/> Blue-green deployment runs the new version beside the old and switches "
            "traffic at once, keeping the old one ready to switch back. <bookmark mark='b'/> A canary, named for the "
            "birds miners carried to detect gas, sends a small share of traffic to the new version and compares it "
            "with the old. <bookmark mark='c'/> Progressive rollout widens the share in stages, one percent, five, "
            "twenty-five, all, rolling back automatically at any stage. <bookmark mark='d'/> And feature flags ship "
            "new code switched off, to be turned on for some users later, so that deploying code and releasing a "
            "feature become separate decisions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old_bar), Create(frame), FadeIn(users))
            self.add(nb, pct)
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            self.play(share.animate.set_value(1.0), run_time=1.0)
            self.play(share.animate.set_value(0.0), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), share.animate.set_value(0.01))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), FadeIn(stages))
            for f in (0.05, 0.25, 1.0):
                self.play(share.animate.set_value(f), run_time=1.2)
                self.wait(0.3)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]), FadeIn(flag_g))
            self.play(flag[1].animate.move_to(flag[0].get_right() + LEFT * 0.23).set_color(YES),
                      Transform(flag_l, label(r"a feature flag: \ on for 5\% of users", font_size=18,
                                              color=LAM).next_to(flag, RIGHT, buff=0.2).align_to(flag_l, LEFT)))
        self.wait(0.4)
        self.clear_scene()

    def canary(self):
        c = load("canary")
        head = label(r"Is the canary sick?", font_size=36).to_edge(UP, buff=0.3)
        import math
        rows = c["rows"]
        g = axes([2.8, 5.2, 0.5], [0, 1.05, 0.25], x_length=6.6, y_length=3.6, x_label=r"requests to each version",
                 y_label=r"probability", xticks=(3, 3.5, 4, 4.5, 5), yticks=(0.25, 0.5, 0.75, 1.0),
                 fx=lambda v: {3: "1,000", 3.5: "3,000", 4: "10,000", 4.5: "30,000", 5: "100,000"}.get(v, ""),
                 fy=lambda v: f"{v * 100:.0f}\\%").move_to([-2.6, -0.4, 0])
        ax = g.ax
        pw = VGroup(trace(ax, [(math.log10(r["requests"]), r["power"]) for r in rows], YES, width=3),
                    *[Dot(ax.c2p(math.log10(r["requests"]), r["power"]), radius=0.06, color=YES) for r in rows])
        fa = VGroup(trace(ax, [(math.log10(r["requests"]), r["false_alarm"]) for r in rows], NO, width=3),
                    *[Dot(ax.c2p(math.log10(r["requests"]), r["false_alarm"]), radius=0.06, color=NO) for r in rows])
        r30 = next(r for r in rows if r["requests"] == 30000)
        notes = VGroup(
            wrapped_label(rf"the old version fails {c['base_rate'] * 100:.1f}\% of requests; \ a bad new one fails "
                          rf"{c['bad_rate'] * 100:.1f}\%: \ twice as often, \ still rare", 5.0, font_size=19,
                          color=GREY_A),
            label(r"bad releases caught", font_size=19, color=YES),
            label(rf"good releases wrongly blocked \ ($\alpha = {c['alpha']}$)", font_size=19, color=NO),
            wrapped_label(rf"a one-sided test of two proportions: \ with 3{{,}}000 requests a bad release is caught "
                          rf"{rows[1]['power'] * 100:.0f}\% of the time; \ with 30{{,}}000, \ "
                          rf"{r30['power'] * 100:.0f}\%", 5.0, font_size=19, color=WHITE),
            wrapped_label(r"rare failures need a lot of traffic to see: \ the canary's size is a statistics "
                          r"question \ (Part 44)", 5.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.1, -0.2, 0])
        with self.voiceover(
            "How big must a canary be? It is a question of statistics. <bookmark mark='a'/> Suppose the old version "
            "fails one request in a thousand, and a bad new version fails two in a thousand: twice as often, and "
            "still rare. Compare the two with a standard test of proportions, allowing one false alarm in a hundred. "
            "<bookmark mark='b'/> With a thousand requests to each, the bad release is almost never caught: one or "
            "two failures cannot be told from noise. With three thousand, seven percent of the time; with thirty "
            "thousand, eighty. <bookmark mark='c'/> Rare failures need a lot of traffic to see, which is why canaries "
            "run for hours, and why Part 44 treats these comparisons as experiments with power calculations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
            vo.wait_until("b")
            self.play(Create(pw), Create(fa), FadeIn(notes[3]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    def migrations(self):
        head = label(r"Changing a database under running code", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(*[module_box(t, c, w=2.6, h=0.9, font=17) for t, c in (
            (r"1. \ expand: \\ add the new column", YES), (r"2. \ write both", HEAD), (r"3. \ backfill old rows", DATA),
            (r"4. \ read the new", LAM), (r"5. \ contract: \\ drop the old", NO))]).arrange(RIGHT, buff=0.25)
        steps.next_to(head, DOWN, buff=0.8)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.03, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        lines = VGroup(
            wrapped_label(r"old and new code run side by side during a rollout, \ so every schema must work with "
                          r"both: \ never rename in place", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"each step is deployed, \ verified, \ and reversible on its own; \ only the last one "
                          r"loses information, \ and it runs when nothing reads the old column", 12.4, font_size=22,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The hardest changes to deliver are changes to stored data, because during a rollout the old and new "
            "versions of the code run side by side against the same database. <bookmark mark='a'/> So schema "
            "changes go in expand and contract steps. Add the new column. Make the code write both old and new. "
            "Copy the old rows across. Switch reads to the new column. And only then, when nothing reads the old "
            "column, drop it. <bookmark mark='b'/> Each step is deployed and verified on its own and can be undone; "
            "only the last destroys anything, and it runs when nobody needs what it destroys."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.3), Create(arrows), FadeIn(lines[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def pipeline(self):
        head = label(r"The Job's change, \ end to end", font_size=36).to_edge(UP, buff=0.3)
        stages = [(r"commit", r"a Merkle node", DATA), (r"review", r"Part 40", HEAD), (r"merge queue",
                  r"batches, \ bisection", YES), (r"build", r"hashes, \ cache", LAM), (r"canary", r"30{,}000 "
                  r"requests", KERN), (r"rollout", r"1\% $\to$ 100\%", YES)]
        boxes = VGroup()
        for i, (a, b, c) in enumerate(stages):
            bx = module_box(a, c, w=1.8, h=0.7, font=18)
            sub = label(b, font_size=15, color=GREY_A).next_to(bx, DOWN, buff=0.12)
            boxes.add(VGroup(bx, sub))
        boxes.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=1.0)
        arrows = VGroup(*[Arrow(boxes[i][0].get_right(), boxes[i + 1][0].get_left(), buff=0.03, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(len(stages) - 1)])
        lines = VGroup(
            wrapped_label(r"a one-line change to the Job's word counter: \ named by a hash, \ reviewed, \ merged "
                          r"only when tested on top of main, \ rebuilt only where its hash changed, \ and released to "
                          r"a few users before all of them", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"at every stage the question is the same: \ what is the least we must redo, \ and how "
                          r"do we know we may stop?", 12.4, font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Follow one change through all of it: a single line in the Job's word counter. <bookmark mark='a'/> It "
            "becomes a commit, a new node in the Merkle graph whose name vouches for the whole history. People "
            "review it. The merge queue tests it on top of everything ahead of it. The build recompiles only what "
            "its hash touches and fetches the rest from the cache. A canary compares it against the old version on "
            "real traffic, and the rollout widens step by step. <bookmark mark='b'/> At every stage the question is "
            "the one the build system asked: what is the least we must redo, and how do we know we can stop?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.35), Create(arrows), FadeIn(lines[0]),
                      run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def knight(self):
        head = label(r"When a release goes wrong", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{Knight Capital}, \ 1 August 2012: \ new trading code reused an old feature flag; \ "
                          r"one of eight servers had not received the new code, \ so the flag woke up code dead for "
                          r"nine years", 12.4, font_size=20, color=NO),
            wrapped_label(r"in 45 minutes it sent millions of unintended orders and lost about \$440 million: \ the "
                          r"firm needed rescue within days \ (SEC order, 2013)", 12.4, font_size=20, color=NO),
            wrapped_label(r"the lessons are this part's: \ deploy the same artifact everywhere and verify it, \ remove "
                          r"dead code and retired flags, \ roll out gradually, \ and keep an automatic stop", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"flags are debt: \ every flag doubles the states the code can be in \ --- \ track them, \ and "
                          r"delete them once the rollout is done", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        servers = VGroup()
        for i in range(8):
            ok = i != 7
            r = RoundedRectangle(width=1.25, height=1.0, corner_radius=0.1, stroke_color=YES if ok else NO,
                                 stroke_width=2, fill_color=BG, fill_opacity=1)
            t = VGroup(label(rf"server {i + 1}", font_size=16, color=GREY_A),
                       label(r"new code" if ok else r"old code", font_size=16, color=YES if ok else NO)).arrange(
                DOWN, buff=0.08).move_to(r)
            servers.add(VGroup(r, t))
        servers.arrange(RIGHT, buff=0.22).next_to(head, DOWN, buff=0.5)
        flag_l = label(r"the reused flag switched on \ $\to$ \ a function dead since 2003", font_size=18,
                       color=NO).next_to(servers[7], DOWN, buff=0.2).align_to(servers[7], RIGHT)
        orders = VGroup(*[Arrow(servers[7].get_bottom() + DOWN * 0.55, servers[7].get_bottom() + DOWN * 0.55 +
                                LEFT * (1.2 + 0.5 * j), buff=0, stroke_width=2, color=NO,
                                max_tip_length_to_length_ratio=0.15) for j in range(4)])
        with self.voiceover(
            "Delivery failures can be very expensive. <bookmark mark='a'/> On the first of August 2012, Knight "
            "Capital deployed new trading code that reused an old feature flag. One of its eight servers had not "
            "received the new code, so on that server the flag switched on a function that had been dead for nine "
            "years. <bookmark mark='b'/> In forty-five minutes it sent millions of unintended orders and lost about "
            "four hundred and forty million dollars; the firm needed rescuing within days. "
            "<bookmark mark='c'/> The lessons are this part's: deploy one artifact everywhere and verify that it "
            "arrived, delete dead code and retired flags, roll out gradually, and keep an automatic way to stop. "
            "<bookmark mark='d'/> Flags are a form of debt: each one doubles the states the code can be in, so they "
            "must be tracked and removed when their rollout is over."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(sv) for sv in servers], lag_ratio=0.15), FadeIn(lines[0]))
            self.play(Indicate(servers[7], color=NO), FadeIn(flag_l))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), LaggedStart(*[GrowArrow(o) for o in orders], lag_ratio=0.2))
            for mk, l in zip("cd", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def rollback(self):
        head = label(r"Back, \ or forward?", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{roll back}: \ return to the last good release \ --- \ fast and safe, \ if the "
                          r"release changed nothing that cannot be undone", 12.4, font_size=23, color=YES),
            wrapped_label(r"\textbf{roll forward}: \ fix and ship again \ --- \ needed once data or clients have "
                          r"moved on \ (a contracted schema, \ a new file format already written)", 12.4,
                          font_size=23, color=HEAD),
            wrapped_label(r"small, \ frequent releases make both easy: \ a change of ten lines is quick to revert, \ "
                          r"to review and to bisect \ (Part 40's DORA finding)", 12.4, font_size=23, color=DATA),
            wrapped_label(r"the rule that follows: \ every release must be revertible until its last irreversible "
                          r"step, \ and that step comes last", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "When a release goes wrong, there are two ways out. <bookmark mark='a'/> Rolling back returns to the last "
            "good version. It is fast and safe, provided the release changed nothing that cannot be undone. "
            "<bookmark mark='b'/> Rolling forward means fixing the problem and shipping again, and it is the only "
            "option once data or clients have moved on: a schema already contracted, files already written in a new "
            "format. <bookmark mark='c'/> Small, frequent releases make both easy, because a change of ten lines is "
            "quick to revert, to review and to bisect, which is the mechanism behind Part 40's DORA finding. "
            "<bookmark mark='d'/> The rule that follows is the expand-and-contract rule again: keep every release "
            "revertible until its last irreversible step, and make that step come last."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def dark(self):
        head = label(r"Testing in production, \ safely", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{shadow traffic}: \ copy real requests to the new version and compare its answers "
                          r"with the old one's, \ while users only ever see the old", 12.4, font_size=23,
                          color=YES),
            wrapped_label(r"\textbf{dark launch}: \ run a new feature's work for real users with its results hidden, \ "
                          r"to measure its load before anyone depends on it", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"\textbf{kill switches}: \ a flag that turns a feature off in seconds, \ without a "
                          r"deploy, \ tested like any other code path", 12.4, font_size=23, color=NO),
            wrapped_label(r"each turns a release from one irreversible moment into a series of measured, \ "
                          r"reversible steps", 12.4, font_size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Some failures appear only under real traffic, so large services test there, carefully. "
            "<bookmark mark='a'/> Shadow traffic copies real requests to the new version and compares its answers "
            "with the old version's, while users only ever see the old ones. <bookmark mark='b'/> A dark launch runs "
            "a new feature's work for real users with the results hidden, to measure its cost before anyone depends "
            "on it. <bookmark mark='c'/> And a kill switch is a flag that turns a feature off in seconds without a "
            "deploy, which must itself be tested, since it is used only on the worst day. <bookmark mark='d'/> Each "
            "of these turns a release from one irreversible moment into a series of measured, reversible steps."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
