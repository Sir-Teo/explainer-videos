from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace


def step_box(num, title, body, col, w=3.9, h=1.45):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    t = label(rf"{num}. \ {title}", font_size=21, color=col)
    b = wrapped_label(body, w - 0.3, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.1).move_to(r)
    return VGroup(r, t, b)


class Chaos(VoiceoverScene):
    def construct(self):
        self.card()
        self.monkey()
        self.principles()
        self.blast()
        self.inject()

    def card(self):
        card = chapter_card(13, r"Chaos engineering", r"Will it survive a failure it has not had yet?",
                            lit=(2011, 2016), extra=((2011, r"Netflix: \ Chaos Monkey"),
                                                     (2016, r"Basiri et al.: \ Chaos Engineering")), part=PART)
        with self.voiceover("Chapter thirteen. Chaos engineering: breaking a system on purpose, before the world "
                            "does it for you."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def monkey(self):
        head = label(r"Chaos Monkey", font_size=36).to_edge(UP, buff=0.3)
        zones = VGroup()
        for z in range(3):
            frame = RoundedRectangle(width=3.6, height=2.5, corner_radius=0.15, stroke_color=GREY_C, stroke_width=1.8)
            name = label(rf"zone {'abc'[z]}", font_size=19, color=GREY_B).next_to(frame, UP, buff=0.08)
            inst = VGroup(*[Square(side_length=0.55, stroke_color=YES, stroke_width=2, fill_color=YES,
                                   fill_opacity=0.35) for _ in range(8)]).arrange_in_grid(rows=2, cols=4, buff=0.22)
            inst.move_to(frame)
            zones.add(VGroup(frame, name, inst))
        zones.arrange(RIGHT, buff=0.45).move_to([0, 0.35, 0])
        users = label(r"users", font_size=24, color=DATA).next_to(zones, DOWN, buff=0.9)
        flows = VGroup(*[Arrow(users.get_top() + UP * 0.08 + RIGHT * 0.3 * (k - 1), z[0].get_bottom(), buff=0.08,
                               color=DATA, stroke_width=2.5) for k, z in enumerate(zones)])
        kills = ((0, 5), (2, 1), (1, 6))

        def cross(sq):
            return VGroup(Line(sq.get_corner(UL), sq.get_corner(DR), color=NO, stroke_width=4),
                          Line(sq.get_corner(UR), sq.get_corner(DL), color=NO, stroke_width=4))
        x_marks = VGroup(*[cross(zones[z][2][i]) for z, i in kills])
        sch = note(r"schematic", font_size=16).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        tags = VGroup(
            label(r"Chaos Monkey: \ terminate an instance at random, \ in working hours", font_size=19, color=NO),
            label(r"Chaos Gorilla: \ take out a whole zone", font_size=19, color=KERN),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "When Netflix moved its streaming service onto Amazon's cloud, its engineers accepted that any machine "
            "could vanish at any moment, and decided to make sure their services believed it too. <bookmark "
            "mark='a'/> They wrote Chaos Monkey, a program that picks instances at random and terminates them, in "
            "production. <bookmark mark='b'/> It runs during working hours, when the engineers who must respond are "
            "at their desks. A service that cannot lose one machine is found out on a Tuesday afternoon, not at "
            "three in the morning. <bookmark mark='c'/> In 2011 Netflix described a whole Simian Army. Latency "
            "Monkey added delays, and Chaos Gorilla took out an entire availability zone, so that traffic had to "
            "move to the others. Later, Chaos Kong drilled the evacuation of a whole region."
        ) as vo:
            self.play(FadeIn(head), FadeIn(zones), FadeIn(users), *[GrowArrow(f) for f in flows], FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(tags[0]))
            for (z, i), x in zip(kills, x_marks):
                sq = zones[z][2][i]
                self.play(Create(x), sq.animate.set_fill(NO, 0.15).set_stroke(NO), run_time=0.6)
            vo.wait_until("b")
            self.play(*[zones[z][2][i].animate.set_fill(YES, 0.35).set_stroke(YES) for z, i in kills],
                      FadeOut(x_marks))
            vo.wait_until("c")
            self.play(FadeIn(tags[1]), zones[1][0].animate.set_stroke(NO), zones[1][2].animate.set_opacity(0.15),
                      FadeOut(flows[1]))
            self.play(flows[0].animate.set_stroke(width=5), flows[2].animate.set_stroke(width=5))
        self.wait(0.4)
        self.clear_scene()

    def principles(self):
        head = label(r"An experiment, \ not an accident", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            step_box(1, r"steady state", r"a measurable output users feel: \ Netflix used stream starts per second",
                     DATA),
            step_box(2, r"hypothesis", r"it stays the same in the experiment group as in the control group", HEAD),
            step_box(3, r"real-world events", r"crashes, \ partitions, \ latency, \ bad deployments, \ load spikes",
                     NO),
            step_box(4, r"look for a difference", r"one found is a weakness, \ found before the world found it", YES),
        )
        pos = ([-3.2, 1.25, 0], [3.2, 1.25, 0], [3.2, -1.25, 0], [-3.2, -1.25, 0])
        for s, p in zip(steps, pos):
            s.move_to(p)
        arrows = VGroup(*[CurvedArrow(steps[k][0].get_edge_center(d1) + o1, steps[(k + 1) % 4][0].get_edge_center(d2)
                                      + o2, angle=-PI / 5, color=GREY_B, stroke_width=2.5)
                          for k, (d1, d2, o1, o2) in enumerate(((RIGHT, LEFT, ORIGIN, ORIGIN),
                                                                (DOWN, UP, ORIGIN, ORIGIN),
                                                                (LEFT, RIGHT, ORIGIN, ORIGIN),
                                                                (UP, DOWN, ORIGIN, ORIGIN)))])
        centre = wrapped_label(r"in production, \ automated, \ continuously", 2.0, font_size=19, color=WHITE)
        centre.move_to(ORIGIN)
        cite = wrapped_label(r"Basiri, \ Behnam, \ de Rooij, \ Hochstein, \ Kosewski, \ Reynolds and Rosenthal, \ "
                             r"\emph{IEEE Software}, \ 2016", 12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2016 Ali Basiri and his colleagues at Netflix set out the discipline as a scientific method. "
            "<bookmark mark='a'/> First, define the steady state: a measurable output that users feel, not an "
            "internal gauge. Netflix used the number of streams started per second. <bookmark mark='b'/> Second, "
            "state a hypothesis: that the steady state will be the same in an experiment group as in a control "
            "group. <bookmark mark='c'/> Third, inject the events the real world produces: machines crashing, "
            "networks partitioning, replies slowing, bad deployments, sudden load. <bookmark mark='d'/> Fourth, look "
            "for a difference between the two groups. If there is none, confidence grows. If there is one, you "
            "have found a weakness before your users did. <bookmark mark='e'/> And do it in production, because "
            "only production has production's traffic, and do it continuously, because the system changes every "
            "day."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite))
            for mk, s, a in zip("abcd", steps, arrows):
                vo.wait_until(mk)
                self.play(FadeIn(s), Create(a))
            vo.wait_until("e")
            self.play(FadeIn(centre))
        self.wait(0.4)
        self.clear_scene()

    def blast(self):
        c = load("chaos")
        pm = c["runs"]["naive"]["per_minute"]
        crash = next(f for f in c["faults"] if f["kind"] == "crash")
        t0 = crash["from"]
        head = label(r"Blast radius, \ and the abort switch", font_size=36).to_edge(UP, buff=0.3)
        # the traffic split
        W, y = 12.0, 2.2
        whole = Rectangle(width=W, height=0.45, stroke_color=GREY_C, stroke_width=1.5, fill_color=GREY_E,
                          fill_opacity=1).move_to([0, y, 0])
        slice_w = 0.24                                  # 2% of the bar, drawn a little wider to be seen
        ctl = Rectangle(width=slice_w, height=0.45, stroke_width=0, fill_color=DATA, fill_opacity=1).move_to(
            whole.get_left() + RIGHT * slice_w / 2)
        exp = Rectangle(width=slice_w, height=0.45, stroke_width=0, fill_color=NO, fill_opacity=1).next_to(
            ctl, RIGHT, buff=0)
        rest_l = label(r"everyone else: \ untouched", font_size=18, color=GREY_A).move_to(whole).shift(RIGHT * 0.5)
        sl_l = label(r"control 1\%, \ experiment 1\%", font_size=18, color=WHITE).next_to(ctl, DOWN, buff=0.12)
        sl_l.align_to(whole, LEFT)
        # the experiment group's good requests, minute by minute, around the injected crash
        n_m = t0 + 6
        g = axes([0, n_m, 2], [0.6, 1.0, 0.1], x_length=6.6, y_length=3.0, x_label=r"minute",
                 xticks=range(0, n_m + 1, 2), yticks=(0.6, 0.8, 1.0), fy=lambda v: rf"{100 * v:.0f}\%")
        g.move_to([-2.6, -1.05, 0])
        ax = g.ax
        ctl_line = trace(ax, [(0, 1.0), (n_m, 1.0)], DATA, width=3)
        cut = t0 + 1
        live = trace(ax, [(m + 0.5, v) for m, v in enumerate(pm[:cut])], NO, width=3.5)
        ghost = DashedVMobject(trace(ax, [(m + 0.5, pm[m]) for m in range(cut - 1, n_m)], GREY_C, width=2),
                               num_dashes=24)
        thr = DashedLine(ax.c2p(0, 0.999), ax.c2p(n_m, 0.999), color=HEAD, stroke_width=1.5)
        stop = Line(ax.c2p(cut, 0.6), ax.c2p(cut, 1.0), color=HEAD, stroke_width=3)
        stop_l = label(r"abort", font_size=18, color=HEAD).next_to(stop, UP, buff=0.08)
        inj = label(r"crash injected", font_size=17, color=NO).next_to(ax.c2p(t0, 0.66), LEFT, buff=0.12)
        # the cost
        bad = 0.01 * (1 - pm[t0])                         # 1% of traffic, for one minute, losing that share
        month_min = 30 * 24 * 60
        cost = bad / (0.001 * month_min)
        full = c["runs"]["naive"]["budget_share"]
        notes = VGroup(
            wrapped_label(rf"abort rule: \ stop as soon as the experiment group misses the 99.9\% objective for a "
                          rf"minute", 4.6, font_size=19, color=HEAD),
            wrapped_label(rf"cost: \ 1\% of traffic, \ losing {100 * (1 - pm[t0]):.0f}\% for one minute: \ "
                          rf"{100 * cost:.3f}\% of the month's error budget", 4.6, font_size=19, color=YES),
            wrapped_label(rf"unconfined, \ all traffic for chapter 14's whole hour of faults: \ {100 * full:.0f}\%",
                          4.6, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.5).align_to(g, UP)
        with self.voiceover(
            "Experimenting in production is responsible only if the damage is bounded, so the practitioners' "
            "published principles add a fifth rule: minimise the blast radius. <bookmark mark='a'/> Route a small "
            "slice of users, say one percent, to the experiment, and another one percent to a control group with no "
            "fault. Everyone else is untouched. <bookmark mark='b'/> Now crash one of the Job service's three "
            "replicas, under the naive client of chapter fourteen. The experiment group loses a third of its "
            "requests at once. <bookmark mark='c'/> An abort rule, written before the start, stops the experiment "
            "as soon as the group misses the objective for a minute. The dashed line is what it spared them. "
            "<bookmark mark='d'/> The experiment cost under a hundredth of a percent of the month's error budget. "
            "Unconfined, on all traffic for chapter fourteen's hour of faults, the same weakness costs thirteen "
            "percent. The hypothesis was refuted, cheaply."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(whole), FadeIn(rest_l))
            self.play(FadeIn(ctl), FadeIn(exp), FadeIn(sl_l))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(thr), Create(ctl_line))
            self.play(Create(live), FadeIn(inj), run_time=2)
            vo.wait_until("c")
            self.play(Create(stop), FadeIn(stop_l), FadeIn(notes[0]))
            self.play(Create(ghost))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def inject(self):
        r = load("raft")
        head = label(r"How faults are injected", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"crash", r"kill the process; \ terminate the instance", r"refused at once"],
                [r"partition", r"a firewall rule drops the packets", r"no reply: \ wait out the timeout"],
                [r"slow", r"queueing delay added in the kernel \ (\texttt{tc netem})", r"ten times the latency"]]
        tab = grid_table([r"fault", r"in production", r"in our simulator"], rows, widths=[1.8, 5.6, 4.4],
                         row_h=0.7, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        for i, col in enumerate((NO, LAM, KERN), start=1):
            tab.cells[i][0].set_color(col)
        steps = [m["what"] for m in r["script"]]
        hyp = {"crash the leader": r"a new leader within a few election timeouts; \ nothing committed is lost",
               "partition 2 | 3": r"the old leader, \ in the minority, \ can commit nothing; \ the majority goes on",
               "crash two followers": r"no pause at all: \ three of five is still a majority"}
        hrows = VGroup()
        for s in steps:
            if s in hyp:
                a = label(s.replace("|", r"$|$"), font_size=19, color=HEAD)
                b = wrapped_label(hyp[s], 7.4, font_size=19, color=WHITE)
                hrows.add(VGroup(a, b))
        for row in hrows:
            row[0].move_to([-6.4, 0, 0], aligned_edge=LEFT)
            row[1].move_to([-2.0, 0, 0], aligned_edge=LEFT)
        hrows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        for row in hrows:
            row[1].align_to([-2.0, 0, 0], LEFT)
        ttl = label(r"Part 38's Raft cluster: \ the hypotheses, \ written before the run", font_size=21,
                    color=GREY_A)
        VGroup(ttl, hrows).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(tab, DOWN, buff=0.8).to_edge(
            LEFT, buff=0.55)
        foot = label(r"chapter 14 runs both experiments", font_size=20, color=YES).to_edge(DOWN, buff=0.3).to_edge(
            RIGHT, buff=0.6)
        with self.voiceover(
            "How is a fault injected? <bookmark mark='a'/> A crash is the easiest: kill the process, or terminate "
            "the machine, and connections are refused at once. <bookmark mark='b'/> A partition is a firewall rule "
            "that silently drops packets, so a caller hears nothing and must wait out its timeout. <bookmark "
            "mark='c'/> Slowness is added in the kernel's queueing layer by Linux's network emulator: chapter "
            "three's gray failure. Our simulator models all three. <bookmark mark='d'/> For Part 38's Raft cluster "
            "the hypotheses are stronger, because consensus promises more. Crash the leader: a new one within a few "
            "election timeouts, and nothing committed lost. Cut the leader off in a minority: it can commit "
            "nothing, while the majority carries on. Crash two of five followers: no pause at all. <bookmark "
            "mark='e'/> Written down before the run, each is a claim that can fail. Chapter fourteen runs both "
            "experiments."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            for mk, row in zip("abc", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*row)))
            vo.wait_until("d")
            self.play(FadeIn(ttl))
            for row in hrows:
                self.play(FadeIn(row), run_time=0.8)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, YES)
