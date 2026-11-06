from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.compute import load as load39
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, module_box, trace


def log_strip(n_filled, n=8, color=DATA, side=0.26):
    """A replication log: n slots, the first n_filled holding entries."""
    g = VGroup(*[Square(side_length=side, stroke_color=GREY_C, stroke_width=1.2,
                        fill_color=color, fill_opacity=0.8 if k < n_filled else 0.0) for k in range(n)])
    return g.arrange(RIGHT, buff=0.04)


class Replication(VoiceoverScene):
    def construct(self):
        self.card()
        self.replicas()
        self.lag()
        self.failover()
        self.fencing()
        self.active()

    def card(self):
        card = chapter_card(9, r"Replication in practice", r"What do copies cost when the leader can fail?",
                            lit=(2006, 2006), extra=((2006, r"Burrows: \ Chubby's lock sequencers"),), part=PART)
        with self.voiceover("Chapter nine. Replication in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ leader and read replicas
    def replicas(self):
        head = label(r"One leader, \ many readers", font_size=36).to_edge(UP, buff=0.3)
        leader = module_box(r"leader", KERN, w=1.8, h=0.6, font=20).move_to([-3.6, 1.6, 0])
        fol = VGroup(module_box(r"follower 1", DATA, w=1.8, h=0.6, font=19).move_to([-5.3, -1.0, 0]),
                     module_box(r"follower 2", DATA, w=1.8, h=0.6, font=19).move_to([-1.9, -1.0, 0]))
        llog = log_strip(5, color=KERN).next_to(leader, DOWN, buff=0.15)
        flogs = VGroup(log_strip(4).next_to(fol[0], DOWN, buff=0.15), log_strip(3).next_to(fol[1], DOWN, buff=0.15))
        ship = VGroup(*[DashedLine(llog.get_bottom(), f.get_top(), buff=0.1, color=KERN, stroke_width=2,
                                   dash_length=0.1).add_tip(tip_length=0.15) for f in fol])
        shl = label(r"the log, \ shipped", font_size=17, color=KERN).move_to([-3.6, 0.05, 0])
        wl = label(r"writes", font_size=19, color=HEAD).move_to([-6.2, 2.55, 0])
        rl = label(r"reads", font_size=19, color=YES).move_to([-3.6, -2.6, 0])
        w = Dot([-6.2, 2.25, 0], radius=0.09, color=HEAD)
        reads = [Dot([-3.6, -2.3, 0], radius=0.08, color=YES) for _ in range(4)]
        notes = VGroup(
            wrapped_label(r"every write goes to the leader, \ which appends it to its log", 5.2, font_size=19,
                          color=KERN),
            wrapped_label(r"followers replay the log; \ reads, \ usually most of the traffic, \ spread across "
                          r"them, \ and each is a warm spare", 5.2, font_size=19, color=YES),
            wrapped_label(r"the log takes time to ship: \ a follower is behind by milliseconds normally, \ and by "
                          r"far more under load", 5.2, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 0.3, 0])
        foot = note(r"schematic", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Part 39 gave the theory of replication; here is how it is used day to day. <bookmark mark='a'/> Most "
            "systems start with one leader that takes every write and appends it to a log. "
            "<bookmark mark='b'/> Followers replay that log. Reads, usually the bulk of the traffic, spread across "
            "the followers, so each new follower adds read capacity, and is a warm spare besides. "
            "<bookmark mark='c'/> The catch is that shipping the log takes time. A follower's copy is a little "
            "behind: by milliseconds normally, and by far more when it is overloaded."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leader), FadeIn(fol), FadeIn(llog), FadeIn(flogs), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(wl), FadeIn(w), FadeIn(notes[0]))
            self.play(w.animate.move_to(leader), run_time=0.8)
            self.play(FadeOut(w), llog[5].animate.set_fill(KERN, 0.8))
            vo.wait_until("b")
            self.play(Create(ship), FadeIn(shl), flogs[0][4].animate.set_fill(DATA, 0.8))
            self.add(*reads)
            self.play(FadeIn(rl), FadeIn(notes[1]),
                      LaggedStart(*[r.animate.move_to(fol[k % 2]) for k, r in enumerate(reads)], lag_ratio=0.3),
                      run_time=2.0)
            self.remove(*reads)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), Indicate(flogs[1][3:6], color=NO), flogs[1][3].animate.set_fill(DATA, 0.8))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ replication lag
    def lag(self):
        L = load39("lag")
        rows = L["rows"]
        head = label(r"Reading your own writes", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 500, 100], [0, 0.8, 0.2], x_length=6.0, y_length=3.6,
                 x_label=r"time from the write to the read, \ ms", y_label=r"reads that miss the user's own write",
                 xticks=[0, 100, 200, 300, 400, 500], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 fy=lambda v: rf"{100 * v:.0f}\%", font=16)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.15)
        ax = g.ax
        pts = [(r["t_ms"], r["violations"]) for r in rows]
        line = trace(ax, pts, NO, width=3)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=NO) for x, y in pts])
        vals = VGroup(*[label(rf"{100 * y:.1f}\%" if y < 0.01 else rf"{100 * y:.0f}\%", font_size=17, color=NO)
                        .next_to(ax.c2p(x, y), UR, buff=0.08) for x, y in pts if x in (0, 100, 500)])
        setup = wrapped_label(rf"Part 39's simulation: \ followers apply a write after {L['lag_ms']} ms on average; "
                              rf"\ the next read goes to any of {L['followers'] + 1} replicas", 5.4, font_size=19,
                              color=GREY_A)
        fixes = VGroup(
            label(r"two fixes", font_size=22, color=YES),
            wrapped_label(r"1. \ for a short while after a user writes, \ send that user's reads to the leader",
                          5.4, font_size=19, color=WHITE),
            wrapped_label(r"2. \ the write returns its log position; \ read only from a replica that has reached "
                          r"it, \ or wait until one has", 5.4, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(setup, fixes).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.75, 0.1, 0])
        with self.voiceover(
            "That lag breaks a promise users take for granted: to see what they just wrote. "
            "<bookmark mark='a'/> In Part 39's simulation, followers apply each write a hundred milliseconds "
            "after the leader, on average, and the user's next read goes to any of three replicas. "
            "<bookmark mark='b'/> Reading at once, two reads in three miss the write. After a hundred "
            "milliseconds, about one in four; after half a second, one in two hundred. "
            "<bookmark mark='c'/> Two fixes are common. For a short while after a user writes, send that user's "
            "reads to the leader. <bookmark mark='d'/> Or have the write return its position in the log, and "
            "read only from a replica that has reached it."
        ) as vo:
            self.play(FadeIn(head), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(vals))
            vo.wait_until("c")
            self.play(FadeIn(fixes[0]), FadeIn(fixes[1]))
            vo.wait_until("d")
            self.play(FadeIn(fixes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ failover
    def failover(self):
        d = load39("detect")
        fx = {r["timeout_ms"]: r for r in d["fixed"]}
        head = label(r"Failover", font_size=36).to_edge(UP, buff=0.3)
        shown = (150, 200, 300, 1000, 3000)
        tab = grid_table([r"timeout", r"false alarms / hour", r"time to detect"],
                         [[f"{t} ms", f"{fx[t]['false_per_hour']:.1f}", f"{fx[t]['detect_ms']:.0f} ms"]
                          for t in shown], widths=[1.6, 2.6, 2.0], row_h=0.5, font_size=20,
                         colors=[[WHITE, NO if fx[t]["false_per_hour"] > 10 else YES,
                                  YES if fx[t]["detect_ms"] < 300 else NO] for t in shown], mono_cols=())
        tab.move_to([-3.5, 0.6, 0])
        tl = wrapped_label(rf"heartbeats every {d['interval_ms']:.0f} ms on a jittery network, \ "
                           rf"{d['hours']:.0f} simulated hours \ (Part 39)", 6.2, font_size=18,
                           color=GREY_A).next_to(tab, UP, buff=0.25).align_to(tab, LEFT)
        # promotion
        old = module_box(r"leader", KERN, w=1.6, h=0.55, font=19).move_to([2.2, 1.7, 0])
        f1 = module_box(r"follower 1", DATA, w=1.6, h=0.55, font=18).move_to([5.3, 1.7, 0])
        olog = log_strip(7, color=KERN).next_to(old, DOWN, buff=0.15)
        flog = log_strip(5).next_to(f1, DOWN, buff=0.15)
        dead = Cross(old, stroke_color=NO, stroke_width=5, scale_factor=0.7)
        new_lab = module_box(r"new leader", YES, w=1.6, h=0.55, font=18).move_to(f1)
        lost = SurroundingRectangle(olog[5:7], color=NO, buff=0.05)
        lost_l = wrapped_label(r"acknowledged, \ never shipped: \ gone", 2.6, font_size=17, color=NO).next_to(
            lost, DOWN, buff=0.12)
        clients = label(r"clients", font_size=18, color=GREY_A).move_to([3.75, 2.75, 0])
        to_old = Arrow(clients.get_bottom(), old.get_top(), buff=0.08, color=GREY_B, stroke_width=2,
                       max_tip_length_to_length_ratio=0.15)
        to_new = Arrow(clients.get_bottom(), f1.get_top(), buff=0.08, color=YES, stroke_width=2,
                       max_tip_length_to_length_ratio=0.15)
        notes = VGroup(
            wrapped_label(r"\textbf{asynchronous}: \ the unshipped tail is lost on promotion", 5.4, font_size=19,
                          color=NO),
            wrapped_label(r"\textbf{semi-synchronous}: \ wait for one follower to confirm each write; \ nothing "
                          r"acknowledged is lost, \ for a round trip per write", 5.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.8, -1.75, 0])
        with self.voiceover(
            "When the leader dies, a follower must take over, and the first problem is knowing that it died. "
            "<bookmark mark='a'/> Followers expect a heartbeat, here every hundred milliseconds, and suspect the "
            "leader after a timeout. Part 39 measured the trade on a jittery network. A timeout of a hundred and "
            "fifty milliseconds notices a crash in about a tenth of a second, but raises two hundred and fifty "
            "false alarms an hour; three hundred milliseconds, about three; three seconds, none. "
            "<bookmark mark='b'/> Then the most up-to-date follower is promoted, and clients are redirected. "
            "<bookmark mark='c'/> With asynchronous replication, writes the old leader acknowledged but never "
            "shipped are simply gone. <bookmark mark='d'/> Semi-synchronous replication waits for one follower to "
            "confirm each write, and loses nothing acknowledged, at the cost of a round trip."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old), FadeIn(f1), FadeIn(olog), FadeIn(flog), FadeIn(clients),
                      GrowArrow(to_old))
            vo.wait_until("a")
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r), shift=RIGHT * 0.15) for r in tab.cells[1:]], lag_ratio=0.4),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(Create(dead), FadeOut(to_old))
            self.play(Transform(f1, new_lab), GrowArrow(to_new))
            vo.wait_until("c")
            self.play(Create(lost), FadeIn(lost_l), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ split brain and fencing
    def fencing(self):
        head = label(r"Split brain and fencing tokens", font_size=36).to_edge(UP, buff=0.3)
        lanes = {"A": 2.05, "lock": 1.05, "B": 0.05, "store": -0.95}
        names = {"A": (r"leader A", KERN), "lock": (r"lock service", LAM), "B": (r"leader B", DATA),
                 "store": (r"storage", YES)}
        x0, x1 = -4.3, 6.6
        lane = VGroup()
        for k, y in lanes.items():
            t, c = names[k]
            lane.add(VGroup(label(t, font_size=19, color=c).move_to([-5.6, y, 0]),
                            Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=1.5)))

        def msg(xa, a, xb, b, text, color, side=UP):
            ar = Arrow([xa, lanes[a], 0], [xb, lanes[b], 0], buff=0.05, color=color, stroke_width=2.2,
                       max_tip_length_to_length_ratio=0.1)
            t = label(text, font_size=17, color=color).next_to(ar.get_center(), side, buff=0.08).shift(RIGHT * 0.45)
            return VGroup(ar, t)
        grant_a = msg(-4.1, "lock", -3.8, "A", r"lease, \ token 33", LAM)
        write_a = msg(-3.3, "A", -2.8, "store", r"write, \ 33", KERN, side=RIGHT)
        pause = VGroup(Rectangle(width=5.4, height=0.3, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
                       .move_to([-0.1, lanes["A"], 0]))
        pause.add(label(r"paused: \ a long garbage collection", font_size=17, color=WHITE).move_to(pause[0]))
        expire = VGroup(Line([-1.0, lanes["lock"] - 0.2, 0], [-1.0, lanes["lock"] + 0.2, 0], color=NO,
                             stroke_width=3),
                        label(r"lease expires", font_size=17, color=NO).move_to([-1.0, lanes["lock"] + 0.38, 0]))
        grant_b = msg(-0.4, "lock", 0.0, "B", r"token 34", LAM)
        write_b = msg(0.7, "B", 1.1, "store", r"write, \ 34", DATA, side=RIGHT)
        seen = label(r"largest token seen: \ 34", font_size=18, color=YES).move_to([2.6, lanes["store"] - 0.45, 0])
        write_a2 = msg(3.4, "A", 4.6, "store", r"write, \ 33", KERN, side=RIGHT)
        rej = Cross(scale_factor=0.16, stroke_color=NO, stroke_width=5).move_to([4.6, lanes["store"], 0])
        rej_l = label(r"rejected: \ 33 $<$ 34", font_size=18, color=NO).next_to(rej, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"two nodes both believe they lead: \ \textbf{split brain}", 12.6, font_size=20,
                          color=NO),
            wrapped_label(r"fencing \ (Part 38): \ every write carries its lease's number, \ and the storage itself "
                          r"refuses any number smaller than the largest it has seen; \ a paused node cannot be "
                          r"trusted to check its own clock", 12.6, font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.55)
        foot = note(r"illustrative", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "The dangerous failure is a leader that is not dead, only paused. <bookmark mark='a'/> Leader A holds "
            "a lease, numbered thirty-three, and writes under it. Then it stalls, perhaps in a long garbage "
            "collection, and its lease runs out. <bookmark mark='b'/> The lock service grants a new lease to B, "
            "numbered thirty-four, and B starts writing. <bookmark mark='c'/> Then A wakes, still believing it "
            "leads, and writes too: two leaders, split brain. <bookmark mark='d'/> Part 38's fencing tokens stop "
            "it. Every write carries its lease number, and the storage remembers the largest it has seen, so it "
            "rejects thirty-three after thirty-four. The check must live in the storage: a paused leader cannot "
            "be trusted to check its own clock."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lane), FadeIn(foot))
            vo.wait_until("a")
            self.play(GrowArrow(grant_a[0]), FadeIn(grant_a[1]))
            self.play(GrowArrow(write_a[0]), FadeIn(write_a[1]))
            self.play(GrowFromEdge(pause[0], LEFT), FadeIn(pause[1]), run_time=1.5)
            self.play(FadeIn(expire))
            vo.wait_until("b")
            self.play(GrowArrow(grant_b[0]), FadeIn(grant_b[1]))
            self.play(GrowArrow(write_b[0]), FadeIn(write_b[1]), FadeIn(seen))
            vo.wait_until("c")
            self.play(GrowArrow(write_a2[0]), FadeIn(write_a2[1]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(Create(rej), FadeIn(rej_l))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ active-active
    def active(self):
        w = load39("lww")
        R = {r["skew_ms"]: r for r in w["rows"]}
        head = label(r"Active--active across regions", font_size=36).to_edge(UP, buff=0.3)
        eu = module_box(r"leader, \ Europe", KERN, w=2.2, h=0.6, font=18).move_to([-5.2, 1.9, 0])
        us = module_box(r"leader, \ America", DATA, w=2.2, h=0.6, font=18).move_to([-1.6, 1.9, 0])
        link = DoubleArrow(eu.get_right(), us.get_left(), buff=0.08, color=GREY_B, stroke_width=2,
                           max_tip_length_to_length_ratio=0.12)
        ll = label(rf"{w['delta_ms']:.0f} ms", font_size=17, color=GREY_B).next_to(link, UP, buff=0.08)
        wa = label(r"\texttt{x = 1}", font_size=20, color=KERN).next_to(eu, DOWN, buff=0.3)
        wb = label(r"\texttt{x = 2}", font_size=20, color=DATA).next_to(us, DOWN, buff=0.3)
        cross = VGroup(Arrow(wa.get_right(), [us.get_x() - 0.6, wb.get_y() - 0.75, 0], buff=0.1, color=KERN,
                             stroke_width=2, max_tip_length_to_length_ratio=0.1),
                       Arrow(wb.get_left(), [eu.get_x() + 0.6, wa.get_y() - 0.75, 0], buff=0.1, color=DATA,
                             stroke_width=2, max_tip_length_to_length_ratio=0.1))
        lww = VGroup(label(r"last writer wins:", font_size=19, color=NO), label(r"\texttt{x = 2}", font_size=20,
                                                                                 color=DATA),
                     label(r"\texttt{x = 1} \ discarded", font_size=19, color=NO)).arrange(RIGHT, buff=0.25)
        vv = VGroup(label(r"version vectors:", font_size=19, color=YES),
                    label(r"siblings \ \{\texttt{1}, \ \texttt{2}\}: \ merge them", font_size=19, color=YES)).arrange(
            RIGHT, buff=0.25)
        VGroup(lww, vv).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, -1.0, 0])
        shown = (0, 100, 250)
        tab = grid_table([r"clock skew", r"concurrent", r"lost by LWW", r"lost by VV"],
                         [[f"{s} ms", rf"{100 * R[s]['concurrent']:.1f}\%", rf"{100 * R[s]['lww_lost']:.1f}\%",
                           rf"{100 * R[s]['vv_lost']:.0f}\%"] for s in shown],
                         widths=[1.5, 1.6, 1.7, 1.5], row_h=0.5, font_size=19,
                         colors=[[WHITE, HEAD, NO, YES]] * 3, mono_cols=())
        tab.move_to([3.6, 1.0, 0])
        tl = wrapped_label(rf"Part 39: \ two regions, \ each writing one key {w['rate']:.0f} times a second; \ "
                           r"skew: \ America's clock fast by", 6.2, font_size=18, color=GREY_A).next_to(
            tab, UP, buff=0.25).align_to(tab, LEFT)
        notes = VGroup(
            wrapped_label(r"LWW drops half of every concurrent pair; \ with skew it also drops writes that had "
                          r"\textit{seen} the one it keeps", 6.2, font_size=19, color=NO),
            wrapped_label(r"version vectors keep both, \ for the application or a CRDT \ (Part 39) \ to merge",
                          6.2, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Finally, leaders in several regions, each accepting writes locally: active-active. Writes are fast "
            "everywhere, but two regions can change the same record before hearing of each other. "
            "<bookmark mark='a'/> Part 39 simulated it: two regions, each writing one key five times a second, "
            "fifty milliseconds apart. A fifth of all writes were concurrent with one from the other region. "
            "<bookmark mark='b'/> Last writer wins keeps the larger timestamp and silently discards the other: "
            "nearly ten percent of writes lost, with perfect clocks. <bookmark mark='c'/> With one clock a hundred "
            "milliseconds fast, it also discards writes that had seen the one it keeps: about sixteen percent "
            "lost; at a quarter of a second, twenty-three. <bookmark mark='d'/> Version vectors lose nothing. "
            "They hand both versions back, to be merged by a rule, or by a CRDT."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eu), FadeIn(us), GrowFromCenter(link), FadeIn(ll))
            vo.wait_until("a")
            self.play(FadeIn(wa), FadeIn(wb))
            self.play(GrowArrow(cross[0]), GrowArrow(cross[1]))
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(tab.cells[1][1]),
                      FadeIn(tab.cells[1][0]))
            vo.wait_until("b")
            self.play(FadeIn(lww), FadeIn(tab.cells[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[2][:3])), FadeIn(VGroup(*tab.cells[3][:3])), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(vv), FadeIn(VGroup(tab.cells[1][3], tab.cells[2][3], tab.cells[3][3])),
                      FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD, LAM, load)
